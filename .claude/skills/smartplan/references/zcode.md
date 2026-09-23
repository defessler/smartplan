# smartplan §C deep reference — ZCode (Z.ai) levers & limits

> Facts verified 2026-08-12 against `zcode.z.ai/en/docs`, `docs.z.ai`, and
> Z.ai's Terms of Use; **re-swept 2026-08-31**, **re-read 2026-09-15**, and
> **re-read 2026-09-22** (web docs, changelog, the public source, local
> build 3.14.3 / zcode.cjs 0.16.9). Every "not
> documented" below is a genuine
> absence at the source, not a shrug: ZCode's docs are young and several
> pages describe a settings **form** rather than the on-disk file it writes.
>
> **Part of this file is measured, not read** — see § Measured against a
> live install. ZCode is installed on this machine and has been serving this
> skill family since at least 2026-08-03.

Load this only when the session is ZCode. For the flow itself, see `flow.md`.

## Contents

- What ZCode is
- The one fact that decides everything
- The tiering lever — real, but coarser than §A
- Parallelism
- Skills
- Plugins — and why this repo does NOT install as-is
- Hooks
- Goal Mode — a built-in verify gate
- Execution modes
- Models — ZCode is not GLM-only
- Vendor benchmark claims — treat as self-reported
- Headless — real, fully self-documenting, and separately configured
- MCP
- Measured against a live install (2026-08-12; re-read 2026-09-22 at build 3.14.3, zcode.cjs 0.16.9)
- What is still unknown

## What ZCode is

A desktop **Agentic Development Environment** from Z.ai — not a
CLI, not an IDE fork. Electron, with macOS (Apple Silicon + Intel), Windows
(x64 + ARM64) and Linux (x64 + ARM64; AppImage, DEB and RPM, no Beta marker)
installers. Vendor's current release is **v3.14.3, 2026-09-22** (read
2026-09-22, docs download links `ZCode-3.14.3-*`). Recent releases: 3.12.3
(2026-09-17, PDF/media previews, per-workspace plugins, an OpenCode Go
provider template), 3.14.0 (2026-09-19, **dynamic workflows**, Office vs
Coding mode, an independent Start Plan), 3.14.1 (bug fixes, now dated
2026-09-22 on the changelog, probably a republish) and 3.14.3 (workflows:
live concurrency changes, better reuse on amend and restart, cheaper
script submission, a leaner workflow tool). There's no 3.14.2. The
changelog fetches statically to its floor, v3.10.1 (2026-08-28).

The build installed here reads **3.14.3.7762, with `zcode.cjs` 0.16.9
rebuilt 2026-09-22** (`ZCode.exe` VersionInfo plus the uninstall entry).
It auto-updates and matched the vendor on 2026-09-21 and 2026-09-22.

**It's open source now.** Z.ai published `github.com/zai-org/ZCode` under
Apache-2.0 on 2026-09-20: the clients, backend services, shared UI, and
the Agent CLI and runtime. The snapshot there is 3.14.0 while this box runs
3.14.3. Pin a code-level claim to a version. "Code-read" below means
read from that source or the installed bundle, not run.

## The one fact that decides everything

**ZCode does not read `CLAUDE.md` at runtime.** It reads `AGENTS.md` at two
scopes: `~/.zcode/AGENTS.md` (user) and a workspace `AGENTS.md`. `CLAUDE.md`
is consumed once, during onboarding, purely as a migration source — the
built-in flow copies `~/.claude/CLAUDE.md` into `~/.zcode/AGENTS.md`.

It **does** walk directory levels. The shipped `zcode-configuration-guide`
skill states that
ZCode "searches for the workspace `AGENTS.md` from the current working
directory **upward until the detected project root**." It resolves one file:
the web docs add that ZCode "does not merge multiple `AGENTS.md` files
across directory levels" and doesn't expand `@import` / `@include` (read
2026-09-15). **Merge order:** the
user file injects first, then the workspace file, so workspace instructions
can narrow or override user defaults. `/init` targets the workspace file,
never the user default.

So a policy that lives in `CLAUDE.md` is **invisible here**. On ZCode the
standing-instruction surface is `AGENTS.md`, and the skill surface is
`SKILL.md`. Plan for both.

## The tiering lever — real, but coarser than §A

ZCode has a **per-agent model pin**, closest in shape to Copilot's
`.github/agents/` rather than Claude Code's per-call `model:` parameter.

- Custom subagents are Markdown files at `~/.zcode/agents/<name>.md`
  (user) or `.zcode/agents/` in the working directory (project, no upward
  walk, `permissionMode` stripped). The project path is code-read and
  unprobed here. Settings can't create project seats yet.
- The settings form exposes **Name, Color, Model, Thinking effort,
  Description, Available tools, System prompt**. Model is "Inherit
  default" or a specific model. Thinking effort appears only when one is
  pinned (re-read 2026-08-31).
- Invocation is automatic delegation on description match, or explicit
  `@name`. Two built-ins ship: `general-purpose` (all tools) and `Explore`
  (read-only). Neither is editable. Settings can still give each a
  dedicated model and thinking effort (QA and subagents pages, read
  2026-09-22). Pinning `Explore`
  to a cheap model makes a scout tier with no seat file. `Explore` doesn't
  get `AGENTS.md` injected.

**Three limits that change how you seat work here:**

1. **There is no per-call or per-dispatch model override.** Nothing in the
   subagents docs offers one, and the hooks page exposes `model` only as
   read-only `SessionStart` input. The nearest real per-invocation override
   is on **commands**, not agents.
2. **Subagents are Beta.** "User-level custom subagents are rolling out.
   The capability and its scope may still change."
3. **A Claude Code alias pins nothing.** ZCode's subagent parser reads
   `model` values `inherit`, `main`, `sonnet`, `opus` and `haiku` as no
   model. A value without a provider prefix fails to parse and inherits
   too. Neither raises an error. So this repo's seats (`model: haiku`,
   `model: sonnet`) and a bare `model: glm-5.3` all run on the primary
   session's model. `thoughtLevel` attaches only once a model
   resolves. A real pin is provider-qualified,
   `model: <providerId>/<modelId>`, with an optional `$<level>` suffix. Pin
   the newest version of a line your provider serves (`model-classes.md`
   § How to edit). A qualified value that fails to resolve stops the
   dispatch ("Cannot start subagent") rather than falling back. Code-read (3.14.3 bundle and
   source), not yet probed with a live dispatch.

**Frontmatter keys.** `/en/docs/subagents` publishes ten: `name`
(required), `description` (required), `model`, `thoughtLevel`, `color`,
`tools`, `disallowedTools`, `maxTurns`, `injectAgentsMd`, `mcpServers`.
The key is **`thoughtLevel`, not `reasoningEffort`**. The profile parser
also reads four undocumented keys (code-read): `background`, `memory`,
`permissionMode` (ignored in project files) and `skills`. Custom seats get
the user and workspace `AGENTS.md` injected by default since v3.7.1.
`injectAgentsMd: false` opts a leaf out. A custom `tools` list is
exhaustive. Leave `Skill` off it and the seat can't invoke a skill. MCP
tools need full `mcp__server__tool` names, with no wildcards. So this
repo's seats can't load `smartreview` or `smartvoice` mid-leaf here.
Hand-authoring a seat file is documented (new sessions pick changes up).
Subagents **cannot spawn subagents**.

**Consequence for the flow:** ZCode can hold the seats, and there is still
no per-call or per-dispatch model override, but a seat's model is only as
fixed as its pin (subagents page, read 2026-09-21). A **pinned** seat keeps
its model for the running session. Pin edits apply only to a new session.
An **`inherit`** seat, alias-pinned ones included, moves with the primary:
switch the primary session's model and later calls to that seat run on
the new model "immediately on subsequent calls." So pin the seats once in
the qualified form, dispatch against them, and treat
an escalation as *switching which seat you address* rather than raising a
parameter. The **cost ceiling** (`routing.md` § The cost ceiling) applies
at the pin and at the pick: no seat is pinned or first-picked above the
session's own model, and a climb means addressing a stronger seat
deliberately, with the plan-gate ask on a session priced below it.

## Parallelism

Subagents launched together **run in parallel**, and the main task **blocks**
until all finish. A **background mode** also exists where the main task does
not wait and can end its turn; background `Explore` subagents are restricted
to read-only tools. Scheduled tasks can pin a model per subagent. Idle-time
tasks can't be tiered. The form offers a model. The server assigns the one
that runs. They reject background subagents with an explicit error. An
idle wave runs foreground (read 2026-09-15). They're free of plan quota,
foreground subagents and compaction included. They roll out in batches,
need a personal Coding Plan (not Start Plan or an API key), and start with
no promised time. Anything you type into the session still
bills (idle-time page, read 2026-09-22).

That blocking default is the important half: it makes ZCode's foreground
fan-out a barrier, not a pipeline. Size waves accordingly.

**ZCode 3.14.0 (2026-09-19) added dynamic workflows** — "a single script to
orchestrate multiple sub-agents collaborating on complex tasks," started
from the plus menu or a `/workflow` command, the same shape as Claude
Code's. No web docs page covers them. The contract is a bundled
`dynamic-workflows` skill (93,907 bytes) that can't be disabled and doesn't
list. `CreateWorkflow` refuses to run until it loads. Every workflow pays
that context first. It answers two questions. **A workflow is
single-tier per run**: every subagent runs on the session's model, or on a
run-level `subagent_model` (`providerId/modelId` or a bare id, optional
`$level`) set on `CreateWorkflow` or `AmendWorkflow` only when the user
asks. There's no per-agent pick. A tiered wave needs separate runs or
seats. And workflow subagents can't call `CreateWorkflow` (bundled skill,
read 2026-09-22). Gate a workflow the way flow.md gates one everywhere:
the human gate happens at launch, because nothing stops it after.

## Skills

ZCode ships first-class Agent Skills using `SKILL.md`.

- User-level path: `~/.zcode/skills/<skill-name>/SKILL.md`.
- Invoked with `$skill-name` in chat, or through the `/` menu under a Skills
  group.
- ZCode can **import** skills from Claude Code and other agents. The web
  Skill page now documents the import dialog's scope choice — "the current
  Project (current workspace only)" versus Global.

**Four caveats, verified 2026-08-12 and re-read 2026-09-22:**

- **Extra frontmatter keys look harmless in 3.14.3 (code-read).** The
  skill adapter's allowlist is the Set `name`, `description`,
  `when_to_use`, `license`, `metadata`, and `when_to_use` IS parsed. The
  bundle still computes `safeToAutoLoad` (every key in that Set) but only
  prints and serializes it. The skill record hard-codes
  `allowImplicitInvocation: true`. The plugin page says non-allowlisted
  fields don't affect loading. So `smartexec`'s `user-invocable` and
  `disable-model-invocation` probably don't block auto-invocation. That's
  a grep, not a run. Probe one skill before relying on it. The web
  Skill page documents two
  hard caps: "`description` is capped at 1024 characters. Going over drops
  the whole skill," with no truncation, and "a SKILL.md body over 100KB is
  truncated" (read 2026-09-21).
  **Only the first 250 description characters reach the model each turn**,
  from a shared metadata budget that degrades to names-only when too many
  skills are enabled (web Skill page, 2026-09-15). Front-load the trigger.
- **The full discovery order, from the shipped configuration guide.** The
  web Skill page gives only the user path. The web FAQ adds the
  workspace path. The order and the upward walk are product-only.
  Earlier locations win:

  1. Explicitly configured roots
  2. User `~/.zcode/skills`
  3. User `~/.agents/skills`
  4. Workspace `.zcode/skills` — **walked from the cwd up to the repo root,
     every level counts**
  5. Workspace `.agents/skills`
  6. Enabled plugin roots (lowest)

  Within a level `.zcode` is scanned before `.agents`, and a deeper
  working-directory location beats a repo-root one. **Skill identity is the
  file path**, so same-named skills at different paths are all discovered
  but only the first in order loads — the rest are shadowed. That matches
  Claude Code's enterprise > personal > project ordering: here too **user
  scope outranks workspace**. A personal copy silently shadows a repo's own.

  Plugin roots are recognized by `.zcode-plugin/plugin.json` **and**
  `.claude-plugin/plugin.json` **and** `.codex-plugin/plugin.json` **and**
  `.cursor-plugin/plugin.json`.
- **Discovery is `SKILL.md`-scoped, not naive.** The walker recurses but
  yields a directory only when it directly contains a file named
  `SKILL.md`, skipping `node_modules`, `dist`, `build`, `out`, `target`,
  `vendor`, `coverage`, `.cache`, `.next`, `.turbo`, `.venv`, `__pycache__`
  and dotdirs other than `.system`. So a `references/` folder full of `.md`
  files is walked past, never mistaken for extra skills.
- **`references/` is undocumented but supported.** No ZCode docs page
  mentions it, English or Chinese. The shipped engine still implements
  Claude Code's progressive-disclosure contract (§ Measured against a live
  install). So the byte ratchet stays affordable on ZCode.

## Plugins — and why this repo does NOT install as-is

The plugin format looks compatible and mostly is:

- Manifest at `.zcode-plugin/plugin.json` **or** `.claude-plugin/plugin.json`
  (documented lookup priority, on the plugin and hooks pages).
- A plugin bundles `commands/`, `skills/<name>/SKILL.md`, `agents/*.md`,
  `hooks/hooks.json` and `.mcp.json`.
- Marketplaces use a root `marketplace.json`. Its documented top-level
  fields are `name`, `plugins`, `pluginRoot`, `description` and
  `allowCrossMarketplaceDependenciesOn` (read 2026-09-21).
- Documented as plain GA. No beta, preview or SKU gate anywhere on the page.
- ZCode 3.11.2 added per-workspace plugin install. The 3.14.3 build
  here has it. The plugin page doesn't document it yet (read 2026-09-22).

**But "this plugin installs into ZCode unchanged" is false**, on three
counts, each checked at the source:

1. **The `.claude-plugin` fallback covers the plugin manifest only.** Across
   every ZCode docs page, `.claude-plugin` appears in exactly one context —
   the `plugin.json` lookup-priority line. There is **no documented
   `.claude-plugin/marketplace.json` fallback**. The catalog is documented
   solely as "a `marketplace.json` at the root". This repo ships its catalog
   at `.claude-plugin/marketplace.json` and has no root copy, so the one
   file ZCode must read first sits at an undocumented path.
2. **This repo has no `plugin.json` at all** — neither path. ZCode calls the
   manifest "the only required file". This repo declares components inline
   in its marketplace entry instead, which Claude Code accepts and ZCode
   does not document.
3. **Those inline keys aren't documented ZCode fields.** This repo's entry
   carries `"skills": ["./.claude/skills"]` and an `agents` array, but ZCode
   documents `skills`/`agents`/`commands`/`hooks`/`mcpServers` as
   **`plugin.json`** fields, while its `plugins[]` entry table lists only
   name, source, description, version, category, tags, dependencies and
   strict. Neither `metadata` nor `owner` is a documented top-level field,
   though the published catalog carries `owner` (§ Measured).

**The skills payload is the portable part.** The `skills/<name>/SKILL.md`
layout and `name`/`description` frontmatter match this tree, and ZCode
separately documents importing skills "from other AI coding tools such as
Claude Code". The packaging around them is what needs building — a root
`marketplace.json` plus a real `plugin.json`. That's what
the repo's ZCode export script generates.

## Hooks

Seven events, a **subset** of Claude Code's: `SessionStart`,
`UserPromptSubmit`, `PreToolUse`, `PermissionRequest`, `PostToolUse`,
`PostToolUseFailure`, `Stop`. No `PreCompact`, `Notification`,
`SubagentStop` or session-end equivalent.

Config in three places, but **project-level hooks are not executed in the
current version** (web docs, read 2026-08-31 — workspace configs ignored
for security), so the execution order is user → enabled plugin hooks, with
no workspace term. Three other sources disagree. The configuration guide
bundled with 3.9.1 listed `<repo>/.zcode/config.json` → hooks as workspace
scope. The changelog's 3.8.1 entry claims workspace-level hooks. The
open-source NOTICE describes a workspace-hook trust check keyed on
workspace identity and a declaration digest. Treat the NOTICE as a lead.
The denying-hooks consequence below is why it matters which source wins.

**Hooks here can deny**, unlike this repo's warn-only Claude Code guardrail:
`PreToolUse` returns `"permissionDecision": "deny"`, `UserPromptSubmit`
returns `"continue": false`. Read `docs/enforcement-hook.md`'s safety note
before porting the tiered-dispatch hook — a denying variant of it bricks the
default policy, and that warning applies with more force on a harness where
deny actually works. Tool-event matchers accept `Agent` and `Task`
aliases. A port can match `Agent|Task` as it does on Claude Code. A `Stop` block can
continue the loop at most 3 times in a row (hooks page, read 2026-09-22).

**`hooks.enabled: true` IS required for configuration-file hooks.** They are
disabled by default. When any plugin contributes a hook, the hook runner
enables automatically. The web docs and the bundled guide both say so
("The file must set `hooks.enabled: true`", read 2026-08-31).

## Goal Mode — a built-in verify gate

Goal Mode is not just a planner. At the end of **every round** ZCode runs a
**separate check** to decide whether the objective was met, and that check
demands **artifact evidence** rather than a confident-sounding reply. If the
objective is unmet it produces the next step and auto-starts another round.
Goal Mode's commands are `/goal` and `/compact` (full list under § Headless).

This is the closest thing in any tracked harness to smartcheck shipped in
the box. It does not replace an *independent* verifier — same-context
self-checking is tier 3 on `SKILL.md`'s verify floor — but on ZCode the
floor is met by default rather than by discipline. Reach for `/goal` before
rebuilding the loop out of this flow.

## Execution modes

Four modes cycled with Shift+Tab: **Ask
before changes** (default), **Edit automatically**, **Plan mode**, **Full
access** — reworded labels, same four modes and interaction pattern as
Claude Code. Separately, **Thought levels** (Low, High, **Max — the
default**) control reasoning depth for GLM-5.3 through Ctrl+T. "Off" is
gone, and **Max being the default is a cost fact**:
a GLM-5.3 session reasons at max unless told otherwise, while Claude models
default to medium (configuration page, 2026-09-15).
Models and execution modes can both be switched mid-task. The Coding Plan's
Anthropic endpoint gives Claude Code the same max default and folds its
levels onto three: low and below run low, medium and high run high, xhigh
and up run max, and thinking off still runs low. So an effort sweep there
has three real levels, not five (docs.z.ai, read 2026-09-22).

## Models — ZCode is not GLM-only

The docs name nine provider families: **Z.ai (Global), BigModel (China),
Anthropic, OpenAI, OpenRouter, Moonshot/Kimi, MiniMax, Xiaomi MiMo**, and
custom Anthropic- or OpenAI-compatible endpoints including self-hosted.
The 3.14.3 catalog ships 20 templates, adding DeepSeek, Alibaba Cloud
(China and Global), xAI, and three each of OpenCode Go and Zen.
Documented base URLs include `https://api.z.ai/api/coding/paas/v4`,
`https://api.z.ai/api/anthropic`, `https://api.anthropic.com`,
`https://api.openai.com`, `https://openrouter.ai/api`.

**So an Anthropic ladder is reachable from ZCode**, billed through an
Anthropic key, with ZCode supplying the harness. That is the configuration
to prefer if you want the tiering policy to mean what it means everywhere
else. It isn't parity yet. The 3.14.3 Anthropic template tops out at
`claude-fable-5-1` and `claude-opus-5`, with no Opus 5.5. The OpenAI one
tops out at `gpt-6-astra`, with no GPT-6 Sol or Luna (read 2026-09-22). Opus
5.5 is reachable only as a hand-added `claude-opus-5-5`. Two cautions before
seating a Claude 5-series model. A hand-added model gets a 200K window
unless its ID ends in `[1m]` or you enter one. And the bundle's Anthropic
capability table stops at Opus 4.8. An unlisted ID falls back to a
4,096-token max output unless ZCode passes its own value. Whether it does
with the per-model field empty is unprobed (code-read).

**Compaction** reserves about 34K tokens. A 128K window compacts near
94K, 200K near 166K and 1M near 966K, with no user switch. Built-in Coding
Plan GLM models use a fixed window you can't edit (QA page, read
2026-09-22).

### GLM prices ($ per 1M tokens, Latest Models rows re-read 2026-09-22)

| Model | Input | Cached input | Output |
| --- | --- | --- | --- |
| GLM-5.3-Flash | 0.15 | 0.03 | 0.50 |
| GLM-5.3-FlashX | 0.37 | 0.075 | 1.25 |
| GLM-5.3 | 1.40 | 0.26 | 4.40 |
| GLM-5.2 | 1.40 | 0.26 | 4.40 |
| GLM-5.1 | 1.40 | 0.26 | 4.40 |
| GLM-4.5-Air | 0.20 | 0.03 | 1.10 |
| GLM-4.7-FlashX | 0.07 | 0.01 | 0.40 |
| GLM-4.7-Flash | Free | Free | Free |
| GLM-4.5-Flash | Free | Free | Free |

The Flash launch promo (50% off) ended 24:00 **2026-09-09** UTC+8. Rows
outside Latest Models are the 2026-09-15 re-read. Cached-input **storage** stays
"Limited-time Free" for all paid models. **GLM-5-Turbo has no row on this
page** and no published per-token price. It survives in ZCode's trial
marketing and its Z.ai API provider template.

**T32's dollar column for the z.ai arm is understated by about 2×.** It
priced GLM-5-Turbo at 0.60 / 2.20, the GLM-4.7 rate. With no current
per-token figure, there's nothing to reprice it against.

**GLM-5.3 shipped 2026-08-14** in ZCode (3.7.7: "The brand-new flagship
model GLM-5.3 is now available!", an entry now below the changelog's floor)
and 2026-08-18 on Z.ai's API release notes. ZCode brands itself "the
official harness for GLM-5.3". Same base model as GLM-5.2 with post-training gains,
identical price, 1M context, 128K max output, text-only input, reasoning
always on (low/high/max — **cannot be disabled**). On current Coding Plans,
requests for GLM-5.2 and GLM-5.1 **auto-route to GLM-5.3**, and GLM-4.7 to
GLM-5.3-Flash (read 2026-09-15). **The plan FAQ names only GLM-5.3 and
GLM-5.3-Flash as callable** and lists other models among the causes of
error 1113 or balance deduction (read 2026-09-22). One account's bill
shows a plan request for GLM-5-Turbo served as GLM-5.3-Flash, an
undocumented reroute that could become a rejection without notice. Name
the two plan models directly. **GLM-5.5 remains unshipped as of
2026-09-22.** The Latest Models table tops out at 5.3-Flash, 5.3-FlashX,
5.3 and 5.2.

### GLM Coding Plan quotas

| Tier | 5-hour credits | Weekly credits |
| --- | --- | --- |
| Lite | 2,000 | 10,000 |
| Pro | 12,000 | 60,000 |
| Max | 28,000 | 140,000 |

Billing toggles Monthly / Quarterly (−20%) / Yearly (−30%); Lite is $18/mo
at monthly billing. Credit usage = (input × input multiplier + cached input
× cached multiplier + output × output multiplier) / 10,000. 5-hour credits
refresh 5 hours after consumption; weekly credits reset every 7 days.
GLM-5.3-Flash burns a third of GLM-5.3's credits (multipliers 2.3/0.56/8
vs 6.9/1.7/24, read 2026-09-15). MCP calls bill per call: Web Search, Web
Reader and Zread cost 1.2 credits each. Vision MCP bills through
GLM-5.3-Flash's multipliers (read 2026-09-22).

**Peak-hour discount is a routing signal, a 2× clock spread.** Peak hours
are Mon–Fri 14:00–18:00 UTC+8. Off-peak (including all weekends) is
charged at **50% of the standard credit rate**, peak at 1×. The 3×-peak
figures in the 2026-07-30 legacy-plan notice (GLM-5.3 at 1×/3×,
GLM-5.3-Flash at 0.4×/1.2×) describe legacy plans only. Scheduling
mechanical waves off-peak still pays. ZCode 3.8.1 added a 5-hour quota
reset benefit during off-peak hours. The devpack page claims up to 92%
savings versus pay-as-you-go under full off-peak use.

**Two promotions skew plan measurements until 2026-10-07.** From
2026-09-25 to 2026-10-07 every hour bills at the off-peak rate. Timing
buys nothing then, since the clock spread is 1×. The GLM-5.3-Flash campaign
(2026-09-03 to 2026-10-07, extended from 09-20) makes Flash use from 23:00
to 09:00 UTC+8 zero-quota through ZCode 3.10+ and gives other supported
agents doubled quota. It covers Flash only, not GLM-5.3. An account
already at its 5-hour or weekly limit sits out until the reset. A cost or
quota number taken on the plan in that window isn't comparable with one
taken outside it. Re-check both after 2026-10-07 (read 2026-09-22).

## Vendor benchmark claims — treat as self-reported

Z.ai's model card claims Terminal-Bench 2.1 = 81.0 and SWE-bench Pro = 62.1
for GLM-5.2, and "within 1% of Opus 4.8" on FrontierSWE. **GLM-5.2 does not
appear on the official tbench.ai 2.1 board at all.** The highest GLM entry
there is Claude Code + GLM-5.1 at 58.7% ± 1.2%, rank 17. GLM-5.3's card
claims +50% over 5.2 on Z.ai Code Bench, SOTA-open on Terminal-Bench 3.0
(4.6→28.3), and CyberGym 84.5% ahead of Mythos 5 (83.8) and GPT-5.6 Sol
(83.6) — same caution class. **The AA open-weights board on Intelligence
Index v4.3.2** (registry read, 2026-09-21): MiMo-V2.6-Pro 46, GLM-5.3 (max)
45, Kimi K3 (max) 44, GLM-5.3-Flash 42. GLM-5.2 read 34 on 2026-09-15.

## Headless — real, fully self-documenting, and separately configured

No web docs page describes it. The binary documents itself, so run
`--help` rather than searching. The CLI is `resources/glm/zcode.cjs`, a Node bundle with a
`#!/usr/bin/env node` shebang, run directly: `node zcode.cjs --help`. It
self-identifies as **`zcode 0.16.9`** on desktop 3.14.3 (read 2026-09-22),
versioned independently of the desktop app.

**Commands:** `app-server` (ZCode Protocol stdio server), `commands`,
`doctor`, `login`, `logout`, `plugins`, `skills`, `tui`, `version`.

**Flags that matter for a batch or benchmark harness:**

| Flag | Effect |
| --- | --- |
| `--prompt <text>` / `-p` | One-shot, no TUI. `-p` takes a **positional** prompt; `--prompt` takes the text as its value. Mixing them silently falls through to `--help`. |
| `--mode <m>` | `build` · `edit` · `plan` · `yolo`. **Default is `yolo` for `--prompt`.** Set it explicitly. |
| `--disallowed-tools` | Listed in 0.16.9's `--help`, with an argv handler in the bundle. Untested on a prompt run, so probe it before a harness relies on it. |
| `--allowed-tools`, `--max-turns` | **Absent from 0.16.9's `--help` and bundle.** A harness can't allowlist tools or cap turns by flag. |
| `--browser-use <mode>` · `--surface` · `--browser-executable <path>` · `--force-mcs` | Headless Browser Use backend and surfaces. `--force-mcs` exists to fix system-prompt projection when pointed at an **Anthropic** provider — precisely the config this file recommends. |
| `--target <text>` | Sets a session **goal** in headless mode, with `--target-replace`. |
| `--resume <sess_...>` / `-c` | Resume by id, or the latest session for the cwd. |
| `--json` | Machine-readable output where supported. |
| `--cwd`, `--settings`, `--attach`, `--verbose` | Directory, alternate settings file, file attachment, diagnostics. |

Slash commands include `/skill [name] [task]` (force a skill to load next
prompt), `/goal`, `/expert`, `/mode`, `/model`, `/compact`, `/rewind`,
`/fork`, `/mcp`.

**`zcode skills list` is a free, local, no-API-call oracle** for what ZCode
actually sees, and it prints scope, alias and resolved path per skill. Run
it before debugging anything skill-related. On this machine it reports
**`smartexec`, `smartplan`, `smartreview`, `smartvoice` as `user/zcode`**,
the six junctioned minus the two disabled. `zcode doctor` prints runtime
and packaging assumptions.

**The blocker worth knowing before you plan a benchmark.** The CLI needs its
**own** model provider, separate from the desktop app's. With none set it
refuses every prompt:

```
Error: Model config is missing. Create <user-home>\.zcode\cli\config.json
with an explicit model provider before running ZCode.
```

The desktop app's z.ai OAuth in `~/.zcode/v2/setting.json` does **not**
satisfy it. So on a machine where the GUI works fine, headless can still be
unrunnable — and wiring it means writing a provider (and credentials) into
`~/.zcode/cli/config.json`. That is the single gate between this repo and a
live-arm ZCode T-record.

## MCP

Full support, three transports: **stdio** (local commands), **HTTP**
(remote), **SSE**. Workspace config at `.zcode/config.json`. ZCode accepts
both the bare `{"server-name": {...}}` and `{"mcpServers": {...}}` shapes,
and can batch-import existing servers by scanning `~/.claude/settings.json`
and other external agent configs.

## Measured against a live install (2026-08-12; re-read 2026-09-22 at build 3.14.3, zcode.cjs 0.16.9)

Read from a real ZCode install on this machine rather than from docs. This
is observation, not a benchmark — it settles *installability*, not cost or
quality.

**The family is already live on ZCode here, and has been since at least
2026-08-03.**

- `~/.zcode/skills/{smartplan,smartexec,smartreview,smartvoice,smartwiki,smartdiagram}`
  are **NTFS junctions into `~/.claude/skills/`**, which are themselves
  junctions into this checkout. Created 2026-07-31.
- **ZCode follows the junction chain and canonicalizes it.** Its own config
  records the real target — `<your-checkout>/.claude/skills/...`
  — not the `~/.zcode/skills/...` path it was given. So the same
  live-checkout distribution `install-global.ps1` sets up for Claude Code
  reaches ZCode with no copy step.
- **Startup telemetry doesn't measure the family.** The
  `bootstrap.app.startup.plugins.completed` event's `skillRootCount` read
  4 in August and 8 on 2026-09-21 and 09-22. In 0.16.9 it counts plugin
  skill roots, not the junctioned user skills. `zcode skills list` is the
  oracle.

**A half-documented config surface.** The web FAQ names
`~/.zcode/cli/config.json` as the home of plugin and skill toggles, but not
its shape: a `skills` map keyed by **absolute `SKILL.md` path** with an
`{"enable": bool}` value. On this machine `smartwiki` and `smartdiagram`
are set `false` — worth knowing before concluding a skill "isn't loading."

**ZCode ships Claude's plugin directory as a built-in marketplace.**
`~/.zcode/cli/plugins/known_marketplaces.json` lists
`anthropics/claude-plugins-official` with source type `github`, alongside
Z.ai's own. The plugin page now says ZCode preloads the Claude Code
marketplace under Personal.

**Two `marketplace.json` shapes.** ZCode's local cache index,
`~/.zcode/cli/plugins/marketplaces/zcode-plugins-official/marketplace.json`,
has top keys `name`, `plugins` and an integer schema `version`. Every
entry's `source` is the literal `"filesystem"`. The **published** catalog
at `zai-org/zcode-plugins` has `description`, `description_i18n`, `name`,
`owner` and `plugins`, no `version`. Every `source` is a
`"./plugins/<name>"` **path**. `metadata` is in neither. The repo's ZCode
export script emits a hybrid (integer `version`, path `source`, no
`owner`), which needs a probe before it's trusted as a catalog.

**What is installed here and what is not.** The six skills are live. There
is **no `~/.zcode/agents/` and no `~/.zcode/AGENTS.md`**. So the family
runs here without its seats or its routing policy. The ZCode export
script emits both.

**Progressive disclosure works, and smartplan has already run here.** The
skill engine is not `app.asar` — it is `resources/glm/zcode.cjs`. Its
`skillHandler` loads **only `SKILL.md`'s own body**, then appends:

```
Base directory for this skill: <baseDirectory>
Relative paths in this skill are relative to this base directory.
```

and expands `${CLAUDE_SKILL_DIR}` / `${ZCODE_SKILL_DIR}` placeholders to that
path — the `CLAUDE_SKILL_DIR` name being a deliberate Claude Code
compatibility shim. References are then fetched by the model on demand with
`Read`, which takes Claude Code's own `file_path`/`offset`/`limit`
parameters and is **not** workspace-sandboxed (observed reading absolute
paths well outside any project). **That is Claude Code's progressive-
disclosure contract, implemented the same way.**

Live proof rather than inference: `~/.zcode/cli/rollout/` holds a real
`Skill` tool call for **`smartplan`** dated **2026-08-10** on model
`builtin:zai-coding-plan/GLM-5.2`, whose result is the byte-exact body of
this repo's `SKILL.md` wrapped in `<skill_content>` with that base-directory
footer. So the family has not merely loaded on ZCode — it has been
*invoked*. Corroboration at the product level: Z.ai ships Anthropic's own
document skills (`docx`, `pdf`, `pptx`, `xlsx`) as four plugins under
`resources/glm/packages/` (`documents-plugin`, `pdf-plugin`,
`presentations-plugin`, `spreadsheets-plugin`), with `docx` and
`pdf` still carrying full `references/` trees whose `SKILL.md` instructs the
model to load a named file out of its own reference directory mid-task.
Those would be dead on arrival if the mechanism did not work.

**One cap this repo has to respect:** the `Skill` tool truncates its whole
returned block at **100,000 bytes**, head-first, appending
`[Skill content truncated]`. `smartplan/SKILL.md` is ~10KB, far under it.
It's still a second ceiling above gate (i)'s per-file budgets.

**The harness config here is z.ai, not Anthropic.** `~/.zcode/v2/setting.json`
shows `providerFamilyDomain: "zai"`, OAuth mode, and the selected key
`coding-plan:builtin:zai-coding-plan`, with `enabledBuiltinAgentCliProviders:
["glm"]`. So the § Models recommendation above — prefer Anthropic direct if
the ladder should mean what it means elsewhere — is **not** what this
machine is currently doing.

## What is still unknown

Written down so it reads as an open question rather than a settled one:

- **How often a model reaches for a reference here is unmeasured (n=1).**
  The harness half is settled (T37). The one traced `smartplan` session
  read eleven other files without opening a reference, which may be
  correct inline routing, since only fan-out REQUIRES `flow.md`. One
  sample can't separate the two. See
  the development repo's benchmark records.
- **Whether a qualified seat pin resolves, and whether a project
  `.zcode/agents/` seat loads.** Both are code-read. Neither has been
  dispatched, since no seat is installed here.
- Whether ZCode tolerates this repo's `.claude-plugin/marketplace.json`
  location undocumented-but-working. The junction path sidesteps it,
  which is why the skills load anyway.
- **Any cost or quality number. Nothing here is benchmarked.** No cost or
  quality T-record exists for ZCode (T37 is observational only).
  Installability is now observed; routing economics are not.
