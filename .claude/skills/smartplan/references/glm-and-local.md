# smartplan — GLM and local models behind a shim

*Load when your session model is a `glm-*` id or a local model name, or
when `ANTHROPIC_BASE_URL` points at `api.z.ai` or `localhost`. That covers
Claude Code through a z.ai or local-model launcher, and ZCode on GLM
(its levers are in `zcode.md`). Classes and prices are in
`model-classes.md`, which wins on any drift.*

## Read the real ladder first

A launcher remaps the tier aliases. `model: sonnet` means whatever the shim
maps it to, so read `ANTHROPIC_DEFAULT_OPUS_MODEL`, `_SONNET_`, `_HAIKU_`
and `_FABLE_` before you seat anything. Class each seat by the model it
resolves to, never by the alias name. `CLAUDE_CODE_SUBAGENT_MODEL=sonnet`
follows the same map.

**When every alias resolves to one model, the ladder has collapsed.**
Tiering is moot. Route by regime only. Work above that model's class gets
the brief written and a stronger backend offered. Unless the user switches,
this model does it and names the gap. That's the Cheap-seat rule in
`SKILL.md`.

## z.ai GLM (a z.ai shim, or ZCode)

- GLM-5.3 (AA 44.8, AA TB4 41.9%) and GLM-5.3-Flash (41.8, 32.8%) both
  measure Reasoning. Flash costs about a third of the plan credits (2.3
  against 6.9) and an eighth per AA index task ($0.25 against $2.01).
- **Flash is the default for every seat.** T42 measured it level with
  GLM-5.3 (semver 44 of 44 both, C++ recall 12 against 11 to 12) at about
  a tenth of the list cost, but slower. Use GLM-5.3 for a big plan, a
  fail-twice target or a Strong verify. It can't turn reasoning off.
- Both are one family, so a GLM verifier on GLM work is same-family. A
  risky merge wants a cross-family verifier from another backend, by ask.
- The plan answers 429 past about 2 to 4 concurrent agents. Cap a wave at
  three.

## Local models (llama.cpp or llama-swap behind a shim)

- **Zero per-token cost, but not free.** The window is the server's
  per-request context, not the model's native one. One slot (`-np 1`)
  serves subagents one at a time, so a wall-clock fan-out doesn't pay.
- **Class caps what you can trust.** AA measures full-precision weights, and a Q4
  quant scores at or below them (read 2026-09-23). Only Qwen3.8-27B (33.7),
  Qwen3.6-27B (21.4) and Qwen3.6-35B-A3B (18.2) measure Mechanical. The
  Qwen3-Coder rows, gpt-oss, Devstral, the VL and GLM-4.x rows and the R1
  distills are Unclassified. No local model reaches Implementer.
- **Pin one model per class.** Mechanical: Qwen3.8-27B for quality, or
  Qwen3.6-35B-A3B for speed. Implementer and Reasoning go to a cloud CLI
  where one is on offer: `claude -p --model sonnet` or `opus` on the
  subscription, or a z.ai shim on GLM-5.3-Flash or GLM-5.3. A 3B
  utility model may serve the haiku slot's titles and summaries, never
  a seat.
- A text-only seat fails on images. Route an image-bearing request to a
  vision row or a cloud model.

## Mixing local and Anthropic in one job

One Claude Code session reaches one endpoint. `ANTHROPIC_AUTH_TOKEN` and
`ANTHROPIC_API_KEY` outrank the subscription login, so a gateway that
routes tiers by model name bills API rates, not the plan (authentication
docs, read 2026-09-23). Mix by process instead, through Bash:

- **Cloud session, local leaf.** Hand a Mechanical leaf with a scripted
  check to a local headless run (`<local shim> -p "<brief>"`), then run
  the check yourself. Only its short report enters your context.
- **Local session, cloud leaf.** A leaf above Mechanical goes to
  `claude -p --model sonnet` or the z.ai shim, on the user's yes.
- A leaf's result is evidence, never a verdict. The verify floor holds.
