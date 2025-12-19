<p align="center">
  <img
    width="480"
    height="480"
    alt="Image"
    src="https://github.com/user-attachments/assets/5afee59b-2428-4c37-9658-362805c0c2c5"
  />
</p>

# 🛡️ ML-Enhanced Backdoor Activity Analyzer

A Python-based security tool with **Machine Learning capabilities** designed to detect sophisticated backdoor and C2 (Command & Control) activity in network logs. Built for SOC analysts and security researchers who need intelligent, adaptive threat detection.

---

## 📋 Overview

This tool analyzes log files using both traditional threshold-based detection and advanced Machine Learning to identify suspicious IP patterns that may indicate:
- **Backdoor beaconing** (periodic callbacks)
- **Command & Control (C2)** communications
- **Persistent unauthorized access** attempts
- **Data exfiltration** patterns
- **Automated malware** activity

By combining multiple detection techniques and behavioral analysis, it helps security teams identify compromised systems with higher accuracy and fewer false positives.

---

## ✨ Features

### 🤖 Machine Learning Detection
- **Isolation Forest Algorithm**: Automatically identifies anomalous connection patterns
- **Multi-dimensional Analysis**: Evaluates 7 behavioral features simultaneously
- **Beaconing Detection**: Identifies periodic callback patterns typical of malware
- **Anomaly Scoring**: Risk-based scoring instead of binary yes/no decisions
- **Adaptive Learning**: No manual threshold tuning required

### 🔧 Traditional Detection
- **Flexible Time Windows**: Analyze activity in 10-minute or hourly intervals
- **Pattern Recognition**: Detects repeated connections from the same IP
- **Customizable Thresholds**: Set your own frequency limits for suspicious activity

### 📊 Advanced Analytics
- **Time Variance Analysis**: Measures connection timing consistency
- **Entropy Calculation**: Detects robotic vs. human-like behavior
- **Connection Density**: Analyzes activity concentration
- **Geographic Intelligence**: GeoIP location lookup for context
- **Temporal Profiling**: Tracks activity duration and spread

### 🎯 User Experience
- **Dual Mode Operation**: Switch between ML and legacy detection
- **Sensitivity Control**: Adjust detection strictness (low/medium/high)
- **Detailed Reports**: Comprehensive analysis with clear risk indicators
- **Fast Processing**: Efficiently handles large log files

---

## 🚀 Installation

### Prerequisites
```bash
Python 3.7+
```

### Required Libraries
```bash
pip install scikit-learn numpy geoip2
```

### Optional: GeoIP Database
Download the free GeoLite2 database for geographic lookups:
```bash
# Download from MaxMind (free account required)
# Place GeoLite2-City.mmdb in the same directory as the script
```

---

## 📖 Usage

### Machine Learning Mode (Recommended)
```bash
# Basic ML detection
python backdoor_analyzer.py --log access.log --ml

# Adjust sensitivity
python backdoor_analyzer.py -l firewall.log --ml --sensitivity high

# Fine-tune contamination (expected anomaly percentage)
python backdoor_analyzer.py -l server.log --ml --contamination 0.15

# Use hourly windows
python backdoor_analyzer.py -l proxy.log --ml -w hour
```

### Legacy Mode (Threshold-Based)
```bash
# Basic threshold detection
python backdoor_analyzer.py --log access.log

# Custom threshold
python backdoor_analyzer.py -l firewall.log -ts 5

# Hourly analysis
python backdoor_analyzer.py -l server.log -w hour -ts 10
```

---

## 🔧 Command-Line Arguments

| Argument | Short | Required | Default | Description |
|----------|-------|----------|---------|-------------|
| `--log` | `-l` | ✅ | - | Path to the log file to analyze |
| `--ml` | `-ml` | ❌ | `False` | Enable ML-based anomaly detection |
| `--window` | `-w` | ❌ | `10min` | Time window size (`10min` or `hour`) |
| `--threshold` | `-ts` | ❌ | `20` | Minimum frequency (legacy mode only) |
| `--sensitivity` | `-s` | ❌ | `medium` | Detection sensitivity (`low`, `medium`, `high`) |
| `--contamination` | `-c` | ❌ | `0.1` | Expected anomaly proportion (0.05-0.3) |

---

## 📊 Example Output

### ML Mode Output
```
✓ Processed 15,234 log entries
✓ Found 487 unique IP addresses
[ML] Training Isolation Forest (contamination=0.1)...
[ML] Detected 12 anomalous IPs

============================================================
ML-BASED ANOMALY DETECTION (10min window)
============================================================

⚠ Found 12 ANOMALOUS IPs:

────────────────────────────────────────────────────────────
🔴 IP: 203.45.67.89
   Location: Moscow, Russia
   Anomaly Score: -0.234 (lower = more suspicious)

   📊 Analysis:
      • Frequency: 47 connections
      • Time Windows: 12 periods
      • Activity Duration: 3.5 hours
      • Connection Density: 3.92 conn/window
      • Time Variance: 1.2s
      • Entropy: 0.15
      • ⚠ BEACONING DETECTED: 60s intervals (CV: 0.017)

   🕐 Sample Connection Times:
      - 2024-12-10 03:00:00
      - 2024-12-10 03:01:00
      - 2024-12-10 03:02:00
      - 2024-12-10 03:03:00
      - 2024-12-10 03:04:00
      ... and 42 more

────────────────────────────────────────────────────────────
🔴 IP: 118.25.89.156
   Location: Beijing, China
   Anomaly Score: -0.189

   📊 Analysis:
      • Frequency: 203 connections
      • Time Windows: 45 periods
      • Activity Duration: 8.2 hours
      • Connection Density: 4.51 conn/window
      • Time Variance: 0.8s
      • Entropy: 0.09
      • ⚠ BEACONING DETECTED: 30s intervals (CV: 0.023)

============================================================
```

### Legacy Mode Output
```
============================================================
THRESHOLD-BASED DETECTION (10min window)
Threshold: 20 connections
============================================================

⚠ Found 8 IPs above threshold:

203.45.67.89    | Moscow, Russia
   Frequency: 47 periods
   First 5 timestamps:
      - 2024-12-10 03:00:00
      - 2024-12-10 03:10:00
      - 2024-12-10 03:20:00
      - 2024-12-10 03:30:00
      - 2024-12-10 03:40:00
      ... and 42 more
```

---

## 🔍 How It Works

### ML Detection Pipeline

1. **Log Parsing**
   - Extracts IP addresses and timestamps using regex
   - Organizes data into time-based buckets

2. **Feature Extraction** (7 key metrics)
   - Connection frequency
   - Time window spread
   - Timing variance
   - Connection entropy
   - Beaconing detection
   - Connection density
   - Activity duration

3. **Data Preprocessing**
   - Feature standardization (scaling)
   - Normalization for ML model

4. **Isolation Forest Analysis**
   - Trains on all IP behavioral patterns
   - Identifies outliers/anomalies
   - Calculates anomaly scores

5. **Risk Assessment**
   - Ranks IPs by suspiciousness
   - Flags beaconing behavior
   - Provides detailed analysis

### Detection Capabilities

#### Beaconing Detection
Identifies periodic callback patterns:
- Calculates interval consistency
- Low coefficient of variation (CV < 0.3) = suspicious
- Perfect for detecting malware "heartbeats"

#### Entropy Analysis
Measures behavioral randomness:
- High entropy = human-like, unpredictable
- Low entropy = robotic, programmed (malware)

#### Time Variance
Tracks connection timing patterns:
- Consistent intervals = automated behavior
- Random intervals = likely legitimate

---

## 📝 Supported Log Formats

The tool expects logs with:
- **IP addresses** in standard IPv4 format (e.g., `192.168.1.1`)
- **Timestamps** in ISO 8601 format (e.g., `2024-12-10T14:35:22Z`)

### Example Compatible Log Entry
```
2024-12-10T14:35:22Z src=10.10.10.5 dst=198.51.100.50 sport=2663 dport=8080 proto=TCP bytes=701 ua="backdoorA/1.0" tag=C2_hourly
```

---

## 🎯 Use Cases

### SOC Operations
- **Threat Detection**: Identify active backdoors and C2 channels
- **Behavioral Monitoring**: Spot unusual connection patterns
- **Early Warning**: Detect compromises before significant damage

### Threat Hunting
- **Historical Analysis**: Search past logs for IOCs
- **Pattern Discovery**: Find previously unknown threats
- **Campaign Tracking**: Identify related malicious activity

### Incident Response
- **Scope Assessment**: Quickly identify all affected systems
- **Timeline Reconstruction**: Track attacker activity
- **Forensic Analysis**: Deep-dive into suspicious IPs

### Security Research
- **Malware Analysis**: Study backdoor communication patterns
- **C2 Profiling**: Understand attacker infrastructure
- **Detection Engineering**: Develop new detection rules

---

## 🧠 Understanding the Features

### Feature Breakdown

| Feature | Description | Suspicious When |
|---------|-------------|-----------------|
| **Frequency** | Total connections | Unusually high or low |
| **Window Spread** | # of time periods active | Too few or too many |
| **Time Variance** | Timing consistency | Very low (robotic) |
| **Entropy** | Behavioral randomness | Very low (predictable) |
| **Beaconing** | Periodic callbacks | Detected (CV < 0.3) |
| **Density** | Connections per window | Abnormally concentrated |
| **Time Span** | Activity duration | Unusually long |

### Anomaly Score Interpretation

- **Score < -0.2**: Highly suspicious (immediate investigation)
- **Score -0.1 to -0.2**: Suspicious (review recommended)
- **Score > 0**: Normal behavior

---

## ⚙️ Technical Details

### ML Model: Isolation Forest

**Why Isolation Forest?**
- Excellent for anomaly detection in security data
- Doesn't require labeled training data
- Fast and efficient with large datasets
- Handles high-dimensional feature spaces
- Works well with imbalanced data (few attacks, many normal connections)

**Model Parameters**
- `contamination`: Expected % of anomalies (default: 10%)
- `n_estimators`: Number of decision trees (default: 100)
- `random_state`: Reproducibility seed (default: 42)

### Performance
- Handles millions of log entries efficiently
- Memory-optimized data structures
- Parallel processing via scikit-learn
- Fast feature extraction
- Sub-second ML inference

---

## 🛠️ Development

### Project Structure
```
backdoor-activity-analyzer/
│
├── backdoor_analyzer.py      # Main ML-enhanced script
├── README.md                  # This file
├── GeoLite2-City.mmdb        # GeoIP database 
└── example.log                # Sample log file
```

### Extending the Tool

**Potential Enhancements:**
- Additional ML models (Random Forest, One-Class SVM)
- Real-time monitoring mode
- Threat intelligence integration
- SIEM platform connectors
- Web dashboard with visualizations
- Automated alerting (email/webhook/Slack)
- Export to JSON/CSV/SIEM formats
- Deep learning for advanced pattern recognition

---

## 🔐 Security Considerations

### Best Practices
- Run in isolated environment for untrusted logs
- Validate and sanitize log inputs
- Secure storage of GeoIP database
- Regular model retraining with new data
- Monitor for adversarial evasion attempts

### Privacy Notes
- GeoIP data provides approximate location only
- No PII collection beyond what's in logs
- Ensure GDPR/privacy law compliance when analyzing user data

---

## 📜 License

This project is released as open-source software. Use it for good, not evil.

> **Note**: This tool is for legitimate security research and defensive operations only. Unauthorized access to computer systems is illegal.

---

## 🙏 Acknowledgments

![Sadaqah Jariyah](https://img.shields.io/badge/Intentions-Sadaqah_Jariyah-green)
![Python](https://img.shields.io/badge/Python-3.7+-blue)
![ML](https://img.shields.io/badge/ML-Scikit--Learn-orange)
![Security](https://img.shields.io/badge/Security-Threat_Detection-red)

- Built with guidance through hands-on security research
- ML techniques inspired by academic research in anomaly detection
- Developed to serve the cybersecurity community
- **في سبيل الله** - For the sake of Allah

### Special Thanks
- scikit-learn community for excellent ML tools
- MaxMind for GeoLite2 database
- Security researchers sharing threat intelligence
- The open-source security community

---

## ⚠️ Disclaimer

This tool is provided "as is" for educational and defensive security purposes. The author is not responsible for misuse or any damage caused by this software. Always ensure you have proper authorization before analyzing network logs or systems.

**Machine Learning Note**: ML models may produce false positives or miss sophisticated attacks. Always combine automated detection with human analysis and other security controls.

---

**Stay secure. Stay vigilant. Stay adaptive. 🛡️🤖**

*"The believer who mixes with people and bears their annoyance with patience will have a greater reward than the believer who does not mix with people and does not put up with their annoyance." - Prophet Muhammad ﷺ*

---

## 📊 Quick Start Examples

### Example 1: Quick Scan
```bash
python backdoor_analyzer.py -l access.log --ml
```

### Example 2: High-Security Environment
```bash
python backdoor_analyzer.py -l firewall.log --ml --sensitivity high -w 10min
```

### Example 3: Research & Analysis
```bash
python backdoor_analyzer.py -l historical.log --ml --contamination 0.05 -w hour
```

### Example 4: Legacy Compatibility
```bash
python backdoor_analyzer.py -l server.log -ts 15 -w hour
```

---

*Last Updated: December 2024*
*Version: 2.0 (ML-Enhanced)*
