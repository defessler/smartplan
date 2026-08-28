# smartwiki — VCS adapters (deep reference)

Load this only when the common path in `SKILL.md` isn't enough: detecting the
VCS when it's not obvious, handling shelved / pending / working-tree / PR
changes, scripting the gather, or wiring a third VCS. For a routine submitted CL
or a single commit, the Adapter table in `SKILL.md` already has what you need.

The skill needs exactly four verbs from any VCS. Everything below is how to make
those verbs return the right thing per tool.

- **IDENTIFY** — confirm the VCS and turn the user's words into a concrete change ref.
- **DESCRIBE** — message + author + date + affected file list, *without* diffs.
- **DIFF** — the content delta of text files.
- **READ** — one file's full contents at the change's revision.

## IDENTIFY — which VCS, and what's the ref

Detect the VCS from the working directory, not from a guess:

- **Git** — `git rev-parse --is-inside-work-tree` prints `true`. A `.git`
  directory (or a `.git` file for worktrees/submodules) is present.
- **Perforce** — `p4 info` succeeds (prints server + client), or `P4CONFIG` /
  `P4PORT` are set, or a `.p4config` file sits above the cwd. Perforce has no
  per-directory marker like `.git`, so lean on `p4 info`.
- **Both present** (a Git repo inside a Perforce workspace, or vice versa) — the
  *ref shape* the user gave you decides which one they mean. See below. If still
  ambiguous, ask.

Resolve the user's words into a ref by shape:

| The user said... | Ref | VCS |
|---|---|---|
| "CL 12345", "changelist 12345", bare `12345` | `12345` | Perforce |
| "commit a1b2c3d", a 7–40 char hex string, `HEAD`, `HEAD~2`, a tag | that rev | Git |
| "this branch", "since main", "main..feature" | a range `<base>..<head>` | Git |
| "PR 42", "#42", a GitHub PR URL | `42` | Git (via `gh`) |
| "my current changes", "what I have staged/open" | working tree | Git or Perforce |

Bare digits are the only reliably Perforce-shaped ref. Everything hex / named /
ranged / `#`-prefixed is Git.

## Perforce

### Change states
- **Submitted** — already in the depot. `p4 describe <CL>` works fully.
- **Pending** — opened, not yet submitted. `p4 describe -s <CL>` shows the file
  list. The description text is authoritative from `p4 change -o <CL>` (the `Description:` field of the changelist spec).
- **Shelved** — files parked on the server without submitting. Add `-S`:
  `p4 describe -S <CL>` lists shelved files and diffs them against the depot.

### The four verbs, Perforce
- **DESCRIBE** — `p4 describe -s <CL>`. The `-s` flag is "short": changelist
  metadata (user, date, description) and the affected-file list, **without** the
  per-file diffs. Cap a huge CL with `-m <max>` to the first *max* files.
- **DIFF** — `p4 describe <CL>` (default includes diffs), or force a format with
  `-du` (unified, patch-compatible), `-dc` (context), `-ds` (summary counts).
  Shelved: `p4 describe -S -du <CL>`.
- **READ** — `p4 print -q //depot/path#rev` prints file contents at a revision
  (`-q` drops the header line). For a **shelved** revision use the `@=<CL>`
  syntax: `p4 print -q //depot/path@=<CL>`.
- Scripting — prefix any of these with `-ztag` (`p4 -ztag describe -s <CL>`) to
  get key/value output that's stable to parse instead of the human format.

### File types (why some files are unreadable)
`p4 describe` tags each file with its type: `text`, `binary`, `binary+l` (binary
with **exclusive lock** — the norm for game assets so two people can't edit a
`.uasset` at once), `+S` (a temporary/shelved-storage modifier). Anything
`binary*` can't be diffed or read as text — describe it from its name and the CL
description (see *Binary / asset files (both VCS)* below).

## Git

A Git "change" is broader than a Perforce CL. Match the gather to what the ref is.

### Single commit (SHA / `HEAD` / tag)
- **DESCRIBE** — `git show -s --stat <ref>` (metadata + per-file add/del stat),
  or `git show --name-status <ref>` for just the file list with A/M/D status.
  Author/date alone: `git show -s --format='%an %ad %s' <ref>`.
- **DIFF** — `git show <ref>` (the full patch for that commit).
- **READ** — `git show <ref>:<path>` prints the file's full contents *at that
  commit*.

### Range / branch (`<base>..<head>`)
- **DESCRIBE** — `git log --stat <base>..<head>` (or `--name-status`) for every
  commit and file in the range; `git diff --name-status <base>..<head>` for the
  net file list.
- **DIFF** — `git diff <base>..<head>` for the net delta.
- **READ** — `git show <head>:<path>`.

### Pull request (`gh` — GitHub)
- **DESCRIBE** — `gh pr view <n> --json title,body,author,files,commits`. `title`
  + `body` are the human description; `files` is the changed-file list; `commits`
  is the per-commit breakdown. (`gh pr view` also has `additions`, `deletions`,
  `changedFiles`, `baseRefName`, `headRefName`, and more — request only what you
  need.)
- **DIFF** — `gh pr diff <n>` (whole-PR patch). `--exclude '<glob>'` (repeatable)
  drops noisy paths.
- **READ** — check out or fetch the head, then `git show <headSha>:<path>`.

### Uncommitted work (working tree)
- **DESCRIBE** — `git status` (or `git status --porcelain` to parse) for the
  changed-file list and staged/unstaged split.
- **DIFF** — `git diff` (unstaged), `git diff --cached` (staged), `git diff HEAD`
  (both vs the last commit).
- **READ** — the file on disk is the current content; `git show HEAD:<path>` for
  the pre-change version.

### Binary detection in Git
Git decides binary-ness from content and `.gitattributes`. For a **raw binary
committed directly** (LFS off), a diff prints `Binary files ... differ` instead
of a hunk, `--stat` prints `Bin`, and `--numstat` prints `-` `-` in place of
added/deleted counts.

**But game projects almost always use Git LFS**, and then those cues don't fire.
`.uasset` / `.umap` (and often `.fbx`, `.wav`, large media) are tracked through
**Git LFS** via `.gitattributes` lines like
`*.uasset filter=lfs diff=lfs merge=lfs -text`. What Git actually stores and
shows for an LFS file is a tiny **pointer**, so `git show <ref>:<path>` and the
diff body return three lines of text —
`version https://git-lfs.github.com/spec/v1` / `oid sha256:…` / `size …` — and
`--stat` reports a small **line count** (e.g. `3 +++`), *not* `Bin`. A cheap
executor that trusts `--stat` here will mistake the pointer for a readable text
file and try to summarize the `oid`/`size`. So the **reliable** LFS signal is the
`filter=lfs` attribute for that extension **and** the pointer-shaped body — treat
that as an unreadable binary, exactly like a Perforce `binary+l`. LFS-tracked
assets are lockable (`git lfs lock`) for the same reason Perforce exclusive-locks
them: binaries can't be merged.

## Binary / asset files (both VCS)

Same limitation, two spellings:

| | Perforce | Git |
|---|---|---|
| How it's stored | file type `binary` / `binary+l` | LFS-tracked via `.gitattributes` (or, rarely, a raw binary blob) |
| How it shows in a describe/diff | `... (binary+l)` in `p4 describe` | **LFS (usual):** a pointer body (`version …/spec/v1`, `oid`, `size`) + a small `--stat` line count. **Raw binary (LFS off):** `Bin` in `--stat`, `-` in `--numstat`, `Binary files differ`. |
| Can you read it? | No | No — the LFS pointer is not the asset |
| What to do | name the asset, infer intent from the file name + change message | same |

For a designer writeup this is usually fine: the *name* of a `.uasset` widget or
a `.umap` level plus the change description tells the reader what to look at.
Never invent the internal contents of a binary you couldn't open.

## Adding a third VCS

Fill the same four verbs and the skill works unchanged. Sketch:

- **Mercurial (hg):** IDENTIFY `hg root`; DESCRIBE `hg log -v -r <rev>`
  (`--stat` for files); DIFF `hg diff -c <rev>` (or `-r a:b`); READ
  `hg cat -r <rev> <path>`.
- **SVN:** IDENTIFY `svn info`; DESCRIBE `svn log -v -r <rev>`; DIFF
  `svn diff -c <rev>`; READ `svn cat -r <rev> <url/path>`.

If a VCS can't cheaply give one verb (e.g. no clean "metadata without diffs"),
approximate it (take the full diff and ignore the hunks) rather than bending the
Protocol.

## Sources (verified 2026-07-06)

- P4 `describe` flags (`-s` short/no-diffs, `-S` shelved, `-m`, `-d*`):
  <https://help.perforce.com/helix-core/server-apps/cmdref/current/Content/CmdRef/p4_describe.html>
- P4 `changes` (status filtering, pending/shelved/submitted):
  <https://help.perforce.com/helix-core/server-apps/cmdref/current/Content/CmdRef/p4_changes.html>
- Git `show` (incl. `<rev>:<path>`, `--stat`, `--name-status`):
  <https://git-scm.com/docs/git-show>
- Git `diff` (binary `-`/`Bin` markers, range/`--cached`):
  <https://git-scm.com/docs/git-diff>
- `gh pr view` JSON fields, `gh pr diff`:
  <https://cli.github.com/manual/gh_pr_view> · <https://cli.github.com/manual/gh_pr_diff>
- Git LFS for Unreal `.uasset` / `.umap` (`.gitattributes`, locking):
  <https://dev.classmethod.jp/en/articles/using-git-lfs-for-ue5-project/>
