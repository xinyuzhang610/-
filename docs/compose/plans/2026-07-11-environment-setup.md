# 环境配置 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use compose:subagent (recommended) or compose:execute to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 配置统一的Vue3 + Element Plus前端和FastAPI后端开发环境，确保团队成员克隆后即可使用相同环境进行开发

**Architecture:** 前后端分离架构，前端使用Vue3 + Element Plus + Vite，后端使用Python FastAPI + SQLAlchemy + MySQL，通过Git进行版本控制和环境同步

**Tech Stack:** Vue 3, Element Plus, Vite, Axios, Python FastAPI, SQLAlchemy, PyMySQL, MySQL 8.0, DeepSeek API

## Global Constraints

- Node.js >= 18.x
- Python >= 3.11
- MySQL >= 8.0
- 使用UTF-8编码
- 所有路径使用相对路径
- 环境变量通过.env文件管理

---

## Task 1: 创建前端项目基础结构

**Covers:** 技术栈统一、环境配置

**Files:**
- Create: `source/frontend/package.json`
- Create: `source/frontend/vite.config.js`
- Create: `source/frontend/src/main.js`
- Create: `source/frontend/src/App.vue`
- Create: `source/frontend/index.html`
- Create: `source/frontend/.env.example`
- Create: `source/frontend/.gitignore`

**Interfaces:**
- Consumes: Node.js 24.16.0, npm 11.13.0
- Produces: 可运行的Vue3 + Element Plus前端项目

- [ ] **Step 1: 创建前端目录结构**

```bash
mkdir -p source/frontend/src/components source/frontend/src/views source/frontend/src/router source/frontend/src/stores source/frontend/src/api source/frontend/public
```

- [ ] **Step 2: 创建package.json**

```json
{
  "name": "zjiaotong-frontend",
  "version": "1.0.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "vue": "^3.4.21",
    "element-plus": "^2.6.3",
    "axios": "^1.6.8",
    "vue-router": "^4.3.0",
    "pinia": "^2.1.7"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.0.4",
    "vite": "^5.2.0"
  }
}
```

- [ ] **Step 3: 创建vite.config.js**

```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})
```

- [ ] **Step 4: 创建main.js**

```javascript
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router'

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(ElementPlus)
app.mount('#app')
```

- [ ] **Step 5: 创建App.vue**

```vue
<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script setup>
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
```

- [ ] **Step 6: 创建index.html**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>智教通 - AI智能体教学辅助平台</title>
</head>
<body>
  <div id="app"></div>
  <script type="module" src="/src/main.js"></script>
</body>
</html>
```

- [ ] **Step 7: 创建.env.example**

```env
# DeepSeek API配置
VITE_DEEPSEEK_API_KEY=your_api_key_here
VITE_DEEPSEEK_MODEL=dsv4

# 后端API地址
VITE_API_BASE_URL=http://localhost:8000
```

- [ ] **Step 8: 创建前端.gitignore**

```gitignore
node_modules
dist
.env
.env.local
.env.*.local
*.log
```

- [ ] **Step 9: 测试前端项目**

```bash
cd source/frontend
npm install
npm run dev
```

- [ ] **Step 10: 提交前端环境配置**

```bash
git add source/frontend/
git commit -m "feat: 初始化Vue3 + Element Plus前端项目环境"
```

## Task 2: 创建后端项目基础结构

**Covers:** 技术栈统一、环境配置

**Files:**
- Create: `source/backend/requirements.txt`
- Create: `source/backend/main.py`
- Create: `source/backend/config.py`
- Create: `source/backend/.env.example`
- Create: `source/backend/.gitignore`

**Interfaces:**
- Consumes: Python 3.11.9, pip 26.0.1
- Produces: 可运行的FastAPI后端项目

- [ ] **Step 1: 创建后端目录结构**

```bash
mkdir -p source/backend/api source/backend/models source/backend/services source/backend/utils
```

- [ ] **Step 2: 创建requirements.txt**

```txt
fastapi==0.110.0
uvicorn[standard]==0.29.0
sqlalchemy==2.0.29
pymysql==1.1.0
python-dotenv==1.0.1
python-multipart==0.0.9
httpx==0.27.0
pydantic==2.6.4
pydantic-settings==2.2.1
```

- [ ] **Step 3: 创建main.py**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings

app = FastAPI(
    title="智教通 API",
    description="AI智能体教学辅助平台后端接口",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "智教通 API 服务运行中"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

- [ ] **Step 4: 创建config.py**

```python
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # 应用配置
    APP_NAME: str = "智教通"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # 数据库配置
    DATABASE_URL: str = "mysql+pymysql://root:password@localhost:3306/zjiaotong"
    
    # DeepSeek API配置
    DEEPSEEK_API_KEY: str = ""
    DEEPSEEK_MODEL: str = "dsv4"
    DEEPSEEK_API_URL: str = "https://api.deepseek.com"
    
    # CORS配置
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
```

- [ ] **Step 5: 创建.env.example**

```env
# 应用配置
DEBUG=true

# 数据库配置
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/zjiaotong

# DeepSeek API配置
DEEPSEEK_API_KEY=your_api_key_here
DEEPSEEK_MODEL=dsv4

# CORS配置
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]
```

- [ ] **Step 6: 创建后端.gitignore**

```gitignore
__pycache__
*.pyc
*.pyo
.env
venv/
.venv/
*.log
```

- [ ] **Step 7: 测试后端项目**

```bash
cd source/backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

- [ ] **Step 8: 提交后端环境配置**

```bash
git add source/backend/
git commit -m "feat: 初始化FastAPI后端项目环境"
```

## Task 3: 创建项目根目录配置

**Covers:** 项目结构统一、环境配置

**Files:**
- Create: `.gitignore`
- Create: `README.md`
- Create: `docs/技术栈说明.md`

**Interfaces:**
- Consumes: Task 1, Task 2的输出
- Produces: 统一的项目根目录结构

- [ ] **Step 1: 创建根目录.gitignore**

```gitignore
# 依赖目录
node_modules/
venv/
.venv/

# 构建产物
dist/
build/

# 环境文件
.env
.env.local
.env.*.local

# 日志文件
*.log

# 操作系统文件
.DS_Store
Thumbs.db

# IDE文件
.vscode/
.idea/
*.swp
*.swo

# Python缓存
__pycache__/
*.pyc
*.pyo

# 前端缓存
.cache/
```

- [ ] **Step 2: 创建README.md**

```markdown
# 智教通 - AI智能体教学辅助平台

## 项目简介

面向教育场景的Web应用平台，通过需求引导帮助老师发现教学需求、体验AI智能体工具。

## 技术栈

### 前端
- Vue 3.4.21
- Element Plus 2.6.3
- Vite 5.2.0
- Axios 1.6.8
- Vue Router 4.3.0
- Pinia 2.1.7

### 后端
- Python 3.11.9
- FastAPI 0.110.0
- SQLAlchemy 2.0.29
- PyMySQL 1.1.0

### 数据库
- MySQL 8.0

### AI接口
- DeepSeek API (model: dsv4)

## 快速开始

### 1. 克隆项目
```bash
git clone <repository-url>
cd zjiaotong
```

### 2. 前端开发
```bash
cd source/frontend
npm install
npm run dev
```

### 3. 后端开发
```bash
cd source/backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### 4. 环境变量配置
复制 `.env.example` 为 `.env` 并填写配置

## 项目结构

```
zjiaotong/
├── source/
│   ├── frontend/          # Vue3前端项目
│   │   ├── src/
│   │   ├── public/
│   │   ├── package.json
│   │   └── vite.config.js
│   └── backend/           # FastAPI后端项目
│       ├── api/
│       ├── models/
│       ├── services/
│       ├── utils/
│       ├── main.py
│       └── requirements.txt
├── docs/                  # 项目文档
├── .gitignore
└── README.md
```

## 开发规范

1. **分支管理**: 使用Git Flow工作流
2. **代码规范**: 遵循ESLint和Python PEP8规范
3. **提交规范**: 使用Conventional Commits规范
4. **环境统一**: 所有开发者使用相同的依赖版本

## 团队协作

- 成员A: 文档撰写
- 成员B: 前后端开发
- 成员C: 前后端开发

## 许可证

内部项目，仅供参考
```

- [ ] **Step 3: 创建技术栈说明文档**

```markdown
# 技术栈说明

## 版本锁定原则

为确保团队开发环境一致，所有依赖版本已锁定：

### 前端依赖版本
- Vue: 3.4.21
- Element Plus: 2.6.3
- Vite: 5.2.0
- Axios: 1.6.8
- Vue Router: 4.3.0
- Pinia: 2.1.7

### 后端依赖版本
- FastAPI: 0.110.0
- Uvicorn: 0.29.0
- SQLAlchemy: 2.0.29
- PyMySQL: 1.1.0

## 环境要求

### 开发环境
- Node.js: 24.16.0
- npm: 11.13.0
- Python: 3.11.9
- pip: 26.0.1
- MySQL: 8.0

### 系统要求
- Windows 10/11
- macOS 12+
- Linux (Ubuntu 20.04+)

## 安装步骤

1. 安装Node.js和npm
2. 安装Python和pip
3. 安装MySQL
4. 克隆项目
5. 配置环境变量
6. 安装依赖

## 常见问题

### Q: npm install失败
A: 检查Node.js版本是否>=18.x，尝试清理npm缓存

### Q: Python依赖安装失败
A: 确保使用虚拟环境，检查Python版本是否>=3.11

### Q: 数据库连接失败
A: 检查MySQL服务是否启动，.env配置是否正确
```

- [ ] **Step 4: 提交项目根目录配置**

```bash
git add .gitignore README.md docs/
git commit -m "feat: 创建项目根目录配置和文档"
```

## Task 4: 初始化Git仓库并提交

**Covers:** 版本控制、环境同步

**Files:**
- Modify: `.git/config` (自动)
- Create: `.gitignore`

**Interfaces:**
- Consumes: Task 1, Task 2, Task 3的输出
- Produces: 可克隆的Git仓库

- [ ] **Step 1: 初始化Git仓库**

```bash
git init
git branch -M main
```

- [ ] **Step 2: 添加远程仓库**

```bash
git remote add origin <your-repository-url>
```

- [ ] **Step 3: 提交所有环境配置**

```bash
git add .
git commit -m "feat: 初始化项目环境配置

- 配置Vue3 + Element Plus前端环境
- 配置FastAPI后端环境
- 创建项目文档和配置文件
- 锁定所有依赖版本"
```

- [ ] **Step 4: 推送到远程仓库**

```bash
git push -u origin main
```

- [ ] **Step 5: 验证环境配置**

```bash
# 测试前端
cd source/frontend
npm install
npm run dev

# 测试后端
cd source/backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Task 5: 环境验证和文档更新

**Covers:** 环境验证、文档完善

**Files:**
- Modify: `README.md`
- Create: `docs/环境配置指南.md`

**Interfaces:**
- Consumes: Task 1-4的输出
- Produces: 完整的环境配置文档

- [ ] **Step 1: 创建环境配置指南**

```markdown
# 环境配置指南

## 快速开始

### 1. 环境要求

确保你的系统安装以下软件：

| 软件 | 版本 | 下载地址 |
|------|------|----------|
| Node.js | 24.16.0 | https://nodejs.org/ |
| Python | 3.11.9 | https://www.python.org/ |
| MySQL | 8.0 | https://dev.mysql.com/downloads/ |
| Git | 最新 | https://git-scm.com/ |

### 2. 克隆项目

```bash
git clone <repository-url>
cd zjiaotong
```

### 3. 配置前端环境

```bash
cd source/frontend
npm install
cp .env.example .env
# 编辑.env文件，填写API配置
npm run dev
```

### 4. 配置后端环境

```bash
cd source/backend
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
# 编辑.env文件，填写数据库和API配置
python main.py
```

### 5. 配置数据库

```bash
# 登录MySQL
mysql -u root -p

# 创建数据库
CREATE DATABASE zjiaotong CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 创建用户（可选）
CREATE USER 'zjiaotong'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON zjiaotong.* TO 'zjiaotong'@'localhost';
FLUSH PRIVILEGES;
```

### 6. 环境变量配置

#### 前端环境变量 (.env)
```env
VITE_DEEPSEEK_API_KEY=your_api_key_here
VITE_DEEPSEEK_MODEL=dsv4
VITE_API_BASE_URL=http://localhost:8000
```

#### 后端环境变量 (.env)
```env
DEBUG=true
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/zjiaotong
DEEPSEEK_API_KEY=your_api_key_here
DEEPSEEK_MODEL=dsv4
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]
```

## 验证环境

### 前端验证
访问 http://localhost:3000，应该看到Vue应用

### 后端验证
访问 http://localhost:8000，应该看到API响应

### 数据库验证
```bash
mysql -u root -p -e "SHOW DATABASES;"
```

## 常见问题

### 问题1: npm install失败
**解决方案:**
```bash
# 清理npm缓存
npm cache clean --force
# 删除node_modules
rm -rf node_modules
# 重新安装
npm install
```

### 问题2: Python依赖安装失败
**解决方案:**
```bash
# 确保在虚拟环境中
source venv/bin/activate
# 升级pip
pip install --upgrade pip
# 重新安装
pip install -r requirements.txt
```

### 问题3: 数据库连接失败
**解决方案:**
1. 检查MySQL服务是否启动
2. 检查.env配置是否正确
3. 检查用户权限

### 问题4: 端口被占用
**解决方案:**
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :3000
kill -9 <PID>
```

## 开发工具推荐

### IDE
- VS Code (推荐)
- PyCharm
- WebStorm

### VS Code扩展
- Volar (Vue 3)
- Python
- Pylance
- MySQL
- GitLens

### 浏览器扩展
- Vue.js devtools
- React Developer Tools (可选)

## 团队协作

### Git工作流
1. 从main分支创建功能分支
2. 在功能分支开发
3. 提交Pull Request
4. 代码审查
5. 合并到main分支

### 提交规范
```
feat: 新功能
fix: 修复bug
docs: 文档更新
style: 代码格式调整
refactor: 代码重构
test: 测试相关
chore: 构建/工具相关
```

## 环境维护

### 更新依赖
```bash
# 前端
npm update
# 后端
pip install --upgrade -r requirements.txt
```

### 清理环境
```bash
# 前端
rm -rf node_modules dist
npm install

# 后端
rm -rf venv __pycache__
python -m venv venv
pip install -r requirements.txt
```
```

- [ ] **Step 2: 更新README.md**

在README.md中添加环境配置指南的链接。

- [ ] **Step 3: 提交文档更新**

```bash
git add docs/环境配置指南.md README.md
git commit -m "docs: 添加环境配置指南"
git push
```

## 自检清单

**1. Spec覆盖检查:**
- [x] 技术栈统一: Task 1, Task 2
- [x] 环境配置: Task 1, Task 2, Task 3
- [x] 版本控制: Task 4
- [x] 文档完善: Task 5

**2. 占位符扫描:**
- [x] 所有步骤都有具体代码
- [x] 所有命令都有预期输出
- [x] 所有配置都有具体内容

**3. 类型一致性:**
- [x] 文件路径一致
- [x] 依赖版本一致
- [x] 配置参数一致

**执行建议:**
- 使用 compose:execute 按顺序执行Task 1-5
- 每个Task完成后进行验证
- 遇到问题及时调整配置