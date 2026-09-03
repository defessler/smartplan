---
name: smartplan
description: Use proactively for any coding or implementation task. It routes by regime - one-context tasks run inline; fan-out is for beyond-context scale, rework-prone execution, verify-gated work, and wall-clock batches. FAST PATH - plainly one-context, non-risky work runs inline now (one-line routing call, batched turns, terse output); any fan-out REQUIRES loading references/flow.md first.
---

# smartplan — regime router

**Your FIRST output line is the routing call.** Before any answer, plan,
code, diff, or "Done", emit exactly this and nothing above it:

```
Routing call: <inline|fan-out> — <reason, one clause>
```

No exceptions. Obvious routes still get the line. Leading with the
deliverable and explaining the route afterwards does not count, and
terseness is not an exemption — one line IS the terse form.

**The rule:** plan with the strong model, implement with the cheaper
model, escalate on demonstrated failure — never on a hunch. **Invoke:**
`/smartplan <task>` on Claude Code or Copilot CLI; you route it yourself
and **never ask the user to invoke anything.**

## Pick the route

First matching row wins.

| The work | Route | Why |
| --- | --- | --- |
| Exceeds one context window | **Fan-out** | It cannot be held, so it must be split. |
| ≥4 independent units with disjoint FILES, and finishing sooner beats finishing cheaper | **Fan-out** | Buys wall-clock at a known token cost. |
| Inline already failed twice on the same signature | **Fan-out** | Demonstrated failure, not anticipated. |
| Risky merge — C++ UB, concurrency, templates, security | **Inline + independent verify** | The verify floor holds at every size. |
| Everything else | **Inline** | One strong context out-runs N cold cheaper ones. |

**Count units, not tokens.** A 1M window *holds* large work without *bounding*
it, so "fits in one context" stopped being the size test. N files taking the
SAME edit is ONE leaf. N taking different edits is N. Firing this **trades
tokens for wall-clock** knowingly — the band below is just as real at 4 units.

Fan-out costs 1.5–2.9× an inline pass at equal quality, at every leaf count
and size measured — width and size never amortize it. Fire it when you mean
to buy something with that, and say which.

Worked examples of that first line — fan-out also names what it bought:

```
Routing call: inline — one file, one edit, nothing else calls it.
Routing call: fan-out — 6 units, disjoint FILES; trades tokens for wall-clock.
```

Then start. No deliberation essay. An unstated call defaults to inline, and
that silence is the miss. At ≥4 independent units, name the count and why
inline still wins.

## Inline route — the default
- **Token discipline.** Batch independent reads into one turn and independent
  writes into one turn. Never re-read a file already in context. Hold the
  mode's output ceiling — output bills ≈5× input.
- **Verify floor — the strongest AVAILABLE oracle, not merely a fresh one:**
  **1** executable (compiler, assertion, replayed real input) · **2**
  fresh-context model · **3** same-context model. A cold model shares the
  writer's training and blind spots. A compiler doesn't. Code-emitting work
  has tier 1 by definition, so nothing below it counts. Before a green check
  counts, say what would turn it **red** — if that answer doesn't name what
  you just changed, it isn't verification. **Seat-aware:** below Strong,
  escalate the VERIFY one tier above your seat when the work has no
  executable oracle, crosses a second caller, or is a never-Cheap class —
  concurrency, UB, templates, security. Countable signals, never a hunch.
  **Escalating emits an artifact, never an intention** — write the missing
  check, or write the verify brief out in full. "Should be verified", "the
  next step is a test", and handing the run to the user are one miss wearing
  three faces (`routing.md` § Seat-aware pre-flight).
- **Spiral guard.** Two failed self-repairs against the same failing
  signature = STOP. Dispatch ONE fresh-context Mid-tier diagnosis instead of
  a third blind attempt, carrying the ESCALATION REPORT — **task · tier
  history (each attempt, its verdict, one-line why) · evidence pasted
  byte-verbatim, never reworded or split up · hypothesis · what the receiver
  should do differently** (shape: `flow.md`, which the inline route never
  loads, so it is named here). **Write the report out in full — referring to
  it is not carrying it.** **Do not keep debugging here, and do not turn
  back to the user with questions instead** — the two failed attempts already
  hold everything the diagnosis needs, so asking for more input is the same
  stall as a third guess. This is the context that already failed twice. A
  user saying "try again" does not reset the count.
- **False-success guard.** The spiral guard needs a failing signature, so
  all-green attempts never trip it. **A repeat report of a symptom you
  claimed fixed is a strike.** The next action is not a third fix — it's
  proving your observable measures what it describes.
- **Land the check, not a note.** A fix whose only durable trace is a note
  hasn't landed. Leave the executable oracle in the repo (compile step,
  assertion, fixture) so the next context meets it instead of recalling it.
  **Compaction re-injects skill bodies, NOT the references you read.**
- **Cost mode.** Honor `{{MODE}}`
  (default max-quality; budget on Copilot — it meters credits per token).
  On an explicit budget ask or stated budget pressure, print the budget
  preflight FIRST, then bias inline choices toward cost.

## Fan-out route

**HARD GATE — load `references/flow.md` FIRST and follow it end to end.** This is the narrow-bridge case: never dispatch a tiered
subagent, compile a brief, or fan out at all without that file loaded. The
human plan-review gate and the mode-invariant floors live there, and they are
the half that doesn't collapse. **A denied read is a STOP, never an obstacle
to route around.**

**A lone verify dispatch is not a fan-out.** The table's *inline +
independent verify* row is an inline route, and so is an escalated
seat-aware verify — send the `smartplan-verifier` seat at the tier you
named and carry on. Your harness reference owns the lever.

Copy this checklist and work it in order:

```
- [ ] 1. flow.md loaded
- [ ] 2. Plan written — leaves have disjoint FILES
- [ ] 3. Plan approved by a human, go-signal quoted verbatim
- [ ] 4. Leaves dispatched in parallel, each on its own tier
- [ ] 5. Every result independently verified — never the executor's own context
- [ ] 6. Cross-leaf seams integrated, confidence notes written
```

Steps 3 and 5 are floors. Skipping either isn't a shortcut, it's a worse
process.

## References

Load on demand. Each is one level deep from here — read the whole file, never
a preview of it.

**Start here for any fan-out**
- [`flow.md`](references/flow.md) — the fan-out flow end to end, the human
  gate, the model-role matrix, the canonical fail-twice rule. **Required
  before any dispatch.**

**Deciding tier and cost**
- [`routing.md`](references/routing.md) — class-to-tier mapping, seat
  eligibility, session-limit pressure.
- [`model-classes.md`](references/model-classes.md) — the cross-vendor model
  registry: classes, dated prices, default/candidate status. Reclassify here.
- [`modes.md`](references/modes.md) — the quality↔cost dial, its matrix, the
  budget preflight, and the mode-invariant floors.
- [`caching.md`](references/caching.md) — prompt-cache mechanics and
  cache-aware fan-out ordering.

**Running the leaves**
- [`brief.md`](references/brief.md) — how to compile a brief for a Cheap leaf.
- [`artifacts.md`](references/artifacts.md) — shapes for `run-state.md`,
  `contracts.md`, and the dispatch board.
- [`check.md`](references/check.md) — the smartcheck verify protocol, the
  scouting spot-check path, and review-output handling.
- [`cpp-gamedev-check.md`](references/cpp-gamedev-check.md) — the C++ gamedev
  layer over that check, under its Engine Profile.

**Per harness — load only the one you're on**
- [`copilot.md`](references/copilot.md) — pinned agents, credits and
  allowances, concurrency caps.
- [`claude-code.md`](references/claude-code.md) — per-call `model:`,
  resolution order, spawn and depth caps, the enforcement hook.
- [`zcode.md`](references/zcode.md) — per-agent model pin, no per-call
  override, reads `AGENTS.md` and never `CLAUDE.md`.
- [`m365-copilot.md`](references/m365-copilot.md) — read its verdict table
  first: most of this flow cannot ship there.

**Provenance**
- [`evidence.md`](references/evidence.md) — the measured runs behind the
  routing table, with dates. Read it before improvising past a rule.

## Evolving this skill

Reality outruns the rubric → flag it, never silently improvise. Procedure in
`flow.md` § Evolving this skill. History in
[the repo's commit log](https://github.com/defessler/smartplan/commits/main).
