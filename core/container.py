import os
import subprocess
import uuid
from core.namespace import setup_namespaces
from core.filesystem import setup_filesystem
from core.cgroups import apply_cgroup_limits, add_process_to_cgroup

class Container:
    def __init__(self, image_path, container_id=None):
        self.container_id = container_id or str(uuid.uuid4())[:8]
        self.rootfs = f"./containers/container_data/{self.container_id}"
        self.image_path = image_path
        self.pid = None
        self.status = "created"

    def run(self, command=["/bin/bash"]):
        print(f"[+] Starting container {self.container_id}...")

        setup_filesystem(self.image_path, self.rootfs)
        apply_cgroup_limits(self.container_id)  # <-- Enable cgroup limits before fork

        pid = os.fork()
        if pid == 0:
            setup_namespaces()
            add_process_to_cgroup(self.container_id)  # Add child to cgroup
            os.chroot(self.rootfs)
            os.chdir("/")
            os.execvp(command[0], command)
        else:
            self.pid = pid
            self.status = "running"
            print(f"[+] Container {self.container_id} running with PID {self.pid}")

    def delete(self):
        import shutil
        if self.status == "running":
            os.kill(self.pid, 9)
        shutil.rmtree(self.rootfs, ignore_errors=True)
        print(f"[+] Container {self.container_id} deleted.")
