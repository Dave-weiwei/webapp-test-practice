from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app import db
from app.utils.validators import is_valid_username, is_valid_password
import jwt
import datetime
from flask import current_app

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # ✅ 支援兩種輸入格式
        if request.is_json:
            data = request.get_json()
            username = data.get('username', '').strip()
            email = data.get('email', '').strip()
            password = data.get('password', '').strip()
            confirm = data.get('confirm', '').strip()
            ajax_mode = True
        else:
            username = request.form['username'].strip()
            email = request.form['email'].strip()
            password = request.form['password'].strip()
            confirm = request.form['confirm'].strip()
            ajax_mode = False

        # ✅ 驗證邏輯
        if not username or not email or not password:
            msg = '欄位不得為空'
        elif not is_valid_username(username):
            msg = '使用者名稱需為 4-20 字元，僅可包含英文字母、數字與底線'
        elif password != confirm:
            msg = '密碼與確認不符'
        elif not is_valid_password(password):
            msg = '密碼需至少 8 字元，含數字與特殊符號'
        elif User.query.filter((User.username == username) | (User.email == email)).first():
            msg = '使用者名稱或 Email 已存在'
        else:
            hashed_pw = generate_password_hash(password)
            new_user = User(username=username, email=email, password=hashed_pw)
            db.session.add(new_user)
            db.session.commit()
            if ajax_mode:
                return jsonify({"success": True, "message": "註冊成功"})
            flash('註冊成功，請登入')
            return redirect(url_for('auth.login'))

        # ❌ 錯誤處理
        if ajax_mode:
            return jsonify({"success": False, "message": msg})
        else:
            flash(msg)

    return render_template('register.html')

@auth_bp.route("/api/register", methods=["POST"])
def api_register():
    data = request.get_json()
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()
    confirm = data.get('confirm', '').strip()

    if not username or not email or not password:
        return jsonify({"success": False, "message": "欄位不得為空"}), 400
    if not is_valid_username(username):
        return jsonify({"success": False, "message": "使用者名稱格式錯誤"}), 400
    if password != confirm:
        return jsonify({"success": False, "message": "密碼與確認不一致"}), 400
    if not is_valid_password(password):
        return jsonify({"success": False, "message": "密碼格式不符"}), 400
    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"success": False, "message": "使用者名稱或 Email 已存在"}), 409

    hashed_pw = generate_password_hash(password)
    new_user = User(username=username, email=email, password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"success": True, "message": "註冊成功"}), 201



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

@auth_bp.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"success": False, "message": "帳號或密碼錯誤"}), 401

    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, current_app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify({
        "success": True,
        "token": token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_admin": user.is_admin
        }
    })