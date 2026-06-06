"""数据模型定义。"""

from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """用户表。"""

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, max_length=50)
    password_hash: str = Field(max_length=256)
    nickname: str = Field(default="", max_length=50)
    bio: str = Field(default="", max_length=500)
    campus: str = Field(default="", max_length=100)
    phone: str = Field(default="", max_length=20)
    avatar: str = Field(default="", max_length=500)
    balance: Decimal = Field(default=Decimal("0.00"), max_digits=10, decimal_places=2)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Category(SQLModel, table=True):
    """商品分类表。"""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=50)
    is_active: bool = Field(default=True)


class Goods(SQLModel, table=True):
    """商品表。"""

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    description: str = Field(default="", max_length=2000)
    price: Decimal = Field(default=Decimal("0.00"), max_digits=10, decimal_places=2)
    cover_url: str = Field(default="", max_length=500)
    seller_id: int = Field(index=True, foreign_key="user.id")
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    campus: str = Field(default="", max_length=100)
    condition_level: str = Field(default="", max_length=50)
    status: str = Field(default="on_sale", max_length=20)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class GoodsImage(SQLModel, table=True):
    """商品图片表。"""

    id: Optional[int] = Field(default=None, primary_key=True)
    goods_id: int = Field(index=True, foreign_key="goods.id")
    image_url: str = Field(max_length=500)


class Wanted(SQLModel, table=True):
    """求购表。"""

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True, foreign_key="user.id")
    title: str = Field(max_length=200)
    description: str = Field(default="", max_length=2000)
    budget_min: Decimal = Field(default=Decimal("0.00"), max_digits=10, decimal_places=2)
    budget_max: Decimal = Field(default=Decimal("0.00"), max_digits=10, decimal_places=2)
    campus: str = Field(default="", max_length=100)
    condition_level: str = Field(default="", max_length=50)
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    status: str = Field(default="active", max_length=20)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class WantedImage(SQLModel, table=True):
    """求购图片表。"""

    id: Optional[int] = Field(default=None, primary_key=True)
    wanted_id: int = Field(index=True, foreign_key="wanted.id")
    image_url: str = Field(max_length=500)


class Favorite(SQLModel, table=True):
    """收藏表。"""

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True, foreign_key="user.id")
    item_id: Optional[int] = Field(default=None, index=True)
    wanted_id: Optional[int] = Field(default=None, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class TradeOrder(SQLModel, table=True):
    """交易订单表。"""

    id: Optional[int] = Field(default=None, primary_key=True)
    item_id: int = Field(index=True, foreign_key="goods.id")
    buyer_id: int = Field(index=True, foreign_key="user.id")
    seller_id: int = Field(index=True, foreign_key="user.id")
    trade_location: str = Field(default="", max_length=200)
    remark: str = Field(default="", max_length=500)
    status: str = Field(default="pending", max_length=20)
    cancel_reason: str = Field(default="", max_length=500)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TradeOrderLog(SQLModel, table=True):
    """订单操作日志表。"""

    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(index=True, foreign_key="tradeorder.id")
    action: str = Field(max_length=50)
    operator_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Review(SQLModel, table=True):
    """评价表。"""

    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(index=True, foreign_key="tradeorder.id")
    reviewer_id: int = Field(index=True, foreign_key="user.id")
    reviewee_id: int = Field(index=True, foreign_key="user.id")
    rating: int = Field(default=5, ge=1, le=5)
    content: str = Field(default="", max_length=500)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ChatSession(SQLModel, table=True):
    """聊天会话表。"""

    id: Optional[int] = Field(default=None, primary_key=True)
    item_id: Optional[int] = Field(default=None, foreign_key="goods.id")
    wanted_id: Optional[int] = Field(default=None, foreign_key="wanted.id")
    user1_id: int = Field(index=True, foreign_key="user.id")
    user2_id: int = Field(index=True, foreign_key="user.id")
    last_message: str = Field(default="", max_length=500)
    last_message_at: datetime = Field(default_factory=datetime.utcnow)
    unread_count: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ChatMessage(SQLModel, table=True):
    """聊天消息表。"""

    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: int = Field(index=True, foreign_key="chatsession.id")
    sender_id: int = Field(index=True, foreign_key="user.id")
    message_type: str = Field(default="text", max_length=20)
    content: str = Field(max_length=2000)
    is_read: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
