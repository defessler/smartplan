# smartreview — C++ gamedev review standards (the shipped default doc)

The standards doc `{{STANDARDS}}` points at until a project re-points it —
see `../SKILL.md` for the driver: the three-category ranking, the protocol,
PASS/FAIL/N-A discipline, hard rules, and the report template. This is now the **single combined
document**: the A–M checklist, the tag legend, the **Engine** selector, the
C++ fill-once tokens, the custom-engine **[C]** detail (section J), and the
per-rule Epic-standard provenance all live here — no satellite reference
files.

This is **C++ gamedev, engine-profiled**. Most of the checklist is general
C++ that applies to any game project, vanilla or a bespoke engine, and the
engine-specific rows only switch on once a project says which engine it is.
Unspecified stays unspecified: **Engine** ships at `vanilla`, the narrowest
profile, and an unfilled knob resolves to N/A rather than to a guessed
value. Epic's own answer is recorded per rule in § Provenance &
Epic-standard validation, so adopting the Epic standard is something a
project opts into, never something it inherits by saying nothing. Rows
tagged **[G]** are general C++ gamedev and apply in every profile. Rows
tagged **[U]** are Unreal- or Epic-standard, active only when
`Engine = unreal` (changing them breaks builds or violates the engine
standard). Rows tagged **[C]** are custom-engine architecture conventions,
active only when `Engine = custom` — full checklist in § J below. Rows
tagged **[P]** are project choices where the engine is silent — adapt those
freely, in any profile. Three of them (indentation, line length,
local-variable case) live in the driver's profile and ship unfilled.

## Project Profile

<!-- ENGINE-PROFILE-HOME -->
This section is the **canonical Engine-Profile home** — other files point at
`smartreview/references/cpp-review-standards.md § Project Profile` instead
of restating it. Fill it once — Engine included — and every rule below
resolves to your engine and your house style.

| Token | Meaning | This project | Epic / stock answer |
|-------|---------|--------------|---------------------|
| **Engine** | `vanilla`, `custom`, or `unreal` — gates which tagged rows below are active | `vanilla` *(shipped default)* | Epic's answer is `unreal`. Set it explicitly for an Unreal project — `vanilla` is what the rest of the family assumes when nobody says otherwise (`cpp-gamedev-check.md`, `routing.md`, `docs/cpp-gamedev-contracts.md`) |
| `{{COMPANY}}` | Copyright holder text on line 1 | _fill in_ | `Epic Games, Inc. All Rights Reserved.` |
| `{{PREFIX}}` | Project type-name prefix inserted after the Unreal letter (`U`/`A`/`F`/`E`) — `unreal` only | _fill in, or blank_ | none — stock Unreal prefixes |
| `{{MODULE}}` | Module root(s) that root include paths (e.g. `Game`, `GameEditor`) — `unreal` only | _fill in_ | — |
| `{{NAMESPACE}}` | Namespace root for project code (non-`UObject` code, in `unreal`) | _fill in_ | `UE::<Feature>` (Epic guidance; `unreal` only — pick any root in other profiles) |
| `{{LOG}}` | Log-category name root (e.g. `LogGame`) — `unreal` only | _fill in_ | — |
| **Declaration order** | The role-category sequence inside a type that M2 checks against | _fill in, or copy in M2's answer_ | Epic is silent — it prescribes no member order |

**Engine** is the only token in this table with a shipped value, and it
points at the narrowest profile on purpose: under `vanilla` only [G] and
[P] rows are active, so a project that never sets it can't have Unreal
rules fired at code that isn't Unreal. Every other token (`{{COMPANY}}`,
`{{PREFIX}}`, `{{MODULE}}`, `{{NAMESPACE}}`, `{{LOG}}`) is project
identity, not house style, so it stays **N/A until filled in** rather than
guessing.

Three universal knobs — **Indentation**, **Max line length**,
**Local-variable case** — live in the driver's profile
(`../SKILL.md § Project Profile — set once`) and ship **unfilled**. Rules
A4, A5, and D1 read them from there and stay N/A until somebody fills
them. The driver carries Epic's values for all three as a named example to
copy in, and § Provenance & Epic-standard validation records Epic's
position on each.

### Rule tags

| Tag | Meaning | Active when |
|---|---|---|
| **[G]** | General C++ gamedev — the bulk of the checklist | Always, every profile |
| **[U]** | Unreal- or Epic-standard | `Engine = unreal` |
| **[C]** | Custom-engine architecture convention (§ J below) | `Engine = custom` |
| **[P]** | Project choice — engine is silent, house style decides | Any profile |

**How the profiles compose:**
- `vanilla` → **[G]** + **[P]** rows. **[U]** and **[C]** rows are N/A.
- `custom` → **[G]** + **[C]** + **[P]** rows. **[U]** rows are N/A.
- `unreal` → **[G]** + **[U]** + **[P]** rows. **[C]** rows are N/A.

These tags gate **applicability** only: whether a row runs at all. Severity
is a second, independent axis — how loudly a FAIL on that row is reported.
A **[P]** row can be BREAKING and a **[U]** row can be CONVENTION. The two
never substitute for each other.

## Severity map

Every checklist row below carries exactly one severity, and the driver
reports findings in this order. Never let a CONVENTION finding push a
BREAKING one down the page.

**BREAKING** is a concrete runtime failure: crash, UB, memory or save
corruption, data loss, hang, deadlock, desync, or an ODR/link failure.

Findings are **categorized**, not re-defined, using
`smartplan/references/cpp-gamedev-check.md`'s six categories. That file is
the authority and the only place to edit them. It is **not always
installed beside this one** — `install-project.ps1` ships the four
companions without the core pair, and `chat-export.py` bundles this skill
alone — so the six are glossed here well enough to hunt standalone. Read
that file when it's present.

| Category | One-line gloss | Yields |
|---|---|---|
| **Ownership & lifetime** | who frees it, and can anything still reach it after | BREAKING |
| **Undefined behavior** | the standard or the engine gives no meaning to this | BREAKING |
| **Threading model** | two things touch it, and nothing orders them | BREAKING |
| **Determinism & serialization** | it won't reload, replay, or agree across machines | BREAKING |
| **Build & header hygiene** | ODR and link failures are BREAKING, plain IWYU nits are not | either |
| **Performance hot-path** | costs frame time without failing | PRACTICE |

Two of the six therefore produce **no** BREAKING row in this doc. Perf
costs frame time rather than failing, so J1 is PRACTICE, and header hygiene
only breaks when it reaches ODR or the linker, which is why A6 is BREAKING
and A3 is PRACTICE. Section J's **Nearest correctness category** column is
the worked example of the mapping. Name the category on every BREAKING finding so a
smartcheck report and this one collate on `category · file:line` instead
of double-reporting the same defect.

> A6, C4, C8, D6, F1, G1, G3, G4, J2, J3, J4, J5, L1

**PRACTICE** is a named mechanism that degrades behavior, performance,
build health, or asset health without a runtime failure: API misuse,
missing guards, perf traps, dead registration code, silent functional
holes.

> A2, A3, A9, A10, B7, C6, C9, E5, E6, F3, I1, I2, I3, J1, J6, K3, K4, K6, L2, L3, L4

**CONVENTION is the default.** Every row not named above is CONVENTION:
style, naming, formatting, comment content, editor cosmetics.

Four rules place a row, in order. They're what keeps the BREAKING band
honest, and honesty is the band's only value.

1. **Compile-caught is never BREAKING.** If the next build rejects it, no
   reviewer ever sees it. A3's `.generated.h` clause, B1's Unreal letter,
   and K4's `try`/`catch` clause all stay below the line on this.
2. **Delegated is never BREAKING.** A row that hands its failure to another
   row doesn't also carry that severity. L3 and I3 hand GC coverage to C4,
   and F3 hands the base null deref to F1.
3. **A row takes the highest severity it owns**, not the severity of its
   most common finding.
4. **The failure follows from the violation alone**, not from the violation
   plus project setup the row can't see. That's what holds I2 and A2 at
   PRACTICE.

## Per-file checklist

### A. File-level

| # | Tag | Rule | What to check |
|---|-----|------|---------------|
| A1 | [G] | **Copyright header** | First line is exactly `// Copyright {{COMPANY}}` followed by a blank line. Not an engine template placeholder. |
| A2 | [U] | **Include paths** | All `#include` directives use full module-rooted paths (`"{{MODULE}}/Core/..."`, `"{{MODULE}}Editor/..."`). No relative or bare filenames. [P] Includes sorted alphabetically within their group. |
| A3 | [G] | **IWYU** | Header forward-declares where possible. The `.cpp` carries the full includes. Include every header you use directly. Don't lean on transitive includes. [U] In `unreal`, `*.generated.h` is the **last** include in the header (UHT build requirement). Forward declarations sorted alphabetically [P]. [P] Includes run in origin groups — in a source file its own paired header first, then project or module, then engine and third-party, then standard library — one blank line between groups and sorted within a group; A2 owns the path form, and where a formatter config encodes the grouping A10 makes that config the authority and this clause is checked against it rather than by eye. |
| A4 | [P] | **Indentation** | Matches the driver profile's **Indentation** knob, consistently, with no mixing. N/A until that knob is filled. _Epic's answer: tabs (size 4). Many projects choose spaces — set it in the driver's profile and enforce whatever it says._ |
| A5 | [P] | **Line length** | No line exceeds the driver profile's **Max line length** knob. N/A while that knob is unfilled, and N/A if set to `none`. When a cap is set: break long lines at logical boundaries, and split long string literals with adjacent-literal concatenation. _Epic sets no limit._ |
| A6 | [G] | **No anonymous namespaces** | No `namespace { ... }` in `.cpp`. File-locals go in a named namespace path unique to that file or feature (`namespace {{NAMESPACE}}::<Feature>`) **with `static` on the members** — the unique path prevents cross-file collisions, `static` keeps internal linkage. A single shared helper namespace fixes nothing: two files defining the same symbol in it still collide merged, and unmerged the now-external symbols become duplicate-symbol linker errors. A lone `static` helper with a descriptive file-specific name is fine. Why: unity builds concatenate `.cpp` files into one translation unit, collapsing every anonymous namespace into one — cross-file collisions and ODR violations that pass local builds (adaptive unity ejects files under edit, so the author is the one person who can't see it) and only blow up in CI/Shipping. Never an anonymous namespace in a header (per-includer copy — ODR trap); header constants stay `inline constexpr` in a named namespace. |
| A7 | [G] | **Namespace closing comments** | Every `}` closing a namespace carries `}    // namespace <Name>` (four-space gap). |
| A8 | [G] | **`#endif` / `#else` trailing comments** | Every `#endif` has a comment matching its `#if`: `#endif    // WITH_EDITOR` (four-space gap). Same for `#else`. (Headers still guard with `#pragma once`.) |
| A9 | [G] | **No emoji or decorative Unicode in committed text** | Code, comments, string literals, and log messages contain no emoji and no decorative glyphs — a documented generation tell, and MSVC's ANSI-codepage default mangles non-ASCII literals without `/utf-8`. [P] Projects may tighten to strict ASCII-only: no em/en dashes, curly quotes, or ellipsis characters in any committed file. Non-ASCII that is *data* (a deliberately localized literal) is exempt — flag it for confirmation rather than FAIL. |
| A10 | [P] | **Formatter config is the authority** | Resolved once for the fileset rather than per file, and **N/A** where the project declares no formatter — A4 and A5 then carry the load alone. Where it declares one, exactly one config governs the code under review, it sits at the widest tree the project owns, and nothing shadows or voids it. **Resolution** — walk a changed file's parents the way the tool does; resolving to none leaves the file drifting to whatever each editor guesses. **Shadowing** — a nested config silently overrides its parent for a whole subtree with no error and no log line, and one merely duplicating its parent is a leftover. **Exclusions** — read the patterns, not the filename: one glob broad enough to match the language's own extensions makes every format command exit clean having touched nothing, and a tool reporting success while doing nothing is this row's signature failure. **Boundary** — a config reaching a vendored, upstream-engine, third-party, or generated tree is the opposite failure; exclude an unowned subtree positively. Where a config governs, it rather than the driver profile is the source of truth for the axes it encodes: transcribe them into **Indentation** and **Max line length**, name the config they came from in the report, file a disagreeing knob against the profile rather than against the code, then stop hand-checking those axes and file one finding per file. Case is no formatter's axis, so D1–D3 stay hand-checked, and where a config would move what another row pins, pin or exclude that spot instead — [U] A3's last include, A7 and A8's trailing-comment spacing. |

### B. Type declarations (UCLASS, USTRUCT, UENUM, UINTERFACE) — `unreal` only

| # | Tag | Rule | What to check |
|---|-----|------|---------------|
| B1 | [U] | **Type prefix** | Unreal letter is correct for the kind: `A` (Actor), `U` (UObject), `F` (struct), `E` (enum), `I` (interface), `S` (Slate), `T` (template). [P] Project prefix `{{PREFIX}}` follows the letter: `A{{PREFIX}}X`, `U{{PREFIX}}X`, `F{{PREFIX}}X`, `E{{PREFIX}}X`. (Blank `{{PREFIX}}` ⇒ stock Unreal names.) Delegates take the prefix too (`FOn{{PREFIX}}XChanged`). Plugin modules follow the plugin's own established prefix, not `{{PREFIX}}`. Member names, locals, gameplay tags, and folder names are unaffected. |
| B2 | [U] | **Filename matches** | Header filename matches the primary type: `{{PREFIX}}Widget.h` for `A{{PREFIX}}Widget`. |
| B4 | [U]/[P] | **HideCategories** | Level-placed marker/config actors with no physics/collision body add `HideCategories = (HLOD, Collision, Cooking, Replication, Navigation, Networking, Mobile, RayTracing, Physics, Input, LOD)`, dropping entries the actor legitimately uses. |
| B5 | [G] | **Comment style (class/struct)** | `/** ... */` Javadoc block for class and struct declarations only. |
| B6 | [G] | **Access-specifier grouping** | Repeated `public:` / `protected:` / `private:` labels are allowed to separate logical groups (constructor vs properties vs functions); not merged into one block. |
| B7 | [U] | **Reflection earns its macro** | Every `UCLASS`/`USTRUCT`/`UPROPERTY`/`UFUNCTION` has a named engine consumer: GC, editor, Blueprint, replication, config, serialization, or dynamic-delegate binding. Stray reflection on plain C++ is dead registration code compiled into every build and a contract that doesn't exist (pairs with K5; UFUNCTION specifics in G1). The inverse direction is correctness, not style: UObject pointer members GC-covered (C4), `AddDynamic` handlers `UFUNCTION` (G1), replicated/config data reflected. Editor-only metadata (tooltips, categories) costs shipping nothing — registration code is what ships. |

### C. Members and properties

| # | Tag | Rule | What to check |
|---|-----|------|---------------|
| C1 | [G] | **Comment style** | Members, properties, functions, inline notes use `// ...` line comments. Never `/** ... */` (that's declarations only, per B5). |
| C3 | [U] | **DisplayName meta** | `DisplayName` lives inside `meta = (DisplayName = "...")`. Omit entirely when Unreal's auto-generated string (strip prefix, split CamelCase) already matches. |
| C4 | [U]/[P] | **Object-pointer members — ownership picks the type** | `UPROPERTY` object pointers in headers use `TObjectPtr<T>`, not raw `T*` (UE5 GC/cook tracking; UnrealObjectPtrTool migrates the rest). [P] Non-owning cross-actor / widget-to-actor references use `TWeakObjectPtr<T>` default-init `= nullptr` — no `UPROPERTY` required for GC correctness (add one only to serialize or show in-editor). **A non-`UPROPERTY` raw `T*` UObject member is a FAIL** — GC can't see it: it dangles after any GC pass and keeps nothing alive. Fixes: `TWeakObjectPtr`, `UPROPERTY` `TObjectPtr`, or `FGCObject::AddReferencedObjects` on non-reflected classes (Slate, plain C++; `TStrongObjectPtr` roots the target — a leak for anything with a normal world lifecycle, so only for deliberate ownership). In `.cpp` bodies and locals, raw `T*` is correct — `TObjectPtr` is header-only. Mechanical gate a project can adopt: `NonEngineNativePointerMemberBehavior=Disallow` under `[UnrealHeaderTool]` turns a raw-pointer `UPROPERTY` into a build error; UHT never sees non-`UPROPERTY` members — those stay review's. |
| C5 | [G] | **Unit suffixes** | Identifiers carrying physical units encode the unit: `ThresholdCm`, `DurationSec`. |
| C6 | [U] | **Transient for runtime-derived state** | A `UPROPERTY` holding runtime-derived state on a type saved into assets or maps is `Transient` (smaller assets, cleaner diffs, no stale cache on load). `Transient` controls serialization, not visibility — pairing it with `VisibleAnywhere` to inspect runtime state in Details is the engine's own pattern (`Actor.h`, `CharacterMovementComponent.h`). `Transient` + `SaveGame` on one property is a contradiction → FAIL. Edge cases worth knowing: Blueprint CDOs still serialize transient defaults; duplication still copies (that's `DuplicateTransient` — identity-keyed caches and GUIDs usually want it). |
| C7 | [U]/[P] | **Comment is the tooltip** | The comment above a reflected declaration becomes the editor tooltip — UHT compiles it automatically, from `/** */`, `//`, or `///`. One comment serves both readers; `meta = (ToolTip)` only when designer-facing text must differ (it wins over the comment, and the two drift — keep it rare). `//~` comments are excluded from tooltips (the sanctioned engineer-only note). A blank line between `//` blocks discards the earlier block — only the adjacent block becomes the tooltip. |
| C8 | [G] | **Cross-system references are handles, not stored raw pointers** | A member referencing data another system owns is an ID or generation-checked handle resolved through the owning system, or a weak/observing pointer — never a stored raw pointer (a dangling deref is UB; a stale handle resolve returns null the caller can branch on). UObject targets: the engine types already are handles — use C4's, don't build a registry. Bespoke handles (non-UObject pooled data the project owns): ≤8 bytes, trivially copyable, with an adjacent `static_assert` on both — the engine designs to exactly this (`FMassEntityHandle` asserts `sizeof == 8`; 1/2/4/8-byte trivially copyable args ride a register on MSVC x64). Persistent identity stays `FGuid` (16B) at the persistence/network layer, mapped to the runtime handle at load (I2). Raw is fine within one function scope after one resolve — provided no invalidation event sits between the resolve and the last use (E5's window names the categories) — and at engine/third-party API boundaries. No owning registry to generation-check the resolve → no handle: it adds indirection and no safety. |
| C9 | [G] | **Cross-type reads go through the owner's read-only surface** | For every member the change widens or reaches around, name the consumer a published read-only accessor could not have served — no name, or a name the accessor would have served, FAILs, and the accessor on the owner is the fix (G2 places it, G3 and G4 shape its return). A `friend`, a subclass, a cast, or a hand-synchronized duplicate introduced to see a protected or private member FAILs whatever the name. **Accessor shape:** FAIL on a non-const reference or pointer return onto a data member, a mutable container reference, and a setter added beside a new accessor that reopens what it just closed — a caller holding a mutable handle skips whatever the owner runs on write. [U] In `unreal` the consumer must be an *access* one, never a reflection one: a reflected member is editor-visible and serialized at any specifier, so a `UPROPERTY` never needs `public:` to be edited or saved, and Blueprint read/write of a private member is `meta = (AllowPrivateAccess = "true")`, not a promotion. M1 owns which specifier a role takes; this row owns reaching past it. |
| C10 | [G] | **Comment content follows the declaration's audience** | Constrains only a comment that survives K1; never demands one where none exists. **Type declarations and header-public API**: role, contract, preconditions, ownership transfer, failure behavior — never the algorithm, the internal step order, or the structures the body picks. **Members**: meaning, unit, valid range, or invariant, exposed or not (C5 owns the unit in the name). **Exposed configuration a non-engineer authors**: what the value changes, its workable range, and the behavior at the extremes; one naming the storage type, the internal consumer, or the reading call site FAILs though it is perfectly true. Mechanical test: a declaration comment needing an edit after a body rewrite that changed no contract is implementation detail — move it to the definition. An engineer-only aside on a published declaration moves to the audience-excluded form ([U] C7's `//~`) or to the definition. B5 and C1 own comment syntax, K1 whether the line earns itself, this row what it says. |

### D. Naming

| # | Tag | Rule | What to check |
|---|-----|------|---------------|
| D1 | [P] | **Local variables** | Declared inside a function body: matches the driver profile's **Local-variable case** knob. N/A until that knob is filled. _Epic's answer: `PascalCase` (Epic applies no local exception). `lowerCamelCase` for locals is the common house answer — set whichever in the driver's profile._ |
| D2 | [U] | **Function parameters** | `UpperCamelCase`. Epic additionally prefixes `In`/`Out` for input-only vs written-by-reference params (`bOutResult` for a bool out-param) — apply if the project follows it [P]. |
| D3 | [U] | **Members / types / functions** | `UpperCamelCase`. Booleans prefixed `b`: `bIsActive` (`bOut...`/`bIn...` when combined with a param prefix). |
| D4 | [G] | **Named bool args** | Magic `true`/`false` at call sites replaced with a named `constexpr bool` local for readability (`unreal`'s convention: `bIsRetry`; elsewhere: `isRetry`, or per D1's case). |
| D5 | [G] | **Case follows the name's audience** | Classify every identifier the change introduces or renames by its **widest reader**, never by the file it sits in, then check its case against that reader's convention. **File-internal** — block-scope locals, file-local helpers, lambda captures — takes the house local case (D1). **Declaration-surface** — parameters, members, and the type and function names a header exports — takes the API convention (D2, D3), which a house local knob never reaches. **Externally bound** — anything a serializer, reflection or script layer, config parser, tool binding, or peer resolves *by string* — takes the consuming system's convention, and no house knob overrides it; D6 owns what happens when one is renamed. Readers stack, so the widest owns the case, and a rename carrying the house local case across the first of those boundaries FAILs. Where a tool or doc generator derives display text by splitting or stripping the identifier, the derived string reads as the label a non-engineer would write — noun phrase for data, verb phrase for a command. |
| D6 | [G] | **Externally bound names are data** | An identifier is **externally bound** when something outside the compiler resolves it by name: a serializer writes the spelling into save data or authored content, a reflection or script layer looks it up as a string at run time, a config or tool binding keys on it, a peer expects it on the wire. For every rename in the change, search the old spelling across config, script, and text-form authored content before reading the rename as style — bound, it compiles clean and warns nothing, then drops the value from every artifact already written under the old name, or leaves the binding unresolved at run time with no diagnostic at the fault (**Determinism & serialization**). FAIL when a bound name moves and no migration moves with it: a redirect or alias mapping old spelling to new, a version bump with an upgrade path, a shim reading both spellings, or the authored content re-saved inside the same change. **Name the artifact or demote it** — per the driver's reproduce-before-you-file rule, only pointing at the durable artifact, config key, or binding that still resolves the old name earns the BREAKING band; a rename with no such artifact reachable is D5's convention finding. |

### E. Control flow and local variables

E1 to E4 govern the shape of statements; E5 and E6 govern the locals those
statements introduce. The two halves cross-reference each other and no row
here re-files another's finding.

| # | Tag | Rule | What to check |
|---|-----|------|---------------|
| E1 | [G] | **Always brace** | All `if`/`for`/`while` bodies are braced, even single statements (Epic: "Always include braces in single-statement blocks"). Opening brace on its own line (Epic house style). [P] Some house styles exempt a single-line guard-clause early return / continue / break from bracing — Epic does not; enforce whichever the project declares. |
| E2 | [G] | **Early-return guards — a flat prologue** | Prefer early-return over deep nesting, checked two ways. **Shape** — validity, precondition, and range guards form a flat run at the top of the body: each at one level, each ending in `return`, `continue`, or `break`, each followed by the next guard rather than containing it. Two forms FAIL — a guard inverted into a body-wrapping `if` that holds the rest of the function, and an `else` after an arm that already returns, continues, breaks, or throws (drop the `else` and outdent under it). **Floor** — whatever number E4's budget carries, prefer the flattest shape that keeps the same guarantees; this clause has no knob and runs in every profile, so E4 can be renumbered without licensing depth. An early exit added below an acquire, a registration, or a flag set on the way in must discharge the same pairing the fall-through path discharged — a flatten that skips a release, an unregister, or a cleared in-progress flag is an Ownership & lifetime finding (Threading model for a lock) for the driver's breaking hunt, and where the two collide the obligation wins and the nesting stays. E1 owns whether a guard is braced, E4 the depth budget and the flattening moves. |
| E3 | [G] | **Ternary parenthesization** | Parenthesize the condition: `(IsValid(X)) ? A : B`. |
| E4 | [G]/[P] | **Nesting depth budget** | **Statement nesting inside a function body stays within the depth budget — default `3`**, the body's own brace being depth 0, so a fourth level FAILs. [P] A project may set another number; it may not switch the row off, because E2's floor is the ground it would fall to. Counting: sibling arms cost one level between them rather than one each, so an `else if` ladder or a `switch` is one level however many arms it has; a lambda body restarts at its own depth 0; a macro invocation is one statement, never the scopes it expands to. **A depth number with no applicable move is not a finding** — over budget, name the move the shape calls for. Guard-shaped nesting is E2's inversion and files there, never twice. A branch ladder over a closed set flattens to one ladder or a table keyed by that set. A loop-invariant *branch* hoists above the loop; the invariant *expression* is E5's. An inner loop that only finds the outer element's match becomes L2's single-lookup idiom. A loop body that has grown its own guards, inner loop, and exits lifts whole into a single-use named helper — the decomposition K5 exempts by name, named per K7. **Flatten, don't launder**: a helper whose only purpose is moving depth out of view is K5's FAIL and the depth finding stands. Exempt: a level the language or platform forces, including a scope block bounding one object's lifetime; braces E1 mandates; two loop levels over genuinely paired data, though not a third; indented *data*, which is not control flow; generated bodies the change does not own; and pre-existing depth the change only re-indents. |
| E5 | [G] | **Cache a repeated evaluation once** | Two triggers. **Repeat** — one of six role categories evaluated twice on one execution path with nothing between that can change an input it reads: an accessor chain of more than one link, a container lookup on one key, a weak-reference or handle resolve, a subsystem or context accessor call, a pure computation on unchanged arguments, a loop-invariant expression. The second evaluation is the FAIL — the threshold [U] F1 already sets for a weak resolve and L2 for a keyed lookup. Count per path: mutually exclusive branches are not a repeat, one evaluation inside a loop is, and the fix there is a hoist above the loop. One finding per expression, never per occurrence. **Window** — a cached reference, iterator, or interior pointer whose live range spans container mutation or reallocation, a callback, broadcast, timer or latent gap, teardown of the owner, or cross-thread publication. Re-derive it, and name the event. The window is this row's FAIL; the stale dereference belongs to the driver's breaking hunt (Ownership & lifetime, Undefined behavior, Threading model) and is marked already-filed here. Against K7 the boundary is the read count rather than taste: this row's local has two or more reads where a rename-only intermediate has one. E6 owns how the local is then declared. |
| E6 | [G] | **Cached-local declaration** | How a local that has earned its place is declared, never whether it should exist — E5 owns that, a single-read rename is K7's, an unused one K3's. **Placement**: initialized in its own declaration, in the innermost scope containing every use, once per expression per scope, ending at its last read. The test is a path comparison — the paths reaching the initializer are the same as, or a subset of, the paths reaching its uses. FAIL: hoisted above a precondition or validity guard, making a guarded cost unconditional; hoisted out of the one branch that used it, or out of a conditionally entered loop or conditionally compiled block; a declare-at-top run separated from its uses by intervening control flow. **Binding**: by reference where copying is expensive and by value where it is not, on G4's copy-cost threshold, one number for parameters and locals alike — a by-value cache of a non-trivially-copyable value every use only reads puts the hoisted cost straight back, once per pass inside a loop, and a reference cache of a small scalar or handle pays an indirection for nothing. **Const**: `const` unless a later line assigns it; a local that *is* reassigned is an accumulator rather than a cache, and N/A here. [P] A house declaring locals at block top enforces that position instead, keeping the once-per-expression and last-read halves. Bare `auto` copies where `const auto&` aliases (L4). |

### F. Null safety (`IsValid`/`Cast` mechanics) — `unreal` only

| # | Tag | Rule | What to check |
|---|-----|------|---------------|
| F1 | [U] | **Match the check to the pointer type** | Strong members (`UPROPERTY` `TObjectPtr`/raw): `IsValid(...)` before dereference, never a bare `if (Ptr)` — between `Destroy()` and the next GC pass a strong member is non-null and dead (`IsValid` also rejects Garbage/pending-kill objects a null check misses). Weak members (`TWeakObjectPtr`): resolve **once** — `if (T* X = Weak.Get())` — and use the local; `IsValid()`-then-`Get()` runs the identical full resolution twice (the engine deletes `operator bool` on weak pointers with the comment "use Get() once in a function"). `Weak.IsValid()` alone is correct only for validity-only tests that never touch the object. Structurally guaranteed lifetimes (a `CreateDefaultSubobject` component, an owning Outer) may skip the per-use check or use `ensure(IsValid(X))` so an invariant violation still fails loudly. Re-resolve after any latent gap (timer, delegate broadcast, latent action). |
| F2 | [U] | **Cast pattern** | `Cast<>` results flow through a validity ternary: `T* X = (Raw) ? Raw->Get() : nullptr;`. |
| F3 | [U] | **World / subsystems** | `IsValid`-checked (or null-checked for non-`UObject` handles) even when `World` was already checked upstream. |

### G. Functions

| # | Tag | Rule | What to check |
|---|-----|------|---------------|
| G1 | [U] | **UFUNCTION decoration** | BP-safe accessors carry `UFUNCTION(BlueprintPure)`. `AddDynamic` handlers need a bare `UFUNCTION()`, since dynamic delegates bind by function name and resolve through reflection at call time. `AddUObject` handlers bind by pointer and need **no** `UFUNCTION` at all — adding one is dead reflection (see K5). This doc mandates no `Category` policy; use whatever the project's editor organization calls for. |
| G2 | [G] | **Trivial getters** | Inline in the header. Non-trivial (pointer deref, computation) defined in `.cpp`. |
| G3 | [G] | **Reference-return safety** | Return `const T&` only when **every** branch yields a stable-lifetime reference. Otherwise return by value. Never `const` on the return type itself (inhibits move semantics). |
| G4 | [G] | **Parameter passing by copy cost** | `const&` when a copy is expensive: any non-trivially-copyable type (`FString`/`TArray`/`FText` pass by hidden reference on every shipping ABI anyway — `const&` removes the caller-side copy), and trivially copyable types over 16 bytes (LWC doubles make these bigger than float-era intuition: `FVector`/`FRotator` 24B, `FQuat` 32B, `FTransform` 96B). Trivially copyable ≤16B goes by value (`float`, `FName`, handles, `FVector2D`) — `const float&` adds indirection and buys nothing. Sinks with a non-trivial move take by-value + `MoveTemp` (Epic blesses the idiom verbatim); trivially copyable aggregates stay `const&` even when stored (their move is a copy). Out of scope: engine virtual overrides, delegate signatures, and established BP-facing APIs keep their shapes; deferred/async lambdas capture by value (lifetime, not perf); hot `FORCEINLINE` leaf math is deliberate engine practice. [U] **A `BlueprintCallable` parameter converted to a reference must stay `const`** — UHT turns a non-const reference param into an OUTPUT pin: compiles clean, no warning, and the input pin vanishes from the node, dropping the connection in every calling Blueprint. |

### H. Logging

| # | Tag | Rule | What to check |
|---|-----|------|---------------|
| H1 | [U] | **Log category** | Feature-scoped: `DEFINE_LOG_CATEGORY_STATIC({{LOG}}<Feature>, Verbose, All);` in the `.cpp`. Project-wide categories use `DECLARE_LOG_CATEGORY_EXTERN` in a shared header. |
| H2 | [G] | **Message format** | `"ClassName::FunctionName(%s) - <what> so <consequence>."` with a context arg — `unreal`: `*GetActorNameOrLabel()`; other profiles: your project's identifier convention. Long messages: multiline log call — category, verbosity, format string, and each arg on its own indented line. |

### I. Architecture patterns (if applicable) — `unreal` only

| # | Tag | Rule | What to check |
|---|-----|------|---------------|
| I1 | [U] | **Data-asset / actor split** | Shared archetype config in a `UPrimaryDataAsset`; per-instance data on the actor as `EditInstanceOnly`. Skip the asset entirely when values are per-instance and unshared — keep the fields on the actor. The actor mirrors the data-asset getter API, forwarding with safe fallbacks (`FText::GetEmpty()`, `0.f`, default-constructed soft pointer) plus a startup warning when the asset is unset. |
| I2 | [U] | **Reference by stable ID** | Cross-system / persisted references use `FGuid`, not pointers. Resolved on demand via the owning subsystem's `TMap<FGuid, T*>` lookup — give a new long-lived entity that resolver up front. Level-placed actors auto-generate the ID in `OnConstruction` (with `Modify()`) so it bakes into the level on first placement. Direct pointers stay reserved for hot, same-frame, in-system references. `custom` profile: see J2 (handle-based resources) for the non-Unreal equivalent. |
| I3 | [U] | **Actor self-registration** | Two flavors. Designer-wired (owner known at placement): `EditInstanceOnly` owner pointer; `BeginPlay` → `Owner->RegisterX(this)`; `EndPlay` → `Owner->UnregisterX(this)`, guarded by `IsValid(Owner)`. Runtime-wired (owner assigned at runtime): `Transient, VisibleAnywhere` owner pointer plus a `SetOwner` setter as the registration handshake — same-value early-out → unregister from the old owner → assign → register with the new — which avoids the two-actor `BeginPlay` ordering race; `EndPlay` keeps the guarded unregister for direct destroy paths. Owner side is idempotent in both flavors: register = add-unique + auto-select-first-if-none + broadcast on net change; unregister = remove + fall-back-to-first-remaining + broadcast. |

### J. Engine architecture (custom profile) — `custom` only

House style for a bespoke C++ game engine, on top of the **[G]** general-C++
rows above. **These rows check architecture and house style** ("is this
handle-based," "is this static hot-reload-safe") rather than auditing a
specific line for a bug — the line-level audit is the driver's protocol
step 2, which sweeps the same six categories across the fileset. Each row
below names its **Nearest correctness category**, which is how a FAIL here
gets its severity from § Severity map and how it collates with a
`cpp-gamedev-check.md` finding on the same code. That file stays the
author of the six; this one applies them.

| # | Tag | Rule | What to check | Nearest correctness category |
|---|-----|------|----------------|-------------------------------|
| J1 | [C] | **ECS / data-oriented layout** | Gameplay/simulation data lives in contiguous component stores (arrays/pools), not one-object-per-heap-allocation. Systems iterate a component type across all entities in a tight loop, not a virtual-dispatch tree of per-object `Update()` calls. Hot data (touched every frame) and cold data (rarely touched) aren't interleaved in the same struct. | Performance hot-path |
| J2 | [C] | **Handle-based resources** | Cross-system or persisted references to entities, assets, or pooled objects are opaque handles (index + generation counter, or equivalent), never a raw pointer or reference held past the current scope/frame. A handle into a freed/recycled slot fails a validity check instead of silently aliasing the new occupant. | Ownership & lifetime |
| J3 | [C] | **Job/task-system threading discipline** | Work submitted to the job/task system declares its data dependencies (read/write sets) instead of relying on ambient shared state. No raw `std::thread`/spawn-and-forget bypassing the job system. Mutation of shared state happens only at the engine's designated sync/barrier point, never mid-job. | Threading model |
| J4 | [C] | **Custom RTTI** | Type identification and safe downcasting go through the engine's own type-registration/reflection system, not `dynamic_cast` (commonly disabled) or raw `typeid`/`reinterpret_cast` punning. New types self-register (static registration or codegen), not a hand-maintained switch/if-chain. | Undefined behavior |
| J5 | [C] | **Versioned serialization** | Save-game, replay, and asset formats carry an explicit version number and a migration/upgrade path. A file written by an older build still loads, or fails with a clear "unsupported version" error — never silent data corruption. Field additions/removals are backward-compatible or bump the version. | Determinism & serialization |
| J6 | [C] | **Hot-reload-safe statics** | Function-local statics, global statics, and singletons that hold engine state survive a hot-reload / DLL-swap cycle without silently resetting, double-initializing, or holding a dangling pointer into unloaded code/data. State that must persist across reload lives in a reload-stable location, not a static inside the reloaded module. | Determinism & serialization |

### K. Machine-generation tells — every profile

The recognizable tells of carelessly machine-generated code, reviewable
per file like every other section. Same charter as § J: these rows police
style-level generation residue, so most of them are CONVENTION. Hallucinated
or near-miss API usage (a plausible-but-wrong engine call, a misremembered
signature) is **not** out of scope any more. A non-compiling name is
build-caught and never reaches a reviewer, so it stays below the line per
§ Severity map rule 1. A *compiling* near-miss is a live defect: file it
under the driver's breaking hunt at the severity its failure earns, naming
the `cpp-gamedev-check.md` category it trips.
All K rows are **[G]** and run in every engine profile; [U] sub-clauses
activate in `unreal` as usual.

| # | Tag | Rule | What to check |
|---|-----|------|---------------|
| K1 | [G] | **Comment earns its line** | Every prose comment adds information the adjacent code doesn't already state. FAIL: comments restating the next line (`// increment the counter`, `// call Initialize`), step-by-step narration of plain control flow, section banners over two-line groups, and doc blocks that only re-spell the signature (`/** Gets the health. */` on `GetHealth()`). A comment stating *why* — an invariant, a unit, an engine quirk, an ordering constraint — always passes. Structural markers this doc mandates (A7 namespace closers, A8 `#endif` trailers) are exempt. B5/C1 govern comment *syntax*; this row governs *content*. |
| K2 | [G] | **No conversation or edit residue in comments** | Comments address the future reader of the code, never the author's prompter or this change's reviewer. FAIL: edit-narration (`// updated to fix the bug`, `// changed to use TWeakObjectPtr`, `// NEW:`, `// as requested`), apologetic or chatty tone (`// just to be safe`, `// hopefully this works`), and progress markers. What changed belongs in the changelist description; a genuine why-it-is-this-way note stays, rewritten without the temporal frame. |
| K3 | [G] | **No dead or placeholder code** | No generation scaffolding ships: no `TODO: implement` stubs or bodies returning a default in place of the real logic; no commented-out code blocks; no `// ... rest of implementation` elisions; no unused local variables kept "for clarity". A deliberate deferred-work TODO carries an owner or ticket reference; a bare model-emitted TODO FAILs. Unused *parameters* forced by an engine signature (virtual overrides, delegate handlers, interface implementations) are exempt; unused *includes* are A3's finding. Whether an unused variable hides a semantic bug is a BREAKING-band question, not this row's. |
| K4 | [G] | **Defensive code only where the contract allows failure** | Every diff-introduced guard protects a condition that can actually be false on some path. FAIL only when you can point at what makes it impossible: a reference (not pointer) parameter, an assignment on all paths just above, an established caller contract, or the same diff already validating it one level up a private call chain. Can't name the guarantee → PASS — stripping a live guard is worse than keeping a dead one. A genuinely can't-fail invariant worth stating is a `check()`/`ensure()` (or the project's assert) documenting impossibility, not a silent early-return that launders it into a legal path. [U] New `try`/`catch` in runtime module code FAILs unless the module already opts into exceptions (`bEnableExceptions`) — Unreal defaults exceptions-off and packaged builds reject `throw`. UObject validity is always genuinely falsifiable (GC, pending-kill, teardown ordering), so F1–F3 and weak-pointer resolve-then-check are never "redundant" under this row — it governs everything section F does not. Missing guards on conditions that can fail are not this row's: file them in the BREAKING band when the unguarded path crashes, otherwise PRACTICE. |
| K5 | [G] | **No speculative abstraction** | Every interface, base class, factory, template parameter, config knob, and indirection layer the change introduces has at least two real users, or a named concrete second user landing near-term. Two exemptions: patterns this doc prescribes (e.g. I1 mirrored getters, I2 up-front resolvers, I3 registration handshakes, § J machinery) — prescribed generality is house style, not speculation; and abstraction the engine's machinery requires (a `UINTERFACE` for BP-implementable interfaces or `TScriptInterface` decoupling, a base class that exists to be subclassed in Blueprint) — the Blueprint/designer side counts as the second user. One-caller pass-through wrappers, single-implementation interfaces with no engine reason, and "might need it later" generality FAIL — inline them and let the second user extract the abstraction. A single-use named helper extracted for readability (A6's one-off `static`/namespaced helpers) is decomposition, not a layer. |
| K6 | [G] | **Use the existing facility** | New helpers, utilities, or validation logic don't re-implement what the project, engine, or standard library already provides (`FMath`/STL math, existing string/validation utils, an existing subsystem accessor, a shared module's facility). For every helper the change introduces, search for the existing equivalent first; a near-duplicate under a slightly different name FAILs — call the existing one, or extend it only when the project owns it (upstream/engine facilities get called or wrapped, never edited). Prescribed forwarders (I1's mirrored getters) call the existing facility and pass. |
| K7 | [G] | **Names carry information, not ceremony** | The test is "does the name add information", never length. No type-spelling echoes where a role name exists (`FVector VectorPosition`, `TArray<int32> IntArray`); type-as-name locals are idiomatic when the type's noun IS the role (`FHitResult HitResult`, `FTimerHandle TimerHandle`). No rename-only intermediates (`const auto& Result = Compute(); return Result;`); single-use locals that ADD information stay (D4's named bools, F2's Cast-ternary local, F1's `Get()`-resolve local, E5's repeated-evaluation locals). **The boundary with E5 is the read count, not taste**: a rename-only intermediate is read once, E5's cache is read twice or more. No side-effect-enumerating names (`ValidateAndProcessAndSaveX`) — split the function or name its primary effect; single-effect compounds (`FindOrAdd`, `GetOrCreate`) are fine. Descriptive length is NOT a violation (Epic deliberately favors `GetActorNameOrLabel`-length names), and doc-mandated affixes (B1 prefixes, D3 `b` booleans, C5 unit suffixes) are information, not ceremony. |
| K8 | [G] | **Match the surrounding idiom** | New code reads like the file it lands in: same error-handling shape, the file's guard and iteration style within the shape E2 and E4 prescribe, the file's established helpers, comparable comment density and blank-line rhythm. A mid-file style flip — comment density spiking in one function, a different brace/naming rhythm, patterns imported from another codebase's conventions, runs of meaningless blank lines — is a paste-seam; rewrite the new code to the local idiom. A4 covers indentation mixing and D-rows naming case; this row covers the other axes of intra-file consistency, and M3 covers consistency across a mirrored pair. **Precedence**: where another row in this doc prescribes a shape, that row wins and matching the file is not a defense — a uniformly deep or uniformly duplicated file licenses nothing. |
| K9 | [G] | **Logs earn their verbosity level** | No step-by-step narration logging added with the change (`"starting update"`, `"finished loading"`, one log per branch of normal control flow) at Log/Display verbosity. Every new log line at those levels states a consequence a reader acts on (H2's what-so-consequence shape); trace detail goes to Verbose/VeryVerbose. H2 governs the message *format*; this row governs whether the call should exist at that level at all. Hot-path log *cost* is a Performance hot-path finding, so PRACTICE, not this row. |
| K10 | [G] | **Docs state the rule, not a snapshot** | A prose document shipping with the change — a README section, a handoff note, a conventions write-up — states the categories, procedures, and checks a reader can re-run, not a snapshot of the tree as it stands this week. Test each enumeration by asking whether a routine edit falsifies the sentence without anyone touching the doc. FAIL: the current order of one file's declarations stated as fact, current default values, a symbol-by-symbol walkthrough, a count the next addition breaks. Each either restates the rule that produced it (M2's order mirrors the header, not the numbered list of what that order is today) or carries a dated-snapshot marker, so a later reader re-derives it rather than trusting it. Procedures take the same test: a pattern to search for, a condition to compare, a check or build to run, never a step only its author could retrace. Scope is a rule too — the doc names the directories or patterns it covers and the trees it excludes, rather than the file list that happened to be in this change. Exempt: reference material whose whole purpose is the snapshot, where the marker alone satisfies the row. K2 owns edit residue in comments; this row owns the prose a change ships. |

### L. Containers and types — every profile

Container access and type discipline. L1 is the section's one correctness
hazard rather than a preference: the assert most people assume sits under
`operator[]` does not exist in the builds players run.

| # | Tag | Rule | What to check |
|---|-----|------|---------------|
| L1 | [G] | **No unchecked `operator[]`** | Every map/array `operator[]` has a presence/bounds check on the lines just above (`Find`, `IsValidIndex`, `Contains`), or a comment stating the local invariant that guarantees it. `TMap::operator[]` is `FindChecked` and `TArray::operator[]` a `RangeCheck`, both `check()`-backed — and `DO_CHECK` compiles to 0 in Test/Shipping (`USE_CHECKS_IN_SHIPPING` defaults 0 in `Build.h`), so an unchecked subscript ships as a null deref (map) or a silent out-of-bounds read/write (array) in player builds. Never chain subscripts unless every level was checked on the immediately preceding lines. Exempt: iteration protocols (keys/pairs/index loops), a key added in the same scope with no mutation between. Where absence means a program bug rather than a runtime state, `FindChecked`/a checked subscript is the deliberate better tool — it asserts at the fault in Development instead of laundering the bug into a skipped branch. |
| L2 | [G] | **`Find()` over `Contains()`-then-`[]`** | Code that needs the value calls `Find()` once and branches on the returned pointer — `Contains()` + `operator[]` runs the same hash-and-probe twice and the `[]` half is L1's unchecked-in-Shipping access. `Contains()` alone is right when existence is the whole question. Purpose-built one-pass variants beat their two-step idioms: `FindRef` (returns by value — pointer-valued maps only, it silently copies expensive value types), `FindOrAdd` (hashes once, reuses it for the miss-insert), `*ByHash` (hot loops with a precomputed hash), and `TArray`'s `ContainsByPredicate` is literally `FindByPredicate != nullptr`, so the single-scan idiom covers the linear-search family too. |
| L3 | [U] | **Engine types at engine seams** | Anything reflected, serialized, replicated, or on a public module API uses engine types: `TArray`/`TMap`/`TSet`, `FString`/`FName`/`FText`, sized ints (`int32`, `uint8`). For reflected members this is mechanical — UHT rejects std types and the header won't generate. Epic: "Standard containers and strings should be avoided except in interop code." Sized ints are Epic-mandated in serialized/replicated formats; elsewhere plain `int` is Epic-legal ("when the integer width is unimportant") — flag serialized/replicated/reflected `int`, not loop counters. Epic's std allowlist stays available: `std::atomic` ("should be used in new code"), `<type_traits>`, `<initializer_list>`, `std::numeric_limits`, `<cmath>` float functions, editor-only `<regex>`; interop converts to engine types at the boundary. **GC protection comes from `UPROPERTY`, not the container brand** — an unreflected `TArray<UObject*>` member is as GC-invisible as a `std::vector` (C4). |
| L4 | [U]/[P] | **Explicit types over `auto`** | Epic: "You shouldn't use auto in C++ code, except for the few exceptions listed below" — spell the type; a large fraction of reads happen in diffs, merge tools, and single files where no IDE inference exists. Sanctioned exceptions: lambdas bound to variables, verbose iterators, template code where the type can't be discerned, and [P] one house extension — the type already spelled on the same line (`Cast<T>`, `NewObject<T>`, factory calls). Where `auto` is used, qualify it exactly as a named type would be (`auto*`, `const auto&`). Traps deduction hides: `for (auto Elem : Map)` copies a `TPair` per iteration (the engine idiom spells `const TPair<K, V>&`); on a `TObjectPtr<T>` member, `auto` deduces-and-copies the `TObjectPtr` and `auto*` doesn't compile — explicit `T*` is the only spelling that means what was meant. |


### M. Declaration order and organization — every profile

Sections A through L check what a declaration says. This section checks where
it sits. Order carries no runtime consequence, so every row here is
CONVENTION — but it is the axis a reader navigates by, and the first thing a
fan-out of independently written leaves loses. The rows classify declarations
by **role**, never by name, so the same order survives a rename and applies to
a type this doc has never seen.

| # | Tag | Rule | What to check |
|---|-----|------|---------------|
| M1 | [G] | **Access sections are role-defined** | Role picks the specifier, not whatever made the last edit compile. **Public**: constructors and destructor, constants, read-only accessors, and the API read from outside the type. **Protected**: extension points a subclass is meant to use, and a base-declared override at the access its base declares. **Private**: implementation helpers, mutable runtime state, and anything with no outside reader, an internal `constexpr` included. FAIL: a mutable data member under `public:`; a helper, constant, or accessor with no out-of-type caller above `private:`; an override whose access differs from its base's; runtime state left `protected:` on a type no subclass touches; a member widened past this map so one other type can reach it, whose fix is C9's accessor rather than a specifier change. Callers you cannot see never FAIL — a declaration on a module-public header whose consumers sit outside the fileset goes under Ambiguous. B6's repeated labels subdivide a band; they never reopen an earlier one. |
| M2 | [G] | **Declaration order is category order, and definitions mirror it** | Two checks, one mark. **Sequence** — declarations run in the project's declared category order, once across the whole type rather than restarting at each access label, so a read-only accessor below the state it reads, or an implementation helper above the public API it serves, is the finding. [P] The order itself is house style and is **N/A until the Project Profile's Declaration order slot is filled** — never inferred from the code under review. _Copy-in answer: constants and static data, constructors and destructor, read-only accessors, remaining public API, base-interface overrides grouped by owning base with lifecycle first, tool-only or conditionally compiled overrides, exposed configuration, implementation helpers, mutable runtime state last._ **Mirror** — always runs, no declared order needed: the definition file repeats the header's order one-to-one including overloads, definitions with no declaration in that header sit in one contiguous block rather than interleaved, and each category is one uninterrupted run. Exempt: an order the language forces, such as a specialization or a `static` that must precede its first use — note it rather than reorder. |
| M3 | [G] | **A mirrored type keeps its counterpart's shape** | Where the change touches one half of a pair or mirrored family — a runtime type and its tool-only counterpart, or a type and its adapter, view, factory, serializer, or test double — read both halves side by side on four axes: same category order across the categories both sides have, same category behind each label, same relative order for the members that correspond, comparable blank-line rhythm and comment density. **FAIL only where you can name the axis and both sides' values on it** — an unattributable difference PASSes, since two halves doing different jobs legitimately diverge, and a legitimate difference is a whole category rather than an interleave. With no counterpart, the referent is an exemplar of the same **role category** from the review's own scope, picked by role rather than by proximity. A finding names its referent by path and the axis it differs on, or it is not filed. K8 owns consistency inside one file; this row owns it across the pair. |

## Provenance & Epic-standard validation

Every rule above was checked against Epic's **official** C++ Coding
Standard for Unreal Engine and corroborating community references, rule by
rule. **The tag in THIS matrix is the Epic-mandate axis, deliberately not
the checklist's profile-gating tag:** here [U] means Epic/engine-mandated
and [P] means Epic-silent/project-adaptable — so a rule can be all-profile
in the checklist ([G]) yet Epic-mandated in its Unreal expression ([U]
here, e.g. A1/E1), or `unreal`-gated in the checklist yet freely
adaptable ([P] here, e.g. H1/I1–I3). Use this matrix to decide what is
safe to customize; use the checklist tag to know where a row is active.
The two columns are not expected to match. **[U]** means engine/Epic-mandated — enforced by
the engine, UnrealHeaderTool, or Epic's written standard; overriding it
breaks the build, the reflection system, or conformance with the engine
standard (a **[U]** rule can still carry a project *value* — e.g. the
copyright *text* — the *rule* is canonical, the *value* goes in the Project
Profile above). **[P]** means Epic is silent, or the project deliberately
deviates — safe to adapt to house style. Use this section to decide what's
safe to customize when adopting the doc for a new project.

### Validation matrix

| Rule | Tag | Verdict vs Epic standard |
|------|-----|--------------------------|
| A1 Copyright first line | [U] | **Confirmed.** Epic: a copyright notice must be the first line of any distributed source file. CI fails otherwise. Text is project-specific → `{{COMPANY}}`. |
| A2 Full module-rooted includes | [U] | **Confirmed** (fine-grained, IWYU). Alphabetical sorting within groups is a [P] house nicety Epic doesn't mandate. |
| A3 IWYU + forward-declare + `.generated.h` last | [U] | **Confirmed.** Epic: forward declarations preferred, include everything you use, don't rely on transitive includes. `*.generated.h` **must** be the last include — a hard UnrealHeaderTool build rule. |
| **A4 Indentation** | [P] | **Epic and house style collide here.** Epic mandates **tabs, size 4**. The driver's **Indentation** knob ships unfilled — set it to Epic's value or to your own, and the row is N/A until you do. |
| **A5 Line length** | [P] | **Epic and house style collide here.** Epic sets **no** line-length limit. The driver's **Max line length** knob ships unfilled — set it to `none` for Epic, or to a house cap (e.g. 150 chars). |
| A6 No anonymous namespaces / prefer `static` | [P] | House style. Epic bans namespaces around `UCLASS`/`USTRUCT` (UHT) and steers non-UObject APIs into `UE::`, but doesn't forbid anonymous namespaces outright. Reasonable to keep. |
| A7 Namespace closing comments | [P] | House style. Not in Epic's standard; common C++ practice. |
| A8 `#endif`/`#else` trailing comments | [P] | House style. Epic guards headers with `#pragma once`. Trailing comments on conditional-compilation blocks are general good practice, not Epic-mandated. |
| B1 Type prefix (`A/U/F/E/I/S/T`) | [U] | **Confirmed** — UHT requires correct Unreal letters. The extra project prefix after the letter is [P] → `{{PREFIX}}`. |
| B2 Filename matches primary type | [U] | Confirmed convention; UHT/module tooling assumes it. |
| B4 HideCategories meta | [P] | `HideCategories` is a **real** UCLASS specifier. The specific list is project-specific. |
| B5 `/** */` for declarations only | [P] | House comment style; Epic doesn't split comment syntax by scope. |
| B6 Access-specifier grouping | [P] | House style. |
| C1 `//` for members | [P] | House comment style (pairs with B5). |
| C3 DisplayName meta | [U] | `DisplayName` inside `meta = (...)` is the real specifier. "omit when auto-generated matches" is sound Unreal practice. |
| C4 `TObjectPtr` members / `TWeakObjectPtr` weak refs | [U]/[P] | **Confirmed.** UE5 best practice: `UPROPERTY` object pointers in headers use `TObjectPtr<T>` (raw `T*` in `.cpp`/locals); `TWeakObjectPtr<T>` for non-owning refs. |
| C5 Unit suffixes | [P] | Good general practice; not Unreal-specific. |
| D1 Local-variable case | [P] | **Epic and house style collide here.** Epic applies **PascalCase** throughout with no local exception. The driver's **Local-variable case** knob ships unfilled — `PascalCase` for Epic, `lowerCamelCase` for the common house answer. |
| D2 Function parameters | [U] | Confirmed `UpperCamelCase`. Epic's `In`/`Out` prefix convention is an optional [P] note. |
| D3 Members/types/functions + `b` bool prefix | [U] | **Confirmed.** Epic: PascalCase, booleans prefixed `b` (`bPendingDestruction`). |
| D4 Named bool args | [P] | Readability house style. |
| E1 Always brace + brace-on-new-line | [U] | **Confirmed.** Epic: "Always include braces in single-statement blocks"; opening brace on its own line. A single-line guard-clause exemption is a known [P] house deviation some projects adopt. |
| E2 Early-return guards | [P] | General good practice, stated as a checkable prologue shape rather than a preference, and carrying the floor that stops E4's [P] number from reading as permission to nest. |
| E3 Ternary parenthesization | [P] | House style. |
| F2 Cast ternary | [P] | House style around the confirmed validity principle. |
| F3 World/subsystem validity | [U] | Confirmed defensive practice for UObject handles. |
| G1 UFUNCTION decoration | [U]/[P] | **Corrected 2026-07-22.** `BlueprintPure`/`BlueprintCallable` are real specifiers and the decoration policy is project-specific [P]. The `AddUObject`-needs-`UFUNCTION` clause the row used to carry was **wrong**: only `AddDynamic` binds by name through reflection, so only it requires the macro [U]. No `Category` policy is mandated here. |
| G2 Trivial getters inline | [P] | Common house style. |
| G3 Reference-return safety | [U] | **Confirmed.** Epic: **never** `const` on a return type (inhibits move semantics); return `const T&` only for stable-lifetime references, else by value. |
| H1 Log category macro | [P] | `DEFINE_LOG_CATEGORY_STATIC` / `DECLARE_LOG_CATEGORY_EXTERN` are real. The category *name* is project-specific → `{{LOG}}`. |
| H2 Message format | [P] | House logging format. |
| I1–I3 Architecture patterns | [P] | Sound, general UE patterns (data-asset/actor split, `FGuid` references, self-registration). Not project-specific, but "if applicable." |
| A9 No emoji / decorative Unicode | [G]/[P] | Practitioner-attested generation tell ("if the comment has an emoji it's a guarantee" — reviewer study, arXiv 2603.27249) plus the real MSVC codepage risk. Epic is silent; the strict-ASCII tightening is [P] house style. |
| B7 Reflection earns its macro | [U] | Every reflected symbol emits registration code into `.gen.cpp` that compiles into every configuration and constructs `FProperty`/`UFunction` objects at module load; a stray macro also asserts a consumer contract that doesn't exist. The inverse (missing reflection) is C4/G1 correctness. Verified against the UE 5.8 source during the 2026-07 conventions work. |
| C6 Transient | [U] | `CPF_Transient` skips persistent serialization *except when serializing defaults* (`Property.cpp`, 5.8) — the Blueprint-CDO edge is real; `Transient`+`Visible*` runtime inspection is the engine's own pattern (`Actor.h`, `CharacterMovementComponent.h`). |
| C7 Comment-as-tooltip | [U]/[P] | UHT's comment→ToolTip pipeline verified vs `UhtParsingScope.cs` (5.8): blank-line block discard, `/** */`-then-`//` merge, `//~` exclusion. The prefer-comment-over-meta half is [P] house preference. |
| C8 Handles over cross-system raw pointers | [G] | The engine's own shape: `FWeakObjectPtr` pairs `ObjectIndex` + `ObjectSerialNumber` (`WeakObjectPtr.h`), `FMassEntityHandle` static_asserts `sizeof == 8`, `FTimerHandle` bit-packs into one `uint64`. Register rule (1/2/4/8B trivially copyable) per Microsoft's x64 calling-convention docs. Honest pitch: safer everywhere, faster only where a system owns pooled storage and iterates in bulk. |
| F1 Match the check to the pointer type | [U] | Rewritten 2026-07 from "IsValid everywhere": `IsValid()` matches *strong* members (the Destroy()→next-GC-pass window, `KillReference` in `GarbageCollection.cpp`); `TWeakObjectPtr::Get()` already runs the identical flag+serial test, so `IsValid()`-then-`Get()` resolves twice — the engine deletes `operator bool` with a comment saying exactly this ("use Get() once in a function"). The structurally-guaranteed-lifetime carve-out (`ensure(IsValid(X))`) keeps invariant violations loud. |
| G4 Parameter passing | [G]/[U] | Epic mandates `const` on unmodified reference params and blesses the by-value+`MoveTemp` sink verbatim (its own `SetMemberArray` example). The 16-byte threshold is this doc's addition: MSVC x64 registers only 1/2/4/8B trivially copyable args and copies either way at 9–16B; SysV passes ≤16B in register pairs — never meaningfully worse on MSVC, strictly better elsewhere. The BlueprintCallable output-pin trap verified vs `UhtPropertyParser.cs` (5.8). LWC sizes per `MathFwd.h`/`TransformVectorized.h`. |
| L1 No unchecked `operator[]` | [G] | `TMap::operator[]` = `FindChecked`, `TArray::operator[]` = `RangeCheck`, both `check()`-implemented; `DO_CHECK` compiles to 0 in Test/Shipping (`USE_CHECKS_IN_SHIPPING` defaults 0, `Build.h` 5.8). A correctness hazard, not taste — treated as non-negotiable. |
| L2 Find over Contains-then-[] | [G] | `Contains` and `Find` bottom out in the same `FindIndexByHash` walk (`SparseSet.h.inl`) — the second pass adds no safety; the `[]` half is L1's unchecked access. Correctness carries the rule; the perf saving is small in cold code. |
| L3 Engine types at engine seams | [U] | Epic verbatim: "Standard containers and strings should be avoided except in interop code"; explicit-width types mandated in serialized/replicated formats; plain `int` legal "when the integer width is unimportant" — the row scopes the flag accordingly. UHT rejecting std types on reflected members is mechanical, not opinion. |
| L4 Explicit types over auto | [U]/[P] | Epic verbatim: "You shouldn't use auto in C++ code, except for the few exceptions listed below" + the qualify-auto rider. The same-line-type extension (`Cast<T>`, `NewObject<T>`) is [P] house. The `TObjectPtr` deduction trap and the range-for `TPair` copy are 5.8-verified behaviors. |
| J1–J6 Custom-engine architecture | [P] | Epic silent by construction: house architecture for a bespoke engine. Safe to adapt wholesale. |
| K1–K10 Machine-generation tells | [G]/[P] | House/practitioner rows; Epic mostly silent, so all safe to adapt — except K1, which Epic's standard itself demands ("Write useful comments"; `// increment Leaves` is Epic's own bad example), and K4's exceptions-off clause, which UBT enforces (`bEnableExceptions = false`; packaged builds reject `throw`). Measured backing per row: K1 redundant comments are the dominant measured LLM readability issue and K5 Excessive Complexity the top category (arXiv 2605.13280); K2 conversation-context leakage and K9's "verbose style" are reviewer-study detection markers (arXiv 2603.27249); K3 placeholder scaffolding (practitioner slop guides); K4 defensive-ratio divergence from human baselines (arXiv 2511.13972); K6 code-reuse blindness (GitHub agent-PR review guide) + measured intra-repo clones; K7 Redundant Variables is a novel LLM-specific pattern while Poor Naming counts are human/LLM parity — redundancy, not naming quality, is the generation-specific risk — and identifier length is model signature (arXiv 2603.04212), hence the length protection; K8 overblanking (arXiv 2605.13280) + match-the-file practitioner guidance. K10 extends K1's and K2's axis from comments to the prose a change ships, and carries no measurement of its own. |
| A10 Formatter config is the authority | [P] | House style. Epic mandates tabs (size 4) and the brace on its own line as written prose, and is silent on the toolchain entirely — where a config lives, whether a nested one shadows it, what an ignore list excludes, which formatter an IDE is pointed at. Nothing in the row is engine-, UHT-, or build-enforced; the one build-visible consequence nearby, a sorting formatter moving `*.generated.h` off last position, is A3's. Safe to adapt wholesale, and N/A outright for a project that runs no formatter. |
| C9 Cross-type reads via the owner's accessor | [G]/[U] | Encapsulation practice Epic does not legislate, so the general half is [P]-safe. The [U] half is mechanical rather than stylistic: reflection visibility and serialization are independent of the C++ access specifier, so a `UPROPERTY` needs no promotion to be edited or saved, and `AllowPrivateAccess` is the real metadata specifier for Blueprint read/write of a private member. |
| C10 Comment content by audience | [P] | House style, pairing with B5 and C1 on syntax and K1 on whether the line earns itself. Epic demands useful comments and offers no audience taxonomy. The `//~` engineer-only form the row routes to is real, and verified under C7. |
| D5 Case follows the name's audience | [G]/[P] | The boundary rule composing D1–D3 rather than a fourth case convention. Epic applies PascalCase throughout and so never meets the collision; the row exists because a house local knob does. Safe to adapt. |
| D6 Externally bound names are data | [G] | Not a style claim. A name something outside the compiler resolves by string is data, so renaming it without a migration is a data-loss path no build can see — engine-independent, holding for any serializer, script layer, config parser, or wire format. Epic is silent; the hazard is not. Its BREAKING placement follows the doc's own rules 1 and 3: not compile-caught, and owned here rather than delegated. |
| E4 Nesting depth budget | [P] | House style. Epic's standard sets **no** nesting limit and prescribes no flattening moves — silent here, not opposed. The default of `3`, the counting method, and the move catalog are this doc's answer and safe to renumber, though not to switch off, since E2's floor is what a project would otherwise fall below. Epic does mandate the braces that create the levels being counted (E1). |
| E5 Cache a repeated evaluation once | [G] | The general form of two rules the doc already carries: F1's resolve-a-weak-pointer-once, whose engine rationale is 5.8-verified, and L2's single-lookup idiom. The invalidation window is the same hazard C8 carves out, which is why the stale dereference delegates to the breaking hunt instead of inflating this row. Epic is silent on the general case. |
| E6 Cached-local declaration | [G]/[P] | Placement and const-ness are house style Epic does not legislate. The binding half reuses G4's copy-cost threshold rather than restating it, so it inherits G4's provenance and its one number moves in one place. The declare-at-top carve-out is [P] because some houses mandate that position. |
| M1 Access sections are role-defined | [P] | House style. Epic mandates no access-section content map, and B6's repeated-label allowance is this doc's too. |
| M2 Declaration order is category order | [P] | House style, and the order itself is a Project Profile slot rather than a value this doc ships — Epic prescribes no member order at all. The mirror half, definitions repeating the header, is general C++ practice Epic does not write down. |
| M3 A mirrored type keeps its counterpart's shape | [P] | House style. The cross-file counterpart to K8's intra-file rule; Epic is silent on both. |

### The three knobs where Epic and house style collide

Three rules **contradict** — not merely extend — Epic's written standard,
which is exactly why they live in the driver's profile as unfilled knobs
rather than as rows carrying a value. Epic's answer and the common house
answer are both below. Pick one per project:

1. **Indentation** — Epic: tabs (size 4). Common house answer: 4 spaces.
2. **Line length** — Epic: no limit. Common house answer: a cap around 120 to 150 characters.
3. **Local-variable case** — Epic: PascalCase everywhere, no local exception. Common house answer: `lowerCamelCase` for locals.

Neither answer is wrong, and house standards routinely depart from Epic
here. What would be wrong is shipping either one as a silent default, since
this doc travels to projects that aren't Unreal and aren't Epic's.

### Sources

- Epic Games — *The Epic C++ Coding Standard for Unreal Engine* (official): https://dev.epicgames.com/documentation/en-us/unreal-engine/epic-cplusplus-coding-standard-for-unreal-engine
- Epic Games — *Object Pointers in Unreal Engine* (`TObjectPtr`): https://dev.epicgames.com/documentation/en-us/unreal-engine/object-pointers-in-unreal-engine
- Epic Games — *UE5 Migration Guide* (`TObjectPtr` recommendation): https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-5-migration-guide
- Microsoft — *x64 calling convention* (register rule behind C8/G4): https://learn.microsoft.com/en-us/cpp/build/x64-calling-convention
- UE 5.8 engine source — the A6/C4/C6/C7/C8/F1/G4/L1/L2 mechanics were verified against `Engine/Source` in the 5.8 tree during the 2026-07 conventions work (`WeakObjectPtr.cpp`, `GarbageCollection.cpp`, `Build.h`, `SparseSet.h.inl`, `Property.cpp`, `UhtPropertyParser.cs`, `UhtParsingScope.cs`, `Unity.cs`)
- Epic Games — *Metadata Specifiers* (`DisplayName`, `ToolTip`): https://dev.epicgames.com/documentation/en-us/unreal-engine/metadata-specifiers-in-unreal-engine
- Epic Games — *Class Specifiers* (`HideCategories`): https://dev.epicgames.com/documentation/en-us/unreal-engine/class-specifiers
- Epic Developer Community — "*.generated.h should always be the last #include*": https://forums.unrealengine.com/t/the-generated-h-file-should-always-be-the-last-include-in-a-header-why-is-that/1904506
- Epic Developer Community — "*Is IsValid() meant to always be used instead of a nullptr check?*": https://forums.unrealengine.com/t/is-unreals-isvalid-meant-to-always-be-used-instead-of-a-c-nullptr-check-or-is-it-optional-based-on-the-situation/465056
- Tom Looman — *Unreal Engine C++ Complete Guide*: https://tomlooman.com/unreal-engine-cpp-guide/
- Laura (landelare) — *Unreal C++ speedrun*: https://landelare.github.io/2023/01/07/cpp-speedrun.html
- Unreal Garden — *All UCLASS / UPROPERTY Specifiers*: https://unreal-garden.com/docs/uclass/
- Jonas Reich — *Open Unreal Conventions*: https://jonasreich.github.io/OpenUnrealConventions/C++/
- *The Readability Spectrum: Patterns, Issues, and Prompt Effects in LLM-Generated Code* (K1/K5/K7/K8 measurements): https://arxiv.org/abs/2605.13280
- Baltes, Cheong & Treude — *"An Endless Stream of AI Slop"* (reviewer detection markers — A9/K2/K9): https://arxiv.org/abs/2603.27249
- Bohr — *Show and Tell: Prompt Strategies for Style Control in Multi-Turn LLM Code Generation* (K4 defensive ratio): https://arxiv.org/abs/2511.13972
- *Code Fingerprints: Disentangled Attribution of LLM-Generated Code* (K7 identifier-length signature): https://arxiv.org/abs/2603.04212
- GitHub Blog — *Agent pull requests are everywhere. Here's how to review them* (K6 reuse blindness): https://github.blog/ai-and-ml/generative-ai/agent-pull-requests-are-everywhere-heres-how-to-review-them/
- Jose Casanova — *AI Code Slop Reviewer* prompt (K8 practitioner form): https://www.josecasanova.com/prompts/ai-code-slop-reviewer

## Report

Report through the driver's template (`../SKILL.md § Report`); the
profile/selector slot on the `Standards:` line is this doc's **Engine**
value. All rows — including section J's custom-engine detail — count toward
the one `Checklist:` PASS / FAIL / N/A tally. That tally is a coverage
count, not a findings list: each **FAIL** is *also* filed under the
BREAKING, PRACTICE, or CONVENTION heading § Severity map assigns its row,
and the `Findings:` counts on the driver's top line are those three, not
this tally.

## Hard rules (this doc's additions)

The driver's hard rules apply as written (breaking first, exhaustive not
sampled, resolve the Profile first, don't guess, reproduce before you file,
tiering). Two of those bind hardest here. **Tiering is split**: walking this
checklist is mechanical enough for a Cheap tier, and the driver's breaking
hunt over the same files is not — that half takes at least a Mid tier, and
Opus-or-comparable when the diff was Sonnet- or Opus-authored, matching
`cpp-gamedev-check.md`'s own verifier floor. **Reproduce before you file**:
a BREAKING row names the input or path that triggers the failure. On top:

- **Set the Engine.** Left alone it's `vanilla`, so every [U] and [C] row
  is N/A — say so in the report rather than inferring `unreal` from
  `UCLASS`/`GENERATED_BODY` in the diff. If another token above is unset,
  its rows are N/A too — never invent a prefix, company, or engine choice.
- **Don't change [U] rules to taste.** They're engine- or build-enforced.
  Overriding them breaks compilation or the reflection system. Adapt [P]
  rows to house style instead.
- **A conventions pass changes form, not behavior.** Where the change's
  stated goal is form — a conventions pass, a formatting sweep, a naming
  cleanup — form is whitespace, brace and line breaking, declaration and
  definition order, regrouping under repeated same-access labels (B6),
  comment text, and the case of unbound names. These are not: a changed
  default or initial value, an added or removed exposed-configuration
  field, a rewritten condition, a declaration moved to a different access
  level. Check by diffing every default literal and every exposed,
  serialized, or reflected declaration against the pre-change revision
  rather than reading the new file for reasonableness — a *better* default
  is still a behavior change. Behavior work asked for alongside the pass is
  filed under its own rows and stays a separate change, never folded in. On
  any other change this rule is N/A, and D6 runs regardless.
- **Rows outside the active profile are N/A, not deleted.** A
  `custom`-profile review marks every [U] row N/A; an `unreal`-profile
  review marks every [C] row N/A. [G] and applicable [P] rows always apply.

## Changelog / edge-case log

Moved to [the repo's commit log](https://github.com/defessler/smartplan/commits/main) to keep this doc lean and out of the shipped plugin.
