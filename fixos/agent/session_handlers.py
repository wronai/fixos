"""
Command handlers for HITL session.
Each handler processes a specific user command type.
"""

from typing import TYPE_CHECKING, Tuple

from ..platform_utils import (
    is_dangerous, elevate_cmd, run_command,
)
from ..utils.anonymizer import anonymize
from ..utils.web_search import search_all, format_results_for_llm
from . import session_io as io
from .session_core import CmdResult, DEFAULT_COMMAND_TIMEOUT, extract_fixes

if TYPE_CHECKING:
    from ..providers.llm import LLMClient
    from ..config import FixOsConfig


def handle_quit() -> bool:
    """Handle [Q] Quit command. Returns False to exit loop."""
    io.print_session_ended()
    return False


def handle_skip_all(messages: list) -> bool:
    """Handle [S] Skip all command."""
    messages.append({"role": "user",
                  "content": "Skip these fixes. What else can we check?"})
    return True


def handle_describe_problem(messages: list, ask_fn) -> bool:
    """Handle [D] Describe own problem command."""
    problem = ask_fn()
    if problem:
        messages.append({
            "role": "user",
            "content": (
                f"User describes a new problem:\n"
                f"{problem}\n\n"
                f"Analyze this problem and provide numbered list of commands to fix it."
            ),
        })
    return True


def handle_execute_all(
    fixes: list,
    messages: list,
    executed: list,
    run_cmd_fn
) -> bool:
    """Handle [A] Execute all commands."""
    if not fixes:
        io.print_no_commands()
        return True
    
    io.print_executing_all(len(fixes))
    summary_lines = []
    for cmd, comment in fixes:
        result = run_cmd_fn(cmd, comment)
        executed.append(result)
        anon_out, _ = anonymize(result.stdout + result.stderr)
        status = "✅ sukces" if result.ok else f"❌ błąd (kod {result.returncode})"
        summary_lines.append(f"- `{cmd}`: {status}")
    
    messages.append({
        "role": "user",
        "content": (
            f"Executed all commands:\n"
            f"{'\n'.join(summary_lines)}\n"
            f"\nEvaluate results and suggest next steps."
        ),
    })
    return True


def handle_fix_by_number(
    user_in: str,
    fixes: list,
    messages: list,
    executed: list,
    run_cmd_fn
) -> bool:
    """Handle [N] Execute specific fix by number."""
    idx = int(user_in) - 1
    if 0 <= idx < len(fixes):
        cmd, comment = fixes[idx]
        result = run_cmd_fn(cmd, comment)
        executed.append(result)
        anon_out, _ = anonymize(result.stdout)
        anon_err, _ = anonymize(result.stderr)
        messages.append({
            "role": "user",
            "content": (
                f"Executed: `{cmd}`\n"
                f"Success: {result.ok}\n"
                f"Stdout:\n```\n{anon_out[:800]}\n```\n"
                f"Stderr:\n```\n{anon_err[:300]}\n```\n"
                f"What next?"
            ),
        })
    else:
        io.print_invalid_option(user_in, len(fixes))
    return True


def handle_direct_command(
    user_in: str,
    messages: list,
    executed: list,
    run_cmd_fn
) -> bool:
    """Handle [!cmd] Direct command execution."""
    cmd = user_in[1:].strip()
    result = run_cmd_fn(cmd, "Komenda użytkownika")
    executed.append(result)
    anon_out, _ = anonymize(result.stdout + "\n" + result.stderr)
    messages.append({
        "role": "user",
        "content": f"User ran: `{cmd}`\nResult: {anon_out[:600]}\nWhat next?"
    })
    return True


def handle_search(
    user_in: str,
    messages: list,
    serpapi_key: str | None
) -> bool:
    """Handle [search <q>] Web search command."""
    query = user_in[7:].strip()
    results = search_all(query, serpapi_key)
    if results:
        web_ctx = format_results_for_llm(results)
        io.console.print(web_ctx)
        messages.append({
            "role": "user",
            "content": f"Search results for '{query}':\n{web_ctx}\nWhat do you think?"
        })
    else:
        io.print_no_results()
    return True


def handle_free_text(user_in: str, messages: list) -> bool:
    """Handle free text input → send to LLM."""
    messages.append({"role": "user", "content": user_in})
    return True


def run_single_command(cmd: str, comment: str) -> CmdResult:
    """Run a command with full transparency and safety checks."""
    cmd = elevate_cmd(cmd)
    danger = is_dangerous(cmd)
    if danger:
        io.print_blocked_command(cmd, danger)
        return CmdResult(cmd=cmd, comment=comment, ok=False,
                         stdout="", stderr=f"Zablokowano: {danger}", returncode=-99)
    
    io.print_cmd_preview(cmd, comment)
    ans = io.ask_execute_prompt()
    if ans in ("n", "no", "nie"):
        return CmdResult(cmd=cmd, comment=comment, ok=False,
                         stdout="", stderr="Pominięto.", returncode=-1, skipped=True)
    
    io.console.print("  [dim]⏳ Wykonuję...[/dim]", end="")
    ok, stdout, stderr, rc = run_command(cmd, timeout=DEFAULT_COMMAND_TIMEOUT)
    io.console.print("\r" + " " * 30 + "\r", end="")
    result = CmdResult(cmd=cmd, comment=comment, ok=ok,
                       stdout=stdout, stderr=stderr, returncode=rc)
    io.print_cmd_result(result)
    return result


def parse_user_input(
    user_in: str,
    fixes: list,
    messages: list,
    executed: list,
    serpapi_key: str | None
) -> Tuple[bool, bool]:
    """
    Parse user input and execute appropriate handler.
    
    Returns:
        Tuple of (should_continue, was_handled)
        - should_continue: True to continue session, False to exit
        - was_handled: True if input was handled, False if should be treated as free text
    """
    if not user_in:
        return True, True
    
    lo = user_in.lower()
    
    # [Q] Quit
    if lo in ("q", "quit", "exit", "koniec"):
        return handle_quit(), True
    
    # [D] Describe own problem
    if lo == "d":
        return handle_describe_problem(messages, io.ask_user_problem), True
    
    # [S] Skip all
    if lo in ("s", "skip", "pomiń", "pomin"):
        return handle_skip_all(messages), True
    
    # [A] Execute all
    if lo in ("a", "all", "wszystkie"):
        return handle_execute_all(fixes, messages, executed, run_single_command), True
    
    # [N] Execute specific fix by number
    if user_in.isdigit():
        return handle_fix_by_number(user_in, fixes, messages, executed, run_single_command), True
    
    # [!cmd] Direct command execution
    if user_in.startswith("!"):
        return handle_direct_command(user_in, messages, executed, run_single_command), True
    
    # [search <q>] Web search
    if lo.startswith("search "):
        return handle_search(user_in, messages, serpapi_key), True
    
    # Not handled - treat as free text
    return True, False
