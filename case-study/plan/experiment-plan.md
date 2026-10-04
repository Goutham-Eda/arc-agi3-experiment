# Experiment plan

> **STUB — to be filled during Phases 5 & 6.** Do NOT execute any experiment.

## Comparison
- A. Random Agent
- B. Vanilla LLM Agent
- C. Same LLM + Explicit Hypothesis Memory

Keep model / provider / settings identical between **B** and **C** so hypothesis
memory is the primary experimental variable.

## First environment
- [ ] Confirm from current docs whether `ls20` is still an appropriate official
      introductory / local environment (do not assume).

## Metrics (see src/evaluation/metrics.py)
Quantitative: levels completed, environment actions, resets, wins/losses, ARC
scorecard, RHAE / action efficiency, LLM calls, token usage, wall-clock time,
hypotheses generated/confirmed/rejected, repeated/redundant actions.

## Qualitative debugging questions
- [ ] Did the agent identify the controllable object?
- [ ] Did it infer action semantics?
- [ ] Did it distinguish correlation from causal action effects?
- [ ] Did it discover the likely objective?
- [ ] Did it repeat previously failed actions?
- [ ] Did memory prevent repeated mistakes?
- [ ] Did an incorrect hypothesis persist too long?
- [ ] Did it explore when uncertain?
- [ ] Did it exploit knowledge once sufficiently confident?

## Contamination guardrails (Phase 8)
No hidden solutions, no game-specific strategies baked into the agent, no manually
supplied game rules, no prompt-tuning around a specific game's solution. Generic
reasoning stays separate from environment-specific discoveries learned through
interaction.

## Reproducibility (Phase 7)
Record per run: environment/game ID, agent version, model, model parameters,
prompts, random seed (where applicable), full action trajectory, observations,
hypothesis-memory states, scores, timestamps, token/API usage.
