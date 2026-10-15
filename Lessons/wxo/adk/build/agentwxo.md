Agents
Overview
In watsonx Orchestrate, agents are the core building blocks that execute tasks on behalf of users. An agent combines a large language model (LLM) with tools, collaborators, and optional knowledge sources to deliver intelligent, context-aware automation. Agents can be native, built directly in watsonx Orchestrate, or external, integrated from other platforms such as watsonx.ai, Salesforce AgentForce, or third-party frameworks via supported protocols.
​
What makes up an agent?
Every agent includes:
Name and Description
The name uniquely identifies the agent, while the description serves two purposes:
It helps users understand the agent’s role and capabilities in the UI.
It informs supervisor agents when routing requests to collaborators. A well-crafted description should summarize the agent’s purpose, tools, and domain knowledge.
Instructions
Instructions are natural language directives that shape the agent’s behavior. They define the agent’s persona, reasoning style, and how it should use tools and collaborators to solve tasks. Clear instructions ensure predictable, high-quality responses.
Tools and Collaborators
Tools extend the agent’s functionality by enabling API calls, Python scripts, or other operations. Collaborators are other agents—native or external—that the agent can invoke to complete complex workflows.
Knowledge Base (optional) Agents can access domain-specific knowledge from uploaded documents or connected vector stores, improving accuracy for specialized queries.
Scheduling (optional) Configure agents and agentic workflows as schedulable to create recurring executions at specific times or intervals. This enables automation of routine tasks without manual intervention.
​
Agent types
Native Agents: Built and managed within watsonx Orchestrate using the Agent Development Kit (ADK).
External Agents: Integrated from external platforms via protocols like external_chat or A2A.
​
What to do next
Descriptions and instructions
Learn more about agent descriptions and instructions, and how to write them effectively.
Authoring agents
Step-by-step guidance on creating your own agents, structuring their logic, and defining capabilities.
Connect to external agents
Explore how to integrate your system with external agents or services, and manage secure communication.
Importing and deploying agents
Learn how to import existing agents, configure deployment options, and publish agents to your environment.
Managing agents
Find out how to monitor, update, version, and control permissions for agents in your workspace.
Integrating agents with my application
Discover how to embed agents into your application using the embedded chat.

---

Authoring agents
Authoring native agents
You create and import native agents into watsonx Orchestrate. Use YAML, JSON, or Python files to build agents for watsonx Orchestrate.
​
Configuring native agents
Each native agent includes these components:
​
llm
string
Specifies the large language model (LLM) that powers the agent’s ability to understand and respond to queries. For more information, see Managing custom LLMs with the AI gateway.
​
llm_config
object
Provides advanced configuration options for the Large Language Model (LLM) used by the agent. These settings allow you to control decoding behavior, output format, safety parameters, model‑specific behavior, and provider‑specific extensions. If omitted, defaults from the AI gateway or model provider are used.
Supported values

​
model
string
Overrides the model ID for this agent. If not provided, the value from the top‑level llm field is used.
​
decoding_method
string
Specifies the decoding strategy (for example, greedy, sample, or provider‑specific methods).
​
prompt
string | list<string>
Adds a custom prompt or prompt sequence to each model request.
​
max_tokens
integer
Maximum number of tokens the model can generate.
​
max_completion_tokens
integer
Alternative output token limit used by some providers.
​
temperature
float
Controls randomness. Higher values increase creativity; lower values produce more deterministic output.
​
top_p
float
Uses nucleus sampling to restrict generation to tokens within a cumulative probability threshold.
​
n
integer
Number of completion candidates to generate.
​
stream
boolean
Enables streaming responses when supported by the model provider.
​
logprobs
integer
Returns log probabilities for top tokens.
​
top_logprobs
boolean
Provides detailed log probability information for generated tokens.
​
echo
boolean
When set to true, the model returns both the prompt and the completion.
​
stop
string | list<string>
One or more stop sequences that end the model’s output.
​
presence_penalty
float
Penalizes repeated subject matter to encourage exploration of new topics.
​
frequency_penalty
float
Reduces repeated words or phrases by penalizing frequent tokens.
​
best_of
integer
Generates multiple completions and returns the best scoring result.
​
logit_bias
object
Adjusts model probability distributions for specific tokens.
​
user
string
Identifier associated with the end user for logging or safety purposes.
​
context
string
Additional context sent to the model for each request.
​
examples
list<object>
Few-shot examples demonstrating the desired input-output behavior.
​
top_k
integer
Restricts sampling to the k most probable next tokens.
​
response_format
object
Defines the required structure of the model output (for example, JSON schema mode).
​
seed
integer
Ensures repeatable outputs when supported.
​
store
boolean
Indicates whether requests or responses are stored by the model provider.
​
metadata
object
Custom metadata passed to the model provider.
​
modalities
list<string
Modalities supported for the request (for example, text, audio, vision).
​
audio
object
Configuration for generating or processing audio.
​
service_tier
string
Specifies the service tier or quality level for supported providers.
​
prediction
object
Prediction parameters used by specific model providers.
​
safety_settings
object
Safety configuration for providers such as Google’s Gemini Enterprise AI.
​
anthropic_beta
string
Anthropic‑specific beta feature settings.
​
anthropic_version
string
Overrides the Anthropic model version.
​
thinking
object
Configures advanced reasoning or chain-of-thought features for supported models.
​
space_id
string
watsonx.ai space associated with the model execution.
​
project_id
string
watsonx.ai project bound to the request.
​
reasoning_effort
string
Controls reasoning depth for models that support variable reasoning levels.
​
parallel_tool_calls
boolean
Enables the model to call multiple tools in parallel.
​
disable_tool_validation
boolean
Disables schema validation for tool calls (specific for Groq models).
​
style
string
Defines the prompting structure the agent uses. This structure determines how the LLM interprets and responds to instructions. For more information, see Choosing the agent style.
​
hide_reasoning
boolean
Defines whether the agent’s reasoning appears to the end user. When set to True, the agent hides its reasoning from the user. When set to False, the agent displays its reasoning. The default value is False.
​
memory_enabled
boolean
Enables the agent to retain conversation history and context across multiple interactions within a session. When set to True, the agent can recall information from previous messages in the conversation to provide more contextual and personalized responses. When set to False, each interaction is treated independently. The default value is False.
​
instructions
string
Provides natural language guidance to the LLM. These instructions shape the agent’s behavior, such as adopting a specific persona like a customer service representative and explaining how to use tools and collaborators. For more information, see Writing instructions for agents.
​
tools
list<string>
Extends the LLM’s capabilities by enabling access to external functions and services. Examples include:
OpenAPI definitions for external APIs
Python functions for scripting more complex interactions with external systems
Agentic workflows for orchestrating operations across tools and agents
Toolkit-exposed tools such as an MCP server
​
skills
list<string>
Lists the skills available to the agent. A skill is a modular capability bundle defined by a SKILL.md file that can include instructions, reference documents, and scripts. Use skills to keep context lean and improve accuracy when an agent needs multiple focused capability sets. For more information, see Agent skills.
Skills are only supported for agents using the react_intrinsic style.
​
collaborators
list<string>
Lists other agents this agent interacts with to solve complex problems. Collaborators can include native watsonx Orchestrate agents, external agents, or watsonx Assistants. For more information, see Connect to external agents.
​
description
string
Provides a human-readable summary of the agent’s purpose, visible in the Manage Agents UI. It also helps other agents understand its role when used as a collaborator. The description does not affect responses unless invoked as a collaborator. For more information, see Writing descriptions for agents.
​
knowledge_base
list<string>
Represents domain-specific knowledge that is acquired by the LLM from uploaded files or connected vector data stores. Agent Knowledge allows you to provide information that the agent should inherently know and use to answer questions. This knowledge can come from documents you upload or from various data sources integrated with watsonx Orchestrate, such as Milvus, Elasticsearch, AstraDB, and others. To learn more about setting up a knowledge base see the section on Knowledge bases.
​
restrictions
string
Specifies whether the Agent remains editable after import. This field accepts one of the following options:
editable Sets the Agent as editable. This is the default value.
non_editable Sets the Agent as non-editable and prevents it from being exported.
​
icon
string
An SVG-format string of an icon for the agent. The icon is used in the UI and in channels where the agent is connected to. It must follow these restrictions:
SVG format
Square shape
Width and height between 64 and 100
Maximum file size: 200 KB
​
is_schedulable
boolean
Controls whether you can schedule the agent to run at specific times or intervals. When set to True, scheduling is enabled and you can create schedules for this agent through Chat UI. When set to False, scheduling is disabled. The default value is None (scheduling disabled).

YAML

JSON

Python
spec_version: v1
kind: native
name: agent_name
llm: groq/openai/gpt-oss-120b  # groq model provider followed by the model id: openai/gpt-oss-120b
style: react_core
hide_reasoning: False
memory_enabled: False
description: |
    A description of what the agent should be used for when used as a collaborator.
instructions: |
    These instructions control the behavior of the agent and provide
    context for how to use its tools and agents.
collaborators:
  - name_of_collaborator_agent_1
  - name_of_collaborator_agent_2
tools:
  - name_of_tool_1
  - name_of_tool_2
skills:
  - name_of_skill_1
  - name_of_skill_2
knowledge_base:
  - name_of_knowledge_base
restrictions: editable
is_schedulable: false  # Enable scheduling for this agent
icon: "<svg></svg>" # SVG icon string for the agent
​
Additional features of native agents
Customize your agent with extra features to match your needs.
​
Guidelines
Use guidelines to control agent behavior. Guidelines create predictable, rule-based responses. Apply them when you need consistent actions.
Define guidelines using the following format: When condition then perform an action and/or invoke a tool.
Include only guidelines relevant to the current user request in the agent prompt. This reduces complexity for the LLM.
Configure the guidelines in priority order. Guidelines execute it, based on their position in the list.
To configure guidelines, add a guidelines section and define each guideline with these fields:
​
guidelines
list<object>
A list of guidelines the agent should follow. Each guideline uses the format:
When condition then perform an action and/or invoke a tool. Provide at least one of action or tool.
Hide properties

​
display_name
stringdeprecated
The name of the condition shown in the UI. This field is no longer used.
​
condition
stringrequired
The condition that triggers the guideline.
​
action
string
The action the agent performs when the condition is met.
​
tool
string
The tool to invoke when the condition is met, as listed by orchestrate tools list.

YAML

JSON
spec_version: v1
kind: native # Optional, Default=native, Valid options ['native', 'external', 'assistant']
name: finance_agent
style: react_core # Optional, Valid options ['default', 'react', 'react_core']
llm: groq/openai/gpt-oss-120b
description: |
  You are a helpful calculation agent that assists the user in performing math.
  This includes performing mathematical operations and providing practical use cases for math in everyday life.
instructions: |
  Always solve the mathematical equations using the correct order of operations (PEMDAS):
    Parentheses
    Exponents (including roots, powers, and so on)
    Multiplication and Division (from left to right)
    Addition and Subtraction (from left to right)

  Make sure to include decimal points when the user's input includes a float.
guidelines:
  - display_name: "User Dissatisfaction"
    condition: "The Customer expresses dissatisfaction with the agents response."
    action: "Acknowledge their frustration and ask for details about their experience so it can be addressed properly."
  - display_name: "Joy check"
    condition: "If the customer expresses joy or happiness about the response"
    action: "Respond by making chicken noises like 'bock bock' and then take no further action"
  - display_name: "Check user"
    condition: "If the customer expresses the need to check a user in the system."
    action: "Use the 'get_user' tool to check the user in the system"
    tool: "get_user"

tools:
  - get_user
collaborators: []
See all 31 lines
​
Web chat configuration
Adjust web chat settings to control how your agent behaves in the web chat UI. Set up a welcome message and starter prompts to guide users from the start.
​
Welcome message
Welcome message example
Welcome message example

The welcome message is the first thing users see when they start interacting with your agent. Personalize this message to reflect your agent’s purpose. To configure it, define the welcome_content schema in your agent file:
​
welcome_content
object
Configures the welcome content.
Hide properties

​
welcome_message
stringrequired
Specifies the welcome message shown to the user.
​
description
string
The text shown in light gray under the welcome message.
For an optimal experience on the chat welcome screen, keep the welcome message to 100 characters or fewer. Concise messages improve readability and help ensure consistent display across screen sizes and devices.
Example:

YAML

JSON
spec_version: v1
style: react_core
name: service_now_agent
llm: groq/openai/gpt-oss-120b
description:  'Agent description'
instructions: ''
collaborators: []
tools: []
hidden: false
welcome_content:
  welcome_message: "Hello, I'm Agent. Welcome to watsonx Orchestrate!"
  description: "How can I help you today?"
See all 12 lines
​
Starter prompts
Start prompts example
Starter prompts example

Starter prompts are predefined messages that help users start a conversation with your agent. Configure these prompts in the starter_prompts section of your agent file.
First, define whether these prompts are the default set. Then, for each prompt, specify these details:
​
starter_prompts
object
Configures starter prompts shown to the user.
Hide properties

​
prompts
list<object>required
A list of starter prompt tiles shown to the user. You can define up to three tiles.
Hide properties

​
id
string
The unique ID of the tile. It is auto-generated if not provided.
​
title
stringrequired
The bold title text displayed at the top of the starter prompt tile.
​
subtitle
string
The light gray text below the title.
​
prompt
stringrequired
The text sent to the agent as if entered by the user when the tile is clicked.
Example:

YAML

JSON
spec_version: v1
style: react_core
name: service_now_agent
llm: groq/openai/gpt-oss-120b
description:  'Agent description'
instructions: ''
collaborators: []
tools: []
hidden: false
starter_prompts:
    prompts:
        - id: "hello1"
          title: "Hello1"
          subtitle: ""
          prompt: "This is the messages for Hello prompt"
See all 15 lines
​
Chat with documents
Enable Chat with Documents to let users upload a document during a conversation and ask questions about its content. The document is available only within that session and is temporarily stored to support the interaction.
Important:
When you enable this feature, users can upload documents during chat interactions. The agent uses the file name to route prompts to the correct document. Make sure file names are unique and meaningful to avoid confusion.
​
chat_with_docs
object
Configures the Chat with Documents feature.
Hide properties

​
enabled
booleanrequired
Activates Chat with Documents and allows users to upload documents at run time.
​
citations
object
Configures citation display settings.
Hide properties

​
citations_shown
number
Maximum number of citations to display. Use -1 to display all citations.
​
generation
object
Fine-tune how your agent uses chat with documents.
Hide properties

​
idk_message
string
Defines the fallback message sent to the user when the chat with documents feature cannot provide an answer.
​
supports_full_document
boolean
Starting in version 2.2.0, the supports_full_document field is removed. Agents always receive the full documents that users upload by default, so you no longer need to configure or manage this setting.
Enables the Agent to request full documents instead of performing a search when it determines that full documents provide better support for answering the query. This option improves performance for tasks where search is less effective, such as summarization, proofreading, and extracting key points. The default value is True.
​
vector_index
object
Configures document processing settings for Chat with Documents.
Hide properties

​
extraction_strategy
string
Controls text extraction from documents. By default, Chat with Documents uses the express strategy, which does not support Optical Character Recognition (OCR). The system cannot extract text from scanned images or image-based PDFs. To enable OCR support, set this parameter to standard. Accepted values:
express (default): Processes documents faster without OCR support. The system cannot extract text from scanned images.
standard: Enables OCR support and extracts text from scanned images and image-based content.
This option increases document processing times.

YAML

JSON
spec_version: v1
style: react_core
name: service_now_agent
llm: groq/openai/gpt-oss-120b
description:  'Agent description'
instructions: ''
collaborators: []
tools: []
chat_with_docs:
  enabled: true
  citations:
    citations_shown: -1
  generation:
    idk_message: 'Your I don't know message'
  supports_full_document: true
  vector_index:
    extraction_strategy: express  # Use 'standard' to enable OCR for scanned documents
See all 17 lines
​
Providing access to context variables
Use context variables to inject user-specific identifiers—such as username, user ID, or tenant ID—from upstream systems into your agent. This creates personalized, context-aware interactions during execution.
System and custom variables
Context variables are either system variables or custom variables. System variables use the reserved wxo_ prefix and are populated automatically by the platform on every run. Custom variables are defined and supplied by your application. For details, see Types of context variables.
Naming convention for context variables
Follow the standard naming rules for custom context variables. For details, see Naming rules.
Scope and persistence
Context is scoped to a single run and is not persisted across turns in a thread. For details and persistence strategies, see Persisting context across turns.
Channel support
Channels might not support context-variable propagation. For details, see Channel support.
​
context_access_enabled
objectdefault:"false"
Specifies if the agent can access context variables set by the Runs API.
​
context_variables
list<string>default:"[]"
Lists the context variables the agent can access.

YAML

JSON
kind: native
name: context_variables_sample
display_name: Context Variables Agent
description: I'm able to deal with context variables
llm: groq/openai/gpt-oss-120b
style: react_core
instructions: |
  You have access to additional information :
    - wxo_email_id - {wxo_email_id}  
    - wxo_user_name - {wxo_user_name}  
    - wxo_tenant_id - {wxo_tenant_id}  
  Help users by returning the values to you so you can respond back to user with these values.
guidelines: []
collaborators: []
tools: []
knowledge_base: []
spec_version: v1
context_access_enabled: true
context_variables:
  - wxo_email_id
  - wxo_tenant_id
  - wxo_user_name
See all 22 lines
To set context variables, pass a dictionary as context in the request body instead of context_variables when you use these endpoints:
Runs API
Chat Completions API
Streaming Chat Completions API
By default, agents invoked during a run cannot access context variables. To enable access, set context_access_enabled to true.
After enabling access, specify the context_variables your agent uses. These variables define which contextual details—such as user identifiers or session data—are available during execution.
You can reference these variables in descriptions, guidelines, or instructions by using curly braces like {my_context_variable}. You can also pass them as arguments to a Python function. When you pass them to a function, the agent runtime fills the values automatically without asking the user.

YAML

JSON
spec_version: v1
style: react_core
name: service_now_agent
llm: groq/openai/gpt-oss-120b
description:  'Agent description'
instructions: |
  You have access to clientID: {clientID}
collaborators: []
tools: []
context_access_enabled: true
context_variables:
  - clientID
  - channel     # Use it to get access to channel integration (embedded chat)
See all 13 lines
​
Conversation compaction settings
Configure conversation compaction to prevent context overflow in long conversations or when tools return large amounts of data. This feature maintains optimal performance by intelligently managing conversation history through a multi-level compaction strategy and specialized large message handling.
Important:
Conversation compaction is not enabled by default. Enable it explicitly in your agent YAML file by setting context_compaction_enabled to true.
If you enable compaction after a conversational thread encounters a context limit error, compaction does not resolve the issue for that existing thread. Compaction becomes active only for new conversational threads that you create after enabling it.
Carefully adjust the large message threshold. Large messages can trigger context length errors if you set the threshold to a high value because of the asynchronous nature of compaction. Extremely large messages can hit context length errors before compaction triggers.
​
compaction_settings
object
Configure conversation compaction to prevent context overflow.
Hide properties

​
context_compaction_enabled
boolean
Main switch to enable or disable context compaction for the agent. Set this explicitly to true to activate compaction. The default value is false.
Required for: All compaction levels (Level 1, Level 2, Level 3)
​
context_compaction_threshold
integer
Token count threshold that triggers Level 1 compaction. When conversation history exceeds this limit, the agent summarizes conversation segments automatically. The default value is 20000 tokens.
Required for: Level 1 and Level 2 compaction
Considerations:
Lower values = more frequent compaction, less context per summary
Higher values = less frequent compaction, more context per summary
Should be less than your LLM’s max context window
​
compaction_sliding_window
integer
Maximum number of compacted messages to retain in the sliding window fallback (Level 3). This prevents unbounded growth in extremely long conversations. The default value is 10 messages.
Required for: Level 3 compaction fallback for extremely long conversations
Recommended Range: 5-20 messages
​
large_message_threshold
integer
Token count threshold for identifying individual large messages that require special handling. The system processes messages exceeding this limit synchronously before adding them to conversation history. The default value is 50000 tokens.
Required for: Large message handling strategy
Recommended Range: 30,000-50,000 tokens
​
large_message_chunk_size
integer
Size of chunks when splitting large unstructured messages for parallel Map-Reduce processing. Only applicable to unstructured data such as text, logs, and prose. The default value is 30000 tokens.
Required for: Large message Map-Reduce summarization for unstructured data
Recommended Range: 20,000-50,000 tokens
​
large_message_target_summary
integer
Target token count for the truncated large message. This determines the truncation point for structured data. The default value is 10000 tokens.
Required for: Large message handling for structured data
Recommended Range: 5,000-20,000 tokens
​
large_message_detect_structured
boolean
Enables automatic detection of structured data formats in large messages. When true, the system uses truncation for structured data such as JSON, XML, CSV, and YAML to preserve data integrity.
Required for: Structured data preservation in large messages
Detected Formats: JSON, XML, CSV, TSV, YAML, Python literals (dicts/lists)
​
Compaction Architecture
Context compaction uses a three-level strategy to manage conversation history:








Threshold Exceeded

Conversation History

Level 1: Summarize Segments

Level 2: Combine Summaries

Level 3: Sliding Window

Level 1 Compaction (Async):
When conversation history exceeds context_compaction_threshold, the system summarizes conversation segments into CompactedMessages automatically. This runs asynchronously as a background job without blocking the agent loop.
Level 2 Compaction (Async):
As multiple Level 1 summaries accumulate, the system combines them into a single Level 2 summary. This provides a higher-level overview of the conversation while maintaining recent context.
Level 3 - Sliding Window (Fallback):
For extremely long conversations, the compaction_sliding_window setting keeps only the N most recent compacted messages, preventing unbounded growth.
Processing Characteristics:
Asynchronous Operations

Synchronous Operations

Large Message Handling
In addition to conversation-level compaction, the system handles individual large messages such as extensive tool outputs through synchronous processing that reduces token size inline before adding to conversation history.
The system uses different strategies based on content type:
Unstructured Data

Structured Data

​
Configuration Examples
Level 1 & 2 Only
Level 1, 2 & 3
With Large Message Handling
Full Example
Basic compaction for most use cases. Enable Level 1 and Level 2 compaction without sliding window fallback.

YAML

JSON
compaction_settings:
  context_compaction_enabled: true
  context_compaction_threshold: 20000
​
Best practices for conversation compaction
Enable for long conversations:
Activate compaction for agents handling extended interactions or processing large tool outputs
Match LLM context window:
Set context_compaction_threshold below your LLM’s maximum context window. For example, use 20K for models with 32K context.
Use sliding window for extreme cases:
Enable compaction_sliding_window (Level 3) only for conversations that may run indefinitely
Preserve structured data:
Keep large_message_detect_structured enabled by default to maintain data integrity in JSON, XML, and other structured formats
Tune for your use case:
Lower thresholds = more frequent compaction, better for memory-constrained scenarios
Higher thresholds = less frequent compaction, better for context-rich conversations
Monitor performance:
Track compaction frequency and adjust thresholds based on actual usage patterns
Consider tool outputs: If your tools return large datasets, configure large message handling appropriately

---

Authoring agents
Connect to external agents
​
External Agents
External agents are built outside watsonx Orchestrate and can be used as collaborators for native agents.
watsonx Orchestrate supports multiple provider protocols, including external_chat, the Agent-to-Agent Protocol (A2A), and specialized communication protocols for integrating with watsonx AI Agent Builder agents, watsonx Assistants, and Salesforce Agent Force agents.
external_chat and A2A agents can be built on any underlying agent platform such as BeeAI, Langgraph, and CrewAI, where the user hosts the agent themselves, on Code Engine.
​
Providers
​
External Chat (Chat Completions API)
The external_chat provider can be used to integrate with any agent that is capable of providing an OpenAI style chat completions endpoint and is the most common form of integration.
The documentation for this API spec can be found on the watsonx-orchestrate-developer-toolkit.
A reference Langgraph external agent can be found here.

YAML

JSON

Python
spec_version: v1
kind: external 
name: news_agent
title: News Agent
nickname: news_agent 
provider: external_chat
description: |
  An agent built in langchain which searches the news.
tags:
  - test
api_url: "https://someurl.com"   # the url of the external agent
auth_scheme: BEARER_TOKEN        # one of BEARER_TOKEN | API_KEY | NONE 
auth_config:
  token: "123"                   # this is token for both BEARER_TOKEN and API_KEY 
chat_params:                     # chat_parms are parameters sent to an agent on each request
  stream: true                  # should the external agent be invoked using using SSE streaming or as a rest call 
config:                          # config represents the internal configuration of this agent used by wxo
  hidden: false                  # Hide this collaborator agent from the ui
  enable_cot: true               # Does the external agent return all internal steps and tool calls
Collapse
​
Agent to Agent (A2A) Protocol
The Agent to Agent Protocol (A2A) is an open standard designed to enable communication and interoperability between multiple agentic systems. Because the standard evolves rapidly, watsonx Orchestrate specifies the A2A version in the provider field to ensure compatibility when communicating with agents.
The currently supported version is 0.3.0. Earlier versions, such as 0.2.1, are deprecated and will be removed in a future release. To ensure continued support, use version 0.3.0 or later when registering A2A-compatible agents.
For a sample LangGraph agent compatible with the A2A protocol, see the a2a-samples repository.
To register an agent that is compatible with the A2A protocol, set provider to external_chat/A2A/0.3.0, like the following example:

YAML

JSON
spec_version: v1
kind: external 
name: news_agent
title: News Agent
nickname: news_agent 
provider: external_chat/A2A/0.3.0 # this is the identifier for A2A agents, provider/protocol/version of A2A supported
description: |
  An agent built in langchain which searches the news.
tags:
  - test
api_url: "https://someurl.com"   # the url of the external agent
auth_scheme: BEARER_TOKEN        # one of BEARER_TOKEN | API_KEY | NONE 
auth_config:
  token: "123"                   # this is token for both BEARER_TOKEN and API_KEY 
chat_params:                     # chat_parms are parameters sent to an agent on each request
  sendHistory:                   # indicates whether conversation history should be sent to the external A2A agent
  stream: false                  # should the external agent be invoked using using SSE streaming or as a rest call
  pushNotifications: true        # set to true if the external agent can send push notifications to provide updates on async tasks
config:                          # config represents the internal configuration of this agent used by wxo
  hidden: false                  # Hide this collaborator agent from the ui
See all 20 lines
Asynchronous updates with push notifications (technical preview)
For tasks that run for extended periods (e.g., minutes, hours, or days) or in scenarios where clients cannot maintain persistent connections—such as mobile applications or serverless functions — A2A supports asynchronous updates via push notifications. This mechanism enables the A2A Server to actively notify a client-provided webhook whenever a significant task update occurs.
If your agent supports asynchronous push notifications for long-running tasks, register this capability by setting the property:
YAML
pushNotifications: true
The push notification configuration is provided to the external A2A agent in the initial message/send or message/stream request. The A2A agent must include the complete update — such as message, task, and artifact details (as applicable) — in the notification payload, along with the corr_id value received in the metadata of the initial request.
Push notifications use Bearer token authentication, where the token is generated from API keys as described in the Getting Started guide.
Callback URL and authentication
The callback URL is included in the request sent to the A2A agent. To send push notifications, you must:
Use a valid API key to generate a Bearer token for authentication.
Provide complete task update details in the notification payload, following the A2A protocol’s task object specification. Partial status updates are not sufficient.
WXO supports the A2A protocol only over JSON-RPC 2.0 on HTTP. Although A2A can use multiple transport protocols, this implementation is limited to JSON-RPC 2.0.
​
Import external agents from a URL
Use the discovery command to retrieve and import an external agent by using a URL that hosts an agent card. This approach removes the need to manually define the full agent configuration when the external agent already exposes its metadata. External agents that follow the A2A protocol typically publish an agent card at a well-known endpoint. The default location is .well-known/agent-card.json. The discovery command uses this endpoint unless a custom endpoint is provided. After the agent is discovered, the configuration is retrieved and the agent can be exported and saved locally. The exported agent can then be imported and used like other external agents.
Discover an agent by using the default endpoint
BASH
orchestrate agents discover -u https://example.com
Discover an agent by using a custom endpoint
Use a custom endpoint when the agent card is not located at the default path.
BASH
orchestrate agents discover -u https://example.com -e .well-known/agent-card-2.json
Discover an agent by using a connection for authentication
Some external agents require authentication. Provide a connection to retrieve the agent configuration.
BASH
orchestrate agents discover -u https://example.com -a my-a2a-connection
Discover an agent by using a custom name
Override the agent name defined in the agent card.
BASH
orchestrate agents discover -u https://example.com -n my_custom_agent -a my-a2a-connection
​
Command behavior
Retrieves agent configuration from a URL that hosts an agent card.
Uses .well-known/agent-card.json as the default endpoint.
Supports custom endpoints for environments that expose multiple agents or non-standard paths.
Supports authenticated access through a configured connection.
Allows overriding the agent name during discovery.
Enables exporting the discovered agent for local use and later import into an environment.
​
watsonx AI Agent Builder
You can also integrate with agents built using watsonx.ai’s agent builder platform.
For more information, see Registering agents from watsonx.ai. Instead of using the API, complete the following YAML file and import your agent.
Provide well-crafted descriptions for your agents. These descriptions are used by supervisor agents to determine how to route user requests. For more information, see Writing descriptions for agents.

YAML

JSON

Python
spec_version: v1
kind: external 
name: news_agent
title: News Agent
    provider: wx.ai                  # the provider will always be wx.ai
description: | 
  An agent built in langchain which searches the news.
tags:
  - test
api_url: "https://us-south.ml.cloud.ibm.com/ml/v4/deployments/<id>/ai_service_stream?version=2021-05-01"
auth_scheme: API_KEY             # this will always be API_KEY         
auth_config:
  token: "<my_api_key>"          # this is the API key for wx.ai  
chat_params:
  stream: true                   # should the external agent be invoked using using SSE streaming or as a rest call 
config:
  hidden: false                  # Hide this collaborator agent from the ui
  enable_cot: true               # Does the external agent return all internal steps and tool calls
Collapse
​
Salesforce AgentForce
To register an agent that is built within Salesforce Agent Force as an external agent:
Follow the Getting Started Guide for the Agent API. For more information, see the Getting Started Guide.
getting-started-salesforce.png
On the Create a token page, the following information applies to all Salesforce agents within the instance:
api_url: Always set to https://api.salesforce.com/einstein/ai-agent/v1.
auth_config.token: Use the CONSUMER_SECRET provided in the guide.
chat_params:
client_id: Use the CONSUMER_KEY.
domain_url: Use the DOMAIN_URL.
Optionally, specify a list of display types to pass to Orchestrate as a comma-separated string.
Provide well-crafted descriptions for your agents. These descriptions are used by supervisor agents to determine how to route user requests. For more information, see Writing descriptions for agents.
Lastly, under chat_params you need to specify your agent_id. This can be found by hovering over one of your agents and either right-clicking and copying the URL, or by manually writing it based on hover text. In the following example, the agent_id is 0XxfJ0000001d8zSAA.
agent-selection-salesforce.png

YAML

JSON

Python









name: salesforce_ext_agent 
kind: external 
provider: salesforce                            # the provider will always be salesforce
title: Customer Service Agent by Salesforce
tags:
- "salesforce" 
description: An AI customer service agent whose job is to help customers with support questions or other issues. 
api_url: "https://api.salesforce.com/einstein/ai-agent/v1"
auth_scheme: API_KEY
auth_config:
  token: "my-api-key"
chat_params:
  agent_id: "my-agent-id"
  client_id: "my-client-id"
  domain_url: "https://agentforceXXX-dev-ed.develop.my.salesforce.com"
  # display_types: TextChunk,Confirm,Error,Failure,Inquire,Inform
config:
  hidden: false
  enable_cot: false
See all 19 lines
​
LangGraph agent
You can import LangGraph agents directly into watsonx Orchestrate. During the upload process, Orchestrate applies the Agent to Agent protocol behind the scenes to make the agent compatible with the platform. You use the same streamlined experience that you use for Python agents or MCP agents. A2A‑enabled LangGraph agents support lifecycle tasks such as update, delete, and export.
For a detailed description of how to import LangGraph agents, see Importing LangGraph agents.
Limitations:
Supported for Python implementations only.
Agents that are run inside the watsonx Orchestrate environment with the required isolation.
Supports only messages in the agent graph between turns, so complex custom state objects get lost between turns.
Example:
PYTHON
"""
Simple Agent: No LLM - Hello World
A simple agent that returns a static "Hello World" message without using any LLM.
"""
from typing import Annotated, List, TypedDict
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.runnables.config import RunnableConfig
from langgraph.graph import StateGraph, START, END


class AgentState(TypedDict):
    """Simple state with just messages."""
    messages: Annotated[List[BaseMessage], "conversation history"]


def hello_world_node(state: AgentState) -> AgentState:
    """
    Node that returns a static Hello World message.
    No LLM involved - just returns a hardcoded response.
    """
    # Get the last user message if available
    user_message = ""
    if state["messages"]:
        user_message = state["messages"][-1].content
    
    # Create a simple response
    response = AIMessage(
        content=f"Hello World! I received your message: '{user_message}'. "
                f"I'm a simple test agent with no LLM - I just return this static message."
    )
    
    return {"messages": state["messages"] + [response]}


def create_agent(config: RunnableConfig) -> StateGraph:
    """
    Factory function that creates and returns a LangGraph StateGraph.
    This agent has no LLM and just returns a static message.
    
    Args:
        config: Runtime configuration (not used in this simple agent)
    
    Returns:
        StateGraph: The compiled agent graph
    """
    # Build a simple linear graph: START -> hello_world -> END
    workflow = StateGraph(AgentState)
    workflow.add_node("hello_world", hello_world_node)
    workflow.add_edge(START, "hello_world")
    workflow.add_edge("hello_world", END)
    
    return workflow


if __name__ == "__main__":
    # Test the agent locally
    from langchain_core.messages import HumanMessage
    
    app = create_agent({}).compile()
    
    # Test 1: Simple message
    result = app.invoke({"messages": [HumanMessage(content="Hi there!")]})
    print("Test 1 - Simple message:")
    print(result["messages"][-1].content)
    print()
    
    # Test 2: Different message
    result = app.invoke({"messages": [HumanMessage(content="What can you do?")]})
    print("Test 2 - Different message:")
    print(result["messages"][-1].content)
Collapse
This capability is supported through the A2A protocol.
Configuring checkpointers
Checkpointers persist agent state so you can resume execution and maintain context.
Choose the checkpointer that fits your environment and persistence needs, then add its configuration to the checkpointer section of the agent YAML file.
Memory (development or testing)
SQLite
PostgreSQL (production)
No checkpointer (stateless)
Use in-memory storage to persist state during execution. State resets when the process restarts.
YAML
checkpointer:
  type: memory
Example:
spec_version: v1
kind: agent
name: my-agent
title: My LangGraph Agent
description: Agent with PostgreSQL state persistence
framework: langgraph

deployment:
  code_bundle:
    entrypoint: "main:create_graph"

checkpointer:
  type: memory
Notes:
The connection_string_key maps to a credential entry that stores the database connection string. Choose API key as the connection type and enter the connection string as the value.
For SQLite and PostgreSQL, the system manages database connections and schema setup automatically.
The memory checkpointer requires no credentials or additional configuration.
​
External watsonx Assistants
To register assistants from watsonx Assistant, you must obtain the following information:
service_instance_url
api_key
assistant_id
environment_id
Note: The location of the service_instance_url and api_key varies depending on whether the assistant is imported to IBM Cloud or AWS.
To retrieve your assistant ID:
Navigate to the settings on the actions page and open the settings.
actions_page.png
On the farthest right tab, select Upload/Download, and click the Download button.
actions-page.png
Locate your environment_id and assistant_id in the output JSON.
environment-id.png
​
IBM Cloud
On IBM Cloud, your service_instance_url and api_key can be found on the page where you launch your assistant’s tooling UI.
ibmcloud-service-keys.png
Provide well-crafted descriptions for your agents. These descriptions are used by supervisor agents to determine how to route user requests. For more information, see Writing descriptions for agents.

YAML

JSON

Python
spec_version: v1
kind: assistant
name: hr_assistant
title: HR Agent
description: |
  This assistant is capable of acting as a first point of contact for all support requests.
tags:
- wxa
config:
  assistant_id: assistantid
  environment_id: environmentid
  hidden: false
  api_key: my-api-key
  service_instance_url: https://api.eu-de.assistant.watson.cloud.ibm.com/instances/<my-instance-id>
  api_version: '2023-06-15T00:00:00.000Z'
  auth_type: IBM_CLOUD_IAM
  authorization_url: https://iam.cloud.ibm.com
Collapse
​
AWS
Provide well-crafted descriptions for your agents. These descriptions are used by supervisor agents to determine how to route user requests. For more information, see Writing descriptions for agents.

YAML

JSON

Python
spec_version: v1
name: my_assistant
title: my_assistant
description: |
  This assistant is capable of handling call center operations.
kind: assistant
tags:
- wxa
config:
  assistant_id: assistantid
  environment_id: environmentid
  hidden: false
  api_key: my-api-key
  service_instance_url: https://api.us-east-1.preprod.aws.watsonassistant.ibm.com/instances/<my-instance-id>
  api_version: '2023-06-15'
  auth_type: MCSP
  authorization_url: https://iam.platform.saas.ibm.com
Collapse
​
Additional features of external agents
​
Providing access to context variables
Context variables enable builders to incorporate user-specific identifiers—such as username, user ID, or tenant ID—from upstream systems into an agent. For a full explanation of how context variables work, including delivery methods, precedence, scope, persistence strategies, and channel limitations, see Context variables.
By default, agents invoked during a run do not have access to context. To enable access, set the context_access_enabled field to true and provide a list of context_variables to expose to the agent.
Context variables are passed to the agent in the following ways:
Runs API: Use the context field at the root of the request.
Chat Completions API: Use the context field at the root of the request.
Streaming variant: Each SSE event sent to the agent includes the context object.
For external A2A agents, the context variables defined are accessible in the metadata of the message object.
System and custom variables
Context variables are either system variables or custom variables. System variables use the reserved wxo_ prefix and are populated automatically by the platform on every run. Custom variables are defined and supplied by your application. For details, see Types of context variables.
Naming convention for context variables
Follow the standard naming rules for custom context variables. For details, see Naming rules.
Scope and persistence
Context is scoped to a single run and is not persisted across turns in a thread. For details and persistence strategies, see Persisting context across turns.
Channel support
Channels might not support context-variable propagation. For details, see Channel support.

YAML

JSON
spec_version: v1
kind: external
name: news_agent
title: News Agent
nickname: news_agent
provider: external_chat/A2A/0.3.0 # this is the identifier for A2A agents, provider/protocol/version of A2A supported
description: |
  An agent built in langchain which searches the news.
tags:
- test
api_url: "https://someurl.com" # the url of the external agent
auth_scheme: BEARER_TOKEN # one of BEARER_TOKEN | API_KEY | NONE
auth_config:
  token: "123" # this is token for both BEARER_TOKEN and API_KEY
chat_params:                     # chat_parms are parameters sent to an agent on each request
  sendHistory:                   # indicates whether conversation history should be sent to the external A2A agent
  stream: false                  # should the external agent be invoked using using SSE streaming or as a rest call 
config:
  hidden: false # Hide this collaborator agent from the ui
context_access_enabled: true
context_variables:
  - clientID
Collapse
Hide detailed parameter descriptions

​
context_access_enabled
objectdefault:"false"
Indicates whether this agent can access context variables set by the Runs API.
​
context_variables
list<string>default:"[]"
Specifies the list of context variables the agent can access.
​
Restricting Agents
You can restrict external agents in watsonx Orchestrate by using the restrictions parameter in your external agent configuration.

YAML

JSON
spec_version: v1
kind: external
name: news_agent
title: News Agent
nickname: news_agent
provider: external_chat/A2A/0.2.0 # this is the identifier for A2A agents, provider/protocol/version of A2A supported
description: |
  An agent built in langchain which searches the news.
tags:
- test
api_url: "https://someurl.com" # the url of the external agent
auth_scheme: BEARER_TOKEN # one of BEARER_TOKEN | API_KEY | NONE
auth_config:
  token: "123" # this is token for both BEARER_TOKEN and API_KEY
chat_params:                     # chat_parms are parameters sent to an agent on each request
  sendHistory:                   # indicates whether conversation history should be sent to the external A2A agent
  stream: false                  # should the external agent be invoked using using SSE streaming or as a rest call 
config:
  hidden: false # Hide this collaborator agent from the ui
restrictions: editable
Collapse
Hide detailed parameter descriptions

​
restrictions
string
Specifies whether the Agent remains editable after import. This field accepts one of the following options:
editable Sets the Agent as editable. This is the default value.
non_editable Sets the Agent as non-editable and prevents it from being exported.
---

Authoring agents
Authoring agents with the Orchestrate AI Builder
The Orchestrate AI Builder is a powerful tool that helps you create and refine agents.
It simplifies agent creation by allowing you to describe the agent you want. The AI Builder leverages its internal AI to create a new agent from scratch.
The AI Builder can also help with existing agents through conversational interaction where you specify changes, or by using past conversations and feedback to automatically adjust the agent’s behavior to align with expectations.
To use the AI Builder in the watsonx Orchestrate Developer Edition, add the --with-ai-builder flag to the orchestrate server start command. For more information, see Installing watsonx Orchestrate Developer Edition: watsonx Orchestrate server.
​
Creating agents
Use the Orchestrate AI Builder to guide the agent creation flow. Start from scratch and build the agent through natural conversation.
BASH
orchestrate agents ai-builder create
Show command flags

Command examples
Example 1
Example 2
Example 3
Example 4
Basic agent creation:
BASH
orchestrate agents ai-builder create -o output.yaml
Orchestrate AI Builder interaction example
The following example shows how you interact with the Orchestrate AI Builder to create an agent. In this example, you have already created and imported the string_reverser tool into your local instance.
BASH
🤖 Builder: To create a configuration for your agent in the IBM watsonx Orchestrate platform, let's start by describing the functionality of your agent. What tasks do you want your agent to perform, and what kind of operations should it be able to handle? Please provide a detailed or high-level description of your agent's intended functionality.

👤 You: I want to create an agent that can reverse strings

🤖 Builder: Based on your agent description, I've sorted the available tools by their relevancy and suggest the following tools for your agent:

1. **string_reverser**: A tool that can reverse any provided string.

Please select the tools you want your agent to use by specifying their numbers or names. If you want to see the full list of available tools, I can provide that as well. 

Remember, you can choose one, multiple, or no tools for your agent.

👤 You: 1

🤖 Builder: You have selected the **string_reverser** tool for your agent.

🤖 Builder: Based on your task description, I'll create an initial prompt. 

**Role** - 
You are an agent that can reverse strings according to the user's input.

**Tool Usage Guidelines** - 
1. Before you call a tool, make sure you have all the required tool parameters.
2. Do NOT assume any tool parameters
3. Do NOT pass parameters to the tool that are not explicitly defined
4. Do NOT call the same tool multiple times with the same parameters

**How To Use Tools**

- When the user wants to reverse a string, call the string_reverser tool with the string as a parameter.

Here's my initial prompt. How would you like the output to be formatted? Would you like it to be in a specific format, such as uppercase or lowercase?

👤 You: No use that prompt its perfect

╔══════════════════════════════════════════════════════════════════╗
║  Your agent building session finished successfully!             ║
║  Agent YAML saved in file:                                      ║
║  /Users/user123/output.yaml                                     ║
╚══════════════════════════════════════════════════════════════════╝
Collapse
​
Refining agents
Use the Orchestrate AI Builder to take an existing agent and improve its instructions with your input.
BASH
orchestrate agents ai-builder prompt-tune
Show command flags

Command examples
Basic refinement
Refinement with output
Dry run refinement
Refine an existing agent and overwrite the input file:
BASH
orchestrate agents ai-builder prompt-tune -f input.yaml
Orchestrate AI Builder interaction example
The following example shows how you interact with the Orchestrate AI Builder to refine an agent. In this example, you have already created and imported the string_reverser tool into your local instance.
BASH

🤖 Builder: Based on your task description, I'll create an initial prompt. 

**Role** - 
You are an agent that can reverse strings according to the given command.

**Tool Usage Guidelines** - 
1. Before you call a tool, make sure you have all the required tool parameters.
2. Do NOT assume any tool parameters
3. Do NOT pass parameters to the tool that are not explicitly defined
4. Do NOT call the same tool multiple times with the same parameters

**How To Use Tools**

- When the user wants to reverse a string, call the string_reverser tool with the string as a parameter.

How would you like the output to be formatted? Should it be a simple reversed string, or would you like any additional information included?

👤 You: I want the result formatted as a GitHub markdown table with 2 columns. The left column should be the input and the right should be the output. Please include headers on the table

🤖 Builder: Based on your requirements, I'll refine the prompt.

**Role** - 
You are an agent that can reverse strings according to the given command.

**Tool Usage Guidelines** - 
1. Before you call a tool, make sure you have all the required tool parameters.
2. Do NOT assume any tool parameters
3. Do NOT pass parameters to the tool that are not explicitly defined
4. Do NOT call the same tool multiple times with the same parameters

**How To Use Tools**

- When the user wants to reverse a string, call the string_reverser tool with the string as a parameter.
- Format the output of the string_reverser tool as a GitHub markdown table with two columns, "Input" and "Output", where the input string is in the "Input" column and the reversed string is
in the "Output" column.

Here's an example of what the output table might look like:
| Input | Output |
| --- | --- |
| xyz  | zyx  |

Are you interested in continuing to refine the prompt, or is this sufficient for your needs?

👤 You: That is sufficient
See all 46 lines
​
Automatic agent refinement (autotune)
You can automatically refine an agent using feedback from chat sessions.
To do this, start by creating an agent and chatting with it. You will see two icons below each agent response that allow you to provide either positive or negative feedback.
ai-builder-feedback-section.png
After providing feedback, run the following command to refine an agent using feedback from chat sessions:
BASH
orchestrate agents ai-builder autotune
Show command flags

Command examples
Basic autotune
Autotune dry run
Autotune last chat
Autotune an agent with interactive message selection:
BASH
orchestrate agents ai-builder autotune -n <agent_name> -o <output_path>.yaml
Orchestrate AI Builder interaction example
The following example shows how you interact with the watsonx Orchestrate AI Builder to refine an agent. In this example, you have already created and imported a healthcare management agent, chatted with it, and provided feedback.
BASH
                                                            10 Most Recent Chats                                                            
┏━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Number ┃ Chat Date                    ┃ Title                        ┃ Last User Message            ┃ Last User Feedback                 ┃
┡━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│      1 │ October 01, 2025 at 12:49 PM │ Show me healthcare providers │ Show me healthcare providers │ 👎 This would be better as a table │
│        │                              │                              │                              │                                    │
└────────┴──────────────────────────────┴──────────────────────────────┴──────────────────────────────┴────────────────────────────────────┘
Please enter up to 5 indices of chats you'd like to select, separated by commas (e.g. 1): 1

[INFO] - Your agent refinement session finished successfully!
[INFO] - Agent YAML with the updated instruction saved in file: <output_path>.yaml

---

Choosing the agent style
Choosing the agent style
Deprecation notice: The Default and ReAct styles are going to be removed in a future release. Only ReAct Core (react_core) remains. Migrate your agents to ReAct Core as soon as possible. See the agent style migration guide for instructions.
Agent styles define how the agent reasons through problems and how it behaves when collaborating with other agents. You can choose from three styles:
Style	How It Works	Best For
ReAct Core (react_core) ✦ Recommended	Uses the model’s built-in function calling with improved collaboration accuracy.	Complex tasks and multi-agent workflows where performance and collaboration accuracy matter.
Default (default) (Deprecated)	Uses the model’s built-in function calling.	Simple, linear tasks with predictable tool usage.
ReAct (react) (Deprecated)	Iterative loop: Think → Act → Observe, using a prompt-based tool calling approach.	Multi-step tasks on models with limited native function calling support.
Note:
If you use GPT-OSS-120B or GPT-5.4 as your agent’s model, the agent ignores all styles and uses ReAct Core automatically.
​
ReAct Core style
Choose ReAct Core (react_core) for complex tasks and multi-agent workflows. It uses the model’s built-in function calling and is optimized for accurate collaboration, keeping collaborators focused on the task at hand.
Use this style for:
Multi-agent workflows with collaborator agents
Complex reasoning tasks
Any scenario where collaborator accuracy matters
Behavior	Tool Compatibility	Example use cases
Think: Use the model’s built-in function calling to assess the request and select the right tool or collaborator
Act: Execute the tool or collaborator
Observe: Evaluate the outcome and adjust reasoning
Repeat until the goal is achieved
Python tools
OpenAPI tools
MCP tools
Knowledge-intensive tools
Data-intensive tools
Collaborator agents
Multi-agent orchestration
Complex problem-solving with advanced reasoning models
Tasks requiring accurate delegation to specialist collaborators
Note: react_core is the canonical identifier in the ADK and the UI, displayed as ReAct Core. ReAct Core (react_core) was previously named ReAct Intrinsic (react_intrinsic).
In the ADK, react_intrinsic is accepted as an alias for react_core and behaves identically. In the REST API, react_intrinsic is the accepted value.
​
Default style (Deprecated)
Choose Default (default) for simple tasks. This style uses a streamlined, tool-centric reasoning mode. The LLM decides which tool to use, how to use it, and when to respond. It works best for linear logic, such as retrieving a report or checking a ticket, because the agent orchestrates tool calls dynamically.
Use this style for:
Single-step or lightly sequential tasks
Scenarios that need flexibility
Tasks that involve multiple tools without strict sequencing
Behavior	Tool Compatibility	Example use cases
Prompts the LLM to:
- Identify which tool or collaborator to invoke
- Determine inputs
- Decide whether to call more tools or finalize a response
Continues prompting until it gathers enough context for an answer
Python tools
OpenAPI tools
MCP tools
Extract information from a system or the web
Check the status of a task or ticket
Perform tasks with well-defined steps
​
ReAct style (Deprecated)
Choose ReAct (react) for complex or ambiguous problems where each outcome influences the next step. This style uses an iterative loop: Think → Act → Observe. It supports reasoning, validation, and interactive confirmation. Inspired by the ReAct methodology, it surfaces the agent’s chain of thought.
A ReAct agent breaks tasks into smaller steps, reasons through each, takes action, and adjusts based on what it learns. It might ask you for confirmation before continuing.
Use this style for:
Exploratory or research-intensive tasks
Scenarios requiring iterative validation
Tasks with unclear or evolving requirements
Situations where transparent reasoning matters
Behavior	Tool Compatibility	Example use cases
Think: Assess the request and choose the right tool, collaborator, or reasoning step
Act: Execute the tool or collaborator
Observe: Evaluate the outcome and adjust reasoning
Repeat until the goal is achieved
Knowledge-intensive tools
Data-intensive tools
Collaborator agents
Generate or refactor code
Answer complex questions by searching and synthesizing information
Handle support tickets with complex interactions
---

Choosing the agent style
Migrating to ReAct Core agent style
Use this guide to migrate agents that use Default, ReAct, or Plan-Act styles to ReAct Core. This guide includes configuration snippets and tool examples to show what changes during migration. Use the examples as patterns that you can adapt to your agent configuration, prompts, tool names, and model settings.
Before you begin:
Export your current agent configuration so that you can compare the before and after states.
Review any custom instructions, tools, or output requirements that your agent depends on.
Validate the migration in a test or draft environment before you update production agents.
Ensure that you have ADK version 2.5.0 or later. Update it with the following command:
pip install --upgrade ibm-watsonx-orchestrate
The migration steps depend on your agent’s current style and model. Identify your migration path before you begin.
​
Why migrate to ReAct Core
Improve performance: ReAct Core consistently outperforms deprecated styles in benchmarks.
Support current and future models: Works with modern model capabilities.
Simplify agent configuration: Removes hidden style overrides.
Increase model compatibility: Supports more LLM models with native chain-of-thought capabilities.
​
Identify your migration path
Current configuration	Migration path
Uses the gpt-oss-120b model	Scenario 1
Uses Default or ReAct style with other models	Scenario 2
Uses Plan-Act style	Scenario 3
​
Scenario 1: Agents that use GPT-OSS-120B
If your agent uses the gpt-oss-120b model, it already uses ReAct Core internally. This migration does not change agent behavior.
Export your agent configuration:
orchestrate agents export -n <agent-name> -o agent-config.yaml
Edit your agent configuration file, for example, agent-config.yaml. Change style: default or style: react to style: react_core.
Update your agent:
orchestrate agents import -f agent-config.yaml
Your agent continues to work exactly as before with no behavior changes.
​
Scenario 2: Agents that use Default or ReAct with other models
If your agent uses other models, such as llama-3-3-70b-instruct, test the migration carefully because behavior might change.
The ReAct style includes Llama-specific optimizations that ReAct Core does not use.
If agent performance decreases after migration, consider migrating to gpt-oss-120b and rerun your evaluations.
Create benchmark evaluations:
Before you start the migration, create benchmark evaluations to compare agent performance before and after the change. This comparison helps you confirm that the migration does not reduce agent performance.
For more information about evaluations, see Evaluating agents and tools.
Update the style:
Export your agent configuration:
orchestrate agents export -n <agent-name> -o agent-config.yaml
Edit your agent configuration file, for example, agent-config.yaml. Change style: default or style: react to style: react_core.
Update your agent:
orchestrate agents import -f agent-config.yaml
Validate the changes:
Rerun your benchmarks against the updated agent and compare the results to confirm that the migration did not have a negative impact. If performance degrades, proceed to step 4.
(Optional) Update the model:
If benchmark performance worsens significantly after the style change, update the model to the recommended gpt-oss-120b.
Export your agent configuration:
orchestrate agents export -n <agent-name> -o agent-config.yaml
Edit your agent configuration file, for example, agent-config.yaml. Change the LLM to groq/openai/gpt-oss-120b. For example, from llm: watsonx/meta-llama/llama-... to llm: groq/openai/gpt-oss-120b.
Update your agent:
orchestrate agents import -f agent-config.yaml
Rerun the benchmarks and compare the new results against the old baseline.
Troubleshooting
Issue	Solution
Tool calling problems	Ensure your model natively supports tool calling. Verify that your tool descriptions are clear and detailed.
Response format changes	Update your prompts to guide the desired output format.
Performance degradation	Consider switching to gpt-oss-120b or a newer third-party model.
​
Scenario 3: Agents that use Plan-Act
The Plan-Act style has unique features that require special consideration during migration.
Plan-Act agents have two key capabilities:
Custom join tools: Tools that handle response formatting.
Structured output: Enforced output schemas.
You can achieve similar results in ReAct Core through careful prompting and configuration.
​
Migrating custom join tools
Instruct your agent to call a formatting tool before it responds to the user. In that formatting tool, use audience to provide a direct response without LLM interpretation. For more information, see Tool response structure and annotations.
Plan-Act configuration (before)
The following is the Plan-Act configuration before migration:
style: planner
custom_join_tools: my_formatting_tool
In the my_formatting_tool.py:
import json
from typing import Dict, List, Any
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from ibm_watsonx_orchestrate.agent_builder.tools.types import PythonToolKind

@tool(permission=ToolPermission.READ_ONLY, kind=PythonToolKind.JOIN_TOOL)
def format_task_results(original_query: str, task_results: Dict[str, Any], messages: List[Dict[str, Any]]) -> str:
    """
    Format the results from various tasks executed by a planner agent into a cohesive response.

    Args:
        original_query (str): The initial query submitted by the user.
        task_results (Dict[str, Any]): A dictionary containing the outcomes of each task executed within the agent's plan.
        messages (List[Dict[str, Any]]): The history of messages in the current conversation.

    Returns:
        str: A formatted string containing the consolidated results.
    """
    output = f"## Results for: {original_query}\n\n"
    for task_name, result in task_results.items():
        output += f"### {task_name}\n"
        if isinstance(result, dict):
            output += "```json\n"
            output += json.dumps(result, indent=2)
            output += "\n```\n\n"
        elif isinstance(result, list):
            output += "\n".join([f"- {item}" for item in result])
            output += "\n\n"
        else:
            output += f"{result}\n\n"
    output += "## Summary\n"
    output += f"Completed {len(task_results)} tasks related to your query about {original_query.lower()}.\n"
    return output
ReAct Core configuration (after)
The following is the ReAct Core configuration after migration:
style: react_core
instructions: |
  ...
  IMPORTANT: After calling the required tools to answer a user's query,
  call my_formatting_tool to consolidate results and format the response.
In my_formatting_tool.py:
import json
from typing import Dict, Any
from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool()
def format_task_results(original_query: str, task_results: Dict[str, Any]) -> str:
    """
    Format the results from various tools into a cohesive response.

    Args:
        original_query (str): The initial query submitted by the user.
        task_results (Dict[str, Any]): A dictionary containing the outcomes of each task executed within the agent's plan. The key should be the tool name and the value should be the result.

    Returns:
        str: A formatted string containing the consolidated results.
    """
    output = f"## Results for: {original_query}\n\n"
    for task_name, result in task_results.items():
        output += f"### {task_name}\n"
        try:
            result = json.loads(result)
        except:
            pass
        if isinstance(result, dict) or isinstance(result, list):
            output += "```json\n"
            output += json.dumps(result, indent=2)
            output += "\n```\n\n"
        else:
            output += f"{result}\n\n"
    output += "## Summary\n"
    output += f"Completed {len(task_results)} tasks related to your query about {original_query.lower()}.\n"
    return {
        "content": [
            {
                "type": "text",
                "text": output,
                "annotations": {"audience": ["user"]}
            }
        ]
    }
​
Migrating structured output
Include the schema in the instructions field instead of in the structured_output field.
Plan-Act configuration (before)
The following is the Plan-Act configuration before migration:
style: planner
structured_output:
  type: object
  properties:
    summary:
      type: string
    confidence:
      type: number
ReAct Core configuration (after)
The following is the ReAct Core configuration before migration:
style: react_core
instructions: |
  Always format your final response as JSON with the following schema:
  {
    "type": "object",
    "required": ["summary"],
    "properties": {
      "summary": {
        "type": "string"
      },
      "confidence": {
        "type": "number"
      }
    }
  }

  Ensure the response is valid JSON and includes all required fields.
​
Migration best practices
Test before deploying
Always test in the draft environment:
Create a copy of your agent for testing.
Run comprehensive test cases.
Use evaluation datasets when possible.
Monitor after migration
After you migrate to production:
Monitor agent performance metrics.
Watch for unexpected behaviors.
Keep a rollback plan ready.
Update documentation
Update internal documentation to reflect the new style.
Inform users of any behavior changes.
Document any prompt adjustments you made.
​
Getting help
If you encounter issues during migration:
Review the Choosing a style for the agent documentation.
Review ADK agent examples.
---

Authoring agents
Agent descriptions and instructions
Agents in watsonx Orchestrate are intelligent entities that automate tasks by combining a large language model (LLM) with tools, collaborators, and optional knowledge sources. To ensure agents are effective, predictable, and easy to maintain, developers must follow clear guidelines when defining names, descriptions, and instructions. These elements are not just metadata—they directly influence orchestration, user experience, and the quality of responses.
​
Why descriptions and instructions matter
Descriptions and instructions are not just metadata—they directly influence orchestration:
Supervisor agents rely on descriptions to route tasks to the right collaborator.
Instructions guide the LLM’s reasoning, ensuring the agent uses its tools and collaborators effectively.
​
Naming agents and tools
The name uniquely identifies the agent in the system and UI. Assign clear and unique names to each agent and tool you create. These names should reflect their capabilities and functions, making it easier for users to identify them within watsonx Orchestrate.
To write effective names:
Use snake_case instead of camelCase. They usually work better with routing agents. Agent names must not include spaces or special characters.
Keep names short and descriptive.
Avoid generic terms like “helper” or “assistant”.
Use domain-specific language (for example sales_outreach_agent).
Example
Good: ibm_historical_knowledge_agent
Bad: myAgent1
​
Writing instructions for agents
Instructions define how an agent behaves, including its tone, reasoning style, and decision-making process. They guide the underlying language model to produce consistent, predictable outputs and determine how the agent uses tools and collaborators.
They act as the agent’s persona and operating manual.
They ensure the agent responds in a way that aligns with user expectations and organizational standards.
They influence orchestration by determining when and how the agent invokes tools or other agents.
​
Best Practices for Writing Instructions
Use natural language
Write instructions as clear, conversational directives.
Avoid overly technical or ambiguous phrasing.
Example:
Explain technical concepts in simple terms.
When answering questions,
provide short summaries first,
then add details if the user asks for more.
Define tone and style
Specify whether responses should be professional, friendly, concise, etc.
Example:
Respond in a professional tone suitable
for business communication.
Include tool usage rules
Tell the agent when and how to use specific tools.
Example:
Use the CRM API tool for customer data.
If data is missing, ask clarifying questions
before proceeding.
Set error-handling guidance
Define what to do if required information is unavailable.
Example:
If you cannot retrieve data, inform the user and
suggest alternative actions.
Avoid Overloading Instructions
Keep them focused on behavior and decision-making, not on task-specific details.
Example:
Good
Respond in a professional tone. Use the crm_api tool
for customer data. If data is missing, ask
clarifying questions before proceeding.
Bad
Respond professionally, but also be friendly
and humorous when appropriate.
Always check CRM data, but if unavailable,
try ERP, then HR systems, and if
those fail, suggest alternatives. Include
emojis when the user seems happy,
but avoid them in formal contexts. If
scheduling is involved, call the
Calendar agent, but only after confirming
timezone differences and holidays.
Also, summarize every response in bullet
points unless the user asks for paragraphs.
​
Choosing your LLM
The model you choose directly influences how an agent behaves and interprets instructions. Different models excel at different types of tasks, and many are trained with specialized capabilities. For example, some models include vision features, meaning they can process images, detect patterns, and answer questions about visual input. Other models are optimized specifically for code generation, and may not perform as well in general-purpose tasks.
To understand the full capabilities, limitations, and intended use cases of a model, always refer to the model provider’s documentation, typically found in platforms like HuggingFace or watsonx.ai.
watsonx Orchestrate offers a variety of models you can select from when creating agents, each suited for different workflows and business needs. To see the list of all supported models, you can run the following command:
orchestrate models list
You can also add new models to the list of supported models by using the AI gateway. For more information, see Managing custom LLMs with the AI gateway.
​
The default model (groq/openai/gpt-oss-120b)
GPT-OSS-120b is OpenAI’s most powerful open-weight large language model, released under the Apache 2.0 license, making it fully suitable for commercial use, customization, and enterprise deployment. It contains around 117-120 billion parameters using a Mixture of Experts (MoE) architecture, which activates only a subset of parameters during inference, enabling strong performance with manageable compute requirements.
Within watsonx Orchestrate, GPT-OSS-120b has recently become the default model for building agents, leveraging its strong reasoning capabilities and reliable tool-use behavior. IBM hosts the model on watsonx.ai, enabling secure enterprise usage, integration with Orchestrate agents, and optional high-speed inference through providers such as Groq.
Here are a few features of this model:
Advanced Reasoning & Chain-of-Thought: GPT-OSS-120b supports full chain-of-thought reasoning, making it effective for complex instructions, multi-step logic, and orchestrator-style agents that need to autonomously decide which tools or actions to take.
Strong Agentic Capabilities: The model natively supports:
Function/tool calling
Structured output formats
Web browsing & Python execution (where supported)
Interacting with multi-tool agent workflows
Large Context Window: GPT-OSS-120b offers a 131k-128k token context window (depending on provider), enabling it to process lengthy documents, logs, or multi-turn interactions without losing context.
Fine-Tuning & Customization: Because it is fully open-weight and under Apache 2.0, the model can be:
Fine-tuned
Self-hosted
Customized with enterprise data
Integrated into internal workflows
Note:
This model is a non-IBM product governed by a third-party license that may impose use restrictions and other obligations. By using this model you agree to the terms. Read the terms.
​
Writing instructions for GPT-OSS-120b
GPT-OSS-120b is highly capable but also sensitive to vague or conflicting instructions. To ensure reliable behavior:
Be explicit: Clearly state priorities and constraints.
Avoid ambiguity: Conflicting directives can lead to unpredictable outputs.
Test iteratively: Validate instructions with sample tasks before deploying.
Limit complexity: Break down multi-step reasoning into clear, sequential guidance.
Example for groq/openai/gpt-oss-120b:
Always respond in a professional tone. When asked for CRM data,
use the salesforce_api tool. If the request involves scheduling,
call the calendar_agent. If information is incomplete, ask
clarifying questions before proceeding.
​
Special considerations
The default groq/openai/gpt-oss-120b model does not use the standard system prompt from watsonx Orchestrate. As a result, it can behave differently from other models, including:
Not explicitly identifying itself as part of the watsonx Orchestrate ecosystem.
Preferring its internal knowledge over your connected knowledge bases, unless you instruct otherwise.
Hyperlinks might not be formatted properly, unless you instruct otherwise.
It does not follow the supported Agent styles.
If you’re migrating existing agents from Llama to GPT-OSS-120B, see the comprehensive Migration guide for detailed instructions, common challenges, and optimization strategies.
Use explicit, natural-language constraints that limit reasoning depth, enforce brevity, and prioritize external knowledge. Add one or more of the following blocks to your agent’s instructions:
Prioritize knowledge bases over internal knowledge
Always check the connected knowledge base(s) first.
Prefer information retrieved from knowledge over your
own internal knowledge. If relevant content is found,
summarize it faithfully and cite the source title or document
name. If the knowledge base does not contain the answer, say
"I don't know based on the provided knowledge" and ask
a clarifying question.
Cap reasoning depth and iteration count
Use concise reasoning. Limit yourself to
a maximum of 3 reasoning steps before answering.
Do not re-plan unless the last tool result contradicts
prior assumptions. If you cannot progress after 3 steps,
ask one focused clarifying question.
Formatting
When generating hyperlinks, use the correct Markdown syntax: [link](url).
Keep chit-chat short
Keep small talk to a single sentence.
Immediately pivot to the user's task with a
concise question or action.
Enforce a strict output budget
Target an answer length of 4-6 sentences (or ≤150 words).
Use bullet points only when they increase clarity.
Avoid repeating the prompt or restating obvious context.
Fail fast when data is missing
If required inputs are missing, do not speculate.
Ask for the minimum missing fields in a single
question and wait.
​
Combined instruction example (recommended template)
Use this as a compact block tailored for groq/openai/gpt-oss-120b:
Behavior and sources:
- Identify as an agent operating within watsonx Orchestrate.
- Always use available tools to retrieve information before relying on your internal knowledge.
- If tools don't contain the answer, explicitly state "The available tools don't contain the answer", state that clearly and ask one clarifying question.

Reasoning and brevity controls:
- Use concise reasoning with at most 3 reasoning steps before responding.
- Keep chit-chat to one sentence, then proceed.
- Limit final answers to ≤150 words unless the user requests detail.

Formatting:
- When generating hyperlinks, use the correct Markdown syntax: [link](url).
 
Error handling:
- If a tool call or retrieval fails, briefly describe the failure and propose the next best step or ask for a missing input.
​
Good vs. bad instruction snippets for this topic
Good (concise, enforce constraints):
Use knowledge bases as the primary source.
Cite the document name when used.
Limit yourself to 3 reasoning steps
and less than 150 words in the final answer.
If you cannot find an answer in knowledge,
say so and ask one clarifying question.
Bad (encourages runaway reasoning and verbosity):
Think in exhaustive detail until you're
absolutely certain. Explore all possible interpretations.
Provide a comprehensive narrative of your
thoughts and include context for every claim.
​
Writing descriptions for agents
The agent description is used by an agent to determine when and how to delegate a task to a collaborator agent, tool or knowledge ensuring the right request is sent to the right capability. When adding any artifact (a collaborator agent, tool, or knowledge) to an agent, the agent description is critical to the agent’s success.
Agent descriptions complement the agent names by providing detailed information about their purpose, capabilities, and usage. A well-written description helps users understand the agent’s role and potential applications.
Descriptions should not be written in isolation — they must reflect the agent’s scope, use cases, and interaction with collaborators, tools, and knowledge bases. This ensures reliable routing and prevents ambiguity.
​
Key principles
Descriptions as instructions: Treat the agent description like instructions to the agent on how it should use the artifact (collaborator agent, tool, or knowledge base) in question
Hierarchy matters:
Agent descriptions are broader and set the overall purpose.
Collaborator descriptions narrow the scope to specific tasks.
Tool descriptions are the most specific, clarifying exact functionality.
Avoid overlap: Each agent should have a distinct scope. If scopes are similar, clearly differentiate them.
Include context markers:
Geographic scope (for example, “US”) helps route queries correctly.
Domain-specific language (for example, “pet-parents and their fur-babies”) sets tone and aligns with instructions.
Don’t overload descriptions: Mention core capabilities, not every tool. The agent should infer tool usage from context.
Define trigger conditions: Clarify when the agent should use the artifact, such as “Use this when the user requests supplier risk evaluation or mentions creditworthiness.”
Specify actions: Be specific about the actions the artifact should perform. When possible include how the artifact should performs those actions, such as “Access loan data from loan APIs, calculate affordability, and summarize affordability differences”
Define restrictions: Note desired restrictions and limitations. Most artifacts will have a boundary they should stop at, such as “Do not give legal or tax advice, only provide estimates and data-driven comparisons”
Use appropriate jargon: Define any industry specific terms of acronyms so they won’t be misunderstood.
​
Description examples
HR agent description
Use this agent to compare employee compensation data across
similar roles and regions. Retrieve current market benchmarks
from HR databases, analyze differences, and summarize how
internal pay aligns with external trends. **Do not provide
policy recommendations or make promotion decisions**.
Supplier Analysis tool routing description
Assesses supplier risk by retrieving ratings, credit data,
and compliance history from Dun & Bradstreet and internal
procurement systems. Summarizes financial stability, delivery
reliability, and compliance risk. **Do not make purchase
decisions or alter supplier records**.
Finance agent routing description
Analyze portfolio performance by pulling real-time stock
and bond data, calculating returns, and comparing results
against benchmarks. Summarize key performance drivers and
risk factors. Do not provide personalized investment advice
or execute trades.
​
Example: agent and collaborator description for a pet store
The following example demonstrates how to write clear, context-rich descriptions for an agent and its collaborators, tools, and knowledge bases.
This example also shows how tone and language can align with the agent’s persona, which should be reinforced in the instructions for a consistent user experience.
Agent Description
USPetTreeAgent
A US PetTree attendant serving the needs of pet-parents
and their fur-babies. It can help give general pet care
advice, assist in the pet adoption process by matching
users to cats and dogs, and order pet supplies from the
PetTree US Store.
Collaborator description
MatchMakerAgent
An agent to search the PetTree cat & dog registry
to match animal lovers with cats and dogs seeking a
forever home, and file a pet adoption application.
Tools for MatchMakerAgent
SearchPetTreeCats: Search the PetTree registry for cats available for adoption.
SearchPetTreeDogs: Search the PetTree registry for dogs available for adoption.
GetPetTreeAnimalProfile: Get the full profile of an individual cat or dog.
ViewAnimalPhotos: View pictures of cats and dogs available for adoption.
FileAdoptionApplication: File a pet adoption application for a specific cat or dog.
Knowledge Base for MatchMakerAgent
Cat Breeds Care: Facts, personalities, and care guides for different cat breeds.
Dog Breeds Care: Facts, personalities, and care guides for different dog breeds.
​
Writing descriptions for tools
A good tool description helps agents identify and use the tool effectively. It should include a general overview of the tool’s purpose, as well as details about its inputs and outputs. In Python tools, descriptions are defined in docstrings, following Google-style docstrings.
Example:
TEXT
Retrieves all user information based on their unique identifier.

Args:
    id (str): The user's unique identifier.

Returns:
    dict: The user's information, including user_id, user_name, 
    user_email, and user_phone.
​
Designing agents and tools for best performance
When designing agents and tools, aim for balanced complexity. Components that are too simple may lack utility, while overly complex designs can reduce the model’s ability to reason effectively.
​
Guidelines for Agents
Agents using LLaMA-based LLMs perform best with 10 or fewer tools or collaborators.
For complex use cases requiring many tools, break the problem into smaller subproblems and assign them to collaborator agents.
This limit may vary for more powerful models.
​
Guidelines for Tools
Keep input and output schemas as simple as possible.
Avoid tools with:
A large number of input parameters.
Parameters with deeply nested or complex data types.
Complex schemas make it harder for the LLM to use the tool effectively.

---
Authoring agents
Agent development with Skills specifications
IBM watsonx Orchestrate provides two MCP servers and agent-agnostic Skills specifications to help coding agents build solutions more reliably while reducing large context overhead.
​
MCP servers
watsonx Orchestrate provides two MCP servers to support agent development:
Documentation Server — Enables search of watsonx Orchestrate ADK documentation.
CLI Server — Executes ADK CLI commands (for example, listing agents, listing tools, and applying modifications).
Relying exclusively on the Documentation Server for the full programming model can lead to large context sizes. This may limit the agent’s ability to generate non-trivial examples and often requires frequent guidance.
​
SKILL.md specifications
The sop-builder and wxo-builder specifications follow the Agent Skills format. These specifications provide condensed, high-signal guidance about the watsonx Orchestrate programming model.
Benefits
Coding-agent agnostic (works with any agent that supports the format).
Reduces reliance on long, noisy documentation searches.
Improves reliable follow-through and correctness.
​
Recommended approach
Clone the watsonx Orchestrate ADK repository. Agents perform better when ADK examples are locally available.
Repository location:
https://github.com/IBM/ibm-watsonx-orchestrate-adk
​
Configuring MCP servers and SKILL specifications
For all coding agents:
Configure both MCP servers (Documentation Server and CLI Server).
Download the SKILL specifications (sop-builder and wxo-builder).
​
Using modes with MCP access
Choose a mode that includes MCP tool access when external integrations are required. Ask, Plan, and Advanced modes provide MCP capabilities, while Code mode does not. Use Code mode for standard development tasks where MCP is not needed.
​
Specification-driven development workflow
Follow this recommended workflow:
Use sop-builder to generate the Standard Operating Procedure (SOP).
Have the subject matter expert (SME) validate the SOP.
Use wxo-builder to generate the initial watsonx Orchestrate project. The generated README.md serves as the implementation specification.
Update the solution as needed:
If the business specification changes → update the SOP → rerun wxo-builder.
If the implementation changes → update the README.md → rerun wxo-builder.
Apply incremental updates or hand-edit remaining details as required.
​
wxO VS Code extension
The wxO VS Code extension streamlines setup of the wxO ADK environment by automatically initializing and configuring the ADK and connecting to a remote wxO runtime. It eliminates manual steps such as managing folder structures, environment variables, and connections.
The extension is optional.
It does not affect how coding agents, including Bob, consume MCP servers or SKILL specifications.
Coding agents operate independently of the extension.
​
Important considerations
Coding agents differ in agent-loop quality and underlying model strength. Accuracy and consistency therefore vary across tools. These capabilities accelerate development, but you must still:
Understand the generated code and its behavior.
Validate correctness and quality.
Ensure outputs align with the intended business and technical requirements.
For more information on related capabilities, see Skills in Bob.


---
