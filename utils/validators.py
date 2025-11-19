def validate_expense(data):
    if not data:
        return "no data provided"
    required = ["date","amount","category"]
    for f in required:
        if f not in data or data[f] in (None, ""):
            return f"{f} is required"
    return None
