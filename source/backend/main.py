from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from uuid import uuid4
import logging
from config import settings
from api.user import router as user_router
from api.tool import router as tool_router
from api.chat import router as chat_router
from api.usage import router as usage_router
from api.recommend import router as recommend_router
from api.plaza import router as plaza_router
from api.favorite import router as favorite_router
from api.admin import router as admin_router
from sqlalchemy import text
from models.database import SessionLocal

app = FastAPI(title="智教通 API", description="智能教学辅助平台后端接口", version="1.0.0")
logger = logging.getLogger("zjiaotong.request")

class RequestLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request_id = request.headers.get("X-Request-ID") or uuid4().hex
        try:
            response = await call_next(request)
            logger.info("request_id=%s method=%s path=%s status=%s", request_id, request.method, request.url.path, response.status_code)
        except Exception:
            logger.exception("request_id=%s method=%s path=%s failed", request_id, request.method, request.url.path)
            raise
        response.headers["X-Request-ID"] = request_id
        return response

app.add_middleware(RequestLogMiddleware)
app.add_middleware(CORSMiddleware, allow_origins=settings.CORS_ORIGINS, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(user_router, prefix="/api/auth", tags=["auth"])
app.include_router(tool_router, prefix="/api/tools", tags=["tools"])
app.include_router(chat_router, prefix="/api/chat", tags=["chat"])
app.include_router(usage_router, prefix="/api/usage", tags=["usage"])
app.include_router(recommend_router, prefix="/api/recommend", tags=["recommend"])
app.include_router(plaza_router, prefix="/api/plaza", tags=["plaza"])
app.include_router(favorite_router, prefix="/api/favorites", tags=["favorites"])
app.include_router(admin_router, prefix="/api/admin", tags=["admin"])

@app.get("/")
async def root(): return {"message": "智教通 API 服务运行中"}

@app.get("/api/health")
async def health_check(): return {"status": "healthy", "version": "1.0.0"}

@app.get("/api/readiness")
async def readiness_check():
    database = "ready"
    try:
        db = SessionLocal(); db.execute(text("SELECT 1")); db.close()
    except Exception:
        database = "unavailable"
    ai = "configured" if settings.AI_PROVIDER == "mock" or bool(settings.DEEPSEEK_API_KEY) else "unconfigured"
    ready = database == "ready" and ai != "unconfigured"
    return {"status": "ready" if ready else "not_ready", "components": {"database": database, "ai": ai}}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
