from collections import defaultdict
from datetime import timedelta


def find_brute_force(events, threshold=20, window_minutes=5):
    """Detect at least threshold failed logins from one IP in any window."""
    failures_by_ip = defaultdict(list)
    for event in events:
        if event["status"] == "Failed":
            failures_by_ip[event["ip"]].append(event["timestamp"])

    window = timedelta(minutes=window_minutes)
    alerts = []
    for ip, times in failures_by_ip.items():
        times.sort()
        start = 0
        for end in range(len(times)):
            while times[end] - times[start] > window:
                start += 1
            count = end - start + 1
            if count >= threshold:
                alerts.append({"ip": ip, "failures": len(times),
                               "window_failures": count,
                               "first_seen": times[start]})
                break
    return alerts
