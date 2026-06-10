"""用户与认证路由。"""

import os
import uuid

from flask import Blueprint, g, request

from ..services import user_service
from ..utils.response import success, error
from ..utils.security import generate_token, decode_token, login_required

user_bp = Blueprint("user", __name__)


@user_bp.post("/register")
def register():
    """用户注册。"""

    data = request.get_json(silent=True) or {}
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()
    if not username or not password:
        return error("用户名和密码不能为空")
    try:
        user = user_service.register(
            username=username,
            password=password,
            nickname=data.get("nickname", username),
            bio=data.get("bio", ""),
            campus=data.get("campus", ""),
        )
        token = generate_token(user.id)
        return success({
            "token": token,
            "user": _user_to_vo(user),
        })
    except ValueError as e:
        return error(str(e))


@user_bp.post("/login")
def login():
    """用户登录。"""

    data = request.get_json(silent=True) or {}
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()
    if not username or not password:
        return error("用户名和密码不能为空")
    try:
        user = user_service.login(username, password)
        token = generate_token(user.id)
        return success({
            "token": token,
            "user": _user_to_vo(user),
        })
    except ValueError as e:
        return error(str(e))


@user_bp.get("/<int:user_id>")
def get_by_id(user_id: int):
    """按 ID 获取用户信息。"""

    user = user_service.find_by_id(user_id)
    if not user:
        return error("用户不存在")
    return success(_user_to_vo(user))


@user_bp.get("/list")
def list_all():
    """获取用户列表。"""

    users = user_service.find_all()
    return success([_user_to_vo(u) for u in users])


@user_bp.delete("/<int:user_id>")
@login_required
def delete_by_id(user_id: int):
    """删除用户。"""

    user_service.delete_by_id(user_id)
    return success()


@user_bp.put("/profile")
@login_required
def update_profile():
    """更新用户资料。"""

    data = request.get_json(silent=True) or {}
    user_id = g.current_user_id
    try:
        user_service.update_profile(
            user_id=user_id,
            password=data.get("password"),
            phone=data.get("phone"),
            avatar=data.get("avatar"),
            nickname=data.get("nickname"),
            bio=data.get("bio"),
            campus=data.get("campus"),
        )
        return success()
    except ValueError as e:
        return error(str(e))


@user_bp.post("/avatar/upload")
@login_required
def upload_avatar():
    """上传头像。"""

    file = request.files.get("file")
    user_id = g.current_user_id
    if not file or file.filename == "":
        return error("图片文件不能为空")
    ext = os.path.splitext(file.filename)[1] if file.filename else ".png"
    filename = f"{uuid.uuid4()}{ext}"
    upload_dir = os.path.join("uploads", "avatar")
    os.makedirs(upload_dir, exist_ok=True)
    file.save(os.path.join(upload_dir, filename))
    user_service.update_profile(user_id, avatar=f"/uploads/avatar/{filename}")
    return success({"url": f"/uploads/avatar/{filename}"})


@user_bp.get("/wallet")
@login_required
def get_wallet():
    """获取钱包信息。"""

    user_id = g.current_user_id
    try:
        return success(user_service.get_wallet(user_id))
    except ValueError as e:
        return error(str(e))


def _user_to_vo(user) -> dict:
    """用户转 VO。"""

    return {
        "id": user.id,
        "username": user.username,
        "nickname": user.nickname,
        "bio": user.bio,
        "campus": user.campus,
        "phone": user.phone,
        "avatar": user.avatar,
        "balance": str(user.balance) if hasattr(user, "balance") else "0.00",
        "createdAt": user.created_at.isoformat() if user.created_at else "",
    }
