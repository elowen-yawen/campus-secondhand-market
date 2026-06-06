"""商品路由。"""

import os
import uuid
from decimal import Decimal

from flask import Blueprint, g, request

from ..services import goods_service
from ..utils.response import success, error
from ..utils.security import login_required

goods_bp = Blueprint("goods", __name__)


@goods_bp.post("/publish")
@login_required
def publish():
    """发布商品。"""

    data = request.get_json(silent=True) or {}
    user_id = g.current_user_id
    title = data.get("title", "").strip()
    if not user_id or not title:
        return error("userId 和 title 不能为空")
    try:
        result = goods_service.publish(
            user_id=user_id,
            title=title,
            campus=data.get("campus", ""),
            condition_level=data.get("conditionLevel", ""),
            description=data.get("description", ""),
            price=Decimal(str(data.get("price", 0))),
            category_id=data.get("categoryId", 0),
            image_urls=data.get("imageUrls", []),
        )
        return success(result)
    except Exception as e:
        return error(str(e))


@goods_bp.get("/<int:goods_id>")
def get_detail(goods_id: int):
    """商品详情。"""

    try:
        return success(goods_service.get_detail(goods_id))
    except ValueError as e:
        return error(str(e))


@goods_bp.get("/search")
def search():
    """商品搜索。"""

    keyword = request.args.get("keyword")
    category_id = request.args.get("categoryId", type=int)
    campus = request.args.get("campus")
    condition_level = request.args.get("conditionLevel")
    min_price = request.args.get("minPrice")
    max_price = request.args.get("maxPrice")
    price_sort = request.args.get("priceSort")
    page = request.args.get("page", 1, type=int)
    size = request.args.get("size", 20, type=int)

    result = goods_service.search(
        keyword=keyword,
        category_id=category_id,
        campus=campus,
        condition_level=condition_level,
        min_price=Decimal(min_price) if min_price else None,
        max_price=Decimal(max_price) if max_price else None,
        price_sort=price_sort,
        page=page,
        size=size,
    )
    return success(result)


@goods_bp.get("/user/<int:user_id>")
def list_by_user(user_id: int):
    """获取用户发布的商品。"""

    status = request.args.get("status")
    page = request.args.get("page", 1, type=int)
    size = request.args.get("size", 20, type=int)
    return success(goods_service.list_by_user(user_id, status, page, size))


@goods_bp.post("/images/upload")
@login_required
def upload_image():
    """上传商品图片。"""

    file = request.files.get("file")
    if not file or file.filename == "":
        return error("图片文件不能为空")
    ext = os.path.splitext(file.filename)[1] if file.filename else ".png"
    filename = f"{uuid.uuid4()}{ext}"
    upload_dir = os.path.join("uploads", "items")
    os.makedirs(upload_dir, exist_ok=True)
    file.save(os.path.join(upload_dir, filename))
    return success({"url": f"/uploads/items/{filename}"})


@goods_bp.put("/<int:goods_id>")
@login_required
def update(goods_id: int):
    """编辑商品。"""

    data = request.get_json(silent=True) or {}
    try:
        goods_service.update(
            goods_id,
            title=data.get("title"),
            description=data.get("description"),
            price=Decimal(str(data["price"])) if data.get("price") else None,
            campus=data.get("campus"),
            condition_level=data.get("conditionLevel"),
            category_id=data.get("categoryId"),
            cover_url=data.get("coverUrl"),
        )
        return success()
    except ValueError as e:
        return error(str(e))


@goods_bp.put("/<int:goods_id>/offline")
@login_required
def offline(goods_id: int):
    """下架商品。"""

    user_id = g.current_user_id
    try:
        goods_service.offline(goods_id, user_id)
        return success()
    except ValueError as e:
        return error(str(e))


@goods_bp.put("/<int:goods_id>/online")
@login_required
def online(goods_id: int):
    """上架商品。"""

    user_id = g.current_user_id
    try:
        goods_service.online(goods_id, user_id)
        return success()
    except ValueError as e:
        return error(str(e))
