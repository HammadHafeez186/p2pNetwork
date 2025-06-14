# 📡 WiFi P2P File Sharing System

A wireless peer-to-peer (P2P) file sharing system designed for seamless operation across WiFi networks. Share files instantly between laptops, desktops, and other devices connected to the same WiFi network - no cables, no internet required!

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Network](https://img.shields.io/badge/Network-WiFi%20Ready-orange.svg)]()

---

## 🌐 WiFi-First Design

This system is specifically optimized for **WiFi networks**, providing:
- 📶 **Wireless Operation**: No cables needed - pure WiFi connectivity
- 🔄 **Dynamic Peer Discovery**: Automatically finds peers on your WiFi network
- ⚡ **High-Speed Transfers**: Leverages modern WiFi bandwidth (802.11n/ac/ax)
- 🏠 **Home Network Friendly**: Perfect for sharing files between family devices
- 💼 **Office Ready**: Ideal for team collaboration on local networks

---

## 📁 Project Architecture

```
wifi-p2p-sharing/
├── tracker/
│   └── tracker.py              # Central WiFi tracker service
├── peer/
│   ├── Node_Start/            # Primary peer template
│   │   ├── main.py            # Peer application
│   │   ├── shared/            # Your files to share
│   │   └── downloads/         # Received files
│   │       └── chunks/        # Temporary transfer chunks
│   ├── peer_server.py         # Handles incoming requests
│   ├── peer_client.py         # Manages downloads
│   ├── file_utils.py          # File processing utilities
│   ├── tracker_client.py      # Tracker communication
│   └── peer_utils.py          # Core peer functionality
```

---

## ✨ Key Features

### 🚀 **WiFi Optimized**
- **Zero Configuration**: Connect to WiFi and start sharing
- **Multi-Device Support**: Works across Windows, macOS, Linux
- **Smart Bandwidth Usage**: Efficient chunk-based transfers
- **Network Resilience**: Handles WiFi interruptions gracefully

### 📂 **Universal File Sharing**
- **All File Types**: Documents, images, videos, archives - everything
- **Large File Support**: Automatic chunking for big files
- **Parallel Downloads**: Download from multiple peers simultaneously
- **Resume Capability**: Continue interrupted transfers

### 🔐 **Secure & Smart**
- **Token Authentication**: Secure peer verification
- **Local Network Only**: Files never leave your WiFi network
- **Auto-Discovery**: Find available files instantly
- **Duplicate Prevention**: Smart filtering of already-owned files

---

## 🚀 Quick WiFi Setup

### Step 1: Prepare Your WiFi Network
```bash
# Find your WiFi IP address
# Windows:
ipconfig

# macOS/Linux:
ifconfig | grep "inet "
```

### Step 2: Configure the Tracker
1. Edit `tracker/tracker.py`:
```python
# Replace with your WiFi network IP
start_tracker(host="192.168.1.100", port=9000)  # Your actual WiFi IP
```

### Step 3: Start the System
**Terminal 1 - Start Tracker:**
```bash
cd tracker
python tracker.py
# Output: [TRACKER] Listening on 192.168.1.100:9000
```

**Terminal 2+ - Start Peers:**
```bash
cd peer/Node_Start
python main.py
# Follow the interactive prompts
```

### Step 4: Share Files
1. **Add files** to your `shared/` directory
2. **Search** for files from other peers
3. **Download** files to your `downloads/` directory
4. **Enjoy** instant WiFi file sharing!

---

## 💡 WiFi Network Requirements

### ✅ **Compatible Networks**
- Home WiFi networks (WPA2/WPA3)
- Office/Corporate networks (with peer-to-peer allowed)
- Mobile hotspots
- Public WiFi (use with caution)

### ⚙️ **Network Settings**
- **IP Range**: Typically `192.168.1.x` or `192.168.0.x`
- **Ports Required**: 9000 (tracker) + dynamic peer ports
- **Firewall**: Allow Python applications through firewall
- **Bandwidth**: Works on any WiFi speed (optimized for 802.11n+)

---

## 🔧 WiFi Configuration Guide

### For Home Networks (Router-based)
```python
# Common home network IPs
start_tracker(host="192.168.1.100", port=9000)    # Most common
start_tracker(host="192.168.0.100", port=9000)    # Alternative
start_tracker(host="10.0.0.100", port=9000)       # Some routers
```

### For Corporate Networks
```python
# Check with IT department for allowed IP ranges
start_tracker(host="10.10.1.100", port=9000)      # Example corporate
```

### For Mobile Hotspots
```python
# Mobile hotspot typical range
start_tracker(host="192.168.43.1", port=9000)     # Android hotspot
start_tracker(host="172.20.10.1", port=9000)      # iPhone hotspot
```

---

## 📊 WiFi Performance Optimization

### **Speed Expectations**
| WiFi Standard | Typical Speed | File Transfer Rate |
|---------------|---------------|-------------------|
| 802.11n       | 50-150 Mbps  | 6-18 MB/s        |
| 802.11ac      | 200-500 Mbps | 25-60 MB/s       |
| 802.11ax (6)  | 500+ Mbps    | 60+ MB/s         |

### **Optimization Tips**
- **Close Range**: Keep devices within good WiFi range
- **Multiple Peers**: More peers = faster downloads through parallelization
- **Chunk Size**: Adjust in `file_utils.py` for your network speed
- **Background Apps**: Minimize other network-heavy applications

---

## 🛠️ Troubleshooting WiFi Issues

### **Connection Problems**
```bash
# Test WiFi connectivity between devices
ping 192.168.1.100  # Replace with tracker IP

# Check if tracker is accessible
telnet 192.168.1.100 9000
```

### **Common WiFi Issues**
| Problem | Solution |
|---------|----------|
| Can't find tracker | Verify all devices on same WiFi network |
| Slow transfers | Check WiFi signal strength and interference |
| Connection drops | Ensure stable WiFi connection |
| Firewall blocking | Allow Python through Windows/Mac firewall |

### **Network Discovery**
```bash
# Find all devices on your WiFi network
# Windows:
arp -a

# macOS/Linux:
nmap -sn 192.168.1.0/24  # Adjust IP range as needed
```

---

## 🏠 Use Cases

### **Home Networks**
- 👨‍👩‍👧‍👦 **Family Sharing**: Photos, videos, documents between family devices
- 🎮 **Media Center**: Share movies, music across devices
- 💻 **Multi-Device Work**: Access files from any device in the house

### **Office/Work**
- 👥 **Team Collaboration**: Quick file sharing without email attachments
- 📊 **Project Files**: Distribute large files instantly
- 🔄 **Backup & Sync**: Peer-to-peer file synchronization

### **Events & Gatherings**
- 📸 **Photo Sharing**: Instant photo sharing at parties/events
- 🎥 **Video Distribution**: Share recorded content immediately
- 📋 **Document Distribution**: Meeting materials, presentations

---

## 🔮 Advanced WiFi Features

### **Multi-Subnet Support**
```python
# For complex networks with multiple subnets
start_tracker(host="0.0.0.0", port=9000)  # Listen on all interfaces
```

### **WiFi Network Scanning**
```python
# Auto-detect WiFi network and configure accordingly
import subprocess
import re

def get_wifi_ip():
    # Implementation for auto-WiFi detection
    pass
```

### **Dynamic DNS Support**
```python
# For networks with changing IPs
start_tracker(host=socket.gethostname() + ".local", port=9000)
```

---

## 🚨 WiFi Security Considerations

### **Safe Usage**
- ✅ Use on **trusted WiFi networks** only
- ✅ **Home/Office networks** are ideal
- ✅ Consider **VPN** for additional security
- ⚠️ **Avoid public WiFi** for sensitive files

### **Security Features**
- 🔐 **Token-based authentication**
- 🌐 **Local network isolation**
- 🚫 **No internet dependency**
- 🔒 **Direct peer-to-peer encryption** (future enhancement)

---

## 🤝 Contributing

We welcome contributions for WiFi-specific improvements:
- 📡 Better WiFi network detection
- 🔧 Network configuration automation  
- 📊 Bandwidth monitoring and optimization
- 🔐 Enhanced security features
- 📱 Mobile device support

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🎯 Ready to Share?

Get started in under 5 minutes:
1. **Connect** all devices to the same WiFi
2. **Configure** the tracker IP address  
3. **Start** the tracker and peers
4. **Share** files wirelessly!

*No internet required. No cloud services. Just pure WiFi-powered file sharing.* 📡✨