import socket
import os

def request_chunk_from_peer(ip, port, filename, save_dir):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)  # prevent hanging if peer is unresponsive
            s.connect((ip, port))
            s.sendall(filename.encode())

            data = b''
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                data += chunk

        if data == b"NOT_FOUND":
            print(f"[PEER] {filename} not found on peer {ip}:{port}")
            return False

        os.makedirs(save_dir, exist_ok=True)
        with open(os.path.join(save_dir, filename), "wb") as f:
            f.write(data)

        print(f"[PEER] Received {filename} from {ip}:{port}")
        return True

    except Exception as e:
        print(f"[ERROR] Failed to get {filename} from {ip}:{port} — {e}")
        return False
