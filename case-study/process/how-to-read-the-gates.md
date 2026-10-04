# How to read the gate receipts

`gates/` holds 139 JSON files written by Genesis, the harness this project ran under.
Each is a receipt for one gate on one task: a command that ran, or a review that was
signed.

Nobody wrote these by hand, which is the point. They were a condition of the work
proceeding, not a record assembled afterwards to look rigorous.

## A command receipt

```json
{
  "task": "T-B6",
  "gate": "tests",
  "kind": "command",
  "command": ".venv\Scripts\python.exe -m pytest tests -q",
  "started_at": "2026-10-01T10:03:46.057Z",
  "exit_code": 0,
  "stdout": "... 109 passed in 166.48s (0:02:46)",
  "revision": { "commit": "5fbc6b43...", "dirty": true },
  "source_hash": "35f5a189...",
  "hash": "15b3e8f8..."
}
```

- **`task`** - the work item. `T-E5a` through `T-E11a` are experiments, `T-B4` to `T-B6`
  the competition builds, `T-C1a` the frame collection.
- **`gate`** - which bar was being cleared: `build`, `tests`, `rehearse`,
  `independent-review`, `numbers`.
- **`exit_code`, `stdout`** - what actually happened, captured rather than reported.
- **`revision.commit`** - the commit it ran against. `dirty: true` means the tree had
  uncommitted changes at the time. Worth knowing, and not hidden.
- **`source_hash`, `config_hash`** - the inputs, fingerprinted, so a receipt cannot be
  quietly reattached to different code.

## A review receipt

Reviews carry `kind: "review"`, a `reason`, a `human`, and a `reviewed_proofs` hash
binding the signature to the specific receipts examined. `human` is whoever accepted it -
on this project almost always the author, which you should read with the appropriate
scepticism.

## What a receipt does and does not prove

It proves a named command ran at a named commit and produced that output, and that
somebody put their name against a review of specific evidence. That is enough to catch
the ordinary failure: a number quietly produced by code that no longer exists, or a test
suite nobody actually ran.

It does not prove the reviewer was thorough, or that the right test was written. A gate
raises the cost of fooling yourself; it does not make it impossible. The register
contains a bug - a win recorded against the wrong game, roughly doubling a reported score
- that passed every gate for days before it was caught.

## Why they are published at all

Two findings here were overturned by later work: the random floor, by a replay bug, and
the C1 collection's stated rationale, by its own data. In both cases "what did we actually
run, and when" had a mechanical answer. That is the only reason the corrections were
possible.

The companion records are `decisions.md` (39 entries), `knowledge.md` (51), and
`project.json`, the canonical Genesis file both were generated from. `genesis-kickoff.md`
is where the project started.
