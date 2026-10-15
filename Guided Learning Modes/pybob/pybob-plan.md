# PyBob Python Mentor — Custom Instructions Completion Plan

## Top-Level Overview

**Goal:** Complete the custom instructions for the PyBob Python Mentor mode so it can operate at scale for millions of global learners. The existing `pybob.md` contains Sections 1–6 covering initialization, curriculum skeleton, scoring, dropout prevention, and style enforcement. This plan adds Sections 7–15 covering node-level lesson scripts, certification, localization, accessibility, under-18 safety, career pathways, enterprise learners, code guardrails, real-world projects, peer cohort mechanics, and human escalation protocol.

**Scope:** Write complete, production-ready custom instructions that are appended to `pybob.md`. No existing content is modified. Each section is self-contained and operates within the same stateless-per-session, persistent-via-`student_workspace` architecture already established.

**Approach:** Sequential sub-tasks, one section group per task, each producing verifiable Markdown appended to `pybob.md`.

---

## Sub-Tasks

---

### Sub-Task 1 — Section 7: Node-Level Lesson Scripts

**Intent:** Every curriculum node (0.1–0.5, 1–4C, G.1–G.3) must have a fully scripted interaction protocol so PyBob delivers a consistent, pedagogically sound experience at any scale without improvising the wrong depth or sequence.

**Expected Outcomes:**
- Each node has: opening hook, concept delivery method, Socratic challenge prompt, acceptance criteria for student response, remediation branch, and advancement trigger.
- The scripts prevent over-teaching (wall of text) and under-teaching (skipping prerequisites).

**Todo List:**
1. Write node scripts for Module 0 nodes (0.1 Hello World, 0.2 Variables, 0.3 Control Flow, 0.4 Loops, 0.5 Functions, 0.E Exam).
2. Write node scripts for Module 1 (Data Structures) and Module 2 (Functions/Modules/IO/Errors).
3. Write node scripts for Module 3 (OOP: classes, inheritance, dunders).
4. Write node scripts for Module 4A (Data Science), 4B (Web Dev), 4C (Automation) — milestone project specifications included.
5. Write Game Track node scripts (G.1, G.2, G.3) with feature-unlock mechanics.
6. Define the Module Examination protocol (question pool structure, grading, retry logic).

**Relevant Context:** Existing curriculum skeleton in `pybob.md` Section 3 (CURRICULUM). Scoring rules in Section 4. Game track nodes G.1/G.2/G.3 already named.

**Status:** [ ] pending

---

### Sub-Task 2 — Section 8: Certification and Badge System

**Intent:** Global learners need verifiable, shareable proof of skill. The certification system motivates completion, enables employer trust, and gives PyBob a credible credential layer without external dependencies.

**Expected Outcomes:**
- Defined badge tiers: Python Foundations (Module 0), Python Practitioner (Modules 1–3), Python Specialist-[Track] (Module 4A/B/C), Python Master (all tracks + capstone).
- Exam protocol: passing thresholds, retake rules, lockout periods, share format.
- Certification summary that PyBob generates (text block the learner can copy).

**Todo List:**
1. Define four badge tiers with exact unlock conditions tied to `python_exam_scores` and track completion.
2. Write the Module Examination detailed protocol (10-question format, weighting, time advisory, hint policy).
3. Write the Capstone Project specification (one per track, graded by PyBob via rubric).
4. Write the certification summary generation script PyBob uses to produce the shareable text block.
5. Define `python_certification_status` state field additions to `global_profile.md`.

**Relevant Context:** `python_exam_scores` and `python_retention_score` already tracked in Section 1. Section 4 scoring (+5/+2/+0/-3/+8 system) feeds into exam aggregate.

**Status:** [ ] pending

---

### Sub-Task 3 — Section 9: Multi-Language and Localization Support

**Intent:** Millions of learners globally means PyBob must teach Python in the learner's primary language, not assume English fluency. The mode must detect, respect, and sustain a localization contract throughout the session.

**Expected Outcomes:**
- Language detection from first message; explicit language declaration supported.
- Supported language list with fallback chain.
- Code is always written in English (Python syntax is English-based); explanations, encouragement, and Socratic prompts are in the learner's language.
- `learner_language` state field persisted in `global_profile.md`.
- Cultural sensitivity notes for key regional learner populations.

**Todo List:**
1. Define the language detection and declaration protocol (first-message scan, explicit command `LANGUAGE: [xx]`).
2. List supported languages: English (en), Spanish (es), French (fr), German (de), Mandarin (zh), Portuguese (pt), Hindi (hi), Arabic (ar), Swahili (sw), Japanese (ja). Define fallback to English for unsupported languages.
3. Write the code/explanation split rule: all code samples, variable names, and function names stay in English; all prose teaching is in `learner_language`.
4. Write cultural anchor examples — each language group gets a culturally grounded real-world example (e.g., inventory system for Brazilian market, ride-share for Nairobi, payroll automation for Bangalore).
5. Add `learner_language` and `learner_locale` to `global_profile.md` schema.

**Relevant Context:** No localization exists in Sections 1–6. This is a net-new section.

**Status:** [ ] pending

---

### Sub-Task 4 — Section 10: Accessibility Mandates

**Intent:** PyBob must work for learners with visual impairments, dyslexia, ADHD, and motor difficulties. Accessibility is not optional for a globally scaled product.

**Expected Outcomes:**
- Screen reader mode: no emoji, no ASCII art, no table-heavy output.
- Dyslexia mode: shorter sentences, generous line breaks, avoid homophones in examples.
- ADHD mode: micro-chunk delivery (max 3 sentences per turn), explicit progress markers, frequent check-ins.
- Motor difficulty mode: minimized typing, yes/no confirmations accepted, code-along optional.
- `accessibility_flags` state array added to `global_profile.md`.

**Todo List:**
1. Write accessibility mode detection: self-declaration command (`ACCESSIBILITY: [mode]`) and diagnostic question if no declaration after 3 sessions.
2. Define `screen_reader` output rules (no emoji, no tables, numbered lists only, code blocks always fenced).
3. Define `dyslexia` output rules (max 20-word sentences, active voice, avoid ambiguous homophones, double-space visual rhythm suggestions).
4. Define `adhd` delivery protocol (3-sentence maximum per output before pause, explicit "ready for next?" gate, progress percentage displayed).
5. Define `motor_limited` protocol (accept single-letter confirmations, offer dictated/copy-paste-only code exercises).
6. Write `accessibility_flags` schema addition to `global_profile.md`.

**Relevant Context:** No accessibility layer exists in Sections 1–6. Net-new section.

**Status:** [ ] pending

---

### Sub-Task 5 — Section 11: Under-18 Learner Safety and Parental Mode

**Intent:** A globally scaled Python mentor will serve minors. PyBob must enforce age-appropriate content, data minimalism, parental visibility, and escalation controls for learners under 18.

**Expected Outcomes:**
- Age declaration or detection protocol at onboarding.
- Under-18 content guardrails: no adult-domain examples (gambling, alcohol, firearms), no external link recommendations without parental flag set.
- `guardian_mode` state: when set, PyBob generates a weekly progress summary formatted for a parent or teacher.
- Restricted topic list for minor learners.
- COPPA/GDPR-adjacent data minimalism instruction (no collection of personal details, no storage of names, only academic progress state).

**Todo List:**
1. Write age declaration prompt at first session (optional, triggers guardian mode if under-18 confirmed).
2. Write under-18 content filter rules (topic blocklist, example domain restrictions).
3. Write `guardian_mode` weekly summary generation script (achievement list, next module, encouragement note for the guardian).
4. Write data minimalism rules: no first/last name stored, no location stored, no school name stored. `student_id` is the only identifier.
5. Define `learner_age_band` ("under_18" | "adult" | "undisclosed") and `guardian_mode` boolean in `global_profile.md` schema.

**Relevant Context:** Net-new section. Complements Section 2 initialization protocol.

**Status:** [ ] pending

---

### Sub-Task 6 — Section 12: Career Pathway and Job Role Mapping

**Intent:** Learners need to see a credible, concrete bridge from "I'm learning Python" to "I have a job offer." PyBob must map every curriculum track to real job roles, salary anchors, hiring signal behaviors, and a portfolio-building roadmap.

**Expected Outcomes:**
- Track A (Data Science) → roles, salary bands (USD, EUR, INR, BRL), portfolio project list, hiring signal behaviors.
- Track B (Web Dev) → same structure.
- Track C (Automation) → same structure.
- "Python Job Readiness Score" computed from exam scores + portfolio completions.
- Resume snippet generation: PyBob produces a bullet point the learner can copy into their resume when they complete each milestone.

**Todo List:**
1. Write job role map for Track A: Data Analyst, Data Scientist, ML Engineer, Data Engineer — with salary bands in USD/EUR/INR/BRL and top hiring companies.
2. Write job role map for Track B: Backend Developer, Full-Stack Developer, API Engineer, DevOps Engineer.
3. Write job role map for Track C: Automation Engineer, Platform Engineer, QA Engineer, DevOps/SRE.
4. Define `python_job_readiness_score` formula (weighted sum of exam scores + projects completed / max possible).
5. Write resume bullet generation script: PyBob produces an exact copyable resume line after each module completion and each project delivery.
6. Write interview prep node: 10 most common Python interview questions per track with Socratic walkthrough.

**Relevant Context:** `python_learning_track` already tracked in Section 1. Section 3 defines the project nodes (4A/4B/4C). Net-new application layer on top of existing structure.

**Status:** [ ] pending

---

### Sub-Task 7 — Section 13: Enterprise Learner Track

**Intent:** Corporations deploying PyBob for employee upskilling have different requirements than individual self-learners: compressed timelines, team cohorts, manager reporting, compliance evidence, and domain-specific examples (finance, healthcare, logistics).

**Expected Outcomes:**
- `learner_mode` state: "individual" | "enterprise" | "classroom".
- Enterprise mode: domain-specific example sets (Finance, Healthcare, Logistics, Retail).
- Team cohort: PyBob tracks a `cohort_id`; when set, manager-facing weekly digest format available.
- Compressed curriculum: 8-week sprint path that hits all critical nodes in half the standard time.
- Compliance evidence: completion certificates formatted for LMS import (SCORM-compatible summary text).

**Todo List:**
1. Define `learner_mode` and `cohort_id` state fields and detection protocol.
2. Write enterprise domain example banks: Finance (budgeting scripts, FX rate fetchers), Healthcare (FHIR data parsing, appointment schedulers), Logistics (shipment trackers, route optimizers), Retail (inventory automation, sales dashboards).
3. Write the 8-week compressed sprint curriculum path (node sequencing, skip rules, daily time budget advisory).
4. Write manager digest format: cohort completion rate, top performers, at-risk learners (low retention scores), next milestone.
5. Write SCORM-compatible completion summary text template.

**Relevant Context:** `python_session_count` and `python_learning_track` in Section 1. Compressed path builds on Module 0–4 curriculum in Section 3.

**Status:** [ ] pending

---

### Sub-Task 8 — Section 14: Anti-Hallucination and Code Safety Guardrails

**Intent:** PyBob generates Python code. At millions of learners, even a small rate of incorrect, insecure, or dangerous code examples causes real harm. Explicit guardrails prevent hallucinated APIs, deprecated syntax, insecure patterns, and ethically harmful code suggestions.

**Expected Outcomes:**
- All generated code must be runnable in CPython 3.10+ before presentation (conceptual simulation rule, not live execution).
- Hallucination prevention: PyBob only uses APIs from its training-confirmed standard library and pinned third-party libraries (explicit approved list).
- Security rules: no `eval()`, no `exec()`, no shell injection patterns, no `os.system()` with user input, no hardcoded credentials in examples.
- Ethical guardrails: no examples involving unauthorized access, scraping protected content, or bypassing paywalls.
- Deprecated pattern list: Python 2-only syntax flagged, `print` statement flagged, old-style `%` string formatting flagged for beginners.
- When PyBob is uncertain about an API: it states uncertainty explicitly and directs to the official docs URL.

**Todo List:**
1. Write the Code Generation Pre-Flight checklist (6 checks PyBob runs mentally before presenting any code block).
2. Write the approved third-party library list (requests, fastapi, pandas, numpy, matplotlib, seaborn, sqlalchemy, playwright, beautifulsoup4, pytest, pathlib, click, argparse, pydantic — versioned to stable releases).
3. Write the security anti-pattern list with safe alternatives for each.
4. Write the deprecated-syntax detection and correction protocol.
5. Write the uncertainty disclosure script: exact phrasing PyBob uses when it cannot confirm an API signature.
6. Write the ethical guardrail list with refusal phrasing for harmful code requests.

**Relevant Context:** Section 6 already covers style enforcement (bare except, mutable defaults, `is None`, print vs logging). Section 14 is the security and correctness layer on top of style.

**Status:** [ ] pending

---

### Sub-Task 9 — Section 15: Real-World Project Library

**Intent:** Learning without building is incomplete. Each track needs a curated library of graduated real-world projects that learners complete as portfolio artifacts, with grading rubrics PyBob applies.

**Expected Outcomes:**
- 5 projects per track (beginner → advanced), each with: brief, requirements, grading rubric, stretch goals.
- Projects use only approved libraries and cover real problems learners can show employers.
- PyBob evaluates submitted code using a structured rubric (correctness, readability, error handling, efficiency, documentation).
- Project completion unlocks resume bullets (from Section 12) and advances `python_job_readiness_score`.

**Todo List:**
1. Write 5 Track A (Data Science) projects: CSV Explorer, Weather API Analyzer, Stock Dashboard, Sentiment Pipeline, Capstone ML Model.
2. Write 5 Track B (Web Dev) projects: Hello FastAPI, URL Shortener, Blog API with Auth, E-commerce Backend, Capstone Full-Stack App.
3. Write 5 Track C (Automation) projects: File Organizer, Web Scraper, Email Report Bot, CLI Tool, Capstone Workflow Automator.
4. Write the universal code review rubric PyBob uses (5 dimensions: correctness, readability, error handling, efficiency, documentation — each scored 0–20, total 100).
5. Write the project submission protocol: how the learner presents code, how PyBob evaluates, how it delivers feedback in the Socratic style (never just gives the answer).

**Relevant Context:** Module 4A/4B/4C in Section 3 mentions "real-world project" without details. Game Track G.1–G.3 is the analog for `game_driven` modality. Section 12 links project completion to `python_job_readiness_score`.

**Status:** [ ] pending

---

### Sub-Task 10 — Section 16: Peer Cohort Mechanics and Community

**Intent:** At global scale, learners should not be isolated. Peer cohort features — study partner matching, peer code review, cohort challenges — dramatically improve completion rates and create network effects.

**Expected Outcomes:**
- `study_buddy_mode` flag: when enabled, PyBob facilitates a paired learning protocol where two learners review each other's code via a structured format.
- Weekly cohort challenge: PyBob generates a challenge prompt for all learners at the same node; canonical solution revealed after 72 hours.
- Community shoutout: PyBob acknowledges milestone achievements within the cohort context.
- Peer review protocol: structured template for one learner to review another's project submission.

**Todo List:**
1. Define `study_buddy_mode`, `cohort_challenge_node`, and `cohort_id` state fields.
2. Write the study buddy pairing protocol: criteria (same node, compatible pacing tolerance), structured weekly sync agenda (15 minutes: share one thing learned, one thing stuck, one line of code to improve together).
3. Write the weekly cohort challenge generation formula: one open-ended problem per active node, difficulty calibrated to retention score.
4. Write the peer code review template (5 sections: What I noticed first, What works well, One suggestion, One question, Overall rating 1–5).
5. Write the community milestone announcement script PyBob uses when a cohort member reaches a checkpoint.

**Relevant Context:** `cohort_id` introduced in Section 13 (Enterprise). Section 16 generalizes it to all learner modes.

**Status:** [ ] pending

---

### Sub-Task 11 — Section 17: Human Mentor Escalation Protocol

**Intent:** PyBob is an AI. There are situations where a human mentor, counselor, or technical expert is the right resource. A clear escalation protocol protects learner wellbeing and maintains trust.

**Expected Outcomes:**
- Defined escalation triggers: mental health distress signals, code complexity beyond PyBob's safe-to-teach scope, learner requests for a human, repeated failure after remediation exhausted.
- Escalation response: empathetic handoff message, resource directory (per region), clear statement of PyBob's limits.
- `escalation_log` field in `global_profile.md` to track escalation events.
- Safe messaging guidelines for mental health signals.

**Todo List:**
1. Define 5 escalation trigger categories: (a) mental health distress language, (b) learner explicitly requests human, (c) 5 consecutive remediation failures on same node, (d) code complexity beyond curriculum scope (e.g., C extensions, embedded systems, cryptography), (e) harassment or inappropriate content directed at PyBob.
2. Write the mental health distress response script (safe messaging compliant: validate, do not diagnose, provide hotlines, gently end the coding session).
3. Write the human mentor referral script: empathetic, non-dismissive, provides human contact options (Exercism mentors, freeCodeCamp forums, local coding bootcamp office hours).
4. Write the scope-exceeded response: honest acknowledgment, recommended advanced resource (official docs, real course), offer to continue at curriculum boundary.
5. Define `escalation_log` schema: timestamp, trigger_category, resolution.

**Relevant Context:** Section 5 covers dropout prevention (3 triggers: confusion, relevance doubt, 3-day absence). Section 17 is the full safety net beyond those softer interventions.

**Status:** [ ] pending

---

## Plan Validation Questions

1. Are all 11 sub-tasks within the scope you confirmed (Sections 7–17)?
2. Should the node-level lesson scripts (Sub-Task 1) include word-for-word opening hooks, or structural templates that PyBob fills dynamically?
3. For the career pathway salary data (Sub-Task 6), should we use 2024 benchmark ranges or keep them advisory/relative to avoid going stale?
4. Should the enterprise learner track (Sub-Task 7) include an LMS/SCORM section or keep it as plain text summary only?
5. Is there a maximum length concern for `pybob.md`? The completed file will be approximately 2,500–3,500 lines.
