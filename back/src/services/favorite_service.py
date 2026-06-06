"""收藏服务。"""

from datetime import datetime
from typing import Optional

from sqlmodel import Session, select

from ..db import engine
from ..models import Favorite, Goods, Wanted


def add_favorite(item_id: int, user_id: int) -> None:
    """收藏商品。"""

    with Session(engine) as session:
        existing = session.exec(
            select(Favorite).where(
                Favorite.user_id == user_id,
                Favorite.item_id == item_id,
            )
        ).first()
        if existing:
            return
        fav = Favorite(user_id=user_id, item_id=item_id, created_at=datetime.utcnow())
        session.add(fav)
        session.commit()


def cancel_favorite(item_id: int, user_id: int) -> None:
    """取消收藏商品。"""

    with Session(engine) as session:
        fav = session.exec(
            select(Favorite).where(
                Favorite.user_id == user_id,
                Favorite.item_id == item_id,
            )
        ).first()
        if fav:
            session.delete(fav)
            session.commit()


def add_wanted_favorite(wanted_id: int, user_id: int) -> None:
    """收藏求购。"""

    with Session(engine) as session:
        existing = session.exec(
            select(Favorite).where(
                Favorite.user_id == user_id,
                Favorite.wanted_id == wanted_id,
            )
        ).first()
        if existing:
            return
        fav = Favorite(user_id=user_id, wanted_id=wanted_id, created_at=datetime.utcnow())
        session.add(fav)
        session.commit()


def cancel_wanted_favorite(wanted_id: int, user_id: int) -> None:
    """取消收藏求购。"""

    with Session(engine) as session:
        fav = session.exec(
            select(Favorite).where(
                Favorite.user_id == user_id,
                Favorite.wanted_id == wanted_id,
            )
        ).first()
        if fav:
            session.delete(fav)
            session.commit()


def list_my_favorites(user_id: int) -> list[dict]:
    """我的收藏列表。"""

    with Session(engine) as session:
        favs = session.exec(
            select(Favorite).where(Favorite.user_id == user_id)
        ).all()
        result = []
        for fav in favs:
            item = {"id": fav.id, "createdAt": fav.created_at.isoformat() if fav.created_at else ""}
            if fav.item_id:
                goods = session.get(Goods, fav.item_id)
                if goods:
                    item["item"] = {
                        "id": goods.id,
                        "title": goods.title,
                        "price": str(goods.price),
                        "coverUrl": goods.cover_url,
                        "status": goods.status,
                    }
            if fav.wanted_id:
                wanted = session.get(Wanted, fav.wanted_id)
                if wanted:
                    item["wanted"] = {
                        "id": wanted.id,
                        "title": wanted.title,
                        "budgetMin": str(wanted.budget_min),
                        "budgetMax": str(wanted.budget_max),
                        "status": wanted.status,
                    }
            result.append(item)
        return result
