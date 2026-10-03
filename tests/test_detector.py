
from datetime import datetime, timedelta
from src.detector import find_brute_force


def make_events(ip, count, gap_seconds=1, status="Failed"):
    start = datetime(2026, 10, 2, 10, 0, 0)
    return [
        {"timestamp": start + timedelta(seconds=i * gap_seconds),
         "ip": ip, "username": "root", "status": status}
        for i in range(count)
    ]


def test_exactly_at_threshold_is_detected():
    assert len(find_brute_force(make_events("1.1.1.1", 5))) == 1


def test_just_below_threshold_is_not_detected():
    assert find_brute_force(make_events("1.1.1.1", 4)) == []


def test_slow_attempts_outside_window_not_detected():
    # 5 failures but 10 minutes apart each: not a brute force
    assert find_brute_force(make_events("1.1.1.1", 5, gap_seconds=600)) == []


def test_successful_logins_are_ignored():
    assert find_brute_force(make_events("1.1.1.1", 10, status="Accepted")) == []


def test_multiple_ips_are_separated():
    events = make_events("1.1.1.1", 5) + make_events("2.2.2.2", 2)
    alerts = find_brute_force(events)
    assert [a["ip"] for a in alerts] == ["1.1.1.1"]