from .normalize import normalize_id


def import_ids(rows: list[dict[str, object]]) -> list[int]:
    values = [normalize_id(row.get("id")) for row in rows]
    if any(value is None for value in values):
        raise ValueError("invalid inventory id")
    ids = [value for value in values if value is not None]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate inventory id")
    return ids
