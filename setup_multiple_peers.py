#!/usr/bin/env python3
"""
Setup script for creating multiple peer instances for testing P2P network
"""

import os
import json
import subprocess
import time
import sys
from pathlib import Path

def create_peer_config(peer_id, port, tracker_ip="127.0.0.1", tracker_port=9000):
    """Create a peer configuration file"""
    config = {
        "tracker": {
            "ip": tracker_ip,
            "port": tracker_port
        },
        "peer": {
            "id": peer_id,
            "port": port
        },
        "target_files": []
    }
    
    # Create peer directory
    peer_dir = Path(f"Node_Start_{peer_id}")
    peer_dir.mkdir(exist_ok=True)
    
    # Create subdirectories
    (peer_dir / "shared").mkdir(exist_ok=True)
    (peer_dir / "downloads").mkdir(exist_ok=True)
    (peer_dir / "downloads" / "chunks").mkdir(exist_ok=True)
    
    # Copy necessary files
    files_to_copy = [
        "Peer.py",
        "peer_config.json"
    ]
    
    for file in files_to_copy:
        if Path(file).exists():
            with open(file, 'r') as f:
                content = f.read()
            
            # Replace port in Peer.py if it's the config file
            if file == "Peer.py":
                content = content.replace('port = 5001', f'port = {port}')
            
            with open(peer_dir / file, 'w') as f:
                f.write(content)
    
    # Write config
    with open(peer_dir / "peer_config.json", 'w') as f:
        json.dump(config, f, indent=4)
    
    return peer_dir

def start_peer(peer_dir):
    """Start a peer in a new process"""
    try:
        # Change to peer directory and start the peer
        process = subprocess.Popen(
            [sys.executable, "Peer.py"],
            cwd=peer_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return process
    except Exception as e:
        print(f"Failed to start peer in {peer_dir}: {e}")
        return None

def main():
    print("🚀 P2P Network Multi-Peer Setup")
    print("=" * 40)
    
    # Configuration
    tracker_ip = input("Enter tracker IP (default: 127.0.0.1): ").strip() or "127.0.0.1"
    tracker_port = int(input("Enter tracker port (default: 9000): ").strip() or "9000")
    
    num_peers = int(input("Enter number of peers to create (default: 3): ").strip() or "3")
    
    print(f"\n📡 Creating {num_peers} peers...")
    
    # Create peers
    peer_processes = []
    base_port = 5001
    
    for i in range(num_peers):
        peer_id = f"peer{i+1}"
        port = base_port + i
        
        print(f"Creating {peer_id} on port {port}...")
        peer_dir = create_peer_config(peer_id, port, tracker_ip, tracker_port)
        
        # Add some sample files to shared directory
        sample_file = peer_dir / "shared" / f"sample_file_{peer_id}.txt"
        with open(sample_file, 'w') as f:
            f.write(f"This is a sample file from {peer_id}\n")
            f.write(f"Created at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        print(f"✅ Created {peer_id} in {peer_dir}")
    
    print(f"\n🎯 Starting {num_peers} peers...")
    
    # Start peers
    for i in range(num_peers):
        peer_id = f"peer{i+1}"
        peer_dir = Path(f"Node_Start_{peer_id}")
        
        print(f"Starting {peer_id}...")
        process = start_peer(peer_dir)
        if process:
            peer_processes.append((peer_id, process))
            print(f"✅ Started {peer_id} (PID: {process.pid})")
        else:
            print(f"❌ Failed to start {peer_id}")
        
        # Small delay between starts
        time.sleep(1)
    
    print(f"\n🎉 Successfully started {len(peer_processes)} peers!")
    print("\n📋 Peer Information:")
    for peer_id, process in peer_processes:
        port = base_port + int(peer_id[4:]) - 1
        print(f"  - {peer_id}: http://localhost:{port}")
    
    print(f"\n🌐 Tracker: http://{tracker_ip}:{tracker_port}")
    print("\n💡 Tips:")
    print("  - Each peer has a sample file in their shared directory")
    print("  - You can add more files to any peer's shared/ directory")
    print("  - Use the frontend to connect to any peer and start sharing")
    print("  - Press Ctrl+C to stop all peers")
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping all peers...")
        for peer_id, process in peer_processes:
            try:
                process.terminate()
                print(f"✅ Stopped {peer_id}")
            except:
                print(f"❌ Failed to stop {peer_id}")
        print("👋 All peers stopped!")

if __name__ == "__main__":
    main() 