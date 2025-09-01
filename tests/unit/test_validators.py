from web.app.utils.validators import is_valid_username,is_valid_password
from src.json_use import load_test_data
import pytest

username_data = load_test_data("test_validators.json","username_cases")
username_params = [pytest.param(d["input"], d["valid"], id=d["id"]) for d in username_data]
@pytest.mark.parametrize("input, valid", username_params)

def test_username(input,valid):
    assert is_valid_username(input) == valid
    
password_data = load_test_data("test_validators.json","password_cases")
password_params = [pytest.param(d["input"], d["valid"], id=d["id"]) for d in password_data]
@pytest.mark.parametrize("input, valid", password_params)

def test_password(input,valid):
    assert is_valid_password(input) == valid