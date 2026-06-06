"""用户服务。"""

from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlmodel import Session, select

from ..db import engine
from ..models import User
from ..utils.security import hash_password, verify_password


def register(username: str, password: str, nickname: str, bio: str, campus: str) -> User:
    """用户注册。"""

    with Session(engine) as session:
        existing = session.exec(select(User).where(User.username == username)).first()
        if existing:
            raise ValueError("用户名已存在")
        user = User(
            username=username,
            password_hash=hash_password(password),
            nickname=nickname or username,
            bio=bio or "",
            campus=campus or "",
            created_at=datetime.utcnow(),
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


def login(username: str, password: str) -> User:
    """用户登录。"""

    with Session(engine) as session:
        user = session.exec(select(User).where(User.username == username)).first()
        if not user:
            raise ValueError("用户名或密码错误")
        if not verify_password(password, user.password_hash):
            raise ValueError("用户名或密码错误")
        return user


def find_by_id(user_id: int) -> Optional[User]:
    """按 ID 查找用户。"""

    with Session(engine) as session:
        return session.get(User, user_id)


def find_all() -> list[User]:
    """获取所有用户。"""

    with Session(engine) as session:
        return list(session.exec(select(User)).all())


def delete_by_id(user_id: int) -> None:
    """删除用户。"""

    with Session(engine) as session:
        user = session.get(User, user_id)
        if user:
            session.delete(user)
            session.commit()


def update_profile(
    user_id: int,
    password: Optional[str],
    phone: Optional[str],
    avatar: Optional[str],
    nickname: Optional[str],
    bio: Optional[str],
    campus: Optional[str],
) -> None:
    """更新用户资料。"""

    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise ValueError("用户不存在")
        if password:
            user.password_hash = hash_password(password)
        if phone is not None:
            user.phone = phone
        if avatar is not None:
            user.avatar = avatar
        if nickname is not None:
            user.nickname = nickname
        if bio is not None:
            user.bio = bio
        if campus is not None:
            user.campus = campus
        session.add(user)
        session.commit()


def get_wallet(user_id: int) -> dict:
    """获取钱包信息。"""

    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise ValueError("用户不存在")
        return {
            "balance": str(user.balance),
            "totalIncome": "0.00",
            "totalExpense": "0.00",
        }
