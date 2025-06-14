import threading, os, sys
import time

# Ensure we can import from parent
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tracker_client import authenticate_with_tracker, register_with_tracker, get_peers_with_file
from peer_server import start_peer_server
from file_utils import split_file_to_chunks, count_parts
from peer_utils import download_file

# --- Hardcoded Configuration ---
tracker_ip = "127.0.0.1"       # <- Change this to your tracker machine's LAN IP
tracker_port = 9000

peer_id = "peer1"
peer_port = 5001

shared_dir = "./shared"
download_dir = "./downloads"
chunks_dir = os.path.join(download_dir, "chunks")
target_files = ["Notes.txt"]

# --- Setup Directories ---
os.makedirs(shared_dir, exist_ok=True)
os.makedirs(download_dir, exist_ok=True)
os.makedirs(chunks_dir, exist_ok=True)

# --- Prepare Shared Files ---
shared_files = {}
for fname in os.listdir(shared_dir):
    fpath = os.path.join(shared_dir, fname)
    if os.path.isfile(fpath):
        split_file_to_chunks(fpath, chunks_dir)
        shared_files[fname] = count_parts(chunks_dir, fname)

# --- Filter Download Targets ---
target_files = [f for f in target_files if f not in shared_files]
print(f"[INFO] {peer_id} sharing: {shared_files}")
print(f"[INFO] Will download: {target_files}")

# --- Authenticate and Register ---
token = authenticate_with_tracker(tracker_ip, tracker_port, peer_id)
if not token:
    print("[FATAL] Authentication failed.")
    exit(1)

resp = register_with_tracker(tracker_ip, tracker_port, peer_id, token, peer_port, shared_files)
print(f"[TRACKER] {resp}")

# --- Start Peer Server ---
threading.Thread(target=start_peer_server, args=(peer_port, shared_dir, chunks_dir), daemon=True).start()

# --- Download Target Files ---
threads = []
for filename in target_files:
    t = threading.Thread(
        target=download_file,
        args=(filename, peer_id, tracker_ip, tracker_port, token, chunks_dir, download_dir, get_peers_with_file)
    )
    t.start()
    threads.append(t)

for t in threads:
    t.join()

input("[EXIT] Press Enter to close.\n")
