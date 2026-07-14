# 智教通

面向教师与学生的 AI 智能体教学辅助平台：把需求引导、工具推荐、AI 问答和学习轨迹连接成一条可执行的教学路径。

智教通采用教师端与学生端双入口。首页以东方未来主义视觉和“生命水墨”交互呈现知识路径；教师可以完成需求引导、工具管理和数据洞察，学生可以从兴趣出发浏览工具、进行 AI 问答并查看学习记录。

## 核心体验

- **教师端**：登录后选择学科和教学需求，通过规则匹配获得工具推荐，管理与分享工具，并查看使用统计和趋势。
- **学生端**：无需登录即可浏览工具广场或打开分享链接，通过兴趣引导、AI 问答和学习记录持续探索。
- **生命水墨首页**：鼠标移动时以短暂水墨晕染显现主题画面，离开后自然闭合；低性能设备和减少动态偏好会自动降级。
- **AI 与工具边界**：DeepSeek 负责文本问答，推荐逻辑使用可解释的条件匹配；复杂智能体制作跳转到师大智能体平台。

## 技术架构

```text
Vue 3 + Element Plus + Vite
             │ HTTP
             ▼
FastAPI + SQLAlchemy ─────► MySQL 8
             │
             └────────────► DeepSeek API（文本问答）
```

主要版本以锁文件和依赖清单为准：前端使用 Vue 3、Vue Router、Pinia、Axios、Vitest；后端使用 Python 3.11、FastAPI、SQLAlchemy、PyMySQL 和 pytest。

## 目录

```text
.
├── .github/               # CI、Issue 与 PR 模板
├── docs/
│   ├── competition/       # 竞赛原始材料与项目文档
│   ├── design/            # 产品和交互设计规格
│   ├── guides/            # 环境与技术栈指南
│   ├── quality/           # QA 报告和截图
│   └── archive/           # 历史计划、报告和已停用前端
│       └── legacy-frontend/ # 不参与构建的早期页面快照
├── source/
│   ├── frontend/          # 唯一正式 Vue 前端
│   └── backend/           # FastAPI 后端
├── CONTRIBUTING.md
├── SECURITY.md
└── README.md
```

`source/frontend` 与 `source/backend` 是仅有的正式应用代码入口。`docs/archive/legacy-frontend` 只用于历史追溯，不参与安装、路由、测试或生产构建。

完整资料入口见 [文档中心](docs/README.md)。

## 快速开始

### 1. 获取代码

```bash
git clone https://github.com/xinyuzhang610/-.git zjiaotong
cd zjiaotong
```

建议使用 Node.js 20、npm 10、Python 3.11 和 MySQL 8。

### 2. 启动前端

Windows、macOS 和 Linux 均可执行：

```bash
cd source/frontend
npm ci
cp .env.example .env
npm run dev
```

PowerShell 复制环境文件可改用：

```powershell
Copy-Item .env.example .env
```

默认访问地址为 `http://localhost:5173`。

### 3. 启动后端

Windows PowerShell：

```powershell
cd source/backend
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python -m uvicorn main:app --reload
```

macOS / Linux：

```bash
cd source/backend
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
python -m uvicorn main:app --reload
```

后端默认运行在 `http://localhost:8000`，健康检查为 `http://localhost:8000/api/health`，交互式 API 文档为 `http://localhost:8000/docs`。

### 4. 配置数据库与 AI

在 `source/backend/.env` 中至少配置：

```dotenv
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/zjiaotong
DEEPSEEK_API_KEY=your_api_key_here
DEEPSEEK_MODEL=dsv4
```

请先在 MySQL 中创建 `zjiaotong` 数据库，再按 [环境配置指南](docs/guides/环境配置指南.md) 初始化数据。不得把真实 `.env`、数据库密码或 API Key 提交到 Git。

## 演示模式

仅检查前端交互、且暂时没有后端或数据库时，可在 `source/frontend/.env` 中设置：

```dotenv
VITE_DEMO_MODE=true
```

演示模式使用本地模拟数据。正常开发和生产部署必须保持 `false`，并通过 `VITE_API_BASE_URL` 连接真实后端。生产环境不要把私密 DeepSeek Key 暴露在 `VITE_*` 变量中，AI 请求应由后端代理。

## 测试与构建

前端：

```bash
cd source/frontend
npm ci
npm test -- --run
npm run build
```

后端：

```bash
cd source/backend
python -m pip install -r requirements.txt
python -m pytest
```

根目录下的 `source/backend/test_all_apis.py` 是需要后端与数据库均已启动的手工联调脚本，不属于默认 pytest 单元测试集。

## 协作与安全

- 开发流程、分支和提交规范见 [CONTRIBUTING.md](CONTRIBUTING.md)。
- 漏洞、密钥或个人信息泄露请按 [SECURITY.md](SECURITY.md) 私下报告，不要公开创建 Issue。
- 报名表可能包含个人信息，使用前请阅读 [文档中心的资料说明](docs/README.md#资料使用说明)。

## 许可证状态

本仓库当前未声明开源许可证。除非仓库所有者另行授权，不应假定代码或资料可以按 MIT 或其他开源许可证复制、分发或再许可。
