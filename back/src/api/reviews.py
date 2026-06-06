"""评价路由。"""

from flask import Blueprint, g, request

from ..services import review_service
from ..utils.response import success, error
from ..utils.security import login_required

review_bp = Blueprint("review", __name__)


@review_bp.post("")
@login_required
def create():
    """创建评价。"""

    data = request.get_json(silent=True) or {}
    user_id = g.current_user_id
    order_id = data.get("orderId")
    reviewee_id = data.get("revieweeId")
    rating = data.get("rating", 5)
    if not order_id or not reviewee_id:
        return error("orderId 和 revieweeId 不能为空")
    try:
        result = review_service.create(
            user_id=user_id,
            order_id=order_id,
            reviewee_id=reviewee_id,
            rating=rating,
            content=data.get("content", ""),
        )
        return success(result)
    except ValueError as e:
        return error(str(e))


@review_bp.put("/<int:review_id>")
@login_required
def update(review_id: int):
    """更新评价。"""

    data = request.get_json(silent=True) or {}
    user_id = g.current_user_id
    try:
        result = review_service.update(
            review_id=review_id,
            user_id=user_id,
            rating=data.get("rating", 5),
            content=data.get("content", ""),
        )
        return success(result)
    except ValueError as e:
        return error(str(e))


@review_bp.delete("/<int:review_id>")
@login_required
def delete(review_id: int):
    """删除评价。"""

    user_id = g.current_user_id
    try:
        review_service.delete(review_id, user_id)
        return success()
    except ValueError as e:
        return error(str(e))


@review_bp.get("/user/<int:user_id>")
def get_user_reviews(user_id: int):
    """获取用户的评价与统计。"""

    reviews = review_service.get_user_reviews(user_id)
    avg_rating = review_service.get_average_rating(user_id)
    total_count = review_service.get_review_count(user_id)
    return success({
        "reviews": reviews,
        "avgRating": avg_rating,
        "totalCount": total_count,
    })


@review_bp.get("/my")
@login_required
def get_my_reviews():
    """我的评价列表。"""

    user_id = g.current_user_id
    return success(review_service.get_my_reviews(user_id))


@review_bp.get("/check")
def check_reviewed():
    """检查是否已评价。"""

    order_id = request.args.get("orderId", type=int)
    user_id = request.args.get("userId", type=int)
    if not order_id or not user_id:
        return error("orderId 和 userId 不能为空")
    return success(review_service.check_reviewed(order_id, user_id))
