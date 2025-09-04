import os
import time

def monitor_container(pid, duration=10):
    print(f"[+] Monitoring container with PID {pid}...")

    for _ in range(duration):
        try:
            with open(f"/proc/{pid}/status") as f:
                lines = f.readlines()
                vmrss = next((line for line in lines if "VmRSS" in line), "VmRSS:\t0 kB")
                print(f"[Monitor] {vmrss.strip()}")
        except FileNotFoundError:
            print("[-] Process not found")
            break
        time.sleep(1)
