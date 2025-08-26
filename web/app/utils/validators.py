import re

# ✅ 帳號格式：英數底線，開頭為英文，長度 4~20
username_pattern = r'^[a-zA-Z][a-zA-Z0-9_]{3,19}$'

# ✅ 密碼格式：至少 8 字元，含數字與特殊符號
password_pattern = r'^(?=.*[a-zA-Z])(?=.*\d)(?=.*[\W_]).{8,}$'

def is_valid_username(username: str) -> bool:
    return re.fullmatch(username_pattern, username) is not None

def is_valid_password(password: str) -> bool:
    return re.fullmatch(password_pattern, password) is not None