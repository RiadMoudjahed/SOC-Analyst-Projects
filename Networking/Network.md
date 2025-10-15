# WELCOME

In this project, I am going to show you how to make a lab and configure the network with VMware.

---

### Our network should look like this 👇

<p align="center">
  <img src="https://github.com/user-attachments/assets/73a1ea38-87c6-48e3-81df-c7bd885950d1" alt="Network Diagram" width="600">
</p>

---

### Network Details

- **WAN:** `192.168.16.0/24` is the subnet IP of `VMnet8 > em0`, connecting the Virtual Machines and the host.  
- **pfSense:** `192.168.25.1` functions as a router and firewall, monitoring every device on the LAN.
- **Windows 10, Ubuntu, Kali Linux** are on the same LAN which are connected to **pfSense**.

---

### pfSense Network Layout 👇

<p align="center">
  <img src="https://github.com/user-attachments/assets/4563aad6-39bf-4b5f-b2a5-01aa7ba3ea97" alt="pfSense Network Diagram" width="700">
</p>
