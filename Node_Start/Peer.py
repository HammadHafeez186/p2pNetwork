from flask import Flask, request, jsonify
from flask_cors import CORS
import threading, os, sys, time
 
# === Flask App ===
app = Flask(__name__)
cors = CORS(app, origins='*')                             # Origins all *

# === Ensure we can import from parent ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tracker_client import authenticate_with_tracker, register_with_tracker, get_peers_with_file
from peer_server import start_peer_server
from file_utils import split_file_to_chunks, count_parts
from peer_utils import download_file

# === Configuration ===
tracker_ip = "127.0.0.1"      #192.168.100.51
tracker_port = 9000

peer_id = "peer1"             #change
peer_port = 5001              #change

shared_dir = "./shared"
download_dir = "./downloads"
chunks_dir = os.path.join(download_dir, "chunks")
target_files = ["Notes.txt"]

os.makedirs(shared_dir, exist_ok=True)
os.makedirs(download_dir, exist_ok=True)
os.makedirs(chunks_dir, exist_ok=True)

shared_files = {}
token = None

@app.route("/start_peer", methods=["Get", "POST"])
def start_peer():
    global token, shared_files

    # Prepare shared files
    shared_files = {}
    for fname in os.listdir(shared_dir):
        fpath = os.path.join(shared_dir, fname)
        if os.path.isfile(fpath):
            split_file_to_chunks(fpath, chunks_dir)
            shared_files[fname] = count_parts(chunks_dir, fname)

    # Filter out already owned files
    download_targets = [f for f in target_files if f not in shared_files]

    # Authenticate
    token = authenticate_with_tracker(tracker_ip, tracker_port, peer_id)
    if not token:
        return jsonify({"error": "Authentication failed"}), 401

    # Register
    resp = register_with_tracker(tracker_ip, tracker_port, peer_id, token, peer_port, shared_files)

    # Start peer server in background
    threading.Thread(target=start_peer_server, args=(peer_port, shared_dir, chunks_dir), daemon=True).start()

    return jsonify({
        "peer_id": peer_id,
        "shared_files": shared_files,
        "register_response": resp,
        "download_targets": download_targets
    })


@app.route("/download/<filename>", methods=["Get","POST"])
def download(filename):
    if filename in shared_files:
        return jsonify({"message": f"{filename} already shared."}), 200

    t = threading.Thread(
        target=download_file,
        args=(filename, peer_id, tracker_ip, tracker_port, token, chunks_dir, download_dir, get_peers_with_file)
    )
    t.start()
    return jsonify({"message": f"Download started for {filename}"}), 202


@app.route("/")
def home():
    return "P2P Flask Peer is running"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=peer_port)
