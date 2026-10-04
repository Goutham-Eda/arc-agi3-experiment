# Decision record

Every decision Genesis recorded on this project, oldest first. These were not written for
publication — they are the working record, captured at the moment each call was made, which
is the only time a decision record is worth anything. The ids are referenced throughout
`../experiment-register.md`.

## Pin arc-agi 0.9.8 and arcengine 0.9.3

`DECISION-5185896c` · 2026-09-11 · status: accepted

Match the versions in the competition's offline wheels so local behaviour equals the grader's. PyPI ships 0.9.9.

*Source:* documents/arc-prize-2026-arc-agi-3/arc_agi_3_wheels (competition data, not committed)

---

## Kaggle kernel stays private

`DECISION-8b3a4b7f` · 2026-09-11 · status: accepted

Competition code may be shared publicly only on Kaggle itself during the competition (rule 3.6). Making the notebook public for a milestone prize is a separate, deliberate decision.

*Source:* documents/arc_agi_3_kaggel_rules.md sections 3.5.d, 3.6

---

## CPU accelerator for the random agent

`DECISION-28eb39f2` · 2026-09-11 · status: accepted

The random agent needs no GPU; CPU spends no GPU quota. Revisit when a model is added.

*Source:* submission/build_submission.py ACCELERATORS

---

## Validation-run placeholder parquet; agent written to /tmp

`DECISION-171ae5ad` · 2026-09-11 · status: accepted

The validation run writes a placeholder submission.parquet so Kaggle accepts the kernel; the scored rerun's gateway writes the real one. The agent goes to /tmp so it is never offered as a submission file.

*Source:* github.com/arcprize/ARC-AGI-3-Kaggle-Starter scripts/build_notebook.py

---

## Local frozen open-weight model; specific model chosen at E0

`DECISION-ac506dee` · 2026-09-11 · status: superseded

No hosted API: Kaggle scores with internet disabled, so weights must be local and frozen. Candidates Qwen 2.5 7B and Gemma 3, chosen empirically at E0 on floor and variance. Qwen is currently the lower-risk choice under the open-weights rule (2.5.a); confirm Gemma's licence terms before choosing it. Supersedes the 'hosted API vs local weights' open item in older documents.

*Source:* research_prep/notes/peer_review_mapping.md s7; research_prep/notes/experiment_register.md 'Fixed across all experiments'; documents/arc_agi_3_kaggel_rules.md 2.5.a

---

## E0 at two model sizes

`DECISION-43494fdd` · 2026-09-11 · status: superseded

Human decision 12 Sept: E0 runs at both sizes. Small tier: Gemma-4-E4B-it and a small Qwen 3 on T4. Winner tier: Qwen3.6-27B-FP8 and Gemma-4-31B-it on RTX 6000. Local frozen weights throughout (Kaggle scores offline). All four Apache 2.0.

*Source:* research_prep/notes/experiment_register.md amendment 12 Sept 'E0 runs at two model sizes'

---

## E0 tiers and models (revised)

`DECISION-1dc93b90` · 2026-09-11 · status: accepted

Small tier: Gemma-4-E4B-it and Qwen3 4B/8B. Winner tier: Qwen3.8-27B-FP8 (not 3.6: newer, same size and licence) and Gemma-4-31B-it. Both tiers on the same RTX Pro 6000 and vLLM build so model size is the only variable (default; human may override). All Apache 2.0; Qwen 3.8 repack hash-verified before verdicts.

*Source:* research_prep/notes/experiment_register.md amendment 12 Sept 'E0 execution details'

---

## E0 held-out split

`DECISION-a36897eb` · 2026-09-11 · status: accepted

tune: dc22 ft09 ls20 s5i5 sc25 sk48 tn36 tu93; held-out: the other 17 public games. Seeded shuffle random.Random(20260912), fixed before any model run, never regenerated. r11l (held-out) level 1 reported outside verdict metrics.

*Source:* experiments/e0_split.json

---

## E0 scaffold design

`DECISION-e1d4c2fb` · 2026-09-11 · status: accepted

Text input (64x64 hex, last frame layer) because Qwen3 4B/8B are text-only; last 4 exchanges of context; temperature 0.7, 128 tokens, thinking off, per-call seed; parse failures fall back to a random legal action and are counted, runs above 20% failure excluded; one vLLM 0.23.0 build serves all four models.

*Source:* research_prep/notes/experiment_register.md amendment 12 Sept 'E0 scaffold design'; src/agents/llm_baseline.py

---

## E0 decoding identical across models

`DECISION-7355650a` · 2026-09-11 · status: accepted

Human decision 12 Sept: vLLM --generation-config vllm; every request temperature 0.7, top_p 1.0, no top_k. Otherwise vLLM applies each model's generation_config (Gemma top_k 64, Qwen top_k 20).

*Source:* research_prep/notes/experiment_register.md amendment 12 Sept 'before the first verdict run'; experiments/build/e0-smoke-output-v2/vllm.log line 74

---

## Small-tier Qwen is Qwen3-8B

`DECISION-a0ddc575` · 2026-09-11 · status: accepted

Total parameters matched to Gemma-4-E4B: Qwen3-8B 8.19B vs E4B 8.00B (Qwen3-4B is 4.02B). Kaggle: qwen-lm/qwen-3/transformers/8b/1.

*Source:* huggingface.co/api/models safetensors.total for google/gemma-4-E4B-it, Qwen/Qwen3-4B, Qwen/Qwen3-8B, 12 Sept 2026

---

## Label the grid coordinates (E0 scaffold)

`DECISION-43270d83` · 2026-09-12 · status: accepted

Human decision 12 Sept: fix clicking before the second small model. encode_frame prints column-number headers (tens, units) and prefixes each row with its y; the system prompt explains them. Presentation only: no memory and no click pruning, which are H5/H6 and belong to E1 so E0 stays its control. Judged against the recorded before on tune games: dc22 52.5 states/100 with ACTION6 65/80 must rise toward random 77.5; ls20 100.0 must not fall.

*Source:* research_prep/notes/experiment_register.md amendment 12 Sept 'labelled grid coordinates'; KNOWLEDGE-0a551423, KNOWLEDGE-e362f7ea

---

## H3 is not revised on the affordance account; E2 is instrumented instead

`DECISION-90570844` · 2026-09-12 · status: accepted

The affordance literature (Chemero 2003, Davis 2020) holds a control relation to be a relation between abilities and features, not a property of an object. If it transfers, H3's premise - controllability identified once in an opening phase - is mis-specified rather than wrong. Decision: do NOT revise H3 now. No source in the corpus engages Gibson's premise directly; cluster D's review literature is Information Systems affordance theory and the corpus under-samples ecological psychology, whose overviews are books this method cannot reach. Treat as not-found-in-corpus, not unclaimed. Instead instrument E2: re-test controllability at every level and record how often a relation learned at level n still holds at n+1. If it usually holds, the one-off phase is defensible; if not, an E2 null reads as H3 mis-specified rather than an implementation failure. Costs one extra field in the run log.

*Source:* research_prep/notes/cluster_origins.md

---

## E0 31B held-out runs split by seed across two kernels, gpu-memory-utilization 0.95

`DECISION-d5cc9972` · 2026-09-13 · status: accepted

Human decision 13 Sept 2026. Kernel A plays all 17 held-out games with episodes 0-2, kernel B episodes 3-4; seeds are identical to an unsplit run (seed*1000+episode). Reports are concatenated for analysis. --gpu-memory-utilization raised 0.90 -> 0.95 for the 31B kernels only. Serving and execution shape only: prompt, decoding and split are unchanged, so comparability with the small tier holds.

*Source:* session 13 Sept 2026; handoff s6

---

## T-E0c scope widened to research_prep and documents, then completed

`DECISION-fff79275` · 2026-09-13 · status: accepted

Human decision 13 Sept 2026. T-E0c's work legitimately touched the register, handoff doc and companions; scope is widened to match what happened rather than leaving the task active and running the large tier under a misdescribed outcome. Completing it activates T-E0d.

*Source:* session 13 Sept 2026; handoff s7

---

## E1 falsifier: on/on must beat both the off/off control and the random floor

`DECISION-17bcf9bb` · 2026-09-16 · status: accepted

Human decision 16 Sept 2026. E1 primary metric is levels cleared on the 16 verdict games (actions-to-solve is undefined while the control clears nothing). Supported only if on/on beats off/off AND random (0.037 levels/game). Beats off/off but not random = weak/partial result, reported as such. Does not beat off/off = falsified.

*Source:* session 16 Sept 2026

---

## E1 runs at Gemma-4-E4B first; 31B only if E4B shows an effect

`DECISION-e3978a7e` · 2026-09-16 · status: accepted

Human decision 16 Sept 2026. Three treatment cells at 31B cost ~30 GPU-h (~420 s/episode), breaching the register's 40 GPU-h abandon line with tune runs and exceeding the ~16 h weekly quota left. At E4B three cells cost ~4-5 GPU-h. off/off reuses the E0 E4B v2 held-out run, valid only if switches-off prompt and decoding are byte-identical to E0.

*Source:* session 16 Sept 2026; KNOWLEDGE-26754c54

---

## E1 stopped after the E4B held-out verdict; no N=10 and no 31B tier

`DECISION-200ac78f` · 2026-09-17 · status: accepted

Human decision 17 Sept 2026. The verdict was WEAK and carried by --prune-visited alone; its only level clear (lp85) was 64% substituted random swaps, which more seeds would not turn into model judgement. N=10 (permitted by the register for a weak result) is declined, and the 31B tier is not triggered (DECISION-e3978a7e). Kept as findings: pruning dead moves lifts exploration (states/100 68.6 -> 74.4, above random on sb26 and lp85); H5 and H6 are separate mechanisms; the failure-rule null is thin evidence for PRO-LONG because repeated deaths occur once in 85 control episodes at 80 actions.

*Source:* KNOWLEDGE-3b132156; register E1 amendment 17 Sept (verdict)

---

## E2 design: harness-driven controllability probe, levels-cleared falsifier vs matched control and random at 80+k, tune k-pick on dead-move rate

`DECISION-4f50991f` · 2026-09-17 · status: accepted

Human decision 17 Sept 2026. E2 runs at Gemma-4-E4B. Probe is harness-driven: first k actions try each available simple action, then click one cell per distinct colour (largest first), cycling; per-move changed-cell summaries go to the system message in fixed wording; re-probe on a new level. Matched control: no probe, 80+k model actions. Primary: levels cleared on the 16 verdict games; supported only if probe-k beats match-k AND random at 80+k; weak if beats match-k only; falsified otherwise. Tune sweep k in {5,10,20}, 8 tune games x 3 seeds; k chosen mechanically on dead-move rate (share of model moves that change nothing): the k whose seed-mean beats match-k by more than match-k's seed range, largest margin, ties to smaller k; none -> E2 abandoned. A null cannot distinguish a bad probe from H3 mis-specified, because no level is cleared to re-test controllability on.

*Source:* session 17 Sept 2026; register E2 block; cluster_origins.md s4

---

## E4: random play with dead-move pruning, no model, on CPU

`DECISION-fd4761c5` · 2026-09-17 · status: accepted

Human decision 17 Sept 2026. After E0-E2 found no frozen model above the random floor, test whether random play that never repeats a move known to leave the frame unchanged clears more levels than plain random. Held-out 17 games, 20 seeds, budgets 80 and 300 (primary 300: the submission caps at 80 while ~4.9 min/game allows far more). Supported only if a one-sided sign test over seeds on levels cleared (16 verdict games, ties dropped) gives p < 0.05 and total clears are higher; falsified otherwise. Runs locally on CPU; no GPU. A win leads to a separate submission task; a loss goes into the 23 Sept write-up.

*Source:* session 17 Sept 2026; register E1 verdict amendment; submission/my_agent.py MAX_ACTIONS

---

## Build 3: random-prune submission with a 300-action cap

`DECISION-4cd8d5d2` · 2026-09-17 · status: accepted

Human decision 17 Sept 2026. After E4 (supported at 300 actions), the competition agent submission/my_agent.py gains dead-move pruning (inlined; the notebook ships one file) and MAX_ACTIONS 80 -> 300. Gated by unit tests, the local rehearsal of the scored rerun requiring a level clear on lp85, and the notebook build, plus independent review. Pushing the kernel, submitting to the competition, an optional second submission of plain random at 300, and publishing the notebook before Milestone 2 are separate human steps. One hidden-set score cannot separate the cap's effect from pruning's.

*Source:* session 17 Sept 2026; KNOWLEDGE-1ad719a0; register E4 verdict

---

## E0-E4 write-up: portfolio audience, ~2,500 words, numbers checked against data

`DECISION-8028f03b` · 2026-09-17 · status: accepted

Human decision 17 Sept 2026. Write documents/writeup/e0_e4_writeup.md before the 23 Sept register freeze: plain-language summary first, then method, E0, E1, E2, E4 and Build 3, what went wrong and how it was caught, what the evidence does and does not support, cost, open questions, appendix of record IDs and file map. Gated by experiments/check_writeup.py, which recomputes headline numbers from saved result files and checks cited repo paths exist, plus independent review. Publishing as an Artifact or anywhere public is a separate human decision.

*Source:* session 17 Sept 2026; register-level stop conditions

---

## E3 unparked by human choice; option B: LEARN/WIN labels plus a log of LEARN-move outcomes

`DECISION-792aefcb` · 2026-09-18 · status: accepted

Human decision 19 Sept 2026. The register's unpark condition (E1 and E2 both null) is not met - E1 was weak - so E3 runs by explicit choice. Design (option B): the model starts each reply with LEARN or WIN; after each LEARN move the harness records what changed on screen (E2's change description) and shows the last 5 such experiments in the system message; WIN moves are not logged. Switch --learn-labels, off by default, byte-identical to E0 when off. Gemma-4-E4B. T-E3a: tune games x 3 seeds, labels-on vs labels-off; go to held-out only if labels-on's seed-mean dead-move rate beats labels-off's by more than its seed range. Held-out verdict (T-E3b): supported only if levels/game beats the E0 control and corrected random (0.0125, >= 2 clears); weak if control only; falsified otherwise.

*Source:* session 19 Sept 2026; register E3 block

---

## E5 (design P1): masked state judge inside random + prune, no model, on CPU

`DECISION-6efb9578` · 2026-09-24 · status: accepted

Human decision 24 Sept 2026 ('start P1'). Test whether random + prune with a judge that ignores clock-like cells (W=16, >=14/16 changes over >=3 action keys) clears more verdict levels than E4's exact-frame key. Also builds the missing evaluation safeguards (episode IDs, initial-state hash, <=2-action clear flag, trajectory logs, replay test) and a common measurement judge. Held-out 17 games, episodes 100-119, 300 actions primary, 1000 secondary. Supported only if a one-sided sign test over seeds gives p < 0.05, total clears are higher and the concentration rule holds. Void if the dc22/ls20 tune checks fail. Register number E5; the shared pages' 'E5 = Duck' label predates it.

*Source:* research_prep/notes/experiment_register.md E5 block; documents/research_design/next_phase_experiment_design.md Â§4 P1

---

## E5 judge revised: bar rule (whole row/column) added to the cell rule

`DECISION-393bcd0f` · 2026-09-24 · status: accepted

Human decision 24 Sept 2026 ('Revise the judge') after E5 checks (ii)/(iii) failed because the tune games' clocks are progress bars. The judge's mask is now the union of the unchanged cell rule and a bar rule: a row or column is masked when, over the last 16 transitions, its changes match an every/even/odd schedule in >= 14 of 16, span >= 3 action keys, and no cell of the line changed more than once. Checks (i) synthetic cell and bar cases, (ii) dc22 row 63, (iii) ls20 rows 61-62, (vi) over-masking on all 8 tune games x 3 seeds. Designed on the tune games (a prototype ran first); stated in the register amendment. Parameters fixed before any held-out run.

*Source:* research_prep/notes/experiment_register.md E5 amendment 'revised judge' 24 Sept

---

## E5 judge: bar rule only; the cell rule is dropped

`DECISION-c600803c` · 2026-09-24 · status: accepted

Human decision 24 Sept 2026 ('Drop the cell rule and keep the bar rule only') after revised-judge check (vi) failed once: the per-cell rule masked 4 dc22 player cells for one step, and it masked no clock on any tune game. The judge's mask is now the bar rule alone (row or column; every/even/odd schedule in >= 14 of 16 transitions; >= 3 action keys; no cell changed twice). Known cost: a single ticking cell is never masked (under-masking, visible in per-game masked lines). Checks (i)-(vi) rerun once before any held-out run.

*Source:* research_prep/notes/experiment_register.md E5 amendments 24 Sept

---

## E6 (design P4) approved with the masked judge

`DECISION-f0b09b26` · 2026-09-27 · status: accepted

Human decision 27 Sept 2026 ('approve with the masked judge, start P4'). E6 tests transition-graph memory with return-to-frontier navigation (G) against the same local systematic rule without navigation (L), both using design P3's arms and the bar-only masked judge (E5) for node identity, tried/dead arm sets and pruning. This departs from E5's consequence (exact hash acting for P2-P4) because under exact identity the 10 of 17 held-out games with bars would never revisit a state. Held-out 17 games x episodes 100-119, 300 and 1000 actions, Holm over budgets, concentration rule; G is credited as best CPU policy only if it also beats E5's C0.

*Source:* research_prep/notes/experiment_register.md E6 block

---

## E7 (design P3): implement the action-success bandit

`DECISION-16a63c9c` · 2026-09-29 · status: accepted

Human instruction 30 Sept 2026 ('implement - P3: the action bandit, still unrun'). E7 tests whether UCB1 over action classes (design-P3 arms: keyboard actions plus one click arm per colour on screen), rewarded by reaching a judged state not seen before in the episode, clears more verdict levels than uniform choice over the same live arms. Both use the bar-only masked judge for state identity and dead-arm pruning (as E6; the novelty reward is otherwise inflated by bars). Held-out 17 games x episodes 100-119; 300 actions primary, 1000 reported. Condition A (E4 random-prune with the masked judge) reuses E5's T1 files. The judge choice and numbering are flagged to the human for confirmation before any held-out run.

*Source:* documents/research_design/next_phase_experiment_design.md section 4 P3; research_prep/notes/experiment_register.md E7 block

---

## E8: confirmatory run of the E7 bandit, 1000 actions primary, fresh episodes 120-139

`DECISION-71ffdc68` · 2026-09-30 · status: accepted

Human instruction 1 Oct 2026 ('start the confirmatory bandit run'). E7's 1000-action result (B 117 vs A' 82, survives the concentration rule) was pre-registered as not decisive; the register-level stop condition requires a re-run before building on a result. E8 re-runs A' and B unchanged (code at f18757b, masked judge) on 17 held-out games x fresh episodes 120-139, with 1000 actions as the primary budget and 300 reported. Same sign test and concentration rule; one run; no parameter changes.

*Source:* research_prep/notes/experiment_register.md E7 verdict amendment and E8 block

---

## E9: the bandit on 40 fresh seeds (episodes 140-179), 1000 actions

`DECISION-aa5692c6` · 2026-09-30 · status: accepted

Human instruction 1 Oct 2026 ('start the bandit run on more seeds'), after E8 replicated the bandit's size (114 vs 79) but failed the concentration rule at 20 seeds (p = 0.105 without lf52). E9 re-runs E7's A' and B unchanged on 17 held-out games x 40 never-used episodes (140-179) at 1000 actions only, with the same sign test and concentration rule. This is the bandit's third test (E7, E8, E9); the verdict counts only for E9's fresh episodes, and all three are reported together.

*Source:* research_prep/notes/experiment_register.md E8 verdict amendment and E9 block

---

## Build 4: the E9 arm bandit in the submission, 1000 actions

`DECISION-61e2dcee` · 2026-09-30 · status: accepted

Human decision 1 Oct 2026 ('approve bandit for the submission') after E9 supported the UCB1 arm bandit (B) over uniform arms at 1000 actions (217 vs 171 on 40 fresh seeds). Build 4 replaces Build 3's random-prune in submission/my_agent.py with B inlined (bar-only masked judge, design-P3 arms, within-episode novelty reward, dead-arm exclusion), MAX_ACTIONS 300 -> 1000, and must play exactly like experiments' ArmBandit(ucb=True) for a shared random stream. Rehearsed locally and built as a notebook; pushing the kernel and submitting to Kaggle need a separate explicit go-ahead.

*Source:* research_prep/notes/experiment_register.md E9 verdict amendment; submission/my_agent.py

---

## Build 5: second submission, uniform arms (E9's A') at 1000 actions, to split Build 4's gain

`DECISION-7f807d34` · 2026-09-30 · status: accepted

Human instruction 30 Sept 2026 ('implement the optional second submission'). Build 4 (E9's UCB1 bandit, 1000 actions) scored 0.15 vs 0.07 for Builds 1 and 3, but changed the policy and the 300 -> 1000 cap at once. Build 5 is Build 4 with UCB switched off: uniform over live design-P3 arms with the same masked judge and dead-arm rule (E9's A'), 1000 actions. Its hidden score against 0.15 isolates the bandit's contribution at a fixed budget. submission/my_agent.py stays Build 4 (UCB = True); build_submission.py --uniform flips the switch for Build 5's notebook. The human submits.

*Source:* research_prep/notes/experiment_register.md Build 4 hidden-set amendment

---

## E10 approved: the bandit with a per-screen memory of deadly moves

`DECISION-71f6688b` · 2026-09-30 · status: accepted

Human decision 30 Sept 2026 ('Approve the block as drafted'). E10 tests B' = E9's bandit B plus one rule: a (screen, arm) pair whose move ended the game is excluded on that screen for the rest of the episode, like a dead arm. Control B unchanged. 17 held-out games x fresh episodes 180-219 x 1000 actions; sign test plus concentration rule; tune no-harm check (B' tune clears >= B's - 1) before held-out. Adaptive: motivated by inspecting sp80/cd82 held-out trajectories; expected outcome narrow (sp80).

*Source:* research_prep/notes/experiment_register.md E10 block; diagnosis 30 Sept

---

## cd82 accepted as a known limit of the novelty bandit

`DECISION-3423e024` · 2026-09-30 · status: accepted

Human decision 30 Sept 2026 ('Accept c'). cd82's loss under the bandit (period-3 bar never masked; novelty cannot credit low-change set-up moves) is recorded as a known limit of novelty-driven exploration. No fix is pre-registered; a period-3 bar rule is revisited only if such bars appear on other games (cheap offline count on tune first).

*Source:* research_prep/notes/experiment_register.md cd82 diagnosis 30 Sept

---

## E11 (design P2) approved: object-targeted clicks inside the bandit

`DECISION-c37f464e` · 2026-09-30 · status: accepted

Human decision 30 Sept 2026 ('Approve as per draft'). E11 tests B_obj = E9's bandit B whose colour arms click one 4-connected component of the chosen colour (uniform over components, centroid-nearest cell, reading-order ties) instead of a uniformly random cell of that colour. Everything else identical. Control B (the statistical baseline, per design section 5 rule 2, rather than the design's random coordinates). 17 held-out games x fresh episodes 220-259 x 1000 actions; sign test plus concentration rule; tune no-harm check first; 2 processes.

*Source:* research_prep/notes/experiment_register.md E11 block

---

## Build 6: the bandit plus death memory as the Kaggle agent

`DECISION-09885665` · 2026-10-01 · status: accepted

Human instruction, 1 Oct 2026: 'start build 6'. Build 6 is Build 4 (E9's UCB1 arm bandit, bar-only masked judge, 1,000 actions) plus E10's per-screen death memory: when a move ends the game, that (screen, arm) pair is excluded on that screen for the rest of the episode. E10 was NARROW (245 vs 227 verdict clears, carried by sp80 18->30; without sp80 215 vs 209, p=0.119), so B' was not adopted as the statistical baseline; B stays it. A hidden-set submission is therefore B's only unseen test, and that is the point of Build 6. Scope stops at built-and-rehearsed: no kernel push and no submit without separate human instruction. Reading fixed before the result: Build 4 scored 0.15, scores are two decimals from one submission, so a difference of <= 0.01 is no difference; a score of 0.16+ means death memory transfers, 0.14-0.15 means it adds nothing visible on the hidden set despite fixing sp80's loops, and <= 0.13 means it costs more on the hidden games than it saves.

*Source:* documents/session_handoff/2026-09-12_e0_small_tier.md next-action 2.i; register E10 verdict amendment 30 Sept

---

## E12 (P5 oracle goal) deferred; the P6 frame collection goes first

`DECISION-4b96acf3` · 2026-10-01 · status: accepted

1 Oct 2026. E12 was drafted from design P5, then deferred the same day before any E12 code existed, on a feasibility check: (1) across E10's and E11's tune checks only sc25 (1) and tn36 (3) ever cleared, so annotating the state before a clear is possible on 2 of 8 tune games and the design's 3-of-8 bar is unreachable; (2) the 8 tune game sources are present but obfuscated (randomised method names), so win conditions are recoverable only by reverse-engineering against a deliberate anti-reverse-engineering measure, which resolves assumption A15 as 'source present, semantics not accessible'; (3) a one-action-from-clear predicate would therefore almost never fire, so B_goal would equal B for a mechanical reason and E12 would report an uninformative null. There is also no human-play agent and no frame renderer in the repository. Four options were put to the human (reorder; annotate now with graded predicates; a two-game probe; reverse-engineer the sources) and they chose REORDER: do the P6 frame collection first, annotate the oracle from those frames, then run E12. Reasons recorded with the choice: the collection is needed for P6 regardless, it does not depend on E12's answer (only P6's ranker design does), and it produces exactly the frames an annotator needs, removing E12's null-risk. C1 (frame and label collection, tune games only, behaviour policies B and A', episodes 300-319 at 1,000 actions, frames stored as changed cells with a measured size budget) is drafted in the register and awaits approval. When E12 returns, its predicate form and success bar must both be revisited and fixed before the comparison run.

*Source:* research_prep/notes/experiment_register.md E12 deferral amendment and C1 block; E10/E11 tune no-harm results; environment_files tune game sources

---

## C1 approved as drafted: frame and label collection for P6

`DECISION-003d00ed` · 2026-10-01 · status: accepted

1 Oct 2026. Human instruction: 'approve C1 and commit', after the three judgement calls were put to them explicitly. Approved as drafted, before any C1 code exists: tune games only (dc22 ft09 ls20 s5i5 sc25 sk48 tn36 tu93); behaviour policies BOTH B (arms-ucb) and A' (arms), because a dataset from the bandit alone inherits its blind spots (cd82 put about 20% of pulls on one arm) and a ranker cannot learn about actions the collecting policy never made; episodes 300-319 at 1,000 actions, run seed 0, 320 episodes, about 2 h CPU; frames stored as the initial frame plus per-step changed cells with a full-frame fallback above 512 changed cells, then npz-compressed, with the size budget fixed from a measured 2-episode sizing probe rather than an estimate; labels NOT decided at collection time but derived offline with version fields, the E5 bar-only judge being the transient-masked label of record; implemented as one flag on the existing runner (e0_random_smoke.py --save-frames DIR), no new runner; one process at a time in resumable chunks of 10 episodes. Integrity criteria replace success criteria: replay-exact cell for cell, complete, within the measured budget, action coverage reported whatever it shows, and provenance on every episode. Checks (i) sizing probe, (ii) replay equality, (iii) saving must not perturb play - an episode with --save-frames must be identical to one without it - and (iv) E5's safeguards, all before the bulk collection. Held-out frames are not collected here; that is a separate later block, machine-read only, and cd82 stays held-out and unannotated. C1 states no hypothesis and has no falsifier: nothing it produces may be cited as evidence for a policy claim.

*Source:* research_prep/notes/experiment_register.md C1 block; documents/arc_agi_3_session_handoff.md sections 8.3-8.5 and the P6 safeguards

---

## C2 approved as drafted: label derivation from C1's frames

`DECISION-27a48243` · 2026-10-04 · status: accepted

4 Oct 2026. Human instruction: 'approved, run the checks'. Approved as drafted before any C2 code existed. Scope, which checking the stores made smaller than the C1 block implied: exact-frame change and transient-masked change need NO derivation - every stored step row already holds exact_before/after and masked_before/after, so those labels are a string comparison already on disk, and the masked one is the label of record. The object-level label is the only real computation, and the progress/information label is deliberately NOT derived because it needs judgement the frames do not contain; it is reported as absent rather than approximated under a name it has not earned. Object label defined before computing, without object identity (A5 components-approximate-objects stays UNKNOWN): 4-connected components per colour on the MASKED last layer, with obj_structural = the per-colour multiset of component sizes differs (appear, vanish, split, merge, resize) and obj_moved = that multiset is unchanged but the cell sets differ; both sub-flags stored. The mask is not stored and is rebuilt offline by feeding consecutive stored frames through MaskedJudge, which is possible because the move key is reconstructible (a keyboard move keys on its action value, a click on the colour under x,y on the before frame's last layer). Criterion 1 is that the rebuilt masked_after equals the stored one for every step; if it fails C2 stops and falls back to replaying episodes through the environment rather than labelling against a mask the run never used. scipy, pandas and pyarrow are all absent and C2 adds none of them: components use the repository's pure-Python object_cells, and output is one npz plus a JSON sidecar. A timing probe on 2 episodes fixes the runtime budget and the full-components-vs-fallback decision before the 320-episode pass, as C1's sizing probe did after its estimate proved wrong by two orders of magnitude; if full components are too slow the fallback is a per-colour count-and-centroid label that cannot see splits or merges within a colour, and it is then named colour-level change, not object-level. Integrity criteria replace success criteria: mask rebuild faithful, aligned one row per stored step, deterministic, and the masked-change rate must reproduce the dead-move rates measured elsewhere (about 0.14 for B and 0.30 for A-prime at 1,000 actions, E9-E11); tune only. C2 labels all 320 episodes under both policies because a label is a property of a transition, not of a policy, leaving P6 to declare which transitions it trains on and which frame layer it reads. Output name carries v1: a changed definition is a new file, never an overwrite.

*Source:* research_prep/notes/experiment_register.md C2 block; documents/arc_agi_3_session_handoff.md section 8.4 label table

---
