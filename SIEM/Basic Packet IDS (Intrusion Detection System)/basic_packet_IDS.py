### ==== IMPORT LIBRARIES ==== ###
from scapy.all import sniff, IP, Raw
import threading

### ==== Core State and Control Variables ==== ###
suspicious_packets= []  # Empty list to contain the suspicious packets
last_suspicious = None  # Threat Status Indicator
MALWARE_SIGNATURE = b'\xDE\xAD\xBE\xEF\xC0\xFF\xEE' # An example of a malware signature, which our IDS is based on
STOP_FLAG = threading.Event()  # A synchronization tool that is used to stop the threading clearly

print ("\n      ======= Packets Captured =======\n")

### ==== DEFINE THE SNIFFING FUNCTION ==== ###
def sniff_packets():    # The function that is responsible for sniffing the packets
    sniff(
        prn=packet_capture,    # Each captured packet is passed to the "packet_capture" function, which checks its payload (Raw Payload) for the suspicious signature (MALWARE_SIGNATURE).
        filter="ip",    # It ensures that only packets containing the IP layer are captured and processed, increasing the efficiency of the tool and reducing unnecessary traffic (such as ARP).
        store=False,    # Preventing the storage of all captured packets frees up a significant amount of memory.
        stop_filter=lambda p: STOP_FLAG.is_set()    # This function uses lambda to check if "STOP_FLAG" (a 'threading.Event' that is activated when the user presses Enter) is set. This is the mechanism that ensures the capture process stops cleanly and safely.
    )


### ==== DEFINE THE CAPTURING FUNCTIONG ==== ###
def packet_capture(packet):
    global last_suspicious

    if IP not in packet: 
        print ("No packet captured...")
        return

    src_ip = packet[IP].src   # Get the source IP of the packet
    dst_ip = packet[IP].dst   # Get the destination IP of the packet
    
    if Raw in packet:
        raw_data = packet[Raw].load   # Get the RAW data of the packet
            
        if MALWARE_SIGNATURE in raw_data:
            print(f"[SUSPICIOUS!!]  {src_ip} -> {dst_ip}")
            suspicious_packets.append(packet)   # Append the suspicious packet (It save it on the list to print it later)
            last_suspicious = (src_ip, dst_ip)
        else:
            print(f"[PASS]  {src_ip} -> {dst_ip}")
    else:
        print(f"[NO RAW DATA] {src_ip} -> {dst_ip}") 

### ==== DEFINE THE MAIN FUNCTIONG ==== ###
def main():
    thread = threading.Thread(target=sniff_packets)   # Create a threading for the 'sniff_packets' function
    thread.start()   # Start threading

    try:
        input("Press Enter to stop...\n")   # Quit the tool by pressing ENTER
    except KeyboardInterrupt:
        print ("Interrupted by user...")    

    STOP_FLAG.set()   # This function changes the internal state of STOP_FLAG from False (not set) to True (set/enabled).
    thread.join()   # It makes the main thread (which executes the main function) wait until the specified thread has completely finished executing it.

### ==== SHOWING THE RESULTS ==== ###
    print ("\n      ======= RESULTS =======  \n")
    if last_suspicious:
        print(f"Suspicious Packets Found: {len(suspicious_packets)}\n")   # Show how many suspicious packets found

        for i, packet in enumerate(suspicious_packets, 1):  # The `enumerate` function is used to provide an index (i) for each item, and the enumeration starts from 1 for user-friendly display.
            src = packet[IP].src    # The IP layer within the packet (packet[IP]) is accessed, and then the source IP address field (src) is extracted from it.
            dst = packet[IP].dst    # The IP layer within the packet (packet[IP]) is accessed, and then the destination IP address field (dst) is extracted from it.
            print (f"[{i}] {src} -> {dst}")   # Print the packet number (i) followed by the source IP address and the destination IP address, for each packet detected.
    else:
        print ("No suspicious packets found.")  

if __name__ == "__main__":
    main()
