# WELCOME

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

