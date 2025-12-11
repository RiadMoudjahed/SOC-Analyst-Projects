###==== IMPORT LIBRARIES ====###
import re
import time
import argparse
import geoip2.database
import numpy as np
from datetime import datetime
from collections import defaultdict
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

###==== MAKE A CLI OF THE TOOL ====###
parser = argparse.ArgumentParser(description="Backdoor Activity Analyzer with ML")
parser.add_argument("--log","-l", required=False, help="Path to log file")
parser.add_argument("--window", "-w", choices=["10min", "hour"], default="10min", help="Time window size")
parser.add_argument("--threshold", "-ts", type=int, default=20, help="Minimum frequency (legacy mode)")
parser.add_argument("--ml", "-ml", action="store_true", help="Use ML-based anomaly detection")
parser.add_argument("--contamination", "-c", type=float, default=0.1, help="Expected proportion of anomalies (0.05-0.3)")
parser.add_argument("--sensitivity", "-s", choices=["low", "medium", "high"], default="medium", help="Detection sensitivity")
args = parser.parse_args()

###==== THE PATTERNS ====###
ip_pattern = re.compile(r"(?P<ip>(25[0-5]|2[0-4]\d|1\d{2}|[0-9]{1,3})(\.(25[0-5]|2[0-4]\d|1\d{2}|[0-9]{1,3})){3})")
time_pattern = re.compile(r"(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)")

###==== CREATE AUTO VALUE DICTIONARY ====###
windows_hour = defaultdict(set)
window_10min = defaultdict(set)
ip_timestamps = defaultdict(list)  # Store all timestamps per IP

###==== READ THE GEOIP DATABASE ====###
try:
    db_reader = geoip2.database.Reader("GeoLite2-City.mmdb")
except FileNotFoundError:
    print("Warning: GeoLite2-City.mmdb not found. Geographic features disabled.")
    db_reader = None

###==== DEFINING FUNCTIONS ====###
def get_geo_info(ip):
    if db_reader is None:
        return "GeoIP DB not available"
    try:
        response = db_reader.city(ip)
        country = response.country.name or "Unknown country"
        city = response.city.name or "Unknown city"
        return f"{country}, {city}"
    except geoip2.errors.AddressNotFoundError:
        return "Unknown location"
    except Exception as e:
        return f"Error: {e}"

def key_hour(dt):
    return dt.replace(minute=0, second=0)

def key_10min(dt):
    minute_bucket = dt.minute - (dt.minute % 10)
    return dt.replace(minute=minute_bucket, second=0)

def calculate_time_variance(timestamps):
    """Calculate variance in connection timing (irregularity score)"""
    if len(timestamps) < 2:
        return 0
    
    sorted_times = sorted(timestamps)
    intervals = [(sorted_times[i+1] - sorted_times[i]).total_seconds() 
                 for i in range(len(sorted_times)-1)]
    
    if len(intervals) == 0:
        return 0
    
    return np.std(intervals) if len(intervals) > 1 else 0

def calculate_connection_entropy(timestamps):
    """Measure randomness/predictability of connection times"""
    if len(timestamps) < 3:
        return 0
    
    sorted_times = sorted(timestamps)
    intervals = [(sorted_times[i+1] - sorted_times[i]).total_seconds() 
                 for i in range(len(sorted_times)-1)]
    
    # Calculate entropy of interval distribution
    if len(intervals) == 0:
        return 0
    
    # Bin intervals into categories
    bins = np.histogram(intervals, bins=10)[0]
    bins = bins[bins > 0]  # Remove empty bins
    
    if len(bins) == 0:
        return 0
    
    probs = bins / bins.sum()
    entropy = -np.sum(probs * np.log2(probs + 1e-10))
    
    return entropy

def detect_beaconing_simple(timestamps):
    """Detect periodic callback patterns (beaconing behavior)"""
    if len(timestamps) < 5:
        return False, 0, 0
    
    sorted_times = sorted(timestamps)
    intervals = [(sorted_times[i+1] - sorted_times[i]).total_seconds() 
                 for i in range(len(sorted_times)-1)]
    
    if len(intervals) == 0:
        return False, 0, 0
    
    # Check for consistent intervals (coefficient of variation)
    mean_interval = np.mean(intervals)
    std_interval = np.std(intervals)
    
    if mean_interval == 0:
        return False, 0, 0
    
    cv = std_interval / mean_interval  # Coefficient of variation
    
    # Low CV indicates regular, periodic behavior (beaconing)
    is_beaconing = cv < 0.3 and len(timestamps) >= 5
    
    return is_beaconing, mean_interval, cv

def extract_features(ip, frequency, windows, timestamps):
    """Extract multiple features for ML model"""
    features = {}
    
    # Feature 1: Connection frequency
    features['frequency'] = frequency
    
    # Feature 2: Number of unique time windows
    features['window_spread'] = len(windows)
    
    # Feature 3: Time variance (irregularity)
    features['time_variance'] = calculate_time_variance(timestamps)
    
    # Feature 4: Connection entropy
    features['entropy'] = calculate_connection_entropy(timestamps)
    
    # Feature 5: Beaconing detection
    is_beaconing, beacon_period, cv = detect_beaconing_simple(timestamps)
    features['beaconing_score'] = 1.0 if is_beaconing else 0.0
    features['beacon_period'] = beacon_period
    features['interval_cv'] = cv
    
    # Feature 6: Connections per window ratio
    features['density'] = frequency / len(windows) if len(windows) > 0 else 0
    
    # Feature 7: Time span (duration of activity)
    if len(timestamps) > 1:
        time_span = (max(timestamps) - min(timestamps)).total_seconds() / 3600  # in hours
        features['time_span'] = time_span
    else:
        features['time_span'] = 0
    
    return features

def ml_anomaly_detection(ip_frequency, ip_window, ip_timestamps, contamination=0.1):
    """Use Isolation Forest to detect anomalous IPs"""
    
    if len(ip_frequency) < 3:
        print("Not enough data for ML detection (minimum 3 IPs required)")
        return {}, {}
    
    print(f"\n[ML] Analyzing {len(ip_frequency)} unique IPs...")
    
    # Extract features for all IPs
    feature_list = []
    ip_list = []
    feature_dict = {}
    
    for ip, freq in ip_frequency.items():
        windows = ip_window[ip]
        timestamps = ip_timestamps[ip]
        
        features = extract_features(ip, freq, windows, timestamps)
        feature_dict[ip] = features
        
        # Create feature vector for ML model
        feature_vector = [
            features['frequency'],
            features['window_spread'],
            features['time_variance'],
            features['entropy'],
            features['beaconing_score'] * 100,  # Scale up
            features['density'],
            features['time_span']
        ]
        
        feature_list.append(feature_vector)
        ip_list.append(ip)
    
    # Convert to numpy array
    X = np.array(feature_list)
    
    # Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Train Isolation Forest
    print(f"[ML] Training Isolation Forest (contamination={contamination})...")
    clf = IsolationForest(
        contamination=contamination,
        random_state=42,
        n_estimators=100,
        max_samples='auto'
    )
    
    predictions = clf.fit_predict(X_scaled)
    anomaly_scores = clf.score_samples(X_scaled)
    
    # Create results dictionary
    results = {}
    for ip, pred, score in zip(ip_list, predictions, anomaly_scores):
        results[ip] = {
            'is_anomaly': pred == -1,
            'anomaly_score': score,
            'features': feature_dict[ip]
        }
    
    print(f"[ML] Detected {sum(1 for r in results.values() if r['is_anomaly'])} anomalous IPs")
    
    return results, feature_dict

def read_log(filepath):
    print(f"\n[*] Reading log file: {filepath}")
    line_count = 0
    
    with open(filepath, "r", encoding="utf-8") as file:
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
                
            windows_hour[k_hour].add(ip)
            window_10min[k_10].add(ip)
            ip_timestamps[ip].append(timestamp_dt)
            
            line_count += 1
    
    print(f"[*] Processed {line_count} log entries")
    print(f"[*] Found {len(ip_timestamps)} unique IPs")

def detect_repeated_ips(window_dict):
    ip_frequency = defaultdict(int)
    ip_window = defaultdict(list)
    for window, ip_set in window_dict.items():
        for ip in ip_set:
            ip_frequency[ip] += 1
            ip_window[ip].append(window)
    return ip_frequency, ip_window

###==== THE EXECUTION ====###
if not args.log:
    print("Error: --log argument is required")
    parser.print_help()
    exit(1)

read_log(args.log)

freq_10, window_10min_map = detect_repeated_ips(window_10min)
freq_hour, windows_hour_map = detect_repeated_ips(windows_hour)

if args.window == "10min":
    freq = freq_10
    win_dict = window_10min_map
else:
    freq = freq_hour
    win_dict = windows_hour_map

# Adjust contamination based on sensitivity
sensitivity_map = {
    'low': 0.05,
    'medium': 0.1,
    'high': 0.2
}
contamination = args.contamination if args.ml else sensitivity_map[args.sensitivity]

###==== DETECTION AND REPORTING ====###
if args.ml:
    # ML-based detection
    print(f"\n{'='*60}")
    print(f"ML-BASED ANOMALY DETECTION ({args.window} window)")
    print(f"{'='*60}")
    
    ml_results, features = ml_anomaly_detection(freq, win_dict, ip_timestamps, contamination)
    
    # Sort by anomaly score (most anomalous first)
    anomalous_ips = [(ip, data) for ip, data in ml_results.items() if data['is_anomaly']]
    anomalous_ips.sort(key=lambda x: x[1]['anomaly_score'])
    
    if len(anomalous_ips) == 0:
        print("\n✓ No anomalous IPs detected. System appears normal.")
    else:
        print(f"\n⚠ Found {len(anomalous_ips)} ANOMALOUS IPs:\n")
        
        for ip, data in anomalous_ips:
            location = get_geo_info(ip)
            feat = data['features']
            
            print(f"\n{'─'*60}")
            print(f"🔴 IP: {ip}")
            print(f"   Location: {location}")
            print(f"   Anomaly Score: {data['anomaly_score']:.4f} (lower = more suspicious)")
            print(f"\n   📊 Analysis:")
            print(f"      • Frequency: {feat['frequency']} connections")
            print(f"      • Time Windows: {feat['window_spread']} periods")
            print(f"      • Activity Duration: {feat['time_span']:.1f} hours")
            print(f"      • Connection Density: {feat['density']:.2f} conn/window")
            print(f"      • Time Variance: {feat['time_variance']:.2f}s")
            print(f"      • Entropy: {feat['entropy']:.3f}")
            
            if feat['beaconing_score'] > 0:
                print(f"      • ⚠ BEACONING DETECTED: {feat['beacon_period']:.0f}s intervals (CV: {feat['interval_cv']:.3f})")
            
            # Show sample timestamps
            print(f"\n   🕐 Sample Connection Times:")
            sample_times = sorted(ip_timestamps[ip])[:5]
            for t in sample_times:
                print(f"      - {t}")
            if len(ip_timestamps[ip]) > 5:
                print(f"      ... and {len(ip_timestamps[ip]) - 5} more")
        
        print(f"\n{'='*60}")

else:
    # Legacy threshold-based detection
    print(f"\n{'='*60}")
    print(f"THRESHOLD-BASED DETECTION ({args.window} window)")
    print(f"Threshold: {args.threshold} connections")
    print(f"{'='*60}")
    
    suspicious_ips = [ip for ip, count in freq.items() if count >= args.threshold]
    
    if len(suspicious_ips) == 0:
        print("\n✓ No suspicious IPs found above threshold.")
    else:
        print(f"\n⚠ Found {len(suspicious_ips)} IPs above threshold:\n")
        
        for ip in suspicious_ips:
            location = get_geo_info(ip)
            print(f"\n{ip:<15} | {location}")
            print(f"   Frequency: {freq[ip]} periods")
            print(f"   First 5 timestamps:")
            for w in win_dict[ip][:5]:
                print(f"      - {w}")
            if len(win_dict[ip]) > 5:
                print(f"      ... and {len(win_dict[ip]) - 5} more")

print("\n" + "="*60)
print("Analysis complete!")
print("="*60 + "\n")

# Cleanup
if db_reader:
    db_reader.close()
