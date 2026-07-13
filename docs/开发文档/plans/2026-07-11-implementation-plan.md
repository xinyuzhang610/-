# 智教通 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use compose:subagent (recommended) or compose:execute to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a complete AI intelligent teaching platform with needs guidance for non-programmers, covering both teacher and student sides.

**Architecture:** Vue3 frontend + FastAPI backend + MySQL database + DeepSeek API integration. Modular design where each feature can be developed and tested independently.

**Tech Stack:** Vue 3, Element Plus, Vite, Python FastAPI, SQLAlchemy, MySQL 8.0, DeepSeek API

## Global Constraints

- Python 3.11+, Node.js 18+
- MySQL 8.0 with utf8mb4 charset
- DeepSeek API key required (model: dsv4)
- All APIs must return JSON with consistent error handling
- Frontend must use Element Plus components for UI consistency
- Each task must be independently runnable and testable

---

## Phase 1: Backend Foundation (Tasks 1-3)

### Task 1: Database Setup & Initialization

**Covers:** Database schema, seed data

**Files:**
- Create: `source/backend/init_db.py` (update existing)
- Modify: `source/backend/sql/init.sql` (verify)
- Modify: `source/backend/sql/seed.sql` (verify)

**Interfaces:**
- Produces: Database `zjiaotong` with all tables and seed data

- [ ] **Step 1: Verify MySQL is running**

Run: `mysql -u root -p`
Expected: MySQL prompt appears

- [ ] **Step 2: Initialize database**

Run: `cd source/backend && python init_db.py`
Expected: "Database initialized successfully" message

- [ ] **Step 3: Verify tables created**

Run: `mysql -u root -p zjiaotong -e "SHOW TABLES;"`
Expected: List of 6 tables (users, tools, tool_templates, usage_logs, favorites, recommend_rules)

- [ ] **Step 4: Verify seed data**

Run: `mysql -u root -p zjiaotong -e "SELECT COUNT(*) FROM tool_templates;"`
Expected: 15 (6 文科 + 6 理科 + 3 通用)

- [ ] **Step 5: Commit**

```bash
git add source/backend/init_db.py source/backend/sql/
git commit -m "feat: database setup with schema and seed data"
```

---

### Task 2: Tool CRUD API

**Covers:** Tool management, preset tools, sharing

**Files:**
- Create: `source/backend/api/tool.py`
- Create: `source/backend/schemas/tool.py`
- Modify: `source/backend/main.py` (register router)

**Interfaces:**
- Consumes: Database tables (tools, tool_templates)
- Produces: RESTful API endpoints for tool management

- [ ] **Step 1: Create tool schemas**

Create `source/backend/schemas/tool.py`:
```python
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ToolCreate(BaseModel):
    name: str
    description: Optional[str] = None
    category: str  # '文科', '理科', '通用'
    subject: Optional[str] = None
    icon: Optional[str] = None
    prompt_template: str
    interface_config: Optional[dict] = None
    is_preset: bool = False
    is_public: bool = True

class ToolResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    category: str
    subject: Optional[str]
    icon: Optional[str]
    prompt_template: str
    interface_config: Optional[dict]
    creator_id: Optional[int]
    is_preset: bool
    is_public: bool
    share_code: Optional[str]
    usage_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ToolListResponse(BaseModel):
    total: int
    items: List[ToolResponse]
```

- [ ] **Step 2: Create tool API**

Create `source/backend/api/tool.py`:
```python
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from models.database import get_db
from models.tool import Tool, ToolTemplate
from schemas.tool import ToolCreate, ToolResponse, ToolListResponse
import uuid

router = APIRouter()

@router.get("/presets", response_model=ToolListResponse)
def get_preset_tools(
    category: str = Query(None, description="筛选分类"),
    db: Session = Depends(get_db)
):
    query = db.query(Tool).filter(Tool.is_preset == True, Tool.is_public == True)
    if category:
        query = query.filter(Tool.category == category)
    total = query.count()
    items = query.all()
    return ToolListResponse(total=total, items=items)

@router.get("/recommend", response_model=ToolListResponse)
def recommend_tools(
    subject: str = Query(..., description="学科"),
    need_type: str = Query(..., description="需求类型"),
    db: Session = Depends(get_db)
):
    # 基于条件匹配的推荐逻辑
    query = db.query(Tool).filter(Tool.is_public == True)
    
    # 根据学科筛选
    if subject in ['语文', '英语', '历史', '政治', '地理']:
        query = query.filter(Tool.category == '文科')
    elif subject in ['数学', '物理', '化学', '生物', '信息技术']:
        query = query.filter(Tool.category == '理科')
    
    # 根据需求类型进一步筛选（简化版）
    if need_type == '兴趣激发':
        query = query.filter(Tool.name.in_(['古诗词趣味赏析', '诗词飞花令', '逻辑思维训练']))
    elif need_type == '课前备课':
        query = query.filter(Tool.name.in_(['作文灵感助手', '公式推导助手', '实验模拟讲解']))
    
    total = query.count()
    items = query.all()
    return ToolListResponse(total=total, items=items)

@router.get("/{tool_id}", response_model=ToolResponse)
def get_tool(tool_id: int, db: Session = Depends(get_db)):
    tool = db.query(Tool).filter(Tool.id == tool_id).first()
    if not tool:
        raise HTTPException(status_code=404, detail="工具不存在")
    return tool

@router.post("/", response_model=ToolResponse)
def create_tool(tool: ToolCreate, creator_id: int = Query(...), db: Session = Depends(get_db)):
    db_tool = Tool(
        **tool.model_dump(),
        creator_id=creator_id,
        share_code=str(uuid.uuid4())[:8]
    )
    db.add(db_tool)
    db.commit()
    db.refresh(db_tool)
    return db_tool

@router.put("/{tool_id}", response_model=ToolResponse)
def update_tool(tool_id: int, tool_update: ToolCreate, db: Session = Depends(get_db)):
    db_tool = db.query(Tool).filter(Tool.id == tool_id).first()
    if not db_tool:
        raise HTTPException(status_code=404, detail="工具不存在")
    
    update_data = tool_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_tool, key, value)
    
    db.commit()
    db.refresh(db_tool)
    return db_tool

@router.delete("/{tool_id}")
def delete_tool(tool_id: int, db: Session = Depends(get_db)):
    db_tool = db.query(Tool).filter(Tool.id == tool_id).first()
    if not db_tool:
        raise HTTPException(status_code=404, detail="工具不存在")
    db.delete(db_tool)
    db.commit()
    return {"message": "删除成功"}

@router.get("/{tool_id}/share")
def get_share_link(tool_id: int, db: Session = Depends(get_db)):
    tool = db.query(Tool).filter(Tool.id == tool_id).first()
    if not tool:
        raise HTTPException(status_code=404, detail="工具不存在")
    return {
        "share_code": tool.share_code,
        "share_url": f"http://localhost:5173/student/tool/{tool.share_code}"
    }
```

- [ ] **Step 3: Register router in main.py**

Modify `source/backend/main.py`:
```python
from api.tool import router as tool_router

app.include_router(tool_router, prefix="/api/tools", tags=["工具管理"])
```

- [ ] **Step 4: Test API endpoints**

Run: `cd source/backend && python main.py`
Open new terminal: `curl http://localhost:8000/api/tools/presets`
Expected: JSON response with preset tools list

- [ ] **Step 5: Commit**

```bash
git add source/backend/api/tool.py source/backend/schemas/tool.py source/backend/main.py
git commit -m "feat: tool CRUD API with preset and recommendation"
```

---

### Task 3: AI Chat API (DeepSeek Integration)

**Covers:** AI interaction, tool usage

**Files:**
- Create: `source/backend/api/chat.py`
- Create: `source/backend/services/deepseek.py`
- Create: `source/backend/schemas/chat.py`
- Modify: `source/backend/main.py` (register router)

**Interfaces:**
- Consumes: Tool prompt templates, DeepSeek API
- Produces: Chat completion responses

- [ ] **Step 1: Create chat schemas**

Create `source/backend/schemas/chat.py`:
```python
from pydantic import BaseModel
from typing import Optional, List

class ChatRequest(BaseModel):
    message: str
    tool_id: Optional[int] = None  # 如果是使用特定工具
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    reply: str
    session_id: str
    tool_name: Optional[str] = None
```

- [ ] **Step 2: Create DeepSeek service**

Create `source/backend/services/deepseek.py`:
```python
import httpx
from config import settings

async def chat_with_deepseek(message: str, system_prompt: str = None) -> str:
    headers = {
        "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": message})
    
    payload = {
        "model": settings.DEEPSEEK_MODEL,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 2000
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.DEEPSEEK_API_URL}/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30.0
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
```

- [ ] **Step 3: Create chat API**

Create `source/backend/api/chat.py`:
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.database import get_db
from models.tool import Tool
from models.usage import UsageLog
from schemas.chat import ChatRequest, ChatResponse
from services.deepseek import chat_with_deepseek
import uuid

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    session_id = request.session_id or str(uuid.uuid4())
    
    # 获取工具提示词（如果指定了工具）
    system_prompt = None
    tool_name = None
    if request.tool_id:
        tool = db.query(Tool).filter(Tool.id == request.tool_id).first()
        if not tool:
            raise HTTPException(status_code=404, detail="工具不存在")
        system_prompt = tool.prompt_template
        tool_name = tool.name
        
        # 更新使用次数
        tool.usage_count += 1
        db.commit()
    
    # 调用DeepSeek API
    try:
        reply = await chat_with_deepseek(request.message, system_prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI服务调用失败: {str(e)}")
    
    # 记录使用日志
    usage_log = UsageLog(
        tool_id=request.tool_id or 1,  # 默认工具ID
        input_text=request.message,
        output_text=reply,
        session_id=session_id
    )
    db.add(usage_log)
    db.commit()
    
    return ChatResponse(
        reply=reply,
        session_id=session_id,
        tool_name=tool_name
    )
```

- [ ] **Step 4: Register router in main.py**

Modify `source/backend/main.py`:
```python
from api.chat import router as chat_router

app.include_router(chat_router, prefix="/api/chat", tags=["AI对话"])
```

- [ ] **Step 5: Test chat API**

Run: `cd source/backend && python main.py`
Test with curl:
```bash
curl -X POST http://localhost:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "你好，请介绍一下你自己"}'
```
Expected: JSON response with AI reply

- [ ] **Step 6: Commit**

```bash
git add source/backend/api/chat.py source/backend/services/deepseek.py source/backend/schemas/chat.py
git commit -m "feat: AI chat API with DeepSeek integration"
```

---

## Phase 2: Backend Business Logic (Tasks 4-6)

### Task 4: Usage Tracking & Statistics API

**Covers:** Data collection, dashboard statistics

**Files:**
- Create: `source/backend/api/usage.py`
- Create: `source/backend/schemas/usage.py`
- Modify: `source/backend/main.py` (register router)

**Interfaces:**
- Consumes: UsageLog table
- Produces: Statistics and dashboard data

- [ ] **Step 1: Create usage schemas**

Create `source/backend/schemas/usage.py`:
```python
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class UsageLogCreate(BaseModel):
    tool_id: int
    user_id: Optional[int] = None
    input_text: Optional[str] = None
    output_text: Optional[str] = None
    session_id: Optional[str] = None

class UsageLogResponse(BaseModel):
    id: int
    tool_id: int
    user_id: Optional[int]
    input_text: Optional[str]
    output_text: Optional[str]
    session_id: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class DashboardStats(BaseModel):
    total_tools: int
    total_users: int
    today_usage: int
    weekly_trend: List[dict]
    top_tools: List[dict]
    recent_logs: List[UsageLogResponse]
```

- [ ] **Step 2: Create usage API**

Create `source/backend/api/usage.py`:
```python
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, date
from models.database import get_db
from models.usage import UsageLog
from models.tool import Tool
from models.user import User
from schemas.usage import UsageLogResponse, DashboardStats
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/my", response_model=List[UsageLogResponse])
def get_my_usage(
    user_id: int = Query(...),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    logs = db.query(UsageLog)\
        .filter(UsageLog.user_id == user_id)\
        .order_by(UsageLog.created_at.desc())\
        .limit(limit)\
        .all()
    return logs

@router.get("/tool/{tool_id}")
def get_tool_usage(
    tool_id: int,
    db: Session = Depends(get_db)
):
    total = db.query(UsageLog).filter(UsageLog.tool_id == tool_id).count()
    today = db.query(UsageLog)\
        .filter(UsageLog.tool_id == tool_id, 
                func.date(UsageLog.created_at) == func.date(func.now()))\
        .count()
    return {"tool_id": tool_id, "total_usage": total, "today_usage": today}

@router.get("/dashboard", response_model=DashboardStats)
def get_dashboard(db: Session = Depends(get_db)):
    # 基础统计
    total_tools = db.query(Tool).count()
    total_users = db.query(User).count()
    today_usage = db.query(UsageLog)\
        .filter(func.date(UsageLog.created_at) == func.date(func.now()))\
        .count()
    
    # 本周趋势（简化版）
    weekly_trend = []
    for i in range(7):
        day = datetime.now() - timedelta(days=6-i)
        count = db.query(UsageLog)\
            .filter(func.date(UsageLog.created_at) == func.date(day))\
            .count()
        weekly_trend.append({"date": day.strftime("%m/%d"), "count": count})
    
    # 热门工具
    top_tools = db.query(
        Tool.name,
        func.count(UsageLog.id).label('usage_count')
    ).join(UsageLog)\
     .group_by(Tool.id)\
     .order_by(func.count(UsageLog.id).desc())\
     .limit(5)\
     .all()
    
    # 最近使用记录
    recent_logs = db.query(UsageLog)\
        .order_by(UsageLog.created_at.desc())\
        .limit(10)\
        .all()
    
    return DashboardStats(
        total_tools=total_tools,
        total_users=total_users,
        today_usage=today_usage,
        weekly_trend=weekly_trend,
        top_tools=[{"name": t[0], "count": t[1]} for t in top_tools],
        recent_logs=recent_logs
    )
```

- [ ] **Step 3: Register router in main.py**

Modify `source/backend/main.py`:
```python
from api.usage import router as usage_router

app.include_router(usage_router, prefix="/api/usage", tags=["使用统计"])
```

- [ ] **Step 4: Test dashboard API**

Run: `cd source/backend && python main.py`
Test with curl:
```bash
curl http://localhost:8000/api/usage/dashboard
```
Expected: JSON with statistics

- [ ] **Step 5: Commit**

```bash
git add source/backend/api/usage.py source/backend/schemas/usage.py
git commit -m "feat: usage tracking and dashboard statistics API"
```

---

### Task 5: Recommendation Logic API

**Covers:** Needs guidance, tool recommendation

**Files:**
- Create: `source/backend/api/recommend.py`
- Create: `source/backend/schemas/recommend.py`
- Modify: `source/backend/main.py` (register router)

**Interfaces:**
- Consumes: Recommend rules, tool templates
- Produces: Personalized recommendations

- [ ] **Step 1: Create recommend schemas**

Create `source/backend/schemas/recommend.py`:
```python
from pydantic import BaseModel
from typing import List, Optional

class RecommendRequest(BaseModel):
    step: int  # 1: 文理分科, 2: 需求选择, 3: 获取推荐
    category: Optional[str] = None  # '文科' or '理科'
    need_type: Optional[str] = None  # 需求类型
    subject: Optional[str] = None  # 具体学科

class RecommendResponse(BaseModel):
    step: int
    message: str
    options: Optional[List[dict]] = None  # 下一步选项
    tools: Optional[List[dict]] = None  # 推荐工具列表
```

- [ ] **Step 2: Create recommend API**

Create `source/backend/api/recommend.py`:
```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.database import get_db
from models.tool import Tool
from schemas.recommend import RecommendRequest, RecommendResponse

router = APIRouter()

# 需求引导流程配置
GUIDANCE_FLOW = {
    1: {
        "message": "请选择您的教学方向：",
        "options": [
            {"value": "文科", "label": "文科", "desc": "语文/英语/历史/政治/地理"},
            {"value": "理科", "label": "理科", "desc": "数学/物理/化学/生物/信息技术"}
        ]
    },
    2: {
        "文科": {
            "message": "您目前最需要帮助的是？",
            "options": [
                {"value": "课前备课", "label": "课前备课", "desc": "找资料、做课件"},
                {"value": "课堂教学", "label": "课堂教学", "desc": "互动、提问、演示"},
                {"value": "课后辅导", "label": "课后辅导", "desc": "作业批改、答疑"},
                {"value": "兴趣激发", "label": "学生兴趣激发", "desc": "趣味学习"}
            ]
        },
        "理科": {
            "message": "您目前最需要帮助的是？",
            "options": [
                {"value": "课前备课", "label": "课前备课", "desc": "找资料、做课件"},
                {"value": "课堂教学", "label": "课堂教学", "desc": "互动、提问、演示"},
                {"value": "课后辅导", "label": "课后辅导", "desc": "作业批改、答疑"},
                {"value": "兴趣激发", "label": "学生兴趣激发", "desc": "趣味学习"}
            ]
        }
    }
}

@router.post("/", response_model=RecommendResponse)
def get_recommendation(request: RecommendRequest, db: Session = Depends(get_db)):
    if request.step == 1:
        # 返回文理分科选项
        flow = GUIDANCE_FLOW[1]
        return RecommendResponse(
            step=1,
            message=flow["message"],
            options=flow["options"]
        )
    
    elif request.step == 2:
        # 返回需求类型选项
        if request.category not in GUIDANCE_FLOW[2]:
            return RecommendResponse(step=2, message="无效的分类")
        flow = GUIDANCE_FLOW[2][request.category]
        return RecommendResponse(
            step=2,
            message=flow["message"],
            options=flow["options"]
        )
    
    elif request.step == 3:
        # 返回推荐工具
        query = db.query(Tool).filter(Tool.is_public == True)
        
        # 根据分类筛选
        if request.category == "文科":
            query = query.filter(Tool.category == "文科")
        elif request.category == "理科":
            query = query.filter(Tool.category == "理科")
        
        # 根据需求类型筛选
        if request.need_type == "兴趣激发":
            query = query.filter(Tool.name.in_([
                "古诗词趣味赏析", "诗词飞花令", "逻辑思维训练"
            ]))
        elif request.need_type == "课前备课":
            query = query.filter(Tool.name.in_([
                "作文灵感助手", "公式推导助手", "实验模拟讲解"
            ]))
        
        tools = query.all()
        tool_list = [
            {
                "id": t.id,
                "name": t.name,
                "description": t.description,
                "icon": t.icon,
                "subject": t.subject
            }
            for t in tools
        ]
        
        return RecommendResponse(
            step=3,
            message=f"根据您的选择，为您推荐以下工具：",
            tools=tool_list
        )
    
    return RecommendResponse(step=request.step, message="无效的步骤")
```

- [ ] **Step 3: Register router in main.py**

Modify `source/backend/main.py`:
```python
from api.recommend import router as recommend_router

app.include_router(recommend_router, prefix="/api/recommend", tags=["需求推荐"])
```

- [ ] **Step 4: Test recommendation flow**

Run: `cd source/backend && python main.py`
Test step 1:
```bash
curl -X POST http://localhost:8000/api/recommend/ \
  -H "Content-Type: application/json" \
  -d '{"step": 1}'
```
Test step 3:
```bash
curl -X POST http://localhost:8000/api/recommend/ \
  -H "Content-Type: application/json" \
  -d '{"step": 3, "category": "文科", "need_type": "兴趣激发"}'
```
Expected: Tool recommendations based on selection

- [ ] **Step 5: Commit**

```bash
git add source/backend/api/recommend.py source/backend/schemas/recommend.py
git commit -m "feat: needs guidance recommendation API"
```

---

### Task 6: Tool Plaza API

**Covers:** Tool browsing, categorization, search

**Files:**
- Create: `source/backend/api/plaza.py`
- Create: `source/backend/schemas/plaza.py`
- Modify: `source/backend/main.py` (register router)

**Interfaces:**
- Consumes: Tools table
- Produces: Plaza browsing data

- [ ] **Step 1: Create plaza schemas**

Create `source/backend/schemas/plaza.py`:
```python
from pydantic import BaseModel
from typing import List, Optional

class PlazaTool(BaseModel):
    id: int
    name: str
    description: Optional[str]
    category: str
    subject: Optional[str]
    icon: Optional[str]
    usage_count: int
    share_code: Optional[str]

    class Config:
        from_attributes = True

class PlazaResponse(BaseModel):
    categories: List[dict]
    tools: List[PlazaTool]
    hot_tools: List[PlazaTool]
```

- [ ] **Step 2: Create plaza API**

Create `source/backend/api/plaza.py`:
```python
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from models.database import get_db
from models.tool import Tool
from schemas.plaza import PlazaResponse, PlazaTool

router = APIRouter()

@router.get("/", response_model=PlazaResponse)
def get_plaza(
    category: str = Query(None, description="分类筛选"),
    search: str = Query(None, description="搜索关键词"),
    db: Session = Depends(get_db)
):
    # 获取分类列表
    categories = [
        {"value": "文科", "label": "文科专区", "icon": "📚"},
        {"value": "理科", "label": "理科专区", "icon": "🔬"},
        {"value": "通用", "label": "通用工具", "icon": "🛠️"}
    ]
    
    # 查询工具
    query = db.query(Tool).filter(Tool.is_public == True)
    
    if category:
        query = query.filter(Tool.category == category)
    
    if search:
        query = query.filter(Tool.name.contains(search) | Tool.description.contains(search))
    
    tools = query.order_by(Tool.usage_count.desc()).all()
    
    # 热门工具（按使用次数排序）
    hot_tools = db.query(Tool)\
        .filter(Tool.is_public == True)\
        .order_by(Tool.usage_count.desc())\
        .limit(5)\
        .all()
    
    return PlazaResponse(
        categories=categories,
        tools=tools,
        hot_tools=hot_tools
    )

@router.get("/categories")
def get_categories():
    return [
        {"value": "文科", "label": "文科专区", "icon": "📚"},
        {"value": "理科", "label": "理科专区", "icon": "🔬"},
        {"value": "通用", "label": "通用工具", "icon": "🛠️"}
    ]

@router.get("/hot")
def get_hot_tools(limit: int = Query(5, ge=1, le=20), db: Session = Depends(get_db)):
    tools = db.query(Tool)\
        .filter(Tool.is_public == True)\
        .order_by(Tool.usage_count.desc())\
        .limit(limit)\
        .all()
    return tools
```

- [ ] **Step 3: Register router in main.py**

Modify `source/backend/main.py`:
```python
from api.plaza import router as plaza_router

app.include_router(plaza_router, prefix="/api/plaza", tags=["工具广场"])
```

- [ ] **Step 4: Test plaza API**

Run: `cd source/backend && python main.py`
Test with curl:
```bash
curl http://localhost:8000/api/plaza/
curl "http://localhost:8000/api/plaza/?category=文科"
```
Expected: Tool list with categories

- [ ] **Step 5: Commit**

```bash
git add source/backend/api/plaza.py source/backend/schemas/plaza.py
git commit -m "feat: tool plaza API with categories and search"
```

---

## Phase 3: Frontend Foundation (Tasks 7-9)

### Task 7: Router & Layout Setup

**Covers:** Frontend routing, page structure

**Files:**
- Modify: `source/frontend/src/router/index.js`
- Create: `source/frontend/src/layouts/TeacherLayout.vue`
- Create: `source/frontend/src/layouts/StudentLayout.vue`

**Interfaces:**
- Produces: Route configuration, layout components

- [ ] **Step 1: Update router configuration**

Modify `source/frontend/src/router/index.js`:
```javascript
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/auth/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/auth/Register.vue')
  },
  // 教师端
  {
    path: '/teacher',
    component: () => import('../layouts/TeacherLayout.vue'),
    children: [
      {
        path: '',
        name: 'TeacherHome',
        component: () => import('../views/teacher/Guidance.vue')
      },
      {
        path: 'tools',
        name: 'TeacherTools',
        component: () => import('../views/teacher/MyTools.vue')
      },
      {
        path: 'dashboard',
        name: 'TeacherDashboard',
        component: () => import('../views/teacher/Dashboard.vue')
      }
    ]
  },
  // 学生端
  {
    path: '/student',
    component: () => import('../layouts/StudentLayout.vue'),
    children: [
      {
        path: '',
        name: 'StudentHome',
        component: () => import('../views/student/Plaza.vue')
      },
      {
        path: 'tool/:shareCode',
        name: 'StudentTool',
        component: () => import('../views/student/ToolUse.vue')
      },
      {
        path: 'chat',
        name: 'StudentChat',
        component: () => import('../views/student/AIChat.vue')
      },
      {
        path: 'records',
        name: 'StudentRecords',
        component: () => import('../views/student/Records.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
```

- [ ] **Step 2: Create TeacherLayout**

Create `source/frontend/src/layouts/TeacherLayout.vue`:
```vue
<template>
  <el-container class="layout-container">
    <el-aside width="200px" class="aside">
      <div class="logo">智教通</div>
      <el-menu
        :default-active="activeMenu"
        router
        class="aside-menu"
      >
        <el-menu-item index="/teacher">
          <span>需求引导</span>
        </el-menu-item>
        <el-menu-item index="/teacher/tools">
          <span>我的工具</span>
        </el-menu-item>
        <el-menu-item index="/teacher/dashboard">
          <span>数据看板</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="header">
        <span>教师端</span>
        <el-button type="text" @click="logout">退出登录</el-button>
      </el-header>
      <el-main class="main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const activeMenu = computed(() => route.path)

const logout = () => {
  localStorage.removeItem('token')
  router.push('/login')
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
}
.aside {
  background-color: #304156;
}
.logo {
  height: 60px;
  line-height: 60px;
  text-align: center;
  color: #fff;
  font-size: 20px;
  font-weight: bold;
}
.aside-menu {
  border-right: none;
}
.header {
  background-color: #fff;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 1px 4px rgba(0,21,41,.08);
}
.main {
  background-color: #f0f2f5;
  padding: 20px;
}
</style>
```

- [ ] **Step 3: Create StudentLayout**

Create `source/frontend/src/layouts/StudentLayout.vue`:
```vue
<template>
  <el-container class="layout-container">
    <el-header class="header">
      <div class="header-left">
        <span class="logo">智教通</span>
        <el-menu
          :default-active="activeMenu"
          mode="horizontal"
          router
          class="nav-menu"
        >
          <el-menu-item index="/student">工具广场</el-menu-item>
          <el-menu-item index="/student/chat">AI问答</el-menu-item>
          <el-menu-item index="/student/records">学习记录</el-menu-item>
        </el-menu>
      </div>
      <el-button type="text" @click="goHome">返回首页</el-button>
    </el-header>
    <el-main class="main">
      <router-view />
    </el-main>
  </el-container>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const activeMenu = computed(() => route.path)

const goHome = () => {
  router.push('/')
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
}
.header {
  background-color: #fff;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 1px 4px rgba(0,21,41,.08);
}
.header-left {
  display: flex;
  align-items: center;
}
.logo {
  font-size: 20px;
  font-weight: bold;
  margin-right: 30px;
}
.nav-menu {
  border-bottom: none;
}
.main {
  background-color: #f0f2f5;
  padding: 20px;
}
</style>
```

- [ ] **Step 4: Test routing**

Run: `cd source/frontend && npm run dev`
Open browser: http://localhost:5173/teacher
Expected: Teacher layout with sidebar menu

- [ ] **Step 5: Commit**

```bash
git add source/frontend/src/router/index.js source/frontend/src/layouts/
git commit -m "feat: frontend router and layout components"
```

---

### Task 8: Login/Register Pages

**Covers:** User authentication UI

**Files:**
- Create: `source/frontend/src/views/auth/Login.vue`
- Create: `source/frontend/src/views/auth/Register.vue`
- Create: `source/frontend/src/api/auth.js`

**Interfaces:**
- Consumes: Backend auth API
- Produces: Token stored in localStorage

- [ ] **Step 1: Create auth API service**

Create `source/frontend/src/api/auth.js`:
```javascript
import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 10000
})

export const login = (data) => api.post('/auth/login', data)
export const register = (data) => api.post('/auth/register', data)
export const getProfile = (userId) => api.get(`/auth/profile/${userId}`)
```

- [ ] **Step 2: Create Login page**

Create `source/frontend/src/views/auth/Login.vue`:
```vue
<template>
  <div class="login-container">
    <el-card class="login-card">
      <h2>登录智教通</h2>
      <el-form :model="form" :rules="rules" ref="formRef">
        <el-form-item prop="username">
          <el-input v-model="form.username" placeholder="用户名" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="form.password" type="password" placeholder="密码" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleLogin" :loading="loading" style="width: 100%">
            登录
          </el-button>
        </el-form-item>
      </el-form>
      <div class="footer">
        还没有账号？<router-link to="/register">立即注册</router-link>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { login } from '@/api/auth'
import { ElMessage } from 'element-plus'

const router = useRouter()
const formRef = ref(null)
const loading = ref(false)

const form = reactive({
  username: '',
  password: ''
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

const handleLogin = async () => {
  try {
    await formRef.value.validate()
    loading.value = true
    
    const { data } = await login(form)
    localStorage.setItem('token', data.access_token)
    localStorage.setItem('user', JSON.stringify(data.user))
    
    ElMessage.success('登录成功')
    
    // 根据角色跳转
    if (data.user.role === 'teacher') {
      router.push('/teacher')
    } else {
      router.push('/student')
    }
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '登录失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
.login-card {
  width: 400px;
  padding: 20px;
}
h2 {
  text-align: center;
  margin-bottom: 30px;
}
.footer {
  text-align: center;
  margin-top: 20px;
}
</style>
```

- [ ] **Step 3: Create Register page**

Create `source/frontend/src/views/auth/Register.vue`:
```vue
<template>
  <div class="register-container">
    <el-card class="register-card">
      <h2>注册智教通</h2>
      <el-form :model="form" :rules="rules" ref="formRef">
        <el-form-item prop="username">
          <el-input v-model="form.username" placeholder="用户名" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="form.password" type="password" placeholder="密码" />
        </el-form-item>
        <el-form-item prop="role">
          <el-radio-group v-model="form.role">
            <el-radio value="teacher">我是老师</el-radio>
            <el-radio value="student">我是学生</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item v-if="form.role === 'teacher'" prop="name">
          <el-input v-model="form.name" placeholder="姓名" />
        </el-form-item>
        <el-form-item v-if="form.role === 'teacher'" prop="subject">
          <el-select v-model="form.subject" placeholder="选择学科" style="width: 100%">
            <el-option label="语文" value="语文" />
            <el-option label="数学" value="数学" />
            <el-option label="英语" value="英语" />
            <el-option label="物理" value="物理" />
            <el-option label="化学" value="化学" />
            <el-option label="生物" value="生物" />
            <el-option label="历史" value="历史" />
            <el-option label="政治" value="政治" />
            <el-option label="地理" value="地理" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleRegister" :loading="loading" style="width: 100%">
            注册
          </el-button>
        </el-form-item>
      </el-form>
      <div class="footer">
        已有账号？<router-link to="/login">立即登录</router-link>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { register } from '@/api/auth'
import { ElMessage } from 'element-plus'

const router = useRouter()
const formRef = ref(null)
const loading = ref(false)

const form = reactive({
  username: '',
  password: '',
  role: 'teacher',
  name: '',
  subject: ''
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
  role: [{ required: true, message: '请选择角色', trigger: 'change' }]
}

const handleRegister = async () => {
  try {
    await formRef.value.validate()
    loading.value = true
    
    await register(form)
    ElMessage.success('注册成功')
    router.push('/login')
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '注册失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
.register-card {
  width: 400px;
  padding: 20px;
}
h2 {
  text-align: center;
  margin-bottom: 30px;
}
.footer {
  text-align: center;
  margin-top: 20px;
}
</style>
```

- [ ] **Step 4: Test login/register**

Run: `cd source/frontend && npm run dev`
Open browser: http://localhost:5173/register
Expected: Registration form, can submit and redirect to login

- [ ] **Step 5: Commit**

```bash
git add source/frontend/src/views/auth/ source/frontend/src/api/auth.js
git commit -m "feat: login and register pages with API integration"
```

---

### Task 9: API Service Layer

**Covers:** Frontend-backend communication

**Files:**
- Create: `source/frontend/src/api/tools.js`
- Create: `source/frontend/src/api/chat.js`
- Create: `source/frontend/src/api/usage.js`
- Create: `source/frontend/src/api/recommend.js`
- Create: `source/frontend/src/api/plaza.js`

**Interfaces:**
- Produces: API service functions for all endpoints

- [ ] **Step 1: Create tools API service**

Create `source/frontend/src/api/tools.js`:
```javascript
import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 10000
})

export const getPresetTools = (category) => 
  api.get('/tools/presets', { params: { category } })

export const getTool = (id) => 
  api.get(`/tools/${id}`)

export const createTool = (data, creatorId) => 
  api.post('/tools/', data, { params: { creator_id: creatorId } })

export const updateTool = (id, data) => 
  api.put(`/tools/${id}`, data)

export const deleteTool = (id) => 
  api.delete(`/tools/${id}`)

export const getShareLink = (id) => 
  api.get(`/tools/${id}/share`)
```

- [ ] **Step 2: Create chat API service**

Create `source/frontend/src/api/chat.js`:
```javascript
import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 30000
})

export const sendMessage = (data) => 
  api.post('/chat/', data)
```

- [ ] **Step 3: Create usage API service**

Create `source/frontend/src/api/usage.js`:
```javascript
import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 10000
})

export const getMyUsage = (userId, limit = 20) => 
  api.get('/usage/my', { params: { user_id: userId, limit } })

export const getToolUsage = (toolId) => 
  api.get(`/usage/tool/${toolId}`)

export const getDashboard = () => 
  api.get('/usage/dashboard')
```

- [ ] **Step 4: Create recommend API service**

Create `source/frontend/src/api/recommend.js`:
```javascript
import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 10000
})

export const getRecommendation = (data) => 
  api.post('/recommend/', data)
```

- [ ] **Step 5: Create plaza API service**

Create `source/frontend/src/api/plaza.js`:
```javascript
import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 10000
})

export const getPlaza = (category, search) => 
  api.get('/plaza/', { params: { category, search } })

export const getCategories = () => 
  api.get('/plaza/categories')

export const getHotTools = (limit = 5) => 
  api.get('/plaza/hot', { params: { limit } })
```

- [ ] **Step 6: Commit**

```bash
git add source/frontend/src/api/
git commit -m "feat: frontend API service layer for all endpoints"
```

---

## Phase 4: Frontend Core Pages (Tasks 10-14)

### Task 10: Teacher - Needs Guidance Flow (Core Innovation)

**Covers:** [S2, S3] Core innovation point - needs guidance

**Files:**
- Create: `source/frontend/src/views/teacher/Guidance.vue`

**Interfaces:**
- Consumes: Recommend API
- Produces: Multi-step guidance UI

- [ ] **Step 1: Create Guidance page**

Create `source/frontend/src/views/teacher/Guidance.vue`:
```vue
<template>
  <div class="guidance-container">
    <el-card class="guidance-card">
      <h2>需求引导</h2>
      <p class="subtitle">让我帮您找到最合适的AI工具</p>
      
      <!-- 步骤条 -->
      <el-steps :active="currentStep" finish-status="success" align-center>
        <el-step title="选择方向" />
        <el-step title="明确需求" />
        <el-step title="获取推荐" />
      </el-steps>
      
      <!-- 步骤1: 文理分科 -->
      <div v-if="currentStep === 0" class="step-content">
        <h3>{{ guidanceData.message }}</h3>
        <div class="options-grid">
          <el-card 
            v-for="option in guidanceData.options" 
            :key="option.value"
            class="option-card"
            :class="{ active: selectedCategory === option.value }"
            @click="selectCategory(option.value)"
          >
            <div class="option-icon">{{ option.value === '文科' ? '📚' : '🔬' }}</div>
            <div class="option-label">{{ option.label }}</div>
            <div class="option-desc">{{ option.desc }}</div>
          </el-card>
        </div>
      </div>
      
      <!-- 步骤2: 需求选择 -->
      <div v-if="currentStep === 1" class="step-content">
        <h3>{{ guidanceData.message }}</h3>
        <div class="options-list">
          <el-radio-group v-model="selectedNeed" @change="handleNeedSelect">
            <el-radio 
              v-for="option in guidanceData.options" 
              :key="option.value"
              :value="option.value"
              class="need-option"
            >
              <span class="need-label">{{ option.label }}</span>
              <span class="need-desc">{{ option.desc }}</span>
            </el-radio>
          </el-radio-group>
        </div>
      </div>
      
      <!-- 步骤3: 推荐结果 -->
      <div v-if="currentStep === 2" class="step-content">
        <h3>{{ guidanceData.message }}</h3>
        <div class="tools-grid">
          <el-card 
            v-for="tool in guidanceData.tools" 
            :key="tool.id"
            class="tool-card"
          >
            <div class="tool-icon">{{ tool.icon }}</div>
            <div class="tool-name">{{ tool.name }}</div>
            <div class="tool-desc">{{ tool.description }}</div>
            <div class="tool-subject">{{ tool.subject }}</div>
            <el-button type="primary" size="small" @click="useTool(tool)">
              立即体验
            </el-button>
          </el-card>
        </div>
        
        <div class="action-buttons">
          <el-button @click="resetGuidance">重新选择</el-button>
          <el-button type="primary" @click="goToCreateTool">
            没有合适的？创建新工具
          </el-button>
        </div>
      </div>
      
      <!-- 导航按钮 -->
      <div class="nav-buttons" v-if="currentStep < 2">
        <el-button v-if="currentStep > 0" @click="prevStep">上一步</el-button>
        <el-button 
          type="primary" 
          @click="nextStep"
          :disabled="!canProceed"
        >
          下一步
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getRecommendation } from '@/api/recommend'
import { ElMessage } from 'element-plus'

const router = useRouter()
const currentStep = ref(0)
const selectedCategory = ref('')
const selectedNeed = ref('')
const guidanceData = ref({ message: '', options: [] })

const canProceed = ref(false)

onMounted(async () => {
  await loadStep1()
})

const loadStep1 = async () => {
  try {
    const { data } = await getRecommendation({ step: 1 })
    guidanceData.value = data
  } catch (error) {
    ElMessage.error('加载失败')
  }
}

const selectCategory = (value) => {
  selectedCategory.value = value
  canProceed.value = true
}

const nextStep = async () => {
  if (currentStep.value === 0) {
    // 加载步骤2
    try {
      const { data } = await getRecommendation({ 
        step: 2, 
        category: selectedCategory.value 
      })
      guidanceData.value = data
      currentStep.value++
      canProceed.value = false
    } catch (error) {
      ElMessage.error('加载失败')
    }
  } else if (currentStep.value === 1) {
    // 加载步骤3
    try {
      const { data } = await getRecommendation({ 
        step: 3, 
        category: selectedCategory.value,
        need_type: selectedNeed.value
      })
      guidanceData.value = data
      currentStep.value++
    } catch (error) {
      ElMessage.error('加载失败')
    }
  }
}

const prevStep = () => {
  currentStep.value--
  if (currentStep.value === 0) {
    loadStep1()
    canProceed.value = true
  }
}

const handleNeedSelect = () => {
  canProceed.value = true
}

const useTool = (tool) => {
  router.push(`/student/tool/${tool.share_code}`)
}

const resetGuidance = () => {
  currentStep.value = 0
  selectedCategory.value = ''
  selectedNeed.value = ''
  loadStep1()
  canProceed.value = false
}

const goToCreateTool = () => {
  router.push('/teacher/tools')
}
</script>

<style scoped>
.guidance-container {
  max-width: 800px;
  margin: 0 auto;
}
.guidance-card {
  padding: 20px;
}
.subtitle {
  color: #666;
  text-align: center;
  margin-bottom: 30px;
}
.step-content {
  margin-top: 30px;
}
.options-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-top: 20px;
}
.option-card {
  cursor: pointer;
  text-align: center;
  transition: all 0.3s;
}
.option-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
.option-card.active {
  border-color: #409eff;
  background-color: #ecf5ff;
}
.option-icon {
  font-size: 48px;
  margin-bottom: 10px;
}
.option-label {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 5px;
}
.option-desc {
  color: #666;
  font-size: 14px;
}
.need-option {
  display: block;
  margin: 15px 0;
  padding: 15px;
  border: 1px solid #eee;
  border-radius: 8px;
}
.need-label {
  font-weight: bold;
  display: block;
  margin-bottom: 5px;
}
.need-desc {
  color: #666;
  font-size: 14px;
}
.tools-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 20px;
}
.tool-card {
  text-align: center;
}
.tool-icon {
  font-size: 36px;
  margin-bottom: 10px;
}
.tool-name {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 5px;
}
.tool-desc {
  color: #666;
  font-size: 14px;
  margin-bottom: 10px;
}
.tool-subject {
  color: #999;
  font-size: 12px;
  margin-bottom: 15px;
}
.action-buttons {
  text-align: center;
  margin-top: 30px;
}
.nav-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 30px;
}
</style>
```

- [ ] **Step 2: Test guidance flow**

Run: `cd source/frontend && npm run dev`
Open browser: http://localhost:5173/teacher
Expected: 3-step guidance flow with category selection → need selection → tool recommendations

- [ ] **Step 3: Commit**

```bash
git add source/frontend/src/views/teacher/Guidance.vue
git commit -m "feat: teacher needs guidance flow (core innovation)"
```

---

### Task 11: Teacher - Tool Management

**Covers:** Tool CRUD UI, sharing

**Files:**
- Create: `source/frontend/src/views/teacher/MyTools.vue`
- Create: `source/frontend/src/components/ToolCard.vue`

**Interfaces:**
- Consumes: Tools API
- Produces: Tool management UI

- [ ] **Step 1: Create ToolCard component**

Create `source/frontend/src/components/ToolCard.vue`:
```vue
<template>
  <el-card class="tool-card">
    <div class="tool-header">
      <span class="tool-icon">{{ tool.icon }}</span>
      <span class="tool-name">{{ tool.name }}</span>
    </div>
    <div class="tool-info">
      <div class="tool-category">
        <el-tag :type="tool.category === '文科' ? 'success' : 'primary'">
          {{ tool.category }}
        </el-tag>
        <el-tag v-if="tool.subject">{{ tool.subject }}</el-tag>
      </div>
      <div class="tool-usage">使用次数: {{ tool.usage_count }}</div>
    </div>
    <div class="tool-actions">
      <el-button size="small" @click="$emit('edit', tool)">编辑</el-button>
      <el-button size="small" type="primary" @click="$emit('share', tool)">分享</el-button>
      <el-button size="small" type="danger" @click="$emit('delete', tool)">删除</el-button>
    </div>
  </el-card>
</template>

<script setup>
defineProps({
  tool: {
    type: Object,
    required: true
  }
})

defineEmits(['edit', 'share', 'delete'])
</script>

<style scoped>
.tool-card {
  margin-bottom: 15px;
}
.tool-header {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}
.tool-icon {
  font-size: 24px;
  margin-right: 10px;
}
.tool-name {
  font-size: 16px;
  font-weight: bold;
}
.tool-info {
  margin-bottom: 15px;
}
.tool-category {
  margin-bottom: 5px;
}
.tool-usage {
  color: #666;
  font-size: 14px;
}
.tool-actions {
  display: flex;
  gap: 10px;
}
</style>
```

- [ ] **Step 2: Create MyTools page**

Create `source/frontend/src/views/teacher/MyTools.vue`:
```vue
<template>
  <div class="my-tools">
    <div class="header">
      <h2>我的工具</h2>
      <el-button type="primary" @click="showCreateDialog">
        + 创建新工具
      </el-button>
    </div>
    
    <div class="tools-list">
      <ToolCard
        v-for="tool in tools"
        :key="tool.id"
        :tool="tool"
        @edit="editTool"
        @share="shareTool"
        @delete="deleteTool"
      />
      
      <el-empty v-if="tools.length === 0" description="还没有工具，快去创建吧！" />
    </div>
    
    <!-- 创建/编辑对话框 -->
    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑工具' : '创建工具'" width="600px">
      <el-form :model="form" :rules="rules" ref="formRef">
        <el-form-item label="工具名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入工具名称" />
        </el-form-item>
        <el-form-item label="工具描述" prop="description">
          <el-input v-model="form.description" type="textarea" placeholder="请输入工具描述" />
        </el-form-item>
        <el-form-item label="分类" prop="category">
          <el-radio-group v-model="form.category">
            <el-radio value="文科">文科</el-radio>
            <el-radio value="理科">理科</el-radio>
            <el-radio value="通用">通用</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="学科" prop="subject">
          <el-input v-model="form.subject" placeholder="如：语文、数学" />
        </el-form-item>
        <el-form-item label="图标" prop="icon">
          <el-input v-model="form.icon" placeholder="输入emoji图标" />
        </el-form-item>
        <el-form-item label="提示词模板" prop="prompt_template">
          <el-input 
            v-model="form.prompt_template" 
            type="textarea" 
            :rows="4"
            placeholder="输入AI系统的提示词，如：你是一个古诗词赏析助手..." 
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitTool" :loading="loading">
          {{ isEdit ? '保存' : '创建' }}
        </el-button>
      </template>
    </el-dialog>
    
    <!-- 分享对话框 -->
    <el-dialog v-model="shareDialogVisible" title="分享工具" width="400px">
      <div class="share-content">
        <p>分享链接：</p>
        <el-input v-model="shareUrl" readonly>
          <template #append>
            <el-button @click="copyLink">复制</el-button>
          </template>
        </el-input>
        <p style="margin-top: 20px;">学生可以通过此链接直接使用工具</p>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getPresetTools, createTool, updateTool, deleteTool as apiDeleteTool, getShareLink } from '@/api/tools'
import { ElMessage, ElMessageBox } from 'element-plus'
import ToolCard from '@/components/ToolCard.vue'

const tools = ref([])
const dialogVisible = ref(false)
const shareDialogVisible = ref(false)
const isEdit = ref(false)
const loading = ref(false)
const formRef = ref(null)
const shareUrl = ref('')

const form = ref({
  name: '',
  description: '',
  category: '文科',
  subject: '',
  icon: '🤖',
  prompt_template: ''
})

const rules = {
  name: [{ required: true, message: '请输入工具名称', trigger: 'blur' }],
  category: [{ required: true, message: '请选择分类', trigger: 'change' }],
  prompt_template: [{ required: true, message: '请输入提示词模板', trigger: 'blur' }]
}

onMounted(async () => {
  await loadTools()
})

const loadTools = async () => {
  try {
    const { data } = await getPresetTools()
    tools.value = data.items
  } catch (error) {
    ElMessage.error('加载工具列表失败')
  }
}

const showCreateDialog = () => {
  isEdit.value = false
  form.value = {
    name: '',
    description: '',
    category: '文科',
    subject: '',
    icon: '🤖',
    prompt_template: ''
  }
  dialogVisible.value = true
}

const editTool = (tool) => {
  isEdit.value = true
  form.value = { ...tool }
  dialogVisible.value = true
}

const submitTool = async () => {
  try {
    await formRef.value.validate()
    loading.value = true
    
    const user = JSON.parse(localStorage.getItem('user'))
    
    if (isEdit.value) {
      await updateTool(form.value.id, form.value)
      ElMessage.success('更新成功')
    } else {
      await createTool(form.value, user.id)
      ElMessage.success('创建成功')
    }
    
    dialogVisible.value = false
    await loadTools()
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '操作失败')
  } finally {
    loading.value = false
  }
}

const deleteTool = async (tool) => {
  try {
    await ElMessageBox.confirm('确定要删除这个工具吗？', '提示', {
      type: 'warning'
    })
    
    await apiDeleteTool(tool.id)
    ElMessage.success('删除成功')
    await loadTools()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const shareTool = async (tool) => {
  try {
    const { data } = await getShareLink(tool.id)
    shareUrl.value = data.share_url
    shareDialogVisible.value = true
  } catch (error) {
    ElMessage.error('获取分享链接失败')
  }
}

const copyLink = () => {
  navigator.clipboard.writeText(shareUrl.value)
  ElMessage.success('链接已复制')
}
</script>

<style scoped>
.my-tools {
  max-width: 1000px;
  margin: 0 auto;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.tools-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}
.share-content {
  text-align: center;
}
</style>
```

- [ ] **Step 3: Test tool management**

Run: `cd source/frontend && npm run dev`
Open browser: http://localhost:5173/teacher/tools
Expected: Tool list with create/edit/delete/share functionality

- [ ] **Step 4: Commit**

```bash
git add source/frontend/src/views/teacher/MyTools.vue source/frontend/src/components/ToolCard.vue
git commit -m "feat: teacher tool management with CRUD and sharing"
```

---

### Task 12: Teacher - Data Dashboard

**Covers:** Statistics visualization, usage trends

**Files:**
- Create: `source/frontend/src/views/teacher/Dashboard.vue`

**Interfaces:**
- Consumes: Dashboard API
- Produces: Statistics charts and tables

- [ ] **Step 1: Create Dashboard page**

Create `source/frontend/src/views/teacher/Dashboard.vue`:
```vue
<template>
  <div class="dashboard">
    <h2>数据看板</h2>
    
    <!-- 统计卡片 -->
    <div class="stats-cards">
      <el-card class="stat-card">
        <div class="stat-value">{{ stats.total_tools }}</div>
        <div class="stat-label">工具总数</div>
      </el-card>
      <el-card class="stat-card">
        <div class="stat-value">{{ stats.total_users }}</div>
        <div class="stat-label">学生人数</div>
      </el-card>
      <el-card class="stat-card">
        <div class="stat-value">{{ stats.today_usage }}</div>
        <div class="stat-label">今日使用</div>
      </el-card>
    </div>
    
    <!-- 使用趋势图 -->
    <el-card class="trend-card">
      <template #header>
        <span>本周使用趋势</span>
      </template>
      <div class="trend-chart">
        <div 
          v-for="item in stats.weekly_trend" 
          :key="item.date"
          class="trend-bar"
        >
          <div class="bar" :style="{ height: getBarHeight(item.count) + 'px' }"></div>
          <div class="date">{{ item.date }}</div>
          <div class="count">{{ item.count }}</div>
        </div>
      </div>
    </el-card>
    
    <!-- 热门工具排行 -->
    <el-card class="ranking-card">
      <template #header>
        <span>热门工具排行</span>
      </template>
      <div class="ranking-list">
        <div 
          v-for="(tool, index) in stats.top_tools" 
          :key="tool.name"
          class="ranking-item"
        >
          <span class="rank">{{ index + 1 }}</span>
          <span class="name">{{ tool.name }}</span>
          <span class="count">{{ tool.count }}次</span>
        </div>
      </div>
    </el-card>
    
    <!-- 最近使用记录 -->
    <el-card class="records-card">
      <template #header>
        <span>最近使用记录</span>
      </template>
      <el-table :data="stats.recent_logs" stripe>
        <el-table-column prop="tool_id" label="工具ID" width="80" />
        <el-table-column prop="input_text" label="输入内容" show-overflow-tooltip />
        <el-table-column prop="created_at" label="时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getDashboard } from '@/api/usage'
import { ElMessage } from 'element-plus'

const stats = ref({
  total_tools: 0,
  total_users: 0,
  today_usage: 0,
  weekly_trend: [],
  top_tools: [],
  recent_logs: []
})

onMounted(async () => {
  await loadDashboard()
})

const loadDashboard = async () => {
  try {
    const { data } = await getDashboard()
    stats.value = data
  } catch (error) {
    ElMessage.error('加载数据看板失败')
  }
}

const getBarHeight = (count) => {
  const maxCount = Math.max(...stats.value.weekly_trend.map(i => i.count), 1)
  return (count / maxCount) * 100
}

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN')
}
</script>

<style scoped>
.dashboard {
  max-width: 1200px;
  margin: 0 auto;
}
.stats-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}
.stat-card {
  text-align: center;
}
.stat-value {
  font-size: 36px;
  font-weight: bold;
  color: #409eff;
}
.stat-label {
  color: #666;
  margin-top: 10px;
}
.trend-card, .ranking-card, .records-card {
  margin-bottom: 20px;
}
.trend-chart {
  display: flex;
  align-items: flex-end;
  justify-content: space-around;
  height: 150px;
  padding: 20px 0;
}
.trend-bar {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.bar {
  width: 40px;
  background: linear-gradient(180deg, #409eff, #66b1ff);
  border-radius: 4px 4px 0 0;
  min-height: 5px;
}
.date {
  margin-top: 10px;
  font-size: 12px;
  color: #666;
}
.count {
  font-size: 12px;
  color: #409eff;
}
.ranking-list {
  padding: 0;
}
.ranking-item {
  display: flex;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #eee;
}
.rank {
  width: 30px;
  height: 30px;
  background: #409eff;
  color: #fff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
  font-weight: bold;
}
.ranking-item:nth-child(1) .rank {
  background: #f56c6c;
}
.ranking-item:nth-child(2) .rank {
  background: #e6a23c;
}
.ranking-item:nth-child(3) .rank {
  background: #67c23a;
}
.name {
  flex: 1;
}
.count {
  color: #666;
}
</style>
```

- [ ] **Step 2: Test dashboard**

Run: `cd source/frontend && npm run dev`
Open browser: http://localhost:5173/teacher/dashboard
Expected: Statistics cards, trend chart, ranking list, recent logs

- [ ] **Step 3: Commit**

```bash
git add source/frontend/src/views/teacher/Dashboard.vue
git commit -m "feat: teacher data dashboard with statistics"
```

---

### Task 13: Student - Needs Guidance Flow

**Covers:** Student-side innovation point - needs guidance for students

**Files:**
- Create: `source/frontend/src/views/student/Guidance.vue`
- Modify: `source/frontend/src/router/index.js` (add student guidance route)
- Modify: `source/frontend/src/layouts/StudentLayout.vue` (update navigation)

**Interfaces:**
- Consumes: Recommend API (student version)
- Produces: Student guidance UI

**Note:** This is the student-side counterpart to Task 10. The innovation point "needs guidance" must serve BOTH teachers and students.

- [ ] **Step 1: Create Student Guidance page**

Create `source/frontend/src/views/student/Guidance.vue`:
```vue
<template>
  <div class="guidance-container">
    <el-card class="guidance-card">
      <h2>探索你的学习需求</h2>
      <p class="subtitle">让我帮你找到最适合的学习工具</p>
      
      <!-- 步骤条 -->
      <el-steps :active="currentStep" finish-status="success" align-center>
        <el-step title="选择学科" />
        <el-step title="明确目标" />
        <el-step title="获取推荐" />
      </el-steps>
      
      <!-- 步骤1: 学科选择 -->
      <div v-if="currentStep === 0" class="step-content">
        <h3>{{ guidanceData.message }}</h3>
        <div class="options-grid">
          <el-card 
            v-for="option in guidanceData.options" 
            :key="option.value"
            class="option-card"
            :class="{ active: selectedCategory === option.value }"
            @click="selectCategory(option.value)"
          >
            <div class="option-icon">{{ option.value === '文科' ? '📚' : '🔬' }}</div>
            <div class="option-label">{{ option.label }}</div>
            <div class="option-desc">{{ option.desc }}</div>
          </el-card>
        </div>
      </div>
      
      <!-- 步骤2: 学习目标 -->
      <div v-if="currentStep === 1" class="step-content">
        <h3>{{ guidanceData.message }}</h3>
        <div class="options-list">
          <el-radio-group v-model="selectedGoal" @change="handleGoalSelect">
            <el-radio 
              v-for="option in guidanceData.options" 
              :key="option.value"
              :value="option.value"
              class="goal-option"
            >
              <span class="goal-label">{{ option.label }}</span>
              <span class="goal-desc">{{ option.desc }}</span>
            </el-radio>
          </el-radio-group>
        </div>
      </div>
      
      <!-- 步骤3: 推荐结果 -->
      <div v-if="currentStep === 2" class="step-content">
        <h3>{{ guidanceData.message }}</h3>
        <div class="tools-grid">
          <el-card 
            v-for="tool in guidanceData.tools" 
            :key="tool.id"
            class="tool-card"
          >
            <div class="tool-icon">{{ tool.icon }}</div>
            <div class="tool-name">{{ tool.name }}</div>
            <div class="tool-desc">{{ tool.description }}</div>
            <div class="tool-subject">{{ tool.subject }}</div>
            <el-button type="primary" size="small" @click="useTool(tool)">
              立即体验
            </el-button>
          </el-card>
        </div>
        
        <div class="action-buttons">
          <el-button @click="resetGuidance">重新选择</el-button>
          <el-button type="primary" @click="goToPlaza">
            去工具广场看看
          </el-button>
        </div>
      </div>
      
      <!-- 导航按钮 -->
      <div class="nav-buttons" v-if="currentStep < 2">
        <el-button v-if="currentStep > 0" @click="prevStep">上一步</el-button>
        <el-button 
          type="primary" 
          @click="nextStep"
          :disabled="!canProceed"
        >
          下一步
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getRecommendation } from '@/api/recommend'
import { ElMessage } from 'element-plus'

const router = useRouter()
const currentStep = ref(0)
const selectedCategory = ref('')
const selectedGoal = ref('')
const guidanceData = ref({ message: '', options: [] })
const canProceed = ref(false)

// 学生端的引导配置
const STUDENT_GUIDANCE = {
  1: {
    message: '你想学习哪个方向？',
    options: [
      { value: '文科', label: '文科', desc: '语文/英语/历史/政治/地理' },
      { value: '理科', label: '理科', desc: '数学/物理/化学/生物/信息技术' }
    ]
  },
  2: {
    '文科': {
      message: '你最想做什么？',
      options: [
        { value: '学习新知识', label: '学习新知识', desc: '理解概念、背诵诗词、学习语法' },
        { value: '完成作业', label: '完成作业', desc: '写作文、做阅读、翻译句子' },
        { value: '准备考试', label: '准备考试', desc: '复习重点、练习题目、查漏补缺' },
        { value: '探索兴趣', label: '探索兴趣', desc: '玩飞花令、趣味学习、拓展视野' }
      ]
    },
    '理科': {
      message: '你最想做什么？',
      options: [
        { value: '学习新知识', label: '学习新知识', desc: '理解公式、学习概念、掌握方法' },
        { value: '完成作业', label: '完成作业', desc: '解题思路、分析错题、推导公式' },
        { value: '准备考试', label: '准备考试', desc: '复习重点、练习题目、总结技巧' },
        { value: '探索兴趣', label: '探索兴趣', desc: '逻辑训练、实验模拟、数据分析' }
      ]
    }
  }
}

onMounted(async () => {
  guidanceData.value = STUDENT_GUIDANCE[1]
})

const selectCategory = (value) => {
  selectedCategory.value = value
  canProceed.value = true
}

const nextStep = async () => {
  if (currentStep.value === 0) {
    // 加载步骤2
    guidanceData.value = STUDENT_GUIDANCE[2][selectedCategory.value]
    currentStep.value++
    canProceed.value = false
  } else if (currentStep.value === 1) {
    // 加载步骤3 - 获取推荐
    try {
      const { data } = await getRecommendation({
        step: 3,
        category: selectedCategory.value,
        need_type: selectedGoal.value
      })
      guidanceData.value = data
      currentStep.value++
    } catch (error) {
      ElMessage.error('获取推荐失败')
    }
  }
}

const prevStep = () => {
  currentStep.value--
  if (currentStep.value === 0) {
    guidanceData.value = STUDENT_GUIDANCE[1]
    canProceed.value = true
  }
}

const handleGoalSelect = () => {
  canProceed.value = true
}

const useTool = (tool) => {
  router.push(`/student/tool/${tool.share_code}`)
}

const resetGuidance = () => {
  currentStep.value = 0
  selectedCategory.value = ''
  selectedGoal.value = ''
  guidanceData.value = STUDENT_GUIDANCE[1]
  canProceed.value = false
}

const goToPlaza = () => {
  router.push('/student/plaza')
}
</script>

<style scoped>
.guidance-container {
  max-width: 800px;
  margin: 0 auto;
}
.guidance-card {
  padding: 20px;
}
.subtitle {
  color: #666;
  text-align: center;
  margin-bottom: 30px;
}
.step-content {
  margin-top: 30px;
}
.options-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-top: 20px;
}
.option-card {
  cursor: pointer;
  text-align: center;
  transition: all 0.3s;
}
.option-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
.option-card.active {
  border-color: #409eff;
  background-color: #ecf5ff;
}
.option-icon {
  font-size: 48px;
  margin-bottom: 10px;
}
.option-label {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 5px;
}
.option-desc {
  color: #666;
  font-size: 14px;
}
.goal-option {
  display: block;
  margin: 15px 0;
  padding: 15px;
  border: 1px solid #eee;
  border-radius: 8px;
}
.goal-label {
  font-weight: bold;
  display: block;
  margin-bottom: 5px;
}
.goal-desc {
  color: #666;
  font-size: 14px;
}
.tools-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 20px;
}
.tool-card {
  text-align: center;
}
.tool-icon {
  font-size: 36px;
  margin-bottom: 10px;
}
.tool-name {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 5px;
}
.tool-desc {
  color: #666;
  font-size: 14px;
  margin-bottom: 10px;
}
.tool-subject {
  color: #999;
  font-size: 12px;
  margin-bottom: 15px;
}
.action-buttons {
  text-align: center;
  margin-top: 30px;
}
.nav-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 30px;
}
</style>
```

- [ ] **Step 2: Add route for student guidance**

Modify `source/frontend/src/router/index.js` to add student guidance route:
```javascript
{
  path: '/student',
  component: () => import('../layouts/StudentLayout.vue'),
  children: [
    {
      path: '',
      name: 'StudentHome',
      component: () => import('../views/student/Guidance.vue')  // Changed from Plaza
    },
    {
      path: 'plaza',
      name: 'StudentPlaza',
      component: () => import('../views/student/Plaza.vue')
    },
    // ... other routes
  ]
}
```

- [ ] **Step 3: Update student layout navigation**

Modify `source/frontend/src/layouts/StudentLayout.vue` to add guidance link:
```vue
<el-menu-item index="/student">需求引导</el-menu-item>
<el-menu-item index="/student/plaza">工具广场</el-menu-item>
```

- [ ] **Step 4: Test student guidance flow**

Run: `cd source/frontend && npm run dev`
Open browser: http://localhost:5173/student
Expected: 3-step guidance flow for students

- [ ] **Step 5: Commit**

```bash
git add source/frontend/src/views/student/Guidance.vue source/frontend/src/router/index.js source/frontend/src/layouts/StudentLayout.vue
git commit -m "feat: student needs guidance flow (innovation point)"
```

---

### Task 14: Student - Tool Plaza

**Covers:** Tool browsing, categorization

**Files:**
- Create: `source/frontend/src/views/student/Plaza.vue`

**Interfaces:**
- Consumes: Plaza API
- Produces: Tool browsing UI

- [ ] **Step 1: Create Plaza page**

Create `source/frontend/src/views/student/Plaza.vue`:
```vue
<template>
  <div class="plaza">
    <div class="search-bar">
      <el-input 
        v-model="searchKeyword" 
        placeholder="搜索工具..." 
        prefix-icon="Search"
        @input="handleSearch"
        clearable
      />
    </div>
    
    <!-- 分类标签 -->
    <div class="category-tabs">
      <el-radio-group v-model="selectedCategory" @change="loadTools">
        <el-radio-button value="">全部</el-radio-button>
        <el-radio-button 
          v-for="cat in categories" 
          :key="cat.value" 
          :value="cat.value"
        >
          {{ cat.icon }} {{ cat.label }}
        </el-radio-button>
      </el-radio-group>
    </div>
    
    <!-- 工具列表 -->
    <div class="tools-grid">
      <el-card 
        v-for="tool in tools" 
        :key="tool.id"
        class="tool-card"
        @click="useTool(tool)"
      >
        <div class="tool-icon">{{ tool.icon }}</div>
        <div class="tool-name">{{ tool.name }}</div>
        <div class="tool-desc">{{ tool.description }}</div>
        <div class="tool-meta">
          <el-tag :type="tool.category === '文科' ? 'success' : 'primary'" size="small">
            {{ tool.category }}
          </el-tag>
          <span class="usage-count">{{ tool.usage_count }}次使用</span>
        </div>
      </el-card>
    </div>
    
    <el-empty v-if="tools.length === 0" description="暂无工具" />
    
    <!-- 热门推荐 -->
    <el-card class="hot-section" v-if="hotTools.length > 0">
      <template #header>
        <span>🔥 热门推荐</span>
      </template>
      <div class="hot-list">
        <div 
          v-for="(tool, index) in hotTools" 
          :key="tool.id"
          class="hot-item"
          @click="useTool(tool)"
        >
          <span class="hot-rank">{{ index + 1 }}</span>
          <span class="hot-icon">{{ tool.icon }}</span>
          <span class="hot-name">{{ tool.name }}</span>
          <span class="hot-count">{{ tool.usage_count }}次</span>
        </div>
      </div>
    </el-card>
    
    <!-- 想要更多？ -->
    <el-card class="more-section">
      <div class="more-content">
        <p>想要更多工具？</p>
        <p>告诉老师你的需求，让老师为你创建工具</p>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getPlaza, getHotTools } from '@/api/plaza'
import { ElMessage } from 'element-plus'

const router = useRouter()
const tools = ref([])
const hotTools = ref([])
const categories = ref([])
const selectedCategory = ref('')
const searchKeyword = ref('')

onMounted(async () => {
  await loadCategories()
  await loadTools()
  await loadHotTools()
})

const loadCategories = async () => {
  try {
    const { data } = await getPlaza()
    categories.value = data.categories
  } catch (error) {
    ElMessage.error('加载分类失败')
  }
}

const loadTools = async () => {
  try {
    const { data } = await getPlaza(selectedCategory.value, searchKeyword.value)
    tools.value = data.tools
  } catch (error) {
    ElMessage.error('加载工具失败')
  }
}

const loadHotTools = async () => {
  try {
    const { data } = await getHotTools(5)
    hotTools.value = data
  } catch (error) {
    ElMessage.error('加载热门工具失败')
  }
}

const handleSearch = () => {
  loadTools()
}

const useTool = (tool) => {
  router.push(`/student/tool/${tool.share_code}`)
}
</script>

<style scoped>
.plaza {
  max-width: 1200px;
  margin: 0 auto;
}
.search-bar {
  margin-bottom: 20px;
}
.category-tabs {
  margin-bottom: 20px;
}
.tools-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}
.tool-card {
  cursor: pointer;
  transition: all 0.3s;
}
.tool-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
.tool-icon {
  font-size: 48px;
  text-align: center;
  margin-bottom: 15px;
}
.tool-name {
  font-size: 18px;
  font-weight: bold;
  text-align: center;
  margin-bottom: 10px;
}
.tool-desc {
  color: #666;
  font-size: 14px;
  text-align: center;
  margin-bottom: 15px;
}
.tool-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.usage-count {
  color: #999;
  font-size: 12px;
}
.hot-section {
  margin-bottom: 20px;
}
.hot-list {
  padding: 0;
}
.hot-item {
  display: flex;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #eee;
  cursor: pointer;
}
.hot-item:hover {
  background: #f5f7fa;
}
.hot-rank {
  width: 24px;
  height: 24px;
  background: #409eff;
  color: #fff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
  font-size: 12px;
}
.hot-item:nth-child(1) .hot-rank {
  background: #f56c6c;
}
.hot-item:nth-child(2) .hot-rank {
  background: #e6a23c;
}
.hot-item:nth-child(3) .hot-rank {
  background: #67c23a;
}
.hot-icon {
  font-size: 20px;
  margin-right: 10px;
}
.hot-name {
  flex: 1;
}
.hot-count {
  color: #666;
  font-size: 14px;
}
.more-section {
  text-align: center;
  background: #f5f7fa;
}
.more-content p {
  margin: 5px 0;
  color: #666;
}
</style>
```

- [ ] **Step 2: Test plaza**

Run: `cd source/frontend && npm run dev`
Open browser: http://localhost:5173/student
Expected: Tool grid with categories, search, hot tools section

- [ ] **Step 3: Commit**

```bash
git add source/frontend/src/views/student/Plaza.vue
git commit -m "feat: student tool plaza with categories and search"
```

---

### Task 15: Student - AI Q&A & Tool Use & Records

**Covers:** AI interaction, tool usage, learning records

**Files:**
- Create: `source/frontend/src/views/student/AIChat.vue`
- Create: `source/frontend/src/views/student/ToolUse.vue`
- Create: `source/frontend/src/views/student/Records.vue`

**Interfaces:**
- Consumes: Chat API, Tools API, Usage API
- Produces: AI chat UI, tool usage UI, records UI

- [ ] **Step 1: Create AIChat page**

Create `source/frontend/src/views/student/AIChat.vue`:
```vue
<template>
  <div class="ai-chat">
    <el-card class="chat-card">
      <template #header>
        <span>🤖 AI 学习助手</span>
      </template>
      
      <div class="chat-hints">
        <p>我可以帮你：</p>
        <div class="hint-tags">
          <el-tag 
            v-for="hint in hints" 
            :key="hint"
            @click="sendHint(hint)"
            class="hint-tag"
          >
            {{ hint }}
          </el-tag>
        </div>
      </div>
      
      <div class="chat-messages" ref="messagesContainer">
        <div 
          v-for="(msg, index) in messages" 
          :key="index"
          :class="['message', msg.role]"
        >
          <div class="message-content">{{ msg.content }}</div>
        </div>
      </div>
      
      <div class="chat-input">
        <el-input 
          v-model="inputMessage" 
          placeholder="输入你的问题..."
          @keyup.enter="sendMessage"
        >
          <template #append>
            <el-button @click="sendMessage" :loading="loading">
              发送
            </el-button>
          </template>
        </el-input>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import { sendMessage } from '@/api/chat'
import { ElMessage } from 'element-plus'

const inputMessage = ref('')
const messages = ref([
  { role: 'assistant', content: '你好！我是AI学习助手，有什么可以帮你的吗？' }
])
const loading = ref(false)
const messagesContainer = ref(null)

const hints = [
  '帮我解释勾股定理',
  '推荐一些学习方法',
  '什么是人工智能？',
  '如何提高写作能力？'
]

const sendHint = (hint) => {
  inputMessage.value = hint
  sendMessage()
}

const sendMessage = async () => {
  if (!inputMessage.value.trim() || loading.value) return
  
  const userMessage = inputMessage.value
  messages.value.push({ role: 'user', content: userMessage })
  inputMessage.value = ''
  
  await nextTick()
  scrollToBottom()
  
  loading.value = true
  try {
    const { data } = await sendMessage({ message: userMessage })
    messages.value.push({ role: 'assistant', content: data.reply })
  } catch (error) {
    ElMessage.error('发送失败，请重试')
    messages.value.pop()
  } finally {
    loading.value = false
    await nextTick()
    scrollToBottom()
  }
}

const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}
</script>

<style scoped>
.ai-chat {
  max-width: 800px;
  margin: 0 auto;
}
.chat-card {
  height: calc(100vh - 160px);
  display: flex;
  flex-direction: column;
}
.chat-hints {
  padding: 15px;
  background: #f5f7fa;
  border-radius: 8px;
  margin-bottom: 15px;
}
.chat-hints p {
  margin-bottom: 10px;
  color: #666;
}
.hint-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
.hint-tag {
  cursor: pointer;
}
.hint-tag:hover {
  background: #409eff;
  color: #fff;
}
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 15px;
  background: #fafafa;
  border-radius: 8px;
  margin-bottom: 15px;
}
.message {
  margin-bottom: 15px;
  display: flex;
}
.message.user {
  justify-content: flex-end;
}
.message-content {
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 12px;
  line-height: 1.5;
}
.message.assistant .message-content {
  background: #fff;
  border: 1px solid #eee;
}
.message.user .message-content {
  background: #409eff;
  color: #fff;
}
.chat-input {
  padding: 15px;
  background: #fff;
  border-top: 1px solid #eee;
}
</style>
```

- [ ] **Step 2: Create ToolUse page**

Create `source/frontend/src/views/student/ToolUse.vue`:
```vue
<template>
  <div class="tool-use">
    <el-card class="tool-card" v-if="tool">
      <template #header>
        <div class="tool-header">
          <span class="tool-icon">{{ tool.icon }}</span>
          <span class="tool-name">{{ tool.name }}</span>
        </div>
      </template>
      
      <div class="tool-description">
        <p>{{ tool.description }}</p>
      </div>
      
      <div class="chat-section">
        <div class="chat-messages" ref="messagesContainer">
          <div 
            v-for="(msg, index) in messages" 
            :key="index"
            :class="['message', msg.role]"
          >
            <div class="message-content">{{ msg.content }}</div>
          </div>
        </div>
        
        <div class="chat-input">
          <el-input 
            v-model="inputMessage" 
            :placeholder="`输入内容，如：${tool.subject === '语文' ? '静夜思' : '勾股定理'}`"
            @keyup.enter="sendMessage"
          >
            <template #append>
              <el-button @click="sendMessage" :loading="loading">
                发送
              </el-button>
            </template>
          </el-input>
        </div>
      </div>
    </el-card>
    
    <el-card v-else class="loading-card">
      <el-skeleton :rows="5" animated />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { getTool } from '@/api/tools'
import { sendMessage } from '@/api/chat'
import { ElMessage } from 'element-plus'

const route = useRoute()
const tool = ref(null)
const messages = ref([])
const inputMessage = ref('')
const loading = ref(false)
const messagesContainer = ref(null)

onMounted(async () => {
  // 通过shareCode获取工具信息（简化版，实际需要根据shareCode查询）
  const toolId = route.params.toolId || 1
  try {
    const { data } = await getTool(toolId)
    tool.value = data
    messages.value.push({
      role: 'assistant',
      content: `你好！我是${data.name}，${data.description}。请输入内容开始使用。`
    })
  } catch (error) {
    ElMessage.error('加载工具失败')
  }
})

const sendMessage = async () => {
  if (!inputMessage.value.trim() || loading.value || !tool.value) return
  
  const userMessage = inputMessage.value
  messages.value.push({ role: 'user', content: userMessage })
  inputMessage.value = ''
  
  await nextTick()
  scrollToBottom()
  
  loading.value = true
  try {
    const { data } = await sendMessage({
      message: userMessage,
      tool_id: tool.value.id
    })
    messages.value.push({ role: 'assistant', content: data.reply })
  } catch (error) {
    ElMessage.error('发送失败，请重试')
    messages.value.pop()
  } finally {
    loading.value = false
    await nextTick()
    scrollToBottom()
  }
}

const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}
</script>

<style scoped>
.tool-use {
  max-width: 800px;
  margin: 0 auto;
}
.tool-card {
  height: calc(100vh - 160px);
  display: flex;
  flex-direction: column;
}
.tool-header {
  display: flex;
  align-items: center;
}
.tool-icon {
  font-size: 24px;
  margin-right: 10px;
}
.tool-name {
  font-size: 18px;
  font-weight: bold;
}
.tool-description {
  padding: 15px;
  background: #f5f7fa;
  border-radius: 8px;
  margin-bottom: 15px;
}
.chat-section {
  flex: 1;
  display: flex;
  flex-direction: column;
}
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 15px;
  background: #fafafa;
  border-radius: 8px;
  margin-bottom: 15px;
}
.message {
  margin-bottom: 15px;
  display: flex;
}
.message.user {
  justify-content: flex-end;
}
.message-content {
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 12px;
  line-height: 1.5;
}
.message.assistant .message-content {
  background: #fff;
  border: 1px solid #eee;
}
.message.user .message-content {
  background: #409eff;
  color: #fff;
}
.chat-input {
  padding: 15px;
  background: #fff;
  border-top: 1px solid #eee;
}
.loading-card {
  height: calc(100vh - 160px);
}
</style>
```

- [ ] **Step 3: Create Records page**

Create `source/frontend/src/views/student/Records.vue`:
```vue
<template>
  <div class="records">
    <h2>我的学习记录</h2>
    
    <!-- 统计卡片 -->
    <div class="stats-cards">
      <el-card class="stat-card">
        <div class="stat-value">{{ stats.total_usage }}</div>
        <div class="stat-label">使用次数</div>
      </el-card>
      <el-card class="stat-card">
        <div class="stat-value">{{ stats.unique_tools }}</div>
        <div class="stat-label">使用工具数</div>
      </el-card>
      <el-card class="stat-card">
        <div class="stat-value">{{ stats.streak_days }}</div>
        <div class="stat-label">连续天数</div>
      </el-card>
    </div>
    
    <!-- 最近使用 -->
    <el-card class="recent-card">
      <template #header>
        <span>最近使用</span>
      </template>
      <div class="recent-list">
        <div 
          v-for="record in records" 
          :key="record.id"
          class="record-item"
        >
          <div class="record-time">{{ formatDate(record.created_at) }}</div>
          <div class="record-content">
            <span class="record-tool">工具ID: {{ record.tool_id }}</span>
            <span class="record-input">{{ record.input_text }}</span>
          </div>
        </div>
      </div>
      
      <el-empty v-if="records.length === 0" description="还没有使用记录" />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getMyUsage } from '@/api/usage'
import { ElMessage } from 'element-plus'

const records = ref([])
const stats = ref({
  total_usage: 0,
  unique_tools: 0,
  streak_days: 0
})

onMounted(async () => {
  await loadRecords()
})

const loadRecords = async () => {
  try {
    const user = JSON.parse(localStorage.getItem('user'))
    if (!user) {
      ElMessage.warning('请先登录')
      return
    }
    
    const { data } = await getMyUsage(user.id)
    records.value = data
    
    // 计算统计
    stats.value.total_usage = data.length
    const uniqueToolIds = new Set(data.map(r => r.tool_id))
    stats.value.unique_tools = uniqueToolIds.size
    
    // 简化版连续天数计算
    const dates = [...new Set(data.map(r => new Date(r.created_at).toDateString()))]
    stats.value.streak_days = dates.length
  } catch (error) {
    ElMessage.error('加载记录失败')
  }
}

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  const now = new Date()
  const diff = now - date
  
  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
  return date.toLocaleDateString('zh-CN')
}
</script>

<style scoped>
.records {
  max-width: 800px;
  margin: 0 auto;
}
.stats-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}
.stat-card {
  text-align: center;
}
.stat-value {
  font-size: 36px;
  font-weight: bold;
  color: #409eff;
}
.stat-label {
  color: #666;
  margin-top: 10px;
}
.recent-card {
  margin-bottom: 20px;
}
.recent-list {
  padding: 0;
}
.record-item {
  display: flex;
  padding: 15px 0;
  border-bottom: 1px solid #eee;
}
.record-time {
  width: 100px;
  color: #666;
  font-size: 14px;
}
.record-content {
  flex: 1;
}
.record-tool {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
}
.record-input {
  color: #666;
  font-size: 14px;
}
</style>
```

- [ ] **Step 4: Test AI chat and records**

Run: `cd source/frontend && npm run dev`
Open browser: http://localhost:5173/student/chat
Expected: AI chat interface with hints and message history

- [ ] **Step 5: Commit**

```bash
git add source/frontend/src/views/student/
git commit -m "feat: student AI chat, tool use, and learning records"
```

---

## Phase 5: Integration & Testing (Tasks 15-16)

### Task 16: Frontend-Backend Integration

**Covers:** API connection, CORS, error handling

**Files:**
- Modify: `source/frontend/vite.config.js` (proxy)
- Modify: `source/backend/main.py` (CORS)
- Test: Full flow testing

**Interfaces:**
- Produces: Working frontend-backend connection

- [ ] **Step 1: Configure Vite proxy**

Modify `source/frontend/vite.config.js`:
```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})
```

- [ ] **Step 2: Update API base URLs**

Update all API files in `source/frontend/src/api/`:
```javascript
// Change from:
const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 10000
})

// To:
const api = axios.create({
  baseURL: '/api',
  timeout: 10000
})
```

- [ ] **Step 3: Test full flow**

1. Start backend: `cd source/backend && python main.py`
2. Start frontend: `cd source/frontend && npm run dev`
3. Open http://localhost:5173
4. Register a teacher account
5. Login
6. Test guidance flow
7. Test tool creation
8. Test AI chat

- [ ] **Step 4: Commit**

```bash
git add source/frontend/vite.config.js source/frontend/src/api/
git commit -m "feat: frontend-backend integration with proxy"
```

---

### Task 17: Final Testing & Documentation

**Covers:** End-to-end testing, deployment guide

**Files:**
- Create: `docs/deployment-guide.md`
- Create: `docs/user-manual.md`

**Interfaces:**
- Produces: Complete documentation

- [ ] **Step 1: Create deployment guide**

Create `docs/deployment-guide.md`:
```markdown
# 智教通部署指南

## 环境要求

- Python 3.11+
- Node.js 18+
- MySQL 8.0

## 部署步骤

### 1. 数据库初始化

```bash
mysql -u root -p < source/backend/sql/init.sql
mysql -u root -p zjiaotong < source/backend/sql/seed.sql
```

### 2. 后端部署

```bash
cd source/backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # 编辑 .env 填写配置
python main.py
```

### 3. 前端部署

```bash
cd source/frontend
npm install
npm run build  # 生成 dist 目录
```

### 4. Nginx配置

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        root /path/to/source/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 环境变量配置

编辑 `source/backend/.env`:

```env
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/zjiaotong
DEEPSEEK_API_KEY=your-api-key
DEEPSEEK_MODEL=dsv4
DEEPSEEK_API_URL=https://api.deepseek.com
```

## 常见问题

### 1. 数据库连接失败

检查 `.env` 中的 `DATABASE_URL` 配置

### 2. DeepSeek API调用失败

检查 `DEEPSEEK_API_KEY` 是否正确

### 3. 前端页面空白

检查浏览器控制台是否有错误
```

- [ ] **Step 2: Create user manual**

Create `docs/user-manual.md`:
```markdown
# 智教通用户手册

## 教师端

### 登录注册

1. 访问首页，点击"注册"
2. 选择"我是老师"，填写信息
3. 注册成功后登录

### 需求引导

1. 登录后进入教师首页
2. 第1步：选择文科或理科
3. 第2步：选择需求类型（备课/教学/辅导/兴趣激发）
4. 第3步：查看推荐工具，点击"立即体验"

### 工具管理

1. 点击左侧菜单"我的工具"
2. 点击"创建新工具"
3. 填写工具信息和提示词
4. 保存后可生成分享链接

### 数据看板

1. 点击左侧菜单"数据看板"
2. 查看统计数据和使用趋势

## 学生端

### 工具广场

1. 访问 /student 进入工具广场
2. 按分类浏览工具
3. 点击工具卡片进入使用

### AI问答

1. 点击顶部菜单"AI问答"
2. 输入问题或点击提示标签
3. 查看AI回复

### 学习记录

1. 点击顶部菜单"学习记录"
2. 查看使用统计和历史记录
```

- [ ] **Step 3: Final test**

1. 完整流程测试
2. 检查所有页面功能
3. 修复发现的问题

- [ ] **Step 4: Commit**

```bash
git add docs/
git commit -m "docs: deployment guide and user manual"
```

---

## Summary

| Phase | Tasks | Description | Independent Test |
|-------|-------|-------------|------------------|
| 1 | 1-3 | Backend Foundation | API endpoints work with curl |
| 2 | 4-6 | Backend Business Logic | Statistics and recommendation work |
| 3 | 7-9 | Frontend Foundation | Router, layouts, auth pages |
| 4 | 10-15 | Frontend Core Pages (Teacher + Student) | All pages functional including both guidance flows |
| 5 | 16-17 | Integration & Testing | Full flow works end-to-end |

**Total: 17 tasks, each independently runnable and testable**

**Innovation Point Coverage:**
- Task 10: Teacher Needs Guidance Flow (core innovation)
- Task 13: Student Needs Guidance Flow (core innovation)
- Both flows use the same Recommend API with different configurations
