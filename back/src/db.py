"""数据库连接与初始化。"""

from sqlmodel import SQLModel, create_engine

from .config import settings


engine = create_engine(
    settings.database_url,
    echo=False,
    connect_args={"check_same_thread": False}
    if settings.database_url.startswith("sqlite")
    else {},
)


def init_db() -> None:
    """初始化数据库结构。"""

    SQLModel.metadata.create_all(engine)
