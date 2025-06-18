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

### 🎯 Testing Your Setup

1. **Start the tracker**:
   ```bash
   cd P2P-Tracker-Service
   python tracker.py
   ```

2. **Start the frontend**:
   ```bash
   cd Frontend_client
   npm run dev
   ```

3. **Connect to a peer** via the frontend (e.g., `http://localhost:5001`)

4. **Add files to download** using the "Download File" section

5. **Check system logs** for successful connections

### 🔄 Network Flow
```
Frontend (React) → Peer 1 (Port 5001) → Tracker (Port 9000)
                                    ↓
                              Peer 2 (Port 5002)
                                    ↓
                              Peer 3 (Port 5003)
```

### 🚨 Common Issues

| Issue | Solution |
|-------|----------|
| Port already in use | Change port in `peer_config.json` |
| Tracker not found | Check tracker IP/port configuration |
| No files available | Add files to `shared/` directory |
| Download progress 404 | Restart peer after adding endpoints |

### 📊 Expected Behavior

**With Multiple Peers:**
- ✅ Files appear in "Available Files" list
- ✅ Downloads start successfully
- ✅ Progress updates in real-time
- ✅ Files complete and appear in "Completed Files"

**With Single Peer:**
- ⚠️ Limited functionality
- ⚠️ Can only share files, not download from others
- ⚠️ May see connection errors for missing peers

### 🎉 Success Indicators

- **Tracker**: `[TRACKER] Listening on 127.0.0.1:9000`
- **Peer**: `[REGISTER] peer1 at 127.0.0.1:5001`
- **Frontend**: "Peer started successfully" in system logs
- **Downloads**: Progress bars showing download advancement

### 📞 Need Help?

If you're still experiencing issues:

1. **Check all services are running**:
   - Tracker on port 9000
   - At least 2 peers on different ports
   - Frontend on port 5173

2. **Verify network connectivity**:
   ```bash
   ping 127.0.0.1
   telnet 127.0.0.1 9000  # Tracker
   telnet 127.0.0.1 5001  # Peer 1
   ```

3. **Check firewall settings** - allow Python applications

4. **Review system logs** in the frontend for specific error messages 