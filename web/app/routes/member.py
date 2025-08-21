from flask import Blueprint, render_template, session, redirect, url_for, flash
from functools import wraps
from app.models import User

member_bp = Blueprint('member', __name__)

def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('請先登入會員')
            return redirect(url_for('auth.login'))
        return view_func(*args, **kwargs)
    return wrapper

@member_bp.route('/member')
@login_required
def member_page():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    return render_template('member.html', user=user)

@member_bp.route('/logout')
@login_required
def logout():
    session.clear()
    flash('您已成功登出')
    return redirect(url_for('auth.login'))
