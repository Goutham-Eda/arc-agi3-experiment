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

## The concentration rule

A pass on the aggregate is not enough. Before a result is recorded as supported, it
must also survive **removing the game with the largest gain**, and **at least two games
must improve**. A result that passes significance but fails this is recorded as
**"narrow: carried by `<game>`"** — reported honestly, never built on.

This rule is the formalisation of the per-game lesson below, and it has done real work
here. Two experiments passed their aggregate test and were filed as narrow, carried by
a single game. One passed with six games improving, and that is the only broad positive
result in the register.

The test used alongside it is a **paired, one-sided exact sign test across seeds**, on
the per-seed difference in levels cleared, ties dropped, p < 0.05. Where two action
budgets are both tested, apply a **Holm correction** across them — otherwise two
budgets are two chances at the same hypothesis.

**One surviving delta is a candidate, not a result.** A positive at a small seed count
gets re-run at a larger one, on fresh seeds, before anything is built on top of it. The
broad positive here was confirmed at 40 fresh seeds after first appearing at 20.

## Diagnosis makes a game adaptive

When a method loses on a held-out game and you investigate *why* on that game, you have
looked at held-out data. Any later test on that game is now **adaptive**, and the
write-up has to say so. Two of this project's held-out games were diagnosed this way —
one loss was then fixed narrowly, the other accepted as a limit of the method.

Diagnosis is still worth doing; the losses are where the next hypothesis comes from.
But it spends the game. After that, **the hidden set is the only genuinely unseen
test**, and you get very few shots at it.

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
