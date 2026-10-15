# PyBob Python Mentor — Scale-Ready Custom Instructions Plan

## Top-Level Overview

**Goal:** Complete the PyBob Python Mentor custom instructions to match the production-grade depth of `jenny.md` — a retention-engineered, psychometrically adaptive, globally scalable mentor system capable of serving millions of learners.

**Scope:** The `pybob.md` Custom Instructions section (below the `Custom instructions` header) is structurally thin. It has 6 sections covering state, phases, curriculum outline, scoring, dropout prevention, and style. It is missing the full retention engine, the blind assessment loop, the generation-first iron rule enforcement, the session close protocol, the Engram FSRS flashcard export, the return amnesty protocol, the depth architecture score, and the full language-equivalent "Python Module Library" (concept WHY, bridges, false friends, threshold nodes per module).

**Approach:** Mirror Jenny's 7-phase retention loop exactly — adapted for Python pedagogy. Add all missing architectural layers. The final document must score >= 94.7 on the Depth Score Architecture rubric defined in jenny.md.

**Reference files:**
- [`jenny.md`](jenny.md) — gold standard architecture
- [`pybob.md`](pybob.md) — current state (role definition + partial custom instructions)

---

## Sub-Tasks

---

### Sub-Task 1: Mandate Hardening — Role Definition Strengthening

**Intent:** The existing Role Definition in `pybob.md` is good but missing 3 of Jenny's 7 non-negotiable mandates that are critical for scale: Generation-First (Iron Rule), Psychometric Vector definition, and the Retention Over Interaction mandate. These are the mandates that separate a chatbot from a learning system.

**Expected Outcomes:**
- Role Definition contains all 7 mandates translated for Python pedagogy
- `psychometric_vector` fields are fully defined (level, modality, correction_style, industry_context, goal, track)
- Generation-first enforcement is explicit and non-negotiable
- Logical Fallacy Correction mandate is expanded to cover all Python-specific fallacies

**Todo List:**
1. Map all 7 Jenny mandates to Python equivalents
2. Add Mandate 3 (Generation-First / Iron Rule) explicitly to Role Definition
3. Add Mandate 4 (Psychometric Adaptation) with full psychometric_vector fields
4. Add Mandate 5 (Retention Over Interaction) with Engram FSRS reference
5. Expand Mandate 6 (Logical Fallacy Correction) to include all 4 Python fallacies from existing + 3 new ones
6. Add Mandate 7 (WHY Behind Every Rule) as explicit non-negotiable

**Relevant Context:** `jenny.md` lines 14–21, `pybob.md` lines 11–19

**Status:** [ ] pending

---

### Sub-Task 2: Phase 1 — Full Diagnostic Intake Rebuild

**Intent:** Current Phase 1 (Section 2) asks 3 proficiency questions and a modality question but does not follow the structured 5-question Socratic diagnostic that Jenny uses. It also does not confirm the psychometric_vector with the student before locking it. This is the intake that governs all downstream adaptation.

**Expected Outcomes:**
- 5 conversational diagnostic questions, one at a time
- Questions cover: Level, Real-World Goal/Use Case, Industry Context, Learning Modality, Correction Style
- psychometric_vector is confirmed with the student before proceeding
- Returning students get warm re-entry with profile confirmation (not full re-diagnostic)
- Track selection (A/B/C) follows the diagnostic, not precedes it

**Todo List:**
1. Rewrite STEP 1.2 to be a 5-question Socratic intake matching Jenny's structure
2. Add "Real-World Goal" question (the specific project/problem they want to solve)
3. Add "Industry Context" question (automation for finance vs data science for biotech changes everything)
4. Add "Correction Style" question (immediate interrupt vs end-of-turn review)
5. Add internal psychometric_vector confirmation step
6. Rewrite STEP 1.4 (returning students) to include profile confirmation check

**Relevant Context:** `jenny.md` lines 28–28, `pybob.md` lines 26–31

**Status:** [ ] pending

---

### Sub-Task 3: Phase 2 — Curriculum Architecture as Concept Map

**Intent:** Current curriculum is a flat node list. Jenny builds a backward-chained Concept Map with Threshold nodes (the unlock-everything concepts), Probes, and Rubrics per node. This architecture is what enables blind assessment and adaptive routing. Without it, the system cannot know when to advance vs remediate.

**Expected Outcomes:**
- Each module has a Concept Map with: # | Node | Type | Probe | Rubric columns
- Threshold nodes (dagger-marked) are identified for each module
- Each node has: Claim (one testable sentence), Probe (no answer leak), Rubric (2–3 criteria), Type (Threshold/Arbitrary/Derivable)
- Module 0 Concept Map fully specified
- Track-specific Concept Maps (4A, 4B, 4C) outlined with threshold nodes
- Video-first modality triggers YouTube/resource recommendations for threshold nodes

**Todo List:**
1. Define Concept Map schema (Claim, Probe, Rubric, Type) for Python pedagogy
2. Build full Module 0 Concept Map (Nodes 0.1–0.5 + Exam)
3. Identify threshold nodes per module (e.g., functions are the threshold for all Modules 2–4)
4. Add Concept Map outlines for Modules 1–3
5. Add Track Concept Map stubs for 4A/4B/4C
6. Add video-first resource recommendations for top threshold nodes

**Relevant Context:** `jenny.md` lines 29–29, `pybob.md` lines 32–39

**Status:** [ ] pending

---

### Sub-Task 4: Phase 3 — Immersive Socratic Teaching Loop (Full 6-Step)

**Intent:** The current custom instructions do not implement the full Socratic loop. They mention "Socratic questioning" in the Role Definition but the Custom Instructions section only has a scoring table. The 6-step loop (Scene Setting → Attempt Gate → Struggle Budget → Correction Block → 3-Option Rescue → Advance Gate) is the core engine that drives retention — it is entirely absent.

**Expected Outcomes:**
- Full 6-step Phase 3 loop defined for Python pedagogy
- Step 3.1: Code scenario described with real-world stakes (not abstract)
- Step 3.2: Generation-first gate enforced (student must attempt before PyBob helps)
- Step 3.3: Struggle budget defined (Socratic hint on failure 1, rescue after failure 2)
- Step 3.4: [PyBob Notes] correction block table: What you wrote | Better code | The Pattern | The WHY
- Step 3.5: 3-Option Rescue adapted for code (Option A: Direct/Idiomatic, Option B: Verbose/Safe, Option C: Functional/Elegant)
- Step 3.6: Advance gate tied to Concept Map rubric criteria

**Todo List:**
1. Write Step 3.1 Scene-Setting protocol for code challenges
2. Write Step 3.2 Attempt Gate with generation-first enforcement
3. Write Step 3.3 Struggle Budget with warm struggle-naming ("That friction is the memory forming")
4. Write Step 3.4 [PyBob Notes] correction table schema
5. Write Step 3.5 3-Option Code Rescue format
6. Write Step 3.6 Advance Gate tied to Concept Map rubric

**Relevant Context:** `jenny.md` lines 30–30, `pybob.md` lines 18–19 (Role Definition reference only)

**Status:** [ ] pending

---

### Sub-Task 5: Phase 4 — Blind Assessment Engine

**Intent:** Blind assessment (running silently after every student production, never announced) is the core of the retention loop. It is completely absent from `pybob.md`. Without it, the system has no mechanism to distinguish Recalled vs Partial vs Lapsed — which means it cannot route to remediation, cannot generate correct FSRS intervals, and cannot advance students at the right pace.

**Expected Outcomes:**
- Blind assessment runs after every code submission
- Three grades defined: Recalled (advance), Partial (repeat with variation), Lapsed (re-teach new angle)
- Python-specific grading rules: style violations are always Partial; logic errors that produce correct output by accident are Lapsed; type errors / NameErrors are Partial; working but unidiomatic code is Partial
- Critical rules table matching Jenny's format
- High confidence + wrong pattern = Partial or Lapsed (not Recalled)

**Todo List:**
1. Define Recalled/Partial/Lapsed rubric for Python code assessment
2. Define FSRS routing: Recalled → Easy/Good → advance; Partial → Hard → repeat; Lapsed → Again → re-teach
3. Write Python-specific grading rules (style, logic, idiom, error type)
4. Add "silent" enforcement note (never announce the grade aloud)
5. Add False Friend trap detection (Python-specific cognitive traps listed in Section 6 of Sub-Task 7)

**Relevant Context:** `jenny.md` lines 31–31, `pybob.md` lines 40–42 (existing scoring is input-side, not assessment-side)

**Status:** [ ] pending

---

### Sub-Task 6: Phase 5 & 6 — Session Close + Engram FSRS Export

**Intent:** The session close protocol and retention scheduling (Phases 5 and 6) are entirely absent from `pybob.md`. These phases are the reason Jenny scores +9.7 in Engram FSRS Export on the depth rubric. For a system serving millions of learners, spaced repetition scheduling is the difference between knowledge that persists and knowledge that evaporates within 48 hours.

**Expected Outcomes:**
- Session Close Protocol: Vocabulary Recap table (Code Pattern | Use Case | Idiom Level | Status), Progress Note (specific improvement named), Homework Challenge
- Engram FSRS flashcard generation: 3–5 nodes with Partial or Lapsed grades
- Flashcard format: Topic / Node / Probe (no answer leak) / Target (code pattern) / Rubric
- Instruction to student: how to load in Engram CLI
- `source:told` tracking for concepts the student asked to be told directly (returns sooner)

**Todo List:**
1. Write Step 5.1 Code Pattern Recap table schema
2. Write Step 5.2 Progress Note protocol (specific to the work, not generic praise)
3. Write Step 5.3 Homework Challenge (one pattern to implement before next session)
4. Write Phase 6 FSRS flashcard generation logic
5. Write FSRS flashcard format for Python (Topic / Node / Probe / Target / Rubric)
6. Add `source:told` tracking mechanic to the system

**Relevant Context:** `jenny.md` lines 32–33, `pybob.md` — absent

**Status:** [ ] pending

---

### Sub-Task 7: Phase 7 + Python Module Library (Concept WHY Architecture)

**Intent:** Two critical layers are missing: (1) the Amnesty Protocol for returning students (prevents shame-driven dropout after a gap), and (2) the Python-equivalent of Jenny's Language Module Library — a per-module WHY architecture with bridges, threshold nodes, false friends (cognitive traps), and cultural/historical context for every major Python concept. This is the deepest differentiator between a syntax tutor and a system that engineers understanding.

**Expected Outcomes:**
- Phase 7 Amnesty Protocol implemented: no shame, capped review queue, choices offered
- Python Module Library covering all modules: Bridge (how prior knowledge transfers), Threshold nodes, False Friends (Python cognitive traps), Historical WHY, Industry anchors
- At minimum: Module 0 (Foundations), Module 1 (Data Structures), Module 2 (Functions/Modules), Module 3 (OOP), Module 4A (Data Science), Module 4B (Web Dev), Module 4C (Automation)

**Todo List:**
1. Write Phase 7 Amnesty Protocol for Python (gap return, no guilt, capped reviews)
2. Write Module Library entry for Module 0 (Bridge: everyday logic → code; Threshold: variables + functions; False Friends: assignment vs equality, mutable defaults; WHY: why indentation?)
3. Write Module Library entry for Module 1 (Bridge: spreadsheet rows → lists; Threshold: dict comprehension; False Friends: list.append vs list + [x]; WHY: why immutable tuples?)
4. Write Module Library entry for Module 2 (Bridge: recipe steps → functions; Threshold: scope/closure; False Friends: import vs from-import; WHY: why modules exist?)
5. Write Module Library entry for Module 3 (Bridge: real-world objects → classes; Threshold: __init__ and self; False Friends: class variable vs instance variable; WHY: why OOP?)
6. Write Module Library entries for 4A/4B/4C (abbreviated with top threshold nodes and false friends)
7. Add Game Track Library entry for game_driven modality

**Relevant Context:** `jenny.md` lines 34–43, `pybob.md` — absent

**Status:** [ ] pending

---

### Sub-Task 8: Depth Score Architecture + Final Assembly

**Intent:** Jenny's system has an explicit Depth Score Architecture that ensures no critical layer is skipped. PyBob needs the equivalent. This sub-task also assembles all prior sub-tasks into the final `pybob.md` custom instructions block — fully replacing the existing Section 1–6 with the complete 7-phase system.

**Expected Outcomes:**
- Depth Score Architecture defined with named dimensions and point values summing >= 94.7
- All 7 phases present and integrated
- All mandates cross-referenced in the instruction body
- Persistent memory schema finalized (updated for new fields)
- Style Enforcement section updated to be tied to Phase 4 blind assessment (not a standalone section)
- Final `pybob.md` is production-ready for millions of learners

**Todo List:**
1. Define PyBob Depth Score Architecture (map Jenny's 13 dimensions to Python equivalents)
2. Finalize persistent memory schema (add new fields: fsrs_queue, source_told_nodes, concept_map_state, correction_style, industry_context)
3. Integrate Style Enforcement into Phase 4 grading rules (not a disconnected section)
4. Write Available Tools section (Read/Edit/Execute/MCP)
5. Assemble and write complete final `pybob.md`
6. Verify all 7 phases are present, all 7 mandates are in Role Definition, depth score >= 94.7

**Relevant Context:** `jenny.md` lines 44–50, `pybob.md` lines 26–50

**Status:** [ ] pending

---

## Architecture Overview

```
PYBOB SYSTEM LAYERS
─────────────────────────────────────────────────────────
Role Definition          7 Mandates (Iron Rules)
─────────────────────────────────────────────────────────
Phase 1: Diagnostic      5-question psychometric intake
Phase 2: Curriculum      Concept Map (Threshold nodes)
Phase 3: Teaching Loop   6-step Socratic + Correction Block
Phase 4: Assessment      Blind FSRS grading (Recalled/Partial/Lapsed)
Phase 5: Session Close   Recap + Progress Note + Homework
Phase 6: FSRS Export     Engram flashcard generation
Phase 7: Amnesty         Gap-return protocol (no shame)
─────────────────────────────────────────────────────────
Module Library           WHY + Bridge + False Friends per module
─────────────────────────────────────────────────────────
Depth Score              >= 94.7 (13 named dimensions)
─────────────────────────────────────────────────────────
```

## Validation Questions for User

1. Should PyBob support **SQL and data analysis** within Track A (Data Science) as a parallel track, or keep it pure Python? (Jenny's SqlBob is a separate mode)
2. Should the **Game Track** receive the same full 7-phase treatment as the main tracks, or remain a lighter supplement?
3. Is the **Engram FSRS** integration assumed available for all learners, or should PyBob fall back to a manual "review list" when Engram is not installed?
4. Should PyBob generate **executable code cells** (Jupyter/Colab style) in the correction block, or plain code blocks only?
5. The current pybob.md has `student_workspace/global_profile.md` for persistence — should this remain, or adapt to a simpler in-context memory model for scale?
