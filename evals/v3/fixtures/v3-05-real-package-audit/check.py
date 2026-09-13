import subprocess
import sys

failed = False
for label, script in (("PACKAGE", "scripts/test_package_plugin.py"), ("FIXTURE", "scripts/test_prepare_eval.py")):
    result = subprocess.run([sys.executable, script], capture_output=True, text=True)
    print(label + "_SUITE_" + ("PASS" if result.returncode == 0 else "FAIL"))
    print(result.stdout, end="")
    print(result.stderr, end="")
    failed = failed or result.returncode != 0
raise SystemExit(int(failed))
