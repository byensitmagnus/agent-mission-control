import subprocess
import sys


failures = []
for path in ("cache/test_invalidation.py", "ingest/test_idempotency.py"):
    result = subprocess.run([sys.executable, path], capture_output=True, text=True)
    if result.returncode:
        failures.append(path)
if failures:
    raise SystemExit("FAIL: " + ", ".join(failures))
print("PASS")
