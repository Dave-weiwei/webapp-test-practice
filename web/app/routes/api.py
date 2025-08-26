# app/routes/api.py
from flask import Blueprint, jsonify
from app.models import Product

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
