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