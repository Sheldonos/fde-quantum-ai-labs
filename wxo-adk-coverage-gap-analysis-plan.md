# WxO ADK Coverage Gap Analysis & Remediation Plan

**Date:** 2026-08-12
**Scope:** Compare Lessons/ + wxo-adk-package 2/ against official docs site + GitHub repo
**Sources checked:**
- `Lessons/wxo/adk/` (10 source files)
- `wxo-adk-package 2/` (8 skills, 3 modes, onboarding guide, engineering audit)
- `github/ibm-watsonx-orchestrate-adk-main/` (README, examples/*, src/)
- Official docs: `https://developer.watson-orchestrate.ibm.com/`

---

## Executive Summary

The package covers the core ADK build loop well. Seven clearly scoped gaps were identified against the official documentation, GitHub examples, and the CLI's own `--help` output. Three are **medium priority** (missing knowledge bases skill, channels/voice skill, evaluations skill). Three are **low priority** (stale CLI commands in the vibe coder mode, incomplete LLM model list in agent-build, missing `orchestrate partners` CLI coverage). One **structural issue** exists in the onboarding guide (uses deprecated `style: default` in the Hello World example).

---

## Gap Inventory

### GAP-01 — Knowledge Bases: No dedicated skill (MEDIUM)

**Source evidence:** `Lessons/wxo/adk/adk.md` lists Knowledge Bases as a core ADK component. The official docs menu has a full "Knowledge Bases" section covering creation, indexing, OpenSearch/Elasticsearch schemas, credential validation (new in 2.14.0), and dynamic input/output schemas (new in 2.10.0). The GitHub repo has `examples/agent_builder/ibm_knowledge/` with a full knowledge base YAML + agent.

**What we have:** Agent-build skill mentions `knowledge: [hr_policy_kb]` in an agent YAML example and Module 1 Node 1.4 in the learn mode. There is no `wxo-adk-knowledge` skill.

**Gap:** No skill covers the `orchestrate knowledge-bases import/list/export/delete` CLI commands, the knowledge base YAML spec (`ibm_knowledge_base.yaml`), OpenSearch/Elasticsearch index configuration, dynamic input/output schema (new 2.10.0), or credential validation (new 2.14.0).

**Files affected:** Add new `wxo-adk-knowledge/SKILL.md`; update vibe mode routing table.

---

### GAP-02 — Channels & Voice: No dedicated skill (MEDIUM)

**Source evidence:** `Lessons/wxo/adk/build/agentdesign.md` lists Channels. `Lessons/wxo/adk/whats_new.md` covers channel support from v2.1.0 through v2.14.0. The GitHub repo has `examples/channel-integrations/` with 7 channel types (Slack, Teams, Facebook Messenger, Twilio SMS, Twilio WhatsApp, SIP phone, Genesys Bot Connector, Genesys Audio Connector) and `examples/agent_builder/voice_enabled_*/` with 4 voice providers (Deepgram, ElevenLabs, Google, Watson). The CLI `--help` output shows `channels` and `phone` as top-level commands.

**What we have:** `wxo-adk-troubleshoot` notes that OAuth connections are limited to the web chat UI. The learn mode Module 2 Node 2.7 mentions "form tools, file tools" but not channels. No skill covers channels or voice configs.

**Gap:** No coverage of `orchestrate channels` commands, `orchestrate voice-configs` commands, channel YAML specs (Slack, Teams, Facebook, Twilio SMS/WhatsApp, Genesys), phone/SIP trunk YAML specs, or voice provider configuration (Deepgram STT/TTS, ElevenLabs TTS, Google TTS new in 2.14.0, Watson).

**Files affected:** Add new `wxo-adk-channels-voice/SKILL.md`; update vibe mode routing table.

---

### GAP-03 — Evaluations Framework: No dedicated skill (MEDIUM)

**Source evidence:** `Lessons/wxo/adk/whats_new.md` covers evaluation framework additions from v2.1.0 through v2.14.0. The GitHub repo has a full `examples/evaluations/` with 13 test categories: basic evaluation, non-legacy mode, context variable evaluation, file upload evaluation, record chat sessions, generate test cases from stories, analysis, red-teaming (plan/run), native agent validation, external agent validation, and quick-eval. The CLI `--help` output shows `evaluations` as a top-level command group.

**What we have:** `wxo-adk-agentops` mentions rubric evaluations (LLM-as-judge, new in 2.9.0) and `orchestrate evaluations run --config evaluation_config.yaml`. This covers only the rubric sub-system.

**Gap:** The full `orchestrate evaluations` command group is much larger: `evaluate`, `record`, `generate`, `analyze`, `validate-native`, `validate-external`, `quick-eval`, and `red-teaming`. Test case format (`.json`), stories CSV format, environment manager pattern, and evaluation with context variables and file uploads are all undocumented in the package.

**Files affected:** Expand `wxo-adk-agentops/SKILL.md` with evaluations section OR add `wxo-adk-evaluations/SKILL.md`.

---

### GAP-04 — Vibe Coder Mode: Stale CLI Commands (LOW-STRUCTURAL)

**Source evidence:** `wxo-adk-package 2/modes/wxo-adk-vibe.yaml` Rule 4 lists CLI commands including `orchestrate agents publish -f agent.yaml`, `orchestrate tools publish -f tools.py`, `orchestrate app run`, and `orchestrate agentops traces list`. These are not valid ADK 2.14.0 CLI commands.

**Correct commands (from README, source files, and audit):**
- `orchestrate agents import -f agent.yaml` (not `publish`)
- `orchestrate tools import -k python -f tools.py` (not `publish`)
- `orchestrate server start -e .env` (not `app run`)
- `orchestrate observability traces search` (not `agentops traces list`)

**Impact:** A user copying vibe coder output would get CLI errors. This contradicts the engineering audit's "100% correct CLI commands" finding, which did not read the vibe mode YAML carefully.

**Files affected:** `wxo-adk-package 2/modes/wxo-adk-vibe.yaml` — Rule 4 and Pre-Flight Checklist.

---

### GAP-05 — Onboarding Guide: Deprecated Agent Style in Hello World Example (LOW-STRUCTURAL)

**Source evidence:** `wxo-adk-package 2/wxo-adk-onboarding-guide.md` Phase 6 Step 3 shows a Hello World `agent.yaml` with `style: default`. This style was deprecated in ADK 2.13.0 and is no longer supported.

**Impact:** New teammates following the onboarding guide will get a deprecation warning or error on import.

**Files affected:** `wxo-adk-package 2/wxo-adk-onboarding-guide.md` Phase 6, Step 3.

---

### GAP-06 — Agent Build Skill: LLaMA and Mistral Models Missing (LOW)

**Source evidence:** Engineering audit W-01 already identified this. `wxo-adk-package 2/skills/wxo-adk-agent-build/SKILL.md` LLM examples include groq, granite, bedrock, openai, red_hat_ai, gemini but not LLaMA or Mistral. The vibe mode (Rule 9) lists `meta-llama/llama-3-3-70b-instruct` and `mistralai/mistral-large` but under the wrong provider prefix — they should be `watsonx/meta-llama/llama-3-3-70b-instruct` and `watsonx/mistralai/mistral-large`.

**Files affected:** `wxo-adk-package 2/skills/wxo-adk-agent-build/SKILL.md` LLM field options section.

---

### GAP-07 — Partners CLI Command: No coverage (LOW)

**Source evidence:** The GitHub README CLI `--help` output shows `partners` as a top-level command: "Generate a well-structured, submission-ready agent artifact package for partner-built agents." This CLI command group is not covered in any skill, mode, or lesson file.

**Gap:** No coverage of `orchestrate partners` for partner-built agent artifact packaging.

**Files affected:** Could be added as a note to `wxo-adk-tutorials/SKILL.md` or as a brief addition to `wxo-adk-agent-build/SKILL.md`.

---

## Previously Identified Warnings (from engineering-audit.md) — Status

| Warning | Status |
|---|---|
| W-01: LLaMA/Mistral models missing from agent-build | Confirmed — documented as GAP-06 above |
| W-02: AsyncOpenAPI SaaS vs Dev Edition not distinguished | Still open — not yet fixed |
| W-03: Conversation compaction trigger guidance missing | Still open — not yet fixed |

---

## What Is Already Well-Covered (No Action Needed)

| Domain | Coverage | Notes |
|---|---|---|
| Installation & env setup | ✅ Complete | install-setup skill + onboarding guide (except GAP-05) |
| Agent YAML spec | ✅ Complete | agent-build skill covers all fields and anti-patterns |
| Python tools | ✅ Complete | tools-build skill with thread safety |
| OpenAPI tools | ✅ Complete | timeout rules, operationId requirements |
| MCP toolkits | ✅ Complete | CM-REFRESH-TOKEN-FAILED-001 fix, HTTP 431 fix |
| Python toolkits | ✅ Complete | new in 2.8.0, bundling pattern |
| Connections | ✅ Complete | all 4 connection kinds, draft/live pattern |
| Agentic workflows | ✅ Complete | all 8 node types, callbacks, masking, scheduling |
| LangGraph agents | ✅ Complete | custom kind, checkpointers, context vars |
| Workspaces | ✅ Complete | IBM Cloud only, all CLI commands |
| AgentOps traces | ✅ Complete | CLI + Python TracesController |
| Langfuse | ✅ Complete | configure, get, remove |
| Rubric evaluations | ✅ Partial | covered in agentops skill (full eval CLI not covered — GAP-03) |
| OTEL export | ✅ Complete | new in 2.14.0 |
| Troubleshooting | ✅ Complete | all known issues covered |
| Tutorials | ✅ Complete | Hello World + Empower multi-agent |
| Agent anti-patterns | ✅ Complete | covered in agentdesign.md and agent-build skill |
| Deprecated styles guard | ✅ Complete | all 3 modes enforce react_core |
| ADK version gate | ✅ Complete | 2.14.0 enforced in mentor and vibe modes |
| Scheduling | ✅ Complete | agents and flows, new in 2.11.0 |
| Agent skills (portable packages) | ✅ Mentioned | new in 2.13.0, in whats_new.md |
| FedRAMP GovCloud activation | ✅ Complete | fedramp_activate script in install-setup |
| Developer Edition | ✅ Complete | start, stop, reset, doc-processing, telemetry flags |

---

## Sub-Tasks

---

### TASK-01: Fix Deprecated Style in Onboarding Guide

**Intent:** Remove the deprecated `style: default` from the Hello World agent YAML in the onboarding guide. This is a structural correctness issue that will cause errors for new teammates on ADK 2.13.0+.

**Expected Outcomes:**
- `wxo-adk-onboarding-guide.md` Phase 6 Step 3 uses `style: react_core`
- No deprecated agent style exists anywhere in the onboarding guide

**Todo List:**
1. Open `wxo-adk-package 2/wxo-adk-onboarding-guide.md`
2. Find the Hello World `agent.yaml` block in Phase 6, Step 3 (around line 251-261)
3. Change `style: default` to `style: react_core`
4. Verify no other deprecated styles (`react`, `planner`, `default`) appear in the file

**Relevant Context:** `wxo-adk-package 2/wxo-adk-onboarding-guide.md` lines ~251-262

**Status:** [x] done — `style: default` replaced with `style: react_core` in Phase 6 Step 3. No other deprecated styles found.

---

### TASK-02: Fix Stale CLI Commands in Vibe Coder Mode

**Intent:** Replace four stale CLI commands in `wxo-adk-vibe.yaml` Rule 4 and the Pre-Flight Checklist with the correct ADK 2.14.0 commands. This prevents users from getting CLI errors when copying vibe coder output.

**Expected Outcomes:**
- `orchestrate agents publish` replaced with `orchestrate agents import`
- `orchestrate tools publish` replaced with `orchestrate tools import -k python`
- `orchestrate app run` replaced with `orchestrate server start -e .env`
- `orchestrate agentops traces list` replaced with `orchestrate observability traces search`
- Pre-Flight Checklist updated to reflect correct commands

**Todo List:**
1. Open `wxo-adk-package 2/modes/wxo-adk-vibe.yaml`
2. In SECTION 3 Rule 4, replace all four stale commands with correct ADK 2.14.0 equivalents
3. In SECTION 4 OUTPUT FORMAT, update the Publish Sequence block
4. Update Pre-Flight Checklist to use `orchestrate server start -e .env` not `orchestrate app run`
5. Verify the Smoke Test section references correct UI navigation (Agent Builder, not Studio)

**Relevant Context:** `wxo-adk-package 2/modes/wxo-adk-vibe.yaml` SECTION 3 (lines ~59-70) and SECTION 4 (lines ~99-128)

**Status:** [x] done — All 4 stale commands replaced. LLaMA/Mistral provider prefix fixed to `watsonx/` in Rule 9. Publish Sequence and Pre-Flight Checklist updated.

---

### TASK-03: Add LLaMA + Mistral to Agent-Build LLM Examples

**Intent:** Add the two most common watsonx-hosted open-source LLM options to the LLM field examples in the agent-build skill, fixing engineering audit W-01.

**Expected Outcomes:**
- `watsonx/meta-llama/llama-3-3-70b-instruct` appears as a documented LLM option
- `watsonx/mistralai/mistral-large` appears as a documented LLM option
- LLaMA known limitation (array-of-strings bug) is cross-referenced

**Todo List:**
1. Open `wxo-adk-package 2/skills/wxo-adk-agent-build/SKILL.md`
2. In the LLM FIELD OPTIONS section, add the two LLaMA/Mistral entries
3. Add a note: "LLaMA models: do not pass arrays of strings as tool arguments (converts to single string — see known issue in troubleshoot skill)"
4. Also fix the vibe mode Rule 9 model list to use the correct `watsonx/` provider prefix

**Relevant Context:** `wxo-adk-package 2/skills/wxo-adk-agent-build/SKILL.md` lines ~53-65; `wxo-adk-package 2/modes/wxo-adk-vibe.yaml` Rule 9 lines ~84-91

**Status:** [x] done — `watsonx/meta-llama/llama-3-3-70b-instruct` and `watsonx/mistralai/mistral-large` added with ⚠️ LLaMA array-of-strings warning. Vibe mode Rule 9 provider prefix corrected.

---

### TASK-04: Add Conversation Compaction Trigger Guidance

**Intent:** Add when-to-enable guidance for `conversation_compaction` in the agent-build skill, fixing engineering audit W-03.

**Expected Outcomes:**
- Agent-build skill explains when to enable conversation compaction (conversation length threshold, context window warning)
- Agent-build skill cross-references AgentOps traces for monitoring

**Todo List:**
1. Open `wxo-adk-package 2/skills/wxo-adk-agent-build/SKILL.md`
2. In the CONVERSATION COMPACTION section, add trigger guidance: "Enable when conversations regularly exceed 20 messages or when token usage approaches the LLM's context window limit. Monitor via traces in AgentOps to identify when compaction is triggering."
3. Add guidance on the `max_messages` setting trade-off (lower = more aggressive compression, higher = more context retained)

**Relevant Context:** `wxo-adk-package 2/skills/wxo-adk-agent-build/SKILL.md` lines ~161-168

**Status:** [x] done — When-to-enable guidance and `max_messages` trade-off paragraph added after the compaction YAML block.

---

### TASK-05: Add AsyncOpenAPI SaaS vs Dev Edition Distinction to AgentOps Skill

**Intent:** Clarify in the agentops skill that SaaS environments do not require ngrok for async callbacks, fixing engineering audit W-02.

**Expected Outcomes:**
- `wxo-adk-agentops/SKILL.md` explicitly states: SaaS async callbacks use publicly reachable endpoints — no ngrok required
- Developer Edition async callback ngrok requirement cross-referenced to troubleshoot skill

**Todo List:**
1. Open `wxo-adk-package 2/skills/wxo-adk-agentops/SKILL.md`
2. In the AVAILABILITY NOTES section, add: "Async OpenAPI callbacks: In SaaS environments, callback endpoints must be publicly reachable — ngrok is not required because SaaS is not local. In Developer Edition, use ngrok to expose the local callback endpoint (see wxo-adk-troubleshoot skill for details)."

**Relevant Context:** `wxo-adk-package 2/skills/wxo-adk-agentops/SKILL.md` lines ~245-251

**Status:** [x] done — SaaS (no ngrok) vs Developer Edition (ngrok required) distinction added to AVAILABILITY NOTES.

---

### TASK-06: Create wxo-adk-knowledge Skill

**Intent:** Create a dedicated skill for knowledge bases — the only core ADK building block with no corresponding skill. Covers KB creation, indexing, CLI management, and the OpenSearch/Elasticsearch schema patterns from the official docs.

**Expected Outcomes:**
- New file `wxo-adk-package 2/skills/wxo-adk-knowledge/SKILL.md` exists and is complete
- Covers: `orchestrate knowledge-bases import/list/export/update/delete` CLI commands
- Covers: Knowledge base YAML spec fields (name, description, index_config, credential)
- Covers: Dynamic input/output schemas (new in 2.10.0)
- Covers: Credential validation (new in 2.14.0)
- Vibe coder routing table updated to include `wxo-adk-knowledge`
- Learn mode MODULE 1 Node 1.4 updated to reference the new skill

**Todo List:**
1. Review `Lessons/wxo/adk/build/agentdesign.md` knowledge section and the GitHub `examples/agent_builder/ibm_knowledge/` example for concrete YAML
2. Create `wxo-adk-package 2/skills/wxo-adk-knowledge/SKILL.md` following the same structure as other skills (frontmatter, WHAT YOU COVER, DOCUMENTATION REFERENCE, patterns, CLI commands, OUTPUT STYLE)
3. Add `Knowledge bases (KB creation, indexing, CLI)` → `wxo-adk-knowledge` to vibe mode routing table in `wxo-adk-package 2/modes/wxo-adk-vibe.yaml`
4. Verify the learn mode `wxo-adk-learn.yaml` Module 1 Node 1.4 text is consistent with the new skill

**Relevant Context:**
- `Lessons/wxo/adk/build/agentdesign.md` knowledge section
- `github/ibm-watsonx-orchestrate-adk-main/examples/agent_builder/ibm_knowledge/knowledge_base/ibm_knowledge_base.yaml`
- `Lessons/wxo/adk/whats_new.md` — v2.10.0 dynamic schemas, v2.14.0 credential validation

**Status:** [x] done — `wxo-adk-package 2/skills/wxo-adk-knowledge/SKILL.md` created. Covers KB YAML spec (uses correct `knowledge_base:` field from GitHub example), all CLI commands, dynamic schemas (v2.10.0), credential validation (v2.14.0). Vibe routing table updated.

---

### TASK-07: Create wxo-adk-channels-voice Skill

**Intent:** Create a skill covering all channel integrations (Slack, Teams, Facebook Messenger, Twilio SMS/WhatsApp, SIP phone, Genesys) and voice provider configurations (Deepgram, ElevenLabs, Google TTS, Watson TTS). These are listed as CLI commands but have no skill coverage.

**Expected Outcomes:**
- New file `wxo-adk-package 2/skills/wxo-adk-channels-voice/SKILL.md` exists and is complete
- Covers: `orchestrate channels` command group (list, add, update, remove, embed)
- Covers: `orchestrate voice-configs` command group
- Covers: Channel YAML specs for at least Slack, Teams, Facebook Messenger, Twilio WhatsApp
- Covers: Voice provider configs (Deepgram STT/TTS, ElevenLabs TTS, Google TTS new in 2.14.0, Watson TTS)
- Covers: Phone/SIP trunk config YAML
- Notes OAuth limitation (web chat only) and SSO/IDP limitation (embedded web chat only)
- Vibe coder routing table updated to include `wxo-adk-channels-voice`

**Todo List:**
1. Review `github/ibm-watsonx-orchestrate-adk-main/examples/channel-integrations/` YAML examples (slack, teams, facebook, twilio, genesys, SIP)
2. Review `github/ibm-watsonx-orchestrate-adk-main/examples/agent_builder/voice_enabled_*/voice/` YAML examples
3. Review `Lessons/wxo/adk/whats_new.md` v2.1.0, v2.2.0, v2.8.0, v2.11.0, v2.14.0 channel/voice sections
4. Create `wxo-adk-package 2/skills/wxo-adk-channels-voice/SKILL.md`
5. Add `Channels / voice / phone / Slack / Teams` → `wxo-adk-channels-voice` to vibe mode routing table

**Relevant Context:**
- `github/ibm-watsonx-orchestrate-adk-main/examples/channel-integrations/`
- `github/ibm-watsonx-orchestrate-adk-main/examples/agent_builder/voice_enabled_*/`
- `Lessons/wxo/adk/known_issues.md` lines 29-30 (OAuth and SSO limitations)

**Status:** [x] done — `wxo-adk-package 2/skills/wxo-adk-channels-voice/SKILL.md` created (367 lines). Covers all 7 channel types, 4 voice providers including Google TTS v2.14.0, SIP trunk, Genesys Audio Connector, known limitations. Vibe routing table updated.

---

### TASK-08: Expand AgentOps Skill with Full Evaluations Framework

**Intent:** The current agentops skill covers only rubric evaluations (LLM-as-judge). The full `orchestrate evaluations` CLI has 8 sub-commands covering recording, generation, analysis, red-teaming, native/external agent validation, and quick-eval. Add coverage for the complete evaluations framework.

**Expected Outcomes:**
- `wxo-adk-agentops/SKILL.md` includes a FULL EVALUATIONS FRAMEWORK section
- Covers: `orchestrate evaluations evaluate`, `record`, `generate`, `analyze`, `validate-native`, `validate-external`, `quick-eval`, `red-teaming`
- Covers: Test case JSON format, stories CSV format, environment manager pattern
- Covers: Evaluation with context variables and file uploads
- Covers: Red-teaming (plan + run sub-commands)

**Todo List:**
1. Review `github/ibm-watsonx-orchestrate-adk-main/examples/evaluations/README.md` for all 13 test categories and CLI patterns
2. Open `wxo-adk-package 2/skills/wxo-adk-agentops/SKILL.md`
3. Add a new FULL EVALUATIONS FRAMEWORK section after the RUBRIC EVALUATIONS section, covering all `orchestrate evaluations` sub-commands with example CLI invocations
4. Add a note clarifying the distinction between rubric evaluations (LLM-as-judge, config-driven) and the broader `orchestrate evaluations evaluate` command (test case-driven, journey metrics)

**Relevant Context:**
- `github/ibm-watsonx-orchestrate-adk-main/examples/evaluations/README.md`
- `wxo-adk-package 2/skills/wxo-adk-agentops/SKILL.md` current RUBRIC EVALUATIONS section (lines ~173-211)

**Status:** [x] done — FULL EVALUATIONS FRAMEWORK section added with all 10 sub-commands, test case JSON format, stories CSV format, CI/CD env manager pattern, and key notes including red-teaming SaaS-only restriction.

---

### TASK-09: Add Partners CLI Note to Agent-Build Skill

**Intent:** Add a brief note about the `orchestrate partners` command to the agent-build skill so users building partner-submitted agents know the artifact packaging option exists.

**Expected Outcomes:**
- `wxo-adk-agent-build/SKILL.md` CLI COMMANDS section includes a note about `orchestrate partners`

**Todo List:**
1. Open `wxo-adk-package 2/skills/wxo-adk-agent-build/SKILL.md`
2. In the CLI COMMANDS section, add: `orchestrate partners  # Generate partner-submission-ready artifact package`
3. Add a brief note: "For agents being submitted as partner contributions to the watsonx Orchestrate catalog, use orchestrate partners to generate a well-structured, submission-ready agent artifact package."

**Relevant Context:** `wxo-adk-package 2/skills/wxo-adk-agent-build/SKILL.md` CLI COMMANDS section (lines ~179-188)

**Status:** [x] done — `orchestrate partners` command and partner-submission explanatory note added to CLI COMMANDS section.

---

## Priority Order for Implementation

| Priority | Task | Reason |
|---|---|---|
| 1 (Do first) | TASK-01: Fix deprecated style in onboarding guide | Structural correctness — fails on import |
| 1 (Do first) | TASK-02: Fix stale CLI in vibe mode | Structural correctness — CLI errors |
| 2 (Quick wins) | TASK-03: LLaMA/Mistral in agent-build | Low effort, fills audit W-01 |
| 2 (Quick wins) | TASK-04: Conversation compaction guidance | Low effort, fills audit W-03 |
| 2 (Quick wins) | TASK-05: AsyncOpenAPI SaaS note | Low effort, fills audit W-02 |
| 3 (New content) | TASK-06: Create knowledge skill | Medium effort, fills core gap |
| 3 (New content) | TASK-07: Create channels/voice skill | Medium effort, fills core gap |
| 3 (New content) | TASK-08: Expand agentops with full evaluations | Medium effort, fills core gap |
| 4 (Nice to have) | TASK-09: Partners CLI note | Low value, low effort |

---

## Files to Create

| File | Task |
|---|---|
| `wxo-adk-package 2/skills/wxo-adk-knowledge/SKILL.md` | TASK-06 |
| `wxo-adk-package 2/skills/wxo-adk-channels-voice/SKILL.md` | TASK-07 |

## Files to Modify

| File | Task(s) |
|---|---|
| `wxo-adk-package 2/wxo-adk-onboarding-guide.md` | TASK-01 |
| `wxo-adk-package 2/modes/wxo-adk-vibe.yaml` | TASK-02, TASK-03 |
| `wxo-adk-package 2/skills/wxo-adk-agent-build/SKILL.md` | TASK-03, TASK-04, TASK-09 |
| `wxo-adk-package 2/skills/wxo-adk-agentops/SKILL.md` | TASK-05, TASK-08 |
