from ingest.idempotency import unique_events


events = [{"source": "a", "id": "7"}, {"source": "b", "id": "7"}]
assert unique_events(events) == events
