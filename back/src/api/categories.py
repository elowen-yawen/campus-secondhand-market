"""分类路由。"""

from flask import Blueprint

from ..services import category_service
from ..utils.response import success

category_bp = Blueprint("category", __name__)


@category_bp.get("")
def list_all():
    """获取分类列表。"""

    categories = category_service.list_all_active()
    return success([{"id": c.id, "name": c.name, "isActive": c.is_active} for c in categories])
