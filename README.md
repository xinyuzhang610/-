# 智教通

智教通是面向教师与学生的 AI 教学辅助平台：教师通过需求引导、可解释规则推荐和工具管理组织教学；学生浏览工具广场，在登录后使用 AI 问答、收藏工具并形成学习轨迹。

## 正式代码入口

```text
source/frontend/  Vue 3 + Vite + Element Plus
source/backend/   FastAPI + SQLAlchemy + Alembic + MySQL
docs/             竞赛资料、设计与运行文档
```

DeepSeek 只用于文本学习问答。复杂智能体创建只通过带白名单上下文参数的新窗口跳转师大智能体平台，不交换账号或工作流数据。

## 本地运行

要求：Node.js 20+、Python 3.11、MySQL 8。当前比赛交付版只要求本地运行，不包含线上部署步骤。

```powershell
# 后端
cd source/backend
Copy-Item .env.development.example .env
py -3.11 -m pip install -r requirements.txt
py -3.11 -m alembic -c alembic.ini upgrade head
py -3.11 seed_local_demo.py
py -3.11 -m uvicorn main:app --host 127.0.0.1 --port 8000

# 另一个终端：前端
cd source/frontend
npm ci
npm run dev
```

前端默认地址为 `http://127.0.0.1:3000`，后端存活检查为 `http://127.0.0.1:8000/api/health`，就绪检查为 `http://127.0.0.1:8000/api/readiness`，API 文档为 `http://127.0.0.1:8000/docs`。

首次运行前，请先在 MySQL 中创建 `zjiaotong` 数据库，并把 `source/backend/.env` 中的数据库连接改为本机账号。只做前端页面演示时，可复制 `source/frontend/.env.example`，保持 `VITE_DEMO_MODE=true`；要联调真实接口时将其改为 `false`，并启动后端。

执行 `seed_local_demo.py` 后可用以下本地测试账号联调：`teacher_demo / Teacher2026`、`student_demo / Student2026`、`admin_demo / Admin2026`。这些是演示账号，不要用于生产环境。

不要将 `.env`、MySQL 密码、DeepSeek Key 或备份提交到 Git。生产环境须使用 HTTPS、Turnstile 和受限 MySQL 账号。

## 数据库与验证

生产升级只使用 Alembic；已有旧表的数据库先备份、核对数据，再按 baseline stamp 后增量升级。详细步骤见 [后端与数据库运行手册](docs/guides/backend-operations.md)。

```powershell
# 后端测试
cd source/backend
py -3.11 -m pytest tests -q

# 前端测试、构建与依赖审计
cd ../frontend
npm test -- --run
npm run build
npm audit
```

## 当前交付边界

- 广场和分享链接可公开预览，但 AI、收藏和学习轨迹要求学生登录。
- 工具采用软删除；广场状态、分享启用和分享过期时间独立管理。
- 公开 API 不返回提示词或内部界面配置。
- 二维码在前端本地生成，不依赖第三方二维码服务。

## 比赛最终材料

- 七份最终版 Word 文档位于 [docs/competition/final](docs/competition/final/)；以该目录中的版本为准。
- `docs/competition/project/` 中的 Markdown 是开发辅助资料和索引，不覆盖最终版 Word 文档。
- 推荐交付分支为 `main`；旧分支仅保留 Git 历史，不参与本地运行。
