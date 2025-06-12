import socket
import os

CHUNK_SIZE = 1024 * 1024  # 1MB

def request_chunk_from_peer(peer_ip, peer_port, chunk_name, chunks_dir):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((peer_ip, peer_port))
            sock.sendall(chunk_name.encode())

            response = sock.recv(1024)
            if response != b"OK":
                print(f"[WARN] {chunk_name} not available from {peer_ip}:{peer_port}")
                return False

            file_size = int(sock.recv(1024).decode())
            sock.sendall(b"ACK")

            received = 0
            chunk_path = os.path.join(chunks_dir, chunk_name)
            with open(chunk_path, 'wb') as f:
                while received < file_size:
                    data = sock.recv(min(CHUNK_SIZE, file_size - received))
                    if not data:
                        break
                    f.write(data)
                    received += len(data)

            print(f"[DOWNLOADED] {chunk_name} from {peer_ip}:{peer_port}")
            return True
    except Exception as e:
        print(f"[ERROR] {chunk_name} from {peer_ip}:{peer_port} failed: {e}")
        return False
