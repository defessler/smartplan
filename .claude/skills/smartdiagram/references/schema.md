# wiring.json schema

Purely semantic — no coordinates. Layout (column stacking, group boxes, edge routing) is
computed at render time. Checked into the target repo (`Docs/wiring.json` or `docs/`).

```jsonc
{
  "title": "Inventory",                 // monospace accent part of the H1
  "titleSuffix": "System Wiring",       // plain part of the H1
  "subtitle": "one-line orientation shown beside the title",

  // 2-5 ownership domains, left to right. slot 1-5 picks a theme-paired palette color
  // (1 sage · 2 steel · 3 amber · 4 violet · 5 teal). Edges inherit the SOURCE column's color.
  "columns": [
    { "title": "GAME WORLD", "sub": "your classes", "legend": "Game world", "slot": 1 }
  ],

  // <= ~20 nodes. col = column index, ZERO-BASED (first column is 0). Note the
  // asymmetry: a column's own "slot" above is 1-5, but a node's "col" here is
  // 0-based, so a 2-column diagram uses col 0 and col 1. The renderer rejects an
  // out-of-range col loudly. Stacking order within a column = array order.
  // group: consecutive same-group nodes in one column get a dashed container box with the
  // group string as its label (use for "class X owns these members"). Must be contiguous.
  // badge: short red warning line inside the node (reserve for real, evidenced problems).
  "nodes": [
    {
      "id": "collect", "col": 1,
      "title": "CollectLiveInventoryActors",     // MUST name a real symbol/file
      "sub": "THE enumeration · visible levels", // monospace one-liner
      "desc": "Contract/invariant prose shown in the Inspect panel on click.",
      "group": "UInventoryLibrary — stateless",  // optional
      "badge": "⚠ ITEM CHANNEL EMPTY AT LOAD"    // optional, rendered red
    }
  ],

  // Edges are identified by "from>to" when flows reference them.
  // ret: dashed return/result edge. broken: red dashed - evidenced defects/limitations only.
  "edges": [
    { "from": "carrier", "to": "listener", "label": "OnLevelActorAdded", "ret": false, "broken": false }
  ],

  // First flow MUST be id "over" (overview: everything visible, no labels). Other flows
  // list the edges ("from>to") and node ids to keep at full opacity; everything else dims.
  // caption: optional heading override shown above html (defaults to title).
  // html: 2-4 sentences telling the story; <b>, <code>, <p> allowed.
  "flows": [
    { "id": "over", "title": "Overview", "html": "<p>...</p>" },
    { "id": "mint", "title": "Mint & heal", "caption": "Mint & heal — identity is born here",
      "html": "<p>...</p>", "edges": ["carrier>listener"], "nodes": ["carrier", "listener"] }
  ],

  // Optional extra legend chips (e.g. the broken-red meaning) and a status footer.
  "legendExtra": [ { "slot": "broken", "label": "Known cooked limitation" } ],
  "footer": [ { "label": "Build", "value": "B1 green", "tone": "ok" } ]   // tone: ok|bad|plain
}
```

Authoring rules (enforced socially, validated structurally by the renderer):
- Every node title names something greppable in the repo — that is what makes drift checks
  possible on later updates.
- `desc` states the contract (paraphrase the code's own header comments), never restates
  the title.
- `broken`/`badge`/`tone:bad` require recorded evidence (test log, verified finding).
- If you need more than ~20 nodes, split into per-subsystem diagrams instead.
