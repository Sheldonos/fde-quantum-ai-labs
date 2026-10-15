Release Notes
What's new
See the latest improvements and bug fixes from the new version of the ADK.

Starting from version 2.0.0, watsonx Orchestrate ADK documentation is now versioned per ADK release. If you want to view a specific ADK documentation version, change the documentation version in the version dropdown located at the top left of the page.

​
Version - 2.14.0
2.14.x
2026-08-04
The watsonx Orchestrate ADK version 2.14.0 is now available!
Upgrade to version 2.14.0 to enable observability for external agents, configure language support for document processing, add Google TTS voice configurations, and benefit from enhanced flow lifecycle events and connection validation.
​
⬆️ Upgrade now
To upgrade to version 2.14.0, run:
BASH
pip install --upgrade ibm-watsonx-orchestrate==2.14.0
​
🚀 New features
​
Observability for external agents
External agents can now export traces to any OTEL-compatible backend such as Jaeger or Instana. The SDK includes automatic token refresh, root span creation, tool attributes, and PII decorator support for enhanced observability. For more information, see Traces.
​
Document processing language support
All document processing nodes (Classifier, Extractor, Text Extractor, Unstructured) now accept an optional language parameter, enabling you to specify the document language for improved processing accuracy. For more information, see:
Document classifier node
Document field extractor node
Document text extractor node
​
Google TTS voice configuration
Configure Google Text-to-Speech (TTS) as a voice provider with support for both simple and advanced YAML templates. Advanced configurations allow you to customize pitch, rate, gender, and voice name. For more information, see Managing voice configuration.
​
Deepgram TTS volume normalization
The Deepgram advanced voice configuration now includes a normalize_volume field to automatically adjust audio output levels for consistent playback. For more information, see Managing voice configuration.
​
Extended flow lifecycle events
Agentic workflows now support two additional lifecycle event types: on_flow_abort and on_flow_delete. These events enable more comprehensive monitoring and handling of workflow states. For more information, see Configuring callbacks.
​
Knowledge base credential validation
Credentials are now validated during knowledge base creation and updates before indexing begins. The url field in index_config is now optional, simplifying configuration. For more information, see Building knowledge bases.
​
Red Hat AI model support
The red_hat_ai provider is now recognized in the CLI, enabling you to register and use Red Hat AI models with watsonx Orchestrate. For more information, see Managing custom LLMs.
​
Microsoft Copilot Studio agent provider
microsoft_copilot_studio is now a valid external agent provider type, expanding integration options for external agents. For more information, see Connecting to external agents.
​
Document classifier class limit
A hard upper limit is now enforced on the number of classes in a Document Classifier node at authoring time, preventing configuration errors. For more information, see Document classifier node.
​
Langflow updated to v1.10.0
Langflow has been updated to version 1.10.0, bringing the latest features and improvements to Langflow tool integration. For more information, see Langflow tools.
​
🐛 Bug fixes
Flow import crash on empty OpenAPI request schema: Fixed an issue where importing flows with empty OpenAPI request schemas caused the import process to crash.
Custom agent import overwrites existing connections: Fixed an issue where importing custom agents would overwrite existing connections instead of preserving them.
Custom agent hardcoded default LLM removed: Removed the silent fallback to a hardcoded default model in custom agents, ensuring explicit model configuration.
Flow callback tool validation: Fixed an issue where invalid callback shapes were not properly rejected at import time, now providing clear validation errors.
Voice server missing environment variable: Fixed a startup failure for voice-enabled agents caused by a missing environment variable.
get_city_founding_date 403 error: Fixed HTTP 403 errors when querying Wikidata SPARQL by adding the required User-Agent header to requests.
​
Version - 2.13.0
2.13.x
2026-07-22
The watsonx Orchestrate ADK version 2.13.0 is now available!
Upgrade to version 2.13.0 to surface observations in traces, suppress agent summarization, extract documents by page range, work with agent skills, benefit from extended callback events, and new model support.
​
⬆️ Upgrade now
To upgrade to version 2.13.0, run:
BASH
pip install --upgrade ibm-watsonx-orchestrate==2.13.0
​
🚀 New features
​
Traces update
Traces now surface observations instead of spans, with a simplified search model that filters by time range, user ID, and session ID. The CLI also gains a new --last flag for relative time windows as a shorthand alternative to --start-time / --end-time. For more information, see Traces.
​
Suppress agent summarization
A new suppress_agent_summarization configuration option allows builders to suppress agent reasoning output when an agentic workflow ends, preventing duplicate information from being presented in chat after a flow completes. For more information, see Building a flow.
​
Page range support for document field and text extractor nodes
The docext() and docproc() nodes in agentic workflows now support a page_range parameter, letting you limit extraction to a specific range of pages. For more information, see Document field extractor node and Document text extractor node.
​
Extended event support and payload schema for agentic workflow callbacks
Agentic workflow callbacks now support two additional lifecycle events — ON_FLOW_ABORT and ON_FLOW_DELETE — bringing the total to eight configurable event kinds. Callback tools now receive a structured FlowCallbackEventsPayload that includes elicitation details when a task is waiting for user input, enabling external systems and MCP clients to respond without polling. For more information, see Configuring callbacks.
​
Agent skills
Work with agent skills using the ADK. Agent skills are portable, version-controlled packages that equip your agents with specialized knowledge and workflows. For more information, see Agent skills.
​
Premier models
Enable premier models, including GPT-5.4, to use on watsonx Orchestrate. For more information, see Enabling premier models.
​
Deprecated agent styles
The agent styles default, react, and planner are now deprecated in watsonx Orchestrate. For more information, see Migrating to ReAct Core agent style.
​
🔧 Enhancements
Python 3.14 support: The ADK now supports Python 3.14.
​
🐛 Bug fixes
Lima template not found on fresh installation: Fixed an issue where a fresh installation of the Developer Edition failed with a template "_images/ubuntu-lts.yaml" not found error. The limactl binary now correctly locates its bundled templates when installed for the first time.
​
Version - 2.12.0
2.12.x
2026-06-26
The watsonx Orchestrate ADK version 2.12.0 is now available!
Upgrade to version 2.12.0 to configure multi-language support for agentic workflows, leverage enhanced decision tables and parallel branches, and benefit from context variable support in LangGraph agents.
​
⬆️ Upgrade now
To upgrade to version 2.12.0, run:
BASH
pip install --upgrade ibm-watsonx-orchestrate==2.12.0
​
🚀 New features
​
Multi-language support for agentic workflows
Configure multi-language support for user interactions in agentic workflows within ADK. This enables your workflows to communicate with users in their preferred language. For more information, see Multi-language support.
​
Enhanced decision tables for agentic workflows
Use the updated decision table functionality in agentic workflows to create more sophisticated conditional logic and routing. For more information, see Decision node.
​
Parallel branch support in agentic workflows
Add parallel branches to your agentic workflows, allowing multiple operations to execute simultaneously for improved efficiency. For more information, see Parallel branch node.
​
Anti-pattern documentation
Access comprehensive documentation on anti-patterns to help you avoid common pitfalls in agent design and implementation. For more information, see Foundational architecture considerations.
​
🔧 Enhancements
Context variables in LangGraph agents: Added support for context variables in LangGraph agents, enabling better state management and data flow.
Dutch language support: Dutch (nl-NL) language support is now available for Agentic Orchestrate, expanding language coverage for international deployments.
​
Version - 2.11.0
2.11.x
2026-06-12
The watsonx Orchestrate ADK version 2.11.0 is now available!
Upgrade to version 2.11.0 to use custom agent commands, schedule agentic workflows and agents, mask sensitive data, configure callbacks, and benefit from updated LangChain/LangGraph ecosystem.
​
⬆️ Upgrade now
To upgrade to version 2.11.0, run:
BASH
pip install --upgrade ibm-watsonx-orchestrate==2.11.0
​
🚀 New features
​
Schedule agentic workflows and agents
Schedule agentic workflows and agents to run at specific times or intervals. For more information, see:
Scheduling overview
Agent scheduling parameter
​
Configure callbacks for agentic workflows
Set up callbacks to receive notifications about workflow execution events. For more information, see Callback.
​
Conversation compaction for agents
Compress agent conversations to prevent overflow and optimize memory usage. For more information, see Conversation compaction settings.
​
Mask sensitive text in agentic workflows
Protect sensitive information by masking text in agentic workflows. For more information, see Masking sensitive data.
​
Map connections during agent import
Map connections while importing custom agents from ZIP files, streamlining the import process. For more information, see Associating connections to Custom agents.
​
Flux model support for Deepgram
Enable the Flux model for the Deepgram provider in voice configurations. For more information, see Managing voice configuration.
​
Custom agent command
Previously released in public preview, custom agent commands are now available. Import agents using agent files, create agents directly from the CLI, and configure manual connections for custom agents. For more information, see:
Importing agents using an agent file
Creating agents directly from the CLI
Manual connection
​
🔧 Enhancements
Updated LangChain/LangGraph ecosystem: The LangChain and LangGraph ecosystem updated to their latest major versions:
Show Updated versions

​
Version - 2.10.0
2.10.x
2026-05-20
The watsonx Orchestrate ADK version 2.10.0 is now available!
Upgrade to version 2.10.0 to create dynamic schemas for knowledge bases, use Python toolkits in agentic workflows, and benefit from enhanced workspace messaging.
​
⬆️ Upgrade now
To upgrade to version 2.10.0, run:
BASH
pip install --upgrade ibm-watsonx-orchestrate==2.10.0
​
🚀 New features
​
Dynamic input and output schemas for knowledge bases
Create dynamic input and output schemas for your knowledge bases. For more information, see Configuring dynamic input and output for external knowledge bases.
​
🔧 Enhancements
Python toolkits in agentic workflows: You can now use Python toolkits in agentic workflows just as you use any other toolkits.
Enhanced workspace messaging: Improved copy messages for unhelpful assistant responses and external agent workspaces.
​
Version - 2.9.0
2.9.x
2026-04-30
The watsonx Orchestrate ADK version 2.9.0 is now available!
Upgrade to version 2.9.0 to configure multi‑user activities, enable direct OAuth access flows, configure checkpointing for LangGraph agents, and extend model support and safety controls.
​
⬆️ Upgrade now
To upgrade to version 2.9.0, run:
BASH
pip install --upgrade ibm-watsonx-orchestrate==2.9.0
​
🚀 New features
​
Multi‑user activities
Configure multi‑user activities by assigning a user activity node to a single user or multiple users registered in the tenant. For more information, see Configuring multi-user activities.
​
Import external agents from a URL
Import external agents by using a URL that hosts an agent card through the discovery command. For more information, see Import external agents from a URL.
​
OAuth direct access flow
Use an OAuth direct access flow connection to configure direct access for a team member in the draft environment. For more information, see Oauth auth direct access flow.
​
Checkpointer configuration
Enable state persistence for external agents by configuring checkpointers in the agent YAML file. For more information, see Configuring checkpointers.
​
🔧 Enhancements
OpenAI OAuth model support: Added support for OpenAI models using OAuth client credentials.
Model denylist support: Added support for restricting which LLMs can be selected by using a model denylist.
Safe update confirmation: Added the --safe flag for agents, knowledge bases, and tools commands to prompt for confirmation before updating existing resources.
​
Version - 2.8.0
2.8.x
2026-04-14
The watsonx Orchestrate ADK version 2.8.0 is now available!
Upgrade to version 2.8.0 to create Python toolkits, configure error handling in agentic workflows, use updated voice configurations, define custom connection properties, and benefit from enhanced security and interoperability improvements.
​
⬆️ Upgrade now
To upgrade to version 2.8.0, run:
BASH
pip install --upgrade ibm-watsonx-orchestrate==2.8.0
​
🚀 New features
​
Python toolkits
Create toolkits that bundle multiple Python tools and import them into watsonx Orchestrate. For more information, see Importing Python toolkits.
​
Error handling in agentic workflows
Configure error handling directly in agentic workflow flows. This allows workflows to respond more predictably when errors occur. For more information, see Handling errors.
​
Upgraded voice configurations
Use the updated voice configurations. For more information, see Managing voice configuration.
​
Custom properties in connections
Create custom properties in connections to extend connection configuration. For more information, see Creating a form tool.
​
Form tools
Display watsonx Orchestrate native form widgets from tools. For more information, see Creating a form tool.
​
🔧 Enhancements
OAuth client credentials authentication: Added support for OAuth Client Credentials authentication for virtual models through the AI Gateway.
Improved file transfer security: File upload and download now uses authenticated access instead of pre‑signed URLs.
Flow builder compatibility: Added support for opening flows created with the ADK directly in the flow builder.
Python package validation: Added validation for Python packages defined in requirements.txt against the Python package allowlist.
​
Version - 2.7.0
2.7.x
2026-03-27
The watsonx Orchestrate ADK version 2.7.0 is now available!
Upgrade to version 2.7.0 to manage Workspaces through the CLI, develop agents using Skill specifications, use updated OpenSearch schemas, connect to Genesys platforms, enhance agentic workflows, view custom code tool logs, and import agents from ZIP files.
​
⬆️ Upgrade now
To upgrade to version 2.7.0, run:
BASH
pip install --upgrade ibm-watsonx-orchestrate==2.7.0
​
🚀 New features
​
Workspaces
Use the new Workspaces commands to manage Workspaces with the watsonx Orchestrate ADK CLI. For more information, see Workspaces.
​
Agent development with Skills specifications (Public Preview)
Use the MCP servers and agent‑agnostic Skill specifications provided by IBM watsonx Orchestrate to help coding agents build solutions more reliably while reducing large context overhead. For more information, see Agent development with Skills specifications.
​
Updated schema for OpenSearch
Use the updated schemas for OpenSearch. For more information, see OpenSearch.
​
Genesys Cloud platform connections
Use the orchestrate customer‑care commands to configure connections for your Genesys Cloud platforms. For more information, see Managing connections to Customer Care platforms
​
Agentic workflow updates
Use the updated user activity node for agentic workflows. Configure dynamic forms and use date and time fields in your user activity node. For more information, see:
Dynamic form input
Forms fields
​
Logs for custom code tools
View logs generated by your custom code tools in watsonx Orchestrate Developer Edition. For more information, see Logging behavior for Python tools in watsonx Orchestrate.
​
Import agents from ZIP files
Import agents from ZIP files exported by the watsonx Orchestrate ADK CLI. For more information, see Bulk import from ZIP.
​
🐛 Bug fixes
Voice-configs import failure: Fixed an issue where importing voice configurations failed in on‑premises environments.
Display name mapping: Fixed an issue where display names were not mapped correctly into the flow model for some node types.
​
Version - 2.6.0
2.6.x
2026-03-13
The watsonx Orchestrate ADK version 2.6.0 is now available!
Upgrade to version 2.6.0 to use the new unified connection model, pass metadata to MCP tools, configure external service credentials, upload multiple files through Python tools, and search traces using relative time windows.
​
⬆️ Upgrade now
To upgrade to version 2.6.0, run:
BASH
pip install --upgrade ibm-watsonx-orchestrate==2.6.0
​
🚀 New features
​
Credential configuration for services on watsonx Orchestrate Developer Edition
Configure custom service credentials for watsonx Orchestrate Developer Edition. For more information, see Configure services credentials for watsonx Orchestrate Developer Edition in the .env file and Initializing watsonx Orchestrate Developer Edition server.
​
Updates to the orchestrate chat ask command
Use the expanded capabilities of the orchestrate chat ask command for richer interaction. For more information, see Chatting with an agent in interactive mode through the CLI.
​
Multiple file upload for Python tools
Create Python tools that upload multiple files. For more information, see Creating tools that accept files.
​
Relative time window for trace search
Use the --last flag with the orchestrate observability traces search command to search traces from the last minutes, hours, or days. For more information, see Searching traces.
​
Contextual metadata for MCP toolkits
Pass contextual metadata to tools that come from MCP toolkits. For more information, see Tracing, tenant and agent context.
​
Unified connection experience for knowledge bases
Use the updated connection experience for knowledge bases. Connections now support optional categorization, allowing you to define the connection type and the application that uses it. For more information, see Adding and configuring connections.
​
User activity node updates
Use the updated field types in the form() object for the user activity node. For more information, see Forms.
​
🐛 Bug fixes
Corrected instructions text wrapping: Fixed the wrapping issue for the orchestrate agents ai-builder prompt-tune command.
Updated CPD instance validation: CPD instances no longer need to start with https://cpd.
​
Version - 2.5.0
2.5.x
2026-02-27
The watsonx Orchestrate ADK version 2.5.0 is now available!
Upgrade to version 2.5.0 to search traces, manage Langfuse configuration, create citation‑enabled Python tools, and benefit from improved tool listing behavior.
​
⬆️ Upgrade now
To upgrade to version 2.5.0, run:
BASH
pip install --upgrade ibm-watsonx-orchestrate==2.5.0
​
🚀 New features
​
Traces with ADK
Search and export traces through the ADK CLI or Python scripts. For more information, see Traces.
​
Remove configuration settings for Langfuse
Use the new command to delete Langfuse configuration settings from your environment. For more information, see Removing configuration settings.
​
Citations for Python tools
Create Python tools that trigger citations. For more information, see Creating tools that can trigger citations.
​
Connection types for local MCP servers
Use different connection types to authenticate with your local MCP servers. For more information, see Supported connection types for local MCP servers.
​
🔧 Enhancements
Improved tool listing: The orchestrate tools list command now shows both the name and display_name when they differ, making it easier to identify tools in the output.
​
Version - 2.4.0
2.4.x
2026-02-13
The watsonx Orchestrate ADK version 2.4.0 is now available!
Upgrade to version 2.4.0 to import custom agents, define your own certificate bundles, and use new public preview Customer Care styles that expand how you build and run agents.
​
⬆️ Upgrade now
To upgrade to version 2.4.0, run:
BASH
pip install --upgrade ibm-watsonx-orchestrate==2.4.0
​
🚀 New features
​
Custom agents
Use the --experimental-package_root and --experimental-config-file flags to import your custom LangGraph agents into watsonx Orchestrate through the ADK. For more information, see:
LangGraph agent
Importing agents using an agent file
Creating agents directly from the CLI
Associating connections to Custom agents
​
Custom certificate bundle path
Use the new --cert-bundle-path flag with the orchestrate server start command to inject a custom certificate bundle through Docker volumes into the required microservices. For more information, see Initializing watsonx Orchestrate Developer Edition server.
​
(Public preview) Customer Care style support
Use the new experimental_customer_care style. For more information, see:
(Public preview) Customer Care style
Getting Started with Customer Care
Note:
This public preview has officially ended. The experimental Customer Care style is no longer supported.
​
🔧 Enhancements
Localized welcome experience: The welcome message and quick‑start prompts automatically translate to the language you choose. Translation quality depends on the LLM.
Improved KB import and update messages: Knowledge base import and update operations now show progress messages until completion.
Bedrock gpt‑oss model availability: The bedrock/openai.gpt-oss-120b-1:0 model is now available as one of the models for your agents.
​
🐛 Bug fixes
Resolved agent response failure: Fixed an issue where an agent did not respond when running a flow tool through orchestrate chat ask.
​
📘 Guides
​
Migration guidance from Llama to GPT-OSS-120b
A migration guide is now available to help you switch from Llama to the GPT-OSS-120b model. For more information, see Migrating to GPT-OSS-120B.
​
Version - 2.3.0
2.3.x
2026-01-30
The watsonx Orchestrate ADK version 2.3.0 is now available!
You can now upgrade to version 2.3.0 to access new ways of interacting with your agents, export your models, and control context variables with Python tools.
​
⬆️ Upgrade now
To upgrade to version 2.3.0, run:
BASH
pip install --upgrade ibm-watsonx-orchestrate==2.3.0
​
🚀 New features
​
Chatting with agents through CLI
Chat with agents in your active environment directly from the ADK CLI by using the orchestrate chat ask command. For more information, see Chatting with an agent in interactive mode through the CLI.
​
Export models and model policies
Use the ADK CLI to export models and model policies from watsonx Orchestrate. For more information, see Exporting custom LLM and Exporting model policy.
​
Modifying context variables with Python tools
Modify context variables inside Python tools, including values such as the user identity. For more information, see Using Context Variables.
​
🔧 Enhancements
Improved invalid docstring warnings: You now receive clearer and more accurate messages when a Python tool import fails because of incorrect docstrings.
​
🐛 Bug fixes
OpenAPI import problem: Fixed an issue where OpenAPI specs containing circular jsonref objects could not be imported into the ADK.
Inaccurate error reporting: Fixed an issue where certain failures incorrectly displayed str object has no attribute .decode instead of the actual error message.
​
Version - 2.2.0
2.2.x
2026-01-15
The watsonx Orchestrate ADK version 2.2.0 is now available!
This release expands agent deployment options, enhances extensibility, and simplifies tool and connection configuration. You can now deploy agents across new digital channels, create custom agents, work with dynamic schemas, and take advantage of major MCP and tooling improvements.
​
⬆️ Upgrade now
To upgrade to version 2.2.0, run:
BASH
pip install --upgrade ibm-watsonx-orchestrate==2.2.0
​
🚀 New features
​
Deploy agents on digital channels
Deploy your agents directly to Microsoft Teams and Facebook Messenger channels. This allows you to reach users across multiple communication platforms. For more information, see Establishing Channels.
​
Dynamic input and output schemas in Python tools
Configure custom schemas for Python tools using the new enable_dynamic_schema field. For more information, see Dynamic input and output schemas.
​
Auto-discover for Python tools
Use the new --auto-discover flag with orchestrate tools import to automatically discover and import all Python functions in the module specified by the -f flag. For more information, see Auto-discover.
​
Enhanced Langflow commands
Use the Langflow flow name to import Langflow flows directly into watsonx Orchestrate. When you provide the Langflow flow name, the ADK retrieves the latest JSON with credentials, so you do not need to export the flow before adding it to watsonx Orchestrate. For more information, see Importing langflow flow using langflow flow name.
​
🔧 Enhancements
LangChain core upgrade: Updated langchain-core to version ~1.2.4.
Langflow Builder UI: Updated to version 1.7.1.
Python tool parameter parsing: The ADK now parses input parameter descriptions for Python tools directly from docstrings.
Genesys audio connector credentials: Automatic generation of API key and secret is now supported, matching UI behavior. You can still provide credentials manually or leave them blank to auto-generate.
​
🐛 Bug fixes
Webchat embed deployment: Fixed an issue where the webchat embed command failed for deployed agents.
​
Version - 2.1.0
2.1.x
2025-12-11
The watsonx Orchestrate ADK version 2.1.0 is now available!
​
⬆️ Upgrade now
To upgrade to version 2.1.0, run:
BASH
pip install --upgrade ibm-watsonx-orchestrate==2.1.0
​
🚀 New features
​
Support for new phone and chat channels
ADK now supports more channels to connect to:
Twilio WhatsApp
Slack
Twilio SMS
Genesys Bot Connector
For phone channels, the only supported provider for now is Genesys Audio Connector.
ADK Voice configurations now support the following providers:
Deepgram Speech-To-Text and Text-To-Speech
ElevenLabs Text-To-Speech
To learn more about channels, see Establishing channels. To learn about phone support, see Adding phone configurations.
​
Support for plug-ins
Plug-ins inspect and modify the input or output of an agent run. A plug-in is a tool that is automatically started either before the agent begins generating a response (pre-invoke) or after the agent completes its response (post-invoke).
To learn more about plug-ins, see Plug-ins.
​
watsonx Orchestrate copilot is now watsonx Orchestrate AI Builder
watsonx Orchestrate copilot has been renamed to watsonx Orchestrate AI Builder. The new VS Code extension can now be found as watsonx Orchestrate ADK Extension in the VS Code Extensions store.
The extension now also includes access to an embedded web chat. You can learn more about it on watsonx Orchestrate AI Agent Builder and Orchestrate ADK Extension.
​
Evaluation framework: Langfuse support
The evaluation framework now supports evaluation with Langfuse. You can learn more about it in Agentops evaluation.
​
Document processing custom output format
The “docproc” (text extraction) node now includes an output_format parameter that gives you explicit control over how document processing results are returned. When set to docref, docproc returns a URL reference to the stored extraction results. This is the current and default behaviour. When set to object, docproc returns the actual JSON object.
For more information, see Document processing with output format.
​
🐛 Bug fixes
Channels: Fixed an issue where channel names were not saved after adding them.
Lima VM: Fixed issues related to the installation of the Lima VM when installing the watsonx Orchestrate Developer Edition.
Stop server: The command orchestrate server stop now correctly stops the virtual machine that runs the watsonx Orchestrate Developer Edition server. You can opt to keep the VM running with the --keep-vm flag.
Flows: Uploaded files now support non-ASCII characters in the file name.
​
Version - 2.0.0
2.0.x
2025-11-25
The watsonx Orchestrate ADK version 2.0.0 is now available!
​
⬆️ Upgrade now
To upgrade to version 2.0.0, run:
BASH
pip install --upgrade ibm-watsonx-orchestrate==2.0.0
​
🚀 New features
​
Installing watsonx Orchestrate Developer Edition
The installation process for watsonx Orchestrate Developer Edition is updated. You no longer need Docker installed; the installation configures everything automatically. You still need the .env file. New commands are available to manage your watsonx Orchestrate Developer Edition. For more information, see watsonx Orchestrate Developer Edition.
​
Channels
Channels allow watsonx Orchestrate agents to connect with users across multiple platforms and communication tools. A new set of channels commands has been added to the ADK. For more information, see Channels.
​
Forms support for user activity node
Previously released in public preview, forms support for user activity nodes is now generally available. You can configure forms in a user activity node. For more information, see Forms.
​
Data mapping
Large data in flows is automatically summarized to improve auto-mapping reliability. You can customize the summarization by providing instructions specific to your use case. For more information, see Data mapping
​
Breaking change: Import MCP toolkits
The former orchestrate toolkits import command has been renamed to orchestrate toolkits add. Additionally, a new orchestrate toolkits import command has been added, which works on files in a way that is the inverse of the orchestrate toolkits export command. You can learn more in Importing local MCP toolkits and Importing remote MCP toolkits.
​
Export MCP toolkits
You can now use the ADK CLI to export MCP toolkits. For more information, see Exporting remote MCP toolkits using ADK CLI.
​
AI gateway models in Document Processing
You can now use AI gateway models for KVP extraction in Document Processing nodes. For more information, see Document text extractor node.
Important update for existing users
If you previously used this feature, you must update your model name to include the provider prefix. For example:
Before: mistralai/mistral-small-3-1-24b-instruct-2503 (deployed on watsonx.ai)
Now: watsonx/mistralai/mistral-small-3-1-24b-instruct-2503
​
Groq GPT-OSS Models
watsonx Orchestrate now supports Groq GPT-OSS models. For more information, see Large Language Models.
Note:
This model is a non-IBM product governed by a third-party license that may impose use restrictions and other obligations. By using this model you agree to the terms. Read the terms
​
🐛 Bug fixes
Deleting agents: Fixed an issue where deleting an agent also deleted the modular knowledge attached to it.
Importing complex agentic workflows: Fixed an issue where agentic workflows with complex schemas could be imported by ADK but not executed by watsonx Orchestrate.