from web.app.utils.calculator_core import evaluate_expression

def test_basic_addition():
    assert evaluate_expression("2+3") == 5