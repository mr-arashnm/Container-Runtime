# Container Runtime Simulator

## Overview
This project is a Python-based container runtime simulator designed for educational purposes. It demonstrates key operating system concepts such as namespaces, cgroups, chroot, and process isolation. The simulator provides a command-line interface (CLI) to manage containers with resource constraints and isolated environments.

---

## Features
- **Namespace Isolation**: UTS, PID, mount, and network namespaces.
- **Resource Control**: Memory and CPU limits using cgroups.
- **Filesystem Isolation**: Restricts access with `chroot`.
- **CLI Interface**: Manage containers with commands like `run`, `list`, `monitor`, `freeze`, `resume`, and `delete`.

---

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/container-runtime-simulator.git
   cd container-runtime-simulator
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   sudo python3 run.py
   ```

---

## Usage
### Commands
- **Run a container**:
  ```bash
  container run --memory=64m --cpu=1 bash
  ```
  Starts a container with 64MB memory and 1 CPU core, running the `bash` shell.

- **List active containers**:
  ```bash
  container list
  ```
  Displays all currently running containers.

- **Monitor a container**:
  ```bash
  container monitor --id <container_id>
  ```
  Monitors the resource usage of a specific container.

- **Freeze a container**:
  ```bash
  container freeze --id <container_id>
  ```
  Pauses the execution of a container.

- **Resume a container**:
  ```bash
  container resume --id <container_id>
  ```
  Resumes the execution of a paused container.

- **Delete a container**:
  ```bash
  container delete --id <container_id>
  ```
  Stops and removes a container.

---

## Limitations
- Requires root privileges.
- Simplified implementation for learning purposes, not suitable for production.

---

## License
This project is licensed under the MIT License.

---

## Contributing
Contributions are welcome! Fork the repository and submit a pull request.
