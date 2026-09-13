from inventory.importer import import_ids


assert import_ids([{"id": 0}, {"id": "2"}]) == [0, 2]
try:
    import_ids([{"id": 1}, {"id": "1"}])
except ValueError:
    pass
else:
    raise AssertionError("duplicate id accepted")
print("PASS")
