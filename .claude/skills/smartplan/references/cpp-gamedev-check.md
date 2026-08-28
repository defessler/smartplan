# C++ gamedev correctness (smartcheck's gamedev layer)

*Companion to `check.md` (same directory) — the rubric that file's "C++
gamedev leaves" section dispatches to. Implements
`docs/cpp-gamedev-contracts.md` Surface B (the six-category taxonomy),
gated on Surface A (Engine Profile).*

You are auditing **one leaf's diff** for C++ gamedev correctness bugs — the
class of defect a "does it look done" pass or a scripted acceptance check
cannot see. Not the generic accept/scope protocol (that's `check.md`) —
this is the layer that makes a cheap tier's DONE **safe** on gamedev code.
Run it alongside `check.md`'s protocol, never standalone.

**This file is the source of truth for the six categories below.**
`smartreview` consumes them: its standards doc maps each checklist row onto
a category and hunts the same six across a whole fileset at the merge gate,
rendering a report. This layer is diff-scoped over one leaf, inside the
fan-out, and renders no verdict. Same taxonomy, two seats — one leaf's
diff before the orchestrator accepts it is here, a changelist before it
merges is there. Edit the taxonomy **here only**.

**Verifier tier.** Several rows here (atomic memory-order, strict-aliasing/
alignment, ownership judgment) need systems-level C++ judgment, not a scripted
match — run this layer on **at least a Mid (Sonnet) verifier**, never a
Cheap one, and per `check.md` § Tiering the floor tracks the executor:
a Sonnet- or Opus-authored gamedev diff gets this layer at
**Opus-or-comparable** strength. That's consistent with `check.md`'s
tiering: a Cheap verifier is only safe where a check is fully scripted with
zero judgment, which several rows here are not — and these categories are
exactly the shared-blind-spot domains where the verifier-catchability
guardrail already refuses to floor low.

**On Copilot, get that strength cost-consciously.** The "Opus-or-comparable"
strength this layer needs comes from the cross-family
verifier — **Gemini 3.6 Flash** (0.75/3.75; T18 measured 3.1 Pro, T34
cleared this successor at 8/8 before Copilot retired it 2026-09-01) or
GPT-5.6 Terra — per
`check.md` § Family decorrelation. That call now rests on **cost and
decorrelation, not on the gate**: T30 (2026-07-25) saw Opus 4.8 and 5 serve
on an account that refused 4.8 on 07-11, so treat the Pro+/Max gate as the
base expectation to verify rather than a fact. Gemini still wins here on
price (T18: ties Terra at 47% the cost) and on decorrelating exactly these
categories. What has NOT changed: never accept an Opus pin that silently
degrades to Sonnet-judging-Sonnet. For
these six shared-blind-spot categories, family decorrelation is worth more
than the last few benchmark points, so the cheaper decorrelated judge is the
right default on a UE5 gameplay leaf — not the priciest same-goal one.

## Engine Profile gate

The leaf's Engine Profile (`vanilla` default · `custom` · `unreal` —
canonical definition: the `smartreview` skill's
`cpp-review-standards.md` § Project Profile, per
`docs/cpp-gamedev-contracts.md` Surface A) arrives in
the brief. Every check below is tagged:

- **[G]** general C++ gamedev — apply in **all** profiles, always.
- **[U]** Unreal-only — apply **iff** `profile=unreal`.
- **[C]** custom-engine — apply **iff** `profile=custom`.

Brief silent on Engine Profile → default `vanilla`, apply only [G] checks,
and note the assumed default in your report. If the diff's own code
contradicts the stated (or assumed) profile — e.g. `UCLASS`/
`GENERATED_BODY` shows up under `vanilla`/`custom` — flag the mismatch as
a note; don't silently reclassify and don't guess a profile the brief
never stated.

## Protocol

1. Read the Engine Profile off the brief (default per above).
2. Walk the six categories below against the lines the diff adds or
   changes. Read the surrounding function/class/header for context when
   judging ownership, threading, or lifetime — but don't go hunting for
   preexisting bugs outside what the diff touches or makes newly
   reachable; that's a different leaf's problem.
3. Gate each category's [U]/[C] rows by the resolved profile; [G] rows
   always run.
4. File every real finding as `category · file:line · what's wrong · fix`
   (use the exact category name from the six headings below).
5. Sort findings by **Severity** (below). Blocking findings become
   `check.md` FAIL reasons (tag: CHANGE); non-blocking ones become PASS
   notes.

## 1. Ownership & lifetime

| Tag | What the verifier inspects |
|---|---|
| [G] | A member is a raw pointer that owns a heap allocation, with no RAII wrapper and no comment that *justifies* the raw-owning exception (a comment merely describing the allocation doesn't count). |
| [G] | A pointer or reference is dereferenced with no null/validity check on a path where it can be null (an out-param, a `Find`/lookup result, a `dynamic_cast`/`Cast`, an optional-returning API) and no documented non-null invariant. **[G] null-safety floor** — the `[U]` GC row below is Unreal-specific and does NOT cover plain null derefs under `vanilla`/`custom`. |
| [G] | A moved-from object (`std::move(x)` then `x` used again) read again in the same scope. |
| [G] | A pointer/reference to a local or temporary stored or returned beyond that local's/temporary's scope (dangling reference), including a lambda capturing by reference and outliving the stack frame. |
| [G] | Two members/systems both act as owner of the same resource with no arbitration comment (dual/unclear ownership). |
| [G] | An iterator/pointer/reference into a container held across an insert/erase/reallocation of that container. |
| [G] | A self-referential pointer/iterator (points into `this`) on a type moved or copied without a user-defined move/copy that fixes it up. |
| [U] | A `UObject*`/engine-object raw pointer stored as a class member with no ownership comment and no `TObjectPtr`/`TWeakObjectPtr` — GC can free it out from under the raw pointer. |
| [C] | A resource referenced as a raw pointer into an engine-owned pool/array where the project's convention is a handle (index + generation) — a raw pointer survives a pool free/reallocation, the handle wouldn't. |

**Example finding:** `Ownership & lifetime · Enemy.cpp:142 · AIController stored as a raw AController* member, no ownership note · TWeakObjectPtr<AController> + IsValid() before use`

## 2. Undefined behavior

| Tag | What the verifier inspects |
|---|---|
| [G] | `reinterpret_cast` or a union between unrelated types instead of `memcpy`/`std::bit_cast` (strict-aliasing violation). |
| [G] | A buffer cast to a stricter-alignment type (`char*` → `float*`/SIMD) with no alignment guarantee on the source. |
| [G] | Signed arithmetic that can overflow near a range boundary, or an implicit narrowing conversion (`size_t`→`int`, `float`→`int`) that can truncate. |
| [G] | A variable or struct field read on a path where it hasn't been initialized yet. |
| [G] | A `string_view`/`span`/`FStringView` bound to a temporary that's destroyed before the view is used. |
| [G] | An object touched after its lifetime ends — a returned reference to a stack local, use-after-`delete`, use after Unreal GC/`BeginDestroy`. |

**Example finding:** `Undefined behavior · PacketCodec.cpp:58 · reinterpret_cast<float*> on a byte buffer with no alignment guarantee · memcpy into a local float, or std::bit_cast`

## 3. Performance hot-path

| Tag | What the verifier inspects |
|---|---|
| [G] | Heap allocation (`new`, `make_shared`, vector/`TArray` growth, string concatenation) inside a per-frame function or an inner loop over many entities. |
| [G] | A virtual call or `std::function`/delegate dispatch inside a tight loop where the concrete type is knowable at the call site. |
| [G] | Pass-by-value, or a container `push_back`/`Add`, copying a non-trivial type where a move or `const&` would do. |
| [G] | A hot loop touching one or two fields of a large AoS struct where the access pattern is SoA-shaped. |
| [G] | A `shared_ptr` copied (not referenced) across a per-frame boundary with no actual ownership transfer, churning the refcount. |
| [G] | Logging, string formatting, or debug-only work on a hot path with no build-config guard. |

**Example finding:** `Performance hot-path · ParticleSystem.cpp:210 · new FParticleData per particle inside the per-frame update loop · pool and reuse particle structs; allocate once outside the loop`

## 4. Threading model

| Tag | What the verifier inspects |
|---|---|
| [G] | Shared mutable state (a member, a global, a cache) written from more than one thread with no lock/atomic. |
| [G] | Game-thread-only state (UObject mutation, actor transform) touched from a render/RHI thread or a job/task-pool thread. |
| [G] | An atomic memory order that doesn't match the invariant it protects (e.g. `relaxed` guarding a pointer publish/consume), or a non-atomic access racing an atomic write to the same location. |
| [G] | A blocking call (contended mutex, file I/O, synchronous asset/network load, `sleep`) on a worker/job thread, or on the game thread's per-frame path. |
| [G] | A lambda/task captured by reference and queued onto another thread, referencing an object with no guaranteed-outlives-the-task lifetime. |
| [G] | A lazy-init singleton or double-checked-locking pattern without the atomic/once guard that makes it correct under real thread scheduling. |

**Example finding:** `Threading model · InventorySystem.cpp:77 · ItemCache map written from the loot-generation job thread with no lock, read on the game thread · guard both sides with InventoryMutex, or route the write through a queued game-thread command`

## 5. Build & header hygiene

| Tag | What the verifier inspects |
|---|---|
| [G] | A header includes something only used in the `.cpp` (IWYU violation), or relies on a symbol pulled in transitively rather than including it directly. |
| [G] | A full type definition included where a forward declaration (pointer/reference use only) would do. |
| [G] | A heavy header (container/algorithm/engine-subsystem) pulled into a widely-included header instead of the `.cpp`, or instead of a lighter forward-decl. |
| [G] | A non-`inline` function or variable defined in a header, risking an ODR violation across translation units. |
| [G] | A stable, widely-used header added as a per-file include sweep instead of going through the project's PCH. |
| [U] | `*.generated.h` is not the **last** include in the header. |
| [C] | An engine/module-layer header pulled into a lower architectural layer that shouldn't depend on it. |

**Example finding:** `Build & header hygiene · Weapon.h:12 · Weapon.generated.h included before ProjectileType.h, not last · move Weapon.generated.h to the final include (unreal profile requirement)`

## 6. Determinism & serialization

| Tag | What the verifier inspects |
|---|---|
| [G] | Sim-affecting logic reads variable `DeltaTime` directly instead of accumulating into a fixed timestep, where the project needs determinism. |
| [G] | A float computed via a platform-varying path (SIMD intrinsic, fastmath, transcendental function) with no bit-identical guarantee across the sim's target platforms. |
| [G] | A save/replay format change (new, reordered, or retyped field) with no version tag and no upgrade path for old data. |
| [G] | A `static`/singleton initialized once at startup with no re-init path, so it goes stale or double-inits across a hot-reload. |
| [G] | Non-deterministic container iteration order (`unordered_map`/`TSet`) feeding a result that's saved, replayed, or must match across clients. |
| [G] | A random source not seeded/streamed per the project's determinism contract (global `rand()` instead of a seeded per-instance RNG). |

**Example finding:** `Determinism & serialization · SaveGame.cpp:34 · added PlayerLevel field to the save struct, no version bump or migration · bump SAVE_VERSION, add a migration branch for old saves`

## Severity — what blocks

- **Always blocking (→ FAIL):** any diff-introduced finding in Ownership &
  lifetime, Undefined behavior, or Threading model. These are bugs, not
  style — a cheap executor's "looks done" must not survive one of
  these.
- **Blocking only in context (→ FAIL if the touched code is genuinely
  hot/critical, else a PASS note):** Performance hot-path findings block
  when the code is per-frame or inner-loop (per the brief's CONVENTIONS
  exemplar, or an existing hot-path marker/comment); a one-time or
  cold-path allocation is a note. Determinism & serialization findings
  block when the system is sim-, replay-, or save-critical; editor-only or
  debug-only paths are a note.
- **Blocking only if build-breaking (→ FAIL if it would fail to compile or
  violates ODR, else a PASS note):** Build & header hygiene findings — a
  wrong `generated.h` position or a real ODR violation blocks; a bare
  IWYU/forward-decl nit is a note unless the brief's CONVENTIONS calls out
  header hygiene as in-scope.

## Report

Produce this block before handing off to `check.md`'s verdict:

```
C++ GAMEDEV CORRECTNESS: <leaf name>
Engine Profile: vanilla | custom | unreal  (stated in brief | assumed default)
Findings:
  - <category> · <file:line> · <what's wrong> · <fix>   [BLOCKING | note]
  - ...
Clean categories: <the six minus whichever produced findings, or "all six">
```

Fold **BLOCKING** rows into `check.md`'s FAIL **Reasons** (tag: CHANGE) and
**Evidence**; fold **note** rows into the PASS **Notes** line. Zero
findings is itself evidence — say so, don't just omit the block.

## Hard rules

- **Diff-scoped.** Judge lines the leaf added or changed, plus the minimum
  surrounding context needed to judge ownership/threading/lifetime. A
  preexisting bug the diff didn't touch and didn't make newly reachable is
  not this leaf's finding.
- **Don't guess the profile.** Brief silent → `vanilla`, [G]-only, note the
  default. Don't infer `unreal`/`custom` from cosmetic cues; a code/brief
  mismatch is a note, not a silent reclassification.
- **One bug, one finding — except across always-blocking categories.** A
  defect spanning two categories files once, under the more severe, with the
  overlap named in "what's wrong." *But* when one defect is simultaneously in
  two-or-more **always-blocking** categories (e.g. a line that both overflows
  (UB) and races (Threading)), don't force a pick — file it under each
  applicable always-blocking category. The FAIL is identical either way, and
  the fix needs both angles.
- **No verdict here.** This file has no PASS/FAIL of its own — findings
  feed `check.md`'s verdict (see that file's "C++ gamedev leaves" section).
- **Not a style pass.** Naming, formatting, comment style — that's
  `smartreview`. Everything here is a correctness defect, not a taste call.
  The reverse no longer holds: `smartreview` reports correctness too, under
  its own BREAKING band, sourced from this file's categories. When both
  seats run over the same code, a finding already filed by a leaf's verify
  is marked already-filed there rather than raised twice — they collate on
  `category · file:line`.
- **Context-dependent rows need project context.** The PCH-discipline row
  (cat 5) and the `[C]` layering row (cat 5) can't be judged from a diff
  alone — apply them only when the brief supplies the PCH manifest / module
  dependency graph; absent that, skip, don't guess.

## Pitfall catalog — VERIFY FIRST source

**For smartbrief, not the verifier.** When compiling a C++ gamedev leaf's
brief, `brief.md` rule 9 draws its ONE flagged verify-first fact from this
list — the profile-relevant pitfall most likely to bite that leaf, not a
scan of all six categories. Each pitfall is the brief-writer's condensed
form of a verifier row in the matching category table above (same six
category names, same [G]/[U]/[C] profile gates) — one taxonomy, one home.

- **Ownership & lifetime** — [G] raw owning pointer with no RAII owner ·
  [G] use-after-move · [G] iterator/reference held across a reallocating
  container op · [U] `UObject*` member with no `UPROPERTY()`/`TObjectPtr`
  (GC can collect it).
- **Undefined behavior** — [G] signed overflow in index/size arithmetic ·
  [G] `reinterpret_cast` type-punning (strict aliasing) · [G] dangling
  `string_view`/`span` outliving its buffer · [G] uninitialized POD passed
  to a zero-init-assuming system.
- **Performance hot-path** — [G] heap allocation inside a per-frame/inner
  loop · [G] missing move / pass-by-value copy of a large object · [G]
  virtual dispatch in a tight loop where static would do · [C] AoS layout
  on a hot path that's SoA-shaped.
- **Threading model** — [G] shared/game state written from a worker thread
  without an owning-thread handoff · [G] blocking call on a
  must-not-block thread · [G] atomic with the wrong memory order.
- **Build & header hygiene** — [G] compiles only via a transitive include
  (no IWYU) · [G] full type included where a forward declaration would do ·
  [U] `*.generated.h` not last in the include block.
- **Determinism & serialization** — [G] sim step reading wall-clock or an
  unseeded RNG · [G] save/replay format with no version field · [C]
  hot-reload-unsafe static/singleton.

## Changelog / edge-case log

History: in [the repo's commit log](https://github.com/defessler/smartplan/commits/main).
