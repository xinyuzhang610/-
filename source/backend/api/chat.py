import json
import time
import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from api.dependencies import get_current_user, require_roles
from models.conversation import ConversationMessage, ConversationSession
from models.database import SessionLocal, get_db
from models.tool import Tool
from models.usage import UsageLog
from models.user import User
from schemas.chat import ChatRequest, ChatResponse
from services.deepseek import AIConfigurationError, DeepSeekRequestError, chat_with_deepseek, stream_with_deepseek
from services.tool_access_service import assert_tool_can_be_used

router = APIRouter()

def _session(db, user_id, requested, tool_id):
    if requested:
        row = db.query(ConversationSession).filter(ConversationSession.id == requested, ConversationSession.user_id == user_id).first()
        if not row: raise HTTPException(status_code=403, detail="会话不存在或不属于当前用户")
        return row
    row = ConversationSession(id=str(uuid.uuid4()), user_id=user_id, tool_id=tool_id); db.add(row); db.flush(); return row

def _tool(db, user, tool_id):
    if not tool_id: return None
    row = db.query(Tool).filter(Tool.id == tool_id).first()
    if not row: raise HTTPException(status_code=404, detail="工具不存在")
    assert_tool_can_be_used(user, row); return row

def _history(db, session_id):
    rows = db.query(ConversationMessage).filter(ConversationMessage.session_id == session_id).order_by(ConversationMessage.created_at.desc()).limit(12).all()
    return [{"role": row.role, "content": row.content} for row in reversed(rows)]

def _complete(db, user, session, tool, message, reply, started):
    db.add_all([ConversationMessage(session_id=session.id, role="user", content=message), ConversationMessage(session_id=session.id, role="assistant", content=reply), UsageLog(user_id=user.id, tool_id=tool.id if tool else None, input_text=message, output_text=reply, session_id=session.id, status="completed", latency_ms=int((time.perf_counter() - started) * 1000), completed_at=datetime.utcnow())])
    if tool: tool.usage_count += 1
    session.last_activity_at = datetime.utcnow(); db.commit()

@router.post("/", response_model=ChatResponse)
async def chat(payload: ChatRequest, db: Session = Depends(get_db), user: User = Depends(require_roles("student"))):
    tool = _tool(db, user, payload.tool_id); session = _session(db, user.id, payload.session_id, payload.tool_id); started = time.perf_counter()
    try: reply = await chat_with_deepseek(payload.message, tool.prompt_template if tool else None)
    except AIConfigurationError as error: raise HTTPException(status_code=503, detail=str(error))
    except DeepSeekRequestError as error: raise HTTPException(status_code=error.status_code, detail=str(error))
    _complete(db, user, session, tool, payload.message, reply, started)
    return ChatResponse(reply=reply, session_id=session.id, tool_name=tool.name if tool else None)

@router.post("/stream")
async def stream_chat(payload: ChatRequest, request: Request, db: Session = Depends(get_db), user: User = Depends(require_roles("student"))):
    tool = _tool(db, user, payload.tool_id)
    session = _session(db, user.id, payload.session_id, payload.tool_id)
    # FastAPI closes request-scoped dependencies before a StreamingResponse is
    # consumed. Capture all metadata while this request session is still open,
    # then use a dedicated session for the lifetime of the stream.
    session_id = session.id
    user_id = user.id
    tool_id = tool.id if tool else None
    tool_name = tool.name if tool else None
    system_prompt = tool.prompt_template if tool else None
    db.commit()

    async def events():
        stream_db = SessionLocal()
        reply = ""; started = time.perf_counter()
        try:
            stream_session = stream_db.get(ConversationSession, session_id)
            stream_user = stream_db.get(User, user_id)
            stream_tool = stream_db.get(Tool, tool_id) if tool_id else None
            if not stream_session or not stream_user:
                raise AIConfigurationError("会话已失效，请重新发起对话")
            yield f"event: meta\ndata: {json.dumps({'session_id': session_id, 'tool_name': tool_name})}\n\n"
            async for delta in stream_with_deepseek(payload.message, system_prompt, _history(stream_db, session_id)):
                if await request.is_disconnected():
                    stream_db.add(UsageLog(user_id=user_id, tool_id=tool_id, input_text=payload.message, session_id=session_id, status="aborted")); stream_db.commit(); return
                reply += delta; yield f"event: delta\ndata: {json.dumps({'text': delta}, ensure_ascii=False)}\n\n"
            _complete(stream_db, stream_user, stream_session, stream_tool, payload.message, reply, started)
            yield f"event: done\ndata: {json.dumps({'session_id': session_id})}\n\n"
        except (AIConfigurationError, DeepSeekRequestError) as error:
            stream_db.add(UsageLog(user_id=user_id, tool_id=tool_id, input_text=payload.message, session_id=session_id, status="aborted")); stream_db.commit()
            yield f"event: error\ndata: {json.dumps({'message': str(error)}, ensure_ascii=False)}\n\n"
        finally:
            stream_db.close()
    return StreamingResponse(events(), media_type="text/event-stream", headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})
