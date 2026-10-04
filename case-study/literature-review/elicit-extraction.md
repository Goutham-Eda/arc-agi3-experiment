# Elicit Extraction Spec — ARC-AGI-3 Shortlist

- **Drafted:** 4 September 2026 · **Revised:** 5 September 2026, after seven
  ARC-AGI-3 papers were added and four displaced papers restored
- **Input:** `research_prep/data/shortlist_papers/` (56 PDFs) indexed by
  `research_prep/data/shortlist.csv` (58 unique papers)
- **Related:** [literature_review_plan.md](literature_review_plan.md) ·
  [milestone_brief.md](milestone_brief.md)
- **Output:** two Elicit tables, exported to CSV, joined back onto `shortlist.csv`

---

## 1. Which workflow

**Extract Data.** Not Research Report, not Systematic Review, not Research Agent.

| workflow | why not |
| :-- | :-- |
| Research Report | Search-based only. It finds its own papers and would ignore the shortlist. |
| Systematic Review | Its value is the screening funnel — thousands down to an included set, PRISMA-documented. We already screened 590 to 58 by hand. |
| Research Agent | Caps at 20 uploads and is built for open-ended questions across web sources. It synthesises; it does not tabulate. |
| **Extract Data** | **Builds a table from your own PDFs. Up to 50 papers per table, custom columns. This is the one.** |

**Requires Elicit Pro** ($49/month). Extract Data and Systematic Review are both
gated above the free tier; on Basic you cannot bring your own papers and build a
table over them. One billing cycle covers the milestone window.

A note on honesty: our method was citation-graph snowballing from 11 seeds plus
hand triage. That is a legitimate method but it is **not PRISMA**. Running the
Systematic Review workflow would dress it as something it was not. Describe the
actual method in the write-up.

---

## 2. What to upload

56 PDFs against a 50-per-table cap, so the split is now load-bearing rather than
merely tidy. Split by cluster to keep each table thematically coherent:

| table | clusters | rows | PDFs in hand |
| :-- | :-- | :-- | :-- |
| 1 | A (13) + B (12) + D (1) | 26 | 25 |
| 2 | C (16) + E (16) | 32 | 31 |

Counts are by `cluster_guess`, which is what exists until `cluster_final` is
filled. Both tables sit under the 50-paper cap, but table 2 has less headroom
than before — if the shortlist grows again, split C and E rather than widening.

Total upload is ~311 MB, so upload per table rather than all at once.

**Upload only the top level of `shortlist_papers/`.** The `_not_uploaded/`
subfolder holds one deliberately excluded PDF — SIMA 2, hand-rejected via
`cluster_final`. Everything else in the top level is in the shortlist, so the
folder and the CSV now agree exactly.

### Two papers are excluded — decided, not pending

**Decision, 5 September 2026: do not chase these. Run the tables at 25 and 31 and
declare the gap.** Neither is rated `strong`, and the acquisition cost exceeded
what either would add.

| paper | cluster | verdict | why unavailable |
| :-- | :-- | :-- | :-- |
| Comparative Study on Curiosity with Attention, Memory and Empowerment | C | keep | IEEE `10.1109/ICARSC65809.2025.10970179`, paywalled — needs institutional access |
| Interaction-Based Disentanglement of Entities for Object-Centric World Models | A | keep | no DOI in the export, no arXiv title match above the 0.92 threshold |

**This must appear in the write-up.** Coverage is **56 of 58 shortlisted papers
(96.6%)**, and both exclusions are acquisition failures, not screening decisions
— that distinction is the point of stating it. Do not describe the review as
covering the shortlist without the caveat; a reader who later finds either paper
should find it already accounted for.

`fetch_manifest.csv` records both as `no-source`, so the gap stays visible in the
data as well as in prose. If either becomes reachable later it is one Elicit row
added to an existing table, not a re-run.

*From episodes to concepts and back* was a third entry here and is now resolved —
bioRxiv served it on the 4 Sept re-run after 429-ing every earlier attempt, which
is why this is two and not three.

---

## 3. The columns

Extract Data is not one prompt — you define a question per column. Paste these
one at a time. Nine columns; Pro allows 20 per table.

```
1. Mechanism
   What specific mechanism does this paper introduce? One sentence, naming
   the components. If it introduces none (benchmark, survey, environment),
   answer "none - <type>".

2. Agent state
   Concretely, what data structure holds what the agent knows? (neural latent,
   Python program, natural-language rule list, graph, episodic buffer). Quote
   the paper's own wording. "n/a" if not an agent paper.

3. Update trigger
   What event causes the agent's model or memory to change? (every step, end
   of episode, prediction error, explicit contradiction, external signal).

4. Model and compute
   Which models were used, with size; hosted API or local weights; any
   reported cost, token, or latency figures. Quote exact numbers.

5. Evaluation
   What was it evaluated on? Name benchmarks and domains, number of tasks or
   levels, and state whether any are grid-world or ARC-like.

6. Headline result
   The main quantitative result with its metric and number, quoted, plus the
   baseline it beats. "no quantitative result" if absent.

7. Action efficiency
   Does the paper report actions, steps, or samples needed (RHAE, sample
   efficiency, action count, episode length)? Quote the exact figure.
   Answer "not reported" if absent.

8. Stated limitations
   What do the authors say fails or does not work? Quote. "none stated" if
   the paper claims none.

9. Frontier-model dependence
   Based only on evidence in the paper: would this still work with a small
   open-weight model (<=10B) running offline? Does it rely on strong
   instruction-following, long context, or code generation? Quote supporting
   text. Answer "no evidence" if the paper says nothing.
```

### Why 7 and 9 are the ones that matter

Columns 1–6 and 8 produce the review table, which is a deliverable. Columns 7
and 9 answer the project's actual open question.

**Column 7** tells you who else is competing on RHAE, and — more importantly —
**under which protocol**. The published numbers do not agree, and the spread is
not noise:

| source | number | regime |
| :-- | :-- | :-- |
| Tycho (2607.28287) | 100.00 RHAE, all 183 levels | Opus 5 / GPT-5.6 Sol |
| Prime Agent (2608.23552) | 95.5% RHAE | best@1 |
| PRO-LONG (2607.20064) | 97.4% | best@2, Fable 5, $1,750 |
| OPINE-World (2607.01531) | 78.4 action-efficiency, 20/25 games | no per-game training |
| Rodionov ablation (2607.15439) | ~99% human-relative action efficiency; textual variant 41% fewer actions than human | gpt-5.6-sol at xhigh / max |
| **DreamTeam (2605.09650)** | **36% → 38.4%** | **official scoring protocol, protocol-matched, 2 runs** |

That last row is an order of magnitude below the rest. Until someone reconciles
it, "RHAE is saturated" is a claim about the loose regime only — quote the
protocol every time, and never compare two of these numbers directly. Extracting
this column across all 58 papers is how that gets settled by evidence rather than
by whichever abstract was read most recently.

Rodionov, who owns the reference architecture, states the limit himself: because
gpt-5.6-sol postdates the games and held-out performance is untested, his results
*"indicate public-set saturation only."* Treat every number in that table as a
public-set number unless the paper says otherwise.

**Column 9** is the research question turned into an extraction. Every published
ARC-AGI-3 result runs a hosted frontier model — confirmed across all 56 rows,
including Prime Agent, whose open-weight models (Kimi K3, DeepSeek V4 Pro,
GLM 5.3) appear only in the nanoGPT speedrun, not in its ARC-AGI-3 agent.
Kaggle's sandbox has no internet, so the project runs local weights.

**Result of the extraction — an earlier claim here was too strong.** This spec
previously said nobody has plotted the capability axis downward. That is true
*on ARC-AGI-3* and false in general: **13 of 56 shortlisted papers ran
open-weight models**, several of them small.

| paper | cluster | what it ran | why it matters |
| :-- | :-- | :-- | :-- |
| SAGE | C | 7 open-weight backbones, 1B–7B | wins on all 7; its novelty gate resolves ADD/NOOP **in closed form, without LLM calls** |
| Agentic Episodic Control | E | Qwen2.5 7B vs 32B on grid worlds | closest analogue we have — 7B holds up, degrading most on the hardest task |
| PREMem | B | Qwen2.5 3B/14B/72B, Gemma3 4B/12B/27B | a full size ladder on one method |
| Continual Harness | E | Gemma-4 E2B/E4B/26B/31B, LoRA-tuned locally | frontier teacher relabels open-weight rollouts |
| ReflAct | B | Llama-3.1 8B vs 70B vs GPT-4o | same method across three capability points |
| HEMA | E | Mistral-7B, Llama-3-8B, Phi-3-Mini | all fit on a single GPU |

This is better news than the original claim. The gap is narrower and far more
precisely stated — *the capability axis has been plotted downward in memory,
exploration and episodic-control settings, but never on ARC-AGI-3* — and there
is existing method to borrow rather than invent.

---

## 4. After extraction

1. **Export to CSV** (Plus and above) and join onto `shortlist.csv` by title.
2. **Fill `cluster_final`** while reading the output. Do not fill it first —
   with the extracted mechanism visible next to the title, the cluster letter is
   obvious and fast. That turns 52 blind judgements into informed ones (6 of the 58
   are already set, four of them pins that force cluster membership).
3. **Verify the `strong` rows by hand.** Elicit grounds claims in quotes, but
   the extraction is load-bearing for the review, and two of three `strong`
   ratings in the ad-hoc check did not survive contact with their abstract.
   Spot-check the quotes on those rows specifically.
4. **Watch column 9 for over-claiming.** "Would this work with a small model" is
   a question papers do not ask themselves, so the honest answer is usually
   "no evidence". If Elicit returns confident yes/no answers across the board,
   it is inferring rather than extracting — re-read the quotes before trusting
   it.

---

## 5. This is a deliverable, not a dependency

Nothing in the build waits on this table. A short list of papers drives the
implementation — `arc-3-agents-baseline1` (code first, then paper), Tycho, Sensi,
and now PRO-LONG and OPINE-World — and those are read by hand either way. See
`research_prep/data/implementation_refs.csv`.

If the $49 is unwelcome, the fallback is: read the ones that matter, hand-fill a
thinner table from abstracts for the rest. The review gets weaker; the build
does not.
