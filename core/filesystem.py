import os
import tarfile
import shutil

def setup_filesystem(image_path, target_path):
    print(f"[+] Preparing filesystem for container...")

    if os.path.exists(target_path):
        print("[=] Existing filesystem found. Skipping extract.")
        return

    os.makedirs(target_path, exist_ok=True)
    with tarfile.open(image_path, "r:gz") as tar:
        tar.extractall(path=target_path)

    print("[+] Filesystem ready.")

