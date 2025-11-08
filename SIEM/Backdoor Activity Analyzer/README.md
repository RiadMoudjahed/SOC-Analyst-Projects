# 🛡️ Backdoor Activity Analyzer

A Python-based security tool designed to detect suspicious IP patterns in network logs that may indicate backdoor or C2 (Command & Control) activity. Built for SOC analysts and security researchers.

---

## 📋 Overview

This tool analyzes log files to identify IP addresses that appear repeatedly within specific time windows—a common indicator of:
- Backdoor beaconing
- Command & Control (C2) callbacks
- Persistent unauthorized access attempts
- Data exfiltration patterns

By detecting abnormal connection frequencies, it helps security teams identify compromised systems early.

---

## ✨ Features

- **Flexible Time Windows**: Analyze activity in 10-minute or hourly intervals
- **Pattern Recognition**: Detects repeated connections from the same IP
- **Customizable Thresholds**: Set your own frequency limits for suspicious activity
- **Timestamp Parsing**: Supports ISO 8601 format logs
- **Fast Processing**: Efficiently handles large log files
- **Clear Output**: Easy-to-read suspicious IP reports with timestamps

---

## 🚀 Installation

### Prerequisites
- Python 3.7+
- No external dependencies (uses only standard library)

### Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/backdoor-activity-analyzer.git

# Navigate to directory
cd backdoor-activity-analyzer

# Run directly (no installation needed)
python backdoor_analyzer.py --help
```

---

## 📖 Usage

### Basic Usage
```bash
python backdoor_analyzer.py --log /path/to/logfile.log
```

### With Custom Options
```bash
# Analyze with hourly windows
python backdoor_analyzer.py -l access.log -w hour

# Set custom threshold (minimum 5 occurrences)
python backdoor_analyzer.py -l firewall.log -ts 5

# Combine options
python backdoor_analyzer.py -l server.log -w hour -ts 4
```

---

## 🔧 Command-Line Arguments

| Argument | Short | Required | Default | Description |
|----------|-------|----------|---------|-------------|
| `--log` | `-l` | ✅ | - | Path to the log file to analyze |
| `--window` | `-w` | ❌ | `10min` | Time window size (`10min` or `hour`) |
| `--threshold` | `-ts` | ❌ | `3` | Minimum frequency to flag as suspicious |

---

## 📊 Example Output
```
=== Suspicious IPs (10min window) ===
192.168.1.100   | Frequency 5 Periods | Times: 
   - 2025-10-31 14:30:00
   - 2025-10-31 14:40:00
   - 2025-10-31 14:50:00
   - 2025-10-31 15:00:00
   - 2025-10-31 15:10:00

10.0.0.50       | Frequency 4 Periods | Times: 
   - 2025-10-31 14:20:00
   - 2025-10-31 14:30:00
   - 2025-10-31 14:40:00
   - 2025-10-31 14:50:00
```

---

## 🔍 How It Works

1. **Log Parsing**: Extracts IP addresses and timestamps using regex patterns
2. **Time Bucketing**: Groups connections into time windows (10-minute or hourly)
3. **Frequency Analysis**: Counts how many windows each IP appears in
4. **Threshold Detection**: Flags IPs exceeding the suspicious frequency threshold
5. **Report Generation**: Displays suspicious IPs with their activity timeline

---

## 📝 Supported Log Formats

The tool expects logs with:
- **IP addresses** in standard IPv4 format (e.g., `192.168.1.1`)
- **Timestamps** in ISO 8601 format (e.g., `2025-10-31T14:35:22Z`)

### Example Compatible Log Entry
```
2025-10-25T00:00:00Z src=10.10.10.5 dst=198.51.100.50 sport=2663 dport=8080 proto=TCP bytes=701 ua="backdoorA/1.0" tag=C2_hourly
```

---

## 🎯 Use Cases

### SOC Operations
- Monitor firewall logs for persistent connections
- Detect beaconing patterns in proxy logs
- Identify compromised endpoints

### Threat Hunting
- Analyze historical logs for IOCs
- Investigate suspicious network behavior
- Track lateral movement attempts

### Incident Response
- Quickly identify affected systems
- Timeline reconstruction
- Scope determination

---

## ⚙️ Technical Details

### Detection Logic
- **10-minute windows**: Buckets timestamps into 10-minute intervals
- **Hourly windows**: Aggregates activity per hour
- **Frequency counting**: Tracks unique time periods per IP
- **Threshold-based alerting**: Flags IPs exceeding configured limits

### Performance
- Efficiently processes large log files using Python generators
- Memory-optimized with `defaultdict` and `set` data structures
- Handles millions of log entries

---

## 🛠️ Development

### Project Structure
```
backdoor-activity-analyzer/
│
├── backdoor_analyzer.py    
├── README.md               
└── example.log               
```

### Extending the Tool
Want to add features? Consider:
- Support for additional log formats
- Export results to JSON/CSV
- Integration with SIEM platforms
- GeoIP lookup for flagged IPs
- Automated alerting (email/webhook)

---

## 🤝 Contributing

Contributions that improve security detection capabilities are welcome.

### How to Contribute
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -m 'Add new detection pattern'`)
4. Push to branch (`git push origin feature/improvement`)
5. Open a Pull Request

---

## 📜 License

This project is released as open-source software. Use it for good, not evil.

> **Note**: This tool is for legitimate security research and defensive operations only. Unauthorized access to computer systems is illegal.

---

## 🙏 Acknowledgments
![Sadaqah Jariyah](https://img.shields.io/badge/Intentions-Sadaqah_Jariyah-green)     

- Built with guidance and learning through hands-on security research
- Developed to serve the cybersecurity community
- **في سبيل الله** - For the sake of Allah


---

## ⚠️ Disclaimer

This tool is provided "as is" for educational and defensive security purposes. The author is not responsible for misuse or any damage caused by this software. Always ensure you have proper authorization before analyzing network logs or systems.

---

**Stay secure. Stay vigilant. 🛡️**

*"The believer who mixes with people and bears their annoyance with patience will have a greater reward than the believer who does not mix with people and does not put up with their annoyance." - Prophet Muhammad ﷺ*
