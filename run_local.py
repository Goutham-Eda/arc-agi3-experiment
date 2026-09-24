"""Run the public Build 3 policy locally, offline, on CPU.

This is the day-one gate from references/setup.md. It plays the public games
with random action selection plus dead-action pruning -- the same policy as the
public Kaggle notebook, rewritten against the `arc_agi` package directly so it
runs on a laptop with no gateway, no API key and no internet.

    python run_local.py --games 3 --episodes 5 --max-actions 80

What you are checking:
  * it finds the games
  * every episode starts at level 1
  * no level is cleared in fewer than 5 actions
  * very few levels are cleared at all (random play is bad -- that is correct)

If a check fails, stop and fix your setup. Nothing you measure later is
trustworthy until this passes.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import random
import sys

from arc_agi import Arcade
from arcengine import GameAction, GameState

GRID = 64
REDRAWS = 64
MIN_PLAUSIBLE_CLEAR = 5  # shortest genuine clear observed; shorter means a bug


def screen_key(frame) -> str:
    return hashlib.blake2b(repr(frame.frame).encode(), digest_size=8).hexdigest()


def play_episode(env, rng, max_actions):
    """One episode on a FRESH environment. Returns (levels, clear_lengths, dead_rate)."""
    frame = env.reset()
    if frame is None:
        raise RuntimeError("reset() returned nothing")
    start_level = getattr(frame, "levels_completed", 0)
    if start_level:
        raise RuntimeError(
            f"episode started at level {start_level}, not 1 -- you are reusing an "
            "environment across episodes. See references/safeguards.md."
        )

    dead: set[tuple] = set()
    levels, dead_moves, since_clear = 0, 0, 0
    clear_lengths: list[int] = []
    by_value = {a.value: a for a in GameAction}

    for _ in range(max_actions):
        if frame.state is GameState.WIN:
            break
        if frame.state in (GameState.NOT_PLAYED, GameState.GAME_OVER):
            frame = env.step(GameAction.RESET)
            since_clear += 1
            continue

        screen = screen_key(frame)
        allowed = [by_value[i] for i in (frame.available_actions or [])
                   if i in by_value and by_value[i] is not GameAction.RESET]
        if not allowed:
            allowed = [a for a in GameAction if a is not GameAction.RESET]

        for _ in range(REDRAWS):
            action = rng.choice(allowed)
            data = ({"x": rng.randint(0, GRID - 1), "y": rng.randint(0, GRID - 1)}
                    if action.is_complex() else None)
            grid = frame.frame[-1] if len(frame.frame) else None
            cell = -1 if grid is None else int(grid[data["y"]][data["x"]]) if data else -1
            move = ((screen, action.value) if data is None else
                    (screen, action.value, cell))
            if move not in dead:
                break

        before_level = frame.levels_completed
        frame = env.step(action, data)
        since_clear += 1

        cleared = frame.levels_completed > before_level
        unchanged = screen_key(frame) == screen
        if unchanged and not cleared and frame.state is not GameState.GAME_OVER:
            dead.add(move)
            dead_moves += 1

        if cleared:
            levels += frame.levels_completed - before_level
            clear_lengths.append(since_clear)
            since_clear = 0

    return levels, clear_lengths, dead_moves / max(max_actions, 1)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--env-dir", default=os.environ.get("ARC_ENV_DIR", "environment_files"))
    ap.add_argument("--games", type=int, default=3, help="how many games (0 = all)")
    ap.add_argument("--episodes", type=int, default=5, help="episodes per game")
    ap.add_argument("--max-actions", type=int, default=80)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    if not os.path.isdir(args.env_dir):
        print(f"environment_files not found at {args.env_dir!r}\n"
              "Download the competition data yourself and set ARC_ENV_DIR.\n"
              "See references/setup.md.", file=sys.stderr)
        return 2

    arcade = Arcade(operation_mode="offline", environments_dir=args.env_dir)
    games = [e.game_id for e in arcade.get_environments()]
    games = games if args.games == 0 else games[:args.games]
    print(f"{len(games)} game(s) from {args.env_dir}\n")

    total_levels, all_clears, flags = 0, [], []
    for game in games:
        levels = 0
        for ep in range(args.episodes):
            env = arcade.make(game, seed=args.seed * 1000 + ep)  # FRESH per episode
            try:
                got, clears, dead_rate = play_episode(
                    env, random.Random(f"{args.seed}:{game}:{ep}".__hash__()), args.max_actions)
            finally:
                del env
            levels += got
            all_clears += clears
            flags += [f"{game} ep{ep}: level cleared in {c} actions"
                      for c in clears if c < MIN_PLAUSIBLE_CLEAR]
        total_levels += levels
        print(f"  {game:<16} {levels:>3} level(s) in {args.episodes} episodes")

    n = len(games) * args.episodes
    print(f"\n{total_levels} levels cleared across {n} episodes "
          f"({total_levels / n:.4f} per episode)")

    print("\nday-one gate")
    ok = True
    print(f"  [{'ok' if games else 'FAIL'}] games found")
    ok &= bool(games)
    print(f"  [{'ok' if not flags else 'FAIL'}] no impossible clear lengths "
          f"(< {MIN_PLAUSIBLE_CLEAR} actions)")
    for f in flags:
        print(f"        {f}")
    ok &= not flags
    print(f"  [{'ok' if total_levels / n < 0.5 else 'CHECK'}] clears are rare, as random play should be")
    print("  [ok] every episode started at level 1 (asserted during the run)")
    print("\n" + ("gate PASSED -- your setup is sound." if ok else
                  "gate FAILED -- fix this before running any experiment."))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
