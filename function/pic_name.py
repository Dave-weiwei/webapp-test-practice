def extract_parametrize_id(request):
    """
    從 pytest 的 request 物件中取出 parametrize 的 ID 名稱，
    若不存在則回傳測試函數名稱。
    """
    name = request.node.name
    if "[" in name and "]" in name:
        return name.split("[", 1)[1].rstrip("]")
    return name