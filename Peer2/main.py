import threading
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tracker_client import register_with_tracker, get_peers_with_file
from peer_server import start_peer_server
from peer_client import request_file_from_peer

# ===================== CONFIG =====================
tracker_ip = "127.0.0.1"
tracker_port = 9000

peer_id = "peer2"
peer_port = 5002
shared_dir = "./shared"
download_dir = "./downloads"
target_file = "notes.txt"
# ==================================================

# Ensure downloads folder exists
os.makedirs(download_dir, exist_ok=True)

# List files in shared folder
shared_files = os.listdir(shared_dir)
print(f"[INFO] Files shared by {peer_id}: {shared_files}")

# Register with tracker
response = register_with_tracker(tracker_ip, tracker_port, peer_id, peer_port, shared_files)
print(f"[INFO] Register response: {response}")

# Start peer's file server
threading.Thread(target=start_peer_server, args=(peer_port, shared_dir), daemon=True).start()
print(f"[INFO] Peer server running on port {peer_port}. Press Enter to exit...\n")

# Get peers that have the target file
peers = get_peers_with_file(tracker_ip, tracker_port, target_file)
print(f"[INFO] Tracker responded with peers for '{target_file}': {peers}")

# Filter out self
peers = [p for p in peers if p["peer_id"] != peer_id]

# Attempt file download if available
if peers:
    chosen_peer = peers[0]
    print(f"[INFO] Attempting download from: {chosen_peer}")
    success = request_file_from_peer(chosen_peer["ip"], chosen_peer["port"], target_file, download_dir)
    if success:
        print(f"[SUCCESS] File '{target_file}' downloaded to '{download_dir}'")
    else:
        print(f"[ERROR] Failed to download file from peer {chosen_peer}")
else:
    print(f"[WARN] No other peers found with '{target_file}' (excluding self)")

input()  # Keep program running
