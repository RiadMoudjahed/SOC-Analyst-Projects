###==== IMPORT LIBRARIES ====###
import re
import time
import argparse
import geoip2.database
from datetime import datetime
from collections import defaultdict

###==== MAKE A CLI OF THE TOOL ====###
parser = argparse.ArgumentParser(description="Backdoor Activity Analyzer")
parser.add_argument("--log","-l", required=True, help="Path to log file")
parser.add_argument("--window", "-w", choices=["10min", "hour"], default="10min", help="Time window size")
parser.add_argument("--threshold", "-ts", type=int, default=20, help="Minimum frequency to consider suspicious")
args = parser.parse_args()

###==== THE PATTERNS ====###
ip_pattern = re.compile(r"(?P<ip>(25[0-5]|2[0-4]\d|1\d{2}|[0-9]{1,3})(\.(25[0-5]|2[0-4]\d|1\d{2}|[0-9]{1,3})){3})")
time_pattern = re.compile(r"(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)")

###==== CREATE AUTO VALUE DICTIONARY ====###
windows_hour= defaultdict(set)
window_10min = defaultdict(set)

###==== READ THE GEOIP DATABASE ====###
db_reader = geoip2.database.Reader("E:/your/path/to/GeoLite2-City.mmdb")

###==== DEFINING FUNCTIONS ====###
def get_geo_info(ip):
    try:
        response = db_reader.city(ip)    # GET THE LOCATION FROM THE DB BASED ON THE IP
        country = response.country.name or "Unknown country"    # GET COUNTRY NAME
        city = response.city.name or "Unknown city"    # GET CITY NAME
        return f"{country}, {city}"
    except geoip2.errors.AddressNotFoundError:
        return "Unknown location"    # LOCATION NOT FOUND
    except Exception as e:
        return f"Error: {e}"    # INVALID IP ADDRESS, INVALID DB...etc

def key_hour(dt):
    return dt.replace(minute=0, second=0)    # GET HOURLY PERIODS

def key_10min(dt):
    minute_bucket = dt.minute - (dt.minute % 10)    # ROUND DOWN TIMESTAMP TO THE NEAREST 10-MINUTES WINDOW (e.g; 10:27 → 10:20)
    return dt.replace(minute=minute_bucket, second=0)    # NULL SECONDS, WE ONLY NEEED MINUTES

def key_minute(dt):
    return dt.replace(second=0)    # GET THE TIME WITHOUT SECONDS

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

###==== THE EXECUTION ====###
read_log(args.log)

freq_10, window_10min_map = detect_repeated_ips(window_10min)
freq_hour, windows_hour_map = detect_repeated_ips(windows_hour)

if args.window == "10min":
    freq = freq_10
    win_dict = window_10min_map
else:
    freq = freq_hour
    win_dict = windows_hour_map

###==== PRINTING THE RESULTS ====###
print(f"\n=== Suspicious IPs ({args.window} window) ===")

suspicious_ips = [ip for ip, count in freq.items() if count >= args.threshold]

for ip in suspicious_ips:
    location = get_geo_info(ip)
    print (f"{ip:<15} | {location} | Frequency {freq[ip]} Periods | Times: ")
    for w in window_10min_map[ip]:
        try:
            print (f"   - {w}")
        except KeyboardInterrupt:
            print ("\n      Interrupted by the user - Exiting...")
            time.sleep(0.5)
            exit()
