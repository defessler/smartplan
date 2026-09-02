# smartplan §A deep reference — Claude Code dispatch mechanics

*Load on demand from flow.md §A — when actually dispatching a wave on
Claude Code, wiring enforcement, or making a caching/budget call. Not part
of the per-invocation read.*

## Contents

- The lever, precisely
- Opus 5 seats: two gaps that read as model failure
- Whether the tier lands — contested; say so and route around it
- Caching-aware fan-out
- Adjacent primitives (know when NOT to use them)
- Mechanical enforcement (optional, shipped)
- Structural tool-lockdown (shipped seats)
- Cost levers (researched 2026-07-13 — sources: the development repo's research notes)

## The lever, precisely

- **Resolution order** (documented): `CLAUDE_CODE_SUBAGENT_MODEL` env var >
  per-call `model:` param > subagent frontmatter > session model.
  <!-- claim:cc-subagent-model-resolution-order --> Since v2.1.196 `inherit`
  is **identical to leaving the variable unset** (re-verified 2026-08-12):
  it clears the pin and lets resolution fall through to the per-call param,
  rather than pinning leaves to the session model.
- **Per-leaf lever = per-call `model:`** on each dispatch. **Wave
  guarantee:** `export CLAUDE_CODE_SUBAGENT_MODEL=sonnet` before an
  implementer wave so no leaf can silently inherit the session (priciest)
  model, then **unset it** after (`=inherit` is the same thing, per above).
  The swap is subagent-scoped and cache-safe.
  Switching the **main** session's model or effort mid-run busts *its*
  prompt cache instead — see `caching.md`.
- **Effort has no per-dispatch knob here.** An ad-hoc `Agent()` call takes
  `model` but *not* `effort`, so on Claude Code the second axis is set
  per-seat in agent frontmatter (`effort:`) or per-call only inside a
  workflow script. Copilot's `--effort` is session-global. Plan the effort
  drop into the seat, not the dispatch.
  <!-- claim:cc-agent-call-has-no-effort-param -->
- **`/fast` is not a cheap tier.** Fast mode runs Opus with faster output —
  same model, not a smaller one (Opus 5/4.8). It buys latency, never
  budget, and the header is part of the cache key, so toggling it mid-run
  re-reads the history uncached. Don't let it stand in for a tier drop.
  <!-- claim:cc-fast-mode-is-not-a-model-downgrade -->
- **A seat's window is sized by its own model, not yours** — five Haiku
  seats give five 200k windows, not five 1M. The beyond-one-context
  argument only holds for same-tier fan-out, forks, or Sonnet 5 seats.
- **Fan-out mechanism:** subagents run **background-by-default** (since
  v2.1.198; API errors surface as failures since v2.1.199) — wide dispatch
  is just *fire every Agent call*, then monitor the agent panel.
- **Isolation:** parallel edit leaves get `isolation: worktree` — each a
  temporary git worktree, auto-cleaned when unchanged; guards against a
  stray shared-file touch clobbering a sibling. **Trade-off:** worktrees do
  NOT share the prompt cache (`caching.md`) — so isolate only leaves that
  genuinely edit in parallel; read-only/scout dispatches stay same-directory
  to ride the shared-prefix discount.
- **A `fork` can't be down-tiered — `model` is ignored, nothing errors.**
  It always runs the *session* model on the parent's warm prefix, so on an
  Opus session every fork is an Opus leaf and the tier you passed is a
  no-op you find in the bill. Fork is a **context** lever, never a cost
  one: use it for plan-feeding audit/synthesis that needs the whole
  session, and dispatch a normal subagent to route down.
  <!-- claim:cc-fork-ignores-model-override -->
- **Same-tier retry = resume, not re-dispatch:** a completed subagent sent
  a `SendMessage` auto-resumes in the background with its full history, so
  flow.md's one same-tier retry rides the executor's warm cache instead of
  a cold rebuild. Tier-safe on ≥2.1.211. The §B analog is `--resume`.
- **Hard ceilings:** 200 spawns/session (v2.1.212+; finished subagents
  count, so a long run drains it invisibly;
  `CLAUDE_CODE_MAX_SUBAGENTS_PER_SESSION` raises, `/clear` resets); **20
  concurrent** (v2.1.217; `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`; exempt
  under ultracode); `--max-budget-usd` halts running background subagents
  at the cap. **Depth 3** since v2.1.219
  (`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`) — the docs name this family's
  shape as the reason ("a reviewer subagent that dispatches a verifier per
  finding"). At the limit a seat doesn't error, it does the work itself
  and returns one summary. Workflows carry their own caps (16 concurrent,
  1,000 agents/run, <15 guideline). Size waves to these as `routing.md`
  sizes to credit caps.

## Opus 5 seats: two gaps that read as model failure

- **Auto mode is miscalibrated.** `tengu_auto_mode_config.severityByModel`
  ships no `claude-opus-5` entry (#80977; verified in this box's
  `.claude.json` 2026-08-06), so it falls to a stricter default blocking
  routine actions 4.8 allowed. Use plan mode or allow-rules
  <!-- claim:cc-automode-missing-opus5-thresholds -->
- **The system prompt can carry "don't call the Agent tool unless the user
  requested it."** Seen first-hand on Opus 5, 2026-08-06; Opus-5-only is
  **unverified**. It opposes the fan-out route, so **the plan gate resolves
  it**: step 2's approval IS that request.
  <!-- claim:cc-opus5-dont-dispatch-injection -->

## Whether the tier lands — contested; say so and route around it

Issue **#43869** ("all mechanisms resolve to the parent model") is **open**
(date of record: the development repo's claim ledger) and reports the per-call `model:`,
frontmatter, and env-var levers each ignored on some paths.
<!-- claim:cc-issue-43869-open -->

**`/usage` is the in-harness oracle.** Its Session block prints a
`Usage by model:` breakdown — per-model token counts plus a dollar figure
computed locally at list rates. On a Max or Pro seat the dollars aren't a
bill, but the **model attribution is real**, so the #43869 check is free
and offline: dispatch a cheap-tier wave, then look for whether a line for
that model appears at all. An all-Opus breakdown after a Haiku wave is the
failure, caught without leaving the session.

**Never grep the transcript for it.** A subagent's JSONL `model` field
records the *requested* model, not the one that ran or billed — the #43869
repro read `claude-sonnet-4-6` for all three seats while the dashboard
showed the Sonnet quota untouched. A check built on transcript metadata
measures nothing. One separate path *does* log a greppable line,
`Subagent model "X" is not in the availableModels allowlist; inheriting
the parent model instead`, so grep the log before calling it a #43869 hit.

**Partial fixes:** v2.1.211 stopped an override reverting to the parent on
resume or follow-up, so multi-turn dispatches are tier-safe only on
≥2.1.211, and v2.1.222 covers the allowlist case. #43869 stays open, so
treat "the cheap tier landed" as unconfirmed until `/usage` shows the line.

**Measurement hazard: the safety fallback.** A content-flagged request
re-runs on a different model and the **session continues** on that
fallback. It can fire on the very first request, which carries your
CLAUDE.md content and git status. Set `switchModelsOnFlag: false` in any
benchmark harness so a downgrade prompts instead of quietly cheapening a
run.

**The #43869-immune fallback — `opusplan`.** `/model opusplan` is native
behavior (Opus in plan mode, Sonnet for execution, in the *main* session;
since v2.1.219 `opus`/`default` resolve to **Opus 5**) — no subagent
routing at all, so the contested levers never enter the picture. It
captures most of the core rule (strong plans, cheaper implements) with
zero routing risk, at the cost of the fan-out and the Cheap floor.

## Caching-aware fan-out

Each fresh subagent pays a *cold* cache-write on a **5-minute TTL** (the
1-hour TTL is main-conversation-only), so weigh leaf count against
per-spawn cache cost and prefer a `fork` for a leaf that genuinely needs
full context. The async Batch API 50% discount never touches any of this,
since `/batch`, subagents and Agent Teams are all interactive. Full
policy: `caching.md`.

Three dispatch-construction rules (each live-measured 2026-07-11):

- **End the turn while a wave is in flight.** Completions re-invoke the
  orchestrator; an idle no-op wait turn re-reads the entire session context
  at cache price. Measured: ~30 wait turns at ~150k context cost roughly as
  much as a full 10-dispatch probe wave — pure waste, and the exact failure
  flow.md step 3's "never polling turns" is about.
- **Shared prefix first, brief last.** Build every same-wave prompt as
  [identical protocol + conventions][per-leaf brief at the end] —
  byte-identical prefixes across a concurrent wave cache-hit within the
  TTL, so leaves 2–N read the shared payload at 0.1×.
- **Tell Mid-or-stronger subagents to read the protocol; paste it only for
  Cheap.** Orchestrator output prices ≈5× input — pasting `check.md`
  (~1.7k tokens) into each verifier prompt costs more than one "read
  `references/check.md` and follow it" line that loads the file at input
  price inside the subagent (and identically across verifiers, so it
  caches). Haiku executors keep the attached payload: a Cheap executor may
  skip a read instruction, and that reliability is worth the paste.

## Adjacent primitives (know when NOT to use them)

- **Agent Teams** (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`, experimental):
  teammates coordinate via shared state and *don't inherit the lead's
  model* — an easy un-tiered fleet. Reserve for adversarial /
  competing-hypothesis review. Subagent fan-out stays the default. If
  used: `/config`'s "Default teammate model" sets the fleet tier, a
  teammate from a subagent definition honors its `tools` + `model`, and
  teammates inherit the lead's *effort*. `TeammateIdle`/`TaskCompleted`
  hooks (exit 2 blocks) enforce smartcheck-before-done.
- **Dynamic workflows** (scripted `pipeline()`/`parallel()`, schemas,
  resumable; auto-planned at `/effort ultracode`, v2.1.203+): the
  graduation for heavy runs. **Never reach for one unprompted** — the
  tool's contract makes orchestration opt-in (`ultracode`, a standing
  setting, the user asking, or a skill that says to), and "this task would
  benefit" is explicitly not enough. Ask first; Agent dispatch stays the
  default engine. <!-- claim:cc-workflow-requires-user-opt-in -->
  A script's `agent()` opts are the **only per-call effort dial** (`model`
  + `effort: low|…|max`), though the guidance is to *omit* `model` and
  inherit the session. <!-- claim:cc-workflow-guidance-omit-model -->
  It's an **execution engine** for step-3 at scale, not a policy
  replacement: its agents run acceptEdits with no human gate, so gate
  BEFORE the script runs, route tiers in the script, and ride the verify
  floor as scripted stages. Security sweeps → Anthropic's **Claude
  Security** plugin, which already ships this shape.

## Mechanical enforcement (optional, shipped)

`docs/enforcement-hook.md` (repo, not shipped): a PreToolUse hook +
`Agent(model:…)` deny rules turn "trust the bill" into a guardrail. A wired
warn-only instance ships at `.claude/settings.json` + `.claude/hooks/`;
flip to hard-deny via the one-line opt-in shown in that reference.

## Structural tool-lockdown (shipped seats)

Per-call `model:` tiers *which* model runs, not what a seat may touch — on
an ad-hoc `Agent()` call the seat rules are prompt-only. This repo ships a
tool-locked quartet at `.claude/agents/`
that enforces the seat at the tool layer instead: `smartplan-scout`
(`tools: Read, Glob, Grep`), `smartplan-verifier` (no `Write`/`Edit`/
`NotebookEdit`), `smartplan-implementer`, and `smartplan-implementer-cheap`
— the same shape already shipped on the Copilot side under
`.github/agents/`. Dispatch via `subagent_type: smartplan-scout` /
`smartplan-verifier`; copy the files into another project's own
`.claude/agents/` to reuse them. This closes the *tool-permission* half of
the gap only — a seat's `model:` frontmatter is still subject to the
contested resolution order (#43869, above), so confirm the tier with
`/usage`'s per-model lines.

## Cost levers (researched 2026-07-13 — sources: the development repo's research notes)

- **Fork plumbing** (tier caveat above): `context: fork` skills run
  background-by-default since v2.1.218 (`background: false` opts out where
  the flow needs the result synchronously); **forking is on by default
  since v2.1.232** — Claude can pick `subagent_type: fork` unprompted, so
  the tier caveat above now bites on dispatches you never asked for, and
  `CLAUDE_CODE_FORK_SUBAGENT` no longer gates it; untyped Agent calls still
  resolve general-purpose; `/subtask` is the in-session fork (v2.1.212) while
  `/fork` copies the session into a new background one.
- **Explore/Plan agent types skip CLAUDE.md + git status** (docs) — route
  read-only leaves/scouts there for a smaller cold context.
- **Standing-load knobs:** `skillOverrides` takes four states —
  `on` (the default for an absent skill), `off`, `name-only` (description
  leaves every turn's context) and `user-invocable-only`. Since v2.1.199
  `off` also hides the skill from Remote Control and Agent SDK command
  lists, not just the terminal. **Plugin skills are exempt from
  `skillOverrides` entirely** (re-verified 2026-08-12).
  `disable-model-invocation: true` removes a description entirely;
  `skillListingBudgetFraction` / `skillListingMaxDescChars` cap the whole
  listing.
- **Env vars:** `ANTHROPIC_DEFAULT_HAIKU_MODEL` (background-task model),
  `DISABLE_NON_ESSENTIAL_MODEL_CALLS`, `CLAUDE_CODE_AUTO_COMPACT_WINDOW` /
  `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` (earlier compaction shrinks per-turn
  re-reads on long sessions — but the compact itself busts the prefix;
  measure before adopting).
