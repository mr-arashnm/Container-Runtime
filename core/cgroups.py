import os
import time
from typing import Union

CGROUP_BASE = "/sys/fs/cgroup"
CGROUP_SUBSYS = "mycontainers"  # نام زیرسیستم اختصاصی

def write_file(path: str, value: Union[str, int], retries: int = 3) -> None:
    """تابع ایمن برای نوشتن در فایل‌های cgroup با قابلیت تکرار"""
    for attempt in range(retries):
        try:
            # Use 'open' with 'w' mode, but escalate if permission denied
            with open(path, 'w') as f:
                f.write(str(value))
            return
        except PermissionError as e:
            print(f"[-] Permission denied when writing to {path}. Are you running as root?")
            # Print extra info for debugging
            print(f"    UID: {os.geteuid()}, GID: {os.getegid()}")
            print(f"    Path owner: {get_owner(path)}")
            raise
        except IOError as e:
            raise RuntimeError(f"Failed to write to {path}: {str(e)}")

def get_owner(path):
    try:
        stat = os.stat(os.path.dirname(path))
        import pwd, grp
        return f"{pwd.getpwuid(stat.st_uid).pw_name}:{grp.getgrgid(stat.st_gid).gr_name}"
    except Exception:
        return "unknown"

def setup_cgroup_v2() -> None:
    """بررسی و آماده‌سازی cgroup v2"""
    if not os.path.exists(CGROUP_BASE):
        raise RuntimeError("Cgroups v2 not mounted at /sys/fs/cgroup")
    
    # ایجاد دایرکتوری والد اگر وجود نداشته باشد
    os.makedirs(f"{CGROUP_BASE}/{CGROUP_SUBSYS}", mode=0o755, exist_ok=True)

def apply_cgroup_limits(container_id: str, 
                      memory_limit_mb: int = 50,
                      cpu_shares: int = 25) -> None:
    """اعمال محدودیت‌های منابع برای کانتینر"""
    print("[+] Applying cgroup limits...")

    # Check for root privileges
    if os.geteuid() != 0:
        raise PermissionError("You must run this program as root to modify cgroup files.")

    cgroup_path = f"{CGROUP_BASE}/{CGROUP_SUBSYS}/{container_id}"

    try:
        os.makedirs(cgroup_path, mode=0o755, exist_ok=True)
        # Check if cgroup v2 is mounted and writable
        if not os.access(cgroup_path, os.W_OK):
            raise PermissionError(f"Cannot write to {cgroup_path}. Check cgroup mount options and permissions.")
        write_file(f"{cgroup_path}/memory.max", f"{memory_limit_mb}M")
        write_file(f"{cgroup_path}/cpu.max", f"{cpu_shares * 1000} 100000")
        controllers = ["memory", "cpu"]
        # Only try to write subtree_control if it exists (for parent cgroups)
        subtree_control = f"{cgroup_path}/cgroup.subtree_control"
        if os.path.exists(subtree_control):
            write_file(subtree_control, f"+{' +'.join(controllers)}")
        print(f"[+] Cgroup limits applied at {cgroup_path}")
    except Exception as e:
        print(f"[-] Failed to apply cgroup limits: {str(e)}")
        print("[!] Troubleshooting tips:")
        print("    - Make sure you are running as root (sudo).")
        print("    - Make sure /sys/fs/cgroup is mounted as cgroup2 (single unified hierarchy).")
        print("    - Check if your kernel supports cgroup v2 and is not in hybrid mode.")
        print("    - Try: mount | grep cgroup")
        print("    - Try: ls -ld /sys/fs/cgroup /sys/fs/cgroup/mycontainers")
        raise

def add_process_to_cgroup(container_id: str, pid: int = None) -> None:
    """اضافه کردن یک پردازه به cgroup"""
    pid = pid or os.getpid()
    cgroup_path = f"{CGROUP_BASE}/{CGROUP_SUBSYS}/{container_id}"
    write_file(f"{cgroup_path}/cgroup.procs", str(pid))

def freeze_container(container_id: str) -> None:
    """توقف موقت تمام پردازه‌های کانتینر"""
    cgroup_path = f"{CGROUP_BASE}/{CGROUP_SUBSYS}/{container_id}"
    write_file(f"{cgroup_path}/cgroup.freeze", 1)
    print(f"[+] Container {container_id} frozen")

def unfreeze_container(container_id: str) -> None:
    """ادامه اجرای پردازه‌های کانتینر"""
    cgroup_path = f"{CGROUP_BASE}/{CGROUP_SUBSYS}/{container_id}"
    write_file(f"{cgroup_path}/cgroup.freeze", 0)
    print(f"[+] Container {container_id} resumed")

def cleanup_cgroup(container_id: str) -> None:
    """پاکسازی cgroup بعد از اتمام کار"""
    cgroup_path = f"{CGROUP_BASE}/{CGROUP_SUBSYS}/{container_id}"
    try:
        # ابتدا مطمئن شوید هیچ پردازه‌ای در cgroup نیست
        with open(f"{cgroup_path}/cgroup.procs", 'r') as f:
            procs = f.read().strip()
            if procs:
                raise RuntimeError(f"Cgroup not empty, processes: {procs}")
        
        os.rmdir(cgroup_path)
        print(f"[+] Cgroup {container_id} cleaned up")
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"[-] Failed to cleanup cgroup: {str(e)}")
        raise