"""服务启动脚本。"""

from dotenv import load_dotenv
from flask import Flask, jsonify

from .config import settings
from .db import init_db
from . import models  # noqa: F401  # 确保模型被加载


def create_app() -> Flask:
    """创建并配置 Flask 应用。"""

    app = Flask(__name__)
    app.config["SECRET_KEY"] = settings.secret_key

    @app.get("/api/health")
    def health_check():
        """健康检查。"""

        return jsonify({"code": 0, "message": "success", "data": {"status": "ok"}})

    return app


if __name__ == "__main__":
    # 统一在启动脚本完成初始化
    load_dotenv()
    app = create_app()
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=settings.flask_debug == "1")
