from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password'].strip()
        confirm = request.form['confirm'].strip()

        if not username or not email or not password:
            flash('欄位不得為空')
        elif password != confirm:
            flash('密碼與確認不符')
        elif User.query.filter((User.username == username) | (User.email == email)).first():
            flash('使用者名稱或 Email 已存在')
        else:
            hashed_pw = generate_password_hash(password)
            new_user = User(username=username, email=email, password=hashed_pw)
            db.session.add(new_user)
            db.session.commit()
            flash('註冊成功，請登入')
            return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            flash('帳號或密碼錯誤')
        else:
            session['user_id'] = user.id
            session['username'] = user.username
            flash('登入成功')
            return redirect(url_for('member.member_page'))

    return render_template('login.html')