"""SSH Monitor CLI: analyze a file or follow a live SSH auth log."""
import argparse
from collections import deque
from datetime import timedelta
from src.config import LOG_FILE, FAILURE_THRESHOLD, WINDOW_MINUTES, POLL_INTERVAL_SECONDS
from src.parser import parse_file, parse_line
from src.detector import find_brute_force
from src.db import get_connection, create_tables, insert_events
from src.follow import follow_file


def main():
    cli = argparse.ArgumentParser(description="SSH authentication log monitor")
    cli.add_argument("--log-file", default=LOG_FILE)
    cli.add_argument("--follow", action="store_true", help="Follow appended log entries")
    args = cli.parse_args()
    conn = get_connection()
    create_tables(conn)
    try:
        if not args.follow:
            events = parse_file(args.log_file)
            print(f"Parsed {len(events)} events from {args.log_file}")
            alerts = find_brute_force(events, FAILURE_THRESHOLD, WINDOW_MINUTES)
            for a in alerts:
                print(f"ALERT: {a['ip']} - {a['window_failures']} failures within {WINDOW_MINUTES} minutes")
            insert_events(conn, events)
            print("Saved events to PostgreSQL")
            return
        print(f"Following {args.log_file}; press Ctrl+C to stop")
        recent = deque()
        alerted = set()
        for line in follow_file(args.log_file, POLL_INTERVAL_SECONDS):
            event = parse_line(line)
            if not event:
                continue
            insert_events(conn, [event])
            if event["status"] != "Failed":
                continue
            recent.append(event)
            cutoff = event["timestamp"] - timedelta(minutes=WINDOW_MINUTES)
            while recent and recent[0]["timestamp"] < cutoff:
                recent.popleft()
            for alert in find_brute_force(list(recent), FAILURE_THRESHOLD, WINDOW_MINUTES):
                key = (alert["ip"], alert["first_seen"])
                if key not in alerted:
                    print(f"ALERT: {alert['ip']} - {alert['window_failures']} failures within {WINDOW_MINUTES} minutes")
                    alerted.add(key)
    except KeyboardInterrupt:
        print("\nMonitor stopped")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
