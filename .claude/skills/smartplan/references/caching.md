# caching — context economy & the automatic cost lever

> Facts verified 2026-07-09 against code.claude.com/docs (prompt-caching,
> sub-agents, memory, costs) and platform.claude.com/docs (pricing,
> context-windows, compaction); see the development repo's claim ledger. Fork-command rename and
> the fast-mode / overage-TTL additions re-verified 2026-07-21 at source
> (sub-agents + prompt-caching docs).

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

| TTL | Write | Read | Breaks even on |
| --- | --- | --- | --- |
| 5-minute | 1.25× base input | 0.1× base input | 1st reuse |
| 1-hour | 2× base input | 0.1× base input | 2nd reuse |

Max **4 explicit cache breakpoints** per request. Claude Code auto-requests
the free 1-hour TTL for the main conversation on a paid subscription; the
API/Bedrock/Vertex default is 5-minute (`ENABLE_PROMPT_CACHING_1H=1` to opt
in, at the 2× write cost) — and a subagent never gets the 1-hour tier,
subscription or not (§2, Seam B). Every cache read resets the TTL clock;
only a real idle gap longer than the TTL forces a cold rebuild.

**What invalidates the prefix — don't do these mid-run:**

| Trigger | Why |
| --- | --- |
| Switching `/model` or `/effort` mid-session | Both are part of the cache key. (An effort switch now warns with a confirmation dialog before busting the cache.) |
| Toggling fast mode mid-session | Fast mode adds a request header that is part of the cache key — the next request re-reads the entire history uncached. |
| Falling into usage-credit overage (subscription) | Silently drops the main conversation from the 1-hour to the 5-minute TTL — a long orchestrator session near plan limits loses its TTL margin exactly when spend matters. |
| Churning the tool/MCP set | Tool defs live in the prefix; adding or removing one invalidates tools+system+messages together. |
| A bare-name tool deny, e.g. `deny:["Bash"]` | Strips the tool definition, which busts the cache. A *scoped* rule like `Bash(rm *)` doesn't. |
| A Claude Code version upgrade landing mid-`--resume` | New version → changed system prompt → the entire history reprocesses at full price. `DISABLE_AUTOUPDATER=1` for predictable timing. |

Prefer **`/rewind`** over **`/clear`** to back out of a bad turn: `/rewind`
truncates to a still-cached point, `/clear` discards the cache entirely.
Monitor hit rate with **`/usage`** (cost plus a skills/subagents/MCP
breakdown) or a statusline reading `cache_read_input_tokens` /
`cache_creation_input_tokens` directly.

**Re-verified 2026-07-11** (code.claude.com/docs/en/prompt-caching +
/skills), three additions that change dispatch construction:

- **Same-directory parallel sessions share the cache** — matching prefixes
  read each other's entries. This is the API-level fact behind the
  shared-prefix-first wave rule (`claude-code.md`). It does **not** make a
  simultaneous wave free: an entry only becomes readable once the first
  response starts streaming, so N dispatches fired at the same instant all
  pay the cold write (§ External levers, and flow.md step 3 carries the
  stagger rule). Stagger the wave and the siblings read at 0.1×; fire it
  flat and every one of them writes. Worktrees never share at all (each is
  its own working directory).
- **Deferred MCP tools (the default) are cache-safe** — servers
  connecting/disconnecting only append; tools loaded into the prefix
  (Haiku, `alwaysLoad`, gateways) invalidate on any change.
- **Skill-listing context is capped per skill** — description +
  `when_to_use` truncate at 1,536 chars in the listing; a skill with
  `disable-model-invocation: true` is never auto-loaded by the model (and
  never preloaded into subagents) — pure payload skills like `smartexec`
  carry it to stay out of the listing.
- **Compaction re-injects invoked skill bodies "capped at 5,000 tokens
  per skill and 25,000 tokens total; oldest dropped first"** (confirmed
  verbatim 2026-07-11, context-window docs) — the hard reason the kernel
  carries a byte budget at all. That budget is now **5,120B**
  (the repo's byte-budget gate; ratcheted 16KB→4KB on 2026-07-13, raised
  4→5KB on 2026-07-30), which is a low four-figure token count on any
  plausible tokenizer and so clears the 5,000-token per-skill cap with room
  to spare — the whole body survives a compaction. The pre-M2 36KB kernel
  did not: it blew past the cap and was silently truncated every time.

### 2. The two smartplan seams (why this reference exists)

**Seam A — the §A belt-and-suspenders is safe.** §A's wave guarantee —
`export CLAUDE_CODE_SUBAGENT_MODEL=sonnet` before an implementer wave,
`=inherit` after — only changes which model a *dispatched subagent* resolves
to. Setting it is a shell export plus a tool call appended to the *end* of
the orchestrator's transcript, not an edit to the orchestrator's own model,
tools, or system prompt — by the documented cache-key rules (§1: model,
tools, and system define the key; appending new turns doesn't retroactively
change any of them), that means it never touches the main thread's cache.
That's a different action from the general rule it sits next to: **switching
the MAIN session's own `/model` or `/effort` mid-run busts that session's
whole prompt cache** (§1, above). Drop the orchestrator itself to Sonnet
mid-run instead of exporting the env var, and you pay full retail to rebuild
everything already in its transcript.

**Seam B — fan-out width fights cache economics.** smartplan's decomposition
guidance (flow.md step 1) optimizes for **maximum parallelism** — many
small independent leaves. Caching optimizes for **staying in one warm
context**. Every fresh subagent builds its **own cold cache** and gets only
the **5-minute TTL** — the free 1-hour TTL is main-conversation-only, even on
a subscription. A 5-leaf wave is five cold cache-writes of
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
  CLAUDE.md. Run `/context` between waves first for the window-size read,
  but don't plan around a per-source breakdown: the development repo's claim ledger marks that
  claim PARTIAL and records `/context` as window-size only.
  For a run that's
  genuinely large rather than just accumulated, the **1M context window** is
  the alternative to fighting compaction: no pricing premium above 200K (a
  900K-token request bills at the same per-token rate as a 9K-token one).
  Sonnet 5 runs 1M by default, auto-compacting near 967K; Opus gets it free
  on Max/Team/Enterprise. The real cost of going long isn't dollars, it's
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
2026-07-09 base sweep, the 07-11 additions marked inline, and the 07-21
re-verify named in the header. Model prices move — Sonnet 5's own scheduled
2026-09-01 step-up was cancelled on 2026-08-10 and $2/$10 is now the
standard rate, which is exactly why you re-check rather than extrapolate.
The multipliers in this file don't change, the dollars they multiply do.
Root **the development repo's claim ledger** holds the source check for the
**priced and capped** claims here — the cache multipliers, the base rates,
the compaction and skill-listing caps — so re-verify those against it
rather than trusting these numbers indefinitely. It does **not** cover the
whole page: `/rewind` vs `/clear`, `/subtask`, and the entire auto-memory
bullet carry no row at time of writing, and `/context`'s row is PARTIAL.
Treat those as docs-sourced-when-written, not ledger-backed.

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
  the cold 1.25× write. Fire one leaf, await first output, then the rest
  (flow.md step 3 carries the rule).
- **Byte-stability:** never put dynamic bytes (timestamps, counters) early
  in a reused prefix — one changed byte turns downstream 0.1× reads into
  12.5×-relative writes.
- **API-axis only** (scripted verify, benchmark harnesses — unreachable
  from inside Claude Code/Copilot): 1-hour TTL (2× write, break-even on the
  2nd read per §1's table); `max_tokens:0` pre-warm; Message Batches 50% off for async
  post-hoc work, never merge-gating verify.
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
| Memory tool + context editing | **39%** combined, **84%** on a 100-turn eval | Partly |
| Context editing **alone** | **29%** | Partly |
| Tool-response verbosity enum | 206 → 72 tokens (**~1/3**) on one Slack tool | Yes, if you author the tool |

**The 29% is the finding that changes what to port.** The 39%/84% pair was
already in this file. The third figure was not: **context editing on its own
delivers 29%**, so most of the combined gain comes from pruning stale tool
results rather than from the memory tool. If you can only build one half,
build the pruning.

**The tool-count threshold is the actionable half of the Tool Search
result.** Tool-selection accuracy falls off past **30–50 available tools**.
That is a concrete number for when an MCP-heavy session stops routing
correctly — and it lines up with what Microsoft independently documents on a
different platform (quality degrades past ~10 functions per plugin, and
beyond 5 plugins it stops injecting them and falls back to semantic matching
on descriptions alone). Two vendors, same shape.

Claude Code caps a single tool response at **25,000 tokens**. That cap is
the mechanism behind hook-filtering advice, and it gives that advice a
number.

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
   token and latency control on Opus 5.
2. **Effort does NOT reliably shorten visible output on Opus 5.** The dial
   moves thinking volume; the visible response does not follow. Anthropic's
   stated remedy is an explicit prompt instruction. **So any guidance that
   says "drop effort to cut output tokens" is wrong here.**

A consequence this repo's registry does not model: on Opus 5 a low-effort
Opus run may beat a high-effort Sonnet run on cost-for-quality. The
model-tier axis and the effort axis are not independent, and the registry
only has a column for one of them.

## Where a skill's cost actually lands

**A loaded skill body is a RECURRING per-request cost, not a one-off.** Once
invoked it persists across turns and is re-sent on every subsequent request
for the rest of the session. That is a stronger argument for this repo's
byte ratchet than the compaction cap previously cited here — a fat skill is
expensive even in a session that never compacts.

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
- **Skills** — descriptions every request, body on use.
- **MCP** — names only, schemas deferred.
- **Subagents** — isolated context.
- **Hooks** — zero unless they return output.

Official `SKILL.md` guidance is now **under 500 lines**, with the same
rationale this repo uses (move detail to references). The byte ratchet here
is stricter and differently expressed, but that is the first official number
to benchmark it against.

## Sizing a fan-out, with both halves

The cost model for a wave has an inbound and an outbound half, and this file
previously only carried the inbound one:

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

## Cache invalidation is tiered, not all-or-nothing

Render order is **tools → system → messages**, and a change invalidates its
own level and everything after it:

- **Tool definitions** are the only thing that blows the whole cache.
- **`tool_choice` and images** invalidate the messages cache alone.
- **Effort and thinking** always invalidate the messages cache, and are
  model-specific for tools and system.

The practical advice in §1 survives unchanged. The mental model behind it
was cruder than the mechanism.

**Minimum cacheable prefix is per-model and NOT monotonic across
generations** — a prefix that caches on a newer model can silently fail to
cache on an older, cheaper one:

| Floor | Models |
| --- | --- |
| 512 | Opus 5, Fable 5, Mythos 5 |
| 1,024 | Opus 4.8, Sonnet 5, Sonnet 4.6, Sonnet 4.5, Opus 4.1, Opus 4, Sonnet 4 |
| 2,048 | Opus 4.7, Mythos Preview |
| 4,096 | Opus 4.6, Opus 4.5, **Haiku 4.5** |

Below the floor nothing caches and **no error comes back**. Prove a miss by
checking that both `cache_creation_input_tokens` and
`cache_read_input_tokens` are 0.

## An external yardstick for the benchmark corpus

Anthropic publishes an enterprise-deployment baseline: **~$13 per developer
per active day**, **$150–250 per developer per month**, and under $30 per
active day for 90% of users. This repo's T-records have never had an
outside number to sit against. They do now.

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

- **Coding is a stated poor fit for multi-agent fan-out.** The same post
  that supplies the 15× token multiplier says so directly, on two grounds:
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
