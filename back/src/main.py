"""服务启动脚本。"""

from dotenv import load_dotenv
import os
from flask import Flask, jsonify
from flask import send_from_directory
from flask_cors import CORS

from .config import settings
from .db import init_db
from . import models  # noqa: F401  # 确保模型被加载


def create_app() -> Flask:
    """创建并配置 Flask 应用。"""

    app = Flask(__name__)
    CORS(app, supports_credentials=True, origins='*', methods=['GET','POST','PUT','DELETE','OPTIONS'], allow_headers=['Content-Type', 'Authorization'])
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

    # 静态文件服务（用于访问上传的图片）
    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        # 获取 back 目录的绝对路径（main.py 在 back/src/ 下，所以需要往上一级）
        back_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        uploads_dir = os.path.join(back_dir, 'uploads')
        return send_from_directory(uploads_dir, filename)
    
    @app.get("/api/health")
    def health_check():
        """健康检查。"""

        return jsonify({"code": 0, "message": "success", "data": {"status": "ok", "service": "Campus Secondhand Market API"}})

    @app.route("/")
    def index():
        """根路由。"""
        return jsonify({
            "code": 0, 
            "message": "Campus Secondhand Market API is running", 
            "data": {
                "health_check": "/api/health",
                "api_docs": "/API.md (in repository)"
            }
        })

    return app


if __name__ == "__main__":
    # 统一在启动脚本完成初始化
    load_dotenv()
    app = create_app()
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=settings.flask_debug == "1")
