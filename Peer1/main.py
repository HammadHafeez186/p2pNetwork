import threading
import sys
import os
import time

# Add parent directory to path to allow imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tracker_client import register_with_tracker, get_peers_with_file
from peer_server import start_peer_server
from peer_client import request_chunk_from_peer
from file_utils import split_file_to_chunks, join_chunks_to_file

# ===================== CONFIG =====================
tracker_ip = "127.0.0.1"
tracker_port = 9000

peer_id = "peer1"  # <-- unique per peer
peer_port = 5001   # <-- unique per peer
shared_dir = "./shared"
download_dir = "./downloads"
chunks_dir = os.path.join(download_dir, "chunks")
target_files = ["notes.txt", "img.jpg"]  # Multiple files allowed
target_files = [f for f in target_files if f not in os.listdir(shared_dir)]
# ==================================================

# Setup directories
os.makedirs(shared_dir, exist_ok=True)
os.makedirs(download_dir, exist_ok=True)
os.makedirs(chunks_dir, exist_ok=True)

# Split and share own files
for filename in os.listdir(shared_dir):
    full_path = os.path.join(shared_dir, filename)
    if os.path.isfile(full_path):
        print(f"[INFO] Splitting '{filename}' into chunks...")
        split_file_to_chunks(full_path, chunks_dir, chunk_size_kb=64)

shared_files = list(set(os.listdir(shared_dir) + os.listdir(chunks_dir)))
print(f"[INFO] Files shared by {peer_id}: {shared_files}")

# Register with tracker
response = register_with_tracker(tracker_ip, tracker_port, peer_id, peer_port, shared_files)
print(f"[INFO] Register response: {response}")

# Start peer server thread
threading.Thread(target=start_peer_server, args=(peer_port, shared_dir, chunks_dir), daemon=True).start()
print(f"[INFO] Peer server running on port {peer_port}...\n")

# === Persistent File Download ===
def download_file(target_file):
    downloaded_parts = set()
    retry_delay = 5  # seconds

    print(f"[START] Downloading '{target_file}' (press Ctrl+C to abort)...")

    while True:
        peers = get_peers_with_file(tracker_ip, tracker_port, target_file)
        peers = [p for p in peers if p["peer_id"] != peer_id]

        if not peers:
            print(f"[WAIT] No peers with '{target_file}' found. Retrying in {retry_delay}s...")
            time.sleep(retry_delay)
            continue

        part_num = 0
        while True:
            part_name = f"{target_file}.part{part_num}"
            if part_name in downloaded_parts:
                part_num += 1
                continue

            print(f"[TRYING] Requesting {part_name} from peers...")
            success = False
            for peer in peers:
                if request_chunk_from_peer(peer["ip"], peer["port"], part_name, chunks_dir):
                    downloaded_parts.add(part_name)
                    success = True
                    break

            if not success:
                print(f"[INFO] {part_name} not available. Assuming last part reached or waiting for it...")
                break  # Break inner while loop and retry in outer loop

            part_num += 1

        # Check if we already downloaded a complete file
        if part_num > 0 and f"{target_file}.part{part_num}" not in downloaded_parts:
            output_path = os.path.join(download_dir, target_file)
            join_chunks_to_file(chunks_dir, output_path)
            print(f"[SUCCESS] Reconstructed '{target_file}' at: {output_path}")
            break  # Exit loop for this file

        print(f"[WAIT] Waiting for remaining parts of '{target_file}'. Retrying in {retry_delay}s...")
        time.sleep(retry_delay)

# Start file download threads
threads = []
for file in target_files:
    t = threading.Thread(target=download_file, args=(file,))
    t.start()
    threads.append(t)

# Wait for all downloads to complete
for t in threads:
    t.join()

input("[EXIT] Press Enter to exit...\n")
