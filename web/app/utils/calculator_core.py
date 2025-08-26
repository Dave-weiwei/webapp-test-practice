import re

# 練習用上下限限制（你可自行調整）
MAX_RESULT = 1e10      # 計算結果上限（超過視為錯誤）
MIN_RESULT = 1e-10     # 結果若太小（絕對值小於此），自動視為 0

def evaluate_expression(expression: str) -> float:
    """
    接收左至右邏輯的算式字串，回傳 float 結果，支援 + - * /，不處理運算優先順序。
    範例： "2+3*4" → 20（而不是 14）
    """

    if not re.fullmatch(r"[0-9+\-*/. ]+", expression):
        raise ValueError("無效的字元")

    tokens = re.findall(r"\d+\.?\d*|[+\-*/]", expression)
    if not tokens:
        raise ValueError("空算式")

    result = float(tokens[0])
    i = 1
    while i < len(tokens) - 1:
        op = tokens[i]
        num = float(tokens[i + 1])

        if op == "+":
            result += num
        elif op == "-":
            result -= num
        elif op == "*":
            result *= num
        elif op == "/":
            if num == 0:
                raise ZeroDivisionError("除以零")
            result /= num
        else:
            raise ValueError("不支援的運算符")

        # ⛔ 檢查上限
        if abs(result) > MAX_RESULT:
            raise ValueError("計算結果過大")

        # 🎯 處理極小值為 0（誤差控制）
        if abs(result) < MIN_RESULT:
            result = 0.0

        i += 2

    return result