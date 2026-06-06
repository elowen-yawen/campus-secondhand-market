"""配置加载模块。"""

import os


class Settings:
    """应用配置。"""

    def __init__(self) -> None:
        self.database_url = os.getenv("DATABASE_URL", "sqlite:///./data.db")
        self.secret_key = os.getenv("SECRET_KEY", "dev-secret")
        self.flask_env = os.getenv("FLASK_ENV", "development")
        self.flask_debug = os.getenv("FLASK_DEBUG", "1")


settings = Settings()
