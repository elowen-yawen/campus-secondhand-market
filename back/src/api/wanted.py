"""求购路由。"""

from flask import Blueprint, g, request

from ..services import wanted_service
from ..utils.response import success, error
from ..utils.security import login_required

wanted_bp = Blueprint("wanted", __name__)


@wanted_bp.post("")
@login_required
def create():
    """发布求购。"""

    data = request.get_json(silent=True) or {}
    data["userId"] = g.current_user_id
    try:
        return success(wanted_service.create(data))
    except Exception as e:
        return error(str(e))


@wanted_bp.get("/list")
def list_wanted():
    """求购列表。"""

    campus = request.args.get("campus")
    category_id = request.args.get("categoryId", type=int)
    status = request.args.get("status")
    return success(wanted_service.list_wanted(campus, category_id, status))


@wanted_bp.get("/<int:wanted_id>")
def get_by_id(wanted_id: int):
    """求购详情。"""

    try:
        return success(wanted_service.get_by_id(wanted_id))
    except ValueError as e:
        return error(str(e))


@wanted_bp.put("/<int:wanted_id>")
@login_required
def update_wanted(wanted_id: int):
    """更新求购。"""

    data = request.get_json(silent=True) or {}
    try:
        wanted_service.update_wanted(wanted_id, data)
        return success()
    except ValueError as e:
        return error(str(e))


@wanted_bp.delete("/<int:wanted_id>")
@login_required
def delete_by_id(wanted_id: int):
    """删除求购。"""

    wanted_service.delete_by_id(wanted_id)
    return success()


@wanted_bp.delete("/user/<int:user_id>")
@login_required
def delete_all_by_user(user_id: int):
    """删除用户全部求购。"""

    wanted_service.delete_all_by_user(user_id)
    return success()


@wanted_bp.get("/my")
@login_required
def my_wanted():
    """我的求购。"""

    user_id = g.current_user_id
    return success(wanted_service.my_wanted(user_id))


@wanted_bp.put("/<int:wanted_id>/close")
@login_required
def close_wanted(wanted_id: int):
    """关闭求购。"""

    user_id = g.current_user_id
    try:
        wanted_service.close_wanted(wanted_id, user_id)
        return success()
    except ValueError as e:
        return error(str(e))
