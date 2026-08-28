---
name: smartreview
description: Use when reviewing a changelist or fileset before accepting or merging — triggers on "review this change", "find bugs in this diff", or "apply/check/enforce conventions". Reports three ranked categories — game-breaking bugs first, then best practices, then conventions — against a swappable standards doc; shipped default is C++ gamedev (vanilla/custom/Unreal).
---

# smartreview

You review **one changelist or fileset** and report every finding in **three
ranked categories**. Two layers: this file is the **driver** — the ranking,
the protocol, and the report — and a swappable **standards doc** supplies
the checklist, its tag legend, its breaking-defect classes, and its
fill-once tokens.

**Rank before you report.** A game-breaking bug buried under forty naming
nits has not been surfaced.

| Category | What belongs | Disposition |
|---|---|---|
| **BREAKING** | It ships broken — crash, UB, memory or save corruption, data loss, hang, deadlock, a leak that exhausts memory, desync, or a build/link failure that only shows in another configuration. | **Blocks the merge.** |
| **PRACTICE** | Built the wrong way, works today — API misuse, a missing guard, an avoidable allocation off the hot path, dead registration code, a trap the next change walks into. | Fix, or file it. |
| **CONVENTION** | House style — naming, formatting, comment style, ordering. No runtime consequence. | Fix in place. |

**Name the failure or demote it.** A BREAKING finding states the concrete
failure a player, a build, or a save file would see. Can't name one? It's
PRACTICE. Inflating severity destroys the ranking's only value, and the
reverse is worse: a real crash filed as a style nit ships.

## Project Profile — set once

One token picks the standards doc; three knobs are universal enough to live
here rather than in any one language's doc.

| Token | Meaning | Default |
|-------|---------|---------|
| `{{STANDARDS}}` | the per-project review-standards doc: its checklist, tag legend, severity map, breaking-defect classes, profile selector, and fill-once tokens | [`references/cpp-review-standards.md`](references/cpp-review-standards.md) (C++ gamedev, engine-profiled) |

How it resolves:

- **Set to a path** → load that doc; it defines both "conventions" and
  "breaking" for this project.
- **Unset** → ask which standards doc to use — confirm the shipped C++
  default or take a path to the project's own. Never guess a language's
  conventions from file extensions.
- **A path that doesn't resolve** → say so and stop. A review against an
  imagined standard is not a review.

**Swapping the standards doc:** a Python or TypeScript project points
`{{STANDARDS}}` at its own `references/<lang>-review-standards.md` declaring
its own checklist, tokens, tag legend, and breaking classes — this driver
file is unchanged.

| Knob | Meaning | This project | Epic C++ example |
|------|---------|--------------|------------------|
| **Indentation** | tabs, or _N_ spaces | _fill in_ | `tabs` (size 4) |
| **Max line length** | a number, or `none` | _fill in_ | `none` |
| **Local-variable case** | `lowerCamelCase` or `PascalCase` | _fill in_ | `PascalCase` |

**"This project" ships unfilled, on purpose** — it's a template slot, not a
live value. This skill often installs globally, where a pre-set value
imposes one project's house style on all the rest. Fill it once per
project. Until you do, its rows are **N/A** per the hard rules below, never
a value guessed from the code under review. The Epic column is an example
to copy in (provenance: `references/cpp-review-standards.md § Provenance &
Epic-standard validation`).

## Protocol

1. **Gather files.** Identify files in scope (from a changelist via your
   VCS's describe/diff, or user-specified paths). Read each file in full.
2. **Hunt breaking defects first**, before a single style row. Sweep every
   breaking-defect class `{{STANDARDS}}` names. This pass is **not**
   checklist-driven — a checklist holds the rules somebody already wrote,
   and a bug is what nobody wrote one for. Read for what the code *does*:
   who owns each allocation, what runs on which thread, what the failure
   path does, what a malformed or stale input does. Sweeping a class and
   finding nothing is a result — report it.
3. **Walk the checklist** in `{{STANDARDS}}` per file, gating rows exactly
   as that doc's tag legend and profile selector dictate. Mark each item
   **PASS**, **FAIL**, or **N/A** — don't skip, mark **N/A** instead. File
   each FAIL under the severity that doc's severity map assigns it.
4. **Report** using the template below.

A clean checklist never stands in for the hunt, and a crash never excuses
skipping the checklist. Both run, every time.

## Report

```
REVIEW: <changelist / fileset>
Standards: <doc {{STANDARDS}} resolved to> · <active profile/selector, if the doc declares one>
Files reviewed: <n>
Findings: BREAKING <n> · PRACTICE <n> · CONVENTION <n>

BREAKING — blocks the merge
  - <file>:<line> — <category> — <the failure, concretely> → <fix applied | proposed>
PRACTICE
  - <file>:<line> — <what's wrong> → <fix applied | proposed>
CONVENTION
  - <file>:<line> — <rule #> — <what was wrong> → <fix applied | proposed>

Checklist: <n> items (PASS <n> · FAIL <n> · N/A <n>)
Categories swept, clean: <breaking categories that produced nothing, or "none">
Ambiguous / flagged: <rule # or category> — <why unsure> (asked, did not guess)
```

An empty category prints its heading and `none`. Silence reads as "not
looked at," which is the one thing a review may never imply.

With the shipped doc and the Engine unset, the `Standards:` line reads
`cpp-review-standards.md · Engine: vanilla` (or `custom` / `unreal`).

**Where this sits.** This seat is the merge gate, over a whole fileset.
smartcheck's `cpp-gamedev-check.md` is the verify seat inside a smartplan
fan-out, over one leaf's diff. Same defect classes, different position —
this driver **reuses** that taxonomy through the standards doc rather than
re-stating it, so the two can't drift. Name the category on every BREAKING row
so the two reports collate on `category · file:line`, and mark a row a leaf's
smartcheck already filed as already-filed rather than raising it twice.

## Output register (default: max-savings)

Whenever this review's only reader is another model seat — dispatched as a
smartplan fan-out leaf, or any invocation feeding another agent — the
report's free-text fields (`<what's wrong>`, `<why unsure>`, not the counts,
rule IDs, or category headings) follow `modes.md`'s caveman register.
**Default here is max-savings** (caveman *ultra*): nothing is lost
compressing a report no human will read. It replaces smartplan's
family-wide *shipped default* and sits on that same bottom rung of
`modes.md` § Setting it, so all three levels above still beat it, first one
set winning: an explicit per-invocation ask, a brief's `MODE:` line, then
the project's `{{MODE}}` token. File paths, rule IDs, and quoted code stay
byte-verbatim regardless, as does **a BREAKING finding's failure
description** — that sentence is the one a human reads first. Run
interactively, the report stays full prose per `modes.md`'s human-facing
floor.

## Hard rules

- **Breaking first, no exceptions.** Report BREAKING ahead of everything,
  even when the convention pass returns two hundred rows.
- **Exhaustive, not sampled.** Every class, every item, every file. A
  skipped row is a silent FAIL waiting to ship.
- **Resolve the Profile first.** `{{STANDARDS}}` before reading a line of
  code. If it, a knob, or a standards-doc token is unset, the dependent rows
  are **N/A** — never invent a value, a language, or a standard.
- **Don't guess.** If a rule's applicability or a defect's reachability is
  ambiguous, flag it rather than marking PASS, FAIL, or BREAKING.
- **Reproduce before you file.** A BREAKING row is a claim, not a verdict —
  name the input or path that triggers the failure. A reviewer asked for
  bugs finds some even in sound code (`check.md` § Review / audit output),
  so an unreproducible suspicion goes under Ambiguous, never under BREAKING.
- **Respect the standards doc's enforcement tags.** Rows it marks as
  externally enforced (engine-, build-, or toolchain-mandated — the C++
  doc's **[U]**) are not house style to adapt; change only rows it marks as
  project choice.
- **Gated-off rows are N/A, not deleted.** A row outside the active
  profile/selector still appears in the tally, as N/A.
- Tiering (see smartroute): the convention pass is mechanical and scriptable
  per row — a Cheap tier runs it fine. **The breaking hunt is not.**
  Ownership, threading, and lifetime judgment take at least a Mid tier, and
  the floor tracks the executor: a Sonnet- or Opus-authored diff gets the
  hunt at Opus-or-comparable strength. Run inline unless the fileset won't
  fit one context.
- **Verify before the merge (see smartcheck).** This seat sits at the merge
  gate, so the verify floor holds at any size: a risky merge takes an
  independent check, and this seat can't be it. When it fixes findings
  rather than reporting them, that check covers the fix — a BREAKING finding
  fixed here is exactly the case the floor exists for.

## Changelog / edge-case log

Moved to [the repo's commit log](https://github.com/defessler/smartplan/commits/main) to keep this body lean and out of the shipped plugin.
