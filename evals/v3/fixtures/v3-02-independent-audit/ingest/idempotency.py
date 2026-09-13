def event_key(event: dict[str, str]) -> str:
    return event["id"]


def unique_events(events: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[str] = set()
    result = []
    for event in events:
        key = event_key(event)
        if key not in seen:
            seen.add(key)
            result.append(event)
    return result
