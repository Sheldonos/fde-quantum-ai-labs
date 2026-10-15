# Plan: Build Full `customInstructions` for UI/UX Pro Max Skill

## Top-Level Overview

**Goal:** Replace the single placeholder sentence in `uiux.md`'s `customInstructions` with a
complete, self-contained behavioral contract that makes the UI/UX Pro Max skill functional
at scale for millions of frontend developers globally.

**Scope:** The `customInstructions` field in `uiux.md`. The `SKILL.md` is the knowledge base
(excellent, stays unchanged). The `customInstructions` is the agent's _operating protocol_ —
it governs what the agent DOES with that knowledge every time it runs.

**Approach:** Write `customInstructions` as a structured behavioral spec covering:
1. Session entry protocol (what agent does first on every activation)
2. Stack detection and routing (React, Next.js, Vue, Svelte, Tailwind, shadcn/ui, HTML/CSS)
3. Priority-ordered design decision framework (mirrors SKILL.md rule categories 1→10)
4. Output contract (what code looks like: tokens not hex, accessible, responsive, etc.)
5. Anti-pattern guard (uncodixfy rules baked in: no AI slop UI)
6. Quality gate (pre-delivery checklist enforced before any code is returned)

**Non-goals:**
- Do NOT modify the SKILL.md
- Do NOT add Python CLI dependencies (no scripts, no local tooling required)
- Do NOT make it React Native / mobile only — must serve web-first globally
- Do NOT add features beyond what serves the stated task

---

## Sub-Task 1: Define Session Entry Protocol

**Intent:** Every invocation of the skill must start with the same diagnostic step so the
agent anchors on real context before generating any UI. This prevents random hallucinated
design choices that don't match the product.

**Expected Outcomes:**
- The `customInstructions` opens with a mandatory "Phase 0: Orient" block
- Agent extracts: product type, stack, style preference, target audience, existing design system
- Agent states extracted context back to the user before generating anything
- If context is ambiguous, agent asks 1-2 targeted clarifying questions (not a long survey)

**Todo List:**
1. Write the "Phase 0: Orient" block — 4 extraction dimensions: product type, stack, audience, existing tokens/system
2. Write the disambiguation trigger: if stack is unknown, ask once before proceeding
3. Write the acknowledgment pattern: "I'll build this as [X] for [Y] using [Z]" before code

**Relevant Context:**
- `SKILL.md` Step 1 (Analyze User Requirements) — port this into always-on behavior
- `uiux.md` line 4-5: current instruction is just "Always start by establishing a design system"

**Status:** [x] done

---

## Sub-Task 2: Write Stack Detection and Routing Rules

**Intent:** The skill claims 10 stacks in its description (React, Next.js, Vue, Svelte,
SwiftUI, React Native, Flutter, Tailwind, shadcn/ui, HTML/CSS). The `customInstructions`
must tell the agent HOW to adapt its output per stack — no Python CLI needed.

**Expected Outcomes:**
- Agent selects the right import patterns, component primitives, and class utilities per stack
- Tailwind users get Tailwind utility classes; Vue users get `<script setup>` + Composition API
- shadcn/ui users get `cn()` + shadcn primitives; Next.js users get Server vs Client component guidance
- Agent never mixes React hooks into Vue code or Tailwind classes into Flutter

**Todo List:**
1. Write stack detection heuristic: how agent infers stack from file names, imports, or explicit user statement
2. Write per-stack output rules table: React / Next.js / Vue / Svelte / Tailwind / shadcn/ui / HTML/CSS
3. Write the "when stack is unknown" default: ship HTML/CSS + Tailwind as the universal fallback
4. Write the mobile-native guard: if stack is SwiftUI/Flutter/React Native, redirect to mobile-specific rules in SKILL.md

**Relevant Context:**
- `SKILL.md` Search Reference table (lines 680-700) — domain/stack mapping already defined
- `uiux.md` line 5: "Use Google Stitch for mockups and 21st.dev Magic for components" — preserve these as tools

**Status:** [x] done

---

## Sub-Task 3: Write the Priority-Ordered Design Decision Framework

**Intent:** The agent must apply design rules in the exact priority order defined in SKILL.md
(1→10: Accessibility → Touch/Interaction → Performance → Style → Layout → Typography →
Animation → Forms → Navigation → Charts). Without this embedded in `customInstructions`,
agents skip accessibility and jump straight to visual gloss.

**Expected Outcomes:**
- Every generated component passes rules 1-3 (CRITICAL + HIGH) before cosmetics are applied
- Agent checks contrast, touch targets, and performance constraints first
- Agent applies style (rule 4) only after CRITICAL rules are satisfied
- Agent documents which rules it applied as a brief comment block in generated code

**Todo List:**
1. Write "Phase 2: Apply Rules" block — ordered 1→10 matching SKILL.md priority table
2. Write the "CRITICAL first" gate: agent must state that a11y + touch pass before any style decisions
3. Write the annotation contract: generated code includes `// ✓ a11y: contrast 4.5:1, aria-labels` type markers
4. Write the anti-pattern suppression list: top 5 most common AI UI sins to explicitly ban

**Relevant Context:**
- `SKILL.md` lines 62-78: Rule Categories by Priority table — this is the exact priority order
- `uncodixfy/SKILL.md`: anti-patterns to bake in (no glassmorphism blobs, no gradient text, no >12px radius on buttons)

**Status:** [x] done

---

## Sub-Task 4: Write the Output Contract (Code Quality Standards)

**Intent:** Define exactly what "good output" looks like so every developer globally gets
the same quality bar: semantic tokens not raw hex, accessible HTML structure, responsive
defaults, no hardcoded magic numbers.

**Expected Outcomes:**
- All color values reference CSS custom properties or design tokens (never raw `#3b82f6`)
- All spacing uses the 4/8dp scale or Tailwind's spacing scale (no `margin: 13px`)
- All interactive elements have aria attributes, focus states, and min touch targets
- Typography follows the defined type scale from SKILL.md §6
- Dark mode is handled via token inversion, not duplicate component copies

**Todo List:**
1. Write the token contract: colors → CSS vars or Tailwind tokens; spacing → scale multiples
2. Write the responsive contract: mobile-first, systematic breakpoints, no horizontal scroll
3. Write the accessibility output contract: aria-labels, semantic HTML, focus rings never removed
4. Write the dark mode contract: semantic color tokens, no separate dark component copies
5. Write the animation contract: transform/opacity only, 150-300ms, prefers-reduced-motion respected

**Relevant Context:**
- `SKILL.md` §6 Typography & Color (lines 249-279): semantic token rules
- `SKILL.md` §5 Layout & Responsive (lines 215-247): breakpoint + spacing rules
- `SKILL.md` §7 Animation (lines 281-329): transform-only, timing rules

**Status:** [x] done

---

## Sub-Task 5: Embed the Anti-Pattern Guard (uncodixfy + AI Slop Prevention)

**Intent:** At global scale, the most common failure mode is the agent producing "AI slop UI":
glassmorphism cards, gradient text headings, floating blobs, dramatic drop shadows, oversized
border radii. This guard must be always-on, not opt-in.

**Expected Outcomes:**
- Agent never produces the banned patterns without explicit user override
- Agent self-corrects if it detects it's about to ship an AI-sloppy design
- When user asks for "glassmorphism" explicitly, agent delivers it correctly per SKILL.md §4 (not decoratively)

**Todo List:**
1. Write the always-on banned patterns list (from uncodixfy SKILL.md)
2. Write the "by default, ship Linear/Stripe/GitHub aesthetic" default instruction
3. Write the explicit-override escape hatch: "if user explicitly requests glassmorphism, apply correctly per blur-purpose rule"
4. Write the icon rule: SVG only, consistent stroke width, no emoji as UI icons

**Relevant Context:**
- `uncodixfy/SKILL.md` lines 34-48: the banned patterns list
- `SKILL.md` §4 Style Selection lines 193, 207-211: icon and style rules

**Status:** [x] done

---

## Sub-Task 6: Write the Pre-Delivery Quality Gate

**Intent:** The agent must self-review against the checklist before returning any UI code.
This is the "last mile" enforcement that ensures every single output — regardless of the
developer's experience level — passes a minimum quality bar.

**Expected Outcomes:**
- Agent runs through a compressed version of SKILL.md's Pre-Delivery Checklist mentally before output
- Any failing item is either fixed inline or called out explicitly as a known limitation
- Output ends with a brief "Quality Gate: PASS" summary or flags open issues

**Todo List:**
1. Write the 5-category pre-delivery gate: Visual / Interaction / Accessibility / Responsive / Dark Mode
2. Write the "fix or flag" rule: agent fixes critical issues; flags medium issues with a comment
3. Write the final output format: code block + brief quality summary + any open questions

**Relevant Context:**
- `SKILL.md` Pre-Delivery Checklist (lines 858-925): the full checklist to compress
- `SKILL.md` Tips for Better Results §Pre-Delivery Checklist (lines 784-796): the short version

**Status:** [x] done

---

## Sub-Task 7: Assemble and Write Final `customInstructions` into `uiux.md`

**Intent:** Combine all 6 sub-tasks into a single, coherent `customInstructions` string in
`uiux.md`. The instructions must be readable by any LLM, require zero tooling, and be
compact enough to fit in a mode's custom instructions field while still being comprehensive.

**Expected Outcomes:**
- `uiux.md` `customInstructions` field contains the full behavioral contract
- Instructions are structured as numbered phases, not a wall of prose
- No Python script dependencies anywhere in the instructions
- Works for React, Next.js, Vue, Svelte, Tailwind, shadcn/ui, HTML/CSS out of the box

**Todo List:**
1. Merge sub-tasks 1-6 into a unified `customInstructions` string
2. Ensure total length is appropriate for a mode's instruction field (thorough but not bloated)
3. Write the final `uiux.md` with the complete updated `customInstructions`
4. Verify the YAML is valid and all fields from the original `uiux.md` are preserved

**Relevant Context:**
- `uiux.md` (all 11 lines) — original file to update
- All sub-tasks above feed into this final assembly

**Status:** [x] done
