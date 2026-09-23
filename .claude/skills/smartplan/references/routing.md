# routing — task→tier policy (the smartroute seat)

**Use:** loaded by smartplan at flow step 1 when a task's tier isn't
obvious, or read directly for a routing or budget question. **In:** a
task or routing question. **Out:** a tier + effort decision with its floor,
governed by the escalation rule.

**Core policy:** route by *task class*, not by vibes or by whatever model is
loaded. Every class has a floor — the cheapest tier that reliably lands it.
Start at the floor; escalate one tier only on fail-twice (canonical rule:
flow.md). Never route above the floor "to be safe," never below it to save
pennies, never above the session seat unasked (SKILL.md § Seat
ceiling), and never an initial pick above the incumbent's price at all
(§ The cost ceiling).

## Contents

- Tier ladder
- Routing table
- Seat-aware pre-flight — when the seat is below the work
- The second dial — effort
- Seat eligibility — mapping a user-named roster
- The cost ceiling — no initial pick above the incumbent
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
| **Max** | Fable 5.1 *(where exposed)* | Hardest architecture/decomposition *decisions* only. Never research, audit, or implementation. |
| **Strong** | Opus 5.5 (+ cross-vendor Reasoning-class peers) | Planning escalation, cross-cutting judgment, brief-writing at fan-out. |
| **Mid** | The newest Sonnet (GPT-6 Sol first on Copilot) | Near-frontier implementer and default verifier. The workhorse floor. |
| **Cheap** | Haiku 4.5 (Claude Code) · GPT-6 Luna (Copilot), + Mechanical-class peers | Tightly-scoped leaves behind a verifier. Fails *silently* — never unverified. |
| **Script** | No model — an existing script | A deterministic action an already-written script performs. Zero cost, zero drift. |

Both Lunas are classed Implementer but hold Copilot's Cheap seat on price
(hard floor #6). Class decides which leaves one may take. The seat
decides its ceiling.

**Dated 2026-09-22:** Sonnet 5's $2/$10 is Anthropic's standard price (the
$3/$15 step was cancelled 2026-08-10). Opus 5.5 lists at $4/$20. So
Opus→Sonnet is 2× on the current Opus, down from 2.5× on Opus 5. A
fallback from Opus 5.5 to Opus 5 or 4.8 is a climb in price.

**Window follows the seat, and the harness caps it below native** — Copilot
serves Claude at 264K against a native 1M (`copilot.md`, read 2026-08-06,
before Opus 5.5). So **"beyond one
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
| Verifying a leaf | **Floor tracks the executor** — Mid for Cheap leaves, Strong for Mid/Strong leaves (`check.md` § Tiering) | Fully scripted zero-judgment checks may drop to Cheap. Never the executing instance. Max-savings on Copilot: a fresh Luna verifies Cheap leaves instead (`modes.md` matrix). |
| Scouting: find files/symbols/usages, compress a subsystem into a context pack | **Cheap** | Cheap reads feeding a strong decision. No diff → no smartcheck; the consumer spot-checks load-bearing facts (`check.md`). |
| Security-sensitive: authn/authz, secrets, crypto, input validation | **Mid**, never Cheap | Verifier-catchability guardrail. |
| Irreducibly cross-cutting leaf (a mini-plan) | **Strong** | A planner escape, not a "hard leaf." |
| Conversation, judgment calls, tradeoffs with the human | Session's model | Honor the live choice. |

**Escalation:** governed by flow.md's fail-twice rule (Cheap → Mid →
Strong; Strong strike-out → orchestrator takes the leaf over). A target
above the session seat is asked for first. A Cheap seat stops instead
(hard floor #6). Attempts persist in `run-state.md`.

## Seat-aware pre-flight — when the seat is below the work

The table above routes by the work's *shape* and never asks which model is
holding it: same answer on Haiku as on Opus. The gap that leaves is the
case where a cheap seat spends more failing than a strong one spends
landing it. Run this **before** starting, not after a bounce.

**The constraint that shapes it:** the weak seat is the one applying the
test, so a signal needing strong judgment to read fails exactly when it is
needed. Every signal here is countable without reasoning.

Below Strong, escalate the **verify** one tier above the seat when any one
holds:

1. **No executable oracle.** Name the command that goes red. If none
   exists the only judge is judgment, and that is the seat's weakest axis.
2. **The acceptance check won't fit on one line.** The ex-ante proxy for a
   bounce, and bounces are where the money goes (hard floor #4).
3. **The change crosses a public interface or a second caller.** Countable
   from the diff, and blast radius is what a cheap seat under-reads.
4. **It sits on a never-Cheap row** — concurrency, UB, templates,
   security, determinism-critical code.

**Escalating emits an artifact, never an intention.** Write the missing
check, or write the verify brief out in full — the leaf, the acceptance,
what would turn it red. Measured: detection is the easy half and enactment
is the half that fails. Every with-skill response named its signal
correctly, then a third of them stopped at "should be verified", "the next
step is a test", or handed the run back to the user. That last one is the
stall the spiral guard already bans, arriving by a different door.

That escalates the verify, not the work: the seat still does it and a
stronger judge reads the diff. Verification is input-dominated, so it is
the cheap half of the quality budget. **Two or more signals and the work
itself starts Mid** — at that density the bounce is likelier than not.

**A tier above the seat is an ask before it is a dispatch** (SKILL.md §
Seat ceiling). The artifact rule and the ask compose rather than
compete: write the check or the brief, ask in one line, dispatch on the
yes. What waits on the user is the spend, never the writing. A Cheap
seat skips the ask and stops with the artifact written (hard floor #6).

This is prediction, which the class floors above already do. What stays
banned is escalating on a hunch: no signal fires, start at the floor and
let fail-twice do its job.

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
- **Pick a level at the start and hold it** — changing effort mid-session on most models
  invalidates the cached prefix (`caching.md`).
- **Low effort means fewer tool calls**, so an underspecified brief fails
  *harder* there — it raises the bar on brief quality. A low-effort
  executor can also stop noticing it's stuck, which weakens its BLOCKED.
- **A seat's effort pin lives in its frontmatter:** `effort:`, or
  `reasoningEffort:` on Copilot (`copilot.md`). `--effort` sets the session.

## Seat eligibility — mapping a user-named roster

Named models are a **roster to seat by capability class, never a routing
instruction to obey literally** — naming a stronger model doesn't change
what the work needs. **`model-classes.md` holds the class→seat map** and
the per-model registry (e.g. Fable is Reasoning-class but **planner-only**,
never a verifier or a fail-twice target). Provisional rows are
deliberate-trial only unless the author seats one. **Mapping procedure** at Plan time: (1) classify each
named model by published price + benchmarks, never silently guess; (2)
seat from the roster: planner = strongest Reasoning-class named, floors =
cheapest named class covering each task class, verifier per `check.md` §
Tiering; (3) a roster is a *preference*, not an allowlist — fill missing
seats from the harness and say so; only a stated hard constraint seats a
too-strong model low, flagged as an over-tier; (4) **refuse over-seating by
default** — "use Opus to implement" is reseated and presented at the gate;
an explicit "seat it anyway" is honored and recorded, never a default.
**Newest version first:** seat and dispatch the newest version of a model
line the harness serves, the previous one as fallback (`model-classes.md`
§ How to edit). A roster naming an older version gets the newest, said at
the gate.

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

## The cost ceiling — no initial pick above the incumbent

Cheap hard floor #6's rule, generalized to every seat: **at dispatch
time, an initial seat pick never costs more effectively than the model
currently doing the job — the session seat, or the seat handing the leaf
down.** Seat each leaf on the cheapest registry row that (1) meets the
class floor for the leaf's class, (2) holds measured adequacy
(`model-classes.md`: candidate and provisional rows are
deliberate-trial-only, never default picks unless the author or its
newest-version rule seats them), (3) passes the joint
executor-plus-verifier bounce breakeven (hard floor #4 — the ceiling
compares the PAIR's combined cost, because on small leaves the verify
alone exceeds the Cheap saving), and (4) prices no more than the
incumbent. `scripts/seat-map.py compare <candidate> <incumbent>` is the
deterministic list-price check: exit 1 means above on both axes.

**Climbs above the seat stay legal only through the named gates** — the
ask-first Seat ceiling (SKILL.md), fail-twice escalation with its report
attached, the planner seat, and the verifier floor (`check.md` §
Tiering, including a cross-family verifier priced over a Cheap
executor). Each is a deliberate spend named at the gate, never a
default. A Cheap seat climbs none of them (hard floor #6).

**Effective cost, not list price, where it flips:** the ~30% tokenizer
multiple on newer rows, cache-read tiers, plan credit multipliers
(6.9/1.7/24 on GLM-5.3 vs 2.3/0.56/8 on Flash), DeepSeek peak vs
off-peak, and the switch cost of re-paying a warm prefix cold mid-job.
Below break-even warm prefix, stay on the incumbent even when the
alternative is cheaper per token.

**Pre-conditions, or the rule no-ops:** the incumbent must be known
(under Copilot Auto it is not, and subagent pins are ignored — never
mix, `copilot.md`; Auto's inherit-everything equalizes per-token price
while each subagent still pays its own context reload, so never read
Auto as free tiering), and the registry row must sit inside gate (n)'s
30-day freshness line. When the executor-relative verify floor and this
seat-relative ceiling diverge, the floor sets the minimum and the ask
bridges everything above the seat. **Verify the landing from the bill** — `/usage`
by model, `/tasks`, workflow progress records — never the dispatch
intent: a tier that silently resolved elsewhere voids the comparison.
Pre-registered validation: `the development repo's benchmark records
t41-cost-ceiling-validation-prereg.md`.

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
   is scripted. **The one bought exception:** max-savings on Copilot
   verifies Cheap leaves with a fresh Luna (`modes.md` matrix) at a
   fraction of a Mid verify's input price — an unmeasured same-model
   trade, said out loud at the gate.
5. **C++ isn't automatically cheap.** Template metaprogramming, engine
   internals, perf hot-paths, and determinism-critical code are never
   Cheap-floor — they fail silently in ways a clean compile won't catch.
6. **Never dispatch above its own price.** A Cheap seat, the session
   model or a leaf, hands work only to the same model, a model priced no
   higher on input or output (`model-classes.md`), or a script. The
   general form of this rule binds every seat: see § The cost ceiling. A cheaper
   model never stands in for the verify its own work needs. That check
   stays the script (`check.md` § Tiering). It never asks for more. Work
   that needs a stronger model needs a stronger session, which the user
   picks. Planning stays off this seat (#1). Its fan-out is mechanical
   leaves whose check is fully scripted (`check.md` § Tiering). Where the
   work needs more (a Mid verify, the spiral diagnosis, a fail-twice
   target, a never-Cheap class), it writes the brief or the ESCALATION
   REPORT in full, stops, and names the session model to switch to.

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
