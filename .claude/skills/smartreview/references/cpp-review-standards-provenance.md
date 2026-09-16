# smartreview — C++ standards provenance (Epic-standard validation and sources)

This file holds the validation matrix and sources for `cpp-review-standards.md`, and it is not loaded at review time. A reviewer who needs to know whether a rule is Epic-mandated or house style looks here.

## Provenance & Epic-standard validation

Every rule in `cpp-review-standards.md` was checked against Epic's
**official** C++ Coding Standard for Unreal Engine and corroborating
community references, rule by rule. **The tag in THIS matrix is the
Epic-mandate axis, deliberately not the checklist's profile-gating tag:**
here **[U]** means engine/Epic-mandated, enforced by the engine,
UnrealHeaderTool, or Epic's written standard. Overriding it breaks the
build, the reflection system, or conformance with the engine standard (a
**[U]** rule can still carry a project *value* — e.g. the copyright
*text* — the *rule* is canonical, the *value* goes in the Project Profile
in `cpp-review-standards.md`). **[P]** means Epic is silent, or the
project deliberately deviates — safe to adapt to house style. So a rule
can be all-profile in the checklist ([G]) yet Epic-mandated in its Unreal
expression ([U] here, e.g. A1/E1), or `unreal`-gated in the checklist yet
freely adaptable ([P] here, e.g. H1/I1–I3). Use this matrix to decide what
is safe to customize; use the checklist tag to know where a row is active.
The two columns are not expected to match.

### Validation matrix

| Rule | Tag | Verdict vs Epic standard |
|------|-----|--------------------------|
| A1 Copyright first line | [U] | **Confirmed.** Epic: a copyright notice must be the first line of any distributed source file. CI fails otherwise. Text is project-specific → `{{COMPANY}}`. |
| A2 Full module-rooted includes | [U] | **Confirmed** (fine-grained, IWYU). Alphabetical sorting within groups is a [P] house nicety Epic doesn't mandate. |
| A3 IWYU + forward-declare + `.generated.h` last | [U] | **Confirmed.** Epic: forward declarations preferred, include everything you use, don't rely on transitive includes. `*.generated.h` **must** be the last include — a hard UnrealHeaderTool build rule. |
| **A4 Indentation** | [P] | **Epic and house style collide here.** Epic mandates **tabs, size 4**. The driver's **Indentation** knob ships unfilled — set it to Epic's value or to your own, and the row is N/A until you do. |
| **A5 Line length** | [P] | **Epic and house style collide here.** Epic sets **no** line-length limit. The driver's **Max line length** knob ships unfilled — set it to `none` for Epic, or to a house cap (e.g. 150 chars). |
| A6 No anonymous namespaces (named file-unique namespace + `static`) | [P] | Epic is silent: it bans namespaces around `UCLASS`/`USTRUCT` (UHT) and steers non-UObject APIs into `UE::`, but doesn't forbid anonymous namespaces outright. Not a style claim, though. Unity builds concatenate `.cpp` files into one translation unit and collapse every anonymous namespace into one, giving cross-file ODR collisions that pass local builds and only surface in CI and Shipping (verified vs `Unity.cs`, 5.8), which is why the checklist files it BREAKING. |
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
| G1 UFUNCTION decoration | [U]/[P] | `BlueprintPure`/`BlueprintCallable` are real specifiers and the decoration policy is project-specific [P]. **`AddUObject` does not need `UFUNCTION`:** only `AddDynamic` binds by name through reflection, so only it requires the macro [U]. No `Category` policy is mandated here. |
| G2 Trivial getters inline | [P] | Common house style. |
| G3 Reference-return safety | [U] | **Confirmed.** Epic: **never** `const` on a return type (inhibits move semantics); return `const T&` only for stable-lifetime references, else by value. |
| H1 Log category macro | [P] | `DEFINE_LOG_CATEGORY_STATIC` / `DECLARE_LOG_CATEGORY_EXTERN` are real. The category *name* is project-specific → `{{LOG}}`. |
| H2 Message format | [P] | House logging format. |
| I1–I3 Architecture patterns | [P] | Sound, general UE patterns (data-asset/actor split, `FGuid` references, self-registration). Not project-specific, but "if applicable." |
| A9 No emoji / decorative Unicode | [P] | Practitioner-attested generation tell ("if the comment has an emoji it's a guarantee" — reviewer study, arXiv 2603.27249) plus the real MSVC codepage risk. Epic is silent; the strict-ASCII tightening is [P] house style. |
| B7 Reflection earns its macro | [U] | Every reflected symbol emits registration code into `.gen.cpp` that compiles into every configuration and constructs `FProperty`/`UFunction` objects at module load; a stray macro also asserts a consumer contract that doesn't exist. The inverse (missing reflection) is C4/G1 correctness. Verified against the UE 5.8 source during the 2026-07 conventions work. |
| C6 Transient | [U] | `CPF_Transient` skips persistent serialization *except when serializing defaults* (`Property.cpp`, 5.8) — the Blueprint-CDO edge is real; `Transient`+`Visible*` runtime inspection is the engine's own pattern (`Actor.h`, `CharacterMovementComponent.h`). |
| C7 Comment-as-tooltip | [U]/[P] | UHT's comment→ToolTip pipeline verified vs `UhtParsingScope.cs` (5.8): blank-line block discard, `/** */`-then-`//` merge, `//~` exclusion. The prefer-comment-over-meta half is [P] house preference. |
| C8 Handles over cross-system raw pointers | [P] | The engine's own shape: `FWeakObjectPtr` pairs `ObjectIndex` + `ObjectSerialNumber` (`WeakObjectPtr.h`), `FMassEntityHandle` static_asserts `sizeof == 8`, `FTimerHandle` bit-packs into one `uint64`. Register rule (1/2/4/8B trivially copyable) per Microsoft's x64 calling-convention docs. Honest pitch: safer everywhere, faster only where a system owns pooled storage and iterates in bulk. |
| F1 Match the check to the pointer type | [U] | Rewritten 2026-07 from "IsValid everywhere": `IsValid()` matches *strong* members (the Destroy()→next-GC-pass window, `KillReference` in `GarbageCollection.cpp`); `TWeakObjectPtr::Get()` already runs the identical flag+serial test, so `IsValid()`-then-`Get()` resolves twice — the engine deletes `operator bool` with a comment saying exactly this ("use Get() once in a function"). The structurally-guaranteed-lifetime carve-out (`ensure(IsValid(X))`) keeps invariant violations loud. |
| G4 Parameter passing | [P]/[U] | Epic mandates `const` on unmodified reference params and blesses the by-value+`MoveTemp` sink verbatim (its own `SetMemberArray` example). The 16-byte threshold is this doc's addition: MSVC x64 registers only 1/2/4/8B trivially copyable args and copies either way at 9–16B; SysV passes ≤16B in register pairs — never meaningfully worse on MSVC, strictly better elsewhere. The BlueprintCallable output-pin trap verified vs `UhtPropertyParser.cs` (5.8). LWC sizes per `MathFwd.h`/`TransformVectorized.h`. |
| L1 No unchecked `operator[]` | [P] | `TMap::operator[]` = `FindChecked`, `TArray::operator[]` = `RangeCheck`, both `check()`-implemented; `DO_CHECK` compiles to 0 in Test/Shipping (`USE_CHECKS_IN_SHIPPING` defaults 0, `Build.h` 5.8). Epic's written standard is silent, so [P] on this axis. A correctness hazard, not taste — treated as non-negotiable. |
| L2 Find over Contains-then-[] | [P] | `Contains` and `Find` bottom out in the same `FindIndexByHash` walk (`SparseSet.h.inl`) — the second pass adds no safety; the `[]` half is L1's unchecked access. Epic is silent, so [P] on this axis. Correctness carries the rule; the perf saving is small in cold code. |
| L3 Engine types at engine seams | [U] | Epic verbatim: "Standard containers and strings should be avoided except in interop code"; explicit-width types mandated in serialized/replicated formats; plain `int` legal "when the integer width is unimportant" — the row scopes the flag accordingly. UHT rejecting std types on reflected members is mechanical, not opinion. |
| L4 Explicit types over auto | [U]/[P] | Epic verbatim: "You shouldn't use auto in C++ code, except for the few exceptions listed below" + the qualify-auto rider. The same-line-type extension (`Cast<T>`, `NewObject<T>`) is [P] house. The `TObjectPtr` deduction trap and the range-for `TPair` copy are 5.8-verified behaviors. |
| J1–J6 Custom-engine architecture | [P] | Epic silent by construction: house architecture for a bespoke engine. Safe to adapt wholesale. |
| K1–K10 Machine-generation tells | [P]/[U] | House/practitioner rows; Epic mostly silent, so all safe to adapt — except K1, which Epic's standard itself demands ("Write useful comments"; `// increment Leaves` is Epic's own bad example), and K4's exceptions-off clause, which UBT enforces (`bEnableExceptions = false`; packaged builds reject `throw`). Measured backing per row: K1 redundant comments are the dominant measured LLM readability issue and K5 Excessive Complexity the top category (arXiv 2605.13280); K2 conversation-context leakage and K9's "verbose style" are reviewer-study detection markers (arXiv 2603.27249); K3 placeholder scaffolding (practitioner slop guides); K4 defensive-ratio divergence from human baselines (arXiv 2511.13972); K6 code-reuse blindness (GitHub agent-PR review guide) + measured intra-repo clones; K7 Redundant Variables is a novel LLM-specific pattern while Poor Naming counts are human/LLM parity — redundancy, not naming quality, is the generation-specific risk — and identifier length is model signature (arXiv 2603.04212), hence the length protection; K8 overblanking (arXiv 2605.13280) + match-the-file practitioner guidance. K10 extends K1's and K2's axis from comments to the prose a change ships, and carries no measurement of its own. |
| A10 Formatter config is the authority | [P] | House style. Epic mandates tabs (size 4) and the brace on its own line as written prose, and is silent on the toolchain entirely — where a config lives, whether a nested one shadows it, what an ignore list excludes, which formatter an IDE is pointed at. Nothing in the row is engine-, UHT-, or build-enforced; the one build-visible consequence nearby, a sorting formatter moving `*.generated.h` off last position, is A3's. Safe to adapt wholesale, and N/A outright for a project that runs no formatter. |
| C9 Cross-type reads via the owner's accessor | [P]/[U] | Encapsulation practice Epic does not legislate, so the general half is [P]-safe. The [U] half is mechanical rather than stylistic: reflection visibility and serialization are independent of the C++ access specifier, so a `UPROPERTY` needs no promotion to be edited or saved, and `AllowPrivateAccess` is the real metadata specifier for Blueprint read/write of a private member. |
| C10 Comment content by audience | [P] | House style, pairing with B5 and C1 on syntax and K1 on whether the line earns itself. Epic demands useful comments and offers no audience taxonomy. The `//~` engineer-only form the row routes to is real, and verified under C7. |
| D5 Case follows the name's audience | [P] | The boundary rule composing D1–D3 rather than a fourth case convention. Epic applies PascalCase throughout and so never meets the collision; the row exists because a house local knob does. Safe to adapt. |
| D6 Externally bound names are data | [P] | Not a style claim. A name something outside the compiler resolves by string is data, so renaming it without a migration is a data-loss path no build can see — engine-independent, holding for any serializer, script layer, config parser, or wire format. Epic is silent; the hazard is not. [P] marks Epic's silence, not permission to rename without a migration. Its BREAKING placement follows the doc's own rules 1 and 3: not compile-caught, and owned here rather than delegated. |
| E4 Nesting depth budget | [P] | House style. Epic's standard sets **no** nesting limit and prescribes no flattening moves — silent here, not opposed. The default of `3`, the counting method, and the move catalog are this doc's answer and safe to renumber, though not to switch off, since E2's floor is what a project would otherwise fall below. Epic does mandate the braces that create the levels being counted (E1). |
| E5 Cache a repeated evaluation once | [P] | The general form of two rules the doc already carries: F1's resolve-a-weak-pointer-once, whose engine rationale is 5.8-verified, and L2's single-lookup idiom. The invalidation window is the same hazard C8 carves out, which is why the stale dereference delegates to the breaking hunt instead of inflating this row. Epic is silent on the general case. |
| E6 Cached-local declaration | [P] | Placement and const-ness are house style Epic does not legislate. The binding half reuses G4's copy-cost threshold rather than restating it, so it inherits G4's provenance and its one number moves in one place. The declare-at-top carve-out is [P] because some houses mandate that position. |
| M1 Access sections are role-defined | [P] | House style. Epic mandates no access-section content map, and B6's repeated-label allowance is this doc's too. |
| M2 Declaration order is category order | [P] | House style, and the order itself is a Project Profile slot rather than a value this doc ships — Epic prescribes no member order at all. The mirror half, definitions repeating the header, is general C++ practice Epic does not write down. |
| M3 A mirrored type keeps its counterpart's shape | [P] | House style. The cross-file counterpart to K8's intra-file rule; Epic is silent on both. |

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

