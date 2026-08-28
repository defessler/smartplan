# C++ gamedev reorientation — frozen contracts (Phase 0)

Frozen surfaces for the reorientation fan-out.
**Every leaf cites this.** Do not restate these definitions in the skills —
reference them and implement to them, so the Engine Profile and the correctness
taxonomy read identically everywhere.

> **Amendment 2026-07-09 (v3.0.0):** `smartstyle` was generalized and renamed
> to `smartreview`. Surface A's canonical Engine-Profile home is now
> **`smartreview/references/cpp-review-standards.md` § Project Profile** —
> read every "`smartstyle`'s Project Profile" below as that path. The
> selector values, rule tags, and Surface B taxonomy are unchanged; the
> frozen text below is kept as written for the record.

> **Amendment 2026-08-21 (v4.103.0):** Surface B's taxonomy is still frozen
> and still has exactly one author, `cpp-gamedev-check.md`. What changed is
> that it now has **two consumers**. `smartreview` reports in three ranked
> categories (BREAKING, PRACTICE, CONVENTION) and sources BREAKING from
> these same six names, via a § Severity map in
> `cpp-review-standards.md` that places every checklist row. That is the
> shared-vocabulary intent below made load-bearing rather than a new
> taxonomy — the line above reading "Surface B taxonomy is unchanged" holds
> for the *definitions* and no longer holds for *who reads them*. The two
> seats stay distinguishable by scope: `cpp-gamedev-check.md` is
> diff-scoped over one leaf inside the fan-out and renders no verdict,
> `smartreview` is fileset-scoped at the merge gate. Findings from both
> collate on `category · file:line`, which is why that finding shape below
> is now a dedupe key and not only a format.

---

## Framing directive (binds EVERY leaf)

**C++ game development is the primary domain. Unreal Engine is ONE supported
profile — an addition, never the focus.** Wherever the plugin currently leads
with Unreal (the plugin/skill descriptions, `smartstyle`, README), **demote it**:
lead with general C++ gamedev + custom-engine; present Unreal as one selectable
profile among equals. **Do not remove Unreal support** — keep every existing
Unreal rule intact; just move it behind the `unreal` profile so it's no longer
the headline. A reader who does *not* use Unreal must never feel the tooling is
"for Unreal, adaptable to me" — it's "for C++ gamedev, Unreal included."

---

## Surface A — Engine Profile

One selector, defined canonically in **`smartstyle`'s Project Profile** (LB owns
that definition), passed per-leaf in the brief, and referenced by
`cpp-gamedev-check.md` (LC) and `brief.md` (LE):

| Profile | Meaning |
|---|---|
| `vanilla` *(default)* | Plain modern C++, no engine assumptions. |
| `custom` | A bespoke C++ engine: **no** reflection/UHT/`UCLASS`/`generated.h`; keeps general C++ + gamedev + engine-architecture conventions. |
| `unreal` | Unreal Engine: the existing Epic/Unreal rules apply **on top of** the general C++ rules. |

**Rule tags** (replace smartstyle's current `[U]`/`[P]` scheme):
- **`[G]` general C++ gamedev** — applies in **all** profiles. The bulk of the rules.
- **`[U]` Unreal-only** — active **iff** `profile=unreal`.
- **`[C]` custom-engine** — active **iff** `profile=custom` (engine-arch conventions).
- **`[P]` project choice** — configurable per project, any profile.

**`custom` profile — DROP** (Unreal-isms): `UCLASS`/`UObject`/`UPROPERTY`/`UFUNCTION`/`GENERATED_BODY`,
`*.generated.h` include-ordering, UHT, the module-rooted `"Module/…"` include
convention, the `UE::` namespace default, Unreal `DECLARE_LOG_CATEGORY`.
**KEEP** (general + `[C]`): RAII/ownership, header hygiene/IWYU, naming
consistency, const-correctness, plus the engine-arch rows — ECS/data-oriented
layout, handle-based resources, job/task systems, custom RTTI, versioned
serialization, hot-reload safety.

---

## Surface B — C++ gamedev correctness taxonomy (the `smartcheck` layer)

`cpp-gamedev-check.md` (LC) implements these six categories; `brief.md`'s
pitfall catalog (LE) and `smartstyle`'s `[G]` rows (LB) draw from the **same six
names** so the vocabulary is shared. Each finding: `category · file:line ·
what's wrong · fix`. Engine-specific checks gate on the Engine Profile.

1. **Ownership & lifetime** — raw vs smart pointer choice, RAII, use-after-move,
   dangling references, unclear/dual ownership, iterator/container invalidation,
   self-referential pointers surviving a move.
2. **Undefined behavior** — strict-aliasing violations, misalignment, signed
   overflow / narrowing, uninitialized reads, dangling `string_view`/span,
   out-of-lifetime access, `reinterpret_cast` punning.
3. **Performance hot-path** — heap allocation in per-frame/inner loops, virtual
   dispatch in tight loops, copies where a move/`const&` belongs, cache-hostile
   layout (AoS where SoA fits), needless `shared_ptr` refcount churn.
4. **Threading model** — data races, writes to shared state off the owning
   thread, game/render/job-thread boundary violations, atomics/memory-order
   misuse, blocking calls on a worker/job thread.
5. **Build & header hygiene** — IWYU (include what you use), forward-declare in
   headers, no reliance on transitive includes, compile-time cost (heavy headers
   in headers), PCH discipline, ODR/inline hazards. *(In `unreal`, adds the
   `generated.h`-last rule.)*
6. **Determinism & serialization** — fixed-timestep correctness, float-determinism
   hazards where the sim needs it, **versioned/backward-compatible** serialization
   (save/replay compat), hot-reload-safe statics/singletons.

---

## Naming (frozen — leaves create/reference exactly these)

- **`.claude/skills/smartplan/references/cpp-gamedev-check.md`** *(new, LC)* — the
  correctness rubric; `check.md` points at it for C++ gamedev leaves.
- **`.claude/skills/smartstyle/references/custom-engine-conventions.md`** *(new, LB)* —
  the `[C]` engine-arch conventions for the `custom` profile.
- Engine Profile canonical definition: **`smartstyle/SKILL.md` Project Profile**
  (LB extends it with the `Engine` selector + the `[G]/[U]/[C]/[P]` tag legend).
- New external facts → the development repo's claim ledger rows (LH), id'd + anchored if a skill
  asserts them load-bearingly.
