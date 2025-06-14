import os
import time
from peer_client import request_chunk_from_peer
from file_utils import join_chunks_to_file

def delete_parts(base, chunks_dir):
    for f in os.listdir(chunks_dir):
        if f.startswith(base + ".part"):
            try:
                os.remove(os.path.join(chunks_dir, f))
            except Exception as e:
                print(f"[WARN] Could not delete {f}: {e}")

def download_file(filename, peer_id, tracker_ip, tracker_port, token, chunks_dir, download_dir, get_peers_with_file_func):
    downloaded = set()
    while True:
        try:
            peers, total_parts = get_peers_with_file_func(tracker_ip, tracker_port, peer_id, token, filename)
            peers = [p for p in peers if p["peer_id"] != peer_id]
            if not peers:
                print(f"[WAIT] No peers with '{filename}'. Retrying...")
                time.sleep(5)
                continue

            for part in range(total_parts):
                part_name = f"{filename}.part{part}"
                if part_name in downloaded:
                    continue
                for peer in peers:
                    if request_chunk_from_peer(peer["ip"], peer["port"], part_name, chunks_dir):
                        downloaded.add(part_name)
                        break
                else:
                    time.sleep(2)
                    continue

            out_path = os.path.join(download_dir, filename)
            join_chunks_to_file(chunks_dir, out_path)
            print(f"[SUCCESS] {filename} reconstructed at {out_path}")
            choice = input(f"[CHOICE] Delete parts of '{filename}'? (Y/N): ").strip().lower()
            if choice == 'y':
                delete_parts(filename, chunks_dir)
                print(f"[CLEANUP] Deleted parts for '{filename}'")
            else:
                print(f"[SEEDING] Keeping parts for '{filename}'")
            break
        except Exception as e:
            print(f"[ERROR] {e}")
            time.sleep(5)
