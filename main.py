from src.parser import parse_file
from src.detector import find_brute_force
from src.db import get_connection, create_tables, insert_events

events = parse_file("sample_logs/auth.log")
print(f"Parsed {len(events)} events")

alerts = find_brute_force(events)
for a in alerts:
    print(f"ALERT: {a['ip']} brute force, {a['failures']} failures, first seen {a['first_seen']}")

conn = get_connection()
create_tables(conn)
insert_events(conn, events)
conn.close()
print("Saved to database")