# ARC-AGI-3 Milestone Brief

- **Compiled:** 1 September 2026 · **Revised:** 5 September 2026
- **Shareable page:** <https://claude.ai/code/artifact/54461d0b-ded2-4d5a-ae8c-3ee81f61bb25>
- **Status:** literature review complete (58 papers extracted). Phase 1 —
  interface verification — reserved for the live build, which is **today**.

Where the project stands: one competition constraint that reorders the
architecture, the logistics of submitting, a set of testable hypotheses from the
peer transcript, and — new since 1 September — a literature that has moved
underneath all of it.

| | |
| :-- | :-- |
| Milestone #2 closes | **30 September 2026** — 26 days |
| Total purse | $850K ($700K grand prize) |
| Random baseline, published | RHAE **0.0000** |
| Frontier systems, as of 1 Sept brief | <1% (humans: 100%) |
| **Frontier systems, as of 5 Sept** | **RHAE 34–78 main-study; 95–100 best@k** |

> **The single biggest change since this brief was written.** The "<1%" figure is
> obsolete. Thirteen ARC-AGI-3 agent papers now exist, most published after this
> project started, and the public set is close to solved under permissive
> protocols. §Workstream 2 carries the corrected numbers and, more importantly,
> the protocol caveats that make them comparable.

---

## Read this first — evaluation runs offline, so the agent cannot call an API

Kaggle scores submissions in a sandbox with **no internet access**. That rules out
Claude, GPT, and Gemini API calls at evaluation time. Two independent sources
confirm it, and it explains something that looked strange in the literature: the
strongest published epistemic agent runs **Qwen2.5-0.5B**, and current competitors
run **Qwen 3.6 27B FP8** and **Gemma-4-31B** locally on the provided GPU.

This does not touch the research question. It changes what "the same model, held
constant" means in practice — and the choice has to be made *before* either agent
is written, because Agent B and Agent C must share a model for the comparison to
carry any weight. Swapping model families later invalidates both arms at once.

---

## Workstream 1 — Official logistics

| Parameter | Value |
| :-- | :-- |
| Competition | `kaggle.com/competitions/arc-prize-2026-arc-agi-3` |
| **Milestone #2** | **30 September 2026 — the live deadline** |
| Milestone #1 | 30 June 2026 — passed |
| Milestone prizes | $25,000 / $10,000 / $2,500 |
| Top score awards | $40K / $15K / $10K / $5K / $5K |
| Grand prize | $700,000 — first agent to score 100%, rolls over if unclaimed |
| Licensing | CC0 or MIT-0, open-sourced **before** private evaluation scores are released |
| Internet | Disabled during evaluation |
| Hardware | CPU, T4 x2, P100, or RTX 6000 — the last is reserved for ARC-AGI-3 and burns GPU quota faster |
| Cost ceiling | Leaderboard lists only systems costing under $10,000 to run |

### How a submission is actually made

A code competition in two phases. **Phase A — Save & Run All** validates that the
agent executes. **Phase B — Competition Rerun** scores it against hidden games, and
only starts when you manually click submit.

You edit **one file**: `agent/my_agent.py`, holding a `MyAgent` class with two
methods.

```python
class MyAgent:
    def is_done(self, ...) -> bool: ...
    def choose_action(self, ...) -> Action: ...
```

The toolkit auto-generates the submission notebook from that file, and the Makefile
refuses to push until your Kaggle username is in the notebook metadata.

> **Carry into Saturday.** The `arc-agi` PyPI package hosts *the same game engine*
> the Kaggle gateway runs — if it works locally, it works on Kaggle. This is the
> most useful logistics fact we have. It also means our current
> `random_baseline.py` shape does not match the real `is_done()` /
> `choose_action()` interface, so conforming early avoids a rewrite.

### Leaderboard

Scored on cost-per-task alongside accuracy — the stated position is that
intelligence means solving problems efficiently, not merely solving them.
Incomplete submissions have their remaining tasks marked incorrect. Verification
criteria are published in the ARC Prize Verified Testing Policy.

---

## Workstream 2 — Research tooling and literature method

> **Revised 5 September, after the review.** The four papers below were the whole
> ARC-AGI-3 literature on 1 September. There are now **thirteen**, and the field
> has moved from "frontier systems score below 1%" to near-saturation of the
> public set. The four are kept for the record; the corrected picture follows.

| Paper | Why it matters |
| :-- | :-- |
| **Explore Before You Solve** | Proposes **AERA** (EXPLORE → VERIFY → PLAN) — structurally our bet. Random and no-explore baselines score **RHAE 0.0000**; AERA reaches 0.2116 on public games with a 0.5B model, 0.30 on the 55-game private set. |
| **ARC-AGI-3** (ARC Prize Foundation) | The official benchmark paper. Humans complete 100%; frontier systems below 1%. |
| **Recursive Experiential-Working Memory** | Splits agent memory into *working* and *experiential* — our episodic/semantic distinction, already operationalised. |
| **Meta^n** | Recursive self-improvement; the only method scoring above zero on ARC-AGI-2. |

### The corrected picture — and why the numbers disagree

Published ARC-AGI-3 results span an order of magnitude, and **the spread is
protocol, not progress**. Quote the regime with every number.

| Source | Number | Regime |
| :-- | :-- | :-- |
| Tycho | 100.00 RHAE, all 183 levels | Opus 5 / GPT-5.6 Sol |
| PRO-LONG | 97.4% | best@2, Fable 5, $1,750 total |
| Prime Agent | 95.5% RHAE, up from 30% | best@1 |
| OPINE-World | 78.4% action efficiency, 20/25 games | no per-game training |
| Rodionov ablation | **34.16 – 74.78 RHAE** | **main study, all variants and efforts** |
| DreamTeam | **36% → 38.4% RHAE** | **official protocol, protocol-matched, 2 runs** |

The metric, from OPINE-World's full text: per-level score is `(human/agent)²`,
capped at 1.15, level-weighted, with a per-game cap of 100.

Rodionov — who wrote the reference architecture — states the limit himself:
because gpt-5.6-sol postdates the games and held-out performance is untested, his
results *"indicate public-set saturation only."*

**What this does to our position.** Efficiency as a *novel angle* is closed. What
is not closed is the protocol-matched score (38.4%) and, more importantly, the
axis nobody has swept.

### The gap that survives

Every published **ARC-AGI-3** result runs a hosted frontier model — confirmed
across all 56 extracted papers, including Prime Agent, whose open-weight models
appear only in its nanoGPT speedrun. Kaggle's sandbox has no internet.

But **13 of 56 shortlisted papers ran open-weight models** in adjacent settings:

| Paper | What it ran |
| :-- | :-- |
| **SAGE** | 7 open-weight backbones, 1B–7B; wins on all 7. Its gate resolves in **closed form, without an LLM call** |
| **Agentic Episodic Control** | Qwen2.5 **7B vs 32B** on grid worlds — 0.79/0.43/0.13 vs 0.84/0.45/0.23 |
| **PREMem** | Qwen2.5 3B/14B/72B and Gemma3 4B/12B/27B — a full ladder |
| **Continual Harness** | Gemma-4 E2B/E4B/26B/31B, LoRA-tuned locally, frontier teacher relabelling open-weight rollouts |
| **ReflAct** | Llama-3.1 8B vs 70B vs GPT-4o, one method, three capability points |

So the honest claim is not "nobody has plotted the capability axis downward" — they
have, in memory, exploration and episodic control. **Nobody has plotted it on
ARC-AGI-3.** That is narrower, defensible, and has borrowable method attached.

Two things to carry into the build. **Agentic Episodic Control** is the closest
analogue in the shortlist: grid worlds, a real 7B-vs-32B comparison, with
degradation concentrated in the hardest exploration task — a preview of where a
local model breaks. **SAGE** is the design lesson: push decisions out of the model
into cheap deterministic components and small weights stop being fatal.

### Reference implementations (`research_prep/data/implementation_refs.csv`)

| Name | Licence | Note |
| :-- | :-- | :-- |
| `arc-3-agents-baseline1` | MIT | the reference architecture and the baseline to beat; read the code before the paper |
| `PRO-LONG` | MIT | Python; append-all log searched by code — the context-management decision we have not made |
| `mdlARC` | MIT | wrong benchmark (ARC-AGI-1) but an existence proof for local weights; 3D RoPE worth ~20 points |

### Tool stack

- **Semantic Scholar** — 200M papers, free, and the only one with a scriptable API.
  Worth automating: a small script that walks the citation graph from our seed
  papers makes the search reproducible, which matters if this becomes a paper of
  our own.
- **Elicit** — structured extraction. Define columns once (mechanism / environment /
  metric / needs-training) and it fills a table across dozens of papers, which maps
  directly onto the five clusters from the transcript analysis.
- **Research Rabbit** or **Connected Papers** — citation-graph exploration.
- **Consensus** for fast evidence checks, **Scite** for citation context,
  **NotebookLM** for synthesising our own PDFs.
- **dair.ai academy weekly** stays the incoming feed. Note its search is
  client-side, so its 1,825-paper index cannot be queried programmatically.

### Method — as executed

Full detail in [literature_review_plan.md](literature_review_plan.md). The funnel:

**11 seeds → 512 backward references + 8 forward lists → 590 deduped → 58
shortlisted → 56 PDFs → 2 Elicit tables × 9 columns → joined back onto the
shortlist.**

Two lessons worth repeating to anyone running a review like this.

**A citation graph cannot find a literature that postdates its seeds.** All 13
ARC-AGI-3 papers were invisible to 512 backward references and 8 forward lists,
because no seed cites the benchmark. They were found only by searching the
benchmark name directly. Always pair the graph walk with a direct name search.

**Assign categories after extraction, not before.** `cluster_final` was filled with
the extracted mechanism visible next to each title. Seven of 58 assignments
changed, and two of those moved cluster D from 1 paper to 4.

This is snowball sampling with hand triage, and it is **not PRISMA** — the
write-up must describe the actual method rather than dress it as a systematic
review.

---

## Workstream 3 — Hypotheses from the peer transcript

Six falsifiable claims, each an ablation over the *same* base agent so they stay
independently measurable. Every one traces to something a human actually did.

| # | Hypothesis | Transcript origin | Metric |
| :-- | :-- | :-- | :-- |
| **H1** | Tagging memory as **fact vs. hypothesis** with a confidence level beats a flat observation log | "I think…" shifting to "I'm very sure…" | contradicted-hypothesis persistence; repeated failed actions |
| **H2** | Labelling each action **epistemic vs. instrumental**, under an exploration budget, improves efficiency | touching the plus to learn what it does, later to use it | actions-to-solve; information gain per action |
| **H3** | Spending the first *k* actions identifying the **controllable object** lowers total actions | "what can I control?" as the opening move | actions-to-controllable-ID; total actions |
| **H4** | Separating **self-caused from world-caused** change reduces false causal attribution | the oscillating plus sign moving on its own | precision of learned action effects |
| **H5** | Pruning actions that **return to visited states** reduces redundancy | going left "unwraps" a new state; right returns | redundant-action rate |
| **H6** | Promoting **episodic failures into semantic rules** prevents repeat deaths across resets | "I know the flame kills me because I failed" | repeat-hazard rate after first failure |

### What the review did to each hypothesis — 5 September

Papers counted from `cluster_final` × `maps_to_H` across the 58.

| # | Papers | Status after the review |
| :-- | :-- | :-- |
| **H1** | 14 | **Claimed on ARC-AGI-3.** Tycho does hypothesis-testing-and-repair; Executable World Models validates against observations under an MDL prior. Rodionov's own ablation then found the mechanisms are *not required* at max effort. |
| **H2** | 14 | **Claimed and named.** Tycho calls it "active abstraction"; OPINE-World gives it a quantified signal — Bayesian *ontology error* steering exploration. |
| **H3** | **6** | **Open.** No ARC-AGI-3 paper isolates controllability. The thinnest cluster in our own shortlist. |
| **H4** | 8 | **Claimed.** Tycho's actionable-observation vs animation-frame split is H4. |
| **H5** | **7** | **Open.** Well covered classically (Go-Explore lineage) but unclaimed on ARC-AGI-3. |
| **H6** | 18 | **Claimed off-benchmark and contested.** Cogito Ergo Ludo does post-episode rule induction on grid worlds. PRO-LONG argues the opposite — keep the complete log and search it with code rather than consolidating. |

**H3 and H5 are the only two nobody has claimed on this benchmark**, and they are
also the two with the least support in our shortlist. Treat that as a question to
resolve by reading, not as a green light: thin coverage can mean open ground or it
can mean the idea does not work.

One caution that bears directly on H3/H4: Tycho reports that **high transition
accuracy did not improve action selection**. A better world model is not
automatically a better agent.

### Blocker

**None of these are testable on the current mock environment.** It is a 4x4
fully-observable grid: the agent starts fixed at (0,0), the goal sits fixed at
(3,3), nothing moves, there are no hazards, and `INTERACT` is an explicit no-op. So
there is no goal to discover, no affordance to learn, no hazard to fail against, no
exogenous change to separate out, and no hidden region to map.

Worse for the headline experiment: a vanilla LLM sees the whole grid and solves it
in six optimal moves. **There is no headroom for hypothesis memory to demonstrate
anything** — B vs. C on this mock returns a null result for reasons unrelated to
the research question. The observed 0.4 win rate is a pure random-walk artifact.

Either the mock gains the properties the hypotheses require — partial
observability, a hazard, one object with periodic motion, a meaningful `INTERACT`,
and a goal that is not at a fixed known cell — or hypothesis work waits for the
real environment.

---

## Two decisions blocking the build

**1. Is a Kaggle submission a goal, or is this research-only?**
It settles whether Agents B and C run against a hosted API or local weights.
Research-only keeps the API; a submission requires local weights from the first
line of code. Both arms must share one model — deciding late means rewriting both.

> **The review has narrowed this.** If a submission is the goal, local weights are
> forced, and there is now evidence they are survivable: SAGE wins across seven
> backbones from 1B–7B, and Agentic Episodic Control holds up at Qwen2.5-7B on
> grid worlds. The literature does not name a model, but it removes "local weights
> are hopeless" as a reason to avoid submitting. **Kaggle account and phone
> verification are still not done, and they gate GPU access — do that first.**

**2. Extend the mock, or wait for Saturday?**
The mock cannot discriminate the two LLM arms, so further investment buys little.
The `arc-agi` package already gives local parity with the Kaggle engine.
*Recommendation: skip further mock work; build against the real local engine.*

**Metric change, either way.** Since random scores a flat RHAE 0.0000, win rate
cannot be the headline number. `src/evaluation/metrics.py` currently reports
`win_rate` and `avg_actions_per_episode` only; it needs an efficiency ratio before
any result is interpretable. And if 18 of 25 public games really are trivially
solvable, a completion win on public games is not evidence that hypothesis memory
works.

---

## Sources

Competition figures were read from ARC Prize and the ARC-AGI-3 docs. The two
ARC-AGI-3 papers were opened and verified; remaining papers are listed from search
results and have not been read in full.

- [ARC Prize 2026 — ARC-AGI-3](https://arcprize.org/competitions/2026/arc-agi-3)
- [ARC Prize 2026 documentation](https://docs.arcprize.org/arc-prize-2026)
- [Kaggle competition](https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-3)
- [ARC-AGI-3 leaderboard](https://arcprize.org/leaderboard)
- [Verified Testing Policy](https://arcprize.org/policy)
- [Milestone #1 results](https://arcprize.org/blog/arc-prize-2026-milestone-1)
- [Explore Before You Solve (AERA)](https://arxiv.org/abs/2605.25931)
- [ARC-AGI-3: A New Challenge for Frontier Agentic Intelligence](https://arxiv.org/abs/2603.24621)
- [dair.ai academy — AI Papers of the Week](https://academy.dair.ai/papers)
- [Why LLMs Fail at Causal Discovery](https://arxiv.org/pdf/2605.27567)
- [Joint Agent Memory and Exploration Learning](https://arxiv.org/pdf/2606.01528)
- [Better Decisions through the Right Causal World Model](https://arxiv.org/pdf/2504.07257)
