# Example: FPS Booster release

This is an illustrative end-to-end mission. The values below are sample evidence, not a measured run of FPS Booster.

```text
$agent-mission-control

Prepare the FPS Booster application for release. The optimizer core, dashboard,
and Windows installer changed. Improve p99 frametime without increasing crashes,
preserve every supported profile and setting during upgrade, and stop before
deploy.
```

Mission stages:

1. Freeze the hardware/workload baseline, supported profiles, crash guard, and rollback gates.
2. Fix interfaces, then give optimizer, dashboard, and installer to separate native subagents.
3. Run a candidate loop only for measured optimizer changes; keep the evaluator fixed.
4. Independently review runtime, migration, rollback, and rendered UI evidence.
5. Lead verification returns `PASS`, `FAIL`, `BLOCKED` or `NOT VERIFIED`; repair failed gates and rerun affected checks before stopping at deploy.
Propose skill learning only after the release run is verified.

Illustrative mission record:

```text
MISSION: fps-booster-release
STATUS: NOT VERIFIED
SCOPE: optimizer, dashboard, installer
GATES: p99 baseline; crash rate; profile preservation; migration; rollback; rendered UI
EVIDENCE: baseline=sample; candidate=sample; migration=sample; rollback=sample; UI=sample
DECISION: NOT VERIFIED — sample evidence is not a measured release result
```

Replace each sample with fresh, reproducible evidence from the target application before calling the mission `PASS`. If the delivered artifact is the installer, the accept check runs on that installer. A source-only check leaves it NOT VERIFIED.