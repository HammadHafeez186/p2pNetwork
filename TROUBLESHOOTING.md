# 🔧 P2P Network Troubleshooting Guide

## Common Error: Connection Refused (WinError 10061)

### ❌ Error Message
```
[ERROR] Failed to get Notes.txt.part33 from 127.0.0.1:5002 — [WinError 10061] No connection could be made because the target machine actively refused it
```

### 🔍 What This Means
This error occurs when:
1. **Missing Peers**: The system is trying to connect to a peer at `127.0.0.1:5002` that isn't running
2. **Single Peer Setup**: You're running only one peer, but the system expects multiple peers for file sharing
3. **Stale Tracker Data**: The tracker has information about peers that are no longer active

## Common Error: Bad Request Syntax

### ❌ Error Message
```
192.168.243.122 - - [18/Jun/2025 13:13:12] code 400, message Bad request syntax ('PDC-4.docx.part0')
```

### 🔍 What This Means
This error occurs when:
1. **Port Conflict**: The Flask server and socket server are trying to use the same port
2. **Malformed Requests**: Raw socket data is being sent to the HTTP server
3. **Server Confusion**: P2P transfers are hitting the wrong server endpoint

### ✅ **FIXED** - Port Separation
The system now uses separate ports:
- **Flask Server**: Port 5001 (for frontend communication)
- **P2P Socket Server**: Port 6001 (for file transfers)

This prevents conflicts and ensures proper request handling.

### ✅ Solutions

#### Option 1: Quick Fix - Single Peer Mode
If you want to test with just one peer:

1. **Clear tracker data** by restarting the tracker:
   ```bash
   # Stop the tracker (Ctrl+C)
   # Then restart it
   cd P2P-Tracker-Service
   python tracker.py
   ```

2. **Restart your peer**:
   ```bash
   cd p2pNetwork/Node_Start
   python Peer.py
   ```

3. **Add files to shared directory** before starting the peer:
   ```bash
   # Copy some files to the shared/ directory
   cp /path/to/your/files/* ./shared/
   ```

#### Option 2: Multi-Peer Setup (Recommended)
For proper P2P file sharing, you need multiple peers:

1. **Use the setup script**:
   ```bash
   cd p2pNetwork
   python setup_multiple_peers.py
   ```

2. **Follow the prompts** to create 3-5 peers

3. **Each peer will have sample files** in their shared directories

#### Option 3: Manual Multi-Peer Setup
Create multiple peer instances manually:

1. **Create peer directories**:
   ```bash
   mkdir Node_Start_peer1 Node_Start_peer2 Node_Start_peer3
   ```

2. **Copy files to each directory**:
   ```bash
   cp -r Node_Start/* Node_Start_peer1/
   cp -r Node_Start/* Node_Start_peer2/
   cp -r Node_Start/* Node_Start_peer3/
   ```

3. **Update peer configurations**:
   - `Node_Start_peer1/peer_config.json`: port 5001
   - `Node_Start_peer2/peer_config.json`: port 5002  
   - `Node_Start_peer3/peer_config.json`: port 5003

4. **Start each peer** in separate terminals:
   ```bash
   # Terminal 1
   cd Node_Start_peer1
   python Peer.py
   
   # Terminal 2
   cd Node_Start_peer2
   python Peer.py
   
   # Terminal 3
   cd Node_Start_peer3
   python Peer.py
   ```

### 🧪 Testing Your Setup

1. **Run the test script** to verify everything is working:
   ```bash
   cd p2pNetwork
   python test_peer_connection.py
   ```

2. **Start the tracker**:
   ```bash
   cd P2P-Tracker-Service
   python tracker.py
   ```

3. **Start the frontend**:
   ```bash
   cd Frontend_client
   npm run dev
   ```

4. **Connect to a peer** via the frontend (e.g., `http://localhost:5001`)

5. **Add files to download** using the "Download File" section

6. **Check system logs** for successful connections

### 🔄 Network Flow (Updated)
```
Frontend (React) → Flask Server (Port 5001) → Tracker (Port 9000)
                                    ↓
                              P2P Socket Server (Port 6001)
                                    ↓
                              Peer 2 (Ports 5002/6002)
                                    ↓
                              Peer 3 (Ports 5003/6003)
```

### 🚨 Common Issues

| Issue | Solution |
|-------|----------|
| Port already in use | Change port in `peer_config.json` |
| Tracker not found | Check tracker IP/port configuration |
| No files available | Add files to `shared/` directory |
| Download progress 404 | Restart peer after adding endpoints |
| Bad request syntax | ✅ **FIXED** - Now using separate ports |
| File timeouts | ✅ **FIXED** - Better timeout handling |

### 📊 Expected Behavior

**With Multiple Peers:**
- ✅ Files appear in "Available Files" list
- ✅ Downloads start successfully
- ✅ Progress updates in real-time
- ✅ Files complete and appear in "Completed Files"
- ✅ No more "Bad request syntax" errors
- ✅ Proper timeout handling

**With Single Peer:**
- ⚠️ Limited functionality
- ⚠️ Can only share files, not download from others
- ⚠️ May see connection errors for missing peers

### 🎉 Success Indicators

- **Tracker**: `[TRACKER] Listening on 127.0.0.1:9000`
- **Peer**: `[REGISTER] peer1 at 127.0.0.1:6001` (P2P port)
- **Flask**: `Running on http://0.0.0.0:5001` (Frontend port)
- **P2P Server**: `[PEER SERVER] Listening on port 6001`
- **Frontend**: "Peer started successfully" in system logs
- **Downloads**: Progress bars showing download advancement

### 📞 Need Help?

If you're still experiencing issues:

1. **Run the test script**:
   ```bash
   python test_peer_connection.py
   ```

2. **Check all services are running**:
   - Tracker on port 9000
   - At least 2 peers on different ports
   - Frontend on port 5173

3. **Verify network connectivity**:
   ```bash
   ping 127.0.0.1
   telnet 127.0.0.1 9000  # Tracker
   telnet 127.0.0.1 5001  # Flask Server
   telnet 127.0.0.1 6001  # P2P Server
   ```

4. **Check firewall settings** - allow Python applications

5. **Review system logs** in the frontend for specific error messages 