# Specialists and workflow triggers

Use these routes only when the task calls for them. The lead keeps the user's
chosen model and owns scope, integration, acceptance and authorized actions.
Use a domain skill directly when a separate agent would add no useful expertise
or independence. Role descriptions do not grant tools or permissions.
Projects can define named specialists once as existing skills or native host
roles, such as a commerce facts reviewer or a release build verifier. Declare
the trigger, evidence sources and permissions with each role; AMC routes to it.

| Role | Trigger | Handoff and result |
| --- | --- | --- |
| Implementation specialist | A change needs focused skills or an independently owned slice | Give the authorized code scope, project rules and one acceptance check. Return the diff and actual check output. |
| Domain specialist | A decision depends on expertise, e.g. commerce, finance or communications | Give the one question, authoritative sources and as-of date. Return evidence, exceptions and what remains unknown. Default to read-only. |
| Evidence verifier | A candidate exists and claims can be checked against named evidence | Use a small read-only packet and the least costly supported model capable of the check. Return findings, missing proof or no findings within scope. |
| Independent reviewer | Material risk, a required review, or unresolved correctness that could cause an expensive wrong PASS | Follow [independent proof](verification.md). Use a fresh reviewer who did not author the candidate, with the ability to falsify the unresolved claim. |
| Work buddy | The user asks to resume, choose a next action or review deadlines | Use only the user's selected work sources. Give one concrete next action, up to two dated commitments and any missing owner/deadline. Don't infer deadlines, assign work, or start recurring reminders without the user's request. |

## Check the candidate before publishing

Trigger **after** a coherent candidate and before the authorized publish,
deploy, send or writeback. Skip the model call if no candidate exists or existing
checks already answer the bounded question. Reuse existing tests and source
reads. Freeze the candidate identity first: commit plus relevant dirty diff, or
the hash of the exact artifact. Give a verifier only the candidate, claims,
acceptance criteria and actual check results it needs. Prefer deterministic
checks for facts such as CI state, prices against an authoritative snapshot,
and whether an approval covers this exact artifact.

A verifier compares each claim with its evidence and checks for missing authority
or scope drift. Separate observed evidence, reported evidence, failed checks and
checks not run. Summarize the three highest-priority findings with a source or
reproduction, flag any failure or missing required proof, and include the
remaining count and where the lead can inspect it. It does not fix, approve or
publish. A quiet verifier is not an independent approval. Reuse prior proof only
when the relevant source, inputs and environment are shown unchanged. Missing
required evidence remains NOT VERIFIED and observed failures remain FAIL.
Required independent review is separate from cheap screening. The lead resolves
or escalates a specific finding; no automatic model upgrades or retries.

## Use the host for recurring oversight

Create or change a schedule only on explicit user request. Use the existing
scheduler and mission/project status; check for overlap first. Run read-only
across explicit projects and source lists, using
dated facts rather than entire conversations. Set a run frequency, source and
output cap, explicit model if available, and a stop switch. Don't spawn children,
retry, or expand scope in a scheduled check. Report exceptions such as a
documented overdue date, an unresolved approval or inconsistent proof; give at
most three with links and owners if documented, plus a count of omitted issues.
Skip unchanged issues only when
the host supplies a reliable prior report for comparison. If sources are missing
or stale, say so; do not certify health or invent an owner. Reports stay within the
authorized destination and grant no authority to write, send or release.

The host enforces tool and filesystem restrictions where supported. Read-only
filesystem mode alone does not make network tools read-only. Keep mutation tools
and credentials out of read-only specialists, verifiers and scheduled checks; if
the host cannot restrict them, use deterministic output or a reduced tool set
rather than claiming enforced read-only review. Honor an explicit model choice.
See [capability routing](packets.md) and [resource limits](resources.md).
