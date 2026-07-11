import sqlite3
import json
import datetime
import re
from collections import Counter

DB_PATH = r'C:\Users\Lenovo\.local\share\mimocode\mimocode.db'
conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
c = conn.cursor()

cutoff = int((datetime.datetime(2026, 6, 11).timestamp() * 1000))

# 1. Find repeated bash commands (extracting the actual command)
c.execute("""
    SELECT json_extract(p.data, '$.state.input') as inp
    FROM message m
    JOIN part p ON p.message_id = m.id
    WHERE json_extract(m.data, '$.role') = 'assistant'
      AND json_extract(p.data, '$.type') = 'tool'
      AND json_extract(p.data, '$.tool') = 'bash'
      AND m.time_created > ?
""", (cutoff,))
commands = []
for r in c.fetchall():
    try:
        d = json.loads(r['inp']) if r['inp'] else {}
        cmd = d.get('command', '').strip()
        if cmd:
            # Normalize: remove paths, keep command structure
            commands.append(cmd)
    except:
        pass

print("=== REPEATED BASH COMMANDS (top 30) ===")
cmd_counter = Counter()
for cmd in commands:
    # Simplify: remove full paths to just see the pattern
    simplified = re.sub(r'[A-Z]:\\[^\s"]+', '<PATH>', cmd)
    cmd_counter[simplified] += 1
for cmd, n in cmd_counter.most_common(30):
    if n >= 2:
        print(f"  [{n}x] {cmd[:150]}")

# 2. Find repeated write file paths (what files get written most)
c.execute("""
    SELECT json_extract(p.data, '$.state.input') as inp
    FROM message m
    JOIN part p ON p.message_id = m.id
    WHERE json_extract(m.data, '$.role') = 'assistant'
      AND json_extract(p.data, '$.type') = 'tool'
      AND json_extract(p.data, '$.tool') = 'write'
      AND m.time_created > ?
""", (cutoff,))
write_paths = []
for r in c.fetchall():
    try:
        d = json.loads(r['inp']) if r['inp'] else {}
        fp = d.get('file_path', d.get('filePath', ''))
        if fp:
            # Normalize
            fp_norm = re.sub(r'\\[^\\]+$', '\\<FILE>', fp)
            write_paths.append(fp_norm)
    except:
        pass

print("\n=== REPEATED WRITE PATHS (top 20) ===")
wp_counter = Counter(write_paths)
for path, n in wp_counter.most_common(20):
    if n >= 2:
        print(f"  [{n}x] {path}")

# 3. Find repeated edit file paths
c.execute("""
    SELECT json_extract(p.data, '$.state.input') as inp
    FROM message m
    JOIN part p ON p.message_id = m.id
    WHERE json_extract(m.data, '$.role') = 'assistant'
      AND json_extract(p.data, '$.type') = 'tool'
      AND json_extract(p.data, '$.tool') = 'edit'
      AND m.time_created > ?
""", (cutoff,))
edit_paths = []
for r in c.fetchall():
    try:
        d = json.loads(r['inp']) if r['inp'] else {}
        fp = d.get('file_path', d.get('filePath', ''))
        if fp:
            edit_paths.append(fp)
    except:
        pass

print("\n=== REPEATED EDIT PATHS (top 20) ===")
ep_counter = Counter(edit_paths)
for path, n in ep_counter.most_common(20):
    if n >= 2:
        print(f"  [{n}x] {path[:120]}")

# 4. Find repeated webfetch/websearch URLs
c.execute("""
    SELECT json_extract(p.data, '$.tool') as tool,
           json_extract(p.data, '$.state.input') as inp
    FROM message m
    JOIN part p ON p.message_id = m.id
    WHERE json_extract(m.data, '$.role') = 'assistant'
      AND json_extract(p.data, '$.type') = 'tool'
      AND json_extract(p.data, '$.tool') IN ('webfetch', 'WebFetch', 'WebSearch')
      AND m.time_created > ?
""", (cutoff,))
web_urls = []
for r in c.fetchall():
    try:
        d = json.loads(r['inp']) if r['inp'] else {}
        url = d.get('url', d.get('query', ''))
        web_urls.append((r['tool'], url[:100] if url else ''))
    except:
        pass

print("\n=== WEB FETCH/SEARCH ===")
for tool, url in web_urls:
    print(f"  {tool}: {url}")

# 5. Find Python script creation patterns
c.execute("""
    SELECT json_extract(p.data, '$.state.input') as inp
    FROM message m
    JOIN part p ON p.message_id = m.id
    WHERE json_extract(m.data, '$.role') = 'assistant'
      AND json_extract(p.data, '$.type') = 'tool'
      AND json_extract(p.data, '$.tool') = 'write'
      AND m.time_created > ?
""", (cutoff,))
py_scripts = []
for r in c.fetchall():
    try:
        d = json.loads(r['inp']) if r['inp'] else {}
        fp = d.get('file_path', d.get('filePath', ''))
        content = d.get('content', '')
        if fp and fp.endswith('.py') and len(content) > 50:
            # Extract docstring/first comment to understand purpose
            lines = content.split('\n')
            purpose = ''
            for line in lines[:10]:
                line_stripped = line.strip()
                if line_stripped.startswith('#') or line_stripped.startswith('"""') or line_stripped.startswith("'''"):
                    purpose = line_stripped[:120]
                    break
            py_scripts.append((fp, purpose, len(content)))
    except:
        pass

print("\n=== PYTHON SCRIPTS CREATED ===")
for fp, purpose, length in py_scripts:
    print(f"  {fp[-60:]} ({length} chars) {purpose}")

conn.close()
