# Resource checkpoints

Use the existing mission record or native telemetry, not another tracker/service.
At costly boundaries compare unresolved acceptance gates with the information or
progress the next action is likely to buy: another fan-out, model escalation,
candidate attempt, repeated repair, rapid context growth or a known budget limit.
Tiny operations do not need their own checkpoint.

If an expensive retry produces no new evidence or repeats a known setup failure,
inspect its command and prerequisites before choosing another model or full run.
Escalate a bounded reasoning problem when capability is the bottleneck; more
agents do not resolve a missing runtime or accelerate one serial test process.

When observable, retain wall-clock, lead input/output and cached input, workers
by actual model/effort, active/completed counts, attempts/repairs and verified
progress. Cached input is a subset of input, not additional tokens. Distinguish
root-only from complete child coverage. Do not present missing telemetry as zero.
Summarize redundant work and defects found as well as tokens. Do not expose
secrets or raw conversations to collect metrics.

A user-specified budget is part of the mission contract. Record its unit, scope,
soft/hard thresholds and reliable source; do not invent an account percentage.
Native account quota is account-wide unless documented otherwise, not this
mission's spend. Query it only when useful. Dollars require actual billing or a
verified applicable rate and measured usage; label estimates and exclusions.
Model names or token totals alone do not prove cost or savings.

When applicable rates and counters exist, estimate each model separately:
uncached input (= input minus cached input), cached reads and output, each at its
own rate; add cache writes, tool charges or service-tier adjustments when those
apply and are observable. Include the lead, workers, failed attempts and repair.
Do not equate API estimates with subscription limits or ignore missing charges.
Compare cost alongside verified outcomes, defects and interventions, not token
count alone. Stable useful prefixes can benefit caching; do not add irrelevant
context to chase cache hits. Native host configuration owns caching and compaction.

At a soft threshold, reduce waste internally: reuse current evidence, narrow
worker inputs, stop low-value work, serialize, choose a suitable cheaper tier,
or keep the incumbent instead of another optional attempt. Preserve correctness
and required proof. At a projected overrun, prefer a cheaper equivalent plan;
escalate capability only for a specific unresolved risk/information need.

Before exceeding a hard user budget or a reliably observed material cost change,
stop the next costly optional action. Preserve state and explain observed usage,
remaining gate, why the next step is costly, and any cheaper path with its quality
tradeoff. Ask only when continued spending needs authorization. Existing authority
still covers safe work within the limit. Unknown prices/quota alone never trigger
a cost warning or an invented permission blocker. Never purchase credits or reset
allowances as an automatic recovery action.

Optimization has both correctness and attempt/resource limits. Before another
candidate consider expected improvement, chance it changes the decision, remaining
budget and a cheaper way to learn the same thing. Stop low-value search with the
best verified incumbent; report unresolved gates without calling them complete.

## Cost-aware delegation

Fan-out is a capacity mechanism, not a discount and not AMC's identity. Do not
mix four different outcomes: shorter calendar time, more artifacts, fewer
dollars, and a better accepted result. Parallel workers often help the first two
and can worsen the last two.

Delegation is cheaper than doing the work on the lead only when saved lead
tokens are worth more than worker time, review, retries and coordination. That
usually needs independent jobs, a small packet, a declared accept check before
spawn, an artifact return the lead can judge without repeating the job, and
review only when risk warrants it. It usually fails on unclear architecture,
tightly coupled files, missing tests, shared mutable state, or overlapping
scouts.

Before a costly spawn, answer the preflight. Any "no" keeps the work with the
lead or serializes it:

1. Are the jobs genuinely independent?
2. Can each worker receive a small, precise packet?
3. Is the accept check declared before spawn?
4. Will the lead receive paths, diff, result and evidence — not a transcript?
5. Can the lead accept without redoing the work?
6. Is review risk-based, not automatic?
7. Are saved lead tokens likely worth more than worker, review, retry and
   coordination cost?

Ceilings, not targets:

| Resource | Default ceiling |
|---|---|
| Workers | `min(host concurrency, remaining budget, independent ready jobs)` |
| Retries | At most one cheaper retry with a tighter contract, then escalate the slice |
| Reviewer | Zero unless material risk or a changed acceptance rule; then one independent review unless the user authorized more |

Concurrency is a ceiling. Filling it is not a goal. A host profile
([quality / balanced / throughput](../examples/profiles.md)) may bias how eagerly
the lead spends the ceiling; it does not waive isolation, artifacts or this
preflight.

When the host exposes usage, record lead, worker and review consumption
separately, by actual model or agent identity. Unknown is not zero. Do not merge
those buckets into one total and call it cheaper. Native snapshot tools may
group counters by agent name when spawn metadata exists; they still do not
estimate dollars unless a verified rate is supplied.
