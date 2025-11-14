![2025-11-1406-53-15-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/213b9c7c-a2e2-4f77-bd18-4dca17dd20f9)# 🛡️ Basic Packet IDS (Intrusion Detection System)

A lightweight, real-time network intrusion detection system built with Python and Scapy. Monitors network traffic for suspicious patterns and malware signatures in packet payloads.

---

## 📋 Overview

This tool captures and analyzes network packets in real-time, searching for predefined malware signatures. It runs in the background and allows users to stop monitoring at any time to review detected threats.

**Use Case:** Educational tool for learning network security, packet analysis, and intrusion detection concepts.

---

## ✨ Features

- **Real-time Packet Capture**: Monitors live network traffic using Scapy
- **Signature-based Detection**: Identifies suspicious patterns in packet payloads
- **Multi-threaded Operation**: Runs packet sniffing in background thread
- **Clean Stop Mechanism**: Press Enter to stop monitoring and view results
- **Lightweight**: Minimal resource usage, efficient packet processing
- **Detailed Reporting**: Shows all detected suspicious packets with source/destination IPs

---

## 🚀 Installation

### Prerequisites
- Python 3.13.7+ (should work on Python 3.7+)
- Administrator/Root privileges (required for packet capture)
- Npcap (Windows) or libpcap (Linux)

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/basic-packet-ids.git
cd basic-packet-ids
```

2. **Install dependencies**
```bash
pip install scapy
```

3. **Install Npcap (Windows only)**
   - Download from: https://npcap.com/
   - Install with "WinPcap API-compatible mode" enabled

---

## 📖 Usage

### Basic Usage

**Windows:**
```bash
# Run as Administrator
python packet_ids.py
```

**Linux:**
```bash
sudo python3 packet_ids.py
```

### How It Works

1. Start the tool (requires admin/root privileges)
2. Tool begins monitoring network traffic in real-time
3. Suspicious packets are flagged as they're detected
4. Press **Enter** to stop monitoring
5. View summary of all detected threats

---

## 📸 Demo

![IDS Demo](https://github.com/user-attachments/assets/3de5f80d-84c4-41f9-8124-d676dfb9b4c9)

*Example: Tool detecting a suspicious packet patterns in network traffic*

---

## 🔍 Detection Logic

The tool currently searches for the following signature:
- **DEADBEEF pattern**: `\xDE\xAD\xBE\xEF\xC0\xFF\xEE` (7-byte hex signature)

This pattern can indicate:
- Debug/test payloads in malware
- Memory corruption exploits (DEADBEEF is commonly used in security research)
- Shellcode markers
- Intentional data patterns in malicious payloads

**Note:** DEADBEEF (0xDEADBEEF) is a hexadecimal value traditionally used by programmers as a recognizable debugging pattern. Its presence in network traffic may indicate testing, exploitation attempts, or debugging artifacts.

---

## ⚙️ Configuration

### Customize Malware Signature

Edit the `MALWARE_SIGNATURE` variable in the script:
```python
# Default signature
MALWARE_SIGNATURE = b'\xDE\xAD\xBE\xEF\xC0\xFF\xEE'

# Example: Detect reverse shell commands
MALWARE_SIGNATURE = b'/bin/bash -i'

# Example: Detect Windows executables
MALWARE_SIGNATURE = b'MZ'  # PE header
```

### Multiple Signatures

For multiple patterns, modify the detection logic:
```python
SIGNATURES = [
    b'\x00\x00\x00\x00',
    b'/bin/bash',
    b'cmd.exe'
]

for sig in SIGNATURES:
    if sig in raw_data:
        # Flag as suspicious
```

---

## 🎯 Example Output
```
      ======= Packets Captured =======

[PASS]  192.168.1.100 -> 142.250.185.46
[PASS]  142.250.185.46 -> 192.168.1.100
[SUSPICIOUS!!]  192.168.1.100 -> 203.0.113.42
[NO RAW DATA] 192.168.1.100 -> 8.8.8.8
[PASS]  192.168.1.100 -> 172.217.18.234

Press Enter to stop...

      ======= RESULTS =======

Total Suspicious Packets: 1

[1] 192.168.1.100 -> 203.0.113.42
```

---

## 🧰 Technical Details

### Architecture
```
┌─────────────────────────────────┐
│     Main Thread                 │
│  - Waits for user input         │
│  - Signals stop when Enter      │
└─────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│   Sniffer Thread                │
│  - Captures packets (Scapy)     │
│  - Filters IP packets           │
│  - Extracts payload             │
│  - Checks signatures            │
│  - Stores detections            │
└─────────────────────────────────┘
```

### Technologies Used

- **Scapy**: Packet capture and manipulation
- **Threading**: Background packet processing
- **Python Standard Library**: Event handling, data structures

### Performance

- Handles high-volume traffic efficiently
- Minimal CPU overhead with `store=False` flag
- Real-time processing with immediate alerts

---

## ⚠️ Limitations

- **Encrypted Traffic**: Cannot detect threats in HTTPS/TLS encrypted packets
- **Signature-based Only**: Does not use behavioral analysis or machine learning
- **Single Signature**: Default configuration checks only one pattern
- **False Positives**: Generic signatures may flag legitimate traffic
- **No Packet Logging**: Does not save pcap files for later analysis

### Future Enhancements

- Multiple signature support
- Protocol-specific filtering (HTTP, DNS, etc.)
- IP reputation checking
- Entropy-based detection for encrypted payloads
- PCAP export functionality
- Configuration file support

---

## 📚 Educational Purpose

This tool is designed for:
- ✅ Learning network security concepts
- ✅ Understanding packet analysis
- ✅ Studying intrusion detection systems
- ✅ Practicing Python security programming
- ✅ Exploring Scapy library capabilities

**Not intended for:**
- ❌ Production network monitoring
- ❌ Enterprise security infrastructure
- ❌ Replacing professional IDS/IPS systems

---

## 🔒 Legal & Ethical Use

**IMPORTANT:** This tool is for educational and authorized testing only.

- ✅ Use on YOUR OWN network
- ✅ Use in lab/test environments with permission
- ✅ Use for learning and research
- ❌ Do NOT use on networks without authorization
- ❌ Unauthorized network monitoring is illegal

**By using this tool, you agree to use it responsibly and legally.**

---

## 🛠️ Troubleshooting

### "Socket failed" or "Permission denied"
**Solution:** Run with administrator/root privileges

### "Npcap/WinPcap not found" (Windows)
**Solution:** Install Npcap from https://npcap.com/

### No packets captured
**Solution:** 
- Verify network interface is active
- Check firewall isn't blocking packet capture
- Ensure Npcap/libpcap is installed correctly

### High CPU usage
**Solution:** Add protocol filters to reduce packet volume

---

## 🤝 Contributing

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -m 'Add new signature detection'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Open a Pull Request

### Contribution Ideas
- Additional malware signatures
- Protocol-specific detection modules
- Performance optimizations
- Better error handling
- Cross-platform compatibility improvements

---

## 📜 License

This project is open-source and available for educational purposes.

**Disclaimer:** The author is not responsible for misuse of this tool. Use responsibly and legally.

---

## 🙏 Acknowledgments

- Inspired by professional IDS systems like Snort and Suricata
- Developed to strengthen practical security analysis skills

---

## 🎓 Learning Resources

If you're interested in network security and intrusion detection:
- [Scapy Documentation](https://scapy.readthedocs.io/)
- [Network Security Basics](https://www.cloudflare.com/learning/security/what-is-network-security/)
- [IDS vs IPS Explained](https://www.cisco.com/c/en/us/products/security/intrusion-prevention-system-ips/what-is-an-intrusion-detection-system.html)

---

**Built with dedication to cybersecurity education. في سبيل الله** 🛡️

*"Seek knowledge from the cradle to the grave." - Islamic teaching*

---

**Last Updated:** November 2025  
**Status:** Educational Project - Active
