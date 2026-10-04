# Run reports

One JSON file per experiment condition, each a list of per-episode records. These are the
raw measurements behind the verdicts in `../experiment-register.md`: the register says
what each run was for and what it concluded, and these files are what it concluded from.

Naming is `<experiment>_<condition>_<budget>.json`, so `e9_ucb_1000.json` is E9's UCB
bandit condition at a 1,000-action budget. The `c1_arms*.json` files are the C1
collection's run reports; the frames themselves are competition-derived and are not
published.

## Per-episode fields

Identity and integrity: `game`, `episode`, `episode_id`, `initial_hash`, `policy`,
`model`, `guard_fired`, `fast_clears`. The last two are safeguard outputs - flagging
impossible clear lengths and other guard trips.

Outcome: `levels_completed`, `max_level_cleared`, `level_scores`, `level_actions`, `rhae`,
`final_state`.

Dense secondaries: `distinct_frames`, `states_per_100`, `dead_moves`, `measured_dead`,
`deaths`, `repeat_deaths`, `repeat_hazards`, `resets`, `clicks`, `background_clicks`,
`redraws`, `fallbacks`. Condition-specific fields appear only where an experiment defined
them - `arm_pulls` for the bandits, `nav_*` and `path_len_planned` for E6's navigation,
`masked_*` for E5's judge, `fidelity_*` for E6's checks.

The dense metrics are why several null results still said something. A condition that
cleared no more levels while halving the dead-move rate is a finding, and
`levels_completed` alone would have hidden it.

## One field removed

Each record originally carried **`baseline_actions`**: the per-level human action counts
for that game. Those are the denominator of the official score and come from the
competition's own reference data, so they are stripped from these copies - redistributing
competition data is prohibited.

What it costs you: you cannot recompute `rhae` from these files. The computed `rhae` and
`level_scores` are retained, and `levels_completed` - the primary metric behind every
verdict in the register - is unaffected. Every conclusion the register draws can still be
checked against these numbers.
