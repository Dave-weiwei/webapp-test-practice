from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from functools import wraps
from app.models import User, Product
from app import db
from datetime import datetime

admin_bp = Blueprint("admin", __name__)

# 管理員權限驗證裝飾器
def admin_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        user_id = session.get("user_id")
        if not user_id:
            flash("請先登入")
            return redirect(url_for("auth.login"))

        user = User.query.get(user_id)
        if not user or not user.is_admin:
            flash("此功能僅限管理員")
            return redirect(url_for("member.member_page"))

        return view_func(*args, **kwargs)
    return wrapper

# 管理後台首頁
@admin_bp.route("/admin")
@admin_required
def admin_dashboard():
    user = User.query.get(session.get("user_id"))
    products = Product.query.order_by(Product.id.asc()).all()
    return render_template("admin.html", user=user, products=products)

# 刪除商品
@admin_bp.route("/admin/delete/<int:product_id>", methods=["POST"])
@admin_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash("商品已刪除")
    return redirect(url_for("admin.admin_dashboard"))

# 顯示所有會員（管理用）
@admin_bp.route("/admin/users")
@admin_required
def user_management():
    current_admin_id = session.get("user_id")
    users = User.query.order_by(User.id.asc()).all()
    return render_template("admin_users.html", users=users, current_admin_id=current_admin_id)

# 刪除會員（禁止刪除自己）
@admin_bp.route("/admin/delete_user/<int:user_id>", methods=["POST"])
@admin_required
def delete_user(user_id):
    current_admin_id = session.get("user_id")
    if user_id == current_admin_id:
        flash("無法刪除自己")
        return redirect(url_for("admin.user_management"))

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f"已刪除會員：{user.username}")
    return redirect(url_for("admin.user_management"))

# 修改商品
@admin_bp.route("/admin/edit/<int:product_id>", methods=["GET", "POST"])
@admin_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)

    if request.method == "POST":
        name = request.form["name"].strip()
        price = request.form["price"].strip()
        description = request.form["description"].strip()

        try:
            price_value = float(price)
            if price_value <= 0:
                flash("價格必須大於 0")
            else:
                product.name = name
                product.price = price_value
                product.description = description
                product.updated_at = datetime.utcnow()  # ✅ 更新時間
                db.session.commit()
                flash("商品已更新")
                return redirect(url_for("admin.admin_dashboard"))
        except ValueError:
            flash("價格格式不正確")

    return render_template("admin_edit.html", product=product)