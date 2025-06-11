# peer/peer_client.py

import socket
import os

CHUNK_SIZE = 1024

def request_file_from_peer(peer_ip, peer_port, file_name, download_dir):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((peer_ip, peer_port))
        s.sendall(file_name.encode())

        status = s.recv(1024).decode()
        if status != "OK":
            print(f"[ERROR] {status}")
            return False

        os.makedirs(download_dir, exist_ok=True)
        file_path = os.path.join(download_dir, file_name)

        with open(file_path, 'wb') as f:
            while True:
                data = s.recv(CHUNK_SIZE)
                if not data:
                    break
                f.write(data)

        print(f"[INFO] File '{file_name}' downloaded successfully to '{download_dir}'")
        return True

    except Exception as e:
        print(f"[ERROR] Failed to download file: {e}")
        return False
    finally:
        s.close()
