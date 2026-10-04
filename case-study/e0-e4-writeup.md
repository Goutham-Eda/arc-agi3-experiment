> **Superseded, 4 October 2026.** This write-up covers E0-E4 only. The research ran to
> E11 plus the C1 frame collection, and two of its framing claims have since changed: the
> policy to beat is no longer plain random but a within-episode bandit over action classes,
> and the random floor quoted here predates the replay-bug correction. It is kept because
> it is what was published at the time. For the current position read
> `experiment-register.md` and `session-handoff.md`.

# Can a small frozen model, plus a harness, play ARC-AGI-3?

**E0–E4, 11–19 September 2026.** ARC Prize 2026, ARC-AGI-3 track.
Every experiment here was written down with its pass/fail rule before it ran; the
canonical record is `research_prep/notes/experiment_register.md`. Every headline
number below is recomputed from the saved results by `experiments/check_writeup.py`.

---

## In plain words

ARC-AGI-3 is a set of small video-like puzzle games. Nobody tells the player the
rules or the goal; it has to find them by pressing buttons and watching the screen.
Humans clear these games easily. The question was whether a **small, free AI model
that we do not retrain**, wrapped in a clever program (a "harness"), could play them.

- **The AI models played no better than pressing random buttons.** Not the small one,
  not a model eight times bigger.
- **Giving the AI a memory** (skip buttons that did nothing; remember what killed it)
  made it explore more of each game, but it still did not beat random.
- **Telling the AI in advance what each button does** made it waste *more* moves.
- **Asking the AI to label each move "to learn" or "to win"**, and keeping a diary of
  its experiments, also made it waste more moves — and it ignored the instruction on
  two moves in three.
- **The one thing that worked was not AI at all:** random button-pressing that stops
  pressing buttons it already knows do nothing. On the practice games it cleared twice
  as many levels as plain random.
- **On Kaggle's hidden games that improvement disappeared:** both the old and the new
  entry scored 0.07.
- **Along the way we found a bug** that had made random play look better than it was.
  We fixed it, re-ran everything it touched, and corrected the record in the open.

The honest result is negative, but it is a clean negative: every claim has a
pre-written test, and the claims that turned out wrong are corrected in the open,
not quietly deleted.

---

## 1. The question and the method

**Hypothesis space.** A frozen open-weight model (no weight changes anywhere) choosing
actions from a text rendering of the screen, with the *harness* as the only thing that
varies between conditions. The bet was that at small model size, harness mechanisms
would dominate model differences.

**Games.** The 25 public games, split once, before any model played, into 8 **tune**
and 17 **held-out** games with a fixed seed. Every verdict number comes from held-out.
`r11l` is reported but kept out of verdict aggregates (random can clear its level 1
faster than the human baseline).

**Primary metric.** Levels cleared on the 16 verdict games. The competition metric,
RHAE, only moves when a level is cleared efficiently, and at this performance level it
reads zero for almost everything, so it is reported secondary. The dense proxies were
distinct screens per 100 actions (exploration) and repeat deaths.

**Discipline.** Each experiment was registered with a falsifier before running, fixed
budgets (80 actions per episode for model runs, 5 seeds), and a scaffold that stayed
frozen within an experiment. Changes after a run are dated amendments, never edits.
Models ran on Kaggle (vLLM, one RTX PRO 6000); random policies ran locally on CPU.

---

## 2. E0 — the baseline: frozen models do not beat random

| 16 verdict games, 80 actions, 5 seeds | random | Gemma-4-E4B | Gemma-4-31B |
| :-- | --: | --: | --: |
| levels per game | **0.0125** | 0.000 | 0.000 |
| RHAE | 0.0348 | 0.0000 | 0.0000 |
| distinct screens per 100 actions | 78.5 | 68.6 | 73.2 |
| same, click games only | 73.5 | 59.6 | 66.1 |

- **Both Gemma sizes clear nothing.** Random clears one level in the 80 verdict
  episodes. The gap is one clear — small, but no frozen condition closes it.
- **The whole deficit is in click games.** On keyboard-only games the models explore
  as much as random; on games that need `ACTION6 x y` they fixate on cells that do
  nothing. Eight times the parameters halves that deficit but does not close it.
- **The 31B run was a clean scaffold:** 7 parse failures in 6,800 calls. So its
  result is about the model, not the prompt.
- **Qwen3-8B was a scaffold failure, not a model comparison.** It named click actions
  in games that offer none and collapsed onto a single move; 7 of 85 episodes broke
  the pre-registered 20% parse-failure line and were excluded. It is not reported as
  "Qwen plays worse".
- **A labelled coordinate grid looked decisive on two tune games and did nothing at
  scale** (click gap −13.5 → −13.1 across 13 held-out click games). That claim was
  retracted in the register rather than edited out.

**Cost:** about 13.6 GPU-hours, most of it the 31B run, which had to be split across
two kernels because a single one would have exceeded Kaggle's 9-hour limit.

---

## 3. E1 — memory: explores more, solves no more (weak)

**Treatment.** Two harness switches on the same frozen Gemma-4-E4B, all four
combinations: `--prune-visited` (if a move left the screen unchanged, never let the
model repeat it on that screen; a random live move is substituted) and
`--failure-rules` (after each death, a fixed-wording note of what preceded it goes
into the prompt). With both switches off, prompts were verified byte-identical to E0,
so E0's run served as the control.

**Falsifier.** Supported only if both-on beats *both* the control and random.

| 16 verdict games | random | control | prune only | rules only | both |
| :-- | --: | --: | --: | --: | --: |
| level clears | 1 | 0 | 1 | 0 | 1 |
| distinct screens per 100 | 78.5 | 68.6 | 74.4 | 69.6 | 74.5 |

- **Verdict: weak.** Both-on beats the control but only ties random.
- **Pruning does all of it; the failure rules do nothing.** The two mechanisms,
  merged into one experiment on a reviewer's argument, turned out to be separable.
- **The one clear was mostly random play:** 12.1% of all moves were substitutions,
  and in the clearing episode 64% were.
- **The failure-rule null says little:** 34 rules were written, but the control
  repeats a death only once in 85 episodes, so the failure it targets barely occurs
  at this budget.

**Cost:** about 2.9 GPU-hours. **Stopped** by decision rather than run at 10 seeds:
more seeds would measure the random substitutions more precisely without making them
the model's.

---

## 4. E2 — telling the model what its buttons do backfires

**Treatment.** A *controllability probe*: the harness plays the first *k* moves of each
level itself and puts one line per move into the prompt ("ACTION1: 4 cells changed
in x 10-12..."). **Control:** the same model with *k* extra moves and no probe, so
extra moves cannot masquerade as the probe's effect. The tune rule, fixed in advance,
chose *k* by the model's **dead-move rate** (the share of its own moves that change
nothing), or abandoned E2 if no *k* beat its control by more than the control's seed
range.

| tune games, 3 seeds | k = 5 | k = 10 | k = 20 |
| :-- | --: | --: | --: |
| dead-move rate with probe | 0.344 | 0.321 | 0.333 |
| dead-move rate, matched control | 0.284 | 0.303 | 0.293 |

- **Abandoned at tune: the sign is wrong at every *k*.** With the probe, the model
  wastes *more* of its own moves. One game carries the loss: on `sk48` the dead-move
  rate roughly doubles.
- **It is not simply inert:** on other games the probe raised exploration sharply.
  It changes behaviour, just not in the direction the hypothesis needed.
- **The null cannot tell a bad probe from a wrong hypothesis,** and that was stated
  before the run. The re-test at every level, which could have separated them, never
  fired because no level was cleared.

**Cost:** about 2.7 GPU-hours.

---

## 5. E3 — label each move "learn" or "win": stopped at tune

**Treatment.** Parked since the start — the idea is already published on this
benchmark — and run on 19 September by explicit decision. The model starts each reply
with `LEARN` (a move to find out how the game works) or `WIN` (a move towards the
goal). After each `LEARN` move the harness records what changed on screen, and the
model sees its last five such "experiments". Unlike E2, **the model chooses what to
test**. Same tune rule as E2: continue only if the model's dead-move rate beats a
no-label control by more than the control's seed range.

| tune games, 3 seeds | with labels | without |
| :-- | --: | --: |
| dead-move rate | 0.342 | 0.295 |

- **Stopped at tune: the sign is wrong again.** With labels the model wastes more of
  its own moves, and no level is cleared. The same game as in E2, `sk48`, carries the
  loss — the second time extra prompt text has sent this model into repeated
  do-nothing moves there.
- **The model mostly ignored the instruction.** Of 1,920 replies, 385 were labelled
  `LEARN`, 255 `WIN`, and 1280 carried no label at all. So this is a weak test of the
  idea: it says the model does not reliably follow a labelling instruction, and that
  where it did, play was no better — not that the mechanism fails.

**Cost:** about 1 GPU-hour, including a first kernel that played nothing (below).

---

## 6. E4 — smarter random: wins on practice games, not on hidden ones

**Treatment.** No model. Plain random play, except a move already seen to leave the
current screen unchanged is redrawn. Until the first such redraw it plays exactly like
plain random, so the two are paired seed by seed. Local CPU, 17 held-out games,
**20 seeds**, budgets 80 and 300 actions (300 primary). **Falsifier:** a one-sided
sign test over seeds on levels cleared, p < 0.05, and more total clears.

| held-out, 20 seeds | random | smarter random | seeds won / lost / tied |
| :-- | --: | --: | :-- |
| **300 actions** — level clears | 19 | **38** | **18/0/2**, p < 0.0001 |
| 80 actions — level clears | 6 | 12 | 6/0/14, p = 0.016 |
| RHAE, all 17 games, 300 actions | 0.0916 | 0.1000 | |

- **Supported, and narrow.** Almost all of the gain is one game: `lp85` level 1 is
  cleared in 20/20 seeds against 1/20. Everywhere else the two play the same clears.
- **Build 3** put this policy into the competition agent with a 300-action cap. A local
  rehearsal of the scored rerun cleared `lp85` through the real framework, and unit
  tests confirm the agent plays the same episodes as the experiment's policy.
- **On the 110 hidden games it scored 0.07 — the same as Build 1**, the plain random
  agent at 80 actions. Kaggle reports two decimals, so a smaller change would be
  invisible, but it is not an improvement worth claiming.

**Cost:** CPU only.

---

## 7. What went wrong, and how it was caught

The first two changed conclusions; all five are recorded as amendments, not edits.

1. **A replay bug inflated the random baseline.** The run loop reused one game
   environment for all episodes of a game, and `reset()` keeps level progress. Once an
   episode cleared level 1, every later episode started past it and counted its first
   move as a clear. It was caught because E4's first run showed level clears in 0 or 1
   actions, which is impossible. **Effect:** the random floor at 80 actions was
   recorded as 0.037 levels per game; it is 0.0125. "Random clears `r11l` in 5 of 5
   seeds" became 1 of 5. Model runs were unaffected (none cleared a level before its
   last episode). E1's verdict survived (it was compared against the wrong bar, but
   still did not beat the right one). The contaminated E4 run was discarded and re-run
   before its verdict. A regression test now pins one environment per episode.
2. **A two-game result was over-read.** Coordinate labels "fixed" clicking on two tune
   games and did nothing across thirteen held-out ones. Since then, tune games have only
   fixed settings or triggered a pre-registered abandonment, never supported an effect.
3. **A metric meant something other than it seemed.** "Top-action share" counts the
   action *name*, so a model clicking a different cell every turn reads as fully
   collapsed. Read beside distinct screens, the apparent collapse disappeared.
4. **Seeded model calls are not exact replays.** Identical prompts gave slightly
   different moves when vLLM batched requests differently, so the reused control is a
   draw from the same distribution, not a replay. The falsifiers already required
   beating random as well, which tolerates this.
5. **A kernel shipped without a file it needed.** E3's first Kaggle run crashed on
   import in every game: the run script had gained a dependency during E4 that the
   kernel builder did not package. Nothing was measured and nothing was concluded from
   it; the build check now fails on any missing import.

Two known ceilings were recorded before the runs they affect: on-screen **clocks and
step counters** defeat exact-screen identity (pruning misses dead moves; the probe's
summaries blur), and **80 actions is too short** for repeated deaths to occur often.

---

## 8. What the evidence supports, and what it does not

**Supports:**

- At 80 actions, frozen Gemma-4-E4B and Gemma-4-31B, with this text scaffold, do not
  clear levels random play does not also clear.
- The models' main failure is **clicking cells that do nothing**, and a harness rule
  that blocks those clicks raises exploration, for a model and for random play alike.
- Harness memory of dead moves and harness memory of deaths are **different mechanisms**
  with different effects.
- A description of each button's effect, given up front, **does not** make this model
  waste fewer moves — and neither does a log of the model's own chosen experiments.
- Adding instructions or text to this model's prompt tends to make it **worse** on some
  games (`sk48` twice), and it follows a new output format only a third of the time.

**Does not support:**

- That frozen models *cannot* do this — only this scaffold, these sizes, this budget.
- That H3 (identify what you control first) is wrong: the null was undistinguishable
  from a bad probe, by design.
- That separating learning moves from winning moves is a bad idea: the model used the
  labels on only a third of its moves.
- That PRO-LONG-style full logs beat rule memory: the failure-rule null had almost
  nothing to act on.
- That dead-move pruning helps on unseen games: the public gain did not show on the
  hidden set.

---

## 9. Cost

| Experiment | Compute | Outcome |
| :-- | :-- | :-- |
| E0 | ~13.6 GPU-h (Kaggle) | frozen models not above random |
| E1 | ~2.9 GPU-h | weak; pruning only |
| E2 | ~2.7 GPU-h | abandoned at tune |
| E3 | ~1 GPU-h | stopped at tune |
| E4 | local CPU | supported on public games |
| Build 3 | CPU, one submission | 0.07 hidden, unchanged |
| **Total** | **~20 GPU-h** across two weeks of 30 h quota | |

---

## 10. Open questions (not decided)

- **Longer budgets.** The submission can afford far more than 300 actions per game;
  repeated deaths, and therefore failure memory, only become testable there.
- **Masking on-screen clocks** so screen identity means "the world changed", which
  would sharpen both pruning and the probe.
- **Object-level rather than cell-level dead moves** (closer to Reki's dead-signature
  detection, which this work credits for the mechanism class).
- **A different control architecture**, e.g. acting to hold a perceived variable at a
  target value, from the cross-domain appendix `research_prep/notes/cluster_origins.md`.
- **A different interface for the same frozen-model bet.** The ARC-AGI-3 Milestone 1
  winner (Tufa Labs' Duck Harness) runs a frozen open-weight 27B model that writes
  Python against the game state — objects already segmented, before/after transitions,
  several actions per call — and reports far higher public-game scores than anything
  here. It is the natural next comparison.

---

## Appendix — where everything is

**Records.** Register: `research_prep/notes/experiment_register.md` (E0–E4 blocks and
all dated amendments and corrections). Genesis knowledge records:
`KNOWLEDGE-ae516ae2` (replay bug, corrected floor), `KNOWLEDGE-6c660d7f` (31B),
`KNOWLEDGE-0d7aa9c5` (labelled grid), `KNOWLEDGE-697febf3` (Qwen scaffold failure),
`KNOWLEDGE-8413b47a` (E1), `KNOWLEDGE-086194e3` (E1 probe), `KNOWLEDGE-cfbeb805`
(E2), `KNOWLEDGE-cca50afa` (E3), `KNOWLEDGE-1ad719a0` (E4), `KNOWLEDGE-aafd5a6f`
(Build 3 hidden score).
Decisions: `DECISION-17bcf9bb` (E1 falsifier), `DECISION-e3978a7e` (E4B first),
`DECISION-200ac78f` (E1 stopped), `DECISION-4f50991f` (E2 design),
`DECISION-792aefcb` (E3 unparked, option B),
`DECISION-fd4761c5` (E4), `DECISION-4cd8d5d2` (Build 3).

**Code.**

| Path | What |
| :-- | :-- |
| `src/agents/llm_baseline.py` | the frozen-model agent, with E1's switches, E2's probe and E3's labels (all off by default) |
| `src/agents/random_prune.py` | E4's smarter random policy |
| `experiments/e0_random_smoke.py` | the run loop (random, random-prune, model) |
| `experiments/e0_kernel.py` | builds and verifies the Kaggle experiment kernels |
| `experiments/e0_analyze.py` | per-condition analysis, E2's k rule, E3's tune rule, E4's sign test |
| `experiments/check_writeup.py` | recomputes this document's numbers |
| `submission/my_agent.py` | the competition agent (Build 3) |
| `tests/` | 35 tests, including byte-identical control prompts and saved-episode replays |

**Data.** E4 results are in the repository (`experiments/e4_random_300.json`,
`experiments/e4_prune_300.json` and the 80-action pair). Model-run outputs are
downloaded Kaggle outputs under `experiments/build/`, which is not committed, so the
numbers check runs only where they are present.
