# services/usage_service.py
from sqlalchemy.orm import Session
from sqlalchemy import func
from models.usage import UsageLog
from datetime import datetime, timedelta

def record_usage(db: Session, user_id: int, tool_id: int, action: str, details: dict = None):
    """记录使用日志"""
    log = UsageLog(
        user_id=user_id,
        tool_id=tool_id,
        action=action,
        details=details
    )
    db.add(log)
    db.commit()
    return log

def get_user_usage_stats(db: Session, user_id: int):
    """获取用户使用统计"""
    # 总使用次数
    total_count = db.query(UsageLog).filter(UsageLog.user_id == user_id).count()
    
    # 今日使用次数
    today = datetime.now().date()
    today_count = db.query(UsageLog).filter(
        UsageLog.user_id == user_id,
        func.date(UsageLog.created_at) == today
    ).count()
    
    # 最近7天使用趋势
    seven_days_ago = datetime.now() - timedelta(days=7)
    daily_usage = db.query(
        func.date(UsageLog.created_at).label('date'),
        func.count().label('count')
    ).filter(
        UsageLog.user_id == user_id,
        UsageLog.created_at >= seven_days_ago
    ).group_by(func.date(UsageLog.created_at)).all()
    
    return {
        "total_count": total_count,
        "today_count": today_count,
        "daily_usage": [{"date": str(u.date), "count": u.count} for u in daily_usage]
    }

def get_tool_usage_ranking(db: Session, limit: int = 10):
    """获取工具使用排行榜"""
    ranking = db.query(
        UsageLog.tool_id,
        func.count().label('count')
    ).group_by(UsageLog.tool_id).order_by(func.count().desc()).limit(limit).all()
    
    return [{"tool_id": r.tool_id, "count": r.count} for r in ranking]
