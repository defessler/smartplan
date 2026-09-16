# Completion exemplar

A short source file that shows a project's conventions in code, kept open
in an editor tab so inline completions copy it.

## Why it exists

Inline completions (ghost text and next edit suggestions) never read
instruction files. Copilot's custom instructions, `AGENTS.md`, this skill's
standards doc and every resident rule reach Chat and agent sessions only. What
completions do read is the code around the cursor and related files open in
the editor. So the one place a project's conventions can reach them is a file
in an open tab.

**Unmeasured.** Vendor docs say open files feed completions, and an issue on
the language server shows they sometimes stay on the focused file anyway. Run
the check in § Proving it works before you rely on it.

## When to build one

When someone asks for a completion exemplar, a conventions exemplar, or a way
to make inline suggestions follow house style. One file per language the
project writes by hand.

## Inputs, all resolved first

- `{{STANDARDS}}` and its profile selector, exactly as the review protocol
  resolves them.
- The three knobs: indentation, max line length, local-variable case.
- Two or three real files the user names as good examples of house style.
  Read them for the patterns the standards doc leaves open, such as comment
  voice, include grouping and blank-line rhythm. Don't pick them yourself
  from file extensions.

If any of these is unset, ask. The hard rule is the same as for a review:
never invent a convention. An exemplar built on a guessed knob teaches every
suggestion the wrong style, and it does so quietly.

## What goes in it

- **Only correct code.** Completions copy what they see, so there are no bad
  examples, no before/after pairs, and no commented-out anti-patterns.
- **Every line earns its place.** Aim for 80 to 150 lines. Completions take
  snippets of neighboring files rather than the whole thing, so dense beats
  thorough.
- **Cover each rule the standards doc can show in code**, one instance each:
  - file header, include or import order and grouping
  - naming for types, functions, members, locals, booleans, constants and
    enums
  - indentation, brace placement and line length, from the knobs
  - comment style, matching the project's own voice
  - null and error handling, ownership, and container choice
  - logging, when the doc has logging rules
  - one complete, realistic function that combines the above
- **Rules the doc tags as externally enforced** (the C++ doc's **[U]**) are
  shown exactly as the engine or toolchain requires.
- **Synthetic names only.** Invent a small domain (an inventory, a timer
  queue) rather than copying proprietary code into the file.
- **It must parse cleanly** in its language, with every symbol it uses
  declared in the file or a standard header. A file full of red squiggles
  pulls next edit suggestions toward fixing it.

## Where it goes

`docs/conventions-exemplar.<ext>` by default, or the project's docs folder.
Keep it out of every build target. In an Unreal project that means outside
`Source/`, so the build tool never compiles it. The exact path doesn't matter
to completions, since only the open tab does.

## Checking it before handing it over

Run this skill's own protocol on the exemplar against the same
`{{STANDARDS}}`. It has to come back with zero CONVENTION and zero PRACTICE
findings. A single finding there is a convention the exemplar would teach
wrong. Then check it parses: compile or lint it standalone where the
language allows.

## Using it

Open it in a tab beside the file you're editing, same language, and pin the
tab. Regenerate it whenever the standards doc or a knob changes. A stale
exemplar teaches the old rules.

## Proving it works

A small A/B test, about an hour, that costs completions rather than chat
credits:

1. Pick five function stubs the project needs, each with a one-line intent
   comment.
2. Arm A: only the target file open. Accept the first suggestion for each
   stub and save it.
3. Arm B: same stubs, same completions model, with the exemplar pinned
   beside it.
4. Review both arms with this skill against `{{STANDARDS}}` and compare the
   CONVENTION counts.

If Arm B doesn't cut them, the exemplar isn't reaching completions on that
editor, and there's no reason to maintain it there.
