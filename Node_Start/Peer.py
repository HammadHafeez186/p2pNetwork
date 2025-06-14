import threading, sys, os, time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tracker_client import authenticate_with_tracker, register_with_tracker, get_peers_with_file
from peer_server import start_peer_server
from peer_client import request_chunk_from_peer
from file_utils import split_file_to_chunks, count_parts, join_chunks_to_file
from peer_utils import delete_parts, download_file

# ==== Hardcoded Configuration ====
tracker_ip, tracker_port = "192.168.1.100", 9000  # Replace with your tracker machine's LAN IP
peer_id, peer_port = "peer1", 5001

shared_dir = "./shared"
download_dir = "./downloads"
chunks_dir = os.path.join(download_dir, "chunks")
target_files = ["notes.txt", "img.jpg"]

# ==== Create Folders ====
os.makedirs(shared_dir, exist_ok=True)
os.makedirs(download_dir, exist_ok=True)
os.makedirs(chunks_dir, exist_ok=True)

# ==== Prepare Shared Files ====
shared_files = {}
for fname in os.listdir(shared_dir):
    full = os.path.join(shared_dir, fname)
    if os.path.isfile(full):
        split_file_to_chunks(full, chunks_dir)
        shared_files[fname] = count_parts(chunks_dir, fname)

# ==== Filter out already owned files from download list ====
target_files = [f for f in target_files if f not in shared_files]

print(f"[INFO] {peer_id} sharing: {shared_files}")

# ==== Authenticate & Register ====
token = authenticate_with_tracker(tracker_ip, tracker_port, peer_id)
if not token:
    print("[FATAL] Authentication failed.")
    exit(1)

response = register_with_tracker(tracker_ip, tracker_port, peer_id, token, peer_port, shared_files)
print(f"[TRACKER] {response}")

# ==== Start Peer Server ====
threading.Thread(target=start_peer_server, args=(peer_port, shared_dir, chunks_dir), daemon=True).start()
print(f"[INFO] Peer server running on port {peer_port}.\n")

# ==== Download Needed Files in Threads ====
threads = []
for file in target_files:
    t = threading.Thread(target=download_file, args=(file, tracker_ip, tracker_port, peer_id, token, download_dir, chunks_dir))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

input("[EXIT] Press Enter to close...\n")
