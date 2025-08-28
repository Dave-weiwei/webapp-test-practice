from pathlib import Path
import json

def load_test_data(file_name: str, key: str):
    base_path = Path(__file__).parent.parent  # 根目錄
    json_path = base_path / "tests" / "json" / file_name
    with open(json_path, "r" , encoding="utf-8") as f:
        data = json.load(f)
    return data[key]