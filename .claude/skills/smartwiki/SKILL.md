---
name: smartwiki
description: 'Use when producing a stakeholder-facing wiki summary of a change for a non-engineer audience (designers, QA, producers) — triggers on "write up CL 1234 for designers", "summarize this commit/PR for the wiki", or the change-summary template. Works from any VCS (Perforce changelist, Git commit/range/PR, or uncommitted work) via the VCS Adapter. NOT the changelist-description skill; this writes the designer/wiki page.'
---

# smartwiki

Turn **one change** into **one {{AUDIENCE}}-facing wiki page**: plain-language,
for people downstream of the code who need *what changed* and *what they'll
touch* — not how it was implemented.

**VCS-agnostic.** Fill the **VCS Adapter** once (four verbs; Perforce and Git
are already filled in — any other VCS drops into the same four cells) and the
gather → draft → save flow below is identical no matter what tracks the code.
VCS-specific commands live only in the Adapter — the page you write names
neither the VCS nor any of its commands.

## VCS Adapter — set once

| Verb | Returns | Perforce | Git |
|------|---------|----------|-----|
| **IDENTIFY** | which VCS, then the ref (see below) | `p4 info` succeeds → a **changelist number** | `git rev-parse --is-inside-work-tree` succeeds → **commit SHA / range / PR / working tree** |
| **DESCRIBE** | message, author, date, **affected files** (no diffs) | `p4 describe -s <CL>` | commit: `git show -s --stat <ref>` · PR: `gh pr view <n> --json title,body,author,files` · working tree: `git status` |
| **DIFF** | content change of **text** files | `p4 describe <CL>` (`-du` for unified) | `git show <ref>` · range: `git diff <base>..<head>` · PR: `gh pr diff <n>` · uncommitted: `git diff` / `git diff --cached` |
| **READ** | one file's full contents at that revision | `p4 print -q //depot/path#rev` (shelved: `@=<CL>`) | `git show <ref>:<path>` |

**Change ref:** Perforce is a changelist number — submitted uses `p4 describe`,
shelved adds `-S`, pending uses `p4 change -o`. Git is a commit SHA / `HEAD` /
tag, a range `<base>..<head>`, a PR number (via `gh`), or uncommitted work
(`git diff` unstaged, `git diff --cached` staged; file list from `git status`).

**Disambiguating:** bare digits → Perforce CL; a hex SHA, branch name, `HEAD`,
an `A..B` range, or `#123` → Git. Genuinely unsure → ask, never guess. Edge
cases (dual-VCS detection, scripting flags, shelved/PR/working-tree nuances,
wiring a third VCS) → [`references/vcs-adapters.md`](./references/vcs-adapters.md);
skip it for a routine CL or commit.

## Output profile — set once

| Token | Meaning | Default |
|-------|---------|---------|
| `{{AUDIENCE}}` | who reads the page | designers |
| `{{WIKI_DIR}}` | where the page saves (point at your team wiki) | `change-summaries/` |
| `{{VOICE}}` | house voice for the prose | plain, direct, teammate-to-teammate |

**Voice is decided by the destination, not this skill.** Check for a voice
guide at or above `{{WIKI_DIR}}` before defaulting: if one exists, follow it
and bend this skill's defaults to it. The two that come up most: a dash ban
means rewording every em/en dash out of the page, and a two-axis-only tables
rule means rendering a one-attribute-per-entry table as `Term - description`
bullets (keep any table the reader reads down a column of to compare). Under
`smartvoice` both are Voice Profile rules, not skill-wide — `defaultvoice.md`
allows tables and bans no dash. No guide → default register: plain, direct,
tables fine. This skill's own em-dash style is never the output's style.

## Protocol

Copy this checklist and check off items as you go:

```
- [ ] 1. IDENTIFY the VCS and resolve the ref
- [ ] 2. DESCRIBE — message, author, date, files
- [ ] 3. DIFF and READ the text files
- [ ] 4. Binary assets named, never invented
- [ ] 5. Drafted from the Output template
- [ ] 6. Saved to {{WIKI_DIR}}, filename matching the H1
```

1. **IDENTIFY** the VCS and resolve the change ref.
2. **DESCRIBE** the change: message, author, date, affected files.
3. **Understand the code.** For changed **text** files, **DIFF** for the delta
   and **READ** for context — enough to explain the change in plain language:
   what a `{{AUDIENCE}}` reader sees and does. A newly-added file's DIFF
   already *is* the whole file; only spend a READ on a pre-existing file when
   the hunk isn't enough.
4. **Note binary/asset files** you can't read (below) — name plus the change
   message carry the story.
5. **Draft** the page from the Output template.
6. **Save** to `{{WIKI_DIR}}<change-ref> - <Short Title>.md` — `<change-ref>`
   is `CL 12345` (Perforce) or a short SHA / `PR 42` (Git). Filename matches
   the H1.

## Binary / unreadable assets

Game assets (`.uasset`, `.umap`) and other binaries can't be read or diffed.
Perforce marks them `binary`/`binary+l` in `p4 describe`. Git usually
LFS-tracks them — the reliable tell is a `filter=lfs` rule in
`.gitattributes` **plus** a diff/READ body that's only an LFS pointer
(`version https://git-lfs.github.com/spec/v1`, `oid sha256:…`, `size …`).
That pointer is *not* the asset. Don't trust `--stat`/`--numstat` alone: they
show `Bin`/`-` only when the raw binary is committed (LFS off); a pointer is
a ~3-line text file, so `--stat` shows a small line count that can fool you
into thinking it's readable.

You can't open either form. Name the affected asset/widget (bold it) and
infer intent from the filename plus the change message. Never fabricate a
binary's contents — or an LFS pointer's `oid`/`size` — as if it were the
asset.

## Output template

Save as `{{WIKI_DIR}}<change-ref> - <Short Title>.md` (filename matches the H1):

```markdown
# <change-ref> - <Short Title>

**Ticket:** <jira/issue>
**Author:** <author>
**Date:** <date>

---

## What Changed

### 1. <Feature/Change Title>
Plain-language description of what changed from the reader's perspective.
Focus on *what they'll see* and *what it means for their workflow*.

### 2. <Feature/Change Title>
...repeat for each distinct change...

| Widget / Asset | What It Does |
|---|---|
| **<AssetName>** | One-line description |

---

## How It Works

Explain the high-level flow in non-code terms.
Use bullets or numbered lists for multi-step processes.
Call out where data comes from (e.g. "pulls from network attributes + player inventory").

---

## Config / Settings Changes

Describe any new or modified settings (e.g. DefaultGame.ini, Developer Settings).

| Field | What It Controls |
|---|---|
| **FieldName** | Plain-language description |

If applicable: "To add a new X, go to **Project Settings -> Category -> Setting**."

---

## Debug / QA Aids

Note debug menu additions, console commands, or cheat changes that help verify
the feature works.

---

## Quick Reference: What <AUDIENCE> Might Need to Touch

| Task | Where to Go |
|---|---|
| Do X | **Path or menu location** |
| Do Y | **Path or menu location** |
```

Drop any section a change doesn't need. Keep small changes **under one
page**; use headers or collapsible sections for large ones.

## Writing guidelines

- **No code snippets** — a `{{AUDIENCE}}` reader doesn't need the C++.
- **Bold asset/widget names** in a table so the reader finds them in the
  editor. In `Term - description` bullets the term stays plain.
- **Name Blueprint-callable functions** by friendly name + what they return,
  not by signature.
- **Explain "why"** when something is non-obvious ("resources without a
  display entry won't show up in the HUD").
- **Tables over paragraphs** for list-like content (settings, widgets,
  tasks) — unless `{{VOICE}}` scopes tables away from one-attribute lists, then `Term - description`
  bullets.
- **Config paths** use the editor-friendly name ("Project Settings ->
  Prototype Outpost Settings -> Resources"), not the ini section name. Infer
  the editor category from the settings-class name (a `UDeveloperSettings`
  surfaces under Project Settings) — if you can't confirm the exact menu
  path, give the definite `DefaultGame.ini` location rather than presenting a
  guessed path as fact.
- **Group by feature, not file type**, when a change spans code + assets.
- **Match `{{VOICE}}`** — the prose reads as the wiki's own author wrote it,
  never this skill's own register.

## Tone

Direct, concise, no jargon. Assume the reader knows the design systems but
not the C++ internals. Use "you" for instructions ("To add a new resource,
go to...").

## Hard rules

- **The Adapter is the only VCS-aware part.** About to type `p4` or `git` in
  the *page*? Stop — VCS commands belong in gathering, never the writeup.
- **Never invent binary contents.** An unreadable asset is described from its
  name and the change message, and no further.
- **One change per page.** A range or PR bundling unrelated features gets one
  section each, not one blurred summary.
- **Don't guess the ref's VCS** — see Disambiguating above; genuinely
  unsure → ask.
- **Tiering** (see smartroute): one page is one context, so write it inline
  rather than fanning out. Dispatched, a lone page routes **Mid**: the
  mandatory verify runs 1.5–2× the executor, out-costing the Cheap saving on
  one leaf (hard floor #4). **Cheap** pays only across a batch of pages wide
  enough to amortize it, behind a filled Adapter, an exemplar page, and a
  smartcheck verifier.

Changelog: the repo's commit log (source repo only, so it's a path and not a link) — kept out of the shipped plugin to keep this body lean.
