"""voice_hook.py - smartvoice's resident hook runtime for Claude Code and Copilot CLI.

install_voice.py copies this file next to a rules.md taken from the resolved
voice profile, then wires one hook per mode:

    claude-stop             Claude Code Stop hook. Scans last_assistant_message
                            and exits 2 with the violations on stderr, at most
                            once per turn, when the reply breaks a character ban.
    claude-subagent-start   Claude Code SubagentStart hook. Injects rules.md into
                            every new subagent as additionalContext.
    copilot-stop            Copilot CLI agentStop hook. Scans the last
                            assistant.message in transcriptPath and answers
                            {"decision": "block"} on a violation.
    copilot-subagent-start  Copilot CLI subagentStart hook. Prints
                            {"additionalContext": rules}.
    check                   Scan text on stdin, print each violation, exit 1 on any.

Bans come from --ban, a comma list of `dashes` and `semicolons`. The scan skips
fenced code, inline code, blockquotes, URLs, and smartplan's routing-call line,
because the rules exempt code and a skill's literal output format.

A hook must never break a session. Bad JSON, a missing transcript, an unreadable
rules file, or a malformed command line all exit 0 quietly. Set
SMARTVOICE_HOOKS=off to turn every hook mode off for one run, for example in a
benchmark arm. Set SMARTVOICE_HOOK_LOG to a file path to append one JSON line
per hook call.
"""
import argparse
import io
import json
import os
import re
import sys

VALID_BANS = ("dashes", "semicolons")
DASH_CHARS = ("—", "–")
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
INLINE_CODE = re.compile(r"(`+)(?:(?!\1).)+?\1")
URL = re.compile(r"https?://\S+")
EXEMPT_LINE = re.compile(r"^\s*(?:>|Routing call:)")
SEMICOLON = re.compile(r";(?=\s|$)")
DOUBLE_HYPHEN = re.compile(r"(?<=\S) -- (?=\S)")
MAX_SHOWN = 5


def prose_lines(text):
    """Yield (line_number, line) for prose, with code and exempt lines removed."""
    fence = None
    for number, line in enumerate(text.splitlines(), 1):
        match = FENCE.match(line)
        if fence:
            if match and match.group(1)[0] == fence[0] and len(match.group(1)) >= len(fence):
                fence = None
            continue
        if match:
            fence = match.group(1)
            continue
        if EXEMPT_LINE.match(line):
            continue
        yield number, URL.sub(" ", INLINE_CODE.sub(" ", line))


def scan(text, bans):
    """Return [(line_number, kind, excerpt)] for every banned character in prose."""
    hits = []
    for number, line in prose_lines(text or ""):
        excerpt = line.strip()
        if "dashes" in bans and (any(c in line for c in DASH_CHARS) or DOUBLE_HYPHEN.search(line)):
            hits.append((number, "dash", excerpt))
        if "semicolons" in bans and SEMICOLON.search(line):
            hits.append((number, "semicolon", excerpt))
    return hits


def describe(hits, bans):
    banned = []
    if "dashes" in bans:
        banned.append("em or en dashes")
    if "semicolons" in bans:
        banned.append("prose semicolons")
    shown = "\n".join(
        "  line %d (%s): %s" % (number, kind, excerpt[:120]) for number, kind, excerpt in hits[:MAX_SHOWN]
    )
    if len(hits) > MAX_SHOWN:
        shown += "\n  and %d more" % (len(hits) - MAX_SHOWN)
    return (
        "smartvoice: your last reply used %s outside code in %d place(s).\n%s\n"
        "Send one short follow-up that restates only those sentences without them. "
        "Don't edit any files, and don't repeat the whole reply." % (" or ".join(banned), len(hits), shown)
    )


def last_copilot_reply(path):
    """Return the content of the last non-empty assistant.message in a Copilot transcript."""
    last = ""
    with io.open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if '"assistant.message"' not in line:
                continue
            try:
                event = json.loads(line)
            except ValueError:
                continue
            if event.get("type") != "assistant.message":
                continue
            content = (event.get("data") or {}).get("content")
            if isinstance(content, str) and content.strip():
                last = content
    return last


def read_event():
    try:
        raw = sys.stdin.buffer.read().decode("utf-8", "replace")
        event = json.loads(raw) if raw.strip() else {}
        return event if isinstance(event, dict) else {}
    except (ValueError, OSError):
        return {}


def read_rules(path):
    try:
        with io.open(path, encoding="utf-8") as fh:
            return fh.read().strip()
    except (OSError, TypeError):
        return ""


def emit(stream, text):
    # Bytes, not str: a Windows pipe defaults to the ANSI code page, which can't
    # encode the very dash the message is quoting back.
    stream.buffer.write(text.encode("utf-8"))
    stream.buffer.flush()


def log(record):
    path = os.environ.get("SMARTVOICE_HOOK_LOG")
    if not path:
        return
    try:
        with io.open(path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(record) + "\n")
    except OSError:
        pass


def run(args):
    bans = {b.strip() for b in args.ban.split(",") if b.strip() in VALID_BANS}

    if args.mode == "check":
        text = sys.stdin.buffer.read().decode("utf-8", "replace")
        hits = scan(text, bans)
        for number, kind, excerpt in hits:
            emit(sys.stdout, "line %d (%s): %s\n" % (number, kind, excerpt))
        return 1 if hits else 0

    if os.environ.get("SMARTVOICE_HOOKS", "").strip().lower() in ("off", "0", "false", "no"):
        return 0

    event = read_event()
    active = bool(event.get("stop_hook_active") or event.get("stopHookActive"))

    if args.mode == "claude-stop":
        hits = [] if active else scan(event.get("last_assistant_message") or "", bans)
        log({"mode": args.mode, "active": active, "hits": len(hits)})
        if hits:
            emit(sys.stderr, describe(hits, bans))
            return 2
        return 0

    if args.mode == "copilot-stop":
        path = event.get("transcriptPath")
        text = ""
        if not active and path:
            try:
                text = last_copilot_reply(path)
            except OSError:
                text = ""
        hits = scan(text, bans)
        log({"mode": args.mode, "active": active, "hits": len(hits)})
        if hits:
            emit(sys.stdout, json.dumps({"decision": "block", "reason": describe(hits, bans)}))
        return 0

    rules = read_rules(args.rules)
    log({"mode": args.mode, "rules_bytes": len(rules)})
    if not rules:
        return 0
    if args.mode == "claude-subagent-start":
        payload = {"hookSpecificOutput": {"hookEventName": "SubagentStart", "additionalContext": rules}}
    else:
        payload = {"additionalContext": rules}
    emit(sys.stdout, json.dumps(payload))
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description="smartvoice resident hook runtime")
    parser.add_argument(
        "mode",
        choices=["claude-stop", "claude-subagent-start", "copilot-stop", "copilot-subagent-start", "check"],
    )
    parser.add_argument("--rules", help="rules file injected by the subagent-start modes")
    parser.add_argument("--ban", default="", help="comma list: dashes, semicolons")
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        # A usage error from a Stop hook would exit 2, which blocks the turn.
        # Only `check` run by hand is allowed to fail loudly.
        wanted = list(sys.argv[1:] if argv is None else argv)
        return exc.code if wanted[:1] == ["check"] or "-h" in wanted or "--help" in wanted else 0
    try:
        return run(args)
    except Exception:  # noqa: BLE001 - a hook must never break the session it serves
        return 1 if args.mode == "check" else 0


if __name__ == "__main__":
    sys.exit(main())
