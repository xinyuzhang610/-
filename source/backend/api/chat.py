from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.database import get_db
from models.tool import Tool
from models.usage import UsageLog
from schemas.chat import ChatRequest, ChatResponse
from services.deepseek import chat_with_deepseek
from services.deepseek import AIConfigurationError, DeepSeekRequestError
from api.dependencies import get_current_user
from models.user import User
import uuid

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
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
    except AIConfigurationError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except DeepSeekRequestError as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI服务调用失败: {str(e)}")

    # 记录使用日志
    tool_id = request.tool_id if request.tool_id else 1
    usage_log = UsageLog(
        tool_id=tool_id,
        input_text=request.message,
        output_text=reply,
        session_id=session_id,
        user_id=current_user.id
    )
    db.add(usage_log)
    db.commit()

    return ChatResponse(
        reply=reply,
        session_id=session_id,
        tool_name=tool_name
    )
