# <ID> — result

**Author:** <name>  ·  **Run:** <YYYY-MM-DD>
**Stage reached:** smoke / probe / tune / held-out
**Verdict:** supported / falsified / stopped at tune / no measurement

> If the stage reached is "tune" because the stopping rule fired, this is a complete
> experiment. Write it up the same way.

## What was run

- Preregistration: `<path>`
- Code version / commit:
- Environment: `arc-agi <v>`, `arcengine <v>`, Python <v>, <CPU/GPU>
- Seeds:
- Action budget:

## Safeguard checks

| Check | Result |
| :-- | :-- |
| Fresh environment per episode | |
| Every episode started at level 1 | |
| No episode-ID reuse | |
| No impossible clear lengths (< 5 actions) | |
| Trajectories replay to the same outcome | |

## Primary result

| <split>, <n> seeds | Control | Treatment | Paired won/lost/tied |
| :-- | :-- | :-- | :-- |
| Levels cleared | | | |

## Per-game outcomes

| Game | Control | Treatment | Note |
| :-- | :-- | :-- | :-- |

**Is the aggregate carried by one game?** <yes/no — and if yes, say so in the headline>

## Secondary metrics

| Metric | Control | Treatment |
| :-- | :-- | :-- |
| Distinct screens / 100 actions | | |
| Dead-move rate | | |
| Repeat deaths | | |

## Instruction-following (if structured model output was required)

Compliant replies: <n>/<total> (<%>). Harness substitutions: <n> (<%>).

## Against the preregistered criterion

- Criterion was:
- Observed:
- **Therefore:**

## Hypothesis failure or scaffold failure?

<Answer it explicitly. Cite the probe-stage evidence.>

## What this changes

- For the next experiment:
- For the research record:
- Surprises not anticipated in the preregistration:
