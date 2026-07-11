import sqlite3
import json
import datetime

DB_PATH = r'C:\Users\Lenovo\.local\share\mimocode\mimocode.db'
conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
c = conn.cursor()

# 1. Get all sessions in last 30 days (since Jun 11 2026)
cutoff = int((datetime.datetime(2026, 6, 11).timestamp() * 1000))
c.execute("""
    SELECT id, title, time_created, directory
    FROM session
    WHERE time_created > ?
    ORDER BY time_created DESC
""", (cutoff,))
sessions = [(r['id'], r['title'], r['time_created'], r['directory']) for r in c.fetchall()]
print(f"=== SESSIONS SINCE 2026-06-11: {len(sessions)} ===")
for sid, title, ts, d in sessions:
    dt = datetime.datetime.fromtimestamp(ts/1000).strftime('%m-%d %H:%M')
    print(f"  {dt} | {sid[:16]}... | {(title or 'N/A')[:70]} | {(d or '')[-30:]}")

# 2. Tool usage patterns - most common tools
c.execute("""
    SELECT json_extract(p.data, '$.tool') as tool,
           count(*) as n
    FROM message m
    JOIN part p ON p.message_id = m.id
    WHERE json_extract(m.data, '$.role') = 'assistant'
      AND json_extract(p.data, '$.type') = 'tool'
      AND m.time_created > ?
    GROUP BY tool
    ORDER BY n DESC
    LIMIT 20
""", (cutoff,))
print("\n=== TOOL USAGE (last 30 days) ===")
for r in c.fetchall():
    print(f"  {r['tool']}: {r['n']} calls")

# 3. Most common write/edit file patterns
c.execute("""
    SELECT json_extract(p.data, '$.state.input') as inp,
           count(*) as n
    FROM message m
    JOIN part p ON p.message_id = m.id
    WHERE json_extract(m.data, '$.role') = 'assistant'
      AND json_extract(p.data, '$.type') = 'tool'
      AND json_extract(p.data, '$.tool') = 'write'
      AND m.time_created > ?
    GROUP BY inp
    ORDER BY n DESC
    LIMIT 20
""", (cutoff,))
print("\n=== WRITE OPERATIONS (top 20 by frequency) ===")
for r in c.fetchall():
    inp = r['inp'][:150] if r['inp'] else 'N/A'
    print(f"  [{r['n']}x] {inp}")

# 4. User messages with repeated keywords
c.execute("""
    SELECT substr(json_extract(p.data, '$.text'), 1, 200) as txt, count(*) as n
    FROM message m
    JOIN part p ON p.message_id = m.id
    WHERE json_extract(m.data, '$.role') = 'user'
      AND json_extract(p.data, '$.type') = 'text'
      AND m.time_created > ?
    GROUP BY txt
    HAVING n > 1
    ORDER BY n DESC
    LIMIT 20
""", (cutoff,))
print("\n=== REPEATED USER MESSAGES ===")
for r in c.fetchall():
    print(f"  [{r['n']}x] {r['txt'][:120]}")

conn.close()
