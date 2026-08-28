# Copilot on a Budget: Getting the Most from a Low Credit Allowance

*This page is meant as a quick reference on practical cost control for
GitHub Copilot CLI. The cost comparisons below come from our own direct
measurement. The billing rates and CLI behavior come from published
GitHub and Anthropic pages, listed under Sources at the end.*

## Where this page sits

This is the practical companion to
[the model guide](https://dougfessler.com/smartplan-plugin/copilot-model-guide.html). It tells you what to pick,
this tells you how to spend less once you have picked.

## How Copilot Billing Works (the Mental Model)

Since 2026-06-01, credits have been token-metered. 1 credit equals $0.01.
That means the 7,000-credit Pro+ monthly allowance is worth $70 of usage,
on a plan that itself costs $39 a month. Four things drive the bill, and
only four:

- Which model - Sonnet 5 runs $2/$10 per 1M in/out (see the [GitHub pricing
  table](https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing)).
  Haiku 4.5 is half of that. GPT-5 mini comes in at $0.25/$2, which makes
  it roughly 8× cheaper than Sonnet on input and 5× on output. (It used to
  be an "included" model under the old premium-request billing. Under
  credits it's metered per token like everything else.) Opus 4.8 sits at
  $5/$25. Fable/fast tops out at $10/$50.
- How much context - this is the trap. The whole context gets
  re-read every turn (cache-read, ~$0.2/M on Sonnet). A big context
  gets paid *per turn*, not once.
- How many turns - each extra round re-bills that context. There's no
  clean way to isolate the cost of a single turn. Per-session totals
  (below) are the best available scale.
- How much output - output bills ~5× input. That includes
  reasoning and thinking tokens, which bill as output too.

Rough scale: a small, clean task run entirely inline on Sonnet costs ~8.5
to 13 credits (call it ~10 on average). A real feature involving more
files and turns runs more like 20 to 50 credits. A two-file UE5 feature we
measured came in just over 19. So the 7,000 credits a month work out to
roughly 150 to 400 real tasks. That's comfortable if you avoid the
accidents below. It gets tight if you don't.

## The Levers, Ranked by Impact

1. **Don't fan out ordinary work.** Fan-out means splitting one task
   across multiple agent sessions, for example with `/fleet`. On a task
   that fits in one context, fan-out costs 2.3 to 4.2× more than doing it
   inline on one model, at identical quality. The tax runs highest on
   small, easily parallelized modules. It narrows on larger, more complex
   ones. But it rarely turns into a win below the one-context threshold.
   Fan-out only pays off for work that's genuinely bigger than one
   context, or for failure-prone work. For most tasks, one focused
   session is the cheapest option.
2. **Right-size the model. Don't leave the session on a premium one.**
   Sonnet is the floor. Drop mechanical, boilerplate, rename,
   and codemod work to GPT-5 mini. It's roughly 8× cheaper than Sonnet on
   input. On a real task, it came in at about 39% of the Haiku cost. Kimi
   K2.7 Code ($0.95/$4, the first open-weight option) is a natural A/B
   candidate for the same mechanical share of the work. One note: its
   always-on thinking bills as output. Its cache reads price at 0.2×
   input, double the usual ratio.
   (Raptor mini used to be mentioned here as a same-price alternative. It
   was never selectable in Copilot CLI, and GitHub is retiring it in favour
   of MAI-Code-1-Flash, so it's dropped rather than listed with a caveat.)
   Opus is
   worth reserving for a genuinely hard *one-shot* plan, not a whole
   session, since it runs 2.5× Sonnet per token. Fable/fast is worth it
   only for the single hardest decision.
3. **Turn on Auto for a [flat 10% discount](https://docs.github.com/en/copilot/concepts/models/auto-model-selection).**
   Auto routes each request to a model matched to the task's
   complexity. It's good for
   ordinary inline work. Pin an explicit model only when deliberately
   tiering a fan-out.
4. **Keep context small and sessions warm.** Scope the session to the
   files being changed. Don't open the whole repo or big headers. They
   get re-paid every turn. For follow-ups and fixes,
   `copilot --resume <id>` rides the *warm* cache instead of re-paying
   the cold context from scratch. We measured this at ~14k tokens for a
   bare session, and 75 to 160k with a skill tree loaded.
5. **Terse output, low effort on mechanical turns.** Use `--effort low`
   (or `none`/`minimal`) on boilerplate, since reasoning tokens are
   output-priced at $10/M on Sonnet. Don't request long explanations that
   won't be read. With named subagents, `effortLevel: low` can be pinned
   per agent under `subagents.agents.<name>` in Copilot settings so the
   mechanical ones default low without passing the flag every time.
6. **Cap the runaway tail: it's the #1 budget accident.** A single
   uncapped blind-repair spiral has burned 167 credits in one of our
   sessions. Two defenses help here. First, put `--max-ai-credits` (or
   `/limits`) on a session so a loop can't run away. Second, when a fix
   fails twice, *stop and diagnose* instead of blind-retrying. Note:
   don't cap a session that's expected to load a skill. A cap can make
   the model skip loading the skill entirely, to conserve budget. Cap the
   fan-out *leaves* (the individual units of work handed to each
   sub-agent), not a skill-driven orchestrator.
7. **Script anything deterministic.** A repeatable command sequence
   becomes a shell script. After that, it's zero model calls, forever.

## Budget Killers (the Anti-Patterns)

- Fanning out / `/fleet` on ordinary one-context tasks (a 2.3 to 4.2×
  tax).
- Leaving the session on Opus, or on Auto that picks a premium model,
  for a long grind.
- Huge context (whole repo, big engine headers) reloaded every turn.
- Blind repair loops instead of stop-and-diagnose.
- Verbose output and high effort on mechanical work.

## Watch the Meter

- `/usage` - session credits, a monthly plan bar (credits used out of
  your allowance), and an activity graph. The token breakdown (input,
  output, cached) renders inconsistently in a live session, even when
  there's spend to show. Restarting and resuming the session with
  `copilot --resume` gets it to appear. There are no per-model totals on
  AI-credits sessions.
- `/statusline` with `ai-credits` (month) plus `ai-used` (session) -
  always-on spend visibility.
- `/context` - a per-source breakdown of what is consuming the context.

## One Caveat for Budgeting

The Sonnet $2/$10 rates launched as introductory pricing, and on 2026-08-10
Anthropic [made them the standard price](https://platform.claude.com/docs/en/about-claude/pricing):
the increase to $3/$15 that had been scheduled for 2026-09-01 will not
happen. So the levers below keep exactly the value they have today rather
than getting more valuable in September, and nothing on this page needs
re-costing.

GitHub's own pricing reference still footnotes $2/$10 as promotional
through 2026-08-31. Copilot bills provider list pricing, so read that as a
stale label rather than a second schedule — but GitHub has published nothing
about its wording after that date. <!-- RECHECK:2026-09-01 -->

## Sources

The cost-comparison figures above (the fan-out tax, the model cost
ratios, the runaway-spiral example) come from our own measurement rather
than from published documentation. The rates and CLI behavior come from
these external, publicly documented sources:

- Usage-based billing announcement - the GitHub [announcement](https://github.blog/news-insights/company-news/github-copilot-is-moving-to-usage-based-billing/) of the 2026-06-01 move from premium requests to token-metered AI credits.
- Models and pricing - the GitHub [pricing reference](https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing) with the per-1M token rates for every model, the 1 credit = $0.01 conversion, and the Sonnet promo footnote.
- Claude Sonnet 5 pricing - the Anthropic [pricing page](https://platform.claude.com/docs/en/about-claude/pricing), whose note anchored at `#claude-sonnet-5-introductory-pricing` states that $2/$10 "is now the standard price" and that the $3/$15 increase scheduled for 2026-09-01 "will not occur". The [launch post](https://www.anthropic.com/news/claude-sonnet-5) is the original source of the superseded promotional framing.
- Copilot plans - the GitHub [plans page](https://github.com/features/copilot/plans) showing the monthly credit allowance on the Pro+ tier (listed there as $70 of total credits, i.e., 7,000 at $0.01 each) and the $39 monthly price. The `/usage` plan bar displays the same allowance directly as 7,000 AIC.
- Included models retired - [coverage from heise](https://www.heise.de/en/news/GitHub-removes-free-models-from-Copilot-plans-11275252.html) of the June change dropping the free fallback models, the reason GPT-5 mini is no longer described as "included" above.
- Auto model selection - the GitHub [Auto docs](https://docs.github.com/en/copilot/concepts/models/auto-model-selection) with the 10% paid-plan discount and the per-request routing by task complexity.
- Extended thinking billing - the Anthropic [extended thinking docs](https://platform.claude.com/docs/en/build-with-claude/extended-thinking) confirming that thinking tokens bill as part of the output token count.
- CLI command reference - the GitHub [command reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference) for `/usage`, `/context`, and `--resume`. Note that the `/usage` description there promises per-model token totals, which AI-credits sessions don't display. The built-in `copilot help billing` output describes what actually appears: credits, token breakdown, and limit progress.
- Session limits - the GitHub [session-limit how-to](https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/set-session-limit) for `--max-ai-credits` and `/limits`. Note that these are soft limits, currently in public preview.
- Reasoning effort levels - the [Copilot CLI changelog](https://github.com/github/copilot-cli/blob/main/changelog.md) (v1.0.52 and v1.0.69) for the `none` and `minimal` effort options, confirmed against the local `copilot --help`. The web reference lags behind here. Some levels are also gated by model capability.
- Per-subagent effort pins - `subagents.agents.<name>` with `effortLevel` in `.github/copilot/settings.json` isn't in the web docs either. It comes from CLI v1.0.70 and was verified locally on 2026-07-13. The claim that reasoning tokens bill at the output rate is the Anthropic extended-thinking behaviour cited above, applied to Sonnet 5's $10/M output rate from the pricing reference, so the $10/M figure in step 5 is those two sources multiplied out rather than a separately published number.
- Statusline items - the `ai-credits` and `ai-used` options aren't in the web docs at time of writing. They come from the `copilot help billing` output built into the CLI (CLI 1.0.70), which is the only GitHub-authored documentation naming them.
