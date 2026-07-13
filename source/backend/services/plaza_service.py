# services/plaza_service.py
from sqlalchemy.orm import Session
from models.tool import Tool
from models.favorite import Favorite

def get_plaza_tools(db: Session, category: str = None, keyword: str = None):
    """获取工具广场的工具列表"""
    query = db.query(Tool).filter(Tool.is_public == True)
    
    if category:
        query = query.filter(Tool.category == category)
    
    if keyword:
        query = query.filter(Tool.name.contains(keyword) | Tool.description.contains(keyword))
    
    return query.all()

def get_popular_tools(db: Session, limit: int = 10):
    """获取热门工具"""
    # 这里简化实现，实际应该根据使用次数排序
    return db.query(Tool).filter(Tool.is_public == True).limit(limit).all()

def add_favorite(db: Session, user_id: int, tool_id: int):
    """添加收藏"""
    # 检查是否已收藏
    existing = db.query(Favorite).filter(
        Favorite.user_id == user_id,
        Favorite.tool_id == tool_id
    ).first()
    
    if existing:
        return None  # 已收藏
    
    favorite = Favorite(user_id=user_id, tool_id=tool_id)
    db.add(favorite)
    db.commit()
    db.refresh(favorite)
    return favorite

def remove_favorite(db: Session, user_id: int, tool_id: int):
    """取消收藏"""
    favorite = db.query(Favorite).filter(
        Favorite.user_id == user_id,
        Favorite.tool_id == tool_id
    ).first()
    
    if not favorite:
        return False
    
    db.delete(favorite)
    db.commit()
    return True

def get_user_favorites(db: Session, user_id: int):
    """获取用户收藏列表"""
    return db.query(Favorite).filter(Favorite.user_id == user_id).all()
