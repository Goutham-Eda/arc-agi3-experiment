# Peer pack

Everything a collaborator on this ARC-AGI-3 project needs to read, in reading order.
No competition code and no competition data is in here: the games you download
yourself, and the agent source is not shared (see the note at the end).

## Start here

| File | What it is |
| :-- | :-- |
| `intial_setup.md` | The fifteen steps, from publishing a notebook to writing up a result. Steps 3-8 are the onboarding gate: nobody gets an experiment before passing the day-one test. |
| `ARC-AGI-3-five-questions.pdf` | The five questions the programme is actually asking. |

## What has been found

| File | What it is |
| :-- | :-- |
| `ARC-AGI-3-eleven-experiments.pdf` | **The current results.** Eleven preregistered experiments and their verdicts. |
| `ARC-AGI-3-can-a-small-ai-play.pdf` | The same story written for a general reader. Good for sharing outward. |
| `ARC-AGI-3-architecture-diagram.pdf` | How the pieces fit together, on one page. |
| `ARC-AGI-3-five-experiments.pdf` | **Superseded** by `eleven-experiments`. Kept because it is what was published at the time. |

## How the method works

Read these if you are running an experiment, not just following one.

| File | What it is |
| :-- | :-- |
| `ARC-AGI-3-research-process.pdf` | The process end to end. |
| `ARC-AGI-3-what-would-prove-it-wrong.pdf` | Falsifiers: the one habit the rest depends on. |
| `ARC-AGI-3-the-register-out-loud.pdf` | What the experiment register is and why nothing in it is ever edited. |
| `ARC-AGI-3-silent-wrong-answers.pdf` | The bugs that faked results here, and how they were caught. |

## How the hypotheses were derived

The literature review that produced H1-H6, rather than picking them by taste.

| File | What it is |
| :-- | :-- |
| `ARC-AGI-3-reproducible-lit-review.pdf` | The method, as a process someone else can run. |
| `ARC-AGI-3-from-590-to-58.pdf` | The harvest and screening: 590 candidates down to 58, with a reason recorded for each inclusion. |
| `ARC-AGI-3-what-the-58-say.pdf` | The extraction table: what each paper actually claims. |
| `ARC-AGI-3-ranking-h1-to-h6.pdf` | How the six hypotheses were ranked, and which one was the bet. |

## Working notes

Raw internal notes, converted as-is. Less polished than the rest; included because they
show the working rather than the conclusion.

| File | What it is |
| :-- | :-- |
| `ARC-AGI-3-cluster-origins.pdf` | The cross-domain appendix: 611 candidates screened down to 16 sources from outside AI - developmental psychology, affordances, cybernetics - one per cluster question. Three of them challenge the hypotheses rather than support them. |
| `ARC-AGI-3-genesis-trial.pdf` | The pre-registration for adopting Genesis itself, written and committed *before* the trial, so the success criteria could not be fitted to the outcome afterwards. The same rule as the experiment register, applied to a tooling decision. |
| `ARC-AGI-3-peer-review-mapping.pdf` | A live review of the literature review, mapped section by section onto what each criticism changed. The most useful single file for understanding why the hypotheses look the way they do. |

## Talks

| File | What it is |
| :-- | :-- |
| `ARC-AGI-3-random-genesis-e0.pdf` | The early weekly build note. |
| `ARC-AGI-3-talk-track.pdf` | Talking points for presenting this work. |

## On the agent code

It is not in this folder, and not linked from it. Accepting the ARC Prize rules makes
you a Participant: public code sharing is permitted but belongs on the competition's own
forum or notebooks, under an OSI-approved licence, available to every participant. The
competition is also still open, with a final submission on 2 November 2026.

What this means for you in practice: you can read every decision and every verdict here,
but you cannot rebuild the submitted agent from this pack. The random-plus-pruning floor
you can run yourself - `run_local.py` in the repository root implements it, and passing
its day-one gate is step 8 of `intial_setup.md`.
