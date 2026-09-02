# evidence — what the routing table is measured on

*Loaded when a routing rule looks wrong. Read this before improvising past
one.* The rules in `SKILL.md` are terse because the evidence lives here, not
because it's thin.

## Contents

- Why the ceremony costs more than it saves
- What the 1.5–2.9× is measured across
- Where fan-out still wins
- The rework-prone regime, and why it stopped firing
- Verify value outlives fan-out economics
- Old patterns (superseded findings)
- Re-running these

## Why the ceremony costs more than it saves

Two effects stack against fan-out on work one strong context can hold:

- **Per-leaf overhead.** Every subagent reloads its own context on a cold
  cache. Tiering lowers the *bill*, never the token *count*.
- **Inline strong-model token-efficiency.** One strong context reaches the
  answer in fewer tokens than N cheaper ones reach it separately.

Together those made the full ceremony cost **1.5–2.9× one inline pass at
equal oracle quality**.

## What the 1.5–2.9× is measured across

| Run | Shape | Result |
| --- | --- | --- |
| T14 | 1 leaf | ceremony costs more |
| T19 | 5 small leaves, k=2 | ceremony costs more |
| T20 | 12 tiny leaves | ceremony costs more |
| T21 | 5 big leaves | ceremony costs more |
| T25 | one-context task routed through the full skill body | **1.52× bare inline** |

Every leaf count and size tested landed in that band. **Neither width nor size
amortizes the ceremony** — that's the finding, and it's why the inline route
in `SKILL.md` is lean enough to cost almost nothing to read.

T25 is the sharpest one: merely *routing* a one-context task through the full
skill body cost 1.52× just running it. A router that deliberates is a router
that already lost.

## Where fan-out still wins

Three regimes, and only these three:

- **Beyond one context window.** Not a preference. The work cannot be held.
- **Wall-clock-bound batches**, including ≥4 independent units with disjoint
  files. The 1.5–2.9× is just as real at 4 units — this trades tokens for
  wall-clock **knowingly**. Say which one you bought.
- **Demonstrated failure.** Inline flailed twice against one signature.

## The rework-prone regime, and why it stopped firing

T9 (dated 2026-07-11) measured failure-prone execution at **39–55% of inline**
— fan-out's clearest win, on a model generation where inline reliably flailed.

That regime has since closed on current models. T26 found no trap on current
Sonnet, and **T33 measured 2.78× *against* tiering** once inline stopped
failing. So this trigger fires on **demonstrated** failure, never on
anticipated failure. Predicting a model will flail is how you pay 2.78× for
nothing.

## Verify value outlives fan-out economics

The two are separable, and only one collapses. Independent verification still
gates risky merges at **any** size — C++ shared blind spots (UB, concurrency,
templates) and security — because a cold model shares the writer's training
and blind spots while a compiler doesn't. Ceremony collapses. The verify floor
never does.

## Old patterns

<details>
<summary>Superseded findings, kept for provenance</summary>

**"Fan out on failure-prone classes."** Retired. It anticipated failure rather
than observing it. T26 and T33 (above) are what retired it. The replacement is
the two-strike spiral guard, which needs an actual failing signature.

**"The 4× tax."** Retired framing. T25 measured the honest with/without at
**1.52×**, not 4×, and found the skill routes inline 3 of 3 times at quality
parity. The larger figure came from comparing against a bare inline run that
skipped work the routed run did.

**"80–90% of Opus."** Uncited folklore about the Sonnet floor, removed. The
real, sourced gap is **85.2 vs 88.6 on SWE-bench Verified** (Sonnet 5 System
Card, 2026-06-30) — near-frontier, and worth stating with its source rather
than as a range somebody remembered.

</details>

## Re-running these

Each T-number is a timestamped benchmark record in the source repo, carrying
structured spend frontmatter. Those records are not part of the shipped
bundle.

`claude plugin eval <plugin> --ablation with-without` is the supported way to
re-measure the with/without question these T-numbers were hand-rolled to
answer, once the feature is enabled on the account.
