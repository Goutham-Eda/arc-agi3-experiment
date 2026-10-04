---
name: arc-agi3-experiment
description: Run a preregistered, falsifiable experiment on ARC-AGI-3 on your own hardware. Use when designing or running an agent experiment on ARC-AGI-3 (or any interactive benchmark where an agent must discover the rules by acting), when writing a preregistration, when deciding whether a result counts as a verdict, or when someone asks how to reproduce this line of work. Triggers on "ARC-AGI-3", "preregister", "falsifier", "tune vs held-out", "does this beat random", "concentration rule", "experiment register".
---

# Preregistered experiments on ARC-AGI-3

ARC-AGI-3 is a set of small interactive games: a 64x64 screen in 16 colours, a few
buttons, no instructions. The agent has to work out the rules and the goal by acting.

This skill is the **process**, not an agent. It exists because the fastest way to
produce a worthless ARC-AGI-3 result is to run something, see a good number, and
decide afterwards what it meant.

## The one rule that makes the rest work

**Write down what would prove you wrong, before you run.**

Everything below is downstream of that. If you cannot say what result would make you
abandon the idea, you do not have an experiment — you have a demo.

## Before anything else

Most ideas do not need a GPU, an API key, or a token budget. The two policies worth
measuring against both cost nothing, and you need both:

- **The floor — random action selection with dead-action pruning.** Pick uniformly from
  the available actions, but never repeat an action already known to leave the screen
  unchanged. On the hidden set this scores about **0.07**.
- **The bar — a within-episode bandit over action classes**, learning during the episode
  which classes of move reveal something new. On the hidden set this scores about
  **0.15**, and a uniform-arms control at a matched budget scores **0.12** — so roughly
  **0.03 of the gap is the learning**, and the rest is the action grouping it sits on.
  That decomposition only exists because the control was run.

**Beat the floor to exist. Beat the bar to matter.** A new capability that does not
clear a policy with no model in it has not earned its complexity — and one that clears
random but not the bandit has only rediscovered structured exploration.

Note what it took to state that cleanly: a treatment, a matched control, and the
hidden-set number for each. "Our agent scored 0.15" would have been true and would have
told you nothing about why.

See `references/hardware-tiers.md` for what runs on what, and which Tier 0 questions
are already answered. Tier 0 is a laptop.

## The workflow

1. **Set up and pass the day-one gate.** `references/setup.md`. Do not skip it — if
   your environment is wrong, nothing you produce later is trustworthy.
2. **Write the preregistration.** `templates/prereg.md`, guided by
   `references/preregistration.md`. Twelve fields. It is not done until field 8
   (falsifier and stopping rule) is something you would actually honour.
3. **Smoke run.** Does it execute end to end on one game? No conclusions drawn.
4. **Probe run on tune games.** Does the scaffold behave as designed — are the
   switches firing, is the treatment actually different from the control? This
   catches implementation failure before you spend the real budget.
5. **Tune run.** Settings are chosen here, or the preregistered abandonment rule
   fires here. **Tune games never establish an effect.**
6. **Held-out run.** The verdict. Report per-game outcomes next to aggregates.
7. **Write the result.** `templates/result.md`. Record it whether it worked or not.
8. **Amend, never overwrite.** New information is a dated amendment appended below
   the original entry. The original claim stays visible and wrong.

Stopping at step 5 under your own abandonment rule is a complete, publishable
experiment. Several of the twelve experiments run through this process ended there, and
one was deferred before it ran at all.

## The safeguards are not optional

`references/safeguards.md` lists them. They exist because a real replay bug in this
project reused one environment across episodes; because `reset()` kept level progress,
later episodes inherited earlier success and appeared to clear levels in one action.
It inflated a baseline roughly three-fold before it was caught.

The tell was an impossible clear length. **Flag impossible clear lengths
automatically.** If your harness cannot replay a trajectory and reproduce the reported
outcome, you do not have a result.

## What counts as a verdict

`references/split-and-verdicts.md`. In short: split the public games once, with a fixed
seed, into a tune set and a held-out set. Selection happens on tune. Verdicts come from
held-out. Never move a game between them, and never let a good tune number talk you
into reporting it as a finding.

And report per-game. An aggregate can be carried entirely by one favourable game — this
has already happened repeatedly here, the first time where nearly all of a doubled clear
count came from a single level of a single game.

That lesson is now a rule with a name. Under the **concentration rule**, a result counts
only if it also survives removing the largest-gain game and at least two games improve;
otherwise it is recorded as *"narrow: carried by `<game>`"*. Of the experiments that
passed their aggregate test here, most were narrow. One was not, and that one is the
bar in the section above.

## What the process has produced, so you can skip ahead

Twelve preregistered experiments have been run through this process. The point of
listing them is not the scores — it is that **every row below was decided by a
falsifier written before the run**, including the rows that killed ideas their authors
liked.

| Asked | Verdict |
| :-- | :-- |
| Does a frozen small model beat random play? | **No.** Both a 4B-class and a 31B-class model cleared nothing where random cleared one level in eighty. |
| Does a memory of failed trajectories help? | **Exploration only.** Clears stayed level with random. Memory helped search, not understanding. |
| Does telling the model what the controls do help? | **No — it hurt.** Wasted moves went up. |
| Does labelling each move by intent help? | **Stopped at tune.** Two thirds of replies ignored the required label; an interface failure, not a hypothesis failure. |
| Does dead-action pruning beat plain random? | **Narrow.** Real, but carried by one game. |
| Does masking clock and counter cells help? | **Narrow**, and kept as infrastructure: the common measurement judge. |
| Does graph memory with return-to-frontier help? | **Little.** |
| Does a within-episode bandit over action classes help? | **Yes — the one broad result.** Six games improved; confirmed on 40 fresh seeds; 0.07 → 0.15 on the hidden set. |
| How much of that is the learning, not the grouping? | **About 0.03 of 0.08.** Isolated by a uniform-arms control at matched budget. |
| Does a per-screen memory of deadly moves help? | **Narrow**, on the one game it was designed for — and it then **failed to transfer**: 0.15 on the hidden set, unchanged, against a pre-registered band that called 0.14–0.15 "adds nothing visible". |
| Do object-targeted clicks help? | **Falsified on clears**, though efficiency improved. |
| Can an oracle goal bound what goal inference is worth? | **Deferred before running** — too few tune clears to measure, and the goal predicate could not be written honestly. |

Read top to bottom, that is one answer: **on an unfamiliar interactive environment, a
frozen model's per-move judgement is not the scarce resource — structured exploration
is.** Everything that helped was a way of not wasting moves. Nothing that helped
required the model to understand the game.

Note the last two rows together. A fix that worked locally on the game it was built for
moved the hidden-set score not at all — and because the score bands had been written
down *before* the submission, that was a verdict on the day it landed rather than an
argument afterwards. Narrow results are where "strong locally, not shown to generalise"
gets decided.

The honest limit on all of it: the only genuinely unseen test is the hidden set, and
every held-out number above has been through many experiments on the same games. See
`references/split-and-verdicts.md` on why that is a known weakness rather than a solved
one.

## Labelling external facts

When your preregistration or write-up leans on a claim from outside your own runs,
label it: **VERIFIED**, **COMPANY CLAIM**, **INFERENCE**, **OPEN QUESTION**, or
**UNKNOWN — requires empirical verification**. A design that rests on four unlabelled
company claims is a design that will surprise you.

## Competition rules, if you are also on Kaggle

Accepting the ARC Prize rules to download the games makes you a Participant, which
binds you too. Two consequences worth internalising:

- **No private code sharing outside your own officially merged team.** Public sharing
  is permitted but must go on the competition's own forum or notebooks, under an
  OSI-approved licence, available to every participant.
- **Do not redistribute the competition data.** Every collaborator downloads it
  themselves.

This skill contains no competition code and no competition data, so it can be shared
freely. Keep it that way if you extend it.
