from analytics.events import summarize


events = [
    {"name": "b", "metadata": {"source": "first"}},
    {"name": "a", "metadata": None},
    {"name": "b", "metadata": {"source": "later"}},
]
before = repr(events)
assert summarize(events) == [
    {"name": "b", "count": 2, "metadata": {"source": "first"}},
    {"name": "a", "count": 1, "metadata": None},
]
assert repr(events) == before
print("PASS")
