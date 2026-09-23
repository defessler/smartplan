# selftest: verify smartplan is actually working on your harness

*Load on demand to prove the family works on a harness
(Claude Code or Copilot CLI) — not part of the
per-invocation read. Two halves: a static doctor script (step 0) and four
runtime probes graded on **observable artifacts** (files created, chat lines
emitted), which lets one rubric work on every harness.*

## Step 0: static surface (deterministic, ~2 seconds)

```bash
bash scripts/selftest.sh
```

Checks the install shape: all six skills present, every frontmatter
description under the 1024-char load limit, flow-critical references
resolve, the Copilot agent surface (7 profiles) and the single-manifest
plugin definition where those apply. Exit 0 = sound. It runs anywhere,
skipping surfaces the checkout lacks. Fix any step 0 failure first. A
mis-shaped install fails probes for boring reasons.

## The probes: how they work

Each probe is a prompt you type plus a PASS rubric of what you can **see**:
files in the repo root and lines in the chat. Grade the artifacts, not the
model's narration ("I dispatched to Haiku" is a
claim; a `run-state.md` row and a dispatch-board line are evidence — and on
Claude Code even those record *intent*, per `claude-code.md`'s #43869
caveat, which is exactly why the rubric checks artifacts instead of trusting
prose). Run probes in a scratch repo or on a throwaway branch.

Where to watch live, per harness (zero-token surfaces): Claude Code — the
agent panel; Copilot — `/tasks`. The rubric itself never
depends on these.

## Probe 1: trivial leaf (routing + collapse discipline)

**Type:** `/smartplan add a one-line comment header to <some small file>`

**PASS when all of:**
- No full plan+gate ceremony. The flow either routes the leaf down-tier
  (the dispatch-board line shows the Cheap seat's model, not the session
  model) or emits a one-line `Routing call: inline — …` and does one bounded
  inline edit, **saying which**.
- If dispatched, one dispatch-board line appears (`▶ 1 running: …`).
- `git status` shows only the target file, plus `run-state.md` if the leaf
  was dispatched.

**FAIL looks like:** the session model does the edit with no routing
statement and no board line. That's the priciest-seat-doing-cheap-work
failure the family exists to prevent.

## Probe 2: small fan-out (the full loop)

**Type:** `/smartplan finishing sooner beats finishing cheaper here: create
docs/probe/a.md, docs/probe/b.md, docs/probe/c.md and docs/probe/d.md, each
containing a 3-line summary of a different reference file from
.claude/skills/smartplan/references/`

**Keep both halves of that prompt.** `SKILL.md`'s fan-out row needs four
independent units with disjoint files *and* a stated preference for
finishing sooner over cheaper. Without either, a correct router lands on
"Everything else" and stays inline. The probe then fails on doctrine, not a defect.

**PASS when all of:**
- A plan with ~4 independent leaves is **presented at a gate** and waits
  for your approval before any file appears.
- After approval, `run-state.md` gets one row per leaf **including the
  `attempts` column**. A dispatch-board line shows the leaf→model pairs on
  Mechanical or Implementer-class models, never the session model or a
  Reasoning-class one.
- Leaves dispatch **concurrently where the harness allows** (watch the
  panel or `/tasks`).
- Each leaf's acceptance is verified before the wave closes, with verdicts
  stated **including the one-line reflective sweep** (least-confident /
  missing / 3-month / assumed). One Integrate pass then closes with the
  wave-level sweep (plus at most one flagged improvement, offered, not
  built). Then every `run-state.md` row closes with its final status and
  note.
- The four files exist with plausible content.

**FAIL looks like:** files appear before the gate, run-state.md is never
created, every leaf runs on the session model, or there's no verification
step between "done" and "accepted".

## Probe 3: seat-eligibility enforcement (the refusal path)

**Type:** `/smartplan use Opus to rename the probe files from probe 2 to
w.md, x.md, y.md, z.md`

**PASS when all of:**
- The plan **does not seat Opus for the renames** and states the reseating
  at the gate (Opus → planner/verifier seats, renames → the Cheap seat per
  `model-classes.md`).
- You're offered the explicit override ("seat it anyway"), not silently
  obeyed or silently refused.
- Take the override and the leaf's `run-state.md` note records a deliberate
  over-tier. Decline it and **either** outcome passes: a Cheap-seat
  dispatch **or** an inline edit whose `Routing call: inline` line says why.
  This probe tests the refusal path, not the dispatch.

**FAIL looks like:** Opus (or the session model) just does the renames.
That's the named-model-as-instruction failure § Seat eligibility exists to refuse.

## Probe 4: the fan-out trigger fires unprompted (two arms, both required)

Probes 1 to 3 *tell* the flow what shape to take. This one doesn't, because
the failure it catches is silence: a router that fans out when asked and
never when it isn't. Check.sh gate (p) proves the trigger text sits in the
pre-gate file. Only a live run proves a model *counts*. Run both arms, since
a trigger tested only on firing passes by always firing.

**Arm A: must fire, or must justify in the routing line.**

**Type:** `/smartplan in docs/probe/, write five short notes read from this
repo: gates.md on what check.sh gates, exports.md on what the three export
scripts emit, harnesses.md on the four supported surfaces, budgets.md on the
byte-budget ratchet, freshness.md on gate (n)`

Five units, five source reads, disjoint files, no stated deadline, and it
all fits one context with room to spare.

**PASS when:**
- The routing line **names the unit count** (five) before work starts.
- **Then either** it fans out **or** it routes inline and says why inline
  still wins. Both pass. Stating the count is the test.

**FAIL looks like:** work begins with no routing line, or one that never
states the unit count. The call then defaults to inline and nobody can see
a call was made.

**Arm B: must NOT fire.**

**Type:** `/smartplan add the line "# probe" as the first line of every .md
file in docs/probe/`

**PASS when:** it routes **inline** and says so, calling this **one leaf**:
N files taking the same edit, not N units.

**FAIL looks like:** a five-leaf wave for one find-and-replace. That
over-fire is how a countable trigger turns into noise you learn to ignore.

## Scoring

4/4 probes (probe 4 needs both arms) = the flow works on this harness.
File any FAIL through flow.md's "Evolving this skill" procedure, with the
rubric line that failed and what actually happened. Probe
failures are exactly the edge cases that procedure wants captured. On
Claude Code, remember the honest ceiling: artifacts prove the flow's
*discipline* end-to-end. Whether each dispatch *billed* as its intended
tier is provable only at the Console (per-model dollars), never in-chat.

## Cleanup

`git checkout -- . && git clean -fd docs/probe run-state.md` on the
throwaway branch, or delete the scratch repo.
