import argparse
from core.container import Container
from core.monitor import monitor_container
from core.cgroups import freeze_container, unfreeze_container
import time

# ساخت یک دیکشنری برای ذخیره‌ی کانتینرها
containers = {}

def main():
    parser = argparse.ArgumentParser(description="Simple Daemonless Container Runtime")
    
    parser.add_argument("command", choices=[
        "run", "list", "monitor", "freeze", "resume", "delete"
    ], help="Command to run")
    
    parser.add_argument("--image", help="Path to rootfs image (tar.gz)")
    parser.add_argument("--id", help="Container ID to manage")

    args = parser.parse_args()

    if args.command == "run":
        if not args.image:
            print("[-] Please provide --image path")
            return
        container = Container(args.image)
        container.run()
        containers[container.container_id] = container

    elif args.command == "list":
        if not containers:
            print("[-] No containers found.")
        else:
            print("Running containers:")
            for cid, c in containers.items():
                print(f"{cid} - status: {c.status} - pid: {c.pid}")

    elif args.command == "monitor":
        if not args.id:
            print("[-] Please provide --id")
            return
        container = containers.get(args.id)
        if container:
            monitor_container(container.pid)
        else:
            print("[-] Container not found")

    elif args.command == "freeze":
        if not args.id:
            print("[-] Please provide --id")
            return
        freeze_container(args.id)

    elif args.command == "resume":
        if not args.id:
            print("[-] Please provide --id")
            return
        unfreeze_container(args.id)

    elif args.command == "delete":
        if not args.id:
            print("[-] Please provide --id")
            return
        container = containers.get(args.id)
        if container:
            container.delete()
            del containers[args.id]
        else:
            print("[-] Container not found")

if __name__ == "__main__":
    main()
