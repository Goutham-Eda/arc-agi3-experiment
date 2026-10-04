# Knowledge record

Findings as they were logged, oldest first. Read top to bottom, this is the research in
order — including the entries later corrected. The replay-bug correction is the one to look
at: it moved the random floor and forced an earlier verdict to be restated against it. The
superseded entries are kept deliberately; see `../../references/split-and-verdicts.md` on
amendments.

## RHAE level index is 1-based

`KNOWLEDGE-fc4ad6fd` · 2026-09-11

EnvironmentScoreCalculator weights each level by its index; arc_agi's own caller passes level_index=level_idx+1. Passing 0-based indices silently zeroes the first level.

*Source:* .venv/Lib/site-packages/arc_agi/scorecard.py (arc-agi 0.9.8, caller at add_level level_idx + 1)

---

## Windows: use 127.0.0.1, never localhost

`KNOWLEDGE-96ee3880` · 2026-09-11

Against a server bound to IPv4, Windows tries localhost over IPv6 first and stalls ~2 s per request. Measured: two games 188.6 s via localhost, 6.5 s via 127.0.0.1.

*Source:* submission/rehearse.py; rehearsal runs 2026-09-11

---

## Random agent scores 0.07 on the hidden set

`KNOWLEDGE-f28a554b` · 2026-09-11

Build 1 (random over available_actions, 80 actions/game, CPU) scored public 0.07 on the 110-game hidden set. The random floor is not zero there.

*Source:* Kaggle submission 56171083, kernel goutham12/arc-agi-3-build-1-random v1

---

## Milestone 1 winners ran 27-31B local models

`KNOWLEDGE-4a8114fc` · 2026-09-11

1st Tufa Labs: Qwen 3.6 27B FP8, agent writes and runs code, context eviction; 'hand-crafted tools actually hurt'. 2nd Reki and 3rd forge: Gemma-4-31B as vision policy; Reki used dead-signature detection and reflection memory; forge's winning run disabled most extra machinery.

*Source:* https://arcprize.org/blog/arc-prize-2026-milestone-1

---

## Gemma 4 and Qwen 3.6 are Apache 2.0; Gemma 3 is not

`KNOWLEDGE-4153c098` · 2026-09-11

Publisher tags on Hugging Face: every google/gemma-4-* and Qwen/Qwen3.6-* repo is license:apache-2.0; google/gemma-3-* is license:gemma.

*Source:* huggingface.co/api/models?author=google&search=gemma-4 and ?author=Qwen&search=Qwen3.6, queried 12 Sept 2026

---

## Qwen 3.6 is on Kaggle only as community mirrors

`KNOWLEDGE-47c341f0` · 2026-09-11

qwen-lm on Kaggle hosts Qwen 3 and 3.5, not 3.6. Mirrors include michaelpoluektov/qwen3-6-27b-fp8 (30.9 GB). Verify hashes against Qwen/Qwen3.6-27B-FP8 before a verdict run.

*Source:* kaggle models list -s qwen3.6, 12 Sept 2026

---

## E0 smoke v1: Kaggle RTX run facts

`KNOWLEDGE-79b6c192` · 2026-09-11

GPU: NVIDIA RTX PRO 6000 Blackwell Server Edition, 97.9 GB, driver 580.159.04 (CUDA 13 ok). Offline installs: arc-agi 3 s, vLLM 0.23.0 178 s. Gemma-4-E4B load: 14.9 GiB over NFS in 188 s (~80 MB/s), 15.3 GiB GPU; torch.compile 31 s. Quota: 0.14 GPU-h for an ~8 min run, charged at wall-clock time.

*Source:* experiments/build/e0-smoke-output/e0_run.json, vllm.log; kaggle quota after run

---

## E0 smoke v2: pipeline works on Kaggle RTX

`KNOWLEDGE-1e4af147` · 2026-09-11

Gemma-4-E4B via vLLM 0.23.0 on RTX PRO 6000: arc install 2.7 s, vLLM install 104 s, load+compile to healthy 210 s, 40 actions in 29 s. Parse failures 0/40 (incl. ACTION6 on dc22). Median 862 ms/call (ls20), 691 ms (dc22). ~19k prompt tokens per call (4 history frames + current, ~4k tokens each); prefix caching gave ~20k tok/s prompt throughput. KV cache 2.71M tokens, 82x concurrency at 32k. Quota 0.09 GPU-h for ~7 min.

*Source:* experiments/build/e0-smoke-output-v2/e0_run.json, e0_report.json, vllm.log

---

## vLLM applies each model's generation_config sampling defaults

`KNOWLEDGE-176c3de5` · 2026-09-11

vLLM warned that default sampling parameters were overridden by the model's generation_config.json (Gemma-4-E4B: temperature 1.0, top_k 64, top_p ...). E0 sets only temperature, so top_k/top_p come from each model: a decoding difference between models the register did not fix.

*Source:* experiments/build/e0-smoke-output-v2/vllm.log line 74

---

## E0 random baseline at the verdict budget

`KNOWLEDGE-927373e7` · 2026-09-11

Random policy, 17 held-out games x 5 seeds x 80 actions (E0's exact budget): mean 0.04 levels cleared over the 16 verdict games, all from sp80 (level 1 in 3/5 seeds); r11l level 1 in 5/5 seeds, kept outside verdict aggregates as registered. Mean RHAE 0.1539, mean 78.7 distinct states per 100 actions (lp85 3.8 to lf52/tr87 100).

*Source:* experiments/e0_random_heldout_80.json via experiments/e0_analyze.py, 12 Sept 2026

---

## E0 small tier: Gemma-4-E4B scores below random

`KNOWLEDGE-972c7bbe` · 2026-09-11

17 held-out games x 5 seeds x 80 actions, identical decoding, RTX Pro 6000, 71 min (play 61.5 min, 9.3 s median per call under 17-way concurrency). Gemma-4-E4B: 0.00 levels over the 16 verdict games vs random 0.04; 67.5 distinct states/100 actions vs 78.7; RHAE 0.0000 vs 0.1539; above random on 0/16 games; lost sp80, which random clears in 3/5 seeds. Parse failures 0.0% among kept episodes (2 of 85 episodes excluded above the 20% threshold). Exploration collapsed on su15 (2.0 states/100 vs 61.5) and sb26 (17.5 vs 53.5).

*Source:* experiments/build/e0-out-gemma4-e4b/e0_report.json via experiments/e0_analyze.py; kernel goutham12/arc-agi-3-e0-gemma4-e4b v1

---

## E0 cost model: 20k tokens/call, prefix cache defeated by the sliding window

`KNOWLEDGE-98bbc916` · 2026-09-11

Gemma-4-E4B run: ~20k input tokens per call on most games (hex screen + 4 history frames; games with uniform screens tokenise shorter, e.g. cn04 4.6k, sp80 7.3k), ~7 output tokens. vLLM prefix cache hit rate only ~19% because HISTORY_TURNS slides: the oldest exchange drops each turn, so the stable prefix is little more than the system prompt. Prompt throughput ~23k tok/s shared across 17 concurrent games gives 9.3 s median per call (0.8 s single-stream). Implication: a 27-31B model at the same prompt size is likely 3-4 GPU-h per held-out run, not 1. An append-only context window (reset at a cap) would raise cache hits, but that is a behavioural change and would need a dated amendment.

*Source:* experiments/build/e0-out-gemma4-e4b/e0_report.json and vllm.log, 12 Sept 2026

---

## Gemma-4-E4B explored less than a constant-action policy

`KNOWLEDGE-7a4ace08` · 2026-09-12

Local control, no GPU: a policy that always plays the first available action (fixed cell for complex actions), 80 actions, seed 0, distinct screens per 100 actions -- su15 constant 40.0 vs random 68.8 vs Gemma 2.5; sb26 constant 80.0 vs random 57.5 vs Gemma 8.8; lp85 constant 1.3 vs random 2.5 vs Gemma 1.3. Simple repetition does NOT reproduce Gemma's collapse: on su15 and sb26 it explored far less than mindless repetition. On sb26 a constant action beats random, so those games reward persistence. The mechanism is still unknown; the queued diagnostic's action histogram is needed.

*Source:* local control run 12 Sept 2026 against experiments/build/e0-out-gemma4-e4b/e0_report.json and experiments/e0_random_heldout_80.json

---

## Neither repetition nor oscillation explains Gemma's collapse

`KNOWLEDGE-59e4fa00` · 2026-09-12

Local controls, no GPU, 80 actions, seed 0, distinct screens per 100 actions. Alternating the first two available actions: su15 80.0, sb26 100.0, lp85 1.3, ls20 100.0, dc22 100.0. Constant first action: su15 40.0, sb26 80.0, lp85 1.3, ls20 8.8, dc22 50.0. Random: su15 68.8, sb26 57.5, lp85 2.5. Gemma-4-E4B: su15 2.5, sb26 8.8, lp85 1.3. Both mechanical policies explore far MORE than Gemma, so its collapse is neither 'repeat one action' nor 'oscillate between two'. Remaining candidates, separable only by the action histogram: clicking a dead cell repeatedly, choosing an advertised-but-inert action, or the choice not reaching the game as intended. lp85 scores 1.3-2.5 for every policy and discriminates nothing.

*Source:* local control runs 12 Sept 2026; experiments/build/e0-out-gemma4-e4b/e0_report.json

---

## E0 diagnostic: Gemma fixates on dead click targets, not on one action

`KNOWLEDGE-e362f7ea` · 2026-09-12

Kernel arc-agi-3-e0-diag (Gemma-4-E4B, 80 actions, seed 0, tune games). ls20 (keyboard only): actions spread 38/14/13/15 across ACTION1-4, top-action share 0.475, 100.0 states/100 -- identical to random, no collapse. dc22 (has clicks): ACTION6 65 of 80 (share 0.81), 52.5 states/100 vs random 77.5; sample replies repeat the same cells ('ACTION6 0 0' twice, 'ACTION6 63 9' twice), i.e. corners and edges where nothing happens. So the failure is coordinate fixation on click games, not action repetition (refuted) or oscillation (refuted). It also emits coordinates for simple actions ('ACTION3 1 1'), which the parser ignores: the model is unclear which actions take a target. Timing: 1.5 s/call with 2 concurrent games vs 9.3 s with 17 -- concurrency, not model size, drove the earlier cost. Setup 250 s to vLLM ready, play 124 s for 160 calls.

*Source:* experiments/build/e0-out-diag/e0_report.json and e0_run.json, 12 Sept 2026

---

## E0: the whole Gemma deficit is in click games

`KNOWLEDGE-0a551423` · 2026-09-12

Held-out games split by whether ACTION6 is available at reset, comparing distinct states per 100 actions (seed 0, 80 actions): games with a click action, n=13, mean Gemma minus random -17.3; keyboard-only games, n=4, mean +0.3. Worst: su15 [6,7] -66.2, sb26 [5,6,7] -48.8, cn04 -25.0, ar25 -23.8, cd82 -22.5. Exceptions: lp85 [6] and vc33 [6] are click-only but show ~0 gap because those games barely respond to any policy (every control scores 1-2.5 on lp85). Mechanism from the diagnostic: repeated clicks on the same dead cells (corners/edges). Implication: the text encoding gives no usable basis for choosing WHERE to click; a fix belongs in how coordinates are offered, and would be a dated amendment to the registered scaffold.

*Source:* experiments/build/e0-out-gemma4-e4b/e0_report.json, experiments/e0_random_heldout_80.json, local availability probe 12 Sept 2026

---

## Labelled grid fixes the clicking; control inconclusive

`KNOWLEDGE-c09d2018` · 2026-09-12 · status: superseded

Kernel arc-agi-3-e0-diag2 (Gemma-4-E4B, 80 actions, 2 seeds, tune games). dc22 (click): 52.5 before -> 66.25 and 75.0 after, mean 70.6, against random 77.5 -- most of the gap closed. ACTION6 share fell from 65/80 (0.81) to 47/80 and 33/80; replies show scanning (ACTION6 0 0, 0 1, 0 2) and varied targets (61 12, 63 19, 20 20) instead of the same dead corner. ls20 (keyboard control): 88.75 and 100.0 after, against a single before-run of 100.0 -- one seed before and two after cannot separate a real cost from seed variance, so the control test is OPEN, not passed; the held-out re-run has 4 keyboard games x 5 seeds and settles it. Cost: 22.4k tokens/call, +9% over 20.5k; 1.8 s/call at 2 concurrent. The model still emits coordinates on simple actions (ACTION1 11 11), which the parser ignores.

*Source:* experiments/build/e0-out-diag2/e0_report.json; compared with experiments/build/e0-out-diag/e0_report.json

---

## Cross-domain origins pass: 16 sources, 3 challenges, 3 supports

`KNOWLEDGE-d47c8d48` · 2026-09-12

One sitting, 12 Sep 2026, run with the lit-review skill under a 15-20 source reviews-only stopping rule. 611 pooled, 16 shortlisted, 1 PDF obtainable (books and chapters have no open full text), extraction abstract-only. Verdicts 10 nothing / 3 supports / 3 challenges. Cluster A (theory-theory, program hierarchies, Heckerman's causal-vs-acausal split) supports H1 and H6 while reframing the unit as a competing program rather than a confidence-tagged assertion. Cluster C returned nothing: requisite variety never reached the corpus in review form. Cluster E's one usable source inverts the act-then-observe loop the whole register assumes. 14 of 15 seed pairs share zero references, so the four cluster questions have four unconnected origins.

*Source:* research_prep/notes/cluster_origins.md

---

## Labelled grid fails at scale: click gap unchanged

`KNOWLEDGE-fae8ed20` · 2026-09-12 · status: superseded

Held-out re-run (kernel arc-agi-3-e0-gemma4-e4b v2, 17 games x 5 seeds x 80 actions, 85 episodes, 0 excluded, play 78.8 min). Click games (13): v1 -13.5 vs random, v2 -13.1 -- a 0.4-point change, i.e. no fix. Keyboard games (4): v1 -1.1, v2 +2.1, so the control passes at five seeds. Levels/game 0.000 both versions vs random 0.037; 0/16 games above random. Per-game the labels swing both ways: su15 2.0 -> 56.0 (collapse repaired), ar25 69.5 -> 43.2 and m0r0 69.2 -> 49.2 (made worse). r11l level 1, cleared by v1 and by random in every seed, was cleared in none of v2. Parse failures 0.7% -> 0.0%. Conclusion: the two-game diagnostic (dc22 52.5 -> 70.6) did not generalise; coordinate labelling is not the cause of the click deficit. Next candidate: the 20k-token context whose sliding window defeats prefix caching.

*Source:* experiments/build/e0-out-gemma4-e4b-v2/e0_report.json vs experiments/build/e0-out-gemma4-e4b/e0_report.json and experiments/e0_random_heldout_80.json

---

## Qwen3-8B E0 held-out is a scaffold failure, not a model comparison

`KNOWLEDGE-697febf3` · 2026-09-12

Kernel arc-agi-3-e0-qwen3-8b, 17 held-out games x 5 seeds x 80 actions, labelled grid, identical decoding. 7 of 85 episodes excluded by the pre-registered 20% parse-failure rule, all on the keyboard-only games wa30 (5/5) and re86 (2/5): Qwen names ACTION6 on 35% of replies for games that do not offer it (Gemma 0%), so parse_action rejects them and a random legal action is substituted. wa30 has zero surviving episodes, so Qwen's aggregate covers 15 verdict games against Gemma's 16. Separately, 78/78 surviving episodes have a top-action share >= 0.95 and 14/16 games are identical across all five seeds (Gemma 4/17, random 2/17): the model collapses to one action for 80 turns. states/100 click 44.4 vs random 73.7; keyboard 73.3 vs 93.5. Falsifier unchanged: 0/15 games above the random floor on levels. Do not report this as 'Qwen plays worse'; Gemma-4-E4B is the small-tier baseline.

*Source:* experiments/build/e0-out-qwen3-8b/e0_report.json; research_prep/notes/experiment_register.md amendment 12 Sept 2026

---

## Gemma-4-31B scaffold probe passed: respects the available-action list

`KNOWLEDGE-ca77f06d` · 2026-09-13

Kernel arc-agi-3-e0-probe-gemma4-31b, 12 Sept 2026, tune games ls20 and tu93, 1 seed, 20 actions: 0/40 parse failures, never named ACTION5/ACTION6 (both games offer [1,2,3,4]), top-action share 0.35, 13.4 s median/call. Scaffold check only, not evidence of play quality. Runtime: vLLM ready at 600 s; KV cache 24.58 GiB = 84,388 tokens, 2.58x concurrency at 32k/request, ~4 concurrent at E0's ~20k prompts. Single held-out kernel (6,800 calls) projected ~6.5 h against the 9 h limit.

*Source:* experiments/build/e0-out-probe-gemma4-31b (e0_run.json, vllm.log); documents/session_handoff/2026-09-12_e0_small_tier.md s4

---

## E0 large tier: Gemma-4-31B is also below random; falsifier unchanged at three conditions

`KNOWLEDGE-caf80d52` · 2026-09-16 · status: superseded

Kernels arc-agi-3-e0-gemma4-31b-e012 and -e34, both status ok: 17 held-out games x 5 seeds x 80 actions, 85 episodes, 0 excluded, 6800 calls, 7 parse failures (0.1%) so the scaffold is clean and this is a model result. Verdict over 16 games: levels/game 0.000 vs random 0.037; states/100 73.2 vs 78.7; RHAE 0.0000 vs 0.1539; 0/16 games above random on levels. Click games (12) 66.1 vs random 73.7, so the E4B click deficit halves (-14.1 -> -7.6) but does not close; keyboard-only (4) 94.7 vs 93.5. Four games beat random on exploration (su15 +25.0, m0r0 +8.2, wa30 +4.8, cn04 +2.5) against sb26 -46.8 and sp80 -28.8. No level cleared anywhere; r11l level 1 cleared in 0/5 seeds where random clears 5/5. Size does not lift the frozen baseline above the floor.

*Source:* experiments/build/e0-out-gemma4-31b-e012 and -e34 e0_report.json via experiments/e0_analyze.py; register amendment 16 Sept 2026

---

## E0 31B runtime: 90 s per call at 17-way concurrency made the seed split necessary

`KNOWLEDGE-26754c54` · 2026-09-16

Median 90.1 s per LLM call (min 85.0, max 97.7) against the 12 Sept probe's 13.4 s: 6.7x slower because 17 game processes contend for a KV cache holding about four concurrent 20k-token requests. Play 5.95 h (e012, 51 episodes) and 3.98 h (e34, 34 episodes), ~420 s per episode; vLLM ready in 575 s and 460 s. A single 85-episode kernel would have needed ~9.9 h of play plus load, over Kaggle's 9 h limit, so the split was necessary rather than prudent and the ~6.5 h projection was optimistic by 50%. Budget any future 31B run at ~420 s per held-out episode. gpu-memory-utilization was 0.95.

*Source:* experiments/build/e0-out-gemma4-31b-{e012,e34}/e0_run.json and vllm.log

---

## top_action_share counts the action name, not the move; do not compare click-heavy conditions on it

`KNOWLEDGE-28a8a94c` · 2026-09-16

LLMBaseline.stats derives top_action_share from action_counts, which is keyed by action name only (src/agents/llm_baseline.py). For 31B, 25 of 85 episodes read >= 0.95 on bp35, lp85, r11l and sb26, meaning 'clicked nearly every turn', not 'repeated one move': r11l reads 1.00 while visiting 98.5 distinct states per 100 actions, so its coordinates varied. Qwen3-8B's collapse was genuine (ACTION6 15 15 eighty times, 1.2 states/100). Read the field alongside states/100, or count distinct (action, x, y) triples, before calling any condition degenerate.

*Source:* experiments/build/e0-out-gemma4-31b-{e012,e34}/e0_report.json action_counts; src/agents/llm_baseline.py stats()

---

## E1 tune probe: switches fire, scaffold clean, H6 starved of deaths, replay not exact under batching

`KNOWLEDGE-086194e3` · 2026-09-16

Kernel arc-agi-3-e1-probe-e4b, 16 Sept 2026, status ok: Gemma-4-E4B, dc22 sc25 tu93, 1 seed, 80 actions, 4 cells, 0 parse failures in 960 calls, play 415 s. --verify-output passes. Pruning: 60 dead moves, 32 substitutions (13.3%); states/100 sc25 50.0->68.8, dc22 65.0->56.3 (clock ceiling), tu93 never fires. Failure rules: 1 death in 12 episodes (tu93), so 1 rule; E4B dies less than random, so H6 may read null for lack of deaths - report deaths per cell. Identical prompts (dc22 off-off vs off-on) gave different action counts: vLLM is not bit-deterministic under changing batch composition despite per-call seeds, so the reused E0 off/off run is a draw, not a replay. Mechanism check only.

*Source:* experiments/build/e1-out-probe-e4b report_*.json and e0_run.json; register E1 amendment 16 Sept (probe)

---

## E1 held-out at E4B: WEAK, carried by --prune-visited alone; --failure-rules null

`KNOWLEDGE-3b132156` · 2026-09-17 · status: superseded

Kernel arc-agi-3-e1-heldout-e4b, 17 Sept 2026, status ok, 255 episodes, 0 excluded, 0 parse failures, play 2.42 h. Verdict games (16): levels/game random 0.037 (3 clears), off-off 0.000, on-off 0.013, off-on 0.000, on-on 0.013 (1 clear, lp85 seed 4, 48 actions). Pre-registered verdict WEAK: beats off/off, not random (needed >= 4 clears). Partially supported: pruning carries all of it, failure rules none, so H5 and H6 are not one experiment. The lp85 clear had 64% substitutions - largely random swaps, not model judgement. Pruning lifts states/100 68.6 -> 74.4 (random 78.7), passing random on sb26 (56.0 vs 53.5) and lp85 (15.0 vs 3.8). H6: 34 deaths, 34 rules, but the control repeats a death once in 85 episodes, so its target failure barely occurs at 80 actions; null is thin evidence for PRO-LONG. 31B tier not triggered (DECISION-e3978a7e). Next (human): N=10 permitted by register, or stop.

*Source:* experiments/build/e1-out-heldout-e4b report_*.json via e0_analyze.py; register E1 amendment 17 Sept (verdict)

---

## E2 abandoned at tune: the controllability probe raises dead-move rate at every k

`KNOWLEDGE-cfbeb805` · 2026-09-17

Kernel arc-agi-3-e2-tune-e4b, 17 Sept 2026, status ok, Gemma-4-E4B, 8 tune games x 3 seeds, cells probe/match x k 5,10,20, 144 episodes, no parse-failure exclusions. Pre-registered pick-k rule: no k separates -> E2 abandoned. Dead-move rate probe vs match: k5 0.344 vs 0.284 (match range 0.016), k10 0.321 vs 0.303 (0.042), k20 0.333 vs 0.293 (0.036) - the probe makes the model waste more of its own moves. No level cleared. Two-directional by game: sk48 dead 0.5 -> 0.9+, states 45 -> 11; s5i5 states 55 -> 98, tn36 65 -> 90 (k10,20), sc25 dead rate lower and states 40 -> 65 (k10,20). Affordance instrument empty (no re-probe, no level cleared). Null does not distinguish bad probe (step-counter blur, cycling repeats) from H3 mis-specified; Gibson/Tycho threat unrefuted. ~2.7 GPU-h.

*Source:* experiments/build/e2-out-tune-e4b report_*.json via e0_analyze.py --pick-k; register E2 amendment 17 Sept (abandoned)

---

## Replay bug: episodes after a level clear started past level 1; random floor at 80 actions is 0.0125, not 0.037

`KNOWLEDGE-ae516ae2` · 2026-09-17

Found 17 Sept 2026. e0_random_smoke.py played all episodes of a game on one environment; env.reset() keeps level progress, so every episode after a clear started past level 1 and counted its first action as a clear. Fixed: one environment per episode, regression test test_each_episode_starts_at_level_one. Affected only episodes after a clear in the same game/process: random baselines and E4B v1 r11l. Unaffected: E0 v2, 31B, Qwen3-8B, E1 and E2 model runs (no clear before the last episode). Corrected random floor, 16 verdict games, 80 actions, seeds 0-4: levels/game 0.0125 (1 clear, sp80 seed 2), RHAE 0.0348, states/100 78.5 (was 0.037, 0.1539, 78.7). Random clears r11l level 1 in 1/5 seeds, not 5/5. E1 verdict unchanged (weak): on/on 1 clear ties random instead of trailing; the bar was >= 2 clears, not >= 4.

*Source:* experiments/e4_random_80.json seeds 0-4 (fixed code); register E0 and E1 corrections 17 Sept

---

## E1 verdict restated against the corrected random floor: still weak

`KNOWLEDGE-8413b47a` · 2026-09-17

E1 held-out at E4B (17 Sept): on/on 1 level clear (lp85 seed 4, 64% substituted) vs off/off 0 and corrected random 1 clear (0.0125 levels/game, not 0.037). Pre-registered verdict WEAK stands: beats off/off, ties rather than beats random (needed >= 2 clears, not >= 4). Carried by --prune-visited alone; --failure-rules null (control repeats a death once in 85 episodes). Pruning lifts states/100 68.6 -> 74.4. The r11l 'random 5/5' contrast is withdrawn (random 1/5).

*Source:* register E1 verdict amendment and E1 correction 17 Sept

---

## E4 supported at 300 actions: random-prune doubles verdict clears (38 vs 19), carried by lp85

`KNOWLEDGE-1ad719a0` · 2026-09-17

17 Sept 2026, local CPU, fixed replay code, 17 held-out games x 20 seeds. 300 actions (primary): random 19 verdict clears, random-prune 38; sign test 18 wins, 0 losses, 2 ties, p < 0.0001: SUPPORTED. 80 actions: 6 vs 12, 6/0/14, p = 0.016. One game carries it: lp85 level 1 cleared in 20/20 seeds vs 1/20; sp80, r11l, vc33 identical episodes; cd82 one each. RHAE verdict 0.0735 -> 0.0824, all 17 0.0916 -> 0.1000 - small, because lp85 clears take 38-288 actions vs human 17. First run was contaminated by the replay bug (1-action clears) and was discarded and re-run before the verdict. Submission change is a separate task.

*Source:* experiments/e4_{random,prune}_{80,300}.json via e0_analyze.py --e4-verdict; register E4 verdict amendment 17 Sept

---

## E0 large tier (restated after the replay-bug correction): Gemma-4-31B not above random

`KNOWLEDGE-6c660d7f` · 2026-09-17

Kernels arc-agi-3-e0-gemma4-31b-e012 and -e34, 85 episodes, 0 excluded, 7 parse failures (0.1%): a model result. 16 verdict games: levels/game 0.000 vs corrected random 0.0125 (1 clear, not 0.037); states/100 73.2 vs 78.5; RHAE 0.0000 vs 0.0348. Click-game exploration deficit halves vs E4B (66.1 vs random 73.7; E4B 59.6); keyboard-only 94.7 vs 93.5. The model runs are unaffected by the replay bug (no clears). The r11l contrast 'random 5/5, models 0/5' is withdrawn: random clears r11l level 1 in 1/5 seeds.

*Source:* register E0 16 Sept amendment and 17 Sept correction; KNOWLEDGE-ae516ae2

---

## Labelled grid fails at scale: click gap unchanged (r11l note corrected)

`KNOWLEDGE-0d7aa9c5` · 2026-09-17

Held-out re-run (arc-agi-3-e0-gemma4-e4b v2, 17 games x 5 seeds x 80 actions, 85 episodes, 0 excluded, play 78.8 min). Click games (13): v1 -13.5 vs random, v2 -13.1 - no fix. Keyboard games (4): v1 -1.1, v2 +2.1, control passes at five seeds. Labels help where the model was stuck (su15 2.0 -> 56.0) and hurt where it coped (ar25 69.5 -> 43.2, m0r0 69.2 -> 49.2). Correction 17 Sept: the r11l 'loss' (v1 and random clear level 1 in every seed, v2 in none) was mostly the replay bug - v1 has one real clear (seed 0), random 1/5.

*Source:* experiments/build/e0-out-gemma4-e4b-v2 vs e0-out-gemma4-e4b; register E0 correction 17 Sept

---

## Build 3 scored 0.07 on the hidden set, same as Build 1

`KNOWLEDGE-aafd5a6f` · 2026-09-17

Submission 56309101, 17 Sept 2026, kernel goutham12/arc-agi-3-build-3-random-prune v1 (random + dead-move pruning, MAX_ACTIONS 300): public score 0.07, identical to Build 1 (56171083, random, 80 actions). Kaggle reports two decimals, so changes below 0.01 are invisible. Neither the 300-action cap nor pruning moved the hidden-set score at that resolution; E4's public-set gain (mostly one game, lp85) is not shown to generalise. A second submission (plain random at 300) would not be informative and is not recommended.

*Source:* kaggle competitions submissions arc-prize-2026-arc-agi-3; register E4 section, Build 3 hidden-set amendment

---

## E3 stopped at tune: LEARN/WIN labels raise dead moves, and 67% of replies ignore the label

`KNOWLEDGE-cca50afa` · 2026-09-18

Kernel arc-agi-3-e3-tune-e4b v2, 19 Sept 2026, status ok, Gemma-4-E4B, 8 tune games x 3 seeds, labels-on vs labels-off, 48 episodes (1 labels-on episode excluded at >20% parse failures). Pre-registered tune rule: STOP. Dead-move rate labels-on 0.342 (0.427/0.284/0.316) vs labels-off 0.295 (0.308/0.255/0.322); needed to be lower by > 0.067, is 0.047 higher. states/100 59.0 vs 61.7; no level cleared. Uptake: of 1,920 replies 385 LEARN (20%), 255 WIN (13%), 1,280 unlabelled (67%) - weak test, the model mostly ignores the instruction. sk48 again carries the loss (dead 0.42 -> 0.70, states 55 -> 26), as in E2. v1 kernel played nothing (agents.random_prune not shipped); fixed with an import check in e0_kernel.py --check. No held-out run. Next: compare against Tufa Labs' Duck Harness (Milestone 1 winner).

*Source:* experiments/build/e3-out-tune-e4b report_*.json via e0_analyze.py --e3-tune; register E3 amendment 19 Sept (stopped)

---

## E5 void at checks (ii)/(iii): dc22 and ls20 'clocks' are progress bars, not ticking cells

`KNOWLEDGE-cbfb0bb8` · 2026-09-24

24 Sept 2026, local CPU, tune games, random-prune-masked, episodes 0-2, 300 actions. The masked judge (W=16, >=14/16 changes, >=3 action keys, per cell) masked no cell in any episode: dc22 check (ii) fails, ls20 check (iii) fails (masked states/100 = exact: 97.0/96.0/93.0). Traced cell by cell: dc22 colours the next cell of row 63 every second action (no bottom cell changes more than 3 times in 300 steps); ls20 advances a two-row bar on rows 61-62 one column per action (bottom change on 293/300 steps, no cell more than 11 times). Per-cell frequency masking cannot catch a bar at any W or threshold. Design assumption A2 is false for both games. By the pre-registered rule E5 is void (scaffold failure of the judge, no claim about the hypothesis); no held-out game played. Safeguards kept; the masked judge is not adopted for measurement. A revised judge needs a new human decision and pre-registration.

*Source:* research_prep/notes/experiment_register.md E5 amendment 24 Sept; scratch check script (masked_judge recording subclass)

---

## E5 revised judge on tune: bar rule catches every bar, cell rule falsely masks dc22's player once

`KNOWLEDGE-99345a00` · 2026-09-24

24 Sept 2026, local CPU, tune games x episodes 0-2 x 300 actions, random-prune-masked. Checks (i)-(iii) pass: dc22 row 63 masked at step 16 in all seeds; ls20 rows 61-62 masked, masked states 112/124/109 vs exact 289/294/294. Check (vi) over-masking fails once: dc22 episode 2 step 165, the original cell rule masked 4 player cells (40-41, 10-11) after the player moved back and forth over them for 14 of 16 transitions under 3 keys. The bar rule masked only the hand-listed bars (dc22 r63, ls20 r61-62, s5i5 r63, tn36 r1, tu93 r63, sc25 c62-63). The cell rule masked no clock on any tune game. No held-out run; next step is a human decision.

*Source:* research_prep/notes/experiment_register.md E5 amendment 'revised-judge checks' 24 Sept; scratch run e5tune.json + trajectories

---

## E5 bar-only judge passes every implementation check on tune

`KNOWLEDGE-c8c930f2` · 2026-09-24

24 Sept 2026, local CPU, 8 tune games x episodes 0-2 x 300 actions. Bar-only judge (row/column, every/even/odd schedule in >= 14 of 16 transitions, >= 3 action keys, no cell changed twice). (i) synthetic pass; (ii) dc22 row 63 masked at step 16 in all seeds; (iii) ls20 rows 61-62 masked, masked states 112/124/109 vs exact 289/294/294; (iv) E4 replays exact, T1 = C0 while unmasked; (v) C0 acting verdict = exact-hash equality on 7200/7200 steps; (vi) only the hand-listed bars ever masked (dc22 r63, ls20 r61-62, s5i5 r63, tn36 r1, tu93 r63, sc25 c62-63). Safeguards pass. sc25 timer under-masked as predicted. Held-out run and --e5-verdict analysis not yet built or run.

*Source:* research_prep/notes/experiment_register.md E5 amendment 'bar-only checks' 24 Sept; scratch runs e5tune.json, c0tune.json

---

## E5 verdict: narrow, carried by vc33 (masked bar judge 57 vs 37 verdict clears at 300)

`KNOWLEDGE-5f812c8e` · 2026-09-24

24 Sept 2026, local CPU, 17 held-out games x episodes 100-119. T1 (random-prune with the bar-only masked judge) vs C0 (E4 random-prune, exact hash). 300 actions (primary): verdict clears 57 vs 37, sign test 18 wins 0 losses 2 ties, p < 0.0001, but the concentration rule fails: all gain is vc33 (0 -> 20; without it 37 vs 37, p = 0.69; one game improved). Verdict NARROW: carried by vc33. 1000 actions: 74 vs 55, also narrow on vc33 (2 -> 22). vc33 is click-only with a row-0 bar changing every click, so exact identity never finds a dead move; masking row 0 let pruning learn 1903 dead clicks. Likely over-masking on bp35 at 1000 (16 alternating columns), no clears either way. Safeguards passed; replay test exact. Consequences: exact hash stays the acting default; the bar-only masked judge is adopted as the common measurement judge; E5 stops.

*Source:* research_prep/notes/experiment_register.md E5 verdict amendment 24 Sept; experiments/e5_{prune,masked}_{300,1000}.json via e0_analyze.py --e5-verdict

---

## E6 falsified: return-to-frontier navigation adds little (Holm p 0.27 / 0.09)

`KNOWLEDGE-23097345` · 2026-09-27

27 Sept 2026, local CPU, 17 held-out games x episodes 100-119. G (graph + BFS navigation) vs L (local systematic, design-P3 colour arms, bar-only masked judge). Verdict clears 61 vs 57 at 300 (p = 0.274), 90 vs 80 at 1000 (raw p = 0.046, Holm 0.092): FALSIFIED; the 1000 gain is concentrated on lf52 (3 -> 9). G navigated only 4-6% of actions, mean path 1.5-1.8: within these budgets the local rule rarely exhausts untried arms. Fidelity < 0.8 on cd82, m0r0, wa30 (and r11l) only, so testable. Secondary: L beats E5's C0 (57 vs 37, 80 vs 55, p <= 0.0001) but carried by vc33 (+21/+24); G not credited as best CPU policy. Next on the CPU branch per design section 5: P5 (oracle goal, tune only); P3 still unrun.

*Source:* research_prep/notes/experiment_register.md E6 verdict amendment 27 Sept; experiments/e6_{local,nav}_{300,1000}.json via e0_analyze.py --e6-verdict

---

## E7 bandit: narrow at 300 (lf52), broad at 1000 (not decisive) - strongest signal so far

`KNOWLEDGE-af0d409b` · 2026-09-29

1 Oct 2026, local CPU, 17 held-out games x episodes 100-119. B (UCB1 over design-P3 arms, within-episode novelty reward, masked judge) vs A' (uniform over the same live arms). 300 actions (primary): 71 vs 60, sign test 12-3-5, p = 0.018, but carried by lf52 (0 -> 14; without it 57 vs 60): NARROW. 1000 actions (pre-registered as reported, not decisive): 117 vs 82, 15-2-3, p = 0.0012, and survives removing lp85 (77 vs 59, p = 0.038), six games improve (ar25, bp35, lf52, lp85, m0r0, vc33); cd82 and sp80 lose. First result in the register to survive the concentration rule, but not a verdict. B halves dead-move rate (0.30 -> 0.14-0.18), RHAE verdict 0.084 -> 0.132 at 300. B not adopted as baseline; a confirmatory pre-registration with 1000 as primary on fresh episodes (e.g. 120-139) is the recommended human decision.

*Source:* research_prep/notes/experiment_register.md E7 verdict amendment 1 Oct; experiments/e7_{uniform,ucb}_{300,1000}.json via e0_analyze.py --e7-verdict

---

## E8 confirmatory bandit: narrow (lf52) at 1000; size replicates (114 vs 79), breadth test fails

`KNOWLEDGE-173fdde8` · 2026-09-30

1 Oct 2026, local CPU, 17 held-out games x fresh episodes 120-139, E7's A' and B unchanged. 1000 actions (primary): B 114 vs A' 79, sign test 14-3-3, p = 0.0064, but without lf52 (0 -> 15) 99 vs 79, p = 0.105: NARROW. Seven games improve (ar25 0->10, cn04, ka59, lf52, lp85 23->35, m0r0, vc33); cd82 (8->4) and sp80 (21->8) lose, the same two as E7. 300 actions: p = 0.090, falsified. E7+E8: size and per-game direction replicate, the concentration rule passes once (E7) and fails once (E8). B not adopted as baseline; further bandit tests need a new pre-registration (e.g. more seeds, or a fix for the cd82/sp80 losses tested on tune).

*Source:* research_prep/notes/experiment_register.md E8 verdict amendment 1 Oct; experiments/e8_{uniform,ucb}_{300,1000}.json via e0_analyze.py --e8-verdict

---

## E9 supported: the UCB1 arm bandit beats uniform arms at 1000 actions on 40 fresh seeds (217 vs 171)

`KNOWLEDGE-2d3b2359` · 2026-09-30

1 Oct 2026, local CPU, 17 held-out games x 40 fresh episodes 140-179, E7's A' and B unchanged. B 217 vs A' 171 verdict clears; sign test 22-4-14, p = 0.0003; without lf52 (2 -> 25) 192 vs 169, p = 0.044; seven games improve (ar25 1->17, bp35, cn04, lf52, lp85 41->63, m0r0 1->18, vc33): SUPPORTED. Caveats: third test of the bandit (E7 narrow, E8 narrow, E9 supported); concentration leg borderline; cd82 and sp80 lose in all three runs (E9 22->9, 41->21), plus ka59 and tr87 small losses in E9; same 17 held-out games. Dead-move rate 0.30 -> 0.14 in all three. Consequence per design section 5: B is the statistical baseline that P6/P8 must beat, and the best CPU policy so far. Submission use and the cd82/sp80 losses are separate tasks.

*Source:* research_prep/notes/experiment_register.md E9 verdict amendment 1 Oct; experiments/e9_{uniform,ucb}_1000.json via e0_analyze.py --e9-verdict

---

## Build 4 scored 0.15 on the hidden set (Builds 1 and 3: 0.07)

`KNOWLEDGE-611f3b13` · 2026-09-30

Submission 56700446, 30 Sept 2026, kernel goutham12/arc-agi-3-build-4-arm-bandit v1 (E9's UCB1 arm bandit with the bar-only masked judge, MAX_ACTIONS 1000): public score 0.15, up from 0.07 for Build 1 (56171083, random, 80 actions) and Build 3 (56309101, random + prune, 300). First hidden-set gain in the project. It cannot be split between the policy and the 300 -> 1000 cap without a second submission (e.g. uniform arms A' at 1000); on public games at a fixed 1000 budget the bandit beat A' 217 vs 171 (E9).

*Source:* kaggle competitions submissions arc-prize-2026-arc-agi-3; register Build 4 hidden-set amendment

---

## Bandit losses diagnosed: death loops on sp80, ACTION5 fixation on cd82

`KNOWLEDGE-db18c6da` · 2026-09-30

30 Sept 2026, analysis of E9's saved held-out trajectories only. On both cd82 and sp80 every level clear (A' and B) is made with ACTION5, a commit-like move that on sp80 also most often ends the game. sp80: the bandit dies in loops - a move that ended the game is never marked dead and the reset returns to the same screen, where near-deterministic UCB picks ACTION5 again; 38% of B's ACTION5 deaths repeat a screen already died on (up to 18 from one screen) vs 3% for A'; B's losing episodes average 24.7 ACTION5 deaths vs 9.2 for A'. cd82: no death loops; B fixates on ACTION5 (new-screen rate 0.90-0.96, the highest arm), ~20% of pulls vs 9% for A', under-sampling other moves. Candidate fixes, untested: per-screen memory of moves that ended the game (sp80); some uniform coverage, e.g. epsilon mixing (cd82). Games were inspected, so a fix needs fresh episodes and the caveat.

*Source:* research_prep/notes/experiment_register.md diagnosis 30 Sept; experiments/build/e9/traj-{uniform,ucb}

---

## E10 narrow (sp80), as predicted: death memory ends the bandit's death loops

`KNOWLEDGE-1e3e4421` · 2026-09-30

30 Sept 2026, local CPU, 17 held-out games x fresh episodes 180-219 x 1000 actions. B' (E9 bandit + per-screen exclusion of moves that ended the game) vs B: 245 vs 227 verdict clears, sign test 20-8-12, p = 0.018; without sp80 (18 -> 30) 215 vs 209, p = 0.119: NARROW, the pre-stated expected outcome. sp80 repeat deaths 403 -> 2, ACTION5 pulls 4745 -> 3330; cd82 identical in both conditions (no death loops; its loss is the separate ACTION5 fixation). Repeat deaths overall 534 -> 34. B stays the statistical baseline; death memory is a submission candidate needing a separate hidden-set test. First run killed at ~58% by low memory; rerun as two processes.

*Source:* research_prep/notes/experiment_register.md E10 verdict amendment 30 Sept; experiments/e10_{ucb,safe}_1000.json via e0_analyze.py --e10-verdict

---

## cd82 diagnosed: period-3 progress bar is never masked; novelty is mostly counter noise and cannot credit set-up clicks

`KNOWLEDGE-a0c6db37` · 2026-09-30

30 Sept 2026, deterministic instrumented replays of saved E10 cd82 episodes 180-184 (both conditions, replays match). cd82's row-63 bar ticks on a period-3 schedule (tick, tick, pause; ticks on 0.64 of moves); the bar rule accepts periods 1 and 2 only, so it is never masked. Per-move new-screen rates 0.59-0.78 as judged fall to 0.02-0.26 with row 63 ignored; 47% of the bandit's ACTION5 presses change only the bar. With the bar ignored clicks almost never produce new screens, yet A''s clears usually follow clicks, so masking alone is not expected to fix cd82: novelty cannot credit low-change set-up moves. Candidate fixes (untested): period-3 bar rule (judge change, needs over-masking checks), epsilon-uniform mixing, or accept as a limit of novelty-driven exploration.

*Source:* research_prep/notes/experiment_register.md cd82 diagnosis 30 Sept

---

## E11 falsified: object clicks inside the bandit raise totals and RHAE but not the per-seed test

`KNOWLEDGE-aac86241` · 2026-10-01

1 Oct 2026, local CPU, 17 held-out games x fresh episodes 220-259 x 1000 actions. B_obj (colour arms click one 4-connected component of the colour at its centroid-nearest cell) vs B: 230 vs 209 verdict clears, sign test 18-13-9, p = 0.237: FALSIFIED. Six games improve (lf52, lp85, sp80, cd82, ka59, m0r0); vc33 and ar25 lose. Without lp85, 159 vs 151, p = 0.286. RHAE favours B_obj (verdict 0.119 -> 0.149; all 17 0.221 -> 0.325), suggesting faster clears where it clears; not a verdict. Two run attempts were killed by whole-machine memory pressure; a probe showed no runner leak (flat ~300 MB over 40 episodes). Completed one process at a time, B_obj in four resumable chunks; replay of the merged file is exact.

*Source:* research_prep/notes/experiment_register.md E11 verdict amendment 1 Oct; experiments/e11_{ucb,obj}_1000.json via e0_analyze.py --e11-verdict

---

## Build 5 scored 0.12: the hidden-set gain splits between the setup (+0.05) and the bandit (+0.03)

`KNOWLEDGE-5a58316c` · 2026-10-01

Submission 56745474, 1 Oct 2026: Build 5 (uniform over live design-P3 arms, bar-only masked judge, 1000 actions; Build 4 with UCB off) scored 0.12 on the hidden set, against Build 4 (the UCB bandit) 0.15 and Build 3 (random + prune, 300 actions) 0.07. By the reading fixed before the result, 0.12 is in the 'both contribute' band: about +0.05 from the arms, judge and 300 -> 1000 cap together, about +0.03 from the bandit at a fixed budget. The bandit's own hidden-set gain (0.12 -> 0.15) matches E9's public result in direction, so it transfers to unseen games. One submission each, two decimals: approximate.

*Source:* kaggle competitions submissions arc-prize-2026-arc-agi-3; register Build 5 hidden-set amendment

---

## Build 6 built and rehearsed: the bandit plus E10 death memory, not pushed

`KNOWLEDGE-7bb7fa93` · 2026-10-01 · status: superseded

1 Oct 2026, Genesis T-B6. submission/my_agent.py gains DEATH_MEMORY = True beside Build 5's UCB switch and a per-screen _deadly set; a fatal move is recorded against the masked screen it was made from in both conditions, and the exclusion runs after the dead-arm filter and before the all-arms fallback, in ArmBandit's order. Gates: 109 tests pass (equivalence is now 3 builds x 4 games against ArmBandit; Build 6 vs ucb+death_memory, Build 4 vs ucb, Build 5 vs uniform), rehearsal PASS at 27 ms/action, about 40 min projected for 110 games. Two findings worth carrying: (1) on sp80 at rng seed 7 the bandit never dies twice on one screen, so death memory is inert and the Build 6 equivalence case is vacuous - a pre-added assertion caught this; sp80 is pinned to seed 0 (13 repeat deaths -> 0, 291 exclusions), and across probe seeds 0-7 B' cleared 3 episodes to B's 1. (2) The gate rehearsal games (lp85, ls20, r11l) score identically to Build 4 because the rule never fires there; a two-way sp80 rehearsal confirmed it fires live but went the other way on that one episode (switch off 0.9144, 1 level, 23 resets; on 0.0000, 0 levels, 37 resets) - one seed against E10's 40, recorded because it was seen before the submission decision. Reading fixed in advance (DECISION-09885665): s >= 0.16 transfers, 0.14-0.15 adds nothing visible, s <= 0.13 costs more than it saves, with the click-colour exclusion as the first confound. Kernel arc-agi-3-build-6-death-memory built locally, NOT pushed and NOT submitted; independent-review gate pending a human.

*Source:* research_prep/notes/experiment_register.md Build 6 section; .genesis evidence T-B6 tests and rehearse

---

## Build 6 built, rehearsed and pushed as version 1; awaiting its run, then a human submission

`KNOWLEDGE-912d98e0` · 2026-10-01 · status: superseded

1 Oct 2026, Genesis T-B6. submission/my_agent.py gains DEATH_MEMORY = True beside Build 5's UCB switch and a per-screen _deadly set; a fatal move is recorded against the masked screen it was made from in both conditions, and the exclusion runs after the dead-arm filter and before the all-arms fallback, in ArmBandit's order, so the fallback can still return a fatal arm once every other arm is dead. Gates: 109 tests pass (equivalence is now 3 builds x 4 games against ArmBandit; Build 6 vs ucb+death_memory, Build 4 vs ucb, Build 5 vs uniform), rehearsal PASS at 27 ms/action, about 40 min projected for 110 games. independent-review was still pending when the human asked for the push. Two findings worth carrying: (1) on sp80 at rng seed 7 the bandit never dies twice on one screen, so death memory is inert and the Build 6 equivalence case is vacuous - a pre-added assertion caught this; sp80 is pinned to seed 0 (13 repeat deaths -> 0, 291 exclusions), and across probe seeds 0-7 B' cleared 3 episodes to B's 1. (2) The gate rehearsal games (lp85, ls20, r11l) score identically to Build 4 because the rule never fires there; a two-way sp80 rehearsal confirmed it fires live but went the other way on that one episode (switch off 0.9144, 1 level, 23 resets; on 0.0000, 0 levels, 37 resets) - one seed against E10's 40, recorded because it was seen before the submission decision. Reading fixed in advance (DECISION-09885665): s >= 0.16 transfers, 0.14-0.15 adds nothing visible, s <= 0.13 costs more than it saves, with the click-colour exclusion as the first confound. Kernel goutham12/arc-agi-3-build-6-death-memory PUSHED 1 Oct 2026 as version 1 (private, CPU) at the human's request; status RUNNING just after the push. NOT submitted: the human submits from the Kaggle website once the ordinary run writes submission.parquet, as for Builds 4 and 5.

*Source:* research_prep/notes/experiment_register.md Build 6 section; .genesis evidence T-B6 tests and rehearse; kaggle kernels push/status

---

## Build 6 scored 0.15: E10's death memory adds nothing visible on the hidden set

`KNOWLEDGE-e20155ae` · 2026-10-04

Submission 56805419, 3 Oct 2026 19:31 UTC, public score 0.15, from kernel arc-agi-3-build-6-death-memory v1 (source confirmed by the human against the competition submissions page; the Kaggle CLI does not expose a submission source kernel and no description was typed). Build 6 is Build 4 plus one rule: a move that ended the game is excluded on the screen it was made from. By the reading fixed before the push (>= 0.16 transfers, 0.14-0.15 adds nothing visible, <= 0.13 costs more than it saves, <= 0.01 is no difference), 0.15 equals Build 4 exactly, so the death memory adds nothing visible on 110 unseen games. Ladder: Build 3 random+prune 300 = 0.07; Build 5 arms+masked judge+uniform at 1000 = 0.12; Build 4 with UCB = 0.15; Build 6 plus death memory = 0.15. So +0.05 is arms/judge/budget, +0.03 is the bandit, +0.00 is the death memory. This is the cleanest comparison the project has made: exactly one rule changed, unlike Build 4 vs Build 3 which bundled three. It is not an implementation failure - E10 measured repeat deaths 534 -> 34 overall, sp80 403 -> 2 and sp80 clears 18 -> 30 - so the finding is about generality: death loops do not limit play across the hidden set at 1000 actions, and E10's narrow verdict carried entirely by sp80 is confirmed on unseen games. Claim is nothing

*Source:* kaggle competitions submissions arc-prize-2026-arc-agi-3; register Build 6 hidden-set amendment 4 Oct

---
