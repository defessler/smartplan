# Terminology & Mechanics

Part of the [`smartvoice`](../SKILL.md) skill's keyed voice profile layer — not the generic `defaultvoice.md`, which is self-contained and loads neither this file nor the templates. Capitalization, abbreviations, prose mechanics, and spelling conventions for the author's voice. The voice pillars live in the profile doc. The generic anti-AI-slop layer lives in [`../SKILL.md`](../SKILL.md). [`document-templates.md`](./document-templates.md) has the optional scaffolds.

### Capitalization principle

Title-Case a noun when it **names a specific concept, system, or status**. Lowercase the same word when used **generically** in running prose. Apply consistently within a doc.

- Concept: "<Concept> Debugger", "<Concept> Component", "<Feature> Scene Component", the "<Concept>" feature or section.
- Generic: "a data layer", "a concept", "this component", "save the player's progress".

This applies to named statuses too: Title-Case a named status value (e.g. the setting is set to `Complete`), but lowercase a transient condition in flowing prose (e.g. "must be active for this to be evaluated").

`UI` follows the same principle: Title-Case it when it names a specific subsystem or feature (e.g. "the <Feature> UI"), and keep generic references plain ("the UI", "the UI flow", "in the UI").

When you reference a term from an upstream tool, follow that tool's own capitalization. Epic/Unreal proper terms keep their established casing as concepts: Data Layer, Data Asset, Smart Object, Actor, Blueprint, Component, Common UI, Slate, Data Validation, Map Error, UMG. (Lowercase them only in truly generic back-reference, e.g. "a data layer", "this component".)

### Speculative / out-of-scope nouns

When introducing a noun that isn't already established, default to **lowercase** unless it is a known Epic/Unreal proper term (Smart Object, Common UI, Data Validation, Map Error, Slate). Do not over-capitalize plausible-but-invented nouns (e.g., write "currency", "inventory", "an item reward", not "Currency"/"Inventory"/"Item"). Don't invent house vocabulary. Default to lowercase for a tag or similar generic noun.

### Approved abbreviations (never expanded)

`PIE`, `QTE` / `QTEs`, `UMG`, `GPS`, `GUID` / `GUIDs`, `UI`, `AR`, `SDF` / `SDFs`, `MVC`, `MVVM`. Pluralize by adding a lowercase `s` (QTEs, GUIDs, SDFs). Assume an Unreal-literate reader.

### Asset paths

- Use a neutral placeholder for the path, e.g., `<project-path>/<area>/<asset>`. The path illustrates the formatting convention only, never a real location.
- Place a path on its own line under an introducing sentence. Introduce an example asset with a short label line (`Example asset:`, `You can look here for ...:`, or `You should be able to find the asset here:`). Label a volatile path with the fixed string `Location at time of writing:`.

### Canonical spellings & normalizations

Fix obvious typos and standardize new docs on the canonical column without treating existing pages as errors. This table is the normalization reference. The pillars in the resolved profile teach each habit. This is where you check, when editing an existing page, whether a variant is canonical, common in the wild, a real error, or just a soft preference. The "Status" column marks which is which.

| Item | Canonical (new docs) | Other form seen | Status |
|---|---|---|---|
| "it is" contraction | `it's` | `Its` | `Its` is an error, so fix it. |
| possessive of "it" | `its` | `it's` | typo when misapplied, so fix it. |
| possessive nouns | `the player's progress` | `the players progress` | error, so fix it. |
| dashes in prose | reword with a comma, colon, parentheses, or a new sentence | em-dash, en-dash, or ` - ` / ` -- ` used as a sentence dash | error, so reword it. Compound-word hyphens, code identifiers, and the `Term - description` separator are fine. |
| comma-joined clauses | split into two sentences, or fold in a trailing dependent clause | two standalone clauses spliced with `, so` / `, but` / `, and` / `, or` (e.g., "It is a stretch goal, and it will need support") | error, so split it. List commas (`A, B, and C`) and trailing dependent clauses are fine. |
| `e.g.` | `e.g.,` (trailing comma) | bare `e.g.` | Soft preference, not an error. Prefer `e.g.,` for consistency. Bare `e.g.` is also fine. |
| `i.e.` (if needed) | `i.e.,` | `i.e.` | normalize to comma form. |
| small counts in prose | prefer spelled out: `two`, `three`, `four` | digits: `3 categories`, `the first 2 items`, `only ever be 1`, `or 2` | **Soft preference, not error.** Spelling out is the majority and preferred for readability, but small counts also appear as digits in running prose, so do not flag those as wrong. Always use digits for indices (`Index 0`), code values, timecodes (`0:00`/`3:32`), and playback speed (`1x`). |
| serial lists | Oxford comma (`A, B, and C`) | no serial comma | normalize to Oxford comma. |
| conjunction in prose | spelled-out `and` / `or` | `&` | reserve `&` for headings/proper page names. |
| UI label quoting | straight double quotes (`"Use Display Name"`) | backtick-open/apostrophe-close; space-padded bare words | normalize to double quotes. |
| inline page-title link | exact title, trailing period (e.g. `System: <System> .`) | paraphrase or generic "here" | normalize to exact title. |
| external-resource attribution | `<Title> -- <Author>` (double hyphen) for short personal-author credits; `<Title> - <description/org>` (single hyphen) for a descriptive gloss or organization credit | mixed | **Both are correct by use, not right-vs-wrong.** A personal-author credit (`-- <Author>`) uses the double hyphen. A descriptive note or organization credit (`- <Organization>`, `- Great way to get a better understanding...`) uses the single hyphen. |
| internal link-list heading | `Other Pages` for siblings; `Documentation` for a system's own child topics | mislabeling either | normalize. |

### Body vs heading case

- **Body prose:** sentence case (proper nouns stay capitalized mid-sentence).
- **Headings & TOC entries:** Title Case.
