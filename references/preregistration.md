# Writing the preregistration

Twelve fields. Fill them in `templates/prereg.md` before you run anything. The
preregistration is committed before the first real run and is not edited afterwards —
changes become dated amendments.

## The fields, and what makes each one honest

**1. Research question.** One sentence, answerable yes or no. "Does X clear more levels
than Y at a matched action budget?" — not "How does X perform?"

**2. Exact capability being isolated.** Name one of: exploration, learning, memory,
causal or world modelling, goal inference, action selection, planning, perception,
interface. If you cannot pick one, your experiment changes more than one variable.

**3. Treatment and matched control.** The control must differ from the treatment in
exactly the thing named in field 2. The commonest failure is a control that also gets
fewer actions — then you have measured budget, not capability. If your treatment spends
k actions on a probe, your control gets k extra actions too.

**4. Information available to each condition.** Write down literally what each side can
see. Differences you did not intend to create usually show up here.

**5. Primary and secondary metrics.** Primary is normally levels cleared. Secondary are
the dense metrics from `setup.md`. Declare them now, so you cannot go hunting after the
run for the metric that happens to look good.

**6. Action budget, seed plan, and game split.** Budgets matched across conditions.
Seeds fixed and recorded. State which games are tune and which are held-out, and use a
fresh seed block if these games have been used before.

**7. Predeclared success criterion.** A number, decided now. "Beats the control on
levels cleared across held-out games, outside the control's seed range."

**8. Falsifier and stopping rule.** What result makes you stop, and at which stage. A
tune-stage stopping rule is the most valuable thing in this document — it is what lets
you abandon an idea for the cost of a tune run instead of a full one.

**9. Expected compute, token, and implementation cost.** Written before, so that "this
turned out expensive" is a recorded surprise rather than a quiet overrun.

**10. Main confounds or failure modes.** Include at least one way the *scaffold* could
fail while the hypothesis is fine. Then say how the probe run would detect it.

**11. What a positive, negative, or mixed result would mean.** All three. If a negative
result means nothing to you, the experiment is not worth running.

**12. Type.** Prerequisite infrastructure, scientific experiment, or both. Infrastructure
work is legitimate and should be labelled, not smuggled in as a finding.

## Design rules that override convenience

- **Change one important variable at a time.**
- **Match action budgets and interaction opportunities** across conditions.
- **Distinguish model-selected actions from harness substitutions.** If your harness
  overrides the model's choice, count how often — otherwise you may be measuring the
  harness and calling it the model.
- **Measure mechanics discovery and plan quality where relevant, not only clears.** A
  method can understand more and still clear nothing.
- **Prefer the cheapest experiment that can falsify the hypothesis.**
- **Define how instruction-following will be measured** whenever the experiment needs
  structured output from a model. In this project's runs, two thirds of replies ignored
  a required label — without measuring that, the result would have been read as a
  failed hypothesis instead of a failed interface.
- **Do not conclude a capability is impossible when you have only shown one
  representation of it failed.** Telling a model what the controls do made things worse
  here; that is evidence about *that description*, not proof that controllability
  knowledge is useless.

## A worked shape

> **Question.** Does judging screen change with clock cells masked clear more levels
> than judging with an exact screen hash?
> **Capability.** Perception of change.
> **Treatment/control.** Identical random + pruning policy; the only difference is the
> change-judge. Control must byte-reproduce the previous exact-hash result.
> **Falsifier.** No improvement outside seed spread on held-out games.
> **Either way.** Positive: part of the ceiling was perceptual. Negative: still
> delivers a validated common judge and removes clocks as an explanation for later
> null results.
> **Type.** Both — infrastructure and science.

Note the shape of the last line. The best first experiment is one that is **informative
whichever way it goes**.
