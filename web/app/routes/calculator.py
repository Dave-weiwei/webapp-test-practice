from flask import Blueprint, render_template, request, jsonify
from app.utils.calculator_core import evaluate_expression

calculator_bp = Blueprint("calculator", __name__)

@calculator_bp.route("/calculator", methods=["GET"])
def calculator_page():
    return render_template("calculator.html")


@calculator_bp.route("/calculate", methods=["POST"])
def calculate():
    data = request.json
    expression = data.get("expression", "")

    try:
        result = evaluate_expression(expression)
        return jsonify({"result": result})
    except ZeroDivisionError:
        return jsonify({"error": "除數不能為 0"}), 400
    except Exception as e:
        return jsonify({"error": f"計算錯誤: {str(e)}"}), 400