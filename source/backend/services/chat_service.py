# services/chat_service.py
from sqlalchemy.orm import Session
from models.tool import Tool
from services.deepseek import chat_with_deepseek

def chat_with_tool(db: Session, tool_id: int, message: str, history: list = None):
    """使用工具进行AI对话"""
    tool = db.query(Tool).filter(Tool.id == tool_id).first()
    if not tool:
        return None
    
    # 构建系统提示
    system_prompt = f"你是一个教学助手，专门帮助学生使用{tool.name}工具。{tool.description}"
    
    # 调用DeepSeek API
    response = chat_with_deepseek(message, system_prompt, history)
    return response

def chat_general(db: Session, message: str, history: list = None):
    """通用AI对话"""
    system_prompt = "你是一个教学助手，帮助学生解答学习问题。请用简单易懂的语言回答。"
    response = chat_with_deepseek(message, system_prompt, history)
    return response
