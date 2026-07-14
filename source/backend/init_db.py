from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from models.database import engine, Base, SessionLocal
from models import User, Tool, ToolTemplate, UsageLog, Favorite, RecommendRule
from sqlalchemy.orm import Session
from config import settings
import json

def server_url_from_database_url(database_url: str) -> str:
    """Return a SQLAlchemy URL that connects to the server without selecting a database."""
    return make_url(database_url)._replace(database=None).render_as_string(hide_password=False)


def create_database_if_not_exists():
    """如果数据库不存在则创建"""
    # 连接到MySQL服务器（不指定数据库）
    server_url = server_url_from_database_url(settings.DATABASE_URL)
    server_engine = create_engine(server_url)

    with server_engine.connect() as conn:
        # 创建数据库
        conn.execute(text("CREATE DATABASE IF NOT EXISTS zjiaotong CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
        conn.commit()
    print("数据库创建/确认完成")

def init_database():
    """初始化数据库：创建表并插入预设数据"""
    # 先创建数据库
    create_database_if_not_exists()

    # 创建所有表
    Base.metadata.create_all(bind=engine)
    print("数据库表创建完成")

    # 插入预设工具模板
    with Session(engine) as session:
        # 检查是否已有预设数据
        existing_count = session.query(ToolTemplate).count()
        if existing_count == 0:
            insert_preset_templates(session)
            print("预设工具模板插入完成")
        else:
            print("预设工具模板已存在，跳过插入")
    
    # 插入预设工具到tools表
    with Session(engine) as session:
        existing_tools = session.query(Tool).filter(Tool.is_preset == True).count()
        if existing_tools == 0:
            insert_preset_tools(session)
            print("预设工具插入完成")
        else:
            print("预设工具已存在，跳过插入")

def insert_preset_templates(session: Session):
    """插入预设工具模板"""
    templates = [
        # 文科工具
        {
            "name": "古诗词趣味赏析",
            "category": "文科",
            "subject": "语文",
            "description": "输入诗词名，获得趣味化赏析、背景知识、知识卡片",
            "prompt_template": "你是一个古诗词赏析助手，请用趣味的方式赏析这首诗，包括：1.诗句解读 2.创作背景 3.趣味知识 4.知识卡片",
            "icon": "🏮"
        },
        {
            "name": "作文灵感助手",
            "category": "文科",
            "subject": "语文",
            "description": "输入作文题目/主题，获得写作思路和素材建议",
            "prompt_template": "你是一个作文辅导助手，请帮助学生打开写作思路，提供：1.写作角度 2.素材建议 3.优秀开头 4.注意事项",
            "icon": "✍️"
        },
        {
            "name": "名词解释器",
            "category": "文科",
            "subject": "政治",
            "description": "输入专业名词，获得通俗易懂的解释",
            "prompt_template": "你是一个名词解释助手，请用通俗易懂的语言解释这个名词，包括：1.基本含义 2.生活例子 3.相关概念 4.记忆技巧",
            "icon": "📖"
        },
        {
            "name": "阅读理解辅助",
            "category": "文科",
            "subject": "语文",
            "description": "输入文章段落，获得理解要点和分析",
            "prompt_template": "你是一个阅读理解助手，请帮助分析这段文字，包括：1.中心思想 2.关键句子 3.写作手法 4.练习题",
            "icon": "📚"
        },
        {
            "name": "英语单词卡片",
            "category": "文科",
            "subject": "英语",
            "description": "输入单词，生成趣味化学习卡片",
            "prompt_template": "你是一个英语学习助手，请生成单词学习卡片，包括：1.音标 2.词义 3.例句 4.记忆方法 5.相关词汇",
            "icon": "🔤"
        },
        {
            "name": "诗词飞花令",
            "category": "文科",
            "subject": "语文",
            "description": "输入关键字，AI带你玩飞花令游戏",
            "prompt_template": "你是一个飞花令游戏助手，请和用户玩飞花令游戏，规则：1.输入关键字 2.轮流说出含该字的诗句 3.评判并计分",
            "icon": "🌸"
        },
        # 理科工具
        {
            "name": "公式推导助手",
            "category": "理科",
            "subject": "数学",
            "description": "输入公式名，获得推导过程和几何直觉解释",
            "prompt_template": "你是一个数学公式推导助手，请详细推导这个公式，包括：1.公式内容 2.推导过程 3.几何解释 4.应用场景",
            "icon": "🧮"
        },
        {
            "name": "实验模拟讲解",
            "category": "理科",
            "subject": "物理",
            "description": "输入实验名，获得步骤讲解和注意事项",
            "prompt_template": "你是一个实验讲解助手，请详细讲解这个实验，包括：1.实验目的 2.实验步骤 3.注意事项 4.思考题",
            "icon": "🔬"
        },
        {
            "name": "逻辑思维训练",
            "category": "理科",
            "subject": "数学",
            "description": "提供逻辑题并引导思考过程",
            "prompt_template": "你是一个逻辑思维训练助手，请出一道逻辑题，引导学生思考，包括：1.题目描述 2.思考提示 3.解题思路 4.类似题目",
            "icon": "🧠"
        },
        {
            "name": "错题分析器",
            "category": "理科",
            "subject": "数学",
            "description": "输入错题，分析错误原因并给出正确思路",
            "prompt_template": "你是一个错题分析助手，请分析这道错题，包括：1.错误原因 2.正确思路 3.类似题目 4.预防方法",
            "icon": "📝"
        },
        {
            "name": "概念辨析器",
            "category": "理科",
            "subject": "物理",
            "description": "输入易混淆概念，获得对比分析",
            "prompt_template": "你是一个概念辨析助手，请对比分析这两个概念，包括：1.概念定义 2.相同点 3.不同点 4.记忆技巧",
            "icon": "⚖️"
        },
        {
            "name": "数据分析助手",
            "category": "理科",
            "subject": "数学",
            "description": "输入数据集描述，获得分析思路",
            "prompt_template": "你是一个数据分析助手，请提供数据分析思路，包括：1.数据整理 2.分析方法 3.可视化建议 4.结论方向",
            "icon": "📊"
        },
        # 通用工具
        {
            "name": "AI学习助手",
            "category": "通用",
            "subject": "通用",
            "description": "通用AI问答，解答学习问题",
            "prompt_template": "你是一个AI学习助手，请帮助学生解答学习问题，包括：1.问题解答 2.相关知识 3.学习建议 4.拓展内容",
            "icon": "🤖"
        },
        {
            "name": "知识卡片生成器",
            "category": "通用",
            "subject": "通用",
            "description": "输入知识点，生成学习卡片",
            "prompt_template": "你是一个知识卡片生成助手，请生成学习卡片，包括：1.知识点标题 2.核心内容 3.记忆口诀 4.相关链接",
            "icon": "📋"
        },
        {
            "name": "思维导图助手",
            "category": "通用",
            "subject": "通用",
            "description": "输入主题，生成思维导图结构",
            "prompt_template": "你是一个思维导图助手，请生成思维导图结构，包括：1.中心主题 2.一级分支 3.二级分支 4.关键词",
            "icon": "🗺️"
        }
    ]
    
    for template_data in templates:
        template = ToolTemplate(**template_data)
        session.add(template)
    
    session.commit()

def insert_preset_tools(session: Session):
    """插入预设工具到tools表"""
    import uuid
    
    tools = [
        # 文科工具
        {
            "name": "古诗词趣味赏析",
            "category": "文科",
            "subject": "语文",
            "description": "输入诗词名，获得趣味化赏析、背景知识、知识卡片",
            "prompt_template": "你是一个古诗词赏析助手，请用趣味的方式赏析这首诗，包括：1.诗句解读 2.创作背景 3.趣味知识 4.知识卡片",
            "icon": "🏮",
            "is_preset": True,
            "share_code": str(uuid.uuid4())[:8]
        },
        {
            "name": "作文灵感助手",
            "category": "文科",
            "subject": "语文",
            "description": "输入作文题目/主题，获得写作思路和素材建议",
            "prompt_template": "你是一个作文辅导助手，请帮助学生打开写作思路，提供：1.写作角度 2.素材建议 3.优秀开头 4.注意事项",
            "icon": "✍️",
            "is_preset": True,
            "share_code": str(uuid.uuid4())[:8]
        },
        {
            "name": "名词解释器",
            "category": "文科",
            "subject": "政治",
            "description": "输入专业名词，获得通俗易懂的解释",
            "prompt_template": "你是一个名词解释助手，请用通俗易懂的语言解释这个名词，包括：1.基本含义 2.生活例子 3.相关概念 4.记忆技巧",
            "icon": "📖",
            "is_preset": True,
            "share_code": str(uuid.uuid4())[:8]
        },
        {
            "name": "阅读理解辅助",
            "category": "文科",
            "subject": "语文",
            "description": "输入文章段落，获得理解要点和分析",
            "prompt_template": "你是一个阅读理解助手，请帮助分析这段文字，包括：1.中心思想 2.关键句子 3.写作手法 4.练习题",
            "icon": "📚",
            "is_preset": True,
            "share_code": str(uuid.uuid4())[:8]
        },
        {
            "name": "英语单词卡片",
            "category": "文科",
            "subject": "英语",
            "description": "输入单词，生成趣味化学习卡片",
            "prompt_template": "你是一个英语学习助手，请生成单词学习卡片，包括：1.音标 2.词义 3.例句 4.记忆方法 5.相关词汇",
            "icon": "🔤",
            "is_preset": True,
            "share_code": str(uuid.uuid4())[:8]
        },
        {
            "name": "诗词飞花令",
            "category": "文科",
            "subject": "语文",
            "description": "输入关键字，AI带你玩飞花令游戏",
            "prompt_template": "你是一个飞花令游戏助手，请和用户玩飞花令游戏，规则：1.输入关键字 2.轮流说出含该字的诗句 3.评判并计分",
            "icon": "🌸",
            "is_preset": True,
            "share_code": str(uuid.uuid4())[:8]
        },
        # 理科工具
        {
            "name": "公式推导助手",
            "category": "理科",
            "subject": "数学",
            "description": "输入公式名，获得推导过程和几何直觉解释",
            "prompt_template": "你是一个数学公式推导助手，请详细推导这个公式，包括：1.公式内容 2.推导过程 3.几何解释 4.应用场景",
            "icon": "🧮",
            "is_preset": True,
            "share_code": str(uuid.uuid4())[:8]
        },
        {
            "name": "实验模拟讲解",
            "category": "理科",
            "subject": "物理",
            "description": "输入实验名，获得步骤讲解和注意事项",
            "prompt_template": "你是一个实验讲解助手，请详细讲解这个实验，包括：1.实验目的 2.实验步骤 3.注意事项 4.思考题",
            "icon": "🔬",
            "is_preset": True,
            "share_code": str(uuid.uuid4())[:8]
        },
        {
            "name": "逻辑思维训练",
            "category": "理科",
            "subject": "数学",
            "description": "提供逻辑题并引导思考过程",
            "prompt_template": "你是一个逻辑思维训练助手，请出一道逻辑题，引导学生思考，包括：1.题目描述 2.思考提示 3.解题思路 4.类似题目",
            "icon": "🧠",
            "is_preset": True,
            "share_code": str(uuid.uuid4())[:8]
        },
        {
            "name": "错题分析器",
            "category": "理科",
            "subject": "数学",
            "description": "输入错题，分析错误原因并给出正确思路",
            "prompt_template": "你是一个错题分析助手，请分析这道错题，包括：1.错误原因 2.正确思路 3.类似题目 4.预防方法",
            "icon": "📝",
            "is_preset": True,
            "share_code": str(uuid.uuid4())[:8]
        },
        {
            "name": "概念辨析器",
            "category": "理科",
            "subject": "物理",
            "description": "输入易混淆概念，获得对比分析",
            "prompt_template": "你是一个概念辨析助手，请对比分析这两个概念，包括：1.概念定义 2.相同点 3.不同点 4.记忆技巧",
            "icon": "⚖️",
            "is_preset": True,
            "share_code": str(uuid.uuid4())[:8]
        },
        {
            "name": "数据分析助手",
            "category": "理科",
            "subject": "数学",
            "description": "输入数据集描述，获得分析思路",
            "prompt_template": "你是一个数据分析助手，请提供数据分析思路，包括：1.数据整理 2.分析方法 3.可视化建议 4.结论方向",
            "icon": "📊",
            "is_preset": True,
            "share_code": str(uuid.uuid4())[:8]
        },
        # 通用工具
        {
            "name": "AI学习助手",
            "category": "通用",
            "subject": "通用",
            "description": "通用AI问答，解答学习问题",
            "prompt_template": "你是一个AI学习助手，请帮助学生解答学习问题，包括：1.问题解答 2.相关知识 3.学习建议 4.拓展内容",
            "icon": "🤖",
            "is_preset": True,
            "share_code": str(uuid.uuid4())[:8]
        },
        {
            "name": "知识卡片生成器",
            "category": "通用",
            "subject": "通用",
            "description": "输入知识点，生成学习卡片",
            "prompt_template": "你是一个知识卡片生成助手，请生成学习卡片，包括：1.知识点标题 2.核心内容 3.记忆口诀 4.相关链接",
            "icon": "📋",
            "is_preset": True,
            "share_code": str(uuid.uuid4())[:8]
        },
        {
            "name": "思维导图助手",
            "category": "通用",
            "subject": "通用",
            "description": "输入主题，生成思维导图结构",
            "prompt_template": "你是一个思维导图助手，请生成思维导图结构，包括：1.中心主题 2.一级分支 3.二级分支 4.关键词",
            "icon": "🗺️",
            "is_preset": True,
            "share_code": str(uuid.uuid4())[:8]
        }
    ]
    
    for tool_data in tools:
        tool = Tool(**tool_data)
        session.add(tool)
    
    session.commit()

if __name__ == "__main__":
    init_database()
