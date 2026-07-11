import sqlite3
import json
import os

DB_PATH = r'C:\Users\Lenovo\.local\share\mimocode\mimocode.db'
conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
c = conn.cursor()

# 1. List tables
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in c.fetchall()]
print("=== TABLES ===")
print(tables)

# 2. Schema
for t in tables:
    c.execute(f"SELECT sql FROM sqlite_master WHERE name='{t}'")
    row = c.fetchone()
    if row:
        print(f"\n--- Schema: {t} ---")
        print(row[0])

# 3. Session count and date range
print("\n=== SESSION SUMMARY ===")
c.execute("SELECT count(*) FROM session")
print(f"Total sessions: {c.fetchone()[0]}")

# 4. Recent sessions (last 30 days)
c.execute("""
    SELECT id, title, time_created, directory
    FROM session
    ORDER BY time_created DESC
    LIMIT 30
""")
print("\n=== RECENT 30 SESSIONS ===")
for r in c.fetchall():
    import datetime
    ts = r[2]
    if ts:
        dt = datetime.datetime.fromtimestamp(ts/1000)
        date_str = dt.strftime('%Y-%m-%d %H:%M')
    else:
        date_str = "N/A"
    print(f"  {r[0]} | {date_str} | {r[1][:80] if r[1] else 'N/A'} | {r[3][:60] if r[3] else 'N/A'}")

conn.close()
