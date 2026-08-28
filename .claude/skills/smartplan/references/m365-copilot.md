# smartplan §D deep reference — Microsoft 365 Copilot: what fits, what can't

> Facts verified 2026-08-12 against `learn.microsoft.com`, the raw
> declarative-agent JSON schemas at `developer.microsoft.com`, and Microsoft's
> published pricing. Nothing here is measured — no Microsoft surface is
> installed on this machine, so every claim is read rather than observed.

Load this only when the target is a Microsoft 365 Copilot surface. **Read the
verdict first — most of this family does not ship here, and knowing which
half does saves a wasted build.**

## The verdict, up front

M365 Copilot is not one surface. It is three delivery targets with different
rules, and smartplan's fit differs sharply across them:

| Target | Can it carry smartplan? | Why |
| --- | --- | --- |
| **Declarative agent** (M365 Copilot) | **No** | 8,000-char instructions, one inline string, no runtime file reference, no progressive disclosure, no frontier-model pick |
| **Copilot Studio — GitHub Copilot harness** | **Yes, partially** | Ships a real `SKILL.md` Skills feature and a per-agent model picker |
| **Copilot Studio — standard harness** | Policy only, no skills | Has model choice and a `reason` escalation keyword, but its "Skills" is a different, legacy feature |

So the honest shape is: **a mapping doc plus a narrow export for the GitHub
Copilot harness.** The declarative-agent path is closed, and that is a
structural fact, not a limitation to engineer around.

## Declarative agents — why the family can't ship there

**The manifest root is a closed set of exactly 15 keys.** Verified by
downloading and parsing the raw v1.8 schema (53,896 bytes): `id`, `version`,
`name`, `description`, `disclaimer`, `instructions`, `capabilities`,
`behavior_overrides`, `conversation_starters`, `actions`, `user_overrides`,
`editorial_answers`, `worker_agents`, `$schema`, `sensitivity_label`. The
docs pin it shut: *"Unrecognized or extraneous properties in any JSON object
make the entire document invalid."*

- **Manifest file:** referenced from the app manifest's
  `copilotAgents.declarativeAgents[].file`. Docs show `declarativeAgent1.json`;
  Copilot Studio exports `declarativeAgent.json`.
- **Schema URI:** `https://developer.microsoft.com/json-schemas/copilot/declarative-agent/v1.8/schema.json`,
  and the manifest sets `"version": "v1.8"`. **v1.8 is current** — v1.9 and
  v2.0 both return 404. v1.8 added `EmailActions` and `MeetingActions`.
- **Shipping unit:** a `.zip` holding `manifest.json` (the Microsoft 365 app
  manifest), a 192×192 `color.png` and a 32×32 `outline.png`.

**`instructions` is a single String with `maxLength` 8000.** Both the docs
table and the schema file agree, and Copilot Studio's quotas page
independently lists "Instructions for a Copilot agent | 8,000 characters".

**There IS a file-reference mechanism, and it is authoring-time only.** The
Agents Toolkit template ships `"instructions": "$[file('instruction.txt')]"`,
and the tutorial states the file's contents *"are inserted in the
`instructions` property in the agent's manifest during provisioning."* So:
**no *runtime* file reference, only a token that inlines at provisioning,
and the 8,000-character cap applies to the expanded string.** It buys editor
ergonomics, not headroom, and never progressive disclosure. Worth knowing
before building tooling that assumes either extreme.

**Don't route around the cap through knowledge.** The "Write effective
instructions" page carries an Important callout naming XPIA
(cross-prompt-injection) classifiers, runtime truncation, attack-surface
expansion and governance bypass, closing with *"the platform makes no
guarantee they will be honored as agent instructions."* That is stronger
than a style preference.

Put together: this family's shape is a `SKILL.md` body plus a `references/`
tree loaded on demand. A declarative agent has one 8,000-character string and
no way to defer anything. `flow.md` alone is 17KB.

### The model-selection nuance

"Declarative agents expose no model selection" is **wrong**, though the
practical conclusion survives. There is no top-level `model` property, but
the schema defines a **`ScenarioModels`** capability holding a required
`models` array whose each entry has a required string `id`. The TypeSpec
reference gives real syntax:
`op scenarioModels is AgentCapabilities.ScenarioModels<Models = [{ id: "model-id" }]>;`
with examples like `{ id: "financial-forecasting-model-v3" }`.

Three qualifiers that put it back in its box:

1. **These are not frontier models.** The schema calls them "tenant/task
   specific models" and the docs "task-specific models", identified by opaque
   tenant-scoped IDs. You cannot select Opus over Sonnet with it.
2. **They come from Microsoft 365 Copilot Tuning**, whose overview page is
   titled "(early access preview)" and states availability is limited to
   customers in early access programs.
3. **It is not new in v1.8** — it first appears in v1.4 (v1.0/1.2/1.3 have
   zero occurrences).

The overview table's actual wording is *"Limited to Copilot's orchestrator
and models."* — possessive, with a trailing period. Quote it exactly.

### The one real tiering dial on this surface

`behavior_overrides.default_response_mode`, a closed enum of exactly three
members in sentence case with literal spaces:

| Value | Behavior |
| --- | --- |
| `Auto` | Orchestrator picks per query. **The default if unspecified.** |
| `Quick response` | Low-latency, speed over reasoning depth |
| `Think deeper` | Reasoning mode, higher latency |

It is an **effort** tier, not a model ID; **per-agent**, not per-call; and
advisory — the property is prefixed `default_` precisely because *"users can
always override this value through the model selector UI."* A known issue
voids it outright: **"Default response mode isn't applied when the agent is
invoked via @mention from the main Copilot experience."**

Map smartplan's effort axis onto it and stop there. It cannot express a
model ladder.

### Multi-agent — `worker_agents`

Real, and narrower than it first reads:

- **Referenced by title ID only.** The 1.6 Worker agent object has exactly
  one property: `id`, "the title ID of the application that contains the
  declarative agent" — a single letter, an underscore, and a GUID. In v1.8
  `id` became Optional with *"You must specify either `id` or `file`, but not
  both."*
- **Selection uses three signals, not two:** *"based on the connected agent's
  `name`, `description`, and `conversation_starters` in the manifest"*, and
  only a conversation starter's `text` field counts. Those are runtime
  ranking signals, never manifest fields on the worker entry itself.
- **DA-to-DA only, text-only payloads** (adaptive cards are a partial
  exception), the user must have each connected agent installed, and **no
  parallel-dispatch guarantee is documented either way.**
- **Still preview** on the 1.8 page.

Description-level routing is the same mechanism this family already relies
on, so the *selection* model ports. The dispatch economics don't: with no
documented parallelism and no per-worker model, a fan-out here buys
separation of concerns, not tiering.

## Copilot Studio — the one surface that can carry a skill

### Three harnesses, not two

The current "Choose a harness" page documents **three**: the **GitHub Copilot
harness**, the **standard harness**, and the **Copilot chat harness**. An
older page (`agents-experience/overview`, ms.date 2026-06-23) still says
"the two harnesses" — the newer harnesses-overview (ms.date 2026-07-28,
updated 2026-08-03) carries three and wins. Microsoft's own docs disagree
with each other at time of writing.

"Agents cannot be transferred between them" is confirmed **verbatim but
narrowly** — the sentence covers the GitHub Copilot / standard pair only.
Nothing published addresses the Copilot chat harness either way.

### The Skills feature — real, and its specifics are thinner than they look

**Confirmed:** the GitHub Copilot harness ships Skills, and a package is a
**ZIP containing a `SKILL.md` with YAML front matter (`name`, `description`)
and Markdown instructions, plus optional supporting files.**

That is the delivery path. But every load-bearing specific fails at the
Copilot Studio source, and four of them are traps:

1. **The frontmatter allowlist is not published.** Copilot Studio names only
   `name` and `description` and never says the set is exhaustive. The
   six-key table (adding `license`, `compatibility`, `metadata`,
   `allowed-tools`, with 64- and 1,024-character caps) exists **only on
   Microsoft's Visual Studio and SSMS pages**, which document a different
   surface. Don't cite it here.
2. **Whether extra keys are rejected is undocumented** — at Microsoft and at
   agentskills.io. Publish no claim in either direction.
3. **Subdirectories inside the ZIP are not documented.** Copilot Studio says
   "supporting files" and never says subdirectories. The
   `scripts/`/`references/`/`assets/` layout appears only on the VS and SSMS
   pages, and there it describes a directory discovered **on disk** from
   `.github/skills/` or `.claude/skills/`, not a ZIP upload. **So this
   family's `references/` tree is unproven here too** — the same open
   question as ZCode, and for the same reason.
4. **The "Skills | 100 per agent" quota is a name collision, not a limit on
   these skills.** That row sits on a page banner-scoped to the **standard**
   harness and its own gloss reads "Azure Bot Framework skills" — the legacy
   Azure Bot Service skill protocol, a different feature reusing the word.
   Citing it as a cap on `SKILL.md` skills would be wrong.

The name rule is real but wrongly framed: *"Use only lowercase letters,
numbers, and hyphens. Don't start or end the name with a hyphen"* describes
the **UI Name field** on the create and edit forms, not stated `SKILL.md`
frontmatter validation. Copilot Studio also omits the 64-character maximum
and the no-consecutive-hyphens rule the spec carries elsewhere.

**"Shape-compatible with Anthropic Agent Skills" is unsupported at this
source.** Those pages never cite agentskills.io, never mention Anthropic and
never reference `.claude/skills`. The shape rhymes. Treat compatibility as a
hypothesis to test on upload, not a fact.

### Model selection, per harness

- **GitHub Copilot harness:** *"Select the Build tab. In the components
  panel, select the Model list. Select the model you want. Select Save."*
- **Standard harness:** Overview → Model. This path carries the banner
  "Features in this article are powered by the standard harness", so a doc
  that says "Copilot Studio exposes a dropdown at Overview → Model" is wrong
  for one of the three harnesses. Qualify it.

Published availability includes Claude Opus 4.7 and 4.6 (Deep, GA), Claude
Sonnet 5 (GA, **GitHub Copilot harness only**), Claude Sonnet 4.6, GPT-5.5
Chat, GPT-5 Chat, GPT-4.1 (Default), GPT-5 Reasoning / GPT-5 Auto (Preview),
plus Experimental GPT-5.3/5.4/5.5, Grok 4.1 Fast and Mistral Medium 3.5.
GPT-4o and Claude Sonnet 4.5 are **Retired in every region**.

Note what that roster means for this family: **Opus 5, Fable 5 and Haiku 4.5
are absent.** The ladder smartplan routes against does not exist here. Seat
by capability class against what's actually offered, and say so at the gate.

### `reason` — step-level escalation, heavily gated

The standard harness supports escalating a step to a reasoning model by
writing the literal keyword **`reason`** into the agent instructions:
*"An agent can use deep reasoning models for multiple tasks or steps, but
each one must contain the keyword reason."*

This is the closest thing on the whole Microsoft surface to per-call
tiering, and it is expressed in natural language inside instruction text
rather than a config field. Four gates before it does anything:

1. **Preview.** The page is titled "Add a deep reasoning model for complex
   tasks (preview)" and says it is prerelease documentation.
2. **Two switches:** generative orchestration must be on *and* deep-reasoning
   access enabled for that agent, then Settings → **Deep reasoning
   (preview)** turned on.
3. **Region-limited** to the United States and the EU excluding the UK.
4. **The model is Azure OpenAI o3**, not the agent's selected primary model.
   These are explicitly separate settings.

The keyword is also not the only trigger — *"Your agent determines which
tasks or steps benefit from a deep reasoning model. You can also tell your
agents to use deep reasoning."*

### Multi-agent in Copilot Studio

The richer story: child (inline) agents, connected Copilot Studio agents,
and external agents over **A2A**, plus Microsoft Foundry agents, Fabric Data
agents and Microsoft 365 Agents SDK agents (all preview). **Fan-out is
prompt-directed, not a platform primitive** — the recommended parent
instruction is literally *"Invoke both child agents… Wait for both child
agents to return their findings… Combine."*

## Hard limits (declarative agents)

`instructions` 8,000 chars · `name` 100 · `description` 1,000 · unspecified
strings 4,000 · `conversation_starters` max 12 · `actions` 1–10 · embedded
knowledge files max 10 at 1 MB each · disclaimer 500 chars · group mailboxes
max 25 · meetings `items_by_id` max 5.

Plugin side: **up to 5 plugins are always injected into the prompt; beyond 5
it switches to semantic matching on the plugin description alone**, and
quality degrades past ~10 functions/tools. That is the same
tool-count-degradation shape Anthropic documents for tool selection, arrived
at independently — worth noting when sizing an MCP-heavy agent.

## MCP

Supported, but **only inside declarative agents as plugin actions** — never
in bare Microsoft 365 Copilot. The plugin manifest is `ai-plugin.json` with
`schema_version: "v2.4"`; v2.4 added `RemoteMCPServer` as a Runtime `type`
alongside `OpenApi` and `LocalPlugin`, carrying a `url` and optional
`mcp_tool_description`. Auth: `None`, `OAuthPluginVault`, `ApiKeyPluginVault`.
Copilot resolves MCP tools dynamically at runtime by default, or a developer
pins a fixed set. Requires Agents Toolkit 6.12.0+. Copilot Studio also lists
MCP servers as a Tools source.

## There is a CLI — three, in fact

Not a GUI-only surface:

- **Microsoft 365 Agents Toolkit CLI** — binary `atk`, installed with
  `npm install -g @microsoft/m365agentstoolkit-cli`. Covers
  new/add/provision/deploy/package/validate/publish/preview/install/uninstall.
  `atk new -c declarative-agent` scaffolds one directly.
- **Work IQ Dev Tools** — binary `wiqd`, official Microsoft
  (github.com/microsoft/wiqd), preview v0.11.0, with
  `wiqd agent create|validate|provision|package|eval` and an alpha
  `wiqd plugin` tree.

`atk` is what an export script targets: it packages and validates the ZIP.

## Money

- **M365 Copilot (Enterprise add-on):** $30.00 user/month paid yearly, or
  $31.50 paid monthly on an annual commitment.
- **M365 Copilot Business (SMB):** $18.00 user/month paid yearly on
  promotional pricing **through 2026-09-30** (regular $21.00), or $25.20
  billed monthly. <!-- RECHECK:2026-10-01 -->
- **Bundles:** Business Premium with Copilot $32.00; Business Standard with
  Copilot $23.50, both user/month paid yearly.
- **Copilot Chat** is included at no extra cost with an eligible M365 license.
- **Copilot Studio capacity pack:** $200.00/pack/month for 25,000 Copilot
  Credits, tenant-wide, replenished each billing period.

Published credit rates: classic answer 1 · generative answer 2 · agent
action 5 · tenant graph grounding 10 · agent flow actions 13 per 100 · AI
tools basic 1 / standard 15 / premium 100 per 10 responses. **Reasoning
models bill twice** — the feature rate plus "Text and generative AI tools
(premium)" at 10 credits per 1,000 tokens. Overage disables custom agents at
125% of prepaid capacity.

**With an M365 Copilot add-on license there are "No extra charges for
accessing or using extensibility features (Copilot connectors, agents,
plugins)."** Declarative agents incur no hosting cost — Microsoft hosts them.
Custom engine agents you host yourself.

Pay-as-you-go per-credit price is **not published** — the Azure pricing page
renders it literally as "$-".

## What smartplan actually becomes here

Say this at the gate rather than implying more:

- **The policy ports. The machinery doesn't.** Plan-then-execute, the
  spiral guard, the verify floor and the honesty rules are all prose and
  survive intact in a `SKILL.md` on the GitHub Copilot harness.
- **Tiering degrades to two coarse dials:** a per-agent model pick from a
  roster that has no Opus 5, no Fable 5 and no Haiku, and a three-way
  effort mode. There is no per-call override anywhere on this surface.
- **Independent verify has no dispatch lever.** Nothing here lets you send a
  diff to a *different* model and get a verdict back under your control.
  `flow.md`'s verifier seat has no home on M365. Say so rather than
  pretending a `reason` step is a smartcheck.
- **Nothing here is measured, and on this machine nothing can be.** No
  T-record exists for any Microsoft surface. Checked directly on
  2026-08-12: `atk` and `wiqd` are both unrecognized, `npm ls -g` carries no
  `@microsoft/*` toolkit package, and there is no `.fx`, `.teamsapp`,
  `TeamsToolkit`, `.m365` or `.atk` directory anywhere under the user
  profile, nor any tenant-login trace. So this page is documentation-only
  **by necessity rather than by choice** — there is nothing here to run it
  against. Never describe a claim on this page as observed. Compare
  `zcode.md`, whose install section *is* observation, and say which you mean.
