# Quality↔cost modes — one dial over every discretionary knob

*Load from flow.md § Quality↔cost mode. The dial biases the judgment
calls the flow already makes; it never overrides the invariants at the
bottom. Model names and prices below are illustrative — `model-classes.md`
is the registry and wins on any drift.*

## Setting it

Resolution order (first wins): an explicit per-invocation ask
(`/smartplan --mode budget …`, or plain words — "budget mode", "max
quality for this one") → a brief's MODE line (per-leaf override,
`brief.md` § Dispatch) → the `{{MODE}}` token set once for the project →
the shipped default — **max-quality** here, **budget** on Copilot CLI.
A non-default mode is recorded per leaf in `run-state.md`'s note column;
the floors below don't move, whatever the default is.

**The default follows the billing meter.** No per-token meter runs on a
flat subscription (Claude Code), so the quality column's extras — Opus
planner, one-strike escalation, 3-verifier panel — cost only wall-clock,
and are worth taking by default. Copilot meters credits per token, where
T27 measured `budget` at equal quality for **60% of balanced's corrected
cost** — the Copilot export ships that default
hard-coded. Neither is free: max-quality still spends wall-clock and
rate-limit headroom, so step down when a session races a weekly cap.

## The matrix

| Knob | **max-quality** (default) | high-quality | balanced | **budget** (default on Copilot) | max-savings |
| --- | --- | --- | --- | --- | --- |
| Planner seat | Opus; Fable freely for the hardest decomposition (planning only, as ever) | Opus, no drop-down | Opus default, drop on fit | Sonnet default; Opus only for cross-cutting or ambiguous plans | Sonnet always; flag when a plan needed more |
| Implementer floor | Sonnet for mechanical, Opus for correctness-sensitive | Today's floors; doubt rounds up to Mid | Class floors (`routing.md`) | Cheap wherever the check is scriptable, incl. borderline-mechanical | Cheap for anything checkable; Mid only via fail-twice |
| Verify | Verifier one tier above executor (capped at Strong — Strong leaves get a fresh cross-family Strong verifier, never Fable), no session-diff exception; 3-verifier decorrelated panel on correctness-sensitive leaves | No session-diff exception; Strong verify on Mid leaves | `check.md` tiering + the documented session-diff exception; credit-billed harness → check.md's credit-billed default (script-first, sampled batch) | Exception preferred where legal; script pre-checks first | Script checks wherever scriptable; single Mid-verifier cap (an escalated-to-Mid leaf keeps its Strong/cross-family verifier — `check.md` hard rule); sampling on homogeneous waves ≥5 — verify ⌈N/3⌉, all on any failure (**accepts silent-failure risk on unsampled leaves; said out loud at the gate**) |
| Escalation | One strike escalates | fail-twice (canonical) | fail-twice | fail-twice | fail-twice; a Reserve (Opus) dispatch needs an explicit user OK |
| Effort | high/max everywhere | high on plan + verify | Harness defaults; low on Cheap leaves | low on Cheap + mechanical Mid | low everywhere but the plan turn |
| Output register | Full prose allowed (templates still apply) | Terse templates (`check.md` § Verdict budget) | Terse templates + telegraphic agent-consumed prose (caveman *lite*) | Caveman *full* on all agent-consumed prose | Caveman *ultra* — fragments |
| Fan-out | ≤3 leaves/wave, extra Integrate attention | 3–5 | 3–5 (flow default) | Size to survive caps; wider cheap waves | Width stops paying past ≥5 (T27); batch/sample the verify |
| Inline output ceiling | No ceiling (templates apply) | One-paragraph close | One-paragraph close | Routing line + diffs only; echo-free edits (never reprint file content); ≤3-line close; no offers/retro | Same as budget, fragments allowed |

**Inline output ceiling — the narration cap.**
Output bills ≈5× input, so the ceiling row above is a hard cap on the
session's own narration during inline work: at budget and below, the
routing line and the diffs ARE the deliverable — never reprint file
contents after an edit, close in ≤3 lines, skip offers and retros. It
narrows the gap against a bare session without closing it: T29 measured
**1.12× at budget**, verdict "<1× at budget: NOT met" (k=1). The one
sub-1× point on record is T30's 0.88×, and that session routed off the
skill *description* and never loaded this body — so <1× is a routing
result, not a ceiling result.

## The caveman register (output-side language compression)

Levels borrowed from the upstream skill (github.com/juliusbrussee/caveman
— *lite* / *full* / *ultra*; upstream claims ~65% avg output reduction,
range 22–87%, and itself warns the savings are **output-only** and go
**net-negative on already-terse text**). Application here, at every mode:
the fixed DONE/BLOCKED/verdict **templates never change register** —
they're already terse contracts; the register applies to **prose whose
only reader is another model seat** (scout packs, report narration,
investigation notes). Code, paths, commands, errors, and quoted evidence
stay byte-verbatim at every level — invariant, not a mode choice.
Human-facing turns are never telegraphic; only `max-quality` changes the
*agent-facing* register (back to full prose, for maximum executor
comprehension on the hardest work).

Quality evidence: the register has now run live with zero measured
quality loss — T7 (register-compliant fragments, verifier-confirmed),
T8 (5-leaf × 2 arms = 50-case hidden oracle, 25/25 per arm), T13
(judgment-class, 2 matched pairs, 11/11 per arm). On template-bound micro-leaves it saves ≈nothing (upstream's own
net-negative-on-terse warning, observed) — its value is on prose-heavy
packs/reports, still upstream-claimed rather than measured here. So apply
it only there; don't spend instruction budget forcing *ultra* onto
micro-leaves where it can't pay.

## Mode-invariant floors (no mode may dial these)

- The **human plan gate** and verbatim AUTHORIZATION quoting.
- **Never merge unverified** — max-savings may swap a model verifier for
  a script/sample only where `check.md` § Tiering already permits a
  scripted check; a zero-verification merge doesn't exist at any mode.
- **Shared-blind-spot classes keep the full tiered verifier at every
  mode** — C++ UB, concurrency, templates, security. No mode scripts,
  batches or samples these away, and budget/max-savings' script-only and
  ⌈N/3⌉ rows don't reach them (`check.md` § Credit-billed default,
  `SKILL.md` § Verify floor).
- **Honesty rules** — the development repo's claim ledger discipline, no fabricated evidence,
  acceptance re-runs over pasted claims.
- **Attempt bookkeeping** — strikes persist in `run-state.md` at every
  mode.
- **Byte-verbatim code/paths/errors** in every register.

## Harness mapping

- **Claude Code (§A):** floors move via per-call `model:`; effort via
  `effort:`; the panel is 3 concurrent verifier dispatches, cross-family
  when the roster allows.
- **Copilot (§B):** floors pick among `@smartplan-implementer-cheap` /
  `-implementer` / `-implementer-reserve`; effort via `--effort`; budget
  modes lean on `/limits` soft caps (`copilot.md`). **Confirm the Opus pin
  actually lands:** the documented **Pro+/Max** requirement is the base-Pro
  expectation, and a refusal prints a downgrade warning (live 2026-07-11) —
  but T30 (2026-07-25, DB-confirmed) saw Opus 4.8 *and* Opus 5 both serve
  un-gated on the very account that refused 4.8 in July. Check the pin
  rather than pre-emptively degrading, and if it does refuse, say so at the
  gate rather than presenting the mode as landed. **Route the verify
  cross-family on price either way**, not because Opus is gated: `check.md`
  § Tiering sends every Mid leaf to a Strong verifier — prefer the
  Gemini/GPT-5.6 Terra judge (`check.md` § Family decorrelation; Gemini is
  the measured cost-sensitive default, T18), never a silent
  Sonnet-judging-Sonnet self-check. Panel concurrency rides the
  plan's subagent cap — it may partially serialize on Pro. **And the
  effort lever excludes Haiku** (live 2026-07-11: `--effort` on
  `claude-haiku-4.5` errors pre-flight, "does not support reasoning
  effort configuration") — budget/max-savings' low-effort row applies to
  Sonnet-and-up leaves only on Copilot; the Cheap floor's savings there
  come from the register + verify machinery rows alone.

## Measured economics + budget personas (Copilot, live 2026-07-13)

T27 ran all five modes end to end on one canonical 3-leaf mechanical wave
(k=1, Pro+, the development repo's benchmark records) — **this replaces T7's projected 5-mode
table for this shape of task**. Measured credits, balanced at its
corrected cost (the original run wrongly gave it budget's script-only
free ride):

| Mode | cr/wave | vs balanced | Pro 1,500/mo | Pro+ 7,000/mo |
| --- | --- | --- | --- | --- |
| max-quality | 87.6 | 386% | ~17 waves | ~80 |
| high-quality | 54.5 | 240% | ~28 | ~128 |
| **balanced** | 22.7 | 100% | ~66 | ~308 |
| budget | 13.6 | **60%** | ~110 | ~514 |
| max-savings | ~14.4 *(clean est.)* | 63% | ~104 | ~486 |

Personas: **flat-subscription (Claude Code)** → any mode; `max-quality`
ships as the default there, and what argues for stepping down is
wall-clock or a rate-limit cap, never token price. **~$40/mo ≈ Copilot Pro+
(7,000 cr)** → every mode lands incl. real Opus rows; budget default,
balanced where per-leaf model verify is wanted.
**Copilot Pro (1,500 cr)** → budget default, max-savings for
wide waves; max-quality/high-quality run Pro-degraded **only if the Opus pin
actually refuses** — T30 saw it serve un-gated (mapping above). **Measured at wave scale (T8, 5-leaf arms,
matched-pair tasks, 50-case hidden oracle):** max-savings delivered
**identical quality at 54% of balanced cost** (5.34 vs 9.98 cr/leaf) on
scriptable mechanical leaves — sampling live-tested, the unsampled leaves
hid nothing, and a real false-BLOCKED (~9% organic bounce, 1/11) was
orchestrator-visible regardless of sampling since BLOCKED always
surfaces. Judgment-class too (T13, 2 matched pairs): zero delta at 32% of
balanced cost, convention-standard judgment only.

## Honest note

budget/max-savings **increase silent-failure exposure by design** — the
matrix trades verification strength for spend, and the sampling row says
so at the gate rather than burying it. If a max-savings wave bounces past
routing.md's ~20–30% breakeven, the mode is costing more than balanced
would: say so and recommend stepping up one mode. Quality parity is
**measured** on the two classes above (T8, T13 — zero delta each); the
≥90% bar holds for mechanisms, costs, and those classes, and
novel-ambiguity judgment stays the one unmeasured frontier.

The max-savings-vs-balanced cost figure is **not one number** — quote the
right one: **63%** (T27, 3-leaf mechanical, against balanced's corrected
verify); **54%** (T8, 5-leaf mechanical, 50-case hidden oracle); **32%**
(T13, judgment-class, 2 matched pairs). All three are measured, and T7's
old ~40% projection is retired. The gap mostly closes past ≥5 leaves: in
T27's no-failure steady state balanced and max-savings landed ~23 vs ~22
cr, both sampling ⌈N/3⌉.

## Budget preflight (budget / max-savings — print before the work)

On an **explicit** `budget`/`max-savings` ask or a stated tight budget,
print this first, then run the max-savings column above (a standing
budget default alone doesn't re-print it). It confirms the **launch
levers the skill can't set itself** (the human's, at session start):

1. **Model:** Auto (10% off, cache-safe) or explicit cheap; never
   Opus/Fable for a whole session; mechanical → GPT-5 mini ($0.25/$2,
   cheapest metered — the old 0×/"included" status ended 2026-06-01).
2. **Cap leaves, not the orchestrator:** `--max-ai-credits` bounds a
   runaway repair, but a cap can suppress skill loading (T25) — cap leaves.
3. **Warm cache:** `--resume` for repairs; minimal context (re-read every
   turn).
4. **Effort/output:** `--effort low` on mechanical turns; terse output
   (≈5× input).

Full human-facing guide: `docs/copilot-on-a-budget.md`.
