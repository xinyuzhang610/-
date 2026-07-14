# 智教通 - 详细任务模块划分

> 更新时间：2026-07-12
> 基于：实施计划 + 实际代码状态

---

## 一、任务状态总览

| 阶段 | 任务编号 | 任务名称 | 代码状态 | 验证状态 |
|------|----------|----------|----------|----------|
| **Phase 1** | T1 | 数据库初始化 | ✅ 已创建 | ❌ 未验证 |
| **Phase 1** | T2 | 工具CRUD API | ✅ 已创建 | ❌ 未验证 |
| **Phase 1** | T3 | AI对话API | ✅ 已创建 | ❌ 未验证 |
| **Phase 2** | T4 | 使用统计API | ✅ 已创建 | ❌ 未验证 |
| **Phase 2** | T5 | 推荐逻辑API | ✅ 已创建 | ❌ 未验证 |
| **Phase 2** | T6 | 工具广场API | ✅ 已创建 | ❌ 未验证 |
| **Phase 3** | T7 | 路由与布局 | ✅ 已创建 | ❌ 未验证 |
| **Phase 3** | T8 | 登录注册页面 | ✅ 已创建 | ❌ 未验证 |
| **Phase 3** | T9 | API服务层 | ✅ 已创建 | ❌ 未验证 |
| **Phase 4** | T10 | 教师端-需求引导 | ✅ 已创建 | ❌ 未验证 |
| **Phase 4** | T11 | 教师端-工具管理 | ✅ 已创建 | ❌ 未验证 |
| **Phase 4** | T12 | 教师端-数据看板 | ✅ 已创建 | ❌ 未验证 |
| **Phase 4** | T13 | 学生端-需求引导 | ✅ 已创建 | ❌ 未验证 |
| **Phase 4** | T14 | 学生端-工具广场 | ✅ 已创建 | ❌ 未验证 |
| **Phase 4** | T15 | 学生端-AI问答/工具使用/记录 | ✅ 已创建 | ❌ 未验证 |
| **Phase 5** | T16 | 前后端集成 | ❌ 待修改 | ❌ 未验证 |
| **Phase 5** | T17 | 最终测试与文档 | ❌ 待创建 | ❌ 未验证 |

**状态说明：**
- ✅ 已创建：代码文件已存在
- ❌ 未验证：未启动运行测试
- ❌ 待修改/待创建：需要新建或修改代码

---

## 二、详细任务流程

### Phase 1: 后端基础 (T1-T3)

#### T1: 数据库初始化

**目标：** 创建数据库表结构和种子数据

**文件清单：**
- `source/backend/init_db.py` ✅
- `source/backend/sql/init.sql` ✅
- `source/backend/sql/seed.sql` ✅

**执行流程：**
```
Step 1: 检查MySQL服务是否运行
        → 命令: mysql -u root -p
        → 预期: 出现MySQL提示符

Step 2: 运行初始化脚本
        → 命令: cd source/backend && python init_db.py
        → 预期: "Database initialized successfully"

Step 3: 验证表结构
        → 命令: mysql -u root -p zjiaotong -e "SHOW TABLES;"
        → 预期: 6张表 (users, tools, tool_templates, usage_logs, favorites, recommend_rules)

Step 4: 验证种子数据
        → 命令: mysql -u root -p zjiaotong -e "SELECT COUNT(*) FROM tool_templates;"
        → 预期: 15 (6文科 + 6理科 + 3通用)
```

**验收标准：**
- [ ] 数据库zjiaotong创建成功
- [ ] 6张表结构正确
- [ ] 种子数据完整插入
- [ ] 无SQL错误

**验收人：** 人工检查
**预计耗时：** 10分钟

---

#### T2: 工具CRUD API

**目标：** 实现工具管理的RESTful接口

**文件清单：**
- `source/backend/api/tool.py` ✅
- `source/backend/schemas/tool.py` ✅
- `source/backend/main.py` ✅ (已注册路由)

**执行流程：**
```
Step 1: 启动后端服务
        → 命令: cd source/backend && python main.py
        → 预期: 服务启动在 http://localhost:8000

Step 2: 测试获取预设工具
        → 命令: curl http://localhost:8000/api/tools/presets
        → 预期: JSON返回预设工具列表

Step 3: 测试获取单个工具
        → 命令: curl http://localhost:8000/api/tools/1
        → 预期: JSON返回工具详情

Step 4: 测试创建工具
        → 命令: curl -X POST http://localhost:8000/api/tools/ -H "Content-Type: application/json" -d '{"name":"测试工具","category":"文科","prompt_template":"测试提示词"}' -G -d "creator_id=1"
        → 预期: 返回创建的工具信息

Step 5: 测试推荐接口
        → 命令: curl "http://localhost:8000/api/tools/recommend?subject=语文&need_type=兴趣激发"
        → 预期: 返回推荐工具列表
```

**验收标准：**
- [ ] GET /api/tools/presets 返回预设工具
- [ ] GET /api/tools/{id} 返回工具详情
- [ ] POST /api/tools/ 创建工具成功
- [ ] PUT /api/tools/{id} 更新工具成功
- [ ] DELETE /api/tools/{id} 删除工具成功
- [ ] GET /api/tools/recommend 推荐逻辑正确

**验收人：** curl命令验证
**预计耗时：** 15分钟

---

#### T3: AI对话API

**目标：** 集成DeepSeek API实现AI对话

**文件清单：**
- `source/backend/api/chat.py` ✅
- `source/backend/services/deepseek.py` ✅
- `source/backend/schemas/chat.py` ✅

**执行流程：**
```
Step 1: 检查.env配置
        → 文件: source/backend/.env
        → 当前状态: DEEPSEEK_API_KEY=your_api_key_here (需替换为真实key)

Step 2: 测试基础对话
        → 命令: curl -X POST http://localhost:8000/api/chat/ -H "Content-Type: application/json" -d '{"message":"你好"}'
        → 预期: 返回AI回复 (mock模式或真实回复)

Step 3: 测试带工具的对话
        → 命令: curl -X POST http://localhost:8000/api/chat/ -H "Content-Type: application/json" -d '{"message":"静夜思","tool_id":1}'
        → 预期: 使用工具提示词的AI回复

Step 4: 验证使用日志记录
        → 命令: mysql -u root -p zjiaotong -e "SELECT COUNT(*) FROM usage_logs;"
        → 预期: 使用次数增加
```

**验收标准：**
- [ ] POST /api/chat/ 基础对话正常
- [ ] POST /api/chat/ 带tool_id的对话正常
- [ ] 使用日志正确记录
- [ ] Mock模式和真实API模式可切换

**验收人：** curl命令 + 数据库验证
**预计耗时：** 20分钟 (含配置API Key)

---

### Phase 2: 后端业务逻辑 (T4-T6)

#### T4: 使用统计API

**目标：** 实现使用数据统计和看板接口

**文件清单：**
- `source/backend/api/usage.py` ✅
- `source/backend/schemas/usage.py` ✅

**执行流程：**
```
Step 1: 测试获取个人使用记录
        → 命令: curl "http://localhost:8000/api/usage/my?user_id=1"
        → 预期: 返回使用记录列表

Step 2: 测试工具使用统计
        → 命令: curl http://localhost:8000/api/usage/tool/1
        → 预期: 返回总使用次数和今日使用次数

Step 3: 测试看板数据
        → 命令: curl http://localhost:8000/api/usage/dashboard
        → 预期: 返回统计数据(工具数、用户数、今日使用、周趋势、热门工具、最近记录)
```

**验收标准：**
- [ ] GET /api/usage/my 返回个人记录
- [ ] GET /api/usage/tool/{id} 统计正确
- [ ] GET /api/usage/dashboard 数据完整

**验收人：** curl命令验证
**预计耗时：** 10分钟

---

#### T5: 推荐逻辑API

**目标：** 实现3步需求引导推荐

**文件清单：**
- `source/backend/api/recommend.py` ✅
- `source/backend/schemas/recommend.py` ✅

**执行流程：**
```
Step 1: 测试步骤1 - 文理分科
        → 命令: curl -X POST http://localhost:8000/api/recommend/ -H "Content-Type: application/json" -d '{"step":1}'
        → 预期: 返回文科/理科选项

Step 2: 测试步骤2 - 需求选择
        → 命令: curl -X POST http://localhost:8000/api/recommend/ -H "Content-Type: application/json" -d '{"step":2,"category":"文科"}'
        → 预期: 返回文科需求选项

Step 3: 测试步骤3 - 获取推荐
        → 命令: curl -X POST http://localhost:8000/api/recommend/ -H "Content-Type: application/json" -d '{"step":3,"category":"文科","need_type":"兴趣激发"}'
        → 预期: 返回推荐工具列表
```

**验收标准：**
- [ ] Step 1 返回正确的分科选项
- [ ] Step 2 返回正确的需求选项
- [ ] Step 3 返回正确的推荐工具
- [ ] if-else匹配逻辑正确 (非AI)

**验收人：** curl命令验证
**预计耗时：** 10分钟

---

#### T6: 工具广场API

**目标：** 实现工具浏览、分类、搜索

**文件清单：**
- `source/backend/api/plaza.py` ✅
- `source/backend/schemas/plaza.py` ✅

**执行流程：**
```
Step 1: 测试获取广场数据
        → 命令: curl http://localhost:8000/api/plaza/
        → 预期: 返回分类列表、工具列表、热门工具

Step 2: 测试分类筛选
        → 命令: curl "http://localhost:8000/api/plaza/?category=文科"
        → 预期: 只返回文科工具

Step 3: 测试搜索
        → 命令: curl "http://localhost:8000/api/plaza/?search=诗词"
        → 预期: 返回包含"诗词"的工具

Step 4: 测试热门工具
        → 命令: curl http://localhost:8000/api/plaza/hot
        → 预期: 返回按使用次数排序的工具
```

**验收标准：**
- [ ] GET /api/plaza/ 返回完整数据
- [ ] 分类筛选正确
- [ ] 搜索功能正常
- [ ] 热门工具排序正确

**验收人：** curl命令验证
**预计耗时：** 10分钟

---

### Phase 3: 前端基础 (T7-T9)

#### T7: 路由与布局

**目标：** 配置前端路由和布局组件

**文件清单：**
- `source/frontend/src/router/index.js` ✅
- `source/frontend/src/layouts/TeacherLayout.vue` ✅
- `source/frontend/src/layouts/StudentLayout.vue` ✅

**执行流程：**
```
Step 1: 启动前端开发服务器
        → 命令: cd source/frontend && npm run dev
        → 预期: 服务启动在 http://localhost:5173

Step 2: 测试教师端布局
        → 浏览器: http://localhost:5173/teacher
        → 预期: 显示教师端侧边栏布局

Step 3: 测试学生端布局
        → 浏览器: http://localhost:5173/student
        → 预期: 显示学生端顶部导航布局

Step 4: 测试路由跳转
        → 点击菜单项验证页面切换
```

**验收标准：**
- [ ] /teacher 显示教师布局
- [ ] /student 显示学生布局
- [ ] 菜单导航正常工作
- [ ] 页面切换无报错

**验收人：** 浏览器验证
**预计耗时：** 10分钟

---

#### T8: 登录注册页面

**目标：** 实现用户认证界面

**文件清单：**
- `source/frontend/src/views/auth/Login.vue` ✅
- `source/frontend/src/views/auth/Register.vue` ✅
- `source/frontend/src/api/auth.js` ✅

**执行流程：**
```
Step 1: 测试注册页面
        → 浏览器: http://localhost:5173/register
        → 操作: 填写表单，选择角色，点击注册
        → 预期: 注册成功，跳转到登录页

Step 2: 测试登录页面
        → 浏览器: http://localhost:5173/login
        → 操作: 输入用户名密码，点击登录
        → 预期: 登录成功，根据角色跳转

Step 3: 验证token存储
        → 浏览器开发者工具 → Local Storage
        → 预期: 存储token和user信息
```

**验收标准：**
- [ ] 注册页面表单正常
- [ ] 登录页面表单正常
- [ ] 登录后正确跳转
- [ ] token正确存储

**验收人：** 浏览器验证
**预计耗时：** 10分钟

---

#### T9: API服务层

**目标：** 创建前端API调用封装

**文件清单：**
- `source/frontend/src/api/auth.js` ✅
- `source/frontend/src/api/tools.js` ✅
- `source/frontend/src/api/chat.js` ✅
- `source/frontend/src/api/usage.js` ✅
- `source/frontend/src/api/recommend.js` ✅
- `source/frontend/src/api/plaza.js` ✅

**执行流程：**
```
Step 1: 检查API文件是否完整
        → 验证所有API文件存在

Step 2: 测试API调用 (在浏览器控制台)
        → 打开浏览器开发者工具
        → 测试API函数是否可调用
```

**验收标准：**
- [ ] 所有API文件存在
- [ ] 导出函数正确
- [ ] baseURL配置正确

**验收人：** 代码检查
**预计耗时：** 5分钟

---

### Phase 4: 前端核心页面 (T10-T15)

#### T10: 教师端-需求引导 (核心创新点)

**目标：** 实现教师端3步需求引导流程

**文件清单：**
- `source/frontend/src/views/teacher/Guidance.vue` ✅

**执行流程：**
```
Step 1: 登录教师账号
        → 浏览器: http://localhost:5173/login
        → 操作: 使用教师账号登录

Step 2: 进入需求引导页面
        → 浏览器: http://localhost:5173/teacher
        → 预期: 显示步骤条和文理分科选项

Step 3: 测试步骤1 - 选择方向
        → 操作: 点击"文科"或"理科"卡片
        → 预期: 卡片高亮，下一步按钮可用

Step 4: 测试步骤2 - 明确需求
        → 操作: 点击"下一步"
        → 预期: 显示需求选项列表

Step 5: 测试步骤3 - 获取推荐
        → 操作: 选择需求类型，点击"下一步"
        → 预期: 显示推荐工具列表

Step 6: 测试工具使用
        → 操作: 点击"立即体验"
        → 预期: 跳转到工具使用页面
```

**验收标准：**
- [ ] 3步引导流程完整
- [ ] 步骤条状态正确
- [ ] 选项交互正常
- [ ] 推荐工具显示正确
- [ ] 跳转链接正确

**验收人：** 浏览器完整流程测试
**预计耗时：** 15分钟

---

#### T11: 教师端-工具管理

**目标：** 实现工具CRUD界面

**文件清单：**
- `source/frontend/src/views/teacher/MyTools.vue` ✅
- `source/frontend/src/components/ToolCard.vue` ✅

**执行流程：**
```
Step 1: 进入我的工具页面
        → 浏览器: http://localhost:5173/teacher/tools
        → 预期: 显示工具列表

Step 2: 测试创建工具
        → 操作: 点击"创建新工具"，填写表单，点击保存
        → 预期: 工具创建成功，列表更新

Step 3: 测试编辑工具
        → 操作: 点击工具卡片的"编辑"按钮
        → 预期: 弹出编辑对话框，可修改信息

Step 4: 测试删除工具
        → 操作: 点击"删除"按钮，确认删除
        → 预期: 工具删除成功

Step 5: 测试分享功能
        → 操作: 点击"分享"按钮
        → 预期: 弹出分享链接对话框
```

**验收标准：**
- [ ] 工具列表显示正确
- [ ] 创建工具成功
- [ ] 编辑工具成功
- [ ] 删除工具成功
- [ ] 分享链接生成正确

**验收人：** 浏览器CRUD测试
**预计耗时：** 15分钟

---

#### T12: 教师端-数据看板

**目标：** 实现数据统计可视化

**文件清单：**
- `source/frontend/src/views/teacher/Dashboard.vue` ✅

**执行流程：**
```
Step 1: 进入数据看板页面
        → 浏览器: http://localhost:5173/teacher/dashboard
        → 预期: 显示统计卡片和图表

Step 2: 验证统计数据
        → 预期: 工具总数、学生人数、今日使用显示正确

Step 3: 验证趋势图
        → 预期: 本周使用趋势柱状图显示

Step 4: 验证热门排行
        → 预期: 热门工具排行列表显示

Step 5: 验证最近记录
        → 预期: 最近使用记录表格显示
```

**验收标准：**
- [ ] 统计卡片数据正确
- [ ] 趋势图显示正常
- [ ] 排行列表正确
- [ ] 记录表格正常

**验收人：** 浏览器验证
**预计耗时：** 10分钟

---

#### T13: 学生端-需求引导 (核心创新点)

**目标：** 实现学生端3步需求引导流程

**文件清单：**
- `source/frontend/src/views/student/Guidance.vue` ✅
- `source/frontend/src/router/index.js` ✅ (需添加路由)
- `source/frontend/src/layouts/StudentLayout.vue` ✅ (需更新导航)

**执行流程：**
```
Step 1: 进入学生端首页
        → 浏览器: http://localhost:5173/student
        → 预期: 显示学生端需求引导页面

Step 2: 测试步骤1 - 选择学科方向
        → 操作: 点击"文科"或"理科"
        → 预期: 选项高亮

Step 3: 测试步骤2 - 明确学习目标
        → 操作: 点击"下一步"
        → 预期: 显示学习目标选项

Step 4: 测试步骤3 - 获取推荐
        → 操作: 选择目标，点击"下一步"
        → 预期: 显示推荐工具

Step 5: 测试跳转工具广场
        → 操作: 点击"去工具广场看看"
        → 预期: 跳转到工具广场页面
```

**验收标准：**
- [ ] 学生端引导流程完整
- [ ] 3步流程交互正常
- [ ] 推荐工具显示正确
- [ ] 跳转链接正确

**验收人：** 浏览器完整流程测试
**预计耗时：** 15分钟

---

#### T14: 学生端-工具广场

**目标：** 实现工具浏览和分类

**文件清单：**
- `source/frontend/src/views/student/Plaza.vue` ✅

**执行流程：**
```
Step 1: 进入工具广场页面
        → 浏览器: http://localhost:5173/student/plaza
        → 预期: 显示工具网格和分类标签

Step 2: 测试分类筛选
        → 操作: 点击"文科"、"理科"标签
        → 预期: 工具列表按分类筛选

Step 3: 测试搜索功能
        → 操作: 在搜索框输入关键词
        → 预期: 工具列表按关键词过滤

Step 4: 测试热门推荐
        → 预期: 显示热门工具排行

Step 5: 测试工具使用
        → 操作: 点击工具卡片
        → 预期: 跳转到工具使用页面
```

**验收标准：**
- [ ] 工具网格显示正常
- [ ] 分类筛选正确
- [ ] 搜索功能正常
- [ ] 热门推荐显示
- [ ] 跳转链接正确

**验收人：** 浏览器验证
**预计耗时：** 10分钟

---

#### T15: 学生端-AI问答/工具使用/学习记录

**目标：** 实现学生端核心功能页面

**文件清单：**
- `source/frontend/src/views/student/AIChat.vue` ✅
- `source/frontend/src/views/student/ToolUse.vue` ✅
- `source/frontend/src/views/student/Records.vue` ✅

**执行流程：**
```
--- AI问答页面 ---
Step 1: 进入AI问答页面
        → 浏览器: http://localhost:5173/student/chat
        → 预期: 显示聊天界面和提示标签

Step 2: 测试发送消息
        → 操作: 输入问题，点击发送
        → 预期: AI回复显示

Step 3: 测试提示标签
        → 操作: 点击提示标签
        → 预期: 自动发送该问题

--- 工具使用页面 ---
Step 4: 进入工具使用页面
        → 浏览器: http://localhost:5173/student/tool/1
        → 预期: 显示工具信息和对话界面

Step 5: 测试工具对话
        → 操作: 输入内容，点击发送
        → 预期: AI使用工具提示词回复

--- 学习记录页面 ---
Step 6: 进入学习记录页面
        → 浏览器: http://localhost:5173/student/records
        → 预期: 显示使用统计和记录列表

Step 7: 验证统计数据
        → 预期: 使用次数、工具数、连续天数显示
```

**验收标准：**
- [ ] AI问答页面正常
- [ ] 消息发送和接收正常
- [ ] 提示标签功能正常
- [ ] 工具使用页面正常
- [ ] 工具对话功能正常
- [ ] 学习记录页面正常
- [ ] 统计数据正确

**验收人：** 浏览器完整功能测试
**预计耗时：** 20分钟

---

### Phase 5: 集成与测试 (T16-T17)

#### T16: 前后端集成

**目标：** 配置前后端连接，确保数据流通

**文件清单：**
- `source/frontend/vite.config.js` (需修改)
- `source/frontend/src/api/*.js` (需修改baseURL)

**执行流程：**
```
Step 1: 配置Vite代理
        → 修改 source/frontend/vite.config.js
        → 添加代理配置: /api → http://localhost:8000

Step 2: 更新API baseURL
        → 修改所有 API文件
        → 将 baseURL 从 'http://localhost:8000/api' 改为 '/api'

Step 3: 重启前端服务
        → 命令: cd source/frontend && npm run dev

Step 4: 测试完整流程
        → 1. 注册教师账号
        → 2. 登录
        → 3. 测试需求引导
        → 4. 测试工具创建
        → 5. 测试AI对话
```

**验收标准：**
- [ ] Vite代理配置正确
- [ ] API调用无跨域错误
- [ ] 数据正常返回
- [ ] 完整流程可运行

**验收人：** 浏览器完整流程测试
**预计耗时：** 20分钟

---

#### T17: 最终测试与文档

**目标：** 完整测试和文档编写

**文件清单：**
- `docs/deployment-guide.md` (待创建)
- `docs/user-manual.md` (待创建)

**执行流程：**
```
Step 1: 创建部署指南
        → 文件: docs/deployment-guide.md
        → 内容: 环境要求、部署步骤、Nginx配置、常见问题

Step 2: 创建用户手册
        → 文件: docs/user-manual.md
        → 内容: 教师端和学生端操作指南

Step 3: 完整流程测试
        → 教师端: 注册 → 登录 → 需求引导 → 工具管理 → 数据看板
        → 学生端: 需求引导 → 工具广场 → AI问答 → 学习记录

Step 4: 修复发现的问题
        → 记录问题 → 修复 → 重新测试
```

**验收标准：**
- [ ] 部署指南文档完整
- [ ] 用户手册文档完整
- [ ] 教师端全流程通过
- [ ] 学生端全流程通过
- [ ] 无严重bug

**验收人：** 人工完整流程测试
**预计耗时：** 30分钟

---

## 三、验收流程规范

### 单任务验收

每个任务完成后，按以下流程验收：

```
1. 执行任务步骤
   ↓
2. 检查验收标准 (checkbox)
   ↓
3. 全部通过 → 提交任务
   ↓
4. 任一失败 → 返工修复 → 重新验收
```

### 任务拼接验收

相邻任务完成后，进行拼接验收：

```
Phase 1 (T1+T2+T3) → 后端基础验收
   ↓
Phase 2 (T4+T5+T6) → 后端业务验收
   ↓
Phase 3 (T7+T8+T9) → 前端基础验收
   ↓
Phase 4 (T10-T15) → 前端功能验收
   ↓
Phase 5 (T16+T17) → 整体集成验收
```

### 整体项目验收

所有任务完成后，进行整体项目验收：

```
验收维度：
1. 功能完整性 - 所有功能点是否实现
2. 流程闭环性 - 教师端和学生端流程是否闭环
3. 数据真实性 - 数据是否真正存入MySQL
4. AI真实性 - DeepSeek API是否实际调用
5. 界面美观性 - UI是否符合竞赛要求
6. 文档完整性 - 7份文档是否齐全
```

---

## 四、返工规范

当验收不通过时：

```
1. 记录问题
   → 问题描述
   → 预期结果
   → 实际结果

2. 分析原因
   → 代码问题 → 修改代码
   → 配置问题 → 修改配置
   → 环境问题 → 解决环境

3. 修复并重新验收
   → 执行修复
   → 重新运行验收步骤
   → 确认问题解决

4. 记录修复过程
   → 更新任务状态
   → 记录修复内容
```

---

## 五、今日工作计划

**优先级排序：**

1. **T1: 数据库初始化** (10分钟)
   - 运行init_db.py
   - 验证表和数据

2. **T2: 工具CRUD API** (15分钟)
   - 启动后端
   - curl测试API

3. **T3: AI对话API** (20分钟)
   - 配置DeepSeek API Key
   - 测试对话功能

4. **T4-T6: 后端业务API** (30分钟)
   - 逐个测试统计、推荐、广场API

5. **T16: 前后端集成** (20分钟)
   - 配置代理
   - 测试完整流程

**预计总耗时：** 约2小时

---

*文档结束*
