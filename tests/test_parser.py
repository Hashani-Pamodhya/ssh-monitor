import pytest
from src.parser import parse_line, parse_file


def test_failed_password_line():
    line = "Oct  2 10:15:01 server sshd[1234]: Failed password for root from 203.0.113.5 port 54321 ssh2"
    result = parse_line(line)
    assert result["ip"] == "203.0.113.5"
    assert result["username"] == "root"
    assert result["status"] == "Failed"


def test_invalid_user_line():
    line = "Oct  2 10:15:05 server sshd[1234]: Failed password for invalid user admin from 203.0.113.5 port 54323 ssh2"
    result = parse_line(line)
    assert result["username"] == "admin"


def test_accepted_line():
    line = "Oct  2 10:22:00 server sshd[1241]: Accepted password for hashani from 198.51.100.7 port 50001 ssh2"
    assert parse_line(line)["status"] == "Accepted"


@pytest.mark.parametrize("bad_line", [
    "",
    "garbage text",
    "Oct  2 10:15:01 server sshd[1234]: Failed password for",
    "\x00\x01\x02",
])
def test_bad_lines_return_none(bad_line):
    assert parse_line(bad_line) is None


def test_missing_file_does_not_crash():
    assert parse_file("this_file_does_not_exist.log") == []


def test_parse_sample_file():
    events = parse_file("tests/data/test_auth.log")
    assert len(events) == 10