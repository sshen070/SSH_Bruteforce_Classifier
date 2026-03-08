import json
from collections import defaultdict
from pathlib import Path

# Find conn.log in repo
def find_conn_log(root: Path, log_name: str) -> Path:
    for path in root.rglob(log_name):
        return path
    raise FileNotFoundError(f"{log_name} not found under {root}")

def suspicious_activity_classifier():

    file = input('Enter file path: ')

    # Find input file in repo
    root = Path.cwd().resolve().parent
    
    # Input log file
    input_path = find_conn_log(root, file)
    print(f"Using conn.log at: {input_path}")

    # Output summary file
    output_path = Path('../data/ip_bruteforce_summary.json')

    # Dictionary to hold IP stats
    ip_stats = defaultdict(lambda: {"total": 0, "suspicious": 0, "benign": 0})

    with open(input_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            ip = entry.get("id.orig_h")
            conn_state = entry.get("conn_state")
            orig_bytes = entry.get("orig_ip_bytes", 0)
            resp_port = entry.get("id.resp_p")

            # Increment total connections per IP
            ip_stats[ip]["total"] += 1

            # Mark suspicious if conditions are met 
            if conn_state in {"RSTR", "RSTO"} and orig_bytes > 1000:
                ip_stats[ip]["suspicious"] += 1
            else:
                ip_stats[ip]["benign"] += 1

    # Prepare final list with ratios
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

    # Sort by ratio descending
    summary.sort(key=lambda x: x["conn_fail_ratio"], reverse=True)

    # Write to JSON
    with open(output_path, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"Summary written to {output_path}")


if __name__ == "__main__":
    suspicious_activity_classifier()
