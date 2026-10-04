Package this project's literature-review method as a reusable Claude Code skill,
so it can be run on a completely different research problem.

Read first, in this repo:
  documents/literature_review_plan.md          the method as executed, both failed
                                               rules recorded as revisions
  documents/elicit_extraction.md               extraction columns, and what broke
  research_prep/notes/peer_review_mapping.md   section 1: the confirmation-order
                                               defect and its fix
  research_prep/notes/experiment_register.md   how findings become falsifiable
                                               experiments
  research_prep/scripts/*.py                   fetch_references, rank_candidates,
                                               merge_forward, join_elicit
  research_prep/data/seeds.csv, shortlist.csv, cluster_overrides.csv  (shapes, not
                                               content)

The skill takes a research question and produces, in order:
  1. clusters of questions derived from how humans describe the problem
  2. a seed set of trusted papers, with why each was chosen
  3. a citation-graph harvest, backward and forward
  4. a shortlist with provenance for every inclusion
  5. an extraction table with quote-grounded columns
  6. findings mapped to experiments that state what would prove them wrong

Encode these failure modes explicitly; each cost me real time:
  - co-citation ranking collapses when seeds share no references. Check overlap
    before designing the rule
  - a citation graph never finds work that cites nothing you seeded. Direct name
    search is a separate, required step
  - extraction tools mis-key rows (two papers exported under the same venue name
    and one was lost). Join on a filename you chose, never on a title
  - "not found in my corpus" is not "unclaimed in the field". Enforce that wording
  - the pipeline must have a column where a paper can propose something the
    hypotheses do not name, or that answer can never appear
  - a metric that only ever reports zero cannot separate conditions; pick dense
    metrics early

Deliverable: ~/.claude/skills/lit-review/SKILL.md plus scripts/ and references/,
runnable on a fresh problem with no ARC content in it. Paid tools must not sit in
the critical path; degrade gracefully when unavailable.

Test it end to end on an unrelated question before declaring it done, for example
"do sleep-staging models generalise across devices". Report where it needed
human judgement.

Do not include: competition data, Elicit exports, or anything under
documents/arc-prize-2026-arc-agi-3/.