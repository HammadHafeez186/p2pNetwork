# 🔁 P2P File Sharing System with Tracker

A lightweight peer-to-peer (P2P) file sharing system built in Python using sockets. It supports simultaneous sharing and downloading of multiple file types (e.g., `.txt`, `.jpg`, `.pdf`, etc.) across multiple peers in a LAN environment. The tracker coordinates peer discovery and file availability.

---

## 📁 Project Structure

```
p2p-file-sharing/
├── tracker/
│   └── tracker.py              # Central tracker that manages file availability
├── peer/
│   ├── peer1/                  # First peer instance
│   │   ├── main.py            # Peer main script
│   │   ├── shared/            # Files to share
│   │   └── downloads/         # Downloaded files
│   │       └── chunks/        # Chunked parts of downloaded files
│   ├── peer2/                  # Second peer instance
│   │   ├── main.py
│   │   ├── shared/
│   │   └── downloads/
│   │       └── chunks/
│   ├── peer_server.py          # Handles incoming chunk requests
│   ├── peer_client.py          # Requests chunks from other peers
│   ├── file_utils.py           # Handles file splitting and joining
│   └── tracker_client.py       # Client to communicate with the tracker
```

---

## ⚙️ Features

- 🧩 **File Chunking**: Automatic file splitting into `.partN` chunks for efficient transfer
- 🔗 **Tracker-based Discovery**: Centralized peer discovery and file availability tracking
- 🔁 **Parallel Downloads**: Simultaneous file downloads from multiple peers
- 🔍 **Auto-retry Logic**: Automatic retry mechanism if files are not yet available
- ✅ **Universal File Support**: Compatible with all file types (.txt, .jpg, .pdf, etc.)
- 🔐 **Smart Filtering**: Prevents re-downloading of already shared files
- 🌐 **LAN Optimized**: Designed for local area network environments

---

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- All devices must be on the same local network

### 1. Start the Tracker
```bash
cd tracker
python tracker.py
```
The tracker will start listening on the default port and coordinate peer connections.

### 2. Start the Peers
Open separate terminal windows for each peer:

**For Peer 1:**
```bash
cd peer/peer1
python main.py
```

**For Peer 2:**
```bash
cd peer/peer2
python main.py
```

### 3. Using the System
1. Place files you want to share in the `shared/` directory of each peer
2. Use the peer interface to search for and download files from other peers
3. Downloaded files will appear in the `downloads/` directory
4. Temporary chunks are stored in `downloads/chunks/` during transfer

---

## 🔧 Configuration

- **Tracker Address**: Default is localhost. Modify in peer configuration if tracker runs on different machine
- **Chunk Size**: Configurable in `file_utils.py` for optimal network performance
- **Port Settings**: Ensure firewall allows communication on configured ports

---

## 📝 Important Notes

> **Notice**: The tracker code is placed in a separate GitHub repository named: `tracker`

This distributed architecture allows for:
- Independent tracker deployment
- Easier maintenance and updates
- Scalable peer management

---

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).