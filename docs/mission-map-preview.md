# Agent Mission Control — Markdown preview

One lead chooses the smallest useful route for each coding task. The host runs
the work; AMC is a portable skill, not a graph runtime.

## The main path

```mermaid
flowchart TD
  Task["Coding task<br/>goal · limits · proof · authority"] --> Lead["Lead agent<br/>routes · integrates · accepts"]
  Lead --> Route{"Smallest useful route?"}
  Route -->|Known work| Direct["Direct<br/>lead implements + checks"]
  Route -->|Focused gap| Specialist["Specialist<br/>bounded inputs · scope · check"]
  Route -->|Independent jobs| Parallel["Parallel<br/>isolated writers · owned scope"]
  Direct --> Integrate["Lead integrates<br/>current artifact + evidence"]
  Specialist --> Integrate
  Parallel --> Integrate
  Integrate --> Check["Check current artifact<br/>run relevant checks"]
  Check -->|Failed check| Lead
  Check -->|Current evidence| Risk{"Material risk?"}
  Risk -->|Yes| Review["Independent review<br/>read-only falsification"]
  Review -->|Finding| Lead
  Review -->|Cleared| Report["Final report<br/>PASS · FAIL · NOT VERIFIED · BLOCKED"]
  Risk -->|No| Report
  Report -.->|After task, optional| Learn["Record a reusable lesson separately"]
```

## Add only when needed

| Trigger | Lead adds |
| --- | --- |
| Scope is unclear | Scout maps dependencies and advises the lead. |
| Work was interrupted | Resume reconciles the saved record with current files. |
| A measurable goal has a frozen evaluator and baseline | An AVO-inspired loop runs a candidate, compares it, and keeps only a strict gain; otherwise the incumbent remains. |
| The next attempt is costly | A budget checkpoint weighs new evidence against attempt cost. |

The lead may reroute after new evidence. A PASS is an **advisory claim** backed
by current checks, not a release authorization. [Decision rules](how-it-works.md)
and [evidence limits](evidence.md) explain the boundaries.
