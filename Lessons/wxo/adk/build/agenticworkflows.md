Agentic Workflows
Understanding agentic workflows
Agentic workflow is a type of tool with built-in agentic capabilities and automations that support arbitrarily complex orchestration of multiple agents, tools, and people.
Each node can represent an agent, a tool, or built-in capabilities such as user interactions, prompts, or decision logic.
With agentic workflows, you design workflows using control structures such as conditional branching with if-then-else or switch-case, iteration over lists with foreach, and loops that repeat actions until specific conditions are met.
An agentic workflow is composed of nodes and edges. You define nodes of different types and connect them using edges. Because agentic workflows can take several seconds to execute depending on their complexity, they run asynchronously.
Agentic workflows apply to various scenarios, such as:
Repeatable, predictable sequencing of agents, tools, and human tasks is required.
Long-running processes are involved. Agentic workflow supports extended task chains that can take minutes, hours, or even days to complete.
Human-in-the-loop interaction is needed for approvals or decision-making.
Scheduling is necessary to trigger tasks at specific times or intervals.
When an agentic workflow tool is invoked, the system returns an instance ID and waits for the response.
To check the progress, use the Get agentic workflow status tool in a new chat session. Provide the instance ID to retrieve the current status of the agentic workflow.
Tools built using Agentic workflows do not require connection support as connections within Agentic workflows are configured via their downstream component tools.
​
Agentic workflow and ADK
Unlike the UI experience, the pro-code approach uses the ADK CLI and Python library. You build agentic workflows with the Python library included in ADK, then manage them with the ADK CLI in your active environment. This environment can be local or remote. For details, see Environments.
1
Create an agentic workflow

Use Python and the ADK library to create agentic workflows and their nodes. For more information, see:
Building agentic workflows
Agentic workflow nodes
Testing agentic workflow
2
Import the workflow into your environment

After creating a workflow, import it into your active watsonx Orchestrate environment using the command orchestrate tools import with the flag --kind flow. For more information, see Import the agentic workflow.
3
Manage agentic workflows in your environment

After you import an agentic workflow, you can also list it, export it, update it, and remove it from your active environment. Because an agentic workflow is a type of tool, you manage it with the same commands you use for other tools in ADK. For more information, see Managing tools.
​
Agentic workflow key concepts
The sections below introduce the key concepts and components you’ll use when working with agentic workflows:
Edges

Node types

Node specification

Data mapping

Scheduling

Flow callbacks

Multi-language support

​
Agentic workflow examples
The examples/flow_builder directory includes sample agentic workflow that demonstrate key agentic workflow features:
agent_scheduler: Demonstrates agent scheduling.
collaborator_agents: Shows how to sequence multiple agents.
extract_support_request: Uses an LLM to extract information from support requests.
foreach_email: Applies the Foreach control to iterate over a set of items.
get_facts_numbers: Uses the Loop control to repeat work until a condition is met.
get_insurance_rate: Uses a Decisions node to determine insurance rates based on credit rating and loan amount.
get_pet_facts: Demonstrates branching to route requests.
get_tuition_reimbursed: Uses multiple branches to support complex logic routing.
hello_message_flow: Sequences two Python tools together.
ibm_knowledge_to_emails: Combines an agent and a tool in a single agentic workflow.
schedule_helpdesk_alert: Creates a schedulable agentic workflow to check helpdesk availability.
text_extract: Uses the DocProc node to extract text from a document.
user_flow_application_form: Displays a form to the user in the chat.

---

Agentic Workflows
Building agentic workflows
An agentic workflow is a collection of nodes and edges that define the logic of your workflow. To build an agentic workflow, follow these steps:
1
Import your agents and tools

Ensure that the agents and tools you want to connect in an agentic workflow are already imported.
2
Define a Python function with the @flow decorator

Use the @flow decorator to define your agentic workflow. In the decorator, set the name, display_name, description, input_schema, output_schema, initiators, schedulable, suppress_agent_summarization, llm_model, and agent_conversation_memory_turns_limit parameters.
Show @flow decorator parameters

The function must take a single parameter of type Flow and return a Flow object.
Construct the agentic workflow using a combination of tool(), agent(), and edge-building functions like sequence() or edge().
For Branch and Loop nodes, use a Python expression in the evaluator to define the branching or looping condition. For more information, see Agentic workflow expressions.
To support multiple languages, use aflow.target_locales(['fr', 'es', 'de']) to specify target languages for user activities. After you import the agentic workflow, export translations to CSV, translate them, and import them back. For details, see Multi-language support.
When you use forms in user nodes, connect the form buttons to the next node in the flow using the edge() function with the button_label parameter. This connection enables users to trigger the transition to the next node when they click a button on the form.
The following tabs show some code snippet examples of agentic workflow:
Example 1
Example 2
Example 3
Example 4
Example 5
Example 1: Sequencing two tools
Python
@flow(
    name = "hello_message_flow",
    input_schema=Name,
    output_schema=str
)
def build_hello_message_flow(aflow: Flow = None) -> Flow:
    """ Based on the first and last name of a person, combine into a single name and create a simple hello world message. """

    combine_names_node = aflow.tool(combine_names)
    get_hello_message_node = aflow.tool(get_hello_message)

    aflow.edge(START, combine_names_node).edge(combine_names_node, get_hello_message_node).edge(get_hello_message_node, END)

    return aflow
See all 14 lines
For the full example and complete code, see hello_message_flow.
3
Import the agentic workflow

Import the agentic workflow as a tool using the orchestrate tools import command in the CLI.
BASH
orchestrate tools import -k flow -f <file-path>
Show command flags

4
Test the agentic workflow locally in the ADK

Test the agentic workflow you created using a Python script before adding it to an agent. For more information, see Testing flows.
5
Add the agentic workflow to one agent

After successfully testing the agentic workflow, add it to an agent’s specification and update the agent.

---

Workflow nodes
Agent node
Use an agent node to call an agent in your agentic workflow.
To configure an agent node, call the agent() method in your agentic workflow. In this method, define the following parameters:
​
name
stringrequired
The name of the agent.
​
agent
stringrequired
The agent used in the agentic workflow.
​
display_name
string
The display name of the agent.
​
title
string
The title of the agent.
​
message
string
The message of the agent. If not configured, the default message is “Follow the agent instructions”.
​
description
string
The description of the agent.
​
input_schema
type[BaseModel]
Input schema for the tool.
​
output_schema
type[BaseModel]
Output schema for the tool.
​
guidelines
string
The guidelines of the agent.
​
input_map
DataMap
Define input mappings using a structured collection of Assignment objects.
The following example shows how to configure an agent node in an agentic workflow:
Python
'''
Build a simple flow that will sequence call an agent and a tool.
'''

from pydantic import BaseModel, Field
from ibm_watsonx_orchestrate.flow_builder.flows import Flow, flow
from ibm_watsonx_orchestrate.flow_builder.flows.constants import END, START
from .send_emails import send_emails

class FlowInput(BaseModel):
    question: str = Field(description="A topic to search for about IBM")
    emails: str = Field(description="a list of comman separated email address")

class FlowOutput(BaseModel):
    question: str = Field(description="A topic to search for about IBM")
    answer: str = Field(description="A fact about IBM")
    emails: str = Field(description="The email addresse the we sent. comma separated.")

class IBMAgentInput(BaseModel):
    question: str = Field(description="A topic to search for")

class IBMAgentOutput(BaseModel):
    answer: str = Field(description="A fact about IBM")

class EmailAgentInput(BaseModel):
    emails: str = Field(description="Comma separated list of email addresses")
    question: str = Field(description="A topic to search for about IBM")
    answer: str = Field(description="The email content")

class EmailAgentOutput(BaseModel):
    message: str = Field(description="The message we sent.")

@flow(
    name="ibm_knowledge_to_emails",
    description="This flow will send a random fact about IBM to a group of people",
    input_schema=FlowInput,
    output_schema=FlowOutput
)
def build_ibm_knowledge_to_emails(aflow: Flow) -> Flow:
    """ Retrieve a random fact about IBM and send it out to an email list. """

    # when talking to an agent, we need to be very precise on what we want to get done.
    # or there is a chance the agent will not be able to response correctly.
    # In the message, you should refer to information that the Flow engine will send 
    # to the agent.
    ask_agent_for_ibm_knowledge = aflow.agent(
        name="ask_agent_for_ibm_knowledge",
        agent="ibm_agent",
        description="Ask the IBM agent to get a fact based on the provided question.",
        message="Give an answer about IBM based on the provided question.  If you don't know the answer, just say 'I do not know'",
        input_schema=IBMAgentInput,
        output_schema=IBMAgentOutput,
    )

    send_emails_node = aflow.tool(send_emails)
   
    aflow.sequence(START, ask_agent_for_ibm_knowledge, send_emails_node, END)

    return aflow
Collapse


---

Workflow nodes
Tool node
Use a tool node to call a tool in your agentic workflow.
To configure a tool node, use the tool() method in your agentic workflow. In this method, define the following parameters:
​
tool
Any or stringrequired
The tool used in the agentic workflow. Configure it as a string such as "myTool" or as a Python function such as myTool.
Note:
Only functions that use the @tool decorator qualify for the Python function option.
​
name
string
The name of the tool.
​
display_name
string
The display name of the tool.
​
description
string
The description of the tool.
​
input_schema
type[BaseModel]
Input schema for the tool.
​
output_schema
type[BaseModel]
Output schema for the tool.
​
input_map
DataMap
Define input mappings using a structured collection of Assignment objects.
​
error_handler_config
NodeErrorHandlerConfi
Defines the configuration for the retry option using a JSON structure. In this JSON, set the following fields:
error_message: an optional string that describes the retry error.
max_retries: an optional integer that limits how many times the node retries.
retry_interval: an optional integer that sets the interval between retries in milliseconds.
​
Tool callbacks
Tool nodes support four tool types: OpenAPI, Python, Flow, and MCP. The Flow runtime executes these callbacks using a fire-and-forget pattern for optimal performance.
Recommendation
For Flow callbacks, use OpenAPI tools as the preferred callback mechanism. OpenAPI tools provide a clean, stateless callback interface without the complexity of managing user interactions or correlation ID propagation.
Limitation: Flow Tools as Callbacks
When using a Flow as a callback tool within another Flow, there is a current limitation:
Restriction: Flow callback tools must not contain user activity nodes (nodes that require user interaction or input).
Reason: If a Flow callback contains user activity nodes, the Flow runtime would need to submit user activity events to the user’s chat thread. This requires propagating correlation IDs through the Flow callback event chain, which adds significant complexity to the implementation.
Workaround: To keep the implementation simple and maintainable, Flows used as callback tools should be designed without user interaction requirements.
​
Example
The following example shows how to configure a tool node in an agentic workflow:
Python
'''
Build a simple flow that will sequence call an agent and a tool.
'''

from pydantic import BaseModel, Field
from ibm_watsonx_orchestrate.flow_builder.flows import Flow, flow
from ibm_watsonx_orchestrate.flow_builder.flows.constants import END, START
from .send_emails import send_emails

class FlowInput(BaseModel):
    question: str = Field(description="A topic to search for about IBM")
    emails: str = Field(description="a list of comman separated email address")

class FlowOutput(BaseModel):
    question: str = Field(description="A topic to search for about IBM")
    answer: str = Field(description="A fact about IBM")
    emails: str = Field(description="The email addresse the we sent. comma separated.")

class IBMAgentInput(BaseModel):
    question: str = Field(description="A topic to search for")

class IBMAgentOutput(BaseModel):
    answer: str = Field(description="A fact about IBM")

class EmailAgentInput(BaseModel):
    emails: str = Field(description="Comma separated list of email addresses")
    question: str = Field(description="A topic to search for about IBM")
    answer: str = Field(description="The email content")

class EmailAgentOutput(BaseModel):
    message: str = Field(description="The message we sent.")

@flow(
    name="ibm_knowledge_to_emails",
    description="This flow will send a random fact about IBM to a group of people",
    input_schema=FlowInput,
    output_schema=FlowOutput
)
def build_ibm_knowledge_to_emails(aflow: Flow) -> Flow:
    """ Retrieve a random fact about IBM and send it out to an email list. """

    # when talking to an agent, we need to be very precise on what we want to get done.
    # or there is a chance the agent will not be able to response correctly.
    # In the message, you should refer to information that the Flow engine will send 
    # to the agent.
    ask_agent_for_ibm_knowledge = aflow.agent(
        name="ask_agent_for_ibm_knowledge",
        agent="ibm_agent",
        description="Ask the IBM agent to get a fact based on the provided question.",
        message="Give an answer about IBM based on the provided question.  If you don't know the answer, just say 'I do not know'",
        input_schema=IBMAgentInput,
        output_schema=IBMAgentOutput,
    )

    send_emails_node = aflow.tool(send_emails)
   
    aflow.sequence(START, ask_agent_for_ibm_knowledge, send_emails_node, END)

    return aflow
Collapse


---

Workflow nodes
Branch node
Use a conditions branch node to create different branches in your agentic workflow. When conditions are evaluated, conditions branch nodes execute only the first matching path, providing sequential decision-making logic similar to if-else statements.
To configure a conditions branch node, call the conditions() method to create a branch with conditional expressions.
The example below demonstrates how to configure a branch node.
Python
"""
Based on the request, we will return the list of facts about the pet.
A pet can be either a cat or a dog.
"""

from pydantic import BaseModel, Field

from ibm_watsonx_orchestrate.flow_builder.flows import (
    Flow, flow, START, END, Branch
)

class Pet(BaseModel):
    kind: str = Field(description="the kind of pet: dog or cat")

class PetFacts(BaseModel):
    facts: list[str] = Field(description="A list of facts about the pet")

@flow(
        name = "get_pet_facts_if_else",
        input_schema = Pet,
        output_schema = PetFacts
)
def build_get_pet_facts_if_else_flow(aflow: Flow) -> Flow:
    """ Based on the request, we will return the list of facts about the pet. A pet can be either a cat or a dog. """
    
    dog_fact_node = aflow.tool("getDogFact")
    cat_fact_node = aflow.tool("getCatFact")

    # create a branch with conditions
    check_pet_kind_conditions_branch: Branch = aflow.conditions()
    check_pet_kind_conditions_branch.condition(
        expression="flow.input.kind.strip().lower() == 'dog'", to_node=dog_fact_node
        ).condition(expression="flow.input.kind.strip().lower() == 'cat'", to_node=cat_fact_node
        ).condition(to_node=dog_fact_node, default=True)
    aflow.edge(START, check_pet_kind_conditions_branch)


    aflow.edge(dog_fact_node, END)
    aflow.edge(cat_fact_node, END)

    return aflow
Collapse


---

Workflow nodes
Parallel node
Use a parallel branch node to run multiple branches of your agentic workflow at the same time. When conditions match, the node runs every matching path so you can complete independent work in parallel.
Parallel branch nodes differ from conditions branch nodes in these ways:
Feature	Conditions branch node (conditions())	Parallel branch node (parallel_conditions())
Processing	First matching condition only	ALL matching conditions
Semantics	Sequential evaluation such as if-else logic	Concurrent evaluation
Use case	Exclusive paths	Concurrent execution
Merging	Single path continues	Waits for all paths to complete
​
Configuring unconditional parallel branch
To configure an unconditional parallel branch node, call the parallel() method in your agentic workflow. Use this node when you want every branch to run every time. Define the following parameters in this method:
Use unconditional parallel when you need to:
Run multiple teams at the same time
Send work to multiple services at the same time
Process data through multiple pipelines at the same time
​
evaluator
Union[Conditions, None]
Set to None for unconditional execution. All branches run.
​
name
string
Name for the parallel node. watsonx Orchestrate generates this value if you do not provide it.
​
display_name
string
Display name for the parallel node.
Example
from ibm_watsonx_orchestrate.flow_builder.flows import flow, Flow, START, END

@flow(name="multi_squad_development")
def build_flow(aflow: Flow) -> Flow:
    # Create unconditional parallel agentic workflow
    parallel_dev = aflow.parallel(
        evaluator=None,  # No evaluator = all paths run
        name="parallel_development",
        display_name="Development Phase"
    )
    
    # Define work for each squad (all run in parallel)
    squad1 = parallel_dev.script(
        name="squad1_work",
        script="print('Squad 1 working...')"
    )
    
    squad2 = parallel_dev.script(
        name="squad2_work",
        script="print('Squad 2 working...')"
    )
    
    squad3 = parallel_dev.script(
        name="squad3_work",
        script="print('Squad 3 working...')"
    )
    
    # Connect each squad from START to END within parallel agentic workflow
    parallel_dev.sequence(START, squad1, END)
    parallel_dev.sequence(START, squad2, END)
    parallel_dev.sequence(START, squad3, END)
    
    # Continue after all squads complete
    completion = aflow.script(
        name="all_complete",
        script="print('All squads completed!')"
    )
    
    aflow.sequence(START, parallel_dev, completion, END)
    return aflow
See all 40 lines
​
Configuring conditional parallel branch
To configure a conditional parallel node, call the parallel_conditions() method in your agentic workflow. Use this node when you want to run every branch whose condition matches. Define the following parameters in this method:
Use conditional parallel when you need to:
Process work based on multiple criteria
Route work to multiple handlers based on attributes
Fan out work only when conditions match
​
name
stringrequired
Name for the parallel node. watsonx Orchestrate generates this value if you leave it empty.
​
display_name
string
Display name for the parallel node. The default value is the node name.
​
Adding conditions to parallel branch
To add conditions to the parallel branch node, call the condition() method. The node runs all matching conditions in parallel. Define the following parameters in this method:
​
to_node
Noderequired
Node to run when the condition matches.
​
expression
string
Python expression to evaluate. Required unless default=True.
​
default
bool
When set to True, this parameter defines the default case.
Example
from pydantic import BaseModel
from ibm_watsonx_orchestrate.flow_builder.flows import flow, Flow, START, END

class TaskInput(BaseModel):
    priority: str
    category: str
    value: float

@flow(
    name="conditional_parallel_processing",
    input_schema=TaskInput
)
def build_flow(aflow: Flow) -> Flow:
    # Create conditional parallel agentic workflow
    parallel_processing = aflow.parallel_conditions(
        name="task_processing",
        display_name="Task Processing"
    )
    
    # Define handlers within the parallel subflow
    high_priority = parallel_processing.script(
        name="high_priority_handler",
        script="print('Processing high priority task')"
    )
    
    billing = parallel_processing.script(
        name="billing_handler",
        script="print('Processing billing task')"
    )
    
    large_value = parallel_processing.script(
        name="large_value_handler",
        script="print('Processing large value task')"
    )
    
    default_handler = parallel_processing.script(
        name="default_handler",
        script="print('Default processing')"
    )
    
    # Add conditions - all matching conditions run in parallel
    parallel_processing.condition(
        expression="flow.input.priority == 'high'",
        to_node=high_priority
    ).condition(
        expression="flow.input.category == 'billing'",
        to_node=billing
    ).condition(
        expression="flow.input.value > 1000",
        to_node=large_value
    ).condition(
        default=True,  # Default case (like 'else')
        to_node=default_handler
    )
    
    # Connect handlers to END within parallel agentic workflow
    parallel_processing.sequence(high_priority, END)
    parallel_processing.sequence(billing, END)
    parallel_processing.sequence(large_value, END)
    parallel_processing.sequence(default_handler, END)
    
    # Continue after all matching paths complete
    aflow.sequence(START, parallel_processing, END)
    return aflow
See all 64 lines
​
Expression syntax
Conditions in parallel agentic workflows use Python expressions that can access:
flow.input.* - Input data
flow.private.* - Private state
flow.output.* - Output data from upstream nodes
The following examples show common expression patterns you can use:
# Simple comparison
expression="flow.input.priority == 'high'"

# Multiple conditions with 'and'
expression="flow.input.priority == 'high' and flow.input.value > 1000"

# Multiple conditions with 'or'
expression="flow.input.category == 'billing' or flow.input.category == 'finance'"

# Checking boolean flags
expression="flow.private.needs_approval is True"

# Numeric comparisons
expression="flow.input.amount > 5000"

# String operations
expression="'urgent' in flow.input.tags"
​
Common patterns
The following examples show common ways to use parallel nodes in your agentic workflows:
Fan-Out Processing
Conditional Multi-Handler
Parallel with Aggregation
Use this pattern to process data through multiple independent handlers:
parallel = flow.parallel(evaluator=None, name="fan_out")

# Create multiple processors
processor1 = parallel.tool(name="process_type_a", tool=process_a)
processor2 = parallel.tool(name="process_type_b", tool=process_b)
processor3 = parallel.tool(name="process_type_c", tool=process_c)

# All processors run in parallel
parallel.sequence(START, processor1, END)
parallel.sequence(START, processor2, END)
parallel.sequence(START, processor3, END)
​
Best practices
Follow these best practices when you work with parallel nodes:
Choose the Right Node Type

Avoid Infinite Loops

Merge Parallel Paths

Handle Errors in Parallel Branches

​
Example: Feature delivery agentic workflow
This example shows how you can use both conditional and unconditional parallel processing to complete feature delivery work.
Example
from typing import List
from pydantic import BaseModel, Field
from ibm_watsonx_orchestrate.flow_builder.flows import (
    Flow, flow, ScriptNode, START, END
)

class FlowInput(BaseModel):
    feature_name: str = Field(description="Name of the feature to deliver")
    design_needed: bool = Field(default=True, description="Whether design work is needed")
    arch_needed: bool = Field(default=True, description="Whether architecture work is needed")

class FlowOutput(BaseModel):
    status: str = Field(description="Final status of the feature delivery")
    phases_completed: List[str] = Field(description="List of completed phases")

class PrivateState(BaseModel):
    design_needed: bool = Field(default=False)
    arch_needed: bool = Field(default=False)
    phases_completed: List[str] = Field(default_factory=list)

@flow(
    name="feature_delivery_workflow",
    display_name="Feature Delivery Agentic Workflow",
    description="An agentic workflow demonstrating parallel execution in multiple phases",
    input_schema=FlowInput,
    output_schema=FlowOutput,
    private_schema=PrivateState
)
def build_feature_delivery_flow(aflow: Flow) -> Flow:
    # Initialize state
    init_state = aflow.script(
        name="init_state",
        script="""
flow.private.design_needed = flow.input.design_needed
flow.private.arch_needed = flow.input.arch_needed
flow.private.phases_completed = []
        """
    )
    
    # PHASE 1: Conditional Parallel (Design & Architecture)
    phase1_parallel = aflow.parallel_conditions(
        name="parallel_phase1",
        display_name="Phase 1 - Design & Architecture"
    )
    
    design_work = phase1_parallel.script(
        name="design_work",
        script="""
print("Starting design work...")
flow.private.phases_completed.append("Design")
print("Design work completed")
        """
    )
    
    architecture_work = phase1_parallel.script(
        name="architecture_work",
        script="""
print("Starting architecture work...")
flow.private.phases_completed.append("Architecture")
print("Architecture work completed")
        """
    )
    
    phase1_skip = phase1_parallel.script(
        name="phase1_skip",
        script="print('Phase 1: Skipping...')"
    )
    
    # Add conditions
    phase1_parallel.condition(
        expression="flow.private.design_needed is True",
        to_node=design_work
    ).condition(
        expression="flow.private.arch_needed is True",
        to_node=architecture_work
    ).condition(
        default=True,
        to_node=phase1_skip
    )
    
    phase1_parallel.sequence(design_work, END)
    phase1_parallel.sequence(architecture_work, END)
    phase1_parallel.sequence(phase1_skip, END)
    
    # PHASE 2: Unconditional Parallel (Development)
    phase2_parallel = aflow.parallel(
        evaluator=None,
        name="parallel_phase2",
        display_name="Phase 2 - Development"
    )
    
    squad1_work = phase2_parallel.script(
        name="squad1_work",
        script="print('Squad 1: Development completed')"
    )
    
    squad2_work = phase2_parallel.script(
        name="squad2_work",
        script="print('Squad 2: Development completed')"
    )
    
    squad3_work = phase2_parallel.script(
        name="squad3_work",
        script="print('Squad 3: Development completed')"
    )
    
    phase2_parallel.sequence(START, squad1_work, END)
    phase2_parallel.sequence(START, squad2_work, END)
    phase2_parallel.sequence(START, squad3_work, END)
    
    # PHASE 3: Sequential (QA)
    qa_work = aflow.script(
        name="qa_work",
        script="""
print("Starting QA testing...")
flow.private.phases_completed.append("QA")
        """
    )
    
    finalize = aflow.script(
        name="finalize",
        script="""
flow.output.status = "Feature delivery completed successfully"
flow.output.phases_completed = flow.private.phases_completed
        """
    )
    
    # Connect all phases
    aflow.edge(START, init_state)
    aflow.edge(init_state, phase1_parallel)
    aflow.edge(phase1_parallel, phase2_parallel)
    aflow.edge(phase2_parallel, qa_work)
    aflow.edge(qa_work, finalize)
    aflow.edge(finalize, END)
    
    return aflow


---


Workflow nodes
Foreach node
Use a foreach node to create a sub agentic workflow that repeats nodes for each item in the input schema.
To configure a foreach node in an agentic workflow, call the foreach() method to define a nested agentic workflow. In this method, define the following parameters:
​
item_schema
BaseModel
The schema that defines each item to iterate over.
​
input_schema
BaseModel
The input schema for the nested agentic workflow executed by the foreach node.
​
output_schema
BaseModeldeprecated
The output schema for the nested agentic workflow executed by the foreach node.
Example
foreach_flow: Flow = aflow.foreach(item_schema = CustomerRecord)
Next, call the foreach agentic workflow for the node you want to repeat. You can include more than one node in the same foreach flow.
Example
node2 = foreach_flow.tool(send_invitation_email)
foreach_flow.sequence(START, node2, END)
The example below shows how to configure a foreach node:
Python
"""
In this example, the user is retrieving a set of email addresses from a contact list, and 
for each email address, sending out an invitation.
"""

from typing import List

from pydantic import BaseModel, Field

from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from ibm_watsonx_orchestrate.flow_builder.flows import Flow, flow, START, END
from ibm_watsonx_orchestrate.flow_builder.types import ForeachPolicy

from .send_invitation_email import send_invitation_email
from .get_emails_from_customer import get_emails_from_customer, CustomerRecord


class CustomerName(BaseModel):
    name: str = Field(description="The name of the customer")

class Invitations(BaseModel):
    invitations: List[str]

@flow(
    name="send_invitation_to_customer",
    input_schema=CustomerName
)
def build_send_invitation_to_customer_flow(aflow: Flow) -> Flow:
    """ Given a list of customers, we will iterate through the list and send email to each """
    
    get_customer_list_node = aflow.tool(get_emails_from_customer)

    # calling add_foreach will create a subflow, and we can add more node to the subflow
    foreach_flow: Flow = aflow.foreach(item_schema = CustomerRecord) \
        .policy(kind=ForeachPolicy.SEQUENTIAL)
        # .policy(kind=ForeachPolicy.PARALLEL) # replace with 'ForeachPolicy.PARALLEL' if need to run .foreach in parallel
    
    node2 = foreach_flow.tool(send_invitation_email)
    foreach_flow.sequence(START, node2, END)

    # add the foreach flow to the main flow
    aflow.edge(START, get_customer_list_node)
    aflow.edge(get_customer_list_node, foreach_flow)
    aflow.edge(foreach_flow, END)

    return aflow
See all 46 lines
​
Foreach processing method
You can configure how your foreach node processes input items. There are two processing methods:
Sequential
A sequential foreach processes items one after another. The next item starts only after the previous one finishes. Use this method when the order of item processing affects the result.
Parallel
A parallel foreach processes one or more items at the same time. In most cases, this method runs faster than the sequential approach.
To set the processing method, call the policy() method in your foreach node. This method accepts the following parameter:
​
kind
ForeachPolicyrequired
Defines the processing method. Use ForeachPolicy.SEQUENTIAL for sequential processing or ForeachPolicy.PARALLEL for parallel processing.
Python
def build_send_invitation_to_customer_flow(aflow: Flow) -> Flow:
    """ Given a list of customers, we will iterate through the list and send email to each """
    
    get_customer_list_node = aflow.tool(get_emails_from_customer)

    # calling add_foreach will create a subflow, and we can add more node to the subflow
    foreach_flow: Flow = aflow.foreach(item_schema = CustomerRecord) \
        .policy(kind=ForeachPolicy.SEQUENTIAL)
        # .policy(kind=ForeachPolicy.PARALLEL) # replace with 'ForeachPolicy.PARALLEL' if need to run .foreach in parallel


---
Workflow nodes
Decisions node
A decisions node manages and executes a decision table composed of a set of rules. The system evaluates each rule in order from top to bottom and returns the result of the first successful rule as the final result.
​
Rule
Each rule includes two parts:
conditions: A set of conditions to evaluate.
actions: The results to return when all conditions are satisfied.
​
Condition
Each condition includes a variable reference and a value expression. To simplify condition building and ensure correct syntax, use the DecisionsCondition class.
Variable Naming Convention: Conditions can reference all upstream variables using fully qualified path formats:
Agentic workflow inputs: flow.input.<variable_name>. For example, to check the grade input variable, use flow.input.grade.
Agentic workflow private variables: flow.private.<variable_name>
Upstream node outputs: use the variable path emitted by the upstream node
Show supported types

Show supported expressions

The following example checks whether the value of revenue_quote_ratio falls within the range from 0 (inclusive) to 50 (exclusive).
Python
rule.condition("flow.input.revenue_quote_ratio", DecisionsCondition().in_range(0, 50, True, False))
​
Action
An action defines the result when all conditions in a rule are satisfied. Actions can reference agentic workflow output variables using the fully qualified path format flow.output.<variable_name>, or any other agentic workflow variable, such as flow.private.<variable_name>. You can also define a default action to return when no rules match.
Show supported action types

​
Decision Table Columns
Decision table columns define the mapping between technical variable names and user-friendly display names in the agentic workflow Builder UI. Use the DecisionTableColumn class to specify columns for both conditions and actions.
Python
from ibm_watsonx_orchestrate.flow_builder.types import DecisionTableColumn

decision_table_columns=[
    DecisionTableColumn(variable="flow.input.grade", display_name="Credit Grade"),
    DecisionTableColumn(variable="flow.input.loan_amount", display_name="Loan Amount"),
    DecisionTableColumn(variable="flow.output.insurance_required", display_name="Insurance Required"),
    DecisionTableColumn(variable="flow.output.insurance_rate", display_name="Insurance Rate"),
]
​
Locale
You can specify a locale string, such as en-US, fr-FR, or es-MX, to control how dates are parsed. Currently, locale only affects date parsing.
​
Example
In this example get_insurance_rate, you define a set of rules to calculate the insurance rate based on credit grade and loan amount:
Python
'''
Build a simple agentic workflow that will programmatically create a decisions table.
'''

from typing import Literal
from pydantic import BaseModel

from ibm_watsonx_orchestrate.flow_builder.flows import END, Flow, flow, START, DecisionsNode, DecisionsRule, DecisionsCondition
from ibm_watsonx_orchestrate.flow_builder.types import DecisionTableColumn


class Assessment(BaseModel):
    """
    This class represents the outcome of the assessment.
    """
    insurance_required: bool = False
    insurance_rate: float = 0.0
    assessment_error: str | None = None

class AssessmentData(BaseModel):
    """
    This class represents the data to be assessed.
    """
    loan_amount: float
    grade: Literal['A', 'B']

def build_decisions(aflow: Flow) -> DecisionsNode:
    """
    Build a Decisions Table programmatically as a node.

    For example, read from an Excel spreadsheet or CSV and populate the decision table.
    """

    rules = []

    ## We will be build the rules programmatically.
    rule1 = DecisionsRule()
    rule1.condition("flow.input.grade", DecisionsCondition().equal("A")).condition("flow.input.loan_amount", DecisionsCondition().less_than(100000))
    rule1.action("flow.output.insurance_required", False)
    rules.append(rule1)

    rule2 = DecisionsRule()
    rule2.condition("flow.input.grade", DecisionsCondition().equal("A")).condition("flow.input.loan_amount", DecisionsCondition().in_range(100000, 300000, True, False))
    rule2.action("flow.output.insurance_required", True).action("flow.output.insurance_rate", 0.001)
    rules.append(rule2)

    rule3 = DecisionsRule()
    rule3.condition("flow.input.grade", DecisionsCondition().equal("A")).condition("flow.input.loan_amount", DecisionsCondition().in_range(300000, 600000, True, False))
    rule3.action("flow.output.insurance_required", True).action("flow.output.insurance_rate", 0.003)
    rules.append(rule3)

    rule4 = DecisionsRule()
    rule4.condition("flow.input.grade", DecisionsCondition().equal("A")).condition("flow.input.loan_amount", DecisionsCondition().greater_than_or_equal(600000))
    rule4.action("flow.output.insurance_required", True).action("flow.output.insurance_rate", 0.005)
    rules.append(rule4)

    ## We will be build the rules programmatically.
    rule5 = DecisionsRule()
    rule5.condition("flow.input.grade", DecisionsCondition().equal("B")).condition("flow.input.loan_amount", DecisionsCondition().less_than(100000))
    rule5.action("flow.output.insurance_required", False)
    rules.append(rule5)

    rule6 = DecisionsRule()
    rule6.condition("flow.input.grade", DecisionsCondition().equal("B")).condition("flow.input.loan_amount", DecisionsCondition().in_range(100000, 300000, True, False))
    rule6.action("flow.output.insurance_required", True).action("flow.output.insurance_rate", 0.0025)
    rules.append(rule6)

    rule7 = DecisionsRule()
    rule7.condition("flow.input.grade", DecisionsCondition().equal("B")).condition("flow.input.loan_amount", DecisionsCondition().in_range(300000, 600000, True, False))
    rule7.action("flow.output.insurance_required", True).action("flow.output.insurance_rate", 0.005)
    rules.append(rule7)

    rule8 = DecisionsRule()
    rule8.condition("flow.input.grade", DecisionsCondition().equal("B")).condition("flow.input.loan_amount", DecisionsCondition().greater_than_or_equal(600000))
    rule8.action("flow.output.insurance_required", True).action("flow.output.insurance_rate", 0.0075)
    rules.append(rule8)

    node = aflow.decisions(
        name="assess_insurance_rate",
        display_name="Assess insurance rate.",
        description="Based on credit rate and loan amount, assess insurance rate.",
        rules=rules,
        default_actions={
            "flow.output.assessment_error": "Not assessed. Incorrect data submitted."
        },
        decision_table_columns=[
            DecisionTableColumn(variable="flow.input.grade", display_name="Grade"),
            DecisionTableColumn(variable="flow.input.loan_amount", display_name="Loan Amount"),
            DecisionTableColumn(variable="flow.output.insurance_required", display_name="Insurance Required"),
            DecisionTableColumn(variable="flow.output.insurance_rate", display_name="Insurance Rate"),
            DecisionTableColumn(variable="flow.output.assessment_error", display_name="Assessment Error"),
        ]
    )
    return node


@flow(
    name="get_insurance_rate",
    input_schema=AssessmentData,
    output_schema=Assessment
    )
def build_get_insurance_rate(aflow: Flow = None) -> Flow:
    """
    Creates an agentic workflow to calculate the insurance rate based on provided information.
    """
    decisions_node = build_decisions(aflow)

    aflow.sequence(START, decisions_node, END)

    return aflow
See all 110 lines
Note:
The decision_table_columns parameter is required for proper UI integration in agentic workflow Builder.

---

Workflow nodes
Generative prompt node
Use a generative prompt node to generate AI-driven content using large language models (LLMs). To configure a generative prompt node in your agentic workflow, call the prompt() method. In this method, define the following parameters:
​
name
stringrequired
Unique identifier for the node.
​
display_name
string
Display name for the node.
​
system_prompt
string or list[string]
Initial instructions that guide the LLM’s behavior.
It also supports expressions. For example: flow.input.variable_1.
​
user_prompt
string or list[string]
The specific request or task you want the LLM to perform.
It also supports expressions. For example: flow.input.variable_1.
​
prompt_examples
list[PromptExample]
Examples of user prompts. You can configure:
input: The example input prompt.
expected_output: The expected output for the given input.
enabled: A boolean value to enable or disable the example.
​
llm
string
LLM used for content generation.
​
llm_parameters
PromptLLMParameters
Parameters for the LLM. You can configure:
temperature: Controls randomness. Higher values produce more diverse outputs.
min_new_tokens: Sets the minimum number of tokens to generate.
max_new_tokens: Sets the maximum number of tokens to generate.
top_k: Limits token selection to the top k most likely options.
top_p: Uses nucleus sampling to select from the top p cumulative probability.
stop_sequences: Defines sequences that stop generation when encountered.
​
description
string
Description of the node.
​
input_schema
type[BaseModel]
Input schema for the LLM.
​
output_schema
type[BaseModel]
Output schema for the LLM.
​
input_map
DataMap
Define input mappings using a structured collection of Assignment objects.
​
error_handler_config
NodeErrorHandlerConfi
Defines the configuration for the retry option using a JSON structure. In this JSON, set the following fields:
error_message: an optional string that describes the retry error.
max_retries: an optional integer that limits how many times the node retries.
retry_interval: an optional integer that sets the interval between retries in milliseconds.
The following example shows how to configure a generative prompt node in a Python function and instantiate it in an agentic workflow:
Python
'''
Build a simple hello world agentic workflow that will combine the result of two tools.
'''

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from ibm_watsonx_orchestrate.flow_builder.flows import END, Flow, flow, START, PromptNode

from .email_helpdesk import email_helpdesk

class Message(BaseModel):
    """
    This class represents the content of a support request message.

    Attributes:
        message (str): support request message
    """
    message: str
    requester_name: Optional[str] = Field(default=None, description="Name of the support requestor.")
    requester_email: Optional[str] = Field(default=None, description="Email address of the support requestor.")
    received_on: Optional[str|datetime] = Field(default=None, description="The date when the support message was received.")

class SupportInformation(BaseModel):
    requester_name: str | None = Field(description="Name of the support requestor.")
    requester_email: str | None = Field(description="Email address of the support requestor.")
    summary: str = Field(description="A high level summary of the support issue.")
    details: str = Field(description="Original text of the support request.")
    order_number: str | None = Field(description="The order number.")
    received_on: datetime | None = Field(description="The date when the support message was received.")

def build_prompt_node(aflow: Flow) -> PromptNode:
    prompt_node = aflow.prompt(
        name="extract_support_info",
        display_name="Extract information from a support request message.",
        description="Extract information from a support request message.",
        system_prompt=[
            "You are a customer support processing assistant, your job take the supplied support request received from email,",
            "and extract the information in the output as specified in the schema."
        ],
        user_prompt=[
            "Here is the {message}"
        ],
        llm="meta-llama/llama-3-3-70b-instruct",
        llm_parameters={    
            "temperature": 0,
            "min_new_tokens": 5,
            "max_new_tokens": 400,
            "top_k": 1,
            "stop_sequences": ["Human:", "AI:"]
        },
        error_handler_config={
            "error_message": "An error has occurred while invoking the LLM",
            "max_retries": 1,
            "retry_interval": 1000
        },
        input_schema=Message,
        output_schema=SupportInformation
    )
    return prompt_node

@flow(
        name = "extract_support_info",
        input_schema=Message,
        output_schema=SupportInformation
    )
def build_extract_support_info(aflow: Flow = None) -> Flow:
    """
    Creates an agentic workflow that will use the Prompt node to extract information from a support
    message, and forward the summary to the helpdesk.
    This agentic workflow will rely on the agentic workflow engine to perform automatic data mapping at runtime.

    Args:
        flow (Flow, optional): During deployment of the agentic workflow model, it will be passed an agentic workflow instance.

    Returns:
        Flow: The created agentic workflow.
    """
    email_helpdesk_node = aflow.tool(email_helpdesk)
    prompt_node = build_prompt_node(aflow)

    aflow.sequence(START, prompt_node, email_helpdesk_node, END)

    return aflow
Collapse


---

Workflow nodes
User activity node
Use a user activity node to define interactive steps in your agentic workflow where users provide or receive information in one of two ways:
In a multi-turn conversation, where the user provides or receives one piece of data at a time
Through a form, which prompts the user for several pieces of data in a single conversational turn
Note:
User activity nodes support multi-language configurations. Define target languages in your agentic workflow code and manage translations through CSV export and import. For complete details, see Multi-language support.
To add a user activity node to your agentic workflow, start by creating a userflow() object.
​
Multi-turn conversations user activity
To collect or deliver one piece of data at a time, call field() on the userflow() object. This method accepts the following input parameters:
​
name
stringrequired
Unique identifier for the node.
​
kind
UserFieldKindrequired
Type of user activity. Supported types: Text, Date, DateTime, Time, Number, File, Boolean, Object, Choice.
​
display_name
string
Display name for the node.
​
description
string
Description of the node.
​
direction
stringrequired
Indicates whether the node is for input or output.
​
default
any
Default value for the node.
​
option
UserFieldOption
List of predefined options with their labels and values.
​
is_list
bool
Indicates whether the node accepts multiple values.
​
min
any
Minimum value or constraint.
​
max
any
Maximum value or constraint.
​
input_map
DataMap
Define input mappings using a structured collection of Assignment objects.
​
custom
dictionary
Dictionary for additional metadata or configuration.
Here is an example that shows how to use field():
Python
from typing import List
from pydantic import BaseModel, Field
from ibm_watsonx_orchestrate.flow_builder.flows import (
    Flow, flow, UserNode, START, END
)
from ibm_watsonx_orchestrate.flow_builder.types import Assignment, UserFieldKind
from ibm_watsonx_orchestrate.flow_builder.data_map import DataMap

class Name(BaseModel):
    """
    This class represents a person's name.

    Attributes:
        name (str): The person's first name.
    """
    first_name: str = Field(default="John Doe", description="First name")

@flow(
    name ="user_flow_example",
    display_name="user_flow_example",
    description="Example user flow.",
    input_schema=Name,
)
def build_user_flow(aflow: Flow = None) -> Flow:
    # user_flow which is a subflow to be added to the aflow
    user_flow = aflow.userflow()

    # add file upload
    user_node1 = user_flow.field(direction="input",name="upload", display_name="File upload 1",  kind=UserFieldKind.File)

    # add file download
    data_map = DataMap()
    data_map.add(Assignment(target_variable="self.input.value",value_expression="flow[\"userflow_1\"][\"File upload 1\"].output.value"))
    user_node2 = user_flow.field(direction="output",name="download", display_name="Download file",  kind=UserFieldKind.File, input_map=data_map)

    # add a Display user text field
    user_node3 = user_flow.field(direction="output",name="display_first_name", display_name="Display first name", kind=UserFieldKind.Text, text="Display of first name is {flow.input.first_name}")

    # add a text input field
    user_node4 = user_flow.field(direction="input",name="last_name", display_name="Last name",  kind=UserFieldKind.Text)
    
    # add a Number input field
    user_node5 = user_flow.field(direction="input",name="age", display_name="Age",  kind=UserFieldKind.Number)

    # create a data map to build an array to be assigned to a user field of kind List
    data_map = DataMap()
    data_map.add(Assignment(target_variable="self.input.value",value_expression="[\"Alice\", \"Bob\", \"Charlie\", \"Diana\", \"Ethan\", \"Fiona\", \"George\"]"))
    user_node6 = user_flow.field(direction="output",name="Friends", display_name="List of friends", kind=UserFieldKind.List, input_map=data_map)

    # add a Choice input field
    data_map_choices = DataMap()
    data_map_choices.add(Assignment(target_variable="self.input.choices",value_expression='["dog", "cat", "bird", "fish"]'))
    user_node7 = user_flow.field(direction="input",name="pet_choice",display_name="Select Your Pet",kind=UserFieldKind.Choice,text="Choose your favorite pet:",input_map=data_map_choices)
    
    # A user flow edges
    user_flow.edge(START, user_node1)
    user_flow.edge(user_node1, user_node2)
    user_flow.edge(user_node2, user_node3)
    user_flow.edge(user_node3, user_node4)
    user_flow.edge(user_node4, user_node5)
    user_flow.edge(user_node5, user_node6)
    user_flow.edge(user_node6, END)
    
    # add the user flow to the flow sequence to create the flow edges
    aflow.sequence(START, user_flow, END)

    return aflow
Collapse
​
Forms user activity
To prompt for multiple pieces of data in a single turn, instantiate the form() object to create a form node. This method accepts the following input parameters:
​
name
stringrequired
The internal name of the form.
​
display_name
string
The display name shown on the form.
​
instructions
string
Instructions text for the form.
​
submit_button_label
string
The label for the submit button. Defaults to Submit if not set.
​
cancel_button_label
string
The label for the cancel button. If set to None, hides the button.
​
Forms fields
After instantiating the form object, add fields to it. Each field type requires its own configuration. Supported field types include:
text_input_field

Creates a text input field. Configure it as a single-line input or a multi-line text area.
Parameters:
​
name
stringrequired
The internal name of the field.
​
label
string
Display label for the field.
​
required
bool
Whether the field is required. Defaults to False.
​
single_line
bool
Whether the field uses a single line. If False, creates a multi-line text area. Defaults to True.
​
placeholder_text
string
Placeholder text for the field.
​
help_text
string
Help text for the field.
​
default
any
Default value for the field, passed as DataMap.
​
regex
string
Regular expression pattern for input validation.
​
regex_error_message
string
Custom error message for failed regex validation. Defaults to: “Input does not match the required pattern”.
boolean_input_field

Creates a boolean input field. Render it as a checkbox or radio buttons.
Parameters:
​
name
stringrequired
The internal name of the field.
​
label
string
Display label for the field.
​
single_checkbox
bool
Whether to display as a single checkbox. If False, displays as radio buttons. Defaults to True.
​
default
any
Default value for the field, passed as input_map.
​
true_label
string
Label for the true option. Defaults to True.
​
false_label
string
Label for the false option. Defaults to False.
date_range_input_field

Creates a date range input field with start and end date pickers.
Parameters:
​
name
stringrequired
The internal name of the field.
​
label
string
Display label for the field.
​
required
bool
Whether the field is required. Defaults to False.
​
start_date_label
string
Label for the start date field.
​
end_date_label
string
Label for the end date field.
​
default_start
any
Default value for the start date, passed as DataMap.
​
default_end
any
Default value for the end date, passed as DataMap.
​
min_date
any
DataMap that sets the minimum date constraint and maps to self.input.min_date.
​
max_date
any
DataMap that sets the maximum date constraint and maps to self.input.max_date.
date_input_field

Creates a date input field.
Parameters:
​
name
stringrequired
The internal name of the field.
​
label
string
Display label for the field.
​
required
bool
Whether the field is required. Defaults to False.
​
default
any
Default value for the field, passed as DataMap.
​
min_date
any
Minimum date value for the allowed range.
​
max_date
any
Maximum date value for the allowed range.
​
multiple_dates
bool
Whether the field supports selecting more than one date. Defaults to False.
datetime_input_field

Creates a datetime or time input field.
​
name
stringrequired
Internal name of the field.
​
label
string
Display label for the field.
​
required
bool
Whether the field is required. Defaults to False.
​
default
any
Default value for the field, provided through a DataMap.
​
min_time
any
Minimum allowed datetime or time value.
​
max_time
any
Maximum allowed datetime or time value.
​
inputType
UserFieldKind
Type of field, either DateTime or Time. Defaults to DateTime.
datetime_range_input_field

Creates a datetime or time range input field with start and end pickers.
​
name
stringrequired
Internal name of the field.
​
label
string
Display label for the field.
​
required
bool
Whether the field is required. Defaults to False.
​
start_date_label
string
Label for the start value.
​
end_date_label
string
Label for the end value.
​
default_start
any
Default start value, provided through a DataMap.
​
default_end
any
Default end value, provided through a DataMap.
​
min_time
any
Minimum allowed value for the range.
​
max_time
any
Maximum allowed value for the range.
number_input_field

Creates a number input field.
Parameters:
​
name
stringrequired
The internal name of the field.
​
label
string
Display label for the field.
​
required
bool
Whether the field is required. Defaults to False.
​
is_integer
bool
Whether the field accepts only integers. If False, accepts decimal numbers. Defaults to True.
​
help_text
string
Help text for the field.
​
default
any
Default value for the field, passed as DataMap.
​
minimum
any
Minimum allowed value, passed as DataMap.
​
maximum
any
Maximum allowed value, passed as DataMap.
file_upload_field

Creates a file upload field.
Parameters:
​
name
stringrequired
The internal name of the field.
​
label
string
Display label for the field.
​
instructions
string
Instructions for the file upload.
​
required
bool
Whether the field is required. Defaults to False.
​
allow_multiple_files
bool
Whether multiple files can be uploaded. Defaults to False.
​
file_max_size
int
Maximum file size in MB. Defaults to 10.
​
supported_file_types
List[string]
List of supported file extensions, for example pdf and docx.
​
min_num_files
Any
Minimum number of files. Valid only when allow_multiple_files=True.
​
max_num_files
Any
Maximum number of files. Valid only when allow_multiple_files=True.
message_output_field

Creates a message output field to display static text.
Parameters:
​
name
stringrequired
The internal name of the field.
​
label
string
Display label for the field.
​
message
string
The message text to display.
field_output_field

Creates a field output to display dynamic values.
Parameters:
​
name
stringrequired
The internal name of the field.
​
label
string
Display label for the field.
​
value
any
The value to display, passed as DataMap.
list_output_field

Creates a list output field to display tabular data.
Parameters:
​
name
stringrequired
The internal name of the field.
​
label
string
Display label for the field.
​
choices
any
The list of items to display, passed in a DataMap.
​
columns
dict[string, str]
Mapping of source property names to table column labels. Only those columns appear if present.
list_input_field

Creates a list input field to display tabular data.
Parameters:
​
name
stringrequired
The internal name of the field.
​
label
string
Display label for the field.
​
isRowAddable
bool
Whether the user can add rows.
​
isRowDeletable
bool
Whether the user can delete rows.
​
default
any
The list of items to display, passed in a DataMap.
​
columns
dict[string, str]
Mapping of source property names to table column labels. Only those columns appear if present.
file_download_field

Creates a file download field.
Parameters:
​
name
stringrequired
The internal name of the field.
​
label
string
Display label for the field.
​
value
any
The file to download, passed as DataMap.
single_choice_input_field

Creates a single-choice input field. Display options as a dropdown or as radio buttons.
Parameters:
​
name
stringrequired
The internal name of the field.
​
label
string
Display label for the field.
​
required
bool
Whether the field is required. Defaults to False.
​
choices
any
The list of available choices, passed as DataMap.
​
show_as_dropdown
bool
Whether to display options as a dropdown. If False, display as radio buttons. Defaults to True.
​
dropdown_item_column
string
Column name used for display text in dropdown.
​
placeholder_text
string
Placeholder text for the dropdown.
​
default
any
Default selected value, passed as DataMap.
​
columns
dict[string, str]
Mapping of source property names to display labels for complex choice objects.
multi_choice_input_field

Creates a multi-choice input field. Display options as a multi-select dropdown or as checkboxes.
Parameters:
​
name
stringrequired
The internal name of the field.
​
label
string
Display label for the field.
​
required
bool
Whether the field is required. Defaults to False.
​
choices
any
The list of available choices, passed as DataMap.
​
show_as_dropdown
bool
Whether the field shows as a dropdown. If False, the field shows as checkboxes. Defaults to True.
​
dropdown_item_column
string
Column name for the display text in a dropdown.
​
placeholder_text
string
Placeholder text for the dropdown.
​
default
any
Default selected values, provided as a DataMap.
​
columns
dict[string, str]
Mapping of source property names to display labels for complex choice objects.
​
minItems
any
Minimum number of items the user must select.
​
maxItems
any
Maximum number of items the user can select.
user_input_field

Creates a user selection field in the form.
Parameters:
​
name
stringrequired
Internal name of the field.
​
label
string
Display label for the field.
​
required
bool
Whether the field is required. Defaults to False.
​
multiple_users
bool
Whether the user can select more than one person. Defaults to False.
​
min_num_users
any
Minimum number of users to select. Applies only when multiple_users=True. Accepts an integer or a DataMap for dynamic configuration through expressions.
​
max_num_users
any
Maximum number of users to select. Applies only when multiple_users=True. Accepts an integer or a DataMap for dynamic configuration through expressions.
Here is an example that shows how to use form():
Python
from typing import List
from pydantic import BaseModel, Field
from ibm_watsonx_orchestrate.flow_builder.flows import (
    Flow, flow, UserNode, START, END
)
from ibm_watsonx_orchestrate.flow_builder.types import Assignment, UserFieldKind
from ibm_watsonx_orchestrate.flow_builder.data_map import DataMap

class Name(BaseModel):
    """
    This datatype represents a person's name.

    Attributes:
        name (str): The person's first name.
    """
    first_name: str = Field(default="John", description="First name")
    last_name: str = Field(default="Doe", description="Last name")

class Book(BaseModel):
    """
    This datatype represents a book.

    Attributes:
        title (str): The book's title.
        author (str): The book's author.
    """
    title: str = Field(default="Shaken", description="Book title")
    author: str = Field(default="John Grisham", description="Author")

class StringListNames(BaseModel):
    listOfNames: List[Name] = Field(
        default=[{"John", "Doe"}, {"Jane", "Doe"}, {"Jean", "Doe"}],
        description="A list of Name objects with first and last names."
    )

class MyDate(BaseModel):
    """
    This datatype represents date information.

    Attributes:
        dateStart (str): The start date.
        dateEnd (str): The end date.
        dateEvent (str): The event date.
    """
    dateStart: str = Field(default="2023-01-01", description="Start date")
    dateEnd: str = Field(default="2023-12-31", description="End date")
    dateEvent: str = Field(default="2023-06-15", description="Event date")

class FlowInput(BaseModel):
    salutations: List[str] = Field(
        default=["Mr", "Mrs"],
        description="A list of string salutations."
    )
    listOfLanguages: List[str] = Field(
        default=["java", "python", "typescript"],
        description="A list of languages."
    )
    salary_expectation: int = Field(
        default=200000,
        description="Expected salary as an integer number."
    )

    friends: StringListNames = Field(
        default=StringListNames(
            listOfNames=[
                Name(first_name="John", last_name="Doe"),
                Name(first_name="Jane", last_name="Doe"),
                Name(first_name="Jean", last_name="Doe")
            ]
        ),
        description="A list of friends with their names."
    )
    books: List[Book] = Field(
        default=[Book()],
        description="A list of books."
    )

    event_date: MyDate = Field(
        default=MyDate(),
        description="The event date"
    ),

    listOfFruits: List[str] = Field(
        default=["apple", "oranges", "bananas"],
        description="A list of fruits."
    )

    listOfPreferredFruits: List[str] = Field(
        default=["apple", "oranges"],
        description="A list of preferred fruits."
    )

@flow(
    name ="user_flow_application_form",
    display_name="Application form",
    description="Creates a sample application form.",
    input_schema=FlowInput,
)

def build_user_form(aflow: Flow = None) -> Flow:

    user_flow = aflow.userflow()
    user_flow.spec.display_name= "Application"

    # Create form with default submit button and visible cancel button
    user_node_with_form = user_flow.form(
        name="ApplicationForm",
        display_name="Application",
        cancel_button_label="Cancel"
    )
    
    data_map = DataMap()
    data_map.add(Assignment(target_variable="self.input.choices", value_expression="flow.input.salutations"))
 
    #Single-choice: Salutation
    user_node_with_form.single_choice_input_field(name="salutation", label="Salutation", required=True, choices=data_map, 
                                                  show_as_dropdown=True, placeholder_text="Please enter your title")
   
    #Boolean: Married
    user_node_with_form.boolean_input_field(name="married", label="Married", single_checkbox = True, true_label="Married", false_label="Not married")
    
    #Text: Last Name
    user_node_with_form.text_input_field(name="lastName", label="Last name", required=True, placeholder_text="Enter your name here", help_text="Enter name", 
        regex="^[a-zA-Z0-9\s]+$", regex_error_message="No special characters allowed")
    
    #Number: Age
    user_node_with_form.number_input_field(name="age", label="Age", required=True, help_text="Enter your age")

    data_map_salary = DataMap()
    data_map_salary.add(Assignment(target_variable="self.input.default", value_expression="flow.input.salary_expectation"))
    
    #Number: Desired Salary
    user_node_with_form.number_input_field(name="salary", label="Desired salary", is_integer=False, help_text="Your dream salary is here", default=data_map_salary)
  
    data_map_desired_salary = DataMap()
    data_map_desired_salary.add(Assignment(target_variable="self.input.value", value_expression="flow.input.salary_expectation"))

     #Field: Projected salary
    user_node_with_form.field_output_field(name="acknowledge", label="Projected salary", value = data_map_desired_salary)

    #FileUpload
    data_map_min_files = DataMap()
    data_map_min_files.add(Assignment(target_variable="self.input.min_num_files", value_expression="1"))

    data_map_max_files = DataMap()
    data_map_max_files.add(Assignment(target_variable="self.input.max_num_files", value_expression="2"))

    user_node_with_form.file_upload_field(name="credentials", label="Upload credentials", allow_multiple_files=True, file_max_size=256,
                                          min_num_files=data_map_min_files, max_num_files=data_map_max_files)

    #Date: End Date
    data_map_default_date = DataMap()
    data_map_default_date.add(Assignment(target_variable="self.input.default",value_expression="flow.input.event_date.dateEnd"))

    data_map_min_date = DataMap()
    data_map_min_date.add(Assignment(target_variable="self.input.min_date",value_expression="\"2026-01-05\""))
    
    data_map_max_date = DataMap()
    data_map_max_date.add(Assignment(target_variable="self.input.max_date",value_expression="\"2026-01-12\""))

    user_node_with_form.date_input_field(name="endDate", label="End Date", required=True, default=data_map_default_date, 
                                        min_date=data_map_min_date, max_date=data_map_max_date)
  
    data_map_list_source = DataMap()
    data_map_list_source.add(Assignment(target_variable="self.input.choices", value_expression="flow.input.listOfLanguages"))
    
    #Output List: Qualification
    user_node_with_form.list_output_field(name="strength", label="Qualification", choices=data_map_list_source)

    #Output list: Friends table
    data_map_list_friends = DataMap()
    data_map_list_friends.add(Assignment(target_variable="self.input.choices", value_expression="flow.input.friends.listOfNames"))
    user_node_with_form.list_output_field(name="friends", label="Friends", choices=data_map_list_friends, columns={"first_name": "First", "last_name": "Last"})

    #Mult-chocice: List of fruits dowpdown primitives
    data_map_multi_choice = DataMap()
    data_map_multi_choice.add(Assignment(target_variable="self.input.choices", value_expression="flow.input.listOfFruits"))

    data_map_multi_choice_default = DataMap()
    data_map_multi_choice_default.add(Assignment(target_variable="self.input.default", value_expression="flow.input.listOfPreferredFruits"))

    user_node_with_form.multi_choice_input_field(name="multi-choice", label="List of Fruits", required=False, choices=data_map_multi_choice, 
                                                  show_as_dropdown=True, placeholder_text="Please enter your choice", default=data_map_multi_choice_default,
                                                  minItems=1, maxItems=2)
    
    #Mult-chocice: Books dowpdown complex
    data_map_list_books = DataMap()
    data_map_list_books.add(Assignment(target_variable="self.input.choices", value_expression="flow.input.books"))
    user_node_with_form.multi_choice_input_field(name="multi-choice_as_dropdown_1", label="List of Books", required=False, choices=data_map_list_books, 
                                                  show_as_dropdown=True, dropdown_item_column="title", placeholder_text="Please enter your choice")
 
    #Mult-chocice: List of names table
    data_map_list_friends_choice2 = DataMap()
    data_map_list_friends_choice2.add(Assignment(target_variable="self.input.choices", value_expression="flow.input.friends.listOfNames"))

    user_node_with_form.multi_choice_input_field(name="multi-choice_as_table", label="List of Names", required=False, choices=data_map_list_friends_choice2, 
                                                  show_as_dropdown=False, placeholder_text="Please enter your choice", columns={"first_name": "First", "last_name": "Last"} )

    #Input list: Books editable table
    data_map_list_books = DataMap()
    data_map_list_books.add(Assignment(target_variable="self.input.default", value_expression="flow.input.books"))

    user_node_with_form.list_input_field(name="books", label="Books", default=data_map_list_books, columns={"title": "Book Title", "author": "Book Author"})
    #Input list: Fuits editable table
    data_map_list_fruits = DataMap()
    data_map_list_fruits.add(Assignment(target_variable="self.input.default", value_expression="flow.input.listOfFruits"))

    user_node_with_form.list_input_field(name="Fruits", label="Preferred fruits", default=data_map_list_fruits)

    # User field: Select multiple approvers (min 1, max 5)
    data_map_min_users = DataMap()
    data_map_min_users.add(Assignment(target_variable="self.input.min_num_users", value_expression="1"))
    data_map_max_users = DataMap()
    data_map_max_users.add(Assignment(target_variable="self.input.max_num_users", value_expression="5"))
    user_node_with_form.user_input_field(name="approvers", label="Select Approvers", required=True, multiple_users=True,
                                         min_num_users=data_map_min_users, max_num_users=data_map_max_users)

    # User field: Select a single assignee (min/max not applicable for single user)
    user_node_with_form.user_input_field(name="assignee", label="Select Assignee", required=True, multiple_users=False)
    #Output Message: Successful submission
    user_node_with_form.message_output_field(name="success", label="Successful submission", message="Application successfully completed.")
 
    # Add additional buttons using the new API
    save_draft_btn = user_flow.add_button("Save Draft")
    review_btn = user_flow.add_button("Submit for Review")
    
    # Create different nodes for each button action
    submit_node = user_flow.script(
        name="process_submit",
        script='print("Processing full submission...")'
    )
    
    save_draft_node = user_flow.script(
        name="process_save_draft",
        script='print("Saving as draft...")'
    )
    
    review_node = user_flow.script(
        name="process_review",
        script='print("Submitting for review...")'
    )

    # Connect nodes using the new edge API
    user_flow.edge(START, user_node_with_form)
    
    # Connect default "Submit" button using button_label parameter
    user_flow.edge(user_node_with_form, submit_node, button_label="Submit")
    user_flow.edge(submit_node, END)
    
    # Connect "Save Draft" button using Button object
    user_flow.edge(save_draft_btn, save_draft_node)
    user_flow.edge(save_draft_node, END)
    
    # Connect "Submit for Review" button using Button object
    user_flow.edge(review_btn, review_node)
    user_flow.edge(review_node, END)

    # Script to initialize friends list
    init_script = """
flow.input.friends.listOfNames = [
    {"first_name": "John", "last_name": "Doe"},
    {"first_name": "Alice", "last_name": "Smith"},
    {"first_name": "Bob", "last_name": "Johnson"}
]
flow.input.books=[
    { "title": "Shaken", "author":"John Grisham"},
    {"title": "The Client", "author":"John Grisham"},
]
flow.input.listOfFruits = ["apple", "oranges", "bananas"]
"""
    init_data = aflow.script(name="init_data", script=init_script)
    
    # add the user flow to the flow sequence to create the flow edges
    aflow.sequence(START, init_data, user_flow, END)
  
    return aflow
Collapse
​
Dynamic form input
Form fields can change based on user actions. You define the dependencies between the user’s interactions and your tools to control dynamic behavior in the form. This includes progressive selection, showing or hiding widgets, and updating widget labels.
Use the following methods to configure dynamic forms:
visibility_behaviour_field

Adds a visibility behaviour that shows or hides fields based on conditions.
​
name
stringrequired
Unique identifier for this behaviour.
​
on_change_to_field
stringrequired
Field that triggers evaluation of visibility rules when its value changes.
​
rules
list[dict]required
List of visibility rules. Each rule specifies a condition and an impacted_field that changes visibility.
​
display_name
string
Display name for this behaviour.
label_behaviour_field

Adds a label-changing behaviour that updates field labels based on conditions.
​
name
stringrequired
Unique identifier for this behaviour.
​
on_change_to_field
stringrequired
Field that triggers label evaluation when its value changes.
​
rules
list[dict]required
List of label rules. Each rule includes a condition and an impacted_field whose label changes.
​
display_name
string
Display name for this behaviour.
value_source_behaviour_field

Adds a value-source behaviour that populates a field using results from a tool. Supports a simplified API or a manual API.
​
name
stringrequired
Unique identifier for this behaviour.
​
on_change_to_field
stringrequired
Field that triggers execution of the tool when its value changes.
​
impacted_field
stringrequired
Field that receives values returned by the tool.
​
Simplified API parameters
​
tool_name
string
Name of the tool to call, for example get_states_or_provinces.
​
tool_id
string
UUID of the tool.
​
field_mappings
dict[string, string]
Mapping of tool parameters to field expressions. For example country maps to parent.field.country.
​
client
any
Client instance that enables automatic retrieval of the tool schema.
​
Manual API parameters
​
tool
string
Tool identifier in name colon UUID format.
​
tool_input_schema
dict
Schema that describes the expected inputs for the tool.
​
tool_input_map
dict
Mapping of input parameters to values or expressions used by the tool.
​
Common optional parameters
​
display_name
string
Display name for this behaviour.
Here is an example that shows how to configure dynamic forms:
Python
from typing import List
from pydantic import BaseModel, Field
from ibm_watsonx_orchestrate.flow_builder.flows import (
    Flow, flow, UserNode, START, END
)
from ibm_watsonx_orchestrate.flow_builder.types import Assignment
from ibm_watsonx_orchestrate.flow_builder.data_map import DataMap
from ibm_watsonx_orchestrate.flow_builder.utils import RuleBuilder


class FlowInput(BaseModel):
    """Input schema for the flow."""
    countries: List[str] = Field(
        default=["USA", "Canada"],
        description="A list of available countries."
    )
    usa_states: List[str] = Field(
        default=["California", "Texas", "New York", "Florida"],
        description="A list of US states."
    )
    canada_provinces: List[str] = Field(
        default=["Ontario", "Quebec", "British Columbia", "Alberta"],
        description="A list of Canadian provinces."
    )
    default_country: str = Field(
        default="USA",
        description="Default country selection."
    )
    default_region: str = Field(
        default="California",
        description="Default region selection."
    )


@flow(
    name="user_activity_with_dynamic_forms_full",
    display_name="Dynamic Form - A simple example",
    description="Demonstrates dynamic form behaviours",
    input_schema=FlowInput,
)
def build_dynamic_form_full(aflow: Flow = None) -> Flow:
    
    # Create user flow
    user_flow = aflow.userflow()
    user_flow.spec.display_name = "Example dynamic form"
    
    # Create form node
    form_node = user_flow.form(
        name="dynamic_form", 
        display_name="Dynamic form example",
        cancel_button_label="Cancel")
    
    #FIELD 1: Country
    country_choices = DataMap()
    country_choices.add(Assignment(
        target_variable="self.input.choices",
        value_expression="flow.input.countries"
    ))
    
    country_default = DataMap()
    country_default.add(Assignment(
        target_variable="self.input.default",
        value_expression="flow.input.default_country"
    ))
    
    form_node.single_choice_input_field(
        name="country",
        label="Country",
        required=False,
        choices=country_choices,
        default=country_default,
        show_as_dropdown=True,
        placeholder_text="Select an option"
    )
    
    #FIELD 2: Visibility Behaviour
    # Controls city and url fields
    form_node.visibility_behaviour_field(
        name="visibility_behaviour",
        on_change_to_field="country",
        rules=[
            RuleBuilder.visibility_rule(
                field_name="country",
                field_value="USA",
                impacted_field="city",
                visible_when_true=True,
                operator="equals"
            ),
            RuleBuilder.visibility_rule(
                field_name="country",
                field_value="Canada",
                impacted_field="url",
                visible_when_true=True,
                operator="equals"
            )
        ],
        display_name="Visibility rule"
    )
    
    # FIELD 3: Label Behaviour
    # Controls code, region, and documents field labels
    form_node.label_behaviour_field(
        name="label_behaviour",
        on_change_to_field="country",
        rules=[
            RuleBuilder.label_rule(
                field_name="country",
                field_value="USA",
                impacted_field="code",
                label_when_true="Zip code",
                label_when_false="Postal code",
                operator="equals"
            ),
            RuleBuilder.label_rule(
                field_name="country",
                field_value="USA",
                impacted_field="region",
                label_when_true="State",
                label_when_false="Province",
                operator="equals"
            ),
            RuleBuilder.label_rule(
                field_name="country",
                field_value="USA",
                impacted_field="documents",
                label_when_true="US W-2 Form",
                label_when_false="Canadian T4 Form",
                operator="equals"
            )
        ],
        display_name="Label rule"
    )
    
    # FIELD 4: Value-Source Behaviour
    # Populates region field options from tool
    form_node.value_source_behaviour_field(
        name="value_source_behaviour",
        on_change_to_field="country",
        impacted_field="region",
        tool_name="get_states_or_provinces",
        tool_id="9f0ecb53-dbd9-4e41-be46-29c8d47d6df8",
        field_mappings={
            "country": "parent.field.country"
        },
        display_name="ProgSelect"
    )
    
    # FIELD 5: Region
    region_choices = DataMap()
    region_choices.add(Assignment(
        target_variable="self.input.choices",
        value_expression='',
        has_no_value=True
    ))
    region_choices.add(Assignment(
        target_variable="self.input.display_text",
        value_expression='',
        has_no_value=True
    ))
    region_choices.add(Assignment(
        target_variable="self.input.display_items",
        value_expression='',
        has_no_value=True
    ))
    
    form_node.single_choice_input_field(
        name="region",
        label="Region",
        required=False,
        choices=region_choices,
        show_as_dropdown=True,
        placeholder_text="Select an option"
    )
    
    # FIELD 6: Code
    form_node.text_input_field(
        name="code",
        label="Code",
        required=False
    )
    
    # FIELD 7: City
    form_node.text_input_field(
        name="city",
        label="City",
        required=False
    )
    
    # FIELD 8: Documents
    form_node.file_upload_field(
        name="documents",
        label="Documents"
    )
    
    # FIELD 9: URL
    form_node.text_input_field(
        name="url",
        label="URL",
        required=False
    )
    
    # Add edges
    user_flow.edge(START, form_node)
    user_flow.edge(form_node, END)
    
    # Script to initialize input data
    init_script = """
# Initialize countries list
flow.input.countries = ["USA", "Canada"]

# Initialize US states
flow.input.usa_states = ["California", "Texas", "New York", "Florida", "Illinois", "Pennsylvania"]

# Initialize Canadian provinces
flow.input.canada_provinces = ["Ontario", "Quebec", "British Columbia", "Alberta", "Manitoba", "Saskatchewan"]

# Set default selections
flow.input.default_country = "USA"
flow.input.default_region = "California"
"""
    init_data = aflow.script(name="init_data", script=init_script)
    
    # Add user flow to main flow with initialization
    aflow.sequence(START, init_data, user_flow, END)
    
    return aflow


---

Workflow nodes
Timer node
Use a timer node to set a delay between actions in your agentic workflow.
To configure a timer node, call the timer() method in your agentic workflow. This method accepts the following input arguments:
​
name
stringrequired
Unique identifier for the node.
​
delay
integerrequired
Timer delay in milliseconds.
​
display_name
string
Display name for the node.
​
description
string
Description of the node.
​
input_map
DataMap
Define input mappings using a structured collection of Assignment objects.
The following example shows how to add a timer node to a loop:
Python
from pydantic import BaseModel, Field
from ibm_watsonx_orchestrate.flow_builder.flows import END, Flow, flow, START
from .get_facts_about_numbers import get_facts_about_numbers
from .get_request_status import get_request_status

class InputtedNumber(BaseModel):
    number: int = Field(description="Inputted number from user")

class Attempt(BaseModel):
    atmp: int = Field(description="Represent each attemp to check if the request is finish", default=0)

class FlowOutput(BaseModel):
    info: str = Field(description="Fact about a number")

@flow(
    name="get_number_random_fact_flow",
    input_schema=InputtedNumber,
    output_schema=FlowOutput,
    description="A flow to get a random fact about a number"
)
def get_number_random_fact_flow(aflow: Flow) -> Flow:
    get_facts_about_numbers_node = aflow.tool(
        get_facts_about_numbers,
        input_schema=InputtedNumber,
        output_schema=FlowOutput
    )

    while_loop: Flow = aflow.loop(
        evaluator="not parent.get_request_status.input.attempt.atmp or parent.get_request_status.input.attempt.atmp < 5",
        input_schema=Attempt,
        output_schema=FlowOutput
    )

    timer_node = while_loop.timer(
        name="wait_1_sec",
        delay=1000,
        description="Wait for 1 second before polling again"
    )

    get_request_status_node = while_loop.tool(get_request_status)
    while_loop.sequence(START, get_request_status_node, timer_node, END)
    aflow.sequence(START, get_facts_about_numbers_node, while_loop, END)

    return aflow


---

Document processing
Document field extractor node (Public preview)
Use the document field extractor node to extract specific fields from your documents.
​
Pre-requisites
Run the following command to enable watsonx Orchestrate Developer Edition to process documents:
BASH
orchestrate server start -e <.env file path> -d
Note: You need to configure a minimum allocation of 20GB RAM to your Docker engine during installation of watsonx Orchestrate Developer edition to support document processing features.
​
Limitations
Text extractors have the following limits and restrictions:
Area	Description
Maximum file size	10 MB (except for Microsoft Excel files). Note: The maximum file size for Microsoft Excel files is 0.1 MB.
Maximum number of uploaded files	5 files
Accepted file types	.doc, .docx, .jpe, .jpeg .jpg, .pdf, .png, .ppt, .pptx, .tif, .tiff, and .xlsx
Maximum number of pages	600 pages
Maximum number of images	No limit
Maximum number of images per page	No limit
Note: To run the document field extractor, you must define the WATSONX_SPACE_ID, WATSONX_APIKEY, and WATSONX_PROJECT_ID credentials in your .env file. For more information on configuring the .env file, see Installing the watsonx Orchestrate Developer Edition.
​
Configuring document extractor node in agentic workflows
Define the fields to extract. Create a class that defines the fields you want to extract. Each field must follow this structure:
Python
field: DocExtConfigField = Field(name="Field name", default=DocExtConfigField(name="Field name", field_name="field_name"))
Class example:
Python
class Fields(BaseModel):
    """
    Configuration schema for document extraction fields.
    
    Defines the fields to be extracted from contract documents, including
    their names, types, and descriptions. Each field is configured with
    a DocExtConfigField that specifies how the document extractor should
    identify and extract the information.
    
    In this example, we define a number of custom fields for a Contract or 
    Agreement document:
        buyer: The purchasing party in the contract
        seller: The selling party in the contract
        agreement_date: The date when the agreement was signed (date type)
        agreement_number: Unique identifier for the contract
        contract_type: Classification of the contract 
    """
    buyer: DocExtConfigField = Field(
        name="Buyer",
        default=DocExtConfigField(
            name="Buyer",
            field_name="buyer"
        )
    )
See all 24 lines
Configure the document extract node
In your agentic workflow, include a call to the docext() method to extract an field from a document. This method accepts the following input arguments:
​
name
stringrequired
Unique identifier for the node.
​
llm
string
The LLM used for field extraction. The default value is watsonx/meta-llama/llama-3-2-90b-vision-instruct.
​
display_name
string
Display name for the node.
​
fields
objectrequired
The fields you want to extract.
​
description
string
Description of the node.
​
input_map
DataMap
Define input mappings using a structured collection of Assignment objects.
​
enable_hw
bool
Enable the handwritten feature by setting this to true.
​
min_confidence
float
The minimum acceptable confidence for an extracted field value.
​
review_fields
List[string]
The fields that require user review.
​
enable_review
bool
Enables or disables the human-in-the-loop feature. Set to True to activate it and False to deactivate. The default value is False.
​
field_extraction_method
string
Selects the Document Extractor runtime. The default value is classic, which uses the Unstructured Document Extractor. To use the Structured Document Extractor, set the value to layout. For more information, see Choosing a tool option for extracting fields from documents.
​
page_range
PageRange
Limits extraction to a specific range of pages. Use this parameter only when field_extraction_method is set to layout. Using page_range with the classic method raises an error.
Show PageRange fields

Use PageRange(start=1, end=5) to extract fields from pages 1 through 5.
​
language
LanguageCode
The ISO-639 language code that specifies the document’s language for OCR processing. Use the LanguageCode enum to specify supported languages (e.g., LanguageCode.fr for French, LanguageCode.ja for Japanese). This parameter is essential for scanned PDFs and images containing non-Latin scripts, as it ensures the correct OCR engine is used to recognize characters accurately. Programmatic documents (PDF, .docx, .pptx) do not require this setting.
Note:
The min_confidence and review_fields settings control the human-in-the-loop feature. This feature only works when you run the Flow from a chat session. If a field is extracted with confidence lower than min_confidence, and its name appears in review_fields, the agent opens a review window in the chat. You can then review and confirm the extracted values.
The docext node accepts input of type DocumentProcessingCommonInput, from the module ibm_watsonx_orchestrate.flow_builder.types.
You can also supply page_range on DocumentProcessingCommonInput instead of setting it at design time on docext(). The same layout-only constraint applies: page_range has no effect unless you set field_extraction_method='layout' on the node.
Example use of the docext node in an agentic workflow:
Python
from pydantic import BaseModel, Field
from ibm_watsonx_orchestrate.flow_builder.flows import (
    Flow, flow, START, END
)
from ibm_watsonx_orchestrate.flow_builder.types import DocExtConfigField, DocumentProcessingCommonInput


class Fields(BaseModel):
    """
    Configuration schema for document extraction fields.
    
    Defines the fields to be extracted from contract documents, including
    their names, types, and descriptions. Each field is configured with
    a DocExtConfigField that specifies how the document extractor should
    identify and extract the information.
    
    In this example, we define a number of custom fields for a Contract or 
    Agreement document:
        buyer: The purchasing party in the contract
        seller: The selling party in the contract
        agreement_date: The date when the agreement was signed (date type)
        agreement_number: Unique identifier for the contract
        contract_type: Classification of the contract 
    """
    buyer: DocExtConfigField = Field(
        name="Buyer",
        default=DocExtConfigField(
            name="Buyer",
            field_name="buyer"
        )
    )
    
    seller: DocExtConfigField = Field(
        name="Seller",
        default=DocExtConfigField(
            name="Seller",
            field_name="seller"
        )
    )
    
    agreement_date: DocExtConfigField = Field(
        name="Agreement date",
        default=DocExtConfigField(
            name="Agreement Date",
            field_name="agreement_date",
            type="date"
        )
    )
    
    agreement_number: DocExtConfigField = Field(
        name="Agreement number",
        default=DocExtConfigField(
            name="Agreement Number",
            field_name="agreement_number",
            description="The identifier of this contract."
        )
    )
    
    contract_type: DocExtConfigField = Field(
        name="Contract type",
        default=DocExtConfigField(
            name="Contract Type",
            field_name="contract_type",
            type="string",
            description="The type of contract between the buyer and the seller."
        )
    )


@flow(
    name ="custom_flow_docext_example",
    display_name="custom_flow_docext_example",
    description="Extraction of custom fields from a document, specified by the user.",
    input_schema=DocumentProcessingCommonInput
)
def build_docext_flow(aflow: Flow = None) -> Flow:
    # aflow.docext returns 2 objects: the document extractor node and the schema of the extracted values.
    # In this example, doc_ext_node is the node and is added to the flow.
    # _ExtractedValues is the output schema of doc_ext_node and can be used as the input schema of nodes downstream in the flow.

    doc_ext_node, _ExtractedValues = aflow.docext(
        name="contract_extractor",
        display_name="Extract fields from a contract",
        description="Extracts fields from an input contract file",
        llm="watsonx/mistralai/mistral-small-3-1-24b-instruct-2503",
        fields=Fields()
    )

    aflow.sequence(START, doc_ext_node, END)
    return aflow
Collapse
​
Using the language parameter
For scanned PDFs and images containing non-Latin scripts, specify the document’s language to ensure accurate OCR processing:
Python
from pydantic import BaseModel, Field
from ibm_watsonx_orchestrate.flow_builder.flows import (
    Flow, flow, START, END
)
from ibm_watsonx_orchestrate.flow_builder.types import (
    DocExtConfigField, DocumentProcessingCommonInput, LanguageCode
)


class Fields(BaseModel):
    """
    Configuration schema for document extraction fields.
    
    Defines the fields to be extracted from contract documents, including
    their names, types, and descriptions.
    """
    buyer: DocExtConfigField = Field(
        default=DocExtConfigField(
            name="Buyer",
            field_name="buyer"
        )
    )
    
    seller: DocExtConfigField = Field(
        default=DocExtConfigField(
            name="Seller",
            field_name="seller"
        )
    )
    
    agreement_date: DocExtConfigField = Field(
        default=DocExtConfigField(
            name="Agreement Date",
            field_name="agreement_date",
            type="date"
        )
    )
    
    agreement_number: DocExtConfigField = Field(
        default=DocExtConfigField(
            name="Agreement Number",
            field_name="agreement_number",
            description="The identifier of this contract."
        )
    )
    
    contract_type: DocExtConfigField = Field(
        default=DocExtConfigField(
            name="Contract Type",
            field_name="contract_type",
            type="string",
            description="The type of contract between the buyer and the seller."
        )
    )


@flow(
    name="document_extractor_with_language",
    display_name="Document Extractor with Language",
    description=(
        "Extracts custom fields from a document using a specified OCR language. "
        "Setting the language ensures the correct OCR engine is used for scanned PDFs "
        "and images, improving field extraction accuracy for non-Latin script documents."
    ),
    input_schema=DocumentProcessingCommonInput
)
def build_docext_language_flow(aflow: Flow = None) -> Flow:
    """
    Build a document extraction flow with language-aware OCR support.
    
    This example demonstrates how to use the language parameter to select the
    correct OCR engine before field extraction.
    
    Use the LanguageCode enum to specify the ISO-639 language code that matches
    the document's language.
    """
    doc_ext_node, _ExtractedValues = aflow.docext(
        name="contract_extractor_language",
        display_name="Extract Fields (Japanese)",
        description=(
            "Extracts fields from a Japanese-language scanned contract document. "
            "Uses the Japanese OCR engine to correctly recognise non-Latin characters."
        ),
        llm="watsonx/meta-llama/llama-4-maverick-17b-128e-instruct-fp8",
        fields=Fields(),
        language=LanguageCode.ja,
    )
    
    aflow.sequence(START, doc_ext_node, END)
    return aflow
See all 90 lines
​
Using the language parameter with structured document extractor
When using the layout field extraction method, you can also specify the language parameter:
Python
@flow(
    name="document_extractor_structured_with_language",
    display_name="Structured Document Extractor with Language",
    description=(
        "Extracts custom fields from a document using the structured extractor "
        "with a specified OCR language for improved accuracy."
    ),
    input_schema=DocumentProcessingCommonInput
)
def build_docext_structured_language_flow(aflow: Flow = None) -> Flow:
    """
    Build a structured document extraction flow with language-aware OCR support.
    """
    doc_ext_node, _ExtractedValues = aflow.docext(
        name="contract_extractor_structured_language",
        display_name="Extract Fields (German)",
        description=(
            "Extracts fields from a German-language scanned contract document. "
            "Uses the German OCR engine to correctly recognise Latin-script characters."
        ),
        llm="watsonx/mistralai/mistral-small-3-1-24b-instruct-2503",
        field_extraction_method="layout",
        fields=Fields(),
        language=LanguageCode.de,
    )
    
    aflow.sequence(START, doc_ext_node, END)
    return aflow


---

Document processing
Document classifier node (Public preview)
Use the document classifier node to classify your documents.
​
Pre-requisites
Run the following command to enable watsonx Orchestrate Developer Edition to process documents:
BASH
orchestrate server start -e <.env file path> -d
Note: You need to configure a minimum allocation of 20GB RAM to your Docker engine during installation of watsonx Orchestrate Developer edition to support document processing features.
Note: To run the document classifier, you must define the WO_INSTANCE, WO_API_KEY, and AUTHORIZATION_URL credentials in your .env file. For more information on configuring the .env file, see Installing the watsonx Orchestrate Developer Edition.
​
Configuring document extractor node in agentic workflows
Define document classes. Create a class that defines the document classes to classify. Each document class must follow this structure:
Python
class CustomClasses(BaseModel):
"""
Configuration schema for document classification classes.

Defines the document types/classes that the classifier can identify.
Each class is configured with a DocClassifierClass that specifies the
class name used for categorizing input documents. The classifier uses
an LLM to analyze documents and assign them to one of these classes.

Example custom classes:
    invoice: Configuration for identifying invoice documents
    contract: Configuration for identifying contract documents
    tax_form: Configuration for identifying tax form documents
    bill_of_lading: Configuration for identifying bill of lading documents
"""
invoice: DocClassifierClass = Field(default=DocClassifierClass(class_name="Invoice"))
contract: DocClassifierClass = Field(default=DocClassifierClass(class_name="Contract"))
tax_form: DocClassifierClass = Field(default=DocClassifierClass(class_name="TaxForm"))
bill_of_lading: DocClassifierClass = Field(default=DocClassifierClass(class_name="BillOfLading"))
Configure the document classifier node
Include a call to the docclassifier() method in your agentic workflow to classify the document. This method accepts the following input arguments:
​
name
stringrequired
Unique identifier for the node.
​
llm
stringrequired
The LLM used for document classification. The default value is watsonx/meta-llama/llama-4-maverick-17b-128e-instruct-fp8.
​
display_name
string
Display name for the node.
​
classes
objectrequired
The document classification classes.
​
description
string
Description of the node.
​
min_confidence
float
Minimum confidence threshold for classification.
​
input_map
DataMap
Define input mappings using a structured collection of Assignment objects.
​
enable_hw
bool
Enable the handwritten feature by setting this to true.
​
enable_review
bool
Enables or disables the human-in-the-loop feature. Set to True to activate it and False to deactivate. The default value is False.
​
language
LanguageCode
The ISO-639 language code that specifies the document’s language for OCR processing. Use the LanguageCode enum to specify supported languages (e.g., LanguageCode.fr for French, LanguageCode.ja for Japanese). This parameter is essential for scanned PDFs and images containing non-Latin scripts, as it ensures the correct OCR engine is used to recognize characters accurately. Programmatic documents (PDF, .docx, .pptx) do not require this setting.
Note:
The min_confidence setting controls the human-in-the-loop feature. This feature only works when you run the Flow from a chat session. If the document is classified with confidence lower than min_confidence, or as Other, the agent opens a review window in the chat. You can then review and confirm the extracted values.
Example use of the docext node in an agentic workflow:
Python
from pydoc import Doc
from pydantic import BaseModel, Field
from ibm_watsonx_orchestrate.flow_builder.flows import (
    Flow, flow, START, END
)
from ibm_watsonx_orchestrate.flow_builder.types import DocClassifierClass, DocumentProcessingCommonInput, DocumentClassificationResponse


class CustomClasses(BaseModel):
    """
    Configuration schema for document classification classes.
    
    Defines the document types/classes that the classifier can identify.
    Each class is configured with a DocClassifierClass that specifies the
    class name used for categorizing input documents. The classifier uses
    an LLM to analyze documents and assign them to one of these classes.
    
    Example custom classes:
        invoice: Configuration for identifying invoice documents
        contract: Configuration for identifying contract documents
        tax_form: Configuration for identifying tax form documents
        bill_of_lading: Configuration for identifying bill of lading documents
    """
    invoice: DocClassifierClass = Field(default=DocClassifierClass(class_name="Invoice"))
    contract: DocClassifierClass = Field(default=DocClassifierClass(class_name="Contract"))
    tax_form: DocClassifierClass = Field(default=DocClassifierClass(class_name="TaxForm"))
    bill_of_lading: DocClassifierClass = Field(default=DocClassifierClass(class_name="BillOfLading"))


@flow(
    name ="custom_flow_docclassifier_example",
    display_name="custom_flow_docclassifier_example",
    description="Classifies documents into custom classes.",
    input_schema=DocumentProcessingCommonInput
)
def build_docclassifier_flow(aflow: Flow = None) -> Flow:
    # aflow.docclassifier returns a DocClassifierNode object.
    # The output schema of a DocClassifierNode is a DocumentClassifierResponse object.

    doc_classifier_node = aflow.docclassifier(
        name="document_classifier_node",
        display_name="document_classifier_node",
        description="Classifies documents into one custom class.",
        llm="watsonx/meta-llama/llama-4-maverick-17b-128e-instruct-fp8",
        classes=CustomClasses(),
    )

    aflow.sequence(START, doc_classifier_node, END)

    return aflow

See all 51 lines
​
Using the language parameter
For scanned PDFs and images containing non-Latin scripts, specify the document’s language to ensure accurate OCR processing:
Python
from pydantic import BaseModel, Field
from ibm_watsonx_orchestrate.flow_builder.flows import (
    Flow, flow, START, END
)
from ibm_watsonx_orchestrate.flow_builder.types import (
    DocClassifierClass, DocumentProcessingCommonInput, LanguageCode
)


class CustomClasses(BaseModel):
    """
    Configuration schema for document classification classes.
    
    Defines the document types/classes that the classifier can identify.
    Each class is configured with a DocClassifierClass that specifies the
    class name used for categorizing input documents.
    """
    invoice: DocClassifierClass = Field(default=DocClassifierClass(class_name="Invoice"))
    contract: DocClassifierClass = Field(default=DocClassifierClass(class_name="Contract"))
    tax_form: DocClassifierClass = Field(default=DocClassifierClass(class_name="TaxForm"))
    bill_of_lading: DocClassifierClass = Field(default=DocClassifierClass(class_name="BillOfLading"))


@flow(
    name="document_classifier_with_language",
    display_name="Document Classifier with Language",
    description=(
        "Classifies documents into custom classes using a specified OCR language. "
        "Setting the language ensures the correct OCR engine is used for scanned PDFs "
        "and images, improving classification accuracy for non-Latin script documents."
    ),
    input_schema=DocumentProcessingCommonInput
)
def build_docclassifier_flow_with_language(aflow: Flow = None) -> Flow:
    """
    Build a document classifier flow with language-aware OCR support.
    
    This example demonstrates how to use the language parameter to select the
    correct OCR engine before classification.
    
    Use the LanguageCode enum to specify the ISO-639 language code that matches
    the document's language.
    """
    doc_classifier_node = aflow.docclassifier(
        name="document_classifier_language_node",
        display_name="Classify Document (French)",
        description=(
            "Classifies French-language scanned documents or images into custom classes. "
            "Uses the French OCR engine to correctly recognise Latin-script characters."
        ),
        llm="watsonx/meta-llama/llama-4-maverick-17b-128e-instruct-fp8",
        classes=CustomClasses(),
        language=LanguageCode.fr,
    )
    
    aflow.sequence(START, doc_classifier_node, END)
    return aflow
See all 57 lines


---

Document processing
Document text extractor node (Public preview)
Use the document text extractor node to extract the texts from your documents.
​
Pre-requisites
Run the following command to enable watsonx Orchestrate Developer Edition to process documents:
BASH
orchestrate server start -e <.env file path> -d
Note: You need to configure a minimum allocation of 20GB RAM to your Docker engine during installation of watsonx Orchestrate Developer edition to support document processing features.
​
Configuring document processing in flows
In your agentic workflow, include a call to the docproc() method to process a document.
​
Supported arguments
​
name
stringrequired
Unique identifier for the node.
​
task
stringrequired
Specifies which information is extracted from the document upon processing; supported values are:
text_extraction: Extracts plain text from documents.
​
display_name
string
Display name for the node.
​
description
string
Description of the node.
​
output_format
DocProcOutputFormat
Controls the output schema of the results. The possible values are:
DocProcOutputFormat.docref (“docref”): This is the default value.
Returns a URL reference to the stored extraction result
Response type: TextExtractionResponse
Best for documents that contain large amount of text or complex structures where the expected output is large.
DocProcOutputFormat.object (“object”):
Returns extraction results as an inline JSON object.
Response type: TextExtractionObjectResponse
Best for small documents or when the output of this node needs to flow into another node.
When using this value, it is highly recommended to map all top-level output fields in TextExtractionObjectResponse into the input of downstream nodes or the flow output.
​
input_map
DataMap
Define input mappings using a structured collection of Assignment objects.
​
document_structure
boolean
Controls whether the output includes additional fields as part of the document assembly. Set to true to include these fields.
​
kvp_schemas
list[DocProcKVPSchema]
The key-value pair schemas used for extraction.
​
enable_hw
boolean
Enable the handwritten feature by setting this to true.
​
kvp_model_name
string
The LLM model used for key-value pair extraction. If no value is provided, the default WDU model is used. The default model is currently watsonx/mistralai/mistral-small-3-1-24b-instruct-2503. The name of the model must match the list of models registered with your watsonx Orchestrate environment. To check the list of models, see List all LLMs.
Compatible models must be able to process images as input and respond in JSON format. Examples include:
watsonx/mistralai/mistral-small-3-1-24b-instruct-2503
watsonx/mistralai/mistral-medium-2505
watsonx/meta-llama/llama-4-maverick-17b-128e-instruct-fp8
​
kvp_force_schema_name
string
The schema name used for KVP extraction. If not set or None, uses the default schema.
​
kvp_enable_text_hints
bool
Enables text hints to assist with KVP extraction.
​
page_range
PageRange
Limits text extraction to a specific range of pages. When set, the node extracts text only from that page range. If not set, the node extracts all pages.
Show PageRange fields

Use PageRange(start=1, end=5) to extract text from pages 1 through 5.
​
language
LanguageCode
The ISO-639 language code that specifies the document’s language for OCR processing. Use the LanguageCode enum to specify supported languages (e.g., LanguageCode.fr for French, LanguageCode.ja for Japanese). This parameter is essential for scanned PDFs and images containing non-Latin scripts, as it ensures the correct OCR engine is used to recognize characters accurately. Programmatic documents (PDF, .docx, .pptx) do not require this setting.
​
Using the docproc() method
The input to a docproc node uses the DocProcInput type from the ibm_watsonx_orchestrate.flow_builder.types module. You can optionally configure the kvp_schemas parameter to define key-value pair input schemas. For more information, see Semantic Key-Value Pair (KVP) Extraction.
Example use of the docproc node in an agentic workflow:
Python
from pydantic import BaseModel, Field
from ibm_watsonx_orchestrate.flow_builder.flows import (
    Flow, flow, START, END
)

from ibm_watsonx_orchestrate.flow_builder.types import DocProcInput


@flow(
    name ="text_extraction_flow_example",
    display_name="text_extraction_flow_example",
    description="This flow consists of one node: a docproc node, which extracts text from the input document",
    input_schema=DocProcInput
)
def build_docproc_flow(aflow: Flow = None) -> Flow:
    doc_proc_node = aflow.docproc(
        name="text_extraction",
        display_name="text_extraction",
        description="Extract text out of a document's contents.",
        task="text_extraction",
    )

    aflow.sequence(START, doc_proc_node, END)
    return aflow
Collapse
After the node runs, you receive a URL pointing to a file that contains the extracted text. If you configure key-value pair (KVP) extraction, the file also includes the extracted KVPs.
​
Using the language parameter
For scanned PDFs and images containing non-Latin scripts, specify the document’s language to ensure accurate OCR processing:
Python
from ibm_watsonx_orchestrate.flow_builder.flows import (
    Flow, flow, START, END
)
from ibm_watsonx_orchestrate.flow_builder.types import DocProcInput, LanguageCode


@flow(
    name="text_extraction_with_language_flow",
    display_name="Text Extraction with Language",
    description=(
        "Extracts text from documents using a specified OCR language. "
        "Setting the language improves OCR accuracy for scanned PDFs and images "
        "that contain non-Latin scripts such as Japanese, Korean, or Arabic."
    ),
    input_schema=DocProcInput
)
def build_docproc_language_flow(aflow: Flow = None) -> Flow:
    """
    Build a text extraction flow with language-aware OCR support.
    
    This example demonstrates how to use the language parameter to select the
    correct OCR engine for the document's script.
    
    Use the LanguageCode enum to specify the ISO-639 language code that matches
    the document's language.
    """
    doc_proc_node = aflow.docproc(
        name="text_extraction_language_node",
        display_name="Extract Text (Japanese)",
        description=(
            "Extracts text from a Japanese-language scanned document or image. "
            "Uses the Japanese OCR engine to correctly recognise non-Latin characters."
        ),
        task="text_extraction",
        language=LanguageCode.ja,
    )
    
    aflow.sequence(START, doc_proc_node, END)
    return aflow
Collapse
​
Text extraction with page range
Use the page_range parameter to limit extraction to a specific set of pages. For large documents where only a portion of the content is relevant, this parameter reduces processing time and output size.
Import PageRange from ibm_watsonx_orchestrate.flow_builder.types and pass it to docproc() as shown in the following example:
Example
"""Text Extraction with Page Range Example."""

import logging

from ibm_watsonx_orchestrate.flow_builder.flows import (
    END,
    START,
    Flow,
    flow,
)
from ibm_watsonx_orchestrate.flow_builder.types import DocProcInput, PageRange

# Configure logging
logger = logging.getLogger(__name__)


@flow(
    name="text_extraction_page_range_flow",
    display_name="Text Extraction with Page Range",
    description=(
        "Extracts text from a specific page range of input documents. "
        "Useful for processing only relevant sections of large documents."
    ),
    input_schema=DocProcInput,
)
def build_docproc_page_range_flow(aflow: Flow) -> Flow:
    """
    Build a text extraction flow that processes only a specific page range.

    This flow creates a document processing pipeline that extracts raw text
    content from a specified range of pages in the input document. This is
    particularly useful when:
    - Processing large documents where only certain pages are relevant
    - Extracting specific sections (e.g., pages 1-5 of a report)
    - Reducing processing time and costs by limiting the scope

    Args:
        aflow: Flow builder instance provided by the @flow decorator.

    Returns:
        Flow: Configured text extraction flow with page range filtering
            (START → docproc → END)
    """
    assert aflow is not None, "Flow instance must be provided"
    
    try:
        # Create document processing node configured for text extraction with page range
        # This will extract text only from pages 1 through 5 of the document
        doc_proc_node = aflow.docproc(
            name="text_extraction_with_page_range_node",
            display_name="Extract Text from Pages 1-5",
            description="Extracts raw text from a specific page range of the input document",
            task="text_extraction",
            page_range=PageRange(start=1, end=5),  # Extract only pages 1-5
        )

        # Connect nodes in sequence: START → docproc → END
        aflow.sequence(START, doc_proc_node, END)
        
        logger.info("Text extraction with page range flow built successfully")
        return aflow
        
    except Exception as e:
        logger.error(f"Failed to build text extraction page range flow: {e}", exc_info=True)
        raise

Collapse
​
Semantic Key-Value Pair (KVP) Extraction
Use the kvp_schemas parameter in the text extraction task to extract semantic key-value pairs from input documents.
For more information about configuring text extractors in watsonx Orchestrate, see Semantic key-value pair extraction: When to use and limitations.
You can define this parameter in two places:
Node specification: Set kvp_schemas in the node configuration. The node supports semantic KVP extraction in the following cases:
If you define kvp_schemas in the input, the node uses those schemas. If you pass an empty array, it falls back to default schemas.
If you don’t define kvp_schemas in the input but include them in the node specification, the node uses the specification-defined schemas. Again, if the array is empty, it defaults to the built-in schemas.
The kvp_schemas is configured as a JSON object. The following example shows how to define kvp_schemas in a node configuration.
Python
from pydantic import BaseModel, Field
from ibm_watsonx_orchestrate.flow_builder.flows import (
    Flow, flow, START, END
)

from ibm_watsonx_orchestrate.flow_builder.types import DocProcInput


@flow(
    name ="kvp_extraction_flow_example_for_api",
    display_name="kvp_extraction_flow_example_for_api",
    description="This flow consists of one node: a docproc node, which extracts kvps from the input document",
    input_schema=DocProcInput
)
def build_docproc_flow(aflow: Flow = None) -> Flow:
    doc_proc_node = aflow.docproc(
        name="kvp_extraction",
        display_name="kvp_extraction",
        description="Extract kvp out of a document's contents.",
        task="text_extraction",
        kvp_schemas=[{
        "document_type": "Invoice",
        "document_description": "An invoice is a standard document issued by a seller to a buyer, outlining products or services provided, quantities, prices, and payment terms.",
        "additional_prompt_instructions": "Extract values exactly as they appear in the document, especially numbers and codes.",
        "fields": {
        "invoice_number": {
            "description": "A unique identifier assigned by the vendor for this invoice.",
            "example": "2023-AUS-987654",
            "default": ""
        },
        "document_date": {
            "description": "Date of the document.",
            "example": "2025-07-05",
            "default": ""
        },
        "vendor_name": {
            "description": "Legal or trade name of the company issuing the invoice. Usually located in the header or footer, near the logo, or billing details.",
            "example": "ABC Supply Company Pty Ltd",
            "default": ""
        },
        "vendor_number": {
            "description": "Internal identifier used by the buyer's system to refer to the vendor.",
            "example": "VEND-1023",
            "default": ""
        }
        }
    }]
    )

    aflow.sequence(START, doc_proc_node, END)
    return aflow
Collapse
Runtime input: Set kvp_schemas in the input payload.
The following example shows how to define a kvp_schemas in the input payload.
Python
import asyncio
import logging
import sys
import json
from pathlib import Path

from examples.flow_builder.text_extraction.tools.text_extraction_flow import build_docproc_flow

logger = logging.getLogger(__name__)


def on_flow_end(result):
    """
    Callback function to be called when the flow is completed.
    """
    print(f"Custom Handler: flow `{flow_run.name}` completed with result: {result}")


def on_flow_error(error):
    """
    Callback function to be called when the flow fails.
    """
    print(f"Custom Handler: flow `{flow_run.name}` failed: {error}")


async def main(doc_ref: str, kvp_schema_path):
    '''A function demonstrating how to build a flow and save it to a file.'''
    my_flow_definition = await build_docproc_flow().compile_deploy()
    global flow_name
    flow_name = my_flow_definition.flow.spec.display_name
    generated_folder = f"{Path(__file__).resolve().parent}/generated"
    my_flow_definition.dump_spec(f"{generated_folder}/docproc_flow_spec.json")

    with open(kvp_schema_path, 'r') as file:
        # Load the JSON data from the file into a Python dictionary
        schema_json = json.load(file)

    global flow_run
    flow_run = await my_flow_definition.invoke(
        {
        "document_ref": doc_ref, 
        "language": "en",
        "kvp_schemas": [ schema_json ]
        }, 
        on_flow_end_handler=on_flow_end, on_flow_error_handler=on_flow_error, debug=True)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        logger.error(f"Usage: {sys.argv[0]} file_store_path kvp_schema_path")
    else:
        asyncio.run(main(sys.argv[1], sys.argv[2]))
Collapse
For both the node specification and runtime input, the default value of kvp_schemas is null. If you define the parameter in both places, the runtime input takes precedence and overrides the node specification. To use predefined extraction schemas, pass an empty array (kvp_schemas: []).
Use kvp_force_schema_name to specify the schema name for KVP extraction. Use kvp_enable_text_hints to enable or disable text hints during extraction. Configure both settings inside the docproc() node.
Python
    @flow(
        name="text_extraction_kvps_flow_example",
        display_name="Text Extraction with KVP Extraction Flow",
        description=(
            "This flow consists of one node: a docproc node, which extracts text "
            "and custom key-value pairs from the input document using a predefined schema"
        ),
        input_schema=DocProcInput,
    )
    def build_docproc_flow(aflow: Flow) -> Flow:
        """
        Build a text extraction flow with Key-Value Pair (KVP) extraction capabilities.
        
        This flow creates a document processing pipeline that:
        1. Extracts raw text content from input documents
        2. Identifies and extracts structured key-value pairs based on a predefined schema
        
        The KVP extraction uses a schema-driven approach to identify specific fields
        like company information, invoice numbers, dates, and line items from invoices.
        
        Runtime Parameter Override:
            All KVP-related parameters (kvp_schemas, kvp_model_name, kvp_force_schema_name,
            kvp_enable_text_hints) can be provided at runtime when invoking the flow.
            Runtime values will override the default values configured in this flow definition.
            This allows for dynamic configuration without modifying the flow code.
        
        Args:
            aflow: Flow builder instance provided by the @flow decorator.
        
        Returns:
            Flow: Configured text extraction flow with KVP extraction
                (START → docproc_node → END)
            
        Example:
            >>> flow = build_docproc_flow()
            >>> # Flow will extract text and KVPs from documents
        """
        # Validate Flow instance (defensive programming)
        assert aflow is not None, "Flow instance must be provided by the @flow decorator"
        
        try:
            # Get the KVP schema for invoice processing
            kvp_schemas = get_sample_invoice_kvp_schema()
            
            # Create document processing node configured for text and KVP extraction
            doc_proc_node = aflow.docproc(
                name="text_extraction_with_kvp_node",
                display_name="Text Extraction with KVP Node",
                description="Extracts raw text and structured key-value pairs from an input document",
                task="text_extraction",
                # KVP extraction parameters.
                #  Note: All kvp_* parameters below can be overridden at runtime when invoking the flow.
                #  Runtime values take precedence over these default configuration values.
                kvp_schemas=kvp_schemas,  # type: ignore[arg-type]  # Can be overridden at runtime
                # Optional: Uncomment to use a specific LLM for KVP extraction. This defaults to mistral-small. (can be overridden at runtime)
                kvp_model_name="watsonx/mistralai/mistral-small-3-1-24b-instruct-2503",
                # Optional: Uncomment to force a specific schema (can be overridden at runtime)
                kvp_force_schema_name="MyInvoice", # The "document_type" that will be used for KVP extraction. If not specified, the engine will try to match the input document to the given schemas.
                # Optional: Enable/disable text hints for KVP extraction (can be overridden at runtime)
                kvp_enable_text_hints=True,
            )
            
            # Connect nodes in sequence: START → doc_proc_node → END
            aflow.sequence(START, doc_proc_node, END)
            
            logger.info("Text extraction with KVP flow built successfully")
            return aflow
            
        except Exception as e:
            logger.error(f"Failed to build text extraction KVP flow: {e}", exc_info=True)
            raise
Collapse
​
Document processing with output format
See the following examples to learn how to use custom output formats with document processing:
Python
from typing import Optional
from pydantic import BaseModel, Field
from ibm_watsonx_orchestrate.flow_builder.flows import (
    Flow, flow, START, END
)
from ibm_watsonx_orchestrate.flow_builder.types import (
    DocProcField,
    DocProcInput,
    DocProcKVPSchema,
    DocProcKey,
    DocProcOutputFormat,
    NodeErrorHandlerConfig,
    TextExtractionObjectResponse,
)


class TextSummaryType(BaseModel):
    summary: str = Field(description="Summary of the input text", default="")

class TestFlowResultType(TextExtractionObjectResponse):
    summary_text: str = Field(description="The summary of the text computed by the 'Text summary' node.", default="")

INVOICE_KVP_SCHEMA: DocProcKVPSchema = DocProcKVPSchema(
    document_type="MyInvoice",
    document_description="A simple invoice document",
    fields = {
        "invoice_number" : DocProcField(
            description="he unique identifier for the invoice.",
            default="",
            example="INV-0001",
        ),
        "total_amount" : DocProcField(
            description="The total amount due on the invoice.",
            default="",
            example="1000.00",
        ),
        "due_date" : DocProcField(
            description="The date on which the invoice is due.",
            default="",
            example="2023-01-01",
        )
    }
)

@flow(
    name="text_extraction_and_summary_flow_example",
    display_name="Text Extraction and Summary Flow",
    description="This flow consists of two nodes. The first node extracts the raw text out of a document's contents. The second node uses the raw text to generate a summary using the GenAI node.",
    input_schema=DocProcInput,
    output_schema=TestFlowResultType
)
def build_docproc_flow(flow: Flow) -> Flow:
    # Create the docproc node for text extraction
    doc_proc_node = flow.docproc(
        name="text_extraction_node",
        display_name="Generic text extraction node",
        description="Extract the raw text out of a document's contents.",
        task="text_extraction",
        #document_structure=True,
        output_format=DocProcOutputFormat.object,  # Return JSON object instead of document reference
        # Optional KVP (Key-Value Pair) extraction parameters:
        kvp_schemas=[ INVOICE_KVP_SCHEMA ],
        kvp_force_schema_name="MyInvoice",  # Force a specific schema to be used
    )

    # Explicitly map all flow inputs to the docproc node to prevent automap from
    # overriding input values with potentially incorrect automatic mappings.
    doc_proc_node.map_input(input_variable="document_ref", expression="flow.input.document_ref")
    doc_proc_node.map_input(input_variable="kvp_schemas", expression="flow.input.kvp_schemas")
    doc_proc_node.map_input(input_variable="kvp_model_name", expression="flow.input.kvp_model_name")
    doc_proc_node.map_input(input_variable="kvp_force_schema_name", expression="flow.input.kvp_force_schema_name")
    doc_proc_node.map_input(input_variable="kvp_enable_text_hints", expression="flow.input.kvp_enable_text_hints")

    # A Prompt node that will summarize the text extracted from the input invoice.
    my_summary_node = flow.prompt(
      name="my_summary_node",
      display_name="Text summary node",
      description="Text summary node",
      system_prompt=[
          "You are a knowledge source."
      ],
      user_prompt=[
          "Write a 2 sentence summary of: {text}"
      ],
      error_handler_config=NodeErrorHandlerConfig(
          error_message="An error has occurred while invoking the LLM",
          max_retries=1,
          retry_interval=1000
      ),
      input_schema=TextExtractionObjectResponse,
      output_schema=TextSummaryType,
    )

    # Map the text extracted from the input invoice to the user prompt of the Prompt node.
    my_summary_node.map_input(input_variable="text", expression="flow[\"Generic text extraction node\"].output.text")

    # START --> text extraction node --> prompt node --> END
    flow.sequence(START, doc_proc_node, my_summary_node, END)

    # Explicit output mapping is required when using DocProcOutputFormat.object.
    # Without explicit mapping, the automap feature would attempt to automatically map outputs,
    # which could inject large document structures into the LLM context and cause token overflow.
    # By explicitly mapping each output field, we maintain control over what data flows through.

    # summary_text is the output from the Prompt node.
    flow.map_output(output_variable="summary_text", expression="flow[\"Text summary node\"].output.summary")
    # The text is the original raw text extracted from the input invoice, produced by the text extraction node.
    flow.map_output(output_variable="text", expression="flow[\"Generic text extraction node\"].output.text")
    # The kvps are the extracted kvps produced by the text extraction node.
    flow.map_output(output_variable="metadata", expression="flow[\"Generic text extraction node\"].output.metadata")
    flow.map_output(output_variable="kvps", expression="flow[\"Generic text extraction node\"].output.kvps")

    # These are not produced by this example, but you need them if you set document_structure=True.
    flow.map_output(output_variable="top_level_structures", expression="flow[\"Text extraction node with document structure\"].output.top_level_structures")
    flow.map_output(output_variable="all_structures", expression="flow[\"Text extraction node with document structure\"].output.all_structures")

    return flow
Collapse
Python
from ibm_watsonx_orchestrate.flow_builder.flows import (
    Flow, flow, START, END
)

from ibm_watsonx_orchestrate.flow_builder.types import DocProcInput, DocProcOutputFormat, TextExtractionObjectResponse


@flow(
    name="text_extraction_object_output_flow_example",
    display_name="Text Extraction with Object Output Example",
    description="Extracts text content and document structure from input documents using document processing. The output will be an Object instead of a file URL. Supports PDF, DOCX, images, and other formats.",
    input_schema=DocProcInput,
    output_schema=TextExtractionObjectResponse,
)
def build_docproc_flow(flow: Flow) -> Flow:
    """
    Build a text extraction flow that outputs both text and document structure.
    
    This flow creates a document processing pipeline that extracts raw text
    content along with the structural information (headings, paragraphs, tables,
    etc.) from input documents.
    
    Args:
        aflow (Flow, optional): Flow builder instance.
    
    Returns:
        Flow: Configured text extraction flow with structure output (START → docproc → END)
        
    Note:
        The document_structure parameter is set to True to include structural
        information in the output. This is useful for downstream processing
        that requires understanding of document layout.
    """
    assert flow is not None, "Flow instance must be provided"
    
    # Create document processing node for text extraction with structure
    doc_proc_node = flow.docproc(
        name="a_text_extraction_node",
        display_name="Text extraction node with document structure",
        description="Extracts the raw text from an input document and its structure",
        task="text_extraction",  # Specifies text extraction task
        document_structure=True,  # Output the document structure. This defaults to False.

        output_format=DocProcOutputFormat.object,  # Output format is JSON object

    )

    # Explicitly map all flow inputs to the docproc node to prevent automap from
    # overriding input values with potentially incorrect automatic mappings.
    doc_proc_node.map_input(input_variable="document_ref", expression="flow.input.document_ref")
    doc_proc_node.map_input(input_variable="kvp_schemas", expression="flow.input.kvp_schemas")
    doc_proc_node.map_input(input_variable="kvp_model_name", expression="flow.input.kvp_model_name")
    doc_proc_node.map_input(input_variable="kvp_force_schema_name", expression="flow.input.kvp_force_schema_name")
    doc_proc_node.map_input(input_variable="kvp_enable_text_hints", expression="flow.input.kvp_enable_text_hints")

    # Connect nodes in sequence: START → docproc → END
    flow.sequence(START, doc_proc_node, END)

    # Explicit output mapping is required when using DocProcOutputFormat.object.
    # Without explicit mapping, the automap feature would attempt to automatically map outputs,
    # which could inject large document structures into the LLM context and cause token overflow.
    # By explicitly mapping each output field, we maintain control over what data flows through.
    flow.map_output(output_variable="text", expression="flow[\"Text extraction node with document structure\"].output.text")
    flow.map_output(output_variable="metadata", expression="flow[\"Text extraction node with document structure\"].output.metadata")
    flow.map_output(output_variable="kvps", expression="flow[\"Text extraction node with document structure\"].output.kvps")
    flow.map_output(output_variable="top_level_structures", expression="flow[\"Text extraction node with document structure\"].output.top_level_structures")
    flow.map_output(output_variable="all_structures", expression="flow[\"Text extraction node with document structure\"].output.all_structures")

    return flow

    ---

    Agentic Workflows
Configuring callbacks
Use callbacks to invoke a tool when specific events occur during an agentic workflow. Callbacks are fire-and-forget, the workflow engine invokes the registered tool and ignores its return value. Callbacks are part of the workflow specification and are serialized into the compiled flow JSON. The tools that you register as callbacks must already be deployed in watsonx Orchestrate, since they are not runtime Python callables.
To configure a callback, call the add_callback() method on your Flow instance. The method creates a FlowCallback object, appends it to the workflow specification, and returns Self to support method chaining. Call add_callback() multiple times to register separate callbacks for different event sets.
​
tool
stringrequired
The identifier of the deployed tool to invoke when the callback fires. Use one of the following formats:
tool_name: The tool name only.
tool_name:tool_uuid: The tool name with a specific instance UUID.
toolkit:tool_name: The tool scoped to a toolkit.
toolkit:tool_name:tool_uuid: The toolkit-scoped tool with a specific instance UUID.
​
events
List[FlowCallbackEventKind]required
The lifecycle events that trigger this callback. Specify at least one value. For all available values, see Events reference.
​
batch_interval
int
The time, in milliseconds, that the engine waits to accumulate events before it dispatches a single batched invocation. If you omit this parameter, the server default applies.
​
Batching rules
The flow engine batches callback events before it invokes the registered tool. The following rules govern how and when the engine dispatches a batch:
The engine accumulates events for the duration specified by batch_interval before it dispatches a single invocation. If you omit batch_interval, the server default applies.
When a blocking event is dispatched, the engine immediately flushes all events that are currently queued for that callback. If the callback tool is registered for both blocking and non-blocking events, the queued non-blocking events are dispatched at flush time regardless of whether the batch timer has elapsed.
​
Events reference
The following FlowCallbackEventKind members and their wire values are available. Pass any combination to add_callback(events=[...]).
​
ON_FLOW_START
flow:on_flow_start
The flow started execution.
​
ON_FLOW_END
flow:on_flow_end
The flow completed successfully.
​
ON_FLOW_ERROR
flow:on_flow_error
The flow failed with an error.
​
ON_FLOW_ABORT
flow:on_flow_abort
An external action aborted the flow instance.
​
ON_FLOW_DELETE
flow:on_flow_delete
The flow instance was deleted.
​
ON_TASK_WAIT
task:on_task_wait
A task is waiting for user input (elicitation). The callback payload includes an elicitation object that describes the required input.
​
ON_TASK_ERROR
task:on_task_error
A task failed during execution.
​
ON_TASK_MESSAGE
task:on_task_message
A task generated a message.
​
Callback event payload
The flow engine calls the registered tool and passes a FlowCallbackEventsPayload object as input.
​
FlowCallbackEventsPayload
​
events
List[FlowCallbackEventPayload]required
One or more event payloads delivered in this callback invocation.
​
FlowCallbackEventPayload
​
event
EventMetadatarequired
Metadata that describes the event: its kind, when it occurred, the flow instance it belongs to, and any task or error context.
​
output
dict
The flow output value. Present only when state is completed.
​
elicitation
ElicitationDetails
Details of the pending user input request. Present only when state is input_required, which corresponds to ON_TASK_WAIT events.
​
EventMetadata
​
id
stringrequired
A unique identifier for this event occurrence.
​
kind
stringrequired
One of the wire strings listed in the Events reference.
​
created_at
stringrequired
An ISO 8601 timestamp that records when the event occurred.
​
instance_id
stringrequired
A unique identifier for the running flow instance that generated this event.
​
flow_name
stringrequired
The name of the flow.
​
environment_id
stringrequired
The environment where the flow is running, for example draft or live.
​
state
stringrequired
The execution state of the flow when the event fired. Valid values are working, input_required, completed, failed, aborted, and deleted.
​
parent_instance_id
string
The parent flow instance ID. Present only when this flow is a child flow.
​
parent_flow_name
string
The parent flow name. Present only when this flow is a child flow.
​
task_id
string
The task ID. Present only for ON_TASK_* events.
​
task_name
string
The internal task name. Present only for ON_TASK_* events.
​
task_display_name
string
The human-readable task name. Present only for ON_TASK_* events.
​
error
ErrorDetails
Details of the error that caused the flow or task to fail. Present only for ON_FLOW_ERROR and ON_TASK_ERROR events. Contains message (string, required) and code (string, optional).
​
ElicitationDetails
Present only when state is input_required.
​
mode
stringrequired
The elicitation mode. Currently always "form".
​
message
stringrequired
A message that describes the input that the user must provide.
​
elicitationId
stringrequired
A unique identifier for this elicitation request. The value is the same as task_id.
​
requestedSchema
dictrequired
A JSON Schema object that defines the expected structure, types, and validation rules for the user input.
​
meta.assignee
stringrequired
The user ID or email address of the user who must provide the input.
​
meta.response_items
listrequired
An array of ResponseItem objects, where each object describes one input field. Supported response_type values: text, number, option, date, datetime, time, file_upload, file_download, object, and forms.
​
Building a compatible callback tool
The flow engine identifies compatible callback tools by matching the tool’s input schema against the FlowCallbackEventsPayload structure. You can register any of the following tool types as a callback: Python, OpenAPI, MCP, or Flow.
When you use a Flow tool as a callback, the callback flow must not contain user activity nodes. Callback flows run asynchronously and do not have access to the originating user’s chat thread, so the system cannot deliver user interactions inside a callback flow.
For more information, see Flow callback example.
​
FlowCallback direct construction
To build a callback object separately before you attach it, construct a FlowCallback directly and append it to aflow.spec.callbacks. The FlowCallback model mirrors the parameters of add_callback() exactly.
# Import FlowCallback to construct a callback object directly,
# and FlowCallbackEventKind to reference the available lifecycle events.
from ibm_watsonx_orchestrate.flow_builder.types import FlowCallback
from ibm_watsonx_orchestrate.flow_builder.flow_callback_types import FlowCallbackEventKind

# Build a FlowCallback that targets a toolkit-scoped tool identified by name and UUID.
# The callback fires on ON_FLOW_START and ON_FLOW_END, and batches events
# for up to 60 seconds before dispatching a single invocation.
callback = FlowCallback(
    tool="audit_toolkit:audit_logger:xyz-789-ghi-012",
    events=[FlowCallbackEventKind.ON_FLOW_START, FlowCallbackEventKind.ON_FLOW_END],
    batch_interval=60_000  # 1 minute
)

# Attach the callback to the flow by appending it to the spec's callbacks list.
aflow.spec.callbacks.append(callback)
Flow.add_callback() is the preferred, higher-level API. Use direct FlowCallback construction only when you need to manipulate the spec list explicitly.
​
Example
The following example registers two callbacks on the same flow. The first callback handles flow-level lifecycle events and uses the server default batch interval. The second handles task-level events with a custom 30-second interval.
Python
# BaseModel is used to define strongly typed input and output schemas for the flow.
from pydantic import BaseModel
# Flow is the builder class; flow is the decorator that registers the function as a
# flow definition; START and END are sentinel nodes that mark the flow boundaries.
from ibm_watsonx_orchestrate.flow_builder.flows import Flow, flow, START, END
# FlowCallbackEventKind enumerates all lifecycle events that can trigger a callback.
from ibm_watsonx_orchestrate.flow_builder.flow_callback_types import FlowCallbackEventKind

# my_tool is the deployed tool that this flow executes as its sole task node.
from .my_tool import my_tool


# Define the input schema: the flow accepts a single string field named "message".
class FlowInput(BaseModel):
    message: str


# Define the output schema: the flow returns a single string field named "result".
class FlowOutput(BaseModel):
    result: str


# The @flow decorator registers this function as a named, deployable flow definition.
# input_schema and output_schema enforce the contract for callers of this flow.
@flow(
    name="example_flow_with_callbacks",
    display_name="Example Flow with Callbacks",
    input_schema=FlowInput,
    output_schema=FlowOutput,
)
def build_example_flow_with_callbacks(aflow: Flow) -> Flow:
    # Wrap my_tool as a task node in the flow graph.
    node = aflow.tool(my_tool)
    # Connect START → node → END to form a linear single-step flow.
    aflow.sequence(START, node, END)

    # Register a callback for flow-level lifecycle events.
    # "flow_callback_handler" is a deployed tool that receives these events.
    # No batch_interval is set, so the server default batching window applies.
    aflow.add_callback(
        tool="flow_callback_handler",
        events=[
            FlowCallbackEventKind.ON_FLOW_START,   # fires when the flow begins
            FlowCallbackEventKind.ON_FLOW_END,     # fires when the flow completes successfully
            FlowCallbackEventKind.ON_FLOW_ERROR,   # fires when the flow fails
        ],
    )

    # Register a second callback for task-level events using a toolkit-scoped tool.
    # batch_interval=30_000 means the engine waits up to 30 seconds to accumulate
    # task events before dispatching a single batched invocation.
    aflow.add_callback(
        tool="monitoring_toolkit:task_event_handler",
        events=[
            FlowCallbackEventKind.ON_TASK_WAIT,    # fires when a task awaits user input
            FlowCallbackEventKind.ON_TASK_ERROR,   # fires when a task fails
            FlowCallbackEventKind.ON_TASK_MESSAGE, # fires when a task emits a message
        ],
        batch_interval=30_000,
    )

    return aflow

    -----

    Agentic Workflows
Configuring multi-user activities
Multi-user activities let you assign a User Activity Node to specific users registered in your tenant. You configure this behavior directly in your agentic workflow code by using the assign_to method on a UserFlow.
You start by instantiating the UserFlow class in your flow definition.
Python
user_flow: UserFlow = aflow.userflow()
After you create the UserFlow, configure user assignment by calling the assign_to method and passing the required parameters.
​
policy
UserAssignmentPolicyrequired
The assignment policy that controls who receives the user activity. Supported options include:
UserAssignmentPolicy.FLOW_INITIATOR: Assigns the user flow to the user who initiates the flow. If you do not explicitly set a UserAssignmentPolicy or run the flow in Preview mode, the initiator receives the user flow.
UserAssignmentPolicy.USER: Assigns the user flow to one or more users specified in the assignees parameter.
​
assignees
string
An expression that resolves to the user or users who execute the user activity. This parameter is required when you set the policy to UserAssignmentPolicy.USER. You can provide the expression in one of the following forms:
A JSON array with a single user ID string. Example: '["123002B12G"]'
A flow variable path that references a user. Example: flow.private.employee.manager In this case, manager has the User type.
At runtime, the flow evaluates the expression and assigns the user activity to the resolved user.
Python
user_flow.assign_to(policy=UserAssignmentPolicy.USER, assignees='flow.private.designated')
Example:
The following example demonstrates how you configure multiple user activities within a single flow. One user flow runs under a designated user, while a second user flow runs under the flow initiator.
Python
from ibm_watsonx_orchestrate.flow_builder.flows.flow import UserFlow


from typing import List
from pydantic import BaseModel, Field
from ibm_watsonx_orchestrate.flow_builder.flows import (
    Flow, flow, UserNode, START, END
)
from ibm_watsonx_orchestrate.flow_builder.types import Assignment, UserAssignmentPolicy, UserFieldKind
from ibm_watsonx_orchestrate.flow_builder.data_map import DataMap
from ibm_watsonx_orchestrate_core.types.tools.types import WXOUser

class Name(BaseModel):
    """
    This class represents a person's name.

    Attributes:
        name (str): The person's first name.
    """
    first_name: str = Field(default="John Doe", description="First name")

class PrivateData(BaseModel):
    """
    Private data schema for the flow.
    
    Attributes:
        designated (WXOUser): The designated user for this flow
    """
    designated: WXOUser = Field(
        description="The designated user that will run the user flow"
    )
@flow(
    name ="user_flow_assigned_user",
    display_name="user_flow_assigned_user",
    description="Example of a user flow send to a different user than the initiator.",
    input_schema=Name,
    private_schema=PrivateData
)
def build_user_flow(aflow: Flow = None) -> Flow:
    
    init_script = """flow.private.designated = system.user.search_by_email('wxo.archer@ibm.com')[0]"""
    
    # TODO if running in a non local environment, replace with a real user email.
    # init_script = """flow.private.designated = system.user.search_by_email('user_email')[0]"""
    
    init_data = aflow.script(name="init_data", script=init_script)
    
    # user_flow which is a subflow to be added to the aflow
    user_flow: UserFlow = aflow.userflow()
    user_flow.assign_to(policy=UserAssignmentPolicy.USER, assignees='flow.private.designated')

    # add a text input field
    user_node1 = user_flow.field(direction="input",name="last_name", display_name="Last name",  kind=UserFieldKind.Text, text="Enter last name")

   # add user_flow edges
    user_flow.edge(START, user_node1)
    user_flow.edge(user_node1, END)


    initiator_user_flow: UserFlow = aflow.userflow()
    initiator_user_flow.assign_to(policy=UserAssignmentPolicy.FLOW_INITIATOR)
    # add a Display user text field
    user_node2 = initiator_user_flow.field(direction="output",name="display_first_name", display_name="Display the name", kind=UserFieldKind.Text, text="Welcome {flow.userflow_1[\"Last name\"].output.value}")

    initiator_user_flow.edge(START, user_node2)
    initiator_user_flow.edge(user_node2, END) 
    
    # add the user_flow to the flow sequence to create the flow edges
    aflow.edge(START, init_data)
    aflow.edge(init_data, user_flow)
    aflow.edge(user_flow, initiator_user_flow)
    aflow.edge(initiator_user_flow, END)

    return aflow


---

Multi-language support
Multi-language support overview
Agentic workflows support multi-language configurations for user activities. Configure target languages in your agentic workflow code, export translatable text to CSV files, add translations, and import them back using the ADK CLI.
Category	What gets translated	What does NOT get translated
User activities	Field labels and display names
Help text and placeholder text
Form instructions
Button labels
Choice option labels
Error messages	User input
Dynamic content from variables
Tool outputs
Agentic workflow logic	-	Agentic workflow expressions
Conditions
Variable names
Metadata	-	Tool names
Tool descriptions
Agentic workflow names
​
Supported locale codes
en: English
fr: French
es: Spanish
de: German
it: Italian
ja: Japanese
ko: Korean
zh-CN: Chinese (Simplified)
zh-TW: Chinese (Traditional)
pt-BR: Portuguese (Brazilian)
​
Steps
1
Configure target locales

Define target languages in your agentic workflow code using aflow.target_locales(['fr', 'es']). For details, see Configuring target locales.
2
Import the agentic workflow

Import your agentic workflow into watsonx Orchestrate using the ADK CLI. For details, see Managing tools.
3
Manage translations

Export translatable text to CSV, add translations, and import them back. For details, see Managing translations.

---

Multi-language support
Configuring target locales
Configure target locales in your agentic workflow to specify which languages it supports. Use Python APIs in your agentic workflow code to configure these settings.
Use the target_locales() method on your agentic workflow to specify which languages it supports:
Python
from ibm_watsonx_orchestrate.flow_builder.flows import Flow, flow, START, END
from ibm_watsonx_orchestrate.flow_builder.types import UserFieldKind

@flow(
    name="multilingual_flow",
    description="A flow with multi-language support"
)
def build_multilingual_flow(aflow: Flow = None) -> Flow:
    # Define user activities
    user_flow = aflow.userflow()
    user_node = user_flow.field(
        direction="input",
        name="user_name",
        display_name="Enter your name",
        kind=UserFieldKind.Text
    )
    
    user_flow.edge(START, user_node)
    user_flow.edge(user_node, END)
    
    # Configure target locales for translation
    aflow.target_locales(["fr", "es", "de", "ja"])
    
    aflow.sequence(START, user_flow, END)
    return aflow
See all 25 lines
​
Setting the source locale
By default, the source locale is en (English). Change it using the source_locale() method:
Python
aflow.source_locale("fr")  # Set French as source language
aflow.target_locales(["en", "es", "de"])  # Translate to English, Spanish, German
​
Enabling or disabling translation
Enable or disable translation support explicitly:
Python
# Enable translation (default is True)
aflow.translation_enabled(True)

# Disable translation
aflow.translation_enabled(False)
See all 5 lines
When you disable translation, the system ignores the target_locales() configuration and applies no translations.
​
Complete example
The following example shows a customer feedback form with multi-language support:
Python
from ibm_watsonx_orchestrate.flow_builder.flows import Flow, flow, START, END
from ibm_watsonx_orchestrate.flow_builder.types import UserFieldKind

@flow(
    name="customer_feedback_form",
    description="Collect customer feedback in multiple languages"
)
def build_feedback_flow(aflow: Flow = None) -> Flow:
    # Create user flow with form
    user_flow = aflow.userflow()
    
    feedback_form = user_flow.form(
        name="feedback_form",
        display_name="Customer Feedback",
        instructions="Please share your experience with us",
        submit_button_label="Submit Feedback",
        cancel_button_label="Cancel"
    )
    
    # Add form fields
    feedback_form.text_input_field(
        name="customer_name",
        label="Your Name",
        required=True,
        placeholder_text="Enter your full name",
        help_text="We need your name to follow up on your feedback"
    )
    
    feedback_form.text_input_field(
        name="feedback",
        label="Your Feedback",
        required=True,
        single_line=False,
        placeholder_text="Tell us about your experience",
        help_text="Please provide detailed feedback"
    )
    
    feedback_form.choice_input_field(
        name="rating",
        label="Overall Rating",
        required=True,
        choices=[
            {"label": "Excellent", "value": "5"},
            {"label": "Good", "value": "4"},
            {"label": "Average", "value": "3"},
            {"label": "Poor", "value": "2"},
            {"label": "Very Poor", "value": "1"}
        ]
    )
    
    user_flow.edge(START, feedback_form)
    user_flow.edge(feedback_form, END)
    
    # Configure multi-language support
    aflow.target_locales(["fr", "es", "de", "ja"])
    
    aflow.sequence(START, user_flow, END)
    return aflow
See all 58 lines
​
Next steps
After you configure target locales in your agentic workflow code:
Import the agentic workflow into watsonx Orchestrate.
Export translations to a CSV file.
Add translations to the CSV file.
Import translations back into the agentic workflow.
For details on managing translations, see Managing translations.


---

Multi-language support
Managing translations for agentic workflows
After you configure target locales in your agentic workflow, export translatable text to CSV files, add translations, and import them back using CLI commands.
​
Exporting translations
Export translatable text from an agentic workflow to a CSV file:
Bash
orchestrate tools translation-export \
  -k flow \
  --name my_flow_name \
  --translation translations.csv
You can also export from an agentic workflow JSON file before importing:
Bash
orchestrate tools translation-export \
  -k flow \
  -f path/to/flowJson.json \
  --translation translations.csv
Show command flags

​
Creating translations
The exported CSV file contains:
key: Unique identifier for each translatable text element
en: Source language text or your configured source locale
locale: Source locale code
Additional columns for each target locale
Edit the CSV file and add translations for each target locale:
key,en,locale,fr,es
form.instructions,Please fill out this form,en,Veuillez remplir ce formulaire,Por favor complete este formulario
form.submit_button,Submit,en,Soumettre,Enviar
form.cancel_button,Cancel,en,Annuler,Cancelar
field.name.label,Your Name,en,Votre nom,Su nombre
field.name.placeholder,Enter your full name,en,Entrez votre nom complet,Ingrese su nombre completo
user_activity.user_name.display_name,Enter your name,en,Entrez votre nom,Ingrese su nombre
user_activity.user_name.help_text,Please provide your full name,en,Veuillez fournir votre nom complet,Por favor proporcione su nombre completo
Ensure your CSV file uses UTF-8 encoding to properly handle special characters in different languages.
​
Importing translations
Import translations from a CSV file into an agentic workflow:
Bash
orchestrate tools translation-import \
  -k flow \
  --name my_flow_name \
  --translation translations.csv
Show command flags

​
Importing agentic workflows with translations
Import an agentic workflow and its translations in a single command:
Bash
orchestrate tools import \
  -k flow \
  -f path/to/my_flow.py \
  --translation translations.csv
This command imports the agentic workflow and applies the translations automatically.

---

Agentic Workflows
Masking sensitive data
Use masking to protect sensitive information in your agentic workflows. Masking obscures data such as Social Security Numbers, credit card numbers, authentication tokens, and other confidential information in logs, user interfaces, and outputs while maintaining the data’s usability within the workflow.
Important restrictions:
Only STRING properties can be masked. Arrays, objects, numbers, and booleans cannot be masked.
Flow output properties cannot be masked directly. Only flow input, flow private, and node output properties can be masked.
Configure masking by using the mask_property() method on your flow object:
aflow.mask_property(
    property_path,
    masking_policy,
    regex_config=None,
    input_policy=None
)
Parameters:
​
property_path
stringrequired
Dot-notation path to the property to mask. The path uses a hierarchical structure to identify the exact location of the sensitive data within the flow.
Supports masking properties in:
Flow input schema: flow.input.property_name
Flow private schema: flow.private.property_name
Node output schemas: flow.node_name.output.property_name
Nested flow node outputs: flow.nested_flow.node.output.property_name
Nested properties: flow.input.user.emailstructures.
​
masking_policy
MaskingPolicyrequired
The masking strategy to apply. Supported values:
MASK_ALL: Completely masks the entire value with asterisks.
Example: 123-45-6789 becomes ***********
MASK_LAST4: Masks all characters except the last 4.
Example: 123-45-6789 becomes *******6789
MASK_FIRST4: Masks all characters except the first 4.
Example: AUTH-TOKEN-12345 becomes AUTH***********
MASK_VIA_REGEX: Uses custom regex patterns for advanced masking scenarios. Requires regex_config parameter.
Example: 1234-5678-9012-3456 with pattern ^(\\d{4})-(\\d{4})-(\\d{4})-(\\d{4})$ and masking XXXX-XXXX-XXXX-$4 becomes XXXX-XXXX-XXXX-3456
​
regex_config
dict
Required when using MaskingPolicy.MASK_VIA_REGEX.
Show regex_config structure

​
input_policy
InputPolicy
Optional input masking behavior. Supported values:
MASK_WHILE_TYPING: Masks the value in real-time as you type. If omitted, data is masked only on output, not during input.
The following example demonstrates masking across multiple node types in a single workflow:
Python
"""
Comprehensive flow to test masking functionality across different node types.

This flow demonstrates masking of sensitive data across:
- Input schema fields
- Private variables (with nested object)
- Script node outputs
- User flow fields
- Tool node inputs/outputs
- OpenAPI tool responses
- ForEach loop data
"""

from typing import List
from pydantic import BaseModel, Field
from ibm_watsonx_orchestrate.flow_builder.flows import (
    Flow, flow, START, END
)
from ibm_watsonx_orchestrate.flow_builder.masking_utils import InputPolicy, MaskingPolicy
from ibm_watsonx_orchestrate.flow_builder.types import ForeachPolicy, UserFieldKind
from ibm_watsonx_orchestrate.flow_builder.data_map import DataMap, Assignment

# Commented out Python tool imports - tools can be uncommented when import issues are resolved
from .process_user_data import process_user_data
from .validate_credentials import validateCredentials

class UserInput(BaseModel):
    """Input schema with one sensitive field to be masked."""
    username: str = Field(description="User's username")
    ssn: str = Field(description="Social Security Number (sensitive)")

class Credentials(BaseModel):
    """Nested object for private credentials."""
    auth_token: str = Field(description="Authentication token")

class PrivateData(BaseModel):
    """Private schema with nested sensitive data."""
    user_id: str = Field(description="Internal user ID")
    credentials: Credentials = Field(description="User credentials")

class ProcessedUser(BaseModel):
    """Output schema with masked field."""
    user_id: str = Field(description="Generated user ID")
    username: str = Field(description="Username")
    masked_ssn: str = Field(description="Masked SSN for display")
    processing_notes: List[str] = Field(description="Processing notes")

class EmailRecord(BaseModel):
    """Schema for forEach loop items."""
    recipient: str = Field(description="Email recipient")
    api_token: str = Field(description="API token for sending (sensitive)")

@flow(
    name="masking_test_flow",
    display_name="Comprehensive Masking Test Flow",
    description="Tests masking functionality across all node types",
    input_schema=UserInput,
    output_schema=ProcessedUser,
    private_schema=PrivateData
)
def build_masking_test_flow(aflow: Flow) -> Flow:
    """
    Build a comprehensive flow to test masking across different node types.
    
    This flow includes:
    1. Input masking (SSN)
    2. Private variable masking (nested credentials)
    3. Script node with masked outputs
    4. User flow with masked field
    5. Python tool with masked parameters
    6. OpenAPI tool with masked responses
    """
    
    # ============================================================
    # SCRIPT NODE
    # ============================================================
    
    # Define output schema for script with masking extensions
    class ScriptOutput(BaseModel):
        masked_ssn: str = Field(description="Masked SSN for display")
    
    # Single script node to process data
    process_data_script = aflow.script(
        name="process_data",
        display_name="Process User Data",
        output_schema=ScriptOutput,
        script="""

# Generate user ID
flow.private.user_id = f"USER-{hash(flow.input.username) % 10000}"

# Generate auth token (sensitive)
token_input = f"{flow.input.username}:{flow.input.ssn}"
flow.private.credentials.auth_token = '123456789000'

# Create masked SSN for output
self.output.masked_ssn = flow.input.ssn
"""
    )
    
    # ============================================================
    # PYTHON TOOL NODES 
    # ============================================================
    
    # Tool node with masked input/output
    process_tool_node = aflow.tool(process_user_data)
    process_tool_node.map_input(input_variable="username", expression="flow.input.username")
    process_tool_node.map_input(input_variable="ssn", expression="flow.input.ssn")
    
    # Python tool for credential validation
    validate_creds_node = aflow.tool(validateCredentials)
    
    # ============================================================
    # USER FLOW NODE
    # ============================================================
    
    user_flow_form = aflow.userflow()
    user_flow_form.spec.display_name= "Application"

    # Create form with default submit button and visible cancel button
    user_node_with_form = user_flow_form.form(
        name="ApplicationForm",
        display_name="Application",
        cancel_button_label="Cancel"
    )

    user_node_with_form.text_input_field(name="lastName", label="Last name", required=True, placeholder_text="Enter your name here", help_text="Enter name", 
        regex="^[a-zA-Z0-9\s]+$", regex_error_message="No special characters allowed")
    
    user_flow_form.edge(START, user_node_with_form)
    user_flow_form.edge(user_node_with_form, END)
 
    user_flow = aflow.userflow()
    
    # User input field for sensitive data
    user_input_field = user_flow.field(
        direction="input",
        name="additional_ssn",
        display_name="Passport number",
        kind=UserFieldKind.Text,
        text="Enter the passport number"
    )

    user_output_lastName = user_flow.field(
        direction="output",
        name="display_lastName",
        display_name="Last name (from field input) ",
        kind=UserFieldKind.Text,
        text="Last name (masked all ) {flow.Application.Application.output[\"Last name\"]}",
    )

    user_output_middle_name = user_flow.field(
        direction="output",
        name="display_middle_name",
        display_name="Middle name (from tool) ",
        kind=UserFieldKind.Text,
        text="Middle name (masked first 4 ) {flow.process_user_data.output.middle_name}",
    )

    user_output_ssn = user_flow.field(
        direction="output",
        name="display_masked_ssn",
        display_name="Masked SSN (from input) ",
        kind=UserFieldKind.Text,
        text="SSN from input (masked all ) {flow.input.ssn}",
    )

    user_output_health_insurance = user_flow.field(
        direction="output",
        name="display_health_insurance",
        display_name="Health insurance (from tool) ",
        kind=UserFieldKind.Text,
        text="Health insurance (masked first 4 ) {flow.process_user_data.output.health_insurance}",
    )

    user_output_token = user_flow.field(
        direction="output",
        name="display_masked_token",
        display_name="Masked Auth Token (from private)",
        kind=UserFieldKind.Text,
        text="Auth token from private credentials (masked first 4) {flow.private.credentials.auth_token}",
    )

    user_output_additional_ssn = user_flow.field(
        direction="output",
        name="display_additional_ssn",
        display_name="Passport number (from user input)",
        kind=UserFieldKind.Text,
        text="Passport number (masked): {flow.userflow_4.additional_ssn.output.value}",
    )

    user_output_codeblock = user_flow.field(
        direction="output",
        name="display_script_ssn",
        display_name="Masked SSN from script",
        kind=UserFieldKind.Text,
        text="Masked SSN from script: {flow.process_data.output.masked_ssn}",
    )

    validate_credentials = user_flow.field(
        direction="output",
        name="validate_credentials_token",
        display_name="Validate credentials client token",
        kind=UserFieldKind.Text,
        text="Masked Validate credentials client token: {flow.validateCredentials.output.token}",
    )
    
    # User flow edges
    user_flow.edge(START, user_input_field)
    user_flow.edge(user_input_field, user_output_lastName)
    user_flow.edge(user_output_lastName, user_output_middle_name)
    user_flow.edge(user_output_middle_name, user_output_ssn)
    user_flow.edge(user_output_ssn, user_output_token)
    user_flow.edge(user_output_token, user_output_codeblock)
    user_flow.edge(user_output_codeblock, user_output_additional_ssn)
    user_flow.edge(user_output_additional_ssn, user_output_health_insurance)
    user_flow.edge(user_output_health_insurance, validate_credentials)
    user_flow.edge(validate_credentials, END)
    
    # Create email records with sensitive tokens
    create_emails_script = aflow.script(
        name="create_email_records",
        display_name="Create Email Records",
        script="""
# Create list of email records with API tokens
self.output.emails = [
    {
        "recipient": flow.input.username + "@example.com",
        "api_token": f"TOKEN-{flow.private.credentials.auth_token[:16]}"
    }
]
"""
    )
    
    # ============================================================
    # FINAL OUTPUT SCRIPT
    # ============================================================
    
    # Final script to prepare output
    prepare_output_script = aflow.script(
        name="prepare_output",
        display_name="Prepare Output",
        script="""
self.output.user_id = flow.private.user_id
self.output.username = flow.input.username
self.output.masked_ssn = flow.nodes['process_user_data'].output.masked_ssn
self.output.processing_notes = [
    "User data processed successfully",
    "Sensitive fields masked"
]
"""
    )
    
    # ============================================================
    # FLOW EDGES
    # ============================================================
    
    # Main flow sequence (Python tool nodes commented out)
    aflow.edge(START, process_data_script)
    aflow.edge(process_data_script, user_flow_form)
    aflow.edge(user_flow_form, process_tool_node)
    aflow.edge(process_tool_node, validate_creds_node)
    aflow.edge(validate_creds_node, user_flow)
    aflow.edge(user_flow, create_emails_script)
    aflow.edge(create_emails_script, prepare_output_script)
    aflow.edge(prepare_output_script, END)


    # ============================================================
    # MASKING CONFIGURATION
    # ============================================================
    
    # Mask input field
    aflow.mask_property("flow.input.ssn", masking_policy=MaskingPolicy.MASK_ALL)
    
    # Mask nested private variable
    aflow.mask_property("flow.private.credentials.auth_token", masking_policy=MaskingPolicy.MASK_FIRST4)
        
    # Mask script node output
    aflow.mask_property(f"flow.{process_data_script.spec.name}.output.masked_ssn", masking_policy=MaskingPolicy.MASK_FIRST4)

    # Mask user flow field
    aflow.mask_property(f"flow.userflow_4.additional_ssn.output", masking_policy=MaskingPolicy.MASK_LAST4, input_policy=InputPolicy.MASK_WHILE_TYPING)
    # Mask form field 
    aflow.mask_property(f"flow.userflow_3.ApplicationForm.output.lastName", masking_policy=MaskingPolicy.MASK_ALL, input_policy=InputPolicy.MASK_WHILE_TYPING)

    # Mask tool outputs (commented out - uncomment when Python tools are enabled)
    aflow.mask_property(f"flow.{process_tool_node.spec.name}.output.health_insurance", masking_policy=MaskingPolicy.MASK_FIRST4)
    aflow.mask_property(f"flow.{validate_creds_node.spec.name}.output.token", masking_policy=MaskingPolicy.MASK_LAST4)

    aflow.mask_property(f"flow.{process_tool_node.spec.name}.output.middle_name", MaskingPolicy.MASK_FIRST4)
    return aflow
See all 292 lines
---

Agentic Workflows
Mapping inputs and outputs
You can manually map the inputs and outputs of your nodes using the map_input() and map_output() methods. To do this, call map_input() or map_output() in your node and provide the following values:
Show `map_input()` Parameters

Show `map_output()` Parameters

The following example shows how to use map_input() and map_output() to map values for a node:
Python
'''
Build a simple hello world agentic workflow that will combine the result of two tools.
'''

from pydantic import BaseModel
from ibm_watsonx_orchestrate.flow_builder.flows import END, Flow, flow, START

from .get_hello_message import get_hello_message
from .combine_names import combine_names

class Name(BaseModel):
    """
    This class represents a person's name.

    Attributes:
        first_name (str): The person's first name.
        last_name (str): The person's last name.
    """
    first_name: str
    last_name: str

class Message(BaseModel):
    msg: str

@flow(
        name = "hello_message_flow",
        input_schema=Name,
        output_schema=Message
    )
def build_hello_message_flow_datamap(aflow: Flow = None) -> Flow:
    """
    Creates an agentic workflow with two tools: get_hello_message and combine_names.
    Args:
        flow (Flow, optional): The agentic workflow to be built. Defaults to None.
    Returns:
        Flow: The created agentic workflow.
    """
    combine_names_node = aflow.tool(combine_names)
    combine_names_node.map_input(input_variable="first_name", expression="flow.input.first_name")
    combine_names_node.map_input(input_variable="last_name", expression="flow.input.last_name", default_value="default_last_name")

    get_hello_message_node = aflow.tool(get_hello_message, output_schema=Message)

    aflow.edge(START, combine_names_node).edge(combine_names_node, get_hello_message_node).edge(get_hello_message_node, END)

flow.map_output(
    output_variable="Type_Justification",
    expression="flow.Type_Classifier_Node.output.justification_text if flow.Classifier_Node.output.justification_text else \"N/A\"")
             
    return aflow
Collapse
Nodes use schemas to define the structure of incoming and outgoing data, ensuring consistent validation and predictable behavior. The following parameters describe how schemas and mapping functions control the flow of data through a node.
Show Schema definitions and data mapping Parameters

The following example shows how a node applies its schema definitions and mapping parameters to process inputs and generate a structured, validated output.
Python

class GEN_AI_NODE(BaseModel):
    description_original: str = Field(description="Formatted description ....", default="")

class JUSTIFICATION_TYPE_RESULT(BaseModel):
    grievance_type_llm: str = Field(description="Type of thing", default="")
    justification_text: str = Field(description="Justification for classified type", default="")

classifier_node = flow.prompt(
      name="Classifier_Node",
      display_name="Classifier_Node",
      description="Type Classifier",
      ...
      input_schema=GEN_AI_NODE,
      output_schema=JUSTIFICATION_TYPE_RESULT)

classifier_node.map_input(input_variable="description_original", expression="flow.Load_Extracted_Data_Node.output.extracted_kvps.Description_Original")
Collapse

---

Agentic Workflows
Testing agentic workflow
After importing an agentic workflow tool, you can test it using a main Python script before add it to an agent. The following steps guide you through testing a flow, including defining, compiling, and running the flow:
1
Create a test script

Agentic workflow are asynchronous, and so are the functions used to run them.
Start by creating a script that defines a function to invoke your agentic workflow. In the example below, the script hello_message_flow.py contains a function build_hello_message_flow, decorated with @flow, which returns the Flow object you want to test.
Python
import asyncio

from .hello_message_flow import build_hello_message_flow

async def main():

    my_flow_definition = build_hello_message_flow()

if __name__ == "__main__":
    asyncio.run(main())  
Collapse
2
Compile the agentic workflow

Next, compile the agentic workflow. This step generates the agentic workflow model and deploys it to the engine. It returns a CompiledFlow instance, which you can use to start an agentic workflow run. Use compile_deploy() to compile and deploy the agentic workflow.
Python
compiled_flow = await my_flow_definition.compile_deploy()
If you only want to generate the JSON model without deploying it, use compile() instead.
3
Start a run

Agentic workflows are asynchronous, and the engine communicates with your client using events. You can start a run using methods on the CompiledFlow object. Depending on your needs, you can choose from the following approaches:
A simple client

The simplest way to run an agentic workflows is to invoke it and wait for the result. Use CompiledFlow.invoke() to start the agentic workflow. You can optionally pass input data.
Python
flow_run = await compiled_flow.invoke({"first_name": "John", "last_name": "Doe"})
Show optional parameters to invoke() function

To monitor the agentic workflow and retrieve the output:
Python
from ibm_watsonx_orchestrate.experimental.flow_builder.flows.flow import FlowRunStatus

# Wait for the flow to complete
while flow_run.status != FlowRunStatus.COMPLETED and flow_run.status != FlowRunStatus.FAILED:
    await asyncio.sleep(1)  # sleep 1 second between checks
    
print(f"Flow ended with status: {flow_run.status}")
print(f"Flow output: {flow_run.output}" if flow_run.status == FlowRunStatus.COMPLETED else f"Flow error: {flow_run.error}")
Collapse
Note: Always use asynchronous waits to avoid blocking the event loop.
Using event handlers

You can provide custom event handlers to invoke() for more control over agentic workflow completion and error handling.
Python
flow_run = None

def on_flow_end(result):
    """
    Callback function to be called when the agentic workflow is completed.
    """
    print(f"Custom Handler: flow `{flow_run.name}` completed with result: {result}")

def on_flow_error(error):
    """
    Callback function to be called when the agentic workflow fails.
    """
    print(f"Custom Handler: flow `{flow_run.name}` failed: {error}")

async def main():

    my_flow_definition = build_hello_message_flow()
    compiled_flow = await my_flow_definition.compile_deploy()
    
    global flow_run
    flow_run = await compiled_flow.invoke({"first_name": "John", "last_name": "Doe"}, on_flow_end_handler=on_flow_end, on_flow_error_handler=on_flow_error)
Collapse
Processing raw events

To handle all emitted events, use invoke_events(), which returns an asynchronous iterator yielding (FlowEvent, FlowRun) tuples.
Python
from ibm_watsonx_orchestrate.experimental.flow_builder.types import FlowEventType

async for event, run in compiled_flow.invoke_events({"first_name": "John", "last_name": "Doe"}):
    if not event:
        continue
    
    if event.kind == FlowEventType.ON_FLOW_END:
        on_flow_end(event.context.data.output)
        print(f"Flow `{run.name}` completed with result: {run.output}")
        break

    elif event.kind == FlowEventType.ON_FLOW_ERROR:
        print(f"Flow `{run.name}` failed with error: {run.error}")
        break 
Collapse
Hide optional parameters to invoke() function

​
input_data
dict
Input data to pass to the agentic workflow.
​
filters
Sequence[Union[FlowEventType, TaskEventType]]
Callback executed when the agentic workflow completes successfully.
​
debug
bool
Callback executed if the agentic workflow encounters an error.
You can listen for task and agentic workflow events, as defined by FlowEventType and TaskEventType in ibm_watsonx_orchestrate.experimental.flow_builder.types.

---

Agentic Workflows
Running agentic workflows with MCP (Public Preview)
This document provides a technical overview of how the Model Context Protocol (MCP) integrates with the flow execution environment. The integration shows flows as standardized tools that can be discovered, started, and managed by MCP‑compatible clients. The design supports synchronous and asynchronous execution, human‑in‑the‑loop interaction through elicitation, and session‑aware operation.
MCP automatically publishes each flow as a set of tools with explicit schemas for inputs and outputs. Tool contracts standardize discovery and invocation. Registration requires a Watson Orchestrate endpoint and an access token that is derived from an API key. The token has a limited validity period and must be refreshed to maintain connectivity.
​
Capabilities
Dynamic tool discovery: Each flow model is shown as multiple MCP tools for synchronous execution, asynchronous execution, and status queries.
Resilient session management: Multi‑session design supports reconnection and cleanup.
Flexible execution: Synchronous (wait for completion) and asynchronous (claim‑check) patterns.
Protocol compliance: MCP over Streamable HTTP transport.
Security: User‑based authorization for all operations.
​
Overview
Tool discovery: Dynamic registration of tools per flow model (synchronous, asynchronous, query) and management tools.
Management tools: subscribe_flow, replay_flow_pending_elicitation, submit_flow_elicitation, list_flows, cancel_flow.
​
Tool registration
The Flow MCP server provides three tools per flow model to support distinct execution patterns. Draft and versioned models obtain separate tools.
Naming convention:
Draft (latest): run_flow_<model_name>
Specific version: run_flow_<model_name>_<version>
Tool metadata Each tool includes a _meta section for lifecycle management:
json
{
  "_meta": {
    "model_id": "string",
    "version": "string",
    "model_name": "string",
    "kind": "string"
  }
}
Collapse
​
Tool 1 Synchronous flow execution (run_flow__<model_name>)
Runs a flow and waits for completion or interruption:
json
{
  "name": "run_flow__purchase_approval",
  "description": "Process a purchase approval request through the approval workflow",
  "inputSchema": {
    "type": "object",
    "properties": {
      "item": { "type": "string", "title": "Item Name" },
      "amount": { "type": "number", "title": "Amount" },
      "justification": { "type": "string", "title": "Justification" },
      "_context": {
        "type": "object",
        "description": "Optional context parameters for flow execution",
        "properties": {
          "thread_id": { "type": "string", "description": "Agent thread ID" },
          "environment_id": { "type": "string", "enum": ["draft", "live"], "description": "Execution environment" },
          "channel_id": { "type": "string", "description": "Request channel" },
          "channel_capabilities": { "type": "array", "items": { "type": "string" } },
          "agent_id": { "type": "string", "description": "Initiating agent ID" },
          "agent_version": { "type": "number", "description": "Caller agent version" }
        }
      }
    },
    "required": ["item", "amount"]
  },
  "outputSchema": {
    "type": "object",
    "properties": {
      "output": {
        "type": "object",
        "properties": {
          "approval_status": { "type": "string", "enum": ["approved", "rejected"] },
          "approver": { "type": "string" },
          "comments": { "type": "string" }
        }
      },
      "status": {
        "type": "object",
        "properties": {
          "instance_id": { "type": "string", "description": "Flow run ID" },
          "name": { "type": "string", "description": "Flow name" },
          "state": { "type": "string", "enum": ["working","input_required","completed","failed"], "description": "Run state" },
          "created_at": { "type": "string", "description": "ISO 8601 create time" },
          "updated_at": { "type": "string", "description": "ISO 8601 last update time" }
        },
        "required": ["instance_id", "state"]
      }
    },
    "required": ["status"]
  }
}
Collapse
​
Behavior
Runs to completion or returns on user input.
Always returns status; includes output only on successful completion with results.
Elicitations are issued automatically when user input is required.
Response examples for flows that complete with output:
json
{
  "isError": false,
  "content": [
    { "type": "text", "text": "<output JSON>" },
    { "type": "text", "text": "The flow returned successfully..." }
  ],
  "structuredContent": {
    "output": {
      "approval_status": "approved",
      "approver": "manager@example.com",
      "comments": "Approved"
    },
    "status": {
      "instance_id": "abc-123",
      "name": "purchase_approval",
      "state": "completed",
      "created_at": "2024-01-01T12:00:00.000Z",
      "updated_at": "2024-01-01T12:05:00.000Z"
    }
  }
}
Collapse
Return for input:
json
{
  "isError": false,
  "content": [
    { "type": "text", "text": "The flow is waiting for user input..." }
  ],
  "structuredContent": {
    "status": {
      "instance_id": "abc-123",
      "name": "purchase_approval",
      "state": "input_required",
      "created_at": "2024-01-01T12:00:00.000Z",
      "updated_at": "2024-01-01T12:03:00.000Z"
    }
  }
}
Collapse
​
Tool 2 Asynchronous flow execution (run_flow_async__<model_name>)
Starts a flow and returns immediately with an instance_id (claim‑check pattern).
Specification:
json
{
  "name": "run_flow_async__purchase_approval",
  "description": "Process a purchase approval request (async)",
  "inputSchema": {
    "type": "object",
    "properties": {
      "item": { "type": "string" },
      "amount": { "type": "number" },
      "justification": { "type": "string" },
      "_context": { }
    },
    "required": ["item", "amount"]
  },
  "outputSchema": {
    "type": "object",
    "properties": {
      "instance_id": { "type": "string", "description": "Started flow instance ID" }
    },
    "required": ["instance_id"]
  }
}
Collapse
​
Behavior
Starts execution in the background and returns instance_id.
Elicitations are issued when user input is required.
Clients query status through query_flow__<model_name>.
Response:
json
{
  "isError": false,
  "content": [
    { "type": "text", "text": "Flow started" }
  ],
  "structuredContent": {
    "instance_id": "flow-abc123-def456"
  }
}
Collapse
​
Tool 3 Flow status query (query_flow__<model_name>)
Retrieves the status and output (if available) for a flow instance.
Specification:
json
{
  "name": "query_flow__purchase_approval",
  "description": "Query status and output by instance ID",
  "inputSchema": {
    "type": "object",
    "properties": {
      "instance_id": { "type": "string", "description": "Flow run ID" }
    },
    "required": ["instance_id"]
  },
  "outputSchema": {
    "type": "object",
    "properties": {
      "output": {
        "type": "object",
        "properties": {
          "approval_status": { "type": "string", "enum": ["approved", "rejected"] },
          "approver": { "type": "string" },
          "comments": { "type": "string" }
        }
      },
      "status": {
        "type": "object",
        "properties": {
          "instance_id": { "type": "string" },
          "name": { "type": "string" },
          "state": { "type": "string", "enum": ["working","input_required","completed","failed"] },
          "created_at": { "type": "string" },
          "updated_at": { "type": "string" }
        },
        "required": ["instance_id", "name", "state", "created_at", "updated_at"]
      }
    },
    "required": ["status"]
  }
}
Collapse
Output is present only when the flow completes with results.
Status is always present and includes execution metadata.
​
Context Parameters
An optional _context object is available for callers to pass in more context, for example, thread_id, environment_id, channel_id, agent_id, agent_version. For the moment, only thread_id (the wxO message thread_id) and environement_id (‘draft’ or ‘live’) are used.
​
Elicitation Handling
When a flow requires user input, an elicitation request is automatically issued to the MCP client. The client must respond within the timeout period to continue flow execution.
​
Timeout behavior
Elicitations timeout after 5 minutes by default.
When a timeout occurs, the elicitation request fails with a timeout error.
​
Recovery from timeout
If an elicitation times out, note the elicitation ID from the original request.
Collect the user’s response.
Call submit_flow_elicitation with the elicitation ID and response data.
The flow resumes execution with the provided input.
Example:
json
{
  "instance_id": "flow-abc123-def456",
  "elicitation_id": "task-789",
  "response": {
    "action": "accept",
    "content": {
      ... response data ...
    }
  }
}
Collapse
​
Dynamic tool lifecycle management
The server updates tool registrations in response to flow model events (create, update, delete, activate, deactivate).
​
Lifecycle states
Active: Tools available and executable.
Deactivated: Tools that are registered but marked unavailable.
Deleted: Tools registered but marked deleted.
​
Behavior
Tools are marked as [DEACTIVATED] or [DELETED] in descriptions when flows are not runnable.
Clients are notified through notifications/tools/list_changed when tool availability changes.
​
Execution patterns
​
Synchronous
Use run_flow__<flow_name>.
Suitable for short‑running flows.
Returns status and, when available, output.
If user input is required, returns input_required and issues elicitation; continue through the background then query with query_flow__<flow_name>.
​
Asynchronous (claim‑check)
Use run_flow_async__<flow_name>.
Returns instance_id immediately; query with query_flow__<flow_name>.
Elicitations are issued as needed; execution continues in the background.
​
Authorization model
Identity: Each request is associated with an authenticated principal.
Ownership: Initiators can list, query, subscribe to, replay elicitations for, and cancel their own flow instances.
Session binding: Operations are validated per session.
Operation checks: Authorization is evaluated for each action (subscribe_flow, replay_flow_pending_elicitation, submit_flow_elicitation, list_flows, cancel_flow).
​
Session management
Unique session IDs per MCP client and clean up on disconnect.
​
MCP Context Forge support
The flow MCP server is compatible with MCP Context Forge for enhanced context management and orchestration. Current Context Forge clients do not support MCP elicitations; human‑in‑the‑loop features are not available through that path. For more information see, MCP context forge.
​
Connecting to Flow MCP Server
To connect to the Flow MCP server as a remote MCP endpoint, obtain the Watson Orchestrate API endpoint for your instance (https://api.<hostname>/instances/<tenant_id>) and append /v1/orchestrate/flows/mcp. Generate an access token from an API key that uses the documented process and provide it during registration. The access token has a limited validity period, refresh and reregister when it expires.

---

Agentic Workflows
Agentic workflow expressions
When working with agentic workflows, expressions used in branching, looping, and data mapping must follow a defined syntax. This structure also applies to the generated data map within the model.
Below are the keywords and reference patterns used in agentic workflow expressions:
Refers to the top-level agentic workflow context:
Python
flow
Refers to the parent context, equivalent to the top-level agentic workflow for nodes within it:
Python
parent
Refers to the current node:
Python
self
Refers to inputs and outputs of the current agentic workflow within agentic workflow nodes:
Python
parent.[input|output].<name>
parent.[input|output]["<name>"]
Refers to the current index in a foreach loop, returns null if not in a loop:
Python
parent._current_index
Refers to the current item in a foreach loop, returns null if not in a loop:
Python
parent._current_item
Refers to inputs and outputs of other nodes within the current agentic workflow:
Python
parent.<nodeName>.[input|output].<name>
parent["<nodeName>"].[input|output]["<name>"]
Refers to inputs of the current node:
Python
self["input"].<name>
self["input"]["name"]


---

Agentic Workflows
Handling errors
Error handling allows you to control how an agentic workflow responds when a node fails. Instead of stopping execution, you define how the agentic workflow flow reacts. You can retry the node, show a message to the user, or redirect execution to another path. This approach helps you design agentic workflows that handle failure explicitly and predictably.
You configure error handling per node by using the NodeErrorHandlerConfig class. You can attach this configuration to both tool nodes and agent nodes.
NodeErrorHandlerConfig defines how a node behaves when an execution error occurs. It controls retry behavior, error messaging, and redirection within the agentic workflow flow.
When you attach this configuration to a node, you allow the flow engine to evaluate errors at runtime and decide how execution continues.
To configure error handling, create a NodeErrorHandlerConfig instance and pass it to a node when you call tool() or agent() in your agentic workflow.
Python
aflow.tool(
    "someTool",
    error_handler_config=NodeErrorHandlerConfig(
        on_error="branch",
        error_edge_id="some_error_edge"
    )
)
Parameters:
​
error_message
required
Describes the error that occurred.
The flow engine logs this message for observability and debugging.
The agentic workflow flow does not display this message to the user unless you explicitly expose it through a user flow or UI element.
​
max_retries
required
Specifies how many retry attempts occur after a failure.
If you set this value to 0, the node follows the configured error behavior immediately.
If you omit this value, the platform default retry behavior applies.
​
retry_interval
required
Defines the delay between retries in milliseconds.
This setting applies only when max_retries is greater than 0.
​
on_error
required
Defines how the agentic workflow flow responds when the node fails.
Supported values:
show_message: Stops the agentic workflow after displaying an error message to the user. Use this option when no alternate path applies.
branch: Redirects the agentic workflow flow to an alternate path using the edge specified by error_edge_id. Use this option to handle expected failures, guide users to a recovery path, or invoke fallback logic when tools or external services return errors. This option suits agentic workflows that rely on services with variable availability.
​
error_edge_id
required
Specifies the edge that execution follows when on_error="branch" is set.
This value must match an edge defined with aflow.edge(...).
If no matching edge exists, the agentic workflow fails during validation or execution.
The following example shows an agentic workflow that retrieves dog facts. When the tool fails, the agentic workflow flow redirects execution to a user flow that displays an error message.
Python [Expandable]
"""
Error Branching Example Flow
"""

from pydantic import BaseModel, Field
from ibm_watsonx_orchestrate.flow_builder.flows import (
    Flow, flow, START, END
)
from ibm_watsonx_orchestrate.flow_builder.types import (
    UserFieldKind,
    NodeErrorHandlerConfig
)

class PetFacts(BaseModel):
    facts: list[str] = Field(description="A list of facts about the pet")

@flow(
    name="get_pet_facts_error_branching",
    output_schema=PetFacts,
    description="Shows a user message when fetching dog facts fails"
)
def build_get_pet_facts_error_branching_flow(aflow: Flow) -> Flow:

    # User flow that displays an error message
    user_flow = aflow.userflow()

    error_message_node = user_flow.field(
        direction="output",
        name="error_display",
        display_name="Error Message",
        kind=UserFieldKind.Text,
        text="Sorry, we couldn't fetch dog facts at this time. Please try again later."
    )

    user_flow.edge(START, error_message_node)
    user_flow.edge(error_message_node, END)

    # Tool node with error handling
    dog_fact_node = aflow.tool(
        "getDogFact",
        error_handler_config=NodeErrorHandlerConfig(
            error_message="Dog facts retrieval failed; redirecting to user message",
            max_retries=0,
            retry_interval=1000,
            on_error="branch",
            error_edge_id="dog_error_to_user_message"
        )
    )

    # Main execution path
    aflow.sequence(START, dog_fact_node, END)

    # Error branching path
    aflow.edge(dog_fact_node, user_flow, id="dog_error_to_user_message")
    aflow.edge(user_flow, END)

    return aflow
Collapse


---

