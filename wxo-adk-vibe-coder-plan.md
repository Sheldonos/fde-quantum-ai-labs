# WxO ADK Vibe Coder — Build Plan

## Overview

Close the QisBob/WxO trilogy with a **vibe coding mode** for the watsonx Orchestrate ADK.

Architecture:
- 1 orchestrator **mode** (`wxo-adk-vibe`) — routes BUILD intents, classifies what to build,
  activates the correct skill, maintains session state
- 8 **skills** under `~/.bob/skills/wxo-adk-*/SKILL.md` — each one covers a specific ADK build
  domain and contains vibe-coder-grade instructions: code patterns, YAML templates, CLI commands,
  anti-patterns, and doc references (https://developer.watson-orchestrate.ibm.com/)

The orchestrator mode already exists as `wxo-adk-mentor` (Orchestrate) and `wxo-adk-learn` (LEARN).
This plan adds the BUILD arm: `wxo-adk-vibe` orchestrator + 8 code-focused skills.

## Skills to Create

| Skill Slug | Name | Domain |
|---|---|---|
| wxo-adk-install-setup | ADK Install & Env Setup | pip install, env add, Dev Edition |
| wxo-adk-agent-build | Agent YAML Authoring | spec, LLM config, styles, collaborators |
| wxo-adk-tools-build | Tools Development | Python, OpenAPI, MCP, toolkits, connections |
| wxo-adk-flows-build | Agentic Workflows | @flow, nodes, callbacks, LangGraph |
| wxo-adk-workspace | Workspace Management | IBM Cloud workspaces, membership |
| wxo-adk-agentops | AgentOps & Observability | traces, Langfuse, rubric eval |
| wxo-adk-troubleshoot | Troubleshooting | known issues, Docker, MCP, model bugs |
| wxo-adk-tutorials | Tutorials | Hello World, Empower agent, full deploy |

## Sub-Tasks

### ST-1: Create wxo-adk-install-setup SKILL.md
- **Status:** [ ] pending

### ST-2: Create wxo-adk-agent-build SKILL.md
- **Status:** [ ] pending

### ST-3: Create wxo-adk-tools-build SKILL.md
- **Status:** [ ] pending

### ST-4: Create wxo-adk-flows-build SKILL.md
- **Status:** [ ] pending

### ST-5: Create wxo-adk-workspace SKILL.md
- **Status:** [ ] pending

### ST-6: Create wxo-adk-agentops SKILL.md
- **Status:** [ ] pending

### ST-7: Create wxo-adk-troubleshoot SKILL.md
- **Status:** [ ] pending

### ST-8: Create wxo-adk-tutorials SKILL.md
- **Status:** [ ] pending

### ST-9: Create wxo-adk-vibe Orchestrator MODE in custom_modes.yaml
- **Status:** [ ] pending

## Doc Reference
All skills reference: https://developer.watson-orchestrate.ibm.com/getting_started/
Source files: Lessons/wxo/adk/** and Lessons/wxo/agentops_evaluation_monitoring
