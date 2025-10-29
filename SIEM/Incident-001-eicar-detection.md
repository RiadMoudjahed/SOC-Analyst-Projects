# Incident Report #001 - EICAR Malware Detection 👾🛡

## Executive Summary
Successfully detected EICAR test file using Wazuh SIEM with VirusTotal integration, demonstrating complete **NIST SP 800-61** incident response lifecycle.

## What is NIST?

NIST is the **National Metrology Institute** for the United States, also known as an **NMI**. Everything you use in your everyday life works because of measurements. Without precise measurements, your car wouldn’t run, your phone wouldn’t work, and hospitals couldn’t function. We maintain the measurements that make industry and society work. Learn more about our unique role in the national — and global — economy.
https://www.nist.gov/
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/0c53e8bc-f3b9-4160-8dc2-50acc435f940" />


## NIST Framework Implementation

### 1. IDENTIFY Phase
- **Asset:** Windows 10 Endpoint (Main-Win10, 192.168.16.1)
- **Monitored Directory:** C:\Users\Public\Documents
- **Detection Method:** Real-time File Integrity Monitoring (FIM)
  <img width="1915" height="677" alt="Image" src="https://github.com/user-attachments/assets/f2139a21-289a-434a-ad3f-fd4439f72946" />

### 2. PROTECT Phase
- **Controls Implemented:**
  - FIM with real-time monitoring enabled
  - SHA256/MD5 hash calculation on all files
  - Integration with VirusTotal threat intelligence
    <img width="1305" height="812" alt="Image" src="https://github.com/user-attachments/assets/c00fcd68-a852-4f81-843d-295c1b9a4feb" />

### 3. DETECT Phase
- **Detection Timeline:**
  - 08:08:21 - FIM detected file addition (Rule 554)
  - 08:08:21 - Custom EICAR rule triggered (Rule 100200, Level 12)
  - 08:08:24 - VirusTotal confirmed malicious (Rule 87105, 66/69 engines)
- **Mean Time to Detect (MTTD):** < 3 seconds
- **MITRE ATT&CK:** T1204 (User Execution)
  <img width="1914" height="902" alt="Image" src="https://github.com/user-attachments/assets/3f2dcaf4-ebb5-4777-811f-d0b06b4ff8cb" />

### 4. RESPOND Phase
- **Automated Response:**
  - Critical alert generated (Level 12)
  - Email notification triggered
  - Threat intelligence enriched via VirusTotal
- **File Hash:** 44d88612fea8a8f36de82e1278abb02f (EICAR signature)
- **VirusTotal Report:** 66/69 AV engines flagged as malicious

### 5. RECOVER Phase
- **Remediation:** File identified and ready for quarantine/deletion
- **Documentation:** Complete incident timeline captured
- **Lessons Learned:** Detection pipeline validated successfully

## Technical Details

**File Information:**
- Path: `c:\users\public\documents\eicar.com`
- Size: 68 bytes
- MD5: 44d88612fea8a8f36de82e1278abb02f
- SHA256: 275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f

**Alert Sequence:**
1. Rule 553: File deleted (cleanup from previous test)
2. Rule 100200: EICAR custom detection
3. Rule 87105: VirusTotal malware confirmation
   
**The rule I Implemented:**
```
<group name="local,syscheck,">

  <!-- Simple EICAR detection based on filename -->
  <rule id="100200" level="12">
    <if_sid>550,554</if_sid>
    <field name="file">eicar</field>
    <description>EICAR test file detected: $(file)</description>
    <mitre>
      <id>T1204</id>
    </mitre>
  </rule>

</group>
```

**My lab's network:** <img width="1079" height="1289" alt="image" src="https://github.com/user-attachments/assets/a2c77412-3d65-4fe6-a2e2-64ee9de02cf5" />




## Key Metrics
- **Detection Rate:** 100% (3/3 alerts triggered)
- **False Positives:** 0
- **MTTD:** 3 seconds
- **Mean Time to Respond (MTTR):** < 10 seconds (automated)

  ## Methodology & Tools

### AI-Assisted Learning
This project was completed using AI (Claude) as a technical mentor and troubleshooting assistant. AI was used for:

- **Configuration guidance:** ossec.conf syntax, rule structure, integration setup
- **Debugging support:** Service failures, log analysis, error interpretation  
- **Best practices:** NIST framework alignment, MITRE ATT&CK mapping
- **Documentation templates:** Incident report structure, technical writing

### Hands-On Implementation
All infrastructure deployment, configuration, and testing was performed directly:
- Installed Wazuh Manager and Windows Agent
- Configured File Integrity Monitoring
- Created custom detection rules (Rule 100200)
- Integrated VirusTotal API
- Troubleshot and resolved service failures
- Validated detection with EICAR testing

### Skills Demonstrated
- SIEM deployment and configuration
- Linux system administration (systemctl, log analysis)
- Security event correlation and analysis
- API integration (VirusTotal)
- Incident detection and documentation
- Problem-solving and troubleshooting

## Conclusion
Successfully demonstrated end-to-end threat detection using Wazuh SIEM aligned with NIST SP 800-61 guidelines. Integration of custom detection rules and external threat intelligence (VirusTotal) provided comprehensive malware identification capabilities.
