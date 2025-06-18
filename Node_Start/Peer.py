from flask import Flask, request, jsonify
from flask_cors import CORS
import threading, os, sys, time, json
 
# === Flask App ===
app = Flask(__name__)
cors = CORS(app, origins='*')                             # Origins all *

# === Ensure we can import from parent ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tracker_client import authenticate_with_tracker, register_with_tracker, get_peers_with_file
from peer_server import start_peer_server
from file_utils import split_file_to_chunks, count_parts, delete_parts, join_chunks_to_file
from peer_utils import download_file
from peer_client import request_chunk_from_peer

# === Configuration ===
CONFIG_FILE = "peer_config.json"

def load_config():
    default_config = {
        "tracker": {
            "ip": "127.0.0.1",
            "port": 9000
        },
        "peer": {
            "id": "peer1",
            "port": 5001
        },
        "target_files": []  # Initialize empty target files list
    }
    
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        return default_config
    except Exception as e:
        print(f"Error loading config: {e}")
        return default_config

def save_config(config):
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        print(f"Error saving config: {e}")

config = load_config()
tracker_config = config["tracker"]
peer_id = config["peer"]["id"]
peer_port = config["peer"]["port"]
target_files = config.get("target_files", [])

shared_dir = "./shared"
download_dir = "./downloads"
chunks_dir = os.path.join(download_dir, "chunks")

os.makedirs(shared_dir, exist_ok=True)
os.makedirs(download_dir, exist_ok=True)
os.makedirs(chunks_dir, exist_ok=True)

shared_files = {}
token = None

# Global variables for tracking download progress
download_progress = {}
download_threads = {}

@app.route("/add_target_file", methods=["POST"])
def add_target_file():
    data = request.get_json()
    
    if not data or 'filename' not in data:
        return jsonify({"error": "Missing filename"}), 400
    
    filename = data['filename']
    
    # Check if file is already in target files
    if filename in target_files:
        return jsonify({"message": f"{filename} is already in target files"}), 200
    
    # Check if file is already shared
    if filename in shared_files:
        return jsonify({"error": f"{filename} is already shared"}), 400
    
    # Add to target files
    target_files.append(filename)
    
    # Update config
    config["target_files"] = target_files
    save_config(config)
    
    return jsonify({
        "message": f"Added {filename} to target files",
        "target_files": target_files
    })

@app.route("/get_target_files", methods=["GET"])
def get_target_files():
    return jsonify({
        "target_files": target_files
    })

@app.route("/configure_tracker", methods=["POST"])
def configure_tracker():
    data = request.get_json()
    
    if not data or 'ip' not in data or 'port' not in data:
        return jsonify({"error": "Missing IP address or port"}), 400
    
    try:
        port = int(data['port'])
        if not (0 <= port <= 65535):
            return jsonify({"error": "Port must be between 0 and 65535"}), 400
    except ValueError:
        return jsonify({"error": "Invalid port number"}), 400
    
    # Update tracker configuration
    tracker_config["ip"] = data['ip']
    tracker_config["port"] = port
    
    # Save the updated configuration
    config["tracker"] = tracker_config
    save_config(config)
    
    return jsonify({
        "message": "Tracker configuration updated successfully",
        "config": tracker_config
    })

@app.route("/configure_peer", methods=["POST"])
def configure_peer():
    data = request.get_json()
    
    if not data or 'peer_id' not in data or 'port' not in data:
        return jsonify({"error": "Missing peer ID or port"}), 400
    
    try:
        port = int(data['port'])
        if not (0 <= port <= 65535):
            return jsonify({"error": "Port must be between 0 and 65535"}), 400
    except ValueError:
        return jsonify({"error": "Invalid port number"}), 400
    
    # Update peer configuration
    config["peer"]["id"] = data['peer_id']
    config["peer"]["port"] = port
    
    # Save the updated configuration
    save_config(config)
    
    return jsonify({
        "message": "Peer configuration updated successfully",
        "config": config["peer"]
    })

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
    token = authenticate_with_tracker(tracker_config["ip"], tracker_config["port"], peer_id)
    if not token:
        return jsonify({"error": "Authentication failed"}), 401

    # Register
    resp = register_with_tracker(tracker_config["ip"], tracker_config["port"], peer_id, token, peer_port, shared_files)

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

    # Initialize download progress
    download_progress[filename] = {
        "progress": 0,
        "currentPart": 0,
        "totalParts": 0,
        "status": "starting",
        "size": 0
    }

    t = threading.Thread(
        target=download_file_with_progress,
        args=(filename, peer_id, tracker_config["ip"], tracker_config["port"], token, chunks_dir, download_dir, get_peers_with_file)
    )
    download_threads[filename] = t
    t.start()
    return jsonify({"message": f"Download started for {filename}"}), 202

def download_file_with_progress(filename, peer_id, tracker_ip, tracker_port, token, chunks_dir, download_dir, get_peers_with_file_func):
    """Download file with progress tracking"""
    try:
        download_progress[filename]["status"] = "downloading"
        
        # Get file info from tracker
        peers, total_parts = get_peers_with_file_func(tracker_ip, tracker_port, peer_id, token, filename)
        download_progress[filename]["totalParts"] = total_parts
        
        downloaded = set()
        current_part = 0
        
        while True:
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
                        current_part += 1
                        download_progress[filename]["currentPart"] = current_part
                        download_progress[filename]["progress"] = int((current_part / total_parts) * 100)
                        break
                else:
                    time.sleep(2)
                    continue

            # Reconstruct file
            out_path = os.path.join(download_dir, filename)
            join_chunks_to_file(chunks_dir, out_path)
            
            # Get file size
            if os.path.exists(out_path):
                download_progress[filename]["size"] = os.path.getsize(out_path)
            
            download_progress[filename]["status"] = "completed"
            download_progress[filename]["progress"] = 100
            
            print(f"[SUCCESS] {filename} reconstructed at {out_path}")
            break
            
    except Exception as e:
        download_progress[filename]["status"] = "error"
        print(f"[ERROR] {e}")
        time.sleep(5)

@app.route("/download_progress/<filename>", methods=["GET"])
def get_download_progress(filename):
    if filename not in download_progress:
        return jsonify({"error": "Download not found"}), 404
    
    return jsonify(download_progress[filename])

@app.route("/cancel_download/<filename>", methods=["POST"])
def cancel_download(filename):
    if filename not in download_threads:
        return jsonify({"error": "Download not found"}), 404
    
    # Mark download as cancelled
    download_progress[filename]["status"] = "cancelled"
    
    # Clean up
    if filename in download_threads:
        del download_threads[filename]
    
    return jsonify({"message": f"Download cancelled for {filename}"})

@app.route("/delete_chunks/<filename>", methods=["DELETE"])
def delete_chunks(filename):
    try:
        delete_parts(filename, chunks_dir)
        return jsonify({"message": f"Chunk files deleted for {filename}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/share_file", methods=["POST"])
def share_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    try:
        # Save the file to shared directory
        file_path = os.path.join(shared_dir, file.filename)
        file.save(file_path)
        
        # Split file into chunks
        split_file_to_chunks(file_path, chunks_dir)
        parts = count_parts(chunks_dir, file.filename)
        
        # Update shared files
        shared_files[file.filename] = parts
        
        # Register with tracker if connected
        if token:
            register_with_tracker(tracker_config["ip"], tracker_config["port"], peer_id, token, peer_port, shared_files)
        
        return jsonify({
            "message": f"File {file.filename} shared successfully",
            "parts": parts
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "P2P Flask Peer is running"

@app.route("/status", methods=["GET"])
def get_status():
    """Get current peer status"""
    return jsonify({
        "peer_id": peer_id,
        "port": peer_port,
        "tracker_connected": token is not None,
        "tracker_config": tracker_config,
        "shared_files": shared_files,
        "target_files": target_files,
        "active_downloads": list(download_progress.keys()),
        "download_progress": download_progress
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=peer_port)
