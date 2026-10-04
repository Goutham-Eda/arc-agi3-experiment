# Experiment register

Every experiment in this project is written here **before it is run**, with its
falsifier stated in advance. An experiment with no falsifier is not an experiment;
it is a hope. Nothing gets added to the agent on the strength of an argument —
only on the strength of a delta that survived a pre-registered test.

Written 10 September 2026, after Session 29 peer review. Supersedes the planned
hypothesis-ranking write-up, which would have argued which hypothesis is most
promising instead of committing to what would prove it wrong.

**Amendment rule.** A block may be edited freely until its first run. After that,
changes are appended as a dated amendment with a reason, never made in place. The
record of what you predicted before you knew the answer is the whole value.

---

## Fixed across all experiments

| | |
| :-- | :-- |
| **Model** | one frozen open-weight SLM (Qwen 2.5 7B or Gemma 3, decided at E0). No weight changes anywhere in this register. |
| **Why frozen** | Rodionov (2607.15439): capability gains exceed the differences between architectural variants. At frontier scale a mechanism delta is masked by the model's own reasoning. A small frozen model is the condition under which the harness delta is the dominant term rather than the noise term. |
| **Independent variable** | the harness, and only the harness. Same weights, same decoding parameters, same system prompt scaffold in baseline and treatment. |
| **Games** | 25 public ARC-AGI-3 games / 183 levels. Split fixed at E0 and never changed: **tune** (8 games) and **held-out** (17 games). Every number reported for a verdict comes from held-out. |
| **Seeds** | N = 5 runs per condition minimum. A delta smaller than the seed-to-seed spread of the baseline is not a delta. |
| **Reporting** | every experiment reports a **vector over clusters A–E**, not a single score. See "Cross-cluster reporting" below. |
| **Compute** | RunPod hosted inference during development; weights uploaded as a Kaggle dataset for submission. |

### Cross-cluster reporting

From the peer review: *"that second experiment helped one of your clusters but
regressed on another — we can do that detailed review of that delta."*

A harness that promotes failures into rules may suppress exploration; that shows
up as a gain in E and a loss in C, and a single RHAE number hides it completely.
So `src/evaluation/metrics.py` must emit, per run:

| Cluster | Proxy measured |
| :-- | :-- |
| A — understand the unknown world | levels reached on first contact with an unseen game |
| B — what is probably true | rate of acting on a belief later contradicted |
| C — discover useful information | distinct states visited per 100 actions |
| D — knowledge into action | actions between "effect learned" and "effect used" |
| E — improve over experience | repeat-hazard rate after the first failure |

A regression on a non-target cluster does **not** by itself sink an experiment.
It is recorded, and it is the thing the write-up explains.

---

## E0 — Baseline characterisation

**Not optional, and it can fail.** Every other experiment in this register is a
difference from E0. If E0 has no signal, there is nothing to take a difference
from.

| | |
| :-- | :-- |
| **Question** | does a frozen open-weight SLM with a minimal scaffold score anything measurable on ARC-AGI-3? |
| **Setup** | observe → choose action → observe. No memory across steps beyond the raw context window. No harness. |
| **Measured** | RHAE; levels reached; actions-to-solve; the five cluster proxies; seed-to-seed variance on all of them. |
| **Falsified if** | RHAE is 0.0000 on every held-out game across all 5 seeds — i.e. the baseline is indistinguishable from the published random-agent floor. |

**If it falsifies** — and this is a live risk, since random agents are published
at exactly RHAE 0.0000 — the register does not stop. RHAE is a *sparse* metric:
it only registers a level actually solved. Switch the primary metric to dense
alternatives that move before a level is ever completed:

- levels reached, and progress within a level
- distinct states visited before termination
- repeat-hazard rate

and report RHAE as secondary. A harness can be demonstrably better while both
conditions still score zero on the official metric, and that must be visible
rather than fatal.

**Also decided here:** which model (run both candidates, keep the one with a
usable floor and lower variance), and the tune/held-out split.

**Status:** pre-check run 11 September 2026 against the real engine, offline.
See the amendment below. The frozen-SLM run itself is still blocked on Kaggle
account + phone verification for GPU access.

### Amendment, 11 Sept 2026 — random-floor pre-check

Ran a random policy over all 25 games, 2 episodes, 300 actions, offline against
the competition's own `environment_files`
(`experiments/e0_random_smoke.py`, results in `experiments/e0_random_floor.json`).

**RHAE was 0.0000 on all 50 runs.** Two independent causes, both structural:

1. Random almost never clears a level. Only `r11l` (both episodes) and `sp80`
   (one) cleared anything at all.
2. **Even those score zero.** `arc_agi/scorecard.py` weights each level by its
   own index — `total_score += level_scores[i] * level_indices[i]` — so level 0
   carries weight 0 and contributes nothing however well it is played. Verified:
   clearing only level 0 at exactly human pace scores 0.0000; clearing through
   level 1 scores 6.67; through level 3, 40.00; all six, 100.00.

So RHAE does not begin to move until **level 1** is cleared. "Completed a level"
and "scored above zero" are different events, and the gap between them is where
this project's agent is going to live for some time.

**Consequence for E0.** Its falsifier is no longer a contingency to guard
against; it is the expected outcome. E0 runs with the dense metrics as primary
from the start:

| Metric | Random floor, range over 25 games |
| :-- | :-- |
| max level cleared | −1 on 23 games, 0 on 2 |
| distinct states per 100 actions | 1.0 (`lp85`) to 100.0 (`re86`) |
| resets in 300 actions | 1 to 21 |
| repeat hazards | 0 to 3 (`vc33`) |

Those ranges are wide and stable across seeds, which is what E0 needed to
establish: the dense metrics discriminate between games at the floor, where RHAE
reports 25 identical zeros. `lp85` at 1.0 states/100 and `re86` at 100.0 are
completely different problems that RHAE cannot tell apart.

**Promote a metric.** `max_level_cleared` is now E1's and E2's primary, with
actions-to-solve secondary and RHAE reported third. Beating the baseline means
reaching a level index the baseline never reached.

**Two caveats on the pre-check itself.**

- The repeat-hazard proxy hashes the frame at `GAME_OVER`. If a game shows a
  generic death screen rather than the state that killed you, this counts death
  screens, not hazards. Check against `vc33` before the E proxy carries weight.
- 300 actions is a short budget. A longer one may clear more levels and is worth
  one run before E0 fixes its own budget.

### Correction, 12 Sept 2026 — the level-0 claim above is wrong

The amendment above is left as written; this corrects it. Two of its claims were
produced by a bug in `e0_random_smoke.py`, not by the scorer.

**The bug.** The script passed 0-based level indices to
`EnvironmentScoreCalculator.add_level`. The toolkit's own caller passes
`level_index=level_idx + 1`, and the Kaggle data page says the weighting is
"1-indexed". With 0-based indices the first level got weight 0, which produced
the "level 0 contributes nothing" finding. **The scorer does not ignore the
first level.** On a six-level game the first level carries 1/21 of the weight.
Found by checking the claim against the competition's written scoring rule.

**Corrected floor** (same run: 25 games, 2 episodes, 300 actions, seed 0):

| Game | Episode | RHAE | Level-1 score | Note |
| :-- | :-- | --: | --: | :-- |
| `r11l` | 0 and 1 | 4.7619 | 115.0 | random cleared level 1 in ≤ 20 actions against a human baseline of 22, hitting the per-level cap |
| `sp80` | 1 | 0.0951 | 2.0 | cleared level 1 slowly: (39/276)² × 100 |
| other 23 games | all | 0.0000 | — | no level cleared |

3 of 50 runs score above zero. **E0's falsifier as written, "RHAE 0.0000 on every
held-out game", is therefore not guaranteed at the random floor** — `r11l` and
`sp80` would break it if they land in the held-out split.

**What survives from the amendment.** The dense metrics still carry E0: 23 of 25
games read exactly 0.0000, and the dense metrics separate those 23 where RHAE
cannot. `max_level_cleared` stays primary for E1 and E2.

**What is new.** `r11l`'s first level is solvable by random walk *faster than a
human*. A level that random beats discriminates nothing between harnesses, and
any agent will look superhuman on it. Before fixing the held-out split at E0:

- report `r11l` level 1 separately, or exclude it from verdict metrics;
- check whether other games have random-trivial first levels at longer budgets;
- note that the aggregate is capped by the weight of levels actually cleared
  (`min(score, max_weights / total_weights * 100)`), which is why `r11l` reads
  4.7619 = 100/21 and not 115/21.

**Also check.** The Kaggle page gives the per-level rule as
`min(human/agent, 1.0)` squared — a cap at 100. The pinned toolkit 0.9.8 caps at
115. They agree on `r11l` only because the aggregate cap binds first. Which rule
the Kaggle grader applies is not confirmed; the scores above use the toolkit's.

### Amendment, 12 Sept 2026 — the random floor on the hidden set is 0.07

Build 1 (`submission/my_agent.py`: uniform over each frame's
`available_actions`, 80 actions per game, CPU) was submitted as Kaggle
submission `56171083` and scored **0.07 public** on the 110-game hidden set.

This is the first number from the real test distribution rather than the 25
public games. It settles the question the correction above left open: **the
random floor is above zero on the hidden set too**, so E0's falsifier as
written ("RHAE 0.0000 on every held-out game") cannot be the bar. The bar for
E0 is now concrete: **beat 0.07** on the hidden set, and on the public set
beat the random floor per game on `max_level_cleared`.

The leaderboard score also confirms the scored path end to end — offline
install, gateway, framework, agent — so no later build needs to re-prove the
plumbing.

### Amendment, 12 Sept 2026 — E0 runs at two model sizes

**Decision (human, 12 Sept): run E0 at both sizes.** This supersedes the
"Model" row in *Fixed across all experiments*. That row named Qwen 2.5 7B or
Gemma 3; both were written from memory and are a generation behind what
Kaggle hosts.

| Tier | Models | GPU | Role |
| :-- | :-- | :-- | :-- |
| small | Gemma-4-E4B-it; a small Qwen 3 (4B or 8B, fixed at the first run) | T4 ×2 | the registered design: a weak model, where a harness delta is easiest to see |
| winner | Qwen3.6-27B-FP8; Gemma-4-31B-it | RTX 6000 | the size all three Milestone 1 winners ran |

**Why both.** The register chose a small model so that the model's own
reasoning would not mask the harness (Rodionov). Two newer facts cut the other
way. At the small-model floor the official score stays near zero, which is the
problem the random-floor pre-check hit. At winner size the official score moves:
top public scores on 11 Sept were 5–11%. And the Milestone 1 winners reported
that added machinery *hurt* — "hand-crafted tools actually hurt the model"
(Tufa Labs, 1st); forge's winning run "disabled most extra machinery" (3rd) —
so harness effects are visible at that scale, even when negative. Running both
tiers tests directly whether the harness delta depends on model size, which
the frozen-small-model rationale assumed rather than measured.

**Licences.** All four models are Apache 2.0, from the publishers' own
Hugging Face tags (12 Sept). Gemma 3 is under Google's own licence, not an
open-source one; that is a reason not to use it, and no longer a reason to
prefer Qwen.

**Provenance.** Qwen 3.6 is on Kaggle only as community mirrors. Verify the
mirror's file hashes against Qwen/Qwen3.6-27B-FP8 before any verdict run.

**Precedent for E1.** Reki (2nd, Milestone 1) used "dead-signature" detection,
which stops clicks on object types that never respond, and reflection memory
refreshed every ~10 steps. That is close to H5 and H6 on ARC-AGI-3 itself.
H5 was "not found in this corpus"; it is not unclaimed. E1 must cite this and
compare against it.

**Budget.** The winner tier spends GPU quota faster and costs more per action.
9 hours over 110 games is about 4.9 minutes per game; measure ms/action in the
first run before fixing either tier's action budget.

### Amendment, 12 Sept 2026 — E0 execution details, fixed before any model run

1. **Held-out split fixed** in `experiments/e0_split.json`: sorted game ids,
   shuffled with `random.Random(20260912)`, first 8 tune, remaining 17
   held-out. Tune: `dc22 ft09 ls20 s5i5 sc25 sk48 tn36 tu93`. Held-out: the
   other 17. Fixed before any model played a game, and never regenerated.
   `r11l` fell in held-out, so its level 1 (random-trivial) is reported outside
   verdict metrics, as the 11 Sept correction required.
2. **The winner-tier Qwen is Qwen3.8-27B-FP8, not 3.6.** Same size, same
   licence (Apache 2.0, publisher tag), released August 2026 after Milestone 1,
   and the model in the current top public duck-harness notebook (LB ~9).
   Qwen3.8 Flash-Next is excluded: its licence tag is "other". On Kaggle it
   exists only as the community repack
   `foysalemonshanto/qwen3-8-27b-fp8-repacked-v1`, so its hashes must match
   Qwen/Qwen3.8-27B-FP8 before a verdict run.
3. **Kaggle model IDs:** `google/gemma-4/transformers/gemma-4-e4b-it`,
   `google/gemma-4/transformers/gemma-4-31b-it`,
   `qwen-lm/qwen-3/transformers/4b` and `/8b`, and the Qwen 3.8 repack above.
4. **Both tiers run on the same GPU (RTX Pro 6000) and the same vLLM build,**
   not the small tier on T4s, so that model size is the only thing that differs
   between tiers. A hardware or serving-stack difference would be a second
   variable: the protocol confound again. Default set by Claude; the human may
   override. Cost: small-tier runs spend RTX quota, but they are short.
5. **Serving:** vLLM installed offline from a Kaggle wheel dataset, the pattern
   every top public notebook uses. The exact wheelhouse is fixed at the first
   run.

### Amendment, 12 Sept 2026 — E0 scaffold design, fixed before any model run

Implemented as Agent B in `src/agents/llm_baseline.py`, run by
`experiments/e0_random_smoke.py --policy llm`.

- **Input is text:** 64 lines of 64 hex digits, from the last frame layer.
  Text is the only input all four models accept. Qwen3 4B and 8B are text-only
  (`Qwen3ForCausalLM`); Gemma 4 and Qwen 3.8 also take images. E0 therefore
  compares model size under one identical scaffold. **It is not the Milestone 1
  winners' vision setup, and its scores must not be read against theirs as
  like-for-like.**
- **Context:** the system prompt, the last 4 exchanges (`HISTORY_TURNS = 4`)
  and the current frame. Nothing else is carried between steps.
- **Decoding:** temperature 0.7, at most 128 tokens, Qwen thinking disabled.
  Every call carries its own seed (run seed × 10^6 + call index), so seeds
  differ and runs reproduce.
- **Parse failures:** a random legal action is taken and counted. **A run whose
  parse-failure rate exceeds 20% is a scaffold failure, not a model result**,
  and is excluded from verdicts.
- **Serving:** one vLLM 0.23.0 build for all four models. All three
  architectures (`Qwen3_5ForConditionalGeneration`,
  `Gemma4ForConditionalGeneration`, `Qwen3ForCausalLM`) are in its model
  registry; still to be proven on Kaggle. `--max-model-len 32768`.
- **The loop's random path is unchanged:** a test pins it to the pre-check's
  `ls20` numbers.

### Amendment, 12 Sept 2026 — before the first verdict run (small tier)

1. **Decoding is identical for every model** (human decision, 12 Sept). vLLM
   runs with `--generation-config vllm`, and every request sends temperature
   0.7 and top_p 1.0, with no top_k. The smoke run showed that vLLM otherwise
   applies each model's own `generation_config.json`: Gemma top_k 64, Qwen
   top_k 20, temperatures from 0.6 to 1.0. That was a difference between
   models the register had not fixed. The cost: this is not each vendor's
   tuned setting.
2. **The small-tier Qwen is Qwen3-8B, not 4B.** Its total parameter count
   matches Gemma-4-E4B's: 8.19B against 8.00B, from the Hugging Face
   safetensors counts. E4B's "4B" is its effective compute size; Qwen3-4B has
   4.02B total. Matching the stored size, which is what the tier is named for,
   is the fairer pairing.
3. **Execution:** the 17 held-out games run as parallel processes against one
   vLLM server. Each episode plays exactly as it would alone; only wall time
   changes.
4. **Action budget: 80 per game episode.** That is the budget build 1's random
   agent had when it scored 0.07 on the hidden set, so E0 compares against that
   floor like for like.
5. **Order:** Gemma-4-E4B, then Qwen3-8B. Stop and review with the human before
   the winner tier.

### Amendment, 12 Sept 2026 — labelled grid coordinates

**Change (human decision, 12 Sept): fix the clicking before running the second
small model.** `encode_frame` now prints two header lines numbering the columns
(tens, then units) and prefixes every row with its y coordinate. The system
prompt explains them. Nothing else changes.

**Why.** Gemma-4-E4B's entire deficit sits in games with a click action: mean
−17.3 distinct states per 100 actions against random on the 13 click games,
+0.3 on the 4 keyboard-only games. The logged replies show it clicking the same
dead cells, mostly corners and edges (`ACTION6 0 0`, `ACTION6 63 9`). An
unlabelled 64×64 hex dump gives no way to turn a seen position into the numbers
the action needs.

**Presentation only.** No memory, no pruning of repeated or ineffective clicks.
Those are H5 and H6, and they belong to E1: E0 has to stay the control E1 is
measured against.

**How it is judged, before any re-run of the held-out set.** The diagnostic
already recorded the "before" at the same games, seed and budget (kernel
`arc-agi-3-e0-diag`):

| Game | Before | Test |
| :-- | :-- | :-- |
| `dc22` (click) | 52.5 states/100, ACTION6 65/80, top-action share 0.81 | must rise toward random's 77.5 |
| `ls20` (keyboard) | 100.0 states/100, actions spread 38/14/13/15 | must not fall: a pure control |

**If it does not help,** the encoding is not the cause, and the next candidate
is the 20k-token context: four history frames per call, with the prefix cache
defeated by the sliding window.

#### Result of the labelled grid, 12 Sept 2026

Kernel `arc-agi-3-e0-diag2`, Gemma-4-E4B, same games and budget, two seeds.

| Game | Before (1 seed) | After (2 seeds) | Random |
| :-- | --: | --: | --: |
| `dc22` (click) | 52.5 | 66.25, 75.0 | 77.5 |
| `ls20` (keyboard control) | 100.0 | 88.75, 100.0 | 100.0 |

**The click test passes.** `dc22` rose from 52.5 to a mean of 70.6, most of the
way to random's 77.5. The mechanism moved as predicted: ACTION6 fell from 65 of
80 moves to 47 and 33, and the replies show scanning (`ACTION6 0 0`, `0 1`,
`0 2`) and varied targets (`61 12`, `63 19`, `20 20`) instead of the same dead
corner repeatedly.

**The control test is inconclusive, not passed.** `ls20` gave 88.75 and 100.0
against a single before-run of 100.0. One seed before and two after cannot
separate a real cost from seed variance. Recorded as open rather than passed;
the held-out re-run carries four keyboard-only games at five seeds and settles
it at scale.

**Cost:** ~22.4k tokens per call, up 9% from 20.5k, as the added labels predict.
1.8 s per call at two concurrent games.

#### Held-out verdict on the labelled grid, 12 Sept 2026 — the fix does not hold

Kernel `arc-agi-3-e0-gemma4-e4b` v2: 17 held-out games, 5 seeds, 80 actions,
labelled grid. 85 episodes, 0 excluded, play 78.8 min.

| Group | v1 plain vs random | v2 labelled vs random |
| :-- | --: | --: |
| click games (13) | −13.5 | **−13.1** |
| keyboard games (4) | −1.1 | **+2.1** |
| levels/game (16 verdict games) | 0.000 | 0.000 (random 0.037) |
| games above random | 0/16 | **0/16** |

**The click gap closed by 0.4 points: the fix does not survive contact with 13
games.** The two-game diagnostic (dc22 52.5 → 70.6) was not a basis for the
claim, and the amendment above overstated it.

**What is real, and was hidden by the mean.** The labels moved games hard in both
directions: `su15` 2.0 → 56.0 (−59.5 → −5.5), the worst collapse essentially
repaired; but `ar25` 69.5 → 43.2 (−13.8 → −40.0) and `m0r0` 69.2 → 49.2. They
help where the model was stuck and hurt where it was already coping.

**Two things settled.** The keyboard control passes at five seeds: +2.1, no cost,
closing the question the two-seed run left open. And parse failures fell to 0.0%
from 0.7%.

**One loss.** `r11l` level 1 was cleared by v1 in every seed and by random in
every seed; v2 cleared it in none. The labels cost the only level this model
reliably reached.

**Read for E0.** Coordinate labelling is not the cause of the click deficit, so
the deficit stands as a finding about the model rather than the encoding. The
next candidate remains the 20k-token context, whose sliding window defeats the
prefix cache. No further encoding change should be made on two-game evidence.

---

### Amendment, 12 Sept 2026 — Qwen3-8B held-out: a scaffold failure, not a model comparison

Kernel `arc-agi-3-e0-qwen3-8b`: the same 17 held-out games, 5 seeds, 80 actions,
labelled grid, identical decoding. 85 episodes, play 88.9 min, median 14.3 s/call.
**7 episodes excluded by the pre-registered 20% parse-failure rule** — the first
exclusions in E0.

| Group | random | Gemma-4-E4B | Qwen3-8B |
| :-- | --: | --: | --: |
| click games, states/100 | 73.7 | 59.6 (−14.1) | **44.4 (−29.3)** |
| keyboard games, states/100 | 93.5 | 95.6 (+2.1) | **73.3 (−20.2, 3 games)** |
| levels/game (verdict games) | 0.037 | 0.000 | 0.000 |
| games above random on levels | — | 0/16 | 0/15 |

**The exclusions are not random noise, and they name the cause.** All 7 fall on
`wa30` (5/5 seeds) and `re86` (2/5), and both are keyboard-only games whose
available actions are [1,2,3,4,5]. Their replies read `ACTION6 28 3`, `ACTION6 23
25`. Qwen names ACTION6 on **35% of sampled replies for games that do not offer
it**; Gemma does so on **0%**. Parse failures on keyboard-only games: Qwen 35% of
all calls, Gemma 0%. Every such reply is rejected by `parse_action` and falls back
to a random legal action, so those episodes measure the fallback, not the model.

**`wa30` has no surviving episodes at all.** Qwen's aggregate is over 15 verdict
games where Gemma's is over 16. The two columns above are therefore not strictly
like-for-like, and the keyboard row rests on 3 games. Stated rather than patched:
re-running `wa30` under a different scaffold would not be the same experiment.

**The deeper result is degeneracy.** Of the 78 episodes that survived exclusion,
**78 have a top-action share ≥ 0.95** — every one of them played essentially a
single action for 80 turns. 14 of 16 games returned identical results across all
five seeds, against 4 of 17 for Gemma and 2 of 17 for random. On `ar25` the model
played `ACTION6 15 15` eighty times and explored 1.2 states per 100 actions, where
random explores 83.2. This is the collapse-to-repetition failure that was
predicted for Gemma and refuted there; it is real, in a different model.

**Read for E0.** Qwen3-8B's number is not a clean measure of play quality, and it
must not be reported as "Qwen is worse at ARC-AGI-3". It is a model that does not
respect the available-action list under this prompt and collapses to one action.
Gemma-4-E4B is the small-tier baseline. **Falsifier status unchanged: no condition
has beaten the random floor on levels, 0/16 and 0/15.**

**Tooling, same date.** `e0_analyze.py` crashed (`StatisticsError`) when a game
lost every episode to the exclusion rule. Fixed to report the game by name and
average over the survivors, and the aggregate line now prints its own game count
so an uneven comparison cannot be read as an even one.

---

### Amendment, 13 Sept 2026 — Gemma-4-31B scaffold probe, and how its verdict run executes

**Probe passed.** Kernel `arc-agi-3-e0-probe-gemma4-31b` (12 Sept), run on **tune**
games `ls20` and `tu93` so the held-out split stays sealed: 1 seed, 20 actions each.
**0 parse failures in 40 calls.** Both games offer `[1,2,3,4]` only, and the model
never named `ACTION5` or `ACTION6` — the failure that made Qwen3-8B's run
uninterpretable. Top-action share 0.35, so no collapse to one action. Median 13.4 s
per call. This is a scaffold check only: `states/100 = 100.0` on two games is not
evidence of good play.

**Runtime risk it exposed.** vLLM needs 600 s to become ready. After weights, the KV
cache holds 84,388 tokens (24.58 GiB): about four concurrent requests at E0's ~20k
prompts. A single held-out kernel (17 × 5 × 80 = 6,800 calls) projects to ~6.5 h
against Kaggle's 9 h limit.

**Execution shape (human decision, 13 Sept).** The verdict run is split **by seed**
across two kernels, each carrying all 17 held-out games: episodes 0–2
(`arc-agi-3-e0-gemma4-31b-e012`) and episodes 3–4 (`arc-agi-3-e0-gemma4-31b-e34`).
Seeds derive from the episode index, so every episode plays exactly as it would in
one kernel; the two reports are concatenated for analysis. Splitting by *game* was
rejected: it would be a partial held-out peek. `--gpu-memory-utilization` rises
from 0.90 to 0.95 for these two kernels only.

**Comparability.** Both changes are serving and scheduling. The prompt, decoding,
split and budget are unchanged, so the 31B run compares with the small tier like
for like.

---

### Amendment, 16 Sept 2026 — Gemma-4-31B held-out verdict: the large tier is also below random

Kernels `arc-agi-3-e0-gemma4-31b-e012` (episodes 0–2) and `-e34` (episodes 3–4),
both `status ok`: 17 held-out games, 5 seeds, 80 actions, labelled grid, identical
decoding. 51 + 34 = **85 episodes, 0 excluded**, 6,800 LLM calls, **7 parse failures
(0.1%)**. The scaffold is clean, so unlike Qwen3-8B this *is* a model result.

| Metric (16 verdict games) | random | Gemma-4-E4B | **Gemma-4-31B** |
| :-- | --: | --: | --: |
| levels/game | 0.037 | 0.000 | **0.000** |
| states/100 | 78.7 | 68.6 | **73.2** |
| RHAE | 0.1539 | 0.0000 | **0.0000** |
| games above random on levels | — | 0/16 | **0/16** |

> **Falsifier status: unchanged, now at three conditions. No frozen model has beaten
> the random floor on levels — 0/16, 0/15, 0/16.** Size did not rescue it. The
> register's "run E0 at two sizes" amendment (12 Sept) asked whether the harness
> delta depends on model size; on the *baseline* it does not, because neither size
> produces a baseline above the floor.

**Where the 8× size does buy something.** The click deficit halves but does not close:

| Group | random | E4B | 31B |
| :-- | --: | --: | --: |
| click games (12 verdict) | 73.7 | 59.6 (−14.1) | **66.1 (−7.6)** |
| keyboard-only (4) | 93.5 | 95.6 (+2.1) | **94.7 (+1.2)** |

Four games beat random on exploration — `su15` +25.0, `m0r0` +8.2, `wa30` +4.8,
`cn04` +2.5 — against heavy losses on `sb26` −46.8, `sp80` −28.8, `ar25` −15.8,
`ka59` −11.0. So the aggregate again hides two-directional movement, exactly as the
labelled grid did (12 Sept). **No level was cleared anywhere**, so none of this
registers on the primary metric.

**`r11l` again.** 31B cleared level 1 in **0 of 5 seeds**; random clears it in 5 of 5.
Both frozen models fail the one level random reliably beats, which is the clearest
statement of the problem E1 has to attack.

**Cost, and why the seed split was necessary rather than prudent.** Median **90.1 s
per call** (min 85.0, max 97.7) against the probe's 13.4 s — 6.7× slower, because 17
game processes contend for a KV cache holding about four concurrent 20k-token
requests. Play was 5.95 h (e012) and 3.98 h (e34) at ~420 s per episode. **A single
85-episode kernel would have needed ~9.9 h of play plus a 10-minute load, over
Kaggle's 9 h limit.** The 12 Sept projection of ~6.5 h was optimistic by 50%; the
pessimistic case in that note was the real one. GPU quota: ~10 h for the pair,
~13.6 h of 30 used this week.

**Tooling caveat — `top_action_share` counts the action name, not the move.** 25 of
85 episodes read ≥ 0.95, all on `bp35`, `lp85`, `r11l` and `sb26`, and that means
"clicked on nearly every turn", not "played one move repeatedly": `r11l` reads share
1.00 while visiting 98.5 distinct states per 100 actions, so its coordinates varied
every turn. Qwen3-8B's collapse was a different thing — `ACTION6 15 15` eighty times
at 1.2 states/100. **Do not compare the two conditions on this field**; read it with
states/100 beside it, or count distinct `(action, x, y)` triples instead.

**Read for E0.** The baseline characterisation is done at both tiers and the answer
is negative on the primary metric: a frozen open-weight SLM with a minimal scaffold
does not clear a level that random does not also clear, at 8B or at 31B. E0's dense
metrics carry the comparison, as the 11 Sept amendment required. E1 now has its
control, and its bar is `max_level_cleared` on the 16 verdict games, not RHAE.

### Correction, 17 Sept 2026 — the random floor was inflated by a replay bug

The amendments above are left as written; this corrects them. `e0_random_smoke.py` made one environment per game and played every episode on it. `env.reset()` keeps level progress, so once an episode cleared level 1, every later episode of that game started past it and counted its first action as a clear. Found 17 Sept while checking E4's implausible 1-action clears; fixed to one environment per episode, with a regression test (`tests/test_e4_random_prune.py::test_each_episode_starts_at_level_one`).

**Which results it touched.** Only episodes that followed a clear *in the same game and
process*. Every frozen-model run cleared nothing, or only in its last episode, so
**E0 v2, 31B, Qwen3-8B, E1 and E2 model results are unaffected.** The **random
baselines** and **Gemma-4-E4B v1's `r11l`** were not.

| Claim above | As written | Corrected (fresh environment per episode) |
| :-- | :-- | :-- |
| Random floor, 16 verdict games, 80 actions, seeds 0–4 | levels/game **0.037** (3 clears, all `sp80`) | **0.0125** (1 clear: `sp80` seed 2) |
| Same, RHAE | 0.1539 | **0.0348** |
| Same, states/100 | 78.7 | 78.5 |
| "Random clears `r11l` level 1 in 5/5 seeds" | 5/5 | **1/5** (seed 0, in 17 actions) |
| E4B v1 "cleared `r11l` level 1 in every seed" (12 Sept) | 5/5 | **1 real clear** (seed 0); seeds 1–4 were played from level 2, never re-run, so unknown |
| 11 Sept pre-check, `r11l` "both episodes" | 2/2 | **1/2** |

Corrected numbers are seeds 0–4 of `experiments/e4_random_80.json` (fixed code). At
20 seeds the 80-action floor is 0.019 levels/game (6 clears).

**What changes in E0's reading.** Frozen models (0.000) are still not above random,
but the gap is **one clear, not three**. "Both frozen models fail the one level random
reliably beats" (16 Sept) is **withdrawn**: random clears `r11l` level 1 in one seed
of five, and E4B v1's "every seed" rests on one real clear. `r11l` stays outside verdict aggregates — its seed-0 clear in
17 actions is still faster than the human baseline of 22 — but not because random
clears it reliably. `e0_random_heldout_80.json` and `e0_random_floor.json` are kept
unmodified as the record of what was read at the time.

---

## E1 — Trajectory memory (H5 + H6, one treatment)

Merged on the peer review's argument that these are one experiment. They remain
two mechanisms; they are tested as one harness with two switches, because running
them apart doubles the compute for a distinction the metric may not resolve.

| | |
| :-- | :-- |
| **Hypothesis** | an agent that (a) recognises it has returned to a visited state and prunes that branch, and (b) converts a failure episode into a rule that persists across resets, solves levels in fewer actions and dies the same death less often than the same model without those stores. |
| **Baseline** | E0. |
| **Treatment** | harness holding a visited-state signature set (within episode) and a failure→rule store (across resets). Model weights, prompts and decoding identical. |
| **Switches** | `--prune-visited` (H5), `--failure-rules` (H6). Four cells: off/off = E0, on/off, off/on, on/on. |
| **Primary metric** | actions-to-solve on held-out games. |
| **Secondary** | repeat-hazard rate after first failure (E proxy); distinct states per 100 actions (C proxy). |
| **Falsified if** | on/on does not beat off/off on actions-to-solve by more than the baseline seed spread, on held-out, at N = 5. |
| **Partially supported if** | exactly one switch carries the effect. Then the two mechanisms are *not* one experiment after all, and the register is amended to say which. |
| **Abandoned if** | > 40 GPU-hours, or the delta is still inside noise after N = 10. |
| **Expected cross-cluster cost** | C may fall — pruning removes exploration. Record it; do not treat a C regression alone as failure. |
| **Prior art to beat** | PRO-LONG argues the opposite of H6 — retain the complete log and search it with code rather than consolidating it into rules. If `--failure-rules` shows no effect, that is *evidence for* PRO-LONG, and should be written up as such rather than as a null. |

**Status:** not started. Next after E0.

### Amendment, 16 Sept 2026 — E1 pre-registration, fixed before any E1 run

E0 closed negative at both tiers (amendment of 16 Sept above). Four things in the
block as first written cannot survive that result; they are replaced here, before
any treatment plays a game. Genesis task `T-E1a`; human decisions `DECISION-17bcf9bb`
(falsifier) and `DECISION-e3978a7e` (model size).

**1. Primary metric: levels cleared on the 16 verdict games**, the analyzer's
levels/game (mean over seeds per game, then over games; `r11l` shown but outside).
Actions-to-solve is undefined while the control clears nothing: Gemma-4-E4B cleared
0 levels in 80 verdict episodes. It stays a secondary wherever a level is cleared.

**2. Falsifier, replacing "beats off/off by more than the seed spread".** The
control's spread is zero, so that line would pass on one lucky clear.

| Outcome | Condition (held-out, N = 5, 16 verdict games) |
| :-- | :-- |
| **Supported** | on/on levels/game beats **both** off/off (0.000) **and** random (0.037) |
| **Weak** | beats off/off, not random — reported as partial, not as a working agent |
| **Falsified** | does not beat off/off |

Random's 0.037 is 3 clears in 80 episodes, all on `sp80`; beating it takes **at
least 4 clears**. "Partially supported if exactly one switch carries the effect"
stands, judged on the same metric.

**3. Model: Gemma-4-E4B first.** Three treatment cells at 31B cost ~30 GPU-h at
~420 s per episode — the abandon line with tune runs, and more than the week's
quota. At E4B the three cells cost ~4–5 GPU-h. 31B runs only if E4B shows an
effect. **off/off reuses the E0 E4B v2 held-out run** (`e0-out-gemma4-e4b-v2`),
valid because with both switches off the prompt, decoding and seeds are
byte-identical to E0; a test pins this.

**4. What each switch does — "prompts identical" is amended for H6.**

- `--prune-visited` (H5, harness only, prompt unchanged). Within an episode the
  harness learns which moves change nothing: a move whose resulting frame equals
  the frame it was made from is *dead* for that frame. A keyboard move is keyed by
  `(frame, action)`; a click by `(frame, ACTION6, colour of the clicked cell)`, so
  one dead click on a colour predicts the rest of that colour dead in that frame.
  If the model names a dead move, the harness substitutes a random legal move not
  known dead; if every move is dead, the model's choice stands. **Substitutions
  are counted and reported per episode.** They are not an exclusion rule — they are
  the treatment — but an on/off gain carried by a high substitution rate is partly
  random play, and is to be read against random, not only against the control.
  **Known ceiling, found before any run:** the key is the exact frame, so a game
  with a clock defeats it. `dc22` flips one cell every second action whatever the
  move; a dead click is caught only on the off-beat, and the next frame is always
  new, so the dead set rarely re-applies (local check, fixed click: 39 substitutions,
  states/100 unchanged at 50.0; on `sc25` the same check lifts 42.5 → 70.0). Masking
  clock cells would be a scaffold change; it is not made for E1, and a null on
  clock games is to be read with this in mind.
- `--failure-rules` (H6, prompt changes). On each GAME_OVER within an episode the
  harness writes one fixed-wording rule — the attempt's number, its length in
  actions, and its last three moves — and appends the most recent five rules to the
  system message on every later turn. No extra model calls. With the switch off, or
  before the first death, the prompt is unchanged. Deaths occur in 7 of 16 verdict
  games (`bp35 cn04 lf52 r11l sp80 su15 vc33`), so H6 can act only there.

Both stores are empty at the start of each episode (a new `LLMBaseline` per episode),
so no information crosses seeds.

**Prior art — Reki (2nd, Milestone 1).** Reki's dead-signature detection stops clicks
on *object types* that never respond; `--prune-visited`'s colour key is the nearest
equivalent this harness can compute without object segmentation, and is coarser for
it. Reki refreshes a *model-written* reflection memory every ~10 steps;
`--failure-rules` is harness-written and fires only on death, so it costs no calls
and tests a narrower claim. If E1 is supported, the write-up credits Reki with the
mechanism class and claims only the measurement.

**Secondaries** as first registered: repeat-hazard rate after first failure,
states/100, plus substitution rate and rules written. Actions-to-solve where defined.

**Execution.** A tune-split probe first — Gemma-4-E4B, all four cells, 1 seed, 80
actions, on `dc22` (the dead-click game of the 12 Sept diagnostic) and `sc25`, `tu93`
(random dies once in every seed of both). It checks the switches fire on the real
engine and the scaffold stays clean; it is not evidence either way. The held-out run
(three treatment cells × 17 games × 5 seeds × 80 actions) is a separate task.

### Amendment, 16 Sept 2026 — E1 tune probe: the switches fire, the scaffold is clean

Kernel `arc-agi-3-e1-probe-e4b`, status `ok`: Gemma-4-E4B, tune games `dc22 sc25
tu93`, 1 seed, 80 actions, all four cells on one vLLM load. vLLM ready in 220 s,
play 415 s for 12 episodes. **0 parse failures** in 960 calls. Gate
`--verify-output` passes: each switch acted only where it was on.

| cell | `dc22` states/100 | `sc25` | `tu93` | dead moves | substitutions | rules | levels |
| :-- | --: | --: | --: | --: | --: | --: | --: |
| off-off | 65.0 | 50.0 | 92.5 | 0 | 0 | 0 | 0 |
| on-off | 56.3 | 68.8 | 91.3 | 60 | 32 (13.3%) | 0 | 0 |
| off-on | 65.0 | 50.0 | 90.0 | 0 | 0 | 1 | 0 |
| on-on | 56.3 | 68.8 | 90.0 | 60 | 32 (13.3%) | 1 | 0 |

**A mechanism check, not evidence for or against E1** — one seed, tune games. Read
only for what the switches do:

- **Pruning moves exploration both ways**, as the clock ceiling predicted: `sc25`
  50.0 → 68.8, `dc22` 65.0 → 56.3. It never fires on `tu93` (0 dead moves: every
  keyboard move changes the frame).
- **H6 barely engaged.** The model died once in 12 episodes (`tu93`), where random
  dies once in every seed of `sc25` and `tu93`. Frozen E4B dies less than random, so
  on held-out the failure-rule store may see few deaths to learn from. That is a
  reason `--failure-rules` could read null for lack of input rather than lack of
  effect; the held-out report must give deaths per cell beside any H6 claim.
- **Replay is not exact under batching.** `off-on` on `dc22` wrote no rule, so its
  prompts were identical to `off-off`'s, yet its action counts differ (ACTION2 8 vs
  6, ACTION6 48 vs 49) and it happened to reach the same states/100. Other identical-prompt pairs
  (`sc25` off-off/off-on, `dc22` and `sc25` on-off/on-on) replayed exactly. Per-call
  seeds do not make vLLM bit-deterministic when batch composition changes. So the
  reused E0 off/off run is **a draw from the control's distribution, not its replay**
  — which the falsifier already tolerates, since it also requires beating random.

### Amendment, 17 Sept 2026 — E1 held-out verdict at E4B: weak, carried by pruning alone

Kernel `arc-agi-3-e1-heldout-e4b`, status `ok`: Gemma-4-E4B, 17 held-out games × 5
seeds × 80 actions, cells `on-off off-on on-on` on one vLLM load; off/off is the E0
E4B v2 run, as pre-registered. 255 episodes, **0 excluded**, 0 parse failures. Play
2.42 h (median 22.3 s per call at 51 processes, against E0's 12.3 s at 17 — serving
only). `--verify-output` passes.

| Verdict games (16) | random | off-off | on-off | off-on | **on-on** |
| :-- | --: | --: | --: | --: | --: |
| levels/game | 0.037 | 0.000 | 0.013 | 0.000 | **0.013** |
| level clears | 3 (`sp80`) | 0 | 1 (`lp85`) | 0 | **1 (`lp85`)** |
| states/100 | 78.7 | 68.6 | 74.4 | 69.6 | **74.5** |
| RHAE | 0.1539 | 0.0000 | 0.0044 | 0.0000 | 0.0044 |
| deaths / repeat hazards | 32 / 0 | 29 / 1 | 33 / 1 | 34 / 1 | 34 / 2 |
| rules written | — | 0 | 0 | 34 | 34 |
| substitution rate | — | — | 12.2% | — | 12.1% |

> **Verdict under the pre-registered falsifier: WEAK.** on/on beats off/off
> (0.013 > 0.000) but not random (0.013 < 0.037; 1 clear where ≥ 4 were needed).
> It is reported as partial, not as a working agent.

**Partially supported, in the sense the block defines: exactly one switch carries
it.** on-off and on-on give the same result: each clears `lp85` level 1 on seed 4 at
the 48th action with the same states/100 (substitutions 51 vs 52, so near-identical
rather than identical play; 43 of 85 episodes replay exactly across the two cells).
The rules on-on adds change almost nothing. off-on moves nothing. So H5 and
H6 are **not one experiment**: pruning does all of it, failure rules none.

**The one clear is mostly random play.** The `lp85` episode that cleared had a
substitution rate of 64% (the game's mean is 67–70%): the model clicked dead cells
on most turns and the harness swapped in random live ones. Random alone clears
`lp85` in 0/5 and visits 3.8 states/100 there, so the clear needs both the model's
choices and the swaps — but it cannot be credited to the model's judgement. Read, as
the pre-registration asked, against random.

**Where pruning is real: exploration (cluster C).** states/100 rises 68.6 → 74.4,
closing 57% of the gap to random. It is concentrated in the click games with the
most dead clicks, and on two it passes random: `sb26` 18.8 → 56.0 (random 53.5),
`lp85` 1.2 → 15.0 (random 3.8); also `ar25` 43.2 → 64.8, `cn04` 56.0 → 65.8,
`su15` 56.0 → 67.2. Keyboard-only games do not move (substitution ≈ 0%), as the probe
predicted. The clock ceiling did not sink it on held-out.

**H6 is null, and a weak test.** The store was not starved — 34 deaths, 34 rules —
but the failure it targets barely happens: the control repeats a death **once in 85
episodes**, so "dies the same death less often" had nothing to reduce. states/100
69.6 vs 68.6 is inside noise. Per the block, a `--failure-rules` null counts as
evidence for PRO-LONG over rule consolidation; at 80 actions it is thin evidence,
because repeated deaths are too rare to measure either way.

**`r11l` again:** 0/5 in all three cells; random 5/5.

**Cost.** ~2.6 GPU-h (probe ~0.25 h + this run). E1 total well inside the 40 GPU-h
abandon line.

**What the register allows next** (a human decision, not taken here): *weak* permits
N = 10 before abandoning. Two cautions for that choice — the only level gained is a
64%-substituted one, and an H5-only follow-up would drop H6, which this run already
answered. The 31B tier is not triggered: DECISION-e3978a7e requires an effect at E4B,
and a weak result below random is not one.

### Amendment, 17 Sept 2026 — E1 stopped

**Human decision (`DECISION-200ac78f`): E1 ends at the E4B verdict.** N = 10 is
declined and the 31B tier is not run. The one level gained was 64% substituted
random play; more seeds would measure the same thing more precisely without making
it the model's. Genesis `T-E1a` and `T-E1b` are complete.

**What E1 leaves behind:**

1. **Pruning dead moves is an exploration fix, not a solving fix.** It closes 57% of
   the click-game exploration gap to random at E4B and passes random on `sb26` and
   `lp85`, but it did not lift levels past the random floor.
2. **H5 and H6 are separate mechanisms** — the merge on the peer review's argument
   did not hold; any future memory experiment tests them apart.
3. **At 80 actions, "dying the same death twice" is too rare to test** (1 repeat in
   85 control episodes). A failure-memory hypothesis needs a longer budget, or a game
   subset where deaths repeat, before it can be falsified.
4. **The switches stay in the harness**, off by default and pinned byte-identical to
   E0, so a later experiment can reuse `--prune-visited` as a component.

**Status:** stopped, 17 Sept 2026. Weak, partially supported (H5 only).

### Correction, 17 Sept 2026 — the random bar was lower than the verdict used

The random floor the E1 pre-registration and verdict used (0.037 levels/game, "≥ 4
clears to beat") was inflated by a replay bug; see the E0 correction of the same date.
**The corrected floor at 80 actions, seeds 0–4, is 0.0125: one clear**, so beating
random needed **≥ 2** clears, not ≥ 4.

**The verdict does not change.** on/on's 1 clear (`lp85`, seed 4 — the last episode,
so untouched by the bug) now **ties** random instead of trailing it. The falsifier
requires on/on to *beat* random, so E1 remains **weak**. The E1 model runs themselves
are unaffected: no model cleared a level before its last episode.

**Two sentences above are withdrawn:** "random 0.037 = 3 clears, all `sp80`" (it is
one clear) and "`r11l` again: 0/5 in all three cells; random 5/5" (random is 1/5).

---

## E2 — Controllability probe (H3)

| | |
| :-- | :-- |
| **Hypothesis** | spending the first *k* actions deliberately identifying which on-screen object responds to input lowers total actions to solve, relative to spending those same *k* actions on the task. |
| **Baseline** | E0, and additionally a *matched-budget* control: E0 given the same *k* extra actions with no probe instruction. This separates "the probe helped" from "more actions helped". |
| **Treatment** | first *k* actions driven by a controllability probe; *k* ∈ {5, 10, 20} swept on tune games only, fixed before held-out. |
| **Primary metric** | total actions-to-solve, held-out. |
| **Secondary** | actions-to-controllable-ID; A proxy (levels reached on first contact). |
| **Falsified if** | the probe does not beat the matched-budget control outside seed spread. Beating plain E0 while losing to the matched control means the probe bought nothing — the extra actions did. |
| **Abandoned if** | > 25 GPU-hours, or no *k* separates from the control on tune games. |
| **Live threat, stated in advance** | Gibson's affordance account holds that controllability is perceived directly in the act of looking, not established by a separate identification phase. If E2 nulls, that is the likelier explanation than a bad implementation, and it should be written up that way. Tycho's finding that high transition-model accuracy did not translate into action-selection gains points the same direction. |
| **Coverage caveat** | H3 has the thinnest support in the shortlist — 6 papers — and the corpus is known to under-sample ARC-AGI-3. Treat H3 as *not found in this corpus*, never as *unclaimed in the field*. |

**Status:** not started. Runs only if E0 yields a usable floor.

### Amendment, 12 Sept 2026 — H3 and the affordance account (filed 17 Sept)

*Written 12 Sept in `cluster_origins.md` §4 (commit `b941e9e`) with the instruction
that it belongs here; it was not copied across until 17 Sept. Text unchanged.*

> The affordance literature holds that a control relation is a relation between an
> agent's abilities and the environment's features, not a property of an object
> (Chemero 2003; Davis 2020). If that transfers, H3's premise — that
> controllability is identified once, in an opening phase — is **mis-specified
> rather than wrong**: what an agent can identify is a relation conditional on state
> and repertoire, and a relation found at level 1 need not hold at level 3. **This is
> not yet grounds to revise H3.** No source in this corpus engages Gibson's premise
> directly; cluster D's review literature is Information Systems affordance theory,
> and the corpus is known to under-sample ecological psychology, whose overviews are
> books this method cannot reach. Treat as *not found in this corpus*, not as
> *unclaimed*.
>
> **What follows for E2 regardless.** Instrument H3 so the two readings are
> distinguishable: re-test controllability at every level rather than once per game,
> and record how often a control relation learned at level *n* still holds at level
> *n+1*. If it usually holds, the one-off phase is defensible and the affordance
> objection does not bite. If it usually does not, a null result for E2 reads as *H3
> mis-specified*, not as an implementation failure. That measurement costs one extra
> field in the run log.

### Amendment, 17 Sept 2026 — E2 pre-registration, fixed before any E2 run

E0 and E1 closed with no frozen condition above the random floor on levels. The E2
block as first written has four parts that cannot survive that; they are replaced
here before any probe plays a game. Genesis task `T-E2a`; human decision
`DECISION-4f50991f`.

**1. Primary metric: levels cleared on the 16 verdict games** (analyzer levels/game,
`r11l` shown but outside). Actions-to-solve is undefined while the control clears
nothing; it stays a secondary wherever a level is cleared.

**2. Falsifier, with the matched control the block required.**

| Outcome | Condition (held-out, N = 5, 16 verdict games) |
| :-- | :-- |
| **Supported** | `probe-k` levels/game beats **both** `match-k` **and** random at 80 + k actions |
| **Weak** | beats `match-k`, not random — reported as partial |
| **Falsified** | does not beat `match-k`. Beating plain E0 while not beating `match-k` means the extra actions did it, not the probe |

Random at 80 + k is measured locally (CPU) before the held-out verdict, because the
80-action random floor under-counts a longer budget.

**3. Tune rule, replacing "abandoned if no k separates on tune".** Levels cannot
separate on tune (E4B clears none), so the tune metric is the **dead-move rate**: the
share of the *model's own* moves whose resulting frame equals the frame they were
made from. Knowing what responds should lower it directly. Probe moves are excluded
from it. For each k ∈ {5, 10, 20}, 8 tune games × 3 seeds: take the per-seed mean
over games for `probe-k` and `match-k`. **k separates** if `probe-k`'s mean is below
`match-k`'s mean by more than `match-k`'s seed range (max − min). Of the separating
k, choose the largest margin; ties go to the smaller k. **None separates → E2 is
abandoned**, and the tune result is the write-up. The rule is implemented as
`e0_analyze.py --pick-k` and run as a gate, so the choice is mechanical. The E1 clock
ceiling applies: on `dc22` a game clock hides dead moves in both cells alike.

**4. The probe is harness-driven** (not a model instruction — E0 showed E4B cannot
reliably follow click instructions, so a model-driven probe would mostly measure
instruction-following). With `--probe k`, the first k actions of each level are
chosen by the harness, with no model call: each available simple action once, then
one click per distinct colour on screen, largest colour area first, cycling if k is
longer than that list. For each probe move the harness records the changed cells —
count, bounding box, colours before and after, and whether it ended the game — and
the model sees one fixed-wording line per move in its system message for the rest of
the level. On a new level the probe re-runs and its summary replaces the old one;
that is the per-level re-test the 12 Sept amendment asked for. `match-k` has no probe
and 80 + k model actions. With `--probe` off the prompts are byte-identical to E0
(pinned by `tests/test_e1_switches.py`).

**Known ceiling, found before any run: on-screen counters blur the probe.** Checked
locally on the real engine: most tune games draw a step counter or timer that
changes on every move, and the probe reports one bounding box over *all* changed
cells. So an object's move is merged with the counter's tick — `ls20`'s ACTION1
reads "52 cells changed in x 13-38, y 40-62" for a small move; `dc22` adds one cell on
row 63 to every line. The probe still separates "nothing changed" from "something
changed" (`ft09`'s clicks, half of `dc22`'s), which is what the dead-move metric
tests. Splitting changes into connected regions would sharpen it; that is a scaffold
change and is not made. A null is to be read with this in mind, alongside the
undistinguishable-null statement below.

**Stated in advance: the affordance instrument will read empty.** It needs a level
cleared to compare a relation at level *n* with level *n+1*, and no frozen
condition has reached level 2 of a verdict game. So **an E2 null cannot distinguish
a bad probe from H3 mis-specified**, and will be written up as undistinguished — not
as evidence for either.

**Model and budget.** Gemma-4-E4B (per `DECISION-e3978a7e`). Tune sweep ~2–2.5 GPU-h;
held-out (`probe-k`, `match-k`, 17 × 5) ~2.5 GPU-h, as a separate task. E2's 25 GPU-h
abandon line stands.

### Amendment, 17 Sept 2026 — E2 abandoned at the tune rule: the probe raises dead moves

Kernel `arc-agi-3-e2-tune-e4b`, status `ok` (after a long queue for the GPU; play 2.58 h):
Gemma-4-E4B, 8 tune games × 3 seeds, six cells, 144 episodes, no episode above 20%
parse failures. `--verify-output` passes. **`e0_analyze.py --pick-k`: no k separates →
E2 is abandoned**, as pre-registered. No held-out run.

| k | probe-k dead-move rate (per seed) | match-k (per seed) | margin | match range | separates |
| :-- | :-- | :-- | --: | --: | :-- |
| 5 | 0.344 (.361 .339 .333) | 0.284 (.290 .290 .274) | **−0.060** | 0.016 | no |
| 10 | 0.321 (.319 .323 .320) | 0.303 (.321 .279 .310) | **−0.018** | 0.042 | no |
| 20 | 0.333 (.342 .331 .325) | 0.293 (.316 .282 .280) | **−0.040** | 0.036 | no |

**The sign is wrong, not just small.** At every k the probed model wastes *more* of its
own moves than the matched control; at k = 5 by more than three times the control's
seed range. No level was cleared in any cell. Deaths 12 per probe cell vs 9 per match
cell.

**By game it is two-directional**, as E0's and E1's aggregates were:

- **`sk48` carries the loss.** Dead-move rate 0.47–0.56 → **0.90–0.96**, states/100
  41–49 → 10–13 at every k: after the probe summary the model settles on moves that do
  nothing.
- **Where it helps, it helps exploration, not dead moves.** `s5i5` states/100 50–59 →
  98 at every k (dead-move rate 0 in both); `tn36` 61–68 → 89–94 at k = 10, 20; `sc25`
  30–50 → 65–66 at k = 10, 20, with its dead-move rate also lower (0.35–0.38 vs
  0.53–0.69). Overall states/100 is higher with the probe at k = 10 (66.3 vs 58.7) and
  k = 20 (65.2 vs 57.8) — but states/100 counts the probe's own moves, so it flatters the
  probe cells and is not the registered tune metric.
- **Unmoved:** `ft09` (≈ 1.0 dead in both — clicks there change nothing visible), `ls20`
  (≈ 100 states/100 in both), `tu93`.

**The affordance instrument read empty, as stated in advance:** 24 probe runs per cell,
one per episode — no level was cleared, so no re-probe happened and no relation could
be compared across levels.

**Reading.** Telling a frozen E4B what each of its moves changed does not make it waste
fewer moves; on one game it makes it much worse. Per the pre-registration this null
**does not distinguish a bad probe from H3 mis-specified**. Two concrete candidates for
"bad probe" were named before the run and remain untested: the step-counter blur in the
bounding boxes, and cycling repeats of an already-described move at k = 10, 20. The live
threat logged in the block — Gibson's account, and Tycho's finding that transition
knowledge did not become better action selection — fits the result at least as well,
and is recorded here as unrefuted, not as supported.

**Cost:** ~2.7 GPU-h. **Status: abandoned at tune, 17 Sept 2026.**

---

## E3 — Epistemic vs instrumental action labelling (H2) — parked

Recorded so the decision is visible, not run this milestone.

| | |
| :-- | :-- |
| **Why parked** | H2 is claimed and named on this benchmark. Tycho calls it "active abstraction"; OPINE-World supplies a quantified signal (Bayesian ontology error steering exploration). Reproducing a claimed mechanism costs the same compute as testing an open one and returns less. |
| **Unparked if** | E1 and E2 both null, and a mechanism with published traction is needed to establish the harness works at all. |

### Amendment, 19 Sept 2026 — E3 unparked by human choice; pre-registration, fixed before any E3 run

**Why now.** The unpark condition is **not met** — E1 was weak, not null — so E3 runs
by explicit human decision (`DECISION-792aefcb`), not by the rule. The reason for
parking still stands: this is a claimed mechanism, and reproducing it on a small
frozen model is expected to return less than a new one would. Genesis task `T-E3a`.

**Expectation, stated in advance.** A null is the likelier outcome: E0 showed this
model does not use screen information well, and E2 showed that *more* information
made it waste more moves. The published results came from far stronger models.

| | |
| :-- | :-- |
| **Hypothesis** | a frozen model that marks each move as information-seeking (`LEARN`) or goal-seeking (`WIN`), and sees a record of what its own `LEARN` moves did, clears more levels than the same model without either. |
| **Baseline** | E0 (Gemma-4-E4B v2). With `--learn-labels` off the prompts are byte-identical to E0 (pinned by `tests/test_e1_switches.py`), so the E0 held-out run is the control. |
| **Treatment** (`--learn-labels`, option B) | The system message asks the model to start its reply with `LEARN` or `WIN`. After each `LEARN` move the harness records what changed on screen, in E2's fixed wording (count, bounding box, colours, game over), and the system message shows the **last 5** such records. `WIN` moves are not recorded. A reply without a label is played as usual and counted (`label_missing`); labels do not change which action is parsed. |
| **Difference from E2** | E2's harness chose the test moves; here the **model** chooses what to test. That is the mechanism being tested. |
| **Tune rule (T-E3a)** | 8 tune games × 3 seeds, `labels-on` vs `labels-off` in one kernel. Per seed, the mean dead-move rate over games (model moves that change nothing). **Go** to held-out only if `labels-on`'s mean is below `labels-off`'s by more than `labels-off`'s seed range; otherwise **stop at tune**. Implemented as `e0_analyze.py --e3-tune`. |
| **Falsifier (held-out, T-E3b)** | 16 verdict games, N = 5, 80 actions. **Supported** if levels/game beats both the control (0.000) and the corrected random floor (0.0125 — at least 2 clears). **Weak** if it beats the control only. **Falsified** otherwise. |
| **Secondary** | share of `LEARN` vs `WIN` labels, labels missing, experiments logged, dead-move rate, states/100, deaths. |
| **Known ceilings** | E2's step-counter blur applies to the logged descriptions. |
| **Budget** | tune ~1 GPU-h, held-out ~1.5 GPU-h; abandoned if > 10 GPU-h. |

### Amendment, 19 Sept 2026 — E3 stopped at the tune rule: labels raise dead moves, and are mostly not used

**A first kernel played nothing.** Version 1 of `arc-agi-3-e3-tune-e4b` ended
`play_incomplete` with 0 episodes: since E4, `e0_random_smoke.py` imports
`agents.random_prune`, which `e0_kernel.py` did not ship, so every game process died
on import (~6 GPU-minutes, the vLLM load). No E3 data was produced. Fixed by shipping
the file, and `--check` now fails if a shipped file imports an `agents` module that is
not shipped (commit `19830d8`).

**Result.** Version 2, status `ok`: Gemma-4-E4B, 8 tune games × 3 seeds, `labels-on`
vs `labels-off`, 48 episodes, play 53 minutes. `--verify-output` passes. One
`labels-on` episode exceeded 20% parse failures and is excluded, as pre-registered.
**`e0_analyze.py --e3-tune`: STOP at tune.**

| Tune games, 3 seeds | labels-on | labels-off |
| :-- | --: | --: |
| dead-move rate per seed | 0.427, 0.284, 0.316 | 0.308, 0.255, 0.322 |
| mean | **0.342** | 0.295 |
| states/100 | 59.0 | 61.7 |
| level clears | 0 | 0 |

The rule needed `labels-on` below `labels-off` by more than 0.067 (the control's seed
range); it is **0.047 above**. Same sign as E2.

**The treatment was mostly not taken up.** Of 1,920 replies, 385 were labelled `LEARN`
(20%), 255 `WIN` (13%) and **1,280 carried no label (67%)**. The experiment log was
therefore built from about a fifth of moves. This is a weaker test than designed: the
honest reading is *this model does not reliably follow the labelling instruction, and
where it did the result was no better* — not that the mechanism fails.

**`sk48` again.** Dead-move rate 0.42 → 0.70, states/100 55 → 26 with labels — the
same game that carried E2's loss. Twice now, extra instruction or text in the prompt
has pushed this model into repeating do-nothing moves on `sk48`.

**Reading.** Consistent with the stated expectation (a null), and with E0 and E2: this
frozen E4B does not turn more prompt structure into better play. E3 is **stopped at
tune**; no held-out run (T-E3b is not created). Cost ~1 GPU-h including the failed
first kernel.

**Prior art to compare against next.** Tufa Labs' Duck Harness, the Milestone 1
winner, gets far further with a frozen open-weight model (Qwen 3.6 27B FP8) by a
different interface: the model writes Python against game state exposed as variables,
including object segmentation and before/after transitions, and issues several
actions per call. It is the natural comparison for this register's scope, and is
queued as the next thing to examine.

---

## E4 — Random play with dead-move pruning (no model)

Written 17 Sept 2026, before any E4 run. Genesis task `T-E4a`; human decision
`DECISION-fd4761c5`.

**Why this, now.** E0–E2 found no frozen model above the random floor on levels, at
8B or 31B, with or without memory or a controllability probe. The one harness
component that moved anything was E1's `--prune-visited`, and its only level clear
was 64% random substitutions. So the question worth a few CPU-hours is whether the
pruning helps *random* play directly. It is also the only candidate that could
improve the submission (a random agent, RHAE 0.07 on the hidden set) before Milestone
2 on 30 Sept.

| | |
| :-- | :-- |
| **Hypothesis** | random play that never repeats a move already known to leave the current frame unchanged clears more levels than plain random play at the same action budget. |
| **Baseline** | plain random (`e0_random_smoke.py`, policy unchanged since the 11 Sept pre-check; pinned by test). |
| **Treatment** | `--policy random-prune`: the same uniform draw over the frame's available actions, with E1's dead-move key — `(frame, action)` for keys, `(frame, ACTION6, colour clicked)` for clicks — redrawn up to 64 times while the draw is known dead; if every draw is dead, the last stands. Until the first dead move is hit it consumes the random stream exactly as plain random, so the two conditions start identical per seed. |
| **Games, seeds, budgets** | 17 held-out games × **20 seeds** (episodes 0–19, above the register's N = 5 minimum because random clears are rare and CPU is cheap) × budgets **80** and **300** actions. **300 is primary**: the submission caps at 80 while the 9 h limit allows ~4.9 min per game, so 80 understates what a random-family entry can use. 80 is reported for comparability with E0–E2. |
| **Primary metric** | levels cleared on the 16 verdict games (`r11l` shown, outside). |
| **Falsifier (300 actions)** | per seed *s*, D_s = (levels cleared by random-prune) − (levels cleared by random), summed over the 16 verdict games. Drop ties. **Supported** if a one-sided sign test on the D_s gives **p < 0.05** *and* random-prune's total clears exceed random's. **Falsified** otherwise. The same test at 80 actions is reported, not decisive. |
| **Secondary** | RHAE mean over the 16 verdict games and over all 17 (the competition's metric); states/100; actions per cleared level; dead moves learnt and redraws. |
| **Known ceiling** | E1's: exact-frame identity is defeated by on-screen clocks and step counters, so on those games pruning rarely fires and the two conditions stay close. |
| **Execution** | local CPU only, no GPU or Kaggle quota; results saved to `experiments/e4_{random,prune}_{80,300}.json`; the verdict is printed by `e0_analyze.py --e4-verdict experiments`. A test re-plays one saved episode to prove the files came from this code. |
| **If supported** | a separate task, with its own approval, puts random-prune into the submission and raises its action cap. Not before. |
| **If falsified** | recorded here and carried into the E0–E2 write-up due by the 23 Sept freeze. |

**Status:** pre-registered 17 Sept 2026; not run.

### Amendment, 17 Sept 2026 — E4 verdict: supported at 300 actions, carried by one game

**First run discarded, and why.** The first E4 run read *falsified* at 300 and
*supported* at 80. Its data had 1-action and 0-action level clears, which cannot be
real. Cause: `e0_random_smoke.py` made one environment per game and played every episode on it. `env.reset()` keeps level progress, so once an episode cleared level 1, every later episode of that game started past it and counted its first action as a clear. Found 17 Sept while checking E4's implausible 1-action clears; fixed to one environment per episode, with a regression test (`tests/test_e4_random_prune.py::test_each_episode_starts_at_level_one`). All four E4 files were deleted and re-run on the fixed code before
this verdict. The discarded verdict was seen; the pre-registered test and budgets
were not changed after seeing it.

**Result (fixed code), 17 held-out games × 20 seeds.** `e0_analyze.py --e4-verdict
experiments`:

| Budget | random clears | random-prune clears | seeds won / lost / tied | one-sided p | Verdict |
| :-- | --: | --: | :-- | --: | :-- |
| **300 (primary)** | 19 | **38** | 18 / 0 / 2 | < 0.0001 | **SUPPORTED** |
| 80 (reported) | 6 | 12 | 6 / 0 / 14 | 0.016 | supported, not decisive |

| 300 actions | random | random-prune |
| :-- | --: | --: |
| levels/game (16 verdict) | 0.059 | **0.119** |
| RHAE, verdict games | 0.0735 | 0.0824 |
| RHAE, all 17 | 0.0916 | 0.1000 |
| states/100 | 71.0 | 73.1 |
| dead moves learnt / redraws | — | 14,128 / 78,291 |

> **E4 is supported at the primary budget: random play that skips moves known to
> change nothing clears twice as many verdict levels as plain random, winning 18 of 20
> seeds and losing none.**

**Read it narrowly — one game carries it.** random-prune clears `lp85` level 1 in
**20/20** seeds against random's **1/20**. On `sp80`, `r11l` and `vc33` both conditions
clear exactly the same episodes (they share the random stream until a dead move is
drawn). The only other difference is `cd82`: random clears it in seed 7, random-prune
in seed 12. `lp85` is the game where E1's pruning also lifted exploration most (1.2 →
15.0 states/100) and where E1's single clear came from.

**It barely moves the competition metric.** RHAE rises 0.0735 → 0.0824, because the
`lp85` clears are slow — 38 to 288 actions against a human baseline of 17 — and RHAE
squares the action ratio. The gain is in *levels reached*, not in efficiency.

**Register stop condition.** "Any experiment beats its falsifier → re-run at N = 10 on
held-out first." E4 ran at N = 20 held-out from the start, so the condition is met by
the run itself; the one-game concentration is the caveat to carry, not a reason to
re-run. The "if supported" line stands: moving random-prune into the submission is a
separate task with its own approval.

**Status:** supported at 300 actions, 17 Sept 2026.

### Amendment, 17 Sept 2026 — Build 3: E4's policy in the submission, built and rehearsed

Genesis task `T-B3`, human decision `DECISION-4cd8d5d2`. `submission/my_agent.py` now
plays random with dead-move pruning (inlined — the notebook ships one file) and
`MAX_ACTIONS` 300 (was 80). The framework has no post-step hook, so a move is judged
one call later against the screen it was made on; a move that ended the game is never
marked dead. `tests/test_b3_agent.py` drives the agent through the experiment loop
with framework-style frames and asserts **the same episode as E4's `RandomPrune`** on
`lp85`, `sp80` and `ls20` for a shared random stream.

**Local rehearsal of the scored rerun** (`submission/rehearse.py --games
lp85,ls20,r11l --require-level lp85`: reference gateway in competition mode, the real
framework and agent): `lp85` level 1 cleared (score 0.4147), `r11l` level 1 cleared
(0.0254), `ls20` none; **18 ms/action** on Windows with three agents, so 110 games ×
300 actions project to ~10 minutes against the 9 h limit. Kernel built as
`goutham12/arc-agi-3-build-3-random-prune` (private, CPU); **not pushed**.

**What one hidden-set score can and cannot show.** Build 1 scored **0.07** (random, 80
actions). Build 3 changes two things at once. On the public held-out games the cap
does most of the work (random RHAE 0.075 → 0.092 going 80 → 300) and pruning adds a
little (→ 0.100), almost all of it on `lp85`. The hidden set is 110 different games,
so the public gain may not transfer. A Build 3 score above 0.07 cannot be split
between the cap and pruning without a second submission (plain random at 300); a
score at or below 0.07 means neither transferred.

### Amendment, 17 Sept 2026 — Build 3 on the hidden set: 0.07, no visible change

Submission **56309101** (kernel `goutham12/arc-agi-3-build-3-random-prune` v1) scored
**0.07 public**, the same as Build 1's 0.07 (submission 56171083). Kaggle reports the
score to two decimals, both in the leaderboard and through the CLI, so any change
smaller than 0.01 is invisible.

**Reading, as stated in advance:** at this resolution neither the 300-action cap nor
dead-move pruning transferred to the 110 hidden games. On the public held-out games
the combined gain was mean RHAE 0.075 → 0.100 (E4, 20 seeds); whether a gain of that
size would show at two decimals on the hidden aggregate is not known, but a change
that did not move the second decimal is not a submission improvement worth claiming. E4's result
stands on the public games; it is not shown to generalise.

**Consequence.** The planned second submission (plain random at 300) cannot separate
two effects that together did not move the score, so it is not worth a slot. Build 3
remains the entry (not worse, and slightly better on public games).

---

## E5 — Masked state judge inside random + prune (no model)

Written 24 Sept 2026, before any E5 run. Genesis task `T-E5a`; human decision
`DECISION-6efb9578` ("start P1", 24 Sept). Designed as **P1** in
`documents/research_design/next_phase_experiment_design.md` §4; this block is its
pre-registration and wins where the two differ. **Naming:** the register gives the
next free number, E5. The shared pages and the user's handoff copy say "E5 = Duck";
that label came before this block and is not a register number.

**Freeze.** The Milestone #2 stop condition was met by the E0–E4 write-up (23 Sept,
T-W1). This block adds new work; it changes no frozen result, and nothing in it goes
into a submission.

**Why this, now.** E4's pruning key is exact frame identity. E1's probe and E4's
known ceiling showed that on-screen clocks and step counters make every frame new, so
pruning cannot fire on those games. Every later candidate (P3's novelty reward, P4's
graph) depends on the same "did anything change?" judge. The design also found (D1)
that only one of the evaluation safeguards exists in code; this task builds the rest.

| | |
| :-- | :-- |
| **Hypothesis** | pruning with a judge that ignores clock-like cells clears more verdict levels than pruning with exact frame identity, at the same action budget. |
| **Control C0** | E4's `RandomPrune`, unchanged: dead-move key `(exact frame hash, action[, colour clicked])`. Must reproduce E4's saved episodes. |
| **Treatment T1** | the same policy and random stream, with "same frame" decided by the masked hash: key `(masked hash, action[, colour clicked])`. **The only change is the hash.** While the mask is empty, T1 plays exactly as C0 (a test checks this). |
| **Masked judge** | Per episode, a rolling window of the last **W = 16** transitions. For each cell of the **last** layer, count the transitions in the window where its colour changed. A cell is **masked** when it changed in **≥ 14 of 16** **and** those transitions span **≥ 3 distinct action keys**. A cell unchanged for 16 consecutive transitions is unmasked. Nothing is masked before 16 transitions. **Masked hash** = blake2b over every layer with the masked coordinates set to −1, plus the sorted masked coordinates. Parameters fixed a priori; never tuned on tune or held-out. |
| **Deviations from the design** | (1) The design hashes the last layer only; here every layer is hashed, as `frame_signature` does, so an empty mask gives exactly C0's identity. Otherwise T1 would differ from C0 in two things. (2) The design's extra dead-move conditions (not GAME_OVER, `levels_completed` unchanged) are applied only in the **measurement** judge, not the acting key, for the same reason. How often they would have fired is reported. |
| **Common measurement judge** | Both conditions' dead-move rate and distinct states are measured by the masked judge plus the two extra conditions, whichever key the policy acted on. |
| **Safeguards** (built here; any failure voids the run) | fresh environment per episode (exists, tested); episode ID `"E5-{cond}-{game}-{ep}"`, asserted unique per report; after the first `reset()`, the blake2b hash of the frame and `levels_completed` are recorded, with `levels_completed == 0` asserted and one initial hash per game across episodes; any level cleared in **≤ 2 actions** is flagged, and a flagged run is void until inspected; a JSON-lines trajectory per episode (step, action, click, drawn vs redrawn, exact and masked hash before/after, acting verdict, measurement verdict, state, `levels_completed`); no environment reference kept after its episode; one saved episode per condition replayed exactly in the test suite. |
| **Implementation checks** (before any held-out run) | **(i)** synthetic: a counter cell ticking every step in an unchanging world makes every move dead after step 16; in a world that changes only under ACTION1, ACTION1 is never judged dead. **(ii)** `dc22`, tune: its one-cell clock is masked within 32 steps in each of 3 seeds. **(iii)** `ls20`, tune: the step-counter region is masked, and masked distinct states per 100 actions < exact-hash distinct states. **(iv)** safeguards pass; C0 reproduces E4's saved episodes; T1 = C0 while the mask is empty. **(v)** switch check: in C0's trajectories every acting verdict equals the exact-hash verdict. |
| **Games, seeds, budgets** | 17 held-out games; verdict on the 16 (`r11l` shown, outside). Episodes **100–119** (20 seeds, new relative to E4's 0–19; same across conditions, so paired), run seed 0, `Arcade.make(game, seed=0)`. Budgets **300** (primary; resets excluded, as in E4) and **1,000** (secondary). |
| **Primary metric** | levels cleared on the 16 verdict games at 300 actions. |
| **Falsifier (300 actions)** | per seed *s*, D_s = (T1 clears) − (C0 clears), summed over the 16 verdict games. Drop ties. **Supported** if a one-sided exact sign test gives **p < 0.05**, T1's total clears exceed C0's, **and** the concentration rule holds: the result survives removing the game with the largest gain, and ≥ 2 games improve. Failing the concentration rule is reported as "narrow: carried by `<game>`". **Falsified** otherwise. |
| **Secondary** | clears at 1,000 actions (same test, not decisive); dead-move rate and distinct masked states/100 by the common judge; redraws; mean masked cells per game; per-game clears; RHAE on the 16 and on all 17; `r11l`. |
| **Stop / void** | One held-out run, then stop. No change to W or the thresholds after held-out results are seen. If (ii) or (iii) fails on tune, the run is **void**: a scaffold failure of the judge, with no claim about the hypothesis. |
| **Confounds** | under-masking (clocks changing in fewer than 14 of 16 steps); over-masking (real objects that move every step, e.g. an autonomous enemy, could prune live moves). Masked cells per game are reported so over-masking is visible. |
| **Execution** | local CPU only; no GPU, Kaggle quota or tokens. `--policy random-prune-masked` in `experiments/e0_random_smoke.py`; results in `experiments/e5_{prune,masked}_{300,1000}.json`; verdict printed by `e0_analyze.py --e5-verdict experiments`. |
| **If supported** | the masked judge becomes the acting judge for P2–P4. A submission change is a separate task with its own approval. |
| **If falsified** | exact hash stays the acting key. The masked judge is still adopted as the **measurement** judge if checks (i)–(iii) pass. |

**Status:** pre-registered 24 Sept 2026; not run.

### Amendment, 24 Sept 2026 — checks (ii) and (iii) fail: the "clocks" are progress bars; E5 void as registered

Safeguards and check (i) were built first (`src/agents/masked_judge.py`, the runner's
safeguards, `tests/test_e5_masked_judge.py`: 44 tests pass). Then checks (ii) and (iii)
were run on the tune games as registered: policy `random-prune-masked`, episodes 0–2,
300 actions, the measurement judge recording its mask at every step.

| Game | Episodes 0 / 1 / 2 | Check |
| :-- | :-- | :-- |
| `dc22` | no cell masked in any episode; first mask never | **(ii) fails** (needed: clock masked within 32 steps, all 3 seeds) |
| `ls20` | no cell masked; masked states/100 = exact states/100 (97.0 / 96.0 / 93.0) | **(iii) fails** (needed: counter masked, and masked < exact) |

**Why: the judge works as specified; the model of a clock is wrong for these games.**
Traced cell by cell over 300 random actions (episode 0):

- `dc22`'s "clock" is a **progress bar** on row 63: every second action colours the
  next cell, (63,0), (63,1), (63,2), … No bottom cell changed more than 3 times in 300
  steps.
- `ls20`'s "step counter" is a **two-row bar** on rows 61–62 that advances one column
  per action (a bottom change on 293 of 300 steps). No bottom cell changed more than 11
  times in 300 steps.

A bar's cells each change once per pass, so no single cell changes in 14 of 16
transitions, whatever W or the threshold. The design's assumption **A2** ("clock-like cells change on
most steps regardless of action") is **false for both tune games it was based on**.
E1's note "`dc22` flips one cell every second action" was right about the timing but
not about the cell: it is a different cell each time.

**Consequence, by the rule above.** The run is **void**: a scaffold failure of the
judge, with no claim about the hypothesis. No held-out game has been played. The
safeguards stay; they don't depend on the judge. The masked judge is **not** adopted
as the measurement judge, because that adoption required checks (i)–(iii) to pass.
Any revised judge (for example, one that masks a screen region where a change happens on most
steps whatever the action, rather than a single cell) is a new design choice and
needs its own human decision and dated pre-registration before any held-out run.

### Amendment, 24 Sept 2026 — revised judge: a bar rule added; pre-registration, fixed before any held-out run

Human decision 24 Sept: "Revise the judge." (`DECISION-393bcd0f`). Everything in the E5 block
stands except the judge and the checks below.

**What the tune games show** (random play, episode 0, 300 steps, per row): an edge row
changes on a fixed schedule in five of the eight games: `dc22` row 63 (0.50 of steps),
`ls20` rows 61–62 (0.98), `s5i5` row 63 (1.00, a 50-move budget bar), `tn36` row 1
(1.00), `tu93` row 63 (1.00). Change frequency alone doesn't separate them from moving
objects: `sc25`'s object rows change on 0.62 of steps, more than `dc22`'s bar. What does:
**a bar changes each cell once per pass (fill or drain); a moving object changes a cell at
least twice, once as it arrives and once as it leaves.**

**Revised judge.** The mask is the union of two rules, both over the last **W = 16**
transitions of the last layer, with nothing masked before 16 transitions:

1. **Cell rule** (unchanged from the E5 block): a cell changed in ≥ 14 of 16
   transitions, across ≥ 3 distinct action keys.
2. **Bar rule** (new): a whole **row or column** is masked when (a) the transitions in
   which any of its cells changed match one of three schedules (every transition, even
   transitions, odd transitions) in **≥ 14 of 16**; (b) those transitions span **≥ 3**
   distinct action keys; and (c) **no cell of the line changed more than once** in the
   window.

The masked hash, the acting key, the common measurement judge and the "empty mask =
E4's identity" property are as in the E5 block. Each report row also lists the lines ever
masked in its episode, so over-masking on held-out is visible per game.

**Checks (replace (i)–(iii); (iv) and (v) unchanged).**
- **(i)** synthetic, cell rule: as in the E5 block. **Bar rule:** a bar that fills one
  cell of a row per step, and one that fills every second step, are masked by step 16 and
  every later move is judged dead; an object sweeping along a row (entering and leaving
  cells) is never masked.
- **(ii)** `dc22`, tune, 3 seeds: row 63 masked within 32 steps.
- **(iii)** `ls20`, tune, 3 seeds: rows 61–62 masked, and masked distinct states/100 <
  exact distinct states/100.
- **(vi) over-masking**, all 8 tune games × 3 seeds, 300 actions: no line or cell is ever
  masked other than these bars, identified by hand from the traces: `dc22` row 63,
  `ls20` rows 61–62, `s5i5` row 63, `tn36` row 1, `tu93` row 63, `sc25` columns 62–63
  (a vertical timer, found by a prototype of this rule).

**Stated before the checks run: these rules and checks were designed on the same tune
games.** A prototype of the bar rule was run on all 8 tune games × 3 seeds before this
amendment was written. It masked exactly the bars listed in (vi) and nothing else, but it
also showed two known **under-masking** cases:
- `s5i5`'s bar is masked for only about a third to a half of each episode (all its moves
  are clicks, so key diversity is limited);
- `sc25`'s timer advances irregularly (every 1–3 steps), so it rarely matches a schedule.

The checks therefore confirm the implementation, not generalisation. Only the
held-out run can show whether the rule transfers, and its per-game masked lines are
reported for that reason. Parameters are fixed here and are not changed after any
held-out result is seen.

### Amendment, 24 Sept 2026 — revised-judge checks: (i)–(iii) pass, (vi) fails once, on the cell rule

Run: `e0_random_smoke.py --split tune --episodes 3 --max-actions 300 --policy
random-prune-masked`, trajectories kept. Tests: 47 pass (the bar-rule synthetic cases
included; a mutation that drops "no cell changed twice" is caught).

| Check | Result |
| :-- | :-- |
| (i) synthetic | **pass**. The every-second-step bar test uses a 5-action cycle: under a 4-cycle the bar only ever moves under two keys (an aliasing of the test, not of random play) |
| (ii) `dc22` row 63 within 32 steps | **pass**: step 16 in all 3 seeds |
| (iii) `ls20` rows 61–62, masked < exact states | **pass**: masked 112 / 124 / 109 vs exact 289 / 294 / 294 |
| (vi) over-masking, 8 games × 3 seeds | **fail, once**: `dc22` episode 2, step 165, the **cell rule** masked 4 player cells, (40–41, 10–11). The player moved back and forth over them for 14 of 16 transitions under 3 keys. One step of 300; the bar rule masked only the listed bars |

Other observations: every bar listed in (vi) was masked in every seed; `sc25`'s timer was
first masked late (steps 95–252), and its masked states equal its exact states, so it is
under-masked as predicted. No level cleared, no fast-clear flag, no safeguard failure.

**Consequence.** Check (vi) as registered fails, so there is no held-out run. The failure
belongs to the original cell rule, which on the tune games masked no clock at all
(every clock seen is a bar) and this one piece of the player. The next step is a human
decision.

### Amendment, 24 Sept 2026 — bar rule only; fixed before the checks are rerun

Human decision 24 Sept: "Drop the cell rule and keep the bar rule only."
(`DECISION-c600803c`). **The judge's mask is the bar rule alone**, exactly as specified
in the revised-judge amendment. Everything else stands.

**Known cost, stated in advance:** a clock that ticks in one place (a single cell or a
digit changing repeatedly) is never masked. That is under-masking; the per-game masked
lines on held-out show where masking happened, and a game with an unmasked ticking clock
behaves as under E4.

**Checks, rerun once on this code, with no further change to the rule:**
- **(i)** synthetic: the two bar cases masked by step 16, with every later move dead; the
  sweeping object never masked; a single ticking cell **not** masked (the stated cost); in
  a bar world where only ACTION1 changes anything else, ACTION1 is never judged dead.
- **(ii), (iii), (vi)** as in the revised-judge amendment.

### Amendment, 24 Sept 2026 — bar-only checks: all pass

Same commands as the previous run, once, on the bar-only code. Tests: 47 pass.

| Check | Result |
| :-- | :-- |
| (i) synthetic | **pass**: both bars masked by step 16, every later move dead; sweeping object never masked; single ticking cell never masked (the stated cost); ACTION1 never dead in the bar world |
| (ii) `dc22` | **pass**: row 63 masked at step 16 in all 3 seeds |
| (iii) `ls20` | **pass**: rows 61–62 masked at step 16; masked states 112 / 124 / 109 vs exact 289 / 294 / 294 |
| (iv) replay | **pass**: E4's saved random and prune episodes replay exactly; T1 plays as C0 while nothing is masked |
| (v) switch | **pass**: in C0's 7,200 tune steps the acting verdict equals exact-hash equality every time |
| (vi) over-masking | **pass**: across 8 games × 3 seeds, only the listed bars were ever masked, always as whole lines |
| safeguards | **pass**: episode IDs unique, one initial hash per game, no level cleared, no fast-clear flag |

`sc25`'s timer is still under-masked (first masked at steps 95–252; masked states =
exact states), as predicted. `ft09` and `sk48` show no bar and are unaffected.

**Status:** the judge and safeguards pass every implementation check. The held-out run
(C0 and T1, 17 games × episodes 100–119 × 300 and 1,000 actions) and the
`--e5-verdict` analysis have not been run.

### Amendment, 24 Sept 2026 — E5 verdict: narrow, carried by `vc33`

One held-out run, local CPU, commit `995d039` plus the verdict script and a `guard_fired`
counter (no behaviour change). Results: `experiments/e5_{prune,masked}_{300,1000}.json`;
trajectories: `experiments/build/e5/` (not tracked). Verdict printed by `e0_analyze.py
--e5-verdict experiments`. All four runs exited 0: episode IDs unique, one initial frame
per game, no clear in ≤ 2 actions. The replay test re-plays `vc33` episode 100 for both
conditions exactly (53 tests pass).

| | C0 (exact) 300 | T1 (masked) 300 | C0 1,000 | T1 1,000 |
| :-- | --: | --: | --: | --: |
| Verdict clears (16 games × 20 seeds) | 37 | **57** | 55 | 74 |
| RHAE, verdict / all 17 | 0.0952 / 0.1310 | 0.1122 / 0.1473 | 0.0972 / 0.1331 | 0.1143 / 0.1494 |
| Dead-move rate (common judge) | 0.257 | 0.209 | 0.252 | 0.197 |
| Masked states / 100 | 58.2 | 59.2 | 50.7 | 51.5 |
| `r11l` clears (outside) | 10 | 10 | 18 | 17 |

**Test at 300 actions (primary):** 18 wins, 0 losses, 2 ties, one-sided p < 0.0001, total
clears higher. **Concentration rule: fails.** All the gain is `vc33`, 0 → 20 clears (level
1 in every seed). Without `vc33`: 37 vs 37, p = 0.69. Only one game improved.
**Verdict: NARROW, carried by `vc33`.** At 1,000 actions (reported, not decisive):
also narrow, carried by `vc33` (2 → 22). Without it, 52 vs 53.

**What happened on `vc33`.** It is a click-only game with a bar on row 0 that changes on
every click. Under exact identity every frame is new, so C0 learnt no dead move (0 learnt,
0 redraws). T1 masked row 0 from step 16, found that about 71% of clicks change nothing
else, learnt 1,903 dead clicks, and cleared level 1 in 40–245 actions.

**Masking on held-out.** Lines were masked in 10 of 17 games (e.g. `g50t`, `tr87`, `sp80`
row 63; `lf52`, `vc33` row 0; `ar25` column 63; `r11l` column 0). **`bp35` shows likely
over-masking**: at 1,000 actions, 16 alternating columns (c1, c3 … c57) plus row 63. It
cleared nothing under either condition, so the verdict is unaffected. Small per-game
losses at 1,000 actions: `ar25` 2 → 1 and `r11l` 18 → 17.

**Consequences, by the rules above.**
- Not supported, so the exact-hash key stays the acting default for P2–P4 (design §5).
- Checks (i)–(vi) passed, so the bar-only masked judge **is adopted as the common
  measurement judge** for later experiments.
- No general claim that pruning's ceiling was perceptual. The claim is narrow: on a game
  whose bar changes on every move, masking the bar lets pruning work where it could not.
- E5 stops here: no re-parameterisation, no re-run.

---

## E6 — Transition-graph memory with return-to-frontier (design P4)

Drafted 27 Sept 2026 from `documents/research_design/next_phase_experiment_design.md`
§4 P4; **approved 27 Sept with the masked judge** (`DECISION-f0b09b26`), before any E6
run. Genesis task `T-E6a`.
**Numbering:** E6 is the next free register number. The shared pages' "E6 = Jev"
predates this draft (the same clash as E5; still an open human decision).

**The state judge (decided: masked).** E5's consequence says exact hash
stays the acting default for P2–P4. This draft **departs from that for P4**, and uses the
bar-only masked judge (E5) for node identity, tried-arm sets and pruning **in both
conditions**. The reason is known before any run: 10 of 17 held-out games had a bar
masked in E5. Under exact identity, every frame on those games is new, so the graph is a
chain, no state is ever revisited, navigation never fires, and fidelity is near 0. P4's
own rule would then call it "not testable" on most verdict games. The judge is the same in
L and G, so it is not the variable under test. The alternative is exact identity, as E5's rule says,
accepting that likely outcome.

| | |
| :-- | :-- |
| **Question** | Does remembering observed transitions, and navigating back along known paths to states with untried actions, clear more levels than the same local exploration rule without navigation? |
| **Capability isolated** | memory (a transition graph) plus planning-to-explore. The local action-choice rule, the arms, pruning and the judge are the same in both conditions. |
| **Arms** (as design P3) | each available keyboard action; plus, if clicks are available, one arm per colour present in the current frame, the click cell drawn uniformly among that colour's cells (E4's click key). |
| **Node** | masked hash of the frame (bar-only judge, run per episode). Tried arms and dead arms are kept per node; an arm is **dead** at a node when the judge saw it leave the node unchanged. |
| **L: local systematic** | at a node with untried live arms, uniform over them; otherwise uniform over live arms (all dead: uniform over all arms, as in E4). After GAME_OVER, continue with the local rule from the reset state. Memory: per-node tried and dead arm sets only. |
| **G: L + navigation** | same, except at a node with no untried live arm, and after a GAME_OVER reset, **navigate**: BFS over the graph from the current node to the nearest node with an untried live arm (ties: smallest node insertion order), then take each edge's recorded exact action. |
| **Graph** | edges = (node, exact action including (x, y) for clicks) → observed next node. An edge whose re-execution lands elsewhere is marked **unreliable**, excluded from planning, and navigation replans from the current node. Navigation stops at the frontier node, a level clear or GAME_OVER. Navigation actions count toward the budget. The graph and all arm sets reset each episode and whenever `levels_completed` increases. |
| **Safeguards** | all of E5's (episode IDs, initial-state hash, ≤ 2-action clear flag, trajectories, no environment kept, replay test), plus a per-step `navigating` flag in the trajectory. |
| **Implementation checks** (before held-out) | **(i)** synthetic corridor of depth 30, 4 actions per step, where a wrong action ends the game and the reset returns to the start: G reaches depth 30 within **1,500** actions (see the notes below) in ≥ 19/20 seeds, L in fewer (validates navigation, not the hypothesis). **(ii)** navigation fidelity on the 8 tune games × 3 seeds (share of re-executed edges that reproduce their recorded next node), reported per game; below 0.8 = "non-deterministic under this judge". **(iii)** navigation plus exploration actions = actions played, every episode. **(iv)** safeguards and replay. **(v)** switch check: G's actions equal L's, step for step, until G's first navigation. |
| **Games, seeds, budgets** | 17 held-out games; verdict on 16 (`r11l` outside). Episodes **100–119**, the same as E5, so E5's C0 files pair with them. Budgets 300 and 1,000. |
| **Primary metric** | verdict level clears, G vs L. |
| **Success** | sign test (per seed, G − L clears over the 16 games; one-sided, ties dropped) with p < 0.05 at 300 **or** 1,000 actions after a Holm correction over the two budgets, total clears higher, and the concentration rule holds (survives removing the largest-gain game; ≥ 2 games improve). |
| **Credit rule** (design §5 rule 2) | G becomes the "best CPU policy" for P8 only if it also beats E5's C0 (E4's random-prune, `experiments/e5_prune_*.json`) by the same test. Otherwise the gain is credited only against L. |
| **Falsifier / not testable** | falsified otherwise. If fidelity is below 0.8 on more than half the verdict games, the verdict is **"not testable with this judge"**, not falsified. One held-out run per budget; no change to BFS, the arms or the judge after held-out results. |
| **Secondary** | L vs C0 (the arm structure itself, not a verdict); max BFS depth from the level's start node; distinct nodes / 100; fidelity per game; share of actions navigating; mean successful path length; share of navigations that reach their target without replanning; dead-move rate (common judge); per-game clears; RHAE. |
| **Confounds** | non-deterministic games (fidelity < 0.8); colour arms re-executed at the recorded (x, y) are not the arm's distribution; a masked bar can be a move budget (`s5i5`, `ls20`), so nodes that differ only in remaining budget are merged and navigation can plan paths the budget cannot pay for; `bp35`'s likely over-masking (E5) merges states on that game. |
| **Execution** | local CPU only: `--policy local` / `--policy local-nav` in `e0_random_smoke.py`; results `experiments/e6_{local,nav}_{300,1000}.json`; verdict by `e0_analyze.py --e6-verdict experiments`. Estimated 1–2 h of CPU (graph overhead unknown); about 2 days to build. |
| **If supported** | navigation is a missing capability; any Duck-style world model (P8) must beat G. |
| **If falsified** | re-reaching known states is not what limits these games at these budgets; next is P5 (oracle goal, tune only) per design §5. |

**Note, 27 Sept 2026, after approval and before any code or run: check (i)'s budget
changed from 300 to 1,000 actions.** With 4 actions per corridor step and death returning
to the start, a wrong guess at depth *d* costs G *d* + 1 actions. On average G needs about
30 + 1.5 × 465 ≈ 730 actions to reach depth 30 (s.d. about 110), so 300 cannot pass even
with perfect navigation. Within 1,000, G should succeed in about 99% of seeds; L, which
chooses uniformly among 4 arms at every fully tried node, essentially never reaches
depth 30. The check validates navigation, not the hypothesis, so only its budget changed.

**Second note, 27 Sept 2026, before any tune or held-out run: that estimate was wrong;
check (i)'s budget is now 1,500.** It assumed exploration at a depth stops once the correct
action is found. The pre-registered local rule tries **every** untried arm first, and G's
nearest frontier is the shallowest depth with an untried wrong arm. So G tries all 3
wrong actions at every depth, a worst case of exactly 30 + 3 × 465 = 1,425 actions. At
1,000 actions the check failed: G reached depth 25–27, L depth 4–8. Measured with a
3,000-action budget, G reached depth 30 in all 20 seeds using 1,137–1,425 actions; L
never passed depth 8. 1,500 is set from the arithmetic bound, not fitted to the data.
Only the check's budget changed; the policies are unchanged.

### Amendment, 27 Sept 2026 — tune checks pass; how the verdict reads fidelity, fixed before held-out

Tests: 56 pass. Tune run, 8 games × episodes 0–2 × 300 actions, L and G.
- **(i)** the corridor check passes at 1,500 actions.
- **(iii) accounting:** navigation + exploration = actions played in every episode.
- **(iv) safeguards:** unique episode IDs, one initial frame per game, no fast clears.
- **(v) switch:** G's actions equal L's until G's first navigation in all 24 episodes.
- **(ii) fidelity**, G, per game pooled over the 3 seeds:

| | `ft09` | `ls20` | `s5i5` | `tn36` | `tu93` | `dc22`, `sc25`, `sk48` |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| Fidelity | 1.00 | 0.93 | 0.97 | 0.99 | 0.99 | none: never navigated |

On `dc22`, `sc25` and `sk48`, every node still had an untried arm for all 300 actions, so
G never navigated and played exactly as L. No game is below 0.8.

**Clarifications, written before any held-out run** (the block did not define these):
- A game where G re-executed no edge has **undefined** fidelity. It is reported as "never
  navigated", and does not count as below 0.8.
- Fidelity for the "not testable" rule is G's, pooled per game over both budgets' runs.
- The Holm correction is over the two budgets' G-vs-L sign tests. A budget passes if its
  adjusted p < 0.05 and total clears are higher. The overall verdict is **supported** if
  a passing budget also meets the concentration rule, and **narrow** if one passes but
  the concentration rule fails.
- The concentration and credit (G vs C0) tests use the unadjusted p < 0.05, at the
  passing budget, as in E5.

**Status:** pre-registered 27 Sept 2026; checks pass; held-out not run.

### Amendment, 27 Sept 2026 — E6 verdict: falsified

One held-out run per budget, local CPU, commit `93cf706`. Results:
`experiments/e6_{local,nav}_{300,1000}.json`; trajectories in `experiments/build/e6/`
(not tracked). Verdict printed by `e0_analyze.py --e6-verdict experiments`. All four runs
exited 0: accounting holds in every episode, IDs are unique, there is one initial frame
per game, and there are no fast clears. The replay test re-plays `lf52` episode 104 for L
and G exactly (the episode where they part: L 0 clears, G 1 after 60 navigation actions).

| | L 300 | G 300 | L 1,000 | G 1,000 |
| :-- | --: | --: | --: | --: |
| Verdict clears (16 games × 20 seeds) | 57 | 61 | 80 | 90 |
| Sign test G − L | | 7 W / 4 L / 9 ties, p = 0.274 | | 10 W / 3 L / 7 ties, p = 0.046 |
| Holm-adjusted p | | 0.274 | | **0.092** |
| G's share of actions navigating | | 0.037 | | 0.061 |
| Navigations; reached without replanning; mean path | | 2,556; 2,276; 1.5 | | 11,748; 10,052; 1.8 |

**Verdict: FALSIFIED.** Neither budget passes after Holm (the 1,000-action raw p = 0.046
becomes 0.092). The gain was not general at either budget: at 1,000 actions, removing
`lf52` (3 → 9) leaves 81 vs 77, p = 0.29. Fidelity was below 0.8 on 3 verdict games
(`cd82` 0.53, `m0r0` 0.28, `wa30` 0.65) and `r11l` (0.76), so the test counts as run.
`ka59` never navigated.

**Why navigation barely mattered.** G navigated for only 4–6% of its actions, over paths
averaging 1.5–1.8 steps. Within these budgets the local rule rarely runs out of untried
arms, so the graph is seldom needed. Where it was used heavily (`g50t` 38%, `lf52` 36% of
actions at 1,000), it helped `lf52` and did nothing for `g50t`.

**Secondary (not a verdict): the arm structure itself.** L beat E5's C0 (E4's
random-prune) by a wide margin: 57 vs 37 at 300 actions and 80 vs 55 at 1,000 (both
p ≤ 0.0001). Per game this is carried by `vc33` (+21 / +24), the masked-bar game that E5
found. The rest are small: `cd82` +2 / +3 and `lf52` +1 / +3, against `sp80` −3 and
`m0r0` −5. So it's E5's narrow result again, plus the colour-arm structure. It is not
evidence for navigation. G's credit test against C0 is also concentrated (on `vc33`), so
**G is not credited as the best CPU policy.**

**Consequences (design §5).**
- Falsified: re-reaching known states is not what limits these games at these budgets.
  Per the decision tree, **P5 (oracle goal, tune only)** is next on the CPU branch.
- P3 is still unrun. By §5 rule 3, the CPU branch stops only if P3 and P4 both fail and
  P5's oracle does not help.
- The best CPU policy for P8's comparison stays undetermined. No candidate has passed its
  own test without concentration on `vc33`.
- E6 stops here: no change to BFS, the arms or the judge; no re-run.

---

## E7 — Empirical action-success bandit (design P3)

Written 30 Sept 2026, before any E7 code or run, from
`documents/research_design/next_phase_experiment_design.md` §4 P3. Human instruction:
"implement P3" (`DECISION-16a63c9c`). Genesis task `T-E7a`. **Two choices below are
flagged for human confirmation before any held-out run: the judge, and the numbering.**
The shared pages use "E7" for the hybrid.

**The state judge: masked (flagged).** The design says "P1 outcome", which E5 left as
exact hash for acting. This block uses the bar-only masked judge in every condition, for
state identity, dead arms and the novelty reward. The design names the confound itself:
"novelty reward can favour clocks". Under exact identity, a bar that changes every step
makes every state new, so every pull scores 1 and the bandit learns nothing. Bars were
masked on 10 of 17 held-out games in E5. E6 made the same choice, with approval.

| | |
| :-- | :-- |
| **Question** | Does learning within an episode which action classes tend to produce new states, and preferring them, clear more levels than choosing uniformly among the same classes? |
| **Capability isolated** | statistical learning plus action selection, within the episode, with no model. Pruning, the arms and the judge are held constant between A′ and B. |
| **Arms** | as E6: each available keyboard action, plus, if clicks are available, one arm per colour present in the current frame; the click cell is drawn uniformly among cells of that colour. |
| **State; dead arms** | state = masked hash (bar-only judge, one per episode). An arm is **dead** in a state once the judge saw it leave that state unchanged (and not GAME_OVER, and no level cleared). Dead arms in the current state are excluded before choosing; if every arm is dead, the choice is uniform over all arms. |
| **A: E4 random + prune** | E4's policy with the masked judge, i.e. E5's T1. **Not re-run**: `experiments/e5_masked_{300,1000}.json` are the same policy, games and episodes. |
| **A′: uniform arms** | uniform over live arms. |
| **B: UCB1 arms** | UCB1 over live arms: score = mean + √(2 ln N / n), with N the total pulls this episode and n the arm's pulls. An unpulled arm scores +∞; ties are broken by the episode rng. |
| **Reward** | 1 when the transition's resulting state has **not been seen before in this episode** (states seen include every state the policy acted from); GAME_OVER 0; a level clear 1. Estimates are **pooled per arm key across all states** in the episode ((action) for keys, (action, colour) for clicks), and reset each episode. |
| **Primary comparison** | **B vs A′** (learning, with the arm structure fixed). **Secondary:** A′ vs A (the arm structure itself, reported, not a verdict); B vs E6's L (the best systematic rule so far, reported). |
| **Safeguards** | E5's, all of them; the trajectory also logs the chosen arm and whether the bandit chose freely or fell back (all arms dead). |
| **Implementation checks** (before held-out) | **(i)** synthetic 3-arm world where only arm 2 reaches new states (arms 1 and 3 step back to states already seen, so they stay live): B's pull share of arm 2 > 0.8 after 100 steps; A′'s within 1/3 ± 0.1. **(ii)** arm-key agreement: every dead entry is keyed by the arm that was pulled, on every logged transition. **(iii)** substitution accounting: no redraws in A′ or B (dead arms are excluded before choosing); fallbacks logged and counted. **(iv)** safeguards pass; E5's A files replay (existing test); one saved episode per new condition replays after the run. **(v)** tune run, 8 games × episodes 0–2 × 300 actions: B's pulls differ from uniform on at least one game (the bandit is live), and the run is clean. |
| **Games, seeds, budgets** | 17 held-out games; verdict on 16 (`r11l` outside). Episodes **100–119** (paired with E5 and E6), run seed 0. Budgets **300** (primary) and **1,000** (reported, not decisive). |
| **Success** | per seed, B − A′ clears over the 16 verdict games; one-sided exact sign test, ties dropped: **p < 0.05** at 300 actions, total clears higher, and the concentration rule holds (survives removing the largest-gain game; ≥ 2 games improve). A pass without concentration is **narrow**. |
| **Falsifier / stop** | falsified otherwise. One held-out run; no change to the UCB constant, the reward, the arms or the judge after held-out results are seen. |
| **Secondary metrics** | clears at 1,000; distinct masked states/100; dead-move rate (common judge); arm-pull distribution per game (which action classes were learnt productive); per-game clears; RHAE. |
| **Confounds** | novelty favours anything that changes the screen: moving objects, and bars the judge under-masks (`sc25`'s timer); colour arms merge objects of one colour; A′ vs A mixes the arm structure with the click distribution (hence secondary). |
| **Execution** | local CPU: `--policy arms` (A′) and `--policy arms-ucb` (B) in `e0_random_smoke.py`; results `experiments/e7_{uniform,ucb}_{300,1000}.json`; verdict by `e0_analyze.py --e7-verdict experiments`. |
| **If supported** (design §5) | B becomes the statistical baseline that P6 (a learned ranker) and P8 (Duck) must beat. |
| **If falsified** | A′ is the baseline; P6 must beat A′. Knowing which action classes are productive is not what limits these games. With E6 also falsified, the CPU branch continues only through P5 (§5 rule 3). |

**Note, 30 Sept 2026, before the tune run: how check (v) is measured.** "B's pulls differ
from uniform" means: on at least one tune game, the total-variation distance between B's
and A′'s arm-pull distributions (pooled over the game's 3 episodes) is **≥ 0.2**. Check
(ii) uses a synthetic world with a do-nothing fourth action, so dead arms are guaranteed.
The check (i) world has almost none.

### Amendment, 30 Sept 2026 — E7 implementation checks pass

Code: `src/agents/arm_bandit.py` (A′ and B); E6's click-cell drawing moved into a shared
helper, with E6's replay test still exact. `e0_analyze.py --e7-verdict` is built on the
E5/E6 helpers, and E5's verdict output is unchanged byte for byte. Tests: 70 pass.

| Check | Result |
| :-- | :-- |
| (i) synthetic 3-arm | **pass**: B's arm-2 share 0.88 in all 5 seeds (> 0.8); A′ 0.34–0.39 (1/3 ± 0.1) |
| (ii) arm-key agreement | **pass**: dead entries equal the logged (state, pulled arm) pairs exactly (no-op world) |
| (iii) substitution accounting | **pass**: 0 redraws; fallbacks logged per step equal the count, synthetic and tune |
| (iv) safeguards | **pass** on tune: unique IDs, one initial frame per game, no fast clears |
| (v) bandit is live, tune 8 × 3 × 300 | **pass**: B vs A′ arm-pull total-variation distance ≥ 0.2 on `sk48` 0.33, `ft09` 0.25, `dc22` 0.21 (max 0.33). E.g. on `ls20` B pulled ACTION4 40% of the time |

On tune, B and A′ cleared the same levels (`tn36` 3 each, nothing elsewhere). No held-out
game has been played.

**Status:** pre-registered 30 Sept 2026; checks pass. The human said "run it" after the masked
judge and E7 numbering were put to them, so both are confirmed. Held-out run below.

### Amendment, 30 Sept 2026 — E7 verdict: narrow at 300 (primary); broad at 1,000 (not decisive)

One held-out run, local CPU, commit `03894a6`. Results:
`experiments/e7_{uniform,ucb}_{300,1000}.json`; trajectories in `experiments/build/e7/`
(not tracked). Verdict printed by `e0_analyze.py --e7-verdict experiments`. All four runs
exited 0; no redraws; IDs unique; one initial frame per game (across A′, B, A and L); no
fast clears. The replay test re-plays `lf52` episode 100 for A′ and B exactly (A′ 0 clears,
B 1).

| | A′ 300 | B 300 | A′ 1,000 | B 1,000 |
| :-- | --: | --: | --: | --: |
| Verdict clears (16 games × 20 seeds) | 60 | **71** | 82 | **117** |
| RHAE, verdict / all 17 | 0.0840 / 0.1773 | 0.1324 / 0.2686 | 0.0879 / 0.1810 | 0.1592 / 0.2939 |
| Dead-move rate (common judge) | 0.306 | 0.175 | 0.302 | 0.144 |
| Masked states / 100 | 55.4 | 68.6 | 51.5 | 66.7 |
| Sign test B − A′ | | 12 W / 3 L / 5 T, p = 0.018 | | 15 W / 2 L / 3 T, p = 0.0012 |

**Primary, 300 actions: NARROW, carried by `lf52`.** The sign test passes and totals are
higher, but `lf52` (0 → 14) carries it. Without it: 57 vs 60, p = 0.81. Games improved:
`lf52`, `lp85` (21 → 25), `m0r0` (0 → 4), `vc33` (21 → 23). Losses: `cd82` (4 → 0) and
`sp80` (14 → 5).

**Reported, not decisive, 1,000 actions: the same test reads SUPPORTED.** Without the
largest gain (`lp85`, 23 → 40, which includes clears beyond level 1): 77 vs 59, p = 0.038.
Six games improved: `ar25` 1 → 4, `bp35` 0 → 2, `lf52` 4 → 18, `lp85` 23 → 40, `m0r0`
0 → 12, `vc33` 25 → 32. The same two games lost: `cd82` 10 → 2, `sp80` 19 → 7. This is
the first result in the register that survives the concentration rule. **It was
pre-registered as not decisive and is not a verdict.**

**Secondary.**
- A′ vs A: 60 vs 57 and 82 vs 74; not significant, and concentrated. The arm structure
  alone adds little over E4 + masking.
- B vs E6's L: 71 vs 57 (p = 0.038, concentrated); 117 vs 80 (p = 0.0007, **not**
  concentrated).

**Mechanism, as far as the logs show.** B nearly halves the dead-move rate (0.30 → 0.14–0.18)
and raises distinct states per 100 from about 53 to about 68. It learns which action
classes change the screen: on `lp85` it put 67% (300) and 85% (1,000) of its pulls on
clicking colour 8. The losses (`cd82`, `sp80`) look like the stated confound: novelty
rewards whatever changes the screen, and there the bandit fixates on arms that change it
without progress. That is an inference; it has not been checked.

**Consequences, by the rules above.**
- The primary result is narrow, so **B is not adopted** as the statistical baseline under
  design §5; formally A′ stays the baseline.
- The 1,000-action result is the strongest signal so far and deserves a confirmatory
  test. Per the register-level stop condition ("re-run … before building on it"), that means a
  **new pre-registration** with 1,000 actions as the primary budget, on episodes not yet
  used (e.g. 120–139). That is a human decision. No re-run under this block.
- E7 stops here: no change to the UCB constant, the reward, the arms or the judge.

---

## E8 — Confirmatory run of the E7 bandit: 1,000 actions primary, fresh episodes

Written 30 Sept 2026, before any E8 run. Human instruction: "start the confirmatory bandit
run" (`DECISION-71ffdc68`). Genesis task `T-E8a`.

**Why.** E7's 1,000-action result (B 117 vs A′ 82 verdict clears; survives the
concentration rule; six games improve) is the strongest signal in this register, but it
was pre-registered as not decisive. The register-level stop condition says a result is re-run before
anything is built on it. E8 is that re-run, with the budget that showed the effect made
primary, on episodes no experiment has used.

| | |
| :-- | :-- |
| **Hypothesis** | B (UCB1 over design-P3 arms, within-episode novelty reward) clears more verdict levels than A′ (uniform over the same live arms) at 1,000 actions. |
| **Conditions** | A′ = `--policy arms`, B = `--policy arms-ucb`, **code unchanged** from E7 (commit `f18757b`): same arms, reward, UCB constant, bar-only masked judge and dead-arm rule. |
| **Games, seeds, budgets** | the same 17 held-out games; verdict on 16 (`r11l` outside). **Episodes 120–139** (20 seeds, never used: E4 0–19, E5–E7 100–119, tune 0–2), run seed 0. **1,000 actions primary**; 300 reported, not decisive. |
| **Success** | per seed, B − A′ clears over the 16 verdict games; one-sided exact sign test, ties dropped: **p < 0.05** at 1,000 actions, total clears higher, and the concentration rule holds (survives removing the largest-gain game; ≥ 2 games improve). A pass without concentration is **narrow**. |
| **Falsifier / stop** | falsified otherwise. One run; nothing changed after results are seen. |
| **Safeguards** | E5's, all of them, plus: no redraws in either condition; one saved episode per condition replays after the run. |
| **Also reported** | the E7 losses (`cd82`, `sp80`) per game; dead-move rate; masked states/100; B's most-pulled arms per game; RHAE. |
| **Known limit** | the same 17 held-out games again (open assumption A13): fresh episodes reduce, but do not remove, adaptive reuse. Only the hidden set is truly fresh. |
| **Execution** | local CPU; results `experiments/e8_{uniform,ucb}_{300,1000}.json`; verdict by `e0_analyze.py --e8-verdict experiments`. |
| **If supported** | B becomes the statistical baseline (design §5): P6 and P8 must beat it. Putting B into the submission is a separate task with its own approval. |
| **If narrow or falsified** | E7's 1,000-action result did not replicate as a general effect; A′ stays the baseline. |

**Status:** pre-registered 30 Sept 2026; run below.

### Amendment, 30 Sept 2026 — E8 verdict: narrow, carried by `lf52`; the size replicates, the breadth test does not pass

One run, local CPU, commit `2074dca` (policies unchanged from `f18757b`); verdict script
committed before any result (`f8d3ed7`). Results: `experiments/e8_{uniform,ucb}_{300,1000}.json`;
trajectories in `experiments/build/e8/` (not tracked). All four runs exited 0; no
redraws; IDs unique; one initial frame per game; no fast clears. The replay test re-plays
`lf52` episode 122 for A′ and B exactly.

| | A′ 1,000 | B 1,000 | A′ 300 | B 300 |
| :-- | --: | --: | --: | --: |
| Verdict clears (16 games × 20 seeds) | 79 | **114** | 57 | 65 |
| RHAE, verdict / all 17 | 0.0926 / 0.2135 | 0.1913 / 0.3039 | 0.0905 / 0.2114 | 0.1559 / 0.2705 |
| Dead-move rate (common judge) | 0.302 | 0.142 | 0.310 | 0.178 |
| Sign test B − A′ | | 14 W / 3 L / 3 T, p = 0.0064 | | 10 W / 4 L / 6 T, p = 0.090 |

**Primary, 1,000 actions: NARROW, carried by `lf52`.** The sign test passes and totals are
higher, but removing the largest-gain game (`lf52`, 0 → 15) leaves 99 vs 79 with
p = 0.105, so the concentration rule fails on its significance leg. Seven games
improved: `ar25` 0 → 10, `cn04` 0 → 2, `ka59` 0 → 1, `lf52` 0 → 15, `lp85` 23 → 35,
`m0r0` 1 → 6, `vc33` 26 → 33. Two lost, **the same two as in E7**: `cd82` 8 → 4 and
`sp80` 21 → 8. **300 actions** (reported): falsified, p = 0.090; without `lf52`, 56 vs
57.

**E7 and E8 together (description, not a verdict).**
- The size replicated: 117 vs 82 in E7 and 114 vs 79 in E8, both at 1,000 actions.
- The direction replicated on the same games: gains on `lf52`, `lp85`, `m0r0` and `vc33`
  in both runs; losses on `cd82` and `sp80` in both.
- The breadth test did not. E7 passed the concentration rule at 1,000 (p = 0.038 without
  `lp85`); E8 did not (p = 0.105 without `lf52`).
- With 20 seeds, a per-seed sign test after removing the largest-gain game is a strict
  bar. The pre-registered reading stands: **not supported.**

**Consequences.**
- B is **not adopted** as the statistical baseline; A′ stays the baseline (design §5).
- By the register's rules, the confirmatory run did not confirm. Any further test of the
  bandit is a new pre-registration and a human decision. Options include more seeds (the
  per-seed test after removing one game is under-powered at 20), or a fix for the
  `cd82`/`sp80` losses tested on tune first. Neither is run here.
- E8 stops here.

---

## E9 — The E7 bandit on 40 fresh seeds, 1,000 actions

Written 30 Sept 2026, before any E9 run. Human instruction: "start the bandit run on more
seeds" (`DECISION-aa5692c6`). Genesis task `T-E9a`.

**Why.** E8 replicated the bandit's size at 1,000 actions (114 vs 79; E7 117 vs 82) and the
per-game pattern. It failed only the concentration rule's significance leg: without `lf52`,
p = 0.105 on 20 seeds. A per-seed sign test after removing a game is under-powered at 20
seeds. E9 doubles the seeds, on episodes no experiment has used.

**Stated in advance: this is the bandit's third test** (E7, E8, E9), each decided after
seeing the previous one. E9's verdict is read only on its own fresh episodes, by the
same rule. All three are reported together whatever E9 shows. A positive E9 after a
narrow E8 is weaker evidence than a first-time positive would be, and the write-up must
say so.

| | |
| :-- | :-- |
| **Hypothesis** | B (UCB1 over design-P3 arms, within-episode novelty reward) clears more verdict levels than A′ (uniform over the same live arms) at 1,000 actions. |
| **Conditions** | A′ = `--policy arms`, B = `--policy arms-ucb`, **code unchanged** from E7 (commit `f18757b`). |
| **Games, seeds, budget** | the same 17 held-out games; verdict on 16 (`r11l` outside). **Episodes 140–179** (40 seeds, never used), run seed 0. **1,000 actions only**: 300 was reported, and was not decisive, in both E7 and E8. Each condition runs as two halves (140–159, 160–179), merged into one file per condition before the verdict. |
| **Success** | per seed, B − A′ clears over the 16 verdict games; one-sided exact sign test, ties dropped: **p < 0.05**, total clears higher, and the concentration rule holds (survives removing the largest-gain game; ≥ 2 games improve). A pass without concentration is **narrow**. |
| **Falsifier / stop** | falsified otherwise. One run; nothing changed after results are seen. **No fourth test of this bandit under this rule**, whatever E9 shows. |
| **Safeguards** | E5's, all of them; no redraws; one saved episode per condition replays after the run. |
| **Execution** | local CPU; results `experiments/e9_{uniform,ucb}_1000.json`; verdict by `e0_analyze.py --e9-verdict experiments`. |
| **If supported** | B becomes the statistical baseline (design §5). Putting B into the submission is a separate task with its own approval. |
| **If narrow or falsified** | the bandit's gain is recorded as real in size but carried by a few games. A′ stays the baseline. |

**Status:** pre-registered 30 Sept 2026; run below.

### Amendment, 30 Sept 2026 — E9 verdict: supported

One run, local CPU (on battery, so slow; seeded, so the results are unaffected), commit
`22de172` (policies unchanged from `f18757b`); verdict script committed before any result
(`96792db`). Each condition ran as two halves (140–159, 160–179), merged into
`experiments/e9_{uniform,ucb}_1000.json` (680 rows each). Trajectories in
`experiments/build/e9/` (not tracked). All four runs exited 0; no redraws; IDs unique; one
initial frame per game; no fast clears. The replay test re-plays `ar25` episode 141 at
1,000 actions for A′ and B exactly.

| 1,000 actions, 16 verdict games × 40 seeds | A′ | B |
| :-- | --: | --: |
| Verdict clears | 171 | **217** |
| RHAE, verdict / all 17 | 0.1278 / 0.2246 | 0.1499 / 0.2326 |
| Dead-move rate (common judge) | 0.300 | 0.141 |
| Masked states / 100 | 51.8 | 66.4 |

**Sign test:** 22 wins, 4 losses, 14 ties, one-sided p = 0.0003; total clears higher.
**Concentration rule: holds.** Without the largest-gain game (`lf52`, 2 → 25): 192 vs 169,
p = 0.044. Seven games improved: `ar25` 1 → 17, `bp35` 0 → 1, `cn04` 0 → 1, `lf52`
2 → 25, `lp85` 41 → 63, `m0r0` 1 → 18, `vc33` 59 → 62.
**Verdict: SUPPORTED** (at the pre-registered primary budget, on fresh episodes).

**Caveats, stated with the verdict, not after it.**
1. **Third test.** E7 (narrow at its primary budget, broad at 1,000), E8 (narrow) and E9
   (supported) were each decided after the previous result. The E9 block said in advance that a
   positive after a narrow E8 is weaker evidence than a first-time positive.
2. **The concentration leg is borderline:** p = 0.044 without `lf52`, against a 0.05 bar.
3. **The losses replicate every time.** `cd82` and `sp80` lose in all three runs (E7:
   10 → 2, 19 → 7; E8: 8 → 4, 21 → 8; E9: 22 → 9, 41 → 21). E9 adds small losses on
   `ka59` (2 → 0) and `tr87` (2 → 0). The gain is net, not uniform. My guess is novelty
   pulling the bandit toward screen changes without progress; that has not been checked.
4. **Same 17 held-out games** (A13): the episodes are fresh, the games are not.

**What replicated across E7–E9 at 1,000 actions** (description):

| | E7 | E8 | E9 |
| :-- | :-- | :-- | :-- |
| B vs A′ clears | 117 vs 82 | 114 vs 79 | 217 vs 171 (40 seeds) |
| Dead-move rate | 0.30 → 0.14 | 0.30 → 0.14 | 0.30 → 0.14 |

Gains on `lf52`, `lp85`, `m0r0` and `vc33` appear in all three runs; losses on `cd82` and
`sp80` appear in all three.

**Consequences.**
- By design §5, **B becomes the statistical baseline**: any learned ranker (P6) or model
  harness (P8) must beat B, not only random + prune.
- B beat E6's L on E7's episodes (117 vs 80, not concentrated), so it is also the best
  CPU policy measured so far.
- **Not done here, each its own task and approval:** putting B into the submission (it
  would need its own rehearsal, and the hidden set reports two decimals); investigating
  the `cd82`/`sp80` losses on tune.
- As pre-registered, there is no further test of this bandit under this rule.

### Amendment, 30 Sept 2026 — Build 4: E9's bandit in the submission, built and rehearsed

Genesis task `T-B4`, human decision `DECISION-61e2dcee` ("approve bandit for the
submission"). `submission/my_agent.py` now plays E9's B: the bar-only masked judge,
design-P3 arms, a within-game novelty reward, dead-arm exclusion and UCB1, all inlined
because the notebook ships one file. `MAX_ACTIONS` 300 → 1,000, the budget E9 tested.
The framework has no post-step hook, so a move is learnt from at the next call.
`tests/test_b4_agent.py` replaces the Build 3 tests. It drives the agent through the
experiment loop with framework-style frames, and asserts **the same episode as
`ArmBandit(ucb=True)`** at 1,000 actions on `lp85` (click arms), `vc33` (masked row-0
bar) and `ls20` (keys and a two-row bar), for a shared random stream. A mutation of the
bar rule (3 → 2 action keys) breaks all three.

**Local rehearsal of the scored rerun** (`submission/rehearse.py --games lp85,ls20,r11l
--require-level lp85`: reference gateway in competition mode, the real framework and
agent), against Build 3's rehearsal:

| Game | Build 4 score (levels) | Build 3 score (levels) |
| :-- | --: | --: |
| `lp85` | 1.2159 (3) | 0.4147 (1) |
| `r11l` | 4.7619 (1) | 0.0254 (1) |
| `ls20` | 0 (0) | 0 (0) |

**22 ms/action** on Windows with three agents (on battery), so 110 games × 1,000 actions
project to about 40 minutes against the 9 h limit. Kernel built as
`goutham12/arc-agi-3-build-4-arm-bandit` (private, CPU). **Pushed 30 Sept 2026 as
version 1**, at the human's request ("push the kaggle kernel from your end"). The
ordinary Kaggle run completed and wrote `submission.parquet`. **Submitted by the human
from the Kaggle website**: submission **56700446**, 30 Sept 2026 07:14 UTC, status
pending at the time of writing.

**What a hidden-set score can show.** Builds 1 and 3 both scored 0.07. The hidden set is
110 different games, and Kaggle reports two decimals. E9's gain is net: `cd82` and `sp80`
lose in every run. So a hidden score at 0.07 would mean the gain did not transfer, or is
too small to see; it would not falsify E9. Build 4 changes two things (the policy and
the 300 → 1,000 cap), so a higher score cannot be split between them without a second
submission.

### Diagnosis, 30 Sept 2026 — why the bandit loses on `cd82` and `sp80`

Human instruction: "look into bandit losses on cd82 and sp80". This is analysis of E9's
**saved** held-out trajectories only; no new run was made. Both are held-out games, so
any fix designed from this diagnosis must be tested on fresh episodes, with the caveat that
these games were inspected. The hidden set is the only unseen check.

| E9, 40 seeds, 1,000 actions | A′ episodes with a clear | B episodes with a clear |
| :-- | --: | --: |
| `sp80` | 40 / 40 | 19 / 40 |
| `cd82` | 18 / 40 | 8 / 40 |

**The clearing move is ACTION5, every time:** 22/22 and 41/41 clears for A′, 9/9 and
21/21 for B. On `sp80` ACTION5 is also the move that most often ends the game. It behaves
like a "commit" move: it clears the level from the right screen, and kills from others.

**`sp80`: the bandit dies in loops.**
- A move that ends the game is never marked dead (E4's rule), and a death restarts the
  game on the same screen. UCB's choice there is nearly deterministic (same screen, same
  pooled statistics), so it picks ACTION5 again.
- 38% of B's ACTION5 deaths are on a screen where it had already died, up to 18 deaths
  from one screen in one episode. A′: 3%, at most 2.
- B's losing episodes pull ACTION5 153 times with 24.7 deaths; its winning ones 70 and
  7.9; A′ 92 and 9.2.

**`cd82`: the bandit fixates on ACTION5.** Deaths are rare and never repeated here.
ACTION5 produces a new screen on 90–96% of pulls, the highest of any arm, so novelty-UCB
spends about 20% of its pulls on it (A′ 9%), about 200 per episode against 90. It
under-samples the rest, while A′'s even coverage finds the clears. Novelty cannot tell
"new because of progress" from "new because the move changes something that doesn't
lead anywhere".

**Candidate fixes (not tested, not pre-registered):**
1. For `sp80`, remember deadly moves per screen: exclude a (screen, arm) that has
   already ended the game from that screen. It targets the loop directly, and leaves
   ACTION5 available on the screens where it clears.
2. For `cd82`, keep some uniform coverage, for example ε-uniform mixing, or a cap on one
   arm's share. This is less clearly targeted.
Either needs a tune check for no harm (tune never showed these losses) and a
pre-registered test on fresh held-out episodes (e.g. 180–219).

### Amendment, 30 Sept 2026 — Build 4 on the hidden set: 0.15, up from 0.07

Submission **56700446** completed: public score **0.15**. Build 1 (random, 80 actions)
and Build 3 (random + prune, 300) both scored **0.07**. This is the first build to move
the hidden-set score, and the first evidence in this project that a gain measured on the
public held-out games transfers to the 110 hidden games.

**What it can and cannot show.**
- **The gain is real at two decimals:** it is the same metric, on the same hidden set,
  as the two 0.07s.
- **It cannot be split** between the policy (E9's bandit) and the 300 → 1,000 action
  cap. Build 3 → Build 4 changed both. The public games give a hint, not an answer: E9's
  A′ (uniform arms, 1,000) vs B (bandit, 1,000) was 171 vs 217, so part of the gain on
  public games is the policy at a fixed budget. Separating them on the hidden set would
  take a second submission, e.g. A′ at 1,000.
- **One submission, one score:** there is no seed spread on the hidden set.

### Amendment, 30 Sept 2026 — Build 5: the second submission, and how its score will be read

Genesis task `T-B5`, human decision `DECISION-7f807d34` ("implement the optional second
submission"). **Build 5 is Build 4 with UCB switched off:** uniform over live arms (E9's
A′), with the same arms, masked judge, dead-arm rule, seeding and 1,000 actions.
`submission/my_agent.py` gains one switch, `UCB = True`, so the repository still ships
Build 4. `submission/build_submission.py --uniform` flips it for Build 5's notebook,
`goutham12/arc-agi-3-build-5-uniform-arms`. `tests/test_b4_agent.py` checks the switch
both ways: on, the same episodes as `ArmBandit(ucb=True)`; off, the same as
`ArmBandit(ucb=False)`, on `lp85`, `vc33` and `ls20` at 1,000 actions. A mutation that
ignores the switch breaks the three uniform cases. Not rehearsed separately: it is the
rehearsed Build 4 pipeline with one constant changed, and both branches are tested
offline.

**Reading, fixed before the result.** Build 4 scored 0.15. Scores are two decimals from
one submission each, so a difference of **≤ 0.01 is treated as no difference**. With
Build 5's score *s*:
- ***s* ≤ 0.08** (Build 3's level): the gain is the **bandit's**. Uniform arms at 1,000
  with the masked judge add nothing visible over random + prune at 300.
- ***s* ≥ 0.14**: the gain is the **arms, the judge and the 300 → 1,000 cap**. The
  bandit adds nothing visible on the hidden set, despite E9's public result.
- **0.09 ≤ *s* ≤ 0.13**: **both** contribute, roughly in proportion.

Build 5 vs Build 3 changes three things (arms, judge, cap), so that comparison cannot
isolate the cap. Only Build 4 vs Build 5, the bandit at a fixed budget, is a clean split.

### Amendment, 1 Oct 2026 — Build 5 on the hidden set: 0.12; both parts contribute

Submitted by the human from the Kaggle website after the quota reset: submission
**56745474**, 1 Oct 2026 06:45 UTC, public score **0.12**.

| Build | What changed from the one before | Hidden-set score |
| :-- | :-- | --: |
| 3 | random + prune, 300 actions | 0.07 |
| 5 | arms, masked judge, uniform choice, 1,000 actions | **0.12** |
| 4 | the same, with the UCB bandit | 0.15 |

**Reading, by the rule fixed above** (≤ 0.08 bandit; ≥ 0.14 arms, judge and cap;
0.09–0.13 both): **0.12 is in the "both" band.**
- Of Build 4's +0.08 over Build 3, about **+0.05** comes from the arms, the masked judge
  and the 300 → 1,000 cap together, and about **+0.03** from the bandit at a fixed budget.
- Build 4 vs Build 5 is the clean comparison: the bandit's own hidden-set gain is
  0.12 → 0.15. That's in the same direction as E9's public result (217 vs 171 clears),
  so the bandit's effect transfers to unseen games.
- Each score is one submission at two decimals, so the split is approximate. Build 5 vs
  Build 3 still bundles three changes.

Kernel `goutham12/arc-agi-3-build-5-uniform-arms` **pushed 30 Sept 2026 as version 1**
(private, CPU), as part of "implement the optional second submission". **Not submitted:**
the human submits from the Kaggle website once its ordinary run completes. On 30 Sept Kaggle
refused the submission: the daily quota was used (by Build 4's submission 56700446). **To
be submitted the next day.**

**Correction, 30 Sept 2026 (dates only).** The E7 verdict, E8, E9 and Build 4 entries
were first written as "1 Oct 2026". All of that work happened on 30 Sept (see the commit
dates, `f18757b` … `7a10c42`). Corrected in place; no content changed. The Genesis
records made the same day repeat the wrong date in their text: `DECISION-71ffdc68`,
`DECISION-aa5692c6`, `DECISION-61e2dcee`, `KNOWLEDGE-af0d409b`, `KNOWLEDGE-173fdde8` and
`KNOWLEDGE-2d3b2359`. Their `recorded_at` timestamps are correct.

---

## E10 — The bandit with a per-screen memory of deadly moves

Drafted 30 Sept 2026 from the diagnosis above (human instruction: "Draft it");
**approved as drafted** the same day (`DECISION-71f6688b`), before any E10 code or run.
Genesis task `T-E10a`.

**Why.** On `sp80` the bandit (B) dies in loops. A move that ended the game is never
marked dead, the reset returns to the same screen, and near-deterministic UCB repeats the
move: 38% of B's ACTION5 deaths repeat a screen it had already died on, against A′'s 3%.
E10 tests the narrowest fix for that one mechanism. It does **not** address `cd82`'s
ACTION5 fixation, which is a different mechanism and left for separate work.

**Stated in advance: this design is adaptive.** The mechanism was found by inspecting E9's
held-out trajectories on `sp80` and `cd82`. E10 runs on fresh episodes, but the 17 games
are the same, and one of them motivated the fix. A positive E10 is weaker evidence than a
first-time positive; the hidden set is the only unseen test. The write-up must say so.

| | |
| :-- | :-- |
| **Hypothesis** | B plus a per-screen memory of deadly moves (B′) clears more verdict levels than B at 1,000 actions. |
| **Control B** | E9's B unchanged: `--policy arms-ucb` (code at `f18757b`). |
| **Treatment B′** | B, plus one rule: when a move ends the game (GAME_OVER), its (screen, arm) pair is recorded, with the screen being the masked hash the move was made from. **A recorded pair is excluded on that screen for the rest of the episode**, exactly like a dead arm, and if every arm is excluded all are allowed again, as now. Nothing else changes: same arms, reward (GAME_OVER still scores 0), UCB constant, judge, dead-arm rule and level handling. `--policy arms-ucb-safe`. |
| **Why one death, not k** | the simplest rule. A move that kills from a screen once is excluded there; it stays available on every other screen, including the ones where ACTION5 clears. |
| **Games, seeds, budget** | the same 17 held-out games; verdict on 16 (`r11l` outside). **Episodes 180–219** (40 seeds, never used), run seed 0, **1,000 actions**. |
| **Implementation checks** (before held-out) | **(i)** synthetic death-loop world, where from the start screen one move kills and another advances: B repeats the killing move after resets, B′ never makes it twice from that screen. **(ii)** switch check: B′'s actions equal B's, step for step, until B′'s first excluded choice. **(iii)** safeguards (E5's) and, after the run, replay of one saved episode per condition. **(iv) tune no-harm**, 8 tune games × episodes 0–2 × 1,000: B′'s total tune clears ≥ B's − 1. If B′ loses more than that on tune, E10 stops there. |
| **Success** | per seed, B′ − B clears over the 16 verdict games; one-sided exact sign test, ties dropped: **p < 0.05**, total clears higher, and the concentration rule holds (survives removing the largest-gain game; ≥ 2 games improve). A pass without concentration is **narrow**. The most likely outcome, stated now: a gain concentrated on `sp80`, i.e. **narrow**. |
| **Also reported** | per-game clears; the repeat-death share (deaths on a screen already died on) for both conditions; the number of (screen, arm) pairs excluded; ACTION5 pulls and deaths on `sp80` and `cd82`; dead-move rate; RHAE. |
| **Confounds** | a click arm is a colour, not a cell. One death on a colour excludes every cell of that colour on that screen, which could prune a mostly safe click. The count of excluded click arms is reported. Excluding a move can also change which screens are reached later, so a gain or loss on other games is possible. |
| **Stop** | one run; nothing changed after results are seen. |
| **Execution** | local CPU; results `experiments/e10_{ucb,safe}_1000.json` (each run as two halves, 180–199 and 200–219, merged); verdict by `e0_analyze.py --e10-verdict experiments`. About 1–1.5 h of CPU on mains power, roughly 3× longer on battery. |
| **If supported** | B′ replaces B as the statistical baseline, with the adaptivity caveat. A Build 6 is a separate task with its own approval. |
| **If narrow** | the fix works where it was aimed (expected: `sp80`) but is not shown to generalise. A hidden-set submission of B′ would be the only unseen test. |
| **If falsified** | death loops are not what limits B at this budget, or the fix costs as much as it saves elsewhere. |

### Amendment, 30 Sept 2026 — E10 implementation checks pass

Code: `ArmBandit(ucb=True, death_memory=True)` (`--policy arms-ucb-safe`). Both conditions now
count repeat deaths, exclusions and deadly click pairs; B's play is unchanged, and the
E7–E9 replays and Build 4's equivalence tests still pass. `e0_analyze.py --e10-verdict`
generalises the E8/E9 function, whose outputs are unchanged byte for byte.

| Check | Result |
| :-- | :-- |
| (i) synthetic death loop | **pass**. A world with a move budget that returns the agent to a start screen where ACTION1 kills, while ACTION1 reaches new screens everywhere else: B repeats deaths from a screen it already died on (about 91 per 300-step episode); B′ never does, in all 5 seeds. The first world built for this check did not trap B at all (nothing ever returned it to the start), so the check could not have failed; it was rebuilt before the tune run. |
| (ii) switch | **pass**: B′'s moves equal B's until its first exclusion, in all 5 seeds |
| (iii) safeguards | **pass** on tune; replay after the held-out run |
| (iv) tune no-harm, 8 games × episodes 0–2 × 1,000 | **pass**: B 4 clears, B′ 4 (`sc25` 1, `tn36` 3 each). Repeat deaths B 38, B′ 3 (only in all-excluded fallbacks, as the rule allows); B′ 1,388 exclusions, 142 deadly click pairs |

**Status:** pre-registered 30 Sept 2026; checks pass; held-out run below.

### Amendment, 30 Sept 2026 — E10 verdict: narrow, carried by `sp80`, as predicted

One run, local CPU, commit `238c45e`. The first attempt (four processes) was stopped by
Claude Code at about 58% because the machine ran low on memory while the session was
idle. It was restarted, at the human's request, as two processes (one per condition, 40
episodes each), with the partial logs deleted first. Results:
`experiments/e10_{ucb,safe}_1000.json`; trajectories in `experiments/build/e10/` (not
tracked). Both runs exited 0; no redraws; IDs unique; one initial frame per game; no fast
clears. The replay test re-plays `sp80` episode 182 for B and B′ exactly (B 0 clears,
B′ ≥ 1).

| 1,000 actions, 16 verdict games × 40 seeds | B | B′ |
| :-- | --: | --: |
| Verdict clears | 227 | **245** |
| RHAE, verdict / all 17 | 0.1722 / 0.3110 | 0.1732 / 0.3120 |
| Repeat deaths (all games) | 534 | 34 |
| Exclusions | — | 14,796 |

**Sign test:** 20 wins, 8 losses, 12 ties, one-sided p = 0.018; total clears higher.
**Concentration rule fails:** without `sp80` (18 → 30), 215 vs 209, p = 0.119. Games
improved: `bp35` 2 → 4, `lp85` 74 → 76, `sp80`, `vc33` 61 → 65; `lf52` lost 28 → 26.
**Verdict: NARROW, carried by `sp80`**, the outcome the block predicted.

**The mechanism behaved as diagnosed.**
- On `sp80`, repeat deaths fell from 403 to 2, ACTION5 pulls from 4,745 to 3,330, and
  clears rose from 18 to 30.
- On `cd82` nothing changed: its ACTION5 pulls (8,570), deaths (360) and clears (11) are
  identical, as expected, because it has no death loops. Its loss is the separate fixation
  mechanism.

**Consequences.**
- B′ is **not** adopted as the baseline: B stays the statistical baseline.
- The death-memory rule is shown to fix the loop it targets, at no measurable cost
  elsewhere (other games' totals 215 vs 209; RHAE equal). It is a candidate for the
  submission. A hidden-set test would be the only unseen evidence, as a separate task.
- E10 stops here.

### Diagnosis, 30 Sept 2026 — `cd82`: the bar is under-masked, and novelty cannot credit its set-up moves

Human instruction: "look into the cd82 ACTION5 over-use". This is diagnosis on a held-out
game, with the same caveat as the diagnosis before E10. Method: saved E10 episodes
(180–184, both conditions) were **replayed deterministically** with instrumentation (same
seed and code; the replays match the saved results) to see which cells each move changed.
No new held-out run was made.

1. **`cd82`'s progress bar (row 63) ticks on a period-3 schedule:** tick, tick, pause.
   Tick runs are almost all exactly 2 long (about 840 of about 1,080), and the bar ticks on
   0.64 of moves in both conditions. The bar rule accepts only period 1 (every move) and
   period 2 (alternate moves), so the bar is **never masked** on `cd82` (0 masked cells
   in E5 and E9).
2. **Most "new screens" on `cd82` are the counter.** Per-move new-screen rates as the
   judge sees them are 0.59–0.78. With row 63 ignored they fall to 0.02–0.26:
   - B: ACTION5 0.64 → 0.15, other keys 0.78 → 0.15, clicks 0.61 → 0.06;
   - A′: ACTION5 0.70 → 0.26, other keys 0.74 → 0.19, clicks 0.59 → 0.02.
   47% of B's ACTION5 presses change **only** the bar.
3. **Masking the bar would not obviously fix `cd82`.** With the bar ignored, clicks almost
   never produce a new screen, so a novelty bandit would neglect them further. Yet in A′'s
   winning episodes clicks usually came within 5 moves before the clearing ACTION5
   (diagnosis before E10). `cd82` appears to need low-change set-up moves followed by a
   commit move; a new-screen reward cannot credit set-up moves, and A′ reaches them only
   through even coverage. This is inference from 5 replayed episodes per condition.

**Candidate fixes, untested:**
- (a) Extend the bar rule to period 3. This is a judge change that affects every game.
  It removes the noise, but it is not expected by itself to recover `cd82`, and it could
  newly mask something that is not a bar. It needs tune checks like E5's (over-masking
  check (vi)).
- (b) Keep some uniform coverage (ε-uniform mixing), which targets `cd82`'s actual
  need, at the cost of diluting the bandit on games where it helps.
- (c) Accept `cd82` as a limit of novelty-driven exploration: a game where progress needs
  moves that look like nothing is happening.

**Decision, 30 Sept 2026: (c).** Human: "Accept c". `cd82` is recorded as a known limit of
the novelty bandit. Option (a) is revisited only if period-3 bars turn up on other games,
which a cheap offline count on tune can check first. No fix is pre-registered.

---

## E11 — Object-targeted clicks inside the bandit (design P2)

Drafted 30 Sept 2026 from `documents/research_design/next_phase_experiment_design.md` P2.
Human instruction: "Go with P2"; **approved as drafted** the same day
(`DECISION-c37f464e`), before any E11 code or run. Genesis task `T-E11a`.

**Why this differs from the design's P2.** The design compared object clicks with
**random coordinates**, inside E4's random + prune. Since then the bandit (B) has become the
statistical baseline, and design §5 rule 2 says each experiment's control is the best
earlier policy. B already clicks by **colour arm**: it picks a colour, then a cell of that
colour **uniformly**. So a colour's largest region, often the background, gets almost
every click, and small objects of the same colour are rarely hit. E11 changes **only which
cell a colour arm clicks**. The bandit's arms, pooling, reward and judge are untouched, so
the comparison isolates object targeting.

| | |
| :-- | :-- |
| **Question** | Inside the bandit, do clicks aimed at objects clear more levels than clicks at a uniformly random cell of the chosen colour? |
| **Capability isolated** | perception for action generation (where a click lands). Arm choice, learning and memory are unchanged. |
| **Control B** | E9's bandit unchanged (`--policy arms-ucb`): a colour arm clicks a uniformly random cell of that colour. |
| **Treatment B_obj** | the same bandit, except that a colour arm clicks **one object of that colour**. The colour's cells on the last layer are split into 4-connected components, a component is chosen uniformly, and the click goes to its cell nearest the component's centroid (ties by reading order: row, then column). `--policy arms-ucb-obj`. Keyboard arms, arm keys (so pooling and dead-arm memory), the reward, the UCB constant and the judge are identical. |
| **Information** | both see the same frame; B_obj also computes the components of the chosen colour. |
| **Games, seeds, budget** | the same 17 held-out games; verdict on 16 (`r11l` outside). 12 verdict games offer clicks; on the 4 keyboard-only games (`g50t`, `re86`, `tr87`, `wa30`) the two conditions are identical by construction. **Episodes 220–259** (40 seeds, never used), run seed 0, **1,000 actions** (the bandit's validated budget). |
| **Implementation checks** (before held-out) | **(i)** unit: on synthetic frames, a colour with k components yields k candidate cells, one inside each component, at the centroid-nearest cell; a single large region yields one candidate. **(ii)** `dc22` and `ft09` (tune): on the first frame, every component of every colour has a candidate inside it (the design's check). **(iii)** switch: on keyboard-only games, B_obj's episode equals B's exactly. **(iv)** safeguards (E5's), and replay of one saved episode per condition after the run. **(v)** tune no-harm, 8 tune games × episodes 0–2 × 1,000: B_obj's tune clears ≥ B's − 1, or E11 stops at tune. |
| **Success** | per seed, B_obj − B clears over the 16 verdict games; one-sided exact sign test, ties dropped: **p < 0.05**, total clears higher, and the concentration rule holds (survives removing the largest-gain game; ≥ 2 games improve). A pass without concentration is **narrow**. |
| **Also reported** | click-game-only totals; per-game clears; dead-move rate (common judge); distinct masked states/100; mean components per chosen colour; B_obj's click share on the background colour against B's. |
| **Confounds** | the target is part of a large region (one component, one candidate); animated frames can split an object into several components; a colour arm's pooled estimate now mixes objects of one colour. Assumption A5 (components approximate objects) is **UNKNOWN**. |
| **Adaptivity** | not motivated by inspecting these held-out games (the design predates it), but the 17 games are the same ones used since E5 (A13). |
| **Stop** | one run; nothing changed after results are seen. |
| **Execution** | local CPU, **2 processes** (4 exhausted memory in E10); results `experiments/e11_{ucb,obj}_1000.json`; verdict by `e0_analyze.py --e11-verdict experiments`. About 30–60 minutes of CPU on mains power. |
| **If supported** | object targeting becomes the bandit's click generator, and a candidate for a later build (its own task and approval). |
| **If narrow** | report the affected games; no general claim. |
| **If falsified** | click targeting is not the bottleneck for the bandit; colour-uniform clicks stay. |

### Amendment, 30 Sept 2026 — E11 implementation checks pass

Code: `object_cells` and `_object_click_data` in `src/agents/graph_explore.py`;
`ArmBandit(ucb=True, objects=True)` (`--policy arms-ucb-obj`). Both conditions now count
clicks and clicks on the frame's commonest colour. B's play is unchanged: the E6–E10
replays and Build 4's equivalence tests pass. `e0_analyze.py --e11-verdict` is built on the
shared function; the E8–E10 verdicts are unchanged.

| Check | Result |
| :-- | :-- |
| (i) unit | **pass**: 3 components of one colour → 3 candidates at the centroid-nearest cells; a background region → 1 |
| (ii) `dc22`, `ft09` first frame | **pass**: for every colour, one candidate per 4-connected component, checked against an independent union-find labelling |
| (iii) switch | **pass**: on `ls20` (keyboard only) B and B_obj play the same episode |
| (iv) safeguards | **pass** on tune; replay after the held-out run |
| (v) tune no-harm, 8 × 3 × 1,000 | **pass, at the margin**: B 4 clears, B_obj 3 (`sc25` 1 → 0; `tn36` 3 each) |

**Two observations from tune, recorded before the held-out run.**
- **A premise of the block was overstated.** B clicks the frame's commonest colour on
  only 0.06 of clicks (B_obj 0.07): the background is one colour arm among many. The
  difference E11 tests is **within** a colour. B spreads a colour's clicks over its cells,
  so a colour's largest component absorbs most of them; B_obj weights every component
  equally.
- **B_obj reached fewer distinct masked states on tune** (445 per episode vs 513). Clicking
  an object's centroid-nearest cell is less varied than clicking anywhere in it, a
  possible cost as well as a benefit.

**Status:** pre-registered 30 Sept 2026; checks pass; held-out run below.

### Amendment, 1 Oct 2026 — E11 verdict: falsified (totals and RHAE favour B_obj; the per-seed test does not)

One run, local CPU, commit `b68511e`. **How it ran:**
- Two attempts were stopped by Claude Code under whole-machine memory pressure (8 GB, about 1 GB
  free with the editor, browser and two Claude sessions open). A probe found **no leak in the runner**:
  memory stayed flat at about 300 MB over 40 episodes, with about 2 Python objects added per episode.
- The completed run went one process at a time. B ran 680 episodes in one pass. B_obj ran in four
  resumable chunks of 10 episodes, merged into one file.
- B_obj ran about 4× slower than B: its pure-Python flood fill runs on every click.

Results: `experiments/e11_{ucb,obj}_1000.json`; trajectories in `experiments/build/e11/`
(not tracked). Every run exited 0; no redraws; IDs unique; one initial frame per game; no
fast clears. The replay test re-plays `cd82` episode 220 for B and B_obj exactly,
including from the merged chunk file.

| 1,000 actions, 16 verdict games × 40 seeds | B | B_obj |
| :-- | --: | --: |
| Verdict clears | 209 | 230 |
| Clears on the 12 click verdict games | 207 | 228 |
| RHAE, verdict / all 17 | 0.1192 / 0.2214 | 0.1488 / 0.3253 |
| Clicks on the frame's commonest colour | 0.12 | 0.08 |
| Dead-move rate; masked states/100 | 0.140; 66.2 | 0.139; 67.1 |

**Sign test:** 18 wins, 13 losses, 9 ties, one-sided p = 0.237. **Verdict: FALSIFIED.**
- **The per-game picture is mixed.** Six games improve: `lf52` 23 → 32, `lp85` 58 → 71,
  `sp80` 13 → 19, `cd82` 7 → 10, `ka59` 0 → 1, `m0r0` 18 → 19. Two lose: `vc33` 68 → 61 and
  `ar25` 18 → 13.
- **Without the largest gain** (`lp85`): 159 vs 151, p = 0.286.

**Reading.** Totals (+21 clears) and RHAE (0.119 → 0.149 on the verdict games, 0.221 →
0.325 on all 17) both favour object clicks. The pre-registered per-seed test does not: the
seed-to-seed spread is large next to the effect. By the rule, colour-uniform clicks stay.
The RHAE gain says that where B_obj clears, it clears in fewer actions, an efficiency
effect that the clears-based test does not measure. **The tune observation (fewer distinct
states) did not carry over:** 67.1 vs 66.2 per 100 actions. No re-run or
re-parameterisation is allowed under this block. A test of object clicks on efficiency
(RHAE as the primary metric) would be a new pre-registration, adaptive on this result.
- E11 stops here.

---

## Build 6 — E10's death memory in the submission

Written 1 Oct 2026. Human instruction: "start build 6" (`DECISION-09885665`). Genesis task
`T-B6`. Built and rehearsed here; **not pushed and not submitted**.

**Why.** E10's death memory (B′) was **narrow**: 245 vs 227 verdict clears, carried by
`sp80` (18 → 30); without `sp80`, 215 vs 209, p = 0.119. B′ was therefore not adopted as
the statistical baseline, and under E10's own block a hidden-set submission is the rule's
**only unseen test**. Build 6 is that test. It is Build 4 (E9's bandit, bar-only masked
judge, 1,000 actions) plus one rule: when a move ends the game, that (screen, arm) pair is
excluded on that screen for the rest of the game, exactly as E10 defined it.

**The agent.** `submission/my_agent.py` gains a second switch, `DEATH_MEMORY = True`,
beside Build 5's `UCB`, and a per-screen `_deadly` set. A fatal move is recorded against
the masked screen it was made from in **both** conditions, as the experiment does; only
the switch acts on it. The exclusion runs after the dead-arm filter and before the
all-arms fallback, in `ArmBandit`'s order, so the fallback can still return a fatal arm
once every other arm is dead — the behaviour E10 tested, not a stricter version of it.
The repository now ships Build 6; `build_submission.py --no-death-memory` rebuilds
Build 4 and `--uniform` rebuilds Build 5 (it drops both rules, since Build 5 predates the
death memory). All three were rebuilt and their switches checked.

**Tests** (`tests/test_b4_agent.py`, 102 → 109): the equivalence check now runs **three
builds × four games** — Build 6 against `ArmBandit(ucb=True, death_memory=True)`, Build 4
against `ucb=True`, Build 5 against `ucb=False` — on `lp85` (click arms), `vc33` (a masked
row-0 bar), `ls20` (keys and a two-row bar) and **`sp80`**, added because it is the only one
of the four where the new rule fires. A unit check also asserts that a killed (screen, arm)
pair is excluded on that screen afterwards, and that the next three picks are the other
three arms.

**A seed made the first version of that test vacuous, and the test caught it.** On `sp80`
at the shared rng seed 7, the bandit takes 24 resets but never dies twice on one screen,
so death memory never fires (0 exclusions) and Build 6's episode is identical to Build 4's.
A pre-added assertion — that `sp80` must both die and, in the Build 6 case only, exclude
something — failed, which is how this was found rather than shipped. A probe of seeds 0–7
(policy rng, `ArmBandit`, 1,000 actions, `sp80`):

| seed | B: resets / repeat deaths / levels | B′: resets / repeat deaths / exclusions / levels |
| --: | :-- | :-- |
| 0 | 38 / 13 / 0 | 39 / 0 / 291 / 0 |
| 1 | 38 / 17 / 0 | 37 / 1 / 412 / 0 |
| 2 | 36 / 11 / 0 | 38 / 0 / 309 / 0 |
| 3 | 38 / 19 / 0 | 38 / 0 / 280 / 0 |
| 4 | 38 / 24 / 0 | 34 / 0 / 230 / **1** |
| 5 | 37 / 13 / 0 | 36 / 0 / 379 / 0 |
| 6 | 38 / 16 / 0 | 33 / 0 / 297 / **1** |
| 7 | 24 / **0** / 1 | 24 / 0 / **0** / 1 |

Seed 7 is the outlier. `sp80` is pinned to seed 0 in the test, with the reason in a
comment. Across these 8 seeds B′ cleared a level in 3 episodes and B in 1, the direction
E10 measured; this is a diagnostic probe on a held-out game, not a verdict, and nothing
about the policy was changed from it.

**Local rehearsal of the scored rerun** (`submission/rehearse.py --games lp85,ls20,r11l
--require-level lp85`: reference gateway in competition mode, the real framework and
agent). Both passes:

| Game | Build 6 score (levels) | Build 4 score (levels) |
| :-- | --: | --: |
| `lp85` | 1.2159 (3) | 1.2159 (3) |
| `r11l` | 4.7619 (1) | 4.7619 (1) |
| `ls20` | 0 (0) | 0 (0) |

**Identical, because the rule never fires on these three games** — so the gate rehearsal
proves the pipeline, not the new rule. 26 ms/action with three agents, so 110 games ×
1,000 actions still project to about 40 minutes against the 9 h limit.

**One live A/B on `sp80`, and it goes the other way.** To check the rule fires through the
real framework and not only in the experiment loop, `sp80` was rehearsed twice, with the
switch on and off (the file restored from a hash-verified copy afterwards):

| `sp80`, one rehearsal episode | score | levels | resets |
| :-- | --: | --: | --: |
| `DEATH_MEMORY = False` (Build 4) | 0.9144 | 1 | 23 |
| `DEATH_MEMORY = True` (Build 6) | 0.0000 | 0 | 37 |

The rule plainly changes live play, which is what this check was for. The direction is
**one episode at one seed**, against E10's 40 and the 8-seed probe above, so it is not
evidence that Build 6 is worse; it is a reminder that a single `sp80` episode is noise and
that E10's own gain was narrow. It is recorded because it was seen before the submission
decision, not after it.

**Reading, fixed before the result** (`DECISION-09885665`). Build 4 scored 0.15. Each
score is one submission at two decimals, so a difference of **≤ 0.01 is no difference**.
With Build 6's score *s*:
- ***s* ≥ 0.16**: the death memory transfers to unseen games, as it did on `sp80`.
- **0.14 ≤ *s* ≤ 0.15**: it adds nothing visible on the hidden set, despite ending the
  loops it was built for. That is the outcome E10's narrow verdict predicts.
- ***s* ≤ 0.13**: it costs more on the hidden games than it saves. The confound to name
  first is the click arms: one death on a colour excludes every cell of that colour on
  that screen (E10's stated confound).

Build 6 changes exactly one rule from Build 4, so unlike Build 4 vs Build 3 this
comparison is clean.

**Status:** kernel `goutham12/arc-agi-3-build-6-death-memory` **pushed 1 Oct 2026 as
version 1** (private, CPU), at the human's request ("push the kernel"), with the
`independent-review` gate still pending at the time of the push. Its ordinary run completed
1 Oct 09:54 UTC and wrote `submission.parquet`. **Submitted by the human from the Kaggle
website on 3 Oct 2026; scored 0.15 — see the amendment below.**

### Amendment, 4 Oct 2026 — Build 6 on the hidden set: 0.15, indistinguishable from Build 4

Submission **56805419**, 3 Oct 2026 19:31 UTC, public score **0.15**. The source kernel is
`arc-agi-3-build-6-death-memory` v1, **confirmed by the human** against the competition's
submissions page: the Kaggle CLI does not expose a submission's source kernel, and no
description was typed at submit time, so the CLI listing alone could not identify it. (For
future submissions, typing a description makes the record self-identifying; Builds 1 and 3
are the only ones the CLI can name on its own.)

**By the rule fixed before the push** (≥ 0.16 transfers; 0.14–0.15 adds nothing visible;
≤ 0.13 costs more than it saves; a difference of ≤ 0.01 is no difference): **0.15 is
identical to Build 4's 0.15, so E10's death memory adds nothing visible on the hidden set.**

| Build | What changed from the one before | Hidden-set score |
| :-- | :-- | --: |
| 3 | random + prune, 300 actions | 0.07 |
| 5 | arms, masked judge, uniform choice, 1,000 actions | 0.12 |
| 4 | the same, with the UCB bandit | 0.15 |
| 6 | the same, plus E10's per-screen death memory | **0.15** |

**What this shows, and what it does not.**
- **It is the cleanest comparison the project has made.** Build 6 changed **exactly one
  rule** from Build 4 — unlike Build 4 vs Build 3, which bundled three — so the 110 unseen
  games isolate the death memory alone.
- **It is not an implementation failure.** The rule does what it was built to do: E10
  measured repeat deaths 534 → 34 overall, `sp80`'s 403 → 2, and `sp80` clears 18 → 30. The
  mechanism works; it just does not generalise.
- **So the finding is about generality:** death loops are not a limiting factor across the
  hidden set at 1,000 actions. **E10's narrow verdict — a gain carried entirely by `sp80` —
  is now confirmed on unseen games**, which is exactly what a narrow verdict predicts and
  why E10 did not promote B′ to baseline.
- **The claim is "nothing visible", not "exactly zero".** Each score is one submission at
  two decimals, so a gain below 0.01 cannot be seen, and there is no seed spread.
- **The pre-push caveats were right to be recorded.** The rehearsal games scored identically
  to Build 4 because the rule never fired on them, and the one live `sp80` A/B went against
  E10. Neither was evidence on its own, but neither now looks like an outlier to discount.

**Consequences.**
- Under design §5 rule 2, **the death memory earns no credit on unseen games**: B remains
  the statistical baseline that P6 and P8 must beat, and B′ is not promoted.
- **Which agent to ship is now a free choice** and the human's: Builds 4 and 6 are tied, so
  nothing argues for the more complex one. Parsimony favours Build 4; B′ remains available
  at no measured cost on the hidden set, and it does fix a real failure mode on one public
  game. Final submission is 2 Nov.
- **The hidden-set ladder stops here:** 0.07 → 0.12 → 0.15 → 0.15. Of the +0.08 over Build
  3, about +0.05 is the arms, judge and budget together, about +0.03 is the bandit, and
  **+0.00 is the death memory**.
- **The remaining gap is not death loops.** That leaves goal knowledge (E12's question),
  learned cross-game action ranking (P6, now unblocked by C1's frames) and deliberate
  investigation (P8) as the live candidates, and it is a reason to keep E12's question open
  rather than treat `cd82`-style goal blindness as settled.

---

## E12 — Oracle goal on tune games (design P5)

Drafted 1 Oct 2026 from `documents/research_design/next_phase_experiment_design.md` P5,
after Build 6 was pushed. Human instruction: "start the P5 pre-registration draft".
**Status: drafted, awaiting approval. No code written, no run made.** Nothing below is
settled until the human approves it, and the approval must be recorded before any E12
code exists.

**Why this differs from the design's P5.** The design's treatment is "the P4 agent plus a
hand-written goal predicate per tune level", navigating toward any recorded state that
satisfies it, against the P4 agent alone. Two things have changed since:

1. **P4 was falsified** (E6: Holm p 0.27 / 0.09, and G navigated on only 4–6% of actions).
   Building P5 on a planner that barely fires would confound "the oracle does not help"
   with "the navigation does not work", and would answer neither question.
2. **The bandit (B) is the statistical baseline** (E9, design §5 rule 2: each
   experiment's control is the best earlier policy).

So E12 keeps P5's question and its diagnostic status, and changes the mechanism: the
oracle enters as a **reward**, not as a navigation target, inside B. This is the same kind
of adaptation E11 made to P2, and it narrows the claim — see "What this does and does not
bound" below.

**What the oracle has to be, for the question to mean anything.** B's reward is already 1
for a level clear. A predicate that fires exactly when the level clears would therefore add
nothing, and E12 would measure noise. The informative predicate marks the state *before*
the clear: the `cd82` diagnosis found that progress there needs low-change set-up moves
followed by a commit move (ACTION5), and that "a new-screen reward cannot credit set-up
moves". An oracle that recognises "set-up complete" is exactly the signal novelty cannot
supply, so that is what E12 annotates.

| | |
| :-- | :-- |
| **Question** | If the agent could recognise a state from which the level clears, how much more would the bandit clear on tune? |
| **Capability isolated** | goal **recognition**, separated from goal **inference** (the oracle is hand-written) and from planning (no navigation; see the deviation above). |
| **Control B** | E9's bandit unchanged: `--policy arms-ucb`, code at `f18757b`. |
| **Treatment B_goal** | B, except that reaching a state satisfying the level's hand-written predicate scores reward 1, as a clear does. A clear still scores 1 and GAME_OVER still scores 0; novelty supplies the reward everywhere else. Arms, pooling, dead-arm memory, the UCB constant and the judge are identical. `--policy arms-ucb-goal`. |
| **Information** | the treatment holds privileged knowledge. That is the point of an upper-bound test, and is why it can never produce a held-out verdict. |
| **Annotation** | one predicate per tune game, **level 1 only**: `goal(frame) -> bool`, true on states from which the level can be cleared in one action. Written by hand from deterministic replays of **tune** episodes, before the comparison run, and committed and frozen before it. |
| **Games, seeds, budget** | the **8 tune games only** (`dc22 ft09 ls20 s5i5 sc25 sk48 tn36 tu93`). **Episodes 100–119** (20 seeds, unused on tune; tune episodes 0–2 were used for the E10/E11 no-harm checks). **1,000 actions primary** (the bandit's validated budget, as in E9–E11); 300 reported if time allows and decisive at neither. |
| **Success (diagnostic)** | the design's bar, kept as written: **B_goal clears at least 2× B on at least 3 of the 8 tune games**. No significance test and no concentration rule: tune is 8 games, the oracle is privileged, and this is a diagnostic. |
| **Also reported** | per-game clears both conditions; the **fraction of episodes in which a goal-satisfying state is ever observed**, which separates "cannot recognise the goal" from "never reaches it"; each predicate's sensitivity and specificity (below); dead-move rate; RHAE. |
| **Stop** | one run. Nothing is changed after results are seen, and no policy change follows without its own pre-registration. |
| **Execution** | local CPU, **one process at a time** (8 GB machine, as E11 required); results `experiments/e12_{ucb,goal}_1000.json`; verdict by `e0_analyze.py --e12-verdict experiments`. About 2 h at 1,000 actions for both conditions, plus about 35 min if 300 is run. |

### What this does and does not bound

- It bounds the value of **recognising a goal one action away**, given an agent that
  already reaches such states sometimes. It is an upper bound on **credit assignment**.
- It does **not** bound the value of full goal knowledge, of a distance-to-goal potential,
  or of planning toward a goal. A graded potential is a much larger annotation job; a
  planner leg is dropped because E6 falsified the planner.
- It cannot transfer: the oracle is hand-written per game. **E12 never produces a
  held-out verdict** (design P5 item 12), and no build may ship any part of it.

### Annotation protocol, and the checks that keep it honest

The annotation is the experiment's weakest point, so it is constrained in advance.

1. **Tune only.** Predicates are written from replays of tune games. No held-out game is
   inspected for E12. `cd82`, which motivated the design, is held-out and is **not** in the
   measurement set — so the motivating game cannot inflate the result.
2. **Written from replays, not from hashes.** The E5–E11 trajectories store hashes,
   actions and verdicts, not frames, so the states are recovered by **deterministic replay**
   of saved tune episodes with instrumentation, as the `cd82` diagnosis did.
3. **A predicate must be a description, not a snapshot.** It is written over frame
   contents (positions, colours, counts), never a frame hash or a cell-exact copy of one
   observed state. A predicate that can only match one recorded state is recorded as
   **single-instance** and its game's result is reported separately.
4. **Sensitivity and specificity, reported per game.** On replayed clearing episodes the
   predicate must be true at the state before the clearing move; on a sample of
   non-clearing states it must be false. Both counts go in the results table, whatever
   they are.
5. **Games where no clear was ever observed on tune** cannot be annotated this way. They
   are reported as **not annotated**, contribute to neither side of the 3-of-8 bar, and
   the bar is restated as 3 of however many were annotated — a number fixed and recorded
   **before** the comparison run.

### Implementation checks, before the comparison run

| Check | What it establishes |
| :-- | :-- |
| (i) unit | on synthetic frames built to satisfy and to violate each predicate, the predicate fires exactly where intended |
| (ii) sensitivity / specificity | per game, as item 4 above; recorded before the run |
| (iii) **switch** | with every predicate forced to `False`, B_goal's episode equals B's **step for step** on 3 tune games. This is the no-contamination check: it proves the oracle is the only difference |
| (iv) safeguards | E5's, all of them (unique episode IDs, initial-frame hash, fast-clear flag, JSON-lines trajectories), and a replay of one saved episode per condition after the run |
| (v) no tune no-harm check | deliberately absent: tune **is** the measurement set here, so there is nothing to hold back. Stated so that E12's result is not read as a policy improvement |

### Adaptivity, stated in advance

E12 is **adaptive**: it is motivated by the `cd82` diagnosis, which came from inspecting
held-out trajectories. Two things limit the damage. The measurement set is tune only, and
`cd82` is not in it; and the result is diagnostic, so it licenses no claim about unseen
games. What it can do is redirect P6, which is its purpose.

### What follows, either way

- **If the oracle helps** (bar met): goal recognition is worth building, so P6's learned
  ranker should predict goal-adjacency and not only novelty, and P8's goal hypotheses
  matter. The next experiment is goal *inference*, which has a falsifier the oracle does
  not: a learned or inferred predicate must beat novelty on **held-out** games.
- **If it does not help**: goal inference is deprioritised. The gap is exploration or
  manipulation, and P6 should target action ranking for reaching new states. Design §5
  rule 3 ("if P3 and P4 both fail and P5's oracle does not help, the CPU branch stops")
  does **not** fire, because P3 succeeded (E9) — the CPU branch continues either way.
- **If the goal-observed fraction is near zero** on most games, the finding is that the
  bandit rarely reaches goal-adjacent states at all. That is a statement about
  exploration, not about goals, and it would make a distance-to-goal potential the
  obvious follow-up rather than goal inference.

**Cost:** about a day, as the handoff estimates — most of it annotation (8 games, level 1
only), plus the replay instrumentation and about 2 h of CPU.

**Status:** drafted 1 Oct 2026, then **deferred the same day, before any E12 code
existed**, on the feasibility check below. Not approved for running. It runs after the P6
frame collection, which supplies what the annotation needs.

### Amendment, 1 Oct 2026 — E12 deferred: the annotation has no usable source yet

Checked before writing any E12 code, at the human's instruction to proceed. Three facts,
none of which the block had allowed for:

1. **Tune clears are almost nonexistent.** Across E10's and E11's tune checks (8 tune
   games x episodes 0-2 x 1,000 actions) only `sc25` cleared once and `tn36` three times.
   Annotating "the state before a clear" from replays is therefore possible on **2 of 8
   games**, and the block's 3-of-8 bar is unreachable as written.
2. **The game sources are obfuscated.** All eight tune games ship as readable Python
   (986-10,875 lines each), but their method names are randomised (`gvtmoopqgy`,
   `hgivzuhjvj`, ...). A win condition is recoverable only by reverse-engineering each
   game against a deliberate anti-reverse-engineering measure. Assumption A15 is therefore
   resolved as: engine source is present, engine *semantics* are not accessible without
   reverse-engineering, which is not done here.
3. **The experiment would most likely return an uninformative null.** A
   one-action-from-clear predicate pays out only where the bandit nearly clears. Given (1)
   it would almost never fire, so B_goal would equal B for a mechanical reason and E12
   would report "no effect" without saying anything about goals. That is the third outcome
   the block anticipated, and (1) makes it the likely one rather than a tail risk.

There is also no human-play agent and no frame renderer in the repository, so any
eyeball annotation needs a frame-dumping tool built first.

**Decision, 1 Oct 2026: reorder.** Human choice, from four options put to them (reorder;
annotate now with graded predicates; a two-game probe; reverse-engineer the sources):
**do the P6 frame collection first, annotate the oracle from those frames, then run E12.**
The reasons recorded with the choice: the collection is needed for P6 regardless, it does
not depend on E12's answer (only P6's *ranker design* does), and it produces exactly the
frames an annotator needs, which removes E12's null-risk instead of spending a day
discovering it.

**What E12 keeps when it returns.** The question, the diagnostic status, the tune-only
measurement set, and the switch check (iii) that proves the oracle is the only difference.
**What must be revisited:** the predicate's form, since a graded or distance-to-goal
potential fires often enough to be informative where a one-action predicate does not; and
the success bar, which must be restated against the number of games actually annotated and
fixed before the comparison run.

---

## C1 — Frame and label collection for P6 (and E12's annotation)

Drafted 1 Oct 2026, after E12 was deferred on its annotation source. Human choice:
reorder, "do the P6 frame collection first, annotate the oracle from those frames, then
run E12". **Status: drafted, awaiting approval. No code written, no run made.**

**`C` because this is a collection, not an experiment.** It states no hypothesis, has no
treatment, no control and no falsifier, and it **cannot be supported or falsified**. Its
criteria are integrity criteria, listed below. Nothing collected here may later be cited
as evidence for a policy claim; that takes an experiment with its own block.

**Why it is needed.** Checked 30 Sept: the E5–E11 trajectories hold hashes, actions,
clicks and verdicts, **not frames** (`play_one`'s `log.append`), so no ranker can be
trained from them and no state can be looked at. Two things now depend on having frames:
P6's offline comparisons, and E12's goal annotation, which has no other usable source
(the tune clear record is 2 games of 8, and the game sources are obfuscated).

| | |
| :-- | :-- |
| **Output** | one file per episode holding every transition as `(episode_id, game_id, level_id, seed, step, frame_before, action, click xy, frame_after, masked hash before/after, judge verdict, levels_completed, game state, behaviour policy name + version)`. |
| **Games** | the **8 tune games only** (`dc22 ft09 ls20 s5i5 sc25 sk48 tn36 tu93`). Held-out frames are **not** collected here: see "Held-out isolation". |
| **Behaviour policies** | **both B** (`--policy arms-ucb`, the baseline a ranker must beat) **and A′** (`--policy arms`, uniform over live arms). A′ is included because B concentrates its pulls — the `cd82` diagnosis found about 20% of them on one arm — so a dataset from B alone would inherit B's blind spots, and the P6 safeguards require that action coverage not hide untried actions. |
| **Seeds, budget** | **episodes 300–319** (20 seeds, unused by any experiment and clear of every used range), 1,000 actions, run seed 0. 8 games × 20 seeds × 2 policies = **320 episodes**, about 2 h of CPU at E9's rate. |
| **Storage** | frames are 64×64 per layer, so a raw episode is about 4 MB and the collection about 1.3 GB. Stored instead as the initial frame plus, per step, the **changed cells** `(row, col, value)` — which the judge already computes — falling back to a full frame when a step changes more than 512 cells, then `np.savez_compressed` per episode. The real figure is measured, not assumed: see check (i). |
| **Labels** | **not decided here.** The four label types (exact-frame, transient-masked, object-level, progress) are derived offline from the saved frames, each with a version field, so a label definition can change without re-collecting. The judge's verdict and mask are stored as the transient-masked label of record (E5's bar-only judge, the project's common measurement judge). Object-level labels are recomputed offline with E11's `object_cells`; progress labels are deferred and may need human judgement. |
| **Implementation** | one flag on the existing runner, `e0_random_smoke.py --save-frames DIR`, as every policy has been added since E5. No new runner. |
| **Execution** | local CPU, **one process at a time** (8 GB machine, E11's lesson), in **resumable chunks of 10 episodes**. |

### Integrity criteria — what "done" means here

| # | Criterion |
| :-- | :-- |
| 1 | **Replay-exact.** A saved episode, replayed from its seed, reproduces the stored frames **cell for cell**, and the stored masked hashes match the judge's. This is the criterion that matters: a frame store that does not match the run it claims to describe is worse than no store. |
| 2 | **Complete.** Every step of every episode is present, step indices are contiguous, episode IDs are unique, one initial frame per game, and no fast clears (E5's safeguards). |
| 3 | **Within budget.** Total size at or under the figure fixed by check (i). If it would exceed it, **reduce seeds, never games** — games are the transfer axis P6 is judged on. |
| 4 | **Coverage reported.** Per game and policy: pulls per arm, and arms never tried at all. Reported whatever it shows, because a ranker trained on a policy's choices cannot learn about actions that policy never made. |
| 5 | **Provenance.** Behaviour policy name and version, code commit, judge version and seed on every episode, so a transition can always be traced to the run that produced it. |

### Implementation checks, before the full collection

| Check | What it establishes |
| :-- | :-- |
| (i) **sizing probe** | collect **2 episodes** (one per policy, one game), report measured bytes per episode and the extrapolated total, and fix the size budget from that number before collecting 320 |
| (ii) **replay equality** | criterion 1 on those 2 episodes, cell for cell, before any bulk run |
| (iii) **no behaviour change** | with `--save-frames` on, an episode is **identical** to the same episode without it — same actions, resets, clears and hashes. Saving must observe, never perturb; this is the one way a collection can silently corrupt the thing it measures |
| (iv) safeguards | E5's, all of them, as criterion 2 |

### Held-out isolation

Only tune frames are collected. P6's split hierarchy also needs held-out games for its
transfer verdict, and that is a **separate, later step** under its own block, with three
rules fixed now: held-out frames are **read by machine only, never looked at by a human or
an assistant**; they are never used to pick a threshold, a label definition, a feature set
or a stopping point; and no episode crosses a partition. E12's annotation uses **tune**
frames only, and `cd82` — the game that motivated it — stays held-out and unannotated.

### What follows

- **P6** can then run its offline comparisons on the agreed footing: empirical
  action-success probability, state-conditioned nearest neighbour, a small supervised
  classifier and the contrastive ranker, all on the same representation, with pairwise
  ranking accuracy and AUROC for meaningful change.
- **E12** can be re-drafted against real frames: the predicate form revisited (a graded
  potential rather than one-action-from-clear), the annotated-game count known, and the
  success bar restated and fixed before the comparison.
- Neither follows automatically. Each needs its own approval.

**Cost:** about 2 h of CPU, plus the flag and the offline label derivation; well under
E12's day of annotation, and it unblocks both.

**Status:** drafted 1 Oct 2026 and **approved as drafted the same day**
(`DECISION-003d00ed`, human instruction "approve C1 and commit"), before any C1 code
existed. The three judgement calls were put to the human explicitly before approval:
both behaviour policies rather than B alone, changed-cell storage rather than whole
frames, and labels derived offline rather than fixed at collection time. Genesis task
`T-C1a`. Next: run checks (i)–(iv) and commit them, fix the size budget from the
measured figure, and only then collect.

---

### Amendment, 1 Oct 2026 — checks (i)–(iv) pass; the budget is 250 MB, not 1.3 GB

Code: `experiments/frame_store.py` (the store and its reader), one flag on the runner
(`e0_random_smoke.py --save-frames DIR`), `experiments/c1_probe.py` (the sizing report),
and `tests/test_c1_frame_store.py` (checks (ii), (iii) and the round-trip unit checks).
Nothing has been collected yet beyond the two probe episodes.

| Check | Result |
| :-- | :-- |
| (i) sizing probe | **done, and the estimate was wrong by two orders of magnitude.** `dc22` at 1,000 actions, one episode per policy: **53K and 59K on disk** against 4,148K and 4,436K raw, a **75–78x** saving. Extrapolated to the full 320 episodes: **18 MB**, against the block's 1.3 GB estimate. |
| (ii) replay equality | **pass**: a saved `ls20` episode replays **cell for cell** against the same episode held in memory, and every stored `masked_after` equals the judge's own hash for that step. |
| (iii) saving does not perturb play | **pass**: with the store attached and without it, the same seed gives identical actions, resets, distinct frames, masked states, clears, level actions, dead-move count and initial hash. |
| (iv) safeguards | unchanged from E5; the flag adds no new path through the loop other than handing each frame to the store. |

**The size budget is fixed at 250 MB** for the collection, about 14x the extrapolation,
which leaves room for games that churn more than `dc22` and for the multi-layer keyframes
below. If it is exceeded, **seeds are reduced, never games** (criterion 3).

**Finding, and it changes what P6 must say about its representation: a frame is not always
one layer.** Every tune game's *initial* frame is a single 64x64 int8 layer, which is what
the block assumed, but `ls20` emits **6-layer frames mid-episode** (4 of 121 frames on
episode 0). The store was written to fail loudly rather than mis-save, and it did: the
first version stacked keyframes and raised on the shape change. Keyframes now carry their
own shapes, and a step whose shape differs from the frame before it is always a keyframe.

Two consequences, neither of them C1's to settle:
- **P6 must declare what its state representation does with a multi-layer frame.** The
  policies already differ: the judge hashes *all* layers, while `last_layer` - what every
  click arm reads - keeps only the last. A ranker trained on one and evaluated through the
  other would be measuring two different things.
- **E12's annotation will meet these frames too.** A goal predicate must say which layer
  it reads, or it will be ill-defined on exactly the transition frames where something is
  happening.

**Probe observations, recorded because they are cheap and relevant:** `dc22` at 1,000
actions cleared nothing under either policy, with 9–11 resets, which is consistent with
the tune clear record that deferred E12.

**Next:** collect the 8 tune games x episodes 300–319 x 1,000 actions under both B and A',
one process at a time in resumable chunks of 10, then report action coverage per game and
policy (criterion 4).

---

### Amendment, 1 Oct 2026 — C1 collected: 320 episodes, 35 MB, all five criteria hold

Collected at commit `2d796cd`, the 8 tune games x episodes 300–319 x 1,000 actions under
both B (`arms-ucb`) and A' (`arms`): **320 episodes, 323,767 frames, 320,000 steps,
35 MB on disk** (111K per episode). Stores in `experiments/build/c1` (not tracked); run
reports `experiments/c1_arms*.json`; the criteria are reported by
`experiments/c1_report.py`, read from the stores themselves rather than from the run
reports, because the stores are the dataset P6 will train on.

| Criterion | Result |
| :-- | :-- |
| 1 replay-exact | **pass.** Six sampled episodes across `dc22` (click arms, the period-3 bar), `ls20` (multi-layer frames), `tn36` and `sk48` replay **cell for cell**, with every stored `masked_after` equal to the judge's own. The mechanism is also tested on a fresh episode in `tests/test_c1_frame_store.py`. |
| 2 complete | **pass.** 320 stores, 0 duplicate episode ids, every step index contiguous from 1, every episode opening on a reset frame, no integrity problems, one commit across the whole collection. |
| 3 within budget | **pass.** 35 MB against the 250 MB budget. Per-episode cost is 111K, about twice the `dc22` probe's 56K, because other tune games churn more than the probe game. |
| 4 coverage reported | **done, and it refutes part of the block's own reasoning** — see below. |
| 5 provenance | **pass.** Every episode carries its id, game, seed, rng seed, policy, budget, judge version, store format and the commit `2d796cd`. |

**Correction: the stated reason for collecting under both policies was partly wrong.** The
C1 block justified including A' on the grounds that a dataset from B alone "would inherit
B's blind spots", since "a ranker cannot learn about actions the collecting policy never
made". In this data the breadth runs the other way. **No arm was pulled by A' that B never
pulled**, while B pulled arms A' never did on three games (`dc22` 2, `s5i5` 3, `sc25` 2).
The reason is that a click arm is a colour *on screen*: B reaches more distinct screens, so
more colours — and so more click arms — exist for it to pull at all.

What A' does supply is **balance, not breadth**. Its pulls are spread far more evenly over
the arms it does see:

| Game | top-arm share, A' | top-arm share, B | distinct arms A' / B |
| :-- | --: | --: | --: |
| `ft09` | 0.15 | **0.37** | 8 / 8 |
| `tn36` | 0.17 | **0.36** | 8 / 8 |
| `sk48` | 0.08 | 0.19 | 16 / 16 |
| `dc22` | 0.08 | 0.14 | 14 / 16 |
| `sc25` | 0.09 | 0.13 | 12 / 14 |
| `s5i5` | 0.26 | 0.27 | 7 / 10 |
| `ls20` | 0.26 | 0.29 | 4 / 4 |
| `tu93` | 0.28 | 0.26 | 4 / 4 |

So both policies earn their place, for the opposite reasons to the ones given: **B for
breadth of arms and screens, A' for balance across them.** On `ft09` and `tn36` — keyboard-
only games, 8 arms each — B puts over a third of its pulls on one arm where A' puts a
sixth, which is the skew a ranker trained on B alone would learn as the world. P6 must
state which policy's transitions it trains on, or report both.

**Not done, and not C1's to do:** the label derivation (the four label types, each
versioned, from these frames), and any held-out collection, which stays a separate block
under the three isolation rules.

---

## C2 — Label derivation from C1's frames

Drafted 4 Oct 2026, after Build 6's hidden-set null. Human instruction: "draft the register
block first". **Status: drafted, awaiting approval. No C2 code written, no pass made.**

**`C` again, for the same reason as C1:** no hypothesis, no treatment, no falsifier,
**cannot be supported or falsified**, and nothing it produces may be cited as evidence for a
policy claim. Integrity criteria replace success criteria.

**Why it must happen before any model sees the data.** The handoff's own standard (§8.4) is
that the meaningful-change label is "a critical experimental variable" and that the change
detector must not be silently improved inside a model comparison. C2 therefore **fixes the
label definitions, in writing, before P6 exists**. If a later block wants a different label,
that is an ablation with its own pre-registration, not an edit here.

### What the scope actually is, which is smaller than it looked

Checking the stores first changed the job. **Two of the four label types need no derivation
at all:** every stored step row already carries `exact_before`/`exact_after` and
`masked_before`/`masked_after`, so those labels are a comparison of two strings already on
disk. C2's only real computation is the object-level label, and its only real risk is the
mask that label depends on.

| Label | How it is obtained | Status |
| :-- | :-- | :-- |
| **exact-frame change** | `exact_before != exact_after`, already stored per step | free; a documented accessor, not a derivation |
| **transient-masked change** | `masked_before != masked_after`, already stored per step (E5's bar-only judge, the project's common measurement judge) | free; the label **of record** |
| **object-level change** | 4-connected components per colour on the **masked** last layer, before and after | **the work**; see below |
| **progress / information change** | — | **not derived.** It needs judgement the frames do not contain. It is left unimplemented and reported as absent rather than approximated and named as though it were the real thing |

### The object-level label, defined before it is computed

Objects have no identity across frames here, and assumption **A5** (components approximate
objects) is still **UNKNOWN**. So the label is defined without any object matching:

- Components are 4-connected, per colour, on the **last layer with the judge's mask
  applied**, so a progress bar ticking cannot register as an object change.
- **`obj_structural`**: the multiset of component sizes, per colour, differs between before
  and after — an object appeared, vanished, split, merged or changed size.
- **`obj_moved`**: that multiset is unchanged but the component cell sets differ — something
  of the same shape is somewhere else.
- **object-level change** = `obj_structural or obj_moved`. Both sub-flags are stored, because
  the distinction is more informative than their disjunction and costs nothing.

**The mask this depends on is not stored, and is rebuilt offline.** The stores hold each
step's masked *hash* but not the mask itself. It can be rebuilt by feeding consecutive stored
frames through `MaskedJudge`, because the judge needs only the before/after arrays and the
move key, and the move key is reconstructible: a keyboard move keys on its action value, and
a click keys on the colour under `(x, y)` on the before frame's last layer
(`LLMBaseline.move_key`). **Criterion 1 below is the check that this rebuild is faithful**;
if it fails, C2 stops rather than labelling against a mask that is not the one the run used.

### Budget, and the fallback that is renamed rather than quietly weakened

`scipy` is **not** installed and C2 will **not** add it: components are computed with the
repository's own pure-Python helper (E11's `object_cells`). E11 found that per-click flood
fill made `B_obj` about **4× slower**, and C2 needs components over every colour of every
frame, which is heavier. **320 episodes × 1,000 steps = 320,000 steps**, so the runtime is
a real risk and is measured, not assumed:

- **A timing probe on 2 episodes fixes the budget before the full pass**, exactly as C1's
  sizing probe did (where the estimate was wrong by two orders of magnitude).
- If full-frame components are too slow, the declared fallback is a **per-colour cell-count
  and centroid** label — pure NumPy, microseconds — which detects appearance, disappearance,
  resizing and movement per colour but **not splits or merges within a colour**. If the
  fallback is used it is named **`colour-level change`**, not object-level, and A5 is recorded
  as untested rather than approximated. The weaker label does not inherit the stronger name.

### Output

One file, `experiments/c1_labels_v1.npz`, holding parallel arrays (episode index, step, and
one column per flag) with a JSON sidecar for the episode-id mapping, the label definitions,
the definition version, the label-detector version and the commit. **npz because neither
`pandas` nor `pyarrow` is installed**, and 320,000 rows of small integers compress to a few
MB. The `v1` in the name is load-bearing: a changed definition is a new file, never an
overwrite.

### Integrity criteria — what "done" means

| # | Criterion |
| :-- | :-- |
| 1 | **The rebuilt mask is the run's own mask.** For every step, the rebuilt judge's `masked_after` equals the stored one. This is the criterion that matters: labels computed against a different mask would describe a run that did not happen. If it fails, C2 stops and the fallback is replaying episodes through the environment, not guessing. |
| 2 | **Aligned.** Exactly one label row per stored step, per-episode counts matching the stores, every episode id resolvable through the sidecar. |
| 3 | **Deterministic.** A second pass over the same stores produces byte-identical output. |
| 4 | **Reproduces a number measured elsewhere.** The masked-change rate must reproduce the dead-move rate the experiments already report for these policies (about **0.14** for B and **0.30** for A′ at 1,000 actions, E9–E11). An external check that the labels mean what they claim, rather than only being self-consistent. |
| 5 | **Tune only.** No held-out frames are read, by machine or by eye. |

### Implementation checks, before the full pass

| Check | What it establishes |
| :-- | :-- |
| (i) **timing probe** | measured seconds per episode on 2 episodes, and the extrapolated total; the runtime budget and the full-components-vs-fallback decision are fixed from that number |
| (ii) **mask rebuild** | criterion 1 on those 2 episodes, before 320 are processed |
| (iii) **unit** | on synthetic frames: a component that moves sets `obj_moved` only; one that appears, vanishes or resizes sets `obj_structural`; **a bar tick alone sets neither**, because the mask removes it; an unchanged frame sets neither |
| (iv) **determinism** | criterion 3 on 2 episodes |

### What follows, and what C2 does not decide

- **P6's block must declare which label it trains on and which policy's transitions it uses**
  (C1 found B gives breadth of arms, A′ gives balance). C2 deliberately labels **all 320
  episodes under both policies**, because a label is a property of a transition, not of a
  policy — so that choice stays open and is P6's to state.
- **Which layer the representation reads** stays P6's to declare too. C2 commits only to
  computing the object label on the masked **last** layer, because that is where click targets
  and objects are defined; the exact and masked labels keep the judge's all-layer convention,
  as they always have.
- The **progress label remains undone**, and is the honest gap in this dataset.

**Cost:** the two free labels are an accessor. The object label is the timing probe plus one
pass, with the budget fixed from the probe.

**Status:** drafted 4 Oct 2026 and **approved as drafted the same day**
(`DECISION-27a48243`, human instruction "approved, run the checks"), before any C2 code
existed. Genesis task `T-C2a`.

### Amendment, 4 Oct 2026 — checks (i)–(iv) pass; full components stand, budget 51 minutes

Code: `experiments/c1_labels.py` (`check` and `derive` modes) and
`tests/test_c2_labels.py`. Nothing has been derived yet.

| Check | Result |
| :-- | :-- |
| (ii) **mask rebuild** | **PASS, and this was the block's main risk.** On two `dc22` episodes, **2,000 of 2,000 steps** rebuilt a mask whose `masked_after` equals the stored hash exactly — **0 mismatches**. The offline rebuild from stored frames plus a reconstructed move key is therefore faithful, and the environment-replay fallback is not needed. |
| (i) **timing probe** | **9.5 s per episode** with object labelling, **0.3 s** without it, so the full 320 episodes extrapolate to **about 51 minutes**. The runtime budget is fixed at **90 minutes**. |
| (iii) unit | **pass** (10 checks): component sizes count each colour's blobs; masked cells are not objects; a moved shape sets `obj_moved` only; appearing, vanishing, resizing and **splitting** set `obj_structural`; an unchanged frame sets neither; **a bar tick alone sets neither once masked, and the same tick unmasked sets `obj_structural`** — which is why the label is computed on the masked layer; `move_key` matches the live convention; `frame_hash` equals `frame_signature` when nothing is masked and changes with mask membership. |
| (iv) determinism | **pass**: a second pass over the same episode is identical row for row. |

**Decision fixed from the measurement: full 4-connected components, so the label keeps the
name `object-level`.** The `colour-level` fallback is **not** used, which means assumption
A5 (components approximate objects) is actually exercised rather than sidestepped.

**One correctness choice made while implementing, and worth stating.** Both frames of a
transition are read through the **same** mask — the one in force after the judge has observed
that transition. Masking the before frame with the older mask would turn a change in *mask
membership* into an "object change", manufacturing structural labels at exactly the moments
the judge first recognises a bar. Component sizes are cached between steps and recomputed
only when the mask changes, which also halves the flood fills.

**Sample rates, recorded before the full pass** (two `dc22` A′ episodes, 1,000 steps each):
exact 0.669 / 0.667, masked 0.603 / 0.582, `obj_structural` 0.425 / 0.375, `obj_moved`
0.154 / 0.181. `dc22` is the game whose period-3 bar is never masked, so its masked rate
sitting close to its exact rate is expected rather than reassuring; **criterion 4 is checked
on the full pass**, against the dead-move rates E9–E11 report.

**Next:** the full pass, then criterion 4 and the per-game rates.

### Amendment, 4 Oct 2026 — C2 derived: 320,000 rows; **criterion 4 fails as written, because I specified it against the wrong population**

The full pass ran in one process at commit `7f9c99c` and wrote
**`experiments/c1_labels_v1.npz` (320,000 rows, 123 KB) and its JSON sidecar**. Criterion 1
held throughout: the pass writes nothing if any step rebuilds a different mask, and it
wrote. Reported by `experiments/c1_labels.py verify`.

| Criterion | Result |
| :-- | :-- |
| 1 mask rebuild | **pass**, across all 320 episodes (the pass is written to abort otherwise) |
| 2 aligned | **pass**: 320 episodes, 320,000 rows, every step index matching the stores, none misaligned |
| 3 deterministic | **pass on the sample** in `check` mode; the full pass uses the same code path. Re-running 51 minutes to re-confirm was judged waste, and that is a stated limitation rather than a claim |
| 4 reproduces a number measured elsewhere | **FAILS AS WRITTEN — see below** |
| 5 tune only | **pass**: the eight tune games and nothing else |

**Criterion 4, exactly as it happened.** The block required the masked-change rate to
reproduce "the dead-move rates the experiments already report for these policies (about
**0.14** for B and **0.30** for A′ at 1,000 actions, E9–E11)". Measured on C1's episodes:

| Policy | steps | masked-change rate | 1 − masked | stored dead-move rate | the figure I cited | label vs store disagreements |
| :-- | --: | --: | --: | --: | --: | --: |
| B (`arms-ucb`) | 160,000 | 0.764 | 0.236 | **0.235** | 0.141 | **0** |
| A′ (`arms`) | 160,000 | 0.620 | 0.380 | **0.378** | 0.300 | **0** |

**The labels are not what failed.** On all 320,000 steps my `masked` label is exactly the
negation of the runner's own `measured_dead`, outside the two cases where the definitions
legitimately differ (a GAME_OVER or a clear is never called dead) — **zero disagreements**.
The label pipeline agrees with the record written independently by the runner at collection
time, and criterion 1 already showed the stores reproduce the run's own masked hashes.

**What failed is my specification of the criterion.** 0.141 and 0.300 are E9's figures over
the **16 held-out verdict games**. C1 collected the **8 tune games**. The dead-move rate is
game-dependent, so those numbers were never the right target, and no tune-set dead-move
rate for B or A′ exists anywhere in this register to compare against (the tune dead-move
figures at E3 are an LLM policy, and E5's are held-out). **The criterion was unsatisfiable
as written, and I wrote it that way.** It is recorded as mis-specified rather than quietly
rebased onto a number that would pass.

**The substantive observation underneath it, which is worth more than the check was.** Tune
games are deader than held-out games for both policies: B 0.235 against 0.141, A′ 0.378
against 0.300. **The direction replicates** — the bandit still cuts the dead-move rate
substantially (0.378 → 0.235, about 38%) — but the magnitude does not (held-out was 0.300 →
0.141, about 53%). **Consequence for P6: the label base rates differ between the population
it would train on and the population it is judged on**, so P6's block must state how it
handles that shift rather than assuming tune rates transfer. This is the kind of thing C2
existed to surface before a model was fitted.

**Per-game label rates** (20 episodes per cell, 1,000 steps each):

| Game | policy | exact | masked | structural | moved | object |
| :-- | :-- | --: | --: | --: | --: | --: |
| `dc22` | B / A′ | 0.735 / 0.668 | 0.679 / 0.589 | 0.445 / 0.394 | 0.208 / 0.169 | 0.653 / 0.563 |
| `ft09` | B / A′ | 0.369 / 0.230 | 0.369 / 0.230 | 0.247 / 0.114 | **0.000 / 0.000** | 0.247 / 0.114 |
| `ls20` | B / A′ | 0.983 / 0.999 | 0.963 / 0.954 | 0.715 / 0.395 | 0.226 / 0.548 | 0.941 / 0.943 |
| `s5i5` | B / A′ | 0.969 / 1.000 | 0.582 / 0.435 | 0.580 / 0.434 | **0.000 / 0.000** | 0.580 / 0.434 |
| `sc25` | B / A′ | 0.932 / 0.831 | 0.932 / 0.831 | 0.527 / 0.402 | 0.097 / 0.057 | 0.624 / 0.459 |
| `sk48` | B / A′ | 0.851 / 0.510 | 0.851 / 0.510 | 0.643 / 0.286 | 0.088 / 0.054 | 0.732 / 0.339 |
| `tn36` | B / A′ | 1.000 / 1.000 | 0.754 / 0.457 | 0.631 / 0.189 | 0.006 / 0.009 | 0.637 / 0.198 |
| `tu93` | B / A′ | 1.000 / 1.000 | 0.980 / 0.955 | **0.039 / 0.015** | **0.565 / 0.636** | 0.604 / 0.651 |

Three things in that table a later block must not read past:
- **`obj_moved` is exactly 0.000 on `ft09` and `s5i5`** and near zero on `tn36`. On those
  games no transition preserves the per-colour multiset of component sizes, which is
  plausible for games whose moves fill or clear cells rather than translate shapes — but it
  means `obj_moved` carries no signal there, and anything leaning on it should check that
  first rather than assume a near-zero rate is a measurement.
- **`tu93` is the mirror image**: `obj_structural` 0.015–0.039 while `obj_moved` is 0.57–0.64.
  Almost every change there preserves sizes, which is what a game of moving a piece around
  should look like, and is the closest thing here to evidence that the component label
  tracks something real (A5).
- **`exact` 1.000 with `masked` 0.457–0.754 on `tn36` and `s5i5`** shows the masked judge
  doing most of its work on those games: every move changes a pixel, and only some change
  the state identity.

**Decision, 4 Oct 2026: (a).** Human choice from the two options put to them
(`DECISION-8df3e916`). **Criterion 4 is recorded as mis-specified**, not rebased onto a
number that would pass, and C2's integrity case rests on what the evidence supports:

- **criterion 1** — the offline-rebuilt mask reproduces **every** stored `masked_after`
  across all 320 episodes;
- **criterion 2** — 320,000 rows, every step index aligned to the stores, none misaligned;
- **criterion 3** — determinism verified on the sample, with the full pass on the same code
  path, recorded as a stated limitation rather than a claim;
- **criterion 5** — the eight tune games and nothing else;
- and the **zero disagreements** between the `masked` label and the runner's own,
  independently written `measured_dead` across all 320,000 steps.

Option (b) — measuring a tune dead-move rate independently — was **declined**, because it
runs the same code path as the collection and would largely re-establish what criterion 1
already proved.

**What this costs, stated plainly:** C2 has **no external-validity check**. Every criterion
it passes is internal to the collection and its own pipeline. The labels are faithful to the
run that produced them; nothing here shows the label *definitions* are the right ones, and
nothing could, short of a model being fitted and judged. **A later block must not cite C2 as
evidence that these labels are good targets — only that they are the targets they claim to
be.** The substantive finding from the failed check (the tune/held-out base-rate shift)
stands, and P6's block must state how it handles it.

---

## Register-level stop conditions

| Condition | Action |
| :-- | :-- |
| E0 falsified and no dense metric separates conditions either | stop; report the floor problem as the finding. A negative result with a clean baseline is publishable within the milestone and is not a failed milestone. |
| Milestone #2 deadline within 7 days | freeze the register, write up whatever has a verdict, mark the rest "not run" with the reason. |
| Any experiment beats its falsifier | do not immediately build on it. Re-run at N = 10 on held-out first. One surviving delta at N = 5 is a candidate, not a result. |

---

## Open decisions

1. **Model** — Qwen 2.5 7B vs Gemma 3. Decided empirically at E0 on floor and variance.
2. **Seed budget** — N = 5 is the floor. Raise it if baseline variance turns out wide; that is an E0 output.
3. **Held-out split** — 8 tune / 17 held-out is provisional. Fix at E0, then never touch it.

## Feeding this register

Two inputs from the peer review are still owed, and both may add blocks here:

- **Backward pass over the 58** — re-read the nine descriptive Elicit columns
  asking what each paper's mechanism suggests that H1–H6 does not name. New column
  `suggests_experiment`. `Stated limitations` is the richest source; it is a list of
  open problems written by people who tried.
- **Cross-domain pass** — 15–20 sources from developmental psychology, Gibsonian
  affordances, cybernetics (Ashby) and perceptual control (Powers), one per cluster
  question, filed as `cluster_origins.md`. These are the fields where the cluster
  questions were first posed. Gibson is already logged above as a live threat to E2.
