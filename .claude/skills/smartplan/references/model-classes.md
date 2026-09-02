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
| **Implementer** | Mid | Implementer floor (briefed/correctness-sensitive) · verifier of Cheap leaves · small-plan planner (drop-on-fit) | Planning beyond drop-on-fit; mechanical leaves when a Mechanical-class model is available |
| **Mechanical** | Cheap | Mechanical, single-concern, verifier-checkable leaves via smartexec + smartcheck · scouting | Planning, verification (except fully scripted checks), correctness-sensitive leaves |
| **Script** | Script | Deterministic actions an existing script performs — zero model calls | Anything needing judgment |

## The registry

One row per model. Benchmark cells are vendor/system-card numbers unless
labeled otherwise — the official boards (swebench.com, Scale, tbench.ai)
run different harnesses, score lower across the board, and list few of
these models (checked 2026-07-20); compare within one source class.
`Status`: **default** (a seat's standing pick),
**active** (eligible, routinely used), **candidate** (eligible,
trialed deliberately before any floor moves), **provisional** (classified on
incomplete data — price-only or single benchmark), **planner-only** (never
implements or verifies).

| Model | Class | Price $/1M in/out | Key benchmark | Status | Classified | Note |
| --- | --- | --- | --- | --- | --- | --- |
| Fable 5 | Reasoning | 10 / 50 | TB2.1 83.8 — #1 on the official board (re-confirmed 2026-07-24) · vendor SWE-Pro 80.3 | planner-only | 2026-07 · benchmarked 2026-07-20 | Max tier: hardest architecture/decomposition decisions only; never a fail-twice target, never a verifier |
| Mythos 5 | Reasoning | 10 / 50 (cache-read 1.00; 5m write 12.50, 1h write 20; batch 5 / 25) | none published — absent from the boards this file tracks, and Anthropic publishes no benchmark for it | **not a seat — limited availability** | 2026-08-28 | Added 2026-08-28 after a sweep found the pricing page carries it and this registry did not, in a file whose own summary line claims to give the Anthropic lineup strongest to cheapest. Priced identically to Fable 5 on every axis including cache and batch. Gated behind a limited-availability programme rather than generally callable, so it is carried for lineup completeness, not as a candidate — the same reasoning that added the DeepSeek row. Uses the newer tokenizer (~30% more tokens for the same text), so its effective cost sits above Fable 5's at the same list rate. `caching.md`'s minimum-cacheable-prefix table already knew about it, which is how the gap showed |
| Claude Opus 5 | Reasoning | 5 / 25 | **vals.ai SWE-bench Verified 97.0, rank 1** (board updated 2026-08-05, re-read 2026-08-06, ahead of GPT-5.6 Sol 96.2 and Fable 5 95.0); still no Terminal-Bench official-board entry as of 2026-08-06 (TB2.1 unchanged since its 07-11 snapshot) | **default (planner + Strong verifier)** | 2026-07-25 · promoted 2026-08-05 | Same price as Opus 4.8. As of 2026-08-05 Anthropic lists it Active/current and the default on Max, Team Premium, Enterprise PAYG and the Claude API, with 4.8 moved under Legacy on the overview page. **Promoted on that evidence, not on benchmarks** (none had landed as of 2026-08-05), because a same-class same-price up-move is what § How to edit calls cheap to be wrong about, and the predecessor is now the vendor's legacy row. Revisit if the first board entry lands below 4.8. On Claude Code ≥2.1.219 the `opus`/`default` aliases — and opusplan's plan phase — resolve to it. Copilot CLI-selectable since v1.0.75 (Pro+/Max-gated); T30 (07-25) saw it serve where 4.8 was Pro-gate-refused on 07-11 |
| Opus 4.8 | Reasoning | 5 / 25 | **vals.ai SWE-V 88.6** confirmed (read first-hand from the board's own data 2026-08-23) — note the board carries a SECOND row under the identical label, `claude-opus-4-8-claude-code` at 85.8 · SWE-bench Pro 69.2 **(vendor — absent from Scale's public board, checked 2026-08-12)** · SWE-bench Verified 88.6 · TB2.1 78.9 — official board #5 (2026-07-24) | active (same-price fallback) | 2026-07-09 · demoted from default 2026-08-05 | Held the planner + Strong verifier default 07-09 → 08-05 on price + SWE-bench (GPT-5.5 edges it on TB2.1, 83.1 vs 78.9, but is Pro-gated and pricier on output). **Succession resolved 2026-08-05:** Opus 5 takes the default at identical price. 4.8 stays Active and costs the same, so it's the drop-in fallback when an Opus 5 seat is unavailable. Retire not before 2027-05-28 |
| GPT-5.5 | Reasoning | 5 / 30 (>272K: 10 / 45) | **vals.ai SWE-V 82.6** (read first-hand from the board's own data 2026-08-23) — the board carries two more rows under the same display label, codex 76.4 and factory 76.2 · SWE-bench Pro 58.6 **(vendor — absent from Scale's public board, checked 2026-08-12)** · TB2.1 83.1 — official board #2 (2026-07-24) | Pro-plan-gated on Copilot | 2026-07-09 · refined 2026-07-20 | **Refined 2026-07-20 (supported-models):** still GA and CLI-selectable, but Pro = Not included — which is why T18's Pro-roster observation missed it. (The supported-models page dropped its per-plan column before 2026-08-28, so that source is spent; re-derive gating from get-started/plans at the next sweep.) Flagship-superseded by the GPT-5.6 family; on Pro the live cross-family peer is GPT-5.6 Terra |
| GPT-5.6 Sol | Reasoning | **2 / 10 promotional on GitHub's table through 2026-09-03** (>272K: 4 / 15) — **the primaries disagree on the expiry: OpenAI's own pages say "at least through November 21, 2026"** (read 2026-08-28). Standard **4 / 20 (>272K: 8 / 30) is a printed OpenAI figure** (2026-08-28), vindicating the 2026-08-22 arithmetic it was derived by. Past 272K bills the **WHOLE request** at 2× input / 1.5× output — a cliff, not a marginal tier (model page) | TB2.1 88.8 vendor-only — still absent from the official board (re-checked 2026-07-24); vals.ai SWE-V 96.2 (independent, not the official board) | provisional (Copilot-exposed) | 2026-07-09 (GA day) · re-researched 2026-07-20 | Pro+-gated. Elite agentic scores but measured weak on open-brief architecture (Every 56/100 vs Fable 90) and METR's highest eval-gaming rate — never grades work against visible tests; not a planner swap. Full caution set: the model guide |
| Gemini 3.1 Pro | Reasoning | 2 / 12 (>200K: 4 / 18) | **vals.ai SWE-V 78.8** (read first-hand from the board's own data 2026-08-23) (row `Gemini 3.1 Pro Preview (02/26)`) · SWE-bench Pro **46.1, rank 5 (Scale public board)** · TB2.1 65.8 — official board **rank 14**, tied with Gemini 3 Pro also at 14, next row skips to 16 (re-read 2026-08-12) | **RETIRING from Copilot 2026-09-01 — seat handed to Gemini 3.6 Flash** | 2026-07-12 · corrected 2026-08-12 | **MEASURED (T18): ties GPT-5.6 Terra on seeded C++ recall (14/15 each over 2 fixtures) at 47% the cost (8.69 vs 18.53 cr), esp. UE5.** **Two corrections from the 2026-08-12 board re-read:** the old "SWE-bench Pro 54.2" appears nowhere on Scale's board (which says 46.1) and was an unlabelled vendor figure reading as board-sourced; and the TB2.1 rank is 14, not 15 — this file's own 2026-07-20 ledger row had it right and the 2026-08-06 pass introduced the error. **The cost case needs re-measuring:** Terra repriced to an identical 2 / 12, so this seat's list-price advantage over Terra is gone. Slug `gemini-3.1-pro-preview`. Never a planner swap. **Seat vacated 2026-08-16:** Copilot retires this model 2026-09-01 and T34 (2026-08-05) cleared Gemini 3.6 Flash as the successor at 8/8 recall on the seeded custom fixture, cost indistinguishable. All routing sites (`check.md`, `cpp-gamedev-check.md`, `copilot.md`, the Copilot verifier seat) now name 3.6 Flash. Anthropic-side and other harnesses are unaffected by the Copilot retirement date. Added 2026-08-31: GitHub's roster listed it as **Public preview, never GA** — the only non-Anthropic model on the 31-row roster in that state, retired straight out of preview, which contextualizes why the seat went to a GA model (3.6 Flash) rather than a same-model upgrade |
| Sonnet 5 | Implementer | 2 / 10 | **vals.ai SWE-V 79.6** (read first-hand from the board's own data 2026-08-23) — correcting **85.2**, which appears nowhere on that board for Sonnet 5 in any subset, and which this file had carried unsourced · TB2.1 74.6 — official board #10 (2026-07-24) | default (implementer floor + Cheap-leaf verifier) | 2026-07-09 · repriced 2026-08-12 | ~9 pts behind Opus 4.8 on vals.ai SWE-V (79.6 vs 88.6), ~17 behind Opus 5 — the floor argument. **The $2/$10 introductory rate became Anthropic's standard price on 2026-08-10**; the 2026-09-01 step to $3/$15 was cancelled and will not occur. GitHub's billing page dropped the promotional footnote by 2026-08-31, so the $2/$10 now reads unqualified standard on both vendors <!-- claim:sonnet5-standard-price --> |
| Grok 4.5 | Implementer | 2 / 6 · **past 200K bills 4 / 12 on the WHOLE request** (a cliff, not a marginal tier) · cached in 0.50 (1.00 long tier) | Terminal-Bench 2.1 **rank 4, 79.3%** (read 2026-08-14) — above Opus 4.8's 78.9 at a fifth of Opus's output price · vals.ai SWE-bench Verified 86.60, rank 10 | candidate | 2026-08-14 | GA on Copilot since **2026-07-28**, every paid plan **including plain Pro**. Billing: input and output match xAI list, but **cached input does not** — GitHub bills 4.5 at 0.50 / 1.00 against xAI list 0.30 / 0.60, while 4.6 matches at both sources (re-read 2026-08-31), so this row's cache figures are what a Copilot dispatch pays, not xAI list. 500K native; the picker read 328K on 2026-08-06 and GitHub publishes no per-model picker cap, so the two numbers measure different things. xAI runs these directly with no logging, no disk write and no retention of any kind — stricter than Fable 5's 30-day safety-classifier retention. Business/Enterprise admin-enable, off by default. **Boards put it in Reasoning territory at an Implementer price**, which is the shape that earns a deliberate trial, not a default |
| Grok 4.6 | Implementer | 2 / 6 · past 200K 4 / 12 whole-request · cached in 0.50 (1.00 long tier) | vals.ai SWE-bench Verified **95.60** (entered 2026-08-12; rank not re-confirmed 2026-08-19, the board table truncated on fetch) · **Artificial Analysis Intelligence Index 61 at `high`** (read 2026-08-19), above Kimi K3's 60 · Terminal-Bench 3.0 rank 4, 26.5% — TB3.0 is a THIRD board, hosted off-site at frontierbench.ai, not comparable to 2.0 or 2.1 | candidate | 2026-08-14 | GA on Copilot **2026-08-14**, same plans and billing as 4.5. Picker context cap never read: the last picker read predates its arrival. Remaining scores (CursorBench 69.9, DeepSWE 65.9, AA Index 61) are **xAI self-reported**, not independent |
| GPT-5.4 | Implementer | 2.50 / 15 (>272K: 5 / 22.50) | **vals.ai SWE-V 78.2** (read first-hand from the board's own data 2026-08-23) (row `GPT 5.4 (xhigh)`) · SWE-Pro public board 59.1 — co-#1 at xHigh effort (Scale, 2026-07-20) · Epoch SWE-V 76.9 | active (Cheap-leaf diversity verifier on Copilot) | 2026-07-09 · benchmarked 2026-07-20 | Named in check.md's Family decorrelation — the board scores back the diversity-verifier seat |
| GPT-5.3-Codex | Implementer | 1.75 / 14 (cache-read 0.175) | none published | provisional (Copilot roster GA) | 2026-08-31 | On GitHub's supported-models table with no row here, added on the same coverage reasoning as DeepSeek — but unlike DeepSeek, this one is dispatchable. No published benchmark, so provisional and never a floor without a trial |
| GPT-5.4 mini | Mechanical | 0.75 / 4.50 (cache-read 0.075) | none published | provisional (Copilot roster GA) | 2026-08-31 | Sits at Gemini 3.6 Flash's exact price with no published benchmark; classify provisional, trial before any floor move |
| GPT-5.4 nano | Mechanical | 0.20 / 1.25 (cache-read 0.02) | none published | provisional (Copilot roster GA) | 2026-08-31 | Undercuts GPT-5 mini on both axes and ties GPT-5.6 Luna's cache-read, but Luna keeps the cheapest-output title (1.20 vs 1.25), so the registry's cheapest-on-both-axes claim survives |
| GLM-5.3 | Implementer | 1.40 / 4.40 (cache-read 0.26 — a 0.19× ratio; cache storage limited-time free) | AA Intelligence Index **60 (max) — tied #1 open-weights with Kimi K3** (re-read 2026-08-31) · vendor card: CyberGym 84.5% ahead of Mythos 5 (83.8) and GPT-5.6 Sol (83.6), TB3.0 4.6→28.3 SOTA-open, +50% over GLM-5.2 on Z.ai Code Bench · **no independent coding-suite entry** (absent from vals.ai's board) | candidate | 2026-08-31 | Z.ai flagship since 2026-08-14, same base model as GLM-5.2 with post-training gains; 753B / 40B active, 1M ctx / 128K out, text-only input, reasoning always on (low/high/max — **cannot be disabled**). Priced below Sonnet 5 on both axes. Z.ai's flagship, and ZCode's native model. Plan credit multiplier 6.9/1.7/24. Top-of-open-weights at an Implementer price is the Grok 4.5 shape: deliberate trial, T-record before any floor move |
| GLM-5.2 | Implementer | 1.40 / 4.40 (cache-read 0.26) — identical to GLM-5.3 and GLM-5.1 | TB2.1 81.0 vendor ("within a few points of Claude Opus 4.8 at 85.0") · **delisted from the AA open-weights board** (re-read 2026-08-31 — GLM-5.3 and 5.3-Flash are the only GLM rows left on it) | active (API-distinct only) | 2026-08-31 | Previous flagship, 753B, 1M ctx / 128K out. **On current GLM Coding Plans, requests for GLM-5.2 and GLM-5.1 auto-route to GLM-5.3** (devpack overview, read 2026-08-31), so the model is distinct only on the API. A pinned slot still naming it silently serves 5.3 on the plan |
| GPT-5.6 Terra | Reasoning | **2 / 12** (cache-read 0.20; >272K: 4 / 18) | **vals.ai SWE-V 95.4** (read first-hand from the board's own data 2026-08-23), third on the Copilot roster behind Opus 5 and Sol — this file had NO vals.ai figure for it · TB2.1 78.4 — official board, rank 6 (first published numbers, 2026-07-20; vendor SWE-Pro 63.4, AA Coding Index 77) | active (cross-family verifier, Copilot) | 2026-07-12 · benchmarked 2026-07-20 · **repriced 2026-08-12** | **Cut 20% on both axes** from 2.50 / 15 (OpenAI pricing page + GitHub billing agree). **This dissolves the registry's own cost argument:** Terra's list price is now *exactly* Gemini 3.1 Pro's, 2 / 12 default and 4 / 18 long-context, on both axes. T18's finding that Terra costs ~2× Gemini was measured at the old price and no longer follows from list rates — re-measure before treating either as the cost-sensitive default. The quality half of T18 (ties on seeded recall, more thorough on non-seeded defects) is unaffected. Slug `gpt-5.6-terra` |
| Haiku 4.5 | Mechanical | 1 / 5 | **vals.ai SWE-V 66.6** (read first-hand from the board's own data 2026-08-23), row `claude-haiku-4-5-...-thinking` — correcting the unsourced **~73** | default (mechanical floor) | 2026-07 | Silent-failure risk — only ever behind smartcheck. Sole holder of the Cheap tier, no effort dial, nearest retirement horizon in the lineup, and the worst cache floor: see § Notes below |
| GPT-5 mini | Mechanical | 0.25 / 2 (cache-read 0.025, no cache-write line; **metered per token under AI credits** — the "included"/0x status was premium-request-era, retired 2026-06-01; re-verified vs the live pricing page 2026-07-13, the development repo's claim ledger) | **vals.ai SWE-V 60.8** (read first-hand from the board's own data 2026-08-23) — the LOWEST score on the Copilot roster, correcting "no coding-suite placement published"; Arena creative writing #175 of 376 is the only public ranking and it is a writing board | candidate | 2026-07-13 | 4×/2.5× cheaper than Haiku, ~8× cheaper cache-read than promo Sonnet; first live trial 2026-07-12 (T16): mechanical leaf, first-shot pass, 5/5 hidden oracle, 1.2 cr = 39% of Haiku's class avg — the default PROBE workhorse; still n=1, floor unchanged pending more samples |
| GPT-5.6 Luna | Mechanical | **0.20 / 1.20** (cache-read 0.02; Copilot long-context >200K: 0.40 / 1.80) | TB2.1 **75.7 on the official board, rank 9** (verified 2026-08-06) · vals.ai SWE-V 93.0, rank 6 (2026-08-12) | **preferred first pick for Copilot coding leaves (author preference, 2026-08-20)** — still behind the verifier | 2026-07-09 (GA day) · **repriced 2026-08-12** · prioritized 2026-08-20 | **Cut 5× on both axes** from 1 / 6 (OpenAI model page + GitHub billing agree). That makes it the **cheapest model in this registry on both axes** — under GPT-5 mini's 0.25 / 2 — while scoring 93.0 on vals.ai SWE-V, far above anything else at the Mechanical end. Promoted provisional → candidate on that pair of facts; trial it against Haiku 4.5 and GPT-5 mini before moving the floor. The repo's old "long-context recall collapses to 41%" line has **no primary source** — checked OpenAI's model page and the GPT-5.6 Preview System Card, neither carries it — so it is dropped rather than repeated  **Prioritized for Copilot coding 2026-08-20 at the author's direction.** The board case is strong: SWE-Verified 93.0 (rank 6) is *above* Sonnet 5's 79.6 while costing 0.20 / 1.20 against Sonnet's 2 / 10, roughly 10x cheaper in. What it does NOT have is a trial in this repo's own corpus, so it is a first pick, not a floor: route coding leaves to it, keep every result behind the independent verifier exactly as any Cheap-tier output, and open a T-record before promoting it further |
| Kimi K3 | Mechanical | 3 / 15 (cache-read 0.30, the roster's usual 0.1× — Moonshot and GitHub agree) | vals.ai SWE-bench Verified **93.4** (score unmoved, re-read 2026-08-19). **The rank-5 claim is retired**: the board now states seven of 86 models reach 95% or better, so 93.4 sits no higher than 8th. Rank on this board is now churning faster than the score, so track the score and stop quoting a place · **Artificial Analysis Intelligence Index 60** (re-read 2026-08-19, unmoved). The **"#1 open-weights" half is retired**: GLM has since shipped **5.3 at 60**, tying it, so the 2026-08-12 note about displacing GLM-5.2 at 53 is two versions stale. Whether either holds the open-weights top spot was not resolvable at the board on 2026-08-19 and is deliberately left unclaimed rather than guessed. **Resolved 2026-08-31: the board now shows Kimi K3 (max) and GLM-5.3 (max) tied at 60 at the top** | candidate (Copilot-selectable, dispatch-confirmed 2026-08-06; on the supported-models table as GA since CLI v1.0.79, 2026-08-10) | 2026-08-06 · re-checked 2026-08-12 | Shipped 2026-07-16. **Open weights HAVE now shipped** (`moonshotai/Kimi-K3` on Hugging Face, ~2026-07-27) — correcting this file's earlier "still unshipped" note. License is the bespoke **Kimi K3 License, not MIT**. 2.8T total / 104B activated. Priced 3 / 15, which is now *more* than Sonnet 5 rather than equal to it, since Sonnet 5 stayed at 2 / 10 — so the "Sonnet-5 money" framing is retired. Still a *candidate*, not a floor: trial against Haiku 4.5 first |
| GLM-5.3-Flash | Mechanical | **0.075 / 0.25 promotional, list 0.15 / 0.50, ends 24:00 2026-09-09 UTC+8** (cache-read 0.015 promo / 0.03 list; storage limited-time free) | AA Intelligence Index **57 — #4 open-weights** (re-read 2026-08-31), three points off the tied leaders at roughly a tenth of GLM-5.3's price | candidate | 2026-08-31 | Added to ZCode 3.9.2 (2026-08-26), "available out of the box for subscription users". 320B / 18B active MoE, multimodal in (video/image/text/file), 1M ctx / 128K out, first open frontier model combining sparse and linear attention, thinking cannot be disabled. Plan multiplier 2.3/0.56/8. The cheapest paid GLM on output — GLM-4.7-FlashX still undercuts its promo input and cached rates at 0.07 / 0.01. The row should read 0.15 / 0.50 the day after the promo ends <!-- RECHECK:2026-09-09 --> |
| GLM-5-Turbo | Mechanical | **none published** — absent from every table on the API pricing page (re-read 2026-08-31); survives only in Coding Plan marketing | none — its card's scores are chart-image only | provisional (plan-only) | 2026-08-31 | 200K ctx / 128K out, text-only, positioned for the OpenClaw agent scenario (its card introduces ZClawBench). zcode.md's 1.20 / 0.24 / 4.00 row and the ledger row behind it were stale at the source — corrected in the same sweep |
| Qwen3.8-27B_Q4_K_M | Mechanical | **no per-token cost** — local GGUF: 18.9GB at Q4_K_M with MTP draft model + vision mmproj (the local install, 2026-08-29) | vendor card: SWE-bench Pro 61.7 · TB2.1 (Terminus) 73.0 · LiveCodeBench v6 90.3 · GPQA Diamond 89.2 · OSWorld-Verified 84.3 · AA Intelligence **52 (xhigh) — #6 open-weights** (re-read 2026-08-31) | provisional (local candidate seat, not eval-gated) | 2026-08-31 | Alibaba's Qwen3.8-27B (Apache 2.0, shipped 2026-08-14): dense 27B multimodal, 262,144 native ctx extensible to 1M; family siblings are the 2.4T-A95B flagship (AA 58, #3) and Flash-Next 180B. Run locally as an 18.9GB Q4_K_M GGUF it is a zero-marginal-cost Mechanical seat, and wherever one resident model serves every tier alias, the ladder collapses onto it. The hard floors apply: never plans, never merges unverified, and the ~30K real-agentic-ceiling precedent for 30B-class models stands until measured otherwise |
| DeepSeek V4 Pro 0813 | Unclassified | **1.32 / 3.96 peak, 0.66 / 1.98 off-peak** (cache-hit 0.044 / 0.022; peak = 01:00–04:00 and 06:00–10:00 UTC Mon–Fri, all else off-peak at half) — published since the 2026-08-19 "not published" read, re-read 2026-08-31 | vals.ai SWE-bench Verified **96.40, second overall** (read 2026-08-19), within 0.60 of Claude Opus 5's 97.00 · Artificial Analysis Intelligence Index 53 at `max` | **not Copilot-selectable — no seat** | 2026-08-19 | Added 2026-08-19 after a board re-read found it ranked second on SWE-bench Verified with **no row here at all**, in a registry that claims to track the cross-vendor field. Carried for board literacy, not as a candidate: it is absent from GitHub's supported-models table, so nothing in this family can dispatch to it. The gap between its SWE-bench placement (2nd) and its AA Intelligence Index (53, well outside the top ten) is itself the lesson — a single board is not a capability verdict. Priced as read 2026-08-31: at peak it still sits below Sonnet 5 on both axes |
| Kimi K2.7 Code | Mechanical | 0.95 / 4 (cache-read 0.19 — a 0.2× ratio, double the roster's usual 0.1×) | AA Intelligence 42 vs a 25 class median · AA Coding Index 60.8 · MCPMark 81.1 (above Opus 4.8 76.4) — vendor/aggregator only; SWE-bench and Terminal-Bench both absent, confirmed 2026-07-17 | provisional (Copilot CLI v1.0.68+, GA) | 2026-07-13 · priced 2026-07-15 | First selectable open-weight Copilot model (Moonshot AI); Business/Enterprise off-by-default (admin enable). **vals.ai SWE-V 78.2** (read first-hand from the board's own data 2026-08-23), correcting "absent from every standard board"; Moonshot's own numbers trail GPT-5.5/Opus on nearly every cell. **Succession resolved 2026-08-06:** Kimi K3 (shipped 2026-07-16, API 3 / 15) **is now Copilot-selectable**, dispatch-confirmed, and the picker reports it at reasoning **High** where every other roster model shows Medium. It supersedes K2.7 Code here; don't start new K2.7-specific trials. Slug `kimi-k2.7-code` |
| MAI-Code-1-Flash | Mechanical | 0.75 / 4.50 (cache-read 0.075) | none published (re-confirmed 2026-07-27; **absent from vals.ai's 86-model board 2026-08-23 — no Microsoft model appears on it at all**) — failed independent logic tests against same-price peers | **DEPRECATED — retires 2026-09-10** | 2026-07-15 · deprecation noted 2026-08-12 | Microsoft's first first-party code model on the roster. **GitHub announced its deprecation 2026-08-11: it goes away across all Copilot experiences on 2026-09-10**, with MAI-Code-1.1-Flash named as the successor. Note the knock-on — the 2026-07-31 notice had named *this* model as Raptor mini's replacement, so that migration path is now two hops. Don't start new trials here <!-- RECHECK:2026-09-10 --> |
| MAI-Code-1.1-Flash | Mechanical | 0.20 / 1.20 (cache-read 0.02, published 2026-08-31) | none published (2026-08-12; **absent from vals.ai's 86-model board 2026-08-23, same as its predecessor**) | provisional (Copilot roster GA, confirmed 2026-08-19; successor to MAI-Code-1-Flash) | 2026-08-12 · re-checked 2026-08-19 | Named by GitHub as MAI-Code-1-Flash's replacement ahead of the 2026-09-10 retirement. Priced at GPT-5.6 Luna's rate on all three axes (0.20 / 1.20 / 0.02, read 2026-08-31), with no published benchmark of any kind — classify provisional and trial deliberately, never as a floor |
| Gemini 3.5 Flash | Mechanical | 1.50 / 9 (cache-read 0.15) | SWE-bench Verified 78.8, rank 6 (independent) · MCP Atlas 83.6 · TB2.1 74-76 · SWE-bench Pro 55.1 | provisional (Copilot roster, GA) | 2026-07-15 | Target of CLI v1.0.69's `minimal` reasoning-effort support; above Haiku on both axes — not a cheap-floor play. Superseded by 3.6 Flash (below) for new trials |
| Gemini 3.6 Flash | Mechanical | **0.75 / 3.75** (promotional through 2026-12-31, footnote `gemini-flash-promo`; cached in 0.075). **Google now prints what follows: 1.50 / 7.50, cache 0.15 and storage 1.00/hr, from 2027-01-01 — a 2× step on every axis** | **vals.ai SWE-V 79.6** (read first-hand from the board's own data 2026-08-23), its own score at last — the inherited-from-3.5 read is retired; vendor claims ~17% fewer output tokens (AA Index), up to 65% on DeepSWE | **default (cost-sensitive cross-family verifier, from 2026-08-16)** | 2026-07-24 | 3.5 Flash's successor at cheaper output (vendor claims ~17% fewer output tokens on top); Business/Enterprise need admin enable. **Repriced 2026-08-14: at 0.75 / 3.75 it now sits BELOW Haiku 4.5 (1 / 5) on both axes**, which reverses this row's former "still above Haiku input price" reasoning — the price objection is gone, and as of 2026-08-23 so is the quality objection — vals.ai SWE-V 79.6 is its own independent read. What's thin now is this repo's own corpus: T34's 8/8 and T30's n=1. First trial 2026-07-25 (T30): mechanical leaf, first-shot pass, 6.5 cr — no price case vs GPT-5 mini's 1.2 cr class figure at the OLD price; n=1, worth re-running at the new one. **Took the cross-family verifier seat 2026-08-16** when Copilot retired Gemini 3.1 Pro; T34 cleared it at 8/8 recall first, and the 2026-08-14 reprice means the seat also got cheaper. Promo expiry 2026-12-31 is a re-check trigger (gate-readable marker lives in the development repo's claim ledger) |
| Gemini 3.7 Flash | Mechanical | **0.75 / 3.75** (cached in 0.075; the same `gemini-flash-promo` footnote as 3.6 Flash, through 2026-12-31 — read 2026-08-22, correcting this row's "not yet published"; the same printed 2× step from 2027-01-01 as 3.6) | **vals.ai SWE-V 80.8** (read first-hand from the board's own data 2026-08-23), one point above 3.6 Flash at an identical price | provisional (Copilot roster GA since 2026-08-13) | 2026-08-19 | Added to GitHub's supported-models table 2026-08-13 (GitHub changelog, same date), GA on arrival. 3.6 Flash's successor. Priced identically to 3.6 Flash and one vals.ai point above it, which is inside the noise of a single board and not a reason to move the seat. Do NOT move it on version number alone — 3.6 got the seat by clearing T34 at 8/8 recall, and nothing equivalent has been run for 3.7 |

Cross-vendor prices/benchmarks with full sourcing: `copilot.md`'s table
(Copilot SKUs) and the development repo's claim ledger. Anthropic lineup,
strongest → cheapest: Fable 5 > Opus 5 > Opus 4.8 > Sonnet 5 > Haiku 4.5.

## Notes

*Anthropic rows re-verified 2026-08-05 against the pricing, models-overview,
deprecations, effort and prompt-caching docs.*

- **The 5:2:1 ladder is list price, not effective cost.** Opus 5, Opus 4.8,
  Sonnet 5 and Fable 5 use the newer tokenizer (~30% more tokens for the same
  text); **Haiku 4.5 is the only Anthropic row here still on the old one**. So
  on identical source text the real Opus:Haiku multiple is nearer **6.5:1**
  than 5:1, and Sonnet:Haiku nearer 2.6:1. Anything
  that price-weights across tiers — the benchmark **W** unit included — is
  understating the cheap tier's advantage. Derived from two vendor-stated
  facts, not vendor-stated itself.
- **Seating an Opus 5 leaf — four operational facts** (researched
  2026-08-06, the development repo's research notes). None of these
  are benchmark facts and all four present as "the model got worse":
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
  deprecated: GPT-5.6 Luna cut 5× to 0.20 / 1.20, GPT-5.6 Terra cut 20% to
  2 / 12, GLM-5-Turbo corrected upward to 1.20 / 4.00, and MAI-Code-1-Flash
  scheduled for retirement on 2026-09-10. **A price that moves 5× in six
  days is the argument for gate (n)**, not a one-off.
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
  low/medium/high/xhigh/max on Fable 5, Opus 5, Opus 4.8, Opus 4.7 and
  Sonnet 5. `xhigh` is missing on Opus 4.6 and Sonnet 4.6. **Haiku 4.5 and
  Sonnet 4.5 have no effort dial at all**, so a Mechanical-class seat's only
  lever is the size of the brief you hand it.
- **The Cheap tier rests on one model.** Haiku 4.5 holds the Mechanical
  floor alone, has no announced successor, and carries the nearest
  retirement horizon in the lineup: not sooner than 2026-10-15, roughly ten
  weeks out, against Anthropic's 60-day notice commitment. Retirements do
  land. `claude-opus-4-1-20250805` retired on 2026-08-05. The safer shape is
  to write the policy in tier **aliases** plus an effort dial rather than
  pinned model IDs, so a floor swap is one edit here instead of a sweep.
- **The cache floor isn't monotonic, and it's worst on the cheap tier.**
  Minimum cacheable prefix: 512 tokens on Opus 5 and Fable 5, 1,024 on Opus
  4.8 and Sonnet 5, **4,096 on Haiku 4.5**. Below the floor nothing caches
  and no error comes back. A brief that caches on the planner can silently
  fail to cache on a Haiku executor at eight times the floor, so prove a
  miss by checking that both `cache_creation_input_tokens` and
  `cache_read_input_tokens` are 0.
