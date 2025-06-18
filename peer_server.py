import socket
import threading
import os

def handle_peer(conn, shared_dir, chunks_dir):
    try:
        # Set a timeout to prevent hanging
        conn.settimeout(10)
        
        # Receive filename
        data = conn.recv(1024)
        if not data:
            print(f"[PEER SERVER] Empty request from {conn.getpeername()}")
            return
            
        filename = data.decode().strip()
        
        # Validate filename
        if not filename or len(filename) > 255:
            print(f"[PEER SERVER] Invalid filename: {filename}")
            return
            
        print(f"[PEER SERVER] Request for file: {filename}")
        
        found = False
        for directory in [chunks_dir, shared_dir]:
            path = os.path.join(directory, filename)
            if os.path.isfile(path):
                try:
                    with open(path, "rb") as f:
                        file_data = f.read()
                        conn.sendall(file_data)
                    print(f"[PEER SERVER] Sent {filename} ({len(file_data)} bytes)")
                    found = True
                    break
                except Exception as e:
                    print(f"[PEER SERVER] Error reading file {filename}: {e}")
                    continue
                    
        if not found:
            print(f"[PEER SERVER] File not found: {filename}")
            conn.send(b"NOT_FOUND")
            
    except socket.timeout:
        print(f"[PEER SERVER] Timeout from {conn.getpeername()}")
    except Exception as e:
        print(f"[PEER SERVER] Error handling request: {e}")
    finally:
        try:
            conn.close()
        except:
            pass

def start_peer_server(port, shared_dir, chunks_dir):
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(("0.0.0.0", port))  # Bind to all interfaces (LAN/Wi-Fi compatible)
        server_socket.listen()
        print(f"[PEER SERVER] Listening on port {port}")
        while True:
            conn, _ = server_socket.accept()
            threading.Thread(target=handle_peer, args=(conn, shared_dir, chunks_dir), daemon=True).start()
    except Exception as e:
        print(f"[PEER SERVER ERROR] {e}")
