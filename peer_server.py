import socket
import threading
import os

CHUNK_SIZE = 1024 * 1024  # 1MB

def handle_client(conn, addr, shared_dir, chunks_dir):
    try:
        file_name = conn.recv(1024).decode().strip()

        # Check shared_dir first, then chunks_dir
        file_path = os.path.join(shared_dir, file_name)
        if not os.path.isfile(file_path):
            file_path = os.path.join(chunks_dir, file_name)

        if not os.path.isfile(file_path):
            conn.sendall(b"ERROR: File not found.")
            return

        conn.sendall(b"OK")
        file_size = os.path.getsize(file_path)
        conn.sendall(str(file_size).encode())
        conn.recv(1024)

        with open(file_path, 'rb') as f:
            while chunk := f.read(CHUNK_SIZE):
                conn.sendall(chunk)

        print(f"[SENT] {file_name} to {addr}")
    except Exception as e:
        print(f"[ERROR] During transfer: {e}")
    finally:
        conn.close()

def start_peer_server(peer_port, shared_dir, chunks_dir):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', peer_port))
    server.listen()
    print(f"[PEER SERVER] Listening on port {peer_port} for file requests...")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr, shared_dir, chunks_dir), daemon=True).start()
