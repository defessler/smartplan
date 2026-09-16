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
  deliberate, outcome-watched trial — never as a default.
- **Move a model between classes:** change its Class cell and date the Note.
  Moving a model *up* (e.g. Mechanical → Implementer) is cheap to be wrong
  about (work costs more); moving one *down* is not (silent failures) — a
  down-move should cite observed evidence (a bounce rate below the ~20–30%
  breakeven) or a benchmark, not a hunch.
- **Swap a default to its successor:** when the vendor ships a same-class
  successor at the same or lower price, makes it the vendor default, and
  moves the predecessor to Legacy, take the swap and date it even with no
  benchmarks in hand. Say in the Note that it rests on price parity plus
  vendor default rather than numbers, and keep the predecessor Active as the
  fallback. A *pricier* successor waits for benchmarks.
- **Keep prices dated.** Prices move; a dated wrong price beats an undated
  one because it tells the reader when to stop trusting it. Root
  the development repo's claim ledger carries the source checks.

## The classes

| Class | Ladder tiers | Holds these seats | Never |
| --- | --- | --- | --- |
| **Reasoning** | Max · Strong | Planner · verifier of Mid/Strong leaves · escalation reserve · irreducibly cross-cutting leaves | First-pass implementation, mechanical work, scouting |
| **Implementer** | Mid | Implementer floor (briefed/correctness-sensitive) · verifier of Cheap leaves · small-plan planner (drop-on-fit) | Planning beyond drop-on-fit; mechanical leaves when a Mechanical-class model is available (Copilot exception from 2026-09-07: GPT-5.6 Luna holds the Cheap coding and scout seats on price, see its row) |
| **Mechanical** | Cheap | Mechanical, single-concern, verifier-checkable leaves via smartexec + smartcheck · scouting (Haiku 4.5, or GPT-5.6 Luna on Copilot by the Implementer exception) | Planning, verification (except fully scripted checks), correctness-sensitive leaves |
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
| Fable 5.1 | Reasoning | 10 / 50 (5m write 12.50, 1h write 20, **cache-read 0.25 = 0.025×**, batch 5 / 25) | **Terminal-Bench 4.0 #2 at 57.9% ± 3.8%** ($6.2k, official board, read 2026-09-15), still absent from vals.ai and Scale · AA Intelligence Index v4.3 53 (max), tied top with GPT-6 Astra · Copilot's picker lists `claude-fable-5.1` (roster read 2026-09-02) | planner-only | 2026-09-07 | Read first-hand at platform.claude.com (pricing + models overview) 2026-09-07: current lineup, and Fable 5 moved to Legacy on the same read. API id `claude-fable-5-1`, adaptive thinking always on, default effort high, 1M ctx / 128K out, retire not before 2027-09-01. Same Max-tier rules as Fable 5: planning only, never a verifier, never a fail-twice target. **The cache-read price is the seat fact:** 0.25/MTok is half Opus 5's 0.50, so a turn that is mostly cached re-read (an orchestrator waking on a subagent completion) costs less on Fable 5.1 than on Opus 5 once the cached prefix exceeds roughly 20× the turn's new input plus 100× its output, about 140K tokens at 2K in / 1K out. Cold input and output stay 2× Opus, so it is the cheaper seat only for long, cached, low-output orchestration turns, not for reads or writes. **Seat facts from the what's-new page (read 2026-09-15):** forced `tool_choice` (`any`, or a named tool) returns a 400, its thinking blocks can't be read by any earlier model and drop silently on a fallback (permitted targets are Opus 4.8 and Opus 5), and it may make one tool call per turn where Fable 5 batched several. So an orchestrator on this seat can serialize a wave's dispatches unless the brief asks it to batch. Effort defaults to high in Claude Code, medium on claude.ai and Cowork <!-- claim:fable-5-1-price --> |
| Fable 5 | Reasoning | 10 / 50 | TB2.1 83.8 — #1 on the official board (re-confirmed 2026-07-24) · vendor SWE-Pro 80.3 | planner-only (legacy fallback) | 2026-07 · benchmarked 2026-07-20 | Max tier: hardest architecture/decomposition decisions only; never a fail-twice target, never a verifier **Legacy as of 2026-09-07** (models overview, read first-hand): Fable 5.1 is the current Max-tier row; this one stays as the same-price fallback. |
| Mythos 5 | Reasoning | 10 / 50 (cache-read 1.00; 5m write 12.50, 1h write 20; batch 5 / 25) | none on a coding board, absent from every board this file tracks. Anthropic's only published figure found is USAMO 2026 99.8% (vendor, Sonnet 5 System Card §8.6), a math eval that says nothing about coding | **not a seat — limited availability** | 2026-08-28 | Added 2026-08-28 after a sweep found the pricing page carries it and this registry did not, in a file whose own summary line claims to give the Anthropic lineup strongest to cheapest. Priced identically to Fable 5 on every axis including cache and batch. Gated behind a limited-availability programme rather than generally callable, so it is carried for lineup completeness, not as a candidate — the same reasoning that added the DeepSeek row. Uses the newer tokenizer (~30% more tokens for the same text), the same one Fable 5 uses, so its effective cost matches Fable 5's and sits about 30% above an old-tokenizer model at the same list rate. `caching.md`'s minimum-cacheable-prefix table already knew about it, which is how the gap showed. Superseded by Mythos 5.1 (2026-09-01), and still listed on the pricing page |
| Mythos 5.1 | Reasoning | 10 / 50 (cache-read 0.25 = 0.025×; 5m write 12.50, 1h write 20; batch 5 / 25) | none published | **not a seat (invite only, Project Glasswing)** | 2026-09-15 | Released 2026-09-01 as Mythos 5's successor, API id `claude-mythos-5-1`. Anthropic states it is the same model as Fable 5.1 with different safeguards, sharing its specs and pricing, and retire not before 2027-09-01. Carried for lineup completeness, the same reasoning that carries the Mythos 5 row. Its cache-read is 0.025× base input like Fable 5.1's, the only two rows here off the roster's usual 0.1× |
| Claude Opus 5 | Reasoning | 5 / 25 | **vals.ai SWE-bench Verified 97.0, rank 1** (board updated 2026-08-05, re-read 2026-08-06, ahead of GPT-5.6 Sol 96.2 and Fable 5 95.0); **that absence ended: Terminal-Bench 4.0 has it at 51.8% ± 3.4%, #3 behind GPT-6 Astra and Fable 5.1** (re-read 2026-09-15, #1 on the 2026-09-02 read) — the "no official-board entry" note here described TB2.1 and is retired | **default (planner + Strong verifier)** | 2026-07-25 · promoted 2026-08-05 | Same price as Opus 4.8. As of 2026-08-05 Anthropic lists it Active/current. It's the Claude Code default on Max, Team Premium, Enterprise and the Anthropic API (also Claude Platform on AWS, Bedrock and Google Cloud, while Pro and Team Standard default to Sonnet 5 and Microsoft Foundry to Sonnet 4.5 — code.claude.com model-config, read 2026-09-15), with 4.8 moved under Legacy on the overview page. **Promoted on that evidence, not on benchmarks** (none had landed as of 2026-08-05), because a same-class same-price up-move is what § How to edit calls cheap to be wrong about, and the predecessor is now the vendor's legacy row. Revisit if the first board entry lands below 4.8. On Claude Code ≥2.1.219 the `opus` alias and opusplan's plan phase resolve to it on the Anthropic API. `default` isn't an alias. It reverts to the account's recommended model. Copilot CLI-selectable since v1.0.75 (Pro+/Max-gated); T30 (07-25) saw it serve where 4.8 was Pro-gate-refused on 07-11 |
| Opus 4.8 | Reasoning | 5 / 25 | **vals.ai SWE-V 88.6** confirmed (read first-hand from the board's own data 2026-08-23) — note the board carries a SECOND row under the identical label, `claude-opus-4-8-claude-code` at 85.8 · SWE-bench Pro 69.2 **(vendor — absent from Scale's public board, checked 2026-08-12)** · SWE-bench Verified 88.6 · TB2.1 78.9 — official board #5 (2026-07-24) | active (same-price fallback) | 2026-07-09 · demoted from default 2026-08-05 | Held the planner + Strong verifier default 07-09 → 08-05 on price + SWE-bench (GPT-5.5 edges it on TB2.1, 83.1 vs 78.9, but is Pro-gated and pricier on output). **Succession resolved 2026-08-05:** Opus 5 takes the default at identical price. 4.8 stays Active and costs the same, so it's the drop-in fallback when an Opus 5 seat is unavailable. Retire not before 2027-05-28 |
| GPT-5.5 | Reasoning | 5 / 30 (>272K: 10 / 45) | **vals.ai SWE-V 82.6** (read first-hand from the board's own data 2026-08-23) — the board carries two more rows under the same display label, codex 76.4 and factory 76.2 · SWE-bench Pro 58.6 **(vendor — absent from Scale's public board, checked 2026-08-12)** · TB2.1 83.1 — official board #2 (2026-07-24) | not a seat (Pro+-gated on Copilot) | 2026-07-09 · refined 2026-07-20 | **Refined 2026-07-20 (supported-models):** still GA and CLI-selectable, but Pro = Not included — which is why T18's Pro-roster observation missed it. (Re-derived 2026-09-15 from github/docs `model-supported-plans.yml`: `pro: false`, with Pro+, Max, Business and Enterprise true.) Flagship-superseded by the GPT-5.6 family, and then by GPT-6 Astra (GA on Copilot 2026-09-04). On Pro the live cross-family peer is GPT-5.6 Terra |
| GPT-6 Astra | Reasoning | 10 / 50 (cache-read 1.00, write 12.50 · >272K: 20 / 75 on the WHOLE request) | **Terminal-Bench 4.0 #1 at 58.2% ± 2.8%** ($3.3k, official board, read 2026-09-15) · AA Intelligence Index v4.3 53 (max), tied top with Fable 5.1 · absent from vals.ai and Scale, and OpenAI's model page publishes none | provisional (Copilot GA 2026-09-04, Pro+-gated) | 2026-09-15 | OpenAI's new flagship, released 2026-09-03 and GA on Copilot 2026-09-04 for Pro+, Max, Business and Enterprise, not plain Pro. 1.05M ctx / 128K out, effort low to max, not in the CLI Auto pool. Priced at Fable 5's list rate on both axes while costing half as much per board run ($3.3k against $6.2k). A pricier successor waits for benchmarks per § How to edit, so no seat until a trial |
| GPT-5.6 Sol | Reasoning | **4 / 20** (cache-read 0.40, write 5.00 · >272K: 8 / 30 at cache-read 0.80, write 10.00) — GitHub dropped the promo footnote after 2026-09-03 and its table now prints the standard rate (read 2026-09-15), vindicating the 2026-08-22 arithmetic that derived it. **OpenAI's own pages still say the 2 / 10 promo runs "at least through November 21, 2026"** (read 2026-08-28). So the Copilot bill and the API bill may now differ. Past 272K bills the **WHOLE request** at 2× input / 1.5× output — a cliff, not a marginal tier (model page) | **Terminal-Bench 4.0 #6 at 37.3% ± 3.8%** (re-read 2026-09-15, #4 on the 2026-09-02 read), so the vendor-only/absent framing that applied on TB2.1 is retired; the older 88.8 was a TB2.1 vendor figure; vals.ai SWE-V 96.2 (independent, not the official board) | provisional (Copilot-exposed) | 2026-07-09 (GA day) · re-researched 2026-07-20 | Pro+-gated. Elite agentic scores but measured weak on open-brief architecture (Every 56/100 vs Fable 90) and METR's highest eval-gaming rate — never grades work against visible tests; not a planner swap. Full caution set: the model guide |
| Gemini 3.1 Pro | Reasoning | 2 / 12 (>200K: 4 / 18) | **vals.ai SWE-V 78.8** (read first-hand from the board's own data 2026-08-23) (row `Gemini 3.1 Pro Preview (02/26)`) · SWE-bench Pro **46.1, rank 5 (Scale public board)** · TB2.1 65.8 — official board **rank 14**, tied with Gemini 3 Pro also at 14, next row skips to 16 (re-read 2026-08-12) | **RETIRED from Copilot 2026-09-01 (roster read 2026-09-02) — seat handed to Gemini 3.6 Flash** | 2026-07-12 · corrected 2026-08-12 | **MEASURED (T18): ties GPT-5.6 Terra on seeded C++ recall (14/15 each over 2 fixtures) at 47% the cost (8.69 vs 18.53 cr), esp. UE5.** **Two corrections from the 2026-08-12 board re-read:** the old "SWE-bench Pro 54.2" appears nowhere on Scale's board (which says 46.1) and was an unlabelled vendor figure reading as board-sourced; and the TB2.1 rank is 14, not 15 — this file's own 2026-07-20 ledger row had it right and the 2026-08-06 pass introduced the error. **The cost case needs re-measuring:** Terra repriced to an identical 2 / 12, so this seat's list-price advantage over Terra is gone. Slug `gemini-3.1-pro-preview`. Never a planner swap. **Seat vacated 2026-08-16:** Copilot retired this model 2026-09-01 and T34 (2026-08-05) cleared Gemini 3.6 Flash as the successor at 8/8 recall on the seeded custom fixture, cost indistinguishable. All routing sites (`check.md`, `cpp-gamedev-check.md`, `copilot.md`, the Copilot verifier seat) now name 3.6 Flash. Anthropic-side and other harnesses are unaffected by the Copilot retirement date. Added 2026-08-31: GitHub's roster listed it as **Public preview, never GA** — the only non-Anthropic model on the 31-row roster in that state, retired straight out of preview, which contextualizes why the seat went to a GA model (3.6 Flash) rather than a same-model upgrade |
| Sonnet 5 | Implementer | 2 / 10 | **vals.ai SWE-V 79.6** (read first-hand from the board's own data 2026-08-23) — correcting **85.2**, which appears nowhere on that board for Sonnet 5 in any subset, and which is a vendor system-card figure (Sonnet 5 System Card §8.2, read 2026-09-15) rather than a board placement · TB2.1 74.6 — official board #10 (2026-07-24) | default (implementer floor + Cheap-leaf verifier) | 2026-07-09 · repriced 2026-08-12 | ~9 pts behind Opus 4.8 on vals.ai SWE-V (79.6 vs 88.6), ~17 behind Opus 5 — the floor argument. **The $2/$10 introductory rate became Anthropic's standard price on 2026-08-10**; the 2026-09-01 step to $3/$15 was cancelled and will not occur. GitHub's billing page dropped the promotional footnote by 2026-08-31, so the $2/$10 now reads unqualified standard on both vendors <!-- claim:sonnet5-standard-price --> |
| Grok 4.5 | Implementer | 2 / 6 · **past 200K bills 4 / 12 on the WHOLE request** (a cliff, not a marginal tier) · cached in 0.50 (1.00 long tier) | Terminal-Bench 2.1 **rank 4, 79.3%** (read 2026-08-14) — above Opus 4.8's 78.9 at a fifth of Opus's output price · vals.ai SWE-bench Verified 86.60 (score re-read 2026-09-15) | candidate | 2026-08-14 | GA on Copilot since **2026-07-28**, every paid plan **including plain Pro**. Billing: input and output match xAI list, but **cached input does not** — GitHub bills 4.5 at 0.50 / 1.00 against xAI list 0.30 / 0.60, while 4.6 matches at both sources (re-read 2026-08-31), so this row's cache figures are what a Copilot dispatch pays, not xAI list. 500K native; the picker read 328K on 2026-08-06 and GitHub publishes no per-model picker cap, so the two numbers measure different things. xAI runs these directly with no logging, no disk write and no retention of any kind — stricter than Fable 5's 30-day safety-classifier retention. Business/Enterprise admin-enable, off by default. **Boards put it in Reasoning territory at an Implementer price**, which is the shape that earns a deliberate trial, not a default |
| Grok 4.6 | Implementer | 2 / 6 · past 200K 4 / 12 whole-request · cached in 0.50 (1.00 long tier) | vals.ai SWE-bench Verified **95.60** (entered 2026-08-12, score unmoved on the 2026-09-15 re-read) · **AA Intelligence Index v4.3 44 at `high`** (read 2026-09-15), level with Kimi K3's 44 · **Terminal-Bench 4.0 #9 at 20.3% ± 3.1%** (official board, read 2026-09-15) · Terminal-Bench 3.0 rank 4, 26.5% — TB3.0 is a THIRD board, hosted off-site at frontierbench.ai, not comparable to 2.0 or 2.1 | candidate | 2026-08-14 | GA on Copilot **2026-08-14**, same plans and billing as 4.5. Listed in Copilot's picker 2026-09-02 (CLI 1.0.81, Pro account), context cap not recorded. Remaining scores (CursorBench 69.9, DeepSWE 65.9) are **xAI self-reported**, not independent |
| GPT-5.4 | Implementer | 2.50 / 15 (>272K: 5 / 22.50) | **vals.ai SWE-V 78.2** (read first-hand from the board's own data 2026-08-23) (row `GPT 5.4 (xhigh)`) · SWE-Pro public board 59.1 — co-#1 at xHigh effort (Scale, 2026-07-20) · Epoch SWE-V 76.9 | active (diversity verifier for non-OpenAI Cheap executors) | 2026-07-09 · benchmarked 2026-07-20 | Named in check.md's Family decorrelation, but barred while an OpenAI model holds the Copilot Cheap seat (GPT-5.6 Luna, from 2026-09-07). The board scores back the seat, not the pairing |
| GPT-5.3-Codex | Implementer | 1.75 / 14 (cache-read 0.175) | vals.ai SWE-V 78.0 (independent, read 2026-09-15) | provisional (Copilot roster GA) | 2026-08-31 | On GitHub's supported-models table with no row here, added on the same coverage reasoning as DeepSeek — but unlike DeepSeek, this one is dispatchable. No vendor benchmark, and a single independent board read (vals.ai SWE-V 78.0, 2026-09-15) is not a classification, so provisional and never a floor without a trial |
| GPT-5.4 mini | Mechanical | 0.75 / 4.50 (cache-read 0.075) | vals.ai SWE-V 73.0 (independent, read 2026-09-15) | provisional (Copilot roster GA) | 2026-08-31 | Matches Gemini 3.6 Flash on input and cache-read but costs 4.50 out against 3.75. Its exact price twin was the now-retired MAI-Code-1-Flash. Classify provisional and trial before any floor move |
| GPT-5.4 nano | Mechanical | 0.20 / 1.25 (cache-read 0.02) | vals.ai SWE-V 69.8 (independent, read 2026-09-15) | provisional (Copilot roster GA) | 2026-08-31 | Undercuts GPT-5 mini on both axes and ties GPT-5.6 Luna's cache-read, but Luna keeps the cheapest-output title (1.20 vs 1.25), so the registry's cheapest-Copilot-model claim survives. Its 69.8 sits above Haiku 4.5's 66.6 at a fifth of Haiku's input price |
| GLM-5.3 | Implementer | 1.40 / 4.40 (cache-read 0.26 — a 0.19× ratio; cache storage limited-time free) | AA Intelligence Index v4.3 **45 (max), #1 open-weights, one point above Kimi K3** (read 2026-09-15) · vendor card: CyberGym 84.5% ahead of Mythos 5 (83.8) and GPT-5.6 Sol (83.6), TB3.0 4.6→28.3 SOTA-open, +50% over GLM-5.2 on Z.ai Code Bench · **vals.ai SWE-V 95.4** (independent, read 2026-09-15) · **Terminal-Bench 4.0 #5 at 41.8% ± 3.2%** (official board, read 2026-09-15) | candidate | 2026-08-31 | Z.ai flagship since 2026-08-14, same base model as GLM-5.2 with post-training gains; 753B / 40B active, 1M ctx / 128K out, text-only input, reasoning always on (low/high/max — **cannot be disabled**). Priced below Sonnet 5 on both axes. Z.ai's flagship, and ZCode's native model. Plan credit multiplier 6.9/1.7/24. Top-of-open-weights at an Implementer price is the Grok 4.5 shape: deliberate trial, T-record before any floor move |
| GLM-5.2 | Implementer | 1.40 / 4.40 (cache-read 0.26) — identical to GLM-5.3 and GLM-5.1 | vals.ai SWE-V 82.8 (independent, read 2026-09-15) · TB2.1 81.0 vendor ("within a few points of Claude Opus 4.8 at 85.0") · AA Intelligence Index v4.3 **34 (max)**, still on the open-weights table (read 2026-09-15) — the 2026-08-31 "delisted" read had matched only the top-12 chart | active (API-distinct only) | 2026-08-31 | Previous flagship, 753B, 1M ctx / 128K out. **On current GLM Coding Plans, requests for GLM-5.2 and GLM-5.1 auto-route to GLM-5.3, and GLM-4.7 to GLM-5.3-Flash** (devpack overview, read 2026-08-31, re-read 2026-09-15), so the model is distinct only on the API. A pinned slot still naming it silently serves 5.3 on the plan |
| GPT-5.6 Terra | Reasoning | **2 / 12** (cache-read 0.20; >272K: 4 / 18) | **vals.ai SWE-V 95.4** (read first-hand from the board's own data 2026-08-23), fourth on the Copilot roster behind Opus 5, Sol and Grok 4.6 — this file had NO vals.ai figure for it · TB2.1 78.4 — official board, rank 6 (first published numbers, 2026-07-20; vendor SWE-Pro 63.4, AA Coding Index 77) | active (cross-family verifier, Copilot) | 2026-07-12 · benchmarked 2026-07-20 · **repriced 2026-08-12** | **Cut 20% on both axes** from 2.50 / 15 (OpenAI pricing page + GitHub billing agree). **This dissolves the registry's own cost argument:** Terra's list price is now *exactly* Gemini 3.1 Pro's, 2 / 12 default and 4 / 18 long-context, on both axes. T18's finding that Terra costs ~2× Gemini was measured at the old price and no longer follows from list rates — re-measure before treating either as the cost-sensitive default. The quality half of T18 (ties on seeded recall, more thorough on non-seeded defects) is unaffected. Slug `gpt-5.6-terra` |
| Haiku 4.5 | Mechanical | 1 / 5 | **vals.ai SWE-V 66.6** (read first-hand from the board's own data 2026-08-23), row `claude-haiku-4-5-...-thinking` — correcting the unsourced **~73** | default (mechanical floor) | 2026-07 | Silent-failure risk — only ever behind smartcheck. Sole holder of the Cheap tier, no effort dial, nearest retirement horizon in the lineup, and the worst cache floor: see § Notes below. Copilot Cheap and scout seats moved to GPT-5.6 Luna 2026-09-07; Haiku stays the Claude Code Cheap floor (Luna is not on that harness) and the documented Copilot fallback. |
| GPT-5 mini | Mechanical | 0.25 / 2 (cache-read 0.025, no cache-write line; **metered per token under AI credits** — the "included"/0x status was premium-request-era, which ended 2026-06-01; re-verified vs the live pricing page 2026-07-13, the development repo's claim ledger) | **vals.ai SWE-V 60.8** (read first-hand from the board's own data 2026-08-23) — the LOWEST score on the Copilot roster, correcting "no coding-suite placement published"; Arena creative writing #175 of 376 is the only public ranking and it is a writing board | candidate | 2026-07-13 | 4×/2.5× cheaper than Haiku, ~8× cheaper cache-read than promo Sonnet; first live trial 2026-07-12 (T16): mechanical leaf, first-shot pass, 5/5 hidden oracle, 1.2 cr = 39% of Haiku's class avg — the default PROBE workhorse; still n=1, floor unchanged pending more samples |
| GPT-5.6 Luna | Implementer | **0.20 / 1.20** (cache-read 0.02; Copilot long-context >200K: 0.40 / 1.80) | TB2.1 **75.7 on the official board, rank 9** (verified 2026-08-06) · vals.ai SWE-V 93.0 (2026-08-12, score unmoved on the 2026-09-15 re-read) | **default (Copilot coding-leaf floor + scout seat, from 2026-09-07)** — behind the verifier. Held at the Cheap seat tier by price, though classed Implementer | 2026-07-09 (GA day) · **new price first recorded 2026-08-12** · prioritized 2026-08-20 | **Cut 5× on both axes** from 1 / 6 (OpenAI model page + GitHub billing agree). That makes it the **cheapest Copilot-dispatchable model in this registry on both axes**, tied with MAI-Code-1.1-Flash and under GPT-5 mini's 0.25 / 2, while scoring 93.0 on vals.ai SWE-V, far above anything else at its price. Promoted provisional → candidate on that pair of facts; trial it against Haiku 4.5 and GPT-5 mini before moving the floor. The repo's old "long-context recall collapses to 41%" line has **no primary source** — checked OpenAI's model page and the GPT-5.6 Preview System Card, neither carries it — so it is dropped rather than repeated  **Prioritized for Copilot coding 2026-08-20 at the author's direction.** The board case is strong: SWE-Verified 93.0 is *above* Sonnet 5's 79.6 while costing 0.20 / 1.20 against Sonnet's 2 / 10, roughly 10x cheaper in. What it did NOT have on 2026-08-20 was a trial in this repo's own corpus, so it stayed a first pick, not a floor, until the seat move recorded next **Reclassified Implementer and seated 2026-09-07** on the two independent boards (vals.ai SWE-V 93.0 above Sonnet 5's 79.6; TB4.0 17.3% above Sonnet 5's 12.4%), price unchanged, at the author's direction ("luna is so high value, we want to get the most out of luna"). `@smartplan-implementer-cheap` and `@smartplan-scout` pin it on Copilot; Sonnet 5 is the fail-twice target; the verifier stays cross-family (Gemini 3.6 Flash or Sonnet 5, never GPT-5.4 while an OpenAI model executes). Still no T-record in this corpus: a live bounce rate past ~20–30% is the reclassify-back trigger. |
| Kimi K3 | Mechanical | 3 / 15 (cache-read 0.30, the roster's usual 0.1× — Moonshot and GitHub agree) | vals.ai SWE-bench Verified **93.4** (score unmoved, re-read 2026-08-19). **The rank-5 claim is retired**: the board stated seven of 86 models at 95% or better on that read. The 2026-09-15 re-read carries 88 models with eight at 95.4 or above. So 93.4 is outside the board's leading group. Rank on this board is now churning faster than the score, so track the score and stop quoting a place · **AA Intelligence Index v4.3 44 (max), #2 open-weights** (read 2026-09-15). The **"#1 open-weights" half is retired**: GLM has since shipped **5.3 at 60**, tying it, so the 2026-08-12 note about displacing GLM-5.2 at 53 is two versions stale. Whether either holds the open-weights top spot was not resolvable at the board on 2026-08-19 and is deliberately left unclaimed rather than guessed. **Resolved 2026-08-31: the board showed Kimi K3 (max) and GLM-5.3 (max) tied at 60 at the top of the pre-v4.3 scale. On v4.3, read 2026-09-15, GLM-5.3 leads alone at 45 to K3's 44** | candidate (Copilot-selectable, dispatch-confirmed 2026-08-06; on the supported-models table as GA since CLI v1.0.79, 2026-08-10) | 2026-08-06 · re-checked 2026-08-12 | Shipped 2026-07-16. **Open weights HAVE now shipped** (`moonshotai/Kimi-K3` on Hugging Face, ~2026-07-27) — correcting this file's earlier "still unshipped" note. License is the bespoke **Kimi K3 License, not MIT**. 2.8T total / 104B activated. Priced 3 / 15, which is now *more* than Sonnet 5 rather than equal to it, since Sonnet 5 stayed at 2 / 10 — so the "Sonnet-5 money" framing is retired. Still a *candidate*, not a floor: trial against Haiku 4.5 first |
| GLM-5.3-Flash | Mechanical | **0.15 / 0.50** (cache-read 0.03, storage limited-time free) — the 50% launch promo ended 24:00 2026-09-09 UTC+8, list rate re-read 2026-09-15 | **vals.ai SWE-V 92.0** (independent, read 2026-09-15) · AA Intelligence Index v4.3 **42, #3 open-weights** (read 2026-09-15), three points off the leader at roughly a tenth of GLM-5.3's price | candidate | 2026-08-31 | Added to ZCode 3.9.2 (2026-08-26), "available out of the box for subscription users". 320B / 18B active MoE, multimodal in (video/image/text/file), 1M ctx / 128K out, first open frontier model combining sparse and linear attention, thinking cannot be disabled. Plan multiplier 2.3/0.56/8. The cheapest paid GLM-5 model on every axis. GLM-4.7-FlashX undercuts it on all three at 0.07 / 0.01 / 0.40. Plan requests for GLM-4.7 are served here (devpack overview, read 2026-09-15) |
| GLM-5-Turbo | Mechanical | **none published** — absent from every table on the API pricing page (re-read 2026-08-31); survives only in Coding Plan marketing | none — its card's scores are chart-image only | provisional (plan-only) | 2026-08-31 | 200K ctx / 128K out, text-only, positioned for the OpenClaw agent scenario (its card introduces ZClawBench). zcode.md's 1.20 / 0.24 / 4.00 row and the ledger row behind it were stale at the source — corrected in the same sweep |
| Qwen3.8-27B_Q4_K_M | Mechanical | **no per-token cost** — local GGUF: 18.9GB at Q4_K_M with MTP draft model + vision mmproj (the local install, 2026-08-29) | **vals.ai SWE-V 86.0** (independent, read 2026-09-15) · vendor card: SWE-bench Pro 61.7 · TB2.1 (Terminus) 73.0 · LiveCodeBench v6 90.3 · GPQA Diamond 89.2 · OSWorld-Verified 84.3 · AA Intelligence Index v4.3 **34 (xhigh)** (read 2026-09-15), below the 2.4T flagship's 40 | provisional (local candidate seat, not eval-gated) | 2026-08-31 | Alibaba's Qwen3.8-27B (Apache 2.0, shipped 2026-08-14): dense 27B multimodal, 262,144 native ctx extensible to 1M; family siblings are the 2.4T-A95B flagship (AA v4.3 40, tied 4th) and Flash-Next 180B. Run locally as an 18.9GB Q4_K_M GGUF it is a zero-marginal-cost Mechanical seat, and wherever one resident model serves every tier alias, the ladder collapses onto it. The hard floors apply: never plans, never merges unverified, and the ~30K real-agentic-ceiling precedent for 30B-class models stands until measured otherwise |
| DeepSeek V4 Pro 0813 | Unclassified | **0.66 / 1.98 off-peak, 1.32 / 3.96 peak** (cache-hit 0.022 / 0.044; peak = 01:00–04:00 and 06:00–10:00 UTC Mon–Fri, all else off-peak at half) — read 2026-08-16 (the development repo's claim ledger `deepseek-v4-peak-offpeak-0816`), re-read 2026-08-31 | vals.ai SWE-bench Verified **96.40, second overall** (read 2026-08-19), within 0.60 of Claude Opus 5's 97.00 · AA Intelligence Index v4.3 36 at `max` (read 2026-09-15) | **not Copilot-selectable — no seat** | 2026-08-19 | Added 2026-08-19 after a board re-read found it ranked second on SWE-bench Verified with **no row here at all**, in a registry that claims to track the cross-vendor field. Carried for board literacy, not as a candidate: it is absent from GitHub's supported-models table, so nothing in this family can dispatch to it. The gap between its SWE-bench placement (2nd) and its AA Intelligence Index (36 on v4.3, well outside the top ten) is itself the lesson — a single board is not a capability verdict. Priced as read 2026-08-31: at peak it still sits below Sonnet 5 on both axes. DeepSeek had scheduled the V4 Pro API to end 2026-09-14 and extended it indefinitely "in response to user demand" (pricing page, read 2026-09-15), so treat its availability as notice-driven |
| Kimi K2.7 Code | Mechanical | 0.95 / 4 (cache-read 0.19 — a 0.2× ratio, double the roster's usual 0.1×) | AA Intelligence Index v4.3 26 (read 2026-09-15, class median not re-read) · AA Coding Index 60.8 · MCPMark 81.1 (above Opus 4.8 76.4) — vendor/aggregator only; vals.ai SWE-V 78.2 (independent, read 2026-08-23) · Terminal-Bench absent (confirmed 2026-07-17) | provisional (Copilot CLI v1.0.68+, GA), retiring from Copilot 2026-10-02 (changelog 2026-09-03), successor Kimi K3 | 2026-07-13 · priced 2026-07-15 | First selectable open-weight Copilot model (Moonshot AI); Business/Enterprise off-by-default (admin enable). **vals.ai SWE-V 78.2** (read first-hand from the board's own data 2026-08-23), correcting "absent from every standard board"; Moonshot's own numbers trail GPT-5.5/Opus on nearly every cell. **Succession resolved 2026-08-06:** Kimi K3 (shipped 2026-07-16, API 3 / 15) **is now Copilot-selectable**, dispatch-confirmed, and the picker reports it at reasoning **High** where every other roster model shows Medium. It supersedes K2.7 Code here; don't start new K2.7-specific trials. Slug `kimi-k2.7-code` |
| MAI-Code-1-Flash | Mechanical | 0.75 / 4.50 (cache-read 0.075) | vendor card only (Microsoft-run, Copilot VS Code harness, read 2026-09-15): SWE-bench Verified 71.6 · TB2.1 51.7 · **absent from vals.ai's 86-model board 2026-08-23 — no Microsoft model appears on it at all** — failed independent logic tests against same-price peers | **RETIRED from Copilot 2026-09-10** (deprecation history, read 2026-09-15) | 2026-07-15 · deprecation noted 2026-08-12 | Microsoft's first first-party code model on the roster. **GitHub announced its deprecation 2026-08-11 and it retired across all Copilot experiences on 2026-09-10** (changelog, confirmed 2026-09-15), with MAI-Code-1.1-Flash named as the successor. Note the knock-on — the 2026-07-31 notice had named *this* model as Raptor mini's replacement, so that migration path is now two hops. Don't start new trials here |
| MAI-Code-1.1-Flash | Mechanical | 0.20 / 1.20 (cache-read 0.02, published 2026-08-31) | vendor card (Microsoft-run, Copilot VS Code harness, read 2026-09-15): SWE-bench Verified 72.6 · TB2.1 62.9 · **absent from vals.ai's board 2026-08-23, same as its predecessor, and still no Microsoft row at 88 models on 2026-09-15** | provisional (Copilot roster GA, confirmed 2026-08-19; successor to MAI-Code-1-Flash) | 2026-08-12 · re-checked 2026-08-19 | Named by GitHub as MAI-Code-1-Flash's replacement ahead of the 2026-09-10 retirement. Priced at GPT-5.6 Luna's rate on all three axes (0.20 / 1.20 / 0.02, read 2026-08-31), with vendor-only benchmarks and no independent board entry — classify provisional and trial deliberately, never as a floor |
| Gemini 3.5 Flash | Mechanical | 1.50 / 9 (cache-read 0.15) | SWE-bench Verified 78.8, rank 6 (independent) · MCP Atlas 83.6 · TB2.1 74-76 · SWE-bench Pro 55.1 | provisional (Copilot roster, GA), retiring from Copilot 2026-10-02 (changelog 2026-09-03), successor Gemini 3.8 Flash | 2026-07-15 | Target of CLI v1.0.69's `minimal` reasoning-effort support; above Haiku on both axes — not a cheap-floor play. Superseded by 3.6 Flash (below) for new trials |
| Gemini 3.6 Flash | Implementer | **0.75 / 3.75** (promotional through 2026-12-31, footnote `gemini-flash-promo`; cached in 0.075). **Google now prints what follows: 1.50 / 7.50, cache 0.15 and storage 1.00/hr, from 2027-01-01 — a 2× step on every axis** | **vals.ai SWE-V 79.6** (read first-hand from the board's own data 2026-08-23), its own score at last — the inherited-from-3.5 read is retired; vendor claims ~17% fewer output tokens (AA Index), up to 65% on DeepSWE | **former cross-family verifier (2026-08-16 to 2026-09-16)**, retiring from Copilot 2026-10-02 (changelog 2026-09-03), GitHub names Gemini 3.8 Flash | 2026-07-24 | 3.5 Flash's successor at cheaper output (vendor claims ~17% fewer output tokens on top); Business/Enterprise need admin enable. **Repriced 2026-08-14: at 0.75 / 3.75 it now sits BELOW Haiku 4.5 (1 / 5) on both axes**, which reverses this row's former "still above Haiku input price" reasoning — the price objection is gone, and as of 2026-08-23 so is the quality objection — vals.ai SWE-V 79.6 is its own independent read. What's thin now is this repo's own corpus: T34's 8/8 and T30's n=1. First trial 2026-07-25 (T30): mechanical leaf, first-shot pass, 6.5 cr — no price case vs GPT-5 mini's 1.2 cr class figure at the OLD price; n=1, worth re-running at the new one. **Took the cross-family verifier seat 2026-08-16** when Copilot retired Gemini 3.1 Pro; T34 cleared it at 8/8 recall first, and the 2026-08-14 reprice means the seat also got cheaper. Promo expiry 2026-12-31 is a re-check trigger (gate-readable marker lives in the development repo's claim ledger) **Reclassified Implementer 2026-09-07:** this row holds the cross-family verifier seat while § The classes says Mechanical never verifies, so the class cell contradicted the seat; its own vals.ai SWE-V 79.6 matches Sonnet 5's, which supports the move rather than driving it. |
| Gemini 3.7 Flash | Mechanical | **0.75 / 3.75** (cached in 0.075; the same `gemini-flash-promo` footnote as 3.6 Flash, through 2026-12-31 — read 2026-08-22, correcting this row's "not yet published"; the same printed 2× step from 2027-01-01 as 3.6) | **vals.ai SWE-V 80.8** (read first-hand from the board's own data 2026-08-23), one point above 3.6 Flash at an identical price · **Terminal-Bench 4.0 #14 at 11.2% ± 2.4%** (official board, read 2026-09-15), below Sonnet 5's 12.4% even though it sits above Sonnet 5 on vals.ai | provisional (Copilot roster GA since 2026-08-13) | 2026-08-19 | Added to GitHub's supported-models table 2026-08-13 (GitHub changelog, same date), GA on arrival. 3.6 Flash's successor. Priced identically to 3.6 Flash and one vals.ai point above it, which is inside the noise of a single board and not a reason to move the seat. Do NOT move it on version number alone — 3.6 got the seat by clearing T34 at 8/8 recall, and nothing equivalent has been run for 3.7 |
| Gemini 3.8 Flash | Implementer (provisional) | **0.75 / 3.75** (cache-read 0.075, the same `gemini-flash-promo` footnote as 3.6 and 3.7 Flash through 2026-12-31, then 1.50 / 7.50 from 2027-01-01) | **vals.ai SWE-V 80.0** (independent, read 2026-09-15) · **Terminal-Bench 4.0 #10 at 19.1% ± 3.4%** (official board, read 2026-09-15), above GPT-5.6 Luna's 17.3% · AA Intelligence Index v4.3 41 at `high` | **default (cross-family verifier pin, from 2026-09-16), unmeasured** · Copilot GA 2026-09-03, every paid plan including plain Pro | 2026-09-15 | GitHub's named successor for both Gemini 3.5 Flash and Gemini 3.6 Flash when they leave Copilot on 2026-10-02, and the cross-family verifier seat moved here from 3.6 Flash on 2026-09-16, at the author's direction, ahead of that retirement. Same price as 3.6 and 3.7 Flash under the same footnote. The seat moved to 3.6 only after T34 cleared it at 8/8 seeded recall. This pin has had no such trial, because the account is on Copilot Free, so run T34 here before trusting it on a shared-blind-spot leaf. Class is provisional until it does |

Cross-vendor prices/benchmarks with full sourcing: `copilot.md`'s table
(Copilot SKUs) and the development repo's claim ledger. Anthropic lineup,
strongest → cheapest: Fable 5.1 = Mythos 5.1 (invite only) > Fable 5 (legacy)
= Mythos 5 (limited, not a seat) > Opus 5 = Opus 4.8 > Sonnet 5 > Haiku 4.5.
`=` marks an identical list price. Where price ties, as it does across the
four 10 / 50 rows, the `>` steps read as capability.

## Notes

*Anthropic rows re-verified 2026-09-15 against the pricing, models-overview,
deprecations, effort and prompt-caching docs, plus the Fable 5.1 and Opus 5
what's-new pages.*

- **Two Copilot-selectable models have no row here** (release-status YAML
  re-read 2026-09-15, after a live roster read 2026-09-02 on CLI 1.0.81, Pro
  account — availability is per-plan, so treat a picker read as one seat's
  view rather than general availability): `claude-opus-4.7`, itself retiring
  from Copilot 2026-10-02, and `claude-opus-4.8-fast`. The four others listed
  here until 2026-09-15 (`gemini-3.7-flash`, `grok-4.6`, `mai-code-1.1-flash`,
  `gpt-5.4-mini`) all took rows between 2026-08-12 and 2026-08-31,
  `claude-fable-5.1` was seated 2026-09-07 from a first-hand pricing read, and
  GPT-6 Astra and Gemini 3.8 Flash took rows on 2026-09-15. **None is seated
  until researched.** The registry's default-vs-candidate discipline exists
  exactly so a new slug cannot be routed to on sight.
- **The 2026-09-01 Copilot retirement completed.** The same read confirms
  Opus 4.5, Opus 4.6, Sonnet 4.5, Sonnet 4.6, Gemini 3.1 Pro and Raptor mini
  are all gone from the picker, though GitHub's plan table still lists Sonnet
  4.6 for individual annual Pro and Pro+ subscribers (read 2026-09-15), so
  that one reads as account-scoped rather than withdrawn. The Gemini 3.1 Pro
  row above is retained as a retirement record, not a routing option.
- **Terminal-Bench 4.0 replaced 2.1, and it reorders the field.** Read in a
  browser 2026-09-02 and re-read 2026-09-15 (the table renders client-side and
  returns nothing to a plain fetch). Resolution rate ± 95% CI, agent in
  parens, 14 rows as of the 2026-09-15 read. Every carried score and cost is
  unchanged since 2026-09-02. Two arrivals pushed the field down:

  | # | Model | Agent | Rate | Cost |
  |---|---|---|---|---|
  | 1 | **GPT-6 Astra** (max) | Codex | **58.2% ± 2.8%** | $3.3k |
  | 2 | **Fable 5.1** (max) | Claude Code | 57.9% ± 3.8% | $6.2k |
  | 3 | **Opus 5** (max) | Claude Code | 51.8% ± 3.4% | $6.0k |
  | 4 | Fable 5 (max) | Claude Code | 44.5% ± 3.8% | $7.3k |
  | 5 | **GLM-5.3** (max) | Claude Code | 41.8% ± 3.2% | **$2.7k** |
  | 6 | GPT-5.6 Sol (max) | Codex | 37.3% ± 3.8% | $2.5k |
  | 7 | Opus 4.8 (max) | Claude Code | 23.6% ± 3.6% | $6.5k |
  | 8 | GPT-5.6 Terra (max) | Codex | 21.5% ± 3.3% | $1.7k |
  | 9 | **Grok 4.6** (high) | Grok Build | 20.3% ± 3.1% | $3.6k |
  | 10 | Gemini 3.8 Flash (high) | mini-SWE-agent | 19.1% ± 3.4% | $1.8k |
  | 11 | GPT-5.6 Luna (max) | Codex | 17.3% ± 2.8% | $0.3k |
  | 12= | Grok 4.5 (high) | Grok Build | 12.4% ± 2.6% | $2.1k |
  | 12= | **Sonnet 5** (max) | Claude Code | 12.4% ± 3.1% | $9.6k |
  | 14 | Gemini 3.7 Flash (high) | mini-SWE-agent | 11.2% ± 2.4% | $1.3k |

  **Two claims in the rows above were false and are marked stale there:**
  Opus 5 has a board entry (#1 on 2026-09-02, #3 on 2026-09-15), and GPT-5.6
  Sol has one (#4 then, #6 now) — both were recorded here as absent. **The
  spread also widens sharply**: on TB2.1 Sonnet 5 sat ~4 points behind Opus
  4.8 and ~9 behind the leader. On 4.0 it is at *a quarter* of Opus 5's rate
  and ties Grok 4.5 for 12th. A harder benchmark separates the tiers this
  family routes between far more than 2.1 did, which strengthens the
  implementer-floor argument rather than weakening it. Every TB2.1 figure in
  the rows above is **historical**.
- **GLM-5.3 is the cost story on that board** — 41.8% at $2.7k against Opus
  5's 51.8% at $6.0k, and Sonnet 5's 12.4% at $9.6k. Not a seat change on one
  board read, but the cheapest credible planner-class result recorded here.
- **vals.ai SWE-bench Verified, full order read in a browser 2026-09-02 and
  re-read 2026-09-15** (board updated 9/1/2026, 88 models, rows ranked by
  total tasks resolved). Top 12, unchanged across both reads:
  Opus 5 · **DeepSeek V4 Pro 0813** · GPT-5.6 Sol · **Grok 4.6** · GPT-5.6
  Terra · GLM 5.3 · Fable 5 · Kimi K3 · GPT-5.6 Luna · GLM 5.3 Flash ·
  DeepSeek V4 Flash 0731 (since retired by DeepSeek) · Opus 4.8. Sonnet 5
  sits **25th** on the 2026-09-15 read, behind a new Gemini 3.8 Flash at 24th. Overall
  percentages confirmed on this read: Opus 5 97.00, DeepSeek V4 Pro 96.40,
  Kimi K3 93.40, Opus 4.8 88.60, Grok 4.5 86.60.
- **Four unseated models now have board positions**, which is what turns them
  from roster noise into a real gap: **Grok 4.6** is 4th here and 9th on TB
  4.0 — above GPT-5.6 Terra, GLM 5.3 and Fable 5 on this board — while
  **DeepSeek V4 Pro 0813** is 2nd and carries only an unseated,
  non-dispatchable row here. **Opus 4.7** (21st), the one still without a row,
  and **Gemini 3.7 Flash** (23rd) both sit above Sonnet 5. None is seated on a
  board read alone. The point is that the registry's ordering no longer
  matches the evidence.
- **Scale's SWE-bench Pro board re-read 2026-09-02, and it moved host** to
  `labs.scale.com` (the old `scale.com/leaderboard/...` now 308s). Gemini 3.1
  Pro holds **46.10 ± 3.60, rank 5**, unchanged. The absence of Opus 4.8,
  Opus 5, GPT-5.5 and GPT-5.6 is re-confirmed — so the 69.2 and 58.6 figures
  carried here stay marked vendor-only. One drift, re-read 2026-09-15: the board ranks by upper
  CI bound (Rank (UB)). So ties share a place. `claude-opus-4-6 (thinking)`
  reads **rank 3**, tied with `Muse Spark` at 55.00, while the new `Muse Spark
  1.1` at 61.50 shares rank 1 with `gpt-5.4`. The 2026-09-02 read recorded it
  as rank 4.
- **Artificial Analysis moved to Intelligence Index v4.2, then v4.3, in
  September 2026** (methodology page, read 2026-09-15). v4.3 swapped
  Terminal-Bench 2.1 for 4.0 and τ³-Banking for AutomationBench-AA. Every
  model re-scored far lower: the overall top is now 53. Every AA figure in
  this file dated before 2026-09-15 is on the retired scale and does not
  compare with a v4.3 read.
- **The 5:2:1 ladder is list price, not effective cost.** Fable 5.1, Fable 5, Mythos 5.1,
  Mythos 5, Opus 5, Opus 4.8 and Sonnet 5 use the newer tokenizer (~30% more tokens for the same
  text); **Haiku 4.5 is the only Anthropic row here still on the old one**. So
  on identical source text the real Opus:Haiku multiple is nearer **6.5:1**
  than 5:1, and Sonnet:Haiku nearer 2.6:1. Anything
  that price-weights across tiers — the benchmark **W** unit included — is
  understating the cheap tier's advantage. Derived from two vendor-stated
  facts, not vendor-stated itself.
- **Seating an Opus 5 leaf — five operational facts** (researched
  2026-08-06, the development repo's research notes). None of these
  are benchmark facts and all five present as "the model got worse":
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
- **The ladder is 5:2:1 and stays there.** Opus:Sonnet:Haiku is exactly
  5:2:1 on both axes. Anthropic cancelled the scheduled Sonnet 5 increase on
  2026-08-10 — the release note reads "the previously scheduled increase to
  $3 / $15 per MTok on September 1, 2026 will not occur" — so the
  Opus→Sonnet multiple stays 2.5×, down-tiering keeps its full saving, the
  fan-out break-even does not move out, and the benchmark corpus's
  W = 5·Opus + 2·Sonnet + 1·Haiku remains a **live** unit rather than
  expiring. Write "standard price", not "permanent": the vendor retired the
  schedule, it did not promise the rate never moves again.
  <!-- claim:sonnet5-standard-price -->
- **Effort is a second dial this table has no column for.** Full
  low/medium/high/xhigh/max on Fable 5.1, Fable 5, Mythos 5.1, Mythos 5,
  Opus 5, Opus 4.8, Opus 4.7 and Sonnet 5. `xhigh` is missing on Opus 4.6 and
  Sonnet 4.6. Opus 4.5 takes effort with neither `xhigh` nor `max`. **Haiku 4.5 and
  Sonnet 4.5 have no effort dial at all**, so a Mechanical-class seat's only
  lever is the size of the brief you hand it.
- **The Cheap tier rests on one model.** Haiku 4.5 holds the Mechanical
  floor alone, has no announced successor, and carries the nearest
  retirement horizon in the lineup: not sooner than 2026-10-15 (floor re-read
  2026-09-15), about four weeks out. No deprecation notice had posted by that
  read. The 60-day notice commitment means it cannot retire on
  Anthropic-operated platforms before about 2026-11-14 at the earliest. Retirements do
  land. `claude-opus-4-1-20250805` retired on 2026-08-05. The safer shape is
  to write the policy in tier **aliases** plus an effort dial rather than
  pinned model IDs, so a floor swap is one edit here instead of a sweep.
- **The cache floor isn't monotonic, and it's worst on the cheap tier.**
  Minimum cacheable prefix: 512 tokens on Fable 5.1, Mythos 5.1, Opus 5,
  Fable 5 and Mythos 5, 1,024 on Opus 4.8 and Sonnet 5, **4,096 on Haiku 4.5**. Below the floor nothing caches
  and no error comes back. A brief that caches on the planner can silently
  fail to cache on a Haiku executor at eight times the floor, so prove a
  miss by checking that both `cache_creation_input_tokens` and
  `cache_read_input_tokens` are 0.
