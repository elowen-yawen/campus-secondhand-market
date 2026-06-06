"""通用响应结构。"""

from flask import jsonify
from typing import Any, Tuple


def success(data: Any = None) -> Tuple:
    """成功响应。"""

    return jsonify({"code": 0, "message": "success", "data": data}), 200


def error(message: str, code: int = 1, status_code: int = 400) -> Tuple:
    """错误响应。"""

    return jsonify({"code": code, "message": message, "data": None}), status_code
