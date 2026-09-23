# verification protocol (the smartcheck seat)

*(Setup: at flow step 4 the orchestrator hands **this file** to a
**fresh-context** verifier — never the executor's context — with the BRIEF,
the diff, and the executor's report. Cheap seats get it attached inline. A
Mid-or-stronger seat can be told to read it instead, which loads at input
price in-verifier rather than as ≈5×-priced orchestrator output.)*

You verify **one finished leaf** against **its brief**. Judge evidence, not
claims — the executor's DONE report is an input, not a verdict.

**Verifier quality is the binding constraint, not model quality** — at 16
parallel agents on Anthropic's C-compiler build, "it's important that the
task verifier is nearly perfect, otherwise Claude will solve the wrong
problem" (`anthropic.com/engineering/building-c-compiler`, 2026-02-05).
This floor isn't safety bolted onto fan-out, it's what makes fan-out
possible.

**Flag only what matters.** A gap counts when it affects **correctness** or
the brief's **stated requirements**. Everything else is an optional Note,
never a FAIL reason. A reviewer told to find gaps reports some even when
the work is sound, because that's what it was asked to do, and chasing
every finding becomes over-engineering (`code.claude.com/docs/en/best-practices`).

## Contents

- Protocol
- C++ gamedev leaves
- Scouting / recon leaves
- Review / audit output — findings are a work queue, not a verdict
- Script-assisted verification (mechanical leaves)
- Batch verification (same-class waves)
- Compression / rewrite leaves
- Reflective sweep — answer before rendering the verdict
- Verdict: PASS
- Verdict: FAIL
- Verdict: UNKNOWN
- Hard rules
- Changelog

## Protocol

1. Read the brief (AUTHORIZATION / TASK / FILES / CHANGE / VERIFY FIRST /
   CONVENTIONS / ACCEPTANCE / NON-GOALS) and the executor's report. No
   quoted go-signal under AUTHORIZATION → FAIL (executed unauthorized),
   regardless of the diff. Plan-task-text leaves: the gate's quoted
   go-signal is AUTHORIZATION, the plan's file list FILES. DONE report
   missing its Verify-first line → note it; missing **and** the VERIFY
   FIRST fact was wrong in a way the diff shows → FAIL.
2. **Re-run the ACCEPTANCE command yourself** — never trust pasted output;
   a different result than reported → FAIL. Then judge the check itself.
   **Rank the oracle: 1** executable (compiler, assertion, replayed real
   input) **2** fresh-context model **3** same-context model — and name
   the tier in the verdict. Code-emitting leaves have tier 1 by
   definition, so an ACCEPTANCE that only greps the output FAILs on
   ACCEPTANCE even when it passes. **Falsify it:** say what would turn
   this check red; if that doesn't name what the diff changed, it isn't
   verifying the change (live: substring + round-trip assertions over
   generated C++, both green, output that never compiled — one `emcc` call
   found it).
3. Diff the change. Any modified file **not** in FILES → FAIL (scope
   creep), even if the acceptance check passes.
4. Check the diff against CHANGE and NON-GOALS: what was asked, only what
   was asked, none of the forbidden things.
5. Spot-check conventions against the CONVENTIONS exemplar. Cosmetic drift
   is a note; structural drift is a FAIL. When CONVENTIONS names a standards
   doc, check the diff against the **rule IDs it lists** and cite the ID in any
   finding — a violation of a declared rule is a FAIL, not a note, because the
   executor was given the doc before writing. Full-checklist coverage and
   the merge-gate breaking sweep are `smartreview`'s: check the declared
   rules and file anything further as a Note. That seat dedupes against
   what this layer already filed.
6. Report with exactly one verdict template below — **PASS**, **FAIL** or
   **UNKNOWN** — and grade each dimension separately: steps 1–5 are five
   grades, not one impression, so one clean acceptance re-run never softens
   the scope or conventions grade. On a high-risk leaf give each dimension
   its own isolated judge rather than one prompt judging correctness,
   conventions and scope at once.

## C++ gamedev leaves

Additionally apply **`cpp-gamedev-check.md`** (same directory) — the
six-category correctness layer (ownership/lifetime, UB, hot-path perf,
threading, header hygiene, determinism/serialization) a generic accept/scope
pass can't see. The brief's **Engine Profile** (`vanilla` · `custom` ·
`unreal`) gates its profile-specific checks. A blocking finding is a
**FAIL** under CHANGE with the category named, non-blocking is a PASS
Note. Skip for non-C++/non-gamedev leaves.

## Scouting / recon leaves

A scouting leaf produces a context pack or a factual answer, not a diff —
steps 2–4 have nothing to attach to. **Don't force the diff-shaped protocol
onto a leaf with no diff.** Treat the scout's report as an *input to a
decision*, not a verified output: before a scouted fact shapes the plan or
a brief, its **consumer spot-checks it** (re-read the cited `file:line`, or
re-scout if the citation looks thin), sized to how hard the plan leans on
it, and record the checked fact in the plan artifact — the check leaves a
trace or it didn't happen. Lighter, but mandatory. Any Cheap leaf that
*does* produce a diff uses the normal Protocol.

## Review / audit output — findings are a work queue, not a verdict

A review fan-out emits *claims*, and a claim entering a plan is § Scouting
at volume. Three additions: **reproduce a finding before acting on it**
(one live 177-agent review hand-checked 8 of 63: 6 real, 1 not
reproducible, 1 real by another mechanism — expect a fraction wrong, not a
rate); **log every cap, sample or truncation** — that run silently dropped
17 findings to a per-dimension cap of 8, and silence reads as full
coverage; **a refutation is a finding too** — a refuter told to default to
"refuted" when uncertain is an unverified claim with the sign flipped, and
that killed 3 of 4 instances of one real defect.

## Script-assisted verification (mechanical leaves)

When the brief's ACCEPTANCE is a runnable command with exact expected
output and FILES yields an allow-list, protocol steps 2–3 run as a
**script first** — `scripts/smartcheck-mechanical.sh --cmd … --expect …
--allow …` — at zero model cost. Precompute extra input/output pairs where
the contract permits (T8's oracle style): **a model verifier never
re-derives what a script already proved.** The model pass then covers only
steps 1, 4, 5 (authorization, CHANGE-substance, conventions) — it stays
mandatory at balanced-and-above (credit-billed samples it, below) because
it catches *adjacent* defects scripts don't test (live: a
self-contradictory brief ACCEPTANCE, T9), but on template-bound
micro-leaves it has measured ≈zero marginal yield (T7/T8), which is why
budget/max-savings may go script-only per `modes.md`. A script FAIL is a
strike like any smartcheck FAIL.

**Credit-billed default (Copilot at balanced — measured T22/T23/T24):**
the model verify is the dominant fixed tax there (one batched smartcheck
ran 16 cr, 83% of the entire inline arm, T22), so the ladder is script
stage first (mandatory), then the model pass **batched** (§ Batch) **and
sampled** on homogeneous waves ≥5 — verify ⌈N/3⌉, all on any failure —
declared at the plan gate. Shared-blind-spot classes (C++ UB, concurrency,
templates, security) are exempt and keep the full model verifier at tier.
**Untrialed levers, recorded not adopted:** a two-sample Cheap agreement
gate (arXiv:2509.21837, Trust-or-Escalate ICLR-25) and continuous scoring
(arXiv:2607.05391). The gate needs § Hard rules' Cheap-verifier ban amended
first, and neither fixes cross-family bias.

## Batch verification (same-class waves)

Up to **~3 disjoint same-class leaves** MAY share ONE fresh verifier
context — per-verifier setup measured ~15–20k tokens each and verification
**55% of an UNBATCHED wave (T2, Copilot, v4.1.0) — cut to ~25% by this rule
plus script-first (T10/T11)**. Quote the 25%, not the 55%: the 55% is the
cost of not doing this. Hard
rules: the batch runs at the **max tier any member requires**; the verdict
is **one template per leaf** (never a combined verdict); one leaf's FAIL
never infects siblings — each strike is per-leaf; a leaf needing escalation
leaves the batch alone. Independence holds: the batch verifier authored
none of them. A seeded FAIL member raised the batch verdict ~29% (T11),
still ~2.4× under per-leaf verifies, with isolation holding exactly.

## Compression / rewrite leaves

A leaf that rewrites a file meaning-preserving (compression, migration,
restructure) is verified by **independent inventory**: the verifier
derives its own rule inventory from the ORIGINAL
(`git show <pre-ref>:<path>`), never reading the executor's inventory or
claims first, then classifies every rule **PRESERVED / WEAKENED (quote
old and new) / LOST** against the new file. PASS needs zero LOST and zero
unacknowledged WEAKENED. The executor's own coverage count is an input,
never evidence.

## Reflective sweep — answer before rendering the verdict

Four questions about *this diff*, one line each, folded into the verdict
block:

1. **LEAST CONFIDENT:** the one thing you're least sure about. If it's
   load-bearing, that's a FAIL reason, an UNKNOWN, or an explicit re-check.
   Never "nothing." Attach a **recommended action** — a bare doubt with no
   next step is unreportable.
2. **MISSING:** the biggest blind spot of this *review* — a domain you
   can't judge, context you didn't have, the same-family risk.
3. **3-MONTH BREAK:** the most likely way this change breaks later — a
   dated price, a pinned version, a drift-prone cross-reference.
4. **UNSTATED ASSUMPTIONS:** what the executor (or you) assumed but never
   stated. Named is checkable; unnamed is a bias.

Scope guard: observations only, never new work. Wave-level reflection lives
in smartplan's Integrate step, not here.

**Verdict budget** *(output ≈5× input, never cached)*: Notes ≤2 lines;
Sweep clauses ≤15 words each; Evidence = the smallest proving excerpt.
Live verdicts ran 200–600 words where ~100 carries it.

## Verdict: PASS

```
PASS: <one-line task name>
Acceptance re-run:
$ <command>
<pasted real output>
Notes: none | <non-blocking observations>
Sweep: least-confident <…> · missing <…> · 3-month <…> · assumed <…>
```

## Verdict: FAIL

```
FAIL: <one-line task name>
Reasons: <numbered, each tied to a brief section — AUTHORIZATION / ACCEPTANCE / FILES / CHANGE / NON-GOALS / CONVENTIONS / VERIFY FIRST>
Evidence: <re-run output or diff excerpt per reason>
Smallest fix: <the minimal change that would flip this to PASS>
Sweep: least-confident <…> · missing <…> · 3-month <…> · assumed <…>
```

## Verdict: UNKNOWN

When you genuinely can't see enough to judge — a file out of reach, a check
you can't run, a domain you can't assess. A forced binary invents
confidence. Not a strike and not a PASS: it goes back to the orchestrator.

```
UNKNOWN: <one-line task name>
Can't judge: <which dimension, and what is missing>
Unblock by: <the one input or run that would settle it>
Sweep: least-confident <…> · missing <…> · 3-month <…> · assumed <…>
```

## Hard rules

- **Independence:** never verify a leaf you executed, in the context that
  executed it. Fresh context or different model. Do not fix the code
  yourself — verdicts only.
- **Strikes, and a bounded loop:** your FAIL is a strike and goes back to
  the executor **once** with the Smallest fix. Escalation arithmetic is
  flow.md's fail-twice rule (canonical there), attempts persist in
  `run-state.md`. That arithmetic is also the **maximum iteration limit**,
  and the loop needs one: generator-verifier pairs fail three documented
  ways — rubber-stamping, unevaluable work, non-convergent oscillation —
  and the published remedy is a cap plus a *named* fallback
  (`claude.com/blog/multi-agent-coordination-patterns`). Name it at the
  gate: on cap, escalate to a human or return the best attempt with its
  caveats stated. `maxTurns` is the mechanical form on Claude Code.
- **Tiering — the verifier floor tracks the executor** *(research-backed,
  2026-07-09; budget/max-savings may modulate the machinery per `modes.md`,
  but an escalated-to-Mid leaf keeps its Strong/cross-family verifier)*:
  never weaker than the executor it judges. The verifier rides the cost
  ceiling's **joint pick** (`routing.md` § The cost ceiling): executor
  plus verifier are priced as a pair against the incumbent, because on a
  small leaf the verify alone out-eats the Cheap saving (hard floor #4). The **session-diff exception**
  (canonical: flow.md step 4): an Opus-or-stronger session model reading
  the full diff may verify leaves it did not author.
  - **Cheap executor → Mid (Sonnet) verifier.** A Cheap verifier only for
    fully scripted, zero-judgment checks, via
    `scripts/smartcheck-mechanical.sh`. A Cheap seat gets no further than
    that script on its own work, inline included (`routing.md` Cheap
    hard floor #6).
  - **Mid executor → Strong (Opus-or-comparable) verifier.** Critique
    quality scales with judge capability (larger critics miss materially
    fewer real bugs), and Sonnet judging Sonnet adds self-preference risk
    to shared-blind-spot risk. On a seat below Strong that dispatch is
    an ask first (SKILL.md § Seat ceiling). **On Copilot, confirm the Opus pin actually
    lands** — T30 (2026-07-25) saw Opus 4.8 *and* 5 serve un-gated on a
    previously-refusing account, so check rather than assume the Pro+/Max
    gate. Where it is gated the Strong verifier is the
    cross-family peer (Gemini 3.8 Flash / GPT-5.6 Terra, per Family
    decorrelation below), *never* a silent fall-back to
    Sonnet-judging-Sonnet. Name the actual verifier at the gate.
  - **Inline work counts.** The floor reads *executor*, not *subagent* —
    a session seat that wrote the diff IS the executor, so a below-Strong
    seat clearing its own inline work is the self-review banned below.
    `routing.md` § Seat-aware pre-flight names when to spend the verify.
  - **Strong executor → Strong verifier, fresh context, prefer a different
    family.** No stronger tier exists, so independence does what strength
    can't; self-preference bias grows with capability. (Fable is never a
    verifier.)
  Verification is input-dominated (read brief + diff, emit a short
  verdict), so upgrading the verifier is the cheap half of the quality
  budget — **not** license for a weaker judge.
- **Family decorrelation:** same-family executor+verifier share blind
  spots — prefer a cross-family verifier when the harness offers one, at
  minimum a different instance. Current picks (registry is the source of
  truth, re-pinned 2026-09-16): on Copilot, Cheap leaves → **Gemini 3.8
  Flash** (or Sonnet 5); **GPT-5.4** only when the executor is not an
  OpenAI model, since the Cheap seat is OpenAI (GPT-6 Luna first by author
  direction 2026-09-22, GPT-5.6 Luna the untested fall-through until a
  CLI build names `gpt-6-luna`) and would be same-family; never mini/nano
  tiers. GPT-5.4 leaves Copilot
  2026-10-19 and its named successor Sol is Pro+-gated, so plain Pro's
  cross-family pool after that date is Gemini 3.8 Flash and Grok 4.7.
  At max-savings a fresh
  Luna verifies Cheap leaves instead (`modes.md`), an unmeasured
  same-model trade. Mid and Strong leaves (Sonnet, Opus, or GPT-6 Sol once
  a CLI build names it) →
  **Gemini 3.8 Flash** (0.75/3.75, cost-sensitive, Implementer-class,
  ungated on Copilot Pro. Its predecessor 3.6 Flash earned the seat on
  measured recall. 3.8 is unmeasured, so Terra holds C++ UB leaves) or,
  on a non-GPT executor, **GPT-5.6 Terra** only when its thoroughness edge earns
  ~2× the cost. **Measured (T18, Gemini 3.1 Pro): tied Terra on seeded C++
  recall, 14/15 each, at 47% the cost at July prices. T34 cleared 3.6 Flash
  at 8/8, before 3.8 took the pin untested** — don't reach for the pricier judge by habit.
  Copilot's built-in rubber-duck critic (default on from CLI 1.0.58,
  auto-invoke off, every session family from 1.0.87) runs on an
  opposite-family model. It's a second opinion, not a verifier: no
  PASS/FAIL protocol, undisclosed model. When strength and
  decorrelation conflict: shared-blind-spot domains (C++ UB, concurrency,
  security — **UE5 gameplay is all of these**) favor the decorrelated
  judge; subtle-judgment domains favor the stronger same-family judge
  fresh-context. Same-family is an accepted risk noted in
  the verdict, not a FAIL. **Decorrelation has a ceiling (2026-07-25):**
  cross-family fixes *idiosyncratic* blind spots, not *systemic* ones —
  9/17 vulnerability classes crossed ALL three families tested, risk
  tracking task category not model identity (arXiv:2607.20713). Systemic
  classes (security above all) also need the class-specific layer;
  `cpp-gamedev-check.md` is that layer for C++.
  **Self-review stays banned:** a judge's mislabel rate swung 74.4%→3.3%
  on whether the outcome favored its own values (Anthropic Alignment
  Science, 2026-07-13).
- **Optional panel mode:** 3 independent verifiers, majority verdict, zero
  shared context — for higher-risk Cheap leaves (skip under budget
  pressure, `routing.md` § Session-limit), or for a Sonnet leaf whose
  Strong verdict was asked for and declined (the Weaver result). It never
  replaces the Strong floor or its Seat ceiling ask.

## Changelog

History: in the repo's commit log.
