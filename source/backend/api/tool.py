from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
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
    query = db.query(Tool).filter(Tool.is_public == True)
    
    # 根据学科筛选
    if subject in ['语文', '英语', '历史', '政治', '地理']:
        query = query.filter(Tool.category == '文科')
    elif subject in ['数学', '物理', '化学', '生物', '信息技术']:
        query = query.filter(Tool.category == '理科')
    
    # 根据需求类型进一步筛选
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
def create_tool(tool: ToolCreate, creator_id: int = Query(None), db: Session = Depends(get_db)):
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
