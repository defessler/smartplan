# Document Templates

Part of the [`smartvoice`](../SKILL.md) skill's keyed voice profile layer — not the generic `defaultvoice.md`, which is self-contained and ships no scaffolds. These are **optional scaffolds, not mandates**. When you are modifying or extending an existing document, prefer THAT document's own template: infer its structure, mirror its headings and section order, and write the author's voice into it rather than reshaping it to anything below. The skeletons here are starting points for **brand-new documents only**, and even then you should adapt them freely, adding, dropping, reordering, and renaming sections to fit what the page actually needs. `<...>` = fill in. *(Optional)* marks a section that is especially commonly skipped, but treat every section as opt-in by page need. The voice and formatting rules live in the resolved profile, the generic anti-AI-slop layer in [`../SKILL.md`](../SKILL.md), and [`terminology.md`](./terminology.md) covers terminology.

**`How To: <Feature>` tends to take one of three shapes, so pick by content depth, not the title:**
1. **Deep reference**: a deep nested data hierarchy (e.g. `<Feature>` -> `<Sub-Feature>` -> `<Setting>`). Usually uses `How does it work?`, often a TOC, and sometimes a Reference section.
2. **Tutorial**: a step-by-step build process. Usually uses `Core Concepts` + `Workflow: Step N`.
3. **Setup/config**: a lighter "configure this asset" page (e.g. a setup/config asset). Usually skips `How does it work?`, `Core Concepts`, the TOC, and the Reference section.

`Overview` first is about the only thing that stays constant. A `Debugger` section tends to show up whenever there is something to debug. Treat all of this as a habit, not a rule.

---

## Contents

- 1. How-To page: Deep reference variant
- 2. How-To page: Tutorial variant
- 3. How-To page: Setup/config variant
- 4. Design Spec
- 5. Documentation (landing) page

### 1. How-To page: Deep reference variant

A good starting point when the page **documents a deep, nested data hierarchy**. Title: `How To: <Feature>`.

```
How To: <Feature>

Other Pages                      ← (Optional) sibling-page link list; on a long reference page
                                    with a TOC, Other Pages co-occurs WITH the TOC
   <Exact Sibling Page Title>
   <Exact Sibling Page Title>

Table of Contents                ← (Optional) labeled TOC; on long pages, mirror the heading tree,
   Overview                          nested up to 4 levels, including per-setting leaf entries
   How does it work?
      <Group>
         <Sub-Group>
            <Setting>
   Debugger
   Reference

Overview
This page is meant as a quick reference on <X> and how to use it. This system is meant to <verb>...
You can check out an example asset to see some examples of how it works:
<project-path>/<area>/<asset>

How does it work?
<Concept paragraph naming the building blocks.>

   <Group Name>                  ← e.g. <Feature>
   <one-line intro>

      <Config Group Name>        ← e.g. <Feature> Configurations
      Check out the Reference section to see the options. The asset will have more options added
      over time so this list is not comprehensive. Opening the asset and reading the comments
      should give you information about any specific configuration that is available.

         <Setting Name>          ← own heading per setting (H4), nested to match data hierarchy
         <short paragraph; opener: "Currently used to..." / "This is where you configure..." />
           <Sub-property> - <description>      ← Term - description bullets
           <Sub-property> - <description>

   <Concept Name>                ← (Optional) CONCEPTUAL subsection inside How does it work?
   <concept paragraph naming what it is and why it matters>
   Note: <soft caveat, optionally closing with a we-voice improvement coda>

      How to <verb> a <thing>?   ← question-phrased sub-heading is house style here, not just FAQ
      There are two methods for <doing X>.

         <Method Name A>         ← one named sub-heading per method
         The first method is <...>.

         <Method Name B>
         The second method is <...>.

      How to <verb> a <thing>?   ← second question sub-heading
      <prose / bulleted ways>

Walkthrough                      ← (Optional) only for video-backed tutorials
These videos show how to set up <...>.
   <Video Sub-heading>

Debugger                         ← present when there is a debugger to document
This will change over time but you can find a basic debugger by pressing <key>.
   <View Name>                   ← one sub-heading per debug view
   <description>

Reference                        ← (Optional) place LAST when present
```

**Section openers:**
- Overview → `This page is meant as a quick reference on <X> and how to use it.`
- Config group intro → the verbatim incompleteness disclaimer above.
- Field heading body → `Currently used to...` / `This is where you configure how <X> will...` / `This lets you...`
- Conceptual subsection → concept paragraph, then `How to <verb> a <thing>?` + `There are two methods for...`.

A deep-reference page **may** end with an optional `Reference` / `Examples` section. If it contains code, put the code in a fenced block and introduce the block with a sentence.

---

### 2. How-To page: Tutorial variant

A good starting point when the page **teaches a build process step-by-step**. Title: `How To: <Feature>`. If you go this way, lean on one spine rather than blending it with the deep-reference or setup/config skeletons.

This variant's TOC is the **unlabeled** form: an outline list placed directly **under the `Overview` heading**, with the real Overview prose immediately below the outline. There is no `Table of Contents` label and no `Other Pages` block.

```
How To: <Feature>

Overview                                       ← single Overview heading carries BOTH outline + prose

   Overview                                    ← unlabeled outline (conventional; mirrors heading tree)
   Core Concepts
   Workflow: Creating a <Thing>
      Step 1: <...>
      Step 2: <...>
   Advanced Features
   Debugging & Tools
   Best Practices
   FAQ

<This framework is designed to help you <verb>...>   ← prose (state the capability plainly, skip "using a modular, data-driven approach" and similar flourishes)
   Check out an example asset for some examples.            ← indented soft aside

Core Concepts
To use this system, you need to understand <N> main building blocks:
  <Concept Name>: <short definition>            ← Concept: gloss bullets (note colon, not " - ")
  <Concept Name>: <short definition>

Workflow: Creating a <Thing>
Step 1: <Imperative title>
<Action paragraph.>

Step 2: <Imperative title>
<Lead sentence.>
1. <Label>: <explanation>                       ← numbered ONLY for ordered sub-actions
2. <Label>: <explanation>
3. (Optional) <Label>: <explanation>

Advanced Features                               ← (Optional)
   <Feature Name>
   <bulleted Term - description or prose>

Debugging & Tools                               ← present when there are debug tools (tutorial title)
The <component> includes built-in tools to help you visualize your setup before hitting Play:
  <Tool> - <description>

Best Practices                                  ← (Optional)
  <Imperative Tip Label>: <advice> (e.g., <example>).

FAQ                                             ← (Optional)
Q: <question or symptom>
  Check <...>.                                  ← indented fix bullets, no "A:" label
Q: <question or symptom>
  <fix>
```

**Section openers:**
- Overview → outline list, then `This framework is designed to help you <verb>...`
- Core Concepts → `To use this system, you need to understand <N> main building blocks:`
- Each Step → bare imperative verb (Place, Define, Author, Link, Add, Assign).
- Debugging & Tools → `The <component> includes built-in tools to help you visualize your setup before hitting Play:`
- FAQ entry → `Q: <symptom-phrased question>` then `Check <...>` bullets.

---

### 3. How-To page: Setup/config variant

A good starting point for a lighter **"configure this asset" page** with no deep hierarchy and no walkthrough. Title: `How To: <Feature>`. The body is a flat sequence of named asset/settings headings, and it usually skips `How does it work?`, `Core Concepts`, the TOC, and the Reference section.

```
How To: <Feature>

Overview
This page is meant to talk about the <Feature> and how to set it up. <One or two sentences on
what it organizes / why it exists.>

<Asset/Settings Group Name>                    ← e.g. <Asset> Settings
<This lets you <verb>... / short prose describing the asset.>

Location at time of writing:                   ← (Optional) volatile path label
<project-path>/<area>/<asset>

Example asset:                                  ← (Optional) example-asset label + path
<one sentence on what the example demonstrates>
<project-path>/<area>/<asset>

<Settings Group Name>                          ← e.g. Project Settings
<prose>

<Sub-Asset / Entry Name>                       ← e.g. <Asset> Entry
  <Field> - <description>                       ← Term - description bullets under the heading
  <Field> - <description>

Debugger                                        ← present when there is a debugger to document
   <Debug View Name>
```

**Section habits:**
- Open with `This page is meant to talk about <X> and how to set it up.`
- One heading per asset or settings group; put `Term - description` bullets directly under the heading that owns those fields.
- Use `Location at time of writing:` for volatile paths and `Example asset:` to introduce an illustrative (possibly not-hooked-up) asset.

---

### 4. Design Spec

A good starting point for forward-looking design proposals. Title: `<Topic> Spec`. Four sections, in order, tends to be enough, so adapt freely. There usually isn't an Overview, TOC, or Debugger.

```
<Topic> Spec
Goal
Create <a new way to ...> <comparison point> <without conflicting with ...>. This version should
provide <parity requirement> (e.g. <example>) but doesn't necessarily need <explicit scope limit>.

Problems
<Prose: the typical way we handle <X> requires <Y>. <Why the current approach is insufficient.>>

Solutions
  <Proposed approach.>
    <sub-bullet>
    <sub-bullet>
    TBD                                         ← bare TBD is an acceptable placeholder
  <Proposed approach.>

Phases
Phase 1
  <work item>                                   ← a phase may be a single bullet line
Phase 2
  <work item>
```

**Section habits:**
- **Goal** → start with the imperative verb `Create ...`. Fold constraints / non-goals inline (no separate Scope or Non-Goals heading). Specs tend to use **bare `e.g.`** (no comma).
- **Problems** → prose describing current limitations, often `The typical way we handle <X> ...`.
- **Solutions** → bulleted (nestable) proposals; `TBD` allowed.
- **Phases** → `Phase N` sub-headings, each a short bullet list.

---

### 5. Documentation (landing) page

A good starting point for a hub page that **routes readers to many sub-pages** rather than teaching one workflow. Title: `<Area> Documentation` (no colon, no "How To:"). Three sections, in order, tends to be enough, so adapt freely.

```
<Area> Documentation

Overview
<Architecture/philosophy prose characterizing the system, NOT "This page is meant...".>
In general, here is the current vision for how <X> should work.
  <Design/flow statement.>
  <Design/flow statement.>
<You should feel comfortable using what works best for the job and I wouldn't want to impose
any hard rules other than <minimal constraints>.>     ← low-prescription closing sentence

Documentation
Here you can find a list of resources for using <X> in your project. You may find some small
examples of how to use these systems in the editor at <project-path>/<area>/<asset>.

   <Internal Page Title>                        ← nested link list; indent children under parents
   <Internal Page Title>
      <Child Page Title>
      <Child Page Title>

  For <X> feel free to add them to <Page Title> .   ← inline forward-pointers, end of section
  <One-line pointer to a sibling page> .

Useful Resources
  <External Talk/Article Title> -- <Author>     ← " -- <Author>" for SHORT personal-author credits
  <External Talk/Article Title> - <gloss>       ← " - <gloss>" for a descriptive note or org credit
```

**Section habits:**
- **Overview** → architecture characterization (e.g. "Our system is not exactly MVC or MVVM..."); close with the low-authority guidance sentence.
- **Documentation** → `Here you can find a list of resources for using <X> in your project.`; internal links only; append inline `For <X> feel free to...` forward-pointers.
- **Useful Resources** → external talks/articles/plugins only. Attribute a short personal author with the ` -- <Author>` double-hyphen suffix. Use a single ` - <description>` for a descriptive gloss or organization credit (e.g. `- <Organization>`). Both are in voice.
