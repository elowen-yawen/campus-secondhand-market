"""分类服务。"""

from sqlmodel import Session, select

from ..db import engine
from ..models import Category


def list_all_active() -> list[Category]:
    """获取所有活跃分类。"""

    with Session(engine) as session:
        return list(session.exec(select(Category).where(Category.is_active == True)).all())
