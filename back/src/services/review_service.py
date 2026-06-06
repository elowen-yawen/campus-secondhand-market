"""评价服务。"""

from datetime import datetime
from typing import Optional

from sqlmodel import Session, select, func

from ..db import engine
from ..models import Review


def create(user_id: int, order_id: int, reviewee_id: int, rating: int, content: str) -> dict:
    """创建评价。"""

    with Session(engine) as session:
        existing = session.exec(
            select(Review).where(Review.order_id == order_id, Review.reviewer_id == user_id)
        ).first()
        if existing:
            raise ValueError("已评价过此订单")
        review = Review(
            order_id=order_id,
            reviewer_id=user_id,
            reviewee_id=reviewee_id,
            rating=rating,
            content=content or "",
            created_at=datetime.utcnow(),
        )
        session.add(review)
        session.commit()
        session.refresh(review)
        return _review_to_vo(review)


def update(review_id: int, user_id: int, rating: int, content: str) -> dict:
    """更新评价。"""

    with Session(engine) as session:
        review = session.get(Review, review_id)
        if not review:
            raise ValueError("评价不存在")
        if review.reviewer_id != user_id:
            raise ValueError("无权操作")
        review.rating = rating
        review.content = content or ""
        session.add(review)
        session.commit()
        return _review_to_vo(review)


def delete(review_id: int, user_id: int) -> None:
    """删除评价。"""

    with Session(engine) as session:
        review = session.get(Review, review_id)
        if not review:
            raise ValueError("评价不存在")
        if review.reviewer_id != user_id:
            raise ValueError("无权操作")
        session.delete(review)
        session.commit()


def get_user_reviews(user_id: int) -> list[dict]:
    """获取用户的评价列表。"""

    with Session(engine) as session:
        reviews = session.exec(
            select(Review)
            .where(Review.reviewee_id == user_id)
            .order_by(Review.created_at.desc())
        ).all()
        return [_review_to_vo(r) for r in reviews]


def get_average_rating(user_id: int) -> float:
    """获取用户平均评分。"""

    with Session(engine) as session:
        result = session.exec(
            select(func.avg(Review.rating)).where(Review.reviewee_id == user_id)
        ).one()
        return round(float(result or 0), 1)


def get_review_count(user_id: int) -> int:
    """获取用户评价数量。"""

    with Session(engine) as session:
        return session.exec(
            select(func.count()).where(Review.reviewee_id == user_id)
        ).one()


def get_my_reviews(user_id: int) -> list[dict]:
    """我的评价列表。"""

    with Session(engine) as session:
        reviews = session.exec(
            select(Review)
            .where(Review.reviewer_id == user_id)
            .order_by(Review.created_at.desc())
        ).all()
        return [_review_to_vo(r) for r in reviews]


def check_reviewed(order_id: int, user_id: int) -> bool:
    """检查是否已评价。"""

    with Session(engine) as session:
        existing = session.exec(
            select(Review).where(Review.order_id == order_id, Review.reviewer_id == user_id)
        ).first()
        return existing is not None


def _review_to_vo(review: Review) -> dict:
    """评价转 VO。"""

    return {
        "id": review.id,
        "orderId": review.order_id,
        "reviewerId": review.reviewer_id,
        "revieweeId": review.reviewee_id,
        "rating": review.rating,
        "content": review.content,
        "createdAt": review.created_at.isoformat() if review.created_at else "",
    }
