---
name: arc-agi3-experiment
description: Run a preregistered, falsifiable experiment on ARC-AGI-3 on your own hardware. Use when designing or running an agent experiment on ARC-AGI-3 (or any interactive benchmark where an agent must discover the rules by acting), when writing a preregistration, when deciding whether a result counts as a verdict, or when someone asks how to reproduce this line of work. Triggers on "ARC-AGI-3", "preregister", "falsifier", "tune vs held-out", "does this beat random", "experiment register".
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

Most ideas do not need a GPU, an API key, or a token budget. The strongest known
policy on this benchmark that costs nothing is *random action selection with dead-action
pruning*: pick uniformly from the available actions, but never repeat an action already
known to leave the screen unchanged.

**That is your baseline. Beat it or report that you did not.** A new capability that
does not beat a policy with no model in it has not earned its complexity.

See `references/hardware-tiers.md` for what runs on what. Tier 0 is a laptop.

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
experiment. Three of the first five experiments in this line of work ended there.

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
has already happened once here, where nearly all of a doubled clear count came from a
single level of a single game.

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
