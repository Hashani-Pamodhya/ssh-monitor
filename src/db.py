import psycopg2
from src.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


def get_connection():
    if not DB_PASSWORD:
        raise RuntimeError("DB_PASSWORD is not set. Copy .env.example to .env and configure it.")
    return psycopg2.connect(host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
                            user=DB_USER, password=DB_PASSWORD)


def create_tables(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id BIGSERIAL PRIMARY KEY,
                ts TIMESTAMPTZ NOT NULL,
                ip TEXT NOT NULL,
                username TEXT,
                status TEXT NOT NULL,
                UNIQUE (ts, ip, username, status)
            )
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_events_ip_ts ON events (ip, ts)")
    conn.commit()


def insert_events(conn, events):
    with conn.cursor() as cur:
        cur.executemany("""
            INSERT INTO events (ts, ip, username, status)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (ts, ip, username, status) DO NOTHING
        """, [(e["timestamp"], e["ip"], e["username"], e["status"]) for e in events])
    conn.commit()
