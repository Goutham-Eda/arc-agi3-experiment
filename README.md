# arc-agi3-experiment

A reusable process for running **preregistered, falsifiable experiments on ARC-AGI-3**
on whatever hardware you have — including a laptop with no GPU.

ARC-AGI-3 is a set of small interactive games: a 64x64 screen in 16 colours, a few
buttons, and no instructions. The agent must work out the rules and the goal by acting.

This repository contains **no competition code and no competition data**. It is the
method, the templates, and the hard-won list of things that go wrong.

## Why it exists

The fastest way to produce a worthless result on this benchmark is to run something,
see a good number, and decide afterwards what it meant. A research programme that ran
five experiments here produced five negative or abandoned results — and the record is
useful precisely because each one had its falsifier written down first.

Two findings from that programme shape everything in here:

1. **The baseline to beat costs nothing.** Random action selection with dead-action
   pruning — no model at all — is competitive with everything a frozen small model was
   able to do. Any new capability has to beat it.
2. **An aggregate can be a lie.** A doubled level-clear count turned out to come almost
   entirely from one level of one game. Report per-game outcomes, always.

## Start here

- **`SKILL.md`** — the process, end to end.
- **`references/setup.md`** — install, get the games, and pass the day-one gate.
- **`references/hardware-tiers.md`** — what you can actually answer on a laptop.
  (More than you would expect.)
- **`references/preregistration.md`** — the twelve fields, and what makes each honest.
- **`references/split-and-verdicts.md`** — tune vs held-out, the stages, reading a result.
- **`references/safeguards.md`** — the bugs that faked results here, and how to catch them.
- **`templates/`** — fill-in preregistration and result forms.

## Using it with an AI coding agent

Drop the directory into your agent's skills location (for Claude Code:
`.claude/skills/arc-agi3-experiment/`). The agent will load it when you ask for help
designing or running an ARC-AGI-3 experiment.

It works just as well read by a human.

## Getting the games

You download them yourself from the competition page after accepting the rules. They
are not redistributable, so nobody can send them to you. See `references/setup.md`.

## Competition rules

Accepting the ARC Prize rules to download the games makes you a Participant. Private
code sharing outside your own officially merged team is prohibited; public sharing must
go on the competition's own forum or notebooks under an OSI-approved licence. This
repository stays free of competition code so that it can be shared without any of that
applying.

## Licence

Apache-2.0.
