# brief compilation (the smartbrief seat)

*Formerly the standalone smartbrief skill; consolidated into smartplan 2026-07-06
(v3.0.0). Loaded by smartplan's flow; seat vocabulary unchanged.*

**Use:** loaded by smartplan at flow step 3 for every Cheap leaf — never on
its own. `SKILL.md`'s hard gate forbids compiling a brief without `flow.md`
loaded, because the human gate and the mode-invariant floors live there, and
a brief is the artifact that carries an approval forward. **In:** one leaf
task + access to the codebase (for the exemplar). **Out:** a standalone
BRIEF in the template below — **save it to a file**. It's the handoff
artifact, consumable now or later, on any harness.

**Core policy:** weak models don't fail because they can't type code — they
fail on *missing context* and *open scope*. A brief removes both. Spend the
strong model here, once, so the cheap tier can't wander.

## Contents

- Authoring rules
- The brief template
- AUTHORIZATION
- TASK
- FILES
- CHANGE
- VERIFY FIRST
- CONVENTIONS
- ACCEPTANCE
- NON-GOALS
- IF BLOCKED
- Dispatch
- Changelog / edge-case log

## Authoring rules

1. **One concern per brief.** If you need the word "and" to describe the
   change, split it into two briefs.
2. **Standalone.** The executor has no chat history and no plan document.
   Never write "as discussed" or "per the plan" — inline everything needed.
   For code context, inline an aider-style **signatures-only map** of the
   relevant symbols the planner already paid to discover (~1k tokens) rather
   than sending the leaf off to re-explore the repo — exploration reads are
   the variable half of leaf cost.
3. **Exemplar over prose.** Paste a real snippet from the codebase showing the
   pattern to imitate (naming, error handling, test shape). Weak models
   imitate exemplars far better than they follow style prose.
4. **Objective acceptance — TDD-shaped when testable.** The ACCEPTANCE field
   is a runnable command and an expected observable result — never "code looks
   correct." The strongest form: write a concrete **failing test** at brief
   time, commit it with the brief, and make ACCEPTANCE "this test passes" —
   the executor turns red to green, which also defeats lazy passes that a
   grep-check would miss. If you can't script any check, the leaf isn't ready
   for a cheap executor. Route it Mid (per `routing.md`, same directory).
   **Runnable is not sufficient — rank the oracle** (`check.md` step 2):
   tier 1 is executable (compiler, assertion, replayed real input), and a
   code-emitting leaf has tier 1 by definition, so a substring or
   round-trip assertion over generated code is NOT its acceptance. Before
   writing the field, say what would have to break to turn it red; if that
   doesn't name the leaf's CHANGE, the field is decorative.
5. **Size to the executor.** A brief is a *hint, not a draft* — the
   measured operating range for strong-model guidance is 10–30% of the
   expected leaf output (Shepherding, arXiv:2601.22132); past that you pay
   planner-output rates for implementer work. For a Cheap-class executor, keep the brief ≤ ~1,500 tokens
   and the touched files small enough that brief + files + smartexec fit its
   window with room to work. Too big to fit = too big a leaf. Split it. The
   ~1,500 figure is eyeballed and runs *optimistic* on current Anthropic models
   — Opus 4.7+/Sonnet 5/Fable 5 use a newer tokenizer that yields ~30% more
   tokens for the same text — so treat it as a ceiling, not a target, and where
   the fit is tight run a `count_tokens` preflight instead of trusting the eyeball.
6. **Name the walls.** NON-GOALS is where scope creep dies. List the adjacent
   things the executor will be tempted to "fix" and forbid them explicitly.
7. **Give the exit.** IF BLOCKED tells the executor what to do instead of
   guessing. This powers the fail-twice escalation — canonical statement in
   `flow.md` (same directory), which `routing.md` forwards to.
8. **Quote the go-signal.** AUTHORIZATION carries the human's *actual approval
   words*, verbatim, with a date. Plan approval and execution authorization
   are different events, and a saved brief may be executed long after the
   conversation that approved it — the quote is the executor's only proof of
   the second event. **No quote, no execution**, and there is no path that
   waives this: every brief comes out of the gated flow (step 2), so a real
   approval event always exists to quote. If you can't find one, the brief
   isn't ready — go get the gate, don't substitute the original ask for it.
9. **Flag exactly ONE verify-first fact.** Pick the brief's most drift-prone
   assumption (an API signature, a config key, a line anchor) and make it
   checkable with an exact command plus a fallback. Exactly one: zero is blind
   trust, several re-verifies what the compile pass already verified and burns
   the savings the fan-out bought. Exactly-one is the default, not a cap on
   honesty: a brief with TWO genuinely load-bearing drift-prone assumptions
   should split into two briefs rather than ship one of them unverified.
   **For a C++ gamedev leaf**, state the **Engine Profile** line (template
   below) and draw the ONE flagged pitfall from `cpp-gamedev-check.md`'s
   catalog (same directory, § Pitfall catalog — VERIFY FIRST source), gated
   on that profile — the one profile-relevant pitfall most likely to bite
   this leaf, not a general scan of all six categories. Omit the profile and
   the checker defaults to `vanilla` **silently** (`cpp-gamedev-check.md`
   § Engine Profile gate), so every `[U]` Unreal and `[C]` custom-engine
   rule goes unapplied on code that needed them. A wrong-by-omission profile
   fails open, which is why the line is worth its three words.

9b. **Never add post-hoc self-verification language to a brief.** VERIFY
   FIRST above is a *pre-flight* check of one drift-prone fact, and that
   stays. What must not appear anywhere in a brief is the other shape:
   "double-check your work", "include a final verification step", "use a
   subagent to verify", "review your answer before returning". Anthropic's
   Opus 5 prompting guidance names that exact instruction class as a cause
   of **over-verification loops**, and says to delete it when migrating
   prompts written for Opus 4.8. It is not a hypothetical here: T32
   measured Opus 5 self-verifying unprompted on two of three Copilot runs,
   shelling out to check its own output and doubling input tokens 25.8k →
   52.0k. Telling a model that already self-verifies to verify again buys
   nitpicks, token-cap truncation, and loops.

   **The guidance goes further than this rule does, and that tension is
   real.** Read at source on 2026-08-06, it also says *"The same applies to
   legacy harness scaffolding that adds separate verification steps"*, and
   its suggested prompt includes *"do not use subagents to verify or
   double-check your own work"*. Taken alone that reads as an argument
   against the smartcheck seat itself. **The floor still stands**, for a
   reason the same page supplies: it calls Opus 5's **writer-verifier
   patterns "effective"** and its own wording is scoped to verifying *your
   own* work. smartcheck is cross-seat — a fresh verifier checking a
   *different*, usually cheaper executor's diff — which is the
   writer-verifier shape, not self-verification. What the guidance does
   kill here is the executor being told to check itself, and any verify
   step layered on an **Opus 5 leaf verifying its own output**. If a leaf's
   executor and verifier would be the same seat, drop the verify step
   rather than prompting for it.

10. **Conventions bind at write time.** Resolve the project's conventions doc
   once at plan time and pin its path in every brief's CONVENTIONS block, with
   the rule IDs the leaf is most likely to trip. Conventions are an authoring
   input, not only a review output: an executor that writes non-conforming code
   and a reviewer that catches it later costs two passes. Where the project
   declares no doc, write "none declared" rather than inventing house rules from
   the surrounding files.

11. **Contract references.** When the plan ships a `contracts.md` (frozen
   shared surfaces — scaffold + worked example at `artifacts.md`,
   same directory), the brief's CHANGE/CONVENTIONS must cite the contract
   **row** by **Surface** name for each shared surface the leaf consumes —
   never restate the frozen definition.

## The brief template

Emit exactly this shape (the executor's smartexec protocol keys off these
headings):

```markdown
# BRIEF: <one-line task name>

## AUTHORIZATION
<The human's go-signal from the plan gate, quoted verbatim with a date —
e.g. "approved, ship it" (2026-07-06). Absent or empty → the executor must
not execute.>

MODE: <optional — omit to inherit the run's mode; to override this leaf,
one of max-quality|high-quality|balanced|budget|max-savings, per modes.md>

ENGINE PROFILE: <C++ gamedev leaves only — one of vanilla|custom|unreal,
per cpp-gamedev-check.md § Engine Profile gate. Omit on non-C++ leaves.
Omitting it on a C++ leaf is not neutral: the checker assumes vanilla
without asking and skips every [U] and [C] rule.>

## TASK
<One sentence. What must be true when done.>

## FILES
<Exact paths, one per line. Optionally an anchor: function/class name or line range.
These are the ONLY files that may change.>

## CHANGE
<Precise description of the edit(s). Bullet per edit. Say where, what, and
with what — not "improve" or "clean up".>

## VERIFY FIRST
<Exactly ONE fact to re-check before editing — the brief's most drift-prone
assumption. Everything else here is pre-verified; do not re-verify it.>
Check: `<exact command or file:anchor>`
Expect: <what confirms the brief>
On mismatch: <fallback, or report BLOCKED>

## CONVENTIONS
Standards: <path to the project's conventions doc — smartreview's `{{STANDARDS}}`
— plus the rule IDs this leaf touches, or "none declared" when the project has no
doc. The executor READS it before the first edit; conformance is part of DONE,
not a later review.>
<A pasted exemplar snippet from this codebase to imitate. 5–20 lines.>

## ACCEPTANCE
<One runnable command and the expected result.>
Run: `<command>`
Expect: <exit 0 / specific output line / test name passes>

## NON-GOALS
<Explicit list of tempting-but-forbidden changes: refactors, renames,
formatting sweeps, "while I'm here" fixes, other files.>

## IF BLOCKED
Stop. Do not guess or widen scope. Report BLOCKED using your executor
protocol, with the exact error or the smallest question that unblocks you.
```

## Dispatch

Attach the brief and `smartexec` to the executor, and route per **`routing.md`**
(same directory): Mid floor; Cheap only with a scripted acceptance check
and a **smartcheck** verifier behind it. The active quality↔cost mode
(`modes.md`) rides the brief as an optional `MODE:` line directly under
AUTHORIZATION when non-default — it sets the executor's report **register**
(telegraphic at balanced-and-below, fragments at max-savings, full prose at
max-quality) and only that, since smartexec step 8 acts on register alone.
Effort is the dispatcher's lever, never the brief's: dispatch Cheap briefs
at low/medium reasoning effort where the harness has one (the brief is
designed to not need deep reasoning). On escalation, the orchestrator attaches the
ESCALATION REPORT (fields per the smartplan flow: TASK, TIER HISTORY, EVIDENCE,
HYPOTHESIS, NEXT) alongside a re-compiled brief — the receiving tier gets both,
never a bare retry. Authoring briefs is planner-seat work
(smartplan): keep it on the strong model, after the human plan-review gate —
briefs compile the *approved* plan, they don't replace it.

## Changelog / edge-case log

History: in the repo's commit log.
