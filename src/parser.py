import re
from datetime import datetime

LINE_PATTERN = re.compile(
    r"^(?P<month>\w{3})\s+(?P<day>\d{1,2})\s+(?P<time>\d{2}:\d{2}:\d{2})\s+\S+\s+"
    r"sshd\[\d+\]:\s+(?P<status>Failed|Accepted) password for "
    r"(?:invalid user )?(?P<user>\S+) from (?P<ip>[0-9a-fA-F:.]+) port (?P<port>\d+)"
)


def parse_line(line, year=2026):
    """Return a dict for one SSH log line, or None if the line is not interesting."""
    match = LINE_PATTERN.match(line.strip())
    if not match:
        return None
    text = f"{year} {match['month']} {match['day']} {match['time']}"
    timestamp = datetime.strptime(text, "%Y %b %d %H:%M:%S")
    return {
        "timestamp": timestamp,
        "ip": match["ip"],
        "username": match["user"],
        "status": match["status"],
    }


def parse_file(path, year=2026):
    """Read a whole log file and return a list of events."""
    events = []
    try:
        with open(path, "r", errors="ignore") as f:
            for line in f:
                event = parse_line(line, year)
                if event:
                    events.append(event)
    except FileNotFoundError:
        print(f"File not found: {path}")
    return events