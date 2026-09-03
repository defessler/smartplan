# smartplan

**v4.119.0** · MIT · Model-tiering skills for AI coding agents.

Plan with the strong model. Implement with the cheaper model. Escalate on
demonstrated failure, never on a hunch.

This is the **release** repo: the runtime only. Install it in Claude Code or
GitHub Copilot CLI and the skills self-trigger from their descriptions. You
don't have to invoke anything by hand.

## Does it work?

Seven scenarios, run with the skill and without it, on three model tiers,
three independent judges grading every response.

| | With the skill | Without |
| --- | --- | --- |
| **All cases** | **62 / 63** | 4 / 21 |

It carries on the cheap seat, not just the tier it was written on. The newest
case passed 3/3 on Haiku, Sonnet and Opus alike.

**Two caveats ride with those numbers.** The no-skill arm was *told* not to use
the skill rather than prevented from it, and the run is a hand-built stand-in
for the vendor's own eval harness while that is in early access. One of the seven
cases passes without the skill too — a bare model already ranks a memory bug
above naming nits — and it stays in the suite for exactly that reason.

## Install

**Claude Code**

```
/plugin marketplace add defessler/smartplan
/plugin install sp@smartplan
```

Commands land namespaced, so you get `/sp:smartplan`. The bare
`/smartplan` still works if you copy the tree into a project instead.

**GitHub Copilot CLI**

```
/plugin marketplace add defessler/smartplan
/plugin install sp
```

Copilot also reads `.claude/skills/` directly, so cloning this repo into a
project works without the plugin step. The six pinned agent seats in
`.github/agents/` come with the plugin install.

**One caveat worth knowing.** Plugin skills load at the lowest precedence
slot. `.github/skills/` and `.claude/skills/` are project-level locations,
so a same-named skill sitting in your project silently shadows the plugin
copy. A marketplace install and a local checkout don't merge. Pick one.

## What's in the box

Two skills carry the loop. `smartplan` is the entry point and the routing
policy, and it loads its own references for routing, brief-writing and
verification. `smartexec` is the executor payload that rides along with a
cheap model.

Four companions are optional and independent. `smartreview` reviews a
changelist against a swappable per-project standards doc and ranks what it
finds: game-breaking bugs first, then best practices, then conventions. It
ships defaulting to C++ gamedev with Unreal, custom-engine and vanilla
profiles. `smartwiki` turns
one change into a stakeholder-facing page. `smartvoice` is a house-voice
pass that resolves a profile per user. `smartdiagram` builds curated
interactive architecture diagrams.

## What it actually does

It routes by regime. A task one strong context can swallow whole runs
**inline**, because the full fan-out ceremony measured 1.5x to 2.9x the cost
of a single inline pass at equal output quality, across every leaf count and
size tested. Fan-out is reserved for work that exceeds one context window,
execution that's proven prone to rework, batches bound by wall-clock, and
merges that need an independent check.

The verify floor never collapses, whichever route you're on. It ranks the
oracle rather than just asking for a fresh one: an executable check beats a
fresh-context model, which beats a same-context model.

That "fan-out usually loses" finding is the project's own, measured against
itself and published rather than buried. Three independent sources have since
agreed.

## Voice profiles

`smartvoice` ships the generic `defaultvoice.md` only. The per-user
mechanism is live, so drop your own `<username>.md` into
`.claude/skills/smartvoice/references/voice-profiles/` and it resolves from
your OS username automatically. Copy the shape of the shipped profile.

## Contents

Everything here is runtime. The development repo (benchmarks, research notes,
the site sources, the gates) is separate.

```
.claude/skills/          the six skills, read by BOTH harnesses
.claude/agents/          four tool-locked Claude Code agent seats
.claude-plugin/          Claude Code marketplace manifest
.github/plugin/          Copilot plugin + marketplace manifests
.github/agents/          six pinned Copilot agent seats
docs/                    the four reference pages the skills link to
scripts/                 the mechanical verifier and the install selftest
```

Verify an install with `bash scripts/selftest.sh`, which checks the static
surface in about two seconds.

## License

MIT. See [LICENSE](LICENSE).
