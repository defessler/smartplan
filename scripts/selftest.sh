#!/usr/bin/env bash
# scripts/selftest.sh — static install doctor for the smartplan family.
#
# Answers "is this checkout/install SHAPED right for smartplan to work?"
# on any machine, service-agnostically: it checks files, not model
# behavior. The runtime half — does the flow actually behave correctly on
# your harness — is the probe rubric in
# docs/selftest.md in the source repo (this script is step 0
# of that rubric).
#
# Works on: a full repo checkout, AND a copilot-export output tree (the
# harness-specific checks skip themselves when their surface is absent).
# Portability: Git-Bash on Windows AND Linux. grep/sed/wc only.

set -u
# Root = nearest ancestor of this script carrying a skills tree — works
# from scripts/ in the repo AND from .github/skills/smartplan/scripts/ in
# a Copilot export.
d="$(cd "$(dirname "$0")" >/dev/null 2>&1 && pwd)"
while [ -n "$d" ] && [ "$d" != "/" ]; do
  if [ -d "$d/.claude/skills" ] || [ -d "$d/.github/skills" ]; then cd "$d"; break; fi
  d="$(dirname "$d")"
done
SKILLS_ROOT=""
for r in .claude/skills .github/skills; do
  if [ -d "$r" ]; then SKILLS_ROOT="$r"; break; fi
done
if [ -z "$SKILLS_ROOT" ]; then
  echo "selftest: no .claude/skills or .github/skills tree found"; exit 1
fi

PASS=0; FAIL=0; SKIP=0
ok()   { echo "  PASS: $1"; PASS=$((PASS+1)); }
bad()  { echo "  FAIL: $1"; FAIL=$((FAIL+1)); }
skip() { echo "  skip: $1"; SKIP=$((SKIP+1)); }

echo "== smartplan selftest (static install surface) =="
echo

# (1) Canonical skill tree: the six family skills, each with a SKILL.md
echo "-- (1) skill tree --"
SKILLS="smartplan smartexec smartreview smartwiki smartvoice smartdiagram"
for s in $SKILLS; do
  if [ -f "$SKILLS_ROOT/$s/SKILL.md" ]; then
    ok "skill present: $s"
  else
    bad "missing skill: $SKILLS_ROOT/$s/SKILL.md"
  fi
done

# (2) Frontmatter sanity: STRICT-YAML-parseable (live 2026-07-10 failure
#     class: an unquoted value containing ': ' fails the whole file on
#     Copilot's parser — "mapping values are not allowed"), name +
#     description present, description < 1024 chars (live 2026-07-09
#     failure class: over-long descriptions refuse to load).
echo "-- (2) frontmatter --"
fm_verdict() {  # fm_verdict <file> -> OK:<desclen> | ERR:<why>
  python - "$1" << 'EOF' 2>/dev/null
import io, re, sys
p = sys.argv[1]
s = io.open(p, encoding='utf-8').read()
if not s.startswith('---\n'): print('ERR:no frontmatter'); raise SystemExit
end = s.find('\n---', 3)
if end < 0: print('ERR:unclosed frontmatter'); raise SystemExit
block = s[4:end]
try:
    import yaml
    try:
        yaml.safe_load(block)
    except Exception as e:
        print('ERR:strict YAML parse failed: %s' % str(e).replace('\n', ' ')[:90]); raise SystemExit
except ImportError:
    pass
for i, line in enumerate(block.split('\n'), start=2):
    m = re.match(r'^[A-Za-z0-9_-]+:\s+(.*)$', line)
    if not m: continue
    v = m.group(1)
    if v[:1] in ('"', "'", '|', '>', '[', '{'): continue
    v = re.split(r'\s#', v, 1)[0]
    if re.search(r':(\s|$)', v):
        print('ERR:line %d has an unquoted value containing a colon (breaks strict YAML parsers)' % i); raise SystemExit
dm = re.search(r'^description:\s*(?:"(.*?)"\s*$|(.+?)\s*$)', block, re.S | re.M)
if not dm: print('ERR:no description'); raise SystemExit
print('OK:%d' % len((dm.group(1) or dm.group(2)).strip()))
EOF
}
for s in $SKILLS; do
  f="$SKILLS_ROOT/$s/SKILL.md"
  [ -f "$f" ] || continue
  v="$(fm_verdict "$f")"
  case "$v" in
    OK:*)
      desc_len="${v#OK:}"
      if [ "$desc_len" -ge 1024 ]; then
        bad "$s: description is $desc_len chars (must be < 1024 or the harness refuses to load it)"
      else
        ok "$s: frontmatter strict-YAML-safe, description $desc_len chars"
      fi ;;
    *)
      bad "$s: ${v#ERR:}" ;;
  esac
done

# (3) Flow-critical references: every file SKILL.md's flow loads must exist
echo "-- (3) flow-critical references --"
for r in routing.md model-classes.md brief.md check.md cpp-gamedev-check.md \
         artifacts.md; do
  if [ -f "$SKILLS_ROOT/smartplan/references/$r" ]; then
    ok "reference present: $r"
  else
    bad "missing flow-critical reference: $r"
  fi
done

# (4) Copilot surface (skips when absent — e.g. a non-Copilot checkout)
echo "-- (4) Copilot surface --"
if [ -d ".github/agents" ]; then
  n=$(ls .github/agents/*.agent.md 2>/dev/null | wc -l)
  if [ "$n" -eq 6 ]; then
    ok "6 Copilot agent profiles present"
  else
    bad "expected 6 .github/agents/*.agent.md profiles, found $n"
  fi
  for a in .github/agents/*.agent.md; do
    v="$(fm_verdict "$a")"
    case "$v" in
      OK:*) ok "$(basename "$a"): frontmatter strict-YAML-safe" ;;
      *)    bad "$(basename "$a"): ${v#ERR:}" ;;
    esac
  done
else
  skip ".github/agents absent (not a Copilot-facing checkout)"
fi

# (5) Marketplace manifest (skips in a copilot-export tree, which drops it)
echo "-- (5) marketplace manifest --"
if [ -f ".claude-plugin/marketplace.json" ]; then
  if grep -q '"source": "./"' .claude-plugin/marketplace.json && grep -q '"strict": false' .claude-plugin/marketplace.json; then
    ok "single-manifest plugin definition intact (source ./ + strict:false)"
  else
    bad "marketplace.json missing the inline plugin definition (source ./ / strict:false)"
  fi
  if command -v claude >/dev/null 2>&1; then
    if claude plugin validate . >/dev/null 2>&1; then
      ok "claude plugin validate: passed"
    else
      bad "claude plugin validate: FAILED (run it directly for detail)"
    fi
  else
    skip "claude CLI not on PATH — validator not run"
  fi
else
  skip ".claude-plugin/marketplace.json absent (copilot-export tree, or not the source repo)"
fi

echo
echo "======================================"
echo "selftest: $PASS pass · $FAIL fail · $SKIP skipped"
if [ "$FAIL" -gt 0 ]; then
  echo "selftest: FAIL"
  exit 1
fi
echo "selftest: PASS — static surface is sound. Runtime behavior: run the"
echo "probes in docs/selftest.md (source repo) on your harness."
exit 0
