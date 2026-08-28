---
name: smartdiagram
description: Generate an interactive system-wiring diagram (ownership columns, selectable flows, click-to-inspect invariants) for any codebase. Use when asked for an architecture/wiring/system diagram, "how is everything hooked up", or to update a repo's existing diagram. Curation-first - never emit an auto-generated symbol hairball.
---

# smartdiagram — curated interactive architecture graphs

The output is an interactive HTML diagram (self-contained, artifact-ready): ownership
columns, selectable **flows** that dim everything else, click-to-inspect **contracts** per
node, and honest **health annotations**. The renderer is generic; all judgment lives in a
per-repo spec file. The 80/20 rule this skill exists for: rendering is mechanical,
**curation is the value** — a diagram nobody has to squint at beats a complete one.

## Procedure

1. **Scout the system** (read, don't guess): the repo's CLAUDE.md / README / design docs,
   module or package boundaries, the handful of load-bearing types/functions, and — the part
   auto-tools always miss — *verification evidence* (test results, known limitations, TODO
   debt). You are looking for four things:
   - **Columns** (2–5): ownership domains, not folders. e.g. consumer code · core module ·
     tooling module · platform/engine.
   - **Nodes** (≤ 20 total): the load-bearing pieces only. Every node must name a REAL
     symbol/file; if you can't point at it, it doesn't go in.
   - **Flows** (3–6): named end-to-end stories of how the system is *used or lives*
     (creation, the main query, the special case, the deploy/build boundary). Flows are
     semantic — they come from docs and headers, never from a call graph.
   - **Health**: what is verified, what is broken/limited — with evidence. Mark it; an
     honest red edge is the most valuable ink in the diagram.

2. **Author the spec** at `<repo>/Docs/wiring.json` (or `docs/`), schema + authoring rules
   in [references/schema.md](references/schema.md). Node `desc` texts must state the
   *contract/invariant* (ideally paraphrasing the code's own header comments), never
   restate the title. Check the spec into the repo — it is documentation, versioned and
   diffable.

3. **Render**: `python <this-skill-dir>/scripts/render_wiring.py <spec.json> -o <out.html>`
   The script validates all references (edges, flows, groups) and fails loudly on dangling
   ones.

4. **Publish** with the Artifact tool (suggested favicon 🧭). Re-render + republish the same
   file path to update an existing diagram's URL.

5. **On updates — drift check first**: before re-publishing, grep the repo for each node's
   named symbol; a node whose symbol no longer exists is a spec bug to fix, not a rendering
   detail. This is what keeps the diagram from rotting like every other architecture doc.

## Rules

- Never exceed ~20 nodes or ~30 edges. If the system is bigger, raise the altitude (merge
  nodes) or split into multiple diagrams (one per subsystem), not one hairball.
- Every flow's `html` is 2–4 sentences that tell the story in the system's own
  vocabulary. `caption` is the optional heading above it, not the prose — a
  paragraph put there renders as an `<h2>`.
- Health/limitation markings require evidence (a test run, a recorded finding) — never mark
  something broken or verified on vibes.
- The `over` flow id is reserved: it shows everything and its `html` states the system's
  one-sentence load-bearing shape.

## Family fit and tiering

`smartdiagram` is an **optional** companion seat (like `smartreview`/`smartwiki`/`smartvoice`):
the family works without it, and it sits outside the tiering loop — it is a reusable
procedure, not a model-role. It pairs naturally with `smartwiki`, which renders a change for
a non-engineer audience; a diagram is the same job for system shape.

Tiering (see `smartroute`): the scout-and-curate step is judgment-heavy — deciding which 20
nodes carry a system is exactly the call a weak model gets wrong — so authoring a spec fits
**Strong**, or **Mid** when the repo already has a good design doc to work from. The render
step is a script and costs nothing. A drift check (step 5) is mechanical grep work and routes
**Cheap** behind the usual verify.

## Changelog

the repo's commit log (source repo only, so it's a path and not a link) — kept
out of the shipped plugin to keep this body lean.
