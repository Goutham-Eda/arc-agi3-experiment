# arc-agi3-experiment

A reusable process for running **preregistered, falsifiable experiments on ARC-AGI-3**
on whatever hardware you have — including a laptop with no GPU.

ARC-AGI-3 is a set of small interactive games: a 64x64 screen in 16 colours, a few
buttons, and no instructions. The agent must work out the rules and the goal by acting.

This repository contains **no competition code and no competition data**. It is the
method, the templates, and the hard-won list of things that go wrong.

## Why it exists

The fastest way to produce a worthless result on this benchmark is to run something,
see a good number, and decide afterwards what it meant. A research programme has run
twelve preregistered experiments here. **One produced a broad positive result.** The
rest were negative, narrow, or abandoned — and the record is useful precisely because
each one had its falsifier written down first.

Three findings from that programme shape everything in here:

1. **The baselines to beat cost nothing, and there are two.** Random action selection
   with dead-action pruning is the floor, and it is competitive with everything a frozen
   small model managed. A within-episode bandit over action classes is the bar, and it
   roughly doubled the hidden-set score without any model at all. Beat the floor to
   exist; beat the bar to matter.
2. **An aggregate can be a lie.** A doubled level-clear count turned out to come almost
   entirely from one level of one game. Report per-game outcomes, always — and make the
   concentration rule part of the preregistration, not of the post-mortem.
3. **Structured exploration was the scarce resource, not per-move judgement.**
   Everything that helped was a way of not wasting moves. Nothing that helped required
   the model to understand the game.

## Start here

- **`run_local.py`** — run the baseline on your own machine, offline, on CPU. This is
  the day-one gate. Start by making it pass.
- **`SKILL.md`** — the process, end to end.
- **`references/setup.md`** — install, get the games, and pass the day-one gate.
- **`references/hardware-tiers.md`** — what you can actually answer on a laptop.
  (More than you would expect.)
- **`references/preregistration.md`** — the twelve fields, and what makes each honest.
- **`references/split-and-verdicts.md`** — tune vs held-out, the stages, reading a result.
- **`references/safeguards.md`** — the bugs that faked results here, and how to catch them.
- **`templates/`** — fill-in preregistration and result forms.
- **`case-study/`** — the actual research record this method came out of: twelve
  preregistered experiments, their verdicts and corrections, the decision and gate
  records, and the raw run reports. No agent source and no competition data; the
  reasons are in `case-study/README.md`.

## Using it with an AI coding agent

**Claude Code** — copy the folder into your skills directory, then just ask for help
designing or running an experiment; it loads itself when relevant.

```bash
git clone https://github.com/Goutham-Eda/arc-agi3-experiment.git
mkdir -p ~/.claude/skills                                  # all your projects
cp -r arc-agi3-experiment ~/.claude/skills/
# or, for one project only:  mkdir -p .claude/skills && cp -r arc-agi3-experiment .claude/skills/
```

**Codex, or any agent that reads `AGENTS.md`** — clone the repository and work inside
it, or copy `AGENTS.md`, `SKILL.md`, `references/` and `templates/` into your own
project. `AGENTS.md` carries the rules that should override an agent's defaults.

**Genesis** — adopt this repository, or your own experiment repository built from it:

```bash
genesis adopt .          # read the discovery report first
genesis adopt . --write  # only after you have accepted it
```

It works just as well read by a human with no agent at all.

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
