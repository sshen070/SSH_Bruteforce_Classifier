import json
from collections import defaultdict
import math
from pathlib import Path

# Find conn.log in repo
def find_conn_log(root: Path, log_name: str) -> Path:
    for path in root.rglob(log_name):
        return path
    raise FileNotFoundError(f"{log_name} not found under {root}")

# Accept JSON file with set of connections --> Create JSON file containing SSH connection-fail ratio & other details
def conn_fail_ratio(input_path, output_path):
    # Dictionary to hold IP stats
    ip_stats = defaultdict(lambda: {"total": 0, "suspicious": 0, "benign": 0})

    # Try to load as standard JSON
    try:
        with open(input_path, "r") as f:
            data = json.load(f)
        if isinstance(data, dict):
            data = [data]
    except json.JSONDecodeError:
        data = []
        with open(input_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    data.append(entry)
                except json.JSONDecodeError:
                    continue

    # Process entries
    for entry in data:
        ip = entry.get("id.orig_h")
        conn_state = entry.get("conn_state")
        orig_bytes = entry.get("orig_ip_bytes", 0)

        if not ip:
            continue

        ip_stats[ip]["total"] += 1
        if conn_state in {"RSTR", "RSTO"} and orig_bytes > 1000:
            ip_stats[ip]["suspicious"] += 1
        else:
            ip_stats[ip]["benign"] += 1

    # Prepare summary
    summary = []
    for ip, stats in ip_stats.items():
        total = stats["total"]
        suspicious = stats["suspicious"]
        benign = stats["benign"]
        ratio = suspicious / total if total > 0 else 0
        summary.append({
            "ip": ip,
            "total_conn": total,
            "suspicious": suspicious,
            "benign": benign,
            "conn_fail_ratio": ratio
        })

    summary.sort(key=lambda x: (x["conn_fail_ratio"], x["total_conn"]), reverse=True)

    # Write summary JSON
    with open(output_path, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"Summary written to {output_path}")


# Creates a file containing the pkt_consistency for all ip addresses 
# Calculate the Coefficient of Variation (CV) ~ dipersion of packet amount over connections
# pkt_consistency(ip) = std(orig_pkts) / mean(orig_pkts)
def pkt_consistency(input_path, output_path):

    ip_pkts = defaultdict(list)

    # Collect packet counts per IP
    with open(input_path, "r") as f:
        for line in f:
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            ip = entry.get("id.orig_h")
            pkts = entry.get("orig_pkts")

            if ip is None or pkts is None:
                continue

            ip_pkts[ip].append(pkts)

    ip_consistency = []

    # Compute coefficient of variation per IP
    for ip, pkt_list in ip_pkts.items():

        if len(pkt_list) == 0:
            continue

        mean_val = sum(pkt_list) / len(pkt_list)

        variance = sum((x - mean_val) ** 2 for x in pkt_list) / len(pkt_list)
        std_val = math.sqrt(variance)

        consistency = std_val / mean_val if mean_val > 0 else 0

        ip_consistency.append({
            "ip": ip,
            "mean_orig_pkts": mean_val,
            "std_orig_pkts": std_val,
            "pkt_consistency": consistency,
            "total_conn": len(pkt_list),
        })

    # Sort by pkt_consistency descending
    ip_consistency.sort(key=lambda x: x["pkt_consistency"], reverse=True)

    # Write summary JSON
    with open(output_path, "w") as f:
        json.dump(ip_consistency, f, indent=2)

    print(f"Summary written to {output_path}")


def dest_ip_features(input_path, output_path):

    ip_total = defaultdict(int)

    # Use set to track if number of destination ip (set hashes dest ips & can check if ip exists in O(1)) 
    ip_dests = defaultdict(set)

    with open(input_path, "r") as f:
        for line in f:
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            ip = entry.get("id.orig_h")
            dest = entry.get("id.resp_h")

            if not ip:
                continue

            ip_total[ip] += 1

            if dest:
                ip_dests[ip].add(dest)

    results = []

    for ip in ip_total:

        total_conn = ip_total[ip]
        unique_dest = len(ip_dests[ip])

        dest_ratio = unique_dest / total_conn if total_conn > 0 else 0

        results.append({
            "ip": ip,
            "unique_dest_ips": unique_dest,
            "dest_ip_ratio": dest_ratio,
            "total_conn": total_conn
        })

    results.sort(key=lambda x: x["unique_dest_ips"], reverse=True)

    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"Summary written to {output_path}")

def main():

    user_input = int(input('conn_fail_ratio (1), pkt_consistency (2), dest_ip_features (3): '))
    input_file = input('Enter input file NAME: ')

    # Find input file in repo
    root = Path.cwd().resolve().parent
    
    # Input log file
    input_path = find_conn_log(root, input_file)
    print(f"Using conn.log at: {input_path}")

    # Output summary file
    output_file = input('Enter output file NAME: ').strip()
    output_path = Path('../data/ip_bruteforce_summary_logs') / output_file

    try:
        if (user_input == 1):
            conn_fail_ratio(input_path, output_path)

        elif (user_input == 2):
            pkt_consistency(input_path, output_path)

        elif (user_input == 3):
            dest_ip_features(input_path, output_path)

    except:
        print('ERROR')


if __name__ == "__main__":
    main()