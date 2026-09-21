# GitHub settings checklist (human execution)

This checklist is **not** claimed active. `GET
/repos/byensitmagnus/agent-mission-control/branches/main/protection` returned
HTTP 404 on 2026-09-18 (`Branch not protected`). Private vulnerability reporting
was last recorded `enabled: false` in [SECURITY.md](../SECURITY.md) (2026-09-15).

Do not run these from an agent session without a separate mandate. Exact GitHub
UI/API actions for a maintainer:

1. Protect `main`: Settings → Branches → Add branch ruleset / protection for `main`.
2. Require a pull request before merging; dismiss stale reviews on new commits.
3. Require status checks: the current `Validate` workflow
   (`.github/workflows/validate.yml`), including both Python 3.11 and 3.14 matrix
   jobs. Do not require a check that this repository does not run.
4. Block force pushes and branch deletion on `main`.
5. Enable private vulnerability reporting where the plan supports it:
   Settings → Code security → Private vulnerability reporting.
6. Decide whether signed commits and/or signed tags are required. Do not enable
   them as a silent default; record the decision. This repository currently
   makes no signed-commit claim.

Recheck with the GitHub API after changing settings. Until then, protection and
private reporting remain UNVERIFIED / off as last observed.
