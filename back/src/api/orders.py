"""订单路由。"""

from flask import Blueprint, g, request

from ..services import order_service
from ..utils.response import success, error
from ..utils.security import login_required

order_bp = Blueprint("order", __name__)


@order_bp.post("")
@login_required
def create_order():
    """创建订单。"""

    data = request.get_json(silent=True) or {}
    user_id = g.current_user_id
    item_id = data.get("itemId")
    if not item_id:
        return error("itemId 不能为空")
    try:
        result = order_service.create_order(
            item_id=item_id,
            user_id=user_id,
            trade_location=data.get("tradeLocation", ""),
            remark=data.get("remark", ""),
        )
        return success(result)
    except ValueError as e:
        return error(str(e))


@order_bp.get("/my-buy")
@login_required
def list_my_buy():
    """我的买入订单。"""

    user_id = g.current_user_id
    return success(order_service.list_my_buy(user_id))


@order_bp.get("/my-sell")
@login_required
def list_my_sell():
    """我的卖出订单。"""

    user_id = g.current_user_id
    return success(order_service.list_my_sell(user_id))


@order_bp.put("/<int:order_id>/cancel")
@login_required
def cancel_order(order_id: int):
    """取消订单。"""

    user_id = g.current_user_id
    data = request.get_json(silent=True) or {}
    try:
        result = order_service.cancel_order(order_id, user_id, data.get("cancelReason"))
        return success(result)
    except ValueError as e:
        return error(str(e))


@order_bp.put("/<int:order_id>/complete")
@login_required
def complete_order(order_id: int):
    """完成订单。"""

    user_id = g.current_user_id
    try:
        result = order_service.complete_order(order_id, user_id)
        return success(result)
    except ValueError as e:
        return error(str(e))
