from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.database import get_db
from models.tool import Tool
from schemas.recommend import RecommendRequest, RecommendResponse

router = APIRouter()

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
        flow = GUIDANCE_FLOW[1]
        return RecommendResponse(
            step=1,
            message=flow["message"],
            options=flow["options"]
        )

    elif request.step == 2:
        if request.category not in GUIDANCE_FLOW[2]:
            return RecommendResponse(step=2, message="无效的分类")
        flow = GUIDANCE_FLOW[2][request.category]
        return RecommendResponse(
            step=2,
            message=flow["message"],
            options=flow["options"]
        )

    elif request.step == 3:
        query = db.query(Tool).filter(Tool.is_public == True)

        if request.category == "文科":
            query = query.filter(Tool.category == "文科")
        elif request.category == "理科":
            query = query.filter(Tool.category == "理科")

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
