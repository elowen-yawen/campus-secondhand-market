"""聊天路由。"""

import os
import uuid

from flask import Blueprint, g, request

from ..services import chat_service
from ..utils.response import success, error
from ..utils.security import login_required

chat_bp = Blueprint("chat", __name__)


@chat_bp.post("/sessions")
@login_required
def create_session():
    """创建聊天会话。"""

    data = request.get_json(silent=True) or {}
    user_id = g.current_user_id
    try:
        result = chat_service.create_chat_session(
            item_id=data.get("itemId"),
            wanted_id=data.get("wantedId"),
            user_id=user_id,
        )
        return success(result)
    except ValueError as e:
        return error(str(e))


@chat_bp.get("/sessions")
@login_required
def list_my_sessions():
    """我的会话列表。"""

    user_id = g.current_user_id
    return success(chat_service.list_my_sessions(user_id))


@chat_bp.post("/messages")
@login_required
def send_message():
    """发送消息。"""

    data = request.get_json(silent=True) or {}
    user_id = g.current_user_id
    session_id = data.get("sessionId")
    if not session_id:
        return error("sessionId 不能为空")
    try:
        result = chat_service.send_message(
            session_id=session_id,
            user_id=user_id,
            message_type=data.get("messageType", "text"),
            content=data.get("content", ""),
        )
        return success(result)
    except ValueError as e:
        return error(str(e))


@chat_bp.get("/sessions/<int:session_id>/messages")
@login_required
def list_messages(session_id: int):
    """会话消息列表。"""

    user_id = g.current_user_id
    try:
        return success(chat_service.list_messages(session_id, user_id))
    except ValueError as e:
        return error(str(e))


@chat_bp.put("/sessions/<int:session_id>/read")
@login_required
def mark_as_read(session_id: int):
    """标记会话已读。"""

    user_id = g.current_user_id
    try:
        chat_service.mark_as_read(session_id, user_id)
        return success()
    except ValueError as e:
        return error(str(e))


@chat_bp.post("/images/upload")
@login_required
def upload_chat_image():
    """上传聊天图片。"""

    file = request.files.get("file")
    if not file or file.filename == "":
        return error("图片文件不能为空")
    ext = os.path.splitext(file.filename)[1] if file.filename else ".png"
    filename = f"{uuid.uuid4()}{ext}"
    upload_dir = os.path.join("uploads", "chat")
    os.makedirs(upload_dir, exist_ok=True)
    file.save(os.path.join(upload_dir, filename))
    return success({"url": f"/uploads/chat/{filename}"})
