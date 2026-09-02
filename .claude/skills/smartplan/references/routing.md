# routing — task→tier policy (the smartroute seat)

**Use:** loaded by smartplan at flow step 1 when a task's tier isn't
obvious, or read directly for a routing or budget question. **In:** a
task or routing question. **Out:** a tier + effort decision with its floor,
governed by the escalation rule.

**Core policy:** route by *task class*, not by vibes or by whatever model is
loaded. Every class has a floor — the cheapest tier that reliably lands it.
Start at the floor; escalate one tier only on fail-twice (canonical rule:
flow.md). Never route above the floor "to be safe," never below it to save
pennies.

## Contents

- Tier ladder
- Routing table
- The second dial — effort
- Seat eligibility — mapping a user-named roster
- C++ gamedev task classes
- What a wave costs (T33 · T35, 2026-08-05, Copilot Pro)
- Session-limit pressure (caps are a routing signal)
- Hard floors for the Cheap class (non-negotiable)
- Harness dispatch notes
- Outcome record and amendments

## Tier ladder

Strongest → cheapest (live roster: `/model`). **`model-classes.md` owns
which model sits in each tier** — edit classifications there, not here.

| Tier | Anchor model | Character |
| --- | --- | --- |
| **Max** | Fable 5 *(where exposed)* | Hardest architecture/decomposition *decisions* only. Never research, audit, or implementation. |
| **Strong** | Opus 5 (+ cross-vendor Reasoning-class peers) | Planning escalation, cross-cutting judgment, brief-writing at fan-out. |
| **Mid** | The newest Sonnet | Near-frontier implementer and default verifier. The workhorse floor. |
| **Cheap** | Haiku 4.5 (+ Mechanical-class peers) | Tightly-scoped leaves behind a verifier. Fails *silently* — never unverified. |
| **Script** | No model — an existing script | A deterministic action an already-written script performs. Zero cost, zero drift. |

**Dated 2026-08-12:** Sonnet 5's $2/$10 became Anthropic's standard price on
2026-08-10 — the 2026-09-01 step to $3/$15 was cancelled. The Opus→Sonnet
multiple stays 2.5× and the fan-out break-even does not move.

**Window follows the seat, and the harness caps it below native** — Copilot
serves Claude at 264K against Opus 5's 1M (`copilot.md`), so **"beyond one
context" is a live regime there and nearly unreachable in Claude Code: the
same task routes differently per harness.** Within one, a subagent's window
is its *own* model's — five Haiku seats give five 200k, not five 1M — so
scale argues for fan-out only at the same tier, via a fork, or on Sonnet 5
seats. Routing down shrinks the window you fanned out to get.

## Routing table

| Task class | Floor | Notes |
| --- | --- | --- |
| Architecture, planning, decomposition, ambiguous scope | **Planner seat** — Opus default, drop-on-fit per flow.md | N× blast radius. Never Mechanical-class. |
| Audit / review / synthesis feeding a plan | **Planner seat** (cap Opus, never Fable) | A weak audit cascades into a weak plan. |
| Writing leaf briefs | **Planner seat**; bias up a tier before a wide fan-out | Brief quality is bought once, reused N times. |
| Leaf implementation from an approved brief | **Mid** | Sonnet lands briefed leaves at near-Opus parity. |
| Leaf implementation, *single-concern + scripted acceptance check* | **Cheap** — only via smartexec behind smartcheck | The family's point. No brief or no verifier → route Mid. |
| Mechanical transforms: renames, formatting, codemods, boilerplate-from-exemplar, test skeletons, docstrings, commit/changelog text | **Cheap** *(lone leaf → Mid, hard-floor #4)* | Imitation work — give an exemplar; Cheap-class models imitate far better than they follow prose. |
| Verifying a leaf | **Floor tracks the executor** — Mid for Cheap leaves, Strong for Mid/Strong leaves (`check.md` § Tiering) | Fully scripted zero-judgment checks may drop to Cheap. Never the executing instance. |
| Scouting: find files/symbols/usages, compress a subsystem into a context pack | **Cheap** | Cheap reads feeding a strong decision. No diff → no smartcheck; the consumer spot-checks load-bearing facts (`check.md`). |
| Security-sensitive: authn/authz, secrets, crypto, input validation | **Mid**, never Cheap | Verifier-catchability guardrail. |
| Irreducibly cross-cutting leaf (a mini-plan) | **Strong** | A planner escape, not a "hard leaf." |
| Conversation, judgment calls, tradeoffs with the human | Session's model | Honor the live choice. |

**Escalation:** governed by flow.md's fail-twice rule (Cheap → Mid →
Strong; Strong strike-out → orchestrator takes the leaf over). Attempts
persist in `run-state.md`.

## The second dial — effort

Tier isn't the only axis. When a run comes out wrong, ask which gap it was:
it **didn't know enough** → raise the model; it **didn't try hard enough**
→ raise effort. A briefed leaf missing on thoroughness wants effort first,
and that's usually cheaper. Seat effort at plan time, next to the tier.

- **Not every seat has the dial**, and the hole is bigger than it looks.
  Haiku 4.5 and Sonnet 4.5 have **none**; `xhigh` is missing on Opus 4.6
  and Sonnet 4.6. **T36 (2026-08-05): on Sonnet 5 via Copilot the dial moved
  nothing on the BILL below `max`** — `none`/`low`/`medium`/`high` within
  0.4%; only `max` moved it (1.92×). Quality tied everywhere, but on a task
  `none` already aced, so that's a ceiling, not parity evidence.
- **Pick a level at the start and hold it** — changing effort mid-session
  invalidates the cached prefix (`caching.md`).
- **Low effort means fewer tool calls**, so an underspecified brief fails
  *harder* there — it raises the bar on brief quality.
- **Frontmatter effort is §A-only.** On Copilot it's session-wide
  (`--effort`) or a repo-level per-agent pin (`copilot.md`).

## Seat eligibility — mapping a user-named roster

Named models are a **roster to seat by capability class, never a routing
instruction to obey literally** — naming a stronger model doesn't change
what the work needs. **`model-classes.md` holds the class→seat map** and
the per-model registry (e.g. Fable is Reasoning-class but **planner-only**,
never a verifier or a fail-twice target). Provisional rows are
deliberate-trial only. **Mapping procedure** at Plan time: (1) classify each
named model by published price + benchmarks, never silently guess; (2)
seat from the roster: planner = strongest Reasoning-class named, floors =
cheapest named class covering each task class, verifier per `check.md` §
Tiering; (3) a roster is a *preference*, not an allowlist — fill missing
seats from the harness and say so; only a stated hard constraint seats a
too-strong model low, flagged as an over-tier; (4) **refuse over-seating by
default** — "use Opus to implement" is reseated and presented at the gate;
an explicit "seat it anyway" is honored and recorded, never a default.

## C++ gamedev task classes

Engine Profile (`vanilla` default · `custom` · `unreal`) picks the lens;
the six-category correctness taxonomy in `cpp-gamedev-check.md` gates these
leaves at smartcheck time.

| Task class | Floor | Notes |
| --- | --- | --- |
| Boilerplate/scaffolding — component/class stubs, accessors, data-glue | **Cheap** (behind smartcheck) *(lone stub → Mid)* | Imitation-shaped; the profile supplies the pattern (e.g. `unreal` UCLASS/UPROPERTY stubs). The forced verify floor swamps the saving on narrow waves — hard-floor #4. |
| Serialization/reflection glue, data tables/config | **Cheap + smartcheck** | Verifier checks schema/format correctness, not just compile. |
| Gameplay logic, build-system edits (CMake / Build.cs) | **Mid + check** | Blast radius past the touched file. |
| Perf hot-path, template metaprogramming, engine architecture | **Planner seat / Strong** | Architecture-shaped; `custom`-profile subsystem design defaults here (no engine underneath to absorb a mistake). |

**Compile is the acceptance signal:** a C++ leaf's DONE requires a pasted
clean compile of the touched target — a leaf that doesn't compile is FAILED
regardless of how the diff reads.

## What a wave costs (T33 · T35, 2026-08-05, Copilot Pro)

Same task both arms, within each record: tiered cost **2.78×** inline at
one leaf (T33) and **2.37×** at five (T35), quality identical every run.
The planner billed **5.14 cr** in both, one brief or five.

**Don't fit a per-leaf slope across them** — different tasks (hard at N=1,
five easy at N=5), so the line measures difficulty, not width. Fan-out
earns its keep on scale, rework, a verify gate, or wall clock, never
per-leaf price.

## Session-limit pressure (caps are a routing signal)

1. **Shift mechanical work down immediately** — everything in the Cheap
   rows drops to the Cheap floor, and to Script wherever a script already
   covers the action.
2. **Defer judgment work, don't demote it** — planning, brief-writing, and
   plan-feeding audits WAIT for the reset; a capped plan still has N×
   blast radius.
3. **Spend remaining budget by seat value** — a brief or a verdict buys
   more than another mechanical leaf.
4. **Design fan-outs cap-aware** — a wide wave can die mid-run on a session
   limit (observed live); order items most-important-first and size the
   batch to the remaining budget. Harness ceilings count too — subagent
   caps count *finished* leaves, nesting depth is capped; the §A/§B
   references have the numbers.

## Hard floors for the Cheap class (non-negotiable)

1. **Never plan, decompose, or make cross-cutting decisions.** Not even
   "just a small refactor plan."
2. **Never run unbriefed.** A Cheap-class executor gets a smartbrief or it
   gets nothing.
3. **Never merge unverified.** smartcheck gates every Cheap-produced diff.
4. **Cheap is cheap per-token, not per-merge.** Above a **~20-30% bounce
   rate** the escalation rounds cost more than the tier saves — that's the
   reclassify trigger, and breakeven must amortize the fixed per-leaf
   overhead (brief + independent verify + bookkeeping). **Measured (live,
   2026-07-11, 5 samples):** the mandatory Mid verify runs **1.5–2× the
   executor's own tokens** — on a small leaf that alone exceeds the
   Cheap-vs-Mid saving *at a 0% bounce rate*. Route tiny leaves Mid (+ the
   session-diff-read exception) or Script-check; the Cheap floor pays only
   on leaves wide or large enough to out-earn the verify, or whose verify
   is scripted.
5. **C++ isn't automatically cheap.** Template metaprogramming, engine
   internals, perf hot-paths, and determinism-critical code are never
   Cheap-floor — they fail silently in ways a clean compile won't catch.

## Harness dispatch notes

Dispatch mechanics live in flow.md §A/§B and their deep references
(`claude-code.md`, `copilot.md`) — don't re-derive them here. **Once per
session, verify reality.** Claude Code's `/usage` Session block prints
`Usage by model:` lines with per-model token counts and a locally-computed
dollar figure. On a Max/Pro seat those dollars aren't a bill, but the model
attribution is real, which makes it the free tiering oracle: run a Cheap
wave, then look for whether a line for that model appears at all. An
all-Opus breakdown after a Haiku wave is in-harness evidence of the #43869
silent-inherit (`claude-code.md`). Copilot: `/context` with `/experimental`
(`/usage` is per-model totals only). Judge on **cost-per-merged-change**,
not cost-per-token.

## Outcome record and amendments

`run-state.md` is the run's outcome record (shape: `artifacts.md`) — each
leaf's row closes with final status, attempts, and any escalation or
over-tier note. Floor reclassification is observational: no clean class
fit, a floor that under- or over-tiers, or roster drift → capture the case
plus a proposed amendment and surface it through smartplan's "Evolving this
skill". Never self-mutate unreviewed. History:
the repo's commit log.
