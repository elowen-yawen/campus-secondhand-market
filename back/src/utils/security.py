"""安全工具：密码加密与 JWT。"""

import hashlib
import hmac
import os
from datetime import datetime, timedelta
from functools import wraps

import jwt
from flask import request, g

from ..config import settings
from .response import error


def hash_password(password: str) -> str:
    """密码哈希。"""

    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
    return salt.hex() + ":" + key.hex()


def verify_password(password: str, password_hash: str) -> bool:
    """校验密码。"""

    try:
        salt_hex, key_hex = password_hash.split(":")
        salt = bytes.fromhex(salt_hex)
        key = bytes.fromhex(key_hex)
        new_key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
        return hmac.compare_digest(key, new_key)
    except (ValueError, AttributeError):
        return False


def generate_token(user_id: int) -> str:
    """生成 JWT。"""

    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(days=7),
        "iat": datetime.utcnow(),
    }
    return jwt.encode(payload, settings.secret_key, algorithm="HS256")


def decode_token(token: str) -> dict | None:
    """解码 JWT。"""

    try:
        return jwt.decode(token, settings.secret_key, algorithms=["HS256"])
    except jwt.PyJWTError:
        return None


def login_required(f):
    """JWT 登录校验装饰器。

    从请求头 Authorization: Bearer <token> 中提取并校验 JWT，
    校验通过后将 user_id 注入 g.current_user_id，否则返回 401。
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return error("未登录或 Token 无效", code=401, status_code=401)
        token = auth_header[7:]
        payload = decode_token(token)
        if payload is None:
            return error("Token 已过期或无效", code=401, status_code=401)
        g.current_user_id = payload["user_id"]
        return f(*args, **kwargs)

    return decorated

