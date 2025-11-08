# WELCOME 👋

In this project, I am going to show you how to make a lab and configure the network with VMware.

---

### Our network should look like this 👇

<p align="center">
  <img src="https://github.com/user-attachments/assets/73a1ea38-87c6-48e3-81df-c7bd885950d1" alt="Network Diagram" width="600">
</p>

Before we get started, head to **Edit > Virtual Network Editor**, based on how much LANs do you need, add networks.
<p align="center">
  <img src="https://github.com/user-attachments/assets/b59d7fe6-2609-4da1-a79d-4eab325d8aaa" alt="Lab Configuration Overview" width="60%">
</p>
I added extra networks in anticipation of any future updates to our lab.

---

### Network Details

- **WAN:** `192.168.16.0/24` is the subnet IP of `VMnet8 > em0`, connecting the Virtual Machines and the host.  
- **pfSense:** `192.168.25.1` functions as a router and firewall, monitoring every device on the LAN.
- **Windows 10**, **Ubuntu**, and **Kali Linux** are all on the same LAN, connected through **pfSense**.  
- Note: These devices **will not have Internet access** unless **pfSense** is turned **ON**.
- **Linux Server** is connected to both the **LAN** and the **WAN**.  
- This configuration allows us to **monitor the host** using **Wazuh** through `span > em3` (traffic mirroring).



---

### pfSense Network Layout 👇

<p align="center">
  <img src="https://github.com/user-attachments/assets/4563aad6-39bf-4b5f-b2a5-01aa7ba3ea97" alt="pfSense Network Diagram" width="700">
</p>

---

### Windows 10, Ubuntu, and Kali Linux Network Layout 👇

<p align="center">
  <img src="https://github.com/user-attachments/assets/51193201-572a-4a68-a832-0dda919f5bd5" alt="Lab Screenshot 1" width="48%">
  <img src="https://github.com/user-attachments/assets/085ceebf-19a5-4d8e-adcf-656f986f9b65" alt="Lab Screenshot 2" width="48%">
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/d622e814-bd5d-47b6-8b29-cf381eb53c0c" alt="Lab Screenshot 3" width="60%">
</p>


**After running Windows 10 you will notice that network is undifiend, follow these steps to troubleshoot the issue:**

Control Panel > Network and Internet > Network and Sharing Center > Ethernet1 > Properties > Internet Protocol Version 4, and then fill the blanks based on your network (IP Address, Subnet Mask, Default Gateway...etc) 

For Example:

<p align="center">
  <img src="https://github.com/user-attachments/assets/ccc223fb-f7ba-4c31-92c6-ac1f93ee41bb" alt="Network Diagram Overview" width="75%">
</p>

---

### Linux Server Network Layout 👇

<p align="center">
  <img src="https://github.com/user-attachments/assets/ea49e378-3776-4517-b4a3-aee63ae5e657" alt="Centered Lab Image" width="80%">
</p>

---

## Key Networking Concepts in This Lab

### Network Segmentation
This lab demonstrates **network segmentation**, a critical security practice where a network is divided into multiple isolated segments. By separating the WAN (`192.168.16.0/24`) from the LAN (`192.168.25.0/24`), we create security boundaries that limit the blast radius of potential security incidents and make it easier to monitor and control traffic flow.

### Subnetting and CIDR Notation
The `/24` notation (CIDR - Classless Inter-Domain Routing) indicates that the first 24 bits of the IP address represent the network portion, leaving 8 bits for host addresses. This means each subnet can support 254 usable host addresses (256 total minus network and broadcast addresses).

### Default Gateway
The **pfSense** router (`192.168.25.1`) serves as the default gateway for devices on the LAN. Any traffic destined for networks outside the local subnet is forwarded to this gateway, which then routes it appropriately. This is why Internet access depends on pfSense being active.

### Virtual Network Interfaces
VMware's **VMnet** interfaces act as virtual network adapters that enable communication between virtual machines and between VMs and the host system. Each VMnet can be configured as:
- **Bridged**: Connects VMs directly to the physical network
- **NAT**: Provides Internet access through the host's network connection
- **Host-only**: Creates an isolated network for VM-to-VM and VM-to-host communication

### pfSense as a Stateful Firewall
**pfSense** operates as a stateful firewall, meaning it tracks the state of network connections and makes decisions based on connection context, not just individual packets. This allows it to:
- Monitor all traffic entering and leaving the LAN
- Apply security rules based on connection state
- Detect and block suspicious traffic patterns
- Log network activity for security analysis

### Port Mirroring (SPAN)
The **SPAN** (Switched Port Analyzer) configuration on `em3` creates a mirror of network traffic, sending copies of packets to the monitoring interface. This is essential for:
- **Intrusion Detection Systems (IDS)** like Wazuh
- Network traffic analysis without interfering with normal operations
- Packet capture for forensic investigation
- Real-time security monitoring

### Dual-Homed Host
The **Linux Server** is configured as a dual-homed host with interfaces on both the LAN and WAN. This architecture allows the server to:
- Act as a bridge between network segments
- Monitor traffic from both networks simultaneously
- Run security tools (like Wazuh) that need visibility into multiple network zones
- Provide services to both internal and external networks

### Static IP Configuration
Unlike DHCP (Dynamic Host Configuration Protocol), which automatically assigns IP addresses, this lab uses **static IP addressing**. Each device has a manually configured IP that doesn't change. This is crucial for:
- Consistent firewall rules
- Reliable monitoring and logging
- Predictable network behavior for security analysis
- Easy identification of devices in security logs

### Network Address Translation (NAT)
When VMs access the Internet through pfSense, **NAT** translates their private IP addresses (`192.168.25.x`) to the public-facing IP of the WAN interface. This:
- Conserves public IP addresses
- Adds a layer of security by hiding internal network structure
- Allows multiple devices to share a single public IP

### Layer 3 Routing
**pfSense** operates at Layer 3 (Network Layer) of the OSI model, making routing decisions based on IP addresses. It determines the best path for packets to travel between the LAN and WAN segments, enforcing security policies at the network boundary.

---

## Why This Lab Matters for SOC Analysts

This lab environment replicates enterprise network architecture in miniature, providing hands-on experience with:
- **Traffic analysis**: Understanding normal vs. suspicious network patterns
- **Firewall management**: Configuring rules and monitoring enforcement
- **Network forensics**: Capturing and analyzing packets for incident investigation
- **Segmentation strategies**: Implementing defense-in-depth principles
- **SIEM integration**: Feeding network data into security monitoring tools like Wazuh

By building and maintaining this lab, you develop practical skills in network security monitoring, incident detection, and defensive architecture—core competencies for any SOC analyst.

---

## Technologies Used
- **VMware Workstation**: Virtualization platform
- **pfSense**: Open-source firewall and router
- **Wazuh**: Security monitoring and SIEM solution
- **Multiple OS environments**: Windows 10, Ubuntu, Kali Linux
- **Network protocols**: TCP/IP, ICMP, DNS, HTTP/HTTPS

---

## Future Enhancements
Consider expanding this lab with:
- **IDS/IPS rules** configured in pfSense or Suricata
- **VLANs** for additional network segmentation
- **VPN server** for secure remote access
- **DNS filtering** and logging
- **Honeypot systems** to attract and analyze attacks
- **Traffic generation tools** for testing detection capabilities
