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

    # 注册 API 路由
    from .api.auth import user_bp
    from .api.goods import goods_bp
    from .api.categories import category_bp
    from .api.favorites import favorite_bp
    from .api.wanted import wanted_bp
    from .api.orders import order_bp
    from .api.reviews import review_bp
    from .api.chat import chat_bp

    app.register_blueprint(user_bp, url_prefix="/api/user")
    app.register_blueprint(goods_bp, url_prefix="/api/items")
    app.register_blueprint(category_bp, url_prefix="/api/categories")
    app.register_blueprint(favorite_bp, url_prefix="/api/favorites")
    app.register_blueprint(wanted_bp, url_prefix="/api/wanted")
    app.register_blueprint(order_bp, url_prefix="/api/orders")
    app.register_blueprint(review_bp, url_prefix="/api/reviews")
    app.register_blueprint(chat_bp, url_prefix="/api/chat")

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
