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

## The win-recording bug

Later, and separately: a harness recorded a win against the *next* game in the sweep
whenever a game was won, roughly doubling the reported score. It survived many runs
before it was caught.

Both bugs are the same shape — **success leaking across a boundary it should not
cross** — which is why "independent success accounting" is on the list above and why
replay is the check that catches the whole family. A bug like this is worth a
regression test and worth recording in the register. It is not worth writing a paper
about: it is a missed line, not a transferable finding.

## If you collect a dataset from your own runs

Transitions collected by an agent are a *sample taken by a policy*, and the policy
shapes the sample. Two findings here bind anything trained on such data:

- **A frame is not always one layer.** Some games render in multiple layers, so "the
  screen" is ambiguous. Whatever you train or reason over must **declare which layer it
  reads**, and a stored frame must replay cell-for-cell against the judge that produced
  it. Six sampled episodes were replayed by hand here before the collection was trusted.
- **A learning policy gives breadth; a uniform policy gives balance.** Collecting under
  a learning policy and a uniform policy at matched budgets, the learning policy reached
  more distinct screens and therefore more distinct actions — it pulled actions the
  uniform policy never saw, and never the reverse. But it concentrated: over a third of
  its pulls on one action where the uniform policy spread a sixth. A model trained on
  the learning policy's data alone would learn that skew as the world. **Say which
  policy's transitions you trained on, or report both.**

This correction is also an example of the amendment discipline in
`split-and-verdicts.md`. The collection was justified in writing on the grounds that a
dataset from the learning policy alone would inherit its blind spots — and the data
showed the breadth ran the opposite way. The original reasoning stays in the record,
with the correction beneath it.

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
