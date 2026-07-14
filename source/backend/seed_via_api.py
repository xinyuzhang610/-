import pymysql
import requests

BASE = "http://localhost:8000/api"

# 删除刚才手动插入的用户（id >= 4）
conn = pymysql.connect(host='localhost', user='root', password='admin', database='zjiaotong', charset='utf8mb4')
cur = conn.cursor()
cur.execute("DELETE FROM usage_logs WHERE user_id >= 4")
cur.execute("DELETE FROM users WHERE id >= 4")
conn.commit()
print("Cleaned up manual users")

# 通过API注册用户（bcrypt哈希）
users = [
    {"username": "teacher_wang", "password": "123456", "role": "teacher", "name": "王老师", "school": "长沙市第一中学", "subject": "数学"},
    {"username": "teacher_li", "password": "123456", "role": "teacher", "name": "李老师", "school": "湖南师大附中", "subject": "语文"},
    {"username": "teacher_zhang", "password": "123456", "role": "teacher", "name": "张老师", "school": "长沙市雅礼中学", "subject": "英语"},
    {"username": "student_chen", "password": "123456", "role": "student", "name": "陈同学", "school": "长沙市第一中学", "grade": "高一"},
    {"username": "student_liu", "password": "123456", "role": "student", "name": "刘同学", "school": "湖南师大附中", "grade": "高二"},
    {"username": "student_zhao", "password": "123456", "role": "student", "name": "赵同学", "school": "长沙市雅礼中学", "grade": "高三"},
]

user_ids = {}
for u in users:
    try:
        r = requests.post(f"{BASE}/auth/register", json=u)
        data = r.json()
        user_ids[u["username"]] = data["id"]
        print(f"  Registered {u['username']} -> id={data['id']}")
    except Exception as e:
        print(f"  Failed {u['username']}: {e}")

# 添加使用记录
usage_records = [
    (user_ids["teacher_wang"], 1, "静夜思", "床前明月光...", "s001"),
    (user_ids["teacher_wang"], 7, "勾股定理", "勾股定理是...", "s002"),
    (user_ids["teacher_li"], 2, "我的梦想", "写作思路...", "s003"),
    (user_ids["student_chen"], 9, "逻辑题", "这道题的解法...", "s004"),
    (user_ids["student_liu"], 5, "apple", "单词卡片...", "s005"),
    (user_ids["teacher_wang"], 10, "错题分析", "错误原因...", "s006"),
    (user_ids["teacher_li"], 3, "人工智能", "名词解释...", "s007"),
    (user_ids["student_chen"], 8, "牛顿第一定律", "实验讲解...", "s008"),
    (user_ids["student_liu"], 11, "速度和速率", "概念辨析...", "s009"),
    (user_ids["student_zhao"], 13, "Python学习", "AI问答...", "s010"),
    (user_ids["teacher_wang"], 9, "逻辑推理", "逻辑题...", "s011"),
    (user_ids["teacher_li"], 1, "望庐山瀑布", "诗词赏析...", "s012"),
    (user_ids["student_chen"], 7, "二次方程", "公式推导...", "s013"),
    (user_ids["student_liu"], 14, "学习方法", "知识卡片...", "s014"),
    (user_ids["student_zhao"], 15, "历史事件", "思维导图...", "s015"),
    (user_ids["teacher_wang"], 12, "成绩分析", "数据分析...", "s016"),
    (user_ids["teacher_li"], 4, "阅读理解", "文章分析...", "s017"),
    (user_ids["student_chen"], 10, "数学错题", "错题分析...", "s018"),
    (user_ids["student_liu"], 8, "化学实验", "实验讲解...", "s019"),
    (user_ids["student_zhao"], 13, "英语学习", "AI问答...", "s020"),
    (user_ids["teacher_wang"], 1, "春望", "诗词赏析...", "s021"),
    (user_ids["teacher_li"], 2, "环保主题", "作文思路...", "s022"),
    (user_ids["student_chen"], 9, "逻辑题2", "逻辑推理...", "s023"),
    (user_ids["student_liu"], 5, "banana", "单词卡片...", "s024"),
    (user_ids["student_zhao"], 15, "地理知识", "思维导图...", "s025"),
]

for uid, tid, inp, out, sid in usage_records:
    cur.execute(
        "INSERT INTO usage_logs (user_id, tool_id, input_text, output_text, session_id) VALUES (%s,%s,%s,%s,%s)",
        (uid, tid, inp, out, sid)
    )

conn.commit()
print(f"Inserted {len(usage_records)} usage records")

# 更新工具使用次数
cur.execute("UPDATE tools SET usage_count = (SELECT COUNT(*) FROM usage_logs WHERE usage_logs.tool_id = tools.id)")
conn.commit()
print("Updated tool usage counts")

# 验证
for tbl in ['users', 'tools', 'usage_logs', 'recommend_rules']:
    cur.execute(f"SELECT COUNT(*) FROM {tbl}")
    cnt = cur.fetchone()[0]
    print(f"  {tbl}: {cnt}")

conn.close()
