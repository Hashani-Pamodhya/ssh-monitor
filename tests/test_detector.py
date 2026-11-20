from datetime import datetime, timedelta
from src.detector import find_brute_force


def make_events(ip, count, gap_seconds=1, status="Failed"):
    start = datetime(2026, 10, 2, 10, 0, 0)
    return [{"timestamp": start + timedelta(seconds=i * gap_seconds),
             "ip": ip, "username": "root", "status": status}
            for i in range(count)]


def test_default_threshold_detects_twenty_failures():
    assert len(find_brute_force(make_events("1.1.1.1", 20))) == 1


def test_default_threshold_ignores_nineteen_failures():
    assert find_brute_force(make_events("1.1.1.1", 19)) == []


def test_custom_threshold_is_supported():
    assert len(find_brute_force(make_events("1.1.1.1", 5), threshold=5)) == 1


def test_slow_attempts_outside_window_not_detected():
    assert find_brute_force(make_events("1.1.1.1", 5, gap_seconds=600), threshold=5) == []


def test_successful_logins_are_ignored():
    assert find_brute_force(make_events("1.1.1.1", 25, status="Accepted")) == []


def test_multiple_ips_are_separated():
    events = make_events("1.1.1.1", 20) + make_events("2.2.2.2", 2)
    alerts = find_brute_force(events)
    assert [a["ip"] for a in alerts] == ["1.1.1.1"]


def test_alert_reports_count_in_triggering_window():
    alert = find_brute_force(make_events("1.1.1.1", 22))[0]
    assert alert["window_failures"] == 20
