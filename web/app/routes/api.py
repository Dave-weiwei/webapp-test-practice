# app/routes/api.py
from flask import Blueprint, jsonify, request
from app.models import Product
from app import db
from app.utils.jwt_helper import jwt_required

api_bp = Blueprint("api", __name__)

# ✅ /api/products - 回傳所有商品（JSON 格式）
@api_bp.route("/api/products", methods=["GET"])
def get_all_products():
    products = Product.query.order_by(Product.id.asc()).all()

    # 將商品列表轉為 JSON 格式
    product_list = []
    for p in products:
        product_list.append({
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "description": p.description,
            "created_at": p.created_at.strftime("%Y-%m-%d %H:%M"),
            "updated_at": p.updated_at.strftime("%Y-%m-%d %H:%M") if p.updated_at else None
        })

    return jsonify(product_list)

# ✅ /api/products/<id> - 回傳單一商品資訊（JSON 格式）
@api_bp.route("/api/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "商品不存在"}), 404

    return jsonify({
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "description": product.description,
        "created_at": product.created_at.strftime("%Y-%m-%d %H:%M"),
        "updated_at": product.updated_at.strftime("%Y-%m-%d %H:%M") if product.updated_at else None
    })

# 新增商品api
@api_bp.route("/api/product/add", methods=["POST"])
@jwt_required(admin_only=True)
def api_add_product(current_user):
    data = request.get_json()
    name = data.get("name", "").strip()
    price = data.get("price", None)
    description = data.get("description", "").strip()

    if not name:
        return jsonify({"success": False, "message": "商品名稱為必填"}), 400

    try:
        price = float(price)
        if price <= 0:
            return jsonify({"success": False, "message": "價格必須為正數"}), 400
    except (TypeError, ValueError):
        return jsonify({"success": False, "message": "價格格式錯誤"}), 400

    new_product = Product(name=name, price=price, description=description)
    db.session.add(new_product)
    db.session.commit()

    return jsonify({"success": True, "message": "商品新增成功", "product_id": new_product.id}), 201

# 編輯商品api
@api_bp.route("/api/product/edit/<int:product_id>", methods=["PUT"])
@jwt_required(admin_only=True)
def api_edit_product(current_user, product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"success": False, "message": "商品不存在"}), 404

    data = request.get_json()
    name = data.get("name", "").strip()
    price = data.get("price", None)
    description = data.get("description", "").strip()

    if not name:
        return jsonify({"success": False, "message": "商品名稱為必填"}), 400

    try:
        price = float(price)
        if price <= 0:
            return jsonify({"success": False, "message": "價格必須為正數"}), 400
    except (TypeError, ValueError):
        return jsonify({"success": False, "message": "價格格式錯誤"}), 400

    # 更新資料
    product.name = name
    product.price = price
    product.description = description
    product.updated_at = datetime.utcnow()
    db.session.commit()

    return jsonify({"success": True, "message": "商品已更新", "product_id": product.id}), 200

# 刪除商品api
@api_bp.route("/api/product/delete/<int:product_id>", methods=["DELETE"])
@jwt_required(admin_only=True)
def api_delete_product(current_user, product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"success": False, "message": "商品不存在"}), 404

    db.session.delete(product)
    db.session.commit()

    return jsonify({"success": True, "message": f"商品 {product.name} 已刪除"}), 200