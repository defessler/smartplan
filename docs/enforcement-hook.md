# smartplan §A deep reference: mechanical tiering enforcement (optional)

> Facts verified 2026-07-06 against code.claude.com/docs (hooks, sub-agents,
> permissions) and the anthropics/claude-code CHANGELOG (v2.1.178+); see
> the development repo's claim ledger.

Load this only when you want tiering **enforced mechanically**, not just
socially agreed — a bad dispatch gets blocked outright, not caught later by
reading the transcript or the bill. §A's per-call `model:` override stays
the primary lever. This is a guardrail on top of it.

**A wired, warn-only instance runs in the development repo** as
`.claude/settings.json` + `.claude/hooks/require-tiered-dispatch.sh`. Neither
file ships in this bundle — settings.json carries machine-local configuration
that has no business in a distribution. Build your own from the matcher block
and script below, both reproduced in full on this page, and you get the
warning layer: it prints a `stderr` warning on an un-tiered, or Opus/Fable-on-
an-implementer-leaf, `Agent`/`Task` dispatch, and **never blocks anything**
(see the safety note in "Shipped instance" below). Everything else on this
page — including both hard-`deny` variants — is documented as **opt-in**,
off by default, so adopting this reference can never silently block
dispatch in a repo (like this one) that fans work out to subagents when a
fan-out signal holds.

## Declarative layer: settings.json permission rules (opt-in hard-deny)

No script needed. Since v2.1.178, permission rules support `Tool(param:value)`
syntax (`*` wildcard) matched against the tool's resolved input. Deny specific
model values on `Agent` dispatch to hard-block a tier from ever landing
without a human lifting the rule:

```json
{
  "permissions": {
    "deny": ["Agent(model:opus)", "Agent(model:fable)"],
    "allow": ["Agent(model:sonnet)", "Agent(model:haiku)"]
  }
}
```

This blocks Opus/Fable leaf spawns while leaving Sonnet/Haiku untouched. It
does **not** catch a dispatch that omits `model:` entirely (inherits the
session model) — that needs the hook below.

**Not active by default.** The shipped `.claude/settings.json` registers
only the warn-only hook (next section) — no `permissions` key at all. To
turn this on, merge the `permissions` block above into `.claude/settings.json`
alongside its existing `hooks` key: one paste, no script edit.

## Scripted layer: PreToolUse hook

### Shipped instance (default: warn-only, non-blocking)

`.claude/settings.json` wires the hook:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Task|Agent|Workflow",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"${CLAUDE_PROJECT_DIR}/.claude/hooks/require-tiered-dispatch.sh\""
          }
        ]
      }
    ]
  }
}
```

(`Task|Agent` hedges the dispatch tool's name across Claude Code docs/
versions, which use both spellings — the script re-checks `tool_name` itself
rather than trusting the matcher alone, since this environment has at least
one unrelated tool whose name merely *contains* "Task" as a substring
(`TaskStop`). The explicit `bash` prefix sidesteps shebang/exec-bit
ambiguity on a Windows checkout, which is this repo's own dev environment.)

`Workflow` joined the matcher on 2026-08-05. A dynamic workflow spawns its own
fleet from inside a script the hook can't read, and every `agent()` stage
inherits the session model unless the script passes `opts.model` per call — so
before that change the one dispatch path that fans out widest was also the only
one the guardrail never saw. The launch is the last point a warning can land,
since nothing stops the script once it starts. Same contract as the rest: one
stderr line, always exit 0.

The fork branch changed the same day, and it inverted. A `fork` subagent always
runs the session model and the harness **ignores** a `model` passed to it,
without erroring. So an omitted model on a fork is correct and stays silent,
while *passing* one is now the warned case: the caller believes they tiered
down, they didn't, and nothing else in the harness says so.

Since Claude Code 2.1.232 (2026-08-13) forking is on by default, so Claude can
pick `subagent_type: fork` unprompted. The hook sees that dispatch (its matcher
is the tool name) and stays silent, correctly, because a bare fork is a valid
fork. What it can't tell you is whether *you* asked for it. Measured 2026-08-16
on this machine: a two-word fork probe with zero tool uses billed 601,326
subagent tokens in 3.6 seconds, since a fork inherits the whole parent context.
Cached tokens are cheap, and that is still the per-call price of a fork nobody
requested on the session model. The durable defense is the note in
`claude-code.md`, not a hook change.

`.claude/hooks/require-tiered-dispatch.sh` reads that payload's `tool_input`
and prints one `stderr` line when:

- `model` is missing entirely (the dispatch silently inherits the session
  model, which may be an expensive tier), or
- `model` is `opus`/`fable` **and** the description/prompt doesn't read like
  a planning/research task (a crude keyword heuristic, not a real
  classifier — opus/fable-for-planning is the documented `opusplan`
  pattern, not a violation).

`subagent_type: fork` is skipped before either check: `model:` is a
documented no-op there, since a fork always inherits the parent/session
model. jq is used when present, for a correct parse; a best-effort grep/sed
fallback covers machines without it — this repo's own Windows/Git-Bash dev
box has no `jq` at authoring time, so the fallback is the path actually
exercised day to day here, not a hypothetical. **The script always exits
0** and never emits a `hookSpecificOutput` object, so there is nothing for
Claude Code to act on beyond the warning text — wiring it up cannot break
existing dispatch, including the fan-out this repo runs on the tasks where
a fan-out signal holds.

### Opt-in hard-deny variant (not what ships)

To make the *hook itself* block instead of warn — the one thing the
declarative layer above can't do, since it can't see a `model:` field that
was never provided — swap the shipped script's decision tail for this:

```sh
model="$(cat | jq -r '.tool_input.model // empty')"
if [ -z "$model" ]; then
  echo '{"hookSpecificOutput":{"permissionDecision":"deny","permissionDecisionReason":"dispatch missing explicit model: field"}}'
  exit 2
fi
exit 0
```

This is a full behavior change (a missing `model:` goes from "printed
warning" to "blocked dispatch"), not a settings.json toggle — test it
against this repo's own fan-out before shipping it as a project default, or
the safety note above about not bricking the orchestration stops holding.

## Caveats

- Hooks run with **user permissions** — no extra sandboxing beyond your shell.
- Keep the deny list in **project** `settings.json` (not local/personal) so
  it ships with the repo and applies to every contributor.
- An Opus/Fable escalation must go through a **human toggling the rule** —
  that friction is the point, not a bug to route around.
- Enforces §A (Claude Code) only. Other harnesses enforce tiering via their
  own per-harness config (§B–§E), not this mechanism.

## Auto-trigger recipe (default the routing policy without naming the skill)

What these layers default is the **routing policy**, not the ceremony. A
plainly one-context, non-risky task still runs inline without the skill body
loaded, and smartplan gets invoked when a fan-out signal holds. Three layers,
weakest to strongest; stack them:

1. **Description matching** — smartplan's description opens with "Use
   proactively for any coding or implementation task", the documented lever
   for auto-delegation. The clause right after it does the regime split, so
   a match hands the task to the router rather than to a wave. Free, but
   probabilistic.
2. **Standing instruction** — CLAUDE.md / AGENTS.md carry the default-policy
   rule ("Route every coding or implementation task by regime yourself ...
   Invoke `smartplan` only when a fan-out signal holds"). Loaded every
   session on every harness that reads those files.
3. **SessionStart hook (mechanical)** — inject the rule as context at session
   start so it survives long sessions and compaction:

```json
{
  "hooks": {
    "SessionStart": [{
      "hooks": [{
        "type": "command",
        "command": "echo '{\"hookSpecificOutput\":{\"hookEventName\":\"SessionStart\",\"additionalContext\":\"Default policy: route coding tasks by regime yourself - plainly one-context, non-risky tasks run inline without the skill body; invoke smartplan only on a fan-out signal (beyond-context working set, a failed first fix, verify-gated class, wall-clock batch). It routes by regime - one-context tasks run inline; fan-out is for beyond-context scale, rework-prone execution, verify-gated work, and wall-clock batches.\"}}'"
      }]
    }]
  }
}
```

Claude Code only; on other harnesses the standing-instruction layer is the
mechanical one (AGENTS.md-style standing files load unconditionally).

## Binding code conventions at write time (the inline-route gap)

The family's review machinery (`smartreview` and its `{{STANDARDS}}` doc)
runs over a *finished* changelist, and briefs bind executors on the fan-out
route. Neither reaches the **inline** route, which the default policy makes the
common case for a single-file edit — and at the moment `Write`/`Edit` fires
there, the skill bodies aren't loaded and the shipped PreToolUse hook only
matches `Task|Agent|Workflow`, so it never sees a code write at all. (That
matcher gained `Workflow` on 2026-08-05; this sentence said `Task|Agent` until
2026-08-21, contradicting the JSON above it.) Since v4.103.0 the gap is
narrower for *correctness* and unchanged for *conventions*: smartreview now
hunts breaking defects at the merge gate, so an inline-route bug has one more
place to get caught before it ships. A convention violation still has none. Honest scope: that
leaves exactly two surfaces in context, the standing file and any SessionStart
injection, and both are prompts rather than gates. Neither can *guarantee*
conformance; they make the doc present at the moment code is written, which is
the difference between conforming code and a review that finds the drift later.

Stack the same three layers, pointed at the conventions doc rather than the
routing doctrine. Epic ships the same mechanism for UE conventions in its own
Claude Code plugin, so the pattern is not novel.

1. **Standing file** — one line in the project's CLAUDE.md / AGENTS.md naming
   the doc and requiring it be read before the first edit to a source file.
2. **SessionStart injection** — the block above, with the text swapped for:
   `Conventions: code written in this project conforms to <abs path>. Read it
   before the first source edit, inline route included. A violation of a
   declared rule is a defect, not a style note.` Keep it under ~300B; it bills
   into every session.
3. **Brief + verify** — on fan-out, `brief.md`'s CONVENTIONS block pins the doc
   path and rule IDs, and `check.md` step 5 FAILs a violation of a declared
   rule. This layer *is* mechanical, and it is why fan-out conformance is
   stronger than inline conformance.

Install it in the project whose code is being written, not in the skills repo:
the standards doc travels with the codebase it governs.

## Cross-harness note: Copilot CLI has a real hook lever

Everything above is §A (Claude Code)-only, per the caveat above. Copilot
CLI sits closest: it has its own real `preToolUse` hook event (JSON, under
`~/.copilot/hooks/` or `.github/hooks/` — see `references/copilot.md`)
that the warn-only pattern above would port to directly. This repo doesn't
yet ship that port as a file, unlike the Claude Code instance above — a
gap, not a claim otherwise. (A Codex CLI worked example lived here until
Codex support was dropped, 2026-07-10.)
