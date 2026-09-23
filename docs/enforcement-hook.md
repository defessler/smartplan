# smartplan §A deep reference: mechanical tiering enforcement (optional)

> Facts first verified 2026-07-06. The hook, sub-agent and permission claims
> were re-read on 2026-09-15 against code.claude.com/docs and the
> anthropics/claude-code CHANGELOG. The hook output channel, the matcher
> rules and Copilot CLI's handling of this hook were re-read on 2026-09-22
> against code.claude.com/docs/en/hooks and docs.github.com's Copilot hooks
> reference. See the development repo's claim ledger.

Load this only when you want tiering **enforced mechanically**, not just
socially agreed. A bad dispatch gets blocked outright, not caught later by
reading the transcript or the bill. §A's per-call `model:` override stays
the primary lever. This is a guardrail on top of it.

**A wired, warn-only instance runs in the development repo** as
`.claude/settings.json` + `.claude/hooks/require-tiered-dispatch.sh`. Neither
file ships in this bundle. Build your own from the matcher block and the
behavior described below. That gets you the warning layer. On an un-tiered,
or Opus/Fable-on-an-implementer-leaf, `Agent`/`Task` dispatch it emits one
note that you see and Claude reads. It **never blocks anything** (see
"Reference instance" below for how that holds on Copilot CLI too).
Everything else on this page, including both hard-`deny` variants, is
**opt-in** and off by default. Adopting this reference can't silently block
dispatch in a repo (like this one) that fans work out to subagents when a
fan-out signal holds.

## Declarative layer: settings.json permission rules (opt-in hard-deny)

No script needed. Since v2.1.178, permission rules support `Tool(param:value)`
syntax (`*` wildcard) matched against the literal input Claude sends, before
any normalization. Deny specific model values on `Agent` dispatch to
hard-block a tier from ever landing without a human lifting the rule:

```json
{
  "permissions": {
    "deny": ["Agent(model:*opus*)", "Agent(model:*fable*)"]
  }
}
```

This blocks Opus/Fable leaf spawns requested by alias or by full model ID.
Allow rules can't match parameters. Sonnet/Haiku need no entry. It
does **not** catch a dispatch that omits `model:` entirely (inherits the
session model). That needs the hook below.

**Not active by default.** The development repo's `.claude/settings.json`
registers only the warn-only hook (next section), with no `permissions` key at
all. To turn this on, merge the `permissions` block above into
`.claude/settings.json` alongside its existing `hooks` key: one paste, no
script edit.

## Scripted layer: PreToolUse hook

### Reference instance (warn-only, non-blocking)

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
            "command": "bash -c 'f=\"${CLAUDE_PROJECT_DIR:-.}/.claude/hooks/require-tiered-dispatch.sh\"; if [ -f \"$f\" ]; then exec bash \"$f\"; fi; exit 0'"
          }
        ]
      }
    ]
  }
}
```

A matcher made only of letters and `|` is a list of exact tool names to
Claude Code, not a regex. So `TaskStop` can't match `Task|Agent|Workflow`.
`Task` is the dispatch tool's pre-2.1.63 name, still accepted as an alias.
The script re-checks `tool_name` for an exact `Agent`, `Task` or `Workflow`
anyway, which costs nothing.

The command is one single-quoted `bash -c` string. That way bash, not the
shell that launches the hook, expands `${CLAUDE_PROJECT_DIR}`. Each part
closes a gap that matters once Copilot CLI loads the same file (see the
Copilot section at the end):

- **`bash -c '...'`.** Copilot runs a hook's `command` under PowerShell on
  Windows. There, `${CLAUDE_PROJECT_DIR}` names a PowerShell variable, not
  the environment variable, and expands to nothing. Single quotes hand the
  text to bash untouched.
- **`${CLAUDE_PROJECT_DIR:-.}`.** Claude Code sets the variable. Copilot
  documents it for plugin hooks only. Under Copilot the path falls back to
  the working directory. Copilot runs hook commands in the project root
  when no `cwd` is set (CLI 1.0.88).
- **`if [ -f "$f" ] ... exit 0`.** A missing script becomes a silent no-op,
  never a non-zero exit. Copilot fails closed on a non-zero `preToolUse`
  exit. Without this test a bad path there denies the dispatch.

Running the script as `bash "$f"` still sidesteps shebang and exec-bit
ambiguity on a Windows checkout, which is this repo's own dev environment.
The string was tested on 2026-09-22 by running it under each shell on that
box, not yet through a live Copilot dispatch:

- bash with `CLAUDE_PROJECT_DIR` set, the Claude Code shape: runs the hook.
- bash with the variable unset, from the repo root, the Copilot shape on
  Linux and macOS: runs the hook.
- pwsh 7.6 from the repo root, the Copilot shape on Windows: runs the hook.
- Any launch from outside the repo with the variable unset: exits 0
  silently.
- Windows PowerShell 5.1: strips the inner quotes, then exits 0 silently.
  No note and no deny.

`Workflow` joined the matcher on 2026-08-05. A dynamic workflow spawns its own
fleet from inside a script the hook can't read. Each workflow agent's model
follows the subagent order. A model the script names counts as the
per-invocation model, then comes the agent definition's model, then
`CLAUDE_CODE_SUBAGENT_MODEL`, then the session model. So exporting
`CLAUDE_CODE_SUBAGENT_MODEL` also catches stages that set no model.
`CLAUDE_CODE_SUBAGENT_MODEL_FORCE` (v2.1.257 or later) forces one model onto
subagents, teammates and workflow agents alike. Before 2026-08-05 the one
dispatch path that fans out widest was also the only one the guardrail never
saw. The launch is the last point a note can reach you or Claude, since
nothing stops the script once it starts. Same contract as the rest: one JSON
note, always exit 0.

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
and emits one note when:

- `model` is missing entirely (the dispatch runs the seat's frontmatter
  model if the seat pins one, else `CLAUDE_CODE_SUBAGENT_MODEL`, else the
  session model, which may be an expensive tier). A `smartplan-*` seat
  stays silent, since it pins its own model, or
- `model` is in the Opus or Fable tier, matched by family (an alias like
  `opus`, a full id like `claude-opus-5-5` or `claude-opus-5`, or `best`,
  which resolves to Fable where Fable is available and always counts as
  the Fable tier here. The family match is future-proofing, since the
  Agent tool's per-call `model` takes only `sonnet`, `opus`, `haiku` and
  `fable` in Claude Code 2.1.280), **and** the description/prompt
  doesn't read like a planning/research task (a crude keyword heuristic,
  not a real classifier. Opus/fable-for-planning is the documented
  `opusplan` pattern, not a violation. A verifier seat also excuses Opus.
  Fable gets the narrower pass of an architecture or decomposition
  decision), or
- `model` **prices above the session seat on both list-price axes** per
  the generated seat map (`scripts/seat-map.py`, derived from
  `model-classes.md`), when the seat is exported as `$SMARTPLAN_SEAT`
  (added 2026-09-21). PreToolUse payloads carry no session-model field.
  The seat arrives by environment instead. The note stays silent when
  it's unset or either model is unknown. Nothing exports it by default.
  The seat map resolves dotted Copilot slugs such as `grok-4.7`. It prices
  a per-call family alias like `opus` as the session's own model when the
  seat is already that family. The ceiling's enforcement lives in
  `routing.md` § The cost ceiling. This note is its observability half.
  It compares list price only.

`subagent_type: fork` is skipped before any of these checks: `model:` is a
documented no-op there, since a fork always inherits the parent/session
model. jq is used when present, for a correct parse. A best-effort grep/sed
fallback covers machines without it. This repo's own Windows/Git-Bash dev
box had no `jq` at authoring time. The fallback is the path actually
exercised day to day here, not a hypothetical.

**How the note reaches anyone.** The script always exits 0. When it has a
note, it prints it as one JSON object on stdout:

```json
{"systemMessage":"[require-tiered-dispatch] <note> (warn-only, not blocked)",
 "hookSpecificOutput":{"hookEventName":"PreToolUse",
  "additionalContext":"[require-tiered-dispatch] <note> (warn-only, not blocked)"}}
```

`systemMessage` is the warning Claude Code shows you.
`additionalContext` lands in Claude's context beside the tool result,
wrapped as a system reminder rather than a chat message. The object
carries no `permissionDecision`. Exit 0 doesn't approve the call either. So
the permission flow runs exactly as it would without the hook. Notes are
written as facts, not commands, because the hooks docs warn that text
framed as out-of-band system commands can trip Claude's prompt-injection
defenses.

JSON is the channel because nothing else on exit 0 is seen. Claude Code
sends exit-0 stderr to the debug log only. Plain PreToolUse stdout that
doesn't parse as JSON goes there too. Neither you nor Claude sees either
one. The hooks reference says so explicitly as of 2026-09-22. No archived
copy of that page ever stated that exit-0 stderr was visible either. A
stderr-only build of this hook fired 69 notes across 14 sessions on the
dev box by that date. None of them reached a tool result or Claude.

The script still echoes each note to stderr, as an audit trail rather
than a warning. Claude Code 2.1.280 keeps that copy in the session JSONL
as a `hook_success` attachment (observed on the dev box, not documented).
A script can count notes from there after the fact. Reading stderr live
takes `--debug` or `--debug-file` at launch, or `/debug` mid-session.
`--debug` writes `~/.claude/debug/<session-id>.txt` and prints nothing to
the terminal.

Building the JSON needs no jq. `finish()` assembles it with `printf`,
escaping backslashes and double quotes and dropping control characters.
That keeps a model id or seat string from breaking the object. A
schema-invalid object would still only show a hook-error notice, never a
block.

Wiring it up can't break existing dispatch on Claude Code, including the
fan-out this repo runs on the tasks where a fan-out signal holds. On
Copilot CLI the `bash -c` wrapper above is what keeps that true.

### Opt-in hard-deny variant (off by default)

To make the *hook itself* block instead of warn (the one thing the
declarative layer above can't do, since it can't see a `model:` field that
was never provided), swap the reference script's decision tail, its closing
`if`/`elif` block, for this. It replaces that block only, never the whole
script. The `Workflow` and `fork` early exits above it still run first. By
then `$model`, `$tier_family`, `$planningish`, `$decisionish` and
`$verifier_seat` are all set. So is the script's `note` function.
The deny fires only when jq parsed the payload. The grep/sed fallback is
only good enough for a warning. Without jq, a dispatch with no `model:`
gets a warn-only note instead. The snippet must not re-read stdin, because the script's head has already
drained it.

```sh
if [ -z "$model" ] && command -v jq >/dev/null 2>&1; then
  printf '%s\n' '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"dispatch missing explicit model: field"}}'
  exit 0
elif [ -z "$model" ]; then
  note "This Agent dispatch sets no model. Without jq the deny can't fire. The dispatch runs."
elif [ "$tier_family" = "fable" ] && [ "$decisionish" = "0" ]; then
  note "This dispatch pins model:$model (Fable tier) on a task that doesn't read like an architecture or decomposition decision."
elif [ "$tier_family" = "opus" ] && [ "$planningish" = "0" ] && [ "$verifier_seat" = "0" ]; then
  note "This dispatch pins model:$model (Opus tier) on a task that doesn't read like planning or research."
fi
```

`hookSpecificOutput` requires a `hookEventName` field. On a deny,
`permissionDecisionReason` is what Claude reads. The three surviving
warnings call `note`. Their text rides the JSON object `finish` prints,
just as in the warn-only script. A bare `echo ... >&2` there would reach
the debug log only. Keeping the `elif` keeps those warnings visible.

Printing JSON on exit 0 is one documented deny channel. Exit 2 with the
reason on stderr and no JSON is the other. Pick one per hook rather than
mixing them. Don't reach for exit 1 to make a warning visible. Claude Code
shows it as a hook-error notice with stderr's first line and never passes
it to Claude. Copilot CLI treats any non-zero `preToolUse` exit as a deny.

The reference script carries the cost-ceiling note block after that tail and
before `finish`. Keep it when swapping: it has no deny path by design, since
a price comparison that can misresolve a model name must never block.

This is a full behavior change (a missing `model:` goes from a visible note
to a blocked dispatch), not a settings.json toggle. Test it against this
repo's own fan-out before shipping it as a project default. Otherwise the
safety note above about not bricking the orchestration stops holding.
Copilot CLI loads the same hook. Test a Copilot dispatch from the repo root
too.

## Caveats

- Hooks run with **user permissions**, with no extra sandboxing beyond your shell.
- Keep the deny list in **project** `settings.json` (not local/personal) so
  it ships with the repo and applies to every contributor.
- An Opus/Fable escalation must go through a **human toggling the rule**.
  That friction is the point, not a bug to route around.
- Written for §A (Claude Code). Copilot CLI loads the hook as well (see the
  last section). The other harnesses still enforce tiering through their
  own config (§B in `flow.md`, §C `zcode.md`, §D `m365-copilot.md`), not
  through this hook.

## Auto-trigger recipe (default the routing policy without naming the skill)

What these layers default is the **routing policy**, not the ceremony. A
plainly one-context, non-risky task still runs inline without the skill body
loaded, and smartplan gets invoked when a fan-out signal holds. Three layers,
weakest to strongest. Stack them:

1. **Description matching**: smartplan's description opens with "Use
   proactively for any coding or implementation task", the documented lever
   for auto-delegation. The clause right after it does the regime split, so
   a match hands the task to the router rather than to a wave. Free, but
   probabilistic.
2. **Standing instruction**: CLAUDE.md / AGENTS.md carry the default-policy
   rule ("Route every coding or implementation task by regime yourself ...
   Invoke `smartplan` only when a fan-out signal holds"). Loaded every
   session on every harness that reads those files.
3. **SessionStart hook (mechanical)**: inject the rule as context at session
   start so it survives long sessions and compaction:

```json
{
  "hooks": {
    "SessionStart": [{
      "hooks": [{
        "type": "command",
        "command": "echo '{\"hookSpecificOutput\":{\"hookEventName\":\"SessionStart\",\"additionalContext\":\"Default policy: route coding tasks by regime yourself - plainly one-context, non-risky tasks run inline without the skill body; invoke smartplan only on a fan-out signal (beyond-context working set, two failed inline fixes on the same signature, verify-gated class, wall-clock batch). It routes by regime - one-context tasks run inline; fan-out is for beyond-context scale, rework-prone execution, verify-gated work, and wall-clock batches.\"}}'"
      }]
    }]
  }
}
```

Claude Code only. On other harnesses the standing-instruction layer is the
mechanical one (AGENTS.md-style standing files load unconditionally).

## Binding code conventions at write time (the inline-route gap)

The family's review machinery (`smartreview` and its `{{STANDARDS}}` doc)
runs over a *finished* changelist, and briefs bind executors on the fan-out
route. Neither reaches the **inline** route, which the default policy makes the
common case for a single-file edit. At the moment `Write`/`Edit` fires
there, the skill bodies aren't loaded and the reference PreToolUse hook only
matches `Task|Agent|Workflow`, so it never sees a code write at all. Since
v4.103.0 the gap is narrower for *correctness* and unchanged for
*conventions*: smartreview now
hunts breaking defects at the merge gate, so an inline-route bug has one more
place to get caught before it ships. A convention violation still has none. Honest scope: that
leaves exactly two surfaces in context, the standing file and any SessionStart
injection, and both are prompts rather than gates. Neither can *guarantee*
conformance. They make the doc present at the moment code is written, which is
the difference between conforming code and a review that finds the drift later.

Stack the same three layers, pointed at the conventions doc rather than the
routing doctrine. Epic ships the same mechanism for UE conventions in its own
Claude Code plugin, so the pattern is not novel.

1. **Standing file**: one line in the project's CLAUDE.md / AGENTS.md naming
   the doc and requiring it be read before the first edit to a source file.
2. **SessionStart injection**: the block above, with the text swapped for:
   `Conventions: code written in this project conforms to <abs path>. Read it
   before the first source edit, inline route included. A violation of a
   declared rule is a defect, not a style note.` Keep it under ~300B. It bills
   into every session.
3. **Brief + verify**: on fan-out, `brief.md`'s CONVENTIONS block pins the doc
   path and rule IDs, and `check.md` step 5 FAILs a violation of a declared
   rule. This layer *is* mechanical, and it is why fan-out conformance is
   stronger than inline conformance.

Install it in the project whose code is being written, not in the skills repo:
the standards doc travels with the codebase it governs.

## Cross-harness note: Copilot CLI runs this hook too

This page is written for §A (Claude Code). Copilot CLI loads the same hook
anyway. It reads `.claude/settings.json` and `.claude/settings.local.json` as
repo hook sources (CLI 1.0.12) and runs every hook entry from every source.
Per docs.github.com's hooks reference and the CLI changelog, read
2026-09-22:

- **It fires on every Copilot subagent dispatch.** A PascalCase
  `PreToolUse` entry gets Claude matcher semantics. Copilot maps its `task`
  tool to `Agent` and accepts a literal `Task`. So `Task|Agent|Workflow`
  matches. The payload's `tool_name` reads `Agent`.
- **Most branches go quiet there.** Copilot's `tool_input` carries the
  task tool's own arguments: `agent_type` rather than `subagent_type`. A
  logged 1.0.70 call also carried `name`, `mode` and `model`. The fork and
  verifier-seat branches read `subagent_type` and never match. GPT
  and Gemini slugs match neither tier family. That leaves the
  missing-model note and the cost-ceiling note, plus the Opus note when a
  dispatch passes a `claude-opus-*` slug (code-read, unprobed).
- **It fails closed.** A crash or any non-zero exit from a command
  `preToolUse` hook denies the tool call ("Denied by preToolUse hook (hook
  errored)"). Timeouts fail open.
- **Windows parses the command with PowerShell.** `command` is an alias
  for Copilot's `bash` and `powershell` fields (CLI 1.0.2), picked by OS.
  The docs' Windows examples need PowerShell 7.0 or later. Copilot falls
  back to Windows PowerShell for its shell tool when pwsh is missing (CLI
  1.0.45). The docs don't say whether hooks share that fallback.
  Unqualified `${CLAUDE_PROJECT_DIR}` reads a PowerShell variable there.
  Only `${Env:NAME}` reads the environment, which isn't portable since the
  same string runs under bash on Linux and macOS.
- **`CLAUDE_PROJECT_DIR` is documented for plugin hooks only** (CLI
  1.0.12). Nothing documents it for a hook loaded from
  `.claude/settings.json`. Open issue github/copilot-cli#4001 (Windows, CLI
  1.0.67) reports it missing there, along with the deny that follows.
- **Repo hooks need a trusted folder.** They load only after folder trust
  is confirmed. In prompt mode (`-p`) they load only when the folder is
  already trusted, `COPILOT_ALLOW_ALL` is set, or
  `GITHUB_COPILOT_PROMPT_MODE_REPO_HOOKS=true`.
- **The cloud agent doesn't load `settings.json`.** Only local CLI sessions
  run this hook.

A bare `bash "${CLAUDE_PROJECT_DIR}/..."` command hits three of those at
once on Windows. PowerShell expands the path to
`/.claude/hooks/require-tiered-dispatch.sh`. Bash exits 127 on the missing
file. PowerShell reports that as exit 1. Copilot turns it into a deny.
This repo's own copy of that command denied a Copilot `task` dispatch from
the repo root on 2026-07-12 (CLI 1.0.70, prompt mode). The `bash -c`
wrapper in "Reference instance" above is the repair.

`disableAllHooks: true` in `.github/copilot/settings.json` is the blunt
switch. It skips every hook from every source, user-level hooks included.
Only policy hooks survive it. Fixing the command string is the narrower
repair.

Copilot also has its own native `preToolUse` event (JSON under
`.github/hooks/` or `~/.copilot/hooks/`, per `references/copilot.md`).
This repo ships no native port, since the Claude-format entry above
already reaches Copilot.
