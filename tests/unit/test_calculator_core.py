from web.app.utils.calculator_core import evaluate_expression
from src.json_use import load_test_data
import pytest

test_data = load_test_data("test_calculator_core.json","test_cases")
params = [pytest.param(d["expr"], d["expect"], id=d["id"]) for d in test_data]
@pytest.mark.parametrize("expr, expect", params)

def test_calculator_core(expr, expect):
    if isinstance(expect, (int, float)):
        # ✅ 數值比對使用 pytest.approx() 處理浮點誤差
        assert evaluate_expression(expr) == pytest.approx(expect)
    elif isinstance(expect, str):
        # ✅ 字串代表預期拋出錯誤，且訊息包含該文字
        with pytest.raises(Exception) as e:
            evaluate_expression(expr)
        assert expect in str(e.value)
