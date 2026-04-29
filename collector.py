from metrika_client import get_daily_stats
from database import init_db, save_daily_stats


def main():
    init_db()
    rows = get_daily_stats()
    save_daily_stats(rows)
    print(f"Saved {len(rows)} daily rows to SQLite.")


if __name__ == "__main__":
    main()
