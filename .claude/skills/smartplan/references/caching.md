# caching — context economy & the automatic cost lever

> Facts verified 2026-07-09 against code.claude.com/docs (prompt-caching,
> sub-agents, memory, costs) and platform.claude.com/docs (pricing,
> context-windows, compaction); see the development repo's claim ledger. Fork-command rename and
> the fast-mode / overage-TTL additions re-verified 2026-07-21 at source
> (sub-agents + prompt-caching docs). §1's TTL-bucket, per-seat
> `cacheTtl` and hit-ratio lines came with the 2026-08-28 sweep. The
> invalidation rows and the API-axis facts were re-read 2026-09-15 and
> again in the 2026-09-22 Opus 5.5 sweep, which also added the OpenAI
> cache facts for the GPT seats.

Load this on Claude Code when sizing a fan-out for cost, choosing an
in-session fork (`/subtask`) vs. a fresh subagent, debugging an unexpectedly cold cache, or trimming
CLAUDE.md / the tool surface / the orchestrator's own thread. Cross-referenced
from flow.md's Honest scope note, `claude-code.md`, `copilot.md` and
`routing.md`.

## Contents

- Caching & context economy
- Language compression — which side of the token to compress
- External levers (API-axis + dispatch construction)
- Measured levers, ranked by published saving (swept 2026-08-12)
- What does NOT save tokens (checked, so nobody re-derives it)
- Effort is a cost lever, and not the one you think
- Where a skill's cost actually lands
- Sizing a fan-out, with both halves
- Verified 2026-08-31 — controls, confirmation, and what is free
- Two caps on the skill listing, not one
- Cache invalidation is tiered, not all-or-nothing
- An external yardstick for the benchmark corpus
- What the community actually converged on
- Anthropic's own guidance pushes toward inline, twice

## Caching & context economy

Model tiering (`routing.md`, same directory) buys a cheaper *rate* — but only
where you actively route work to a cheaper tier. Caching buys a cheaper
*resend*, and it isn't something you invoke: it's on by default, and Claude
Code resends the whole growing transcript every turn, so caching is already
doing most of the cost-saving work before any routing decision happens. The
only real lever left is not breaking it — and smartplan's own fan-out
pattern, many fresh subagents, is exactly the shape that breaks it most
easily (§2, below).

### 1. Caching — the automatic ~90% lever

A prompt-cache **read costs 0.1× base input** — roughly a 90% discount on
every token Claude Code re-sends from the stable prefix (system + tools +
the conversation so far). Matching is **exact, not per-segment**: a change
anywhere in the prefix invalidates everything *after* it, not just the part
that changed.

Exception: cache hits and refreshes on Fable 5.1 and Mythos 5.1 bill at
0.025× base input, about a 97.5% discount, and on Opus 5.5 at 0.05×,
about 95%. On those models a broken prefix costs 50× the read (25× on
Opus 5.5), not 12.5×. Opus 5.5 has been the default Opus since
2026-09-22. Byte-stability now matters twice as much on the planner seat
as it did on Opus 5.

| TTL | Write | Read | Breaks even on |
| --- | --- | --- | --- |
| 5-minute | 1.25× base input | 0.1× base input | 1st reuse |
| 1-hour | 2× base input | 0.1× base input | 2nd reuse |

Max **4 explicit cache breakpoints** per request. Every cache read resets the
TTL clock; only a real idle gap longer than the TTL forces a cold rebuild.

**TTL is set per bucket, and the buckets are separate.** The main conversation
takes `promptCacheTtl` / `CLAUDE_CODE_PROMPT_CACHE_TTL`; everything else,
subagents included, takes `subagentPromptCacheTtl` /
`CLAUDE_CODE_SUBAGENT_PROMPT_CACHE_TTL` (both need Claude Code ≥ 2.1.242,
read 2026-08-28). Resolution runs **six levels**, first match winning:
`FORCE_PROMPT_CACHING_5M=1` · the bucket's env var · the bucket's setting ·
a subagent's `experimental.cacheTtl` frontmatter (≥ 2.1.248, read
2026-08-28) · `ENABLE_PROMPT_CACHING_1H=1`, which requests an hour for
*both* buckets · the bucket default. In the everything-else bucket a small
set of server-controlled helper requests gets an hour, but only on a Claude
subscription within plan usage. On usage credits, an API key or a cloud
provider the whole bucket defaults to five minutes (read 2026-09-22).

**A subagent is not locked out of the 1-hour tier — it just defaults to five
minutes** on every billing path, and a longer tier is settable per seat. One
ceiling to know: level 4 is ignored while a Claude subscription is running on
usage credits, so the per-seat knob bends in overage. Seam B's cold-write
argument is unaffected either way, since a fresh subagent still warms its own
prefix and pays its own write.

**What invalidates the prefix — don't do these mid-run:**

| Trigger | Why |
| --- | --- |
| Switching `/model` mid-session, or `/effort` on most models | Each model has its own cache. On most models so does each effort level. Opus 5.5 and Fable 5.1 on an API key or a subscription keep the cache across an effort change. Claude Code applies the new level there without asking (on Fable 5.1 since v2.1.260). Not on Bedrock, Google Cloud's Agent Platform, a Claude apps gateway, with `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS`, or for an org with a HIPAA configuration (read 2026-09-22). Elsewhere Claude Code asks you to confirm an effort switch only while the cache is warm. `/model` asks only while the cache is warm and the new model isn't the one that produced the last response. |
| A skill or command whose `model:` frontmatter differs from the session, an automatic safety fallback, or an `opusplan` plan-mode toggle | Each is a model switch. So the next request re-reads the whole history uncached. |
| **First** fast-mode enable in a conversation | Fast mode adds a request header that is part of the cache key, so that one turn re-reads the whole history uncached — **at fast-mode rates**, which makes enabling it late in a long session the expensive case. Turning it off and on again later is free. `/clear` and `/compact` reset the once-per-conversation clock. The header is set once per turn. So a mid-turn enable moves the miss to the next turn's first request. Enabling it on an unsupported model also switches models, which starts a fresh cache. Running out of usage credits retries at standard speed and keeps the cache (read 2026-09-22). |
| Falling into usage-credit overage (subscription) | Silently drops the main conversation from the 1-hour to the 5-minute TTL — a long orchestrator session near plan limits loses its TTL margin exactly when spend matters. |
| Churning the tool/MCP set | Tool defs live in the prefix; adding or removing one invalidates tools+system+messages together. The one exception is toggling `/advisor`. Its tool definition sits after the cache breakpoint. So enabling or disabling it keeps the prefix. |
| A deny that removes a whole tool, when tool search is off or unavailable. That's a bare name like `deny:["Bash"]`, `Bash(*)`, a tool-name glob like `"*"`, or an MCP-only glob like `"mcp__*"` | Strips the tool definition, which busts the cache. Removing the rule later does it again. With tool search on (the default on supported models) the prefix survives. A *scoped* rule like `Bash(rm *)` never touches it. |
| Setting `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS` | Three costs at once. Claude Code stops marking its mid-conversation system context (file-change notices and the like) for caching. MCP tool search turns off. Every MCP tool then loads into the prefix, where each connect busts it, unless managed settings keep tool search on (v2.1.227+). Opus 5.5 and Fable 5.1 also lose the effort-change keep in the first row. |
| Accumulating many images or PDFs | Two limits apply: the API's image and PDF count per request, and Claude Code's own cap on their total size. When the next request would pass either one, Claude Code drops a batch of the oldest images and PDFs. The next request reprocesses from the earliest affected message. So a screenshot-heavy session pays a periodic partial rebuild. |
| A Claude Code version upgrade | The new version's system prompt makes the next *new* conversation build its cache from the top. A `--resume` keeps the prompt it started with by default. So its rebuild moves to the first compaction instead. Auto-update applies on next launch, never mid-session. `DISABLE_AUTOUPDATER=1` for predictable timing. |

Prefer **`/rewind`** over **`/clear`** to back out of a bad turn: `/rewind`
truncates to a still-cached point, `/clear` discards the cache entirely.
Two more actions keep the cache (read 2026-09-22). Switching output style
does. Since v2.1.251 the new style arrives as a conversation message and
applies from the next message rather than waiting for `/clear`.
**`/recap`** appends its summary as command output, which makes it the
cache-safe way to get a summary without `/compact`'s rebuild.
Monitor hit rate with **`/usage`**: it breaks cost down by skills, subagents,
plugins, Loops and per-MCP-server, and on v2.1.251+ prints a **Prompt cache
(main) hit-ratio** line (read 2026-08-28) that makes a hand-rolled statusline
redundant for subscribers. It covers the main conversation only. So a wave's
cold writes never show there. A miss is more than 5% and at least 2,000
tokens re-processed. v2.1.260+ names the likely cause (e.g. `tool
definitions changed`). Watch its **behavior flags** rather than raw
counters — "cache misses" is a named signal that fires on a 10% threshold,
and the Prompt cache (main) line splits out the misses Claude Code itself
caused — "when Claude Code has itself just rewritten the conversation, by
compaction or by clearing old tool results from context" — so a spike there
is machinery, not your prompt (read 2026-09-21).
So it tells you the prefix is breaking without your having to diff two
numbers yourself. A
statusline reading `cache_read_input_tokens` / `cache_creation_input_tokens`
still works where `/usage` isn't available.

**Re-verified 2026-07-11** (code.claude.com/docs/en/prompt-caching +
/skills), three additions that change dispatch construction:

- **Same-directory parallel sessions share the cache** — matching prefixes
  read each other's entries. This is the API-level fact behind the
  shared-prefix-first wave rule (`claude-code.md`). It does **not** make a
  simultaneous wave free: an entry only becomes readable once the first
  response starts streaming, so N dispatches fired at the same instant all
  pay the cold write (§ External levers, and flow.md step 3 carries the
  stagger rule). Where staggering pays, the siblings read at 0.1×; fire it
  flat and every one of them writes. Worktrees never share at all (each is
  its own working directory). Sequential sessions share only when the
  startup git-status snapshot matches. So a commit between two headless arms
  cools the second one's cache.
- **Deferred MCP tools (the default) are cache-safe** — servers
  connecting/disconnecting only append; tools loaded into the prefix
  invalidate on any change (tool search unavailable, e.g. a custom
  `ANTHROPIC_BASE_URL` gateway or pre-4.5 Google Cloud models, plus
  `alwaysLoad` and threshold-based loading). A Microsoft Foundry deployment
  hosted on Azure is on that list too. It rejects tool search server-side.
  Once Claude Code detects the rejection, it loads MCP tools upfront.
  `ENABLE_TOOL_SEARCH` can't override it (read 2026-09-22).
- **Skill-listing context is capped per skill** — description +
  `when_to_use` truncate at 1,536 chars in the listing; a skill with
  `disable-model-invocation: true` is never auto-loaded by the model (and
  never preloaded into subagents) — pure payload skills like `smartexec`
  carry it to stay out of the listing.
- **Compaction re-injects invoked skill bodies "capped at 5,000 tokens
  per skill and 25,000 tokens total; oldest dropped first"** (confirmed
  verbatim 2026-07-11, context-window docs) — the hard reason the kernel
  carries a byte budget at all. That budget is now **10,752B**
  (the repo's byte-budget gate; ratcheted 16KB→4KB on 2026-07-13, raised in
  steps since, most recently on 2026-09-15), which is a low four-figure
  token count on any plausible tokenizer and so clears the 5,000-token
  per-skill cap with room to spare — the whole body survives a compaction.
  The pre-M2 36KB kernel did not: it blew past the cap and was silently
  truncated every time.

### 2. The two smartplan seams (why this reference exists)

**Seam A — the §A belt-and-suspenders is safe.** §A's wave guarantee —
`export CLAUDE_CODE_SUBAGENT_MODEL=sonnet` before an implementer wave,
`=inherit` after — only changes which model a *dispatched subagent* resolves
to when nothing else already names one (a per-call model or a seat's own
frontmatter wins). Setting it is a shell export plus a tool call appended to
the *end* of the orchestrator's transcript, not an edit to the
orchestrator's own model,
tools, or system prompt — by the documented cache-key rules (§1: model,
tools, and system define the key; appending new turns doesn't retroactively
change any of them), that means it never touches the main thread's cache.
That's a different action from the general rule it sits next to: **switching
the MAIN session's own `/model` mid-run busts that session's whole prompt
cache** (§1, above). So does `/effort` on most models. The exception is an
Opus 5.5 or Fable 5.1 orchestrator on an API key or a subscription, where an
effort change keeps the cache. There you can raise effort for one hard step
without a cold rebuild. Drop the orchestrator itself to Sonnet
mid-run instead of exporting the env var, and you pay full retail to rebuild
everything already in its transcript. On Opus 5.5 there's little to win
from that drop anyway. Its $0.20 cache-read is Sonnet 5's exact rate. A
mostly-cached orchestrator turn costs the same on either. The saving lives
only in cold input (4 vs 2) and output (20 vs 10). A `PreModelSwitch` hook
(v2.1.251+) runs before Claude Code applies a requested model switch and
can allow, deny or ask. That turns "don't switch the orchestrator mid-run"
into an enforced rule rather than a remembered one.

**Seam B — fan-out width fights cache economics.** smartplan's decomposition
guidance (flow.md step 1) optimizes for **maximum parallelism** — many
small independent leaves. Caching optimizes for **staying in one warm
context**. Every fresh subagent builds its **own cold cache** and gets the
**5-minute TTL by default**, even on a subscription, until you raise its
bucket or its seat (§1). A 5-leaf wave is five cold cache-writes of
system+CLAUDE.md+tools that the main thread would otherwise pay for once;
this is the documented reason fan-out multiplies spend.

This doesn't undo the case for isolation (`routing.md`; `check.md`'s
fresh-context verifier) — a subagent's *internal* read volume still leaves
the main window either way. It means leaf-sizing is a **tradeoff, not a free
maximization**: weigh the parallelism a wave buys against the cold-cache
write each new spawn re-pays. When a leaf genuinely needs the parent's full
context — an audit/synthesis pass, an Integrate step — prefer an **in-session
fork** over a fresh subagent: the command is **`/subtask`** since
v2.1.212 (`/fork` now copies the whole session into a NEW background
session — the wrong primitive here). A fork's prefix is identical to its
parent's, so its first request reuses the parent's *warm* cache instead
of paying to rebuild it. (A forked subagent can't itself fork again.)

### 3. Batch API — not applicable

The Batch API's 50% discount is **async only**; `/batch`, Task subagents,
Agent Teams, and Managed Agents are all "stateful and interactive" — the
disqualifying property. No dispatch mechanism routes a fan-out through it.

### 4. Companion context levers (pair with caching)

These cut the *count* of tokens headed into the window — the other side of
the same coin. Generic session hygiene (CLAUDE.md leanness, tool/MCP
surface trimming) is the harness docs' job, not this file's; two levers
matter specifically to a fan-out run:

- **Orchestrator-thread compaction across waves.** A multi-wave smartplan
  run accumulates plan + N leaf returns + Integrate passes **in the
  orchestrator's own thread** — isolation protects subagents' windows, not
  this one. At each wave boundary, run `/compact <focus on the plan + open
  leaves>` rather than trust the default heuristic, or steer every
  compaction in the project with a `# Compact instructions` block in
  CLAUDE.md. A mid-run CLAUDE.md edit is cache-safe but takes effect only at
  the next `/compact`, `/clear` or restart. Compact while the wave's returns
  are still warm, not after an idle gap. A warm `/compact` reads the prefix
  from cache and costs a fraction of the context size. A cold one
  reprocesses the whole history as uncached input. **Compaction also bills a
  file re-read pass (documented 2026-09-21):** "Right after compaction,
  Claude Code re-reads up to five of the files Claude has read or edited in
  the session, choosing the ones modified most recently. A file over 5,000
  tokens comes back as a path reference without its content, shown as
  `Referenced file` instead of `Read`." So a compacted session re-buys its
  five hottest files — or their path stubs — before any new work runs. Run `/context` between
  waves first for the window-size read, but don't plan around a per-source
  breakdown, which no ledger row backs. For a run that's genuinely large
  rather than just accumulated, the **1M context window** is
  the alternative to fighting compaction: no pricing premium above 200K (a
  900K-token request bills at the same per-token rate as a 9K-token one).
  On the Anthropic API, Sonnet 5 and every Opus from 4.7 on, Opus 5.5
  included, run 1M on every plan, Pro included. Every native-1M model
  there, the Fable models too, auto-compacts near 967K unless you set an
  auto-compact window. That includes the Opus 5.5 orchestrator whose thread
  this bullet is sizing. `CLAUDE_CODE_DISABLE_1M_CONTEXT=1` drops them to
  200K. On Bedrock, Google Cloud and Foundry, Opus 4.8 and later
  compact at 200K unless pinned with `[1m]` (model-config, read
  2026-09-22). The real cost of going long isn't dollars, it's
  **context rot** — accuracy and recall decay as the window fills — so 1M
  buys room, not a reason to stop compacting with judgment.
- **Cross-session persistence.** `run-state.md` (flow.md step 3) and
  `contracts.md` (step 1) — both shapes defined in `artifacts.md`, same
  directory — already carry a capped-then-resumed run's state; the risk is a
  *new* session not knowing to look. Claude Code's **auto memory** is on by
  default (v2.1.59+): the first 200 lines / 25KB of a `MEMORY.md` auto-load
  every session (~680 tok), deeper files load on demand, and it survives
  `/compact` by re-injection — a re-spend, not free. Point `MEMORY.md` at an
  in-flight run — which plan, which `run-state.md`, what's still open — so a
  resumed session picks it up unprompted. `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`
  turns the feature off. The separate API-level memory tool
  (`memory_20250818`) is a file-backed primitive for custom Agent-SDK
  harnesses, not a Claude Code CLI command — relevant only if smartplan ever
  drives the raw API directly.

### 5. Honest framing

Caching lowers **the bill** on tokens you resend — roughly a 90% discount on
cache reads. It does **not** shrink token **count**: the full transcript is
still there, still counted, and a cold cache-write costs *more* than an
uncached call would (1.25×/2× against 1×), recouped only if something
actually reuses it. Caching pairs with **isolation** (`routing.md`,
`check.md` — the lever that moves the *count*) and **tiering** (`routing.md`
— the lever that moves the *price*); it is not a substitute for either, the
same way flow.md's Honest scope note says tiering isn't a substitute for
isolation. All three levers are independent and additive — skipping one
doesn't get made up for by the other two.

Numbers above carry the date of the pass that verified them — the
2026-07-09 base sweep, the 07-11 additions marked inline, the 07-21
re-verify named in the header, the 08-28 sweep additions marked inline,
the 2026-09-15 re-read of the invalidation rows and the API-axis facts, and
the 2026-09-22 Opus 5.5 sweep marked inline.
Model prices move — Sonnet 5's own scheduled 2026-09-01 step-up was
cancelled on 2026-08-10 and $2/$10 is now the standard rate, which is
exactly why you re-check rather than extrapolate.
The multipliers in this file mostly don't change, the dollars they multiply
do. Fable 5.1 and Mythos 5.1 already broke that rule with a 0.025× read,
and Opus 5.5 with a 0.05× one.
Root **the development repo's claim ledger** holds the source check for the
**priced and capped** claims here — the cache multipliers, the base rates,
the compaction and skill-listing caps — so re-verify those against it
rather than trusting these numbers indefinitely. It does **not** cover the
whole page: `/rewind` vs `/clear`, `/context`, and the entire auto-memory
bullet carry no row at time of writing. Treat those as
docs-sourced-when-written, not ledger-backed.

## Language compression — which side of the token to compress

Telegraphic "caveman" prose (drop articles and filler; code/paths/errors
byte-verbatim) saves real tokens on exactly one side. Intensity is
mode-gated: `modes.md`'s register row maps *lite/full/ultra* onto the dial
and each brief's optional `MODE:` line carries it, so executors never load
this file.

**Output side — adopt.** Output prices ≈5× input and is never cached.
Agent-consumed prose (scout packs, report bodies — text whose only reader
is another model seat) goes telegraphic; human-facing turns stay normal
prose.

**Input side — refuse.** Grammar-stripping briefs, skill bodies, or policy
text: (1) measurably degrades accuracy — LLMs store contextual signal in
exactly those "filler" tokens (LLM-Microscope, arXiv:2502.15007), worst on
subtle-fact tasks, which is what briefs are; (2) the cache already took the
win — hot surfaces re-read at 0.1×, so a word-level trim saves pennies
against a precision loss the verification apparatus exists to prevent;
(3) cheap executors need MORE explicitness, not less. (LLMLingua-class
pruning protects instructions by its own design — same verdict.)

## External levers (API-axis + dispatch construction)

- **Stagger wave dispatch:** a cache entry is readable only after the first
  response BEGINS streaming — N simultaneous same-prefix dispatches ALL pay
  the cold 1.25× write. Fire one leaf, await first output, then the rest,
  but only when the saved cold writes outweigh the extra orchestrator turn
  (flow.md step 3 carries the break-even test and a measured case where
  staggering loses).
- **Byte-stability:** never put dynamic bytes (timestamps, counters) early
  in a reused prefix — one changed byte turns downstream 0.1× reads into
  12.5×-relative writes (50× on Fable 5.1 and Mythos 5.1, 25× on Opus 5.5).
- **Through an LLM gateway, a custom `ANTHROPIC_BASE_URL`, or a cloud
  base-URL override such as `ANTHROPIC_BEDROCK_BASE_URL`, what stays cached
  depends on how the gateway handles `cache_control`** (prompt-caching docs,
  read 2026-09-22 — this box's zai shim is exactly such a gateway).
  Forwards the marker unchanged: caches like the provider's own endpoint.
  Rejects the marked request with a 400 naming `cache_control`: Claude Code
  re-sends with the marker moved onto the last conversation message, so the
  conversation stays cached and only the new block bills uncached. Strips
  the markers while returning success: "your entire conversation history
  bills as uncached input on every turn" — the single biggest cost
  multiplier a proxied harness can hit, and it presents as a mysteriously
  expensive session, not as an error. A gateway that converts block-form
  system content to a plain string strips the marker the same way. To spot
  the strip case, read `/usage`'s Prompt cache (main) line. Its counts come
  from the API's cache token fields. So it works on every provider and
  gateway. When no response reported cache tokens, it ends with "no prompt
  caching reported by the API" (costs docs, read 2026-09-22). The same line
  names the TTL in effect. An explicit one-hour TTL through a gateway needs
  the `anthropic-beta` header forwarded unchanged, since part of the
  one-hour request travels in it. A Claude apps gateway can't carry the
  hour at all.
- **API-axis only** (scripted verify, benchmark harnesses — unreachable
  from inside Claude Code/Copilot): `max_tokens:0` pre-warm; Message Batches
  50% off for async post-hoc work, never merge-gating verify. A pre-warm
  has to match the follow-up's thinking configuration and
  `output_config.effort`. It also needs an explicit breakpoint, since
  automatic caching would key the entry to the placeholder. A pre-warm at
  another effort writes an entry the real traffic never reads.
  `max_tokens:0` is rejected with `stream: true`, extended thinking
  enabled, structured outputs, a forced `tool_choice`, and inside Message
  Batches (read 2026-09-22). Cache hits inside a batch are best-effort,
  since its requests run concurrently and in any order. So a batch-priced
  verify shouldn't count on reads unless it writes a 1-hour prefix first,
  the pattern the docs recommend for batches. A breakpoint
  only finds writes within the last 20 blocks (a run of parallel tool calls
  counts as one). So a harness with a long growing transcript needs a second
  breakpoint. Cache hits don't count against rate limits. Two harnesses in
  different workspaces never share a cache on the Claude API.
- **The 1-hour TTL is not one of them.** It's settable in Claude Code too,
  through §1's per-bucket settings. On the API it's `ttl: "1h"` (2×
  write, break-even on the 2nd read per §1's table). Only Copilot has no
  control for it. On the API a request can mix both TTLs as long as the
  1-hour entries come before the 5-minute ones.
- **API-axis prefix edits that keep the cache** (read 2026-09-22).
  Appending a `role: "system"` message mid-conversation keeps the system
  and message caches on Fable 5.1, Mythos 5.1, Fable 5, Mythos 5, Opus 5.5,
  Opus 4.8 and Opus 5 (Claude API, Bedrock and Google Cloud). Sonnet 5
  isn't on that list. A Sonnet-seated harness still pays a full miss for
  a system edit. Adding or removing tools mid-conversation needs the
  `mid-conversation-tool-changes-2026-07-01` beta header. Defining a tool
  by value in a `tool_addition` block uses `inline-tools-2026-09-15`
  instead (beta since 2026-09-22, Claude API only). It adds a tool,
  changes its schema or moves it to a newer server-tool version without
  editing `tools`. It costs one full miss only when `tools` has no
  non-deferred tool. Compaction on demand (`compact-2026-09-04`, beta since
  2026-09-14, not on Bedrock) returns a signed compaction block. Kept
  turns' thinking can stay valid through it on preserved-thinking models,
  Opus 5.5 included.
- **One API-axis prefix edit is an error, not a miss.** For accounts
  created on or after 2026-08-31, replaying an Opus 5.5 or Fable 5.1
  thinking block after the system prompt, tools or an earlier message
  changed returns a 400 by default, on the Claude API and the cloud
  platforms. The fix is an append-only conversation, or `drop_block` under
  the `thinking-binding-controls-2026-08-01` beta. Claude Code is already
  append-only. So this bites only a scripted harness that edits its prefix
  mid-run.
- **Two API-axis facts for a benchmark harness.** Cache diagnostics
  (`cache-diagnosis-2026-04-07`, beta, Claude API only) takes the previous
  response id as `diagnostics.previous_message_id` and reports where the
  prefix first diverged: model, system, tools or messages. It's the
  API-side twin of `/usage`'s likely-cause text. US data residency
  (`inference_geo: "us"` on Claude 4.6 and later) multiplies every token
  category by 1.1×, cache reads and writes included, on the Claude API and
  Claude Platform on AWS. `/usage` applies it since v2.1.239. So a
  benchmark priced from list rates undercounts a US-residency org by 10%.
- **OpenAI seats cache on the same write shape, with a longer life**
  (OpenAI prompt-caching guide, read 2026-09-22). From GPT-5.6 on, GPT-6
  included, a cache write costs 1.25× uncached input and a read 0.1×.
  Earlier OpenAI models carry no write charge. A cached prefix stays
  eligible at least 30 minutes after its latest write or reuse. Thirty
  minutes is both the only value and the default. The floor is 1,024
  visible input tokens. A request can make up to four cache writes. An
  implicit breakpoint takes one of the four. GitHub's own price table
  charges the cache write on Anthropic models and on GPT-5.6 and later
  only. So the stagger arithmetic above now holds for every GPT slug on
  the Copilot seats (GPT-6 Sol, GPT-6 Luna, GPT-5.6 Luna). N simultaneous same-prefix
  dispatches all pay the cold write. Cached state lives on individual
  machines. Traffic above 15 requests per minute can overflow to other
  machines. So a wide same-prefix wave on an OpenAI seat can miss even
  when staggered (derived, not vendor-stated). Copilot builds the
  request. GitHub doesn't document whether it places breakpoints or passes
  the 30-minute window through.
- **Closed negatives:** token-efficient-tools is built into Claude 4+ (a
  no-op header); **prompted** LLM-summarizing of context LOSES
  to omission/masking (arXiv:2508.21433) — never spend a model call to
  recap state; use the fixed-schema artifacts (`run-state.md`) instead.
  The *prompted* scoping is deliberate: an RL-trained compactor beats a
  prompted one (+7.0pp SWE-V, arXiv:2607.05378), so this is a fixable
  training gap, not a hard ceiling. It just isn't reachable from a
  prompt-level policy today.

## Measured levers, ranked by published saving (swept 2026-08-12)

Every figure here is Anthropic-published with the mechanism named. Ranked by
size, but read the reachability column first — the biggest three are
API-axis and cannot be reached from inside Claude Code or Copilot.

| Lever | Published saving | Reachable from a harness? |
| --- | --- | --- |
| MCP tools presented as code on a filesystem | 150,000 → 2,000 tokens (**98.7%**) on one worked example | No — API axis |
| Tool Search Tool | **85%** cut, plus selection accuracy 49→74% (Opus 4) and 79.5→88.1% (Opus 4.5) | No — API axis |
| Programmatic tool calling | 43,588 → 27,297 avg (**37%**) on complex research, accuracy up on two benchmarks | No — API axis |
| Memory tool + context editing | **39%** better *performance over baseline* on agentic search — not a token cut — plus **84%** token reduction on a 100-turn web-search eval | Partly |
| Context editing **alone** | **29%** better *performance over baseline*, same unit and eval as the 39% above | Partly |
| Tool-response verbosity enum | 206 → 72 tokens (**~1/3**) on one Slack tool | Yes, if you author the tool |

**Read the units before you size a port.** 39% and 29% are
performance-over-baseline on the same eval, so comparing them is valid;
**neither is a token saving**, and only the 84% is. The comparison that
matters still holds: **context editing on its own delivers 29 of the 39
points**, so most of the combined gain comes from pruning stale tool results
rather than from the memory tool. If you can only build one half,
build the pruning.

**The tool-count threshold is the actionable half of the Tool Search
result.** Tool-selection accuracy falls off past **30–50 available tools**.
That is a concrete number for when an MCP-heavy session stops routing
correctly — and it lines up with what Microsoft independently documents on a
different platform (quality degrades past ~10 functions per plugin, and
beyond 5 plugins it stops injecting them and falls back to semantic matching
on descriptions alone). Two vendors, same shape.

Claude Code caps a single MCP tool response at **25,000 tokens** by
default, with a fixed warning past 10,000 (read 2026-09-22).
`MAX_MCP_OUTPUT_TOKENS` raises the cap. A tool that declares
`anthropic/maxResultSizeChars` uses that limit for its text instead. An
over-limit result with no image content is saved to a file in the session's
tool-results directory rather than dropped. Bash output is sized
separately, inline up to about 30,000 characters by default, with
`bashOutputMaxChars` going up to 128,000. Those caps are the mechanism
behind hook-filtering advice. They give that advice a number.

## What does NOT save tokens (checked, so nobody re-derives it)

- **Structured outputs.** `output_config.format` with `strict: true` buys
  schema compliance and eliminates retries. The docs frame the benefit as
  reliability, explicitly. It is a retry-elimination lever — a real but
  indirect saving — and does not belong on a token-efficiency list.
- **A `verbosity` parameter.** There isn't one. That is an OpenAI knob.
  Anthropic's documented output-token levers are `output_config.effort`,
  an explicit prompt instruction about length (Anthropic supplies
  recommended wording), `max_tokens` as a hard ceiling, and advisory task
  budgets.
- **Stop sequences.** No primary source claims a measured saving. The docs
  treat `stop_sequences` as a control mechanism, not an economy one.
- **`/clear` and `/compact`.** No published figure in dollars or tokens.
  The costs page describes both qualitatively. Useful, unquantified.

## Effort is a cost lever, and not the one you think

Two corrections that matter on the current flagship:

1. **Effort reliably reduces the NUMBER of tool calls** — and tool calls,
   not response prose, are the dominant cost driver in an agentic loop. That
   makes effort a first-class lever alongside model tier rather than a
   secondary one. Anthropic now names effort, not model choice, the primary
   token and latency control on Opus 5, and on Opus 5.5, which drops the
   default to medium and can't turn thinking off at all.
2. **Effort does NOT reliably shorten visible output on Opus 5.** The dial
   moves thinking volume; the visible response does not follow. Anthropic's
   stated remedy is an explicit prompt instruction. **So any guidance that
   says "drop effort to cut output tokens" is wrong here.**

A consequence this repo's registry does not model: on Opus 5 a low-effort
Opus run may beat a high-effort Sonnet run on cost-for-quality. Opus 5.5
sharpens it. AA's index scores it 51 at its default medium, level with
Opus 5 at max, at $1.34 against $5.86 per task (read 2026-09-22).
Anthropic's own testing agrees. Its Opus 5.5 prompting guide puts the
model at default medium level with or ahead of Opus 5 at high on
repository coding, in fewer steps and tokens. The same guide says lowering
effort cuts thinking, and with it cost and latency, more reliably than
prompt instructions do. The model-tier axis and the effort axis are not
independent. The registry only has a column for one of them.

## Where a skill's cost actually lands

**A loaded skill body is a RECURRING per-request cost, not a one-off.** Once
invoked it persists across turns and is re-sent on every subsequent request
for the rest of the session. That is a stronger argument for this repo's
byte ratchet than the compaction cap — a fat skill is expensive even in a
session that never compacts.

Progressive disclosure is now a published three-state table:

| Setting | Description in context? | Body loads |
| --- | --- | --- |
| default | Always | On invocation |
| `disable-model-invocation: true` | **No** | Manual invoke only — zero standing cost |
| `user-invocable: false` | Yes | On invocation |

The middle row is what `smartexec` relies on. **Subagents are the
exception**: skills named in a subagent's `skills:` field are fully
preloaded, so a subagent seat pays the whole body up front.

Anthropic's own loading-strategy table, worth carrying because it prices
each feature differently:

- **CLAUDE.md** — full content, every request. Stated rule of thumb: keep it
  **under 200 lines**. *(This repo's own CLAUDE.md is well past that, and that
  is a live per-request cost rather than a hypothetical one.)*
- **Output styles**, the active style's full instructions, every request.
  They load at session start. The Default style loads nothing. That's one
  more reason a benchmark arm pins `outputStyle` to Default.
- **Skills** — descriptions every request, body on use.
- **MCP** — names only, schemas deferred.
- **Subagents** — isolated context.
- **Hooks** — zero unless they return output.

Official `SKILL.md` guidance is now **under 500 lines**, with the same
rationale this repo uses (move detail to references). The byte ratchet here
is stricter and differently expressed, but that is the first official number
to benchmark it against.

## Sizing a fan-out, with both halves

The cost model for a wave has an inbound and an outbound half. Size both:

- **Inbound:** N leaves cost N cold cache writes at 1.25×, unless staggered
  so siblings read a warm prefix at 0.1×.
- **Outbound:** a subagent summary runs **1,000–2,000 tokens**. That is the
  number to size an Integrate step against.

Two hard bounds to respect while decomposing:

- **20 concurrent subagents per session.** The 21st fails with
  `Concurrent subagent limit reached` and the error tells the model not to
  retry. Configurable via `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`; sessions
  with ultracode active are exempt. Requires v2.1.217+.
- **The prompt cache TTL runs from request start, not response end.** A long
  streaming response eats its own window: on a 5-minute TTL, a 4-minute
  response leaves roughly 1 minute of usable cache. This bites exactly the
  long agentic turns a fan-out dispatches.

## Verified 2026-08-31 — controls, confirmation, and what is free

**Confirm the TTL a session actually used, rather than inferring it.** Run
`claude -p "hello" --output-format json` and read `usage.cache_creation`:
one-hour writes land under `ephemeral_1h_input_tokens`, five-minute writes
under `ephemeral_5m_input_tokens`. That turns "which tier did I get" from a
guess into a check.

**Claude Code staggers a workflow fan-out for you now.** In a fan-out of
same-prefix agents it holds all but the first **for up to 5 seconds by
default** (read 2026-09-21), so the rest read the prefix the first one
cached instead of each paying a cold write. **Workflow agents share that
prefix only when model, effort, agent type, tools, output schema and
working directory all match** (workflows docs, read 2026-09-22). A leaf
that differs in any of them processes its own prefix uncached. The
stagger doesn't help it. So keep effort uniform within a fan-out stage and
vary it only between stages. The same holds for output schema and agent
type. Workflow agents also default to the five-minute TTL, even on a
subscription. The knob is
`CLAUDE_CODE_WORKFLOW_PREFIX_STAGGER_MS`: default `5000`, `0` disables the
wait, agents never wait when `DISABLE_PROMPT_CACHING` is set, and it
requires v2.1.229 or later. The manual
stagger in `flow.md` step 3 is still the right instinct on other harnesses
and for hand-rolled dispatch, where its break-even test says it pays, but on
Claude Code workflows it is no longer work you have to do.

**Measure the listing before blaming the work.** "Run `/doctor` for an
estimate of the listing's context cost and its biggest contributors. To
find skills worth turning off, run `/skill-doctor`." (skills docs, read
2026-09-21; `/skill-doctor` requires v2.1.252.) That is the first-party
measurement for exactly what gate (k) encodes by hand.

**Agent teams cost about 7× a standard session** when teammates run in plan
mode, because each teammate keeps its own context window and runs as a
separate instance. Size a team against that multiplier, not against a
subagent's.

**Kill switches, if you need to prove caching is the variable.**
`DISABLE_PROMPT_CACHING` turns it off everywhere; `DISABLE_PROMPT_CACHING_HAIKU`
/ `_SONNET` / `_OPUS` / `_FABLE` do it per model. Claude Code warns at startup
when caching is off this way (since 2.1.108), so a silent misconfiguration
announces itself.

**Some spend mysteries are harness bugs, not your prompt.** 2.1.248 fixed a
prompt-cache miss (and lost extended-thinking context) recurring roughly
hourly in long sessions, caused by tool definitions re-rendering after an
OAuth token refresh. Eleven more prompt-cache fixes landed after 2.1.267,
which is still npm's `stable` tag while `latest` is 2.1.280 (read
2026-09-22). That's one in 2.1.268 (SDK sessions using
`excludeDynamicSections`), three in 2.1.269 (output-token-limit resume,
interrupted resume, the cloud first request), one in 2.1.273 (`/login`,
`/upgrade` and `/extra-usage` dropping thinking), one in 2.1.275 (the
memory age note), three in 2.1.277 (SessionStart hook output after
`/clear`, resumed subagents and teammates re-rendering their MCP tool
definitions, re-rendered attachments) and two in 2.1.280 (a host-app model
switch, resumed fork subagents rebuilding their tool list). The 2.1.277 and
2.1.280 resume fixes bear on a same-tier `SendMessage` retry
(`claude-code.md`). On the stable channel a resumed subagent or fork still
pays those misses. Separately, 2.1.273 fixed the context meter and
auto-compact counting advisor-tool turns at twice their real size, which
fired auto-compact at about half the real window. Check your version
before designing around an unexplained cost spike.

**Adding a plugin mid-session is mostly free.** A plugin's skills, commands,
agents, hooks, monitors and themes append *after* the existing conversation,
so the next request pays for that content once and still reads everything
before it from the cache. This is the rare mid-run change that does not
invalidate. The exception is a plugin that ships MCP servers. It follows the
MCP rule. So tools loaded into the prefix force a full re-read.
`/reload-plugins` warns and holds that reload unless you pass `--force`.

**Automatic caching is the recommended starting point on the API axis.** A
single top-level `cache_control` field lets the system manage breakpoints
as the conversation grows. It doesn't replace the 4-breakpoint cap. It
takes one of the four slots (read 2026-09-22). So a request returns a 400
when four explicit block-level breakpoints already exist and a top-level
`cache_control` asks for a fifth. It also returns a 400 when the last
block's explicit TTL differs from the automatic one. On the legacy Amazon
Bedrock integration (Opus 4.6 and earlier) a top-level `cache_control`
returns a 400 as well. Use explicit breakpoints there.

**Extended thinking splits by model.** Non-tool results with extended thinking
preserve thinking blocks on Opus 4.5+ and Sonnet 4.6+; earlier models strip
them, which invalidates the cache.

**Budget in tokens, not characters, across model generations.** Claude 4.7 and
later, plus Mythos Preview, use a newer tokenizer producing roughly **30% more
tokens for the same text**. Sonnet 4.6 and earlier use the previous one. Every
byte budget in this repo is measured in bytes for exactly this reason — a
character count is stable across that change and a token count is not.

## Two caps on the skill listing, not one

The 1,536-character per-skill description cap is Claude Code's, and it is
configurable via `skillListingMaxDescChars` (read 2026-09-20). This repo's
own gate (k) is tighter, capping all six descriptions at 2,304 bytes
combined. There is a second above it: **the listing budget scales at 1% of
the model's context window**, with a fallback of 8,000 characters (read
2026-09-22). When it overflows, Claude Code drops
descriptions **starting with the skills you invoke least**, so the ones you
use most keep their full text. A family that installs six descriptions is
competing against every other installed skill for that 1%. **The budget is
configurable too (read 2026-09-21):** raise it with the
`skillListingBudgetFraction` setting (e.g. 0.02 = 2%) or
`SLASH_COMMAND_TOOL_CHAR_BUDGET` (a fixed character count, under a legacy
name kept for compatibility), and
`skillOverrides: name-only` frees budget by listing a skill without its
description. Exceeding the budget writes a warning to the debug log
(`--debug`), and `/context`'s Skills row reports the post-budget size
(before v2.1.196 it could show several times the budget).

**The listing doesn't come back after `/compact`.** Compaction re-injects
invoked skill bodies only. Skill descriptions aren't reloaded
(context-window docs, read 2026-09-22). So after a compaction,
description-level routing has no listing to match against for any skill
the run hasn't invoked. That matters for a long orchestrator run that
compacts between waves.

**Truncation keeps the START of a skill body.** So the most important
instruction belongs near the top of `SKILL.md`, above everything explanatory —
which is independently why `smartplan`'s routing call sits on the first line.
Re-invoking a skill whose rendered content is unchanged adds a note rather
than a second copy, so repeat invocation is cheap.

## Cache invalidation is tiered, not all-or-nothing

Render order is **tools → system → messages**, and a change invalidates its
own level and everything after it:

- **Tool definitions** are the only thing that blows the whole cache.
- **`tool_choice` and images** invalidate the messages cache alone.
- **Web search, citations and `speed`** invalidate system and messages but
  keep tools.
- **Effort and thinking** always invalidate the messages cache, and are
  model-specific for tools and system. Two exceptions. An explicit effort
  equal to the model default is a no-op. A per-message effort change in a
  `role: "system"` message keeps the prefix. That works on Fable 5.1,
  Mythos 5.1, Opus 5.5 and Opus 5, behind the
  `mid-conversation-output-config-2026-07-01` beta header, on the Claude
  API and Google Cloud (read 2026-09-22). Models without per-message
  effort, Fable 5 included, return a 400. A top-level effort change starts
  the cache over.
- **Dropped thinking blocks** invalidate the messages cache from that
  block onward. The API drops a Fable 5.1 or Mythos 5.1 thinking block
  that isn't preserved on a request, for example one replayed to an
  earlier model. So a Fable 5.1 planner that falls back to Opus 5 or 4.8
  re-reads from the first dropped block uncached.

The practical advice in §1 survives unchanged. The mental model behind it
was cruder than the mechanism.

**Minimum cacheable prefix is per-model and NOT monotonic across
generations** — a prefix that caches on a newer model can silently fail to
cache on an older, cheaper one:

| Floor | Models |
| --- | --- |
| 512 | Fable 5.1, Mythos 5.1, Opus 5.5, Opus 5, Fable 5, Mythos 5 |
| 1,024 | Opus 4.8, Sonnet 5, Sonnet 4.6, Sonnet 4.5, Opus 4.1, Opus 4, Sonnet 4 |
| 2,048 | Opus 4.7, Mythos Preview, Haiku 3.5 (retired, except on Bedrock and Google Cloud) |
| 4,096 | Opus 4.6, Opus 4.5, **Haiku 4.5** |

Below the floor nothing caches and **no error comes back**. Prove a miss by
checking that both `cache_creation_input_tokens` and
`cache_read_input_tokens` are 0.

## An external yardstick for the benchmark corpus

Anthropic publishes an enterprise-deployment baseline: **~$13 per developer
per active day**, **$150–250 per developer per month**, and under $30 per
active day for 90% of users. This repo's T-records have never had an
outside number to sit against. They do now. The floor is published too.
Background usage, meaning conversation summarization for `claude --resume`
and status checks like `/usage`, runs under $0.04 per session (costs docs,
read 2026-09-22).

## What the community actually converged on

Star counts read live from the GitHub API on 2026-08-12. Community-sourced,
labelled as such — these are adoption signals, not evidence of efficacy.

| Repo | Stars | Forks |
| --- | --- | --- |
| obra/superpowers | 271,224 | 24,237 |
| anthropics/skills | 168,512 | 20,074 |
| anthropics/claude-code | 141,220 | 22,686 |
| hesreallyhim/awesome-claude-code | 52,211 | 4,558 |
| wshobson/agents | 38,746 | 4,130 |
| github/awesome-copilot | 37,741 | 4,757 |

**`superpowers` is the most-adopted public statement of the same shape this
family implements**: brainstorm → git worktree → plan into 2–5 minute tasks
→ subagent-driven development with a fresh agent per task → TDD → two-stage
code review → branch completion. Two differences worth noting rather than
copying blindly. Its dispatch unit is **far smaller** than a smartplan leaf,
and it pairs every dispatch with TDD, which supplies the tier-1 executable
oracle this repo's verify floor asks for. `wshobson/agents` has gone
multi-harness — Claude Code, Codex, Cursor, OpenCode, Copilot and Gemini —
which is the same four-harness pressure that produced `zcode.md` and
`m365-copilot.md` here.

## Anthropic's own guidance pushes toward inline, twice

Both of these are primary-source support for a route-inline-first default
that until now rested on this repo's own measurement:

- **Coding is a stated poor fit for multi-agent fan-out.** Anthropic's
  multi-agent research post, which measured multi-agent runs at about 15× a
  chat's tokens, says so directly, on two grounds:
  fewer genuinely parallelizable subtasks than research, and weak real-time
  coordination between agents.
- **Simplest solution first.** The foundational agents post states the
  default independently — find the simplest solution and increase complexity
  only when needed, noting that agentic systems trade latency and cost for
  performance.

And one that pushes against a piece of this repo's machinery, worth stating
precisely because the scope is narrow: **Anthropic tells callers to delete
explicit verification instructions on Opus 5**, naming "legacy harness
scaffolding that adds separate verification steps". Read the scope. The same
doc set praises Opus 5's "effective writer-verifier patterns", and the
current Claude Code best-practices page recommends a verification subagent
so "the agent doing the work isn't the one grading it". What must go is a
**standing blanket instruction** to self-verify every task. What survives is
an **invoked gate** run by a context that did not produce the work. The
verify floor stands; a `brief.md` that tells Opus 5 to double-check itself
does not.
