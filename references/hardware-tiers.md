# What runs on what

The useful finding is that most of the open questions on this benchmark are answerable
without a GPU. Pick the cheapest tier that can falsify your hypothesis.

## Tier 0 — any laptop, CPU only

**Cost: nothing. Runtime: under an hour per experiment. Tokens: zero.**

Everything here is a policy, not a model. This is where the controls live, and controls
are what tell you whether a more complex component was ever necessary.

Five of these questions have since been answered by running them. They are recorded
here as results rather than prompts, because the most expensive thing a new
collaborator can do is re-run a settled experiment.

**Answered.**

- **Perception of change.** Screen-identity comparison is imperfect: clocks and step
  counters change even when the game world does not, so a dead action can look like it
  changed something. Masking those cells **helped, narrowly** — the gain was carried
  almost entirely by one game, and is reported as "narrow", not as an effect. The
  masked judge was kept anyway, as the common measurement judge for everything after
  it. Infrastructure value, not a finding.
- **Action generation.** On games needing clicks, clicking one cell per detected object
  rather than a uniformly random coordinate was **falsified on levels cleared**, even
  though it improved the efficiency score. The capability was real and the primary
  metric still said no. See `preregistration.md` on declaring the primary first.
- **Within-episode learning.** A bandit over action classes, learning which classes
  produce new states, **beat uniform choice over the same classes** — 217 clears
  against 171 on 40 fresh seeds, surviving the concentration rule with six games
  improving. This is the **only broad positive result** in the line of work, and it is
  now the policy to beat.
- **Memory and planning-to-explore.** Remembering transitions in a graph and navigating
  back to unexplored frontier states **added little** over the same local rule with no
  navigation. Separately, a memory of previously failed trajectories improved
  *exploration* while leaving levels cleared level with random: **memory helped search,
  not understanding.**
- **Added prompt text.** Telling a frozen model what each control does, and asking it
  to label each move by intent, both **increased wasted moves**. Evidence about those
  descriptions, not proof that controllability knowledge is useless.

**Still open, with a caveat earned the hard way.**

- **Value of goal knowledge (upper bound).** Hand-annotate the goal on tune games, give
  it to a planner, measure the gap. Attractive on paper, and it was preregistered here
  — then **deferred on feasibility** before running: tune-set clears are too rare for
  the gap to be measurable, and the game sources are obfuscated, so writing an honest
  goal predicate is harder than it sounds. If you attempt it, settle the predicate form
  and the success bar first. Preregistering an experiment and then deferring it with a
  recorded reason is a legitimate outcome, not a failure.
- **A learned ranker over collected transitions**, and **deliberate investigation** (an
  explicit inspect → hypothesise → test loop) are the open questions the bandit's
  weakness points at: it cannot see the value of moves that set something up without
  revealing anything new.

If a Tier 1 or Tier 2 method does not beat the best Tier 0 policy, it has not earned
its cost. Run Tier 0 first — and note that the bar moved: the best Tier 0 policy is no
longer plain random.

## Tier 1 — free cloud GPU (Colab T4, Kaggle weekly quota)

**Cost: free but quota-limited. Expect hours, not minutes.**

Small open-weight models, served locally. Realistic questions:

- Does a frozen small model choosing each move from a text rendering of the screen beat
  random? (In this project's runs, it did not — both a 4B-class and a 31B-class model
  cleared zero levels where random cleared one in eighty.)
- Does the same frozen model play better from an **image** of the screen than from a
  text grid? This isolates interface from reasoning and is a genuinely open question.
- Does added prompt text help or hurt? There is evidence it can hurt: telling the model
  what each control does, and asking it to label moves by intent, both *increased*
  wasted moves.

Verify your serving stack supports what you need before you plan around it — image
input on a given model and server version is an empirical question, not a spec sheet
question.

## Tier 2 — rented or granted GPU

**Cost: real. Tens of GPU-hours, tens of millions of tokens.**

Reasoning harnesses around a mid-size open-weight model: an explicit loop of inspect →
hypothesise → test → update the world model → plan, with a structured interface to the
game rather than raw pixels.

Do not start here. Start here only when a Tier 0 control battery has established what
the simple methods cannot do, so that a Tier 2 result means something specific.

Compute grants exist for this benchmark (the prize's research-partner programme, and
several GPU providers). They take weeks to come through — apply while you run Tier 0.

## Choosing

| You want to test | Tier | Why |
| :-- | :-- | :-- |
| Whether a capability is *necessary* | 0 | A control that beats the complex method kills it cheaply |
| Whether a *model* can do something at all | 1 | Cheapest honest test of a frozen model |
| Whether *deliberate reasoning* beats search | 2 | Only meaningful once 0 and 1 are known |
