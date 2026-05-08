"""
Storage optimization diagnostics module.
Analyzes partition layout, resize potential, filesystem health,
and disk optimization opportunities.
"""

from typing import Any
from ._shared import _cmd, IS_LINUX, IS_WINDOWS, IS_MAC


def diagnose_storage() -> dict[str, Any]:
    """
    Diagnostyka optymalizacji dysków i partycji.
    Sprawdza:
    - Układ partycji i wolne miejsce (możliwość poszerzenia)
    - Niezaalokowana przestrzeń na dysku
    - Btrfs: balance, scrub, kompresja, snapshoty
    - LVM: wolne PE, thin pools
    - Swap: rozmiar vs RAM, zram optymalizacja
    - Filesystem health i fragmentacja
    """
    result: dict[str, Any] = {}

    if IS_LINUX:
        result.update(_diagnose_partitions())
        result.update(_diagnose_btrfs())
        result.update(_diagnose_lvm())
        result.update(_diagnose_swap_optimization())
        result.update(_diagnose_filesystem_health())

    elif IS_WINDOWS:
        result.update({
            "disk_partitions": _cmd(
                'powershell -Command "Get-Partition | Select-Object DiskNumber,'
                'PartitionNumber,Size,Type | Format-Table -AutoSize" 2>nul'
            ),
            "disk_unallocated": _cmd(
                'powershell -Command "Get-Disk | Select-Object Number,'
                'Size,AllocatedSize | Format-Table -AutoSize" 2>nul'
            ),
            "volume_info": _cmd(
                'powershell -Command "Get-Volume | Select-Object DriveLetter,'
                'FileSystemLabel,Size,SizeRemaining,FileSystem | Format-Table -AutoSize" 2>nul'
            ),
        })

    elif IS_MAC:
        result.update({
            "disk_list": _cmd("diskutil list 2>/dev/null"),
            "apfs_info": _cmd("diskutil apfs list 2>/dev/null | head -40"),
            "disk_free": _cmd("diskutil info / 2>/dev/null | grep -E '(Size|Free|Available|Used)'"),
        })

    return result


def _diagnose_partitions() -> dict[str, Any]:
    """Analyze partition layout and resize potential."""
    return {
        # Full partition table with sizes
        "partition_table": _cmd(
            "lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINT,FSUSED,FSAVAIL,FSUSE% 2>/dev/null"
        ),

        # Detailed partition info (GPT/MBR, start/end sectors)
        "partition_details": _cmd(
            "fdisk -l 2>/dev/null | head -60 || "
            "parted -l 2>/dev/null | head -60 || echo 'N/A'"
        ),

        # Unallocated space on disks
        "unallocated_space": _cmd(
            "parted -l free 2>/dev/null | grep -E '(Free Space|Disk /|Number)' || "
            "sfdisk -F 2>/dev/null || echo 'N/A'"
        ),

        # Can partitions be resized? (neighboring free space)
        "resize_potential": _cmd(
            "lsblk -b -o NAME,SIZE,TYPE,MOUNTPOINT 2>/dev/null | "
            "awk '/part/ {print $1, $2/1073741824 \"GB\", $4}'"
        ),

        # Disk model and capacity
        "disk_info": _cmd(
            "lsblk -d -o NAME,SIZE,MODEL,ROTA,TRAN 2>/dev/null"
        ),

        # Check if there are other OS partitions (dual-boot) that could be reclaimed
        "other_os_partitions": _cmd(
            "lsblk -f 2>/dev/null | grep -iE '(ntfs|fat32|exfat|hfsplus)' || echo 'Brak partycji innych OS'"
        ),

        # SMART health status
        "smart_health": _cmd(
            "smartctl -H /dev/nvme0 2>/dev/null || "
            "smartctl -H /dev/sda 2>/dev/null || echo 'smartctl niedostępny'"
        ),
    }


def _diagnose_btrfs() -> dict[str, Any]:
    """Btrfs-specific optimization checks."""
    return {
        # Check if btrfs is used
        "btrfs_filesystems": _cmd(
            "btrfs filesystem show 2>/dev/null || echo 'Btrfs nieużywany'"
        ),

        # Space usage breakdown (data, metadata, system)
        "btrfs_usage": _cmd(
            "btrfs filesystem usage / 2>/dev/null | head -30 || echo 'N/A'"
        ),

        # Compression status
        "btrfs_compression": _cmd(
            "grep -E 'btrfs.*compress' /etc/fstab 2>/dev/null || "
            "mount | grep btrfs | grep -oE 'compress=[a-z:0-9]+' || "
            "echo 'Brak kompresji btrfs (można włączyć dla oszczędności ~30%)'"
        ),

        # Compression ratio (how much space is saved)
        "btrfs_compsize": _cmd(
            "compsize / 2>/dev/null | head -5 || echo 'compsize niedostępny (dnf install compsize)'"
        ),

        # Subvolumes
        "btrfs_subvolumes": _cmd(
            "btrfs subvolume list / 2>/dev/null | head -20 || echo 'N/A'"
        ),

        # Snapshots consuming space
        "btrfs_snapshots": _cmd(
            "btrfs subvolume list -s / 2>/dev/null | head -15 || "
            "snapper list 2>/dev/null | head -15 || echo 'Brak snapshotów'"
        ),

        # Balance status (defragmentation/optimization)
        "btrfs_balance_status": _cmd(
            "btrfs balance status / 2>/dev/null || echo 'N/A'"
        ),

        # Device stats (errors)
        "btrfs_device_stats": _cmd(
            "btrfs device stats / 2>/dev/null || echo 'N/A'"
        ),
    }


def _diagnose_lvm() -> dict[str, Any]:
    """LVM resize potential."""
    return {
        # Volume groups with free space
        "lvm_vgs": _cmd(
            "vgs --noheadings -o vg_name,vg_size,vg_free 2>/dev/null || echo 'LVM nieużywany'"
        ),

        # Logical volumes
        "lvm_lvs": _cmd(
            "lvs --noheadings -o lv_name,vg_name,lv_size,data_percent 2>/dev/null || echo 'N/A'"
        ),

        # Physical volumes
        "lvm_pvs": _cmd(
            "pvs --noheadings -o pv_name,vg_name,pv_size,pv_free 2>/dev/null || echo 'N/A'"
        ),
    }


def _diagnose_swap_optimization() -> dict[str, Any]:
    """Swap and memory optimization checks."""
    return {
        # Current swap setup
        "swap_devices": _cmd("swapon --show --bytes 2>/dev/null || echo 'Brak swap'"),

        # zram configuration
        "zram_status": _cmd(
            "zramctl 2>/dev/null || echo 'zram niedostępny'"
        ),
        "zram_config": _cmd(
            "cat /etc/systemd/zram-generator.conf 2>/dev/null || "
            "cat /usr/lib/systemd/zram-generator.conf 2>/dev/null || echo 'N/A'"
        ),

        # Current swappiness
        "swappiness": _cmd("cat /proc/sys/vm/swappiness 2>/dev/null"),

        # RAM vs swap ratio
        "memory_swap_ratio": _cmd(
            "free -b 2>/dev/null | awk '"
            "NR==2 {ram=$2} NR==3 {swap=$2; "
            "if(swap>0) printf \"RAM: %.1f GB, Swap: %.1f GB, Ratio: %.1f:1\\n\", "
            "ram/1073741824, swap/1073741824, ram/swap; "
            "else print \"RAM:\", ram/1073741824, \"GB, Swap: brak\"}'"
        ),
    }


def _diagnose_filesystem_health() -> dict[str, Any]:
    """Filesystem health and optimization."""
    return {
        # Mount options (noatime, discard, etc.)
        "mount_options": _cmd(
            "mount | grep -E '^/dev' | awk '{print $1, $3, $5, $6}' 2>/dev/null"
        ),

        # fstab configuration
        "fstab": _cmd(
            "cat /etc/fstab 2>/dev/null | grep -v '^#' | grep -v '^$'"
        ),

        # TRIM/discard support (SSD optimization)
        "trim_support": _cmd(
            "systemctl status fstrim.timer 2>/dev/null | head -5 || "
            "fstrim -v / 2>/dev/null || echo 'N/A'"
        ),
        "trim_timer": _cmd(
            "systemctl is-enabled fstrim.timer 2>/dev/null || echo 'fstrim.timer nie włączony'"
        ),

        # Inode usage (can run out even with free space)
        "inode_usage": _cmd(
            "df -i / /home /boot 2>/dev/null | awk 'NR>1 {print $1, $5, $6}'"
        ),
    }
