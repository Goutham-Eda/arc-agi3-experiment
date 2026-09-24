# What runs on what

The useful finding is that most of the open questions on this benchmark are answerable
without a GPU. Pick the cheapest tier that can falsify your hypothesis.

## Tier 0 — any laptop, CPU only

**Cost: nothing. Runtime: under an hour per experiment. Tokens: zero.**

Everything here is a policy, not a model. This is where the controls live, and controls
are what tell you whether a more complex component was ever necessary.

Questions that are fully answerable at Tier 0:

- **Perception of change.** Screen-identity comparison is imperfect: clocks and step
  counters change even when the game world does not, so a dead action can look like it
  changed something. Does masking those cells, or comparing at object level instead of
  exact-hash level, clear more levels?
- **Action generation.** On games needing clicks, does clicking one cell per detected
  object beat clicking a uniformly random coordinate?
- **Within-episode learning.** Does a bandit over action classes, learning which ones
  produce new states, beat uniform choice over the same classes?
- **Memory and planning-to-explore.** Does remembering transitions in a graph and
  navigating back to unexplored frontier states clear more levels than the same local
  rule with no navigation?
- **Value of goal knowledge (upper bound).** Hand-annotate the goal on tune games, give
  it to a planner, and measure the gap. This is a diagnostic, never a verdict — but it
  tells you how much a goal-inference component could possibly be worth before you
  build one.

If a Tier 1 or Tier 2 method does not beat the best Tier 0 policy, it has not earned
its cost. Run Tier 0 first.

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
