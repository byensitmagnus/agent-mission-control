# Hidden: both planted defects must be named. Read-only.
from pathlib import Path

root = Path(__file__).resolve().parents[1] / "fixtures" / "c9-02-two-audits"
auth = (root / "auth.py").read_text(encoding="utf-8")
http = (root / "http.py").read_text(encoding="utf-8")
report = Path("AUDIT.md").read_text(encoding="utf-8").lower()
assert "wall" in report or "clock" in report
assert "429" in report
assert "timeout" in auth.lower()
assert "should_retry" in http
print("hidden c9-02 PASS")
