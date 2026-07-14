from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from api.user import router as user_router
from api.tool import router as tool_router
from api.chat import router as chat_router
from api.usage import router as usage_router
from api.recommend import router as recommend_router
from api.plaza import router as plaza_router

app = FastAPI(
    title="智教通 API",
    description="AI智能体教学辅助平台后端接口",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(user_router, prefix="/api/auth", tags=["用户认证"])
app.include_router(tool_router, prefix="/api/tools", tags=["工具管理"])
app.include_router(chat_router, prefix="/api/chat", tags=["AI对话"])
app.include_router(usage_router, prefix="/api/usage", tags=["使用统计"])
app.include_router(recommend_router, prefix="/api/recommend", tags=["需求推荐"])
app.include_router(plaza_router, prefix="/api/plaza", tags=["工具广场"])

@app.get("/")
async def root():
    return {"message": "智教通 API 服务运行中"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)