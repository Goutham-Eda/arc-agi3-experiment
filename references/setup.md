# Setup and the day-one gate

## 1. Environment

Python 3.13 in a virtual environment. Versions this process has been run against:
`arc-agi` 0.9.8, `arcengine` 0.9.3, `numpy` 2.5.3, `pytest` 9.1.1.

```bash
python -m venv .venv
source .venv/bin/activate          # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install arc-agi arcengine numpy pytest
```

No GPU. No API key. No tokens. Tier 0 work needs nothing else.

## 2. The games

**Download them yourself.** The competition data is not redistributable, so nobody can
send it to you — not a collaborator, not a repository.

1. Register on Kaggle and accept the ARC Prize 2026 / ARC-AGI-3 competition rules.
2. Download the competition data from the competition page.
3. Unpack it. The games live under `environment_files/<game>/<version_hash>/`.

Point your runner at it with an environment variable rather than editing code:

```bash
export ARC_ENV_DIR=/absolute/path/to/environment_files     # bash
$env:ARC_ENV_DIR = "C:\path\to\environment_files"          # PowerShell
```

There are 25 public games. A separate hidden set (used for the leaderboard) is never
visible to you and is not part of local experimentation.

## 3. The day-one gate

Before you are assigned an experiment, prove your environment is correct. Run a plain
random policy over the public games and check that you reproduce a random floor: a
very small number of level clears, and a score near zero.

What you are checking for:

- **The runner finds the games.** If `environment_files` is not found, `ARC_ENV_DIR` is
  wrong.
- **Episodes start at level 1.** Print the starting level of every episode. If any
  episode starts above level 1, you are reusing an environment across episodes — see
  `safeguards.md`. Fix this before anything else.
- **Clear lengths are plausible.** The shortest genuine level clear observed in this
  project took 5 actions. A one-action clear is a bug, not a result.
- **Your numbers are in the right neighbourhood.** Plain random clears roughly one
  level in eighty episodes on held-out games at an 80-action budget. If you are seeing
  far more, suspect the environment before celebrating.

If the gate fails, stop. Nothing downstream is trustworthy until it passes.

## 4. Scoring

Do not reimplement the score. The `arc_agi` package ships its own scorer
(`EnvironmentScoreCalculator`) — hand it the episode and let it compute.

The headline metric rewards clearing levels in few actions: 100% means matching human
action counts, and scores are capped there. For local experiments, **levels cleared is
the primary metric** and the score is secondary — at low performance the score barely
moves and hides differences that level counts show clearly.

Useful dense secondary metrics, all cheap to compute:

- distinct screens per 100 actions (exploration)
- dead-move rate (fraction of actions leaving the screen unchanged)
- repeat deaths
- action efficiency where the experiment makes it meaningful

Dense metrics are what let a null result still say something. If your treatment clears
no more levels but halves the dead-move rate, that is a finding.
