# smartplan §B deep reference — Copilot CLI economics & standing levers

> Facts verified 2026-07-06; re-swept 2026-07-24, 2026-08-05, 2026-08-12,
> 2026-09-15, 2026-09-20, 2026-09-22. Re-check trigger: **ten** Copilot retirements —
> four on 2026-10-02 (Gemini 3.5/3.6 Flash, Kimi K2.7 Code, Opus 4.7), six
> more on 2026-10-19 (Gemini 3.7 Flash, GPT-5.5, GPT-5.4, GPT-5.4 mini,
> GPT-5 mini, Grok 4.5).

Load this only on Copilot CLI — for dispatch mechanics beyond flow.md §B's
summary, budget decisions, fan-out sizing, or repo setup.

## Contents

- The five levers (most reliable first)
- AI-credit economics (billing changed 2026-06-01)
- Context tiers (docs, 2026-09-15)
- Per-seat model control isn't guaranteed here (checked 2026-08-05)
- Dispatch engine — task tool vs /fleet (updated 2026-07-09)
- Command naming — plugin sp, executor hidden (why it's set up this way)
- Marketplace install vs project-local — they don't merge
- Standing levers (set once, help every session)
- Testing against Copilot cheaply (the probe-cost playbook, 2026-07-12)
- Running real UE5 work cheaply on Copilot (not just probing, 2026-07-12)

## The five levers (most reliable first)

| # | Lever | How |
| --- | --- | --- |
| 1 | Cheap default | `/fleet` subagents use a low-cost model by default — native. |
| 2 | Agent frontmatter | `model:` on the seven shipped `.github/agents/` profiles — slug form (`claude-opus-5` / family alias `opus`), or a display name since 1.0.24 (untested for a model the build doesn't list). Since v1.0.83 an ordered `models:` list takes the first plan-reachable model. Each list leads with the newest version of its line (`model-classes.md` § How to edit). `model:` stays the older-build fallback. `modelPolicy: required` refuses substitution. `reasoningEffort` sets effort. Pins can be silently downgraded (§ Per-seat model control), so never mix Auto with tiered dispatch. |
| 3 | `/subagents` | Sets default and per-agent subagent models in-session (alias `/agents`). |
| 4 | NL directive | Name agents inline: `use @smartplan-planner to plan, then @smartplan-implementer per item, then @smartplan-verifier`. |
| 5 | Scoped pins | `/model --session` pins model/effort for this session only (v1.0.72). **`/model plan` pins a plan-mode-only model (v1.0.74) — the native analog of §A's `opusplan`:** plan on Opus, revert automatically on exit; captures the core rule with zero dispatch machinery. |

## AI-credit economics (billing changed 2026-06-01)

Token-metered AI credits (1 credit = $0.01). Monthly allowances: Pro 1,500 /
Pro+ 7,000 / Max 20,000 per user, of which 500 / 3,100 / 10,000 is a
variable flex share that can move. All reset 00:00 UTC on the 1st.
Business 1,900 and Enterprise 3,900 per
user, pooled, since the promo ended 2026-09-01 (plans data, 2026-09-15).
**Subagent tokens bill**, so tiering the fan-out is the bill, not politeness.

Copilot bills Anthropic's list rates, so `model-classes.md`'s Anthropic rows
are the Copilot rows too (models-and-pricing, re-checked 2026-08-12).
Four SKUs list at $10/$50: "Claude Fable 5", Fable 5.1 (cache read $0.25),
"Claude Opus 4.8 (fast mode) (Preview)" and GPT-6 Astra (>272K $20/$75,
the table's top). The Claude three are planning-only.

**soft caps (public preview, CLI 1.0.66+ / SDK 1.0.5+):** `/limits`
(interactive), `--max-ai-credits` (programmatic). An in-flight response
finishes before the stop takes effect. A cap can't be set under 30
credits (1.0.67). GitHub's docs disagree on scope. The CLI reference
resets a cap each user message. The session-limit how-to spans the
session. A `-p` run is one message either way.
Use them to lean on budget pressure, not just watch `/usage` (quota bars).
**Caveat (T25, 2026-07-12): caps are visible to the
model and can suppress skill loading** — a capped session skipped
`/smartplan` citing "limited credits"; cap leaves, not a skill-driven
orchestrator. (`-p` doesn't expand skill slash-commands, so loading is
model-mediated. T30+B5, 2026-07-25: headless `-p` sessions DO get the
descriptions listing (~+780 tokens) and one-context tasks then run inline off
the description alone, the FAST PATH working as designed at 6/6 parity with
no body load. Whether a fan-out-shaped task loads flow.md headless is
untested.) **Caveat (T28, 2026-07-21): junctioned companion skills
whose target lies OUTSIDE the project root are unreadable** — the
sandbox denies reads through the junction (a review session honestly
stood down, 13.2 cr sunk). Trust the checkout with `--add-dir
<checkout>` (or the trusted-directories config) in any project that got
`install-project.ps1` junctions.

Default subagent concurrency is per plan: Free 2, Pro/Pro+ 4, Max 8,
Business 16, Enterprise and usage-based billing 32, depth 6 (CLI
reference, read 2026-09-22). It doesn't say which row a Pro user on
usage-based billing gets. The same page's env-var table says 32, depth 4.
The `subagents.*` knobs (`maxConcurrency` cap 32, `maxDepth` cap 256,
`disabledSubagents`) live in `~/.copilot/settings.json` or `/settings`,
the first two honored only on usage-based billing. Size waves to the row.

**`/usage` has a real ceiling — session-level only, confirmed 2026-07-08.**
GitHub's own CLI reference documents it as "session usage metrics and
statistics, including per-model token totals" — there is no skill,
subagent, plugin, or MCP-server attribution *under `/usage` itself*, unlike
Claude Code's `/usage`. Don't let a session import Claude Code's
`/usage`-attribution language here. A live 2026-07-08 case did exactly that,
quoting §A's skills/subagents breakdown as Copilot's own behavior right after
correctly observing that `/usage` is aggregate-only.
CLI 1.0.85 (2026-09-16) added per-model AI-credit rows, still with no
skill or subagent attribution. This box runs 1.0.83.

**Live-tested 2026-07-09:** the finer breakdown lives
elsewhere — `/context` under `/experimental` shows per-source attribution
(skills, subagents, MCP servers, plugins), and `/statusline`'s
`ai-credits`/`ai-used` options give always-visible live spend. Check
`/context` first; the fallback is `run-state.md`'s rows (routed-tier
*intent*, not bill-confirmed landing).

**Headless metering is native now (measured T30):** `-p` runs print an
`AI Credits` footer, and `~/.copilot/session-store.db`'s
`assistant_usage_events` table carries per-request nano-AIU (1e9 = one
credit) — per-session spend is exactly measurable without `/usage`.

Plan gating: Opus 4.8, Opus 5 (GA 2026-07-24), Opus 5.5 (GA 2026-09-22), Fable 5 and Fable 5.1 (GA 2026-09-01) are documented Pro+/Max. (T30+B4, 2026-07-25: an account that refused Opus 4.8 on 07-11 served both Opus models, so tiers change. Verify, don't assume the gate.) Both
Fables retain data by default for Anthropic's safety classifiers, where
other Claude models stay zero-data-retention (plans footnote, 2026-09-15).
**Re-derived 2026-09-15 from `github/docs`
`model-supported-plans.yml`:** plain Pro excludes GPT-5.5, GPT-5.6 Sol,
GPT-6 Sol, GPT-6 Astra, GPT-5.4 nano and every Opus and Fable SKU —
everything else on the roster it reaches, including Terra, GPT-6 Luna,
GPT-5.3-Codex, Kimi K3, the Gemini Flashes and the Groks (re-read
2026-09-22).

**Cross-vendor model economics.** Copilot exposes Anthropic, OpenAI,
Google, xAI, Moonshot and Microsoft models. Grok 4.5 and 4.6 are GA on
every paid plan at xAI list 2 / 6.

Seat verdicts, cross-vendor:

- Planner is **Opus 5.5** (4/20, Pro+/Max). The planner and reserve
  seats list `[claude-opus-5.5, claude-opus-5]`. The 5.5 slug is in
  `copilot help config` from prerelease 1.0.89-0, not stable 1.0.88. A
  stable build lands on Opus 5. GPT-6 Astra gets no seat: it lists at
  10/50 and scores under Opus 5.5 on AA (53 vs 58) and vals.ai TB4
  (57.07 vs 61.62).
- **Coding leaves:** `@smartplan-implementer-cheap` and `@smartplan-scout`
  list `[gpt-6-luna, gpt-5.6-luna, claude-haiku-4.5]` at
  `reasoningEffort: low`. GPT-6 Luna (0.10 / 0.50) leads as the newest
  Luna, level with GPT-5.6 Luna on the AA index (37.26 vs 37.32) at
  under half the cost per task. No build names `gpt-6-luna` yet. Today
  the list lands on GPT-5.6 Luna. That one beats
  Sonnet 5 on vals.ai SWE-V (93.0 vs 79.6) and tbench.ai TB4 (17.3% vs
  12.4%) but trails on vals.ai TB4 (4.55 vs 8.08). Never-Cheap classes
  (security, C++ UB, concurrency, templates) start at the Mid seat, the
  fail-twice target too. Neither Luna has a T-record. Every result stays
  behind the cross-family verifier. A bounce rate past ~20-30%
  reclassifies it back.
- **Mid seat:** `@smartplan-implementer` lists
  `[gpt-6-sol, claude-sonnet-5]` at the author's direction. GPT-6 Sol lists
  at Sonnet 5's 2/10 with no tbench.ai or vals.ai row yet (AA's own TB4
  run: 43.9%). Its predecessor GPT-5.6 Sol leads Sonnet 5 on every board
  both sit on. Sol is Pro+ and up. No build names `gpt-6-sol` yet. Today
  every plan lands on Sonnet 5. Untrialed.
- **Verifier:** `gemini-3.8-flash` (in `copilot help config` from CLI
  1.0.83), cross-family to both the Claude and GPT seats per `check.md`'s
  Family decorrelation rule. At max-savings, `@smartplan-verifier-cheap`
  runs Cheap leaves on the Luna list. The pin moved from T34-cleared 3.6
  Flash (retiring 2026-10-02) to its named successor 2026-09-16,
  **unmeasured** until a T34 re-run. Copilot's built-in rubber-duck critic
  runs an opposite-family model too (every family from 1.0.87). It has no
  PASS/FAIL protocol and doesn't replace smartcheck.
- **Haiku 4.5** is the Copilot fallback when the picker lacks Luna, and
  stays the Claude Code Cheap floor (Luna is not on that harness). GPT-5
  mini stays a deliberate-trial candidate, never a default off secondhand
  benchmark blogs.

Opus 5.5 and GPT-6 Luna lead by `model-classes.md`'s newest-version
rule. GPT-6 Sol over Sonnet 5 is an author move across lines.
Fall-through past a slug the build doesn't know is untested, since this
box is on Copilot Free.
`copilot help config` prints a per-build static list that needs no login or
paid plan. Availability comes from the authenticated server catalog. On
Free, 1.0.89-0 refused `--model claude-opus-5.5` as "not available"
though its static list names it. The `/model` picker also shows server
models the build doesn't list (code-read).
So a slug is live once a build names it or a paid-plan probe dispatches it.

**The cost ceiling (`routing.md` § The cost ceiling) binds pinned seats
too.** With the session pinned — never Auto, where the incumbent is
unknown and pins are ignored — no initial leaf pick prices above the
session's own model. The profile set above is priced for that, and
anything above the session seat (Strong verifier, Opus planner, a
never-Cheap leaf forced to the Mid seat on a Luna session) is the plan-gate
ask, not a silent default.

**Long-context surcharge.** The OpenAI and xAI SKUs charge one that
Anthropic rows lack (Sol >272K $8/$30 · GPT-5.5 >272K $10/$45 · GPT-5.4
>272K $5/$22.50 · Terra >272K $4/$18 · Luna >200K $0.40/$1.80 · GPT-6 Sol
>272K $4/$15 · GPT-6 Luna >272K $0.20/$0.75 · Grok ≥200K $4/$12,
2026-09-22) — price
big-context leaves and verifies off that column.

**Roster watch (re-swept 2026-09-22).** New-SKU details live in
`model-classes.md`. **Landed 2026-09-22: Claude Opus 5.5** (Pro+ and up,
4/20), **GPT-6 Sol** (Pro+, 2/10) and **GPT-6 Luna** (every paid plan,
0.10/0.50). None is in Auto. Each leads a seat's
list above. Business/Enterprise get new GA models by default since the
2026-08-26 policy. Opus 4.8 **fast mode**:
$10/$50, cache-read $1, write $12.50; still "(preview)", Pro+-gated.
Trust the changelog's 2026-10-19 batch (2026-09-18) over GitHub's
retirement table, which lacked it at the 2026-09-22 read.

**Auto model selection, the honest retreat candidate (re-checked
2026-08-05, tiers added 2026-09-20):** Auto has been **GA since 2026-04-17
across all plans**, and it routes on *evaluated task complexity*, not
availability alone (changelog 2026-04-17, auto-model-selection). **Three
user-selectable Auto tiers landed with the 2026-09-14 docs change —
Efficiency, Balance, Intelligence** — in VS Code, Copilot CLI and the
Copilot App: a complexity dial over Auto's own routing. Usage bills as the
model Auto picks, plus the 10% paid-plan discount. Auto won't pick a model
the plan excludes. **GPT-5.3-Codex is the base and the LTS last resort** on
Business and Enterprise. CLI Auto's 12-model pool (GPT-6 Astra from
2026-09-16) holds no Gemini after 2026-10-19 unless GitHub adds 3.8 Flash,
which no Auto pool lists. Say the uncomfortable part plainly:
description-level routing is smartplan's stated surviving value, and on this
harness it's first-party now. What's left for us here is the regime gate and
the verify floor, not the act of picking a model. Routing runs "along
natural cache boundaries" so it stays cache-safe, though that's the page's
rationale rather than a worded guarantee. Split guidance:
**inline/fast-path sessions → Auto is the sensible default, and the fair
control to measure against.** On individual plans Auto can also route to
codenamed evaluation models. Record or disable the evaluation-models
setting for a control arm. Sessions *dispatching a tiered wave* still pin
explicit models (under Auto a subagent inherits the resolved session model
whatever its pin says, per the CLI reference, read 2026-09-15).

**Per-seat effort rides frontmatter:** `reasoningEffort: low` on
`smartplan-implementer-cheap` and `smartplan-scout`, `high` on the Mid
implementer, the Reserve and both verifiers, applied on `task`
dispatch and, from 1.0.88, on selection (unprobed). The repo's
`.github/copilot/settings.json` honors a fixed key list and silently
ignores every `subagents.*` key (CLI config reference, read 2026-09-22).
`subagents.agents.<name>` works only in `~/.copilot/settings.json`.
Reasoning bills as output. The planner stays unpinned, so the mode's effort lands on the plan turn.

**Verify on credits:** the default verify ladder here is `check.md`'s
credit-billed default — script stage first, model pass batched + sampled
(T22: one batched model verify alone was 83% of the entire inline arm).

## Context tiers (docs, 2026-09-15)

Default tier (picker, 2026-08-06): every Claude model here is **264K**, and
so are the Geminis. GPT-5.6 Sol/Terra, 5.5 and
5.4 get **400K**; Luna and Grok 4.5 **328K**. More room than a Claude seat
means a cross-family seat: context, not tiering. Reasoning reads Medium
everywhere except **Kimi K3 (High)**. Most also offer a **selectable 1M
tier** (`--context long_context`).

## Per-seat model control isn't guaranteed here (checked 2026-08-05)

§A is honest about Claude Code's #43869. Copilot's version runs the other
way, and it's two separate reports:

- **copilot-cli#2758** (open, opened 2026-04-16). When the session model has
  a lower cost multiplier, sub-agent model overrides get downgraded to the
  session model. That covers both carriers we use, `.agent.md` frontmatter
  and a `task()` call. The CLI logs it itself: `Downgrading subagent model
  from "claude-sonnet-4.6" (1x) to session model "gpt-4.1" (0x)`. This repo's
  own `.github/agents/*.agent.md` pins are subject to it.
- **copilot-cli#3824** (closed 2026-06-17, one day after opening, with no
  visible resolution note). Sub-agent types map to their own models
  independent of the session model, and a server-side treatment arm can route
  a sub-agent to a different model family. Nothing tells you which model
  actually ran. **Closed isn't evidence of fixed**, so treat the mismatch
  class as live until a run with a pinned session model shows otherwise.

So per-seat model control on Copilot CLI is **not currently guaranteed**. Pin
the seats anyway, since the pins are the only statement of intent we have,
and report a routed tier as intent rather than as bill-confirmed landing. The
verify floor doesn't depend on the pins landing, which is where the value
case belongs. Never mix Auto with tiered dispatch.

## Dispatch engine — `task` tool vs `/fleet` (updated 2026-07-09)

After the step-2 plan gate, fan the leaves out yourself — **don't ask the
human to activate anything.** The model-invocable path is Copilot's built-in
**`task` tool** (`task(agent_type=…)`): issue several `task` calls in one
turn and they **run in parallel**, bounded by the subagent *concurrency*
limit (set per plan, § AI-credit economics, and distinct from the
*depth* limit). A maintainer calls this the *agent-driven equivalent of
`/fleet`* (copilot-cli#3568). <!-- claim:copilot-task-tool-parallel-dispatch --> The plugin agents in `.github/agents/`
(`@smartplan-planner` / `@smartplan-implementer` / `@smartplan-implementer-cheap` /
`@smartplan-implementer-reserve` / `@smartplan-verifier` / `-verifier-cheap` / `@smartplan-scout`) register as
`task` subagents — name them per leaf; all seven carry
`disable-model-invocation`, so tier selection is always the orchestrator's
explicit call, never Copilot's auto-pick. So Copilot keeps the family's core
rule (*never ask the user to invoke anything*) without giving up the
concurrent wave.

**What still needs a human is `/fleet`** — the heavier *orchestrated* engine
on the same task machinery (decompose → manage dependencies → background run
→ validate → synthesize; its validation is NOT a substitute for
`smartcheck`). The model **can't** self-trigger `/fleet` (three human triggers:
typed, autopilot after `/plan`/Shift+Tab, or the `--fleet` launch flag,
which also runs headless under `-p`) — treat it as an
**optional** upgrade for a big background wave, offered in passing, never
blocked on.

One honest caveat: the genuinely serial path is single-agent
auto-inference, which delegates to *one* agent. `disable-model-invocation`
turns it off. The older `infer` key is retired, though the CLI
reference's table still lists it. Concurrency comes from the `task` tool. Monitor with `/tasks`.

## Command naming — plugin `sp`, executor hidden (why it's set up this way)

On a marketplace install Copilot always namespaces commands as
`<plugin>:<skill>`; there is **no bare form, no plugin default-command, and
no command alias** — a skill has exactly one name, shown bare when
project-local and namespaced when plugin-installed. The `:` prefix is the
**`plugin.json` `name` field** (not the directory, not the marketplace
name), and the `/` menu is **plain alphabetical with no ordering/priority
knob.** *(Re-verified 2026-07-22 against docs.github.com's CLI plugin reference. CLI
v1.0.74 (2026-07-23) does support Open Plugin Spec v1 manifests, but the
namespacing behavior is unchanged.)* Two things are designed around that:

1. The plugin package is named **`sp`**, not `smartplan`, so the entry point
   reads `/sp:smartplan` instead of the redundant `smartplan:smartplan` —
   while the skill dirs stay `smart*`, so a **project-local checkout still
   invokes the branded bare `/smartplan`** (from `.claude/skills`, the only
   project skill tree this repo ships since the `.agents/skills` mirror was
   removed 2026-07-09; when both existed, a live test that day observed
   `.agents/skills` resolving first — Copilot documents no precedence/dedupe
   order (the development repo's claim ledger), so treat that as observed behavior, not a contract).
2. `smartexec` — a machine payload the orchestrator dispatches, never a
   human `/`-command — carries **`user-invocable: false`**, which drops it
   from the `/` menu while leaving it model-invocable (copilot-cli#3095) —
   and since v1.0.74 (2026-07-23) `disable-model-invocation` is actually
   enforced too (a live bug before then), so the payload also stays out of
   auto-invocation;
   since `exec` < `plan` it was the only skill sorting *above* `smartplan`,
   so hiding it makes `smartplan` the top/highlighted pick and `/sp`+Enter
   lands on it.

Diagnostic: `copilot skill list` (confirm the exact flag with `--help`;
machine output may be `--output-format=json`, printing each skill's resolved
`source`/`path`). A true bare `/smartplan` from a marketplace install is
**not** achievable — only a project-local checkout yields it. (Both paths
serve `.claude/skills` directly, so there's one copy of every skill and
uncommitted edits are live immediately in project-local use.)

## Marketplace install vs project-local — they don't merge

Plugin skills load at the **lowest** priority slot; `.github/skills` and
`.claude/skills` are **project-level** locations, not plugin ones. A
project-local skill of the same name silently wins and the plugin copy never
loads, with no warning — so a marketplace install plus a project-local
checkout is not additive. Pick one. (Verified 2026-07-22, docs.github.com
Copilot CLI plugin reference.)

## Standing levers (set once, help every session)

- **Repo instructions:** Copilot reads `.github/copilot-instructions.md`,
  root/nested `AGENTS.md`, **and `CLAUDE.md`** (add-custom-instructions
  docs, checked 2026-07-24 — a Claude-Code-shaped repo's standing context
  carries over for free), plus path-scoped `NAME.instructions.md` under
  `.github/instructions/` with `applyTo:` globs. Encode the non-negotiables
  (verification-before-done, smallest-diff, tiering defaults) there so they
  hold when no skill fires. A custom agent dispatched as a subagent gets
  none of them unless it sets `include-custom-instructions: true` (CLI
  1.0.86, default false).
- **Hooks:** fully documented at docs.github.com's hooks-reference
  (checked 2026-07-24): JSON under `.github/hooks/` (repo),
  `~/.copilot/hooks/` (user), or inline in the settings files; 14 events
  including `preToolUse` — the one **fail-closed** event, where a crash
  or any non-zero exit denies (a timeout fails open) — and `agentStop`, where an
  always-blocking hook force-ends after 8 consecutive blocks
  (`stop_hook_active` flag, v1.0.72). The §A enforcement-hook pattern ports
  directly; a smartcheck-before-done gate belongs on `agentStop`/
  `preToolUse`.
- **Claude Code hooks run here too.** In a trusted folder Copilot runs a
  repo's `.claude/settings.json` hooks (`PreToolUse` matches `task` as
  `Agent` or `Task`) and loads `.claude/agents/`, where same-named
  `.github/agents/` seats win. A non-zero exit there denies every
  dispatch, which is why the enforcement hook's command exits 0 when its
  script is missing (`docs/enforcement-hook.md`).
- **Reasoning effort:** `--effort none|minimal|low|medium|high|xhigh|max` tunes depth
  separately from model — drop effort on mechanical fan-outs before dropping
  model tier. `--effort` and `~/.copilot/settings.json`'s `effortLevel`
  (low to xhigh) are session-wide. Per-seat effort rides `reasoningEffort`
  frontmatter (above), spelled `reasoning-effort` in the 1.0.88 changelog
  (copilot-cli#2904 closed 2026-09-16).

## Testing against Copilot cheaply (the probe-cost playbook, 2026-07-12)

Copilot is the harness where costs are *observable*, so it stays the
primary test target — and probe spend is engineered down with these
levers, in order of measured impact:

1. **Script/oracle grading first** — precomputed hidden oracles grade at
   zero credits; model verifiers only where judgment is the question
   (T8–T13 standard).
2. **Batch verification** — one context per ~3 same-class leaves: 32% of
   per-leaf verify cost (T10), FAIL-isolation proven (T11).
3. **Only the leaves under test bill** — when the *verifier* is the
   subject, script-write the leaves (T11: a full seeded-FAIL batch probe
   for 7.1 cr total).
4. **`--resume` for same-seat repairs** — a repair belongs to the
   executor's own context; resuming its session rides the warm cache
   instead of paying a fresh 75–160k cold context. Never for verifiers
   (independence requires fresh context).
5. **`/limits` / `--max-ai-credits` caps on probe sessions** — bound the
   runaway-repair tail (a single uncapped inline repair once burned 167
   cr, T9). Caps can't go under 30 cr. They bound that tail, not a
   normal 1 to 13 cr leaf.
6. **Minimal probe workspace** — dispatch context is ~40% of a Copilot
   dispatch's bill (cache reads of the session tree); probes that don't
   need the full skill tree should run from a stripped directory.
7. **Cheapest-capable probe models** — mechanism probes (does the lever
   work?) don't need top tiers. GPT-5.6 Luna now holds the
   probe-workhorse role GPT-5 mini earned in T16 (mini retires
   2026-10-19). GPT-6 Luna leads the Luna seats untrialed. Record its
   probe outcomes (`routing.md` § Seat eligibility).

## Running real UE5 work cheaply on Copilot (not just probing, 2026-07-12)

The playbook above is for *testing* the skill; this is for *doing* Unreal
work, where the bill is dominated by two things — engine context and a
forced-high verify tier. Levers, most impactful first:

1. **Cross-family verify, on price, not because Opus is gated.** A UE5
   gameplay leaf forces an Opus-comparable verify
   (`cpp-gamedev-check.md`). Route it to the **Gemini 3.8 Flash**
   cross-family verifier (`gemini-3.8-flash`) per `check.md` —
   decorrelated on the shared-blind-spot categories UE5 lives in, and it
   dodges the gate. **Measured on predecessor 3.1 Pro (T18): tied GPT-5.6
   Terra on seeded UE5 recall at 47% the cost, saving ~24%/leaf vs the
   Sonnet self-verify Pro would degrade to (T17); T34 cleared 3.6 Flash at
   8/8 before 3.1 Pro retired 2026-09-01. Its successor 3.8 is untested.**
   The 47% predates Terra's 2026-08-12 reprice to 3.1 Pro's rate. The 3.8
   Flash pin at 0.75 / 3.75 is the cheaper judge outright. Holds whether
   or not your Opus pin lands.
2. **Context discipline is the other ~40%.** Engine headers,
   `*.generated.h` and large TUs reload on each cold subagent cache (5 min
   on Claude seats, 30 min at OpenAI from GPT-5.6, pass-through undocumented),
   and dispatch context is ~40% of a Copilot bill. Scope each brief to the
   touched TU plus the *minimal* engine surface; never hand a leaf a whole
   module. Keep the cached prefix stable across a wave (`caching.md`).
   The CLI's C++ language server indexes the whole codebase by default
   from 2026-09-22. Symbol lookups may undercut grep-and-read on engine
   headers (unmeasured). The first UE5 index build costs time and memory.
3. **Batch-verify gameplay leaves.** ~3 same-profile leaves share one
   verifier context (`check.md`) at 32% of per-leaf verify cost, and the
   engine-context load is paid once, not three times.
4. **Drop effort before model** where the seat has a dial: a mechanical UE5
   stub runs low-effort at its floor before a pricier model, but keep the
   *verify* at strength (that is where UE5 bugs hide).
5. **Route lone stubs Mid, not Cheap** (`routing.md` hard-floor #4): a lone
   UE5 stub's forced Mid+ verify out-costs the Cheap saving. Cheap-tier UE5
   pays only on *wide* scaffolding waves.

**Attribution discipline for any UE5 cost claim.** Even with per-model
rows (CLI 1.0.85+), `/usage` has no skill or context attribution. The
credits a wave "cost" blend skill + engine-context
overhead with the work itself. For a defensible number, run the measured
leaf in a **minimal workspace** and cross-check `/context` under
`/experimental` (§ `/usage` ceiling above) so the figure attributed to the
work excludes skill/context overhead — otherwise a UE5 cost is an aggregate
with an asterisk. (Measured across T17's three verify arms.)
