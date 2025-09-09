from functools import wraps
from flask import request, jsonify
import jwt
from app.models import User
from flask import current_app

def jwt_required(admin_only=False):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith("Bearer "):
                return jsonify({"success": False, "message": "未提供有效授權"}), 401

            token = auth_header.split(" ")[1]
            try:
                payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
                user_id = payload.get("user_id")
                user = User.query.get(user_id)
                if not user:
                    return jsonify({"success": False, "message": "無效使用者"}), 401
                if admin_only and not user.is_admin:
                    return jsonify({"success": False, "message": "非管理員無權操作"}), 403
            except jwt.ExpiredSignatureError:
                return jsonify({"success": False, "message": "Token 已過期"}), 401
            except jwt.InvalidTokenError:
                return jsonify({"success": False, "message": "無效的 Token"}), 401

            # 傳遞 user 給 view function
            return view_func(user, *args, **kwargs)
        return wrapper
    return decorator