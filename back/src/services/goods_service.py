"""商品服务。"""

from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlmodel import Session, select

from ..db import engine
from ..models import Goods, GoodsImage
from ..utils.pagination import paginate


def publish(
    user_id: int,
    title: str,
    campus: str,
    condition_level: str,
    description: str,
    price: Decimal,
    category_id: int,
    image_urls: list[str],
) -> dict:
    """发布商品。"""

    with Session(engine) as session:
        goods = Goods(
            title=title,
            description=description or "",
            price=price,
            seller_id=user_id,
            category_id=category_id,
            campus=campus or "",
            condition_level=condition_level or "",
            cover_url=image_urls[0] if image_urls else "",
            status="on_sale",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        session.add(goods)
        session.commit()
        session.refresh(goods)

        for url in image_urls:
            img = GoodsImage(goods_id=goods.id, image_url=url)
            session.add(img)
        session.commit()

        return _goods_to_detail(goods, image_urls)


def get_detail(goods_id: int) -> dict:
    """获取商品详情。"""

    with Session(engine) as session:
        goods = session.get(Goods, goods_id)
        if not goods:
            raise ValueError("商品不存在")
        images = session.exec(
            select(GoodsImage).where(GoodsImage.goods_id == goods_id)
        ).all()
        image_urls = [img.image_url for img in images]
        return _goods_to_detail(goods, image_urls)


def search(
    keyword: Optional[str],
    category_id: Optional[int],
    campus: Optional[str],
    condition_level: Optional[str],
    min_price: Optional[Decimal],
    max_price: Optional[Decimal],
    price_sort: Optional[str],
    page: int,
    size: int,
) -> dict:
    """搜索商品。"""

    with Session(engine) as session:
        stmt = select(Goods).where(Goods.status == "on_sale")
        if keyword:
            stmt = stmt.where(Goods.title.contains(keyword))
        if category_id:
            stmt = stmt.where(Goods.category_id == category_id)
        if campus:
            stmt = stmt.where(Goods.campus == campus)
        if condition_level:
            stmt = stmt.where(Goods.condition_level == condition_level)
        if min_price is not None:
            stmt = stmt.where(Goods.price >= min_price)
        if max_price is not None:
            stmt = stmt.where(Goods.price <= max_price)
        if price_sort == "asc":
            stmt = stmt.order_by(Goods.price.asc())
        elif price_sort == "desc":
            stmt = stmt.order_by(Goods.price.desc())
        else:
            stmt = stmt.order_by(Goods.created_at.desc())

        items = list(session.exec(stmt).all())
        cards = [_goods_to_card(g) for g in items]
        return paginate(cards, page, size)


def list_by_user(user_id: int, status: Optional[str], page: int, size: int) -> dict:
    """获取用户发布的商品。"""

    with Session(engine) as session:
        stmt = select(Goods).where(Goods.seller_id == user_id)
        if status:
            stmt = stmt.where(Goods.status == status)
        stmt = stmt.order_by(Goods.created_at.desc())
        items = list(session.exec(stmt).all())
        cards = [_goods_to_card(g) for g in items]
        return paginate(cards, page, size)


def update(goods_id: int, **kwargs) -> None:
    """更新商品。"""

    with Session(engine) as session:
        goods = session.get(Goods, goods_id)
        if not goods:
            raise ValueError("商品不存在")
        for key, value in kwargs.items():
            if value is not None and hasattr(goods, key):
                setattr(goods, key, value)
        goods.updated_at = datetime.utcnow()
        session.add(goods)
        session.commit()


def offline(goods_id: int, user_id: int) -> None:
    """下架商品。"""

    with Session(engine) as session:
        goods = session.get(Goods, goods_id)
        if not goods:
            raise ValueError("商品不存在")
        if goods.seller_id != user_id:
            raise ValueError("无权操作")
        goods.status = "offline"
        session.add(goods)
        session.commit()


def online(goods_id: int, user_id: int) -> None:
    """上架商品。"""

    with Session(engine) as session:
        goods = session.get(Goods, goods_id)
        if not goods:
            raise ValueError("商品不存在")
        if goods.seller_id != user_id:
            raise ValueError("无权操作")
        goods.status = "on_sale"
        session.add(goods)
        session.commit()


def _goods_to_card(goods: Goods) -> dict:
    """商品转卡片视图。"""

    return {
        "id": goods.id,
        "title": goods.title,
        "price": str(goods.price),
        "coverUrl": goods.cover_url,
        "campus": goods.campus,
        "status": goods.status,
        "sellerId": goods.seller_id,
        "createdAt": goods.created_at.isoformat() if goods.created_at else "",
    }


def _goods_to_detail(goods: Goods, image_urls: list[str]) -> dict:
    """商品转详情视图。"""

    return {
        "id": goods.id,
        "title": goods.title,
        "description": goods.description,
        "price": str(goods.price),
        "coverUrl": goods.cover_url,
        "imageUrls": image_urls,
        "sellerId": goods.seller_id,
        "categoryId": goods.category_id,
        "campus": goods.campus,
        "conditionLevel": goods.condition_level,
        "status": goods.status,
        "createdAt": goods.created_at.isoformat() if goods.created_at else "",
        "updatedAt": goods.updated_at.isoformat() if goods.updated_at else "",
    }
