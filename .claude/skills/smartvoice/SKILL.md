---
name: smartvoice
description: "Use when a technical document (how-to guide, design spec, reference page, README, inline doc prose) should read in the resolved voice, or when asked to make writing sound less like AI, less generic, or more human. Anti-AI-slop pass + per-user Voice Profile, auto-resolved per OS username (references/voice-profiles/{username}.md → defaultvoice.md → neither = the skill stands down, no voice pass). Set {{VOICE_PROFILE}} to override, or none for the slop-strip alone."
---

# smartvoice

Makes a technical document read like a person wrote it, in two layers: a universal strip of the generic AI voice (tells below), plus an optional personal **Voice Profile** — a per-user doc capturing how one author writes (vocabulary, grammar, tone, hedging, stance). Profiles resolve automatically per user (below); with none resolved, the skill stands down entirely. This is about voice, not layout (see *Structure is malleable*).

## Voice Profile — resolved per user

| Token | Meaning | Default |
|-------|---------|---------|
| `{{VOICE_PROFILE}}` | optional override: a path to a profile doc anywhere in the repo, or `none` | unset — auto-resolve by username |

Resolves automatically, first match wins:

1. **`{{VOICE_PROFILE}}` set** → honor it. A path loads that doc; `none` restricts to the generic layer below. A set path that fails to resolve is a config error — say so, then proceed as `none`. Never guess a voice.
2. **`references/voice-profiles/<username>.md`** — keyed by OS username: `whoami`, strip any `domain\` or path prefix, lowercase (`CORP\Doug` → `doug.md`).
3. **[`defaultvoice.md`](references/voice-profiles/defaultvoice.md)** — house fallback when no keyed profile exists (shipped: a generic register grounded in AI-writing-tells research).
4. **Neither file exists** → **smartvoice is inactive.** Say one line ("no voice profile resolved — smartvoice inactive") and change nothing — no personal register, no slop-strip. Delete/rename `defaultvoice.md` as the whole-skill off switch. (Unlike `none`, an opt-in slop-strip.)

A loaded profile's register applies atop the generic layer; its deliberate choices aren't tells.

To house a new voice, copy [`defaultvoice.md`](references/voice-profiles/defaultvoice.md)'s shape (pillars, formatting habits, phrasing bank, worked example, self-check), fill it from the author's real writing, and name it `<username>.md` to auto-resolve. (Skill machinery: a profile's own formatting rules, like its table-scoping habit, govern documents you write, not this file.)

## Avoiding the generic AI voice

Left alone you default to a machine register — inflated words, symmetrical sentences, relentless enthusiasm, empty hedging. This layer strips it under every profile, and is the whole job under `{{VOICE_PROFILE}} = none`.

- **Inflated diction.** Register, not any single word: plain over dressed-up ("use" not "leverage"; "important" not "crucial"/"essential"; drop "powerful", "seamless", "elevate", "landscape", "game-changer"). Cut an adjective the sentence survives without — one strong word is fine, a paragraph isn't. The measured word cluster drifts by model generation (fading: "delve", "tapestry", "testament", "underscore", "showcase", "pivotal", "meticulous", "intricate", "realm", "myriad"; rising: "emphasizing", "highlighting") — symptoms of the register, not a blacklist; a loaded profile's own vocabulary outranks this list.
- **Dash-heavy punctuation.** Trim stacked em dashes — the top tell, especially "clause, dash, punchline" rhythm — to commas, colons, parens, or a new sentence. A profile may ban them outright. The default only trims.
- **The "not just X, it's Y" tic** (and "not only… but also"). State the thing plainly — a real factual contrast is fine, empty inflation isn't. Includes the standalone two-sentence form ("It's not X. It's Y.") and the fragment triad ("No X. No Y. Just Z.") — same carve-out: a real contrast split into sentences stays; the empty reframe goes.
- **Fancy linking verbs.** "serves as", "stands as", "functions as", "acts as", "represents" dressing up a plain "is" — write "is" (or "has") unless the verb carries real meaning (a proxy genuinely acts as a fallback; an enum value represents a state).
- **Synonym cycling.** Rotating names for one thing (the "controller", then the orchestrator, then the manager) to dodge repetition — reuse the exact term every time; the reader must never wonder whether two names are two things. (A profile's quoted nickname repeats exactly after its debut, and a lowercase generic back-reference shortens the same noun — neither is cycling.)
- **Rule-of-three padding.** Cut decorative triads ("fast, flexible, and powerful") for the one true thing; a real list of three is fine.
- **Hollow transitions and narrating the writing.** Drop "It's worth noting", "Moreover", "Furthermore", "When it comes to" and kin — plain connectors ("so", "but") carry the load unaided.
- **Tour-guide narration.** "In this guide, we'll explore…", "Let's dive in", "Let's take a closer look" — a document isn't a guided tour; say what the page covers and get on. (A profile's team-"we" for shared work isn't this tell — the narrator-and-reader "we" is.)
- **Chat residue.** No "I hope this helps", "Certainly!", "Let me know if…", "Would you like me to…", or "as of my last update" cutoff talk — the conversation never leaks onto the page. (A profile's dated hedges like "at time of writing" are facts, not this tell.)
- **Fake candor and self-answered questions.** "Here's the thing:", "Let's be honest", "The answer? …", "So why does this matter? It matters because…", and aphoristic pull-quote kickers closing a paragraph — say the point straight, once. (Question-phrased headings and FAQ "Q:" entries are structure, not this tell.)
- **Summary closers.** No "In summary", "In conclusion", "Overall" restating a section — stop when the point lands.
- **Manufactured enthusiasm.** No "powerful feature", "Great question", or hype punctuation — register stays even, not a product launch.
- **Over-explaining.** Don't define terms the audience knows, expand every abbreviation, or restate an example — write for the actual reader.
- **Audience hedging.** Skip "whether you're a beginner or a seasoned pro" — pick the reader, talk straight to them.
- **Throat-clearing openers.** No participial lead-ins ("Leveraging X, you can…") — start with the bare verb or subject.
- **Vague scale claims.** "plays a key role", "a wide range of", "in today's fast-paced world" say nothing — name the actual role, range, or condition.
- **Decorative formatting.** No emoji, no mid-sentence bolding for emphasis, no bullet-splitting prose just because you can, and no walls of "**Label:** sentence" bullets standing in for structure — prose, a real heading, or a plain-label list (a profile's definition-list device, where one exists, is the in-voice form).

- **Structural tics, and density over presence.** A page can pass every word check and still read generated: reveal-colons ("clause: lowercase payoff") doing the banned dash's job, every rationale paragraph closing on "So", a ", not Y" tail on every claim, graded-abstraction subjects ("The real problem is…"), one paragraph rhythm repeated per section. Two rules the word list can't carry — **ban a device and its job migrates** (cut dashes, watch colons and fragments absorb the rhythm), and **rate is the tell, not membership** (one abstraction reached for five times is a tic whatever the word; a lone impressive word isn't).

Depth on demand — per-term carve-outs (the literal sense that always stays: `underscore` the character, an auth `realm`, `ALandscape`, tileable `seamless`), replacements, the structural tells in full, and the *not tells* protections against over-correction: **load [`ai-tells.md`](references/ai-tells.md)** for any slop pass over real prose.

Two cautions: a concrete hedge ("mostly", "at time of writing") carries information and stays — only vague hedges ("may potentially") are tells. Warmth isn't a tell either — a profile's deliberate register choice stays.

Same idea, both ways — AI default: "Leveraging this powerful system, you can seamlessly delve into a wide range of robust configuration options that play a crucial role in your workflow." Stripped: "This system lets you configure how the flow behaves."

## Structure is malleable

No fixed document shape, under any profile. Modifying or extending an existing document: infer its template, mirror structure/headings/order, and write the voice in — never reshape it to a scaffold.

A profile may ship optional scaffolds for **brand-new documents only** — the keyed profile's live in [`document-templates.md`](references/document-templates.md) (deep-reference, tutorial, setup/config, spec, landing shapes with per-section opening lines). Starting points only, never retrofit onto an existing page; adapt freely. `defaultvoice.md` ships none, and under `{{VOICE_PROFILE}} = none` there are none either — shape new documents however content needs.

## Quick self-check

Before shipping a page: scan for the tells above, then run the active profile's own checklist (each ships one at file's end). Under `none` this list is the whole check.

- No AI tells from the list above.
- No structural tic: counted the top abstractions (none reached for repeatedly), and the rationale paragraphs don't all close the same way.
- No dash doing work a comma, colon, parens, or a new sentence would do better.
- Hedges are concrete ("mostly"), not vague ("may potentially").
- Nothing defined or expanded that the audience already knows.
- One exact name per concept, and "is" doing the linking (no "serves as" dressing).
- Nothing from the chat on the page — no "I hope this helps", no offers to continue.

Two of these are character checks, not reading: where a profile bans dashes or prose semicolons (a resolved profile bans both), `grep -n '[—–;]' <file>` is the tier-1 executable oracle — one pass, then clear each hit by hand (a `;` inside inline code or a fence is exempt).

## References

Everything swappable lives in `references/` (part of this skill): load the profile doc whenever you apply a voice and `ai-tells.md` on any slop pass; the other two only when needed.

- [`voice-profiles/`](references/voice-profiles/) — one doc per voice, `<username>.md` auto-resolving (shipped: [`defaultvoice.md`](references/voice-profiles/defaultvoice.md) the generic fallback). It shows the shape (pillars, formatting habits, phrasing, worked example, self-check) — copy it to house another voice.
- [`ai-tells.md`](references/ai-tells.md) — the researched tell layer: per-term carve-outs and replacements, the structural tics (reveal colon, fixed consequence closer, contrastive tail, template rhythm), the density rule, and the *not tells* list. Universal, not profile-scoped — load it on any slop pass, including under `{{VOICE_PROFILE}} = none`.
- [`document-templates.md`](references/document-templates.md) — OPTIONAL scaffolds for brand-new documents (deep-reference, tutorial, setup/config, spec, landing). Part of the keyed profile (not `defaultvoice.md`); prefer an existing document's own template; adapt freely.
- [`terminology.md`](references/terminology.md) — capitalization, approved abbreviations, prose mechanics, canonical-spellings table. Part of the keyed profile (not `defaultvoice.md`); the lookup when editing an existing page.

## Family fit and tiering

`smartvoice` is an **optional** companion seat (like `smartreview`/`smartwiki`): the family works without it, and with no keyed profile or `defaultvoice.md` it stands down by itself (step 4). `{{VOICE_PROFILE}} = none` keeps it active but runs the slop-strip alone. It sits outside the tiering loop — a reusable ruleset, not a model-role — and is the house-voice authority other seats defer to when a profile is set: `smartwiki` rendering into a wiki whose voice guide is this skill targets the active profile. Under a strict profile that means dashes get reworded and a one-attribute-per-entry table becomes `Term - description` bullets, while a genuinely two-axis comparison table stays a table; the generic default allows tables freely.

Tiering (see `smartroute`): voice work is one-context, so it runs **inline** by default, in the session already writing. The tiers below apply once you've chosen to fan out. A fresh in-voice page is judgment-heavy (subtle tells) and fits **Mid**. **Cheap** lands it only with a strong exemplar plus a `smartcheck` pass reading for the tells and the profile's mechanics — the Quick self-check plus the profile's checklist is what that verifier runs. A slop-strip-only pass (`none`) is more mechanical and can route a tier lower behind the same check.

## Changelog / edge-case log

Moved to [the repo's commit log](https://github.com/defessler/smartplan/commits/main) to keep this body lean and out of the shipped plugin.
