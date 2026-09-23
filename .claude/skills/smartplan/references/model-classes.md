# Model classes — the hand-editable classification registry

*The single source of truth for which model belongs to which capability
class. **Edit this file by hand to reclassify a model** — the policy files
(`flow.md`, `routing.md`, `check.md`) read classes and point here; they
never carry their own rosters. Seat rules live in `routing.md` § Seat
eligibility; this file only answers "who is in each class."*

## Contents

- How to edit
- The classes
- The registry
- Notes

## How to edit

- **Add a model:** one row in the registry below. Classify by published
  price + benchmarks (the § Seat eligibility step-1 procedure) — if either
  is missing, mark Status `provisional` and route work to it only as a
  deliberate, outcome-watched trial — never as a default. A newer version
  of a line that already holds a seat skips that wait (newest version
  first, below), and so does a row the author seats.
- **Move a model between classes:** change its Class cell and date the Note.
  Moving a model *up* (e.g. Mechanical → Implementer) is cheap to be wrong
  about (work costs more); moving one *down* is not (silent failures) — a
  down-move should cite observed evidence (a bounce rate below the ~20–30%
  breakeven) or a benchmark, not a hunch.
- **Newest version first, always** (author rule, 2026-09-22). A model
  line is one name across version numbers: Opus 5 and Opus 5.5, GPT-5.6
  Luna and GPT-6 Luna. When a newer version lands in this registry it
  takes every seat and dispatch its line holds, as soon as the harness
  serves it. No Legacy notice, board result or trial comes first. A
  pricier successor moves too, with the price change dated in its Note.
  On an ordered `models:` list the newest version leads and the previous
  one stays behind it as the fallback, so a build or plan that can't reach
  it falls through. Family aliases (`opus`, `sonnet`, `haiku`) resolve to
  the newest version wherever the provider follows Anthropic's alias, so
  keep a seat on one where the harness offers it. Where an alias lags,
  point it at the newest id. A repo gate fails any seat that leads a
  line with an older version. To hold a newer version back, mark its row
  `not a seat` with a dated reason.
- **Keep prices dated.** Prices move; a dated wrong price beats an undated
  one because it tells the reader when to stop trusting it. Root
  the development repo's claim ledger carries the source checks.

## The classes

| Class | Ladder tiers | Holds these seats | Never |
| --- | --- | --- | --- |
| **Reasoning** | Max · Strong | Planner · verifier of Mid/Strong leaves · escalation reserve · irreducibly cross-cutting leaves | First-pass implementation, mechanical work, scouting |
| **Implementer** | Mid | Implementer floor (briefed/correctness-sensitive) · verifier of Cheap leaves · small-plan planner (drop-on-fit) | Planning beyond drop-on-fit; mechanical leaves when a Mechanical-class model is available (Copilot exception from 2026-09-07: the Luna rows hold the Cheap coding and scout seats on price, GPT-6 Luna listed first from 2026-09-22, see their rows) |
| **Mechanical** | Cheap | Mechanical, single-concern, verifier-checkable leaves via smartexec + smartcheck · scouting (Haiku 4.5, or a Luna row on Copilot by the Implementer exception) | Planning, verification (except fully scripted checks), correctness-sensitive leaves |
| **Script** | Script | Deterministic actions an existing script performs — zero model calls | Anything needing judgment |

## The registry

One row per model. Benchmark cells are vendor/system-card numbers unless
labeled otherwise — the official boards (swebench.com, Scale, tbench.ai)
run different harnesses and score lower across the board. Scale still
lists few of these models, while Terminal-Bench 4.0 and vals.ai now cover
most of them (re-checked 2026-09-15). Compare within one source class.
`Status`: **default** (a seat's standing pick),
**active** (eligible, routinely used), **candidate** (eligible,
trialed deliberately before any floor moves), **provisional** (classified on
incomplete data — price-only or single benchmark), **planner-only** (never
implements or verifies). Two more values are in use on rows below:
**retiring** / **retired** (a dated vendor notice, with the harness named)
and **not a seat** (carried for lineup or board literacy, never dispatched).
A parenthetical scopes any of them. A row nobody has classified keeps
Class `Unclassified`.

| Model | Class | Price $/1M in/out | Key benchmark | Status | Classified | Note |
| --- | --- | --- | --- | --- | --- | --- |
| Fable 5.1 | Reasoning | 10 / 50 (5m write 12.50, 1h write 20, **cache-read 0.25 = 0.025×**, batch 5 / 25) | **Terminal-Bench 4.0 #2 at 57.9% ± 3.8%** ($6.2k, official board, read 2026-09-15, unchanged 2026-09-22), absent from Scale and the archived vals.ai SWE-V board · vals.ai Terminal-Bench 4.0 49.49 ± 3.07 blended, 42.42 on its own attempts (28 of 198 served by Opus 5) · AA Intelligence Index v4.3.2 53 (max with fallback), joint 4th with GPT-6 Astra behind three Opus 5.5 rows (read 2026-09-22) · Copilot's picker lists `claude-fable-5.1` (roster read 2026-09-02) | planner-only | 2026-09-07 | Read first-hand at platform.claude.com (pricing + models overview) 2026-09-07: current lineup, and Fable 5 moved to Legacy on the same read. API id `claude-fable-5-1`, adaptive thinking always on, default effort high, 1M ctx / 128K out, retire not before 2027-09-01. Same Max-tier rules as Fable 5: planning only, never a verifier, never a fail-twice target. **The cache-read price was the seat fact against Opus 5:** 0.25/MTok is half Opus 5's 0.50. So a turn that is mostly cached re-read (an orchestrator waking on a subagent completion) costs less on Fable 5.1 than on Opus 5 once the cached prefix exceeds roughly 20× the turn's new input plus 100× its output, about 140K tokens at 2K in / 1K out. **Against the current Opus the crossover is gone:** Opus 5.5 reads cache at 0.20 (2026-09-22), under Fable 5.1 on every axis. No orchestration shape makes Fable 5.1 the cheaper seat now. **Seat facts from the what's-new page (read 2026-09-15):** forced `tool_choice` (`any`, or a named tool) returns a 400, its thinking blocks can't be read by any model but Mythos 5.1, Opus 5.5 included, and drop silently on a fallback (permitted targets are Opus 4.8 and Opus 5), and it may make one tool call per turn where Fable 5 batched several. So an orchestrator on this seat can serialize a wave's dispatches unless the brief asks it to batch. Effort defaults to high in Claude Code, medium on claude.ai and Cowork <!-- claim:fable-5-1-price --> |
| Fable 5 | Reasoning | 10 / 50 | TB2.1 83.8 — #1 on the official board (re-confirmed 2026-07-24) · vendor SWE-Pro 80.3 · vals.ai TB4 22.73 blended, 16.67 on its own attempts (51 of 198 served by Opus 4.8, read 2026-09-22) | planner-only (legacy fallback) | 2026-07 · benchmarked 2026-07-20 | Max tier: hardest architecture/decomposition decisions only; never a fail-twice target, never a verifier **Legacy as of 2026-09-07** (models overview, read first-hand): Fable 5.1 is the current Max-tier row; this one stays as the same-price fallback. |
| Mythos 5 | Reasoning | 10 / 50 (cache-read 1.00; 5m write 12.50, 1h write 20; batch 5 / 25) | none on a coding board, absent from every board this file tracks. Anthropic's only published figure found is USAMO 2026 99.8% (vendor, Sonnet 5 System Card §8.6), a math eval that says nothing about coding | **not a seat — limited availability** | 2026-08-28 | Added 2026-08-28 after a sweep found the pricing page carries it and this registry did not, in a file whose own summary line then claimed to give the Anthropic lineup strongest to cheapest. Priced identically to Fable 5 on every axis including cache and batch. Gated behind a limited-availability programme rather than generally callable, so it is carried for lineup completeness, not as a candidate — the same reasoning that added the DeepSeek row. Uses the newer tokenizer (~30% more tokens for the same text), the same one Fable 5 uses, so its effective cost matches Fable 5's and sits about 30% above an old-tokenizer model at the same list rate. `caching.md`'s minimum-cacheable-prefix table already knew about it, which is how the gap showed. Superseded by Mythos 5.1 (2026-09-01), and still listed on the pricing page |
| Mythos 5.1 | Reasoning | 10 / 50 (cache-read 0.25 = 0.025×; 5m write 12.50, 1h write 20; batch 5 / 25) | none published | **not a seat (invite only, Project Glasswing)** | 2026-09-15 | Released 2026-09-01 as Mythos 5's successor, API id `claude-mythos-5-1`. Anthropic states it is the same model as Fable 5.1 with different safeguards, sharing its specs and pricing, and retire not before 2027-09-01. Carried for lineup completeness, the same reasoning that carries the Mythos 5 row. Its cache-read is 0.025× base input like Fable 5.1's. Those two and Opus 5.5 (0.05×) are the only Anthropic rows off the roster's usual 0.1× |
| Claude Opus 5.5 | Reasoning | 4 / 20 (5m write 5, 1h write 8, **cache-read 0.20 = 0.05×**, batch 2 / 10 and fast mode 8 / 40, both Claude API only) | **No official-board row yet** (tbench.ai, read 2026-09-22 about 21:00 UTC). Independent: **AA Intelligence Index v4.3.2 58 (max with fallback), #1 overall**, and 51 at its default medium against Opus 5's 45 at medium · vals.ai Terminal-Bench 4.0 **61.62 ± 1.01, #1 on that board** (Terminus 2, avg@3). Counting its 30 fallback-served attempts as failures drops it to 53.54, second to GPT-6 Astra's 57.07 · AA's own TB4 run 59.6%, tied with GPT-6 Astra. Vendor (system card, safeguards on): SWE-bench Pro 89.9 against Opus 5's 79.2, Terminal-Bench 4.0 66.4% (xhigh) | **default (planner + Strong verifier), from 2026-09-22** · first in the Copilot planner and Reserve `models:` lists, ahead of Opus 5 | 2026-09-22 | Released 2026-09-22, API id `claude-opus-5-5` (Bedrock adds an `anthropic.` prefix), 1M ctx / 128K out, knowledge cutoff June 2026, retire not before 2027-09-22. **Promoted as the newest Opus under § How to edit, not on benchmarks.** It's also the same class, 20% under Opus 5 on input and output and 60% under on cache-read, and the vendor's recommended starting model, and Opus 5 moved to Legacy the same day. The independent boards point the same way. Anthropic's own claim (vendor): 40% cheaper per typical task than Opus 5 at default settings, and over 30% faster output. In Claude Code (v2.1.280+) it is `default` on every paid plan, Pro and Team Standard included. `opus` resolves to it on the Anthropic API, Claude Platform on AWS, Bedrock, and Google Cloud, while Foundry keeps `opus` on Opus 4.6 and a Sonnet 4.5 default (model-config docs, read 2026-09-22). **Effort defaults to medium**, one notch under Opus 5's high. Thinking can't be disabled at any effort (a 400). At a given level it thinks more per turn than Opus 5, most at xhigh and max. Re-budget `max_tokens` upward before porting a seat. Per task it still ran cheaper than Opus 5 at matching effort on AA's index, at every level but max (read 2026-09-22). Forced `tool_choice` returns a 400, as on Fable 5.1. Only Fable 5.1 and Mythos 5.1 read its thinking blocks. An escalation or fallback off it drops them silently. Safety classifiers: biology and frontier-LLM-development flags fall back to Opus 5 and cybersecurity flags to Opus 4.8. `reasoning_extraction` refuses with no fallback. vals.ai logged 30 of 198 TB4 tasks served by a fallback model. Every Opus 5.5 board score is blended. Copilot: GA 2026-09-22 on Pro+ and up, billed at this list rate with no fast SKU, not in Auto. In GitHub's early testing it matched Opus 5 in significantly fewer steps and tokens. Its slug `claude-opus-5.5` is in `copilot help config` from prerelease 1.0.89-0 (2026-09-22T22:08Z), not stable 1.0.88. The Copilot planner and Reserve seats list it ahead of an Opus 5 fallback. A stable build lands on Opus 5. Anthropic says Sonnet 5.5 and Haiku 5.5 "will follow in the coming weeks" <!-- claim:opus-5-5-price --> |
| Claude Opus 5 | Reasoning | 5 / 25 (cache-read 0.50, 5m write 6.25, batch 2.50 / 12.50) | **vals.ai SWE-bench Verified 97.0, rank 1** (board updated 2026-08-05, re-read 2026-08-06, ahead of GPT-5.6 Sol 96.2 and Fable 5 95.0; the board archived 2026-09-21, so the figure is frozen); **Terminal-Bench 4.0 shows it at 53.9% ± 3.2% (xhigh), #3 behind GPT-6 Astra and Fable 5.1, $6.1k.** The xhigh row came from a 2026-09-17 effort sweep. The default table shows each model's best row. Its (max) row, 51.8% ± 3.4%, is still in the board's data (read 2026-09-22). Quote the effort label with the score · AA Intelligence Index v4.3.2 51 (max) | active (Legacy since 2026-09-22, the pricier fallback) · the Copilot planner and Reserve `model:` pin, behind `claude-opus-5.5` in their `models:` lists | 2026-07-25 · promoted 2026-08-05 · default handed to Opus 5.5 2026-09-22 | Held the planner + Strong verifier default from 2026-08-05 to 2026-09-22. It was promoted then on price parity and vendor default: same class, same price as Opus 4.8, and no benchmarks yet. **Legacy from 2026-09-22** on the models overview, still Active in the deprecations table, retire not before 2027-07-24. It now lists 25% above Opus 5.5 on input and output and 2.5× on cache-read. A fallback onto it is a climb in price, which `routing.md` § The cost ceiling treats as one. `opus` resolves to Opus 5.5 wherever a harness follows Anthropic's alias. Select this one by its full id `claude-opus-5`. Copilot CLI-selectable since v1.0.75 (Pro+/Max-gated), still GA there with no retirement notice. T30 (07-25) saw it serve where 4.8 was Pro-gate-refused on 07-11. **Fast mode (research preview) re-prices it 10 / 50** on the Claude API only, read 2026-09-20, the same price as the Opus 4.8 fast row `copilot.md` carries. Copilot has no Opus 5 fast SKU |
| Opus 4.8 | Reasoning | 5 / 25 | **vals.ai SWE-V 88.6** confirmed (read first-hand from the board's own data 2026-08-23) — note the board carries a SECOND row under the identical label, `claude-opus-4-8-claude-code` at 85.8 · SWE-bench Pro 69.2 **(vendor — absent from Scale's public board, checked 2026-08-12)** · SWE-bench Verified 88.6 · TB2.1 78.9 — official board #5 (2026-07-24) · AA Intelligence Index v4.3.2 41.79 (max, read 2026-09-22) | active (Legacy, second fallback) | 2026-07-09 · demoted from default 2026-08-05 | Held the planner + Strong verifier default 07-09 → 08-05 on price + SWE-bench (GPT-5.5 edges it on TB2.1, 83.1 vs 78.9, but is Pro-gated and pricier on output). **Succession resolved 2026-08-05:** Opus 5 takes the default at identical price. 4.8 stays Active and costs the same as Opus 5. So it's the drop-in fallback when an Opus 5 seat is unavailable. Since 2026-09-22 both sit 25% above the Opus 5.5 default. Opus 5.5's cybersecurity safety fallback lands here. Retire not before 2027-05-28. Fast mode (preview) re-prices it 10 / 50 with cache-read 1 and write 12.50, the figures `copilot.md` carries (re-read 2026-09-20) |
| GPT-5.5 | Reasoning | 5 / 30 (>272K: 10 / 45) | **vals.ai SWE-V 82.6** (read first-hand from the board's own data 2026-08-23) — the board carries two more rows under the same display label, codex 76.4 and factory 76.2 · SWE-bench Pro 58.6 **(vendor — absent from Scale's public board, checked 2026-08-12)** · TB2.1 83.1 — official board #2 (2026-07-24) | not a seat (Pro+-gated on Copilot), retiring from Copilot 2026-10-19 (changelog 2026-09-18), successor GPT-5.6 Sol (Pro+-gated) | 2026-07-09 · refined 2026-07-20 · retiring noted 2026-09-21 | **Refined 2026-07-20 (supported-models):** still GA and CLI-selectable, but Pro = Not included — which is why T18's Pro-roster observation missed it. (Re-derived 2026-09-15 from github/docs `model-supported-plans.yml`: `pro: false`, with Pro+, Max, Business and Enterprise true.) Flagship-superseded by the GPT-5.6 family, and then by GPT-6 Astra (GA on Copilot 2026-09-04). On Pro the live cross-family peer is GPT-5.6 Terra. **Leaves Copilot entirely 2026-10-19, all plans** (changelog 2026-09-18, refute-verified 2026-09-20), so its Codex-side exit on 2026-10-14 lands the same week |
| GPT-6 Astra | Reasoning | 10 / 50 (cache-read 1.00, write 12.50 · >272K: 20 / 75 on the WHOLE request · Batch and Flex 5 / 25, Fast mode 20 / 100, where Copilot bills Standard) | **Terminal-Bench 4.0 #1 at 58.2% ± 2.8%** ($3.3k, official board, read 2026-09-15, unchanged 2026-09-22) · vals.ai Terminal-Bench 4.0 57.07 ± 3.07 · AA Intelligence Index v4.3.2 53 (max), joint 4th with Fable 5.1 behind three Opus 5.5 rows (read 2026-09-22) · absent from Scale and the archived vals.ai SWE-V board · vendor (launch post, max at any effort): Terminal-Bench 4.0 57.9%, DeepSWE v1.1 74.1%, FrontierCode 1.1 Main 53.3% | provisional, no seat (2026-09-22 seat review) · Copilot GA 2026-09-04, Pro+-gated | 2026-09-15 | OpenAI's new flagship, released 2026-09-03 and GA on Copilot 2026-09-04 for Pro+, Max, Business and Enterprise, not plain Pro. 1.05M ctx (922K max input) / 128K out, effort low to max. It joined Copilot's Auto pool with the 2026-09-16 docs change (every Auto surface, CLI included). On Pro+ and up, Auto can now route a hard prompt to a 10 / 50 model. CLI support landed in 1.0.85. Priced at Fable 5's list rate on both axes while costing half as much per board run ($3.3k against $6.2k). **No seat, per the 2026-09-22 seat review at the author's direction:** Opus 5.5 lists cheaper (4 / 20 against 10 / 50) and scores higher on AA (58 against 53) and on vals.ai TB4 blended (61.62 against 57.07). On Opus 5.5's own vals.ai attempts (53.54) Astra leads. That board's half of the case rests on a blended score |
| GPT-5.6 Cyber | Unclassified | 12.50 / 75 | none published | **not a seat — surfaced via a Daybreak alias, not on the Copilot roster** | 2026-09-20 | Surfaced on OpenAI's own pages 2026-09-20 with no registry row: the GPT-5.6 family's cybersecurity variant, priced above every other family row on input. Not Copilot-dispatchable and no coding board entry, so it is carried for price literacy only, the DeepSeek row's reasoning |
| GPT-5.6 Sol | Reasoning | **4 / 20** (cache-read 0.40, write 5.00 · >272K: 8 / 30 at cache-read 0.80, write 10.00) — GitHub dropped the promo footnote after 2026-09-03 and its table prints the standard rate (read 2026-09-15). **OpenAI prints the same 4 / 20** and calls that rate itself promotional "at least through November 21, 2026". The 2 / 10 on OpenAI's pricing page is the Batch and Flex row. Both vendors bill 4 / 20 (re-read 2026-09-22). OpenAI's 2026-08-21 changelog calls 4 / 20 a 20% input and 33% output cut, which implies a prior 5 / 30. No page prints a post-promo rate. Past 272K bills the **WHOLE request** at 2× input / 1.5× output — a cliff, not a marginal tier (model page) | **Terminal-Bench 4.0 #7 at 37.3% ± 3.8%** (re-read 2026-09-22, #6 on 2026-09-15 before Grok 4.7 entered, #4 on the 2026-09-02 read), so the vendor-only/absent framing that applied on TB2.1 is retired; the older 88.8 was a TB2.1 vendor figure; vals.ai SWE-V 96.2 (independent, not the official board) · vals.ai TB4 27.78 ± 1.82, 6th of 32, with 7 provider refusals scored as failures · AA Intelligence Index v4.3.2 46.97 (max), AA's own TB4 run 39.9% (read 2026-09-22) | provisional (Copilot-exposed) | 2026-07-09 (GA day) · re-researched 2026-07-20 | Pro+-gated. Elite agentic scores but measured weak on open-brief architecture (Every 56/100 vs Fable 90) and METR's highest eval-gaming rate — never grades work against visible tests; not a planner swap. Full caution set: the model guide. OpenAI names GPT-6 Sol its successor at 2 / 10 (2026-09-22) but keeps GPT-5.6 available and un-deprecated. § How to edit's newest-version rule puts GPT-6 Sol ahead of it. No seat pins GPT-5.6 Sol. The Copilot Mid seat lists its successor first |
| GPT-6 Sol | Implementer (provisional) | **2 / 10** (cache-read 0.20, write 2.50 · >272K: 4 / 15 on the WHOLE request, cache-read 0.40) · OpenAI and GitHub agree · Batch and Flex 1 / 5, Fast mode 4 / 20, where Copilot bills Standard | absent from tbench.ai and vals.ai TB4 (read 2026-09-22) · **AA's own TB4 run 43.9% (max)**, against GPT-5.6 Sol's 39.9% · AA Intelligence Index v4.3.2 48 (max), 47.53 against GPT-5.6 Sol's 46.97, at $1.06 per index task against $1.99 · vendor: DeepSWE v1.1 68.8% (max), FrontierCode 1.1 49.3% (max) | provisional · **first in the Copilot Mid seat's `models:` list from 2026-09-22** (author direction, untrialed, Sonnet 5 behind it) · Copilot GA 2026-09-22, Pro+-gated, not in Auto | 2026-09-22 | Released 2026-09-22 as GPT-5.6 Sol's successor at half its price, API id `gpt-6-sol`, 1.05M ctx (922K max input) / 128K out, effort none to max (default medium). It takes the "balance intelligence and cost" slot GPT-5.6 Terra held. There is no GPT-6 Terra. **Seated at the author's direction 2026-09-22** ("GPT models should be prioritized based on what they are good at due to the discount"): it heads `@smartplan-implementer`'s `models:` list ahead of Sonnet 5, at the same 2 / 10. The Mid seat is an author move across model lines, which § How to edit's newest-version rule doesn't cover. Within the Sol line that rule puts it first. **Class moved from Reasoning to Implementer the same day.** That keeps the Mid seat consistent with § The classes. The down-move rests on boards, not a trial. AA puts it at 48 against Sonnet 5's 38. Its predecessor leads Sonnet 5 on every board both sit on (tbench.ai TB4 37.3% against 12.4%, vals.ai TB4 27.8 against 8.08, vals.ai SWE-V 96.2 against 79.6). It's Pro+/Max/Business/Enterprise only. Plain Pro lands on Sonnet 5. No CLI build names a `gpt-6-sol` slug yet. Today every plan lands on Sonnet 5. The ordered fall-through is untested here, since this account is on Copilot Free. METR's eval-gaming caution on GPT-5.6 Sol doesn't transfer automatically. OpenAI's own card reports far less coding misrepresentation than its predecessor |
| Gemini 3.1 Pro | Reasoning | 2 / 12 (>200K: 4 / 18) | **vals.ai SWE-V 78.8** (read first-hand from the board's own data 2026-08-23) (row `Gemini 3.1 Pro Preview (02/26)`) · SWE-bench Pro **46.1, rank 5 (Scale public board)** · TB2.1 65.8 — official board **rank 14**, tied with Gemini 3 Pro also at 14, next row skips to 16 (re-read 2026-08-12) | **RETIRED from Copilot 2026-09-01 (roster read 2026-09-02) — seat handed to Gemini 3.6 Flash** | 2026-07-12 · corrected 2026-08-12 | **MEASURED (T18): ties GPT-5.6 Terra on seeded C++ recall (14/15 each over 2 fixtures) at 47% the cost (8.69 vs 18.53 cr), esp. UE5.** **Two corrections from the 2026-08-12 board re-read:** the old "SWE-bench Pro 54.2" appears nowhere on Scale's board (which says 46.1) and was an unlabelled vendor figure reading as board-sourced; and the TB2.1 rank is 14, not 15 — this file's own 2026-07-20 ledger row had it right and the 2026-08-06 pass introduced the error. **The cost case needs re-measuring:** Terra repriced to an identical 2 / 12, so this seat's list-price advantage over Terra is gone. Slug `gemini-3.1-pro-preview`. Never a planner swap. **Seat vacated 2026-08-16:** Copilot retired this model 2026-09-01 and T34 (2026-08-05) cleared Gemini 3.6 Flash as the successor at 8/8 recall on the seeded custom fixture, cost indistinguishable. All routing sites (`check.md`, `cpp-gamedev-check.md`, `copilot.md`, the Copilot verifier seat) now name 3.6 Flash. The Gemini API and other harnesses are unaffected by the Copilot retirement date. Added 2026-08-31: GitHub's roster listed it as **Public preview, never GA** — the only non-Anthropic model on the 31-row roster in that state, retired straight out of preview, which contextualizes why the seat went to a GA model (3.6 Flash) rather than a same-model upgrade |
| Sonnet 5 | Implementer | 2 / 10 | **vals.ai SWE-V 79.6** (read first-hand from the board's own data 2026-08-23) — correcting **85.2**, which appears nowhere on that board for Sonnet 5 in any subset, and which is a vendor system-card figure (Sonnet 5 System Card §8.2, read 2026-09-15) rather than a board placement · TB2.1 74.6 — official board #10 (2026-07-24) · AA Intelligence Index v4.3.2 38 (max) · vals.ai TB4 8.08, which scores its 7 provider refusals as failures (both read 2026-09-22) | default (implementer floor + Cheap-leaf verifier) · on Copilot the Mid seat's `model:` fallback behind GPT-6 Sol from 2026-09-22, and what every plan lands on until a `gpt-6-sol` slug ships | 2026-07-09 · repriced 2026-08-12 | ~9 pts behind Opus 4.8 on vals.ai SWE-V (79.6 vs 88.6), ~17 behind Opus 5 — the floor argument. Active (latest), retire not before 2027-06-30, 1M ctx / 128K out, default effort high (read 2026-09-22). **The $2/$10 introductory rate became Anthropic's standard price on 2026-08-10**; the 2026-09-01 step to $3/$15 was cancelled and will not occur. GitHub's billing page dropped the promotional footnote by 2026-08-31, so the $2/$10 now reads unqualified standard on both vendors <!-- claim:sonnet5-standard-price --> |
| Grok 4.5 | Implementer | 2 / 6 · **past 200K bills 4 / 12 on the WHOLE request** (a cliff, not a marginal tier) · cached in 0.50 (1.00 long tier) | Terminal-Bench 2.1 **rank 4, 79.3%** (read 2026-08-14) — above Opus 4.8's 78.9 at a fifth of Opus's output price · vals.ai SWE-bench Verified 86.60 (score re-read 2026-09-15) · vals.ai TB4 6.57 (read 2026-09-22) | candidate, retiring from Copilot 2026-10-19 (changelog 2026-09-18), successor Grok 4.6 | 2026-08-14 · retiring noted 2026-09-21 | GA on Copilot since **2026-07-28**, every paid plan **including plain Pro**. Billing: input and output match xAI list, but **cached input does not** — GitHub bills 4.5 at 0.50 / 1.00 against xAI list 0.30 / 0.60, while 4.6 matches at both sources (re-read 2026-08-31), so this row's cache figures are what a Copilot dispatch pays, not xAI list. 500K native; the picker read 328K on 2026-08-06 and GitHub publishes no per-model picker cap, so the two numbers measure different things. xAI runs these directly with no logging, no disk write and no retention of any kind — stricter than Fable 5's 30-day safety-classifier retention. On Business/Enterprise it follows the default-on model policy in force since the 2026-08-26 to 09-01 rollout, unless an admin turned the global default off. **Boards put it in Reasoning territory at an Implementer price**, which is the shape that earns a deliberate trial, not a default. **Retiring 2026-10-19** (changelog 2026-09-18, refute-verified 2026-09-20): a same-price sideways move to 4.6, which stays on every paid plan |
| Grok 4.6 | Implementer | 2 / 6 · past 200K 4 / 12 whole-request · cached in 0.50 (1.00 long tier) | vals.ai SWE-bench Verified **95.60** (entered 2026-08-12, score unmoved on the 2026-09-15 re-read; the board archived 2026-09-21, so the figure is frozen) · **AA Intelligence Index v4.3.2 44 at `high`** (read 2026-09-21), level with Kimi K3's 44 · **Terminal-Bench 4.0 #10 at 20.3% ± 3.1%** (official board, re-read 2026-09-21) · vals.ai TB4 17.17 (read 2026-09-22) · Terminal-Bench 3.0 rank 4, 26.5% — TB3.0 is a THIRD board, hosted off-site at frontierbench.ai, not comparable to 2.0 or 2.1 | candidate | 2026-08-14 | GA on Copilot **2026-08-14**, same plans and billing as 4.5. Listed in Copilot's picker 2026-09-02 (CLI 1.0.81, Pro account), context cap not recorded. No build's static catalog or `copilot help config` has named `grok-4.6` (1.0.79 through 1.0.89-0). It reached the picker from the server. A slug missing from help config isn't proven unusable. Remaining scores (CursorBench 69.9, DeepSWE 65.9) are **xAI self-reported**, not independent. Grok 4.7 shipped same-price on 2026-09-21 and holds the family's newest row. 4.6 keeps this row. No seat holds a Grok, so nothing moves |
| Grok 4.7 | Implementer | 2 / 6 · past 200K 4 / 12 whole-request · cached in 0.50 (1.00 long tier) — identical to 4.5 and 4.6 on every axis (models-and-pricing.yml + xAI models page, read 2026-09-21) | **Terminal-Bench 4.0 #6 at 37.6% ± 3.5%** (official board, model release date 2026-09-21, the day it shipped and was read, $3.7k partial cost over 324 of 330 trials, agent Grok Build) · vals.ai TB4 28.28 ± 1.34, 5th of 32 (read 2026-09-22) · AA Intelligence Index v4.3.2 46 (xhigh and high, read 2026-09-22) · no vals.ai SWE-V entry, since that board archived 2026-09-21 | candidate (Copilot GA 2026-09-21, gradual rollout) | 2026-09-21 | Shipped into Copilot the same day it hit the TB board (changelog "Grok 4.7 is now available in GitHub Copilot", every paid plan including plain Pro, billed at provider list pricing). A #6 board entry above GPT-5.6 Sol at the same 2 / 6 as 4.6 is the deliberate-trial shape, not a seat move: no Copilot seat is pinned to a Grok today, and the 09-20 sweep had not read a single 4.7 fact before this. tbench.ai, vals.ai TB4 and AA are its independent numbers. xAI lists 500K ctx, text and image in, effort low to xhigh (default high) and a May 2026 knowledge cutoff (read 2026-09-22) |
| GPT-5.4 | Implementer | 2.50 / 15 (>272K: 5 / 22.50) | **vals.ai SWE-V 78.2** (read first-hand from the board's own data 2026-08-23) (row `GPT 5.4 (xhigh)`) · SWE-Pro public board 59.1 — co-#1 at xHigh effort (Scale, 2026-07-20) · Epoch SWE-V 76.9 | active (diversity verifier for non-OpenAI Cheap executors), retiring from Copilot 2026-10-19 (changelog 2026-09-18), successor named GPT-5.6 Sol (Pro+-gated) | 2026-07-09 · benchmarked 2026-07-20 · retiring noted 2026-09-21 | Named in check.md's Family decorrelation, but barred while an OpenAI model holds the Copilot Cheap seat (a Luna row, from 2026-09-07). The board scores back the seat, not the pairing. **Retiring 2026-10-19** (changelog 2026-09-18, refute-verified 2026-09-20). The notice names Sol as successor, but Sol is Pro+-gated, so plain Pro loses this row's OpenAI diversity option outright: after 2026-10-19 the plain-Pro cross-family verifier picks are Gemini 3.8 Flash and Grok 4.7 |
| GPT-5.3-Codex | Implementer | 1.75 / 14 (cache-read 0.175) | vals.ai SWE-V 78.0 (independent, read 2026-09-15) | provisional (Copilot roster GA) | 2026-08-31 | On GitHub's supported-models table with no row here, added on the same coverage reasoning as DeepSeek — but unlike DeepSeek, this one is dispatchable. No vendor benchmark, and a single independent board read (vals.ai SWE-V 78.0, 2026-09-15) is not a classification, so provisional and never a floor without a trial |
| GPT-5.4 mini | Mechanical | 0.75 / 4.50 (cache-read 0.075) | vals.ai SWE-V 73.0 (independent, read 2026-09-15) | provisional (Copilot roster GA), retiring from Copilot 2026-10-19 (changelog 2026-09-18), successor GPT-5.6 Luna | 2026-08-31 · retiring noted 2026-09-21 | Matches Gemini 3.6 Flash on input and cache-read but costs 4.50 out against 3.75. Its exact price twin was the now-retired MAI-Code-1-Flash. Classify provisional and trial before any floor move. **Retiring 2026-10-19** (changelog 2026-09-18, refute-verified 2026-09-20); Luna is the named successor and already holds the Copilot Cheap seat |
| GPT-5.4 nano | Mechanical | 0.20 / 1.25 (cache-read 0.02) | vals.ai SWE-V 69.8 (independent, read 2026-09-15) | provisional (Copilot roster GA) | 2026-08-31 | Undercuts GPT-5 mini on both axes and ties GPT-5.6 Luna's cache-read, while Luna keeps the cheaper output (1.20 vs 1.25). GPT-6 Luna (0.10 / 0.50, 2026-09-22) now undercuts both on every axis. Its 69.8 sits above Haiku 4.5's 66.6 at a fifth of Haiku's input price |
| GLM-5.3 | Implementer | 1.40 / 4.40 (cache-read 0.26 — a 0.19× ratio; cache storage limited-time free) | AA Intelligence Index v4.3.2 **45 (max), #2 open-weights of 68 (168 models total), one behind MiMo-V2.6-Pro (46), one above Kimi K3** (read 2026-09-21) · vendor card: CyberGym 84.5% ahead of Mythos 5 (83.8) and GPT-5.6 Sol (83.6), TB3.0 4.6→28.3 SOTA-open, +50% over GLM-5.2 on Z.ai Code Bench · **vals.ai SWE-V 95.4** (independent, read 2026-09-15; board now archived) · **Terminal-Bench 4.0 #5 at 41.8% ± 3.2%** (official board, re-read 2026-09-21) · vals.ai TB4 25.25 ± 1.34 (read 2026-09-22) | candidate | 2026-08-31 | Z.ai flagship since 2026-08-14 (Z.ai's API release notes date it 2026-08-18), same base model as GLM-5.2 with post-training gains; 753B / 40B active, 1M ctx / 128K out, text-only input, reasoning always on (low/high/max — **cannot be disabled**). Priced below Sonnet 5 on both axes. Z.ai's flagship, and ZCode's native model. Plan credit multiplier 6.9/1.7/24. Top-of-open-weights at an Implementer price is the Grok 4.5 shape: deliberate trial, T-record before any floor move |
| GLM-5.2 | Implementer | 1.40 / 4.40 (cache-read 0.26) — identical to GLM-5.3 and GLM-5.1 | vals.ai SWE-V 82.8 (independent, read 2026-09-15) · TB2.1 81.0 vendor ("within a few points of Claude Opus 4.8 at 85.0") · AA Intelligence Index v4.3 **34 (max)**, still on the open-weights table (read 2026-09-15) — the 2026-08-31 "delisted" read had matched only the top-12 chart | active (API-distinct only) | 2026-08-31 | Previous flagship, 753B, 1M ctx / 128K out. **On current GLM Coding Plans, requests for GLM-5.2 and GLM-5.1 auto-route to GLM-5.3, and GLM-4.7 to GLM-5.3-Flash** (devpack overview, read 2026-08-31, re-read 2026-09-15), so the model is distinct only on the API. A pinned slot still naming it silently serves 5.3 on the plan |
| GPT-5.6 Terra | Reasoning | **2 / 12** (cache-read 0.20; >272K: 4 / 18) | **vals.ai SWE-V 95.4** (read first-hand from the board's own data 2026-08-23), fourth on the Copilot roster behind Opus 5, Sol and Grok 4.6 — this file had NO vals.ai figure for it · TB2.1 78.4 — official board, rank 6 (first published numbers, 2026-07-20; vendor SWE-Pro 63.4, AA Coding Index 77) · vals.ai TB4 26.26 ± 0.51, 8th of 32, against 21.5% (#9) on tbench.ai · AA Intelligence Index v4.3.2 42 (max, read 2026-09-22) | active (cross-family verifier, Copilot) | 2026-07-12 · benchmarked 2026-07-20 · **repriced 2026-08-12** | **Cut 20% on both axes** from 2.50 / 15 (OpenAI pricing page + GitHub billing agree). **This dissolves the registry's own cost argument:** Terra's list price is now *exactly* Gemini 3.1 Pro's, 2 / 12 default and 4 / 18 long-context, on both axes. T18's finding that Terra costs ~2× Gemini was measured at the old price and no longer follows from list rates — re-measure before treating either as the cost-sensitive default. The quality half of T18 (ties on seeded recall, more thorough on non-seeded defects) is unaffected. Slug `gpt-5.6-terra`. It has no GPT-6 successor: OpenAI's "balance intelligence and cost" slot moved to GPT-6 Sol on 2026-09-22, which ties it on input and cache-read and undercuts it on output (10 against 12) |
| Haiku 4.5 | Mechanical | 1 / 5 | **vals.ai SWE-V 66.6** (read first-hand from the board's own data 2026-08-23), row `claude-haiku-4-5-...-thinking` — correcting the unsourced **~73** · AA Intelligence Index v4.3.2 16.88 (reasoning) · no vals.ai TB4 row (both read 2026-09-22) | default (mechanical floor) | 2026-07 | Silent-failure risk — only ever behind smartcheck. Holds the Cheap tier wherever no Luna row is served, no effort dial, nearest retirement horizon in the lineup, and the worst cache floor: see § Notes below. Copilot Cheap and scout seats moved to GPT-5.6 Luna 2026-09-07; Haiku stays the Claude Code Cheap floor (Luna is not on that harness) and the documented Copilot fallback. On Copilot it's last in the Cheap and scout `models:` lists, after both Lunas. 200K ctx / 64K out, extended rather than adaptive thinking (read 2026-09-22). |
| GPT-5 mini | Mechanical | 0.25 / 2 (cache-read 0.025, no cache-write line; **metered per token under AI credits** — the "included"/0x status was premium-request-era, which ended 2026-06-01; re-verified vs the live pricing page 2026-07-13, the development repo's claim ledger) | **vals.ai SWE-V 60.8** (read first-hand from the board's own data 2026-08-23) — the LOWEST score on the Copilot roster, correcting "no coding-suite placement published" · Arena creative writing #196 of 400 (snapshot to 2026-09-13), a writing board | candidate, retiring from Copilot 2026-10-19 (changelog 2026-09-18), successor GPT-5.6 Luna | 2026-07-13 · retiring noted 2026-09-21 | 4×/2.5× cheaper than Haiku, ~8× cheaper cache-read than promo Sonnet; first live trial 2026-07-12 (T16): mechanical leaf, first-shot pass, 5/5 hidden oracle, 1.2 cr = 39% of Haiku's class avg — the default PROBE workhorse; still n=1, floor unchanged pending more samples. **Retiring 2026-10-19** (changelog 2026-09-18, refute-verified 2026-09-20), successor GPT-5.6 Luna. T16 stays as historical evidence; the probe-workhorse role moves to Luna, which undercut it on output the day it repriced. On the API, its only snapshot `gpt-5-mini-2025-08-07` shuts down 2026-12-11. OpenAI names `gpt-5.6-terra` as the replacement there |
| GPT-5.6 Luna | Implementer | **0.20 / 1.20** (cache-read 0.02; Copilot long-context >200K: 0.40 / 1.80) · a plain rate, not a promo: OpenAI's pricing page footnotes only Sol as promotional (read 2026-09-22) | TB2.1 **75.7 on the official board, rank 9** (verified 2026-08-06) · vals.ai SWE-V 93.0 (2026-08-12, score unmoved on the 2026-09-15 re-read) · **the two TB4 boards disagree:** tbench.ai 17.3%, above Sonnet 5's 12.4%, while vals.ai TB4 gives 4.55 ± 0.88, 25th of 32, below Sonnet 5's 8.08 · AA Intelligence Index v4.3.2 37.32 (max), AA's own TB4 run 11.6% (read 2026-09-22) | **default (Copilot coding-leaf floor + scout seat, from 2026-09-07)** — behind the verifier. Held at the Cheap seat tier by price, though classed Implementer. Since 2026-09-22 it's the `model:` fallback and second in `models:` behind GPT-6 Luna, and what every plan runs until a `gpt-6-luna` slug ships | 2026-07-09 (GA day) · **new price first recorded 2026-08-12** · prioritized 2026-08-20 | **Cut 5× on both axes** from 1 / 6 (OpenAI model page + GitHub billing agree). That made it the **cheapest Copilot-dispatchable model in this registry on both axes**, tied with MAI-Code-1.1-Flash and under GPT-5 mini's 0.25 / 2, while scoring 93.0 on vals.ai SWE-V, far above anything else at its price. It held that title until GPT-6 Luna (0.10 / 0.50) landed on 2026-09-22. The repo's old "long-context recall collapses to 41%" line has **no primary source** — checked OpenAI's model page and the GPT-5.6 Preview System Card, neither carries it — so it is dropped rather than repeated. **Prioritized for Copilot coding 2026-08-20 at the author's direction.** The board case is strong: SWE-Verified 93.0 is *above* Sonnet 5's 79.6 while costing 0.20 / 1.20 against Sonnet's 2 / 10, roughly 10x cheaper in. What it did NOT have on 2026-08-20 was a trial in this repo's own corpus, so it stayed a first pick, not a floor, until the seat move recorded next. **Reclassified Implementer and seated 2026-09-07** on the two independent boards (vals.ai SWE-V 93.0 above Sonnet 5's 79.6; TB4.0 17.3% above Sonnet 5's 12.4%), price unchanged, at the author's direction ("luna is so high value, we want to get the most out of luna"). `@smartplan-implementer-cheap` and `@smartplan-scout` pin it on Copilot. The fail-twice target is the Mid seat (GPT-6 Sol where served, else Sonnet 5). The verifier stays cross-family (Gemini 3.8 Flash from 2026-09-16, or Sonnet 5, never GPT-5.4 while an OpenAI model executes). Still no T-record in this corpus: a live bounce rate past ~20–30% is the reclassify-back trigger. **Second in line from 2026-09-22:** GPT-6 Luna (row below), OpenAI's named successor at under half the price, heads the Cheap, scout and Cheap-verifier `models:` lists at the author's direction. OpenAI keeps this model available and un-deprecated. It stays each list's resolving entry until a CLI build names `gpt-6-luna`. **The TB4 half of the 2026-09-07 case is harness-dependent:** vals.ai's TB4 board puts this model below Sonnet 5, the reverse of tbench.ai. That doesn't move a seat. It does put more weight on the verifier and the bounce-rate trigger |
| GPT-6 Luna | Implementer (provisional) | **0.10 / 0.50** (cache-read 0.01, write 0.125 · >272K: 0.20 / 0.75 on the WHOLE request) · OpenAI and GitHub agree · Batch and Flex 0.05 / 0.25, Fast mode 0.20 / 1.00, where Copilot bills Standard | absent from tbench.ai and vals.ai TB4 (read 2026-09-22) · **AA's own TB4 run 12.6% (max)**, against GPT-5.6 Luna's 11.6% · AA Intelligence Index v4.3.2 37 (max), 37.26 against GPT-5.6 Luna's 37.32, at $0.068 per index task against $0.178 · vendor: DeepSWE v1.1 66.6% (max), FrontierCode 1.1 42.4% (max) | provisional · **first in the Copilot Cheap, scout and Cheap-verifier `models:` lists from 2026-09-22** (author direction, untrialed, GPT-5.6 Luna behind it) · Copilot GA 2026-09-22, every paid plan including plain Pro, not in Auto | 2026-09-22 | Released 2026-09-22 as GPT-5.6 Luna's successor, API id `gpt-6-luna`, 1.05M ctx (922K max input) / 128K out, effort none to max (default medium). **The cheapest Copilot-dispatchable model in this registry on every axis**: half GPT-5.6 Luna's input and cache-read and 42% of its output. Its Copilot long-context line also moves out to 272K from Luna's 200K. **Seated first at the author's direction 2026-09-22** ("Luna-6 should be prioritized on a budget"): it heads the `models:` lists of `@smartplan-implementer-cheap` and `@smartplan-scout` (both at `reasoningEffort: low`) and `@smartplan-verifier-cheap`, with GPT-5.6 Luna behind it. It leads under § How to edit's newest-version rule too, which needs no Legacy notice. AA scores the two level. The move buys a price cut at equal capability, not a capability gain. No CLI build names a `gpt-6-luna` slug yet. Every plan runs GPT-5.6 Luna today. The ordered fall-through is untested here, since this account is on Copilot Free. Record the bounce rate once the slug resolves. Past ~20 to 30% is the trigger to reorder the lists. OpenAI's own card reports GPT-5.6 Luna misrepresenting coding work more than 3× as often as GPT-6 Luna, a vendor point in the successor's favour |
| Kimi K3 | Mechanical | 3 / 15 (cache-read 0.30, the roster's usual 0.1× — Moonshot and GitHub agree) | vals.ai SWE-bench Verified **93.4** (score unmoved, re-read 2026-08-19), outside the frozen board's leading group of six at 95.4 or above (read 2026-09-21). Track the score, not a place · **AA Intelligence Index v4.3.2 44 (max), #3 open-weights** (read 2026-09-21), behind MiMo-V2.6-Pro (46) and GLM-5.3 (45). Its pre-v4.3 tie with GLM-5.3 at 60 is on the retired scale · vals.ai TB4 12.63 ± 1.01 (read 2026-09-22), its first TB4 read, well below GLM-5.3 | candidate (Copilot-selectable, dispatch-confirmed 2026-08-06; on the supported-models table as GA since CLI v1.0.79, 2026-08-10) | 2026-08-06 · re-checked 2026-08-12 | Shipped 2026-07-16. **Open weights HAVE now shipped** (`moonshotai/Kimi-K3` on Hugging Face, ~2026-07-27) — correcting this file's earlier "still unshipped" note. License is the bespoke **Kimi K3 License, not MIT**. 2.8T total / 104B activated. Priced 3 / 15, which is now *more* than Sonnet 5 rather than equal to it, since Sonnet 5 stayed at 2 / 10 — so the "Sonnet-5 money" framing is retired. Still a *candidate*, not a floor: trial against Haiku 4.5 first. At Moonshot, cache writes bill 3.00 (5-minute TTL, the default) or 6.00 (1-hour), 1× and 2× input, where Anthropic's 5-minute write is 1.25×. A hit refreshes the TTL at no write charge. Context is 1,048,576 tokens. GitHub hosts K3 on Fireworks AI under zero data retention and prints no K3 cache-write price. A Copilot dispatch isn't affected |
| GLM-5.3-Flash | Mechanical | **0.15 / 0.50** (cache-read 0.03, storage limited-time free) — the 50% launch promo ended 24:00 2026-09-09 UTC+8, list rate re-read 2026-09-15 | **vals.ai SWE-V 92.0** (independent, read 2026-09-15; board now archived) · AA Intelligence Index v4.3.2 **42, #4 open-weights of 68** (read 2026-09-21), three points off GLM-5.3 and four off the open-weights leader, at roughly a tenth of GLM-5.3's price · vals.ai TB4 19.70 ± 0.88 at $0.645 a test, ahead of Sonnet 5 and Opus 4.8 (read 2026-09-22) | candidate | 2026-08-31 | Added to ZCode 3.9.2 (2026-08-26), "available out of the box for subscription users". 320B / 18B active MoE, multimodal in (video/image/text/file), 1M ctx / 128K out, first open frontier model combining sparse and linear attention, thinking cannot be disabled. Plan multiplier 2.3/0.56/8. The cheapest paid GLM-5 model on every axis. GLM-4.7-FlashX undercuts it on all three at 0.07 / 0.01 / 0.40. Plan requests for GLM-4.7 are served here (devpack overview, read 2026-09-15). So are requests naming `glm-5-turbo`, undocumented (see its row) |
| GLM-5.3-FlashX | Mechanical | 0.37 / 1.25 (cache-read 0.075, a 0.2× ratio — read 2026-09-21) | none on a board this file tracks | provisional (Z.ai-side, no seat here) | 2026-09-20 | Surfaced on Z.ai's pricing page 2026-09-20 with no registry row. Sits between GLM-5.3-Flash (0.15 / 0.50) and GLM-5.3 (1.40 / 4.40) on both axes, so it is the faster-Flash tier, not a cheaper one. Z.ai's model page calls it the same model as GLM-5.3-Flash served at about 200 tokens/s, 1M ctx, and says it isn't on the Coding Plan yet (read 2026-09-22). Nothing on this box or on Copilot dispatches it, so provisional and never a floor without a trial |
| GLM-5-Turbo | Mechanical | **none published** — absent from every table on the API pricing page (re-read 2026-08-31), and not a Coding Plan model either (devpack FAQ, read 2026-09-22) | none — its card's scores are chart-image only | **retired on the GLM Coding Plan** (undocumented reroute to GLM-5.3-Flash, observed 2026-09-17 to 2026-09-22), unpriced on the API | 2026-08-31 · plan status 2026-09-22 | 200K ctx / 128K out, text-only, positioned for the OpenClaw agent scenario (its card introduces ZClawBench). Its guide page still resolves. The devpack FAQ and overview name only GLM-5.3 and GLM-5.3-Flash as plan models. None of Z.ai's three published tier mappings for the plan names it (both read 2026-09-22). Plan requests naming `glm-5-turbo` still complete. The account monitor bills all of that traffic as GLM-5.3-Flash (2026-09-17 to 2026-09-22, matched against client-side session records), a reroute no Z.ai page documents. It landed between 2026-09-02 and 2026-09-17. So a pinned `glm-5-turbo` runs GLM-5.3-Flash. zcode.md's 1.20 / 0.24 / 4.00 row and the ledger row behind it were stale at the source — corrected in the same sweep |
| Qwen3.8-27B_Q4_K_M | Mechanical | **no per-token cost** — local GGUF: 18.9GB at Q4_K_M with MTP draft model + vision mmproj (the local install, 2026-08-29) | **vals.ai SWE-V 86.0** (independent, read 2026-09-15) · vendor card: SWE-bench Pro 61.7 · TB2.1 (Terminus) 73.0 · LiveCodeBench v6 90.3 · GPQA Diamond 89.2 · OSWorld-Verified 84.3 · AA Intelligence Index v4.3 **34 (xhigh)** (read 2026-09-15), below the 2.4T flagship's 40 · vals.ai TB4 4.04 (read 2026-09-22) | provisional (local candidate seat, not eval-gated) | 2026-08-31 | Alibaba's Qwen3.8-27B (Apache 2.0, shipped 2026-08-14): dense 27B multimodal, 262,144 native ctx extensible to 1M; family siblings are the 2.4T-A95B flagship (AA v4.3 40; its own page would not resolve on the 2026-09-21 read, and with four open-weights models now above 40 the "tied 4th" place is retired rather than restated) and Flash-Next 180B. Run locally as an 18.9GB Q4_K_M GGUF it is a zero-marginal-cost Mechanical seat, and wherever one resident model serves every tier alias, the ladder collapses onto it. The hard floors apply: never plans, never merges unverified, and the ~30K real-agentic-ceiling precedent for 30B-class models stands until measured otherwise. Qwen Cloud now lists a hosted `qwen3.8-27b` at 0.50 / 3 per 1M with 1M ctx (read 2026-09-22). This row's seat stays local |
| DeepSeek V4 Pro 0813 | Unclassified | **0.66 / 1.98 off-peak, 1.32 / 3.96 peak** (cache-hit 0.022 / 0.044; peak = 01:00–04:00 and 06:00–10:00 UTC Mon–Fri except Chinese public holidays, all else off-peak at half) — read 2026-08-16 (the development repo's claim ledger `deepseek-v4-peak-offpeak-0816`), re-read 2026-08-31 | vals.ai SWE-bench Verified **96.40, second overall** (read 2026-08-19), within 0.60 of Claude Opus 5's 97.00 · AA Intelligence Index v4.3 36 at `max` (read 2026-09-15) · vals.ai TB4 1.01 (read 2026-09-22) | **not Copilot-selectable — no seat** | 2026-08-19 | Added 2026-08-19 after a board re-read found it ranked second on SWE-bench Verified with **no row here at all**, in a registry that claims to track the cross-vendor field. Carried for board literacy, not as a candidate: it is absent from GitHub's supported-models table, so nothing in this family can dispatch to it. The gap between its SWE-bench placement (2nd), its AA Intelligence Index (36 on v4.3, well outside the top ten) and its vals.ai TB4 1.01 is itself the lesson — a single board is not a capability verdict. Priced as read 2026-08-31: at peak it still sits below Sonnet 5 on both axes. DeepSeek had scheduled the V4 Pro API to end 2026-09-14 and extended it indefinitely "in response to user demand" (pricing page, read 2026-09-15), so treat its availability as notice-driven |
| DeepSeek V4.1 Flash | Unclassified | **0.15 / 0.60 off-peak, 0.30 / 1.20 peak** (cache-hit 0.003 / 0.006; same peak windows as V4 Pro) — read 2026-09-21 | AA Intelligence Index v4.3.2 39 (max), read 2026-09-22, the top DeepSeek row there · vals.ai TB4 11.62 (read 2026-09-22) · no SWE-V entry (vals.ai archived that board before it could enter) | **not Copilot-selectable — no seat** | 2026-09-21 | `deepseek-flash` on the pricing page, model version DeepSeek-V4.1-Flash, 1M ctx / 384K out, vision supported. Serves requests made to the legacy names `deepseek-v4-flash` and `deepseek-v4-flash-vision-exp` (pricing page footnote, read 2026-09-22). DeepSeek's changelog scheduled `deepseek-chat` to end 2026-07-24. No current page says this model serves it. That routing retires the "V4 Flash 0731, since retired" note below. The line lives on as this row. The V4 Pro row's literacy argument covers it; no dispatch reaches it |
| Kimi K2.7 Code | Mechanical | 0.95 / 4 (cache-read 0.19 — a 0.2× ratio, double the roster's usual 0.1×) | AA Intelligence Index v4.3 26 (read 2026-09-15, class median not re-read) · AA Coding Index 60.8 · MCPMark 81.1 (above Opus 4.8 76.4) — vendor/aggregator only; vals.ai SWE-V 78.2 (independent, read 2026-08-23) · Terminal-Bench absent (confirmed 2026-07-17) | provisional (Copilot CLI v1.0.68+, GA), retiring from Copilot 2026-10-02 (changelog 2026-09-03), successor Kimi K3 | 2026-07-13 · priced 2026-07-15 | First selectable open-weight Copilot model (Moonshot AI); Business/Enterprise off-by-default (admin enable). **vals.ai SWE-V 78.2** (read first-hand from the board's own data 2026-08-23), correcting "absent from every standard board"; Moonshot's own numbers trail GPT-5.5/Opus on nearly every cell. **Succession resolved 2026-08-06:** Kimi K3 (shipped 2026-07-16, API 3 / 15) **is now Copilot-selectable**, dispatch-confirmed, and the picker reports it at reasoning **High** where every other roster model shows Medium. It supersedes K2.7 Code here; don't start new K2.7-specific trials. Slug `kimi-k2.7-code` |
| MAI-Code-1-Flash | Mechanical | 0.75 / 4.50 (cache-read 0.075) | vendor card only (Microsoft-run, Copilot VS Code harness, read 2026-09-15): SWE-bench Verified 71.6 · TB2.1 51.7 · **absent from vals.ai's 86-model board 2026-08-23 — no Microsoft model appears on it at all** — failed independent logic tests against same-price peers | **RETIRED from Copilot 2026-09-10** (deprecation history, read 2026-09-15) | 2026-07-15 · deprecation noted 2026-08-12 | Microsoft's first first-party code model on the roster. **GitHub announced its deprecation 2026-08-11 and it retired across all Copilot experiences on 2026-09-10** (changelog, confirmed 2026-09-15), with MAI-Code-1.1-Flash named as the successor. Note the knock-on — the 2026-07-31 notice had named *this* model as Raptor mini's replacement, so that migration path is now two hops. Don't start new trials here |
| MAI-Code-1.1-Flash | Mechanical | 0.20 / 1.20 (cache-read 0.02, published 2026-08-31) | vendor card (Microsoft-run, Copilot VS Code harness, read 2026-09-15): SWE-bench Verified 72.6 · TB2.1 62.9 · **absent from vals.ai's board 2026-08-23, same as its predecessor, and still no Microsoft row at 88 models on 2026-09-15** | provisional (Copilot roster GA, confirmed 2026-08-19; successor to MAI-Code-1-Flash) | 2026-08-12 · re-checked 2026-08-19 | Named by GitHub as MAI-Code-1-Flash's replacement ahead of the 2026-09-10 retirement. Priced at GPT-5.6 Luna's rate on all three axes (0.20 / 1.20 / 0.02, read 2026-08-31), with vendor-only benchmarks and no independent board entry — classify provisional and trial deliberately, never as a floor |
| Gemini 3.5 Flash | Mechanical | 1.50 / 9 (cache-read 0.15) | SWE-bench Verified 78.8, rank 6 (independent) · MCP Atlas 83.6 · TB2.1 74-76 · SWE-bench Pro 55.1 · vals.ai TB4 4.04 (read 2026-09-22) | provisional (Copilot roster, GA), retiring from Copilot 2026-10-02 (changelog 2026-09-03), successor Gemini 3.8 Flash | 2026-07-15 | Target of CLI v1.0.69's `minimal` reasoning-effort support; above Haiku on both axes — not a cheap-floor play. Superseded by 3.6 Flash (below) for new trials |
| Gemini 3.6 Flash | Implementer | **0.75 / 3.75** (promotional through 2026-12-31, footnote `gemini-flash-promo`; cached in 0.075). **Google now prints what follows: 1.50 / 7.50, cache 0.15 and storage 1.00/hr, from 2027-01-01 — a 2× step on every axis** | **vals.ai SWE-V 79.6** (read first-hand from the board's own data 2026-08-23), its own score at last — the inherited-from-3.5 read is retired; vendor claims ~17% fewer output tokens (AA Index), up to 65% on DeepSWE · vals.ai TB4 4.55 (read 2026-09-22) | **former cross-family verifier (2026-08-16 to 2026-09-16)**, retiring from Copilot 2026-10-02 (changelog 2026-09-03), GitHub names Gemini 3.8 Flash | 2026-07-24 | 3.5 Flash's successor at cheaper output (vendor claims ~17% fewer output tokens on top). Business/Enterprise follow the default-on model policy (2026-08-26). **Repriced 2026-08-14: at 0.75 / 3.75 it now sits BELOW Haiku 4.5 (1 / 5) on both axes**, which reverses this row's former "still above Haiku input price" reasoning — the price objection is gone, and as of 2026-08-23 so is the quality objection — vals.ai SWE-V 79.6 is its own independent read. What's thin now is this repo's own corpus: T34's 8/8 and T30's n=1. First trial 2026-07-25 (T30): mechanical leaf, first-shot pass, 6.5 cr — no price case vs GPT-5 mini's 1.2 cr class figure at the OLD price; n=1, worth re-running at the new one. **Took the cross-family verifier seat 2026-08-16** when Copilot retired Gemini 3.1 Pro; T34 cleared it at 8/8 recall first, and the 2026-08-14 reprice means the seat also got cheaper. Promo expiry 2026-12-31 is a re-check trigger (gate-readable marker lives in the development repo's claim ledger) **Reclassified Implementer 2026-09-07:** this row holds the cross-family verifier seat while § The classes says Mechanical never verifies, so the class cell contradicted the seat; its own vals.ai SWE-V 79.6 matches Sonnet 5's, which supports the move rather than driving it. |
| Gemini 3.7 Flash | Mechanical | **0.75 / 3.75** (cached in 0.075; the same `gemini-flash-promo` footnote as 3.6 Flash, through 2026-12-31 — read 2026-08-22, correcting this row's "not yet published"; the same printed 2× step from 2027-01-01 as 3.6) | **vals.ai SWE-V 80.8** (read first-hand from the board's own data 2026-08-23), one point above 3.6 Flash at an identical price · **Terminal-Bench 4.0 #15 at 11.2% ± 2.4%** (official board, re-read 2026-09-22), below Sonnet 5's 12.4% even though it sits above Sonnet 5 on vals.ai SWE-V · vals.ai TB4 6.06, below Sonnet 5's 8.08 there too (read 2026-09-22) | provisional (Copilot roster GA since 2026-08-13), retiring from Copilot 2026-10-19 (changelog 2026-09-18), successor Gemini 3.8 Flash | 2026-08-19 · retiring noted 2026-09-21 | Added to GitHub's supported-models table 2026-08-13 (GitHub changelog, same date), GA on arrival. 3.6 Flash's successor. Priced identically to 3.6 Flash and one vals.ai point above it, which is inside the noise of a single board. **Retiring from Copilot 2026-10-19** (changelog 2026-09-18, refute-verified 2026-09-20): 3.8 Flash, which already holds the cross-family verifier pin, is the named successor. No new trials here |
| Gemini 3.8 Flash | Implementer (provisional) | **0.75 / 3.75** (cache-read 0.075, the same `gemini-flash-promo` footnote as 3.6 and 3.7 Flash through 2026-12-31, then 1.50 / 7.50 from 2027-01-01) | **vals.ai SWE-V 80.0** (independent, read 2026-09-15) · **Terminal-Bench 4.0 #11 at 19.1% ± 3.4%** (official board, re-read 2026-09-22), above GPT-5.6 Luna's 17.3% · vals.ai TB4 13.13 ± 2.53, 16th of 32, above Sonnet 5's 8.08 and GPT-5.6 Luna's 4.55 (read 2026-09-22). Both TB4 boards order it the same way against those two · AA Intelligence Index v4.3 41 at `high` | **default (cross-family verifier pin, from 2026-09-16), unmeasured**, cross-family to both the Claude and the GPT seats · Copilot GA 2026-09-03, every paid plan including plain Pro | 2026-09-15 | GitHub's named successor for both Gemini 3.5 Flash and Gemini 3.6 Flash when they leave Copilot on 2026-10-02, and the cross-family verifier seat moved here from 3.6 Flash on 2026-09-16, at the author's direction, ahead of that retirement. Same price as 3.6 and 3.7 Flash under the same footnote. The seat moved to 3.6 only after T34 cleared it at 8/8 seeded recall. This pin has had no such trial, because the account is on Copilot Free, so run T34 here before trusting it on a shared-blind-spot leaf. Class is provisional until it does. Its slug is in `copilot help config` from CLI 1.0.83. Google has set no API shutdown date for 3.5 through 3.8 Flash (read 2026-09-22). The retirement dates on those rows are Copilot-only |

Cross-vendor prices/benchmarks with full sourcing: `copilot.md`'s table
(Copilot SKUs) and the development repo's claim ledger. Anthropic lineup,
strongest first by Anthropic's own tier order: Fable 5.1 = Mythos 5.1
(one model, invite only) > Opus 5.5 > Opus 5 > Opus 4.8 (both legacy) >
Sonnet 5 > Haiku 4.5, the order `flow.md` ships. The boards put Opus 5.5
ahead of Fable 5.1 (AA, vals.ai Terminal-Bench 4.0, Anthropic's own
table). So that one step is vendor positioning, not a measurement.
Fable 5 (legacy) and Mythos 5 (limited, not a seat) stay off the chain.
By list price: Fable 5.1 = Mythos 5.1 = Fable 5 = Mythos 5 (10 / 50) >
Opus 5 = Opus 4.8 (5 / 25) > Opus 5.5 (4 / 20) > Sonnet 5 (2 / 10) >
Haiku 4.5 (1 / 5). Price no longer tracks strength. Since 2026-09-22 the
strongest Opus is the cheapest one.

## Notes

*Anthropic rows re-verified 2026-09-22 against the pricing, models-overview,
deprecations, effort and prompt-caching docs, plus the Opus 5.5 model,
what's-new, migration and prompting pages.*

- **Two Copilot-selectable models have no row here** (supported-models page
  read 2026-09-22, after a live roster read 2026-09-02 on CLI 1.0.81, Pro
  account — availability is per-plan, so treat a picker read as one seat's
  view rather than general availability): `claude-opus-4.7`, itself retiring
  from Copilot 2026-10-02, and `claude-opus-4.8-fast`. Opus 5.5, GPT-6
  Sol, and GPT-6 Luna shipped to Copilot on 2026-09-22 and took rows the
  same day. Grok 4.7 did the same on 2026-09-21. Earlier arrivals
  (`gemini-3.7-flash`, `grok-4.6`, `mai-code-1.1-flash`, `gpt-5.4-mini`)
  took rows between 2026-08-12 and 2026-08-31. `claude-fable-5.1` was
  seated 2026-09-07 from a first-hand pricing read. Its slug has a CLI
  support line and a help config entry from 1.0.83. GPT-6 Astra and
  Gemini 3.8 Flash took rows on 2026-09-15. **None is seated until
  researched, except by author direction or § How to edit's
  newest-version rule.** The registry's default-vs-candidate discipline
  exists exactly so a new slug cannot be routed to on sight. Opus 5.5,
  GPT-6 Sol and GPT-6 Luna are the exceptions: they head Copilot
  `models:` lists from launch day, untrialed. On a launch day
  read the rendered docs.github.com pages: the public `github/docs` YAMLs
  caught up hours later on 2026-09-22. Those YAMLs key models by display
  name. Their `cli: true` says GitHub offers a model in the CLI, not which
  slug or build. The slug sources are the copilot-cli release notes and
  each build's `copilot help config`. Help config isn't a complete roster
  either (see the Grok 4.6 row).
- **The 2026-09-01 Copilot retirement completed.** The same read confirms
  Opus 4.5, Opus 4.6, Sonnet 4.5, Sonnet 4.6, Gemini 3.1 Pro and Raptor mini
  are all gone from the picker, though GitHub's plan table still lists Sonnet
  4.6 for individual annual Pro and Pro+ subscribers (read 2026-09-15), so
  that one reads as account-scoped rather than withdrawn. The Gemini 3.1 Pro
  row above is retained as a retirement record, not a routing option.
- **Terminal-Bench 4.0 replaced 2.1, and it reorders the field.** Read in a
  browser 2026-09-02, re-read 2026-09-15, 2026-09-21 and 2026-09-22 (the
  table renders client-side and returns nothing to a plain fetch). The
  board now lives at tbench.ai's root. The old `/leaderboard/...` URLs
  308 there. Resolution rate ± 95% CI, agent in parens, **15 rows,
  unchanged cell for cell on 2026-09-22, with no Opus 5.5 row yet**. The
  default view shows each model's best row. A 2026-09-17 effort sweep added
  low-to-xhigh rows for Opus 5 and Fable 5.1, which is why Opus 5 shows at
  xhigh, while its (max) row (51.8% ± 3.4%) stays in the data. GPT-6
  Astra's per-effort rows are older, from 2026-09-03. They sharpen the
  cost story: Astra at high scores 57.88% ± 2.97% for $2.3k, level with
  Fable 5.1's max within CI at 37% of its cost. Fable 5.1 at xhigh
  matches its own max (57.88%) for $4.9k against $6.2k. **Grok 4.7
  arrived at #6** on 2026-09-21, the day it shipped. Its $3.7k covers
  324 of 330 trials:

  | # | Model | Agent | Rate | Cost |
  |---|---|---|---|---|
  | 1 | **GPT-6 Astra** (max) | Codex | **58.2% ± 2.8%** | $3.3k |
  | 2 | **Fable 5.1** (max) | Claude Code | 57.9% ± 3.8% | $6.2k |
  | 3 | **Opus 5** (xhigh) | Claude Code | 53.9% ± 3.2% | $6.1k |
  | 4 | Fable 5 (max) | Claude Code | 44.5% ± 3.8% | $7.3k |
  | 5 | **GLM-5.3** (max) | Claude Code | 41.8% ± 3.2% | **$2.7k** |
  | 6 | **Grok 4.7** (xhigh) | Grok Build | 37.6% ± 3.5% | $3.7k |
  | 7 | GPT-5.6 Sol (max) | Codex | 37.3% ± 3.8% | $2.5k |
  | 8 | Opus 4.8 (max) | Claude Code | 23.6% ± 3.6% | $6.5k |
  | 9 | GPT-5.6 Terra (max) | Codex | 21.5% ± 3.3% | $1.7k |
  | 10 | **Grok 4.6** (high) | Grok Build | 20.3% ± 3.1% | $3.6k |
  | 11 | Gemini 3.8 Flash (high) | mini-SWE-agent | 19.1% ± 3.4% | $1.8k |
  | 12 | GPT-5.6 Luna (max) | Codex | 17.3% ± 2.8% | $0.3k |
  | 13= | Grok 4.5 (high) | Grok Build | 12.4% ± 2.6% | $2.1k |
  | 13= | **Sonnet 5** (max) | Claude Code | 12.4% ± 3.1% | $9.6k |
  | 15 | Gemini 3.7 Flash (high) | mini-SWE-agent | 11.2% ± 2.4% | $1.3k |

  **The spread widens sharply**: on TB2.1 Sonnet 5 sat ~4 points behind Opus
  4.8 and ~9 behind the leader. On 4.0 it is at under a quarter of Opus 5's
  xhigh rate and ties Grok 4.5 for 13th. A harder benchmark separates the
  tiers this family routes between far more than 2.1 did, which strengthens
  the implementer-floor argument rather than weakening it. Every TB2.1
  figure in the rows above is **historical**.
- **Opus 5.5 has three TB4 numbers and none of them is the board's.**
  Vendor 66.4% (xhigh, system card), vals.ai 61.62 ± 1.01 (its own TB4
  board, Terminus 2, avg@3, updated 2026-09-22) and AA's own run 59.6%
  (mini-swe-agent), tied with GPT-6 Astra. Keep each in its source class.
  vals.ai's TB4 board is the live same-harness replacement for its archived
  SWE-V board: Opus 5.5 61.62, GPT-6 Astra 57.07, Fable 5.1 49.49, Opus 5
  45.45, Opus 4.8 16.16, Sonnet 5 8.08. The other rows carry their own
  reads. It logs safety fallbacks too: 30 of 198 Opus 5.5 tasks, 28 on
  Fable 5.1, 51 on Fable 5 and 1 on Opus 5. Counted as failures, they drop
  Opus 5.5 to 53.54 (behind Astra), Fable 5.1 to 42.42 and Fable 5 to
  16.67. So a Fable or Opus 5.5 score there is partly another model's
  work.
  Provider refusals score as failures too, most notably 21 on Qwen 3.8
  Max and 7 each on GPT-5.6 Sol and Sonnet 5.
- **GLM-5.3 is the cost story on that board** — 41.8% at $2.7k against Opus
  5's 53.9% at $6.1k, and Sonnet 5's 12.4% at $9.6k. Not a seat change on one
  board read, but the cheapest credible planner-class result recorded here.
  On vals.ai TB4, GLM-5.3-Flash scores 19.70 at $0.645 a test, ahead of
  Sonnet 5 and Opus 4.8, which vals.ai calls out on cost.
- **vals.ai SWE-bench Verified is now an ARCHIVED board** (read 2026-09-21):
  the page carries an "Archived Benchmark" banner — "Since performance on
  this benchmark has saturated, we no longer run this benchmark on new model
  releases. Previous results are preserved here for posterity." Content
  otherwise untouched since the 9/1/2026 update (88 models). Every vals.ai
  figure in this file is therefore a **frozen reference**, still comparable
  among the models that entered, never updated for arrivals: Grok 4.7 and
  anything after 2026-09-21 can never appear there. The 2026-09-15 re-read's
  correction stands: six models sat at 95.4 or above (Opus 5 97.00, DeepSeek
  V4 Pro 96.40, GPT-5.6 Sol 96.2, Grok 4.6 95.60, GPT-5.6 Terra 95.4, GLM
  5.3 95.4), not eight. Top 12, as frozen:
  Opus 5 · **DeepSeek V4 Pro 0813** · GPT-5.6 Sol · **Grok 4.6** · GPT-5.6
  Terra · GLM 5.3 · Fable 5 · Kimi K3 · GPT-5.6 Luna · GLM 5.3 Flash ·
  DeepSeek V4 Flash 0731 (since retired by DeepSeek) · Opus 4.8. Sonnet 5
  sits **25th**, behind Gemini 3.8 Flash at 24th.
- **Four unseated models now have board positions**, which is what turns them
  from roster noise into a real gap: **Grok 4.6** is 4th here and 10th on TB
  4.0 — above GPT-5.6 Terra, GLM 5.3 and Fable 5 on this board — while
  **DeepSeek V4 Pro 0813** is 2nd and carries only an unseated,
  non-dispatchable row here. **Opus 4.7** (21st), the one still without a row,
  and **Gemini 3.7 Flash** (23rd) both sit above Sonnet 5. None is seated on a
  board read alone. The point is that the registry's ordering no longer
  matches the evidence.
- **Scale's SWE-bench Pro board re-read 2026-09-02, and it moved host** to
  `labs.scale.com` (the old `scale.com/leaderboard/...` now 308s). On
  2026-09-22 the public URL 308s again, to a combined
  `/leaderboard/swe_bench_pro` page with Public and Private tabs. Gemini 3.1
  Pro holds **46.10 ± 3.60, rank 5**, unchanged. The absence of Opus 4.8,
  Opus 5, Opus 5.5, GPT-5.5, GPT-5.6 and GPT-6 is re-confirmed
  (2026-09-22) — so the 69.2 and 58.6 figures
  carried here stay marked vendor-only. One drift, re-read 2026-09-15: the board ranks by upper
  CI bound (Rank (UB)). So ties share a place. `claude-opus-4-6 (thinking)`
  reads **rank 3**, tied with `Muse Spark` at 55.00, while the new `Muse Spark
  1.1` at 61.50 shares rank 1 with `gpt-5.4`. The 2026-09-02 read recorded it
  as rank 4.
- **Artificial Analysis moved to Intelligence Index v4.2, then v4.3, in
  September 2026, and the label now reads v4.3.2** (every AA page,
  re-read 2026-09-22; no v4.4 exists). v4.3 swapped
  Terminal-Bench 2.1 for 4.0 and τ³-Banking for AutomationBench-AA. Every
  model re-scored far lower. **Opus 5.5 took the overall top on
  2026-09-22**: 58 at max, then its xhigh (56) and high (54) rows, with
  Fable 5.1 and GPT-6 Astra joint 4th at 53 and Opus 5 at 51. AA labels the
  Opus 5.5 and Fable 5.1 rows "with fallback" ("Default Fallback" in full),
  a blended score partly served by Opus 5 or 4.8. Fable 5's row reads
  "Opus 4.8 Fallback" (49.63). Opus 5 is unlabelled. AA also flags
  superseded models as deprecated (Opus 5, Opus 4.8, Fable 5, GPT-5.6 Sol,
  GPT-5.6 Luna, GLM-5.2, Grok 4.5, Gemini 3.7 Flash, GPT-5.4) and hides
  them from its default Status: Current view. Their scores stay in the
  data. Set Status to All to find them. That's an AA display flag, not
  a vendor deprecation. Every AA figure in
  this file dated before 2026-09-15 is on the retired scale and does not
  compare with a v4.3 read. **The open-weights order changed under it**:
  AA's models page now reads "The top open weights AI models by
  Intelligence Index are: 1. MiMo-V2.6-Pro (46), 2. GLM-5.3 (max) (45), and
  3. Kimi K3 (max) (44)" — a Xiaomi model nobody had a row for holds #1
  open-weights, and every "#N open-weights" place this file carried below
  it slid one. AA's FAQ counts 68 open-weights models of 168 (read
  2026-09-22). MiMo-V2.6-Pro gets no row: no Copilot or local dispatch
  reaches it, and one index placing is thinner than the coverage bar the
  DeepSeek rows cleared.
- **The ladder is list price, not effective cost.** Fable 5.1, Fable 5, Mythos 5.1,
  Mythos 5, Opus 5.5, Opus 5, Opus 4.8 and Sonnet 5 use the newer tokenizer (~30% more tokens for the same
  text); **Haiku 4.5 is the only Anthropic row here still on the old one**. So
  on identical source text the real Opus 5.5:Haiku multiple is nearer
  **5.2:1** than 4:1 (6.5:1 on the legacy 5 / 25 Opus rows), and
  Sonnet:Haiku nearer 2.6:1. Anything
  that price-weights across tiers — the benchmark **W** unit included — is
  understating the cheap tier's advantage. Derived from two vendor-stated
  facts, not vendor-stated itself.
- **Seating an Opus 5 or 5.5 leaf — five operational facts** (researched
  2026-08-06 on Opus 5, the development repo's research notes, and
  carried to Opus 5.5 where its 2026-09-22 pages restate them). None of
  these are benchmark facts and all five present as "the model got worse":
  1. **Thinking is ON by default**, unlike Opus 4.8 where an absent
     thinking field meant none. **Never disable it**: with thinking off,
     Opus 5 occasionally writes a tool call into visible text instead of
     emitting a `tool_use` block, so the call never runs, no error is
     raised, and the leaked text pollutes later turns. A second artifact
     with thinking off: `<thinking>` and other internal XML tags leak into
     the visible response, and **a system-prompt rule telling the model not
     to think makes that worse** — remove such rules rather than adding
     them. Lower *effort* instead: thinking-on at `low` beats thinking-off
     at similar cost. The API enforces this too — `thinking: {type:
     "disabled"}` with effort `xhigh` or `max` returns a **400**.
  2. **`max_tokens` is a hard limit on thinking + response together**
     (verbatim, migration guide, read 2026-08-06: *"revisit it for
     workloads that ran without thinking on Claude Opus 4.8"*). A seat
     budgeted for a no-thinking 4.8 run can hit the cap and truncate,
     which reads as stopping early. Re-budget anything sized before
     2026-07-24.
  3. **Effort trades failure modes; it does not simply buy quality.**
     CodeRabbit's review benchmark (verified at source 2026-08-06) has Opus 5
     at x-high **more precise** on actionable comments than their production
     mix (39.3% vs 35.2%) but catching **fewer** known issues (55.2% vs
     61.1%) with ~4× the nitpicks (92 vs 23). Their *default* config found
     the most issues overall at worse precision. So x-high is not "better
     effort", it is a narrower, cleaner subset bought with recall — pick the
     failure mode the seat can afford, and re-sweep per seat rather than
     porting a 4.8 tuning. Vendor-run, and the vendor sells code review.
  4. **It self-verifies unprompted.** T32 measured two of three Copilot
     runs shelling out to check their own work, doubling input 25.8k →
     52.0k. Budget for the high end, and never add self-verification
     language to its brief (`brief.md` rule 9b).
  5. **A conservative review instruction backfires.** Told "only report
     high-severity issues" or "be conservative", Opus 5 follows it
     literally and under-reports. Ask for everything and filter in a
     separate pass — relevant wherever a verifier prompt is written
     (`check.md`, `smartreview`).

  **What Opus 5.5 changes** (its what's-new, migration, and prompting
  pages, read 2026-09-22). Fact 1 hardens: thinking can't be disabled at
  any effort. Effort is the only depth and cost lever. A thinking-off
  route can't be ported. Fact 2 hardens: it thinks more per turn than
  Opus 5 at the same effort. Re-budget `max_tokens` upward. Fact 3 gets a
  vendor data point: effort defaults to medium. Anthropic's own
  FrontierCode scores peak at medium and dip above it. Its
  Terminal-Bench 4.0 and CursorBench 4.0 charts rise from medium to high
  instead (57.6 to 64.2, 52.5 to 56.0) and flatten past that. So run a
  5.5 seat at high for agentic coding and verification, and go
  past high only on a measured gain.
  <!-- claim:opus-5-5-effort-curves --> Two are new. Text
  between tool calls comes back as thinking blocks, empty by default. On
  long multi-part tasks it can end a turn with a text-only progress
  report. Treat that as a continuation, capped at two or three, not as
  DONE and not as a strike. And never brief it to write out or quote its
  reasoning or system prompt: that trips the `reasoning_extraction`
  classifier, which refuses with no fallback. Facts 4 and 5 are Opus 5
  measurements, not yet re-run on 5.5.
- **Cross-vendor rows re-swept 2026-08-12** (this closed the "month stale"
  gap the 2026-08-05 pass left open). Four prices moved and one model was
  deprecated: GPT-5.6 Luna found cut 5× to 0.20 / 1.20, GPT-5.6 Terra cut 20% to
  2 / 12, GLM-5-Turbo corrected upward to 1.20 / 4.00 (since delisted from the API
  pricing page, see its row), and MAI-Code-1-Flash
  scheduled for retirement on 2026-09-10. **A 5× move between two
  sweeps is the argument for gate (n)**, not a one-off.
- **Board figures need a source label, and three here didn't have one.** The
  2026-08-12 re-read found that Scale's public SWE-bench Pro board carries
  **no row at all** for Opus 4.8, Opus 5, GPT-5.5, GPT-5.6 or GLM-5.2 — its
  newest Anthropic entry is Opus 4.6 at 51.90 and its newest OpenAI entry is
  GPT-5.4. So this file's 69.2 (Opus 4.8) and 58.6 (GPT-5.5) cannot be board
  figures whatever their provenance, and 54.2 (Gemini 3.1 Pro) contradicts
  the board's own 46.1. **Rule going forward: every benchmark cell states
  its source class** — official board, vendor/system card, or independent
  evaluator — because an unlabelled vendor number reads as a board number
  and that is exactly how these three got in.
- **The ladder is 4:2:1 on the current Opus, and interim.** Opus 5.5 :
  Sonnet 5 : Haiku 4.5 is exactly 4:2:1 on both axes since 2026-09-22
  (4 / 20, 2 / 10, 1 / 5). The legacy Opus rows keep 5:2:1. Anthropic
  cancelled the scheduled Sonnet 5 increase on 2026-08-10 — the release
  note reads "the previously scheduled increase to $3 / $15 per MTok on
  September 1, 2026 will not occur" — so Sonnet stays at 2 / 10. The
  Opus→Sonnet multiple is now 2× on the current Opus rather than 2.5×.
  Down-tiering from Opus now saves half the Opus list price on input and
  output rather than 60%, a third fewer dollars per token moved. It saves
  nothing on cache-read, where both sit at 0.20. The fan-out break-even
  moves out a little (derived, not vendor-stated). The benchmark corpus's
  W = 5·Opus + 2·Sonnet + 1·Haiku stays correct for every record priced on
  Opus 5 or 4.8. A record seated on Opus 5.5 weights it 4·Opus and says
  so. Sonnet 5.5 and Haiku 5.5 are announced for "the coming weeks".
  Expect the ratio to move again. Write "standard price", not "permanent":
  the vendor retired the schedule, it did not promise the rate never moves
  again.
  <!-- claim:sonnet5-standard-price -->
- **Effort is a second dial this table has no column for.** Full
  low/medium/high/xhigh/max on Fable 5.1, Fable 5, Mythos 5.1, Mythos 5,
  Opus 5.5, Opus 5, Opus 4.8, Opus 4.7 and Sonnet 5. In Anthropic's own
  harness the default is medium on Opus 5.5, xhigh on Opus 4.7 and high on
  every other effort model. On the API, Opus 5.5 defaults to medium where
  Opus 5 and Fable 5.1 default to high (read 2026-09-22). `xhigh` is
  missing on Opus 4.6 and Sonnet 4.6. Opus 4.5 takes effort with neither `xhigh` nor `max`. **Haiku 4.5 and
  Sonnet 4.5 have no effort dial at all**, so a Mechanical-class seat's only
  lever is the size of the brief you hand it.
- **The Cheap tier rests on one model.** Haiku 4.5 holds the Mechanical
  floor alone, has no released successor (the Opus 5.5 announcement says
  Haiku 5.5 will follow "in the coming weeks"), and carries the nearest
  retirement horizon in the current lineup: not sooner than 2026-10-15
  (floor re-read 2026-09-22), about three weeks out. No deprecation notice
  had posted by that read. The 60-day notice commitment means it cannot
  retire on Anthropic-operated platforms before about 2026-11-21 at the
  earliest. The Mid floor sits far safer: Sonnet 5 is Active with
  retirement not before 2027-06-30. Legacy Sonnet 4.5's floor is nearer
  than Haiku's, 2026-09-29. Anthropic's
  own harness still resolves its `sonnet` alias to it on Bedrock, Google
  Cloud, and Foundry. Retirements do
  land. `claude-opus-4-1-20250805` retired on 2026-08-05. The safer shape is
  to write the policy in tier **aliases** plus an effort dial rather than
  pinned model IDs, so a floor swap is one edit here instead of a sweep.
  Haiku 4.5 is also the only model in Anthropic's current lineup at 200K
  ctx / 64K out, where the rest run 1M / 128K. A leaf brief sized for a
  1M planner can overflow it.
- **The cache floor isn't monotonic, and it's worst on the cheap tier.**
  Minimum cacheable prefix: 512 tokens on Fable 5.1, Mythos 5.1, Opus 5.5,
  Opus 5, Fable 5 and Mythos 5, 1,024 on Opus 4.8 and Sonnet 5, **4,096 on Haiku 4.5**. Below the floor nothing caches
  and no error comes back. A brief that caches on the planner can silently
  fail to cache on a Haiku executor at eight times the floor, so prove a
  miss by checking that both `cache_creation_input_tokens` and
  `cache_read_input_tokens` are 0.
