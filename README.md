# 智教通

智教通是面向教师与学生的 AI 教学辅助平台：教师通过需求引导、可解释规则推荐和工具管理组织教学；学生浏览工具广场，在登录后使用 AI 问答、收藏工具并形成学习轨迹。

## 正式代码入口

```text
source/frontend/  Vue 3 + Vite + Element Plus
source/backend/   FastAPI + SQLAlchemy + Alembic + MySQL
docs/             竞赛资料、设计与运行文档
```

DeepSeek 只用于文本学习问答。复杂智能体创建只通过带白名单上下文参数的新窗口跳转师大智能体平台，不交换账号或工作流数据。

## 运行

要求：Node.js 20+、Python 3.11、MySQL 8。

```powershell
# 后端
cd source/backend
Copy-Item .env.example .env
py -3.11 -m pip install -r requirements.txt
py -3.11 -m alembic -c alembic.ini upgrade head
py -3.11 -m uvicorn main:app --host 127.0.0.1 --port 8000

# 另一个终端：前端
cd source/frontend
npm ci
npm run dev
```

前端默认地址为 `http://127.0.0.1:5173`，后端存活检查为 `/api/health`，就绪检查为 `/api/readiness`，API 文档为 `/docs`。

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
