from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
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
    categories = [
        {"value": "文科", "label": "文科专区", "icon": "📚"},
        {"value": "理科", "label": "理科专区", "icon": "🔬"},
        {"value": "通用", "label": "通用工具", "icon": "🛠️"}
    ]

    query = db.query(Tool).filter(Tool.is_public == True)

    if category:
        query = query.filter(Tool.category == category)

    if search:
        query = query.filter(Tool.name.contains(search) | Tool.description.contains(search))

    tools = query.order_by(Tool.usage_count.desc()).all()

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
