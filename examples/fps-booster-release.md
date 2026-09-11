# Example: FPS Booster release

```text
$agent-mission-control

Prepare the FPS Booster application for release. The optimizer core, dashboard,
and Windows installer changed. Improve p99 frametime without increasing crashes,
preserve every supported profile and setting during upgrade, and stop before
deploy.
```

Mission Control should:

- freeze the hardware/workload baseline and data-preservation gates;
- isolate optimizer, dashboard, and installer ownership after their interfaces
  are fixed;
- use a candidate loop only for measured optimizer improvements;
- require independent runtime, migration, rollback, and rendered UI evidence;
- return `PASS`, `FAIL`, or `NOT VERIFIED` instead of a confidence statement;
- leave any skill-learning proposal until after the release run is verified.
