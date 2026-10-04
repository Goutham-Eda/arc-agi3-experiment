# Next phase: what does random + prune lack?

**An experiment-design document.** Written 19 September 2026. No experiment in it has
been run, no implementation code has been written, and no numerical result in it is new:
every number is quoted from the E0–E4 record or from a cited external source.

**Question.** *What is the simplest additional capability that can solve failures left by
random action selection plus dead-action pruning?*

**Sources read.** `documents/writeup/e0_e4_writeup.md` (committed version, identical to
`HEAD`) and `documents/writeup/arc_agi_3_session_handoff.md` (dated 18–19 Sept, an
external summary). Both are treated as research context. Where they differ from each
other or from the canonical register, `research_prep/notes/experiment_register.md`, the
register's newer corrected record is preferred (see §0).

---

## 0. Discrepancies found, and which record is used

| # | Discrepancy | Record used |
| :-- | :-- | :-- |
| D1 | The handoff lists evaluation safeguards as mandatory (unique episode IDs, initial-state hash, impossible-clear flags, closing the environment). **The code enforces only one of them**: a fresh environment per episode, with a regression test. `experiments/e0_random_smoke.py` records no episode ID, no initial-state hash and no impossible-clear flag (checked in source). | Treat the missing safeguards as **unbuilt infrastructure** (built in P1), not as existing protection. |
| D2 | The handoff numbers the next experiments E5 = Duck, E6 = Jev, E7 = hybrid. The register has **no E5/E6/E7 blocks**; nothing is preregistered under those names. | This document uses candidate IDs **P1–P8**. Register numbers are assigned only when a candidate is preregistered there. |
| D3 | The write-up says Duck "reports far higher public-game scores than anything here". Tufa's page gives a public-game mean of 1.6002 ± 0.4475 **without stating the scale**, so the comparison with our RHAE figures is not established. | Treat Duck's score as **not comparable** until the scale is verified (§7, A7). |
| D4 | The write-up's filename says E0–E4, but it also covers E3 (added 19 Sept). The handoff refers to it as `e0_e4_writeup(2).md`. | Same content; no conflict. |
| D5 | The handoff says E3 "was originally parked because a similar mechanism had already been published". The register adds that the unpark condition ("E1 and E2 both null") was **not met**: E3 ran by explicit human decision. | The register (the condition was not met). |
| D6 | Older handoff sections quote a random floor of 0.037 levels/game and "random clears `r11l` 5/5". Both were inflated by the replay bug. | The corrected figures: **0.0125** levels/game and **1/5**. |

---

## 1. Current evidence

### What E0–E4 established

- **Frozen Gemma-4 (E4B and 31B), choosing one action per turn from a text grid, does not
  beat random play at 80 actions.** Neither model cleared a verdict level; random cleared
  one in 80 verdict episodes (0.0125 levels/game, corrected).
- **The models' main failure is clicking cells that do nothing.** The exploration deficit
  is concentrated in click games (random 73.5, E4B 59.6, 31B 66.1 screens per 100
  actions); on keyboard-only games the models match random.
- **Blocking moves already seen to change nothing raises exploration**, for the model
  (E1: 68.6 → 74.4) and for random play (E4).
- **Random + dead-move pruning (E4) doubles verdict level clears at 300 actions on the
  public held-out games** (38 vs 19, 18/0/2 seeds). But **one game (`lp85`) supplies
  nearly all of it**, and on the 110 hidden games the entry scored **0.07**, the same
  as plain random.
- **Adding text to this model's prompt can make it worse.** In E2 (a harness-written
  button list) and E3 (LEARN/WIN labels plus a diary), dead-move rates rose, and `sk48`
  degraded badly both times.
- **This model follows a new output format poorly.** 67% of E3 replies omitted the
  required label.

### What E0–E4 did not establish

- **That frozen models cannot play ARC-AGI-3.** Only this interface, these two sizes, and
  this budget were tested. Milestone 1's 2nd and 3rd places used the *same* model,
  Gemma-4-31B, through a different interface (§1.1).
- **That controllability learning fails.** E2 tested one representation (cell-level
  bounding boxes blurred by step counters), and its null could not tell a bad probe from a
  wrong hypothesis.
- **That epistemic action selection fails.** E3's interface was mostly not used.
- **That failure memory is useless.** Repeated deaths almost never occurred at 80 actions.
- **That dead-move pruning generalises.** The hidden-set score did not move.
- **What random + prune fails on.** No experiment has yet asked *why* the other 15
  verdict games stay unsolved.

### 1.1 External facts that bear on the design

| Claim | Status | Source |
| :-- | :-- | :-- |
| Milestone 1 (to 30 June 2026) was won by Tufa Labs ("the Duck"), 2nd Reki, 3rd Md Boktiar Mahbub Murad ("forge"). | **VERIFIED** | [ARC Prize, Milestone 1 post](https://arcprize.org/blog/arc-prize-2026-milestone-1) |
| Duck runs Qwen 3.6 27B FP8 locally; the model writes Python in a live REPL; it perceives the board through rendered images, ASCII grids and segmentation tools; old messages are evicted ("infinite play via eviction"). | **VERIFIED** (as described by ARC Prize) | same |
| Reki runs Gemma-4-31B locally, renders recent frames as labelled images, and returns one JSON object per step describing changes and the next 1–4 actions, with reflection memory refreshed about every 10 steps. | **VERIFIED** (as described by ARC Prize) | same |
| forge (3rd) also uses Gemma-4-31B; its top-scoring run "turns off all of the extra machinery". | **VERIFIED** (as described by ARC Prize) | same |
| "Hand-crafted tools actually hurt the model; letting it improvise worked better"; gains came from "multimodality and better base models". | **COMPANY CLAIM** (Tufa, quoted by ARC Prize) | same |
| Duck's public-games mean is 1.6002 ± 0.4475 over 20 attempts per game; the scale is not stated. | **COMPANY CLAIM**; scale is an **OPEN QUESTION** | [Tufa Labs, Duck Harness](https://tufalabs.ai/research/duck-harness/) |
| Duck exposes `current_frame.segmentation` (connected components, object hashes, boundaries, containment, adjacency), `transitions`/`last_transition`, and `valid_actions`, and hides the raw numeric grid; actions include `MOUSE(row=…, col=…)`; its default cluster config requests two B200 GPUs. | **VERIFIED** (repository documentation) | [duck-harness ARC3-Inference README](https://github.com/Tufalabs/duck-harness) |
| Duck scored 1.03 on Kaggle. | **UNVERIFIED secondary report**; the Kaggle leaderboard figure is an **OPEN QUESTION** | [AlphaSignal](https://alphasignal.ai/news/tufa-labs-wins-25k-beating-frontier-ai-on-the-world-s-hardest-benchmark) |
| Frontier AI systems scored below 1% on ARC-AGI-3 as of March 2026. | **VERIFIED** (paper abstract) | [ARC-AGI-3 paper, arXiv 2603.24621](https://arxiv.org/abs/2603.24621) |
| Jev (TypeSafe AI, announced 15 Sept 2026) is not an LLM. It takes unstructured or structured program state and returns typed values with calibrated probabilities and confidence, trained with "RLCD". | **COMPANY CLAIM** | [TypeSafe AI, Introducing System One Models & Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev) |
| Jev: 70–500 ms per response; $0.042 per million input tokens; API only, early access by waitlist; text and structured state, "not on images (yet…)". Demos include Doom and Wikiracing. | **COMPANY CLAIM** | same |
| Whether Jev can be customised or trained on user examples, its context length, its determinism, and its licence. | **UNKNOWN — requires empirical verification** (not stated in the source) | same |
| Any Jev result on ARC-AGI, or any action-ranking benchmark. | **UNKNOWN** (none published in the source) | same |

**INFERENCE.** Reki's and forge's placement suggests our E0 interface (a text grid, one
action per turn, no images) may be a larger bottleneck than model size. Nothing in E0–E4
tested this.

---

## 2. Capability-gap map: what random + prune lacks

Random + prune remembers exactly one fact: *in this exact screen, this action (or a click
on this colour) changed nothing.* Each row below is a separable capability, ordered by the
simplest mechanism that could supply it. Every candidate in §3 isolates one row.

| Capability | What random + prune does | The gap | Simplest mechanism that could fill it | Candidate |
| :-- | :-- | :-- | :-- | :-- |
| **Perception of change** (state comparison) | Exact screen hash | On-screen clocks and step counters make a do-nothing move look like a change, so pruning misses dead moves. **VERIFIED in-project** on `dc22`. | Mask cells that change regardless of action; compare what is left | P1 |
| **Action generation** (what counts as a candidate click) | A uniform random coordinate | Clicks land mostly on the largest colour areas; small objects are rarely hit | One click candidate per connected object | P2 |
| **Learning action value** (statistical, within an episode) | Binary dead/alive, per exact screen | Doesn't learn that an action class tends to produce new states, or carry that across screens | Count-based estimates with an upper-confidence (UCB) bandit | P3 |
| **Memory + planning to explore** (transition graph) | None; after a death the random walk starts again | Deep states are rarely re-reached; each death costs the whole path | A graph of observed transitions, with shortest-path return to the nearest state that has untried actions | P4 |
| **Goal inference** | None | Doesn't know what state it is trying to reach | Measure its value first with an oracle goal on tune games, before building inference | P5 |
| **Learned prior over action usefulness** (across games) | None | Doesn't transfer "which actions matter" from other games | A small ranker trained on tune-game transitions (Jev-style); Jev itself only if access permits | P6 |
| **Model perception / interface** | — | The E0 model saw a text grid and gave one action per turn | The same frozen Gemma-4, with a rendered image instead of text | P7 |
| **Deliberate investigation + world-model reasoning** | — | No hypotheses, no tests, no mechanics model | A Duck-style REPL harness, reproduced and then compared | P8 |

**Separation of functions.** In every candidate, the preregistration states which function
changes. The categories are exploration, learning, memory, causal/world modelling, goal
inference, action selection and planning. For example, P3 changes *learning + action
selection* but not memory structure, while P4 changes *memory + planning* but not the
action-selection rule. The model is credited only with functions it performs itself;
harness substitutions are always counted separately.

---

## 3. Experiment portfolio

Ordered from cheapest and most diagnostic to most complex. "Best CPU policy" means the
strongest held-out policy among P1–P4 at the time a later experiment runs.

| ID | Research question | Capability isolated | Treatment vs matched control | Compute / tokens / build | Type |
| :-- | :-- | :-- | :-- | :-- | :-- |
| **P1** | Does judging change with clocks masked make pruning clear more levels? | Perception of change | random+prune with the masked judge vs random+prune with the exact hash (E4) | CPU, under 1 h; 0 tokens; ~1 day including safeguards | **Both**: safeguards + a common judge, and a scientific test |
| **P2** | Does clicking one cell per object, instead of a random coordinate, clear more click-game levels? | Action generation (object perception) | object-candidate clicks vs random-coordinate clicks, both with pruning and the P1 judge | CPU, under 1 h; 0 tokens; ~1 day | Scientific |
| **P3** | Does learning, within an episode, which action classes produce new states beat uniform choice? | Learning + action selection (statistical) | UCB bandit over action classes vs uniform over the same classes, both pruned | CPU, under 1 h; 0 tokens; ~1 day | Scientific (the non-model control for P6/P8) |
| **P4** | Does remembering transitions and navigating back to unexplored states clear more levels? | Memory + planning-to-explore | graph memory + return-to-frontier vs the same local rule without navigation | CPU, 1–2 h; 0 tokens; ~2 days | Scientific |
| **P5** | If the goal were known, how many more levels would search clear? | Value of goal knowledge (an upper bound) | oracle goal predicate + P4 planner vs the P4 planner alone, **tune games only** | CPU plus ~1 day of hand annotation | Diagnostic (never a held-out verdict) |
| **P6** | Does a learned cross-game action ranker beat within-episode statistics? | Learned prior (Jev-style) | a ranker trained on tune transitions vs the P3 bandit; optional Jev arm | CPU training + inference, ~2 days; Jev arm ≈ ~$9 by the company's price (**INFERENCE**) | Scientific |
| **P7** | Does the same frozen Gemma-4 play better from an image than from text? | Model perception / interface | image-rendered state vs the E0 text grid; otherwise identical | ~2–4 GPU-h (E4B); ~1.4M tokens per 85 episodes (**INFERENCE**); ~2–3 days | Both: verifies image support, and a scientific test |
| **P8** | Does a Duck-style investigation harness beat the best CPU policy, and does it discover the mechanics? | Deliberate investigation + world-model reasoning | Duck reproduction (public code) vs the best CPU policy at matched actions; ablations only after that | ~10–30 GPU-h (**INFERENCE**); tens of millions of tokens; 3–5 days | Both: reproduction first, then science |

### Detail for each candidate

Every candidate uses the same safeguards (P1 builds them) and the same split: tune = the
frozen 8 games, held-out = the frozen 17, verdict = 16 (`r11l` reported separately).
Every candidate uses the **concentration rule**:

> **Concentration rule.** A claim of improvement is made only if it survives removing the
> game with the largest gain, and at least 2 games improve. A result that fails either
> test is reported as "narrow: carried by `<game>`", never as general.

**P1 · masked state comparison.** *(Preregistered in §4.)*

**P2 · object-level click candidates**
1. **Question:** do clicks aimed at objects instead of random coordinates clear more
   levels in click games?
2. **Capability:** perception for action generation.
3. **Treatment / control:** the treatment's candidate clicks are one cell per 4-connected
   component (the cell nearest the component's centroid, ties broken by reading order),
   and the click is chosen uniformly among components not known to be dead. The control
   is a uniform random coordinate, as in E4. Both use pruning with the P1-selected judge,
   and keyboard actions are identical.
4. **Information:** both see the same frame; the treatment also gets its component list.
5. **Metrics:** primary, verdict level clears in the 12 click verdict games; secondary,
   dead-move rate (common judge), distinct masked states per 100, per-game clears.
6. **Budget / seeds / split:** 300 actions, seeds 100–119, held-out; tune is used only for
   an implementation check (every component on `dc22` and `ft09` receives a click).
7. **Success:** one-sided sign test over seeds, p < 0.05, plus the concentration rule.
8. **Falsifier / stop:** otherwise falsified; random coordinates stay the candidate
   generator.
9. **Cost:** CPU under 1 h; 0 tokens; about 1 day.
10. **Confounds:** games where the target is part of a large region; animated frames
    splitting components.
11. **Meaning:** positive → object perception is a missing capability, and later
    policies use object candidates. Negative → click targeting is not the bottleneck.
    Mixed → report the affected games.
12. **Type:** scientific.

**P3 · empirical action-success bandit.** *(Preregistered in §4.)*

**P4 · transition-graph memory with return-to-frontier.** *(Preregistered in §4.)*

**P5 · value of goal knowledge (oracle)**
1. **Question:** if the agent knew the level's goal, how much would a planner gain?
2. **Capability:** goal knowledge, isolated from goal *inference*.
3. **Treatment / control:** the treatment is the P4 agent plus a hand-written goal
   predicate per tune level. It navigates toward any recorded state that satisfies it,
   and otherwise explores. The control is the P4 agent alone.
4. **Information:** the treatment holds privileged goal knowledge. That is the point of
   an upper-bound test.
5. **Metrics:** tune-level clears; the fraction of episodes in which a goal-satisfying
   state is ever observed. That fraction separates "can't recognise the goal" from
   "never reaches it".
6. **Budget / seeds / split:** 300 and 1,000 actions, seeds 100–119, **tune games only**.
7. **Success (as a diagnostic):** the treatment clears at least 2× the control on at least
   3 of 8 tune games.
8. **Stop:** if the oracle doesn't help, goal inference is deprioritised; the bottleneck is
   reaching or manipulating states.
9. **Cost:** CPU; about 1 day of annotation (8 games, level 1 only), plus half a day of code.
10. **Confounds:** annotation errors, and goals that aren't a state predicate (e.g.
    sequences).
11. **Meaning:** positive → goal inference is worth building (P8's goal hypotheses
    matter). Negative → the gap is exploration or manipulation, not goals.
12. **Type:** diagnostic. It **never produces a held-out verdict**, because the oracle
    cannot transfer.

**P6 · learned action ranker (Jev-style)**
1. **Question:** does a cross-game learned prior rank actions better than within-episode
   statistics?
2. **Capability:** learned prior over action usefulness (transfer from other games).
3. **Treatment / control:** the treatment is a small ranker (logistic regression or
   gradient-boosted trees; the choice is fixed before training) that predicts
   P(novel masked state | features of the state, action and candidate). It is trained
   **only** on tune-game transitions logged by P3 and P4. Actions are sampled in
   proportion to predicted probability, with pruning. The control is the P3 bandit.
   An **optional Jev arm** gets the identical structured state and the identical
   candidate list, returns a typed ranking, and is compared with the local ranker. It is
   research-only: Kaggle scoring has no internet.
4. **Information:** equal per-step inputs. The ranker also carries tune-game experience;
   that transfer is the variable.
5. **Metrics:** verdict clears; ranker calibration (Brier score on held-out
   transitions); per-game gain.
6. **Budget / seeds / split:** 300 actions, seeds 100–119, trained on tune, tested on
   held-out.
7. **Success:** beats P3 by the sign test plus the concentration rule.
8. **Falsifier / stop:** otherwise, learned priors add nothing over counting, and the
   Jev branch (E6) is closed unless a cleaner interface appears.
9. **Cost:** CPU training and inference, about 2 days. The Jev arm's cost is **INFERENCE**
   only: roughly 2k tokens per call × 300 actions × 340 episodes ≈ 204M tokens ≈ $9 at the
   company's price.
10. **Confounds:** tune games are only 8, so distribution shift is likely; feature leakage
    of game identity.
11. **Meaning:** positive → fast learned decisions add value (a necessary condition for a
    hybrid). Negative → routine action ranking is already solved by counting.
12. **Type:** scientific.

**P7 · image vs text interface, same frozen model**
1. **Question:** does the same frozen Gemma-4 play better from a rendered image than
   from the text grid?
2. **Capability:** model perception and interface. **Nothing else changes.** It is still
   one action per turn, the same decoding, and no memory.
3. **Treatment / control:** the treatment is the current frame rendered as an image (same
   palette, a coordinate ruler drawn on it), with the system prompt changed only in the
   sentence describing the input. The control is E0's text grid (byte-identical prompts,
   already pinned by test).
4. **Information:** the same frame, in a different modality.
5. **Metrics:** verdict clears; dead-move rate; click-game distinct states; **compliance**
   (parse rate of a valid action, which must be ≥ 95% on tune for the verdict run to
   proceed).
6. **Budget / seeds / split:** 80 actions (matching E0), 5 seeds, held-out; tune first as
   a scaffold check.
7. **Success:** beats E0 E4B on verdict clears **and** reaches random + prune's click-game
   exploration, with the concentration rule.
8. **Stop:** if vLLM 0.23 cannot serve Gemma-4 image input (**UNKNOWN**), stop as
   infrastructure-blocked, not falsified. If compliance is below 95%, it's a scaffold
   failure and there is no verdict.
9. **Cost:** about 2–4 GPU-h at E4B (**INFERENCE** from E0 E4B at 78.8 min per 85
   episodes). Images cost more tokens per call (**UNKNOWN**).
10. **Confounds:** image token cost changes batching; the ruler's design.
11. **Meaning:** positive → interface is a bottleneck, and Reki-style multi-action becomes
    the next single variable. Negative → image input alone doesn't explain Reki's
    result.
12. **Type:** both.

**P8 · Duck-style investigation harness**
1. **Question:** does deliberate investigation (hypothesis, test, world model) solve games
   the best CPU policy cannot? And does it discover the mechanics?
2. **Capability:** deliberate investigation + world-model reasoning, as a package first.
   Components are separated only by later ablation.
3. **Treatment / control:**
   - **Stage A (reproduction):** Duck's public code with its own model (Qwen 3.6 27B FP8)
     on our 8 tune games, to check it runs and plays as documented.
   - **Stage B (verdict):** Duck vs the best CPU policy on held-out, with the **action
     budget matched in environment actions**. Duck may use unlimited thinking.
   - **Stage C (only after B is positive):** one ablation at a time, e.g. segmentation
     hidden, or eviction off.
4. **Information:** Duck gets segmentation, transitions and images through its REPL.
   That extra information is part of the package being tested.
5. **Metrics:** verdict clears; per-game clears; **mechanics discovery** (the fraction of
   hand-annotated tune-game mechanics that appear as a correct statement in Duck's logged
   REPL code or comments, scored by a fixed rubric); plan quality (the fraction of
   multi-action calls whose predicted effect, if stated, matches the observed one);
   tokens, latency and GPU-h.
6. **Budget / seeds / split:** 300 environment actions per episode, 5 seeds (GPU-limited),
   held-out.
7. **Success:** beats the best CPU policy on verdict clears (sign test over seed × game
   blocks, p < 0.05), plus the concentration rule.
8. **Stop:** if Stage A fails to reproduce or Duck can't run on our hardware, it's
   infrastructure-blocked. If Stage B is not better, investigation adds nothing
   measurable over the CPU policies at this budget.
9. **Cost:** **INFERENCE** 10–30 GPU-h; tens of millions of tokens; 3–5 days. The model
   is ~27B at FP8, so it's comparable to our 31B runs.
10. **Confounds:** a different model from ours (Qwen 3.6 vs Gemma-4), so model and
    harness change together. A Stage C ablation, or Duck run on Gemma-4-31B, is needed
    to separate them. Also mirror provenance (the register requires hash verification).
11. **Meaning:** positive → deliberate investigation is a real capability gap, and
    Stage C finds which part matters. Negative → the best CPU policy is as good at this
    budget.
12. **Type:** both.

**A hybrid (handoff "E7") is not proposed.** It becomes justified only under the rule in
§5, step 7.

---

## 4. Detailed preregistrations: the three highest-priority experiments

The top three are **P1, P3 and P4**. They are the cheapest experiments that can falsify a
capability claim. They need no GPU, no tokens and no model, and together they establish
the non-model controls that any Duck- or Jev-style component must beat.

### Common protocol (applies to P1, P3, P4)

**Environment and safeguards.** These are built in P1, and every run must pass them or
the run is void:

1. **A fresh environment per episode:** `Arcade.make(game, seed=0)` inside the episode
   loop. This is already enforced and tested.
2. **Episode ID:** `"{experiment}-{condition}-{game}-{seed}"`, asserted unique per report.
3. **Initial-state check:** after the first `reset()`, record the blake2b hash of the frame
   and `levels_completed`. Assert `levels_completed == 0`, and assert all episodes of one
   game share one initial hash. A mismatch voids the run.
4. **Impossible-clear flag:** any level cleared in ≤ 2 actions is flagged. A flagged run
   is void until inspected. (The shortest verified real clear is 5 actions, `sp80`
   seed 11.)
5. **Full trajectory log** per episode, as JSON lines: step, action, click (x, y), policy
   decision vs harness substitution, frame hash before and after, judge verdict, state,
   `levels_completed`.
6. **Closing:** the environment object is dropped after the episode, and no references
   are kept.
7. **Replay test:** one saved episode per condition is re-played in the test suite and
   must match the saved record exactly.

**Common judge (measurement).** All conditions' dead-move rates and distinct-state counts
are **measured with the same judge**, P1's masked judge, whichever judge a policy uses to
act. This prevents a treatment from grading itself.

**Split, seeds, budget.** Held-out 17 games, verdict 16 (`r11l` reported separately).
Seeds 100–119, new relative to E4's 0–19 and identical across conditions, so episodes are
paired. Primary budget 300 actions (resets excluded, as in E4); secondary 1,000 actions.

**Statistics.** Per seed, D = (treatment clears) − (control clears), summed over the 16
verdict games. One-sided exact sign test with ties dropped. **Supported** when p < 0.05
and total clears are higher **and** the concentration rule holds (§3). Per-game tables are
always reported beside aggregates.

**Implementation checks that separate scaffold failure from hypothesis failure.** Each
must pass before any held-out run:
- (a) unit tests on synthetic environments with known answers;
- (b) the control reproduces E4's saved episodes exactly (the existing replay tests);
- (c) a "switch acts only where on" check in the run verifier;
- (d) the safeguard assertions above.

If any check fails, the result is recorded as a **scaffold failure**, and no conclusion
is drawn about the hypothesis.

---

### Preregistration P1: masked state comparison inside random + prune

**Question.** Does pruning with a judge that ignores clock-like cells catch more truly
dead moves, and clear more verdict levels, than pruning with exact screen identity?

**Capability isolated.** Perception of change (state comparison). Exploration policy,
memory structure, action selection and candidate generation are unchanged.

**Conditions.**

| | Control C0 | Treatment T1 |
| :-- | :-- | :-- |
| Policy | E4 `RandomPrune`, byte-for-byte | E4 `RandomPrune`, but "same screen" is decided by the masked judge |
| Dead-move key | (exact frame hash, action[, colour clicked]) | (masked frame hash, action[, colour clicked]) |
| Information | current frame | current frame, plus the episode's own recent transitions (for the mask) |

**Masked judge (fully specified).**
- Per episode, keep a rolling window of the last **W = 16** transitions. For each cell
  (x, y) of the last frame layer, count the transitions in the window where the cell's
  colour changed.
- A cell is **masked** when it changed in **≥ 14 of the last 16** transitions **and**
  those transitions include **≥ 3 distinct action keys**. A cell that doesn't change for
  16 consecutive transitions is unmasked.
- Until 16 transitions exist, nothing is masked.
- **Masked hash** = blake2b of the last layer with masked cells set to −1, plus the set of
  masked coordinates (so a change in mask membership is never read as "unchanged").
- A transition is **dead** when its masked hashes before and after are equal, **and** the
  game state is not GAME_OVER, **and** `levels_completed` did not change.
- These parameters are **fixed a priori**. They are not tuned on tune or held-out games.
  Tune games are used only for the implementation checks below.

**Implementation checks (must pass before held-out).**
- **(i) Synthetic:** a counter cell that ticks every step while the world never changes.
  The judge must mark every move dead after step 16. And a world that changes only
  under ACTION1: ACTION1 must never be marked dead.
- **(ii) `dc22`, tune:** the known one-cell clock (flips every second action) is masked
  within 32 steps in each of 3 seeds.
- **(iii) `ls20`, tune:** the step-counter region is masked, and the number of distinct
  masked states per 100 actions is below the exact-hash count.
- **(iv) Safeguards and the replay test pass.** C0 reproduces E4's saved episodes.

**Metrics.**
- **Primary:** verdict level clears at 300 actions.
- **Secondary:**
  - clears at 1,000 actions;
  - dead-move rate by the common judge;
  - distinct masked states per 100 actions;
  - redraws;
  - mean masked cells per game (a mechanics-perception descriptor);
  - per-game clears;
  - RHAE (verdict and all 17);
  - `r11l` separately.

**Success.** p < 0.05 by the sign test at 300 actions, total clears higher, and the
concentration rule holds.

**Falsifier and stopping rule.**
- **Falsified:** otherwise. The exact-hash key remains the policy default. The masked
  judge is still adopted as the **measurement** judge if checks (i)–(iii) pass, because
  it is the better-validated measurement.
- **Stop:** the branch stops after one held-out run. No re-parameterisation of W or the
  threshold is allowed after seeing held-out results.
- **Void:** if checks (ii) or (iii) fail on tune, the run is voided and recorded as a
  scaffold failure of the judge.

**Cost.** Well under 1 CPU-hour (E4's 300-action run took 2–3 minutes per condition; the
masking overhead is **UNKNOWN**, estimated under 10×). 0 tokens. About 1 day to build the
safeguards, 0.5 day for the judge and its checks.

**Confounds.**
- **Clocks that change less often than 14 of 16 steps are not masked** (under-masking).
- **Real objects that move every step, e.g. an autonomous enemy, get masked**
  (over-masking), which could prune live moves. The per-game count of masked cells is
  reported so over-masking is visible.

**Interpretation.**
- **Positive:** measurement noise was hiding dead moves, and part of random + prune's
  ceiling was perceptual.
- **Negative:** clocks are not what limits pruning; the P1 judge still serves as the
  common measurement.
- **Mixed** (gains only at 1,000 actions, or only on clock games): reported per game; no
  general claim.

**Type.** Both. It builds the safeguards and the common judge (prerequisite
infrastructure) and tests a hypothesis.

---

### Preregistration P3: empirical action-success bandit

**Question.** Does learning within an episode which action *classes* tend to produce new
states, and preferring them, clear more levels than choosing uniformly among the same
classes?

**Capability isolated.** Learning + action selection (statistical, within episode, no
model). Pruning, the candidate set and memory structure are held constant.

**Arms (action classes).** At each step the arms are:
- each available keyboard action;
- plus, if clicks are available, one arm per colour present in the current frame. The
  click cell is drawn uniformly among cells of that colour.

This matches E4's click key (the colour clicked).

**Conditions.**

| | A: E4 random + prune | A′: uniform over arms + prune | B: UCB over arms + prune |
| :-- | :-- | :-- | :-- |
| Action choice | uniform action, uniform coordinate | uniform over live arms | UCB1 over live arms |
| Pruning | E4 rule | E4 rule, on the arm key | E4 rule, on the arm key |
| Judge used to act | P1 outcome (exact or masked, as P1 decided) | same | same |

**Primary comparison: B vs A′** (learning; the arm structure is held fixed).
**Secondary: A′ vs A** (the effect of the arm structure itself; reported, not a verdict).

**Reward and estimator (fully specified).**
- **Reward** = 1 when the transition's resulting state (judged hash) has **not been seen
  before in this episode**, else 0. GAME_OVER counts as 0. A level clear counts as 1.
- **Estimates are pooled per arm key across all states in the episode:** (action id) for
  keys, (ACTION6, colour) for clicks. This pooling is the capability: "ACTION3 tends to
  reveal new states".
- **UCB1:** score = mean + √(2 ln N / n), where N = total pulls this episode and n = the
  arm's pulls. An unpulled arm scores +∞, with ties broken by the episode rng.
- **Dead arms in the current state are excluded before scoring.** If every arm is dead,
  the choice is uniform over all arms, as in E4.
- **Estimates reset at the start of each episode** and are never carried across episodes
  or games.

**Implementation checks.**
- **(i) Synthetic:** a 3-arm environment where only arm 2 produces new states. B's pull
  share of arm 2 exceeds 0.8 after 100 steps, and A′ stays near 1/3.
- **(ii) Arm-key agreement:** the arm key and the pruning key agree on 100% of logged
  transitions.
- **(iii) Substitution accounting:** the logs separate the bandit's choice from redraws
  (if any).
- **(iv) Safeguards and replay** pass.

**Metrics.**
- **Primary:** verdict level clears at 300 actions (B vs A′).
- **Secondary:**
  - clears at 1,000 actions;
  - distinct judged states per 100;
  - dead-move rate (common judge);
  - the arm-pull distribution per game, as a mechanics-discovery descriptor (which
    action classes the agent learned are productive);
  - per-game clears;
  - RHAE.

**Success.** B beats A′: sign test p < 0.05, total clears higher, and the concentration
rule holds.

**Falsifier and stopping rule.** Otherwise falsified. No change of the UCB constant or the
reward after seeing held-out results. One held-out run.

**Cost.** CPU, about 1 h for 3 conditions × 2 budgets. 0 tokens. About 1 day to build.

**Confounds.**
- **Novelty reward can favour clocks** (every step is "new"). Mitigated only if P1's masked
  judge is used; with exact hashes this confound is expected, and is reported.
- **Colour arms merge different objects of the same colour.**
- **A′ vs A mixes arm structure with click distribution.** That's why it is secondary.

**Interpretation.**
- **Positive:** simple statistical learning fills part of the gap. Any learned ranker (P6)
  or model harness (P8) must beat B, not just random + prune.
- **Negative:** knowing which action classes are productive is not what limits these
  games.
- **Mixed:** reported per game.

**Type.** Scientific. It is the required non-model control for P6 and P8.

---

### Preregistration P4: transition-graph memory with return-to-frontier

**Question.** Does remembering observed transitions, and navigating back along known
paths to states with untried actions, clear more levels than the same local exploration
rule without navigation?

**Capability isolated.** Memory (a transition graph) + planning-to-explore (shortest known
path to the frontier). The local action-choice rule is held constant.

**Conditions.**

| | L: local systematic | G: local systematic + navigation |
| :-- | :-- | :-- |
| At a state with untried live arms | uniform over untried live arms | same |
| At a state with no untried live arms | uniform over live arms (E4-like) | **navigate**: follow the shortest known path to the nearest state with untried live arms |
| After GAME_OVER reset | continue with the local rule from the reset state | navigate from the reset state to the nearest frontier state |
| Memory | per-state tried-arm sets only | tried-arm sets **plus** a transition graph |

Both use P3's arms, pruning, and the P1-selected judge to act.

**Graph and navigation (fully specified).**
- **Nodes** = judged state hashes.
- **Edges** = (node, exact action including (x, y) for clicks) → observed next node.
- **The frontier** = nodes with at least one untried live arm.
- **Navigation:** BFS over edges from the current node to the nearest frontier node, with
  ties broken by the smallest node insertion order.
- **Executing a path:** each edge's exact action is taken. If the observed next node
  differs from the recorded one, the edge is marked **unreliable** (excluded from
  planning) and navigation replans from the current node.
- **Navigation actions count toward the action budget.**
- **Navigation stops** when the frontier node is reached, a level is cleared, or
  GAME_OVER occurs.
- **The graph resets each episode**, and when `levels_completed` increases (a new level
  starts a new graph).

**Implementation checks.**
- **(i) Synthetic:** a corridor maze of depth 30 where death returns to the start. G
  reaches depth 30 within 300 actions in ≥ 19/20 seeds, and L in fewer (this validates
  navigation, not the hypothesis).
- **(ii) Determinism probe on tune games:** the fraction of re-executed edges that
  reproduce their recorded next node (**navigation fidelity**). This is reported per
  game. Games below 0.8 fidelity are flagged "non-deterministic under this judge" and
  are reported separately in the verdict.
- **(iii) Budget accounting:** navigation actions and exploration actions are logged
  separately, and their sum equals the actions played.
- **(iv) Safeguards and replay** pass.

**Metrics.**
- **Primary:** verdict level clears at 300 actions (G vs L).
- **Secondary:**
  - clears at 1,000 actions (expected to matter more for navigation);
  - maximum BFS depth reached from the level's start node;
  - distinct judged states per 100;
  - navigation fidelity per game (a measure of discovered determinism);
  - fraction of actions spent navigating;
  - mean path length of successful navigations;
  - per-game clears;
  - RHAE.

**Plan-quality metric.** The fraction of navigations that reach their target frontier
node without replanning.

**Success.** G beats L: sign test p < 0.05 at 300 **or** 1,000 actions (both reported, with
a Holm correction over the two budgets), total clears higher, and the concentration rule
holds.

**Falsifier and stopping rule.** Otherwise falsified. If navigation fidelity is below 0.8
on more than half of the verdict games, the verdict is **"not testable with this
judge"** rather than falsified; that result feeds back to improve the judge. One held-out
run per budget.

**Cost.** CPU, 1–2 h (2 conditions × 2 budgets; graph bookkeeping overhead is
**UNKNOWN**). 0 tokens. About 2 days to build.

**Confounds.**
- **Non-deterministic games** (fidelity below 0.8).
- **Colour-arm clicks** re-executed with the exact recorded (x, y) are not the same arm
  distribution.
- **The graph explodes when the judge treats clocks as state** (again tied to P1's
  outcome).

**Interpretation.**
- **Positive:** persistent transition memory + planning-to-explore is a missing
  capability. It is the cheapest form of "world model" (known transitions, no rules), and
  any Duck-style world model must beat it.
- **Negative:** re-reaching deep states is not what limits the unsolved games within
  these budgets.
- **Mixed:** reported per game.

**Type.** Scientific. It also yields navigation fidelity, a mechanics measurement that
later experiments reuse.

---

## 5. Sequence and decision tree

```
P1 (judge + safeguards)
 ├─ checks fail ................ fix the judge; nothing downstream runs until they pass
 ├─ supported .................. masked judge = acting judge for P2–P4
 └─ falsified .................. exact hash stays the acting judge; masked judge = measurement only

P2 (object clicks)  ── independent of P3/P4; its winner becomes the click generator

P3 (bandit) ─┬─ supported ...... B becomes the statistical baseline for P6 and P8
             └─ falsified ...... A′ (uniform arms) is the baseline; P6 must beat A′

P4 (graph + navigation) ─┬─ supported ... G becomes the "best CPU policy" for P8
                         ├─ falsified ... navigation is not the gap; run P5 next
                         └─ untestable .. improve the judge before any world-model claim

P5 (oracle goal, tune only)
   ├─ oracle helps a lot ....... goal inference is a real gap; P8's goal hypotheses are scored
   └─ oracle does not help ..... prioritise manipulation/mechanics; deprioritise goal work

P6 (learned ranker ± Jev) — run only after P3; must beat P3's winner
P7 (image vs text)        — run when GPU time is available; independent of P1–P6
P8 (Duck)                 — Stage B runs only after the best CPU policy is fixed (after P4)
```

**Rules that trigger, modify or cancel later work.**

1. **Nothing runs before P1's implementation checks pass.** The replay bug showed that
   measurement failures masquerade as effects.
2. **Each later experiment's control is the best earlier policy,** not plain random. A
   complex component is credited only with gains over the simplest policy that preceded it.
3. **If P3 and P4 both fail and P5's oracle does not help,** the CPU branch stops. The
   remaining gap is interpretation or manipulation, and P7 and P8 become the priority.
4. **If P4 succeeds,** P8 must beat G, not random + prune. A Duck result that only
   matches G shows no value from reasoning at this budget.
5. **P6's Jev arm runs only if** API access is granted and the typed-output schema can
   express a ranking over a variable-length candidate list (A11). Otherwise the local
   ranker alone runs, and no claim about Jev is made.
6. **P7 negative plus P8 positive** means the gain comes from investigation or code, not
   from images. **P7 positive** means the next single variable is multi-action output
   (Reki-style), tested alone.
7. **Hybrid (the handoff's E7) becomes eligible only if all three hold:**
   - (a) a fast learned ranker (P6, or Jev) beats P3's winner on held-out;
   - (b) P8 beats the best CPU policy on held-out;
   - (c) the per-game winners are complementary: at least 3 verdict games where the
     ranker beats P8 and at least 3 where P8 beats the ranker, and an escalation signal
     preregistered on tune games predicts which component wins.

   Otherwise, no hybrid.

---

## 6. Recommended first experiment: P1

**P1 is the first experiment.** It offers the most information per unit of cost:

1. **It is a prerequisite for everything else.** Five of the handoff's mandatory
   safeguards don't exist in the code yet (§0, D1). Building them inside P1 means no
   later result can repeat the replay bug's false clears.
2. **It fixes the known measurement ceiling that confounds every later metric.** Dead-move
   rate, distinct states, P3's novelty reward and P4's graph all depend on what counts as
   "the same state". A clock that makes every screen look new would silently inflate P3's
   reward and explode P4's graph.
3. **It is the cheapest possible falsifiable test:** well under 1 CPU-hour, no tokens, no
   model, about 1.5 days of work, one variable (the judge), and a control that
   byte-reproduces E4.
4. **It is informative either way.** A positive result shows part of random + prune's
   ceiling was perceptual. A negative result still delivers a validated common judge, and
   removes "clocks" as an explanation for later nulls.

The runner-up is P4. It's the largest capability step still at CPU cost, but its graph is
meaningless until the judge question is settled.

---

## 7. Open assumptions

| # | Assumption | Status | Blocks |
| :-- | :-- | :-- | :-- |
| A1 | The ARC engine is deterministic for a given action sequence from a fresh environment. | **UNKNOWN — requires empirical verification** (P4 check ii measures it) | P4 |
| A2 | Clock-like cells change on most steps regardless of action, so a 14-of-16 rule catches them without masking real moving objects. | **INFERENCE** from `dc22` and `ls20`; **UNKNOWN** for the held-out games | P1, P3, P4 |
| A3 | `reset()` keeps level progress, so a fresh environment is needed per episode. | **VERIFIED** in-project (the replay bug) | all |
| A4 | The shortest real level clear exceeds 2 actions. | **VERIFIED** for observed clears (minimum 5); **UNKNOWN** for unobserved levels | P1 flag threshold |
| A5 | Connected components approximate game objects. | **UNKNOWN**; the ARC-AGI-3 engine's sprite model isn't documented to us | P2, P8 |
| A6 | vLLM 0.23.0 (our Kaggle wheel) serves Gemma-4 with image input. | **UNKNOWN — requires empirical verification** | P7 |
| A7 | Duck's reported 1.6002 is on the same scale as our RHAE, and Duck's Kaggle score is 1.03. | Scale **OPEN QUESTION**; 1.03 is an **unverified secondary report** | interpreting P8 |
| A8 | Duck's public code runs on one Kaggle RTX PRO 6000 with a verifiable Qwen 3.6 27B FP8 mirror. | **COMPANY CLAIM** (a Kaggle notebook reproduces a run); the mirror hash check is required by the register | P8 |
| A9 | Tufa's claim that hand-crafted tools hurt applies to our setting. | **COMPANY CLAIM**; relevant to E2 and E3, not verified here | P8 Stage C |
| A10 | Jev can be accessed, and can be adapted to ARC transitions without training. | **UNKNOWN**. The source documents API-only early access and structured text input; customisation is not documented | P6 Jev arm |
| A11 | Jev's typed outputs can express a ranking over a variable-length candidate list. | **UNKNOWN** | P6 Jev arm |
| A12 | Any Jev result is research-only: Kaggle scoring runs with internet disabled. | **VERIFIED** for Kaggle (competition rules in the handoff); whether an API model meets the rules' "reasonable cost" test is an **OPEN QUESTION** | submission use |
| A13 | Reusing the 17 held-out games across many experiments does not bias verdicts. | **OPEN QUESTION**. New seed blocks (100–119) reduce, but don't remove, adaptive reuse; hidden-set submissions (one per day, two decimals) remain the only fresh test | all |
| A14 | GPU quota is available for P7/P8 in the week they are scheduled. | **UNKNOWN**; check before each push | P7, P8 |
| A15 | Engine-internal state (e.g. sprite positions) is accessible for ground-truth mechanics labels. | **UNKNOWN**; if not, P5/P8 annotations are made by hand | P5, P8 |

---

### Sources

- ARC Prize, *ARC Prize 2026: ARC-AGI-3 Milestone Prize #1*: https://arcprize.org/blog/arc-prize-2026-milestone-1
- Tufa Labs, *Duck Harness: Winning Solution for ARC-AGI-3 Milestone 1*: https://tufalabs.ai/research/duck-harness/
- Tufa Labs, `duck-harness` repository and `ARC3-Inference/README.md`: https://github.com/Tufalabs/duck-harness
- TypeSafe AI, *Introducing System One Models & Jev*: https://typesafe.ai/blog/introducing-system-one-models-and-jev
- *ARC-AGI-3: A New Challenge for Frontier Agentic Intelligence* (arXiv 2603.24621): https://arxiv.org/abs/2603.24621
- AlphaSignal (secondary, unverified): https://alphasignal.ai/news/tufa-labs-wins-25k-beating-frontier-ai-on-the-world-s-hardest-benchmark
