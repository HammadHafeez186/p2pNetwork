import socket
import os
import time

def request_chunk_from_peer(ip, port, filename, save_dir):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(10)  # Increased timeout to 10 seconds
            print(f"[PEER CLIENT] Connecting to {ip}:{port} for {filename}")
            s.connect((ip, port))
            
            # Send filename
            s.sendall(filename.encode())
            print(f"[PEER CLIENT] Requested {filename}")

            # Receive file data
            data = b''
            start_time = time.time()
            while True:
                try:
                    chunk = s.recv(4096)
                    if not chunk:
                        break
                    data += chunk
                    
                    # Check for timeout
                    if time.time() - start_time > 30:  # 30 second total timeout
                        print(f"[PEER CLIENT] Timeout receiving {filename}")
                        return False
                        
                except socket.timeout:
                    print(f"[PEER CLIENT] Timeout receiving {filename}")
                    return False

        if data == b"NOT_FOUND":
            print(f"[PEER CLIENT] {filename} not found on peer {ip}:{port}")
            return False

        # Save the file
        os.makedirs(save_dir, exist_ok=True)
        file_path = os.path.join(save_dir, filename)
        with open(file_path, "wb") as f:
            f.write(data)

        print(f"[PEER CLIENT] Received {filename} from {ip}:{port} ({len(data)} bytes)")
        return True

    except socket.timeout:
        print(f"[PEER CLIENT] Connection timeout to {ip}:{port}")
        return False
    except ConnectionRefusedError:
        print(f"[PEER CLIENT] Connection refused by {ip}:{port}")
        return False
    except Exception as e:
        print(f"[PEER CLIENT] Failed to get {filename} from {ip}:{port} — {e}")
        return False
