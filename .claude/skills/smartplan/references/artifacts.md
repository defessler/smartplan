# run artifacts — run-state.md, contracts.md, the dispatch board

*Load on demand from flow.md steps 1/3/5 — when creating a run's
manifest, freezing shared surfaces, or resuming a crashed run.*

## run-state.md — the live, resumable run-manifest

One row per **leaf in the current plan**, written by the orchestrator at
every dispatch/verify/escalate transition, living at the project repo root.
A manifest updated **in place**, not a log. Since the outcome ledger's
removal it is also the run's **outcome record**: close each row with final
status, attempts, and a note carrying any escalation report, over-tier
override, or script path.

| leaf | status | brief-hash | tier | attempts | oracle | note |
| --- | --- | --- | --- | --- | --- | --- |
| leaf-2 (utils: retryWithBackoff) | passed | `a1c9f2e` | Sonnet | 1 | 1 `pytest -k retry` | smartcheck PASS, wave 1 |
| leaf-3 (importer) | dispatched | `7e04b31` | Cheap | 2 | 2 model-read | FAIL strike 1; re-dispatched, awaiting smartcheck |

- **status** is exactly one of `dispatched`|`passed`|`failed`|`escalated`.
- **brief-hash** — short hash of the compiled brief (or the plan's task
  text for a Sonnet-tier leaf): lets a resume tell a stale row (brief
  changed → re-brief, re-dispatch) from a current one.
- **attempts** — the durable strike count the fail-twice rule reads: bump
  at every dispatch, note strikes in `note`. This column is what makes
  fail-twice survive a crash.
- **oracle** — the tier the leaf's ACCEPTANCE actually ran at (`check.md`
  step 2): **1** executable, **2** fresh-context model, **3**
  same-context. Written at verify, not at plan. It does for the verify
  floor what `attempts` does for fail-twice — puts the rule on disk, where
  a compaction can't delete it.

**Resume recipe:** reload the persisted plan; skip every row already
`passed`; re-dispatch everything else (`dispatched`/`failed`/`escalated`
rows are unknown state, not trusted state) — **except `attempts`: restore
it, never reset it.** Two strikes escalate even across the interruption.

**Delete them at integrate.** These land at the *consuming* repo's root and
nothing cleans them up. Measured 2026-08-05: three such files from a
2026-07-10 run still sat in an unrelated project's root, untracked and
un-ignored, one `git add -A` from a commit. Add them to that repo's
`.git/info/exclude` at run start (no tracked file to touch), then remove
them at integrate.

## contracts.md — frozen shared surfaces (written before fan-out)

When one leaf's function, format, or interface is another leaf's input, the
planner freezes the surface **before** dispatch. Rules:

1. **One row per surface** — a signature, file format, or interface shape,
   not a module.
2. **Freeze, don't describe** — the literal copy-pasteable definition,
   never a paragraph about it.
3. **One owner, N consumers** — exactly one leaf owns the surface; every
   consumer cites the row instead of guessing.
4. **A mismatch found at Integrate is a contracts.md bug, not a leaf bug**
   — fix the row, then re-check consumers against the fix.

| Surface | Kind | Frozen definition | Owner leaf | Consumed-by leaves |
| --- | --- | --- | --- | --- |
| `retryWithBackoff` | signature | `retryWithBackoff(fn: () => Promise<T>, opts: { attempts: number; baseMs: number }): Promise<T>` — rejects with the last error once attempts exhausted | leaf-2 (utils) | leaf-3, leaf-4 |
| `job-status.json` | file-format | `{ "jobId": string, "status": "queued"\|"running"\|"done"\|"failed", "updatedAt": ISO8601 }` — one file per job, written atomically | leaf-3 | leaf-4, leaf-5 |

A consuming brief cites the row: *"Consumes contract row `retryWithBackoff`
(contracts.md) — call as frozen; do not reimplement or alter the
signature."*

## The dispatch board — visibility at near-zero cost

Every transition already writes a run-state row; render the same transition
into chat as **one compact line**:

    ▶ 4 running: L1 renames→haiku · L2 parser→sonnet · L3 tests→sonnet · L4 scout→haiku | seat: opus (plan)

Emit **only at transitions** — never a polling turn, never per-leaf
narration; that spacing keeps the cost ~30–50 output tokens per wave
boundary, piggybacked on a turn that was happening anyway. A wide wave
compresses to per-tier counts (`▶ 7 running: 5×haiku · 2×sonnet | seat:
opus (integrate)`). Between transitions the harness's **zero-token**
surfaces carry the live view: Claude Code's agent panel + `/statusline`,
Copilot's `/tasks` + `/statusline`.
