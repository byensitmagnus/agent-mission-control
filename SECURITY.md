# Security policy

## Reporting a vulnerability

GitHub private vulnerability reporting is currently unavailable for this repository (rechecked 2026-09-15; API `enabled: false`). Do not open a public issue containing credentials, private prompts, customer data, or details that would make an active vulnerability easier to exploit.

If you find a vulnerability, open a public issue only to request a private contact channel and include zero vulnerability details. Wait for the maintainer to provide a private channel before sharing the affected instruction or workflow, realistic impact, or smallest safe reproduction. Do not infer a response-time commitment.

The intended future setting is repository Settings > Security and quality > Advanced Security > Private vulnerability reporting, as described in the [GitHub setup guide](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/configure-for-a-repository). The public API returned `enabled: false`; enabling it is a future maintainer action. Recheck its state before relying on private reporting.

## Scope

This repository contains agent instructions, not an execution service. Reports about authority escalation, unsafe secret handling, destructive defaults, verification bypass, or cross-worktree contamination are in scope.