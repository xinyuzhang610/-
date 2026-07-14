# 架构规范实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use compose:subagent (recommended) or compose:execute to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 按优先级实施架构规范调整，解决状态管理缺失、配置错误、后端业务逻辑层不完整等问题。

**Architecture:** 先解决最紧急的问题（Pinia状态管理、配置修正），再补充后端services目录结构，最后进行代码审查和文档更新。

**Tech Stack:** Vue 3, Pinia, FastAPI, SQLAlchemy, Pydantic

## Global Constraints

- 项目截止日期：2026-07-21
- 团队成员是教育技术专业，不是CS，代码要简单易懂
- 前端功能页面开发必须先与用户讨论方案，确认后再实施
- 每个任务完成后必须给出详细运行说明，供用户人工检查
- 核心创新点：为零基础小白教会使用AI工具并挖掘兴趣

---

## Task 1: 创建 Pinia 状态管理（stores/user.js）

**Covers:** [S3]

**Files:**
- Create: `source/frontend/src/stores/user.js`
- Modify: `source/frontend/src/main.js`
- Modify: `source/frontend/src/views/auth/Login.vue`
- Modify: `source/frontend/src/views/auth/Register.vue`

**Interfaces:**
- Consumes: 无（新模块）
- Produces: `useUserStore()` 函数，包含 `user`, `token`, `isLoggedIn`, `login()`, `logout()`, `register()` 方法

- [ ] **Step 1: 创建 stores/user.js 文件**

```javascript
// stores/user.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login as apiLogin, register as apiRegister, getProfile } from '@/api/auth'

export const useUserStore = defineStore('user', () => {
  // 状态
  const user = ref(null)
  const token = ref(localStorage.getItem('token') || '')

  // 计算属性
  const isLoggedIn = computed(() => !!token.value)
  const isTeacher = computed(() => user.value?.role === 'teacher')
  const isStudent = computed(() => user.value?.role === 'student')

  // 登录
  async function login(credentials) {
    try {
      const res = await apiLogin(credentials)
      token.value = res.data.token
      localStorage.setItem('token', res.data.token)
      await fetchProfile(res.data.user_id)
      return res.data
    } catch (error) {
      throw error
    }
  }

  // 注册
  async function register(userData) {
    try {
      const res = await apiRegister(userData)
      return res.data
    } catch (error) {
      throw error
    }
  }

  // 获取用户信息
  async function fetchProfile(userId) {
    try {
      const res = await getProfile(userId)
      user.value = res.data
    } catch (error) {
      console.error('获取用户信息失败:', error)
    }
  }

  // 退出登录
  function logout() {
    user.value = null
    token.value = ''
    localStorage.removeItem('token')
  }

  return {
    user,
    token,
    isLoggedIn,
    isTeacher,
    isStudent,
    login,
    register,
    fetchProfile,
    logout
  }
})
```

- [ ] **Step 2: 在 main.js 中注册 Pinia**

修改 `source/frontend/src/main.js`：

```javascript
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.use(ElementPlus)

app.mount('#app')
```

- [ ] **Step 3: 安装 Pinia 依赖**

```bash
cd source/frontend
npm install pinia
```

- [ ] **Step 4: 修改登录页使用状态管理**

修改 `source/frontend/src/views/auth/Login.vue`，在 `<script>` 中使用 userStore：

```javascript
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()

// 修改登录方法
const handleLogin = async () => {
  try {
    await userStore.login({
      username: loginForm.username,
      password: loginForm.password
    })
    // 登录成功后跳转
    if (userStore.isTeacher) {
      router.push('/teacher')
    } else {
      router.push('/student')
    }
  } catch (error) {
    ElMessage.error(error.message || '登录失败')
  }
}
```

- [ ] **Step 5: 修改注册页使用状态管理**

修改 `source/frontend/src/views/auth/Register.vue`，在 `<script>` 中使用 userStore：

```javascript
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()

// 修改注册方法
const handleRegister = async () => {
  try {
    await userStore.register({
      username: registerForm.username,
      password: registerForm.password,
      role: registerForm.role,
      // 其他字段...
    })
    ElMessage.success('注册成功，请登录')
    router.push('/login')
  } catch (error) {
    ElMessage.error(error.message || '注册失败')
  }
}
```

- [ ] **Step 6: 验证状态管理功能**

运行前端项目：
```bash
cd source/frontend
npm run dev
```

测试流程：
1. 访问 http://localhost:5173/register，注册一个新用户
2. 访问 http://localhost:5173/login，登录
3. 检查浏览器控制台和 localStorage，确认 token 已保存
4. 刷新页面，确认登录状态保持

- [ ] **Step 7: 提交代码**

```bash
git add source/frontend/src/stores/user.js source/frontend/src/main.js source/frontend/src/views/auth/Login.vue source/frontend/src/views/auth/Register.vue
git commit -m "feat: add Pinia state management for user authentication"
```

**运行说明**：
1. 启动后端：`cd source/backend && uvicorn main:app --reload`
2. 启动前端：`cd source/frontend && npm run dev`
3. 访问 http://localhost:5173/register 注册新用户
4. 访问 http://localhost:5173/login 登录
5. 登录成功后应自动跳转到对应端（教师/学生）
6. 刷新页面后登录状态应保持

---

## Task 2: 修正配置文件问题

**Covers:** [S6]

**Files:**
- Modify: `source/backend/config.py`
- Modify: `source/backend/.env`

**Interfaces:**
- Consumes: 无
- Produces: 修正后的配置文件，密码和模型名正确

- [ ] **Step 1: 修正 config.py 中的数据库密码**

修改 `source/backend/config.py`，将硬编码的密码改为从环境变量读取：

```python
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # 应用配置
    APP_NAME: str = "智教通"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # 数据库配置
    DATABASE_URL: str = "mysql+pymysql://root:admin@localhost:3306/zjiaotong"
    
    # DeepSeek API配置
    DEEPSEEK_API_KEY: str = ""
    DEEPSEEK_MODEL: str = "deepseek-chat"  # 修正：dsv4 -> deepseek-chat
    DEEPSEEK_API_URL: str = "https://api.deepseek.com"
    
    # CORS配置
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
```

- [ ] **Step 2: 检查 .env 文件**

确认 `source/backend/.env` 文件包含正确的配置：

```env
DATABASE_URL=mysql+pymysql://root:admin@localhost:3306/zjiaotong
DEEPSEEK_API_KEY=sk-eb08...（你的实际Key）
DEEPSEEK_MODEL=deepseek-chat
```

- [ ] **Step 3: 验证配置**

重启后端服务，检查日志：
```bash
cd source/backend
uvicorn main:app --reload
```

访问 http://localhost:8000/docs，确认 API 正常运行。

- [ ] **Step 4: 提交代码**

```bash
git add source/backend/config.py source/backend/.env
git commit -m "fix: correct database password and DeepSeek model name in config"
```

**运行说明**：
1. 重启后端：`cd source/backend && uvicorn main:app --reload`
2. 访问 http://localhost:8000/docs，确认 API 文档正常显示
3. 检查后端启动日志，确认无配置错误

---

## Task 3: 补充后端 services 目录结构

**Covers:** [S4]

**Files:**
- Create: `source/backend/services/user_service.py`
- Create: `source/backend/services/tool_service.py`
- Create: `source/backend/services/chat_service.py`
- Create: `source/backend/services/usage_service.py`
- Create: `source/backend/services/recommend_service.py`
- Create: `source/backend/services/plaza_service.py`
- Modify: `source/backend/api/user.py`（示例，其他文件类似）

**Interfaces:**
- Consumes: models, schemas
- Produces: 业务逻辑函数，供 api 层调用

- [ ] **Step 1: 创建 user_service.py**

```python
# services/user_service.py
from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate, UserLogin
from utils.security import hash_password, verify_password

def create_user(db: Session, user_data: UserCreate):
    """创建新用户"""
    hashed_password = hash_password(user_data.password)
    db_user = User(
        username=user_data.username,
        password=hashed_password,
        role=user_data.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    """验证用户登录"""
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password):
        return None
    return user

def get_user_by_id(db: Session, user_id: int):
    """根据ID获取用户"""
    return db.query(User).filter(User.id == user_id).first()
```

- [ ] **Step 2: 创建其他 services 文件（类似结构）**

每个 services 文件包含对应业务模块的核心逻辑函数。

- [ ] **Step 3: 修改 api/user.py 使用 services**

```python
# api/user.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.user import UserCreate, UserLogin, UserResponse
from services.user_service import create_user, authenticate_user, get_user_by_id

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """用户注册"""
    user = create_user(db, user_data)
    return user

@router.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """用户登录"""
    user = authenticate_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    # 生成 token...
    return {"token": "xxx", "user_id": user.id}

@router.get("/profile/{user_id}", response_model=UserResponse)
def get_profile(user_id: int, db: Session = Depends(get_db)):
    """获取用户信息"""
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user
```

- [ ] **Step 4: 验证 API 功能**

重启后端，测试注册和登录接口：
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"123456","role":"student"}'

curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"123456"}'
```

- [ ] **Step 5: 提交代码**

```bash
git add source/backend/services/ source/backend/api/user.py
git commit -m "feat: add service layer for backend business logic"
```

**运行说明**：
1. 重启后端：`cd source/backend && uvicorn main:app --reload`
2. 访问 http://localhost:8000/docs，测试注册和登录接口
3. 确认数据库中用户数据正确写入

---

## Task 4: 代码审查和文档更新

**Covers:** [S7]

**Files:**
- Review: 所有修改的文件
- Update: `docs/compose/specs/2026-07-13-architecture-spec.md`（如需要）

**Interfaces:**
- Consumes: 前三个任务的产出
- Produces: 审查报告、更新后的文档

- [ ] **Step 1: 代码审查**

检查所有修改的文件：
- 代码风格是否一致
- 是否有重复代码
- 是否有安全隐患
- 是否符合架构规范

- [ ] **Step 2: 功能测试**

完整测试流程：
1. 注册新用户
2. 登录
3. 教师端：需求引导 → 我的工具 → 数据看板
4. 学生端：工具广场 → AI问答 → 工具使用 → 学习记录
5. 检查数据库数据

- [ ] **Step 3: 更新文档**

如有需要，更新架构规范文档，记录实际实施中的调整。

- [ ] **Step 4: 提交代码**

```bash
git add -A
git commit -m "docs: update architecture spec and complete code review"
```

**运行说明**：
1. 启动后端和前端
2. 按上述流程完整测试所有功能
3. 检查浏览器控制台无错误
4. 检查后端日志无异常

---

## 实施顺序

1. **Task 1**（Pinia状态管理）— 最紧急，影响登录状态共享
2. **Task 2**（配置修正）— 重要，影响后端运行
3. **Task 3**（后端services）— 重要，提升代码结构
4. **Task 4**（代码审查）— 收尾工作

## 预计时间

- Task 1: 30分钟
- Task 2: 10分钟
- Task 3: 45分钟
- Task 4: 30分钟

总计：约2小时
