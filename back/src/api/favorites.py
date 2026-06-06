"""收藏路由。"""

from flask import Blueprint, g, request

from ..services import favorite_service
from ..utils.response import success, error
from ..utils.security import login_required

favorite_bp = Blueprint("favorite", __name__)


@favorite_bp.post("/<int:item_id>")
@login_required
def add_favorite(item_id: int):
    """收藏商品。"""

    user_id = g.current_user_id
    favorite_service.add_favorite(item_id, user_id)
    return success()


@favorite_bp.delete("/<int:item_id>")
@login_required
def cancel_favorite(item_id: int):
    """取消收藏商品。"""

    user_id = g.current_user_id
    favorite_service.cancel_favorite(item_id, user_id)
    return success()


@favorite_bp.post("/wanted/<int:wanted_id>")
@login_required
def add_wanted_favorite(wanted_id: int):
    """收藏求购。"""

    user_id = g.current_user_id
    favorite_service.add_wanted_favorite(wanted_id, user_id)
    return success()


@favorite_bp.delete("/wanted/<int:wanted_id>")
@login_required
def cancel_wanted_favorite(wanted_id: int):
    """取消收藏求购。"""

    user_id = g.current_user_id
    favorite_service.cancel_wanted_favorite(wanted_id, user_id)
    return success()


@favorite_bp.get("")
@login_required
def list_my_favorites():
    """我的收藏列表。"""

    user_id = g.current_user_id
    return success(favorite_service.list_my_favorites(user_id))
