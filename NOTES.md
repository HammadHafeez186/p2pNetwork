# Project Requirements

# Project Requirements

- File Types: Only `.pdf`,`.txt` and `.jpg`
- Network Mode: Localhost for development; later can be extended to LAN
- Peer Discovery: Via a Tracker server
- Features:
  - File segmentation
  - Segment sharing & joining
  - Avoiding redundant downloads
  - CLI interface


## Protocol Messages

### Tracker <-> Peer
- REGISTER|peer_id|port|file_list
- PEER_LIST|file_name
- PEER_INFO|peer_id|ip|port

### Peer <-> Peer
- SEGMENT_REQ|file_name|segment_index
- SEGMENT_RESP|segment_data
