# flow — the fan-out flow (Plan → Gate → Dispatch → Verify → Integrate → Escalate)

*Loaded from SKILL.md's fan-out gate — never fan out without this file.*

**Core policy:** spend the strong model where it pays — *planning* — and
cheaper models where the work is mechanical — *implementation fan-out*.
Escalate only when a cheaper tier actually fails, and keep a human at the
plan boundary. Harnesses: Claude Code (§A) · Copilot CLI (§B).

## Contents

- Fan out only on independent work
- The flow
- Model-role matrix
- Quality↔cost mode (one dial; default max-quality, budget on Copilot)
- Dispatch — pick your harness
- Reach for the built-in instead
- Escalation report (attach to every escalation)
- Budget / rate-cap pressure
- Honest scope note (don't oversell)
- Evolving this skill

## Fan out only on independent work

**Independence is a precondition you TEST FOR, not one you assume.** Fan out
only when the work splits into genuinely independent, separately verifiable
units. Anthropic's parallel-Claudes C compiler post names the failure mode:
"compiling the Linux kernel is one giant task. Every agent would hit the
same bug." That's this repo's own 148–289% loss seen from the winning side.
Coordinate through durable filesystem or VCS artifacts — a task-lock file,
`contracts.md`, `run-state.md` — never agent-to-agent messaging.

## The flow

You orchestrate the family yourself — load each reference and attach the
smartexec payload at the step that needs it, and **never ask the user to
invoke anything.**

1. **Plan** on the planner seat (matrix below). *(judgment)* Ambiguity that
   would change the plan's *shape* — scope boundaries, competing readings,
   unstated edge-case handling — is asked about **before** decomposing;
   skip when the ask is unambiguous.
   **Bigger-system plans get a wiring-diagram offer:** when the plan spans
   multiple subsystems or reshapes how they connect and `smartdiagram` is in
   the catalog, ASK here (one line) whether to build or update it, and
   invoke only on an explicit yes. Ownership domains then suggest leaf
   boundaries.
   Decompose for **maximum parallelism**: many small independent leaves with
   disjoint FILES; serialize only true dependencies. **Test each candidate
   pair against three questions** — same file? one needs the other's output?
   one renames a symbol the other reads? Any *yes* serializes or merges them.
   All *no* and they run concurrently. Run the test before sizing the wave,
   not after: a pair you assumed independent is the conflict that eats the
   fan-out's whole margin. Waves default to **3–5
   concurrent leaves**; >5–8 needs stated justification. A hotspot file
   several leaves touch **serializes** — conflict avoidance is a
   *precondition* of fan-out economics (a measured swarm rebuild cut
   conflicts 70k→<1k and cost ~8× on this discipline alone).
   When leaves consume each other's outputs, freeze the shared surfaces in a
   plan-adjacent **`contracts.md`** *before* fan-out and have each consuming
   brief cite it (shape: `references/artifacts.md`). Unclear class→tier
   mapping → consult **`references/routing.md`**.
2. **Gate:** present the plan for human review; persist the approved plan.
   Quote the human's go-signal **verbatim** into each brief's AUTHORIZATION —
   plan approval and execution authorization are different events. **The
   request that started the task is NEITHER** — "get them done" and "wall
   clock matters" authorize the work, never the plan, so a gate that quotes
   them has not run. **That
   approval is also the user request the Opus-5 don't-dispatch injection
   requires** (`claude-code.md`): once it exists, quote it and dispatch.
   The gate **re-arms for the delta** when the plan materially changes
   mid-flight; re-gate the changed slice, not the whole plan. **Dynamic
   workflows are out of scope for gated work:** their subagents always run
   `acceptEdits` whatever the session mode says, and the launch prompt is
   skipped under bypass permissions, `claude -p` and the Agent SDK. Launch
   one anyway and the gate moves to the launch boundary — approve before it
   starts, because nothing stops it after.
3. **Dispatch leaves in parallel** with your harness's lever (§A/§B). A
   dispatch is a *subagent with its own model* — never in-context work by
   the session model. Fire every ready, disjoint-FILES leaf **concurrently**;
   one-at-a-time dispatch wastes the fan-out. **Stagger for cache:** a
   cache entry is readable only once its first response starts streaming —
   dispatch ONE leaf, await first output, then fire the rest so siblings
   read the shared prefix at 0.1× instead of each paying the cold 1.25×
   write. Sonnet-tier leaves take the plan's task text; Cheap leaves take a
   compiled brief (**`brief.md`**) *plus* the `smartexec` protocol. Track
   every transition in **`run-state.md`** (one row per leaf) and render each
   into chat as ONE compact **dispatch-board line** —
   `▶ 4 running: L1 renames→haiku · L2 parser→sonnet · … | seat: opus (plan)`
   — transitions only, never polling turns. **While a wave is in flight, end
   the turn** — completions re-invoke you, and every idle wait turn re-reads
   your whole context at cache price. Shapes: **`artifacts.md`**.
4. **Verify:** every Cheap result goes through a fresh-context **smartcheck**
   (**`check.md`**) before acceptance — never the executor's own context.
   **The verifier is never weaker than the executor**: Sonnet- and Opus-tier
   leaves get an Opus-or-comparable check; the one exception is an
   Opus-or-stronger session model reading the full diff, and only for leaves
   it did **not** author — self-review is the self-preference trap, and
   "looks done" is never a review. **Scouting leaves** produce no diff and
   skip the protocol, but the consumer **must** spot-check every
   load-bearing scouted fact (`check.md` § Scouting). A C++ gamedev leaf
   layers **`cpp-gamedev-check.md`** onto the check, under its Engine
   Profile (`vanilla|custom|unreal`, from `smartreview`'s standards doc).
5. **Integrate** *(planner seat, judgment)* once a wave passes verification:
   reconcile the cross-leaf seams per-leaf checks can't see — naming drift,
   duplicate helpers, `contracts.md` mismatches, guessed imports. Verified
   in isolation is not verified in composition. Do it before human
   acceptance, including after a resume. Close with **Confidence notes**
   written FOR the human: 3–4 short bullets in plain full sentences —
   least sure of · what may surprise you · what breaks later · what was
   assumed — each with its recommendation inline, never a dot-separated
   chain (the per-leaf half in `check.md` § Reflective sweep stays terse,
   it's agent-consumed). Then at most ONE optional unrequested-improvement
   offer (never pre-built) and ONE session-retro line; a retro that names a
   rule gap routes into "Evolving this skill".
6. **Escalate** on two strikes — exactly one tier, ESCALATION REPORT
   attached (canonical rule below).

## Model-role matrix

Lineup, strongest → cheapest: **Fable 5 > Opus 5 > Opus 4.8 > Sonnet 5
> Haiku 4.5.** <!-- claim:anthropic-model-lineup --> The full cross-vendor
roster (classes, dated prices, default/candidate/provisional status) is the
hand-editable registry **`references/model-classes.md`** — reclassify there,
never inline here.

**User-named models are a roster, not a routing instruction.** Seat them by
capability class, refuse over-seating by default, and present any reseating
at the gate — full procedure in `routing.md` § Seat eligibility. An explicit
"seat it anyway" is honored and recorded in `run-state.md`.

### Planner seat — default Opus 5, drop on fit

| Choice | Model | Use when |
| --- | --- | --- |
| **Default** | **Opus 5** | Multi-file, cross-cutting, ambiguous, or any plan whose blast radius you can't bound at a glance. |
| Drop down (on fit) | Sonnet 5 · Haiku 4.5 | The plan is unmistakably small, bounded, single-domain, unambiguous. |
| Max (opt-in) | **Fable 5** | The hardest architecture/decomposition decisions. **Planning only.** |

**Bias toward staying on Opus when unsure** — a planning flaw reproduces
across every executor (N× blast radius), so the drop-down is a *certainty*
move — the inverse of the implementer seat below.
**Audit/review/synthesis that feeds a plan is planner-seat work** — same N×
radius — capped at Opus, never Fable. Its findings are a **work queue, not
a verdict**: reproduce before acting, log every cap (`check.md` § Review).

### Implementer seat — start at the class floor, escalate on fail-twice

| Choice | Model | Floor for |
| --- | --- | --- |
| **Cheap** | Haiku 4.5 | Mechanical, single-concern, verifier-checkable leaves (renames, formatting, codemods, boilerplate-from-exemplar) — only via smartexec **behind smartcheck**. Fails silently; never unverified. (Scouting: Cheap-floor, no-diff — step 4's spot-check path, not smartexec.) |
| **Mid** | The newest Sonnet | Everything else — briefed/correctness-sensitive leaves, and anywhere the check can't be scripted. |
| Reserve | Opus 4.8 | An *irreducibly* cross-cutting leaf (a mini-plan), or a fail-twice target. Not "hard algorithm." |

**Two guardrails:** (1) **Bounce breakeven** — weaker-first *raises* token
count (escalations are extra rounds) and pays back only on price/limit,
only when the class bounces under **~20–30%**; a bouncing class gets its
floor bumped up. (2) **Verifier-catchability** — Cheap floors only where
failure is *checkable*; where executor and verifier share a blind spot
(C++ UB, concurrency, templates, security) the floor stays Sonnet.

**Effort is a second axis** — Cheap leaves run low/medium effort; a planner
escalation raises effort too (Claude Code: frontmatter `effort:` /
`--effort`; Copilot: `--effort`, ladder none–max; reasoning bills as
output). Pin it in the **seat** — a Claude Code `Agent()` call takes no
`effort` param and Copilot's is session-global, so neither harness offers
a per-dispatch drop. Cheap seats ship pinned (`effort: low`). **Output verbosity is the third notch**:
output tokens price ≈5× input, so terse executor blocks and the lean
default style are the fan-out norm.

**Universal escalation — the fail-twice rule** *(canonical statement; other
files point here, never restate)*: a smartcheck FAIL is a strike.
**Classify before counting.** A leaf that died on a 5xx/529, a
`stop_reason: "refusal"` (Opus 5's safety classifiers end turns clean, HTTP
200, no error), or `max_tokens` truncation is **infrastructure, not a
strike** — check status.claude.com, retry with backoff, don't escalate a
tier for weather. An
executor BLOCKED gets exactly one same-tier retry with a repaired brief
before it counts, and that retry **resumes the same executor** (warm
context), never a cold re-dispatch (Claude Code: `SendMessage` auto-resumes
the completed subagent, tier-safe ≥2.1.211; Copilot: `--resume`). **Two
strikes** — two FAILs, a FAIL after a repaired-BLOCKED, or two post-repair
BLOCKEDs — **escalate exactly one tier** with the ESCALATION REPORT
attached. Never silently re-run; never skip tiers. Attempt counts persist in
`run-state.md` and survive a resume. **Terminal case:** an Opus strike-out
has no higher implementer tier (Max/Fable is planning-only, never an
escalation target) — the orchestrator takes the leaf over itself,
in-context, report attached. The same arithmetic governs the inline route
(SKILL.md § Spiral guard).

## Quality↔cost mode (one dial; default max-quality, budget on Copilot)

`{{MODE}}` = `max-quality · high-quality · balanced · budget ·
max-savings` — one dial biasing every discretionary knob (planner seat,
floors, verify machinery, escalation trigger, effort, output register,
fan-out width). Matrix plus the mode-invariant floors (human gate,
never-merge-unverified, honesty, byte-verbatim evidence):
**`references/modes.md`**. Set it per invocation (`--mode budget`), per leaf
(brief MODE line), or once via the token; non-defaults go in `run-state.md`.

## Dispatch — pick your harness

Claude Code → **§A**; GitHub Copilot CLI → **§B**. The seats are identical
everywhere — only the *lever* changes.

Two further harnesses are tracked, each needing a different lever shape and
neither with a section here (this file is byte-capped). **ZCode** → load
`zcode.md`: per-agent model pin, **no per-call override**, and it reads
`AGENTS.md`, never `CLAUDE.md`. **M365 Copilot** → load `m365-copilot.md`:
most of this flow **cannot ship there**, so read its verdict table first.

### §A · Claude Code
- **Lever:** per-call `model:` on each dispatch. **Wave guarantee:**
  `export CLAUDE_CODE_SUBAGENT_MODEL=sonnet` before an implementer wave,
  then **unset it** after — since v2.1.196 `=inherit` is merely identical to
  unset, not a pin to the session model. **Clear it before any verify
  dispatch**: it outranks the per-call `model:` a Strong verifier needs, so
  leaving it pinned silently downgrades the gate to Sonnet-judging-Sonnet.
  Parallel edit leaves get `isolation: worktree` (costly — only for real
  parallel edits). Plan-feeding audits dispatch as `fork`: warm cache, but
  it **always runs the session model and ignores `model:` silently** — a
  context lever, never a tier one.
- **Honesty:** whether a routed tier *lands* is contested — #43869 open, no
  assignee (re-checked 2026-08-05). But `/usage` **does** attribute
  per-model: its `Usage by model:` block prints a token line per model, so
  run a cheap wave and look for that model's line. An all-Opus breakdown
  after a Haiku wave is free in-harness evidence the tier didn't land (on a
  subscription seat the dollars aren't a bill, the attribution still is). A
  silently failing lever makes tiering cost-additive, so `/model opusplan`
  stays the routing-free fallback when the core rule must be guaranteed.
- **Undo:** background subagent edits land outside the session's
  checkpoints, so `/rewind` won't restore them — revert with git. A forked
  skill with `background: false` keeps rewind working, costing concurrency.
- **Depth on demand** — resolution order, caching-aware fan-out, hard
  ceilings (spawn cap · depth), Agent Teams and dynamic workflows (incl.
  ultracode), the enforcement hook, tool-locked agent templates: **load
  `references/claude-code.md`**.

### §B · GitHub Copilot CLI
- **Lever:** no per-call override — pinned agents in `.github/agents/`
  (`@smartplan-planner` / `-implementer` / `-implementer-cheap` /
  `-implementer-reserve` / `-verifier` / `-scout`, slug-form `model:`),
  `/subagents` for in-session pins, inline naming. **Never mix Auto with
  tiered dispatch** (pins reported downgraded on 0x-cost-tier sessions,
  copilot-cli#2758). **`/model plan`** (v1.0.74) pins a plan-mode-only
  model and reverts on exit — the native `opusplan` analog.
- **Engine:** after the gate, fan out via the model-invocable **`task`
  tool** — several calls in one turn run in parallel; `/fleet` is the
  heavier human-triggered engine (its validation is NOT a smartcheck).
  Monitor `/tasks`. **Subagent tokens bill.**
- **Depth on demand** — credits/allowances, concurrency caps, cross-vendor
  economics, command naming: **load `references/copilot.md`**.

## Reach for the built-in instead

Each ships in the box and covers one regime outright. Reach for it before
rebuilding it out of this flow.

- **`/batch`** — plan-gated fan-out for beyond-context work: one
  worktree-isolated subagent and one PR per unit.
- **Dynamic workflows** / **`/effort ultracode`** — scripted orchestration,
  loop and intermediates in script variables instead of your context.
  **Ask first:** the tool requires explicit opt-in, and "this task would
  benefit" doesn't count.
- **`/verify`** (builds and runs the app) and **`/code-review`** (reads the
  diff in a fresh subagent) — the two verification shapes.
- **`opusplan`**, Copilot's **`/model plan`** — plan-then-execute tiering
  with no dispatch machinery.

None of them makes verification *mandatory*. That's the half worth carrying.

## Escalation report (attach to every escalation)

```
ESCALATION REPORT
TASK:         one line — what the leaf was supposed to do.
TIER HISTORY: each attempt — tier · verdict (DONE/BLOCKED/FAIL) · one-line why.
EVIDENCE:     exact error text / FAIL reasons, pasted verbatim.
HYPOTHESIS:   suspected root cause.
NEXT:         what the receiving tier should do differently.
```

## Budget / rate-cap pressure

A session/weekly limit or credit budget is a **routing signal**: shift
mechanical leaves down a tier immediately; **defer planner-seat work to the
reset rather than demoting it** (a capped plan still has N× blast radius);
size fan-outs to survive a mid-run cap. Policy: `routing.md` §
Session-limit pressure. **Never cap (`--max-ai-credits`) the orchestrating
session** — caps are visible to the model and can suppress skill loading
entirely (measured, T25 pilot); cap leaves, not the orchestrator.

## Honest scope note (don't oversell)

- Tiering lowers the **bill**, not token *count* — each subagent reloads
  its own context on a cold 5-minute cache. Caching is the automatic lever;
  the discipline is not breaking the cached prefix. Mechanics:
  `claude-code.md` + `caching.md`.
- **Weaker-first is a price/limit play** that pays only under the bounce
  breakeven with real leaf volume. Judge on **cost-per-merged-change**.
- State the real Sonnet-floor gap: 85.2 vs 88.6 on SWE-bench Verified
  (Sonnet 5 System Card, 2026-06-30) — near-frontier, never the uncited
  "80–90%" folklore. <!-- claim:sonnet-vs-opus-swe-bench -->
- `run-state.md` is a **checkpoint, not durable execution** — only `passed`
  rows are safe skips on resume; `dispatched`/`failed`/`escalated` rows
  re-dispatch.

## Evolving this skill

When reality outruns the rubric — a task fits no class, a floor under- or
over-tiers, the roster drifts — **flag it, never silently improvise**:
capture the situation, the wrong rule, and a concrete amendment; surface it
for approval; record it in the changelog
(the repo's commit log). Never self-mutate unreviewed.

To prove the flow on a harness: `bash scripts/selftest.sh`, then the
artifact-graded probes in `docs/selftest.md`.
