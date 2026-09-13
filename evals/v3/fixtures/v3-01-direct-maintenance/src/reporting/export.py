from .format import format_value


def export_row(values: list[object]) -> str:
    return ",".join(format_value(value) for value in values)
