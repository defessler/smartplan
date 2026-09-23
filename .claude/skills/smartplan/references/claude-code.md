# smartplan §A deep reference — Claude Code dispatch mechanics

*Load on demand from flow.md §A — when actually dispatching a wave on
Claude Code, wiring enforcement, or making a caching/budget call. Not part
of the per-invocation read.*

## Contents

- The lever, precisely
- Opus 5 and 5.5 seats: two gaps that read as model failure
- Whether the tier lands — contested; say so and route around it
- Caching-aware fan-out
- Adjacent primitives (know when NOT to use them)
- Mechanical enforcement (optional)
- Structural tool-lockdown (shipped seats)
- Cost levers (researched 2026-07-13 — sources: the development repo's research notes)

## The lever, precisely

- **Resolution order** (documented, v2.1.251+): per-call `model:` param >
  subagent frontmatter > `CLAUDE_CODE_SUBAGENT_MODEL` env var > session
  model. Before v2.1.251 the env var came first and beat both.
  <!-- claim:cc-subagent-model-resolution-order --> Since v2.1.196
  `inherit` is **identical to unset** (re-verified 2026-08-12).
- **Per-leaf lever = per-call `model:`** on each dispatch. It takes only
  the aliases `sonnet`, `opus`, `haiku` and `fable` (2.1.280 schema). A
  full id goes in seat frontmatter or the env var. **Wave
  guarantee:** `export CLAUDE_CODE_SUBAGENT_MODEL=sonnet` before an
  implementer wave so a leaf with no per-call or frontmatter model can't
  silently inherit the session (priciest) model, then **unset it** after.
  Keep it a shell export. A settings `env` entry was reported ignored
  (#43869, 2.1.263, third-party).
  `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1` (v2.1.257) pins every leaf, verifier
  and named seat included, and drops `model` from the Agent schema and
  workflow `agent()` opts. No dispatch can then name a tier. Never set it
  for a verified wave.
  The swap is subagent-scoped and cache-safe.
  Switching the **main** session's model, or its effort on most models,
  mid-run busts *its* prompt cache instead — see `caching.md`.
- **Effort has no per-dispatch knob here.** An ad-hoc `Agent()` call takes
  `model` but *not* `effort`. A seat's frontmatter `effort:` carries it,
  or an `agent()` opt in a workflow script. The Mid seats pin `high`. The
  Haiku seats pin `low`, inert on Haiku 4.5. A pin beats `/effort` and
  ultracode's xhigh. It also rides a per-call `model:`. A Strong
  `model: opus` dispatch then runs Opus 5.5 at high. Escalate a Cheap
  leaf by switching seat, never by `model:`. Its low pin would ride
  along. Only `CLAUDE_CODE_EFFORT_LEVEL`, `auto` included, outranks a
  pin. A `maxEffortLevel` cap clamps one. An unpinned seat takes an
  explicit session level, else its own model's saved level or default.
  Both links probed 2026-09-22 on 2.1.280. Opus 5.5 defaults to
  **medium**, every other effort model high (Opus 4.7 xhigh). A legacy
  top-level `effortLevel` in user settings no longer reaches Opus 5.5.
  <!-- claim:cc-agent-call-has-no-effort-param -->
- **Naming your seat** for SKILL.md § Seat ceiling: the system prompt's
  model line, or `/model` and `/status`. A per-call `model:` above it
  waits on the user's yes; the brief doesn't. A Haiku seat never waits
  on a yes. It sends no `model:` above Haiku at all (`routing.md` Cheap
  hard floor #6).
- **`opus` means Opus 5.5 from v2.1.280** on the Anthropic API, Claude
  Platform on AWS, Bedrock and Google Cloud (Foundry keeps Opus 4.6).
  And `default` is Opus 5.5 on every paid plan, Pro included. A
  subagent's `opus` takes the session's own Opus when the session already
  runs one. **Newest version first** (`model-classes.md` § How to edit):
  keep the session on `default` or `opus` and seats on the aliases, which
  move with each release. A full id like `claude-opus-5` freezes one.
  Where an alias lags (`sonnet` is Sonnet 4.6 on Claude Platform on AWS,
  4.5 on Bedrock, Google Cloud and Foundry), point it at the newest id
  with `ANTHROPIC_DEFAULT_SONNET_MODEL` or `_OPUS_MODEL`. 2.1.280 is
  the floor for Opus 5.5. On 2026-09-22 npm's `stable` tag still sat at
  2.1.267.
- **`/fast` is not a cheap tier.** Fast mode runs Opus with faster output —
  same model, not a smaller one (Opus 5.5/5/4.8, 5.5 the default at
  $8/$40). It buys latency, never budget. Its header is part of the cache
  key. The first enable per conversation re-reads the history uncached at
  fast-mode rates (later toggles keep it). On Sonnet or Haiku it
  switches the session to Opus, which stays after `/fast` goes off.
  Don't let it stand in for a tier drop.
  <!-- claim:cc-fast-mode-is-not-a-model-downgrade -->
- **A seat's window is sized by its own model, not yours** — five Haiku
  seats give five 200k windows, not five 1M. The beyond-one-context
  argument only holds for same-tier fan-out, forks, or Sonnet 5 seats.
- **Fan-out mechanism:** subagents run **background-by-default** (since
  v2.1.198) — wide dispatch
  is just *fire every Agent call*, then monitor the agent panel.
- **Auto mode (permissions) is the shipped starting mode on Pro, Max and
  Team** (effective 2026-08-14, version-gated). Its classifier runs
  **Sonnet 5** unless Anthropic sets one server-side, pinned after
  first-request validation, and bills as token usage on API and
  Enterprise. From 2.1.278 Enterprise, API, cloud-platform and
  `ANTHROPIC_BASE_URL` gateway sessions ask the server to fold those
  checks into session requests where rollout has reached them (`/status`
  shows an `Auto mode server` row). A header-stripping gateway falls back
  to billed local calls. The temporary opt-out
  `CLAUDE_CODE_AUTO_MODE_SERVER=0` isn't read on a direct Anthropic API
  connection. A subscription keeps the local classifier. Three
  consecutive or 20 total classifier blocks pause auto mode.
- **Isolation:** parallel edit leaves get `isolation: worktree`, a
  temporary git worktree each, auto-cleaned when unchanged. A stray
  shared-file touch then can't clobber a sibling. Worktrees do NOT share
  the prompt cache (`caching.md`). Isolate only leaves that really edit in
  parallel. Read-only and scout dispatches stay same-directory.
- **A `fork` can't be down-tiered — `model` is ignored, nothing errors.**
  It always runs the *session* model on the parent's warm prefix, so on an
  Opus session every fork is an Opus leaf. Fork is a **context** lever,
  never a cost one: use it for plan-feeding audit/synthesis that needs the
  whole session, and dispatch a normal subagent to route down.
  <!-- claim:cc-fork-ignores-model-override -->
- **Same-tier retry = resume, not re-dispatch:** a completed subagent sent
  a `SendMessage` auto-resumes in the background with its full history, so
  flow.md's one same-tier retry rides the executor's warm cache instead of
  a cold rebuild. Tier-safe on ≥2.1.211. A resumed agent with MCP tools
  loaded keeps that cache only from 2.1.277, a resumed fork from 2.1.280.
  The §B analog is `--resume`.
- **Hard ceilings:** **20
  concurrent** (v2.1.217; `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`; exempt
  under ultracode). A resume takes a fresh slot without checking it. A
  retry burst can pass 20. `--max-budget-usd` (print mode only) halts
  running background subagents at the cap. **Depth 3** since v2.1.219
  (`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`). At the limit a seat doesn't
  error. It does the work itself and returns one summary. Workflows carry
  their own caps: 16 concurrent by default (fewer on fewer CPUs, 1 to 256
  via `CLAUDE_CODE_WORKFLOW_MAX_CONCURRENT_AGENTS` on 2.1.269+), 1,000
  agents/run, size guideline <10 (<5 on Pro), and a Large workflow warning
  past 25 agents or a projected 1.5M tokens. On v2.1.271+ an
  interactive subscription workflow pauses at a usage limit and resumes
  after the reset. Size waves to these as
  `routing.md` sizes to credit caps.

## Opus 5 and 5.5 seats: two gaps that read as model failure

- **Auto mode is miscalibrated.** `tengu_auto_mode_config.severityByModel`
  ships no `claude-opus-5` or `claude-opus-5-5` entry (#80977, open but
  stale-labelled, re-read in this box's `.claude.json` 2026-09-22). So it
  falls to a stricter default blocking routine actions 4.8 allowed. Use
  plan mode or allow-rules.
  <!-- claim:cc-automode-missing-opus5-thresholds -->
- **On Opus 5 the system prompt can carry a don't-dispatch section:** use
  Agent, a workflow or deep research only when the user, a CLAUDE.md or a
  skill asks. 2.1.280 gates it on capability `opus_5_prompt_bundle`,
  absent on Opus 5.5 unless server-side prompt text adds it (code-read
  2026-09-22). By that wording a skill's or CLAUDE.md's routing policy
  already asks. **The plan gate's approval does too.** Quote it and
  dispatch. A separate `## Delegating to subagents` section, on any model
  when `tengu_thistle_grebe` (server-side, or env
  `CLAUDE_CODE_THISTLE_GREBE`) is `counter_steer`, says to work inline
  unless delegation clearly pays. That agrees with route-inline-first. It
  read `default` here on 2026-09-22. Log it as a benchmark confound.
  <!-- claim:cc-opus5-dont-dispatch-injection -->

## Whether the tier lands — contested; say so and route around it

Issue **#43869** ("all mechanisms resolve to the parent model") is **open**
(date of record: the development repo's claim ledger) and reports the per-call `model:`,
frontmatter, and env-var levers each ignored on some paths.
<!-- claim:cc-issue-43869-open -->

**`/usage` is the in-harness oracle.** Its Session block prints a
`Usage by model:` breakdown — per-model token counts plus a dollar figure
computed locally at list rates (or an org's managed `modelPricing`). On a Max or Pro seat the dollars aren't a
bill, but on Anthropic's endpoint the **model attribution is real**, so
the #43869 check is free and offline: dispatch a cheap-tier wave, then
look for whether a line for that model appears at all. An all-Opus
breakdown after a Haiku wave is the failure. Behind a rerouting gateway
the client's per-model accounting names the alias you asked for, not the
model served (cost-state read 2026-09-22, `/usage` untested). Read the
provider's monitor there.

**Never grep the transcript for it.** #43869 repros disagree on what a
subagent's JSONL `model` field records: the requested model in one, the
served one in a 2.1.233 repro that put the request in `meta.json`
(third-party, unprobed here). If that holds, `meta.json` against the
JSONL is a free offline detector. Until a local probe settles it,
transcript metadata proves nothing. Nor brief a seat to quote its system
prompt or model line as proof: Opus 5.5 refuses that as
`reasoning_extraction` (#96139).
One separate path *does* warn: an `availableModels`
substitution prints an interactive-only warning naming the requested and
the substituted model, so check for it before calling it a #43869 hit.

**Check `/tasks` first.** The task list and agent detail dialogs print
the **model each subagent actually ran at, plus its effort when the seat
pins one** (for an inheriting seat, which shows none, read
`$CLAUDE_EFFORT` in its Bash). That is a sharper #43869 oracle than
`/usage`, which stays a cross-check. A PostToolUse hook on `Agent` logs
`resolvedModel` (the start model) and, from 2.1.212, `modelsUsed` after a
mid-run swap: harness resolution per dispatch, blind to the server side.
In auto mode (2.1.271+) the report arrives via `SubagentHandback`, which
edits nothing and passes the classifier first. Match that too.

**A second silent de-tiering path:** fallback chains cover subagents
(v2.1.247). A chain from `--fallback-model` or a `fallbackModel` settings
array (max 3, turn-scoped, availability-only, never shrinking context at
compaction) can move a pinned leaf mid-wave while the session model reads
unchanged. Neither startup nor `/status` shows one. The parent-side error
text names the model. `modelsUsed` records the swap. Track it alongside
allowlist substitution and #43869.

**Partial fixes:** v2.1.211 stopped an override reverting to the parent on
resume or follow-up, so multi-turn dispatches are tier-safe only on
≥2.1.211, and v2.1.222 covers the allowlist case. #43869 stays open, so
treat "the cheap tier landed" as unconfirmed until `/tasks` shows the
model (or `/usage` the line).

**Measurement hazard: the safety fallback.** A content-flagged request
re-runs on a different model and the **session continues** there. It can
fire on the first request, which carries your CLAUDE.md and git status
(`--safe-mode` isolates your customizations). The published map (read 2026-09-22): on Opus 5.5, Fable
5.1 and Fable 5, biology falls to Opus 5 and cybersecurity to Opus 4.8.
Opus 5.5's frontier-LLM-development flag falls to Opus 5. On Opus 5,
cybersecurity falls to 4.8 and biology refuses. `reasoning_extraction`
refuses everywhere. From Opus 5.5 a fallback is down in capability but up
in price. Set `switchModelsOnFlag: false` in any
benchmark harness: an interactive flag then asks and a `-p` main-thread
flag ends the turn. A flagged subagent or workflow leaf re-serves on the
fallback anyway (a 2.1.280 code read plus #91923, unprobed). Check OTel
`subagent_completed`'s `model_swapped` and `final_model`.

**The #43869-immune fallback — `opusplan`.** `/model opusplan` is native
behavior (Opus 5.5 in plan mode, Sonnet for execution, in the *main*
session) — no subagent routing at all, so the contested levers never enter
the picture.
It captures most of the core rule (strong plans, cheaper implements) with
zero routing risk, at the cost of the fan-out and the Cheap floor.

## Caching-aware fan-out

Each fresh subagent pays a *cold* cache-write, defaulting to a **5-minute
TTL** — liftable to an hour via `subagentPromptCacheTtl`,
`CLAUDE_CODE_SUBAGENT_PROMPT_CACHE_TTL`, or per-agent `experimental.cacheTtl`,
though a subscription running on usage credits ignores the per-agent `1h`
(see `caching.md`). So weigh leaf count against
per-spawn cache cost and prefer a `fork` for a leaf that genuinely needs
full context. Full policy: `caching.md`.

Three dispatch-construction rules (each live-measured 2026-07-11):

- **End the turn while a wave is in flight.** Completions re-invoke the
  orchestrator; an idle no-op wait turn re-reads the entire session context
  at cache price. Measured: ~30 wait turns at ~150k context cost roughly as
  much as a full 10-dispatch probe wave. Scheduled tasks, cross-session
  messages (`crossSessionInbound: hold`) and interactive `/goal` check-ins
  (`CLAUDE_CODE_GOAL_CHECKIN_MINUTES=0`) start idle turns that resend it too.
- **Shared prefix first, brief last.** Build every same-wave prompt as
  [identical protocol + conventions][per-leaf brief at the end] —
  byte-identical prefixes across a concurrent wave cache-hit within the
  TTL, so leaves 2–N read the shared payload at 0.1× once the first leaf
  starts streaming (stagger per flow.md step 3, where it pays). Workflow
  siblings share it only when model, effort, agent type, tools, output
  schema and working directory all match.
- **Tell Mid-or-stronger subagents to read the protocol; paste it only for
  Cheap.** Orchestrator output prices ≈5× input. One "read
  `references/check.md` and follow it" line beats pasting ~4k tokens into
  each verifier prompt. The file then loads at input price inside the
  subagent and caches across verifiers. A Cheap executor may skip a read
  instruction. Haiku keeps the attached payload.

## Adjacent primitives (know when NOT to use them)

- **Agent Teams** (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`, experimental):
  teammates **fall back to the lead's model**. An unconfigured teammate
  lands on the lead's *priciest* one. Precedence, first match winning: the
  model your spawn prompt names · a subagent definition's `model:` (where `inherit` picks the lead's)
  · `CLAUDE_CODE_SUBAGENT_MODEL` when set to anything but `inherit` · the
  lead's current model. **Before v2.1.251 the env var came first.** Name the
  model in the spawn prompt to be sure. Reserve teams for adversarial /
  competing-hypothesis review. Subagent fan-out stays the default.
  **A live hazard:** with teams enabled, an Agent call carrying a `name`
  launches a *teammate*, which reports via idle notification rather than
  the result the Integrate step waits for. Claude may add a name on its
  own. A seat dispatched by `subagent_type` alone, a fork, or a call
  passing `isolation` stays a subagent. So does every named call under
  `claude -p` or the SDK. Setting the variable to `0` in settings `env`
  reverts without a restart.
  Teammates inherit the lead's *effort*. `TeammateIdle`/`TaskCompleted`
  hooks (exit 2 blocks) enforce smartcheck-before-done.
- **Advisor** (flow.md § Reach for the built-in): a seat inherits it.
  Check `advisorModel` before a Cheap wave.
- **Dynamic workflows** (scripted `pipeline()`/`parallel()`, schemas,
  resumable; auto-planned at `/effort ultracode`, v2.1.203+): the
  graduation for heavy runs. Pro switches them on in `/config`. **Never
  reach for one unprompted.** The tool's contract lists five opt-ins: the
  `ultracode` keyword, ultracode on for the session, the user asking, a
  skill or slash command *the user* invoked that says to, or a named or
  saved workflow the user asked for. A skill the model loaded itself,
  smartplan included, isn't one. Nor is "this task would benefit". Ask
  first. Agent dispatch stays the
  default engine. <!-- claim:cc-workflow-requires-user-opt-in -->
  A script's `agent()` opts are the **only per-call effort dial** (`model`
  + `effort: low|…|max`). The tool's script reference says to *omit*
  `model` and inherit the session. The workflows docs' cost section says to
  ask for a smaller model on stages that don't need the strongest.
  <!-- claim:cc-workflow-guidance-omit-model -->
  It's an **execution engine** for step-3 at scale, not a policy
  replacement: a workflow takes no mid-run user input beyond permission
  prompts, so gate BEFORE the script runs, route tiers in the script, and
  ride the verify floor as scripted stages. Its agents inherit the session's
  permission mode. A definition's `permissionMode` counts only from
  default, dontAsk or plan mode. In auto mode the classifier reads an
  `agent()` prompt as computed text, not a user request. A leaf's
  destructive or outward action can't lean on its brief. The launch itself carries a
  mode-dependent approval prompt. Security sweeps → Anthropic's **Claude
  Security** plugin, which already ships this shape.

## Mechanical enforcement (optional)

`docs/enforcement-hook.md`: a PreToolUse hook +
`Agent(model:…)` deny rules turn "trust the bill" into a guardrail. A wired
warn-only instance lives in the source repo at `.claude/settings.json` +
`.claude/hooks/`, described on that page. Its note rides
exit-0 JSON (`systemMessage`, `additionalContext`), since exit-0 stderr
reaches only the debug log. Flip to hard-deny
via the one-line opt-in shown in that reference.

## Structural tool-lockdown (shipped seats)

Per-call `model:` tiers *which* model runs, not what a seat may touch — on
an ad-hoc `Agent()` call the seat rules are prompt-only. This repo ships a
tool-locked quartet at `.claude/agents/`
that enforces the seat at the tool layer instead: `smartplan-scout`
(`tools: Read, Glob, Grep`), `smartplan-verifier` (no `Write`/`Edit`/
`NotebookEdit`), `smartplan-implementer`, and `smartplan-implementer-cheap`.
Dispatch via `subagent_type: smartplan-scout` /
`smartplan-verifier`; copy the files into another project's own
`.claude/agents/` to reuse them. This closes the *tool-permission* half of
the gap only — a seat's `model:` frontmatter is still subject to the
contested resolution order (#43869, above), so confirm the tier with
`/tasks`, cross-checked against `/usage`'s per-model lines.

## Cost levers (researched 2026-07-13 — sources: the development repo's research notes)

- **Fork plumbing** (tier caveat above, for `subagent_type: fork` and
  `/subtask`): **forking is on by default since v2.1.232**. Claude can
  pick a fork unprompted. The caveat then hits dispatches you never asked for.
  The flip is **interactive-only**: a `claude -p` or Agent SDK arm runs
  with fork off unless `CLAUDE_CODE_FORK_SUBAGENT=1`. An interactive and
  a headless arm of one measurement then differ in more than the
  harness. Untyped Agent calls still resolve general-purpose.
  `/subtask` is the in-session fork (v2.1.212). `/fork` copies the session
  into a new background one. A `context: fork` skill is no fork despite
  the name: it starts a fresh subagent with no history, tiered by its own
  `model:` frontmatter, background-by-default since v2.1.218
  (`background: false` opts out).
- **Explore and Plan skip CLAUDE.md and git status** (docs) but run the
  session model (Explore capped at Opus on the Claude API), ignore a bare
  `CLAUDE_CODE_SUBAGENT_MODEL`, and can't be resumed. On an Opus 5.5
  session that's a small context at Opus prices. Prefer `smartplan-scout`.
  On 2.1.271+ a seat's `omitClaudeMd: true` drops user, project and local
  CLAUDE.md too (git status still loads).
- **Standing-load knobs:** `skillOverrides` takes four states —
  `on` (the default for an absent skill), `off`, `name-only` (description
  leaves every turn's context) and `user-invocable-only`. **Plugin skills are exempt from
  `skillOverrides` entirely** (re-verified 2026-08-12).
  `disable-model-invocation: true` removes a description entirely;
  `skillListingBudgetFraction` / `skillListingMaxDescChars` cap the whole
  listing. `/skill-doctor` (2.1.252+) reports per-skill context cost and
  usage.
- **2.1.277 reads `AGENTS.md` directly when a project has no
  `CLAUDE.md`** (configurable under Project instructions in `/config`; not
  on Bedrock, Vertex, Foundry, or telemetry-disabled sessions). On Windows
  the docs still recommend an `@AGENTS.md` import inside `CLAUDE.md`,
  which doesn't double-read.
- **claude.ai skill sync (2.1.275) is a new standing-load surface:**
  skills and plugins enabled on the claude.ai account sync into terminal
  sessions by default — synced skills land in `~/.claude/skills/synced/`
  (~10-minute refresh, collisions invoke as `/anthropic-skills:<name>`).
  Opt out with `syncClaudeAiSkills` / `syncClaudeAiPlugins`.
- **Env vars:** `ANTHROPIC_DEFAULT_MODEL` (v2.1.236+) is a **fifth link in
  the session-model precedence chain**, below `/model`, `--model` and
  `ANTHROPIC_MODEL`, and it can silently repoint new sessions — check it
  before trusting a tiering measurement on a shared box. The `best` alias
  is a **moving target by design** (Fable 5.1 since v2.1.257, not Fable 5),
  so never pin a benchmark arm to it. `ANTHROPIC_DEFAULT_HAIKU_MODEL`
  (background-task model; helper agents come pre-seated cheap — statusline
  setup on Sonnet, the docs guide on Haiku),
  `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` (the documented traffic lever;
  it reaches model-adjacent calls only indirectly, and no switch exists today
  that suppresses background model calls specifically).
- **Compaction:** `/autocompact` (saved as `autoCompactWindow`, 100K to
  1M), `--autocompact` per launch, or `CLAUDE_CODE_AUTO_COMPACT_WINDOW`,
  which wins and takes a plain integer only: `500k` reads as 500 and
  clamps to 100K. `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` can only lower the
  threshold, subagents included. Earlier compaction shrinks per-turn
  re-reads. Each compact busts the prefix, though. Measure before
  adopting.
