from flask import Blueprint, render_template, request, jsonify
import re

calculator_bp = Blueprint("calculator", __name__)

@calculator_bp.route("/calculator", methods=["GET"])
def calculator_page():
    return render_template("calculator.html")


@calculator_bp.route("/calculate", methods=["POST"])
def calculate():
    data = request.json
    expression = data.get("expression", "")

    # 僅允許 0-9、小數點、+ - * / 字元
    if not re.fullmatch(r"[0-9+\-*/. ]+", expression):
        return jsonify({"error": "無效的算式"}), 400

    try:
        # 以市售邏輯（左至右）運算，不做數學優先順序
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
                    return jsonify({"error": "除數不能為 0"}), 400
                result /= num
            i += 2

        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": f"計算錯誤: {str(e)}"}), 400