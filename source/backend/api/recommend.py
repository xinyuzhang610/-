from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.database import get_db
from schemas.recommend import RecommendRequest, RecommendResponse
from services.recommend_service import recommend_student_tools, recommend_tools

router = APIRouter()

@router.post("/", response_model=RecommendResponse)
def get_recommendation(request: RecommendRequest, db: Session = Depends(get_db)):
    if request.step < 3:
        return RecommendResponse(step=request.step, message="请继续完成需求引导")
    if request.difficulty or request.approach:
        tools, reason = recommend_student_tools(
            db,
            request.difficulty,
            request.subject,
            request.approach,
        )
        return RecommendResponse(step=request.step, message="已根据学习线索匹配工具", tools=tools, reason=reason)
    tools, rule = recommend_tools(db, request.category, request.subject, request.need_type)
    return RecommendResponse(
        step=request.step,
        message="已匹配到可解释推荐规则" if rule else "未命中专属规则，已提供同分类热门预设工具",
        tools=tools,
        reason="根据学科、分类和教学目标进行规则匹配",
    )
