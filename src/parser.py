import re
from datetime import datetime


# Older syslog format:
# Oct  2 10:15:01 server sshd[1234]: Failed password for user from 192.168.1.10 port 1234 ssh2
OLD_LINE_PATTERN = re.compile(
    r"^(?P<month>\w{3})\s+(?P<day>\d{1,2})\s+(?P<time>\d{2}:\d{2}:\d{2})\s+\S+\s+"
    r"sshd\[\d+\]:\s+(?P<status>Failed|Accepted) password for "
    r"(?:invalid user )?(?P<user>\S+) from (?P<ip>[0-9a-fA-F:.]+) port (?P<port>\d+)"
)


# Modern Ubuntu/WSL format:
# 2026-10-05T11:04:42.140864+05:30 Hashani sshd-session[2145]: Failed password for acer from 172.18.240.1 port 54756 ssh2
NEW_LINE_PATTERN = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2}T"
    r"\d{2}:\d{2}:\d{2}(?:\.\d+)?"
    r"(?:[+-]\d{2}:\d{2})?)\s+\S+\s+"
    r"sshd-session\[\d+\]:\s+"
    r"(?P<status>Failed|Accepted) password for "
    r"(?:invalid user )?(?P<user>\S+) from "
    r"(?P<ip>[0-9a-fA-F:.]+) port (?P<port>\d+)"
)


def parse_line(line, year=2026):
    """Return a dict for one SSH log line, or None if not interesting."""
    line = line.strip()

    # Try modern Ubuntu/WSL format first
    match = NEW_LINE_PATTERN.match(line)

    if match:
        timestamp = datetime.fromisoformat(match["timestamp"])
        timestamp = timestamp.replace(tzinfo=None)

        return {
            "timestamp": timestamp,
            "ip": match["ip"],
            "username": match["user"],
            "status": match["status"],
        }

    # Try older syslog format
    match = OLD_LINE_PATTERN.match(line)

    if match:
        text = f"{year} {match['month']} {match['day']} {match['time']}"
        timestamp = datetime.strptime(text, "%Y %b %d %H:%M:%S")

        return {
            "timestamp": timestamp,
            "ip": match["ip"],
            "username": match["user"],
            "status": match["status"],
        }

    return None


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