# The case study

`../SKILL.md` is the method. This is the working record it was extracted from: twelve
preregistered experiments on ARC-AGI-3, run between 11 September and 4 October 2026,
with the verdicts, the corrections, and the decisions as they were made at the time.

It is here because a process document is cheap to write and easy to doubt. The register
below is what makes the method checkable — including the parts that went wrong.

## What is here

| Path | What it is |
| :-- | :-- |
| `experiment-register.md` | **Start here.** The canonical record: preregistrations, verdicts, dated amendments, diagnoses, corrections. Every number in the method traces back to a block in this file. |
| `session-handoff.md` | The state of play, written to let a new session continue without reconstructing the discussion. Section 14 is the handoff prompt itself; section 16 is the whole programme in one sentence. |
| `next-phase-design.md` | Designs P1-P8 and the decision tree governing which runs next. |
| `milestone-brief.md` | The brief as submitted for the competition's first milestone. |
| `e0-e4-writeup.md` | A portfolio write-up of the first five experiments. **Superseded** - see the note at its head. |
| `literature-review/` | The reproducible literature-review process: method, plan, Elicit extraction table, and a companion walking through it. 500+ candidates down to 58, with a recorded reason for every inclusion. |
| `plan/` | Earlier planning documents: experiment plan, baseline analysis, working notes, partner templates. |
| `process/` | The harness record - decisions, findings, and 139 machine-written gate receipts. See `process/how-to-read-the-gates.md`. |
| `results/` | Per-episode run reports for E4-E11 and C1, one JSON per condition. See `results/README.md` for the one field removed. |

## What is deliberately absent

**The agent source.** Six policies, the submission agent, the experiment runner and 113
tests are not in this repository and are not linked from it. Accepting the ARC Prize
rules makes you a Participant: public code sharing is permitted, but belongs on the
competition's own forum or notebooks under an OSI-approved licence, available to every
participant - not in a personal repository. The competition is also still open at the
time of writing, with a final submission date of 2 November 2026.

This has a cost worth stating plainly: **you cannot reproduce these numbers from this
repository.** You can read every decision that produced them, check the arithmetic in
`results/`, and rebuild the method from `../SKILL.md` and `run_local.py`, which does
implement the random-plus-pruning floor. The bandit that produced the headline result is
described in the register but not shipped.

**The competition data.** The games, the frames collected from them (320 episodes, 35 MB
of screens) and the per-level human action counts are not here and never entered version
control. Rule 2.4.b forbids redistributing them. Download them yourself; see
`../references/setup.md`.

## How to read it

Ten minutes: `session-handoff.md` section 16, then the twelve-row table in `../SKILL.md`.

An hour, if you want to know whether the process is real rather than decorative - read
these three, in order:

1. **The E0 block** in `experiment-register.md`. A frozen language model at two sizes,
   both below a random baseline. The falsifier was written first, and it fired.
2. **The replay-bug correction** in `process/knowledge.md`. A bug inflated the random
   floor roughly three-fold. Find the original entry, then the correction, then the
   earlier verdict restated against the corrected floor. Three entries, all still
   present, none edited.
3. **The C1 block's closing amendment** in `experiment-register.md`. The block's own
   written justification for collecting under two policies turned out to be wrong, and
   its own data said so. The original reasoning stays above the correction.

Those three are the argument. The rest is detail.

## State, as of 4 October 2026

E0-E11 complete, Builds 1-6 submitted, C1's frame collection done, and C2 - deriving
labels from those frames - pre-registered with its implementation checks passed.

Hidden-set scores: random 0.07, uniform arms (Build 5) 0.12, bandit (Build 4) 0.15,
bandit plus death memory (Build 6) 0.15. The last landed against a band that predeclared
0.14-0.15 as "adds nothing visible", so a fix that demonstrably worked on the one public
game it was built for did not transfer to the 110 unseen ones. It is the cleanest
comparison in the project - Build 6 changed exactly one rule from Build 4 - and it is why
the death memory was not promoted to baseline.

Every document here is current to 4 October. Where two of them cover the same ground,
`experiment-register.md` is authoritative: the handoff summarises it, and the Genesis
records under `process/` are the raw inputs it was written from.

## Licence

This record is prose and data, published under the repository's Apache-2.0 licence for
consistency. The literature-review material summarises third-party papers; the papers
themselves are not redistributed here.
