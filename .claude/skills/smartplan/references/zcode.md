# smartplan §C deep reference — ZCode (Z.ai) levers & limits

> Facts verified 2026-08-12 against `zcode.z.ai/en/docs`, `docs.z.ai`, and
> Z.ai's Terms of Use. Every "not documented" below is a genuine absence at
> the source, not a shrug: ZCode's docs are young and several pages describe
> a settings **form** rather than the on-disk file it writes.
>
> **Part of this file is measured, not read** — see § Measured against a
> live install. ZCode is installed on this machine and has been serving this
> skill family since at least 2026-08-03.

Load this only when the session is ZCode. For the flow itself, see `flow.md`.

## What ZCode is

A proprietary desktop **Agentic Development Environment** from Z.ai — not a
CLI, not an IDE fork. Electron, with macOS (Apple Silicon + Intel), Windows
(x64 + ARM64) and Linux (x64 + ARM64, marked Beta) installers. Vendor's
current release is **v3.7.6, 2026-08-12**. The published changelog only
reaches back to 3.3.5 on 2026-07-13.

**Mind the version gap when reading this page.** The build installed on this
machine is **3.6.5.4145** (confirmed twice, from `ZCode.exe` VersionInfo and
the HKLM uninstall registry entry, 2026-08-12) — one minor version behind
the docs everything below was verified against. So a feature the docs
describe may not exist in the running build. That specifically covers the
v3.7.5 subagent reasoning-effort setting and per-subagent custom models for
idle tasks: **documented, and not necessarily present here.**

**It is not open source.** The Terms of Use assert IP ownership by JINGSHENG
HENGXING TECHNOLOGY PTE. LTD. and prohibit reverse engineering. The only
`zai-org` GitHub repo matching "zcode" is `zai-org/feedback`, an issue
tracker with no source. Blog headlines calling ZCode "the open-source coding
agent harness" are aggregators contradicted by the vendor's own ToS — don't
repeat them.

## The one fact that decides everything

**ZCode does not read `CLAUDE.md` at runtime.** It reads `AGENTS.md` at two
scopes: `~/.zcode/AGENTS.md` (user) and a workspace `AGENTS.md`. `CLAUDE.md`
is consumed once, during onboarding, purely as a migration source — the
built-in flow copies `~/.claude/CLAUDE.md` into `~/.zcode/AGENTS.md`.

It **does** walk directory levels. The shipped `zcode-configuration-guide`
skill states that
ZCode "searches for the workspace `AGENTS.md` from the current working
directory **upward until the detected project root**." **Merge order:** the
user file injects first, then the workspace file, so workspace instructions
can narrow or override user defaults. `/init` targets the workspace file,
never the user default.

So a policy that lives in `CLAUDE.md` is **invisible here**. On ZCode the
standing-instruction surface is `AGENTS.md`, and the skill surface is
`SKILL.md`. Plan for both.

## The tiering lever — real, but coarser than §A

ZCode has a **per-agent model pin**, closest in shape to Copilot's
`.github/agents/` rather than Claude Code's per-call `model:` parameter.

- Custom subagents are Markdown files at `~/.zcode/agents/<name>.md`.
- The settings form exposes **Name, Color, Model, Description, Available
  tools, System prompt**. The Model control offers "Inherit default" (follow
  the primary agent's current model) or a specific model.
- Invocation is automatic delegation on description match, or explicit
  `@name`. Two built-ins ship: `general-purpose` (all tools) and `Explore`
  (read-only).

**Four limits that change how you seat work here:**

1. **The frontmatter keys are undocumented.** `/en/docs/subagents` describes
   the settings *form*, shows no `---` block and names no keys. The only
   page stating agent frontmatter is the Plugin reference, and it names just
   **`name` and `description`** — no `model` key for agents anywhere. The
   same page publishes a full **command** frontmatter table that *does*
   carry `model` ("Overrides the default model"), so the omission for agents
   reads as deliberate contrast rather than an oversight. Hand-authoring
   `~/.zcode/agents/<name>.md` with a `model:` key is undocumented at time
   of writing. Create the seat through the UI and let ZCode write the file.
2. **There is no per-call or per-dispatch model override.** Nothing in the
   subagents docs offers one, and the hooks page exposes `model` only as
   read-only `SessionStart` input. The nearest real per-invocation override
   is on **commands**, not agents.
3. **Subagents are Beta and user-level only.** The docs say "User-level
   custom subagents are rolling out. The capability and its scope may still
   change" (the CN tree marks it 灰度上线, phased rollout), and state that
   workspace/project-level subagents are **not yet supported**. So a
   per-repo pinned seat isn't available — every seat is global to the
   machine, which is the opposite of `.github/agents/`'s per-repo shape.
4. **The docs lag the changelog.** v3.7.5 (2026-08-10) added a subagent
   **reasoning-effort** setting and per-subagent custom models for idle
   tasks. Neither appears on the subagents page. Treat that page as stale
   and check the changelog before concluding a lever doesn't exist.

**Consequence for the flow:** ZCode can hold the seats, but it cannot vary a
seat's model mid-wave. Pin the seats once, dispatch against them, and treat
an escalation as *switching which seat you address* rather than raising a
parameter.

## Parallelism

Subagents launched together **run in parallel**, and the main task **blocks**
until all finish. A **background mode** also exists where the main task does
not wait and can end its turn; background `Explore` subagents are restricted
to read-only tools. Scheduled and idle tasks can be configured with a
specific model per subagent.

That blocking default is the important half: it makes ZCode's foreground
fan-out a barrier, not a pipeline. Size waves accordingly.

## Skills

ZCode ships first-class Agent Skills using `SKILL.md`.

- User-level path: `~/.zcode/skills/<skill-name>/SKILL.md`.
- Invoked with `$skill-name` in chat, or through the `/` menu under a Skills
  group.
- ZCode can **import** skills from Claude Code and other agents.

**Three caveats, verified 2026-08-12:**

- **The docs overstate the frontmatter allowlist; the code parses two
  fields.** The Plugin page lists five keys (`name`, `description`,
  `when_to_use`, `license`, `metadata`). The shipped discovery path
  (`readLooseFrontmatterFields` — strict YAML via the `yaml` package first,
  loose line parser as fallback) extracts **only `name` and `description`**.
  No `when_to_use` and no `allowed-tools` are recognized as parsed fields
  anywhere in the bundle; both appear solely as literal example text inside
  bundled example skills. Extra keys are tolerated rather than rejected, so
  this repo's frontmatter is safe either way — but do not *rely* on
  `when_to_use` doing anything. A Settings-UI linter separately reports
  `skill_unknown_frontmatter`, `skill_description_too_long` (>1024 chars),
  and `skill_invalid_name` (lowercase letters, digits and hyphens only).
- **The full discovery order, from the shipped configuration guide.** The
  *web* Skill page gives only the user path. Workspace scope is documented
  inside the product rather than on the web. Earlier locations win:

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
  but only the first in order loads — the rest are shadowed. That is the
  opposite of Claude Code's enterprise > personal > project ordering in one
  respect worth noting: here **user scope outranks workspace**, so a
  personal copy silently shadows a repo's own.

  Plugin roots are recognized by `.zcode-plugin/plugin.json` **and**
  `.claude-plugin/plugin.json` **and** `.codex-plugin/plugin.json` — it
  reads OpenAI Codex's manifest name too.
- **Discovery is `SKILL.md`-scoped, not naive.** The walker recurses but
  yields a directory only when it directly contains a file named
  `SKILL.md`, skipping `node_modules`, `dist`, `build`, `out`, `target`,
  `vendor`, `coverage`, `.cache`, `.next`, `.turbo`, `.venv`, `__pycache__`
  and dotdirs other than `.system`. So a `references/` folder full of `.md`
  files is walked past, never mistaken for extra skills.
- **`references/` is undocumented but fully supported — read the code, not
  the docs.** Zero occurrences of `references/` across every ZCode docs
  page, English and Chinese. But the shipped engine implements Claude
  Code's exact progressive-disclosure contract. **Settled 2026-08-12 at the
  code level; see § Measured against a live install.** Progressive
  disclosure works here, so the byte ratchet stays affordable on ZCode.

## Plugins — and why this repo does NOT install as-is

The plugin format looks compatible and mostly is:

- Manifest at `.zcode-plugin/plugin.json` **or** `.claude-plugin/plugin.json`
  (documented lookup priority, on the plugin and hooks pages).
- A plugin bundles `commands/`, `skills/<name>/SKILL.md`, `agents/*.md`,
  `hooks/hooks.json` and `.mcp.json`.
- Marketplaces use a root `marketplace.json` carrying `name`,
  `plugins[].source` and `pluginRoot` — all three field names verified.
- Documented as plain GA. No beta, preview or SKU gate anywhere on the page.

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
   strict. Top-level `owner` and `metadata` are likewise absent from ZCode's
   documented top-level set.

**The skills payload is the portable part.** The `skills/<name>/SKILL.md`
layout and `name`/`description` frontmatter match this tree, and ZCode
separately documents importing skills "from other AI coding tools such as
Claude Code". The packaging around them is what needs building — a root
`marketplace.json` plus a real `plugin.json`. That's what
the repo's ZCode export script generates.

## Hooks

Seven events, a **superset** of Claude Code's: `SessionStart`,
`UserPromptSubmit`, `PreToolUse`, `PermissionRequest`, `PostToolUse`,
`PostToolUseFailure`, `Stop`. No `PreCompact`, `Notification`,
`SubagentStop` or session-end equivalent.

Config in three places, executed user → workspace → plugins:
`~/.zcode/cli/config.json`, `<workspace>/.zcode/config.json`, and a plugin's
`hooks/hooks.json`.

**Hooks here can deny**, unlike this repo's warn-only Claude Code guardrail:
`PreToolUse` returns `"permissionDecision": "deny"`, `UserPromptSubmit`
returns `"continue": false`. Read `docs/enforcement-hook.md`'s safety note
before porting the tiered-dispatch hook — a denying variant of it bricks the
default policy, and that warning applies with more force on a harness where
deny actually works.

**`hooks.enabled: true` IS required for configuration-file hooks.** They are
disabled by default. When any plugin contributes a hook, the hook runner
enables automatically.

Source, verbatim from the shipped `zcode-configuration-guide` skill:
"Configuration-file hooks must set `hooks.enabled: true` to run (disabled by
default)." The public web docs omit this, so trust the bundled guide.

## Goal Mode — a built-in verify gate

Goal Mode is not just a planner. At the end of **every round** ZCode runs a
**separate check** to decide whether the objective was met, and that check
demands **artifact evidence** rather than a confident-sounding reply. If the
objective is unmet it produces the next step and auto-starts another round.
Built-in commands are `/goal` and `/compact`.

This is the closest thing in any tracked harness to smartcheck shipped in
the box. It does not replace an *independent* verifier — same-context
self-checking is tier 3 on `SKILL.md`'s verify floor — but on ZCode the
floor is met by default rather than by discipline. Reach for `/goal` before
rebuilding the loop out of this flow.

## Execution modes

Four modes cycled with Shift+Tab: **Confirm Before Changes** (default),
**Auto Edit**, **Plan Mode**, **Full Access** — the same interaction pattern
as Claude Code. Separately, **Thought levels** (Off, High, Max) control
reasoning depth for GLM-5.2 through a thinking icon in the chat input.
Models and execution modes can both be switched mid-task.

## Models — ZCode is not GLM-only

Nine provider families are configurable: **Z.ai (Global), BigModel (China),
Anthropic, OpenAI, OpenRouter, Moonshot/Kimi, MiniMax, Xiaomi MiMo**, and
custom Anthropic- or OpenAI-compatible endpoints including self-hosted.
Documented base URLs include `https://api.z.ai/api/coding/paas/v4`,
`https://api.z.ai/api/anthropic`, `https://api.anthropic.com`,
`https://api.openai.com`, `https://openrouter.ai/api`.

**So the full Anthropic ladder is reachable from ZCode.** A smartplan
deployment here can run the same 5:2:1 seats it runs on Claude Code, billed
through an Anthropic key, with ZCode supplying the harness. That is the
configuration to prefer if you want the tiering policy to mean what it means
everywhere else.

### GLM prices (vendor page, 2026-08-12, $ per 1M tokens)

| Model | Input | Cached input | Output |
| --- | --- | --- | --- |
| GLM-5.2 | 1.40 | 0.26 | 4.40 |
| GLM-5-Turbo | 1.20 | 0.24 | 4.00 |
| GLM-4.5-Air | 0.20 | 0.03 | 1.10 |
| GLM-4.7-FlashX | 0.07 | 0.01 | 0.40 |
| GLM-4.7-Flash | Free | Free | Free |
| GLM-4.5-Flash | Free | Free | Free |

Cached-input **storage** is listed "Limited-time Free" for all paid models.

**GLM-5-Turbo was priced wrong in this repo** at 0.60 / 2.20 — that is the
GLM-4.7/4.6/4.5 rate. The real figure is roughly 2× higher, which means
**T32's dollar column for the z.ai arm is understated by about 2×**. T32 is
the only benchmark pricing that arm in dollars, so the record needs the
correction noted rather than silently repriced.

**GLM-5.5 has not shipped** as of 2026-08-12. The release-notes page ends at
GLM-5.2 (2026-06-16) and no 5.3 or 5.5 appears in the pricing table.
**Amended 2026-08-20: Artificial Analysis now lists GLM-5.3 at Intelligence
Index 60**, tying Kimi K3. So 5.3 exists as a scored model even though z.ai's
own pricing page had not listed it when this was written — treat the pricing
table as the authority for what you can BUY here, and the boards as the
authority for what exists. 5.5 remains unshipped. The
"rumored for August" hedge elsewhere in this repo is still accurate but is
now 12 days into the month it names. <!-- RECHECK:2026-09-01 -->

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

**Peak-hour surcharge is a routing signal.** GLM-5.2 and GLM-5-Turbo consume
at **3×** during Mon–Fri 14:00–18:00 UTC+8 and 1× off-peak, with off-peak
charged at 50% of the standard rate. That's a 6× spread across the clock on
the same model — larger than most tier gaps in `model-classes.md`. Schedule
mechanical waves off-peak before reaching for a cheaper model.

## Vendor benchmark claims — treat as self-reported

Z.ai's model card claims Terminal-Bench 2.1 = 81.0 and SWE-bench Pro = 62.1
for GLM-5.2, and "within 1% of Opus 4.8" on FrontierSWE. **GLM-5.2 does not
appear on the official tbench.ai 2.1 board at all.** The highest GLM entry
there is Claude Code + GLM-5.1 at 58.7% ± 1.2%, rank 17. Artificial Analysis
now places GLM-5.2 **second** among open-weight models at Intelligence Index
53, behind Kimi K3 at 60.

Model ID `glm-5.2`, 1M context, 128K max output.

## Headless — real, fully self-documenting, and separately configured

No web docs page describes it. The binary documents itself, so run
`--help` rather than searching. The CLI is `resources/glm/zcode.cjs`, a Node bundle with a
`#!/usr/bin/env node` shebang, run directly: `node zcode.cjs --help`. It
self-identifies as **`zcode 0.16.1`** — versioned independently of the
desktop app, which is 3.6.5 here.

**Commands:** `app-server` (ZCode Protocol stdio server), `commands`,
`doctor`, `login`, `logout`, `plugins`, `skills`, `tui`, `version`.

**Flags that matter for a batch or benchmark harness:**

| Flag | Effect |
| --- | --- |
| `--prompt <text>` / `-p` | One-shot, no TUI. `-p` takes a **positional** prompt; `--prompt` takes the text as its value. Mixing them silently falls through to `--help`. |
| `--mode <m>` | `build` · `edit` · `plan` · `yolo`. **Default is `yolo` for `--prompt`.** Set it explicitly. |
| `--allowed-tools` / `--disallowed-tools` | Comma or space separated, and `--disallowedTools` accepts a `Bash(git *)`-style scope. |
| `--max-turns <n>` | Hard turn cap on a headless prompt. |
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
**`smartexec`, `smartplan`, `smartreview`, `smartvoice` as `user/zcode`** —
the four the startup telemetry predicted, with the two disabled ones
correctly absent. `zcode doctor` prints runtime and packaging assumptions.

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
ZCode T-record.

## MCP

Full support, three transports: **stdio** (local commands), **HTTP**
(remote), **SSE**. Workspace config at `.zcode/config.json`. ZCode accepts
both the bare `{"server-name": {...}}` and `{"mcpServers": {...}}` shapes,
and can batch-import existing servers by scanning `~/.claude/settings.json`
and other external agent configs.

## Measured against a live install (2026-08-12)

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
- **Startup telemetry confirms the load.** The
  `bootstrap.app.startup.plugins.completed` event reports
  `skillRootCount: 4` on both the 2026-08-03 and 2026-08-09 sessions. Six
  skills are junctioned and two are disabled, which is an exact match.

**An undocumented config surface.** `~/.zcode/cli/config.json` carries a
`skills` map keyed by **absolute `SKILL.md` path** with an `{"enable":
bool}` value. Nothing in the ZCode docs describes it. On this machine
`smartwiki` and `smartdiagram` are set `false` — worth knowing before
concluding a skill "isn't loading."

**ZCode ships Claude's plugin directory as a built-in marketplace.**
`~/.zcode/cli/plugins/known_marketplaces.json` lists
`anthropics/claude-plugins-official` with source type `github`, alongside
Z.ai's own. That is stronger ecosystem compatibility than the docs claim.

**The real `marketplace.json` shape**, read from the marketplace ZCode
actually ships: top-level `name`, `plugins`, and `version` — where `version`
is an **integer schema version (1)**, not a semver string. Entries carry
`name`, `description`, `version`, `source`, `author`, `category`,
`displayName`, `icon`. Two mismatches against the docs: `pluginRoot` does
not appear in the official file, and every entry's `source` is the literal
string `"filesystem"` — a source *type* — where the docs describe `source`
as a path. The repo's ZCode export script emits the observed shape and
records the `source` ambiguity rather than guessing.

**What is installed here and what is not.** The six skills are live. There
is **no `~/.zcode/agents/` and no `~/.zcode/AGENTS.md`** — so on this
machine the tiered agent seats and the standing routing policy are *not*
installed, only the skills. That gap is exactly what the ZCode export
script emits, and it means the family currently runs on ZCode without its policy
surface.

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
`docx` and `pdf` skills under `resources/glm/packages/`, complete with real
reference trees whose `SKILL.md` instructs the model to load a named file
out of its own reference directory mid-task. Those would be dead on arrival
if the mechanism did not work.

**One cap this repo has to respect:** the `Skill` tool truncates its whole
returned block at **100,000 bytes**, head-first, appending
`[Skill content truncated]`. `smartplan/SKILL.md` is ~5KB, so there is no
risk today — but it is a second, larger ceiling sitting above gate (i)'s
per-file budgets.

**The harness config here is z.ai, not Anthropic.** `~/.zcode/v2/setting.json`
shows `providerFamilyDomain: "zai"`, OAuth mode, and the selected key
`coding-plan:builtin:zai-coding-plan`, with `enabledBuiltinAgentCliProviders:
["glm"]`. So the § Models recommendation below — prefer Anthropic direct if
the ladder should mean what it means elsewhere — is **not** what this
machine is currently doing.

## What is still unknown

Written down so it reads as an open question rather than a settled one:

- **How often a model reaches for a reference here is unmeasured (n=1).**
  The *harness* half is settled — T37 observes both halves independently:
  ZCode hands the model the skill's base directory, and its `Read` retrieves
  arbitrary absolute paths outside any workspace. A reference file is just
  such a path. What no local log shows is a model *choosing* to compose them,
  and the one traced `smartplan` session read eleven other files without
  opening a reference. That may be correct inline routing rather than a
  failure — `SKILL.md` says fan-out REQUIRES loading `flow.md`, so an
  inline-routed task **should not** read it. One sample cannot separate the
  two. See the development repo's benchmark records.
- The real on-disk frontmatter keys for `~/.zcode/agents/<name>.md`. Nothing
  to read here, because no agents are installed.
- Whether ZCode tolerates this repo's `.claude-plugin/marketplace.json`
  location undocumented-but-working. The junction path sidesteps the
  question entirely, which is why the skills load despite the packaging
  mismatch described above.
- **Any cost or quality number. Nothing here is benchmarked.** No T-record
  exists for ZCode as a harness. Installability is now observed; routing
  economics are not.
