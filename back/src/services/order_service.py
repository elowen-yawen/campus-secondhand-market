"""订单服务。"""

from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlmodel import Session, select

from ..db import engine
from ..models import Goods, TradeOrder, TradeOrderLog


def create_order(item_id: int, user_id: int, trade_location: str, remark: str) -> dict:
    """创建订单。"""

    with Session(engine) as session:
        goods = session.get(Goods, item_id)
        if not goods:
            raise ValueError("商品不存在")
        if goods.status != "on_sale":
            raise ValueError("商品已下架或已售出")
        if goods.seller_id == user_id:
            raise ValueError("不能购买自己的商品")

        order = TradeOrder(
            item_id=item_id,
            buyer_id=user_id,
            seller_id=goods.seller_id,
            trade_location=trade_location or "",
            remark=remark or "",
            status="pending",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        session.add(order)
        session.commit()
        session.refresh(order)

        _add_log(session, order.id, "create", user_id)
        return _order_to_vo(order)


def list_my_buy(user_id: int) -> list[dict]:
    """我的买入订单。"""

    with Session(engine) as session:
        orders = session.exec(
            select(TradeOrder)
            .where(TradeOrder.buyer_id == user_id)
            .order_by(TradeOrder.created_at.desc())
        ).all()
        return [_order_to_vo(o) for o in orders]


def list_my_sell(user_id: int) -> list[dict]:
    """我的卖出订单。"""

    with Session(engine) as session:
        orders = session.exec(
            select(TradeOrder)
            .where(TradeOrder.seller_id == user_id)
            .order_by(TradeOrder.created_at.desc())
        ).all()
        return [_order_to_vo(o) for o in orders]


def cancel_order(order_id: int, user_id: int, cancel_reason: Optional[str]) -> dict:
    """取消订单。"""

    with Session(engine) as session:
        order = session.get(TradeOrder, order_id)
        if not order:
            raise ValueError("订单不存在")
        if order.buyer_id != user_id:
            raise ValueError("无权操作")
        if order.status not in ("pending",):
            raise ValueError("当前状态不可取消")
        order.status = "cancelled"
        order.cancel_reason = cancel_reason or ""
        order.updated_at = datetime.utcnow()
        session.add(order)
        session.commit()
        _add_log(session, order_id, "cancel", user_id)
        return _order_to_vo(order)


def complete_order(order_id: int, user_id: int) -> dict:
    """完成订单。"""

    with Session(engine) as session:
        order = session.get(TradeOrder, order_id)
        if not order:
            raise ValueError("订单不存在")
        if order.buyer_id != user_id:
            raise ValueError("无权操作")
        if order.status not in ("pending",):
            raise ValueError("当前状态不可完成")
        order.status = "completed"
        order.updated_at = datetime.utcnow()
        session.add(order)
        session.commit()
        _add_log(session, order_id, "complete", user_id)
        return _order_to_vo(order)


def _add_log(session: Session, order_id: int, action: str, operator_id: int) -> None:
    """添加订单操作日志。"""

    log = TradeOrderLog(
        order_id=order_id,
        action=action,
        operator_id=operator_id,
        created_at=datetime.utcnow(),
    )
    session.add(log)
    session.commit()


def _order_to_vo(order: TradeOrder) -> dict:
    """订单转 VO。"""

    return {
        "id": order.id,
        "itemId": order.item_id,
        "buyerId": order.buyer_id,
        "sellerId": order.seller_id,
        "tradeLocation": order.trade_location,
        "remark": order.remark,
        "status": order.status,
        "cancelReason": order.cancel_reason,
        "createdAt": order.created_at.isoformat() if order.created_at else "",
        "updatedAt": order.updated_at.isoformat() if order.updated_at else "",
    }
