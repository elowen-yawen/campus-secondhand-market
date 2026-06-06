"""数据模型定义。"""

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """用户表。"""

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password_hash: str
    nickname: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Goods(SQLModel, table=True):
    """商品表。"""

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str = ""
    price: float
    cover_url: str = ""
    seller_id: int = Field(index=True)
    status: str = "on_sale"
    created_at: datetime = Field(default_factory=datetime.utcnow)
