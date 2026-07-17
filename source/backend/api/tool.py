from datetime import datetime
from urllib.parse import urlencode, urlparse
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from api.dependencies import get_current_user, require_roles
from config import settings
from models.database import get_db
from models.tool import Tool, ToolTemplate
from models.user import User
from schemas.tool import (
    PublicToolListResponse,
    ShareSettings,
    ToolCreate,
    ToolListResponse,
    ToolPublicResponse,
    ToolResponse,
    ToolUpdate,
)
from services.audit_service import write_audit
from services.tool_access_service import (
    assert_tool_can_be_used,
    assert_tool_manager,
    can_view_public_share,
    is_plaza_visible,
    public_tool_payload,
)


router = APIRouter()


def _share_code() -> str:
    return uuid4().hex[:12]


def _page(query, page: int, page_size: int):
    total = query.count()
    return total, query.offset((page - 1) * page_size).limit(page_size).all()


def _tool_or_404(db: Session, tool_id: int, include_deleted: bool = False) -> Tool:
    query = db.query(Tool).filter(Tool.id == tool_id)
    if not include_deleted:
        query = query.filter(Tool.deleted_at.is_(None))
    tool = query.first()
    if not tool:
        raise HTTPException(status_code=404, detail="工具不存在")
    return tool


@router.get("/presets", response_model=ToolListResponse)
def get_preset_tools(
    category: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("teacher", "admin")),
):
    query = db.query(Tool).filter(Tool.is_preset.is_(True), Tool.deleted_at.is_(None))
    if category:
        query = query.filter(Tool.category == category)
    total, items = _page(query.order_by(Tool.created_at.desc()), page, page_size)
    return ToolListResponse(total=total, items=items, page=page, page_size=page_size)


@router.get("/id/{tool_id}", response_model=ToolResponse)
def get_tool(
    tool_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    tool = _tool_or_404(db, tool_id)
    assert_tool_can_be_used(current_user, tool)
    return tool


@router.get("/share/{share_code}", response_model=ToolPublicResponse)
def get_shared_tool(share_code: str, db: Session = Depends(get_db)):
    tool = db.query(Tool).filter(Tool.share_code == share_code).first()
    if not tool or not can_view_public_share(tool):
        raise HTTPException(status_code=404, detail="分享链接不存在、已过期或已撤销")
    return public_tool_payload(tool)


@router.get("/mine/list", response_model=ToolListResponse)
def get_my_tools(
    category: str | None = Query(None),
    search: str | None = Query(None, max_length=100),
    include_deleted: bool = Query(False),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("teacher", "admin")),
):
    query = db.query(Tool)
    if current_user.role != "admin":
        query = query.filter(Tool.creator_id == current_user.id)
    if not include_deleted:
        query = query.filter(Tool.deleted_at.is_(None))
    if category:
        query = query.filter(Tool.category == category)
    if search:
        pattern = f"%{search.strip()}%"
        query = query.filter(or_(Tool.name.ilike(pattern), Tool.description.ilike(pattern)))
    total, items = _page(query.order_by(Tool.updated_at.desc()), page, page_size)
    return ToolListResponse(total=total, items=items, page=page, page_size=page_size)


@router.get("/templates/list")
def get_templates(db: Session = Depends(get_db), current_user: User = Depends(require_roles("teacher", "admin"))):
    return db.query(ToolTemplate).order_by(ToolTemplate.created_at.desc()).all()


@router.post("/", response_model=ToolResponse, status_code=status.HTTP_201_CREATED)
def create_tool(tool: ToolCreate, db: Session = Depends(get_db), current_user: User = Depends(require_roles("teacher", "admin"))):
    external_url = tool.interface_config.get("external_url", "") if tool.interface_config else ""
    db_tool = Tool(
        name=tool.name,
        description=tool.description,
        category=tool.category,
        subject=tool.subject,
        icon=tool.icon,
        prompt_template=tool.prompt_template,
        interface_config=tool.interface_config,
        creator_id=current_user.id,
        source_type="manual",
        plaza_status="published" if tool.is_public else "unlisted",
        share_enabled=tool.is_public,
        is_public=tool.is_public,
        share_code=_share_code(),
        external_platform_url=external_url or None,
    )
    db.add(db_tool)
    db.flush()
    write_audit(db, "create", "tool", db_tool.id, actor_id=current_user.id)
    db.commit()
    db.refresh(db_tool)
    return db_tool


@router.post("/presets/{tool_id}/copy", response_model=ToolResponse, status_code=status.HTTP_201_CREATED)
def copy_preset_tool(tool_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_roles("teacher", "admin"))):
    preset = _tool_or_404(db, tool_id)
    if not preset.is_preset:
        raise HTTPException(status_code=400, detail="只能复制预设工具")
    template = db.query(ToolTemplate).filter(ToolTemplate.name == preset.name).first()
    copy = Tool(
        name=f"{preset.name}（副本）",
        description=preset.description,
        category=preset.category,
        subject=preset.subject,
        icon=preset.icon,
        prompt_template=preset.prompt_template,
        interface_config=preset.interface_config,
        creator_id=current_user.id,
        template_source_id=template.id if template else None,
        source_type="preset_copy",
        plaza_status="unlisted",
        share_enabled=False,
        is_public=False,
        share_code=_share_code(),
    )
    db.add(copy)
    db.flush()
    write_audit(db, "copy_preset", "tool", copy.id, actor_id=current_user.id, details={"source_tool_id": preset.id})
    db.commit()
    db.refresh(copy)
    return copy


@router.put("/{tool_id}", response_model=ToolResponse)
def update_tool(tool_id: int, tool_update: ToolUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_roles("teacher", "admin"))):
    tool = _tool_or_404(db, tool_id)
    assert_tool_manager(current_user, tool)
    update_data = tool_update.model_dump(exclude_unset=True)
    if "plaza_status" in update_data and update_data["plaza_status"] not in {"published", "unlisted"}:
        raise HTTPException(status_code=422, detail="广场状态无效")
    for key, value in update_data.items():
        setattr(tool, key, value)
    if "plaza_status" in update_data:
        tool.is_public = tool.plaza_status == "published"
    write_audit(db, "update", "tool", tool.id, actor_id=current_user.id, details={"fields": sorted(update_data)})
    db.commit()
    db.refresh(tool)
    return tool


@router.delete("/{tool_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tool(tool_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_roles("teacher", "admin"))):
    tool = _tool_or_404(db, tool_id)
    assert_tool_manager(current_user, tool)
    tool.deleted_at = datetime.utcnow()
    tool.share_enabled = False
    tool.plaza_status = "unlisted"
    tool.is_public = False
    write_audit(db, "soft_delete", "tool", tool.id, actor_id=current_user.id)
    db.commit()


@router.post("/{tool_id}/restore", response_model=ToolResponse)
def restore_tool(tool_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_roles("admin"))):
    tool = _tool_or_404(db, tool_id, include_deleted=True)
    if tool.deleted_at is None:
        raise HTTPException(status_code=400, detail="工具未被删除")
    tool.deleted_at = None
    write_audit(db, "restore", "tool", tool.id, actor_id=current_user.id)
    db.commit()
    db.refresh(tool)
    return tool


@router.get("/{tool_id}/share")
def get_share_link(tool_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_roles("teacher", "admin"))):
    tool = _tool_or_404(db, tool_id)
    assert_tool_manager(current_user, tool)
    if not tool.share_code:
        tool.share_code = _share_code()
        db.commit()
    return {
        "share_code": tool.share_code,
        "share_enabled": tool.share_enabled,
        "share_expires_at": tool.share_expires_at,
        "share_url": f"{settings.FRONTEND_URL}/share/{tool.share_code}",
    }


@router.put("/{tool_id}/share")
def update_share_settings(
    tool_id: int,
    settings_payload: ShareSettings,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("teacher", "admin")),
):
    tool = _tool_or_404(db, tool_id)
    assert_tool_manager(current_user, tool)
    if settings_payload.expires_at and settings_payload.expires_at <= datetime.utcnow():
        raise HTTPException(status_code=422, detail="分享过期时间必须在未来")
    tool.share_enabled = settings_payload.enabled
    tool.share_expires_at = settings_payload.expires_at
    tool.share_code = tool.share_code or _share_code()
    write_audit(db, "update_share", "tool", tool.id, actor_id=current_user.id, details={"enabled": tool.share_enabled})
    db.commit()
    return {"share_code": tool.share_code, "share_enabled": tool.share_enabled, "share_expires_at": tool.share_expires_at, "share_url": f"{settings.FRONTEND_URL}/share/{tool.share_code}"}


@router.post("/{tool_id}/share/revoke")
def revoke_share(tool_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_roles("teacher", "admin"))):
    tool = _tool_or_404(db, tool_id)
    assert_tool_manager(current_user, tool)
    tool.share_enabled = False
    write_audit(db, "revoke_share", "tool", tool.id, actor_id=current_user.id)
    db.commit()
    return {"message": "分享已撤销"}


@router.post("/{tool_id}/platform-launch")
def platform_launch(
    tool_id: int,
    need_type: str | None = Query(None, max_length=50),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("teacher", "admin")),
):
    tool = _tool_or_404(db, tool_id)
    assert_tool_manager(current_user, tool)
    base_url = tool.external_platform_url or settings.AGENT_PLATFORM_URL
    parsed = urlparse(base_url)
    if not base_url or parsed.scheme not in {"https", "http"} or not parsed.netloc:
        raise HTTPException(status_code=503, detail="尚未配置师大智能体平台地址")
    query = urlencode({"subject": tool.subject or "", "category": tool.category, "need_type": need_type or "", "source_tool": tool.id})
    separator = "&" if parsed.query else "?"
    url = f"{base_url}{separator}{query}"
    write_audit(db, "platform_redirect", "tool", tool.id, actor_id=current_user.id, details={"need_type": need_type})
    db.commit()
    return {"url": url}
