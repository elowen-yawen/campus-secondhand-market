"""订单服务。"""

from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlmodel import Session, select

from ..db import engine
from ..models import Goods, TradeOrder, TradeOrderLog, User


def create_order(item_id: int, user_id: int, trade_location: str, remark: str) -> dict:
    """创建订单（原子性事务，包含资金划转）。"""

    with Session(engine) as session:
        with session.begin():  # 开启强一致性事务，自动回滚
            # 1. 验证商品
            goods = session.get(Goods, item_id)
            if not goods:
                raise ValueError("商品不存在")
            if goods.status != "on_sale":
                raise ValueError("商品已下架或已售出")
            if goods.seller_id == user_id:
                raise ValueError("不能购买自己的商品")
            
            # 2. 获取买卖双方账户
            buyer = session.get(User, user_id)
            seller = session.get(User, goods.seller_id)
            
            # 3. 余额校验
            if buyer.balance < goods.price:
                raise ValueError("余额不足")
            
            # 4. 买家扣款
            buyer.balance -= goods.price
            
            # 5. 卖家进账
            seller.balance += goods.price
            
            # 6. 商品状态变更为已售
            goods.status = "sold"
            goods.updated_at = datetime.utcnow()
            
            # 7. 创建订单
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
            
            # 8. 添加订单日志（同一事务内）
            log = TradeOrderLog(
                order_id=order.id,
                action="create",
                operator_id=user_id,
                created_at=datetime.utcnow(),
            )
            session.add(log)
            
            # 事务结束前自动提交所有操作，任意异常则全盘回滚
        
        session.refresh(order)
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
    """取消订单（原子性事务，包含资金回滚）。"""

    with Session(engine) as session:
        with session.begin():  # 开启强一致性事务
            order = session.get(TradeOrder, order_id)
            if not order:
                raise ValueError("订单不存在")
            if order.buyer_id != user_id:
                raise ValueError("无权操作")
            if order.status not in ("pending",):
                raise ValueError("当前状态不可取消")
            
            # 获取商品和买卖双方账户
            goods = session.get(Goods, order.item_id)
            buyer = session.get(User, order.buyer_id)
            seller = session.get(User, order.seller_id)
            
            # 资金回滚：卖家扣款，买家退款
            seller.balance -= goods.price
            buyer.balance += goods.price
            
            # 商品状态恢复为在售
            goods.status = "on_sale"
            goods.updated_at = datetime.utcnow()
            
            # 更新订单状态
            order.status = "cancelled"
            order.cancel_reason = cancel_reason or ""
            order.updated_at = datetime.utcnow()
            session.add(order)
            
            # 添加订单日志
            _add_log(session, order_id, "cancel", user_id)
            
            # 事务自动提交
        
        return _order_to_vo(order)


def complete_order(order_id: int, user_id: int) -> dict:
    """完成订单（原子性事务）。"""

    with Session(engine) as session:
        with session.begin():  # 开启强一致性事务
            order = session.get(TradeOrder, order_id)
            if not order:
                raise ValueError("订单不存在")
            if order.buyer_id != user_id:
                raise ValueError("无权操作")
            if order.status not in ("pending",):
                raise ValueError("当前状态不可完成")
            
            # 获取商品
            goods = session.get(Goods, order.item_id)
            
            # 商品状态确认为已售（资金已在下单时划转，此处仅确认状态）
            goods.status = "sold"
            goods.updated_at = datetime.utcnow()
            
            # 更新订单状态
            order.status = "completed"
            order.updated_at = datetime.utcnow()
            session.add(order)
            
            # 添加订单日志
            _add_log(session, order_id, "complete", user_id)
            
            # 事务自动提交
        
        return _order_to_vo(order)


def _add_log(session: Session, order_id: int, action: str, operator_id: int) -> None:
    """添加订单操作日志（需在事务内调用）。"""

    log = TradeOrderLog(
        order_id=order_id,
        action=action,
        operator_id=operator_id,
        created_at=datetime.utcnow(),
    )
    session.add(log)
    # 注意：不再调用 session.commit()，由外层事务统一提交


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
