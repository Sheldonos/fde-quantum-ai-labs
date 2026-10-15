# PyBob Python Mentor — Final Production Plan (Scale for Millions)

## Top-Level Overview

**Goal:** Write the complete, production-ready custom instructions for the PyBob Python Mentor mode — capable of serving millions of global learners at any proficiency level, in any language, on any device, with retention-engineered pedagogy matching or exceeding Jenny's 94.7 Depth Score.

**Scope:** Replace the current Sections 1–6 in `pybob.md` Custom Instructions with the full 7-phase retention loop (matching Jenny's architecture), then append Sections 7–17 covering every global scale requirement. The Role Definition stays and is hardened with all 7 mandates. Final file is `pybob.md` — fully rewritten to production standard.

**Reference files:**
- [`jenny.md`](jenny.md) — gold standard architecture (7-phase loop, Depth Score 94.7, Module Library)
- [`pybob.md`](pybob.md) — current state (Role Definition + Sections 1–6, thin)
- [`pybob-mentor-plan.md`](pybob-mentor-plan.md) — retention architecture sub-tasks (8 sub-tasks)
- [`pybob-plan.md`](pybob-plan.md) — scale features sub-tasks (11 sub-tasks)

**Output file:** `pybob.md` — complete rewrite retaining the header format (Modes / Name / Scope / Role definition / When to use / Custom instructions / Available Tools)

**Depth Score Target:** >= 94.7 across all 13 named dimensions

---

## Sub-Tasks

---

### Sub-Task 1 — Harden Role Definition (7 Mandates)

**Intent:** The current Role Definition has 7 partial mandates embedded in prose but is missing the explicit Generation-First Iron Rule, the full psychometric_vector field list, and the Retention Over Interaction mandate as a named, non-negotiable. These 3 are the architectural backbone that separates a chatbot from a learning system.

**Expected Outcomes:**
- All 7 mandates named, numbered, and stated as non-negotiable in the Role Definition block
- Generation-First (Iron Rule) is explicit, includes the `source:told` mechanic
- `psychometric_vector` is fully defined: level, modality, correction_style, industry_context, goal, track
- Logical Fallacy Correction expanded: 4 existing + 3 new Python-specific fallacies
- Mandate 7 (WHY Behind Every Rule) explicitly named

**Todo List:**
1. Write Mandate 1 (Tone and Presence) — existing content, confirm and format
2. Write Mandate 2 (Non-Intrusive Teaching) — existing content, confirm and format
3. Write Mandate 3 (Generation-First / Iron Rule) — new, with source:told mechanic
4. Write Mandate 4 (Psychometric Adaptation) — define all 6 psychometric_vector fields
5. Write Mandate 5 (Retention Over Interaction) — with Engram FSRS reference
6. Write Mandate 6 (Logical Fallacy Correction) — expand to 7 Python fallacies
7. Write Mandate 7 (WHY Behind Every Rule) — explicit non-negotiable

**Relevant Context:** `jenny.md` lines 14–21, `pybob.md` lines 11–19

**Status:** [ ] pending

---

### Sub-Task 2 — Phase 1: Full 5-Question Diagnostic Intake

**Intent:** Rebuild the initialization phase as a structured 5-question Socratic intake matching Jenny's Phase 1. Current STEP 1.2 only asks 3 proficiency questions and 1 modality question — missing Real-World Goal, Industry Context, and Correction Style. These three questions are what enable meaningful adaptation downstream.

**Expected Outcomes:**
- 5 conversational diagnostic questions, one at a time (Level, Real-World Goal, Industry Context, Learning Modality, Correction Style)
- `psychometric_vector` confirmed with student before proceeding
- Track selection (A/B/C) follows the diagnostic, not precedes it
- Returning student path: warm greeting + profile confirmation (no full re-diagnostic)
- State fields: `python_current_loop_node`, `python_retention_score`, `python_exam_scores`, `python_learning_track`, `python_session_count`, `python_bonus_challenges_unlocked`, `psychometric_vector`, `fsrs_queue`, `source_told_nodes`, `concept_map_state`, `correction_style`, `industry_context`, `learner_language`, `learner_locale`, `accessibility_flags`, `learner_age_band`, `guardian_mode`, `learner_mode`, `cohort_id`, `escalation_log`

**Todo List:**
1. Write Question 1 (Level): proficiency check + level declaration
2. Write Question 2 (Real-World Goal): specific project/problem the student wants to solve
3. Write Question 3 (Industry Context): finance / healthcare / education / etc.
4. Write Question 4 (Learning Modality): hands-on / grammar-first / video-first / game-driven
5. Write Question 5 (Correction Style): immediate interrupt vs end-of-turn review
6. Write psychometric_vector confirmation step
7. Write returning student warm-entry path with profile confirmation
8. Write complete `global_profile.md` state schema with all fields

**Relevant Context:** `jenny.md` Phase 1, `pybob.md` lines 26–31 (Sections 1–2)

**Status:** [ ] pending

---

### Sub-Task 3 — Phase 2: Curriculum as Concept Map with Threshold Nodes

**Intent:** Replace the flat node list with a backward-chained Concept Map architecture. Each module must have named Threshold nodes (the unlock-everything concepts), Probes, and Rubrics. Without this structure, Phase 4 blind assessment cannot route correctly.

**Expected Outcomes:**
- Concept Map schema defined (Claim, Probe, Rubric, Type columns)
- Module 0 fully mapped (Nodes 0.1–0.5 + Exam, threshold nodes identified)
- Modules 1–3 Concept Maps (with threshold nodes)
- Track 4A/4B/4C Concept Map stubs
- Game Track G.1–G.3 concept nodes
- Video-first resource recommendations for top threshold nodes

**Todo List:**
1. Define Concept Map table schema for Python pedagogy
2. Build Module 0 Concept Map (Hello World → Functions → Module Exam)
3. Identify threshold nodes: functions (unlocks Modules 2–4), dicts (unlocks 4A), classes (unlocks 4B/4C)
4. Build Module 1 Concept Map (Data Structures: list/dict/tuple/set)
5. Build Module 2 Concept Map (Functions/Modules/IO/Errors)
6. Build Module 3 Concept Map (OOP: classes, inheritance, dunders)
7. Add Track 4A/4B/4C Concept Map stubs with top threshold nodes
8. Add video-first YouTube search query recommendations for threshold nodes

**Relevant Context:** `jenny.md` Phase 2, `pybob.md` lines 32–39 (Section 3)

**Status:** [ ] pending

---

### Sub-Task 4 — Phase 3: Full 6-Step Socratic Teaching Loop

**Intent:** The 6-step Socratic loop is the core teaching engine. It is referenced in the Role Definition but entirely absent from the Custom Instructions. Without it, PyBob improvises instead of following a proven retention protocol. Every code challenge must go through: Scene Setting → Attempt Gate → Struggle Budget → PyBob Notes Correction Block → 3-Option Code Rescue → Advance Gate.

**Expected Outcomes:**
- Step 3.1: Real-world stakes scenario described (not abstract)
- Step 3.2: Generation-first gate — student must attempt code before PyBob helps
- Step 3.3: Struggle Budget — Socratic hint after failure 1, 3-Option Rescue after failure 2
- Step 3.4: [PyBob Notes] correction table: What you wrote | Better code | The Pattern | The WHY
- Step 3.5: 3-Option Code Rescue (Option A: Direct/Idiomatic, Option B: Verbose/Safe, Option C: Functional/Elegant)
- Step 3.6: Advance Gate tied to Concept Map rubric criteria

**Todo List:**
1. Write Step 3.1 Scene-Setting protocol for Python code challenges
2. Write Step 3.2 Attempt Gate with generation-first enforcement and source:told mechanic
3. Write Step 3.3 Struggle Budget with warm struggle-naming
4. Write Step 3.4 [PyBob Notes] correction table schema (4-column format)
5. Write Step 3.5 3-Option Code Rescue format (3 code styles, student picks)
6. Write Step 3.6 Advance Gate tied to Concept Map rubric

**Relevant Context:** `jenny.md` Phase 3, `pybob.md` Role Definition line 18

**Status:** [ ] pending

---

### Sub-Task 5 — Phase 4: Blind Assessment Engine (FSRS Routing)

**Intent:** Blind assessment runs silently after every student code submission. It is the mechanism that distinguishes Recalled vs Partial vs Lapsed — and drives FSRS interval routing. Completely absent from current `pybob.md`. Without it the system has no feedback loop.

**Expected Outcomes:**
- Recalled / Partial / Lapsed rubric defined for Python code
- FSRS routing: Recalled → Easy/Good → advance; Partial → Hard → repeat with variation; Lapsed → Again → re-teach from new angle
- Python-specific grading rules: style violations = Partial, logic errors with accidentally correct output = Lapsed, type/NameErrors = Partial, working but unidiomatic = Partial
- Style Enforcement rules (from current Section 6) integrated HERE as grading criteria, not a disconnected section
- False Friend trap detection list for Python cognitive traps

**Todo List:**
1. Define Recalled/Partial/Lapsed rubric for Python code assessment
2. Define FSRS routing per grade
3. Write Python-specific grading rules (style, logic, idiom, error type)
4. Integrate Section 6 style enforcement as Phase 4 grading criteria
5. Write Python False Friend cognitive trap list (at minimum 8 traps)
6. Add "silent" enforcement rule (never announce the grade)

**Relevant Context:** `jenny.md` Phase 4, `pybob.md` lines 40–42 (Section 4 scoring) and lines 43–46 (Section 6 style)

**Status:** [ ] pending

---

### Sub-Task 6 — Phases 5 & 6: Session Close + Engram FSRS Export

**Intent:** Session close and spaced repetition scheduling are the difference between knowledge that persists and knowledge that evaporates. Both phases are absent from current `pybob.md`. These two phases are weighted +6.4 + +9.7 in the Depth Score — the highest single contributor.

**Expected Outcomes:**
- Phase 5 Session Close: Code Pattern Recap table (Code Pattern | Use Case | Idiom Level | Status), Progress Note (specific, not generic), Homework Challenge (one pattern to implement)
- Phase 6 FSRS Export: 3–5 flashcards for Partial/Lapsed nodes
- Flashcard format: Topic / Node / Probe (no answer leak) / Target (code pattern) / Rubric
- `source:told` tracking mechanic integrated

**Todo List:**
1. Write Phase 5 Step 5.1: Code Pattern Recap table schema
2. Write Phase 5 Step 5.2: Progress Note protocol (specific to the work, not generic praise)
3. Write Phase 5 Step 5.3: Homework Challenge (one pattern to implement before next session)
4. Write Phase 6 FSRS flashcard generation logic
5. Write FSRS flashcard format (Topic / Node / Probe / Target / Rubric)
6. Add source:told tracking mechanic

**Relevant Context:** `jenny.md` Phases 5–6, `pybob.md` — absent

**Status:** [ ] pending

---

### Sub-Task 7 — Phase 7 + Python Module Library

**Intent:** The Amnesty Protocol (Phase 7) prevents shame-driven dropout after learning gaps. The Python Module Library is the deepest differentiator — per-module WHY architecture with bridges from prior knowledge, threshold nodes, false friends (cognitive traps), historical context, and industry anchors.

**Expected Outcomes:**
- Phase 7 Amnesty Protocol: no shame, capped review queue (5 today), 3 choices offered
- Module Library entries for: Module 0 (Foundations), Module 1 (Data Structures), Module 2 (Functions/Modules), Module 3 (OOP), Track 4A (Data Science), Track 4B (Web Dev), Track 4C (Automation), Game Track
- Each entry: Bridge, Threshold Nodes, False Friends (cognitive traps), Historical WHY, Industry Anchors

**Todo List:**
1. Write Phase 7 Amnesty Protocol (gap return, capped reviews, 3 choices, zero shame)
2. Write Module 0 Library entry (Bridge: everyday logic → code; Threshold: variables + functions; False Friends: assignment vs equality, mutable defaults; WHY: why indentation?)
3. Write Module 1 Library entry (Bridge: spreadsheet rows → lists; Threshold: dict comprehension; False Friends: list mutation traps; WHY: why immutable tuples?)
4. Write Module 2 Library entry (Bridge: recipe steps → functions; Threshold: scope/closure; False Friends: import traps; WHY: why modules?)
5. Write Module 3 Library entry (Bridge: real-world objects → classes; Threshold: __init__ and self; False Friends: class vs instance variable; WHY: why OOP?)
6. Write Track 4A/4B/4C Library entries (abbreviated: top threshold nodes + false friends + industry anchors)
7. Write Game Track Library entry for game_driven modality

**Relevant Context:** `jenny.md` lines 35–43 (Language Module Library), `pybob.md` — absent

**Status:** [ ] pending

---

### Sub-Task 8 — Depth Score Architecture + Scale Sections 7–17

**Intent:** Declare the Depth Score Architecture and then write all global scale sections (7–17) that take PyBob from a single-user mentor to a globally deployed learning system. This is the final assembly sub-task.

**Expected Outcomes:**
- Depth Score Architecture declared (13 named dimensions, total >= 94.7)
- Section 7: Node-level lesson script templates (structural, not word-for-word)
- Section 8: Certification and Badge system (4 tiers, exam protocol, shareable cert)
- Section 9: Multi-language localization (10 languages, code stays English, cultural anchors)
- Section 10: Accessibility mandates (screen_reader, dyslexia, adhd, motor_limited modes)
- Section 11: Under-18 safety and guardian mode
- Section 12: Career pathway and job role mapping (all 3 tracks, resume bullets, interview prep)
- Section 13: Enterprise learner track (learner_mode, cohort, 8-week sprint, manager digest)
- Section 14: Anti-hallucination and code safety guardrails (pre-flight checklist, approved library list, security anti-patterns)
- Section 15: Real-world project library (5 projects per track with rubrics)
- Section 16: Peer cohort mechanics (study buddy, weekly challenge, peer review template)
- Section 17: Human mentor escalation protocol (5 trigger categories, safe messaging, resource directory)
- Available Tools block: Read, Edit, Execute, MCP

**Todo List:**
1. Write Depth Score Architecture block (13 dimensions, point values, total)
2. Write Section 7: Node Lesson Script templates
3. Write Section 8: Certification system
4. Write Section 9: Localization protocol (10 languages)
5. Write Section 10: Accessibility modes
6. Write Section 11: Under-18 safety
7. Write Section 12: Career pathway maps
8. Write Section 13: Enterprise learner track
9. Write Section 14: Code safety guardrails
10. Write Section 15: Real-world project library
11. Write Section 16: Peer cohort mechanics
12. Write Section 17: Human escalation protocol
13. Assemble and write complete final `pybob.md` — all 8 sub-tasks integrated

**Relevant Context:** `jenny.md` line 44 (Depth Score), `pybob-plan.md` Sections 7–17 detail, `jenny.md` lines 46–50 (Available Tools format)

**Status:** [ ] pending

---

## Architecture Overview

```
PYBOB PRODUCTION SYSTEM — FULL LAYER MAP
──────────────────────────────────────────────────────────────────
ROLE DEFINITION        7 Mandates (Iron Rules) — non-negotiable
──────────────────────────────────────────────────────────────────
Phase 1: Diagnostic    5-question psychometric intake
Phase 2: Curriculum    Concept Map (Threshold nodes per module)
Phase 3: Teaching      6-step Socratic loop + PyBob Notes block
Phase 4: Assessment    Blind FSRS grading (Recalled/Partial/Lapsed)
Phase 5: Session Close Recap table + Progress Note + Homework
Phase 6: FSRS Export   Engram flashcard generation (3–5 nodes)
Phase 7: Amnesty       Gap-return protocol (zero shame, capped)
──────────────────────────────────────────────────────────────────
Module Library         Bridge + Threshold + False Friends + WHY
──────────────────────────────────────────────────────────────────
Depth Score            >= 94.7 (13 named dimensions)
──────────────────────────────────────────────────────────────────
Section 7:  Node Lesson Scripts
Section 8:  Certification and Badge System
Section 9:  Localization (10 languages)
Section 10: Accessibility Modes
Section 11: Under-18 Safety and Guardian Mode
Section 12: Career Pathway and Job Role Mapping
Section 13: Enterprise Learner Track
Section 14: Anti-Hallucination and Code Safety
Section 15: Real-World Project Library
Section 16: Peer Cohort Mechanics
Section 17: Human Mentor Escalation Protocol
──────────────────────────────────────────────────────────────────
```

---

## Architecture Decisions (Confirmed)

1. **Output target:** Write directly to `pybob.md` — replace current content entirely. Review at end only.
2. **Review cadence:** All 8 sub-tasks execute in one complete Agent pass. No incremental review.
3. **SQL/Data:** Track A (Data Science) includes pandas + SQL basics — PyBob teaches both. SqlBob is a separate mode for pure SQL learners.
4. **Localization:** Detect learner language automatically from first message. No explicit prompt needed.
5. **Game Track:** Receives the full 7-phase retention treatment — not a lighter supplement.
