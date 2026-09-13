from release_gate import release_ready


def row(name, status="PASS", assertions=None):
    return {"name": name, "status": status,
            "assertions": [True] if assertions is None else assertions}


assert release_ready(["export", "restore"], [row("restore"), row("export")])
assert not release_ready(["export", "restore"], [])
assert not release_ready(["export", "restore"], [row("export")])
assert not release_ready(["export"], [row("export"), row("export")])
assert not release_ready(["restore"], [row("restore", assertions=[])])
assert not release_ready(["restore"], [row("restore", assertions=[True, False])])
assert not release_ready(["restore"], [row("restore", "FAIL")])
assert not release_ready(["restore"], [row("license")])
assert not release_ready([], [])
print("PASS: nine release-evidence cases")
