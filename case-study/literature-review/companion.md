# reproducible-lit-review

- **Repo:** [github.com/Goutham-Eda/reproducible-lit-review](https://github.com/Goutham-Eda/reproducible-lit-review) · MIT · 26 files
- **Installed at:** `~/.claude/skills/lit-review` — a clone of the repo, so edits there are commits

---

## The one-sentence version

> A literature review is finite only when it serves a decision. This skill takes a
> research question, forces you to name the decision first, then walks six stages
> that end in experiments with falsifiers rather than a pile of PDFs — and it
> encodes the ways that process silently fails as mechanical guards rather than as
> advice.

---

## Why it exists

Most review tooling optimises for finding more papers. The failures that actually
cost time are structural — and they share one shape: **a channel that cannot
carry the answer.**

| The failure | Why you can't see it from inside |
| :-- | :-- |
| Ranking rule has nothing to rank on | No tier to rank in |
| Citation graph can't reach a literature | No edge to traverse |
| Extraction tool mis-keys a row | No key to join on |
| No column for an unanticipated answer | Nowhere to write it |
| Metric reports zero for every condition | No range to move in |

Five of the six failure modes are that shape. After the fact you cannot
distinguish "no signal" from "nowhere to put it" — which is why each one is a
check that runs **before** the stage it protects.

---

## The six stages

```
1 clusters      how humans describe the problem   ->  clusters.csv
2 seeds         papers you already trust          ->  seeds.csv
3 harvest       citation graph, both directions   ->  candidates.csv + named.csv + overlap.md
4 shortlist     screened, with provenance         ->  shortlist.csv + funnel.md
5 extraction    quote-grounded columns            ->  shortlist_extracted.csv
6 experiments   findings that can be wrong        ->  experiments.md
```

Each stage writes a file the next one reads, so the whole review is a folder
someone else can re-run. **That file contract is the reproducibility claim.**

**Stage 1 is the irreducibly human one.** Clusters come from a practitioner
describing the problem in their own words — a transcript, a protocol, an expert's
tour of their data — not from a published taxonomy (organised for teaching) and
not from your own hypotheses (then the filing system agrees with you by
construction). Pull out the recurring *questions*, not topics: a question has an
answer, so a paper either answers it or doesn't, and that is screenable.

**Stage 6 is also human.** No script can pick a falsifier.

---

## The guards, concretely

| Failure | The guard in code |
| :-- | :-- |
| Co-citation ranking collapses when seeds share no references | `harvest.py` writes `overlap.md` — the pairwise matrix, and which ranking rule is available — before you write one |
| A graph never finds work that cites nothing you seeded | `rank.py` exits non-zero if `named.csv` is absent; `--allow-graph-only` overrides and records the gap in `funnel.md` |
| Extraction tools mis-key rows, silently | `fetch_pdfs.py` writes a manifest keyed on the filename *you* chose; `table.py join` uses it first, then exact title, then fuzzy ≥ 0.92, reporting every fuzzy and unmatched row |
| "Not found in my corpus" written up as "unclaimed in the field" | `table.py check` greps every cell for *unclaimed*, *nobody has*, *first to*, *no prior work* |
| No column for an answer you didn't anticipate | `table.py check` fails if `suggests_new_question` is missing — and fails again if it exists and is empty, since an empty column is the same defect wearing a header |
| A metric that only ever reports zero | The register requires a floor check on a random/trivial policy before a metric becomes primary |

---

## The scripts

Stdlib-only Python 3.9+, no install step. OpenAlex is primary (no key, both
citation directions); arXiv is the recency channel, because it carries preprints
within a day.

| Script | Job |
| :-- | :-- |
| `oa.py` | OpenAlex + arXiv client, disk cache, backoff, and the pipeline's single paper schema |
| `harvest.py` | Backward + forward hops, `seed_overlap`, the overlap diagnostic |
| `name_search.py` | Direct name search — a required separate step, because the separation is the point |
| `rank.py` | The funnel → `shortlist.csv` + `funnel.md` |
| `fetch_pdfs.py` | PDFs + `manifest.csv` (the join key) |
| `table.py` | `skeleton` \| `join` \| `check` |

The funnel's rules, each with a scar behind it:

- **≥ 2 cluster-keyword hits** — one is noise; "Long Short-Term Memory" matches a
  memory cluster.
- **A fame ceiling** — above ~25k citations a paper is infrastructure or a
  textbook, not a row you extract a mechanism from.
- **A recency floor**, waived by co-citation.
- **Per-seed depth**, so one deep literature can't swamp the rest.
- **Then a cluster quota.**

Never rank on citation count — done for real, it put a plotting library at the
top of a mechanism cluster and pushed every mechanism paper out. Hand judgement
in `overrides.csv` bypasses the guards and survives every re-run.

---

## Two design commitments

**Escape hatches are load-bearing.** Every extraction column carries an explicit
permitted non-answer — `"not reported"`, `"no evidence"`, `"none - <type>"` —
written into the question itself. Without it, gaps get filled with plausible
inference and the column answering your actual question becomes confident
fiction. A high escape-hatch rate is the *good* outcome.

**Nothing paid sits in the critical path.** Every stage degrades: the extraction
table is hand-fillable from abstracts already in `shortlist.csv`. The review gets
thinner; it does not stop.

---

## What the validation run showed

Tested end to end on an unrelated question — *do sleep-staging models generalise
across devices?* 6 seeds, 425 graph candidates + 142 from name search, 535 pooled
→ 38 shortlisted, extraction filled for 14.

- **13 of 38** shortlisted papers were reachable only by name search — a third of
  the shortlist, invisible to both graph directions, including the two that most
  directly answered the question.
- **The consumer-device validation literature and the deep-learning staging
  literature share zero citations.** That fell out of the overlap matrix in stage
  3, before a paper was read — and it is the answer to the question.
- **10 of 14 rows answered "not reported"** on the one metric the decision
  needed. The escape hatch is the only reason that finding was visible.
- **Join tested both ways:** title-only matched 12/14 with two rows collided;
  filename-via-manifest matched 14/14.
- **PDF coverage was 28.6%**, against 96.6% on an arXiv-heavy shortlist —
  clinical publishers 403 any non-browser client. Reported, not hidden.

It also found a defect in its own ranking: best-cluster-wins starved the "does it
transfer" cluster to 2 of 8 and called it a thin literature. It wasn't — any EEG
abstract is dense in EEG words, so the sparser-vocabulary cluster loses. Papers
now count toward any cluster they hit. **A keyword-derived "thin literature" is a
claim about your keyword lists until you've checked it.**

---

## Second run — the cross-domain question

Run on the cross-domain question from `session_info` — Gibson's affordances,
Gopnik/Spelke, Ashby's requisite variety, Powers' perceptual control, under that
task's stopping rule of 15–20 sources, reviews and chapters only. It surfaced two
more defects, both now fixed and re-run:

- **Forward hops sorted by publication date**, which for a 1979 classic returns
  last month's most obscure applications — football tactics, dating-app
  engagement — rather than the influential citing work. Now sorted by citations,
  with `--forward-sort` to override.
- **No document-type filter**, while that stopping rule admits only reviews and
  handbook chapters. The first run returned zero of either in 18 rows. OpenAlex
  has a `type` field, so `rank.py --types review,book-chapter,book` now screens on
  it — **362 `article` rows excluded** on the re-run — and `funnel.md` reports how
  many rows carry no type and so escaped the screen.

A third, milder finding: for pre-1990 books the **backward channel is dead**.
Gibson returned 0 references, Ashby 3, Powers 6, because OpenAlex holds no
reference lists for books — the exact mirror of a corpus whose seeds are too new.
PDF acquisition managed **1 of 16**, since books and chapters have no open PDF.

The substantive result was a defensible negative: cluster D's *review* literature
turned out to be Information Systems affordance theory, not ecological
psychology, so no source in that corpus engages Gibson's premise as it bears on
H3. Stated as "not found in this corpus, which under-samples ecological
psychology" — which is the wording the skill enforces.

---

## What it does not do

It is **not PRISMA**, and says so: the method is citation-graph snowballing plus a
direct name search plus hand triage. It does not read the papers, derive your
clusters, or choose your falsifiers.

[`references/worked-example.md`](https://github.com/Goutham-Eda/reproducible-lit-review/blob/main/references/worked-example.md)
closes with the ten points where the real run needed human judgement — rejecting
four keyword-passing papers that were about sleep but not about staging models;
marking the most co-cited item in the pool as a dataset with no mechanism to
extract; telling "thin literature" apart from "starved by my own scoring rule".
That list is the honest scope of the tooling.
