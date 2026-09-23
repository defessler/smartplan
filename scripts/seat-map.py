#!/usr/bin/env python3
"""seat-map.py - generate the machine-readable seat map from model-classes.md.

The registry (`.claude/skills/smartplan/references/model-classes.md`) is the
single hand-maintained source for model classes and prices. This script
derives a lean JSON map from it (the cost audit's deferred ~2KB map) and
provides the deterministic price comparison the cost ceiling needs
(routing.md "The cost ceiling"). Generated,
never hand-edited: three export scripts and gate (g) consume the registry, so
a second hand-maintained table would drift.

Subcommands:
  build [--out PATH]   write the seat map (default dist/seat-map.json)
  compare A B          print both rows and which one prices above the other
  check A B            exit 0 if A costs no more than B on both axes,
                       exit 1 if A prices above B on input AND output
                       (the ceiling violation), exit 2 on unknown models
  latest               exit 1 if any seat leads a model line with an older
                       version than the registry holds (check.sh gate x)

The comparison is LIST price. Effective cost can flip it: the newer
tokenizer adds ~30% tokens on most Anthropic rows, cache tiers and plan
credit multipliers differ per vendor, and a mid-job switch re-pays a warm
prefix cold. routing.md's ceiling rule carries those terms; this script is
the deterministic core, not the whole rule.

Run from the repo root. No third-party dependencies.
"""

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY = REPO_ROOT / ".claude" / "skills" / "smartplan" / "references" / "model-classes.md"
DEFAULT_OUT = REPO_ROOT / "dist" / "seat-map.json"

# Harness dispatch strings -> registry display names. Aliases are harness
# facts (what a model: field accepts), not registry facts, so they live here.
#
# Claude Code dispatch strings use Anthropic's hyphenated API ids
# (claude-opus-5-5). Copilot slugs dot the version (claude-opus-4.8). So both
# spellings are listed. `opus` follows Claude Code's alias on the Anthropic
# API, which moved to Opus 5.5 in v2.1.280 (2026-09-22). A subagent's `opus`
# resolves to the session's own Opus when the session already runs one, and
# resolve() applies that when the seat is known. The per-call Agent `model`
# takes only the four aliases. A full id goes in agent frontmatter or
# CLAUDE_CODE_SUBAGENT_MODEL. Off the Anthropic API the `sonnet` alias
# reaches an older Sonnet (claude-code.md), so these rows assume that API.
ALIASES = {
    "sonnet": "Sonnet 5",
    "claude-sonnet-5": "Sonnet 5",
    "opus": "Opus 5.5",
    "claude-opus-5-5": "Opus 5.5",
    "claude-opus-5.5": "Opus 5.5",
    "opus-5.5": "Opus 5.5",
    "claude-opus-5": "Opus 5",
    "opus-4.8": "Opus 4.8",
    "claude-opus-4.8": "Opus 4.8",
    "claude-opus-4-8": "Opus 4.8",
    "haiku": "Haiku 4.5",
    "claude-haiku-4.5": "Haiku 4.5",
    "claude-haiku-4-5": "Haiku 4.5",
    "fable": "Fable 5.1",
    "best": "Fable 5.1",
    "fable-5.1": "Fable 5.1",
    "claude-fable-5.1": "Fable 5.1",
    "claude-fable-5-1": "Fable 5.1",
    "gpt-5.6-luna": "GPT-5.6 Luna",
    # A bare line name means its newest version (model-classes.md § How to
    # edit, newest version first). Pass the full slug to price an older one.
    "luna": "GPT-6 Luna",
    "gpt-6-luna": "GPT-6 Luna",
    "gpt-6-sol": "GPT-6 Sol",
    "gpt-5.6-terra": "GPT-5.6 Terra",
    "terra": "GPT-5.6 Terra",
    "gpt-5.6-sol": "GPT-5.6 Sol",
    "sol": "GPT-6 Sol",
    "gpt-5.4": "GPT-5.4",
    "gpt-5.4-mini": "GPT-5.4 mini",
    "gpt-5-mini": "GPT-5 mini",
    "gemini-3.8-flash": "Gemini 3.8 Flash",
    "gemini-3.6-flash": "Gemini 3.6 Flash",
    "gemini-3.1-pro": "Gemini 3.1 Pro",
    "kimi-k3": "Kimi K3",
    "kimi-k2.7-code": "Kimi K2.7 Code",
    "grok-4.5": "Grok 4.5",
    "grok-4.6": "Grok 4.6",
    "glm-5.3": "GLM-5.3",
    "glm-5.3-flash": "GLM-5.3-Flash",
    "glm-5.2": "GLM-5.2",
    "gpt-5.5": "GPT-5.5",
    "gpt-6-astra": "GPT-6 Astra",
    "astra": "GPT-6 Astra",
}

PRICE_RE = re.compile(r"(\d+(?:\.\d+)?)\s*/\s*(\d+(?:\.\d+)?)")
CACHE_RE = re.compile(r"cache-?read\s+(\d+(?:\.\d+)?)|cached in\s+(\d+(?:\.\d+)?)")
RETIRING_RES = [
    re.compile(r"[Rr]etiring from \w+ (\d{4}-\d{2}-\d{2})"),
    re.compile(r"[Rr]etired from \w+ (\d{4}-\d{2}-\d{2})"),
    re.compile(r"[Rr]etiring (\d{4}-\d{2}-\d{2})"),
    re.compile(r"retired across all Copilot experiences on (\d{4}-\d{2}-\d{2})"),
]
STATUS_WORDS = [
    "planner-only", "not a seat", "retiring", "retired",
    "default", "candidate", "provisional", "active",
]
KEEP_FIELDS = ("model", "slug", "class", "in", "out", "cache_read", "status", "retiring")


def slug_for(name):
    s = name.lower().replace(" ", "-").replace(".", "-")
    return re.sub(r"-+", "-", s)


def parse_registry():
    rows = []
    in_table = False
    header_seen = False
    for line in REGISTRY.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            in_table = False
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if len(cells) < 7:
            continue
        if cells[0] == "Model":
            in_table, header_seen = True, True
            continue
        if stripped.startswith("| ---") or set(stripped) <= set("|- :"):
            continue
        if not (in_table and header_seen):
            continue
        model, klass, price, _bench, status, _classified, note = cells[:7]
        plain = price.replace("**", "").replace("*", "")
        m = PRICE_RE.search(plain)
        pin = float(m.group(1)) if m else None
        pout = float(m.group(2)) if m else None
        cm = CACHE_RE.search(price)
        cache_read = None
        if cm:
            cache_read = float(cm.group(1) or cm.group(2))
        retiring = None
        for rx in RETIRING_RES:
            rm = rx.search(status) or rx.search(note)
            if rm:
                retiring = rm.group(1)
                break
        base_status = "unclassified"
        low = status.lower()
        for word in STATUS_WORDS:
            if word in low:
                base_status = word
                break
        rows.append({
            "model": model,
            "slug": slug_for(model),
            "class": klass,
            "in": pin,
            "out": pout,
            "cache_read": cache_read,
            "status": base_status,
            "retiring": retiring,
        })
    return rows


def norm(name):
    n = name.strip().lower()
    if n.startswith("claude "):
        n = n[len("claude "):]
    # 1M bills at standard rates. The [1m] suffix picks a window, not a price row.
    n = re.sub(r"\[1m\]$", "", n)
    return n


FAMILIES = ("opus", "sonnet", "haiku", "fable")


def family(r):
    name = norm(r["model"])
    return next((f for f in FAMILIES if f in name), None)


def resolve(name, rows, seat=None):
    key = norm(name)
    # A per-call family alias takes the session's own model when the session
    # already runs that family (Claude Code sub-agents docs). So `opus` on an
    # Opus 5 seat is Opus 5, not the alias's default.
    if seat is not None and key in FAMILIES and family(seat) == key:
        return seat
    if key in ALIASES:
        key = norm(ALIASES[key])
    for r in rows:
        if norm(r["model"]) == key or r["slug"] == key:
            return r
    # Copilot dots a version (grok-4.7) where the generated slug hyphenates it.
    dashed = slug_for(key)
    for r in rows:
        if r["slug"] == dashed:
            return r
    return None


VERSION_RE = re.compile(r"\d+(?:\.\d+)*")


def line_and_version(name):
    """Split a registry name into its model line and version.

    "GPT-6 Luna" and "GPT-5.6 Luna" share the line "GPT-# Luna". "Opus 5.5"
    and "Opus 5" share "Opus #". The first number in the name is the version.
    """
    n = norm(name)
    m = VERSION_RE.search(n)
    if not m:
        return None, None
    version = tuple(int(p) for p in m.group(0).split("."))
    return n[:m.start()] + "#" + n[m.end():], version


def seat_pins(path):
    """Ordered pins of one seat file: its `models:` list, else `model:`."""
    text = Path(path).read_text(encoding="utf-8")
    fm = text.split("---", 2)[1] if text.startswith("---") else ""
    single, listed = None, None
    for raw in fm.splitlines():
        val = raw.split("#", 1)[0].strip()
        if val.startswith("models:"):
            inner = val[len("models:"):].strip().strip("[]")
            listed = [p.strip().strip("'\"") for p in inner.split(",") if p.strip()]
        elif val.startswith("model:"):
            single = val[len("model:"):].strip().strip("'\"")
    return listed or ([single] if single else [])


def cmd_latest(args):
    """Every seat must lead each model line with the newest version.

    The registry is the list of known versions. A seat that names a line
    must name its newest eligible version first, with older versions only
    as fallbacks behind it. Family aliases (sonnet, opus, haiku, fable) are
    skipped: the harness resolves them to its newest version already.
    """
    from datetime import date
    rows = parse_registry()
    today = date.today().isoformat()

    def eligible(r):
        if r["status"] in ("retired", "not a seat"):
            return False
        return not (r["retiring"] and r["retiring"] <= today)

    newest = {}
    for r in rows:
        line, ver = line_and_version(r["model"])
        if line is None or not eligible(r):
            continue
        if line not in newest or ver > newest[line][0]:
            newest[line] = (ver, r["model"])

    seats = sorted(REPO_ROOT.glob(".github/agents/*.agent.md")) + sorted(REPO_ROOT.glob(".claude/agents/*.md"))
    bad = 0
    checked = 0
    for seat in seats:
        seen = set()
        for pin in seat_pins(seat):
            if norm(pin) in FAMILIES or norm(pin) in ("best", "default", "inherit"):
                continue
            r = resolve(pin, rows)
            if r is None:
                print(f"  WARN: {seat.name} pins '{pin}', which names no registry row")
                continue
            line, ver = line_and_version(r["model"])
            if line is None or line in seen:
                continue
            seen.add(line)
            checked += 1
            top_ver, top_name = newest.get(line, (ver, r["model"]))
            if ver < top_ver:
                # Claude Code frontmatter takes one model, not an ordered list.
                fix = ("Pin the family alias instead." if seat.parent.parent.name == ".claude"
                       else f"Put it first, with {r['model']} behind it as the fallback.")
                print(f"  FAIL: {seat.name} leads the {line.replace('#', 'N')} line with {r['model']}, "
                      f"but the registry's newest is {top_name}. {fix}")
                bad += 1
    print(f"{checked} seat line(s) checked, {bad} not on the newest version")
    return 1 if bad else 0


def cmd_build(args):
    rows = parse_registry()
    payload = {
        "generated_from": "model-classes.md",
        "comparison": "list price, $/1M tokens in/out",
        "note": "effective cost can differ: tokenizer ~30%, cache tiers, plan multipliers, switch cost. See routing.md, The cost ceiling.",
        "rows": [{k: r[k] for k in KEEP_FIELDS} for r in rows],
    }
    out = Path(args.out) if args.out else DEFAULT_OUT
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(f"wrote {len(rows)} rows to {out}")
    return 0


def price_row(r):
    if r is None:
        return "unknown"
    return f"{r['model']}: {r['in']}/{r['out']} in/out ({r['class']}, {r['status']})"


def cmd_compare(args):
    rows = parse_registry()
    b = resolve(args.b, rows)
    a = resolve(args.a, rows, seat=b)
    print(price_row(a))
    print(price_row(b))
    if a is None or b is None:
        print("verdict: unknown model (exit 2)")
        return 2
    if a["in"] is None or b["in"] is None or a["out"] is None or b["out"] is None:
        print("verdict: missing published price (exit 2)")
        return 2
    if a["in"] > b["in"] and a["out"] > b["out"]:
        print(f"verdict: {a['model']} prices ABOVE {b['model']} on both axes (ceiling violation, exit 1)")
        return 1
    if a["in"] > b["in"] or a["out"] > b["out"]:
        print(f"verdict: mixed - {a['model']} above on one axis only (no violation, exit 0)")
        return 0
    print(f"verdict: {a['model']} costs no more than {b['model']} (exit 0)")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build", help="write the seat map JSON")
    b.add_argument("--out", default=None)
    b.set_defaults(func=cmd_build)
    c = sub.add_parser("compare", help="compare two models' list prices")
    c.add_argument("a")
    c.add_argument("b")
    c.set_defaults(func=cmd_compare)
    k = sub.add_parser("check", help="same comparison, exit-code contract for gating")
    k.add_argument("a")
    k.add_argument("b")
    k.set_defaults(func=cmd_compare)
    lt = sub.add_parser("latest", help="fail when a seat leads a model line with an older version")
    lt.set_defaults(func=cmd_latest)
    args = ap.parse_args()
    # Exit 1 is the ceiling violation. Python's default exit for an uncaught
    # exception is also 1. Map any crash to 2 (unknown) so the hook stays
    # silent rather than printing a false "prices above the seat" warning.
    try:
        rc = args.func(args)
    except Exception as exc:
        print(f"seat-map: {type(exc).__name__}: {exc} (exit 2)", file=sys.stderr)
        rc = 2
    sys.exit(rc)


if __name__ == "__main__":
    main()
