from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Product

product_bp = Blueprint("product", __name__)

@product_bp.route("/products")
def product_list():
    products = Product.query.order_by(Product.id.asc()).all()
    return render_template("products.html", products=products)

@product_bp.route("/products/add", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        price = request.form.get("price", "").strip()
        description = request.form.get("description", "").strip()

        # 基本驗證
        if not name or not price:
            flash("名稱與價格為必填欄位")
        else:
            try:
                price_value = float(price)
                if price_value <= 0:
                    flash("價格必須大於 0")
                else:
                    new_product = Product(name=name, price=price_value, description=description)
                    db.session.add(new_product)
                    db.session.commit()
                    flash("商品新增成功")
                    return redirect(url_for("product.product_list"))
            except ValueError:
                flash("價格格式不正確")

    return render_template("product_add.html")