def summarize(events: list[dict[str, object]]) -> list[dict[str, object]]:
    result = []
    for event in events:
        name = event["name"]
        if any(row["name"] == name for row in result):
            for row in result:
                if row["name"] == name:
                    row["count"] += 1
                    break
        else:
            result.append({"name": name, "count": 1, "metadata": event.get("metadata")})
    return result
