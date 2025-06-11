# peer/peer_server.py

import socket
import threading
import os

ALLOWED_EXTENSIONS = ('.pdf', '.txt', '.jpg')
CHUNK_SIZE = 1024

def handle_client(conn, addr, shared_dir):
    try:
        file_name = conn.recv(1024).decode().strip()
        file_path = os.path.join(shared_dir, file_name)

        if not os.path.isfile(file_path) or not file_name.endswith(ALLOWED_EXTENSIONS):
            conn.sendall(b"ERROR: File not found or unsupported format.")
            return

        conn.sendall(b"OK")

        with open(file_path, 'rb') as f:
            while chunk := f.read(CHUNK_SIZE):
                conn.sendall(chunk)
    except Exception as e:
        print(f"[ERROR] During file transfer: {e}")
    finally:
        conn.close()

def start_peer_server(peer_port, shared_dir):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', peer_port))  # Listen on all interfaces (localhost/LAN)
    server.listen()
    print(f"[PEER SERVER] Listening on port {peer_port} for file requests...")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr, shared_dir), daemon=True)
        thread.start()
