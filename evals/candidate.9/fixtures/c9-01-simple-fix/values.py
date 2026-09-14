def format_value(value):
    if value is None:
        return "-"
    if value is False:
        return "no"
    return str(value)
