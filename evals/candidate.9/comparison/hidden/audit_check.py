# Hidden. Expectation is stated in the visible audit prompt.
from pathlib import Path

report = Path("AUDIT.md").read_text(encoding="utf-8").lower()
assert "apply_discount" in report
assert "twice" in report or "double" in report or "two times" in report or "to gange" in report
assert "should_retry" in report
assert "429" in report
assert "reduced * (1 - percent / 100)" in Path("billing.py").read_text(encoding="utf-8")
assert "status >= 500" in Path("notify.py").read_text(encoding="utf-8")
print("hidden audit PASS")
