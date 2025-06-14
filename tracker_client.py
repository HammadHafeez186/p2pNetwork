import socket
import json

def send_request(ip, port, data):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)  # Prevents hanging if tracker is unreachable
            s.connect((ip, port))
            s.sendall(json.dumps(data).encode())
            return s.recv(8192)
    except Exception as e:
        print(f"[TRACKER ERROR] {e}")
        return b''

def authenticate_with_tracker(ip, port, peer_id):
    resp = send_request(ip, port, {"type": "AUTH", "peer_id": peer_id})
    if not resp:
        return None
    try:
        return json.loads(resp.decode())["token"]
    except Exception as e:
        print(f"[AUTH ERROR] Invalid response: {e}")
        return None

def register_with_tracker(ip, port, peer_id, token, peer_port, files):
    req = {
        "type": "REGISTER",
        "peer_id": peer_id,
        "token": token,
        "port": peer_port,
        "files": files
    }
    resp = send_request(ip, port, req)
    try:
        return json.loads(resp.decode()).get("status", "FAIL")
    except Exception as e:
        return f"[REGISTER ERROR] Invalid response: {e}"

def get_peers_with_file(ip, port, peer_id, token, file_name):
    req = {
        "type": "PEER_LIST",
        "peer_id": peer_id,
        "token": token,
        "file_name": file_name
    }
    resp = send_request(ip, port, req)
    if not resp:
        raise Exception("No response from tracker")
    try:
        data = json.loads(resp.decode())
        return data["peers"], data["total_parts"]
    except Exception as e:
        raise Exception(f"Failed to parse tracker response: {e}")
