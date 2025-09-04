import os

def bind_process_to_core(pid, core_id=0):
    try:
        os.sched_setaffinity(pid, {core_id})
        print(f"[+] Process {pid} bound to CPU core {core_id}")
    except Exception as e:
        print("[-] Failed to bind process:", e)
