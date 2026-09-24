# The split, the stages, and what counts as a verdict

## The split

Split the 25 public games **once**, with a fixed recorded seed, into a **tune set** and
a **held-out set**. Write the split to a file and commit it. Never regenerate it, never
move a game between sets, never "just check" a held-out game while developing.

This project uses 8 tune and 17 held-out.

**Exclude games where the baseline is degenerate.** One game here is reported but kept
out of verdict aggregates because random play can beat the human baseline on its first
level — including it would let noise masquerade as capability. Decide such exclusions
from tune-side reasoning, before the verdict run, and record why.

## What each set is for

| Set | Legitimate uses | Never |
| :-- | :-- | :-- |
| **Tune** | choosing hyperparameters; checking the scaffold works; firing a preregistered abandonment rule | establishing that an effect exists |
| **Held-out** | the verdict, once, per preregistration | selecting settings; repeated peeking during development |

The asymmetry is the whole point. Tune games can **kill** an idea but cannot
**support** one.

## The stages

1. **Smoke** — does it run end to end on one game? No conclusions.
2. **Probe** — on tune games, with few seeds: is the scaffold behaving as designed? Are
   the switches actually firing? Is the treatment genuinely different from the control?
   This separates implementation failure from hypothesis failure, which is the single
   most common way an experiment wastes a compute budget.
3. **Tune** — settings are selected, or the preregistered stopping rule fires.
4. **Held-out** — the verdict run.
5. **Submit / publish** — if applicable.

Stopping at stage 3 under your own rule is a complete experiment. Record it as such.

## Seeds

Fix and record seeds. Typical budgets here: 5 seeds for model runs at 80 actions per
episode; 20 seeds for cheap CPU policies at 80 and 300 actions.

Use a **fresh seed block** for each new experiment on the same games. This reduces —
but does not remove — the bias from reusing held-out games across many experiments.
Treat that reuse as a known open weakness and say so in the write-up. The only fully
fresh test is the hidden set, which you get at most a couple of shots at.

## Reading a result

- **Report per-game outcomes next to the aggregate.** Always. In this project a
  doubled clear count across public games turned out to come almost entirely from one
  level of one game, cleared in 20 of 20 seeds versus 1 of 20. The aggregate said
  "strong method"; the per-game table said "one game".
- **Use a paired test across seeds** where conditions share seeds — report wins,
  losses and ties, not just means.
- **A strong public result that does not transfer to the hidden set is a finding**, and
  the honest phrasing is "strong locally, not shown to generalise".
- **Compare against the simple policy, not only against the previous complex one.**

## Amendments

Never edit a recorded claim. Append a dated amendment beneath it saying what changed
and why. When a bug invalidates earlier numbers, the correction goes in as an
amendment, the original stays visible, and the write-up states plainly which numbers
moved and which were unaffected.

A research record where nothing was ever wrong is a research record nobody was
checking.
