import requests
import json

BASE = "http://localhost:8000/api"
passed = 0
failed = 0

def test(name, condition, detail=""):
    global passed, failed
    if condition:
        passed += 1
        print(f"  [PASS] {name} {detail}")
    else:
        failed += 1
        print(f"  [FAIL] {name} {detail}")

print("=== 后端API完整业务逻辑测试 ===\n")

# --- 1. 用户认证 ---
print("--- 用户认证 ---")

r = requests.post(BASE + "/auth/register", json={
    "username": "new_student", "password": "123456", "role": "student", "name": "新同学"
})
test("注册新用户", r.status_code == 200, "id=" + str(r.json().get("id", "")))

r = requests.post(BASE + "/auth/register", json={
    "username": "teacher_wang", "password": "123456", "role": "teacher"
})
test("重复注册拒绝", r.status_code == 400, "status=" + str(r.status_code))

r = requests.post(BASE + "/auth/login", json={
    "username": "teacher_wang", "password": "123456"
})
test("教师登录", r.status_code == 200 and "access_token" in r.json())

r = requests.post(BASE + "/auth/login", json={
    "username": "student_chen", "password": "123456"
})
test("学生登录", r.status_code == 200 and "access_token" in r.json())

r = requests.post(BASE + "/auth/login", json={
    "username": "teacher_wang", "password": "wrong"
})
test("错误密码拒绝", r.status_code == 401, "status=" + str(r.status_code))

r = requests.get(BASE + "/auth/profile/13")
test("获取用户信息", r.status_code == 200 and "username" in r.json())

r = requests.get(BASE + "/auth/profile/999")
test("获取不存在用户", r.status_code == 404, "status=" + str(r.status_code))

# --- 2. 工具管理 ---
print("\n--- 工具管理 ---")

r = requests.get(BASE + "/tools/presets")
test("获取预设工具", r.status_code == 200, "total=" + str(r.json()["total"]))

r = requests.get(BASE + "/tools/presets?category=文科")
test("文科筛选", r.status_code == 200, "total=" + str(r.json()["total"]))

r = requests.get(BASE + "/tools/presets?category=理科")
test("理科筛选", r.status_code == 200, "total=" + str(r.json()["total"]))

r = requests.get(BASE + "/tools/recommend?subject=数学&need_type=兴趣激发")
test("工具推荐(数学)", r.status_code == 200, "total=" + str(r.json()["total"]))

r = requests.get(BASE + "/tools/recommend?subject=语文&need_type=课前备课")
test("工具推荐(语文)", r.status_code == 200, "total=" + str(r.json()["total"]))

r = requests.post(BASE + "/tools/?creator_id=13", json={
    "name": "API测试工具", "description": "测试", "category": "文科",
    "subject": "语文", "prompt_template": "测试prompt", "icon": "test"
})
test("创建自定义工具", r.status_code == 200, "id=" + str(r.json().get("id", "")))

r = requests.get(BASE + "/tools/1")
test("获取单个工具", r.status_code == 200 and "name" in r.json())

r = requests.put(BASE + "/tools/18", json={
    "name": "已更新", "description": "更新", "category": "文科", "prompt_template": "更新"
})
test("更新工具", r.status_code == 200)

r = requests.delete(BASE + "/tools/18")
test("删除工具", r.status_code == 200)

r = requests.get(BASE + "/tools/1/share")
test("分享链接", r.status_code == 200 and "share_code" in r.json())

r = requests.get(BASE + "/tools/999")
test("获取不存在工具", r.status_code == 404, "status=" + str(r.status_code))

# --- 3. AI对话 ---
print("\n--- AI对话 ---")

r = requests.post(BASE + "/chat/", json={"message": "hello"})
test("通用AI对话", r.status_code == 200 and "reply" in r.json())

r = requests.post(BASE + "/chat/", json={"message": "勾股定理", "tool_id": 7})
test("工具专属对话", r.status_code == 200 and "reply" in r.json())

# --- 4. 使用统计 ---
print("\n--- 使用统计 ---")

r = requests.get(BASE + "/usage/dashboard")
d = r.json()
test("仪表板统计", r.status_code == 200, "tools=%d users=%d today=%d" % (d["total_tools"], d["total_users"], d["today_usage"]))

r = requests.get(BASE + "/usage/my?user_id=13")
test("我的使用记录", r.status_code == 200, "count=" + str(len(r.json())))

r = requests.get(BASE + "/usage/tool/1")
test("工具使用统计", r.status_code == 200, "total=" + str(r.json()["total_usage"]))

# --- 5. 推荐规则 ---
print("\n--- 推荐规则 ---")

r = requests.get(BASE + "/recommend/rules")
test("获取推荐规则", r.status_code == 200, "count=" + str(len(r.json())))

# --- 汇总 ---
print("\n" + "=" * 40)
print("测试结果: %d/%d 通过, %d 失败" % (passed, passed + failed, failed))
if failed == 0:
    print("全部通过!")
