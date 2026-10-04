# Literature Review Plan — ARC-AGI-3 Hypothesis Ranking

- **Drafted:** 2 September 2026 · **Revised:** 5 September 2026
- **Window:** independent work, 2–5 September (before Saturday's live build)
- **Status:** **complete.** 590 candidates screened to 58; extraction run;
  `cluster_final` filled 58/58. What remains is reading and the ranking write-up.
- **Related:** [milestone_brief.md](milestone_brief.md) ·
  [elicit_extraction.md](elicit_extraction.md) · Tab 3 of the project doc
- **Staging folder:** `research_prep/` (moved into `docs/` at Saturday's build)

> **How to read this document.** It keeps its own revision log rather than being
> rewritten clean. Sections 1–5 are the plan as designed; sections 6 onward carry
> dated notes where the data contradicted the plan. That trail is the methods
> record — three rules in this document were overturned by their own output, and a
> review that hides those is not reproducible.

---

## 1. Why this review exists

Tab 3 of the project doc analysed the peer-play transcript and extracted 30
cognitive abstractions, then mapped them onto **48 research topics in five
clusters**. It closed with an explicit instruction:

> "I would stop here before designing hypotheses. The transcript has given you a
> vocabulary of mechanisms; the next stage should be literature review to determine
> which of these mechanisms already have strong formalizations, which overlap, and
> which are genuinely underexplored in ARC-like interactive settings."

That is this review's job. Six working hypotheses (H1–H6) already exist as a draft,
written ahead of the review. **The review does not generate hypotheses — it ranks
them**, and decides which one gets built first on Saturday.

Framing the review this way makes it finite. Without a decision to serve, a
citation-graph review expands indefinitely.

### The question the review must answer

> Of H1–H6, which mechanism is (a) underexplored in *interactive* settings,
> (b) implementable without training, and (c) able to run offline on a Kaggle GPU
> — and therefore the right first modification to the baseline agent?

The three conditions come from hard constraints, not preference:

| Condition | Where it comes from |
| :-- | :-- |
| Underexplored in interactive settings | Tab 3's stated aim; also avoids rebuilding Recuris or AERA |
| No training | Phase 9 of the initialization prompt forbids fine-tuning, RL, and imitation learning for this milestone |
| Runs offline | Kaggle evaluation is sandboxed with no internet — no hosted-API models |

---

## 2. The five clusters

The filing system for everything the review collects. Taken directly from Tab 3.

| | Cluster | Question it answers | Topics |
| :-- | :-- | :-- | :-- |
| **A** | Understanding the unknown world | What exists? What can I influence? What happens when I act? | system identification · causal discovery through interventions · affordance learning · object-centric world models · factored/structured state · relational reasoning · controllability discovery · temporal dynamics learning |
| **B** | Deciding what is probably true | What do I know vs. merely suspect, and how should evidence move that? | Bayesian inference & belief states · hypothesis generation and testing · epistemic uncertainty · program induction · representation revision · inductive biases & priors · compositional generalisation |
| **C** | Discovering useful information | Which action should I take when the *point* of the action is to learn? | active learning · Bayesian experimental design · value of information · intrinsic motivation · curiosity-driven exploration · directed exploration · novelty-based exploration · exploration–exploitation |
| **D** | Turning knowledge into action | Given my current model, what should I actually do? | model-based RL · hierarchical planning · subgoal discovery · receding-horizon/MPC · tree search · heuristic search · width-based planning · POMDPs · resource-constrained planning · risk-sensitive planning · plan repair |
| **E** | Improving over experience | What should remain after this action, episode, level, or game? | working/episodic/semantic memory · consolidation · selective forgetting · meta-learning · continual learning · learning from failure · metacognition · bounded rationality · analogical reasoning · cognitive maps · skill chunking |

Tab 3's priority-10 is the realistic reading scope for four days, not all 48:
active system identification · causal discovery through interventions · active
learning / value of information · object-centric world models · POMDPs &
belief states · model-based planning · hierarchical planning ·
exploration–exploitation · episodic + semantic memory · meta-learning.

---

## 3. The six hypotheses being ranked

Each is an ablation over the *same* base LLM agent, so they stay independently
measurable.

| # | Hypothesis | Cluster | Transcript origin |
| :-- | :-- | :-- | :-- |
| **H1** | Tagging memory as **fact vs. hypothesis** with a confidence level beats a flat observation log | B | "I think…" shifting to "I'm very sure…" |
| **H2** | Labelling each action **epistemic vs. instrumental**, under an exploration budget, improves efficiency | C | touching the plus to learn what it does, later to use it |
| **H3** | Spending the first *k* actions identifying the **controllable object** lowers total actions | A | "what can I control?" as the opening move |
| **H4** | Separating **self-caused from world-caused** change reduces false causal attribution | A | the oscillating plus sign moving on its own |
| **H5** | Pruning actions that **return to visited states** reduces redundancy | C + D | going left "unwraps" a new state; right returns |
| **H6** | Promoting **episodic failures into semantic rules** prevents repeat deaths across resets | E | "I know the flame kills me because I failed" |

**Cluster D is deliberately under-weighted.** Experiment 1 tests whether structured
memory helps, not whether planning helps. Adding a planner would confound the
comparison. D is Experiment 2 territory, and the review reflects that with a
smaller quota (§6).

---

## 4. Seed papers and their coverage

A **seed** is a paper you already trust, used as an entry point into the citation
graph. Six individual seeds — not a cluster, not a grouping. They were chosen for
*coverage*: together they must provide a way into every cluster.

| # | Paper | arXiv | Anchors | Verified |
| :-- | :-- | :-- | :-- | :-- |
| 1 | Explore Before You Solve: The Speed–Depth Trade-off in Epistemic Agents for ARC-AGI-3 (AERA) | `2605.25931` | C + D | abstract read |
| 2 | ARC-AGI-3: A New Challenge for Frontier Agentic Intelligence | `2603.24621` | all | abstract read |
| 3 | Recursive Experiential-Working Memory Evolution for Long-Horizon Agent Harnesses (Recuris) | `2608.24876` | E | abstract read |
| 4 | Meta^n: Recursive Self-Improvement through Emergent Depth | `2608.24735` | E | abstract read |
| 5 | Why LLMs Fail at Causal Discovery and How Interventional Agents Escape | `2605.27567` | A + B | title only |
| 6 | Joint Agent Memory and Exploration Learning via Novelty Signals | `2606.01528` | C + E | title only |

### Why each seed is in the set

- **1 and 2** are the ARC-AGI-3 core. Their reference lists define how the field
  itself sees its ancestry. Heavy overlap between them is expected and is a signal,
  not waste.
- **5 and 6** exist to pull the graph *out* of ARC and into the causal-discovery
  and exploration literatures, where the actual mechanisms live.
- **3 and 4** cover memory — the cluster the hypothesis agent depends on most.

### Two caveats to carry into extraction

**Seeds 3 and 4 are non-interactive.** Recuris is evaluated on tau-bench and
SkillFlow; Meta^n on static answer-refinement including ARC-AGI-2, which is
puzzle-solving rather than an environment you act in. Cluster E is therefore well
anchored for *long-horizon agents* but not for *interactive world discovery*. The
transfer is not automatic — record it as a column value, never assume it.

**Recuris is the nearest prior art to H1 and H6.** It already splits memory into
Experiential (skills) and Working (task progress), with a Meta-Agent making
validation-gated updates localised to whichever memory component caused a failure.
It evolves a skill library rather than training weights, so it passes the
no-training filter. If the review finds H1/H6 are essentially Recuris applied to
ARC, that is a finding — it redirects the build rather than blocking it.

**Hop direction: backward only.** All six seeds are from 2026, two of them eight
days old. Forward citations are near-empty and Research Rabbit will look broken.
All yield is in their reference lists.

> **Revised 3–4 September — the seed set grew to eleven, and backward-only was
> wrong.** Five classical seeds were added to reach the mechanism literature the
> 2026 seeds do not cite: **C-SWM**, **DRQN**, **EpisodicControl**,
> **Plan2Explore**, **WorldModels**, plus **CausalEscape**. Forward hops were then
> run from each, producing eight forward lists (`research_prep/data/forward/`).
>
> **The blind spot this exposed is the most important methodological finding in
> the review.** Every seed either predates ARC-AGI-3 or is contemporary with it,
> and *none of them cite the benchmark*. Thirteen ARC-AGI-3 papers were therefore
> invisible to the entire citation graph — 512 backward candidates and eight
> forward lists surfaced none of them. They were found only by searching the
> benchmark name directly, twice, by hand.
>
> **Rule to carry forward:** a citation-graph review cannot find a literature that
> post-dates its seeds. Always run a direct name search for the benchmark, the
> method, and the competition alongside the graph walk. This is not a failure of
> snowballing; it is a known boundary of it, and the fix is one extra search.

---

## 5. Seed extraction — Semantic Scholar API

### What the script does

```
6 arXiv IDs
   → resolve each to a Semantic Scholar paperId
   → pull each paper's reference list (one hop, backward)
   → dedupe by paperId, counting how many seeds cite each result
   → emit candidates.csv
```

### Endpoints

Base: `https://api.semanticscholar.org/graph/v1`

| Purpose | Call |
| :-- | :-- |
| Resolve an arXiv ID | `/paper/arXiv:2605.25931` |
| Pull references | `/paper/{paperId}/references?fields=title,year,abstract,externalIds,citationCount,authors,venue&limit=100&offset=0` |

Unauthenticated requests share a low rate limit; a free API key raises it. Responses
are paginated, so the script pages with `offset` until exhausted, and sleeps between
calls to stay inside the limit.

### Output — `research_prep/data/candidates.csv`

| Field | Notes |
| :-- | :-- |
| `paper_id` | Semantic Scholar ID, the dedupe key |
| `title`, `year`, `venue`, `authors` | for triage |
| `arxiv_id`, `doi` | for feeding Elicit |
| `abstract` | for the interactivity check |
| `citation_count` | field-level influence |
| **`seed_overlap`** | **how many of the 6 seeds cite this paper — the primary ranking signal** |
| `cited_by_seeds` | which ones, so the reason is auditable |

`seed_overlap` is the column that does the work. A paper cited by four of six seeds
is almost certainly foundational to this problem, and that is a number you can sort
by rather than an impression from a graph view.

### Relationship to Research Rabbit

Same underlying citation data, different interface — Research Rabbit is built on
this class of open citation graph. They are **not** alternatives at the same stage:

| | Script | Research Rabbit |
| :-- | :-- | :-- |
| Speed to first result | ~40 lines to write | paste seeds, instant |
| Output | CSV with exactly the needed columns | visual graph, generic export |
| Reproducible | yes — commit it, re-run, identical | no — a browsing session |
| Co-citation count | quantified and sortable | visible, but eyeballed |
| Serendipity | none | real |

**Use both, in this order:** Research Rabbit first for a visual pass and
serendipity, then the script to produce the reproducible, sortable artifact. If the
week runs tight, Research Rabbit alone is sufficient for discovery; the script's
unique value is the reproducible-search record (a methods-section requirement if
this becomes a paper) and the co-citation ranking.

---

## 6. Selecting the 25 candidates

Roughly 250–350 raw references come out of six seeds; deduping leaves ~200. The
funnel to 25 is explicit so the selection is auditable rather than taste.

> **Revised 2 September, after running the harvest.** The co-citation rule below
> was designed before the data existed. It does not survive contact with it —
> see "What the harvest actually showed". The corrected rule follows.

### What the harvest actually showed

The script resolved all six seeds and returned **165 unique references**. The
overlap structure:

| Seed pair | Shared references |
| :-- | :-- |
| Meta^n × Recuris | 10 |
| AERA × ARC-AGI-3 | 2 |
| AERA × NoveltyMem | 1 |
| **all other pairs (12 of 15)** | **0** |

No paper is cited by three or more seeds, so **Tier 1 is structurally empty** and
the recency waiver attached to it never fires. Only 13 papers reach `overlap == 2`,
and they are dominated by the Meta^n ∩ Recuris intersection — Chain-of-Thought,
ReAct, Reflexion, AlphaEvolve, Promptbreeder, GEPA, Gödel Machines. That is the
self-improving-agent-harness literature, not the mechanism literature of clusters
A–E.

**This is itself a result, not a failure.** Six seeds chosen to span five clusters
draw on six near-disjoint literatures. The mechanisms in Tab 3 have not been
connected to each other in interactive settings by anyone — which is the
"underexplored" signal the review was looking for. It simply arrives as an absence
of overlap rather than as a ranking.

Two secondary observations that affect triage: **58 of 165 references have no
abstract** returned by the API, so a third of the harvest cannot be screened on
abstract alone; and 107 are from the 2020s, so a 2023 recency floor would cut
heavily with no waiver to soften it.

### Corrected rule — rank within each seed, not globally

Because the literatures are disjoint, global ranking has nothing to rank on.
Rank *inside* each seed's reference list instead. This also produces cluster
balance by construction, which is what the quota was for.

**Step 1 — per-seed shortlist.** For each seed, take the top 5 references ranked by
**cluster-keyword density**, filtered by the interactivity check.

> **Revised again, 2 September.** This step originally ranked by `citation_count`.
> That ranks by fame, not relevance — and once five classical seeds were added, the
> deep-learning substrate they cite swamped everything. The shortlist came back
> with *Matplotlib: A 2D Graphics Environment* in cluster A, alongside LSTM (109k
> citations), Attention Is All You Need (190k), and Sutton & Barto (44k). All real
> mechanism papers were pushed out.
>
> Two guards now apply, in step 2 as well as step 1: a paper must hit **at least
> two** cluster keywords (one is noise — "Long Short-Term Memory" matches
> "memory"), and papers above **25,000 citations** are excluded as general
> infrastructure or textbooks rather than mechanisms this review can extract a
> column from. Citations survive only as a tiebreak.

**Step 2 — add the co-cited backbone.** Add the `overlap == 2` papers that map to
H1 or H6. These are the nearest prior art for the memory hypotheses and belong in
the review even though they are not cluster-A–E mechanism papers.

**Step 3 — trim to 25** against the cluster quota below, dropping the weakest
entry from any over-represented cluster.

**Handling the missing abstracts.** For the 58 with no abstract, screen on title
and venue; fetch the abstract from arXiv only if the title suggests a mechanism
paper. Do not discard them silently — an empty abstract field is an API gap, not
evidence about the paper.

### Additional filters

- **Recency floor:** published 2023 or later, *unless* `seed_overlap >= 3`. The
  exception deliberately admits the classics — POMDPs, Simon on satisficing,
  options — which are old, foundational, and will be heavily co-cited.
- **Interactivity check:** does the abstract describe an agent taking actions and
  observing consequences? Static-benchmark papers are recorded but deprioritised.
- **Drop on sight:** survey-only papers with no mechanism, and anything whose
  method requires gradient training (record it, do not read it).

### Cluster quota

Balance matters more than raw score — a review that returns 20 exploration papers
and nothing on memory cannot rank H1–H6.

| Cluster | Quota | Rationale |
| :-- | :-- | :-- |
| A — understanding the world | 6 | H3, H4 both live here |
| B — deciding what is true | 5 | H1 |
| C — discovering information | 6 | H2, H5 |
| D — turning knowledge into action | 3 | deliberately light; Experiment 2 territory |
| E — improving over experience | 5 | H6, and the nearest prior art |
| **Total** | **25** | |

### Stopping rule

Stop at 25, **or earlier** when a hop returns no mechanism not already logged.
Saturation, not exhaustiveness. Four days and 48 candidate topics means the
priority-10 is the real scope.

### What the funnel actually produced — 5 September

The target of 25 was set before the forward hops and before thirteen ARC-AGI-3
papers were discovered. It was widened deliberately, in four steps, each recorded
in the merge output.

| Stage | Count |
| :-- | :-- |
| Backward candidates (11 seeds, one hop) | 512 |
| Forward lists (8 files, raw rows) | 83 |
| **Merged pool, deduped** | **590** |
| **Shortlist** | **58** |
| PDFs obtained | 56 |
| Excluded — unreachable, not screened out | 2 |

**Why 25 became 58.** The quota widened three times, each time for a stated
reason rather than to be thorough: 25 → 48 when the classical seeds landed and
cluster C filled with genuine exploration mechanisms; 48 → 54 when six ARC-AGI-3
papers appeared and would otherwise have displaced *Optimistic Active Exploration*
and *Know When to Explore* exactly as H2 became the most contested hypothesis;
54 → 58 when a seventh ARC-AGI-3 paper arrived and four earlier displacements were
restored by pinning. Every widening is auditable in `cluster_overrides.csv`.

### Final cluster distribution

`cluster_final` was filled for all 58 **after** extraction, not before — reading a
paper's extracted mechanism next to its title turns a blind guess into a judgement.
Seven assignments changed as a direct result (§7).

| Cluster | Final | Original quota | Note |
| :-- | :-- | :-- | :-- |
| A — understanding the world | 9 | 6 | |
| B — deciding what is true | 9 | 5 | absorbed the programmatic-world-model papers |
| C — discovering information | 15 | 6 | the exploration literature is the deepest of the five |
| D — turning knowledge into action | 4 | 3 | still deliberately light |
| E — improving over experience | 21 | 5 | memory is where the recent work is |
| **Total** | **58** | **25** | |

Merge command of record:

```
python research_prep/scripts/merge_forward.py --use-final \
    --quota "A=9,B=9,C=15,D=4,E=21" --target 58
```

Every row now carries a `cluster_final`, which pins it. The shortlist is frozen:
the last merge reported churn **−0 / +0**.

### The clusters validate against the hypotheses

Cross-tabulating `cluster_final` against `maps_to_H` is a check on whether the
filing system means anything. If the clusters were arbitrary, hypotheses would
smear across them evenly.

| | H1 | H2 | H3 | H4 | H5 | H6 |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| **A** | 0 | 0 | **5** | **6** | 0 | 0 |
| **B** | **9** | 5 | 0 | 1 | 0 | 0 |
| **C** | 0 | **9** | 0 | 1 | **6** | 0 |
| **D** | 0 | 0 | 1 | 0 | 0 | 0 |
| **E** | 5 | 0 | 0 | 0 | 1 | **18** |

They do not smear. A owns H3/H4, B owns H1, C owns H2/H5, E owns H6 — which is
what Tab 3's taxonomy predicted, arrived at independently through triage.

It also shows where the review is thin: **H3 has 6 papers and H5 has 7**, and they
are the two hypotheses no ARC-AGI-3 paper has claimed. That coincidence is the
most actionable thing in the table.

---

## 7. The Elicit extraction table

> **Revised 4–5 September.** Elicit's **Extract Data** workflow requires Pro
> ($49/mo) and takes uploaded PDFs, not a title list — so the pipeline is: fetch
> PDFs → upload → define columns → export → join. Full operating spec in
> [elicit_extraction.md](elicit_extraction.md); this section records the outcome.
>
> Two columns from the original design were dropped. *Cluster (A–E)* was removed
> because assigning it is our judgement, not the paper's — it is now filled by hand
> from the extraction. *Requires training?* and *Code available?* collapsed into
> the model/compute and limitations columns, which carry the same information with
> supporting quotes attached.

### Getting papers in

Elicit's Extract Data takes uploaded PDFs, capped at **50 per table**, so 56 PDFs
were split by cluster into two tables (26 rows / 25 PDFs, and 32 rows / 31 PDFs).
PDF acquisition is scripted and resumable: `research_prep/scripts/fetch_pdfs.py`
resolves arXiv ID → arXiv DOI → Semantic Scholar open-access → arXiv title search
at a 0.92 match threshold, validates the `%PDF` magic bytes, and reports anything
it cannot reach rather than skipping it silently.

### The nine columns actually used

| # | Column | Why it earns a column |
| :-- | :-- | :-- |
| 1 | Mechanism | what the agent *does*, not what it claims |
| 2 | Agent state | which data structure holds what the agent knows |
| 3 | Update trigger | what event changes the model or memory |
| 4 | Model and compute | model, size, hosted vs local, cost |
| 5 | Evaluation | benchmark, domain, whether grid-world or ARC-like |
| 6 | Headline result | the number, quoted, plus the baseline it beats |
| **7** | **Action efficiency** | **who else competes on RHAE, and under which protocol** |
| 8 | Stated limitations | what the authors say fails |
| **9** | **Frontier-model dependence** | **would this survive a ≤10B open-weight model offline** |

Every question carries an explicit escape hatch — `"not reported"`,
`"no evidence"`, `"none - <type>"`. That is load-bearing: without it the model
fills gaps with plausible inference, and column 9 becomes confident fiction.
Both tables used `Answer structure: Any` for all nine; a Yes/No/Maybe structure on
column 9 would have destroyed its escape hatch.

### Extraction quality — measured, not assumed

| | Table 1 | Table 2 |
| :-- | :-- | :-- |
| Rows | 25 | 31 |
| Columns answered | 9/9 on every row | 9/9 on every row |
| Rows degraded to abstract-only | 1 | 0 |
| `"not reported"` on action efficiency | 21/25 | 23/31 |
| `"no evidence"` on frontier dependence | 24/25 | 29/31 |

The high escape-hatch rate is the *good* outcome. It means the extraction reported
absence rather than inventing presence — the failure mode we were watching for.

### Joining back — and why title matching was not enough

`research_prep/scripts/join_elicit.py` merges the exports onto the shortlist.

It keys on **filename → `fetch_manifest.csv` → shortlist title** first, falling
back to exact title, then fuzzy above 0.92. Filename is authoritative because *we*
chose it at download time; it is the one key Elicit cannot corrupt.

That mattered immediately. Elicit re-derives titles from the PDF and read the
**venue** as the title for two papers — *LLM-Based World Models* and *Cognitive
Architectures for Language Agents* both became "Transactions on Machine Learning",
collided on one key, and one row was silently lost. Title matching gave 21/25 with
a destroyed row; filename matching gives **56/56, zero unused**.

### Filling `cluster_final` from the extraction

Deliberately done *after* extraction. Seven assignments changed once the mechanism
was visible next to the title:

| Move | Paper | Why |
| :-- | :-- | :-- |
| C → E | SAGE | the novelty score is the means; the mechanism routes facts to ADD/NOOP/UPDATE — memory consolidation, not exploration |
| A → B | CoEx | the contribution is the Adaptive Belief State maintained by verification |
| A → D | ObjectZero | object slots in service of MCTS planning |
| A → D | What Drives Success (JEPA) | CEM latent-space planning is the subject |
| B → E | CoALA, Memento 2, PREMem | all three are memory architectures |

Two of those moves took cluster D from 1 paper to 4, fixing a structural thinness
that a pre-extraction pass would have preserved.

---

## 8. Final outcome

### Artefacts produced (all present as of 5 September)

| File | What it is |
| :-- | :-- |
| `data/candidates.csv` | 512 backward references, 11 seeds, with `seed_overlap` |
| `data/forward/*.csv` | 8 forward lists, hand-triaged |
| `data/candidates_merged.csv` | the deduped 590-paper pool |
| `data/shortlist.csv` | the 58, regenerated by `merge_forward.py` |
| `data/cluster_overrides.csv` | every hand judgement, keyed by normalised title — survives regeneration |
| `data/shortlist_papers/` | 56 PDFs + `fetch_manifest.csv` |
| **`data/shortlist_extracted.csv`** | **58 rows × 57 columns — the shortlist joined to the extraction** |
| `data/implementation_refs.csv` | 3 codebases worth reading before writing any agent |
| `scripts/` | `merge_forward.py`, `fetch_pdfs.py`, `join_elicit.py` |

`shortlist_extracted.csv` is the reading artefact. `shortlist.csv` remains the
index and is still owned by `merge_forward.py` — extraction columns are never
written to it, because the next merge would drop them.

### Still to produce

`research_prep/notes/literature_review.md`, promoted to `docs/literature_review.md`
at the build. The extraction is the input to it, not a substitute for it:

1. **A ranked build order for H1–H6**, each with the evidence behind its rank.
2. **Two or three named mechanisms** that are simultaneously underexplored in
   interactive settings, trainless, and offline-capable.
3. **An explicit prior-art note** — what AERA, Tycho, and the executable-world-model
   line already do, so the build does not rebuild any of them by accident.
4. **A "not this milestone" list** — interesting but requires training, a planner,
   or online model access.

### What the review has already settled

**The efficiency angle is not novel, but it is not closed either.** The headline
figures and the protocol-matched figures differ by an order of magnitude:

| Source | Number | Regime |
| :-- | :-- | :-- |
| Tycho | 100.00 RHAE, 183 levels | Opus 5 / GPT-5.6 Sol |
| Prime Agent | 95.5% | best@1 |
| PRO-LONG | 97.4% | best@2, $1,750 |
| OPINE-World | 78.4% | 25 games, no per-game training |
| Rodionov ablation | **34.16 – 74.78** | **main study, all variants** |
| DreamTeam | **38.4%** | **official protocol, 2 runs** |

Rodionov, who owns the reference architecture, states the limit himself: because
gpt-5.6-sol postdates the games, his results *"indicate public-set saturation
only."* **Never compare two ARC-AGI-3 numbers without naming the protocol.**

**The local-weights gap is real but narrower than assumed.** All 56 rows confirm
every published *ARC-AGI-3* result runs a hosted frontier model. But **13 of 56
shortlisted papers ran open-weight models** — SAGE across seven backbones from
1B–7B, Agentic Episodic Control at Qwen2.5 7B vs 32B on grid worlds, PREMem across
a 3B–72B ladder, Continual Harness LoRA-tuning Gemma-4 locally. The honest gap is
therefore: *the capability axis has been plotted downward in memory, exploration
and episodic-control settings, but never on ARC-AGI-3.* That is a better position
than the original claim — there is method to borrow rather than invent.

**One design lesson already extractable.** SAGE survives at 1B because its gate
resolves in closed form without an LLM call. Pushing decisions out of the model
into cheap deterministic components is what makes small weights survivable.

### What it explicitly does not do

It does not generate new hypotheses, design the agent, or touch the ARC interface.
Phase 1 — verifying the real toolkit API — is reserved for the live build.

---

## 9. Schedule

| Day | Planned | Actual |
| :-- | :-- | :-- |
| **Tue 2 Sep** | Kaggle account + phone verification; confirm six seed IDs | seeds confirmed; **Kaggle verification not done** |
| **Wed 3 Sep** | Read AERA in full; Research Rabbit backward pass | backward hop run; seed set grown to 11 |
| **Thu 4 Sep** | Run extraction script; reach 25; start Elicit | forward hops, 6 ARC-AGI-3 papers found, shortlist to 54, PDFs fetched |
| **Fri 5 Sep** | Finish extraction, rank H1–H6, write the review | **extraction complete, `cluster_final` 58/58, join done. Ranking write-up not started** |

The review ran roughly one day behind its plan and one scope-step wider, both for
the same reason: the ARC-AGI-3 literature discovered on Thursday did not exist in
the citation graph and had to be found, verified, and triaged by hand.

Filler task, still not done: add an efficiency-ratio field to
`src/evaluation/metrics.py`. It needs only a configurable reference action count,
not the real interface, and it gets the report schema right before real numbers
land in it.

---

## 10. Open items

**Closed since drafting**

- ~~`research_prep/` folder name~~ — confirmed and in use.
- ~~Seeds 5 and 6 unread~~ — both resolved; seed set expanded to 11.
- ~~Which Elicit workflow~~ — Extract Data on Pro; see
  [elicit_extraction.md](elicit_extraction.md).
- ~~`cluster_final` unfilled~~ — 58/58, filled from the extraction.

**Still open**

- **Kaggle account + phone verification.** Gates GPU access, still not done, and
  it is the only item here with an external dependency. Do it first.
- **Model decision — hosted API vs. local weights.** The review has narrowed it:
  Kaggle's sandbox forces local weights, and 13 shortlisted papers show small
  open-weight models working in adjacent settings. It does not name the model.
- **The ranking write-up.** The deliverable this whole review exists to produce.
- **Two papers unreachable** — *Comparative Study on Curiosity* (IEEE paywall) and
  *Interaction-Based Disentanglement* (no DOI). Excluded by decision, not by
  screening; coverage is 56/58 (96.6%) and the write-up must say so.
- **Reading.** `arc-3-agents-baseline1` code then paper; then Tycho, Sensi,
  OPINE-World; then PRO-LONG for context management.
- **H3 and H5 are the thin ones** — 6 and 7 papers, and the two hypotheses no
  ARC-AGI-3 paper has claimed. Decide whether that is opportunity or absence of
  evidence before betting the build on either.
