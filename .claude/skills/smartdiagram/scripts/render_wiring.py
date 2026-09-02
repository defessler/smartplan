"""render_wiring.py - wiring.json spec -> self-contained interactive HTML diagram.

Usage: python render_wiring.py <spec.json> -o <out.html>

Layout is computed by the template at view time (columns of stacked nodes, groups boxed),
so the spec stays purely semantic. This script validates the spec's referential integrity
and injects it into the template; it fails loudly on any dangling reference, because a
wiring diagram that silently drops an edge is worse than no diagram.
"""
import argparse
import json
import sys
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "template.html"

SPEC_MARKER = "/*__SPEC__*/null"
TITLE_MARKER = "__TITLE__"

# SKILL.md sets the curation rule at ~20 nodes. The check sits two above it so a
# diagram at exactly the guideline never trips an off-by-one, while anything
# that has drifted into a hairball still does. Raising this is a curation
# decision, not a rendering one - merge nodes or split the diagram instead.
MAX_NODES = 22


def fail(msg: str) -> None:
    print(f"wiring spec error: {msg}", file=sys.stderr)
    sys.exit(1)


def validate(spec: dict) -> None:
    for key in ("title", "columns", "nodes", "edges", "flows"):
        if key not in spec:
            fail(f"missing top-level key '{key}'")
    ncols = len(spec["columns"])
    if not 2 <= ncols <= 5:
        fail(f"columns: expected 2-5, got {ncols}")
    for i, c in enumerate(spec["columns"]):
        for k in ("title", "legend", "slot"):
            if k not in c:
                fail(f"columns[{i}] missing '{k}'")
        if c["slot"] not in (1, 2, 3, 4, 5):
            fail(f"columns[{i}].slot must be 1-5")

    node_ids = set()
    for i, n in enumerate(spec["nodes"]):
        for k in ("id", "col", "title", "desc"):
            if k not in n:
                fail(f"nodes[{i}] missing '{k}'")
        if n["id"] in node_ids:
            fail(f"duplicate node id '{n['id']}'")
        node_ids.add(n["id"])
        if not 0 <= n["col"] < ncols:
            fail(f"node '{n['id']}' col {n['col']} out of range")
    if len(node_ids) > MAX_NODES:
        fail(f"{len(node_ids)} nodes - raise the altitude (skill rule: <= ~20)")

    edge_keys = set()
    for i, e in enumerate(spec["edges"]):
        for k in ("from", "to"):
            if k not in e:
                fail(f"edges[{i}] missing '{k}'")
            if e[k] not in node_ids:
                fail(f"edges[{i}].{k} references unknown node '{e[k]}'")
        edge_keys.add(e["from"] + ">" + e["to"])

    flow_ids = set()
    for i, f in enumerate(spec["flows"]):
        for k in ("id", "title", "html"):
            if k not in f:
                fail(f"flows[{i}] missing '{k}'")
        if f["id"] in flow_ids:
            fail(f"duplicate flow id '{f['id']}'")
        flow_ids.add(f["id"])
        for ek in f.get("edges", []):
            if ek not in edge_keys:
                fail(f"flow '{f['id']}' references unknown edge '{ek}'")
        for nk in f.get("nodes", []):
            if nk not in node_ids:
                fail(f"flow '{f['id']}' references unknown node '{nk}'")
    if "over" not in flow_ids:
        fail("flows must include the reserved 'over' (overview) flow")
    if spec["flows"][0]["id"] != "over":
        fail("'over' must be the first flow (it is the landing view)")

    # Groups must be contiguous runs within a column (the layout boxes contiguous runs;
    # a split group renders as two boxes, which is almost never what was meant).
    for ci in range(ncols):
        stack = [n.get("group") for n in spec["nodes"] if n["col"] == ci]
        seen_closed = set()
        cur = None
        for g in stack:
            if g != cur:
                if g in seen_closed:
                    fail(f"group '{g}' in column {ci} is non-contiguous")
                if cur is not None:
                    seen_closed.add(cur)
                cur = g
    print(f"spec OK: {ncols} columns, {len(node_ids)} nodes, "
          f"{len(spec['edges'])} edges, {len(flow_ids)} flows")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("-o", "--out", required=True)
    args = ap.parse_args()

    try:
        raw = Path(args.spec).read_text(encoding="utf-8")
    except OSError as exc:
        fail(f"cannot read spec {args.spec}: {exc.strerror}")
    try:
        spec = json.loads(raw)
    except json.JSONDecodeError as exc:
        fail(f"{args.spec} is not valid JSON: {exc.msg} at line {exc.lineno}, column {exc.colno}")
    if not isinstance(spec, dict):
        fail(f"{args.spec} must hold a JSON object, got {type(spec).__name__}")
    validate(spec)

    try:
        template = TEMPLATE.read_text(encoding="utf-8")
    except OSError as exc:
        fail(f"cannot read the renderer template at {TEMPLATE}: {exc.strerror}")
    # "</" would terminate the surrounding <script> block mid-string.
    payload = json.dumps(spec, ensure_ascii=False).replace("</", "<\\/")
    suffix = spec["titleSuffix"] if spec.get("titleSuffix") else ""
    title = spec["title"] + (" \u2014 " + suffix if suffix else "")
    if SPEC_MARKER not in template:
        fail(f"template {TEMPLATE} no longer contains its {SPEC_MARKER} marker")
    html = template.replace(SPEC_MARKER, payload, 1)
    if TITLE_MARKER not in html:
        fail(f"template {TEMPLATE} no longer contains its {TITLE_MARKER} marker")
    html = html.replace(TITLE_MARKER, title, 1)

    try:
        Path(args.out).write_text(html, encoding="utf-8", newline="\n")
    except OSError as exc:
        fail(f"cannot write {args.out}: {exc.strerror}")
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
