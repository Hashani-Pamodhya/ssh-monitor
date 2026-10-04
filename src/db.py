import psycopg2

CONN_INFO = dict(host="localhost", port=5432, dbname="sshmon",
                 user="monitor", password="monitor123")


def get_connection():
    return psycopg2.connect(**CONN_INFO)


def create_tables(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id SERIAL PRIMARY KEY,
                ts TIMESTAMP NOT NULL,
                ip TEXT NOT NULL,
                username TEXT,
                status TEXT NOT NULL
            )
        """)
    conn.commit()


def insert_events(conn, events):
    with conn.cursor() as cur:
        for e in events:
            cur.execute(
                "INSERT INTO events (ts, ip, username, status) VALUES (%s, %s, %s, %s)",
                (e["timestamp"], e["ip"], e["username"], e["status"]),
            )
    conn.commit()