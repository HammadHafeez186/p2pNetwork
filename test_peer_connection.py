#!/usr/bin/env python3
"""
Test script to verify peer connections are working properly
"""

import socket
import time
import json
import requests

def test_flask_server(port=5001):
    """Test Flask server endpoints"""
    print(f"🔍 Testing Flask server on port {port}")
    
    try:
        # Test basic connectivity
        response = requests.get(f"http://localhost:{port}/", timeout=5)
        print(f"✅ Flask server responding: {response.text}")
        
        # Test status endpoint
        response = requests.get(f"http://localhost:{port}/status", timeout=5)
        if response.status_code == 200:
            status = response.json()
            print(f"✅ Peer status: {status['peer_id']}")
            print(f"   Flask port: {status['flask_port']}")
            print(f"   P2P port: {status['p2p_port']}")
            print(f"   Tracker connected: {status['tracker_connected']}")
            return True
        else:
            print(f"❌ Status endpoint failed: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ Flask server not responding on port {port}")
        return False
    except Exception as e:
        print(f"❌ Flask server error: {e}")
        return False

def test_p2p_server(port=6001):
    """Test P2P socket server"""
    print(f"🔍 Testing P2P server on port {port}")
    
    try:
        # Test socket connection
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect(("localhost", port))
            
            # Send a test request
            test_filename = "test_file.txt"
            s.sendall(test_filename.encode())
            
            # Receive response
            data = s.recv(1024)
            if data == b"NOT_FOUND":
                print(f"✅ P2P server responding (file not found as expected)")
                return True
            else:
                print(f"✅ P2P server responding with {len(data)} bytes")
                return True
                
    except socket.timeout:
        print(f"❌ P2P server timeout on port {port}")
        return False
    except ConnectionRefusedError:
        print(f"❌ P2P server not responding on port {port}")
        return False
    except Exception as e:
        print(f"❌ P2P server error: {e}")
        return False

def test_tracker_connection(tracker_ip="127.0.0.1", tracker_port=9000):
    """Test tracker connectivity"""
    print(f"🔍 Testing tracker on {tracker_ip}:{tracker_port}")
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect((tracker_ip, tracker_port))
            print(f"✅ Tracker connection successful")
            return True
    except Exception as e:
        print(f"❌ Tracker connection failed: {e}")
        return False

def main():
    print("🧪 P2P Network Connection Test")
    print("=" * 40)
    
    # Test tracker
    tracker_ok = test_tracker_connection()
    
    # Test Flask server
    flask_ok = test_flask_server()
    
    # Test P2P server
    p2p_ok = test_p2p_server()
    
    print("\n📊 Test Results:")
    print(f"   Tracker: {'✅' if tracker_ok else '❌'}")
    print(f"   Flask Server: {'✅' if flask_ok else '❌'}")
    print(f"   P2P Server: {'✅' if p2p_ok else '❌'}")
    
    if all([tracker_ok, flask_ok, p2p_ok]):
        print("\n🎉 All tests passed! Your P2P network is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the issues above.")
        
        if not tracker_ok:
            print("   - Make sure the tracker is running on port 9000")
        if not flask_ok:
            print("   - Make sure the peer Flask server is running on port 5001")
        if not p2p_ok:
            print("   - Make sure the peer socket server is running on port 6001")

if __name__ == "__main__":
    main() 