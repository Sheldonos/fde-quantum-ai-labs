Agent design
Overview
Design decisions can affect the reliability, scalability, maintainability, and operational visibility of AI agents.
Understanding key design considerations can help teams create agents that are easier to manage, monitor, and evolve over time. This includes recognizing anti-patterns which are common design approaches that may seem beneficial initially but lead to problems such as poor performance, difficult maintenance, or operational challenges.
Most agent failures are not model failures, they are failures in architecture, control, and data design
​
Topics in this section
Foundational architecture considerations
Tooling and scalability considerations
Knowledge and document processing considerations
watsonx Orchestrate skills

---

Agent design
Foundational architecture considerations
The following table covers the most common foundational architecture anti-patterns that affect agent reliability and scalability.
⭐️ Most common anti-patterns
Anti-pattern	Problem	Impact	Fix
⭐️ The monolithic mega-prompt	500-line instructions	Over constrained agents and reasoning conflicts	Split reasoning from formatting and execution
⭐️ The agent-as-business-process fallacy	Agents approximate processes	Deterministic processes not followed 100%	Use workflows
Invisible state	Hidden state	Incorrect state tracking assumed	External state
All-or-nothing autonomy	Binary autonomy	Cost/UX issues	Risk-based controls
Passing ‘as-is’ information through the model	Paraphrasing authoritative content	Compliance risk	Route around LLM
Chasing the latest research paper	Premature adoption	Low ROI	Stick to well known patterns and fix tools/workflow instead
⭐️The monolithic mega-prompt

⭐️The agent-as-business-process fallacy

Invisible state

All-or-nothing autonomy

Passing 'as-is' information through the model

Chasing the latest research paper

​
Related topics
Tooling and scalability considerations
Knowledge and document processing considerations
watsonx Orchestrate skills
---

Agent design
Tooling & scalability considerations
The following table covers the most common tools and scalability anti-patterns that affect agent performance and reliability.
⭐️ Most common anti-patterns
Anti-pattern	Problem	Impact	Fix
Tool soup	Too many tools (10+ or more)	Accuracy decreases	Curate tools
⭐️ Tool data overload (The firehose effect)	Too much data	Context exhaustion	Filter early
⭐️ Agent-washing	Overuse agents	Unnecessary reasoning cost	Use tools/workflows
Blind trust in unverified components	Unaudited MCP	Security risk	Audit/sandbox
⭐️ Happy-path engineering	No failure handling	Much lower success	Train on failure
Multi-agent chaos	No coordination	Duplication	Tightly bounded agent per use case
⭐️ Responsiveness afterthought	No latency focus	User drop-off	Set budgets and design with scale in mind
Unbounded execution cost	Always large models	High cost	Optimize models and tool usage
Demo-grade agent in production	No real testing	Cannot handle real world situations	Load test, Scale test, design with failure in mind
Tool soup

⭐️Tool data overload (The firehose effect)

⭐️Agent-washing

Blind trust in unverified components

⭐️Happy-path engineering

Multi-agent chaos

⭐️Responsiveness afterthought

Unbounded execution cost

Demo-grade agent in production

​
Related topics
Foundational architecture considerations
Knowledge and document processing considerations
watsonx Orchestrate skills


---

Agent design
Knowledge and document processing considerations
The following table covers the most common knowledge and document processing anti-patterns that affect agent response quality and accuracy.
⭐️ Most common anti-patterns
Anti-pattern	Problem	Impact	Fix
Assumed trust in the knowledge source	Assume truth	Amplified errors	Verification
⭐️ ‘RAG will fix disorganized knowledge’	Poor structure	Bad outputs	Fix knowledge
Knowledge retrieval token bloat	Over-fetching	Large token waste	Top-N retrieval and organize knowledge
⭐️ One-size-fits-all chunking	Fixed chunks	Broken semantics	Content-aware
Using RAG for whole-document operations	Wrong tool	Structure loss	Use DB/API
Ignoring file format implications	Same processing	Lost structure	Format-aware
Mixing extraction with processing	Overloaded extractor	Errors	Separate steps
Lazy field definitions	Vague schema	Fuzzy field errors	Explicit fields
Assumed trust in the knowledge source

⭐️'RAG will fix disorganized knowledge'

Knowledge retrieval token bloat

⭐️One-size-fits-all chunking

Using RAG for whole-document operations

Ignoring file format implications

Mixing extraction with processing

Lazy field definitions

​
Related topics
Foundational architecture considerations
Tooling and scalability considerations
watsonx Orchestrate skills


---

Agent design
MCP tools & integration considerations
The following table covers the most common MCP tools and integration anti-patterns that affect agent reliability and security.
⭐️ Most common anti-patterns
Anti-pattern	Problem	Impact	Fix
⭐️ The glorified API wrapper	Low-level API operations	High reasoning burden	Business capabilities
Raw schema leakage	Exposed internal schemas	Agent must infer logic	Business abstractions
Wishful delegation	”Model will figure it out”	Fragile agents	Encode complexity in tools
Anything-in, garbage-out	No validation	Silent failures	Strong contracts
The god-mode tool	Unrestricted access	Security risks	Constrained capabilities
⭐️ The data firehose	Large unfiltered datasets	Context exhaustion	Bounded outputs
The trusted output trap	Unvalidated tool output	Prompt injection risk	Sanitize outputs
⭐️ The “kitchen sink” server	80+ tools at initialization	Selection entropy	Contextual discovery
The useless error	Raw stack traces	No self-correction	Structured errors
The stateful tool trap	Implicit session state	Race conditions	Stateless design
The glorified API wrapper

​
What it is
Exposing low-level API operations instead of business capabilities
Tools like odata_create(entity_set, payload) instead of create_purchase_order(vendor, items, amount)
Treating MCP as an API gateway rather than agent-ready capability layer
​
Why it fails
Exposes low-level API mechanics: Agents must understand entity sets, payloads, and API structure
No business semantics: Tool name doesn’t convey what business action it performs
Agents must reconstruct intent: Model figures out how to map business intent to API calls
Increases reasoning burden: Amplifies hallucination risk, makes agent fragile to API changes
​
What to do instead: Business capability tools
Design for business actions: create_purchase_order(vendor_id, items, delivery_date) not odata_create(entity_set, payload)
Encode business logic in tools: Move complexity from prompts to code
Clear semantics: Tool names convey business intent
Reduce reasoning burden: Agent operates business capabilities, not API mechanics
Raw schema leakage

​
What it is
Exposing internal data schemas instead of business operations
Tools operate on tables, entities, or endpoints—not business concepts
Inputs are generic JSON structures where field names ≠ business meaning
​
Why it fails
Relationships are implicit: No guidance on valid combinations
No domain rules: Tool doesn’t encode business constraints
Agent must infer business logic from schema: Highly error-prone task
Reverse-engineering burden: Asking LLM to do system design work
​
What to do instead: Business-level abstractions
Hide schema complexity: Expose business operations, not database tables
Encode relationships: Build valid combinations into tool design
Domain rules in code: Validation and constraints in tool implementation
Business parameters: vendor_id, items, delivery_date not generic JSON blobs
Wishful delegation

​
What it is
“The model will figure it out”—pushing system design responsibility onto LLM
Multi-step reasoning chains (discover → fetch metadata → construct query → build payload → execute)
Tool proliferation with dozens of generic CRUD operations
Assuming perfect reasoning from probabilistic models
​
Why it fails
Moves business logic from code to prompts: System responsibility becomes reasoning burden
Increases decision entropy: More tools and steps = more failure modes
Amplifies hallucination risk: Each reasoning step is opportunity for error
More tools ≠ better agents: Increases entropy in decision space
​
What to do instead: Encode complexity in tools
Reduce reasoning steps: Combine multi-step operations into single business capability
Limit tool count: Fewer, well-designed tools better than many generic ones
Business logic in code: Don’t make agent reverse-engineer your system
Clear contracts: Each tool has single, well-defined purpose
Anything-in, garbage-out

​
What it is
Tools without clear validation constraints or domain rules
No required/optional clarity, ambiguous parameter meanings
Tools are syntactically valid but semantically ambiguous
​
Why it fails
No guardrails: Invalid combinations accepted
Silent failures: Operations succeed technically but fail semantically
Runtime failures: Instead of design-time clarity
Agent calls tools with incorrect or meaningless inputs
​
What to do instead: Strong contracts
Explicit validation: Required fields, data types, value ranges
Domain rules: Encode business constraints in tool
Clear parameter semantics: Each parameter has unambiguous meaning
Fail fast: Reject invalid inputs with structured error messages
The God-mode tool

​
What it is
Exposing broad write access or execution capabilities without constraints
Tools allowing arbitrary writes, function execution with user code, unrestricted data access
Too much power at wrong abstraction level
​
Why it fails
Security risks: Agents can be manipulated to perform unauthorized actions
No audit trail: Hard to track what agent actually did
Violates least-privilege principle: Capabilities must be constrained and auditable
​
What to do instead: Constrained, auditable capabilities
Least privilege: Tools get minimum permissions needed
Explicit constraints: Limit scope of operations
Audit trails: Log all actions with context
Approval gates: High-risk operations require confirmation
Separate read/write: Different tools for different privilege levels
The data firehose

​
What it is
Tools returning large datasets without filtering or summarization
Manifestation of Tool Data Overload in MCP context
No pagination, no filtering, raw data injection without context window consideration
​
Why it fails
Context window exhaustion: Tool output competes with instructions, user intent, reasoning steps
Degrades reasoning quality: Large outputs push out critical instructions
Cost explosion: Paying for massive token counts on every turn
Bigger context ≠ better reasoning: Long inputs can degrade performance
​
What to do instead: Bounded and filtered tool output
Filter at source: Return only needed data using query parameters
Implement pagination: Use continuation tokens for large datasets
Summarize appropriately: Return summaries instead of full content
Set hard limits: Enforce maximum output sizes (e.g., 2000 tokens per call)
Monitor token usage: Track and optimize high-volume tools
The trusted output trap

​
What it is
Treating tool output as safe data instead of potential instructions
Security vulnerability: LLMs cannot reliably distinguish trusted instructions from untrusted data
Everything processed as same token stream
​
Why it fails
Prompt injection via tool output: Unvalidated content from external sources (documents, logs, emails, web data) can contain embedded instructions
Can override system behavior: Manipulate reasoning, trigger unintended actions, exfiltrate data
No clear boundary: Between legitimate system instructions and attacker’s embedded commands
​
What to do instead: Treat tool output as untrusted
Content sanitization: Strip/escape instruction markers, remove suspicious markdown, filter patterns
Output validation: Validate against expected schemas before sending to LLM
Structured formats: Use JSON instead of free-form text when possible
Data-instruction separation: Use XML tags, JSON encapsulation, delimiters to separate trusted instructions from untrusted data
Output monitoring: Monitor for suspicious patterns or anomalies
Least privilege: Return only minimum data needed
The "Kitchen sink" server

​
What it is
Registering massive, monolithic list of tools during initialization
Manifestation of Tool Soup in MCP server design
80+ tools presented at initialization regardless of agent’s task or user permissions
​
Why it fails
Handshake bloat: MCP discovery phase floods agent with every possible tool choice
Selection entropy: LLMs degrade in tool-selection accuracy with massive lists
Missing least-privilege: Exposes administrative/sensitive tools to sessions that shouldn’t have access
High tool selection latency: Increased rate of wrong tool invocation
​
What to do instead: Contextual tool discovery
Role-based filtering: Expose only tools relevant to user’s role and permissions
Task-based tool sets: Group by business capability, expose only relevant sets
Dynamic registration: Register/unregister tools based on session state or context
Hierarchical organization: Use gateway tools that expose sub-tools only when needed
Metadata optimization: Keep descriptions concise; provide just enough for selection
The useless error

​
What it is
Returning raw system stack traces or generic error strings instead of structured, LLM-actionable correction hints
Treating LLM like human debugger
No actionable feedback on what to fix or how to fix it
​
Why it fails
Breaks self-correction loop: Agents are probabilistic; with explicit explanation of why call failed, they can fix payload on next turn
Generic errors cause hallucination: Model guesses what went wrong instead of being told explicitly
Amplifies reasoning burden: Forces agent to debug instead of correct
​
What to do instead: Structured, agent-friendly error responses
Structured format: Return JSON with error_code, message, field, correction_hint
Error taxonomy: Define clear codes (VALIDATION_FAILED, RESOURCE_NOT_FOUND, PERMISSION_DENIED, RATE_LIMIT_EXCEEDED, INVALID_STATE)
Examples in hints: Include concrete examples of valid inputs
Reference related tools: Mention tools that can resolve the error
Avoid implementation details: Never expose stack traces, internal variables, system paths
The stateful tool trap

​
What it is
Designing MCP tools that implicitly rely on session state or execution order
Tools like set_active_project(project_id) followed by archive_current_project()
Assuming backend/transport layer preserves stateful sequence
​
Why it fails
Asynchronous drift: MCP transports (stdio, HTTP SSE) can experience race conditions, parallel reasoning loops, multi-agent handoffs
Context reset vulnerability: Conversation context cleared/shifted causes next tool call to execute against dead/incorrect references
Parallel execution hazards: Multiple agents/threads interleave tool calls, corrupting shared state
​
What to do instead: Stateless, self-contained tools
Explicit parameters: Every tool call includes all required context; no implicit “current” or “active” state
Idempotent operations: Tools are safely repeatable with consistent results
Return full context: Responses include enough context for subsequent calls without relying on memory
Avoid “set” and “get” patterns: Use do_operation(context_params) instead of set_context() followed by do_operation()
Document state requirements explicitly: If state genuinely required, make it explicit in tool contract and provide state tokens
​
MCP usage patterns
​
Pattern 1: Direct agent tools (recommended for Enterprise)
Design tools that represent business capabilities with intent-level, constrained inputs, strong contracts with validation, and clear semantics.
Examples:
submit_expense_report(employee_id, amount, category)
approve_purchase_order(po_id)
create_supplier_invoice(vendor_id, items, due_date)
Characteristics:
Low reasoning burden
Strong contracts
Safe execution
Clear audit trail
Business-aligned
​
Pattern 2: Agent-ready tool facade pattern (integration layer)
Use generic MCP tools internally as implementation details, build higher-level business capability tools on top, expose only the business-level interface to agents, and hide complexity behind a simplified, intent-driven facade.
Example:
# Internal (not exposed to agent)
odata_create(entity_set, payload)
odata_update(entity_set, key, payload)

# Exposed to agent (the facade)
create_supplier_invoice(vendor_id, items, due_date)
  → internally orchestrates odata_create with validation
Characteristics:
MCP used as plumbing, not interface
You control abstraction and guardrails
Business logic in code, not prompts
Easier to test and maintain
Follows classic facade design pattern principles
​
Evaluating MCP tool suitability
Quick checks for agent-ready tools:
Check	✅ Agent-Ready	❌ Anti-Pattern
Business action?	YES	NO (likely API wrapper)
Constrained inputs?	Explicit fields with clear semantics	Generic JSON payload
Non-expert friendly?	YES (agent-friendly)	NO (schema leakage)
Safe by default?	Limited, auditable actions	Broad write/execution (high risk)
Logic location?	Logic in system (scalable)	Logic in prompt (fragile)
Reasoning required?	Minimal (good design)	Multi-step inference (anti-pattern)
Designed for agents?	YES	Feels like an API (not for agents)
​
Related topics
Foundational architecture considerations
Tooling and scalability considerations
Knowledge and document processing considerations

---

Agent design
Bob skills
​
Overview
The Bob skill set supports the complete lifecycle of building enterprise AI agent solutions:
solution-architect: Transforms business problems into structured solution architectures with executive summaries, technical designs, and implementation roadmaps. Provides the foundation for SOP development.
sop-builder: Converts technical procedures and workflows (for example, BPMN, Langflow, n8n) into business-readable Standard Operating Procedures with plain-language descriptions, Mermaid diagrams, and detailed process documentation.
wxo-builder: Implements production-ready watsonx Orchestrate solutions from SOPs or prompts, generating agents, tools, flows, and knowledge bases following ADK best practices and project structures.
wxo-analyzer: Reverse-engineers existing watsonx Orchestrate projects to produce comprehensive documentation, relationship diagrams, and anti-pattern analysis across enterprise AI failure modes for auditing and onboarding.
agent-instructions-evaluator: Zooms into a specific agent to assess instruction quality and production viability. Evaluates operational achievability, not writing quality, by identifying runtime reliability risks such as hidden state, conflicting rules, vague scope, and brittle phrasing. Produces per-dimension scores and evidence-backed findings across five evaluation dimensions.
Together, these skills form a closed-loop system for designing, building, documenting, and maintaining enterprise-grade watsonx Orchestrate solutions.
​
Available skills
​
1. solution-architect
Location: solution-architect/SKILL.md
The solution-architect skill turns business problems into clear, structured solution architectures. It bridges business and technical perspectives by producing:
Executive-level solution overviews
Technical architecture and design patterns
Implementation roadmaps and SOP-ready documentation
Best for: Early-stage design and stakeholder alignment
Key capabilities:
Analyzing business requirements and problem statements
Generating three focused architecture documents: Solution Overview, Technical Architecture, and Implementation Plan
Producing business-focused summaries and context
Bridging business needs with technical implementation
Preparing documentation for elaboration into detailed SOPs
Producing modular, manageable documentation
​
2. sop-builder
Location: sop-builder/SKILL.md
The sop-builder skill transforms technical workflows into business-readable Standard Operating Procedures. It:
Converts BPMN, Langflow, and n8n workflows into plain-language procedures
Documents decision points, exceptions, integrations, and prompts
Produces Mermaid diagrams and business-ready process descriptions
Best for: Standardizing and operationalizing processes
Key capabilities:
Analyzing BPMN diagrams, Langflow JSON, and n8n workflows
Generating business-focused SOPs in plain language
Producing business process flow diagrams with Mermaid
Documenting data requirements and custom logic
Documenting LLM prompts
Defining business procedure steps and decision points
Documenting exception handling and integration points
Translating technical concepts into business language
​
3. wxo-builder
Location: wxo-builder/SKILL.md
The wxo-builder skill turns SOPs or prompts into fully implemented watsonx Orchestrate solutions. It:
Generates agents, tools, flows, and knowledge bases
Follows recommended ADK project structures and patterns
Supports multiple knowledge base backends and end-to-end CLI workflows
Best for: Implementing production-ready watsonx Orchestrate builds
Key capabilities:
Generating complete watsonx Orchestrate implementations from Standard Operating Procedures (SOPs)
Transforming business requirements into agents, tools, flows, and knowledge bases
Recommended workflow: use sop-builder to create SOPs from BPMN, n8n, or Langflow first, then use wxo-builder to generate watsonx Orchestrate solutions
Knowledge base providers: Milvus, AstraDB, Elasticsearch
Standard project structure and implementation patterns
Document processing flows and workflow patterns
Python tool and flow decorators
Agent YAML configuration
CLI import commands and best practices
Complete examples from the ADK repository
​
4. wxo-analyzer
Location: wxo-analyzer/SKILL.md
The wxo-analyzer skill reverse-engineers and documents existing watsonx Orchestrate projects. It:
Analyzes project structure and components
Produces multi-report documentation sets (overview, agents, tools)
Generates diagrams and relationship mappings
Detects anti-patterns and provides recommendations
Best for: Understanding, auditing, or onboarding into existing watsonx Orchestrate solutions
Key capabilities:
Analyzing existing watsonx Orchestrate project structures
Generating three-report documentation sets: Solution Overview, Agent Analysis, and Tools & Components
Creating Mermaid diagrams that show component relationships
Documenting agents, tools, connections, and knowledge bases
Producing project structure and component inventories
Mapping relationships between agents, tools, and resources
Detecting anti-patterns across 15 enterprise AI failure modes
Counting instruction lines and analyzing complexity
Assessing production readiness
​
5. agent-instructions-evaluator
Location: agent-instructions-evaluator/SKILL.md
The agent-instructions-evaluator skill zooms into a specific agent to evaluate its instructions for operational achievability in production settings. It focuses on instruction quality and production viability rather than writing quality, identifying runtime reliability risks and execution failures before they reach production. It:
Focuses on a single agent’s instructions to assess runtime reliability and instruction quality
Identifies issues that stem from hidden state, conflicting rules, vague scope, and brittle phrasing
Produces structured evaluation reports with evidence-backed findings
Provides per-dimension scores across five evaluation dimensions (0–5 scale)
Best for: Zooming into a specific agent to validate instruction quality and production viability before deployment
Key capabilities:
Evaluating agent instructions across five dimensions: Task Understanding, Scope and Applicability, Execution and Tool Grounding, Instruction Followability, and State and Conflict Manageability
Counting deterministic signals (exact phrases, nested branches, implicit state)
Producing evidence-backed findings with impact analysis and recommendations
Prioritizing risks and identifying high-leverage improvements
Generating structured JSON output for evaluation harnesses
Supporting watsonx Orchestrate YAML, system prompts, and agent definitions
Assessing production readiness with a focus on runtime reliability
​
How the skills work together
A typical end-to-end workflow:
Business problem
      ↓
[solution-architect] → Solution architecture documents
      ↓
[sop-builder] → Standard Operating Procedures
      ↓
[wxo-builder] → watsonx Orchestrate implementation
      ↓
[wxo-analyzer] → Documentation and anti-pattern analysis
      ↓
[agent-instructions-evaluator] → Per-agent instruction quality assessment
In this closed-loop system:
solution-architect establishes the foundation and high-level design.
sop-builder produces detailed, business-readable procedures.
wxo-builder implements the technical solution.
wxo-analyzer validates, documents, and identifies improvements at the solution level.
agent-instructions-evaluator provides a review of a specific agent’s instructions by focusing on a single agent to evaluate the quality, clarity, effectiveness, and overall viability of its instructions.
​
Using these skills
​
In Claude Desktop or web
Navigate to the Skills section in Claude.
Import the desired skill by selecting the appropriate SKILL.md file:
solution-architect/SKILL.md for solution architecture documentation
sop-builder/SKILL.md for SOP generation from workflows
wxo-builder/SKILL.md for watsonx Orchestrate development
wxo-analyzer/SKILL.md for analyzing existing watsonx Orchestrate projects
agent-instructions-evaluator/SKILL.md for evaluating agent instructions
The skill is available in your conversations.
​
Agent skills overview
Agent skills provide a standardized way to give AI agents new capabilities and domain expertise.
​
What are agent skills?
Agent skills are a lightweight, open format for extending AI agent capabilities with specialized knowledge and workflows.
At its core, a skill is a folder that contains a SKILL.md file. This file includes metadata (at minimum, a name and description) and instructions that tell an agent how to perform a specific task. Skills can also bundle scripts, reference materials, templates, and other resources.
my-skill/
├── SKILL.md          # Required: metadata + instructions
├── scripts/          # Optional: executable code
├── references/       # Optional: documentation
├── assets/           # Optional: templates, resources
└── ...               # Any additional files or directories
​
Why use agent skills?
Agents are increasingly capable, but often lack the context required to do real work reliably. Skills address this by packaging procedural knowledge and organization-specific context into portable, version-controlled folders that agents load on demand. Skills provide agents with:
Domain expertise: Specialized knowledge, including legal review processes, data analysis pipelines, and presentation formatting, packaged as reusable instructions and resources.
Repeatable workflows: Multi-step tasks expressed as consistent, auditable procedures.
Cross-product reuse: Skills built once and used across any skills-compatible agent.
​
How agent skills work
Agents load skills through progressive disclosure in three stages:
Discovery: At startup, agents load only the name and description of each available skill, which is enough to identify when a skill is relevant.
Activation: When a task matches a skill’s description, the agent reads the full SKILL.md instructions into context.
Execution: The agent follows the instructions, running bundled code or loading referenced files as needed.
​
Skill structure
Each skill follows the skills format:
SKILL.md: Main skill file with frontmatter (name, description)
examples.md: Complete reference implementations and code examples (where applicable)
Frontmatter: Skill metadata
Content: Expert guidance, specifications, and best practices
​
Resources
solution-architect/SKILL.md
sop-builder/SKILL.md
wxo-builder/SKILL.md
wxo-analyzer/SKILL.md
agent-instructions-evaluator/SKILL.md
Reference examples


---

Agents
Importing and deploying agents
​
Importing Agents
Importing an agent involves transferring it from your local system into your active environment, where it enters a draft (undeployed) state. There are two supported methods for importing agents:
Using an agent configuration file: Upload a pre-defined configuration that describes the agent’s components and behavior.
Using the ADK CLI: Create and register the agent directly via the Agent Development Kit (ADK) command-line interface.
​
Importing agents using an agent file
Use the orchestrate agents import command to import agents into the watsonx Orchestrate platform from a YAML, JSON, or Python file. You can import either natively built agents, external agents connected from other systemsm, or even custom agents.
Native and External Agents
Custom agents
To specify the agent file path, use the --file or -f flag:
BASH
orchestrate agents import -f <path to .yaml/.json/.py file>
Show command flags

Before running this command, make sure you have a valid agent configuration file. This file defines the parameters that describe the agent’s behavior and structure for watsonx Orchestrate. For details on how to author these configurations, see Authoring agents.
​
Bulk import from ZIP
Import agents along with all their dependencies using a single ZIP file.
You can import an agent and all its dependencies with the following command:
BASH
orchestrate agents import -f my_agent.zip
The structure of the imported ZIP file matches the structure produced by the agent export command:
BASH
orchestrate agents export -k native -n my_agent -o my_agent.zip
During the import process, tools require connections to be manually selected.
​
Creating agents directly from the CLI
The orchestrate agents create command can be used to quickly create and import an agent into the watsonx Orchestrate platform without first having a file to import.
Native Agent
External Agent
watsonx.ai External Agent
Custom agents
BASH
orchestrate agents create \
--name agent_name \
--kind native \
--description "Sample agent description" \
--llm watsonx/ibm/granite-3-8b-instruct \
--style react_core \
--collaborators agent_1
--collaborators agent_2
--tools tool_1
--output "agent_name.agent.yaml"
See all 10 lines
Show command flags

​
Copy agents between workspaces
BASH
orchestrate agents copy --name <agent-name> --source <source-workspace-name> --destination <dest-workspace-name>
Show command flags

​
Deploying Agents
Agents in watsonx Orchestrate operate in one of two states: draft or live.
A draft agent is actively being developed or modified by a builder. You can access draft agents from the Manage Agents page in the UI.
A live agent is available to end users through the Web chat UI on the Orchestrate landing page.
Note: In the watsonx Orchestrate Developer Edition, only the draft environment is available. This edition is designed for single-user, non-production use. As a result, the Web chat UI displays agents in their draft state instead of the live state. Attempting to run deploy commands in the Developer Edition will result in an error.
​
Deploying an agent
Deploying an agent is the act of taking an agent from a draft state into a live state.
BASH
orchestrate agents deploy --name agent_name
Note: By default the deploy agent command timesout after 5 minutes of checking the agent status. If you need to increase this you can use the WXO_AGENT_DEPLOYMENT_TIMEOUT environment variable. Default value is 300.
​
Undeploying an agent
Undeploying an agent is the act of reverting an agent from its current live state to the previous live state.
BASH
orchestrate agents undeploy --name agent_name

---

Agents
Managing agents
​
Listing agents
Use the orchestrate agents list command to list all agents in your environment. You can filter by agent type and get detailed information using the available flags.
BASH
orchestrate agents list -v
Show command flags

​
Exporting agents
Use the orchestrate agents export command to export an agent configuration from your active environment.
You can export the full agent configuration with all its dependencies (default), or only the agent configuration by including the --agent-only flag.
BASH
orchestrate agents export -n <agent-name> -k <agent-type> -o <output-path>.zip
Show command flags

Note: Agentic workflow tools are only exported when you use a local environment with watsonx Orchestrate Developer Edition.
​
Updating agents
To update an agent, run the import command again using the same agent name as the agent you want to update.
BASH
orchestrate agents import -f <path to agent file that you want to update>
If you’re updating an agent to use a different LLM (such as migrating from Llama to GPT-OSS-120B), see the Migration guide for model-specific optimization instructions.
​
Removing agent
To remove an existing agent, run the following command:
BASH
orchestrate agents remove --name my-agent --kind native
Show command flags

​
Chatting with an agent in interactive mode through the CLI
To start a chat session with an agent, run the following command:
BASH
orchestrate chat ask --agent-name <agent_name>
To start a chat session and ask an initial question, run the following command:
BASH
orchestrate chat ask --agent-name <agent_name> "What is the weather?"
To start a chat session and view the agent’s reasoning trace, run the following command:
BASH
orchestrate chat ask --agent-name <agent_name> "What is the weather?" --include-reasoning
​
Additional CLI chat options
You can interact with agents directly from the CLI by using the orchestrate chat ask command.
To see all available flags and options, run:
BASH
orchestrate chat ask --help
​
Capturing execution logs for custom agents
For custom agents, you can capture and display execution logs by using the --capture-logs flag. It is useful for debugging and understanding agent behavior during execution.
BASH
orchestrate chat ask "what is python" \
  --agent-name SimpleWxAIAgent \
  -r \
  --capture-logs
​
Continuing an existing conversation by using a thread ID
To continue an existing conversation, use the --thread-id flag. It allows the agent to maintain conversational context across multiple requests.
BASH
orchestrate chat ask \
  --agent-name customer_care_agent \
  --thread-id <thread-id> \
  "give me more information on claim CLM1234567"
​
Running flow agents from the CLI
The CLI now supports flow agents. From a user perspective, you can run flow agents the same way as other agents.
BASH
orchestrate chat ask \
  --agent-name various_outputs_agent \
  "flow" \
  -r
​
Uploading and downloading files during chat
Agents that require file input or output now support file upload and download capabilities through the CLI.
When an agent requests a file upload or download, the CLI prompts you to provide the local directory path for the file to upload or the destination directory for downloaded files.
File prompts appear only when the agent workflow requires file interaction.

---

Agent skills
Agent skills
Agent skills provide a targeted set of instructions for a specific task, such as processing an invoice, running a data validation, or following a policy review workflow. Instead of writing all instructions directly into the agent configuration, package each capability as a separate skill. The agent loads only the skill that is relevant to each request.
Use agent skills when you want to:
Break a complex agent into independently maintained capabilities.
Reduce context size and token usage by loading instructions only when they are relevant.
Reuse the same skill across multiple agents without duplicating instructions.
A skill is a directory that contains a SKILL.md file. That file has two parts: a YAML frontmatter block with the name and description fields, and a Markdown body with the instructions the agent follows.
​
How the agent activates skills
When an agent has skills attached to it, it does not load all instructions at once. Instead, it uses a progressive disclosure approach and loads only the skill that is relevant to the current request:
Discovery: The agent reads only each skill’s name and description, not the full instructions.
Activation: When a user sends a message, the agent matches it to the most relevant skill based on the skill’s description, then loads the full SKILL.md body into context.
Execution: The agent follows the instructions in the body and invokes the tools declared in the skill.
​
Creating agent skills
1
Create your skill directory

Create a directory with a SKILL.md file at its root. Add a YAML frontmatter block with at least name and description, then write the instructions in the body. Optionally, include a scripts/ subdirectory for Python files and a references/ subdirectory for supporting documents.
For more information, see Skill directory structure.
2
Import the skill into your environment

Register the skill in your active environment by using the import command. Use --dir to upload the skill directory in one step, or --recursive to bulk-import a directory that contains multiple skills.
For more information, see Importing skills.
3
Inspect and verify

Confirm that the skill registered correctly by listing all skills or retrieving the details of a specific one.
For more information, see Listing skills and Inspecting a skill.
4
Update or remove as needed

Replace a skill’s definition at any time by running the update command. Remove skills that you no longer need to keep your environment clean.
For more information, see Updating a skill and Removing a skill.
To add or refresh a single script or reference file after the initial import, use the dedicated upload commands instead of re-importing the entire skill. For more information, see Uploading scripts and Uploading reference documents.
​
Skill directory structure
A skill directory uses the following structure:
my-skill/
├── SKILL.md          # Required: frontmatter (name, description) + instructions
├── scripts/          # Optional: Python scripts referenced by the skill
└── references/       # Optional: reference documents (.md, .txt, .json)
SKILL.md file
SKILL.md has two sections separated by --- delimiters. The top section is YAML frontmatter, a structured metadata block. The section below it is the instructions body, written in plain Markdown.
The frontmatter must include at least name and description. The agent reads description to decide whether this skill is relevant to a user request. Write it as a clear statement of what the skill does and when to use it.
---
name: invoice-management
description: Handles invoice creation, validation, and approval workflows.
---

# Invoice Management

## Procedure

1. Confirm the invoice details with the user.
2. Call the invoice creation tool with the confirmed details.
3. Return the created invoice ID and status to the user.
Why description matters
An agent can have several skills bound to it. When a user makes a request, the agent determines which skill is relevant based on each skill’s name and description. The name and description are the only signals the agent uses to distinguish one skill from another. The agent does not read the full skill body or scripts to make that determination, it matches the request against the description text.
Follow these guidelines when you write a description:
State when to use the skill: Describe not only what the skill does, but also the situation that triggers it. For example: “Use when a user asks for order status or details.”
Be specific enough to disambiguate: Two skills with vague, overlapping descriptions such as “handles orders” and “manages order stuff” make it difficult for the agent to select the correct one.
Keep it short: One or two sentences. The description is a matching signal, not documentation. Include procedural detail in the skill body instead.
allowed-tools
allowed-tools is an optional frontmatter field. When present, the agent can call only the tools listed under it while the skill is active.
---
name: order-submit
description: Place and track customer orders. Use when a user wants to submit a new order or check the status of an existing order.
allowed-tools:
  - create_order
  - update_order_status
---
After the agent selects a skill, its full instruction body takes over. The agent follows those instructions step by step, with only that skill’s allowed-tools available.
scripts/ directory
The scripts/ directory holds Python (.py) files that the agent can run as part of the skill, for example, to perform a validation or transform data before passing it to a tool.
When you import the skill by using orchestrate skills import --dir, the CLI uploads all .py files under scripts/ automatically.
references/ directory
The references/ directory holds documents that provide the agent with additional context while the skill runs, for example, a policy file, a lookup table, or a set of guidelines. The agent can read these files as it follows the skill instructions. Supported file types are .md, .txt, and .json.
​
Invoking scripts and references from the skill body
A skill can include Python scripts (scripts/) and reference documents (references/). Neither is invoked automatically. The skill body must instruct the agent when and how to use them.
Scripts
Specify which script to run and the required arguments:
Before placing any order, run the validation script order_validate.py with:
args={"product_id": "<product_id>", "quantity": <quantity>, "unit_price": <unit_price>}
The script is a plain Python function. Its parameters are defined by the function signature:
def run(product_id: str, quantity: int, unit_price: float) -> dict:
    ...
References
Specify which file to consult and when:
For detailed order limits and shipping rules, read the policy reference: ORDER_POLICY.md
In each case, write plain-language instructions in the skill body that name the exact script or reference file and the condition under which the agent must use it. The agent follows the instruction text and does not infer intent independently.


---
Agent skills
Managing agent skills
Use the orchestrate skills command group to import, inspect, update, and remove skills from your active environment without using the Agent Builder interface.
​
Importing skills
Use orchestrate skills import to register one or more skills in your active environment.
Single file
Skill directory
Bulk import
BASH
orchestrate skills import --file skills/invoice-management/SKILL.md
If a skill with the same name already exists, the command updates it instead of returning an error.
Show command flags

Specifying both --file and --dir in the same command is not supported.
​
Listing skills
To list all skills that are registered in your active environment, run:
Summary table
Full details
BASH
orchestrate skills list
The default output is a table that shows each skill’s name, description, mode, tools, script count, and ID.
Show command flags

​
Inspecting a skill
To view the complete details of a single skill, including its full instructions body, run:
By name
By ID
BASH
orchestrate skills get --skill-name invoice-management
Show command flags

​
Updating a skill
To update an existing skill’s definition, provide the path to the revised SKILL.md and identify the skill by name or ID:
By name
By ID
BASH
orchestrate skills update --skill-name invoice-management --file skills/invoice-management/SKILL.md
Show command flags

You must specify exactly one of --skill-id or --skill-name. The skill must already exist before you can update it.
​
Uploading scripts
Skills can reference Python scripts that the agent runs. Upload individual script files after you import the skill. The CLI derives the script path inside the skill — for example, scripts/validate.py — from the local file path. Use --script-path to override this when the local path does not match the expected relative path inside the skill.
By name
By ID
Custom script path
BASH
orchestrate skills upload-script --skill-name invoice-management --file scripts/validate.py
Show command flags

Script files must be Python (.py) files. You must declare scripts in the skill’s SKILL.md frontmatter. When you use orchestrate skills import --dir, the CLI uploads all scripts under scripts/ automatically.
Scripts are intended for compute tasks such as pre- and post-validation steps. They run in isolation and are validated at upload time. The following items are blocked:
Category	Blocked items
Imports	os, sys, subprocess, socket, shutil, importlib, ctypes, multiprocessing, threading, pickle, shelve, marshal, code, pty, fcntl, resource, signal, tempfile, glob, pathlib, platform, urllib, urllib3, http, httplib, httplib2, requests, aiohttp, httpx, websocket, websockets, ftplib, smtplib, poplib, imaplib, nntplib, telnetlib, xmlrpc, asyncio
Built-in functions	eval, exec, compile, open, __import__, globals, locals, vars, input, breakpoint
Patterns	URL strings, pip install calls, and other network-access patterns
Any script that contains blocked imports, built-in functions, or patterns is rejected at upload time and is not stored.
​
Uploading reference documents
Reference documents provide the agent with additional context, such as policy files, lookup tables, and reference guides. Supported file types are .md, .txt, and .json.
By name
By ID
BASH
orchestrate skills upload-reference --skill-name invoice-management --file references/REFERENCE.md
Show command flags

​
Exporting skills
Export a skill to move it between environments, share it with your team, or add it to source control.
By name
By ID
Extract to directory
BASH
orchestrate skills export --skill-name invoice-management --output ./exported/invoice-management.zip
Show command flags

​
Removing a skill
To remove a skill that you no longer need from your active environment, run:
By name
By ID
BASH
orchestrate skills remove --skill-name invoice-management
Show command flags

You must specify exactly one of --skill-id or --skill-name.


---

Large Language Models (LLMs)
Choosing your LLM
When you create an agent, the choice of LLM determines how effectively the agent can complete your workflow. watsonx Orchestrate provides optimized support for specific model/provider combinations, and allows registration of additional models as virtual models. [1]
​
Available Models
watsonx Orchestrate provides optimized support for the following models:
Model	Description	License
★ groq/openai/gpt-oss-120b	gpt-oss-120b is optimized for high-speed inference and tool calling, designed for multilingual and system-prompt flexibility.	Apache 2.0
★ bedrock/openai/gpt-oss-120b-1:0	GPT-OSS-120b is available through AWS Bedrock, optimized for high-speed inference and tool calling.	Apache 2.0
★ watsonx/openai/gpt-oss-120b	GPT-OSS-120b available through watsonx.ai (GovCloud only - available April mid-release)	Apache 2.0
★ azure-openai/gpt-5.4	GPT-5.4 is one of OpenAI’s frontier models, built to deliver faster, more reliable results for complex professional work.	Microsoft Product Terms
Note:
GPT-5.4 is classified as a Premier Model. It must be explicitly enabled before users can select it. Please see the Enabling Premier Models section to learn more about enabling Premier Models.
Usage of Premier Models will incur additional cost (MAUs). Administrators and users should be aware of this before enabling this model.
GPT-5.4 is only available on commercial SaaS tenants. It is not available on trial tenants, GovCloud/HIPAA environments, or on-premises deployments.
GPT-OSS models require special considerations. For more information, see Special considerations.
If you’re migrating from Llama to GPT-OSS-120B, see the Migration guide for step-by-step instructions and best practices.
GPT-OSS-120b is a non-IBM product governed by a third-party license that may impose use restrictions and other obligations. By using this model you agree to the terms. Read the terms.
GPT-OSS-120b provided by Groq is not available in AWS GovCloud.
​
Optimized Models
Models marked with a ★ have undergone extensive evaluation and are optimized for use with watsonx Orchestrate agents. These models appear as preferred when you run the orchestrate models list command, and are shown as supported on the Manage Agents page in the UI.
​
Using Groq Models Locally
For local development with the Developer Edition, you can use groq/openai/gpt-oss-120b by:
Via watsonx Orchestrate proxy (default): When connected to a SaaS instance, LLM requests are automatically proxied through watsonx Orchestrate without requiring your own Groq API key
With your own API key: Set GROQ_API_KEY in your .env file to use your own Groq account
This allows you to test and develop agents locally while leveraging the optimized gpt-oss-120b model.
​
Virtual Models
watsonx Orchestrate allows you to register models from additional providers as virtual models. These models can be added via the ADK and will be automatically made available to users of the platform. [2]
​
Important Considerations
Tool calling required: Only models that support tool calling will work with watsonx Orchestrate agents
Compatibility not guaranteed: Virtual models are not validated for compatibility with watsonx Orchestrate, unlike the optimized models listed above
Testing required: Thoroughly test virtual models before production use. See Understanding Virtual Models for detailed compatibility considerations
Additional costs: Using virtual models may incur additional costs from the upstream provider
For detailed information about virtual model compatibility, custom endpoints, and authentication options, see Managing custom LLMs.
​
virtual-policies
In addition to adding models, you can configure complex routing rules for your LLMs. Use virtual-policies to establish pseudo-LLM names that can load balance traffic between models or establish fallback policies for when a provider is experiencing an outage.
[1] In the Developer Edition of watsonx Orchestrate, when a WO_INSTANCE and WO_API_KEY are provided in the user’s .env file, if that instance is a SaaS instance, all LLM requests will be proxied through watsonx Orchestrate without the user needing an additional watsonx.ai entitlement.
If the instance is CPD and a WO_INSTANCE and WO_API_KEY are provided, only models deployed via IFM will be available via the watsonx/ prefix.
If neither of the above apply, either provide a WATSONX_SPACE_ID and WATSONX_APIKEY to a watsonx.ai account hosted in us-south, or add a virtual model running within your local Developer Edition server.
[2] virtual-models and virtual-policies added to a SaaS or CPD instance of watsonx Orchestrate will not automatically be available within the Developer Edition. They will need to be manually added by the user.
​
Next steps
Migrating to GPT-OSS-120B
Step-by-step guide for migrating agents from Llama to GPT-OSS-120B with optimization tips.
Managing virtual models
Learn how to manage virtual models by using the ADK’s CLI.
Model policies
Learn how to create and manage model policies for complex LLM routing and fallback.
Examples with supported providers
See how to add OpenAI, Azure, AWS Bedrock, Ollama, and many more models from different providers.
Integrate the Developer Edition with SaaS
Learn how to integrate the watsonx Orchestrate Developer Edition with your watsonx Orchestrate SaaS tenant for LLM inferencing.

---

Large Language Models (LLMs)
Enabling premier models
Premier models, including GPT-5.4, are disabled by default. A tenant administrator must enable them by using ADK CLI version 2.13.0.
Usage of premier models incurs additional costs (MAUs). Administrators must communicate this to users before enabling. Premier models are not available in trial tenants. When premier models are disabled, all agents (live and draft) that use them stop working immediately.
​
Enabling premier models for a local or default tenant
Run the following command to enable premier models on your local or default tenant.
orchestrate models config enable-premier-models
Note: If your local Developer Edition targets a remote watson Orchestrate instance because you set WO_INSTANCE and WO_API_KEY in your environment file, the command above enables premier models on your local tenant only. To make premier models available in the local UI, you must also enable them on the remote instance. The CLI warns you if this applies to your setup. To enable premier models on the remote instance, activate that environment and re-run the command. For more information, see Enabling premier models for a remote tenant (SaaS).
​
Enabling premier models for a remote tenant (SaaS)
Before you run the enable command against a remote SaaS tenant, you must activate that remote environment. Otherwise, the command applies to your local context instead.
Activate the target remote environment.
orchestrate env activate <remote-environment-name>
Enable premier models on that tenant.
orchestrate models config enable-premier-models
​
Confirming that premier models are enabled
Run the following command to check whether premier models are currently enabled on the active tenant.
orchestrate models config are-premier-models-enabled
​
Disabling premier models
To disable premier models on the active tenant, run the following command.
If you disable premier models, all agents (live and draft) that use them stop working immediately.
orchestrate models config disable-premier-models
​
GPT-5.4 pricing
For pricing information, see IBM watsonx Orchestrate (Added Premier LLM) and IBM watsonx Orchestrate on IBM Cloud (Premier LLM and Voice Terms).

---

Large Language Models (LLMs)
Using GPT-5.4
GPT-5.4 is one of OpenAI’s frontier models, available in watsonx Orchestrate through Azure. This page covers model-specific behavior and agent configuration that are relevant to developers and agent builders who use GPT-5.4.
GPT-5.4 is a premier model and must be enabled by a tenant administrator before it can be used. See Enabling premier models for instructions.
​
Agent styles
GPT-5.4 always uses the ReAct Core (react_core) agent style, regardless of the style that is set on your agent. You do not need to configure this explicitly as it is applied automatically.
Agent behavior with GPT-5.4 is architecturally similar to GPT-OSS-120B: the same instruction patterns, tool usage rules, and prompt engineering practices apply. If you have agents that are already tuned for GPT-OSS-120B, they are a solid starting point.
Model behavior is not identical across versions. When you switch to GPT-5.4, you might find that some instructions must be tightened, softened, or reworded to get the same results.
​
Tool name constraints
GPT-5.4 is served through Azure and enforces the OpenAI function object specification. One constraint that may require changes when you move from GPT-OSS-120B on Groq is the tool name format.
watsonx Orchestrate uses the display name of a tool when it builds the function payload that is sent to the model. The display name must therefore conform to the Azure specification:
Display names must match ^[a-zA-Z0-9_-]{1,64}$ — only letters, numbers, underscores, and hyphens, with a maximum length of 64 characters.
This applies to the display names of all tool types that are registered with the agent:
Skills and tools: The skill display name that is sent in the LLM payload.
Knowledge bases: The display name that is used to identify the retrieval tool.
Collaborator agents: The display name that the model uses to invoke a subagent.
​
Prompt guide
GPT-5.4 uses the same ReAct Core (react_core) agent style as GPT-OSS-120B, so the same prompt engineering principles apply. For instruction templates, tool usage rules, and best practices, see the GPT-OSS-120B prompt guide.

---
Large Language Models (LLMs)
Migrating agents from Llama to GPT-OSS-120B
Use this guide to migrate existing agents from llama-3.2-90B-vision-instruct to gpt-oss-120b. Based on extensive testing across 256 production agents, GPT-OSS-120B delivers superior performance in response time, error handling, conversational quality, and user experience when correctly configured.
GPT-OSS-120B is the default model for new agents created in watsonx Orchestrate.
GPT-OSS-120B is available through the following providers:
Groq: groq/openai/gpt-oss-120b
AWS Bedrock: bedrock/openai.gpt-oss-120b-1:0
watsonx.ai: watsonx/openai/gpt-oss-120b (GovCloud only — available in the April mid-release)
Choose the provider that best fits your deployment requirements.
​
Why migrate to GPT-OSS-120b
GPT-OSS-120B offers significant advantages over Llama models:
Faster response times across all scenarios
Superior error handling with intelligent recovery and detailed explanations
Enhanced conversational efficiency through single-turn parameter collection
Better memory and context retention across multi-turn dialogues
Improved safety with robust out-of-scope request handling
More natural interactions that feel less robotic
​
Before you begin
​
Prerequisites
Access to watsonx Orchestrate (SaaS or Developer Edition)
Existing agents built with Llama models
Familiarity with agent configuration and prompt engineering
​
Understanding the differences
GPT-OSS-120B behaves differently from Llama models in the following ways:
Aspect	Llama 3.2 90B	GPT-OSS-120B
System prompt	Uses standard watsonx Orchestrate system prompt	Does not use standard system prompt
Knowledge preference	Balanced between internal and external knowledge	Prefers internal knowledge unless instructed otherwise
Parameter collection	Turn-by-turn questioning	Single-turn collection of multiple parameters
Error communication	Generic error messages	Context-aware, detailed explanations
Instruction following	Flexible interpretation	Literal, precise following of examples
Reasoning approach	Concise execution	More exploratory with additional tool calls
​
Migration process
1
Review your agent configuration

Export your existing Llama-based agent to review its current configuration:
orchestrate agents export -n <agent-name> -k native -o agent-backup.zip
Document the following elements:
Agent instructions and tone
Tool usage patterns
Knowledge base dependencies
Expected user interaction flows
2
Update the LLM configuration

Update your agent configuration to use GPT-OSS-120B. Choose the provider that matches your deployment:

Groq

AWS Bedrock

Groq (JSON)

AWS Bedrock (JSON)

Groq (Python)

AWS Bedrock (Python)
llm: groq/openai/gpt-oss-120b
3
Optimize agent instructions

GPT-OSS-120B requires explicit, model-specific instructions. Add the following blocks to your agent instructions as needed:
​
Essential instruction template
Use this template as a starting point:
Behavior and sources:
- Identify as an agent operating within watsonx Orchestrate.
- Always use available tools to retrieve information before relying on your internal knowledge.
- If tools don't contain the answer, state "The available tools don't contain the answer" and ask one clarifying question.

Reasoning and brevity controls:
- Use concise reasoning with at most 3 reasoning steps before responding.
- Keep chit-chat to one sentence, then proceed.
- Limit final answers to ≤150 words unless the user requests detail.

Error handling:
- If required inputs are missing, ask for the minimum missing fields in a single question.
- When errors occur, explain what went wrong and suggest next steps.

Formatting:
- Use proper Markdown syntax for hyperlinks: [link text](url)
- Format responses clearly with appropriate structure.
​
Prioritize knowledge bases (if applicable)
If your agent uses knowledge bases, add the following instruction:
Always check the connected knowledge base(s) first.
Prefer information retrieved from knowledge over your
own internal knowledge. If relevant content is found,
summarize it faithfully and cite the source title or document
name. If the knowledge base does not contain the answer, say
"I don't know based on the provided knowledge" and ask
a clarifying question.
​
Optimize tool usage
For agents with multiple tools, add explicit guidance:
Tool usage rules:
- Use the [tool_name] tool for [specific purpose].
- Call tools with all available information; don't ask for parameters you can infer.
- If a tool returns an error, analyze the error message and retry with corrections.
- If a tool fails after 2 attempts, inform the user and suggest alternatives.
​
Control agent routing (for supervisor agents)
If your agent delegates to other agents, use explicit action verbs in the instructions:
Agent delegation:
- Call the [agent_name] agent when [specific condition].
- Execute the agent call immediately with available information.
- Do NOT ask for additional parameters before calling the agent unless absolutely required.
4
Remove problematic patterns

Overly specific examples can constrain GPT-OSS-120B. Review your instructions and update accordingly:
❌ Avoid:
When updating employee data, ask for:
1. Employee name
2. Department
3. Location
Then call the update_employee tool.
✅ Prefer:
When updating employee data, collect all required parameters
(name, department, location) in a single question, then call
the update_employee tool.
❌ Avoid:
If the user asks about weather, say "I cannot help with that."
If they ask about sports, say "That's outside my scope."
If they ask about news, say "I don't have access to that."
✅ Prefer:
If the user asks about topics outside your capabilities,
politely acknowledge the request and redirect to your
primary function.
5
Test and validate

After you update your agent configuration, run the following tests:
Test basic interactions:
orchestrate chat ask --agent-name <agent-name> "Hello"
Test tool calling: Verify that tools are called correctly with the appropriate parameters.
Test error scenarios: Confirm that error messages are clear and that recovery is handled correctly.
Test multi-turn conversations: Confirm that context is retained across multiple exchanges.
Test edge cases: Validate behavior with incomplete information, out-of-scope requests, and ambiguous queries.
6
Deploy and monitor

Import the updated agent:
orchestrate agents import -f updated-agent.yaml
Monitor initial usage for:
Response quality and accuracy
Tool call precision
User satisfaction
Error rates and recovery success
​
Recommended config parameters for gpt-oss-120b
Use the following config block as a starting configuration when you register gpt-oss-120b as a virtual model. You can adjust the values as needed. Refer to your LLM provider’s documentation for details on how max_completion_tokens, temperature, reasoning_effort, and seed affect model behaviour:
Groq API reference
watsonx.ai chat completions
AWS Bedrock Converse API
config:
  max_completion_tokens: 8192
  temperature: 0.0
  reasoning_effort: low
  seed: 123
Include this block in your model specification for each provider:

Groq

watsonx.ai
spec_version: v1
kind: model
name: virtual-model/groq/openai/gpt-oss-120b
display_name: GPT-OSS-120b (Groq)
tags:
  - openai
  - gpt-oss-120b
model_type: chat
provider_config:
  custom_host: https://api.groq.com/openai/v1
config:
  max_completion_tokens: 8192
  temperature: 0.0
  reasoning_effort: low
  seed: 123
​
Common migration challenges
​
Challenge 1: Over-reliance on internal knowledge
Symptom: The agent provides answers from its training data instead of using tools or knowledge bases.
Solution: Add explicit knowledge prioritization instructions (see Step 3).
​
Challenge 2: Excessive parameter collection
Symptom: The agent asks for parameters before routing to specialized agents or calling tools.
Solution: Use strong negations in instructions:
Do NOT ask for [parameter_name] before calling [tool/agent].
Call immediately with available information.
​
Challenge 3: Literal example following
Symptom: The agent handles only scenarios exactly as shown in examples.
Solution: Remove specific examples and use generic patterns instead.
​
Challenge 4: Tool call precision issues
Symptom: The agent makes irrelevant tool calls or misses required calls.
Solution:
Improve tool descriptions with clear use cases.
Add explicit tool usage rules in instructions.
Test iteratively and refine based on results.
​
Challenge 5: Agent routing confusion
Symptom: The agent returns JSON instead of executing agent calls.
Solution: Replace implicit instructions with explicit ones:
❌ "Delegate to the appropriate agent"
✅ "Call the [agent_name] agent with the information you have"
​
Prompt engineering best practices
​
Do
✅ Use explicit action verbs (“Call”, “Execute”, “Use”).
✅ Provide strong negations for unwanted behaviors.
✅ Keep examples generic and minimal.
✅ Trust the model’s reasoning capabilities.
✅ Use single-turn parameter collection.
✅ Test iteratively with real scenarios.
​
Do not
❌ Rely on implicit instructions (“delegate”, “route”).
❌ Provide overly specific examples that constrain behavior.
❌ List exhaustive value options (the agent might limit itself).
❌ Use weak negations for critical constraints.
❌ Force turn-by-turn parameter collection.
❌ Over-constrain conversational patterns.
​
Performance optimization tips
​
Reduce response latency
Reasoning efficiency:
- Limit yourself to 3 reasoning steps maximum.
- Do not re-plan unless the last tool result contradicts prior assumptions.
- If you cannot progress after 3 steps, ask one focused question.
​
Improve conversational flow
Conversation style:
- Collect multiple related parameters in a single question.
- Avoid asking for information you can reasonably infer.
- Keep responses concise and action-oriented.
​
Enhance error recovery
Error handling strategy:
- When a tool fails, analyze the error message carefully.
- Retry with intelligent corrections based on the error.
- After 2 failed attempts, explain the issue and suggest alternatives.
- Extract useful information from partial failures when possible.
​
Validation checklist
Before you consider the migration complete, verify the following:
Agent uses GPT-OSS-120B (via Groq, AWS Bedrock, or watsonx) as the LLM
Instructions include model-specific optimizations
Knowledge base prioritization is configured (if applicable)
Tool usage rules are explicit and clear
Agent routing uses explicit action verbs (if applicable)
Overly specific examples have been removed
Basic interactions work as expected
Tool calling is accurate and efficient
Error handling is clear and helpful
Multi-turn conversations maintain context
Edge cases are handled gracefully
​
Troubleshooting
Agent is too verbose

Agent ignores knowledge bases

Agent makes too many tool calls

Agent does not follow instructions

​
Next steps
Managing agents
Update, export, and manage your migrated agents.
Agent descriptions and instructions
Write effective instructions for GPT-OSS-120B.
Managing custom LLMs
Explore advanced LLM configuration options.
Model policies
Set up fallback policies and load balancing for production resilience.
​
Additional resources
GPT-OSS-120B model documentation
Choosing your LLM
Agent evaluation and testing
Prompt engineering guidelines
---

Large Language Models (LLMs)
Managing virtual models
Integrate third-party LLM models from a variety of supported providers as virtual models.
​
Supported providers
Provider	Provider ID
OpenAI	openai
watsonx.ai	watsonx
Groq	groq
Anthropic	anthropic
Google Gen AI	google
Gemini Enterprise Agent Platform	vertex-ai
Azure AI	azure-ai
Azure OpenAI	azure-openai
AWS Bedrock	bedrock
Mistral	mistral-ai
OpenRouter	openrouter
x.ai	x-ai
Ollama	ollama
Red Hat OpenShift AI	redhat-ai
When you import a model from OpenRouter, always set the max_token parameter explicitly. If you omit this parameter, the system defaults to 65536 tokens. This high token count can cause the request to fail if you do not have enough credits.
GPT-OSS-120b is a non-IBM product governed by a third-party license that may impose use restrictions and other obligations. By using this model, you agree to the terms. Read the terms.
​
Understanding virtual models
You can configure watsonx Orchestrate to register an external model or provider as a virtual model. Consider the following important limitations before you proceed.
​
Compatibility and support
Not every model and provider combination is supported or tested. The supported providers list shows providers that have been tested, but this does not guarantee that every model on every listed provider works. Consider the following:
New models and API changes: Models are released frequently, and some introduce API specification changes that can cause runtime errors.
Intermediate infrastructure: Components in the request path between watsonx Orchestrate and the provider (such as gateways, proxies, or adapters) can introduce incompatibilities or special authentication requirements that watsonx Orchestrate does not support.
Model suitability: Not all models are suited for agentic workflows. Even when a model registers successfully and runs without errors, the results might not be accurate enough for business-critical agents.
​
Optimized support
watsonx Orchestrate provides optimized support for:
gpt-oss-120b via Groq or AWS Bedrock
gpt-oss-120b via watsonx.ai in GovCloud environments (available in the April mid-release)
These model and provider combinations have undergone extensive testing and optimization for agent workflows.
​
Testing requirements
When you register virtual models with other providers, allocate sufficient time to validate that the combination works correctly. Testing can identify incompatibilities that prevent the agent from functioning as expected.
​
Using custom provider endpoints
If you self-host an LLM or use a model proxy or gateway as a pass-through to another provider, you can use OpenAI chat completion compatibility. This section covers authentication options for custom endpoints.
​
OpenAI-compatible with API key authentication
The default base URL for the openai provider is https://api.openai.com/v1. For self-hosted OpenAI-compatible endpoints, ensure that your full URL ends with /chat/completions, but exclude this path when you provide the custom_host during registration.
Authentication format:
Authorization: Bearer ${apiKey}
Example:
1
Define the model specification

custom-openai-model.yaml
spec_version: v1
kind: model
name: openai/your-model-id
model_type: chat
provider_config:
  api_key: "your-apikey"
  custom_host: "https://your-url"
Note: Do not include /chat/completions in the custom_host value.
2
Register the model

orchestrate models import --file custom-openai-model.yaml
​
OpenAI-compatible with OAuth 2.0 authentication
For self-hosted OpenAI-compatible endpoints that use OAuth 2.0 client credentials authentication, use the openai-oauth2-client-creds provider type. Use this option when your OAuth token endpoint is separate from your LLM inferencing endpoint.
Prerequisites: Your LLM inferencing URL must meet the following requirements:
End with /chat/completions (per the OpenAI spec)
Accept OAuth tokens in the request header: Authorization: Bearer your-access-token
1
Create OAuth connection

First, create a Team application/connection in watsonx Orchestrate. See OAuth 2.0 Client Credentials for details.
Example OAuth token endpoint:
response = requests.post(
    token_url,
    auth=(client_id, client_secret),
    headers={"Content-Type": "application/x-www-form-urlencoded"},
    data={"grant_type": "client_credentials"}
)
2
Register the model

orchestrate models add \
  --name "openai-oauth2-client-creds/your-model-id" \
  --provider-config '{"custom_host": "https://your-llm-inferencing-url"}' \
  --app-id your-app-id-from-step-1
Note: Exclude /chat/completions from the custom_host value.
Custom endpoints and intermediate infrastructure such as proxies and gateways might not be fully supported. Test thoroughly before using in production.
​
CLI Reference
Importing from a file
Using the CLI only
Add a virtual model to watsonx Orchestrate by using the orchestrate models import command.
1
Define the model specification file

granite-3-3-8b-model.yaml
spec_version: v1
kind: model
name: virtual-model/watsonx/ibm/granite-3.3-8b-instruct
display_name: IBM watsonx.ai (Granite)
description: |
IBM watsonx.ai model using Space-scoped configuration.
tags:
- ibm
- watsonx
model_type: chat
provider_config:
    watsonx_space_id: my-space-id # For any non-sensitive field not already provided by the connection
Show properties

2
Create an API key connection

BASH
orchestrate connections add -a watsonx_credentials
orchestrate connections configure -a watsonx_credentials --env draft -k key_value -t team
orchestrate connections set-credentials -a watsonx_credentials --env draft -e "api_key=my_watsonx_api_key"
3
Add the model

BASH
orchestrate models import --file watsonx-model.yaml --app-id watsonx_credentials
Arguments:
--file (-f): File path of the spec file containing the model configuration.
--app-id (-a): The app ID of a key_value connection containing provider configuration details. These will be merged with the values provided in the provider_config section of the spec.
--skip-validation: Skip the automatic post-import validation check. See Validating virtual models for details.
After a successful import, validation runs automatically for new models. Embedding models are skipped. If validation fails, the model remains registered. Decide whether to proceed with a model that does not pass all checks.
​
Validating virtual models
The orchestrate models validate command tests whether a registered virtual model has the capabilities that are required for agentic behavior in watsonx Orchestrate. The command runs automatically after orchestrate models import and orchestrate models add for virtual models, and you can also run it on demand.
BASH
orchestrate models validate --name virtual-model/groq/openai/gpt-oss-120b
Arguments:
--name (-n): The name of the virtual model to validate. The name must match the registered model name exactly, including the virtual-model/ prefix.
--verbose (-v): Output full JSON results including per-test responses and tool call details.
​
What is tested
The command runs four test cases that cover the capabilities required by the watsonx Orchestrate agent runtime:
Test case	What it checks
basic_invocation	The model responds correctly to a simple prompt
streaming	The model supports streamed responses
tool_calling	The model can call a function, a tool, or both, and incorporate the result
streaming_tool_calling	The model can call a function, a tool, or both, and stream the response
​
Limitations
Virtual models only: Validation runs only against virtual models (models whose name starts with virtual-model/). You cannot use it to test out-of-the-box (OOTB) models.
Embedding models not supported: Do not use the orchestrate models validate command with embedding models. Embedding models do not support inference or tool calling and are skipped automatically during post-import validation.
​
Understanding the output
After the command runs, a summary table and a per-test results table are displayed. Each test shows a success or failure status and a duration in milliseconds.
If any test fails, the overall result is failed. The model remains registered regardless of the outcome. Review the failing test cases to determine whether the model is suitable for your use case.
The following are common failure patterns:
All tests fail with an HTTP error (for example, a 404): The model name might be incorrect, the model might not exist at the provider, or your credentials might not have access to it. Verify the model name and your connection credentials.
Inference tests pass but tool calling tests fail: The model can respond to prompts but does not support function or tool calling. Because tool calling is required for agentic behavior in watsonx Orchestrate, this model cannot be used as an agent LLM.
Validation Summary showing Result: passed and Test Results table with all four test cases at success status
All four tests passing — the model is suitable for use as an agent LLM

Validation Summary showing Result: failed and Test Results table with basic_invocation and streaming at success, tool_calling and streaming_tool_calling at failed
Partial failure — the model supports inference but not tool calling

Pass --verbose (-v) to get the full JSON output, which includes the raw model response, error codes, and tool call details for each test case:
BASH
orchestrate models validate --name virtual-model/groq/openai/gpt-oss-120b --verbose
Show Example verbose JSON output — all tests passing

Show Example verbose JSON output — model not found (all tests failing)

Show Example verbose JSON output — model does not support tool calling (partial failure)

​
Skipping automatic validation
Both orchestrate models import and orchestrate models add run validation automatically after a successful registration. To skip validation, pass the --skip-validation flag:
BASH
# Skip validation when importing from a spec file
orchestrate models import --file my-model.yaml --app-id my_credentials --skip-validation

# Skip validation when adding via the CLI
orchestrate models add --name virtual-model/openai/gpt-5 --app-id my_credentials --skip-validation
Skip validation in the following situations:
You are scripting bulk imports and plan to validate separately by using orchestrate models validate.
The model endpoint is temporarily unavailable at import time.
You do not want to wait for validation to complete during import.
​
Examples using the supported providers
The following sections provide examples and supported schemas for each model provider.
OpenAI

​
provider_config
object
The fields which can either be set by connection or by the provider_config field of the model. Values from a connection will be merged with the provider_config.
Hide properties

​
api_key
stringrequired
The API key for the provider
​
custom_host
string
Send requests to a custom hostname other than the default for the provider
​
response_headers
list[string]
Add one or more additional response headers in the form ["header:value", "header2:value2"] to the request to the server.
​
response_timeout
number
The response timeout in seconds
​
transform_to_form_data
boolean
Transforms the request to form_data.
Example usage:
1
Define the model specification file

Define a specification file with the model details and provider configuration:
gpt-5-2025-08-07.yaml
spec_version: v1
kind: model
name: openai/gpt-5-2025-08-07
display_name: GPT 5
description: |-
    GPT-5 is our flagship model for coding, reasoning, and agentic tasks across domains. Learn more in our GPT-5 usage guide.
tags:
- openai
- gpt
model_type: chat
provider_config:
    custom_host: https://my-openai-compatible-server
2
Create an API key connection

To use the OpenAI API key securely, first create a connection:
BASH
orchestrate connections add -a openai_credentials
orchestrate connections configure -a openai_credentials --env draft -k key_value -t team
orchestrate connections set-credentials -a openai_credentials --env draft -e "api_key=my_openai_key"
3
Add the model

Add the model by using the specification file and the connection you created:
BASH
orchestrate models import --file gpt-5-2025-08-07 --app-id openai_credentials
watsonx.ai

​
provider_config
object
The fields which can either be set by connection or by the provider_config field of the model. Values from a connection will be merged with the provider_config.
Hide properties

​
api_key
stringrequired
The API key for the provider.
​
custom_host
stringrequired
The service instance url of the watsonx.ai instance
​
watsonx_space_id
stringconditionally required
At least one of space/project/deployment is required
​
watsonx_project_id
stringconditionally required
At least one of space/project/deployment is required
​
watsonx_deployment_id
stringconditionally required
At least one of space/project/deployment is required
​
watsonx_cpd_url
stringconditionally required
When connecting to a watsonx.ai instance hosted in CPD, this is the url of the CPD cluster hosting watsonx.ai.
Required connecting to on-prem (CPD) hosted wx.ai instances
​
watsonx_cpd_username
stringconditionally required
When connecting to a watsonx.ai instance hosted in CPD, this is username of a user with access to the CPD cluster.
Required connecting to on-prem (CPD) hosted wx.ai instances
​
watsonx_cpd_password
stringconditionally required
When connecting to a watsonx.ai instance hosted in CPD, this is password of a user with access to the CPD cluster.
Required connecting to on-prem (CPD) hosted wx.ai instances
​
response_timeout
number
The response timeout in seconds
Example usage:
1
Define the model specification file

watsonx-model.yaml
spec_version: v1
kind: model
name: watsonx/ibm/granite-3.3-8b-instruct
display_name: IBM watsonx.ai (Granite)
description: |
    IBM watsonx.ai model using Space-scoped configuration.
tags:
- ibm
- watsonx
model_type: chat
provider_config:
    watsonx_space_id: my-space-id
When registering gpt-oss-120b via watsonx.ai, you must include a config block. See Required config parameters for gpt-oss-120b for details.
2
Create an API key connection

BASH
orchestrate connections add -a watsonx_credentials
orchestrate connections configure -a watsonx_credentials --env draft -k key_value -t team
orchestrate connections set-credentials -a watsonx_credentials --env draft -e "api_key=my_watsonx_api_key"
When you add a watsonx.ai virtual model, include the provider configuration details. Without them, chat access to the model can fail. Provide custom host details by using the --provider-config flag in the orchestrate models add command. For more information, see Using the CLI only.
3
Add the model

BASH
orchestrate models import --file watsonx-model.yaml --app-id watsonx_credentials
Notes:
Provide one of: watsonx_space_id, watsonx_project_id, or watsonx_deployment_id.
Include watsonx_cpd_url, watsonx_cpd_username, watsonx_cpd_password only for on-prem (CPD) setups.
When you register Deploy on Demand (DoD) models, explicitly provide the model configuration. Set these configuration values according to the model’s requirements because they are not automatically transferred during inference from watsonx Orchestrate.
Show example

Groq

​
provider_config
object
The fields which can either be set by connection or by the provider_config field of the model. Values from a connection will be merged with the provider_config.
Hide properties

​
api_key
stringrequired
The API key for the provider
​
custom_host
stringrequired
Send requests to a custom hostname for the provider
​
response_headers
list[string]
Add one or more additional response headers in the form ["header:value", "header2:value2"] to the request to the server
​
response_timeout
number
The response timeout in seconds
Example usage:
1
Define the model specification file

Define a specification file with the model details and provider configuration:
gpt-oss-120b.yaml
spec_version: v1
kind: model
name: virtual-model/groq/openai/gpt-oss-120b
display_name: openai/gpt-oss-120b # Optional
description: Welcome to the gpt-oss series, OpenAI's open-weight models designed for powerful reasoning, agentic tasks, and versatile developer use cases.
tags:
  - openai
  - gpt-oss-120b
model_type: chat # Optional. Default is "chat". Options: ["chat"|"embedding"]
app_id: groq_credentials
provider_config:
    custom_host: https://api.groq.com/openai/v1
When you register gpt-oss-120b as a virtual model, you must include a config block. See Required config parameters for gpt-oss-120b for details.
2
Create an API key connection

To use the API key securely, first create a connection:
BASH
orchestrate connections add -a groq_credentials
orchestrate connections configure -a groq_credentials --env draft -k key_value -t team
orchestrate connections set-credentials -a groq_credentials --env draft -e "api_key=my_openai_key"
3
Add the model

Add the model by using the specification file and the connection you created:
BASH
orchestrate models import --file gpt-oss-120b.yaml --app-id groq_credentials
Anthropic

​
provider_config
object
The fields which can either be set by connection or by the provider_config field of the model. Values from a connection will be merged with the provider_config.
Hide properties

​
api_key
stringrequired
The API key for the provider.
​
anthropic_beta
string
​
anthropic_version
string
​
response_headers
list[string]
Add one or more additional response headers in the form ["header:value", "header2:value2"] to the request to the server.
​
response_timeout
number
The response timeout in seconds
Example usage:
1
Define the model specification file

anthropic-claude.yaml
spec_version: v1
kind: model
name: anthropic/claude-3
display_name: Anthropic Claude 3
description: |
    Anthropic Claude model for safe and helpful AI interactions.
tags:
- anthropic
- claude
model_type: chat
provider_config: {}
2
Create an API key connection

BASH
orchestrate connections add -a anthropic_credentials
orchestrate connections configure -a anthropic_credentials --env draft -k key_value -t team
orchestrate connections set-credentials -a anthropic_credentials --env draft -e "api_key=my_anthropic_key"
3
Add the model

BASH
orchestrate models import --file anthropic-claude.yaml --app-id anthropic_credentials
Google Gen AI

​
provider_config
object
The fields which can either be set by connection or by the provider_config field of the model. Values from a connection will be merged with the provider_config.
Hide properties

​
api_key
stringrequired
The API key for the provider.
​
response_headers
list[string]
Add one or more additional response headers in the form ["header:value", "header2:value2"] to the request to the server.
​
response_timeout
number
The response timeout in seconds
Example usage:
1
Define the model specification file

google-genai.yaml
spec_version: v1
kind: model
name: google/gemini-2.5-pro
display_name: Google Generative AI (Gemini 2.5 Pro)
description: |
    Google Generative AI model via API key authentication.
tags:
- google
- genai
model_type: chat
provider_config: {}
2
Create an API key connection

BASH
orchestrate connections add -a google_credentials
orchestrate connections configure -a google_credentials --env draft -k key_value -t team
orchestrate connections set-credentials -a google_credentials --env draft -e "api_key=my_google_api_key"
3
Add the model

BASH
orchestrate models import --file google-genai.yaml --app-id google_credentials
Gemini Enterprise Agent Platform

Known Limitations:
API key authentication is not supported. Use service account JSON authentication instead.
For more details, see Known issues and limitations.
​
provider_config
object
The fields which can be set in the provider_config field of the model.
Hide properties

​
vertex_region
stringrequired
The GCP region for Gemini Enterprise Agent Platform.
​
vertex_service_account_json
object
The complete service account JSON object for authentication. This includes all necessary credentials for accessing Gemini Enterprise Agent Platform.
​
response_headers
list[string]
Add one or more additional response headers in the form ["header:value", "header2:value2"] to the request to the server.
​
response_timeout
number
The response timeout in seconds.
Example usage:
1
Define the model specification file

my-provider.yaml
spec_version: v1
kind: model
name: vertex-ai/gemini-3.1-pro-preview
display_name: Gemini Enterprise Agent Platform (Gemini 3.1 Pro)
description: Gemini Enterprise Agent Platform model via service account authentication
tags:
  - google
  - vertex-ai
model_type: chat
provider_config:
  vertex_region: <region>
  vertex_service_account_json:
    type: service_account
    project_id: <project-id>
    private_key_id: <private-key-id>
    private_key: <private-key>
    client_email: <client-email>
    client_id: <client-id>
    auth_uri: <auth-uri>
    token_uri: <token-uri>
    auth_provider_x509_cert_url: <auth-provider-cert-url>
    client_x509_cert_url: <client-cert-url>
    universe_domain: <universe-domain>
2
Add the model

BASH
orchestrate models import --file my-provider.yaml
Azure

​
provider_config
object
The fields which can either be set by connection or by the provider_config field of the model. Values from a connection will be merged with the provider_config.
Hide properties

​
api_key
stringrequired
The API key for the provider
​
azure_resource_name
stringrequired
​
azure_deployment_id
stringrequired
​
azure_api_version
stringrequired
​
azure_model_name
stringrequired
​
custom_host
string
Send requests to a custom hostname other than the default for the provider
​
response_headers
list[string]
Add one or more additional response headers in the form ["header:value", "header2:value2"] to the request to the server.
​
response_timeout
number
The response timeout in seconds
Example usage:
1
Define the model specification file

azure-gpt.yaml
spec_version: v1
kind: model
name: azure/gpt-4
display_name: Azure GPT-4
description: |
    Azure-hosted GPT model for enterprise-grade AI workloads.
tags:
- azure
- gpt
model_type: chat
provider_config:
    azure_resource_name: my-resource
    azure_deployment_id: my-deployment
    azure_api_version: 2024-05-01
2
Create an API key connection

BASH
orchestrate connections add -a azure_credentials
orchestrate connections configure -a azure_credentials --env draft -k key_value -t team
orchestrate connections set-credentials -a azure_credentials --env draft -e "api_key=my_azure_key"
3
Add the model

BASH
orchestrate models import --file azure-gpt.yaml --app-id azure_credentials
Azure OpenAI

​
provider_config
object
The fields which can either be set by connection or by the provider_config field of the model. Values from a connection will be merged with the provider_config.
Hide properties

​
api_key
stringrequired
The API key for the provider
​
azure_model_name
string
​
azure_resource_name
stringrequired
​
azure_deployment_id
stringrequired
​
azure_api_version
stringrequired
​
ad_auth
boolean
​
azure_auth_mode
string
​
azure_managed_client_id
string
​
azure_entra_client_id
string
​
azure_entra_client_secret
string
​
azure_entra_tenant_id
string
​
azure_ad_token
string
​
response_headers
list[string]
Add one or more additional response headers in the form ["header:value", "header2:value2"] to the request to the server.
​
response_timeout
number
The response timeout in seconds
Example usage:
1
Define the model specification file

azure-openai-gpt.yaml
spec_version: v1
kind: model
name: azure-openai/gpt-4
display_name: Azure OpenAI GPT-4
description: |
    Azure OpenAI GPT-4 model for enterprise workloads.
tags:
- azure
- openai
model_type: chat
provider_config:
    azure_resource_name: my-resource
    azure_deployment_id: my-deployment
    azure_api_version: 2024-05-01
    custom_host: <host_url>
2
Create an API key connection

BASH
orchestrate connections add -a azure_openai_credentials
orchestrate connections configure -a azure_openai_credentials --env draft -k key_value -t team
orchestrate connections set-credentials -a azure_openai_credentials --env draft -e "api_key=my_azure_openai_key"
3
Add the model

BASH
orchestrate models import --file azure-openai-gpt.yaml --app-id azure_openai_credentials
AWS Bedrock

​
provider_config
object
The fields which can either be set by connection or by the provider_config field of the model. Values from a connection will be merged with the provider_config.
Hide properties

​
api_key
stringrequired
The API key for the provider.
Either the api_key must be provided, or both the aws_secret_access_key and aws_access_key_id must be provided
​
aws_secret_access_key
stringrequired
The aws_secret_access_key.
Either the api_key must be provided, or both the aws_secret_access_key and aws_access_key_id must be provided
​
aws_access_key_id
stringrequired
The aws_access_key_id.
Either the api_key must be provided, or both the aws_secret_access_key and aws_access_key_id must be provided
​
aws_session_token
string
​
aws_region
string
​
aws_auth_type
string
​
aws_role_arn
string
​
aws_external_id
string
​
aws_s3_bucket
string
​
aws_s3_object_key
string
​
aws_bedrock_model
string
​
aws_server_side_encryption
string
​
aws_server_side_encryption_kms_key_id
string
​
response_headers
list[string]
Add one or more additional response headers in the form ["header:value", "header2:value2"] to the request to the server.
​
response_timeout
number
The response timeout in seconds
Example usage:
1
Define the model specification file

aws-bedrock-model.yaml
spec_version: v1
kind: model
name: bedrock/us.anthropic.claude-3-5-sonnet-20241022-v2:0
display_name: AWS Bedrock Claude
description: |
    AWS Bedrock integration for foundation models like Claude.
tags:
- aws
- bedrock
model_type: chat
provider_config:
    aws_region: us-east-1
2
Create an API key connection

BASH
orchestrate connections add -a aws_bedrock_credentials
orchestrate connections configure -a aws_bedrock_credentials --env draft -k key_value -t team
orchestrate connections set-credentials -a aws_bedrock_credentials --env draft -e "api_key=my_aws_key"
3
Add the model

BASH
orchestrate models import --file aws-bedrock-model.yaml --app-id aws_bedrock_credentials
Provide either the api_key, aws_secret_access_key, or aws_access_key_id.
Provide the model name in the name field.
When you register Deploy on Demand (DoD) models, explicitly provide the model configuration. Set these configuration values according to the model’s requirements because they are not automatically transferred during inference from watsonx Orchestrate.
Show example

Mistral

​
provider_config
object
The fields which can either be set by connection or by the provider_config field of the model. Values from a connection will be merged with the provider_config.
Hide properties

​
api_key
stringrequired
The API key for the provider.
​
mistral_fim_completion
boolean
​
response_headers
list[string]
Add one or more additional response headers in the form ["header:value", "header2:value2"] to the request to the server.
​
response_timeout
number
The response timeout in seconds
Example usage:
1
Define the model specification file

mistral-large.yaml
spec_version: v1
kind: model
name: mistralai/mistral-7b-instruct-v0.3
display_name: Mistral 7B Instruct v0.3
description: |
    Mistral model for general-purpose reasoning and coding tasks.
tags:
- mistral
model_type: chat
provider_config:
    mistral_fim_completion: false
2
Create an API key connection

BASH
orchestrate connections add -a mistral_credentials
orchestrate connections configure -a mistral_credentials --env draft -k key_value -t team
orchestrate connections set-credentials -a mistral_credentials --env draft -e "api_key=my_mistral_api_key"
3
Add the model

BASH
orchestrate models import --file mistral-large.yaml --app-id mistral_credentials
OpenRouter

​
provider_config
object
The fields which can either be set by connection or by the provider_config field of the model. Values from a connection will be merged with the provider_config.
Hide properties

​
api_key
stringrequired
The API key for the provider.
​
response_headers
list[string]
Add one or more additional response headers in the form ["header:value", "header2:value2"] to the request to the server.
​
response_timeout
number
The response timeout in seconds
Example usage:
1
Create an API key connection

BASH
orchestrate connections add -a openrouter_credentials
orchestrate connections configure -a openrouter_credentials --env draft -k key_value -t team
orchestrate connections set-credentials -a openrouter_credentials --env draft -e "api_key=my_openrouter_api_key"
2
Define the model specification file

openrouter-model.yaml
spec_version: v1
kind: model
name: openrouter/openai/gpt-5
display_name: OpenRouter GPT-5 Chat
description: |
    OpenRouter model for routing requests across multiple LLM providers.
tags:
- openrouter
- gpt
model_type: chat
provider_config: {}
3
Add the model

BASH
orchestrate models import --file openrouter-model.yaml --app-id openrouter_credentials
x.ai

​
provider_config
object
The fields which can either be set by connection or by the provider_config field of the model. Values from a connection will be merged with the provider_config.
Hide properties

​
api_key
stringrequired
The API key for the provider.
​
response_headers
list[string]
Add one or more additional response headers in the form ["header:value", "header2:value2"] to the request to the server.
​
response_timeout
number
The response timeout in seconds
Example usage:
1
Create an API key connection

BASH
orchestrate connections add -a xai_credentials
orchestrate connections configure -a xai_credentials --env draft -k key_value -t team
orchestrate connections set-credentials -a xai_credentials --env draft -e "api_key=xai_api_key"
2
Define the model specification file

xai-model.yaml
spec_version: v1
kind: model
name: virtual-model/x-ai/grok
display_name: Grok
description: |
    x.ai model
tags:
- x.ai
- gpt
model_type: chat
provider_config: {}
3
Add the model

BASH
orchestrate models import --file xai-model.yaml --app-id xai_credentials
Ollama

​
provider_config
object
The fields which can either be set by connection or by the provider_config field of the model. Values from a connection will be merged with the provider_config.
Hide properties

​
api_key
stringrequired
The API key for the provider
​
custom_host
stringrequired
Send requests to a custom hostname other than the default for the provider
​
url_to_fetch
stringconditionally required
The Ollama url to fetch the list of available ollama models
​
response_headers
list[string]
Add one or more additional response headers in the form ["header:value", "header2:value2"] to the request to the server.
​
response_timeout
number
The response timeout in seconds
​
transform_to_form_data
boolean
Transforms the request to form_data.
Example usage:
1
Start ollama

On some systems, ollama runs under systemctl. Stop it before you start the Ollama server:
systemctl stop ollama
Then start the Ollama server and download the model:
ollama pull llama3.2:latest
export OLLAMA_HOST=0.0.0.0:11434
ollama serve
2
Get your IP address

Get your network IP address by running:

Windows

Linux

macOS
ipconfig # get the IPv4 address
3
Testing your connection

Before you import the model, test your connection to confirm that the watsonx Orchestrate Developer Edition server can reach the Ollama server.
Run the following curl command to test your connection, replacing 198.51.100.42 with the IP address you obtained in the previous step:
curl --request POST \
--url http://198.51.100.42:11434/v1/chat/completions \
--header 'content-type: application/json' \
--data '{
"model": "llama3.2:latest",
"messages": [
{
"content": "Hi",
"role": "user"
}
]
}'
Enter the watsonx Orchestrate Developer Edition gateway container:
docker exec -it docker-wxo-agent-gateway-1 sh
Run the curl command again from within the container shell.
If you experience connection issues with Ollama, try the following:
Wait a few minutes after starting the server before running the command.
Restart the Ollama server.
Close any VPN clients.
Reconnect to both Wi-Fi and wired Ethernet simultaneously.
Avoid switching networks during the process.
Reset the watsonx Orchestrate Developer Edition server:
orchestrate server reset
4
Define the model specification file

For Ollama, you do not need to create a connection or use a real API key. Use any string, such as ollama, as the API key value.
Use your local network IP address as the URL. Ollama does not work if you use localhost or 0.0.0.0 in the model specification file.
ollama-llama2.yaml
spec_version: v1
kind: model
name: ollama/llama3.2:latest
display_name: Ollama LLaMA 3.2
description: |
    Ollama-hosted LLaMA 3.2 model for local or edge deployments.
tags:
- ollama
- llama2
model_type: chat
provider_config:
    api_key: ollama
    custom_host: http://198.51.100.42:11434
Remember: Replace http://198.51.100.42:11434 with the IP address that you have obtained in the previous step.
5
Add the model

BASH
orchestrate models import --file ollama-llama2.yaml
Red Hat AI

​
provider_config
object
The fields which can either be set by connection or by the provider_config field of the model. Values from a connection will be merged with the provider_config.
Hide properties

​
api_key
stringrequired
The API key for the provider.
​
custom_host
stringrequired
Send requests to a custom hostname for the provider.
​
response_headers
list[string]
Add one or more additional response headers in the form ["header:value", "header2:value2"] to the request to the server.
​
response_timeout
number
The response timeout in seconds.
Example usage:
1
Define the model specification file

redhat-genai.yaml
spec_version: v1
kind: model
name: redhat-ai/gpt-oss-120b
display_name: RedHat AI gpt-oss-120b
description: |
    RedHat AI model via API key authentication.
tags:
- redhat-ai
- genai
model_type: chat
provider_config:
    custom_host: https://my-redhat-ai-compatible-server
2
Create an API key connection

To safely use the API key, you must first create a connection:
BASH
orchestrate connections add -a redhat_ai_credentials
orchestrate connections configure -a redhat_ai_credentials --env draft -k key_value -t team
orchestrate connections set-credentials -a redhat_ai_credentials --env draft -e "api_key=my_redhat_ai_api_key"
3
Add the model

You can now add the model using the specification file and the connection that you created:
BASH
orchestrate models import --file redhat-genai.yaml --app-id redhat_ai_credentials
Limitations:
On-Prem:
For the gpt-oss-120b model, the model name must exactly match gpt-oss-120b. If a different model name is used, the ReAct Core style needs to be explicitly configured in the Builder UI.
If the provider uses custom CA certificates, follow the certificate import steps outlined in the on-prem documentation.
SaaS:
For the gpt-oss-120b model, the model name must exactly match gpt-oss-120b. If a different model name is used, the ReAct Core style needs to be explicitly configured in the Builder UI.
Supported only for endpoints using certificates issued by a publicly trusted Certificate Authority (CA).
For more information about Red Hat OpenShift AI setup and configuration, refer to the Red Hat OpenShift AI documentation.
​
List all LLMs
Run the orchestrate models list command to see all available LLMs in your active environment.
BASH
orchestrate models list
By default, the command displays a table of available models. To get raw output, add the --raw (-r) flag.
​
Removing custom LLMs
Run the orchestrate models remove command with the --name (-n) flag to specify the LLM to remove.
BASH
orchestrate models remove -n <model-name-unique-identifier-to-delete>
​
Exporting custom LLM
Run the orchestrate models export command to export LLMs from your active environment.
BASH
orchestrate models export -n <model_name> -o <path>.zip
Show command flags

​
Updating custom LLM
To update a custom LLM, remove it and then add it again:
BASH
orchestrate models remove -n <model-name-unique-identifier-to-delete>
orchestrate models add --name watsonx/meta-llama/llama-3-2-90b-vision-instruct --app-id watsonx_ai_creds
​
Additional configuration options
​
Setting a default LLM in the UI
If you use an on-premises installation with models provisioned only as virtual models, you can specify which model appears as the default in the user interface. Add the default tag under the tags section of a model with the type set to chat.
granite-default-model.yaml
spec_version: v1
kind: model
name: watsonx/ibm/granite-3.3-8b-instruct
display_name: IBM watsonx.ai (Granite)
description: |
    IBM watsonx.ai model using Space-scoped configuration.
tags:
- default # <-- this marks this as the Default model in the ui dropdown
model_type: chat
provider_config:
    watsonx_space_id: my-space-id
See all 11 lines
For on-premises installations that use only externally hosted virtual models, at least one model must be set as the default. Without a default model, the Create Agent page in the UI cannot be opened.
​
Setting a default embedding model
If you use an on-premises installation with models provisioned only as virtual models, you can also set a default model for knowledge bases. Add the default tag under the tags section of a model with the type set to embedding.
virtual-model.yaml
spec_version: v1
kind: model
name: virtual-model/watsonx/ibm/slate-30m-english-rtrvr-v2
display_name: slate30m
tags:
  - default
model_type: embedding
provider_config:
  watsonx_space_id: xxx
  customHost: 'https://us-south.ml.cloud.ibm.com'
  api_key: xxx
See all 11 lines
​
Configuring LLM parameters
Configure additional LLM parameters such as temperature and seed for more control over model behavior. Set these parameters in your agent configuration:
llm_config:
  seed: 123
  temperature: 0.0
Parameters:
seed: Sets a random seed for reproducible outputs (useful for testing and debugging)
temperature: Controls randomness in responses (0.0 = deterministic, higher values = more creative)
These settings apply to the specific agent and override any default model configuration.
---
Large Language Models (LLMs)
Configuring model policies (Public preview)
Model policies allow for the coordination of multiple models to accomplish tasks like load-balancing and fallback.
Model policies only support virtual models. You must import models as virtual models and reference them in your policies using the virtual-model/ prefix (e.g., virtual-model/google/gemini-2.0-flash). Direct references to provider models (e.g., groq/openai/gpt-oss-120b or bedrock/openai.gpt-oss-120b-1:0) are not supported.
​
Adding model policies
BASH
orchestrate models policy add --name <model_name> --model <provider1>/<model_id1> --model <provider2>/<model_id2> --strategy <strategy_type> --strategy-on-code 500 --retry-on-code 503 --retry-attempts 3
Hide command flags

​
--name / -n
string
The name of the policy you want to add.
​
--description / -d
string
An optional description to appear alongside the policy in the list view.
​
--display-name
string
An optional display name for the policy in the UI.
​
--strategy / -s
string
The policy mode you want to use.
loadbalance: Distributes requests between models based on weight values (default is 1 for each).
fallback: Uses another model if one becomes unavailable.
single: Uses only one model, but allows for --retry-on-code and --retry-attempts.
​
--strategy-on-code
list[int]
A list of HTTP error codes which triggers the strategy. Used for fallback strategy.
​
--retry-on-code
list[int]
A list of HTTP error codes for which the model should retry the request.
​
--retry-attempts
int
How many attempts it should make before stopping.
​
Importing model policies
BASH
orchestrate models policy import --file my_spec.yaml
After you create a model policy, assign the policy to your agent by using the ADK and the agent YAML file. Assign the policy the same way that you assign a regular model. You cannot assign a model policy to a Generative Prompt Activity in a flow.
Where the my_spec.yaml file follows this structure:
Load balancing
Fallback
Single
[my_spec.yaml]
spec_version: v1
kind: model
name: anygem
description: Balances requests between 2 Gemini models
display_name: Any Gem
policy:
  strategy:
    mode: loadbalance
    on_status_codes: [503, 504]
  retry:
    attempts: 1
  targets:
    - model_name: virtual-model/google/gemini-2.0-flash
      weight: 0.75   # Weights must be greater than 0 and less than or equal to 1
    - model_name: virtual-model/google/gemini-2.0-flash-lite
      weight: 0.25
Flags:
--file (-f): File path of the spec file containing the model policy configuration.
​
Updating model policy
Use either the add or import commands with the name of the model policy that you want to update to update the model policy.
​
Exporting model policy
BASH
orchestrate models policy export -n <model_name> -o <path>.zip
Hide command flags

Flag	Type	Required	Description
--name (-n)	string	Yes	The model policy name to export.
--output (-o)	string	Yes	The file path where the exported data is saved.
​
Removing model policies
BASH
orchestrate models policy remove -n <name of policy>
Hide command flags

​
--name / -n
string
The name of the policy you want to remove.
---

Large Language Models (LLMs)
Enabling watsonx/* LLMs
The watsonx Orchestrate Developer Edition now supports integration with the wxO SaaS tenant for LLM inferencing. Previously, developers were required to configure the Developer Edition using their own watsonx.ai API key and Space ID. This update simplifies the setup process by enabling proxy usage through Watsonx Orchestrate.
This configuration approach also applies to other supported LLM providers, including Groq and AWS Bedrock.
​
Prerequisites
To retrieve the necessary configuration details, you must have access to an instance of watsonx Orchestrate.
​
Environment Configuration
Additional environment variables are required to enable proxy usage. These variables differ based on the deployment type:
SaaS Deployment
On-premises Deployment
​
Common Parameters
Variable	Description
AUTHORIZATION_URL	IAM URL used to authorize watsonx Orchestrate to access the proxy service.
USE_SAAS_ML_TOOLS_RUNTIME	Enables the ADK to use the proxy.
​
SaaS Deployment Configuration
For SaaS deployments, use the following environment variables:
WO_API_KEY=<your API key for Watson Orchestrate on SaaS>
WO_INSTANCE=<your service instance URL>
# The below two fields are optional and automatically inferred by the Developer Edition
AUTHORIZATION_URL=<your IAM URL>
USE_SAAS_ML_TOOLS_RUNTIME=True
Note:
watsonx.ai API Key and Space ID are no longer required.
​
On-premises Deployment Configuration
For on-premises deployments, use the following environment variables:
authenticating with password
authenticating with API key
WO_USERNAME=<your username for onprem>
WO_PASSWORD=<your password for onprem>
WO_INSTANCE=<your service instance URL>
AUTHORIZATION_URL=<your IAM URL>
Variable	Description
WO_USERNAME	Username used to log in to IBM SoftwareHub.
WO_PASSWORD	Password associated with WO_USERNAME.
WO_INSTANCE	watsonx Orchestrate server instance URL
AUTHORIZATION_URL	Optional, an IAM URL used to authorize watsonx Orchestrate to access the proxy service.
​
Alternative LLM Providers
In addition to watsonx.ai models, the Developer Edition supports other LLM providers. Similar to watsonx.ai configuration, you can either provide your own credentials or use the watsonx Orchestrate proxy service.
​
Groq Configuration
To use the groq/openai/gpt-oss-120b model, you have two options:
Option 1: Using Your Own Groq Credentials
Add the following to your .env file:
GROQ_API_KEY=<your-groq-key>
Option 2: Using watsonx Orchestrate Proxy
Configure the same WO_API_KEY and WO_INSTANCE variables as described in the SaaS Deployment Configuration or On-premises Deployment Configuration sections above.
​
AWS Bedrock Configuration
To use the bedrock/openai.gpt-oss-120b-1:0 model, you have two options:
Option 1: Using Your Own AWS Bedrock Credentials
Add the following to your .env file:
BEDROCK_AWS_ACCESS_KEY_ID=<your-bedrock-access-key-id>
BEDROCK_AWS_SECRET_ACCESS_KEY=<your-bedrock-secret-access-key>
Option 2: Using watsonx Orchestrate Proxy
Configure the same WO_API_KEY and WO_INSTANCE variables as described in the SaaS Deployment Configuration or On-premises Deployment Configuration sections above.
Note: When using the watsonx Orchestrate proxy (Option 2), you don’t need to provide provider-specific credentials. The proxy handles authentication with the LLM providers on your behalf.

---


