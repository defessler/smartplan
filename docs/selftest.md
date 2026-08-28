# selftest — verify smartplan is actually working on your harness

*Load on demand, when you want to prove the family works on a given harness
(Claude Code or Copilot CLI) — not part of the
per-invocation read. Two halves: a static doctor script (step 0) and four
runtime probes graded purely on **observable artifacts** — files created and
chat shapes emitted — so the same rubric works on every harness with no
service-specific API.*

## Step 0 — static surface (deterministic, ~2 seconds)

```bash
bash scripts/selftest.sh
```

Checks the install shape: all six skills present, every frontmatter
description under the 1024-char load limit, flow-critical references
resolve, the Copilot agent surface (6 profiles) and the single-manifest
plugin definition where those apply. Exit 0 = sound. The script skips
harness surfaces that don't exist in the checkout (e.g. a copilot-export
tree has no marketplace manifest), so it runs anywhere. If step 0 fails,
fix that before running probes — a mis-shaped install fails probes for
boring reasons.

## The probes — how they work

Each probe is a prompt you type, plus a PASS rubric of things you can
**see**: files in the repo root and lines in the chat. Grade against the
artifacts, not against the model's narration ("I dispatched to Haiku" is a
claim; a `run-state.md` row and a dispatch-board line are evidence — and on
Claude Code even those record *intent*, per the Honest scope note's #43869
caveat, which is exactly why the rubric checks artifacts instead of trusting
prose). Run probes in a scratch repo or on a throwaway branch — probe 2
creates and edits files.

Where to watch live, per harness (zero-token surfaces): Claude Code — the
agent panel; Copilot — `/tasks`. The rubric itself never
depends on these.

## Probe 1 — trivial leaf (routing + collapse discipline)

**Type:** `/smartplan add a one-line comment header to <some small file>`

**PASS when all of:**
- The flow does NOT run a full plan+gate ceremony — it either routes the
  leaf down-tier (dispatch-board line shows a Mechanical-class model) or
  states the sub-threshold one-off carve-out and does one bounded inline
  edit, **explicitly saying which**.
- One dispatch-board line appears if dispatched (`▶ 1 running: …`).
- Nothing else in the repo changed (`git status` shows only the target
  file, plus `run-state.md` if the leaf was dispatched).

**FAIL looks like:** the session model silently does the edit with no
routing statement and no board line — the exact
priciest-seat-doing-cheap-work failure the family exists to prevent.

## Probe 2 — small fan-out (the full loop)

**Type:** `/smartplan create docs/probe/a.md, docs/probe/b.md,
docs/probe/c.md and docs/probe/d.md, each containing a 3-line summary of a
different reference file from .claude/skills/smartplan/references/`

**Four files, not three, and the count is load-bearing** — four independent
units with disjoint files is exactly the fan-out threshold `SKILL.md` states.
At three a correct router now stays inline and this probe would fail on
doctrine rather than on a defect.

**PASS when all of:**
- A plan with ~4 independent leaves is **presented at a gate** and waits
  for your approval before any file appears.
- After approval: `run-state.md` is created/updated with one row per leaf
  **including the `attempts` column**, and a dispatch-board line shows the
  leaf→model pairs (Mechanical/Implementer-class models — not the session
  model, and not a Reasoning-class model).
- Leaves dispatch **concurrently where the harness allows** (watch the
  panel / `/tasks`).
- Each leaf's acceptance is verified before the wave closes — verdicts
  stated **including the one-line reflective sweep** (least-confident /
  missing / 3-month / assumed) — then one Integrate pass runs and closes
  with the wave-level sweep (+ at most one optional flagged improvement,
  offered not built), then every `run-state.md` row is closed with its final
  status and note.
- The four files exist with plausible content.

**FAIL looks like:** files appear before the gate; run-state.md never
created; every leaf silently runs on the session model; no verification
step between "done" and "accepted".

## Probe 3 — seat-eligibility enforcement (the refusal path)

**Type:** `/smartplan use Opus to rename the probe files from probe 2 to
w.md, x.md, y.md, z.md`

**PASS when all of:**
- The plan **does not seat Opus for the renames**: it states the reseating
  (Opus → planner/verifier seats; the renames → a Mechanical-class model
  per `model-classes.md`) at the gate, in so many words.
- You are offered the explicit override ("seat it anyway") rather than
  silently obeyed or silently refused.
- If you take the override: the leaf's `run-state.md` note records a
  deliberate over-tier. If you don't, **either** outcome passes — a
  Mechanical-class dispatch, **or** an inline edit that explicitly states the
  sub-threshold carve-out. *(Clarified 2026-08-12 after T38. The clause used
  to demand a Mechanical dispatch, which contradicted Probe 1's carve-out for
  exactly this size of task. A fresh agent picked the carve-out and cited this
  repo's own 1.5-2.9x ceremony measurement to justify it. The refusal path is
  what this probe tests, not the dispatch.)*

**FAIL looks like:** Opus (or the session model) just does the renames —
the named-model-as-instruction failure § Seat eligibility exists to refuse.

## Probe 4 — the fan-out trigger fires unprompted (two arms, both required)

Probes 1–3 all *tell* the flow what shape to take. This one doesn't, because
the failure it exists to catch is silence: a router that fans out correctly
when asked and never when it isn't. Check.sh gate (p) proves the trigger text
is present and sits in the pre-gate file. Only a live run proves a model
*counts*. Run both arms — a trigger tested only on firing is passed by
always firing, which is its own defect.

**Arm A — must fire, or must justify in the routing line.**

**Type:** `/smartplan in docs/probe/, write five short notes read from this
repo: gates.md on what check.sh gates, exports.md on what the three export
scripts emit, harnesses.md on the four supported surfaces, budgets.md on the
byte-budget ratchet, freshness.md on gate (n)`

Five units, five different source reads, disjoint files, no stated deadline,
and the whole thing fits one context with room to spare — so under the old
wording nothing fired at all.

**PASS when:**
- The routing line **names the unit count** (five), out loud, before work
  starts.
- **Then either** it fans out, **or** it routes inline and says why inline
  still wins here. Both pass. The count being stated is the test.

**FAIL looks like:** work begins with no routing line, or with one that never
mentions how many units there were. That silence is the original defect —
the call defaults to inline and nobody can see that a call was made.

**Arm B — must NOT fire.**

**Type:** `/smartplan add the line "# probe" as the first line of every .md
file in docs/probe/`

**PASS when:** it routes **inline** and says so, calling this **one leaf** —
N files taking the same edit, not N units. A dispatch board with a leaf per
file is the FAIL.

**FAIL looks like:** a five-leaf wave for one find-and-replace. That is the
over-fire this arm exists to catch, and it is how a countable trigger turns
into noise the user learns to ignore.

## Scoring

4/4 probes (probe 4 needs both arms) = the flow works on this harness.
Any FAIL: file it via
flow.md's "Evolving this skill" procedure with the artifact evidence
(the probe rubric line that failed + what actually happened) — probe
failures are exactly the edge cases that procedure wants captured. On
Claude Code, remember the honest ceiling: artifacts prove the flow's
*discipline* end-to-end; whether each dispatch *billed* as its intended
tier is only provable at the Console (per-model dollars), never in-chat.

## Cleanup

`git checkout -- . && git clean -fd docs/probe run-state.md` on the
throwaway branch (or just delete the scratch repo).
