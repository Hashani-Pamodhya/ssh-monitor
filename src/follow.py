"""Polling-based follower for SSH authentication logs."""
import time
from pathlib import Path

def follow_file(path, poll_seconds=2):
    """Yield appended lines from a log file; seek to start after truncation."""
    log_path = Path(path)
    with log_path.open("r", errors="replace") as handle:
        handle.seek(0, 2)
        while True:
            line = handle.readline()
            if line:
                yield line
                continue
            try:
                if log_path.stat().st_size < handle.tell():
                    handle.seek(0)
            except FileNotFoundError:
                pass
            time.sleep(poll_seconds)
