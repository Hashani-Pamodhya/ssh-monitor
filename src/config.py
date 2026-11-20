"""Environment-based configuration for SSH Monitor."""
import os

def env_int(name, default):
    try:
        return int(os.getenv(name, str(default)))
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer") from exc

LOG_FILE = os.getenv("SSH_LOG_FILE", "sample_logs/auth.log")
FAILURE_THRESHOLD = env_int("SSH_FAILURE_THRESHOLD", 20)
WINDOW_MINUTES = env_int("SSH_WINDOW_MINUTES", 5)
POLL_INTERVAL_SECONDS = env_int("SSH_POLL_INTERVAL_SECONDS", 2)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = env_int("DB_PORT", 5432)
DB_NAME = os.getenv("DB_NAME", "sshmon")
DB_USER = os.getenv("DB_USER", "monitor")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
