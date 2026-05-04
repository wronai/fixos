"""Security diagnostic plugin — firewall, ports, SELinux, SSH, fail2ban."""

from __future__ import annotations

from fixos.plugins.base import DiagnosticPlugin, DiagnosticResult, Finding, Severity
from fixos.platform_utils import run_command


class Plugin(DiagnosticPlugin):
    name = "security"
    description = "Diagnostyka bezpieczeństwa (firewall, porty, SELinux, SSH)"
    platforms = ["linux"]

    def _selinux_findings(self, selinux: dict) -> list:
        """Return findings for SELinux status."""
        status = selinux.get("status")
        if status == "disabled":
            return [Finding(
                title="SELinux wyłączony",
                severity=Severity.WARNING,
                description="SELinux jest wyłączony — brak obowiązkowej kontroli dostępu.",
                suggestion="Rozważ włączenie SELinux w trybie enforcing.",
            )]
        if status == "permissive":
            return [Finding(
                title="SELinux w trybie permissive",
                severity=Severity.INFO,
                description="SELinux loguje naruszenia ale ich nie blokuje.",
            )]
        return []

    def _fail2ban_findings(self, f2b: dict) -> list:
        """Return findings for fail2ban status."""
        if not f2b.get("installed"):
            return [Finding(
                title="Fail2ban nie zainstalowany",
                severity=Severity.INFO,
                description="Fail2ban chroni przed atakami brute-force na SSH.",
                suggestion="Zainstaluj fail2ban.",
                command="sudo dnf install -y fail2ban",
            )]
        if not f2b.get("active"):
            return [Finding(
                title="Fail2ban nieaktywny",
                severity=Severity.WARNING,
                description="Fail2ban jest zainstalowany ale nie działa.",
                command="sudo systemctl enable --now fail2ban",
            )]
        return []

    def _overall_status(self, findings: list):
        """Derive overall severity from findings list."""
        if any(f.severity == Severity.CRITICAL for f in findings):
            return Severity.CRITICAL
        if any(f.severity == Severity.WARNING for f in findings):
            return Severity.WARNING
        return Severity.OK

    def diagnose(self) -> DiagnosticResult:
        findings = []
        raw_data = {}

        # Firewall
        fw = self._check_firewall()
        raw_data["firewall"] = fw
        if not fw.get("active"):
            findings.append(Finding(
                title="Firewall nieaktywny",
                severity=Severity.CRITICAL,
                description="Żaden firewall nie jest aktywny (firewalld/ufw/iptables).",
                suggestion="Włącz firewall dla ochrony systemu.",
                command="sudo systemctl enable --now firewalld",
            ))

        # SELinux
        selinux = self._check_selinux()
        raw_data["selinux"] = selinux
        findings.extend(self._selinux_findings(selinux))

        # Open ports
        ports = self._check_open_ports()
        raw_data["open_ports"] = ports
        risky_ports = [p for p in ports.get("ports", []) if p.get("risky")]
        if risky_ports:
            findings.append(Finding(
                title=f"{len(risky_ports)} ryzykownych otwartych portów",
                severity=Severity.WARNING,
                description=f"Otwarte porty: {', '.join(str(p['port']) for p in risky_ports)}",
                suggestion="Sprawdź czy te usługi powinny być dostępne z zewnątrz.",
            ))

        # SSH config
        ssh = self._check_ssh()
        raw_data["ssh"] = ssh
        if ssh.get("root_login") == "yes":
            findings.append(Finding(
                title="SSH pozwala na logowanie root",
                severity=Severity.WARNING,
                description="PermitRootLogin jest ustawione na 'yes' w sshd_config.",
                suggestion="Ustaw PermitRootLogin na 'no' lub 'prohibit-password'.",
                command="sudo sed -i 's/^PermitRootLogin yes/PermitRootLogin prohibit-password/' /etc/ssh/sshd_config",
            ))
        if ssh.get("password_auth") == "yes":
            findings.append(Finding(
                title="SSH pozwala na logowanie hasłem",
                severity=Severity.INFO,
                description="Logowanie przez hasło jest włączone — rozważ klucze SSH.",
            ))

        # Fail2ban
        f2b = self._check_fail2ban()
        raw_data["fail2ban"] = f2b
        findings.extend(self._fail2ban_findings(f2b))

        return DiagnosticResult(
            plugin_name=self.name,
            status=self._overall_status(findings),
            findings=findings,
            raw_data=raw_data,
        )

    def _check_firewall(self) -> dict:
        # firewalld
        ok, stdout, _, _ = run_command("systemctl is-active firewalld 2>/dev/null", timeout=5)
        if ok and "active" in stdout:
            return {"active": True, "type": "firewalld"}
        # ufw
        ok2, stdout2, _, _ = run_command("ufw status 2>/dev/null", timeout=5)
        if ok2 and "active" in stdout2.lower():
            return {"active": True, "type": "ufw"}
        # iptables (check for non-default rules)
        ok3, stdout3, _, _ = run_command("iptables -L -n 2>/dev/null | wc -l", timeout=5)
        if ok3 and stdout3.strip().isdigit() and int(stdout3.strip()) > 8:
            return {"active": True, "type": "iptables"}
        return {"active": False, "type": None}

    def _check_selinux(self) -> dict:
        ok, stdout, _, _ = run_command("getenforce 2>/dev/null", timeout=5)
        if ok and stdout.strip():
            status = stdout.strip().lower()
            return {"status": status}
        return {"status": "not_available"}

    def _check_open_ports(self) -> dict:
        ok, stdout, _, _ = run_command("ss -tlnp 2>/dev/null | tail -n +2", timeout=5)
        risky_ports = {21, 23, 25, 3306, 5432, 6379, 27017, 11211}
        ports = []
        if ok and stdout:
            for line in stdout.splitlines():
                parts = line.split()
                if len(parts) >= 4:
                    addr = parts[3]
                    port_str = addr.rsplit(":", 1)[-1] if ":" in addr else ""
                    if port_str.isdigit():
                        port = int(port_str)
                        ports.append({
                            "port": port,
                            "address": addr,
                            "risky": port in risky_ports,
                        })
        return {"ports": ports}

    def _check_ssh(self) -> dict:
        ok, stdout, _, _ = run_command(
            "grep -E '^(PermitRootLogin|PasswordAuthentication)' /etc/ssh/sshd_config 2>/dev/null",
            timeout=5,
        )
        result = {"root_login": "unknown", "password_auth": "unknown"}
        if ok and stdout:
            for line in stdout.splitlines():
                if "PermitRootLogin" in line:
                    result["root_login"] = line.split()[-1].lower() if line.split() else "unknown"
                if "PasswordAuthentication" in line:
                    result["password_auth"] = line.split()[-1].lower() if line.split() else "unknown"
        return result

    def _check_fail2ban(self) -> dict:
        ok, stdout, _, _ = run_command("which fail2ban-client 2>/dev/null", timeout=5)
        installed = ok and bool(stdout.strip())
        active = False
        if installed:
            ok2, stdout2, _, _ = run_command("systemctl is-active fail2ban 2>/dev/null", timeout=5)
            active = ok2 and "active" in stdout2
        return {"installed": installed, "active": active}
