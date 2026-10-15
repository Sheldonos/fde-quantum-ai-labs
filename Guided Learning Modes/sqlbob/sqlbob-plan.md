# SqlBob Custom Instructions — Full Scale Plan

## Top-Level Overview

**Goal:** Complete and harden the SqlBob Database Mentor custom instructions to match PyBob's production quality, then extend it with scale-specific architecture for millions of global learners across dialects, locales, and job tracks.

**Scope:** `sqlbob.md` — the custom instructions block only. No changes to role name, mode ID, scope, or when-to-use triggers.

**Approach:** Use `pybob.md` as the reference implementation. Systematically close every gap, then add three SqlBob-specific extensions that PyBob does not need: Dialect Routing, Platform/Environment Guidance, and Global Scale Architecture.

---

## Sub-Tasks

---

### Sub-Task 1 — Harden Role Definition to PyBob Parity

**Intent:** The role definition in SqlBob is missing three behavioral contracts that PyBob carries explicitly: the celebration phrase contract, the mid-sentence correction rule, and the energy-reading/acceleration/deceleration instruction. Without these, the mentor behavior is inconsistent at scale — different LLM instances interpret the role differently.

**Expected Outcomes:**
- Role definition includes an explicit celebration phrase example (parallel to PyBob's "That is a genuinely clever approach…")
- Role definition includes the rule that SqlBob never corrects mid-sentence — lets the student finish, acknowledges what was right, then precisely addresses what was off
- Role definition includes the energy-reading acceleration/deceleration clause
- No existing content is removed or weakened

**Todo List:**
1. After the first TONE AND PRESENCE sentence, add the explicit celebration phrase example
2. After the "never lecture at length" clause, insert the mid-sentence correction prohibition
3. After the "check in" clause, insert the energy-reading + acceleration/deceleration contract
4. Verify the three new clauses are word-for-word defensible against millions of concurrent learners at varying pacing needs

**Relevant Context:** `pybob.md` lines 12–13 (TONE AND PRESENCE and NON-INTRUSIVE TEACHING sections)

**Status:** `[ ] pending`

---

### Sub-Task 2 — Add PROFICIENCY ASSESSMENT MANDATE Section

**Intent:** PyBob has a dedicated `PROFICIENCY ASSESSMENT MANDATE` section that specifies the 3-question proficiency check, the four levels (none/beginner/intermediate/advanced), and the routing logic per level. SqlBob's equivalent is buried inside SECTION 2 STEP 1.2 without a standalone mandate. At scale this creates ambiguity — the diagnostic may be skipped or inconsistently applied.

**Expected Outcomes:**
- A standalone `PROFICIENCY ASSESSMENT MANDATE` paragraph added to the role definition block (between HISTORICAL REASONING MANDATE and FUTURE VISION MANDATE)
- Specifies 3 friendly SQL proficiency questions (SQL-Q1/Q2/Q3)
- Defines the four levels: none, beginner, intermediate, advanced
- Specifies routing: none/beginner → Module 0; intermediate → condensed review; advanced → skip Module 0
- States that the check is run at the start of every first session

**Todo List:**
1. Draft SQL-Q1 (conceptual: "Have you ever opened a spreadsheet and tried to filter or sort data?")
2. Draft SQL-Q2 (syntax: "Have you ever written or seen a SELECT statement before?")
3. Draft SQL-Q3 (applied: "Have you ever tried to combine data from two different tables or sheets?")
4. Write the PROFICIENCY ASSESSMENT MANDATE block with level-to-node routing table
5. Insert after HISTORICAL REASONING MANDATE in the role definition

**Relevant Context:** `pybob.md` line 16 (PROFICIENCY ASSESSMENT MANDATE)

**Status:** `[ ] pending`

---

### Sub-Task 3 — Add FUTURE VISION MANDATE Section

**Intent:** PyBob has an explicit `FUTURE VISION MANDATE` that tells the mentor to connect every concept to a real problem the student could solve, treating them as a future builder. SqlBob's current instructions mention connecting to business questions but it is not a standalone mandate, so it is easily dropped under instruction compression.

**Expected Outcomes:**
- A standalone `FUTURE VISION MANDATE` paragraph added after PROFICIENCY ASSESSMENT MANDATE
- States that every concept must be anchored to a real business question the student could not answer before
- Explicitly positions SQL as the entry point to AI/ML pipelines, data engineering, and executive decision-making
- Treats the student as a future data professional, not a passive consumer

**Todo List:**
1. Write the FUTURE VISION MANDATE block
2. Add three specific anchoring examples: "you could now answer your manager's question about which region had the highest revenue last quarter", "you could now build the dataset your data science team needs", "every AI model you will ever encounter starts with a SQL query"
3. Insert after PROFICIENCY ASSESSMENT MANDATE in role definition

**Relevant Context:** `pybob.md` line 18 (FUTURE VISION MANDATE); `sqlbob.md` line 17 (buried future vision language)

**Status:** `[ ] pending`

---

### Sub-Task 4 — Complete Learning Modality Mandate with Platform Guidance

**Intent:** SqlBob's `LEARNING MODALITY MANDATE` defines the four modalities but is missing: (1) specific platform/resource recommendations for `video_first`, (2) a zero-setup browser IDE recommendation for `game_driven` and `hands_on_only` learners, and (3) explicit `hands_on_only` flow logic. At scale, learners who cannot install a local database must have a clear path to a working environment immediately.

**Expected Outcomes:**
- `video_first` modality lists: Mode Analytics SQL series, then Khan Academy SQL, then official PostgreSQL docs with timestamps (already present — verify it is complete)
- `game_driven` modality adds: recommendation to use DB Fiddle (https://dbfiddle.uk) or SQLiteOnline (https://sqliteonline.com) for zero-setup browser SQL execution alongside the mystery game
- `hands_on_only` modality adds: explicit flow — provide a working query against the course dataset immediately, explain every clause backward from the result set, no preamble
- All four modalities documented with equal depth

**Todo List:**
1. Verify video_first resources are complete in current instructions
2. Add DB Fiddle and SQLiteOnline recommendations to game_driven section
3. Write hands_on_only flow logic explicitly (start with working query → explain backward from result)
4. Add DB Fiddle/SQLiteOnline as default zero-setup recommendation for all modalities during onboarding

**Relevant Context:** `sqlbob.md` lines 14 (LEARNING MODALITY MANDATE); `pybob.md` line 14 (Replit recommendation for game_driven)

**Status:** `[ ] pending`

---

### Sub-Task 5 — Expand Module 0 with Granular Node Breakdown

**Intent:** PyBob's Module 0 has 5 named nodes (0.1–0.5) plus the exam node (0.E). SqlBob's Module 0 is a flat list of topics without node granularity. At scale, granular nodes are critical: they allow precise state persistence in `global_profile.md`, enable targeted remediation, and let returning students resume at the exact node they left — not just "somewhere in Module 0".

**Expected Outcomes:**
- Module 0 broken into named nodes: 0.1 through 0.5 (or equivalent for SQL) plus 0.E
- Each node has a single learning objective
- Node numbers match what is stored in `sql_current_loop_node` in SECTION 1
- The exam node (0.E) retains its existing pass threshold (>= 70, bonus >= 90)

**Proposed node breakdown:**
- Node 0.1 — What is a Database? (tables, rows, columns, relational model, Codd 1970 hook)
- Node 0.2 — Your First Query: SELECT and FROM
- Node 0.3 — Filtering with WHERE and ORDER BY
- Node 0.4 — Column Aliases and DISTINCT
- Node 0.5 — Aggregation Preview: COUNT(*) and the shape of a result set
- Node 0.E — Module Examination (pass >= 70, bonus >= 90)

**Todo List:**
1. Write the six nodes for Module 0 with the above objectives
2. Verify node IDs align with `sql_current_loop_node` state field
3. Insert expanded Module 0 into SECTION 3 curriculum, replacing the current flat description
4. Ensure game_driven track G.1 maps to Module 0/1 boundary

**Relevant Context:** `sqlbob.md` lines 31–41 (SECTION 3); `pybob.md` lines 32–39 (MODULE 0 node breakdown)

**Status:** `[ ] pending`

---

### Sub-Task 6 — Add SECTION 7: SQL Dialect Routing

**Intent:** Unlike Python (one language), SQL has six major production dialects: standard SQL/PostgreSQL, MySQL/MariaDB, SQLite, Google BigQuery, Snowflake, and Microsoft T-SQL (SQL Server). Each has syntax differences that cause real errors for learners. PyBob has no equivalent section — this is a SqlBob-specific requirement. At scale, a learner using BigQuery who receives PostgreSQL-specific window function syntax will fail, lose confidence, and drop out. T-SQL is heavily used in enterprise environments and must be a first-class supported dialect.

**Expected Outcomes:**
- New SECTION 7 added to custom instructions
- Dialect detection: ask once at onboarding "Which SQL environment are you using or learning toward?" with options: PostgreSQL (default), MySQL, SQLite, BigQuery, Snowflake, Microsoft T-SQL/SQL Server, "Not sure yet"
- Dialect stored as `sql_dialect` in `global_profile.md`
- Dialect-specific notes surface at the point of instruction (not as a wall of upfront text)
- Key dialect divergence points documented across all six: LIMIT vs TOP vs FETCH FIRST, date functions, string concatenation (|| vs CONCAT vs +), ISNULL/COALESCE/NVL/IFNULL, window function support, WITH clause support, T-SQL-specific constructs (BEGIN/END blocks, NOCOUNT, GO delimiter, PRINT statement)
- "Not sure yet" students receive PostgreSQL by default with a note that it is the most portable

**Todo List:**
1. Write the dialect detection onboarding question and mapping logic for all six dialects
2. Add `sql_dialect` to the SECTION 1 persistent memory key state list
3. Document all six dialects' major divergence points with inline dialect flags
4. Write the rule: always flag dialect-specific syntax inline as "PostgreSQL syntax — if you are using T-SQL/SQL Server, this becomes X"
5. Write the full SECTION 7 block covering all six dialects

**Relevant Context:** No equivalent in `pybob.md` — new section specific to SQL

**Status:** `[ ] pending`

---

### Sub-Task 7 — Add SECTION 8: Global Scale Architecture

**Intent:** PyBob and SqlBob are designed for millions of learners globally. Neither file currently addresses scale-specific constraints that affect correctness at that volume: state isolation between learners, locale/language accessibility, cohort and cohort-leader routing, exam integrity at scale, and bandwidth-sensitive learner support. This section defines the operating constraints the mentor must respect to function correctly at scale.

**Expected Outcomes:**
- New SECTION 8 added to custom instructions
- State isolation rule: `global_profile.md` is per-learner; the mentor never references or reveals another learner's state
- Language support: English default. If the learner explicitly requests Spanish, French, Portuguese, or Mandarin, SqlBob switches fully to that language for all instructional prose. SQL keywords are always shown in English first, with the translation in parentheses at first use per session (e.g. "SELECIONAR (SELECT) as colunas..."). The language preference is persisted as `sql_language` in `global_profile.md`.
- Cohort support: if `sql_cohort_id` is present in global_profile.md, surface cohort-relevant challenges (same dataset, same business scenario) to build shared vocabulary across teams
- Exam integrity: never reveal examination questions in advance; never confirm whether a response is "the expected answer" — only evaluate correctness and give Socratic follow-up
- Bandwidth-sensitive learners: if `connection_quality` is "low" in global_profile.md, suppress large code blocks in favor of line-by-line teaching; avoid embedding links unless requested
- Mobile-first flag: if `device_type` is "mobile", keep code examples under 5 lines per exchange; use shorter query patterns

**Todo List:**
1. Define seven scale constraints as enumerated rules (language support as rule 1, state isolation as rule 2, cohort as rule 3, exam integrity as rule 4, bandwidth as rule 5, mobile as rule 6, dialect as rule 7)
2. Add `sql_cohort_id`, `connection_quality`, `device_type`, and `sql_language` to the SECTION 1 persistent memory key state list (optional fields; `sql_language` defaults to "en")
3. Write the language switching logic: detect explicit request, confirm once, persist to `sql_language`, apply to all subsequent responses in that session and future sessions
4. Write the SQL keyword bilingual format rule: English keyword always primary, translation in parentheses at first use per session only (not on every occurrence)
5. Write the full SECTION 8 block
6. Verify no existing section conflicts with the new constraints

**Relevant Context:** No equivalent in either file — new section for global scale

**Status:** `[ ] pending`

---

### Sub-Task 8 — Final Assembly and Consistency Audit

**Intent:** After all sub-tasks are applied, the full custom instructions block must be read end-to-end to verify: no duplicate content, no contradictory rules, all section numbers are sequential, all state keys referenced in sections 2–8 are declared in SECTION 1, and the document reads as a coherent single-author instruction set.

**Expected Outcomes:**
- SECTION 1 key state list includes all fields added in sub-tasks 6 and 7: `sql_dialect`, `sql_language`, `sql_cohort_id`, `connection_quality`, `device_type`
- All section numbers sequential: 1–8
- No instruction in sections 2–8 contradicts the role definition
- SECTION 3 curriculum node numbers match `sql_current_loop_node` state field values
- Style is consistent with PyBob (imperative, present-tense, no passive voice in behavioral rules)
- Document is self-contained — no forward references to undefined terms

**Todo List:**
1. Read the assembled sqlbob.md end-to-end
2. Audit SECTION 1 key state list against all section references
3. Verify section numbering 1–8
4. Check for contradictions between role definition behavioral rules and section-level rules
5. Standardize imperative voice across all sections
6. Write final version to sqlbob.md

**Relevant Context:** Full assembled `sqlbob.md` after sub-tasks 1–7

**Status:** `[ ] pending`

---

## Implementation Notes

- All changes target the **Custom instructions** block of `sqlbob.md` only
- The Role definition block and Custom instructions block are both in scope (role definition gaps are fixed in sub-tasks 1–3)
- PyBob is the style reference — when in doubt, match PyBob's phrasing pattern
- Each sub-task produces a self-contained, reviewable diff
- Sub-tasks 1–5 are parity work (closing gaps vs PyBob); sub-tasks 6–8 are SqlBob-specific extensions
