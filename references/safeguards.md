# Evaluation safeguards

These are not best practices. Each one exists because something went wrong.

## The replay bug

A runner created one environment per game and played every episode on it. `reset()`
keeps level progress — so once an episode cleared level 1, every later episode of that
game started past it and counted its first action as a clear. The baseline it produced
was inflated roughly three-fold.

It was caught by noticing **one-action clears**, which are impossible: the shortest
genuine clear observed took 5 actions.

## Enforce all of these

- **One fresh environment instance per episode.** Not one per game. Destroy or close it
  afterwards.
- **Unique episode IDs**, and an explicit check for ID reuse.
- **Explicit initial-state verification** — assert every episode starts at level 1 and
  at the expected starting state.
- **Initial-state hash or checksum**, where the engine allows it.
- **Deterministic seed recording** for every episode.
- **Independent success accounting** — do not let a win in one episode be able to write
  into another's record.
- **Full replayable trajectories.** If you cannot replay the action sequence and
  reproduce the reported outcome, you do not have a result.
- **Automatic flags for impossible clear lengths.** Set a threshold (here: fewer than 5
  actions) and make the run fail loudly, not quietly.
- **Checks for unexpected starting levels.**
- **A regression test for each bug you fix**, so it cannot come back silently.

## Packaging failures count as failures

One run in this project crashed during import on every game because the build omitted a
newly required dependency. It produced no measurements and supports no conclusion —
that is the correct way to record it.

**Make the build check fail whenever a required import is missing.** A run that
produced no data is not a negative result; it is a non-event, and calling it a negative
result is the more dangerous of the two mistakes.

## The known measurement ceiling

Exact screen identity is an imperfect judge of whether anything happened:

- clocks and step counters change even when the game world does not;
- so a dead action can appear to have caused a state change;
- which inflates any metric built on novelty, and explodes any graph built on distinct
  states.

Masking transients, or comparing at object level, may fix it. **Treat that as an
infrastructure change or an explicit ablation — never change it silently inside a
comparison**, or you will not know which variable moved.

## Distinguishing the two failures

Whenever a result comes back negative, answer before writing it up:

> Did the hypothesis fail, or did the scaffold fail?

The probe stage exists to answer this in advance. If you skipped it, you usually cannot
answer it afterwards, and the experiment has to be re-run.
