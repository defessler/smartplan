# smartplan §B deep reference — Copilot CLI economics & standing levers

> Facts verified 2026-07-06; re-swept 2026-07-24, 2026-08-05, 2026-08-12.
> Re-check trigger: Business/Enterprise allowance promo ends 2026-09-01.

Load this only on Copilot CLI — for dispatch mechanics beyond flow.md §B's
summary, budget decisions, fan-out sizing, or repo setup.

## Contents

- The four levers (most reliable first)
- AI-credit economics (billing changed 2026-06-01)
- Context caps (picker, 2026-08-06)
- Per-seat model control isn't guaranteed here (checked 2026-08-05)
- Dispatch engine — task tool vs /fleet (updated 2026-07-09)
- Command naming — plugin sp, executor hidden (why it's set up this way)
- Marketplace install vs project-local — they don't merge
- Standing levers (set once, help every session)
- Testing against Copilot cheaply (the probe-cost playbook, 2026-07-12)
- Running real UE5 work cheaply on Copilot (not just probing, 2026-07-12)

## The four levers (most reliable first)

| # | Lever | How |
| --- | --- | --- |
| 1 | Cheap default | `/fleet` subagents use a low-cost model by default — native. |
| 2 | Agent frontmatter | `model:` on the six shipped `.github/agents/` profiles — slug form (`claude-opus-4.8` / family alias `opus`); arrays rejected. Pins can be silently downgraded (§ Per-seat model control), so never mix Auto with tiered dispatch. |
| 3 | `/subagents` | Sets default and per-agent subagent models in-session (alias `/agents`). |
| 4 | NL directive | Name agents inline: `use @smartplan-planner to plan, then @smartplan-implementer per item, then @smartplan-verifier`. |
| 5 | Scoped pins | `/model --session` pins model/effort for this session only (v1.0.72). **`/model plan` pins a plan-mode-only model (v1.0.74) — the native analog of §A's `opusplan`:** plan on Opus, revert automatically on exit; captures the core rule with zero dispatch machinery. |

## AI-credit economics (billing changed 2026-06-01)

Token-metered AI credits (1 credit = $0.01). Monthly allowances: Pro 1,500 /
Pro+ 7,000 / Max 20,000 per user. Business/Enterprise are mid-promo through
2026-09-01 at 3,000/7,000 per user. 1,900/3,900 are the post-promo
steady-state numbers, not what those plans see today.
**Subagent tokens bill**, so tiering the fan-out is the bill, not politeness.

Copilot bills Anthropic's list rates, so `model-classes.md`'s Anthropic rows
are the Copilot rows too (models-and-pricing, re-checked 2026-08-12). One
cost model across both harnesses — which is why Anthropic making Sonnet 5's
$2/$10 standard on 2026-08-10 lands here too. GitHub dropped its promo
footnote on 2026-08-13; the rate is unqualified standard now.
Two distinct $10/$50 SKUs sit at the top, "Claude Fable 5" and "Claude
Opus 4.8 (fast mode) (Preview)", same price and not the same model. Both are
planning-only.

**soft caps (public preview, CLI 1.0.66+ / SDK 1.0.5+):** `/limits`
(interactive: view/set/remove), `--max-ai-credits` (programmatic) — an in-flight response
finishes before the stop takes effect, so usage can slightly exceed the cap.
Use them to lean on budget pressure, not just watch `/usage` (quota bars;
the documented per-model token totals do NOT render on AI-credits
sessions — live, `docs/copilot-on-a-budget.md`). **Caveat (T25, 2026-07-12): caps are visible to the
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

Subagent concurrency and depth are now documented settings-file knobs:
`.github/copilot/settings.json` `subagents.maxConcurrency` (cap 32),
`subagents.maxDepth` (cap 256), and `subagents.disabledSubagents`
(cli-config-dir-reference, checked 2026-07-24) — size waves to the
configured cap.

**`/usage` has a real ceiling — session/per-model only, confirmed 2026-07-08.**
GitHub's own CLI reference documents it as "session usage metrics and
statistics, including per-model token totals" — there is no skill,
subagent, plugin, or MCP-server attribution *under `/usage` itself*, unlike
Claude Code's `/usage`. Don't let a session import Claude Code's
`/usage`-attribution language here. A live 2026-07-08 case did exactly that,
quoting §A's skills/subagents breakdown as Copilot's own behavior right after
correctly observing that `/usage` is aggregate-only.

**Correction, live-tested 2026-07-09:** the finer breakdown lives
elsewhere — `/context` under `/experimental` shows per-source attribution
(skills, subagents, MCP servers, plugins), and `/statusline`'s
`ai-credits`/`ai-used` options give always-visible live spend. Check
`/context` first; the fallback is `run-state.md`'s rows (routed-tier
*intent*, not bill-confirmed landing).

**Headless metering is native now (measured T30):** `-p` runs print an
`AI Credits` footer, and `~/.copilot/session-store.db`'s
`assistant_usage_events` table carries per-request nano-AIU (1e9 = one
credit) — per-session spend is exactly measurable without `/usage`.

Plan gating: Opus 4.8, Opus 5 (GA 2026-07-24), and Fable 5 are documented Pro+/Max. (T30+B4, 2026-07-25: an account that refused Opus 4.8 on 07-11 served both Opus models, so tiers change. Verify, don't assume the gate.) Fable
additionally requires 30-day data retention for Anthropic's safety
classifiers, where other Claude models stay zero-data-retention
(changelog 2026-06-09, re-checked 07-24). **Settled 2026-08-14 from
`github/docs` `model-supported-plans.yml`:** Opus 4.5/4.6 are Business and
Enterprise ONLY. Plain Pro excludes GPT-5.5, GPT-5.6 Sol, GPT-5.4 nano and
every Opus and Fable SKU — everything else on the roster it reaches,
including Terra, GPT-5.3-Codex, Kimi K3, Gemini 3.1 Pro and both Groks.

**Cross-vendor model economics (re-checked 2026-08-14).** Copilot exposes
Anthropic, OpenAI, Google, xAI, Moonshot and Microsoft models. **Grok is
back**: 4.5 (2026-07-28) and 4.6 (2026-08-14) are GA on every paid plan,
plain Pro included, at xAI list 2 / 6. A prompt reaching 200K bills 4 / 12 on
the WHOLE request — a cliff, not a margin. Grok Code Fast 1 stays deprecated
(2026-05-15) and is a separate model.

Seat verdicts, cross-vendor. Prices and board numbers live in
`model-classes.md`, whose non-Anthropic rows are dated 2026-07 and unchecked
since, so re-verify before leaning on one.

- Planner is **Opus 5** (registry default since 2026-08-05, same 5/25 and
  same Pro+/Max gate as 4.8, which stays the fallback). GPT-5.5 is Pro-plan-gated (confirmed
  2026-07-20, which is why T18 missed it) and loses on price and on SWE-Pro,
  though it edges Opus on TB2.1 (83.1 vs 78.9, 07-24). The Geminis are
  cheaper and trail further. Neither is a planner swap.
- **Coding leaves: try GPT-5.6 Luna first** (standing preference, 2026-08-20).
  **0.20 / 1.20**, ~10x under Sonnet 5 in, and *above* it on SWE-V (93.0 vs
  79.6). Board evidence only, no T-record — keep it behind the verifier.
- Mid/verifier stays **Sonnet 5**. **GPT-5.4** and **Gemini 3.6 Flash** are
  the verifier-diversity picks per `check.md`'s Family decorrelation rule,
  Gemini the cheaper of the two (3.1 Pro held this seat until Copilot's
  scheduled 2026-09-01 retirement; T34 cleared the swap).
- Cheap stays **Haiku 4.5**. **GPT-5 mini** is roughly 4x cheaper in and 2.5x
  cheaper out, and its effectiveness is contested, so trial it deliberately
  with outcomes watched rather than defaulting to it off secondhand benchmark
  blogs.

**GPT-5.6 family (Sol / Terra / Luna, in Copilot's roster since
2026-07-10):** prices, board numbers, and seat placements live in
`model-classes.md` — don't restate them here. What the registry rows don't
carry: the OpenAI and Google SKUs charge a **long-context surcharge**
Anthropic rows lack (Sol >272K $10/$45 · GPT-5.4 >272K $5/$22.50 · Terra
>272K $4/$18 · Luna >200K $0.40/$1.80 · Gemini 3.1 Pro >200K $4/$18 · Grok
4.5/4.6 ≥200K $4/$12) — price big-context leaves
and big-diff Gemini verifies off that column. All three are
deliberate-trial candidates, never defaults, per `routing.md` § Seat
eligibility's provisional classification.

**Roster watch (re-swept 2026-08-19).** New-SKU details live in
`model-classes.md` (MAI-Code-1-Flash, Kimi K2.7 Code, Gemini 3.5/3.6
Flash — 3.6 joined the roster 2026-07-21, CLI included). **Three landed
2026-08-11/13/14: MAI-Code-1.1-Flash, Gemini 3.7 Flash, Grok 4.6**, all
GA. MAI-Code-1-Flash was deprecated the day 1.1 shipped — move that pin. **Claude Opus 5**
joined GA + CLI-selectable 2026-07-24 (CLI v1.0.75; Pro+/Max;
Business/Enterprise admin-enable) at Opus 4.8's exact price — registry row
is provisional, no official benchmarks yet. Opus 4.8 **fast mode**:
$10/$50, cache-read $1, write $12.50; still "(preview)", Pro+-gated. No
default moves — planner, verifier, and both floors stand.

**Auto model selection, the honest retreat candidate (re-checked
2026-08-05):** Auto has been **GA since 2026-04-17 across all plans**, and it
routes on *evaluated task complexity*, not availability alone (changelog
2026-04-17, auto-model-selection). Say the uncomfortable part plainly:
description-level routing is smartplan's stated surviving value, and on this
harness it's first-party now. What's left for us here is the regime gate and
the verify floor, not the act of picking a model. The **10% discount** was
announced in premium-request units six weeks before that unit died, and the
docs now say "10% discount on model costs" without naming a unit, so read it
as 10 percent with the unit unconfirmed post-June-2026. Routing runs "along
natural cache boundaries" so it stays cache-safe, though that's the page's
rationale rather than a worded guarantee. Split guidance:
**inline/fast-path sessions → Auto is the sensible default, and the fair
control to measure against.** Sessions *dispatching a tiered wave* still pin
explicit models (Auto may seat a pricier model, and its interplay with
#2758's pin downgrade is unverified).

**Repo-level pins (CLI v1.0.70, verified locally 2026-07-13):**
`.github/copilot/settings.json` supports `subagents.agents.<name>` with
per-agent `model`/`effortLevel`/`contextTier` — this repo ships effortLevel
**low** for `smartplan-implementer-cheap` and `smartplan-scout`. That
settings key is a local observation, not a documented one, and it isn't
frontmatter (see § Standing levers). Reasoning bills as output, and the
effort ladder is none/minimal/low/medium/high/xhigh/max since v1.0.55–60.
Judgment seats stay unpinned deliberately.

**Verify on credits:** the default verify ladder here is `check.md`'s
credit-billed default — script stage first, model pass batched + sampled
(T22: one batched model verify alone was 83% of the entire inline arm).

## Context caps (picker, 2026-08-06)

Every Claude model here is **264K**, and so are the Geminis. **Opus 5 is
264K against a 1M native window, a 3.8× cut.** GPT-5.6 Sol/Terra, 5.5 and
5.4 get **400K**; Luna and Grok 4.5 **328K**. More room than a Claude seat
means a cross-family seat: context, not tiering. Reasoning reads Medium
everywhere except **Kimi K3 (High)**.

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
limit (default plan-dependent, raise it in `/settings`; distinct from the
*depth* limit). A maintainer calls this the *agent-driven equivalent of
`/fleet`* (copilot-cli#3568). <!-- claim:copilot-task-tool-parallel-dispatch --> The plugin agents in `.github/agents/`
(`@smartplan-planner` / `@smartplan-implementer` / `@smartplan-implementer-cheap` /
`@smartplan-implementer-reserve` / `@smartplan-verifier` / `@smartplan-scout`) register as
`task` subagents — name them per leaf; all three implementer variants carry
`disable-model-invocation`, so tier selection is always the orchestrator's
explicit call, never Copilot's auto-pick. So Copilot keeps the family's core
rule (*never ask the user to invoke anything*) without giving up the
concurrent wave.

**What still needs a human is `/fleet`** — the heavier *orchestrated* engine
on the same task machinery (decompose → manage dependencies → background run
→ validate → synthesize; its validation is NOT a substitute for
`smartcheck`). The model **can't** self-trigger `/fleet` (two human triggers
only: typed, or autopilot after `/plan`/Shift+Tab) — treat it as an
**optional** upgrade for a big background wave, offered in passing, never
blocked on.

Two honest caveats: whether `task` subagents parallelize *by default* depends
on the plan's default concurrency limit, which GitHub doesn't publish per
tier, so set it yourself with the settings knobs above. And the one genuinely
serial path is single-agent auto-inference (`infer`/
`disable-model-invocation`), which delegates to *one* agent. Concurrency
comes from the `task` tool. Monitor with `/tasks`.

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
  hold when no skill fires.
- **Hooks:** fully documented at docs.github.com's hooks-reference
  (checked 2026-07-24): JSON under `.github/hooks/` (repo),
  `~/.copilot/hooks/` (user), or inline in the settings files; 14 events
  including `preToolUse` — exit 2 denies, and it is the one **fail-closed**
  event (other hook errors fail open) — and `agentStop`, where an
  always-blocking hook force-ends after 8 consecutive blocks
  (`stop_hook_active` flag, v1.0.72). The §A enforcement-hook pattern ports
  directly; a smartcheck-before-done gate belongs on `agentStop`/
  `preToolUse`.
- **Reasoning effort:** `--effort none|minimal|low|medium|high|xhigh|max` tunes depth
  separately from model — drop effort on mechanical fan-outs before dropping
  model tier. It's **session-global** (`--effort`, or
  `~/.copilot/config.json`): the custom-agent frontmatter table carries no
  effort field and the request is still open (copilot-cli#2904). So any
  effort-based tiering the policy adopts is **Claude Code only** and has to
  say so.

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
   cr, T9).
6. **Minimal probe workspace** — dispatch context is ~40% of a Copilot
   dispatch's bill (cache reads of the session tree); probes that don't
   need the full skill tree should run from a stripped directory.
7. **Cheapest-capable probe models** — mechanism probes (does the lever
   work?) don't need top tiers; the registry's Cheap-tier candidates
   (GPT-5 mini at ~¼ Haiku's price, GPT-5.6 Luna) are trialed deliberately
   for probe-workhorse duty — outcomes recorded before any floor moves, per
   § Seat eligibility.

## Running real UE5 work cheaply on Copilot (not just probing, 2026-07-12)

The playbook above is for *testing* the skill; this is for *doing* Unreal
work, where the bill is dominated by two things — engine context and a
forced-high verify tier. Levers, most impactful first:

1. **Cross-family verify, on price, not because Opus is gated.** A UE5
   gameplay leaf forces an Opus-comparable verify
   (`cpp-gamedev-check.md`). Route it to the **Gemini 3.6 Flash**
   cross-family verifier (`gemini-3.6-flash`) per `check.md` —
   decorrelated on the shared-blind-spot categories UE5 lives in, and it
   dodges the gate. **Measured (T18): ties GPT-5.6 Terra on seeded UE5
   recall at 47% the cost, saving ~24%/leaf vs the Sonnet self-verify Pro
   would degrade to (T17); T34 cleared 3.6 Flash as the successor at 8/8
   before 3.1 Pro retires 2026-09-01.** Holds whether or not your Opus pin lands.
2. **Context discipline is the other ~40%.** Engine headers,
   `*.generated.h` and large TUs reload on each cold 5-min subagent cache,
   and dispatch context is ~40% of a Copilot bill. Scope each brief to the
   touched TU plus the *minimal* engine surface; never hand a leaf a whole
   module. Keep the cached prefix stable across a wave (`caching.md`).
3. **Batch-verify gameplay leaves.** ~3 same-profile leaves share one
   verifier context (`check.md`) at 32% of per-leaf verify cost, and the
   engine-context load is paid once, not three times.
4. **Drop effort before model** where the seat has a dial: a mechanical UE5
   stub runs low-effort at its floor before a pricier model, but keep the
   *verify* at strength (that is where UE5 bugs hide).
5. **Route lone stubs Mid, not Cheap** (`routing.md` hard-floor #4): a lone
   UE5 stub's forced Mid+ verify out-costs the Cheap saving. Cheap-tier UE5
   pays only on *wide* scaffolding waves.

**Attribution discipline for any UE5 cost claim.** `/usage` is aggregate/
per-model only; the credits a wave "cost" blend skill + engine-context
overhead with the work itself. For a defensible number, run the measured
leaf in a **minimal workspace** and cross-check `/context` under
`/experimental` (§ `/usage` ceiling above) so the figure attributed to the
work excludes skill/context overhead — otherwise a UE5 cost is an aggregate
with an asterisk. (Measured across T17's three verify arms.)
