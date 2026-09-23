# Copilot on a Budget: Getting the Most from a Low Credit Allowance

*This page is meant as a quick reference on practical cost control for
GitHub Copilot CLI. Rates, rosters, and CLI behavior were last read
2026-09-22 from the sources at the end.*

## Where this page sits

[The model guide](https://dougfessler.com/smartplan-plugin/copilot-model-guide.html) tells you what to pick. This
page tells you how to spend less once you've picked.

## How Copilot Billing Works (the Mental Model)

Since 2026-06-01, usage is token-metered in credits worth $0.01 each.
Pro+ costs $39 a month for 7,000 credits, worth $70. That's 3,900 fixed
base credits plus 3,100 flex credits GitHub calls variable and "designed
to adapt". Pro splits 1,000 base plus 500 flex. Max splits 10,000 plus
10,000. Allowances reset at 00:00 UTC on the first of each month,
whatever your billing date. Four things drive the bill:

- Which model - Sonnet 5 runs $2/$10 per 1M in/out (see the [GitHub pricing
  table](https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing)).
  Haiku 4.5 is half that. GPT-6 Luna, GA on every paid plan since
  2026-09-22, is the cheapest Copilot-dispatchable model on every axis at
  $0.10/$0.50. GPT-5.6 Luna is $0.20/$1.20. GPT-5 mini is $0.25/$2 and no
  longer free. Pro+ and up add GPT-6 Sol at Sonnet 5's price and Opus 5.5
  at $4/$20. Opus 5 and Opus 4.8 are $5/$25. Fable 5 (legacy since
  2026-09-07), Fable 5.1, Opus 4.8 fast mode, and GPT-6 Astra's lower tier
  are $10/$50. Astra tops out at $20/$75 past 272K tokens.
- How much context - the trap. The whole context is re-read every turn at
  the cache-read rate (~$0.2/M on Sonnet). A big one is paid *per turn*.
- How many turns - each extra round re-bills that context.
- How much output - output bills at ~5× input, reasoning and thinking
  tokens included.

A small, clean task run inline on Sonnet costs ~8.5 to 13 credits. A real
feature runs 20 to 50 (a two-file UE5 feature we measured came in just
over 19). Pro+'s 7,000 credits cover roughly 150 to 400 real tasks if you
avoid the accidents below.

## The Levers, Ranked by Impact

1. **Don't fan out ordinary work.** Fan-out splits one task across several
   agent sessions, for example with `/fleet`. On a task that fits in one
   context it costs 2.3 to 4.2× more than inline, at identical quality.
   The tax is highest on small, easily parallelized modules. Fan out only
   for work bigger than one context, or for failure-prone work.
2. **Right-size the model. Don't leave the session on a premium one.**
   The fail-twice target is the Mid seat: GPT-6 Sol on Pro+ and up once a
   CLI build names it, Sonnet 5 otherwise. Send mechanical work, and every
   coding leaf outside a never-Cheap class (concurrency, UB, templates,
   security, determinism/serialization), to GPT-6 Luna first.
   It ties GPT-5.6 Luna on Artificial Analysis's index (37.26 against
   37.32) at under half the cost per task, though we haven't trialed it.
   No CLI build names a `gpt-6-luna` slug yet. Until one does, fall back
   to GPT-5.6 Luna. Boards split on whether it beats Sonnet 5. Keep a
   verifier on its work. GPT-5 mini is worth a trial until it retires
   from Copilot on 2026-10-19. Its one measured run cost about 39% of
   Haiku's. Kimi K2.7 Code ($0.95/$4, open-weight) is an A/B candidate
   for mechanical work until Kimi K3 replaces it on 2026-10-02. Its
   always-on thinking bills as output. Its cache reads cost 0.2×
   input, double the usual ratio. Save Opus for a hard *one-shot* plan and
   Fable/fast for the single hardest decision.
3. **Turn on Auto for a [10% discount on paid plans](https://docs.github.com/en/copilot/concepts/models/auto-model-selection).**
   Auto picks a model per request by task complexity. Since 2026-09-14
   the CLI offers three tiers (Efficiency, Balance, Intelligence).
   Efficiency suits ordinary mechanical work. From CLI 1.0.87 you can make
   it the tier every session starts on. An org policy can set it too. The
   changelog doesn't name the setting key yet. Pin an explicit model only
   when you're deliberately tiering a fan-out.
4. **Keep context small and sessions warm.** Scope the session to the
   files you're changing, not the whole repo or big headers. For
   follow-ups, `copilot --resume <id>` rides the *warm* cache instead of
   re-paying the cold context. We measured that at ~14k tokens bare and 75
   to 160k with a skill tree loaded.
5. **Terse output, low effort on mechanical turns.** Use `--effort low`
   (or `none`/`minimal`, where the model supports them) on boilerplate,
   since reasoning tokens are output-priced at $10/M on Sonnet. For named
   subagents, put `reasoningEffort: low` in the mechanical agents'
   frontmatter. It applies on dispatch and, since CLI 1.0.88, on
   selection. We haven't tested either on a paid plan. Don't pin it
   under `subagents.agents.<name>` in the repo's
   `.github/copilot/settings.json`, which silently ignores every
   `subagents.*` key. That key is documented for user settings only.
6. **Cap the runaway tail: it's the #1 budget accident.** One uncapped
   blind-repair spiral burned 167 credits in a session of ours. Put
   `--max-ai-credits` (or `/limits`) on a session so a loop can't run
   away. When a fix fails twice, *stop and diagnose* instead of retrying.
   Note: don't cap a session that should load a skill. A cap can make the
   model skip the skill to save budget. Cap the fan-out *leaves* (each
   subagent's unit of work) instead. A cap can't go below 30 credits.
   Since most leaves we've measured cost 1 to 13, a per-leaf cap catches
   only a runaway past 30. GitHub's docs disagree on whether `/limits`
   caps each response or the whole session.
7. **Script anything deterministic.** A shell script costs zero model
   calls.

## Budget Killers (the Anti-Patterns)

Ignoring any lever above is a budget killer. Auto adds one more. On Pro+
and up it can send a hard prompt to Opus 5, Opus 4.8, or GPT-6 Astra. Opus
5.5, GPT-6 Sol, and GPT-6 Luna aren't in Auto. You reach them only by
picking them. Only prerelease CLI 1.0.89-0 names one of them,
`claude-opus-5.5`.

## Watch the Meter

- `/usage` - session credits, a monthly plan bar, and an activity graph.
  Since CLI 1.0.85 it also lists per-model credit rows, which we haven't
  seen live yet. The token breakdown (input, output, cached) renders
  inconsistently. Restarting with `copilot --resume` makes it appear.
- `/statusline` with `ai-credits` (month) plus `ai-used` (session) -
  always-on spend visibility.
- `/context` - a per-source breakdown of what's using the context.

## One Caveat for Budgeting

Sonnet 5's $2/$10 launched as introductory pricing. On 2026-08-10
Anthropic [made it the standard price](https://platform.claude.com/docs/en/about-claude/pricing)
and dropped the rise to $3/$15 scheduled for 2026-09-01. GitHub lists it
as standard too. Nothing here needs re-costing.

## Sources

The fan-out tax, cost ratios, and runaway spiral are our own measurements. Everything else comes from:

- Usage-based billing - GitHub's [announcement](https://github.blog/news-insights/company-news/github-copilot-is-moving-to-usage-based-billing/) of token-metered credits.
- Models and pricing - GitHub's [pricing reference](https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing), for per-1M rates and the credit conversion.
- Sonnet 5 pricing - Anthropic's [pricing page](https://platform.claude.com/docs/en/about-claude/pricing) (its `#claude-sonnet-5-introductory-pricing` note) and the [launch post](https://www.anthropic.com/news/claude-sonnet-5).
- Copilot plans - GitHub's [plans page](https://github.com/features/copilot/plans) for plan prices, and its [individual billing page](https://docs.github.com/en/copilot/concepts/billing-and-usage/individuals/billing) for the base and flex split and the reset.
- Free models retired - [coverage from heise](https://www.heise.de/en/news/GitHub-removes-free-models-from-Copilot-plans-11275252.html) of the June change.
- Auto - GitHub's [Auto docs](https://docs.github.com/en/copilot/concepts/models/auto-model-selection) for the discount and routing, and its [supported models page](https://docs.github.com/en/copilot/reference/ai-models/supported-models) for the Auto pool.
- New models - GitHub's changelog posts for [Claude Opus 5.5](https://github.blog/changelog/2026-09-22-claude-opus-5-5-is-now-available-in-github-copilot) and [GPT-6 Sol and GPT-6 Luna](https://github.blog/changelog/2026-09-22-openais-gpt-6-sol-and-gpt-6-luna-now-available).
- Extended thinking - Anthropic's [extended thinking docs](https://platform.claude.com/docs/en/build-with-claude/extended-thinking) for thinking tokens billing as output. Step 5's $10/M is derived from that and Sonnet 5's output price.
- CLI command reference - GitHub's [command reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference) for `/usage`, `/context`, `--resume`, and `reasoningEffort`. Its stale eight-row "Supported models" table omits `claude-opus-5` and `gpt-5.6-luna`. Absence there proves nothing.
- Session limits - GitHub's [session-limit how-to](https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/set-session-limit) for `--max-ai-credits` and `/limits`, both soft limits in public preview.
- Settings keys - GitHub's [CLI config reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-config-dir-reference) for which keys each settings file honors.
- CLI changelog - the [Copilot CLI changelog](https://github.com/github/copilot-cli/blob/main/changelog.md) for the `none` and `minimal` effort levels (v1.0.52 and v1.0.69, confirmed in local `copilot --help`), the 30-credit floor (v1.0.67), per-model `/usage` rows (v1.0.85), the startup tier (v1.0.87), and effort on selection (v1.0.88).
- Statusline items - `ai-credits` and `ai-used` aren't in the web docs at time of writing. Only the CLI's `copilot help billing` output (CLI 1.0.70) names them.
