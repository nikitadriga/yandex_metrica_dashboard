import sqlite3
from pathlib import Path

DB_PATH = Path("metrika.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_stats (
            date TEXT PRIMARY KEY,
            visits INTEGER,
            users INTEGER,
            pageviews INTEGER
        )
    """)

    conn.commit()
    conn.close()


def save_daily_stats(rows):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executemany("""
        INSERT OR REPLACE INTO daily_stats (date, visits, users, pageviews)
        VALUES (:date, :visits, :users, :pageviews)
    """, rows)

    conn.commit()
    conn.close()


def load_daily_stats():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT date, visits, users, pageviews
        FROM daily_stats
        ORDER BY date
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows
