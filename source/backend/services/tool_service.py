# services/tool_service.py
from sqlalchemy.orm import Session
from models.tool import Tool, ToolTemplate
from schemas.tool import ToolCreate
import uuid

def get_preset_tools(db: Session, category: str = None):
    """获取预设工具"""
    query = db.query(Tool).filter(Tool.is_preset == True, Tool.is_public == True)
    if category:
        query = query.filter(Tool.category == category)
    return query.all()

def recommend_tools(db: Session, subject: str, need_type: str):
    """推荐工具"""
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
    
    return query.all()

def get_tool_by_id(db: Session, tool_id: int):
    """根据ID获取工具"""
    return db.query(Tool).filter(Tool.id == tool_id).first()

def create_tool(db: Session, tool_data: ToolCreate, creator_id: int = None):
    """创建工具"""
    db_tool = Tool(
        **tool_data.model_dump(),
        creator_id=creator_id,
        share_code=str(uuid.uuid4())[:8]
    )
    db.add(db_tool)
    db.commit()
    db.refresh(db_tool)
    return db_tool

def update_tool(db: Session, tool_id: int, tool_data: dict):
    """更新工具"""
    db_tool = db.query(Tool).filter(Tool.id == tool_id).first()
    if not db_tool:
        return None
    for key, value in tool_data.items():
        if value is not None:
            setattr(db_tool, key, value)
    db.commit()
    db.refresh(db_tool)
    return db_tool

def delete_tool(db: Session, tool_id: int):
    """删除工具"""
    db_tool = db.query(Tool).filter(Tool.id == tool_id).first()
    if not db_tool:
        return False
    db.delete(db_tool)
    db.commit()
    return True
