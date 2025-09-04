import ctypes
import os

# Clone flags
CLONE_NEWUTS = 0x04000000  # Hostname
CLONE_NEWPID = 0x20000000  # Process ID
CLONE_NEWNS  = 0x00020000  # Mount
CLONE_NEWNET = 0x40000000  # Network
CLONE_NEWUSER = 0x10000000  # User

def setup_namespaces():
    print("[+] Setting up namespaces...")
    libc = ctypes.CDLL("libc.so.6")
    flags = CLONE_NEWUTS | CLONE_NEWUSER | CLONE_NEWPID | CLONE_NEWNS | CLONE_NEWNET
    if libc.unshare(flags) != 0:
        raise RuntimeError("[-] unshare() failed")
#    os.sethostname(f"container-{os.getpid()}".encode())
