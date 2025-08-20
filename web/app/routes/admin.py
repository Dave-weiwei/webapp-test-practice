from flask import Blueprint, render_template, session, redirect, url_for, flash
from functools import wraps
from app.models import User, Product

admin_bp = Blueprint('admin', __name__)

# 管理員驗證裝飾器
def admin_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            flash("請先登入")
            return redirect(url_for('auth.login'))

        user = User.query.get(user_id)
        if not user or not user.is_admin:
            flash("此功能僅限管理員")
            return redirect(url_for('member.member_page'))

        return view_func(*args, **kwargs)
    return wrapper

# 管理後台首頁
@admin_bp.route('/admin')
@admin_required
def admin_dashboard():
    user = User.query.get(session['user_id'])
    products = Product.query.order_by(Product.id.asc()).all()
    return render_template('admin.html', user=user, products=products)
