import socket
import json

def register_with_tracker(tracker_ip, tracker_port, peer_id, peer_port, file_list):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((tracker_ip, tracker_port))
            message = f"REGISTER|{peer_id}|{peer_port}|{json.dumps(file_list)}"
            sock.sendall(message.encode())
            return sock.recv(1024).decode()
    except Exception as e:
        return f"[ERROR] Tracker registration failed: {e}"

def get_peers_with_file(tracker_ip, tracker_port, file_name):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((tracker_ip, tracker_port))
            message = f"PEER_LIST|{file_name}"
            sock.sendall(message.encode())
            response = sock.recv(4096).decode()
            return json.loads(response)
    except Exception as e:
        print(f"[ERROR] Fetching peer list failed: {e}")
        return []
