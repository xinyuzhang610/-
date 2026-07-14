from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from models.database import get_db
from models.usage import UsageLog
from models.tool import Tool
from models.user import User
from schemas.usage import UsageLogResponse, DashboardStats
from datetime import datetime, timedelta
from typing import List
from api.dependencies import get_current_user, require_roles

router = APIRouter()

@router.get("/my", response_model=List[UsageLogResponse])
def get_my_usage(
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    logs = db.query(UsageLog)\
        .filter(UsageLog.user_id == current_user.id)\
        .order_by(UsageLog.created_at.desc())\
        .limit(limit)\
        .all()
    return logs

@router.get("/tool/{tool_id}")
def get_tool_usage(
    tool_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("teacher", "admin"))
):
    tool = db.query(Tool).filter(Tool.id == tool_id).first()
    if not tool:
        raise HTTPException(status_code=404, detail="工具不存在")
    if current_user.role != "admin" and tool.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="只能查看自己工具的使用数据")
    total = db.query(UsageLog).filter(UsageLog.tool_id == tool_id).count()
    today = db.query(UsageLog)\
        .filter(UsageLog.tool_id == tool_id,
                func.date(UsageLog.created_at) == func.date(func.now()))\
        .count()
    return {"tool_id": tool_id, "total_usage": total, "today_usage": today}

@router.get("/dashboard", response_model=DashboardStats)
def get_dashboard(db: Session = Depends(get_db), current_user: User = Depends(require_roles("teacher", "admin"))):
    tool_query = db.query(Tool) if current_user.role == "admin" else db.query(Tool).filter(Tool.creator_id == current_user.id)
    total_tools = tool_query.count()
    tool_ids = [tool.id for tool in tool_query.all()]
    total_users = db.query(User).count() if current_user.role == "admin" else 0
    today_usage = db.query(UsageLog)\
        .filter(func.date(UsageLog.created_at) == func.date(func.now()), UsageLog.tool_id.in_(tool_ids or [-1]))\
        .count()

    weekly_trend = []
    for i in range(7):
        day = datetime.now() - timedelta(days=6-i)
        count = db.query(UsageLog)\
            .filter(func.date(UsageLog.created_at) == func.date(day), UsageLog.tool_id.in_(tool_ids or [-1]))\
            .count()
        weekly_trend.append({"date": day.strftime("%m/%d"), "count": count})

    top_tools = db.query(
        Tool.name,
        func.count(UsageLog.id).label('usage_count')
    ).join(UsageLog).filter(Tool.id.in_(tool_ids or [-1]))\
     .group_by(Tool.id)\
     .order_by(func.count(UsageLog.id).desc())\
     .limit(5)\
     .all()

    recent_logs = db.query(UsageLog).filter(UsageLog.tool_id.in_(tool_ids or [-1]))\
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
