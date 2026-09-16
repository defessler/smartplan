# smartvoice — AI tells, researched (words + constructions)

The depth layer behind [`SKILL.md`](../SKILL.md) § *Avoiding the generic AI voice*. The body names the register and the headline clusters; this file carries the per-term carve-outs, the replacements, and the **structural** tells that no word list can catch. Load it on any slop pass over real prose.

**This file is subordinate.** A resolved Voice Profile outranks it, exactly as it outranks the body's list (the resolved profile's § *In-voice, never flag* says so directly). Where a profile deliberately uses something here, the profile wins and the usage is not a tell. See § *Not tells* below before "fixing" anything.

**Register, not a blacklist.** No term here is banned by spelling. Every row is scoped by sense or by rate, because the same word is a tell in one clause and the correct technical term in the next. A pass that swaps words without reading the sentence makes prose worse, not more human.

**Evidence is dated and drifts.** Measured rows come from post-2022 corpus work: Kobak et al.'s excess-vocabulary study over ~15M PubMed abstracts (*Science Advances* 2025, arXiv:2406.07016), Liang et al. on LLM-shifted vocabulary in conference peer reviews (arXiv:2403.07183) and on LLM-modified text across ~950k arXiv, bioRxiv, and Nature papers (arXiv:2404.01268), Reinhart et al.'s genre-matched human-vs-LLM parallel corpus (*PNAS* 122(8)), and Yakura et al. on the same words rising in unscripted podcast speech (arXiv:2409.01754). Practitioner rows come from detection guides and editorial practice, including Wikipedia's *Signs of AI writing* catalog. The word cluster moves by model generation: the 2023–24 wave ("delve", "tapestry", "meticulous") is fading in generator output while staying burned in reader recognition, so a fading word is still worth cutting when its avoidance cost is zero. Surveyed 2026-07-22. The four constructions added 2026-09-15 (change narration, arguing with no one, borrowed authority, and a restated heading) and the use-mention entry under *Not tells* come from blader/humanizer v3.0.0 (MIT), which realigned its patterns to that same Wikipedia catalog on 2026-09-06. Each was checked against this file and the resolved profile before landing, and each carries the carve-out that check turned up.

## Contents

- How to read the verdicts
- Density beats presence
- Scope by sense
- Replace on sight
- Constructions
- Displacement
- What's measured, and what's folklore (re-swept 2026-07-26)
- Not tells
- Self-check

## How to read the verdicts

- **Avoid** - no technical sense worth keeping in engineering prose. Replace or delete on sight.
- **Scope** - the literal sense is correct and unlimited; only the metaphor is the tell. Most rows are this.
- **Cap** - the word is fine and the *rate* is the tell. Once per document unless the row says otherwise.

## Density beats presence

The single most reliable signal in a finished document is not which words appear but how often one reaches for the same move. A term used once reads as a choice. The same abstract noun five times, or the same paragraph rhythm fourteen times, reads generated even when every instance is defensible in isolation.

Check rate, not membership: pick the three abstractions the document leans on and count them. If any exceeds roughly one per thousand words, the document has a tic, whatever the word is. This is why the resolved profile protects a *lone* impressive word while the body still calls the register a problem.

## Scope by sense

The literal column is correct usage and takes no penalty. Flag only the metaphorical sense.

**Rows that ask for a number:** if you don't have it, cut the claim instead. Never manufacture a measurement, a delta, or a before-and-after count to satisfy a row, because an invented figure is worse than the word it replaced. A number you do have needs its baseline. "40% faster" says nothing until it names what it beat, and on which workload.

| Term | Verdict | Keep untouched (literal) | Write instead |
|---|---|---|---|
| `underscore` (verb) | Avoid the verb | the `_` character: snake_case, leading-underscore identifiers, Python/Rust `_` | shows, confirms, means, is why |
| `highlight` (verb) | Scope | syntax highlighting, highlighted rows, "the profiler highlights the hot path", release highlights | shows, means, points to |
| `realm` | Scope | auth realm (Kerberos/AD/HTTP), MMO server realm | in X (delete "the realm of"), area, side |
| `landscape` | Scope | Unreal `ALandscape` and Landscape mode, loss/fitness landscape | the field, the options, what's available |
| `seamless` | Scope | tileable textures, `SeamlessTravel` and other identifiers, seamless roaming | name the seam removed: "no rebuild", "no loading screen" |
| `align with` | Scope | `alignas`/`alignof`, cache-line and SIMD alignment, axis-aligned bounds, text alignment, ML alignment | matches, follows, is consistent with |
| `navigate` | Scope | a route, tree, menu, graph, filesystem, NavMesh; `useNavigate`, `UNavigationSystemV1` | name the constraint instead of gesturing at difficulty |
| `potential` | Scope | hazard position: potential deadlock, potential null deref; physics senses | the measured number, or "not measured yet" |
| `surface` | Scope | established compounds only: API surface, attack surface; every literal rendering and geometry sense | don't invent new ones ("the failure surface" → "the ways it fails") |
| `shape` | Not a tell (see § Not tells) | API shape, response shape, tensor shape, memory layout, and every other established use | keep the word; rewrite only where "the shape of X" stands in for a name X already has |
| `streamline` | Avoid the verb | fluid-dynamics `streamline(s)`, aerodynamic "streamlined" | name what was deleted, with the before/after count |
| `enhance` | Avoid the bare verb | fixed compounds: the `enhancement` label, image/contrast/audio enhancement, enhanced for loop | improve, speed up, extend, sharpen |
| `transformative` | Scope | "transformative use" in copyright/fair-use writing (term of art) | state the measured delta |
| `interplay` | Cap at one | between two *named* mechanisms, where the interaction is the subject | interaction between X and Y, how X and Y affect each other |
| `notably` | Scope | mid-sentence restrictive use ("backends, notably Vulkan") | delete sentence-initial "Notably," outright |
| `particularly` | Scope | narrowing a claim ("particularly on ARM64") | delete the booster sense; give the reason instead |
| `boasts` | Scope | a person or vendor, when you intend the skepticism | has, ships with, supports, includes |

## Replace on sight

No literal technical sense worth preserving. The body already names most of these; the value here is the replacement and the reason.

| Term | Write instead |
|---|---|
| `delve` (all forms) | dig into, walk through, look at, or drop the framing verb entirely |
| `tapestry` (metaphor) | delete it and name the things: "the render, physics, and audio paths" |
| `meticulous` | delete and state the specific: "covers null, empty, and overflow" |
| `intricate` / `intricacies` | complex, then say *why*; "the intricacies of X" → "how X works" |
| `multifaceted` | enumerate the facets; if you can't list them the sentence was empty |
| `crucial` / `pivotal` | name the failure: "without the barrier the worker reads a torn frame" |
| `leverage` (verb) | use, build on, with, reuse |
| `showcase` (verb) | demonstrates, shows, illustrates (the noun "Showcase page" is fine) |
| `foster` | makes it easier to, helps, leads to |
| `garnered` | got, drew, received, or name the actor |
| `commendable` / `invaluable` / `noteworthy` | delete the praise; state the thing that earned it |
| `groundbreaking` / `innovative` / `revolutionize` | the measured result, or a plain priority claim ("the first pass that…") |
| `avenue` / `avenues` | options, approaches, next steps |
| `surpassing` (participle) | beats, exceeds, outperforms, with a number |
| `advancements` | advances, improvements, or name the change |
| `exhibited` / `exhibits` | showed, had, was |
| `valuable insights` | the finding itself ("Insights" as a product name is fine) |
| `additionally` (sentence-initial) | Also, or delete it; don't swap in "Furthermore" |
| `nuanced` | name the distinction it is hedging, or cut |

## Constructions

Stronger signal than any word, and the half a vocabulary sweep always misses. These are what make a de-slopped document still read generated.

- **Present-participle closers.** ", underscoring the importance of X", ", highlighting the value of Y", ", demonstrating Z". Delete any closer whose only job is to comment on its own sentence's significance, or whose implied subject is the whole preceding clause rather than a named noun. Keep closers stating a real consequence with a recoverable subject. **Carve-out:** ", ensuring X" is protected by the resolved profile's § *In-voice, never flag* and is exempt as a word; only the decorative *structure* is in scope.
- **The reveal colon.** "clause: lowercase payoff", where the colon fronts a full explanatory clause rather than a list or an identifier. This is the em dash's job wearing a different hat, and it clusters badly once a document bans dashes. Roughly one per ten sentences is where it starts reading mechanical. **Label colons are not this tell:** a callout label (`IMPORTANT:`, `Note:`), a `Step N:` heading, an `N. <Label>: <explanation>` sub-item, and an introducing label line (`Example asset:`) are structure a profile may mandate, and the resolved profile's § *Portable formatting habits* does exactly that. Only a running-prose colon fronting a full explanatory clause counts. Split those into two sentences; a colon introducing a genuine list or a code identifier stays.
- **The fixed consequence closer.** Every rationale paragraph landing its conclusion on a sentence-initial "So". One or two per document is natural speech, and the profiles bless "so" as a plain connector; the tell is when it becomes the *slot* that closes twelve of fourteen paragraphs. Vary or delete: the claim usually stands alone.
- **The contrastive tail.** ", not Y" / ", never Y" / "rather than Y" appended to state what a thing isn't. Genuinely useful when correcting a misconception the reader actually arrives with. A tell when every paragraph ends on one. Keep a few, state the rest positively.
- **Graded-abstraction subjects.** "The real mechanics are…", "The genuine gap is…", "The honest answer is…", "The dangerous half is…". An abstract noun plus an evaluative adjective, graded before it is explained. Lead with the concrete subject instead. Watch "real", "genuine", "honest", "precise", and "half" specifically; they cluster.
- **Demonstrative subjects.** "That's exactly how X works", "That's the reasoning behind Y", where the demonstrative points back at a whole paragraph rather than a nameable referent. Name the referent.
- **Template rhythm.** A per-section template is a legitimate reference-doc convention and profiles may mandate one. The tell is when the *paragraph shape inside every slot* never varies: mechanism, then consequence marker, then contrastive tail, then a short punch sentence. Keep the slots, vary the filling, and never let two sections open with a byte-identical string.
- **Manner-adverb failure vocabulary.** "silently", "loudly", "cleanly", "quietly" describing how code fails. One or two are precise ("a silent out-of-bounds write" contrasts with an assert). A dozen is a register. Say what observably happens: "matches nothing and still exits 0" beats "quietly dies".
- **Anthropomorphized tooling.** "the engine treats this as a hard line, not a wish", "Epic agrees", "the compiler wants". Attribute to the artifact and cite it. A written standard really can mandate something; a codebase cannot agree, want, or eat anything. **Carve-out:** the soft epistemic hedges "tries to" and "attempts to" describing best-effort system behavior are protected by the resolved profile's § *In-voice, never flag* and by § *Not tells* below. The tell is attributing belief, preference, or endorsement, not describing what a system attempts.
- **Recycled boilerplate in fresh dress.** The same claim restated a few hundred words later with different metaphors, or four sections ending on structurally identical sentences with the nouns swapped. Say it once, then cross-reference.
- **Change narration.** "was added to replace the old loop", "now uses X instead of Y", "no longer needs a restart", on a reference page or in a code comment, describing what the current design replaced when the reader needs what it does. History belongs in changelogs, release notes, and migration guides. **Carve-out:** the resolved profile's § *Hedging*'s admit-iteration note stays, because telling a reader an example asset is stale is a fact about the page they're reading now.
- **Arguing with no one.** "To be clear", "This isn't about X", "Don't get me wrong", "A tempting approach would be…, but", answering an objection or rejecting an option nobody raised. Cut the defense and state the claim. Keep an alternative a reader would actually weigh. A design spec's rejected-alternatives section is exactly that. It stays.
- **Borrowed authority.** "Experts recommend", "studies show", "industry best practice is", standing in for a source. Name the source and what it says, or let the claim stand on its own evidence. Never invent the citation to fill the gap. A missing citation alone isn't a tell, since most technical prose is unsourced.
- **A heading restated as its first sentence.** A `## Caching` heading followed by "Caching matters." before the real content starts. Delete the restatement. **Carve-out:** a profile's stock page opener (the resolved profile's "This page is meant as a quick reference on…") states the page's scope on purpose and stays.

## Displacement

Banning a device does not remove its job. Cut the em dash and its work migrates to colons, parentheses, and sentence fragments; cut the hollow transition and paragraphs start opening on "So". When a mechanical rule is satisfied but the page still reads generated, look for where the banned move went rather than re-running the same check. The rhythm is the tell, and rhythm is portable.

## What's measured, and what's folklore (re-swept 2026-07-26)

The rows above are not equally evidenced, and a skill that claims to detect
tells should say which ones science actually backs. A 2026-07-26 research
pass checked the literature per construct:

- **Measured, per model.** Em-dash rate is the best-evidenced single tell:
  one twelve-model study puts the heaviest emitter at 10.6 per 1,000 words.
  The load-bearing detail for us is that an explicit "no markdown"
  instruction cut it only to 9.1, a **14% reduction**. Instructing a model
  not to do it mostly does not work, which is why the resolved profile
  bans the character outright rather than asking nicely. `defaultvoice.md`
  only trims.
- **Measured, model-agnostic.** Lexical overuse (the "delve" cluster) and
  the slop-marker taxonomies. Real, but population-level, so don't attach
  them to a named model.
- **Folklore, with no measurement behind it.** The **rule-of-three
  cadence** and the **"not just X but Y" antithesis** have no published
  per-model or population measurement at all. The second is confirmed
  absent from the tracked categories of the main verbal-tic index. Both
  stay in the SKILL.md body list because they're real register problems,
  but cite them as editorial judgement, never as research.
- **Actively decoupled from what you might assume.** Measured prose tells
  do **not** predict which text gets accused of being AI-written. Writing
  to beat an accusation and writing well are different projects, and this
  file only pursues the second.
- **Domain-bound.** Detector studies key on dataset-specific cues, so any
  per-model tell ranking should be assumed not to transfer across domains.

One number worth keeping for calibration: EQ-Bench's human-written baseline
scores 6.90 slop per 1,000 words. Human prose is not slop-free, and a
target of zero is the wrong target.

## Not tells

Do not "fix" these. Each is either a house-voice choice that outranks any external list, or a word a generic guide flags wrongly.

- `shape` (noun) - **refuted as a tell.** It is correct and idiomatic (API shape, response shape, tensor shape). The real defect it gets blamed for is *vagueness*: "the shape of X" standing in for something that already has a concrete name. Fix the vagueness, keep the word. If anything deserves a cap it is the verb "shaping", and only in "plays a key role in shaping".
- `comprehensive`, `ensure` / `ensuring`, `utilize`, `robust`, `designed to`, `meant to` - protected verbatim **when a profile is resolved**, by its § *In-voice, never flag*, which outranks every generic list. Under [`defaultvoice.md`](voice-profiles/defaultvoice.md) or `{{VOICE_PROFILE}} = none` that profile never loads and these carry no protection: defaultvoice.md's own phrasing guidance flags `utilize`, and the rest fall back to the body's register rule.
- Title Case headings, stock formulaic openers, question sub-headings, FAQ entries - house structure, not tells.
- Soft hedges ("attempts to", "mostly", "at time of writing", "should be able to") - measured research finds machine text *under*-hedges next to human technical writing, so concrete hedges are part of what reads human. Only vague hedges ("may potentially") are tells.
- Team "we/our", second-person "you", warmth, and the `Term - description` separator - deliberate register and list machinery under the profiles that use them.
- Deliberate terminology repetition - reusing the exact term for one concept is the fix for synonym cycling, not a tic. Only *abstraction* repetition counts against the density rule.
- Mentions, not uses - a watched phrase inside a quotation, a title, a proper name, an error string, or a passage that discusses the phrase is being mentioned. This file is one long example of that.

## Self-check

- Counted the top three abstractions, and none exceeds about one per thousand words.
- No reveal colons where the second half is a full clause, and no more than a few per page.
- Rationale paragraphs don't all close the same way.
- Every metaphor row above is either literal in context or replaced.
- Nothing on the *Not tells* list got "corrected".
- Searched once more for what a rewrite most often leaves behind: a not-X-but-Y contrast, a one-line closer, a dash, a triad, a bold label.
- No reference page or code comment narrates what the current design replaced.
