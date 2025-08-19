from flask import Blueprint, render_template, session, redirect, url_for, flash
from functools import wraps

member_bp = Blueprint('member', __name__)

# 登入檢查裝飾器
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
    return render_template('member.html', username=session.get('username'))

@member_bp.route('/logout')
@login_required
def logout():
    session.clear()
    flash('您已成功登出')
    return redirect(url_for('auth.login'))