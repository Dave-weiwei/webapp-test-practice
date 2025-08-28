from web.app.utils.calculator_core import evaluate_expression
from src.json_use import load_test_data
import pytest

test_data = load_test_data("test_calculator_core.json","test_cases")
params = [pytest.param(d["expr"], d["expect"], id=d["id"]) for d in test_data]
@pytest.mark.parametrize("expr, expect", params)

def test_basic_addition(expr,expect):
    assert evaluate_expression(expr) == expect
