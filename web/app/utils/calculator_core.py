import re

# 計算結果限制
MAX_RESULT = 1e10      # 超過此值視為錯誤
MIN_RESULT = 1e-10     # 絕對值小於此視為 0

def evaluate_expression(expression: str) -> float:
    """
    接收標準運算式字串，回傳正確的 float 結果。
    支援加減乘除與括號，依照 Python 標準運算優先順序。
    """

    # 僅允許數字、小數點、運算符號與括號
    if not re.fullmatch(r"[0-9+\-*/(). ]+", expression):
        raise ValueError("無效的字元")

    try:
        # 安全計算：禁用所有 builtins，避免執行非預期語法
        result = eval(expression, {"__builtins__": None}, {})
    except ZeroDivisionError:
        raise ZeroDivisionError("除以零")
    except Exception:
        raise ValueError("無法計算的表達式")

    # 上限控制
    if abs(result) > MAX_RESULT:
        raise ValueError("計算結果過大")

    # 極小值視為 0
    if abs(result) < MIN_RESULT:
        result = 0.0

    return float(result)