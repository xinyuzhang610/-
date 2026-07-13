import pymysql

conn = pymysql.connect(host='localhost', user='root', password='admin', database='zjiaotong', charset='utf8mb4')
cur = conn.cursor()

sql = """INSERT INTO recommend_rules (subject, need_type, tool_ids, priority) VALUES
('语文', '兴趣激发', '["1","6"]', 1),
('语文', '课前备课', '["2","4"]', 1),
('数学', '兴趣激发', '["9","12"]', 1),
('数学', '课前备课', '["7","10"]', 1),
('英语', '兴趣激发', '["5","13"]', 1),
('物理', '兴趣激发', '["8","11"]', 1),
('通用', '兴趣激发', '["13","14","15"]', 1)"""

cur.execute(sql)
conn.commit()
print(f"Inserted {cur.rowcount} recommend rules")

# Update tool usage counts
cur.execute("UPDATE tools SET usage_count = (SELECT COUNT(*) FROM usage_logs WHERE usage_logs.tool_id = tools.id)")
conn.commit()
print(f"Updated {cur.rowcount} tool usage counts")

# Verify all data
for tbl in ['users', 'tools', 'tool_templates', 'usage_logs', 'favorites', 'recommend_rules']:
    cur.execute(f"SELECT COUNT(*) FROM {tbl}")
    cnt = cur.fetchone()[0]
    print(f"  {tbl}: {cnt}")

conn.close()
