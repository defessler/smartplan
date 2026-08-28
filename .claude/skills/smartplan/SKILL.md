---
name: smartplan
description: Use proactively for any coding or implementation task. It routes by regime - one-context tasks run inline; fan-out is for beyond-context scale, rework-prone execution, verify-gated work, and wall-clock batches. FAST PATH - plainly one-context, non-risky work runs inline now (one-line routing call, batched turns, terse output); any fan-out REQUIRES loading references/flow.md first.
---

# smartplan — regime router

**The rule:** plan with the strong model, implement with the cheaper
model, escalate on demonstrated failure — never on a hunch. **Invoke:**
`/smartplan <task>` on Claude Code or Copilot CLI; you route it yourself
and **never ask the user to invoke anything.**

## Route by regime — measured (T9 · T14 · T19–T21 · T25 · T33)

A task ONE strong context swallows whole defaults **inline**: per-leaf
overhead plus inline strong-model token-efficiency made the full ceremony
cost 1.5–2.9× one inline pass at equal oracle quality across every leaf
count and size tested (1·T14 · 5-small·T19 k=2 · 12-tiny·T20 · 5-big·T21),
and even *routing* a one-context task through the full skill body measured
1.52× bare inline (T25) — which is why the inline route below is lean.
Neither width nor size amortizes the ceremony — one strong context
out-runs N cold cheaper ones. Dispatch the FULL flow only where it
measurably pays: work exceeding one context window; failure-prone
execution where inline flails and reworks (T9: 39–55% of inline —
dated 2026-07-11; T26 found no trap on current Sonnet and T33 measured
2.78× *against* tiering once inline stopped failing, so this fires on
demonstrated failure, not anticipation);
wall-clock-bound batches — **including ≥4 independent units with disjoint
FILES.** Count units, not tokens: a 1M window *holds* large work without
*bounding* it, so "fits in one context" stopped being the size test. N files
taking the SAME edit is ONE leaf; N taking different edits is N. This trades
tokens for wall-clock **knowingly** — the 1.5–2.9× above is just as real at
4 units. Fire it when finishing sooner is worth more than finishing cheaper,
and say which you chose.
And verify-critical work — independent checks
still gate risky merges at ANY size (C++ shared-blind-spots, security);
verify value survives where fan-out economics don't. Ceremony collapses;
the verify floor never does.

## Inline route (the default for one-context work)

- **State the routing call in ONE line, then start** — no deliberation
  essay. When the work splits into **≥4 independent units**, name the count
  and why inline still wins. An unstated call defaults to inline, and that
  silence is the miss: fan-out then fires only when asked for.
- **Token discipline:** batch independent reads into one turn and
  independent writes into one turn; never re-read a file already in
  context; hold the mode's output ceiling
  (`references/modes.md`) — output bills ≈5× input.
- **Verify floor (never collapses) — the strongest AVAILABLE oracle, not
  merely a fresh one:** **1** executable (compiler, assertion, replayed
  real input) **2** fresh-context model **3** same-context model. A cold
  model shares the writer's training and blind spots; a compiler doesn't.
  Code-emitting work has tier 1 by definition, so nothing below it counts.
  And before a green check counts, say what would turn it **red** — if
  that answer doesn't name what you just changed, it isn't verification.
  An independent check (`references/check.md`) still gates risky merges at
  any size — C++ shared-blind-spot classes (UB, concurrency, templates),
  security — and Cheap-tier output never merges unverified.
- **Spiral guard:** two failed self-repairs against the same failing
  signature = STOP; dispatch ONE fresh-context Mid-tier diagnosis with the
  ESCALATION REPORT (`references/flow.md`) instead of a third blind
  attempt (T9: blind repair burned 75–167 cr and once failed; the
  fresh-context ladder never did).
- **False-success guard — the spiral guard's blind side:** that guard needs
  a failing signature, so all-green attempts never trip it. **A repeat
  report of a symptom you claimed fixed is a strike.** Next action is not a
  third fix — it's proving your observable measures what they describe.
- **Land the check, not a note:** a fix whose only durable trace is a note
  hasn't landed — leave the executable oracle in the repo (compile step,
  assertion, fixture) so the next context meets it instead of recalling it.
  **Compaction re-injects skill bodies, NOT the references you read**,
  so a mid-task rule survives only here or on disk; after one, re-read the
  run's artifacts before acting.
- **Cost mode:** honor `{{MODE}}`
  (default max-quality; budget on Copilot — it meters credits per token).
  On an explicit budget/max-savings ask or stated budget pressure, print
  the **budget preflight** FIRST (a standing budget default alone doesn't
  re-print it), then bias inline choices toward cost
  (`references/modes.md` § Budget preflight).

## Fan-out route (beyond-context · rework-prone · verify-gated · wall-clock)

**HARD GATE — load `references/flow.md` FIRST and follow it end to end:**
plan, human plan-review gate, tiered dispatch, independent verify,
integrate, escalate. Never dispatch a tiered subagent, compile a brief, or
fan out at all without flow.md loaded — the human gate and the
mode-invariant floors live there. **A denied read is a STOP, never an
obstacle to route around** (T31).

## Evolving this skill

Reality outruns the rubric → flag it, never silently improvise — procedure
in `references/flow.md` § Evolving this skill; history in
[the repo's commit log](https://github.com/defessler/smartplan/commits/main).
