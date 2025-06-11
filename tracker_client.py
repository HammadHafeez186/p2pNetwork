# peer/tracker_client.py

import socket
import json

def register_with_tracker(tracker_ip, tracker_port, peer_id, peer_port, shared_files):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((tracker_ip, tracker_port))

        files_json = json.dumps(shared_files)
        msg = f"REGISTER|{peer_id}|{peer_port}|{files_json}"
        s.sendall(msg.encode())

        response = s.recv(1024).decode()
        return response
    except Exception as e:
        print(f"[ERROR] Tracker registration failed: {e}")
        return None
    finally:
        s.close()

def get_peers_with_file(tracker_ip, tracker_port, file_name):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((tracker_ip, tracker_port))

        msg = f"PEER_LIST|{file_name}"
        s.sendall(msg.encode())

        data = s.recv(4096).decode()
        peers = json.loads(data)
        return peers
    except Exception as e:
        print(f"[ERROR] Failed to get peer list: {e}")
        return []
    finally:
        s.close()

