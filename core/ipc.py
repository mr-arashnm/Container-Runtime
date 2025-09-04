import os
import socket
import threading

SOCKET_PATH = "/tmp/container_socket"

def start_ipc_server(container_id):
    if os.path.exists(SOCKET_PATH):
        os.remove(SOCKET_PATH)

    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(SOCKET_PATH)
    server.listen(5)

    print(f"[+] IPC server started at {SOCKET_PATH} for container {container_id}")

    def handle_client(client_sock):
        msg = client_sock.recv(1024).decode()
        print(f"[IPC:{container_id}] Received: {msg}")
        client_sock.send(b"ACK")
        client_sock.close()

    def server_loop():
        while True:
            client_sock, _ = server.accept()
            threading.Thread(target=handle_client, args=(client_sock,)).start()

    threading.Thread(target=server_loop, daemon=True).start()

def send_ipc_message(message):
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(SOCKET_PATH)
    sock.send(message.encode())
    print("[+] IPC message sent")
    print("[+] Response:", sock.recv(1024).decode())
    sock.close()
