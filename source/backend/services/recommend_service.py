# services/recommend_service.py
from sqlalchemy.orm import Session
from models.recommend import RecommendRule
from models.tool import Tool

def get_recommend_rules(db: Session):
    """获取推荐规则"""
    return db.query(RecommendRule).filter(RecommendRule.is_active == True).all()

def match_recommendation(db: Session, subject: str, need_type: str):
    """根据学科和需求类型匹配推荐"""
    # 获取所有活跃规则
    rules = db.query(RecommendRule).filter(RecommendRule.is_active == True).all()
    
    matched_tools = []
    for rule in rules:
        # 检查学科匹配
        if subject in rule.subjects or 'all' in rule.subjects:
            # 检查需求类型匹配
            if need_type in rule.need_types or 'all' in rule.need_types:
                # 获取推荐的工具
                tool_ids = rule.tool_ids.split(',') if rule.tool_ids else []
                for tool_id in tool_ids:
                    tool = db.query(Tool).filter(Tool.id == int(tool_id)).first()
                    if tool and tool not in matched_tools:
                        matched_tools.append(tool)
    
    return matched_tools

def create_recommend_rule(db: Session, rule_data: dict):
    """创建推荐规则"""
    rule = RecommendRule(**rule_data)
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return rule

def update_recommend_rule(db: Session, rule_id: int, rule_data: dict):
    """更新推荐规则"""
    rule = db.query(RecommendRule).filter(RecommendRule.id == rule_id).first()
    if not rule:
        return None
    for key, value in rule_data.items():
        if value is not None:
            setattr(rule, key, value)
    db.commit()
    db.refresh(rule)
    return rule
