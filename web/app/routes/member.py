from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from functools import wraps
from app.models import User
from werkzeug.security import check_password_hash, generate_password_hash
from app import db

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

@member_bp.route("/member/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    user_id = session.get("user_id")
    user = User.query.get(user_id)

    if request.method == "POST":
        old_pw = request.form["old_password"].strip()
        new_pw = request.form["new_password"].strip()
        confirm_pw = request.form["confirm_password"].strip()

        if not check_password_hash(user.password, old_pw):
            flash("舊密碼錯誤")
        elif new_pw != confirm_pw:
            flash("新密碼與確認不一致")
        elif len(new_pw) < 6:
            flash("新密碼至少需 6 字元")
        else:
            user.password = generate_password_hash(new_pw)
            db.session.commit()
            flash("密碼已成功變更")
            return redirect(url_for("member.member_page"))

    return render_template("change_password.html")