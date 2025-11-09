###==== IMPORT LIBRARIES ====###
import re
import argparse
import time
from datetime import datetime
from collections import defaultdict

###==== MAKE A CLI OF THE TOOL ====###
parser = argparse.ArgumentParser(description="Backdoor Activity Analyzer")
parser.add_argument("--log","-l", required=True, help="Path to log file")
parser.add_argument("--window", "-w", choices=["10min", "hour"], default="10min", help="Time window size")
parser.add_argument("--threshold", "-ts", type=int, default=3, help="Minimum frequency to consider suspicious")
args = parser.parse_args()

###==== SET & FIND PATTERNS ====###
ip_pattern = re.compile(r"(?P<ip>(25[0-5]|2[0-4]\d|1\d{2}|[0-9]{1,3})(\.(25[0-5]|2[0-4]\d|1\d{2}|[0-9]{1,3})){3})")
time_pattern = re.compile(r"(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)")

windows_hour= defaultdict(set)
window_10min = defaultdict(set)

def key_hour(dt):
    return dt.replace(minute=0, second=0)

def key_10min(dt):
    minute_bucket = dt.minute - (dt.minute % 10)
    return dt.replace(minute=minute_bucket, second=0)

def key_minute(dt):
    return dt.replace(second=0)

def read_log(filepath):
    with open (filepath, "r", encoding="utf-8") as file:
        for line in file:
            src_ip = ip_pattern.search(line)
            timestamp = time_pattern.search(line)

            if not src_ip or not timestamp:
                continue

            ip = src_ip.group("ip")
            timestamp_str = timestamp.group("timestamp")
            timestamp_dt = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%SZ")
            

            k_hour = key_hour(timestamp_dt)
            k_10 = key_10min(timestamp_dt)
                
            windows_hour [k_hour].add(ip)
            window_10min [k_10].add (ip)

def detect_repeated_ips(window_dict):
    ip_frequency = defaultdict(int)
    ip_window = defaultdict(list)
    for window, ip_set in window_dict.items():
        for ip in ip_set:
            ip_frequency[ip] += 1
            ip_window[ip].append(window)
    return ip_frequency, ip_window

read_log(args.log)

freq_10, window_10min = detect_repeated_ips(window_10min)
freq_hour, windows_hour = detect_repeated_ips(windows_hour)

suspicious_ips = [ip for ip, count in freq_10.items() if count >= 3]

if args.window == "10min":
    freq, win_dict = detect_repeated_ips(window_10min)
else:
    freq, win_dict = detect_repeated_ips(windows_hour)

print(f"\n=== Suspicious IPs ({args.window} window) ===")

for ip in suspicious_ips:
    print (f"{ip:<15} | Frequency {freq_10[ip]} Periods | Times: ")
    for w in window_10min[ip]:
        try:
            print (f"   - {w}")
        except KeyboardInterrupt:
            print ("\n      Interrupted by the user - Exiting...")
            time.sleep(0.5)
            exit()
