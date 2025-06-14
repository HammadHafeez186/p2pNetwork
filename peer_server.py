import socket
import threading
import os

def handle_peer(conn, shared_dir, chunks_dir):
    try:
        filename = conn.recv(1024).decode().strip()
        found = False
        for directory in [chunks_dir, shared_dir]:
            path = os.path.join(directory, filename)
            if os.path.isfile(path):
                with open(path, "rb") as f:
                    conn.sendall(f.read())
                found = True
                break
        if not found:
            conn.send(b"NOT_FOUND")
    except Exception as e:
        print(f"[SERVER ERROR] {e}")
    finally:
        conn.close()

def start_peer_server(port, shared_dir, chunks_dir):
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(("0.0.0.0", port))  # Bind to all interfaces (LAN/Wi-Fi compatible)
        server_socket.listen()
        print(f"[PEER SERVER] Listening on port {port}")
        while True:
            conn, _ = server_socket.accept()
            threading.Thread(target=handle_peer, args=(conn, shared_dir, chunks_dir), daemon=True).start()
    except Exception as e:
        print(f"[PEER SERVER ERROR] {e}")
