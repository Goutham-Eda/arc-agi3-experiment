# Agent instructions

This repository is a **method**, not an application. There is no product code to
extend. Your job here is to help a researcher design and run a falsifiable experiment
on ARC-AGI-3 and to write the record honestly.

## Read first

1. `SKILL.md` — the process end to end.
2. `references/preregistration.md` — before helping write any experiment.
3. `references/safeguards.md` — before helping write any runner.

## Rules that override your defaults

- **Do not run an experiment before its preregistration is written.** If the user asks
  you to "just try it", write the preregistration first — it takes five minutes and it
  is the entire point of this repository.
- **Do not choose the success criterion after seeing results.** If the criterion was
  not written down beforehand, say so and treat the run as exploratory, not as a
  verdict.
- **Do not report tune-set numbers as findings.** Tune games select settings or
  trigger abandonment. Only held-out games produce verdicts.
- **Always report per-game outcomes next to aggregates.** An aggregate carried by one
  game is the known failure mode here, and it has already happened once.
- **Never edit a recorded result.** Append a dated amendment beneath it.
- **Never commit competition data.** `environment_files/` is gitignored. It is not
  redistributable.

## When a result comes back negative

Ask, and answer in the write-up: *did the hypothesis fail, or did the scaffold fail?*
Use the probe-stage evidence. If there was no probe stage, say that the experiment
cannot distinguish the two and should be re-run.

## Running things

`python run_local.py --games 3 --episodes 3 --max-actions 80` is the day-one gate. It
is offline, CPU-only, and needs no API key. It must pass before any experiment.
