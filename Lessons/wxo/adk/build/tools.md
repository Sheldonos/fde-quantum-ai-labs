Tools
Overview
Tools are essential components of agents, enabling them to perform actions such as querying data, creating documents, or executing transactions on behalf of users. Some tools might require a connection to work properly.
The watsonx Orchestrate ADK includes a set of built-in tools you can use in agents. These tools are versatile and apply to many scenarios.
You can also create custom tools with ADK when needed. Custom tools can come from:
OpenAPI Use OpenAPI tools to quickly consume remote web services that include an OpenAPI specification file on watsonx Orchestrate. For more information, see Authoring OpenAPI based tools.
Python Python tools give you flexibility and power to extend agent functionality in watsonx Orchestrate, especially when combined with agentic workflows. For more information, see Authoring Python-Based Tools.
Agentic workflows An agentic workflow acts as a tool with built-in agentic capabilities and automations. It supports complex orchestration of multiple agents, tools, and people. For more information, see Authoring agentic workflow tools.
Langflow Langflow lets you visually design, test, and deploy AI applications with a drag-and-drop interface. You can build tools in Langflow and then import them into watsonx Orchestrate. For more information, see Authoring Langflow tools.
ADK also lets you manage tools in your active environment. You can list, export, update, and delete tools. For more information, see Managing tools.

---

Tools
Authoring OpenAPI based tools
OpenAPI tools provide a quick way to consume remote web services that include an OpenAPI specification file.
For watsonx Orchestrate to use an OpenAPI tool, the following conditions must be met:
Endpoints must accept and return JSON.
The specification must include a servers block with exactly one URL. This URL cannot contain parameterization.
Each path that exposes an endpoint must include an operationId. This value becomes the tool name. For best results, use snake_case for operationId values.
Each path that exposes an endpoint must include a description. The agent uses this description to decide when to use the tool and what the tool does.
The OpenAPI version must be 3.0.
Here is an example of a minimal OpenAPI specification:
YAML
servers:
- url: mytoolserver
paths:
/:
   get:
      operationId: my_tool
      description: The description of the tool that clearly explains its purpose to an LLM
      requestBody:
         ...
      responses:
         ...
​
Importing OpenAPI based tools
To import an OpenAPI tool, run:
BASH
orchestrate tools import -k openapi -f <file-path> -a <app-id>
Show command flags

​
Additional features of OpenAPI tools
Securely providing credentials

Asynchronous tools with callbacks

​
Limitations and considerations
Using OpenAPI tools with your agents is straightforward, but default OpenAPI specifications often perform poorly as agent tools for the following reasons. If any of these issues apply to your use case, consider adjusting your OpenAPI specification or using Python tools instead.
OpenAPI endpoints are designed for developers, not agents.
Developers can rely on context from other endpoints and external documentation to understand an endpoint’s purpose. Agents cannot. All necessary context must be included within the endpoint itself.
OpenAPI endpoints often include large sets of input arguments. In contrast, tools should have focused inputs and outputs that resolve a single task. For more information, see Designing agents and tools for best performance .
Agents require a highly descriptive semantic layer.
OpenAPI tools do not support x-ibm- extensions used in older watsonx Orchestrate Skills.


---

Authoring Python-Based Tools
Authoring Python-Based Tools
Python tools are one of the most flexible and powerful ways to extend agent functionality in watsonx Orchestrate, especially when combined with agentic workflows.
A Python tool consists of one or more Python files. Within these files, you define one or more functions and annotate them with the @tool decorator to expose them to Orchestrate.
Each Python tool runs inside an isolated container with its own virtual environment. This design keeps your code and dependencies separate from the host operating system, so you work in a secure and consistent runtime while focusing on your agent’s goal.
Python tool example
Python
#test_tool.py
from ibm_watsonx_orchestrate.agent_builder.tools import tool


@tool()
def my_tool(input: str) -> str:
    """Executes the tool's action based on the provided input.

    Args:
        input (str): The tool's input.

    Returns:
        str: The tool's output.
    """

    #functionality of the tool

    return f"Hello, {input}"
Hide detailed @tool parameter descriptions

​
name
string
The unique name of the tool as it would be referenced by your agent.
This defaults to the name of your python function.
​
display_name
string
The name of the tool as it shows up within the “Manage Agents” UI.
​
description
string
Provides a summary of the tool’s purpose and functionality. This description helps the LLM determine when and how to use the tool effectively.
By default, this text is automatically generated from the tool’s docstring, but you can override it here if needed.
​
expected_credentials
List[ExpectedCredentials]
Specifies a list of connections along with their expected connection types. Any connection required during the tool’s execution must be included in this list. This ensures that all necessary connections are properly defined and bound to the tool at import time.
Show ExpectedCredentials

​
kind
PythonToolKinddefault:"PythonToolKind.TOOL"
The kind of Python tool. Set it to PythonToolKind.TOOL for general-purpose tools.
This controls the type of schema validation that is done on the tool during import time.
​
input_schema
object
The JSON Schema that the tool’s input conforms to. The JSON Schema is always defined as an object for each of the keyword arguments of the tool and is inferred automatically by the typings of the Python function.
The description of each argument will be extracted from the docstring (see below note about compatible docstring types).
The type of each argument will be inferred from the field’s typings or pydantic type.
The generated value can be inspected by running orchestrate tools list -v.
​
output_schema
object
The JSON Schema that the tool’s output conforms to. This is automatically inferred from the return type of the function using either typings or pydantic.
The generated value can be inspected by running orchestrate tools list -v.
​
permission
ToolPermissiondefault:"ToolPermission.READ_ONLY"deprecated
This field is used to determine whether or not an agent would confirm each action before performing it, if the type was not ToolPermission.READ_ONLY.
This behavior has been deprecated and removed; it no longer occurs.
Best Practices:
Use Google-style docstrings to apply descriptions and document the Python tool.
For compute/memory capabilities of the containers in which the python tools run.
For more information, see Python tool design principles.
​
Auto-discover
The ADK can convert ordinary Python files into Python tools that are ready to be uploaded to Orchestrate. The process automatically imports and adds a @tool decorator and generates a docstring for functions in the source file.
For docstring generation, an LLM is invoked, so the command requires an environment (.env) file with valid credentials for Groq, watsonx, or Orchestrate. To convert a Python file, use the following command:
BASH
orchestrate tools auto-discover --file path\to\python\file --output path\to\output\file --env-file .env --llm groq/openai/gpt-oss-120b --function name_of_function1 --function name_of_function2
The command takes the following arguments:
Show Arguments

The auto-discover feature is standalone but also bundled with the import process.
This option takes all the flags of the standalone auto-discover command except --output.
The ADK runs the auto-discover process and uploads the results instead of writing to a file.
If you are using AI Gateway, the model name must start with virtual-model or virtual-policy and you must pass it with the —llm flag.
The auto import process does not support toolkit imports. To complete your import, generate the output file and then run the toolkit import command.
​
Importing Python-based tools
You can import Python-based tools in two forms: as an individual tool or as a toolkit. When you import a tool as an individual tool, you add a single Python tool to watsonx Orchestrate and manage it independently. When you import tools as a toolkit, you group multiple Python tools into one toolkit and manage them together as a single unit.
Choosing between standalone tools and toolkits:
The choice between standalone Python tools and Python toolkits significantly impacts performance and operational characteristics:
Standalone Python tools:
Process-per-invocation model (~100-300ms overhead per call)
Supports non-thread-safe operations
Suitable for infrequent calls or prototyping
Python toolkits:
Shared process model (no process overhead after startup)
Requires thread-safety
Better performance for frequently called tools
Dedicated resources in live premium environments
For detailed guidance on choosing the right approach, see Choosing a tool type.
For step-by-step migration from standalone tools to toolkits, see Migrating to Python toolkits.
Importing Python toolkits
Importing individual Python tools
After you create your Python tools, import them as a Python toolkit. A Python toolkit groups related tools so you can deploy and run them together in a single Python process. To meet this goal, design every tool in the toolkit to be thread-safe and reentrant. This approach gives you faster execution because the tools share the same process.
When you run Python tools outside a toolkit (as standalone Python tools), the system starts a lightweight process each time the tool runs. This design supports tools that use non-thread-safe operations, but it increases execution time by approximately 100-300ms per invocation compared to a toolkit.
When to use Python toolkits vs standalone Python tools:
Use Python toolkits when you have multiple related tools that are thread-safe, called frequently, or share dependencies
Use standalone Python tools when tools use non-thread-safe operations, are called infrequently, or need process isolation
For detailed guidance, see Choosing a tool type.
To create a Python toolkit, place all required Python tools in one folder. Each tool can include one or more Python files. In those files, define your functions and apply the @tool decorator so watsonx Orchestrate exposes each function as a usable tool.
You can place tools that multiple agents use into a single toolkit. When you update tools inside a toolkit, redeploy all related agents to the live environment so you use the updated versions. Choose the number of tools in each toolkit based on the level of concurrent requests you expect. For more information, see CPU and memory allocation for Python toolkits.
​
CPU and memory allocation for Python toolkits
Draft environment:
All imported Python toolkits and Python tools run in a single Kubernetes deployment container per tenant
Process overheads per tool call exist in draft (approximately 100-300ms per invocation)
Container resources: 2 vCPUs, 2 GB of memory, and 5 workers
Deployment supports two replicas
Live environment (Premium plan):
You can import up to five Python toolkits per tenant
Each toolkit runs in its own dedicated Kubernetes deployment container
No process overheads per tool call — tools run in a persistent process
Container resources per toolkit: 2 vCPUs, 2 GB of memory, and 5 workers
Each deployment supports two replicas
Supports up to 10 concurrent requests per toolkit (5 workers × 2 replicas)
Live environment (Non-Premium plan):
--tier is not enabled by default — contact support to request access.
Performance optimization: In live premium environments, Python toolkits eliminate process startup overhead, reducing tool execution time by 100-300ms per call compared to standalone Python tools. For frequently called tools (>10 calls/minute), this can significantly improve agent response times.
​
Add Python toolkits using the ADK CLI
Use the orchestrate toolkits add command to add a Python toolkit.
BASH
orchestrate toolkits add \
  --kind python \
  --name <toolkit-name> \
  --description <toolkit-description> \
  --tier <deployment-tier> \
  --package_root <toolkit-path>
Note:
--tier is required when importing a Python toolkit. Premium plan customers only — contact support to request access.
Show command flags

​
Import Python toolkits from a file
You can also import a Python toolkit from a YAML file. This file defines the same configuration options as the add command and fits well into import scripts and CI/CD pipelines.
Use the orchestrate toolkits import command to import a toolkit from a file.
BASH
orchestrate toolkits import -f <path to spec> --app-id <connection>
Show command flags

For the YAML file, configure the following:
​
spec_version
stringrequired
The version of the YAML specification.
​
kind
stringrequired
The type of toolkit. For Python toolkits, use python.
​
name
stringrequired
The name of the toolkit.
​
description
string
The description of the toolkit.
​
environment
object
Key-value pairs for the toolkit.
Example:
toolkit_name.yaml
spec_version: v1
kind: python
name: toolkit_name
description: A toolkit sample
environment:
    key1: value1
​
Thread-safety requirements
All tools in a Python toolkit must be thread-safe because they run in a shared process with concurrent requests. A tool is thread-safe when multiple threads can call it simultaneously without causing race conditions or data corruption.
Thread-safe patterns:
No global mutable state
Use immutable data structures
Use thread-safe libraries
Non-thread-safe patterns to avoid:
Global variables that change
File system writes
Non-thread-safe libraries
Shared database connections without pooling
For detailed guidance on thread-safety and migration from standalone tools, see Migrating to Python toolkits.
​
Additional features of Python tools
Adding Dependencies

If your Python function relies on external libraries or packages, specify these dependencies in the requirements.txt file to make sure your tool runs correctly.
Important: Dependencies listed in requirements.txt are source specifications only — they define which packages to install, not the binary packages themselves. The actual packages are downloaded and installed server-side at deployment time. For details, see Python dependency management.
When you import Python-based tools, watsonx Orchestrate validates all packages against a tenant-specific Python package allowlist. This validation limits installations to approved packages only.
During import, watsonx Orchestrate verifies each dependency and version in requirements.txt against the allowlist. If the allowlist lacks a required package or the exact version you specify, the import fails. watsonx Orchestrate runs this validation only at import time. To add or update allowed Python packages, configure the Python tool allowlist through the API. Fore more information see Package Configuration.
To complete a successful import, follow these rules:
Declare every dependency in requirements.txt.
Pin each dependency to an exact version, using this format:
requirements.txt
package_name==exact_versionMostrar mais linhas
Use this format in:
requirements.txt
The tenant allowlist configuration
Add all transitive dependencies to the allowlist.
Notes:
watsonx Orchestrate does not revalidate tools that you already imported when the allowlist changes.
When allowlist validation is enabled and the allowlist is empty, you cannot use any Python packages.
Removing all packages from the allowlist does not turn off validation.
Python tool example
Python
import requests
from ibm_watsonx_orchestrate.agent_builder.tools import tool


@tool
def fetch_url(endpoint: str) -> str:
    """Executes a GET request against a given endpoint to fetch its contents.

    Args:
        endpoint (str): the url to fetch

    Returns:
        str: the contents of the page
    """

    #functionality of the tool

    return requests.get(endpoint).text
requirements.txt example
TEXT
requests==2.32.4
Enterprise requirements.txt with private registry (Example only, not actual URL)
TEXT
--index-url https://artifactory.example.com/api/pypi/python-virtual/simple
ibm-watsonx-orchestrate==2.4.0
requests==2.32.4
For more information on the format of a requirements file, see the official pip documentation. For enterprise patterns including Artifactory configuration and hash-based verification, see Python dependency management.
When importing your tool, specify the requirements.txt file by using the -r flag.
BASH
orchestrate tools import -k python -f my-tool.py -r requirements.txt
Using complex input and output argument types with Pydantic

Python tools support input and output arguments based on the following types:
any native Python type from the typings package
classes which extend BaseModel from the popular library Pydantic
Enum types
NaN and Infinity values
Dataclasses
Custom objects with __dict__ attribute
Example
PYTHON
import requests
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic import BaseModel

class InputExample(BaseModel):
    sample: Optional[str] = Field(None, description="description of my field")

class OutputExample(BaseModel):
    result: Optional[str] = Field(None, description="description of my result field")

@tool
def fetch_url(example: InputExample, endpoint: str) -> OutputExample:
    """Executes a GET request against a given endpoint to fetch its contents.

    Args:
        example: An example input object that takes a sample
        endpoint: an example endpoint

    Returns:
        OutputExample: the example output
    """

    #functionality of the tool

    return OutputExample(result=requests.get(endpoint).text)
Securely providing credentials

Python tools are compatible with the watsonx Orchestrate Connections framework. A connection represents a dependency on an external service and are a way to associate credentials to a tool such as those for Basic, Bearer, API Key, OAuth, or IDP SSO based authentication flows. Python tools also support key_value connections which as the name implies are arbitrary dictionaries of keys and values which can be used to pass in credentials for any authorization scheme which does not match one of the existing native schemes.
Connections are referenced by something known as an application id (or app_id). This app_id is the unique identifier of a connection. OpenAPI connections can have at most one Connection’s app_id associated to them.
For more information, see Connections, and the expected_credentials input to the @tool annotation.
Creating multi-file Python tool packages

In addition to importing a single tool file, it is possible to import an entire folder (package) along with your tool file. This is useful when you wish to centralize logic into shared utility libraries, for example, shared authentication, data processing, or including static files such as CSVs or sqlite databases.
Assuming a folder structure as follows:
─── my_agentic_project/
    └── tools/
        └── multi_file_tool/
            └── utils/
               └── csv_utils.py
               └── __init__.py
            └── my_tool.py
            └── my_data.csv
            └── requirements.txt
my_tool.py:
PYTHON
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from os import path
import pandas as pd
from .utils.csv_utils import parse_csv # this is a relative import of my csv_utils.py file I included in this package

@tool
def return_file_contents() -> str:
    """
    Gets the contents of my super important csv file as a table.

    Returns:
        str: the contents of the csv
    """
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = path.join(base_path, 'my_data.csv')
    dataframe: pd.DataFrame = parse_csv(file_path)

    return dataframe.to_markdown() # note dataframe output is unsupported, but dataframe.to_markdown will render a table in a format which the ui knows how to render
Importing your multi-file Python tool:
Assuming your CLI was currently in the my_agentic_project folder, this tool could be imported using the following:
BASH
orchestrate tools import -k python \
    -p tools/multi_file_tool \
    -f tools/multi_file_tool/my_tool.py \
    -r tools/multi_file_tool/requirements.txt
Notes:
Only tools defined in my_tool.py will be imported. Other Python files in the package will not be scanned for tools.
The system will only accept strings composed of alphanumeric characters and underscores (_) in the name attribute of the @tool decorator in my_tool.py.
The system will only accept tool file names composed of alphanumeric characters and underscores (_).
The package root folder and the tool file path CLI arguments MUST share a common base path.
The path of the tool file folder relative to the package root folder, must be composed of folder names which are only composed of alphanumeric characters and underscores (_).
Any whitespace like characters which prefix or suffix provided package root path will be stripped by the system.
A package root folder path that resolves to an empty string will make the system assume that no package root was specified. Then, the system falls back to single Python file tool import.
Limitations:
The max compressed tool size: 50Mb
File resolution for non-python packages must be done relative to the current file, as seen above
Imports to packages within your code must be resolved relatively
Creating tools that accept files

You can create Python tools that accept files or return files to download.
To do that, you must comply with the following requirements:
To accept files as input, the tool must accept a sequence of bytes as arguments.
To return a file for download, the tool must return a sequence of bytes as output.
The following example accepts a file as input and returns the processed file for download:
Python
from typing import Union
from io import BytesIO
from typing import Any
from ibm_watsonx_orchestrate.agent_builder.tools import tool
import base64

@tool
def create_image_with_filter(name: str, age: int, image_bytes: bytes) -> bytes:
    """Gets user information, applies a filter to the image, and returns the processed image.

    Args:
        name (str): The user's name.
        age (int): The user's age.
        image_bytes (bytes): The original image in bytes format.

    Returns:
        bytes: The processed image in bytes format.
    """

    import cv2
    import numpy as np
    from typing import Union
    from io import BytesIO
    # Convert bytes to numpy array
    image_array = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    if image is None:
        raise ValueError("Invalid image bytes provided")

    # Apply bilateral filter for smoothing while preserving edges
    smooth = cv2.bilateralFilter(image, d=9, sigmaColor=75, sigmaSpace=75)

    # Convert to grayscale and detect edges
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.medianBlur(gray, 7)
    edges = cv2.adaptiveThreshold(
        edges, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY, blockSize=9, C=2
    )

    # Convert edges to color image
    edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    # Combine smoothed image with edges
    cartoon = cv2.bitwise_and(smooth, edges_colored)

    # Enhance color saturation
    hsv = cv2.cvtColor(cartoon, cv2.COLOR_BGR2HSV)
    hsv[..., 1] = cv2.multiply(hsv[..., 1], 1.4)  # increase saturation
    cartoon_enhanced = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    # Convert back to bytes
    success, buffer = cv2.imencode('.jpg', cartoon_enhanced)
    if not success:
        raise RuntimeError("Failed to encode image")

    return buffer.tobytes()
See all 58 lines
Use the WXOFile parameter type when a tool must reference a file without processing its full content.
The WXOFile class provides methods to retrieve file properties or content as needed.
You can call the following methods:
get_file_name(url: str) → str | None

get_file_size(url: str) → int | None

get_file_type(url: str) → str | None

get_content(url: str) → bytes

Use the MultiFileConstraints class with WXOFile to set limits and validation rules for selecting or uploading multiple files.
It includes these attributes:
Attributes

Use this approach when a tool only needs file metadata or to read the content on demand. It helps reduce processing overhead and improves performance.
The method signature get_file_metadata(url: str, session_id: str) -> str is deprecated for single‑file uploads. Use WXOFile as the file parameter type instead. To access the updated authentication flow, update ibm-watsonx-orchestrate to the latest version in your requirements.txt.
Single-File upload
Multi-File upload
Python
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission, WXOFile


@tool(permission=ToolPermission.READ_ONLY)
def get_file_metadata(wxo_file: WXOFile, session_id: str) -> str:
    """This tool receives a file reference and a session id and outputs the file's metadata with the session id.

    Args:
        wxo_file (WXOFile): a file input URL reference
        session_id (str): a session ID

    Returns:
        str: A string containing the file name, size and type with the session ID
    """

    filename = WXOFile.get_file_name(wxo_file)
    file_size = WXOFile.get_file_size(wxo_file)
    file_type = WXOFile.get_file_type(wxo_file)
    file_content = WXOFile.get_content(wxo_file) # content in bytes

    return f"File name: {filename}, File size: {file_size}, File type: {file_type} for session ID: {session_id}"
See all 21 lines
Creating tools that return inline tables, images or links

The native watsonx Orchestrate web chat supports Markdown rendering. To ensure correct formatting, the LLM can be instructed to return output in Markdown. In some cases, however, it is more efficient for the tool to return the expected output directly, reducing the amount of transformation required by the LLM.
Inline tables
PYTHON
from ibm_watsonx_orchestrate.agent_builder.tools import tool
import textwrap


@tool
def return_file_contents() -> str:
    """
    Renders a markdown table

    Returns:
        str: the markdown table
    """

    return textwrap.dedent('''
    | a | b | c |
    | -- | -- | -- |
    | value1 | value2 | value3 |
    | value1 | value2 | value3 |
    ''')
Links
PYTHON
from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool
def return_link() -> str:
    """
    Renders a link

    Returns:
        str: the link
    """

    return 'Navigate to [IBM.com](http://ibm.com)'
Images
PYTHON
from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool
def return_image() -> str:
    """
    Renders an image

    Returns:
        str: the image
    """

    return 'Check out this image\n ![alt text](https://mintlify.s3.us-west-1.amazonaws.com/ibm-2e3153bf/assets/agents/deploy-agent.png)'
Using Context Variables

If your agent has access to context variables, provided either by the default context or by passing context with the request, you can use these variables within your Python tool.
Tool type support:
Only Python tools and agentic workflows support reading and updating context variables. All other tool types cannot access the run context.
To do this you will need to pass an AgentRun object parameter to the Python tool:
Get context variables:
Python
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from ibm_watsonx_orchestrate.run.context import AgentRun

@tool
def context_example(context : AgentRun) -> str:
    """
    Retrieves the user's email.

    Args:
        context (AgentRun): The agent run context containing request metadata.

    Returns:
        str: A formatted string displaying the user's email.
    """

    req_context = context.request_context

    user_email = req_context.get('wxo_email_id')

    return f"Context Data: {user_email}"
See all 20 lines
Update context variables:
Python
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from ibm_watsonx_orchestrate.run.context import AgentRun

@tool
def update_user_context(context: AgentRun, user_age: int, user_login: str, user_password: str) -> str:
    """
    Demonstrates two ways to set context variables:
    - Set user_age individually via item assignment (single key).
    - Set user_login and user_password together via update() (bulk).

    Args:
        context (AgentRun): The agent run context containing request metadata.
        user_age (int): The user's age to store.
        user_login (str): The user's login identifier.
        user_password (str): The user's password.

    Returns:
        str: Confirmation with the updated values.
    """
    req_context = context.request_context

    # --- Single-key assignment (ideal for one value)
    req_context["user_age"] = user_age

    # --- Bulk update for multiple related keys
    req_context.update({
        "user_login": user_login,
        "user_password": user_password,
    })

    # Read back to confirm
    age = req_context.get("user_age")
    login = req_context.get("user_login")
    password = req_context.get("user_password")

    return (
        "Context updated -> "
        f"user_age: {age}, "
        f"user_login: {login}, "
        f"user_password: {password}"
    )

See all 42 lines
System and custom variables
Context variables are either system variables or custom variables. System variables use the reserved wxo_ prefix and are populated automatically by the platform on every run. Custom variables are defined and supplied by your application. For details, see Types of context variables.
Naming convention for context variables
Follow the standard naming rules for custom context variables. For details, see Naming rules.
Scope and persistence
Context is scoped to a single run and is not persisted across turns in a thread. For details and persistence strategies, see Persisting context across turns.
Channel support
Channels might not support context-variable propagation. For details, see Channel support.
Tool constraints
A tool can have only one AgentRun parameter. A tool with more than one fails to import.
System variables (wxo_*) cannot be updated by tools.
Dynamic input and output schemas

In integration-heavy environments, schemas change frequently. Dynamic input and output schemas enable select fields in a tool’s input to be mutable at runtime—securely and predictably—without affecting immutable core fields.
Use dynamic it when:
You need to add new attributes to objects (e.g., CRM records).
You need a small number of user-defined fields beyond a stable core API.
You want Builder UI users to change types (e.g., string → number) for dynamic fields only.
Avoid it when:
All fields are stable and tightly coupled to a known data model.
You need complex nested modifications (Phase 1 supports flat properties only in most scenarios).
Python
from ibm_watsonx_orchestrate.agent_builder.tools import tool


@tool(
    enable_dynamic_input_schema=True,  # if false, dynamic_input_schema is ignored
    dynamic_input_schema={  # this is the schema of the kwargs
        'type': 'object',
        'properties': {
            'c': {'type': 'integer', 'description': 'The third integer to add'}
        },
        'required': []
    },
    dynamic_output_schema={  # this is the schema of the kwargs
        'type': 'object',
        'properties': {
            'sum': {'type': 'integer', 'description': 'The sum of a, b and c'},
            'c': {'type': 'string', 'description': 'The third integer to add'}
        },
        'required': []
    }
)
def add_kwargs(a: int, b: int, **kwargs) -> dict:
    """
    Receive required three inputs as a, b, c.
    Adds them and returns the result.

    Args:
        a (int): The first integer to add.
        b (int): The second integer to add.


    Returns:
        int: The sum of `a` and `b`.

    Example:
        >>> add_two_numbers(3, 5)
        8
    """
    sum = a + b + kwargs.get("c", 0)
    return {'sum': sum, 'c': kwargs.get("c", 0)}


if __name__ == "__main__":
    print(add_kwargs(1, 2, c=3))
Python
from ibm_watsonx_orchestrate.agent_builder.tools import tool


@tool(
    enable_dynamic_input_schema=True,  # if false, dynamic_input_schema is ignored
    dynamic_input_schema={  # this is the schema of the kwargs
        'type': 'object',
        'properties': {
            'c': {'type': 'string', 'description': 'The third word'}
        },
        'required': []
    },
    dynamic_output_schema={  # this is the schema of the kwargs
        'type': 'object',
        'properties': {
            'message': {'type': 'string', 'description': 'The message that combines a, b and c'},
            'c': {'type': 'string', 'description': 'The third word'}
        },
        'required': []
    }
)
def combine_words(a: str, b: str, **kwargs) -> dict:
    """
    Receive required three inputs as a, b, c.
    Combine them and returns the result.

    Args:
        a (string): The first word.
        b (string): The second word.


    Returns:
        message: The message combines `a` and `b`.

    Example:
        >>> combine_words("hello", "world")
        "helloworld"
    """
    message = a + b + kwargs.get("c", "")
    return {'message': message, 'c': kwargs.get("c", "")}


if __name__ == "__main__":
    print(combine_words("hello", "world", c="Hana"))
Creating tools that can trigger citations

Create tools that trigger citation generation so Agents provide source references in their responses. Use the ToolResponseFormat.CONTENT_AND_ARTIFACT response format and return both the main content and an artifact that contains citation data.
Example:
Python
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolResponseFormat

@tool(response_format=ToolResponseFormat.CONTENT_AND_ARTIFACT)
def search(query):
    """Searches for information and returns results with citations.

    Args:
        query (str): The search query.

    Returns:
        tuple: A tuple containing (content, artifact) where artifact includes search results and citation information.
    """
    content = "some content"
    artifact = {
        "search_results": [
            {"title": "some title", "body": "some text"}
        ],
        "citations_shown": -1
    }
    return content, artifact
Artifact attributes:
​
search_results
list
A list of search result objects that support citation creation. Each object includes:
title (string): Title of the source.
body (string): Content or excerpt from the source.
​
citations_shown
integerdefault:-1
Controls how many citations to display.
Use -1 to show every citation (default).
Use 0 or a positive number to limit the count.
Creating a form tool

This feature is a preview feature. There are some known bugs which will be resolved in upcoming releases.
Create a tool that returns a form with interactive widgets to collect structured input from users. Define the form by using FormWidget and input components such as TextInput and DatePicker. Return the form through a ToolResult so it renders in the user interface.
For more information, see Tool response and annotations.
Hide Example

PYTHON
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from ibm_watsonx_orchestrate.run.widgets.forms.types import (
    FormWidget, TextInput, TextArea, RadioButton, Checkbox, 
    ComboBox, NumberInput, DatePicker, DateRangePicker,
    FileUpload, Table, TableHeader
)
from ibm_watsonx_orchestrate.run.tool_result import ToolResult, TextContent, Annotations, Role

@tool(
    name="simple_test_form",
    description="Show a simple test form"
)
def simple_test_form():
    """
    Returns a minimal form widget.
    """

    form = FormWidget(
        title="Simple Test Form",
        description="A minimal test form",
        inputs=[
            TextInput(
                name="name",
                title="Name",
                placeholder="Enter your name",
                required=True
            ),
            TextInput(
                name="email",
                title="Email",
                placeholder="Enter your email",
                required=True
            ),
            DatePicker(
                name="date",
                title="Date",
                required=False
            )
        ]
    )

    tool_result = ToolResult(
        content=[
            TextContent(
                text="Please fill out this simple test form.",
                annotations=Annotations(audience=[Role.USER])
            )
        ],
        widget=form
    )

    return tool_result
Hide Form Fields

TextInput

Use to gather basic textual information such as names and emails.
Text Input Input
TextInput(
    name="first_name",
    title="First Name",
    placeholder="Enter Your First Name...",
    description="Your full legal name as it appears on your passport or government issued ID",
    required=True
)
Show Parameters

TextArea

Use to gather long textual information.
Text Area Input
TextArea(
    name="complaint",
    title="Complaint Details",
    placeholder="Please detail your complaint here",
    required=True
)
Show Parameters

RadioButton

Use to gather a singular choice from a user.
Radio Button Input
RadioButton(
    name="title",
    title="Title",
    description="Your preferred prefix title for your name.",
    required=True,
    options=["mr", "ms", "mrs", "dr", "n/a"],
    option_labels=["MR", "MS", "MRS", "DR", "Prefer not to say"]
)
Show Parameters

Checkbox

Use to gather boolean choices from the user.
Checkbox Input
Checkbox(
    name="marketting_signup",
    title="Would you like to recieve marketting emails",
    default_value=False
)
Show Parameters

ComboBox

Dropdown field used for gathering a single user choice
Combo Box Input
ComboBox(
    name="department",
    title="Department",
    options=["finance", "hr", "software", "consulting"],
    option_labels=["Finance", "HR", "Software", "Consulting"]
)
Show Parameters

NumberInput

Use to gather numberical data from a user.
Number Input
NumberInput(
    name="quantity",
    title="Quantity",
    required=True,
    default_value=0,
    minimum=0,
    maximum=10
)
Show Parameters

DatePicker

Use to gather an individual date from a user.
Date Picker Input
DatePicker(
    name="appointment_date",
    title="Appointment Date",
    date_format="DD-MM-YYYY"
)
Show Parameters

DateRangePicker

Use to gather a start and end date from a user.
Date Range Input
DateRangePicker(
    name="flight_date",
    title="Select Your Flight",
    date_format="DD-MM-YYYY",
    required=True,  
)
Show Parameters

FileUpload

Use to gather file or files from a user.
File Upload Input
FileUpload(
    name="receipts",
    title="Receipts",
    upload_button_label="Click Here",
    multi=True
)
Show Parameters

FileDownload

Clickable button that downloads a file
File Download Input
FileDownload(
    name="documentation",
    title="Documentation",
    file_id="docs_file",
    file_name="About Us",
    file_url="https://www.<my_company>/about_us.pdf"
)
Show Parameters

Use the same ADK version when importing tools to ensure compatibility.
Reuse a common requirements.txt across multiple tools to reduce repeated virtual-environment setup.
If tools require conflicting package versions, maintain separate requirements.txt files and environments.
​
Runtime and migration strategy
Python tools execute within a UV virtual environment inside a component called the tools runtime. This runtime includes a predefined set of supported Python versions. Currently, the only supported version is Python 3.12.
​
Version Management
When a tool is imported into the runtime, it uses the Python version it was originally imported with.
If that version becomes deprecated by watsonx Orchestrate, the system will:
Display a deprecation warning in the UI.
Show the same warning when running the command:
BASH
orchestrate tools list
Inform the user that the tool must be reimported to remain compatible.
​
Deprecation Timeline
After 24 months of deprecation:
The runtime will remove support for the deprecated Python version.
If the tool has not been reimported, the runtime will attempt to reimport it using the closest supported Python version.
​
Limitations of Python tools
​
Host networking
watsonx Orchestrate Developer Edition: Python tools run inside a container. In this environment, localhost refers to the container itself, not the host machine. To call an endpoint on the host machine, use docker.host.internal or the host machine’s IP address.
SaaS: The SaaS version of watsonx Orchestrate cannot access your company’s internal network. If internal access is required, prototype with the Developer Edition and then deploy watsonx Orchestrate on premises or consult IBM for alternative solutions.
On premises: To allow a tool to access external internet resources, ensure that firewall rules do not block outbound traffic from the node pool responsible for tool execution.
​
Read only filesystem
For security and stability, tools execute in a read-only filesystem. Each tool can access only its own filesystem and cannot modify files during execution.

---

Authoring Python-Based Tools
Writing tool schemas for Python tools
Define schemas for watsonX Orchestrate Python tools.
A tool schema defines the structure of data that flows into and out of your Python tools. It consists of two parts:
input_schema: Defines what parameters a tool accepts. Wrap it in ToolRequestBody.model_validate()
output_schema: Defines what data a tool returns. Wrap it in ToolResponseBody.model_validate()
Import tool, ToolRequestBody, and ToolResponseBody from the ADK package:
Python
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolRequestBody, ToolResponseBody
Schemas serve multiple purposes:
Runtime validation: Ensures data conforms to expected types and constraints
UI generation: Automatically creates forms in the WatsonX Orchestrate interface
Documentation: Provides clear parameter descriptions for you and LLMs
API integration: Uses in REST APIs for programmatic tool management
​
Configuring input schemas
Input schemas define the parameters your tool accepts, serving as the contract between your tool and its callers. They specify what data you require, what is optional, and the expected format for each parameter.
Input schemas provide validation, automatic UI form generation, clear documentation, type safety, and guidance for AI agents on proper tool usage. Define schemas with clear parameter descriptions, appropriate types, minimal required fields, numeric constraints where applicable, and focused functionality.
You can configure input schemas in two primary forms: single required parameter for simple tools, or multiple parameters with a mix of required and optional fields for more complex operations.
​
Configuring single parameter
This form of input schema has one required parameter. Use this pattern when your tool needs exactly one piece of information to function.
Python
@tool(
    description="Retrieves allowed values for the Country field",
    input_schema=ToolRequestBody.model_validate({
        "type": "object",
        "properties": {
            "substring": {
                "type": "string",
                "description": "Case-insensitive substring to filter countries. For example, use 'United' or 'Canada'",
            },
        },
        "required": ["substring"],
        "additionalProperties": False,
    }),
)
def search_countries(substring: str) -> str:
    # Implementation
    pass
Collapse
​
Configuring multiple parameters
When your tool needs multiple pieces of information, define a mix of required and optional parameters. This pattern is common for update operations where you must provide some fields while others remain optional.
Required parameters: List them in the required array
Optional parameters: Do not include them in the required array. Use | None (Python 3.10+) or Optional[T] from typing in the function signature
Default values: Give optional parameters = None as default value
Python
@tool(
    description="Updates an existing payment method",
    input_schema=ToolRequestBody.model_validate({
        "type": "object",
        "properties": {
            "payment_method_id": {
                "type": "string",
                "description": "The unique identifier of the payment method to update",
            },
            "nickname": {
                "type": "string",
                "description": "Optional new nickname for the payment method",
            },
            "expiry_month": {
                "type": "integer",
                "minimum": 1,
                "maximum": 12,
                "description": "Optional new expiry month (1-12)",
            },
            "is_default": {
                "type": "boolean",
                "description": "Optional flag to set this as the default payment method",
            },
        },
        "required": ["payment_method_id"],
        "additionalProperties": False,
    }),
)
def update_payment_method(
    payment_method_id: str,
    nickname: str | None = None,
    expiry_month: int | None = None,
    is_default: bool | None = None,
) -> str:
    # Implementation
    pass
Collapse
​
Configuring output schemas
Output schemas define the structure of data your tool returns, serving as the contract between your tool and its consumers. They specify the format and type of data that callers can expect to receive.
Output schemas provide validation, automatic UI display generation, clear documentation, type safety, and proper data flow between tools and agents. Define schemas with clear descriptions, appropriate types, and structures that match your return values exactly.
You can configure output schemas in two primary forms: simple string returns for unstructured or formatted text, or Pydantic models for structured data with multiple fields.
​
Returning simple parameters
Use simple string returns for tools that return unstructured text or single values. This is the most common pattern for tools that format their output as human-readable text.
Python
output_schema=ToolResponseBody.model_validate({
    "type": "string",
    "description": "A human-readable string containing the result data",
})
Function signature:
Python
def tool_name(...) -> str:
    return str(data)
​
Returning multiple parameters
When your tool returns structured data with multiple fields of different types, use Pydantic models as return types. For more information, see Pydantic models.
​
Configuring dynamic schemas
In integration-heavy environments, schemas change frequently. Dynamic input and output schemas enable select fields in a tool’s input to be mutable at runtime—securely and predictably—without affecting immutable core fields.
Use dynamic schemas when:
You need to add new attributes to objects such as CRM records
You need a small number of user-defined fields beyond a stable core API
You want Builder UI users to change types for dynamic fields only. For example, change string to number
Python
from ibm_watsonx_orchestrate.agent_builder.tools import tool


@tool(
    enable_dynamic_input_schema=True,   # must be True for dynamic_input_schema to take effect
    enable_dynamic_output_schema=True,  # must be True for dynamic_output_schema to take effect
    dynamic_input_schema={  # schema for the extra **kwargs fields
        'type': 'object',
        'properties': {
            'c': {'type': 'integer', 'description': 'The third integer to add'}
        },
        'required': []
    },
    dynamic_output_schema={  # schema for the extra fields in the returned dict
        'type': 'object',
        'properties': {
            'sum': {'type': 'integer', 'description': 'The sum of a, b and c'},
            'c': {'type': 'integer', 'description': 'The third integer to add'}
        },
        'required': []
    }
)
def add_kwargs(a: int, b: int, **kwargs) -> dict:
    """
    Adds a, b, and an optional c (from kwargs) and returns the result.

    Args:
        a (int): The first integer to add.
        b (int): The second integer to add.

    Returns:
        dict: A dictionary with keys 'sum' (total of a + b + c) and 'c' (value of c, defaulting to 0).

    Example:
        >>> add_kwargs(3, 5, c=2)
        {'sum': 10, 'c': 2}
    """
    sum = a + b + kwargs.get("c", 0)
    return {'sum': sum, 'c': kwargs.get("c", 0)}


if __name__ == "__main__":
    print(add_kwargs(1, 2, c=3))
Collapse
Python
from ibm_watsonx_orchestrate.agent_builder.tools import tool


@tool(
    enable_dynamic_input_schema=True,   # must be True for dynamic_input_schema to take effect
    enable_dynamic_output_schema=True,  # must be True for dynamic_output_schema to take effect
    dynamic_input_schema={  # schema for the extra **kwargs fields
        'type': 'object',
        'properties': {
            'c': {'type': 'string', 'description': 'The third word'}
        },
        'required': []
    },
    dynamic_output_schema={  # schema for the extra fields in the returned dict
        'type': 'object',
        'properties': {
            'message': {'type': 'string', 'description': 'The message that combines a, b and c'},
            'c': {'type': 'string', 'description': 'The third word'}
        },
        'required': []
    }
)
def combine_words(a: str, b: str, **kwargs) -> dict:
    """
    Receive required three inputs as a, b, c.
    Combine them and returns the result.

    Args:
        a (string): The first word.
        b (string): The second word.


    Returns:
        message: The message combines `a` and `b`.

    Example:
        >>> combine_words("hello", "world")
        "helloworld"
    """
    message = a + b + kwargs.get("c", "")
    return {'message': message, 'c': kwargs.get("c", "")}


if __name__ == "__main__":
    print(combine_words("hello", "world", c="Hana"))
Collapse
​
Parameter types
JSON Schema supports various data types for defining tool parameters. Each type has specific properties and validation rules that help ensure data integrity and provide clear documentation.
​
String
Use the string type for text-based parameters such as names, descriptions, identifiers, or any free-form text input.
Python
"parameter_name": {
    "type": "string",
    "description": "Description of the parameter",
}
​
Integer
Use the integer type for whole numbers without decimal points. This is ideal for counts, indices, IDs, or any numeric value that should not have fractional parts.
Python
"parameter_name": {
    "type": "integer",
    "description": "Description of the parameter",
}
You can add validation constraints to ensure values fall within acceptable ranges:
Python
"parameter_name": {
    "type": "integer",
    "minimum": 1,
    "maximum": 12,
    "description": "Month value between 1 and 12",
}
​
Number (Float)
Use the number type for numeric values that may include decimal points. This type accepts both integers and floating-point numbers.
Python
"parameter_name": {
    "type": "number",
    "description": "Description of the parameter",
}
You can add validation constraints to ensure values fall within acceptable ranges:
Python
"parameter_name": {
    "type": "number",
    "minimum": 1,
    "maximum": 12,
    "description": "Month value between 1 and 12",
}
​
Boolean
Use the boolean type for true or false values.
Python
"parameter_name": {
    "type": "boolean",
    "description": "Description of the parameter",
}
​
Date
Use the string type with format: "date" for date values. Dates must be in ISO 8601 format: YYYY-MM-DD.
Python
"parameter_name": {
    "type": "string",
    "format": "date",
    "description": "Date in YYYY-MM-DD format",
}
Example values: "2024-01-15", "2023-12-31", "2025-06-01"
​
Nested object
Use the object type for complex parameters that contain multiple related fields. This allows you to group related data together in a structured way.
Python
"parameter_name": {
    "type": "object",
    "description": "Description of the object",
    "properties": {
        "nested_field1": {
            "type": "string",
            "description": "Description of nested field",
        },
        "nested_field2": {
            "type": "string",
            "description": "Description of nested field",
        },
    },
    "required": ["nested_field1", "nested_field2"],
}
Collapse
Best practices:
Always include a description for the object and each nested field
Use the required array to specify which nested fields are mandatory
Keep nesting levels reasonable and avoid deeply nested structures when possible
Consider using Pydantic models for complex nested structures. For more information, see Pydantic models
​
Pydantic models
When you have complex nested structures or want type-safe parameter definitions, you can define Pydantic models and use them as both input parameters and return types.
Benefits of Pydantic models:
Type validation: Automatic validation of data structure
Clear contracts: Explicit definition of what the tool accepts and returns
IDE support: Autocomplete and type hints when working with parameters and results
Reusability: Use models across multiple tools
Documentation: Self-documenting parameters and return values
​
Using as input parameters
First, create your Pydantic model classes with clear docstrings and type hints:
Python
from pydantic import BaseModel

class ReadDocumentPageRange(BaseModel):
    """Inclusive, 1-indexed range of pages to read from a document."""
    start: int
    end: int

class NamedDocument(BaseModel):
    """A reference to a previously uploaded document."""
    name: str
    key: str
Collapse
Then, use your Pydantic models in the input schema. Each field in the model must be represented in the schema properties:
Python
@tool(
    description="Reads content from a document with optional page range",
    input_schema=ToolRequestBody.model_validate({
        "type": "object",
        "properties": {
            "key": {
                "type": "string",
                "description": "The unique key associated with the document",
            },
            "page_range": {
                "type": "object",
                "description": "Optional range of pages to read",
                "properties": {
                    "start": {
                        "type": "integer",
                        "description": "The 1-indexed page number to start reading at",
                    },
                    "end": {
                        "type": "integer",
                        "description": "The page number to end reading at (inclusive)",
                    },
                },
                "required": ["start", "end"],
            },
        },
        "required": ["key"],
        "additionalProperties": False,
    }),
)
def read_document(
    key: str,
    page_range: ReadDocumentPageRange | None = None
) -> str:
    """Reads content from a document with optional page range filtering.
    
    Args:
        key: Unique identifier for the document
        page_range: Optional page range to read. If None, reads entire document
    
    Returns:
        Document content as a string
    """
    # Implementation
    pass
Collapse
Important:
Use descriptive class names that clearly indicate the data structure
Add docstrings to explain what the model represents
Define all fields with appropriate type hints
Use optional fields with | None or Optional[T] for non-required parameters
Match the schema properties to the Pydantic model fields exactly
Include required fields in the model in the schema’s required array
Ensure each nested object in the schema corresponds to a Pydantic model
​
Using as return parameter
When your tool returns structured data with multiple fields of different types, define a Pydantic model as the return type. This provides type safety and clear structure for complex return values.
Define the Pydantic model:
Python
from pydantic import BaseModel

class DocumentUploadResult(BaseModel):
    """Result returned after uploading a document."""
    status: str
    key: str
Use in output schema:
Match the output schema exactly to your Pydantic model’s structure:
Python
@tool(
    description="Accepts a document upload from the user",
    output_schema=ToolResponseBody.model_validate({
        "type": "object",
        "properties": {
            "status": {
                "type": "string",
                "description": "Status of the upload",
            },
            "key": {
                "type": "string",
                "description": "Unique key identifying the uploaded document",
            },
        },
        "required": ["status", "key"],
        "additionalProperties": False,
    }),
)
def accept_document_upload(content: bytes) -> DocumentUploadResult:
    """Accepts and processes a document upload.
    
    Args:
        content: Raw bytes of the document to upload
    
    Returns:
        DocumentUploadResult with status and unique key
    """
    # Implementation
    pass
Collapse
Complete example with complex return types:
This example shows a tool that returns a complex structure with arrays and nested objects:
Python
from pydantic import BaseModel

class AccountList(BaseModel):
    """List of bank accounts with their details."""
    accounts: list[dict[str, str]]
    total_accounts: int

@tool(
    description="Get a list of all bank accounts with their types and balances",
    output_schema=ToolResponseBody.model_validate({
        "type": "object",
        "properties": {
            "accounts": {
                "type": "array",
                "description": "List of account objects",
                "items": {
                    "type": "object",
                    "properties": {
                        "account_number": {"type": "string"},
                        "account_type": {"type": "string"},
                        "balance": {"type": "number"},
                    },
                },
            },
            "total_accounts": {
                "type": "integer",
                "description": "Total number of accounts",
            },
        },
        "required": ["accounts", "total_accounts"],
        "additionalProperties": False,
    }),
)
def list_accounts() -> AccountList:
    """Retrieves all bank accounts with their details.
    
    Returns:
        AccountList containing all accounts and total count
    """
    # Implementation
    pass
Collapse
​
AgentRun context
When your tools need access to user identity, credentials, or context variables, use the AgentRun parameter. This parameter is special and you should NOT include it in the input schema.
The framework automatically injects the AgentRun context parameter. Do not define it in your input schema. Only include it in your function signature.
Python
from ibm_watsonx_orchestrate.run.context import AgentRun

@tool(
    description="Creates a legal matter using user context",
    input_schema=ToolRequestBody.model_validate({
        "type": "object",
        "properties": {
            "matter_title": {
                "type": "string",
                "description": "Title of the legal matter",
            },
            "matter_description": {
                "type": "string",
                "description": "Brief description of the matter",
            },
        },
        "required": ["matter_title", "matter_description"],
        "additionalProperties": False,
    }),
)
def create_matter(context: AgentRun, matter_title: str, matter_description: str) -> str:
    """Creates a new legal matter with user context."""
    # Access user identity from context
    user_email = context.request_context.get('wxo_email_id')
    user_name = context.request_context.get('wxo_user_name')
    
    return f"Matter '{matter_title}' created by {user_name} ({user_email})"
See all 27 lines
​
Important rules
Every parameter must have a description - You need this for the parameter to show up in the WatsonX UI
Parameter names must match - Match schema property names exactly to function parameter names
List only required parameters - Only include parameters in the required array that you truly require
Optional parameters - Mark optional parameters with | None (Python 3.10+) or Optional[T] from typing in the function signature, and set their default value to = None
Output schema must match return type - Match the output schema exactly to the Pydantic model structure or return type
Context parameter is special - The framework injects the context: AgentRun parameter and you should NOT include it in the input schema. For more information, see AgentRun context
Function signature must match schema - Match the function parameters to the input schema properties exactly:
Python
input_schema=ToolRequestBody.model_validate({
    "type": "object",
    "properties": {
        "origin": {"type": "string", "description": "..."},
        "destination": {"type": "string", "description": "..."},
        "max_price": {"type": "number", "description": "..."},
    },
    "required": ["origin"],
    "additionalProperties": False,
})

def search_flights(
    origin: str,                    # Required, in "required" list
    destination: str | None = None, # Optional, not in "required" list
    max_price: float | None = None, # Optional, not in "required" list
) -> str:
    # Implementation
    pass
Collapse
​
See also
Tool response structure and annotations - Learn about returning structured responses with widgets
Widget integration - Add interactive forms to your tool responses
Creating tools - General guide to creating Python tools

---

Authoring Python-Based Tools
Tool response structure and annotations
Python tools can return structured responses with rich content, widgets, and metadata.

The ToolResult() and dictionary response formats support text content with audience targeting, structured data for downstream processing, widget integration to render interactive UI components, and metadata support for custom extensions and context information.
ToolResult class
Returns tool responses by using a Python class with type-safe parameters and MCP compliance.
Dictionary format
Returns tool responses as a dictionary structure with explicit control over all response fields.
​
ToolResult class
The ToolResult class provides structured tool responses following the MCP specification. It allows tools to return content blocks, structured data, and widgets in a standardized format.
Import
Import the ToolResult class to create structured responses in your Python tools:
from ibm_watsonx_orchestrate.run import ToolResult
Constructor parameters
​
content
List[Union[ContentBlock, str]]required
Content blocks or strings to display to the user and send to the large language model (LLM). Strings are automatically converted to TextContent blocks.
The following example shows two ways to specify content by using simple strings or explicit TextContent blocks:
# Using strings (automatically converted to TextContent)
content=["Operation completed", "Status: Active"]

# Using TextContent blocks explicitly
from ibm_watsonx_orchestrate.run import TextContent
content=[TextContent(text="Operation completed")]
For details on content structure and audience targeting, see Content blocks and annotations.
​
structuredContent
Dict[str, Any]
Structured data for programmatic use. This data is available for downstream processing but not directly displayed to users.
The following example demonstrates how to include structured data in a ToolResult:
structuredContent={
    "user_id": 123,
    "name": "John Doe",
    "balance": 5000.00
}
​
widget
Any
Form widget to render in the UI. Supports form widgets created by using the FormWidget class and its input components.
The following example demonstrates how to include a form widget in a ToolResult response:
from ibm_watsonx_orchestrate.run import ToolResult
from ibm_watsonx_orchestrate.run.forms import FormWidget, TextInput

@tool()
def show_registration_form():
    form = FormWidget(
        title="User Registration",
        inputs=[
            TextInput(
                name="email",
                title="Email Address",
                required=True
            )
        ]
    )
    
    return ToolResult(
        content=["Please complete your registration"],
        widget=form
    )
For widget implementations by using FormWidget(), see Widget integration.
​
meta
Dict[str, Any]
Additional metadata for custom extensions or context. This field is serialized as _meta in the response.
The ToolResult class does not support explicitly setting the _meta parameter and widget contracts as described for dictionary format. To implement widgets with ToolResult, use widget with the FormWidget class.
The following example shows how to add custom metadata using the meta parameter:
# Custom metadata
meta={
    "priority": "high",
    "department": "finance"
}
Example
The following example demonstrates a tool that retrieves account information and returns a comprehensive response with multiple content blocks, structured data, a form widget for updating the budget, and custom metadata:
from ibm_watsonx_orchestrate.run import ToolResult, TextContent
from ibm_watsonx_orchestrate.run.forms import FormWidget, NumberInput

@tool()
def check_account_status(user_id: str):
    # Fetch account data
    account_data = fetch_account(user_id)
    
    # Create form for next action
    form = FormWidget(
        title="Update Budget",
        inputs=[
            NumberInput(
                name="amount",
                title="New Budget Amount",
                default_value=account_data["budget"]
            )
        ]
    )
    
    return ToolResult(
        content=[
            TextContent(
                text=f"Account Status: {account_data['status']}"
            ),
            TextContent(
                text=f"Current Budget: ${account_data['budget']}"
            )
        ],
        structuredContent=account_data,
        widget=form,
        meta={"account_type": "premium"}
    )
See all 33 lines
​
Dictionary format
The dictionary format provides direct control over the response structure, and requires the following top-level fields:
{
    "content": [...],           # Array of content blocks
    "structuredContent": {...}, # Structured data (optional)
    "_meta": {...}              # Metadata and extensions
}
Dictionary fields
​
content
Arrayrequired
Content blocks to display to the user and send to the large language model (LLM).
The following example demonstrates a simple tool that returns content blocks with user audience targeting:
@tool()
def get_dog_breeds():
    return {
        "content": [
            {
                "type": "text",
                "annotations": {
                    "audience": ["user"]
                },
                "text": "Dog breeds: affenpinscher, african, airedale, akita, appenzeller"
            }
        ]
    }
See all 13 lines
For details on content structure and audience targeting, see Content blocks and annotations.
​
structuredContent
Dict[str, Any]
Structured data for programmatic use. This data is available for downstream processing but not directly displayed to users.
The following example demonstrates how to return structured data alongside user-facing content:
@tool()
def get_account_info(account_id: str):
    account_data = {
        "account_id": account_id,
        "balance": 1500.00,
        "status": "active"
    }
    
    return {
        "content": [
            {
                "type": "text",
                "annotations": {
                    "audience": ["user"]
                },
                "text": f"Account {account_id} retrieved successfully"
            }
        ],
        "structuredContent": account_data
    }
See all 20 lines
​
_meta
Dict[str, Any]
Additional metadata for custom extensions or context information. Use this field to pass custom data that doesn’t fit into standard response fields.
The following example demonstrates how to add custom metadata to a tool response:
Custom metadata example
@tool()
def get_account_info(account_id: str):
    return {
        "content": [
            {
                "type": "text",
                "annotations": {
                    "audience": ["user"]
                },
                "text": f"Account {account_id} information retrieved"
            }
        ],
        "_meta": {
            "priority": "high",
            "department": "finance",
            "request_id": "REQ-12345",
            "timestamp": "2024-01-15T10:30:00Z"
        },
        "structuredContent": None
    }
For widget implementations by using _meta, see Widget integration.
​
Content blocks and annotations
Content blocks follow the MCP specification and support audience targeting through annotations. This controls how content is processed by the agent and displayed to users.
​
Text content blocks
Text content blocks represent textual information with optional audience targeting. Use text content to return messages, status updates, or any string-based data from your tool, and to control who sees the content by using the audience annotation.


ToolResult class

Dictionary format
The following examples demonstrate different ways to create text content blocks with audience targeting:
​
Annotations and audience
The audience annotation is set inside content blocks to control content visibility and processing behavior.
​
audience
List[Enum[Role]] or List[str]
Specifies who must see and process the content. The possible values varies according to the response format you implement for the tool result.
ToolResult class
Dictionary format
Possible values:
Role.USER
Role.ASSISTANT
[Role.USER, Role.ASSISTANT]
The Role enum provides type-safe constants for specifying content audience when using the ToolResult class:
The following example shows how to use the Role enum for type-safe audience specification:
from ibm_watsonx_orchestrate.run import Role

Role.USER        # Content for end users
Role.ASSISTANT   # Content for agent/LLM
The audience affects agent reasoning and message display behavior. For more information, see Audience behavior.
​
Audience behavior
The audience annotation controls how content is processed by the agent and displayed to users. Behavior varies based on whether a widget is present in the response. The following audiences are the audience types that determine content handling:
user
Content intended for end users only, bypassing agent reasoning.
assistant
Content for the agent and large language model to process and reason about.
user and assistant
Content for both user and assistant, where the agent processes it before presenting to users.
Content with annotations only
When tool responses contain content with annotations but no widget, the following behavior applies based on the audience type:
User
Assistant
Both user and assistant
Property	Behavior
Agent reasoning	Text is not used for reasoning that would trigger next actions.
Message to agent context	Text is passed as AI message to prevent hallucinations.
User output	The exact text displayed as provided.
For the following code snippet, you might observe the following:
User messages are passed through without agent reasoning.
The exact text content is preserved and displayed to the user.
Context is maintained to prevent hallucinations in follow-up questions.
No transformation or summarization occurs.


ToolResult class

Dictionary format
The following examples show how to create content with user audience that bypasses agent reasoning:
Content with annotations and widget metadata
When tool responses contain both content with annotations and a widget, widget-specific behavior is activated.
When a widget is present in the tool response either through the ToolResult class or dictionary format, the agent runtime does not send the response for agent reasoning. The tool response is considered final and passed directly back to the user.
User
Assistant
Both user and assistant
Property	Behavior
Agent reasoning	The text is not used for reasoning.
Message to agent context	The message is passed to context to prevent hallucinations.
User output	The exact text and widget are rendered.
For the following code snippet, you might observe the following:
No agent reasoning occurs.
The user message is preserved exactly as provided.
The widget data is rendered alongside the content.


ToolResult class

Dictionary format
The following examples demonstrate user audience content with a widget where no agent reasoning occurs:
​
Widget integration
For detailed information about integrating interactive widgets and forms into your tool responses, including form widgets, custom widgets, event handling, and the FormWidget, ToolEvent, and MessageEvent classes, see Widget integration.



----

Authoring Python-Based Tools
Widget integration for Python tools
Widgets provide interactive UI components in tool responses.

Develop your tool response to return the following types of widgets:
Form widgets
Interactive forms with various input field types including text inputs, text areas, number inputs, date pickers, date range pickers, radio buttons, checkboxes, combo boxes, file uploads, and tables for structured data collection.
For interactive forms, you can handle data from form submission with the on_event callback. This is how you capture and process user input from form submissions.
Custom widgets (user_defined)
Custom UI components with flexible rendering. This option is supported in embedded chat only.
​
Forms with interactive widgets
Form widgets provide structured input forms with various field types. You can create forms using either the FormWidget class or the dictionary format with the _meta field.
​
Widget contract with FormWidget class
The FormWidget class provides a Python-based approach to creating form widgets when using the ToolResult return format.
Import
Import the FormWidget class and input components to create forms in your Python tools:
from ibm_watsonx_orchestrate.run.widgets.forms import (
    FormWidget, TextInput, TextArea, NumberInput, DatePicker,
    DateRangePicker, RadioButton, Checkbox, ToolEvent, MessageEvent
)
Constructor parameters
​
title
strrequired
The form title displayed to users.
The following example sets the form title that appears at the top of the form:
title="User Registration Form"
​
inputs
List[InputWidget]required
List of input widgets that define the form fields. Supported input types include:
TextInput
TextArea
NumberInput
DatePicker
DateRangePicker
RadioButton
Checkbox
The following example defines a list of input widgets for the form, including a required email field and an optional comments field:
inputs=[
    TextInput(
        name="email",
        title="Email Address",
        required=True
    ),
    TextArea(
        name="comments",
        title="Comments",
        placeholder="Enter your feedback"
    )
]
For more details on each input widget, see Additional features of Python tools: Creating a form tool.
​
description
str
Optional description text displayed below the form title.
The following example adds a description that appears below the form title to provide additional context:
description="Please complete all required fields to submit your request."
​
submit_text
str
Custom text for the submit button. Defaults to “Submit”.
The following example customizes the submit button text:
submit_text="Register Now"
​
cancel_text
str
Custom text for the cancel button. Defaults to “Cancel”.
The following example customizes the cancel button text:
cancel_text="Go Back"
​
on_event
List[Union[ToolEvent, MessageEvent]]
List of event handlers that define actions when the form is submitted. For more information, see Handling data from form submission.
These examples show how to configure event handlers for form submission using either ToolEvent or MessageEvent:
# Example for ToolEvent
on_event=[
    ToolEvent(
        tool="process_form",
        parameters={"email": "", "name": ""},
        map_input_to="submit"
    )
]

# Example for MessageEvent
on_event=[
    MessageEvent(
        message="Thank you for completing the survey! Your feedback helps us improve.",
        map_input_to="submit"
    )
]
​
Widget contract with dictionary format
When using the dictionary return format, widget contracts are defined in the _meta["com.ibm.orchestrate/widget"] field.
​
_meta
Dict[str, Any]
Additional metadata for custom extensions or context. Widget contracts in _meta["com.ibm.orchestrate/widget"] require the following fields:
Field	Type	Description
response_type	string	Must be "forms" for form widgets.
json_schema	object	JSON Schema defining form fields and validation rules. For more information, see JSON Schema details.
ui_schema	object	UI schema specifying widget types per field. For more information, see UI Schema details.
form_data	object	Pre-populated default values for form fields. For more information, see Form Data details.
on_event	array	Actions triggered on form submission. For more information, see Handling data from form submission.
The following example shows the basic structure of a tool response with a form widget using the dictionary format:
return {
    "content": [
        {
            "type": "text",
            "annotations": {
                "audience": ["user"]
            },
            "text": "Message text"
        }
    ],
    "_meta": {
        "com.ibm.orchestrate/widget": {
            "response_type": "forms",
            "json_schema": {...},
            "ui_schema": {...},
            "form_data": {...},
            "on_event": [...]
        }
    }
}
See all 20 lines
JSON Schema details
The json_schema field defines the structure, validation rules, and metadata for form fields. Implement the following properties to determine what data the form collects and how it must be validated:
Property	Type	Description
title	string	The form title displayed to users
description	string	Optional description text displayed below the form title
type	string	Must be "object" for form schemas
required	array	Array of field names that are required
properties	object	Object containing field definitions. For more information, see properties definition.
properties definition
Each field in the properties object can include:
Property	Type	Description
type	string	Data type: "string", "integer", "number", "boolean", "array", "object".
title	string	Label displayed for the field.
description	string	Help text or description for the field.
default	any	Default value for the field.
enum	array	Array of allowed values for selection widgets.
enumNames	array	Human-readable labels for enum values.
format	string	Format specification, for example, "date" for date fields.
minimum	number	Minimum value for numeric fields.
maximum	number	Maximum value for numeric fields.
minItems	number	Minimum number of items for array fields.
maxItems	number	Maximum number of items for array fields.
oneOf	array	Array of schema options for conditional validation.
The following example demonstrates a complete JSON Schema for a user registration form with required fields, validation rules, and data types:
{
  "title": "User Registration",
  "description": "Please complete all required fields",
  "type": "object",
  "required": ["firstName", "email"],
  "properties": {
    "firstName": {
      "type": "string",
      "title": "First Name"
    },
    "email": {
      "type": "string",
      "title": "Email Address",
      "format": "email"
    },
    "age": {
      "type": "integer",
      "title": "Age",
      "minimum": 18,
      "maximum": 120
    }
  }
}
See all 23 lines
UI schema details
The ui_schema field specifies how form renders widget type and appearance for each field. You can define the following properties:
Property	Type	Description
ui:widget	string	Widget type to render.
ui:placeholder	string	Placeholder text for input fields.
ui:options	object	Additional widget-specific options.
ui:enumNames	array	Custom labels for enum values for combobox widget.
The ui_schema and json_schema work together to define form fields. They reference the same field names as keys:
JSON schema (json_schema.properties.fieldName) defines the data structure, type, validation rules, and metadata for a field.
UI schema (ui_schema.fieldName) specifies how that same field must be rendered as a widget.
For example, if you define a field called "firstName" in your JSON Schema properties, you must use the same key "firstName" in your UI Schema to specify its widget type. The field name acts as the connection point between the two schemas.
The following example shows how the same field name ("firstName") is used consistently across all three schema objects:
{
  "json_schema": {
    "properties": {
      "firstName": {           // Field name: "firstName"
        "type": "string",
        "title": "First Name"
      }
    }
  },
  "ui_schema": {
    "firstName": {             // Same field name: "firstName"
      "ui:widget": "TextWidget"
    }
  },
  "form_data": {
    "firstName": "John"        // Same field name: "firstName"
  }
}
All three objects (json_schema.properties, ui_schema, and form_data) use the same field name as the key to reference the same form field.
Show TextWidget

Show TextareaWidget

Show NumberWidget

Show RadioWidget

Show CheckboxWidget

Show DateWidget (Single Date)

Show DateWidget (Date Range)

Show ComboboxWidget

Show Table

Show FileUpload

Show FileDownloadWidget

Form data details
The form_data field provides pre-populated default values for form fields. These values appear in the form when it’s first displayed to the user, providing sensible defaults to guide users and pre-populating fields with known user data when available. Consider the following implementation details for form data:
Field names in form_data must match the field names defined in json_schema.properties.
Values must match the data type specified in the JSON schema.
Optional fields can be omitted or set to empty values. Use empty strings ("") for optional text fields.
For array fields such as date ranges or tables, provide an array of values.
For date fields, use ISO 8601 format (YYYY-MM-DD).
For selection widgets, ensure default values match one of the enum options.
For file upload fields, provide an object with fileName and url properties.
The following example demonstrates pre-populated form data with various field types including text, numbers, dates, and file uploads:
{
  "firstName": "John",
  "email": "john@example.com",
  "age": 25,
  "dateRange": ["2025-09-12", "2025-09-25"],
  "accountNumber": "231",
  "comments": "",
  "uploadedFile": {
    "fileName": "document.pdf",
    "url": "https://example.com/files/document.pdf"
  }
}
​
Handling data from form submission
The on_event defines actions triggered when users interact with the form. This is how you capture and process user input from form submissions:








Tool
Agent
Chat UI
User
Tool
Agent
Chat UI
User
Fills out form and clicks Submit
Sends form data via /runs API
Calls tool specified in on_event
with form data as parameters
Processes data and returns response
Returns tool result
Displays response
​
on_event parameters
​
type
stringrequired
The action type to perform. Implement the code based on the format:
If you use the dictionary format, set the type value to either "tool" or "message".
If you use the FormWidget() class, you must call either ToolEvent() or MessageEvent() to perform the action.
​
tool
string
The name of the tool to invoke. Required when type is "tool".
​
parameters
object
Key-value pairs mapping form field names to their values. Required when type is "tool". Values are populated automatically from form data.
​
map_input_to
stringrequired
The event trigger. Use "submit" to trigger the action when the form is submitted.
​
message
string
The message to send to the agent. Required when type is "message".
​
Tool call
The ToolEvent() or type: "tool" actions invoke another tool with form data as parameters when the form is submitted. This is the most common approach for processing form submissions.
You can use this approach when you need to process form data with custom logic, validate inputs, make API calls, or perform complex operations.
The tool specified must accept parameters matching the form field names. When the user submits the form, this tool is automatically called with the form data.
​
Using ToolEvent() with FormWidget
When using the FormWidget class, configure on_event by using the ToolEvent class.
ToolEvent class
The ToolEvent class defines a tool invocation event that triggers when a form is submitted. Use this class with FormWidget to process form data through another tool.
Import
Import the ToolEvent class to define tool invocation events:
from ibm_watsonx_orchestrate.run.widgets.forms import ToolEvent
Constructor parameters
​
tool
strrequired
The name of the tool to invoke when the event is triggered. This tool must be defined in your agent and accept parameters matching the form field names.
The following example specifies the tool to invoke when the form is submitted:
tool="process_registration"
​
parameters
Dict[str, str]required
Dictionary mapping form field names to their parameter names in the target tool. Keys must match the name attributes of form inputs. Values are typically empty strings that get populated with form data on submission.
The following example maps form field names to tool parameters that will be populated with form data:
parameters={
    "firstName": "",
    "email": "",
    "age": ""
}
​
map_input_to
strrequired
The event trigger type. Use "submit" to trigger the action when the form is submitted.
The following example sets the event trigger to activate when the form is submitted:
map_input_to="submit"
The following example shows how to create a ToolEvent instance for processing form submissions:
from ibm_watsonx_orchestrate.run.widgets.forms import ToolEvent

# Define a tool event that processes form submission
event = ToolEvent(
    tool="process_user_data",
    parameters={
        "name": "",
        "email": "",
        "phone": ""
    },
    map_input_to="submit"
)
This complete example demonstrates a contact form with ToolEvent handling:
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from ibm_watsonx_orchestrate.run.widgets.forms import FormWidget, TextInput, ToolEvent
from ibm_watsonx_orchestrate.run.tool_result import ToolResult, TextContent, Annotations, Role

@tool()
def show_contact_form():
    """Display contact information form."""
    form = FormWidget(
        title="Contact Information",
        inputs=[
            TextInput(
                name="name",
                title="Full Name",
                required=True
            ),
            TextInput(
                name="email",
                title="Email",
                required=True
            ),
            TextInput(
                name="phone",
                title="Phone Number",
                required=False
            )
        ],
        on_event=[
            ToolEvent(
                tool="save_contact",
                parameters={
                    "name": "",
                    "email": "",
                    "phone": ""
                },
                map_input_to="submit"
            )
        ]
    )
    
    return ToolResult(
        content=[
            TextContent(
                text="Please provide your contact information",
                annotations=Annotations(
                    audience=[Role.USER]
                )
            )
        ],
        widget=form
    )

@tool()
def save_contact(name: str, email: str, phone: str = ""):
    """Save contact information."""
    # Process the contact data
    return ToolResult(
        content=[
            TextContent(
                text=f"Contact saved: {name} ({email})",
                annotations=Annotations(
                    audience=[Role.USER]
                )
            )
        ]
    )
See all 65 lines
​
Using type: "tool" with dictionary format
When using the dictionary return format, configure on_event within the _meta field:
The following example shows the basic structure of a tool event configuration in dictionary format:
"on_event": [
    {
        "type": "tool",
        "tool": "process_registration",
        "parameters": {
            "firstName": "",
            "email": ""
        },
        "map_input_to": "submit"
    }
]
This complete example demonstrates a two-tool workflow where the first tool displays a registration form and the second tool processes the submitted data:
@tool()
def show_registration_form():
    """Display registration form."""
    return {
        "content": [
            {
                "type": "text",
                "annotations": {
                    "audience": ["user"]
                },
                "text": "Please complete the registration form"
            }
        ],
        "_meta": {
            "com.ibm.orchestrate/widget": {
                "response_type": "forms",
                "json_schema": {
                    "title": "User Registration",
                    "type": "object",
                    "properties": {
                        "firstName": {"type": "string", "title": "First Name"},
                        "email": {"type": "string", "title": "Email"}
                    }
                },
                "ui_schema": {
                    "firstName": {"ui:widget": "TextWidget"},
                    "email": {"ui:widget": "TextWidget"}
                },
                "form_data": {"firstName": "", "email": ""},
                "on_event": [
                    {
                        "type": "tool",
                        "tool": "process_registration",  # Name of the tool to call when the event is triggered.
                        "parameters": {
                            # Each key must match a parameter name in process_registration(...).
                            # With map_input_to set to "submit", these fields are populated from the form submission.
                            "firstName": "",
                            "email": ""
                        },
                        "map_input_to": "submit"  # Maps submitted form values to the parameters above.
                    }
                ]
            }
        },
        "structuredContent": None,
        "context_updates": {}
    }

@tool()
def process_registration(firstName: str, email: str):
    """Process the registration form submission."""
    return {
        "content": [
            {
                "type": "text",
                "annotations": {
                    "audience": ["user"]
                },
                "text": f"Registration successful! Welcome, {firstName}. Confirmation sent to {email}."
            }
        ],
        "_meta": {},
        "structuredContent": None,
        "context_updates": {}
    }
See all 65 lines
​
Message call
The MessageEvent() or type: "message" actions send a predefined message to the agent instead of calling a tool. The agent processes this message as if the user had typed it.
You can use this approach when you want to trigger a conversational flow or simple acknowledgment without custom processing logic.
​
Using MessageEvent() with FormWidget
The MessageEvent class defines a message event that sends a predefined message to the agent when a form is submitted. Use this class with FormWidget to trigger conversational flows without custom processing logic.
Import
Import the MessageEvent class to define message events:
from ibm_watsonx_orchestrate.run.widgets.forms import MessageEvent
Constructor parameters
​
message
strrequired
The message to send to the agent when the event is triggered. The agent processes this message as if the user had typed it.
The following example defines the message that will be sent to the agent when the form is submitted:
message="Thank you for your submission. Your request has been received."
​
map_input_to
strrequired
The event trigger type. Use "submit" to trigger the action when the form is submitted.
The following example sets the event trigger to activate when the form is submitted:
map_input_to="submit"
Example
The following example demonstrates a survey form using MessageEvent to send a thank you message upon submission:
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from ibm_watsonx_orchestrate.run.widgets.forms import FormWidget, TextArea, RadioButton, MessageEvent
from ibm_watsonx_orchestrate.run.tool_result import ToolResult, TextContent, Annotations, Role

@tool()
def show_survey_form():
    """Display a simple survey form."""
    form = FormWidget(
        title="Quick Survey",
        description="Help us improve by sharing your feedback",
        inputs=[
            RadioButton(
                name="satisfaction",
                title="How satisfied are you?",
                options=["very_satisfied", "satisfied", "neutral", "dissatisfied"],
                option_labels=["Very Satisfied", "Satisfied", "Neutral", "Dissatisfied"],
                required=True
            ),
            TextArea(
                name="feedback",
                title="Additional Comments",
                placeholder="Share your thoughts...",
                required=False
            )
        ],
        submit_text="Submit Survey",
        on_event=[
            MessageEvent(
                message="Thank you for completing the survey! Your feedback helps us improve.",
                map_input_to="submit"
            )
        ]
    )
    
    return ToolResult(
        content=[
            TextContent(
                text="Please take a moment to complete our survey",
                annotations=Annotations(
                    audience=[Role.USER]
                )
            )
        ],
        widget=form
    )
See all 45 lines
​
Using type: "message" with dictionary format
When using the dictionary return format, configure on_event within the _meta field:
The following example shows the basic structure of a message event configuration in dictionary format:
"on_event": [
    {
        "type": "message",
        "message": "Registration completed successfully",
        "map_input_to": "submit"
    }
]


The following example demonstrates a feedback form that sends a message to the agent upon submission:
@tool()
def show_feedback_form():
    """Display feedback form that sends a message to the agent."""
    return {
        "content": [
            {
                "type": "text",
                "annotations": {
                    "audience": ["user"]
                },
                "text": "Please provide your feedback"
            }
        ],
        "_meta": {
            "com.ibm.orchestrate/widget": {
                "response_type": "forms",
                "json_schema": {
                    "title": "Feedback Form",
                    "type": "object",
                    "properties": {
                        "rating": {"type": "string", "title": "Rating"},
                        "comments": {"type": "string", "title": "Comments"}
                    }
                },
                "ui_schema": {
                    "rating": {"ui:widget": "RadioButtonWidget"},
                    "comments": {"ui:widget": "TextAreaWidget"}
                },
                "form_data": {"rating": "", "comments": ""},
                "on_event": [
                    {
                        "type": "message",
                        "message": "Thank you for your feedback! Your response has been recorded.",
                        "map_input_to": "submit"
                    }
                ]
            }
        },
        "structuredContent": None,
        "context_updates": {}
    }
See all 41 lines
​
Custom widgets with user_defined
Create flexible UI components with custom widgets by rendering your own rich element logic. These widgets are passed through the _meta parameter and are rendered in embedded chat by using the userDefinedResponse event.
Custom widgets in tool responses is a custom solution that operates independently of standardized UI protocols such as MCP-UI or A2UI. Application builders are responsible for implementing the rendering logic and managing security considerations.
The user_defined response type from tools is supported only in embedded chat. The webpage builder is responsible for implementing the rendering logic.
The following example demonstrates how to create a custom widget with user-defined response type and structured data:
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from datetime import datetime, timezone

@tool
def get_custom_widget(
    widget_type: str = "custom_component",
    title: str = "Custom Widget",
    message: str = "This is a custom user-defined widget",
    action_url: str = "https://ibm.com"
):
    """
    Generate a custom widget with user_defined response type.
    
    This tool creates a custom widget that can be rendered in the watsonx Orchestrate
    embedded chat interface using custom rendering logic.
    """
    
    return {
        "content": [
            {
                "type": "text",
                "annotations": {
                    "audience": ["user"]
                },
                "text": f"{title}: {message}"
            }
        ],
        "_meta": {
            "com.ibm.orchestrate/widget": {
                "response_type": "user_defined",
                "user_defined": {
                    "user_defined_type": widget_type,
                    "title": title,
                    "text": message,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "action_url": action_url,
                    "custom_field": "You can add any custom data here",
                    "interactive": True
                }
            }
        },
        "structuredContent": None,
        "context_updates": {}
    }
See all 44 lines
Custom widget structure
When creating custom widgets, you must structure the metadata in a specific nested format that the chat can recognize and process. Place the widget data within the _meta parameter of your tool response by using the standardized namespace key to ensure proper routing to the userDefinedResponse event handler.
The following example shows the required structure for custom widget metadata with detailed annotations:
_meta={
    # Namespace key that identifies this as an widget
    "com.ibm.orchestrate/widget": {
        # Indicates this is a custom user-defined response type
        "response_type": "user_defined",
        
        # Container object that holds all your custom widget properties
        # All custom data must be nested within this object
        "user_defined": {
            # Required: Identifies the specific type of widget being rendered
            # Use this to differentiate between different widget implementations in your handler
            "user_defined_type": "your_widget_type",
            
            # Optional: Display title for the widget
            "title": "Widget Title",
            
            # Optional: Main content or message text
            "text": "Widget content",
            
            # Add any additional custom properties your widget needs
            # Examples: timestamps, URLs, status flags, nested objects, arrays, etc.
            # All properties here are accessible in the userDefinedResponse event handler
        }
    }
}
Where:
Container structure: Nest all custom properties inside the user_defined object. This object acts as a container that isolates your custom data from the standard response structure.
Widget identification: Use the required user_defined_type field to identify your widget type. Your rendering logic uses this field to determine how to display the widget.
Flexible properties: Beyond the required user_defined_type, include any custom properties your widget needs, such as title, text, data, config, or domain-specific fields. The structure adapts to your requirements.
Multiple widget types: This flexible structure accommodates various widget types, from simple cards and notifications to complex dashboards and interactive components. Implement and test the rendering logic for each widget type to ensure proper display.
Rendering custom widgets
The webpage builder must implement the rendering logic for custom widgets in embedded chat. For complete implementation details, examples, and event handling, see the userDefinedResponse event documentation.

---

Authoring Python-Based Tools
Python Dependency Management in watsonx Orchestrate
Understanding how Python dependencies work in watsonx Orchestrate is critical for building secure, repeatable deployments across environments. This guide clarifies what gets packaged during export, when dependencies are installed, and which patterns are officially supported for enterprise deployments.
​
What are “dependencies” in watsonx Orchestrate?
Important: Dependencies in watsonx Orchestrate are the source specifications listed in your requirements.txt file, not the compiled binary packages or installed libraries.
When you export a Python tool or agent, the export includes:
✅ Your Python source code files (.py files)
✅ Your requirements.txt file (dependency specifications)
✅ Any additional resources (data files, configuration files)
❌ Does not include the installed binary packages or virtual environment
This is a source-only export model. The actual Python packages (wheels, compiled binaries) are downloaded and installed separately during deployment.
​
Example: What gets exported
# When you export an agent, you get:
agent/
├── tools/
│   └── my_tool/
│       ├── my_tool.py              # ✅ Source code
│       ├── requirements.txt        # ✅ Dependency specifications
│       └── utils.py                # ✅ Additional source files
├── agents/
│   └── my_agent.yaml               # ✅ Agent configuration
└── connections/
    └── my_connection.yaml          # ✅ Connection definitions

# What is NOT included:
# - site-packages/ (installed libraries)
# - .venv/ (virtual environment)
# - Binary wheels or compiled packages
​
When and where are dependencies installed?
Dependencies are installed server-side at agent deployment time, not during export or import.
​
Installation timeline
Development: You create a tool with a requirements.txt file
Import: You import the tool using orchestrate tools import
Deployment: When the tool is deployed to an environment (Draft or Live):
watsonx Orchestrate reads your requirements.txt
Runs pip install server-side
Creates an isolated virtual environment (venv)
Installs all specified packages
This installation happens in every environment where you deploy the tool—DEV, QA, and PROD instances all perform their own dependency installation.
​
Virtual environment caching
To optimize performance and reduce redundant installations, watsonx Orchestrate uses a canonical hash-based deduplication mechanism:
Hash computation: When you deploy a tool, the system computes a unique fingerprint (hash) of your requirements.txt file
Cache check: The system checks if a virtual environment with this exact hash already exists
Reuse or create:
Hash match found: Reuses the existing cached venv (no installation needed)
No match: Creates new hash, builds new venv, stores in cache
This means packages are downloaded once per unique requirements.txt within a cluster, not once per tool or tenant.
​
When a new virtual environment is created
A new venv will be created when the dependency hash changes due to:
Dependency version changes: Updating from requests==2.32.3 to requests==2.32.4
Adding/removing packages: Adding numpy==1.24.0 to existing dependencies
Different registry URLs: Changing --index-url or --extra-index-url
ADK version changes: If you re-import with a different ADK version and have unpinned dependencies, ADK may add different “latest” versions
Best practice: Use pinned versions in requirements.txt to ensure consistent hash generation and maximize venv reuse across deployments.
​
Enterprise dependency management patterns
​
Using private registries (Artifactory, Nexus)
watsonx Orchestrate supports pulling packages from private PyPI registries like Artifactory or Sonatype Nexus. This is essential for organizations that:
Require security scanning of all packages
Cannot allow direct downloads from public PyPI
Need to control which package versions are available
​
Configuration with --index-url
Use --index-url to specify your primary package registry:
requirements.txt
--index-url https://artifactory.company.com/api/pypi/python-virtual/simple
ibm-watsonx-orchestrate==2.4.0
requests==2.32.3
pydantic==2.8.2
When using --index-url, pip will only check your specified registry. If a package is not found there, the installation will fail—it will NOT fall back to public PyPI.
​
Configuration with --extra-index-url
Use --extra-index-url to add your registry as an additional source while keeping PyPI as a fallback:
requirements.txt
--extra-index-url https://artifactory.company.com/api/pypi/python-virtual/simple
ibm-watsonx-orchestrate==2.4.0
requests==2.32.3
pydantic==2.8.2
With --extra-index-url, pip will check both your private registry AND public PyPI. This provides flexibility but may not meet strict security policies that prohibit any public PyPI access.
​
Direct wheel URLs
You can also specify direct URLs to wheel files hosted in your registry:
requirements.txt
ibm-watsonx-orchestrate==2.4.0
pydantic @ https://artifactory.company.com/python-packages/pydantic-2.8.2-py3-none-any.whl
requests @ https://artifactory.company.com/python-packages/requests-2.32.3-py3-none-any.whl
This approach gives you maximum control over exactly which binary artifacts are used.
​
Pinned dependencies for reproducibility
To ensure consistent builds across environments, always pin your dependencies to exact versions:
​
✅ Recommended: Exact version pinning
requirements.txt
ibm-watsonx-orchestrate==2.4.0
requests==2.32.3
pydantic==2.8.2
numpy==1.24.0
​
❌ Not recommended: Unpinned or range versions
requirements.txt
# Avoid these patterns for production deployments
ibm-watsonx-orchestrate>=2.4.0  # May pull different versions over time
requests                         # Will pull latest version
pydantic~=2.8                   # May pull 2.8.x updates
Unpinned dependencies can lead to:
Different packages installed in DEV vs PROD
Unexpected behavior from minor/patch version changes
Hash mismatches causing unnecessary venv rebuilds
​
Hash-based verification for maximum security
For the highest level of reproducibility and security, use pip-compile to generate hashes:
# Generate requirements.txt with hashes
pip-compile --generate-hashes requirements.in -o requirements.txt
This produces a requirements.txt with cryptographic hashes:
requirements.txt
ibm-watsonx-orchestrate==2.4.0 \
    --hash=sha256:abc123... \
    --hash=sha256:def456...
requests==2.32.3 \
    --hash=sha256:789ghi... \
    --hash=sha256:012jkl...
When hashes are present, pip will verify that the downloaded package matches the expected hash, preventing:
Compromised packages
Registry tampering
Accidental version mismatches
​
Export/import vs Git-based promotion
Understanding the difference between these deployment approaches is crucial for choosing the right strategy.
​
Export/import model
What it provides:
Source code equivalence
Configuration portability
Quick environment setup
What it does NOT provide:
Binary package equivalence (packages are re-installed in target environment)
Guaranteed identical dependencies (unless using pinned versions + private registry)
When to use:
Moving agents between different watsonx Orchestrate instances
Sharing agents with other teams or organizations
Backing up agent configurations
Example workflow:
# Export from DEV environment
orchestrate agents export -n my-agent -k native -o my-agent.zip

# Import to QA environment (switch environment first)
orchestrate env set qa-environment
orchestrate agents import -f my-agent.zip
After import, the QA environment will run pip install using its own registry configuration, potentially pulling different package versions if dependencies are not pinned.
​
Git-based promotion
What it provides:
Version control integration
Commit-based traceability
Code review workflows
What it does NOT provide:
Binary package equivalence (packages are still re-installed)
Protection against registry changes (unless using locked Artifactory)
When to use:
Standard CI/CD pipelines
Promoting tested code through environments
Maintaining audit trails
Example workflow:
# Tag a tested commit in DEV
git tag v1.2.3-qa-ready
git push origin v1.2.3-qa-ready

# Deploy from that commit in QA
git checkout v1.2.3-qa-ready
orchestrate env set qa-environment
orchestrate agents import -f agents/my-agent.yaml
​
Achieving binary equivalence
Neither export/import nor Git-based promotion guarantees binary equivalence by default. To achieve it:
Pin all dependencies to exact versions in requirements.txt
Use a locked private registry (Artifactory/Nexus) with controlled package versions
Optional: Add hash verification with pip-compile --generate-hashes
Ensure the same registry configuration across all environments
Example locked requirements.txt:
requirements.txt
--index-url https://artifactory.company.com/api/pypi/python-locked/simple
ibm-watsonx-orchestrate==2.4.0 \
    --hash=sha256:abc123...
requests==2.32.3 \
    --hash=sha256:def456...
pydantic==2.8.2 \
    --hash=sha256:789ghi...
With this configuration:
✅ Same source code (via export/import or Git)
✅ Same dependency versions (pinned)
✅ Same binary packages (locked registry + hashes)
✅ Repeatable across all environments
​
Air-gapped environments
For deployments in air-gapped or restricted network environments, see the dedicated guide: Operating in an air-gapped environment.
Key considerations:
ADK and all dependencies must be uploaded to your internal registry
Use --index-url to point to your internal registry
Ensure all transitive dependencies are available
​
Best practices summary
Pin all versions
Use exact version pinning (==) in requirements.txt for all dependencies
Use private registries
Configure --index-url to pull from your organization’s Artifactory or Nexus
Add hash verification
Use pip-compile --generate-hashes for maximum security and reproducibility
Lock your registry
Prevent package additions/removals in your Artifactory between deployments
​
Recommended requirements.txt template
requirements.txt
# Use your organization's private registry
--index-url https://artifactory.company.com/api/pypi/python-virtual/simple

# Pin ADK version
ibm-watsonx-orchestrate==2.4.0

# Pin all dependencies with exact versions
requests==2.32.3
pydantic==2.8.2
python-dotenv==1.0.0

# Optional: Add hashes for verification (generated with pip-compile)
# ibm-watsonx-orchestrate==2.4.0 \
#     --hash=sha256:abc123...
​
Troubleshooting
​
Issue: Different packages installed in QA vs PROD
Cause: Unpinned dependencies or registry changes between deployments
Solution:
Pin all dependencies to exact versions
Use a locked Artifactory with controlled package versions
Verify registry configuration is identical across environments
​
Issue: Tool fails to import due to missing packages
Cause: Package not available in private registry
Solution:
Verify package exists in your Artifactory/Nexus
Check --index-url configuration in requirements.txt
Ensure network connectivity from watsonx Orchestrate to your registry
​
Issue: Slow deployment times
Cause: Virtual environment cache misses due to hash changes
Solution:
Use pinned versions to maximize cache hits
Avoid unnecessary changes to requirements.txt
Keep ADK version consistent across re-imports
​
Issue: Security scan failures
Cause: Packages pulled from public PyPI without scanning
Solution:
Use --index-url (not --extra-index-url) to prevent PyPI fallback
Configure your Artifactory to scan packages before making them available
Implement package approval workflows in your registry
​
Related resources
Authoring Python-Based Tools
Importing tools
Operating in an air-gapped environment
Managing tools

---

Authoring Langflow tools
Overview
Langflow is a powerful tool that enables developers to visually design, test, and deploy AI applications using a drag-and-drop interface.
Langflow comes bundled with the watsonx Orchestrate ADK. Any Langflow flow you create with Langflow can be imported into your watsonx Orchestrate environment and used as tools by your agents.
Follow these steps to author Langflow tools:
1
Create and share a Langflow flow

Start by building your Langflow flow in Langflow. Use global variables to define dynamic values and customize behavior.
Once your Langflow flow is ready, share it so it can be used in watsonx Orchestrate.

Langflow example

For more information, see Building Langflow tools.
2
Bind global variables to watsonx Orchestrate connections

During Langflow flow creation, you might configure global variables to support dynamic behavior. To ensure your Langflow flow works correctly in watsonx Orchestrate, bind these variables to the appropriate connections.
For more information, see Binding global variables to connections.
3
Import your Langflow flow into watsonx Orchestrate

Import your Langflow flow using ADK CLI. For more information, see Importing Langflow tools.
4
Optional: Manage your Langflow tool on watsonx Orchestrate

After importing your Langflow tool into watsonx Orchestrate, you can manage it using ADK CLI commands just like any other tool type. Use the CLI to list, update, delete, or export the Langflow JSON used to build the tool. For more information, see Managing tools.
5
Add your Langflow tool to an agent

In your agent file, configure the Langflow tool in the tools schema to make it available to your agent.
If you’re using watsonx Orchestrate Developer Edition, you can run the Langflow UI alongside Orchestrate services by adding the --with-langflow flag to the orchestrate server start command. For more information, see watsonx Orchestrate Developer Edition.
BASH
orchestrate server start -e <your-env-file> --with-langflow


---

Authoring Langflow tools
Langflow versions
watsonx Orchestrate Developer Edition includes Langflow 1.10.0 by default. Langflow 1.10.0 automatically installs its own matching LFX (Langflow Runner), so you don’t need additional configuration.
To run an older version of Langflow, install the version you want locally (outside ADK) from Langflow version history and specify the matching LFX version in your requirements.txt file before you import the flow into watsonx Orchestrate.
Use this table to identify the correct LFX version for your Langflow flow:
Langflow version	LFX version	Notes
1.5.0.post2	0.1.13	Initial GA release; requires explicit lfx specification
> 1.5.0.post2 and < 1.7.1	-	LFX version can be requested on demand; upgrade recommended
1.7.1	0.2.1	Previously ADK‑supported version
1.8.0	1.8.0 – 1.8.2	Compatible minor versions
1.8.1	1.8.3	Verified pairing
1.8.3	0.3.3	Verified pairing
1.9.x	Automatic	Compatible; lfx installed automatically
1.10.0	Automatic	Current ADK‑supported version; lfx installed automatically
Note:
Flows you create with Langflow versions earlier than 1.7.0 may fail or behave unpredictably because these versions lack integrated LFX support. To ensure compatibility:
Open the flow in the latest Langflow version. Use version 1.10.0 or later.
Update deprecated or incompatible components.
Export the flow again.
For Langflow 1.10.0, the system automatically installs the matching LFX runner. For older versions, add the correct LFX version to requirements.txt before you import the flow into watsonx Orchestrate.

---

Authoring Langflow tools
Prerequisites and limitations
Only key-value connection types are supported for Langflow flows.
You can use Langflow tools on watsonx Orchestrate Developer Edition, IBM Cloud, and AWS. However, you can only import them using ADK.
The exported Langflow tool name must contain only alphanumeric characters or underscores. It must not start with a number or an underscore.
Langflow does not support asynchronous execution, so if the Langflow tool takes longer than 120 seconds to respond, the agent returns an error.


---

Authoring Langflow tools
Building Langflow tools
Use the Langflow visual editor to build Langflow tools. It helps you quickly turn ideas into powerful, real-world solutions.
If you’re using watsonx Orchestrate Developer Edition, enable Langflow by starting it with the --with-langflow flag. If you’re not using the Developer Edition, install Langflow manually. For more information, see Install Langflow in the Langflow documentation.
Once you have access to the Langflow editor, start building your Langflow flow. The editor includes several pre-built templates that you can use as-is or customize to fit your needs. For more information, see Use the visual editor in the Langflow documentation.
When building Langflow flow for watsonx Orchestrate, configure dynamic values as global variables. Then, bind these variables to watsonx Orchestrate connections to maintain their dynamic behavior. For more information, see Binding global variables to connections.

Global variable example


---

Authoring Langflow tools
Binding global variables to connections
During Langflow flow creation, you might find fields that require dynamic inputs—such as API keys, user credentials, among others. These inputs typically depend on user-specific configuration to run the Langflow flow properly.
To handle this, configure these inputs as global variables in Langflow. These variables and their values are stored in your local environment.

Global variable example

Global variable names in Langflow must follow the format <app_id>_<variable>, where:
<app_id>: the connection ID defined in watsonx Orchestrate.
<variable>: the environment key defined in the connection.
Example:
langflow_app_USER_NAME
In this case, langflow_app is the connection ID, and USER_NAME is the environment key.
When you share a Langflow flow that includes global variables, Langflow stores the variable names. You can then bind these names to a watsonx Orchestrate connection to make the Langflow flow work correctly in your Orchestrate environment.
Example: Global variable example in shared Langflow flow JSON
{
  ...
  "sender_name": {
    "_input_type": "MessageTextInput",
    "advanced": false,
    "display_name": "Sender Name",
    "dynamic": false,
    "info": "Name of the sender.",
    "input_types": [
      "Message"
    ],
    "list": false,
    "list_add_label": "Add More",
    "load_from_db": true,
    "name": "sender_name",
    "placeholder": "",
    "required": false,
    "show": true,
    "title_case": false,
    "tool_mode": false,
    "trace_as_input": true,
    "trace_as_metadata": true,
    "type": "str",
    "value": "langflow_app_USER_NAME"
  },
  ...
}
See all 27 lines
Follow these steps to bind global variables to a watsonx Orchestrate connection:
1
Add and configure a connection

Add and configure a key-value connection. Currently, only key-value for “team” is supported. You can do this using a file import or the CLI. For more information, see Adding and configuring connections.
Example
orchestrate connections add -a <app_id>
orchestrate connections configure -a <app_id> --env draft -t team -k key_value
2
Set credentials for your connection

Configure the global variables and their values in your key-value connection. Use the orchestrate connections set-credentials command with the —entries (-e) flag to define each variable. For more information, see Key Value Connections.
Example
orchestrate connections set-credentials -a <app_id> --env draft -e <global-variables>=<value>
TIP:
If your environment already defines the global variables as environment variables, you can use them to set values in your watsonx Orchestrate connection. Instead of manually entering each value, reference the variable using the $ syntax. This allows Orchestrate to automatically retrieve the value from your system at runtime.
Example
orchestrate connections set-credentials -a langflow_app --env draft -e USER_NAME=$USER_NAME
After binding your global variables to a watsonx Orchestrate connection, use that connection when importing your Langflow flow into watsonx Orchestrate.


---

Authoring Langflow tools
Importing Langflow tools
Once you finish your Langflow flow, you can import it into watsonx Orchestrate. You have two options:
Import by Langflow flow name
Import by Langflow flow JSON
​
Importing Langflow flow using Langflow flow name
To import a flow by name, pass the Langflow flow name in the CLI import command. This method works only if you use Langflow integrated with watsonx Orchestrate Developer Edition during the import process. Otherwise, the command fails.
The command imports the latest version of the specified Langflow flow with its global variables. If a flow with the same name exists, the command updates it.
To import a Langflow flow using its name, run:
BASH
orchestrate tools import -k langflow -n <langflow-flow-name>
Show command flags

​
Importing Langflow flow using Langflow flow JSON
You can also import a flow using its exported JSON file. After you finish the flow, share it and export it as a JSON file for watsonx Orchestrate. When exporting, select Save with my API keys. For more information, see Import and export flows.

Save with my API keys option

Note:
If your Langflow flow uses global variables, bind these variables to watsonx Orchestrate connections first. For more information, see Binding global variables to connections.
Then, to import a Langflow flow, run:
BASH
orchestrate tools import -k langflow -f <json-file-path> -a <app-id> -r <requirements-file-path>
Hide command flags

Flag	Type	Required	Description
--kind / -k	string	Yes	The kind of tool to import, this is always langflow for Langflow based tools.
--file / -f	string	Yes	The path to the file of the shared JSON you want to import (or a URL containing the file).
--app-id / -a	string	No	The application ID of a connection related to your Langflow flow. Use connections to authenticate or configure global variables. You can include multiple --app-id flags if needed.
--requirements-file / -r	string	No	The path to a requirements.txt file that lists all Python packages needed to run the Langflow flow.


---

Tools
Managing tools
Managing tools in your active environment keeps your tools organized, current, and ready to use. Tools represent the capabilities your agents rely on, so proper management is essential for smooth operations.
​
Listing tools
To check which tools are in your environment, run the orchestrate tools list command. The output shows all available tools and includes details such as their unique names. To get complete information about each tool, use the verbose option. The verbose output returns the list in JSON format with every detail.
BASH
orchestrate tools list -v
Hide command flags

Flag	Type	Required	Description
--verbose (-n)	—	No	List full details of all tools in JSON format.
​
Exporting tools
To migrate a tool to another environment or share it with your team, run the orchestrate tools export command. Exporting saves time and ensures consistency across environments. This command supports Python, Agentic Workflow, Langflow, and OpenAPI tools imported via CLI.
BASH
orchestrate tools export -n <tool-name> -o <zip-output-path>
Hide command flags

Flag	Type	Required	Description
--name (-n)	string	Yes	The name of the tool you want to export. If you do not know the unique name, retrieve it from the orchestrate tools list command.
--output (-o)	string	Yes	Name of the zip file you would like to export the tool to.
Note:
When you export an agentic workflow tool it also exports all tools associated with that agentic workflow tool.
​
Updating tools
To refresh a tool’s configuration, run the orchestrate tools import command again with the same tool unique name. This action keeps the tool current and updated.
BASH
orchestrate tools import -k <kind of the tool> -f <path the tool file that you want to update> -a <id of the app> -r <path to the requirements.txt file>
Hide command flags

Flag	Type	Required	Description
—kind (-k)	string	Yes	The import source format. Possible values: openapi, python, mcp, flow, langflow
—file (-f)	string	No	The path to a Python file, OpenAPI spec YAML file, or agentic workflow JSON/Python file. Required for openapi, python and flow
—app-id (-a)	string	No	The app ID of the connection associated with this tool. An application connection represents the server authentication credentials needed to connect to this tool. Not applicable for agentic workflow tools.
—requirements-file (-r)	string	No	The path to the Python requirements.txt file. Required for python.
—package_root (-p)	string	No	When specified, the package root will be treated as the current working directory from which the module specified by --file will be invoked. All files and dependencies included in this folder will be included within the uploaded package. Local dependencies can either be imported relative to this package root folder or imported using relative imports from the --file. This only applies when the --kind=python. If not specified it is assumed only a single Python file is being uploaded.
​
Removing tools
To remove a tool you no longer need, run the orchestrate tools remove command. Removing unused tools keeps your environment clean and prevents accidental use of outdated tools.
BASH
orchestrate tools remove -n my-tool-name
Hide command flags

Flag	Type	Required	Description
--name (-n)	string	Yes	The name of the tool you want to remove. If you do not know the unique name, retrieve it from the orchestrate tools list command.
Note:
Agentic workflow tools support multi-language configurations. For details on managing translations, see Managing translations.

---

Tools
Logging behavior for Python tools in watsonx Orchestrate
Logging for Python tools in watsonx Orchestrate is intended to help support debugging during tool execution in watsonx Orchestrate SaaS, with clearly defined limits and lifecycle behavior.
The process describes the recommended approach for Python tool development. Start tool development without any dependency of Watson Orchestrate Developer edition or watsonx Orchestrate SaaS. Develop and run all tool unit tests with Python as the only required runtime, along with the open source watsonx Orchestrate ADK Python library and any additional dependencies used by the tool. When you are past the unit test phase, deploy your tool to Developer edition, where the developer has full access to the tool pod outputs. Afterward, deploy the tool to watsonx Orchestrate SaaS.
In SaaS, use the ibm_watsonx_orchestrate.run.logging.SpanLogger class, provided logs are captured per tool invocation and are made available as part of trace data for the tool execution, subject to size constraints.
​
Overview
When a Python tool runs in watsonx Orchestrate, the platform records execution details for that tool invocation to support observability and troubleshooting. To prevent excessive tool logs, overloading the system and to avoid the collection of sensitive customer data, tool logging behaves as follows:
Logs are collected per tool invocation
Logs are associated with the individual execution record of that tool in observability and 20 KB of most recent log data is available.
To aid performance, logs are written after tool execution completes
Process crash in user Python tool code is unexpected and rare. However, in such unexpected cases, only the exit code of the process is available.
​
Supported logging mechanism
Additionally, Python tools can write logs to observability by using the capability that is provided by watsonx Orchestrate:
PYTHON
from ibm_watsonx_orchestrate.run.logging import SpanLogger

logger = SpanLogger()
logger.info("Starting validation step")
logger.error("Failed to fetch employee record")
This logger is designed specifically for tool‑level observability and integrates directly with the watsonx Orchestrate tracing infrastructure. Over and above this specific logger, a tool can write logs to its owned external storage without any restrictions.
​
How tool logging works
The logging lifecycle for a Python tool invocation is as follows:
A tool invocation begins and an execution record for the tool is created.
Log messages that are written during execution are buffered in memory.
When the tool invocation completes, either successfully or with a handled exception, most recent buffered logs are written as part of the tool’s execution record.
The logs can be retrieved together with the execution trace data for that request.
​
Association with tool execution
Log entries that are generated by a Python tool are:
Associated with the span that represents that tool invocation
Part of the overall trace for the request
Retrieved together with traces by using the Traces API
This association allows tool logs to be correlated with the surrounding workflow and other spans in the same request.
​
Error and failure behavior
If a tool raises an exception that is handled by the runtime:
The tool’s span is marked with status ERROR.
Recent buffered log entries are written to the tool span.
The trace remains available for the standard trace retention period.
This behavior provides visibility into both the error status and the tool logs associated with a failed invocation.
Tool logs are written only after execution completes or fails with a handled exception. If the process stops unexpectedly, only the exit code is recorded.
​
Log retention and limits
To prevent excessive tool logs overloading the system, ibm_watsonx_orchestrate.run.logging.SpanLogger logs are subject to the following constraints:
Only the most recent log entries are retained.
The total amount of log data per invocation is capped (approximately 20 KB).
Individual log entries have a maximum size.
When limits are exceeded, older log entries are discarded first.
This logging mechanism is intended to provide context around error paths and failures.
​
Intended usage
This logging capability is designed to:
Support edge‑case debugging for watsonx Orchestrate SaaS tool execution through observability.
Provide contextual information when tools fail.
Enable observability through trace inspection in development and production environments.
​
Recommendations for logging
Persistent, high‑volume, or detailed logging is handled by the tool writing to external storage such as S3 or dedicated logging services.
To enable correlation with watsonx Orchestrate execution data, include the request thread identifier when you log in externally:
PYTHON
thread_id = context.request_context.get("thread_id")
External logs can be correlated with the corresponding tool execution.

---

Toolkits
Overview
Toolkits group related tools so you can import or remove them in one action. You use toolkits to organize and manage tools efficiently in watsonx Orchestrate.
watsonx Orchestrate supports two toolkit types:
MCP toolkits: Group MCP server tools (Python or Node.js) for local or remote execution
Python toolkits: Group Python tools to run together in a single process for better performance
Choosing between toolkits and standalone tools:
Toolkits offer performance benefits but require specific considerations. For help deciding between standalone Python tools, Python toolkits, local MCP toolkits, remote MCP toolkits, and OpenAPI tools, see Choosing a tool type.
​
MCP toolkits
Use MCP toolkits to integrate tools built with the Model Context Protocol (MCP). MCP toolkits support both local and remote execution:
Local MCP toolkits:
Run inside the watsonx Orchestrate runtime using stdio transport
Support Python and Node.js implementations
Can be imported from npm, PyPI, or local filesystem
Behave like standalone Python tools with process-per-invocation model
Suitable for tools that need MCP protocol features or Node.js runtime
Remote MCP toolkits:
Connect to external MCP servers via HTTP (SSE or streamable HTTP)
Run on your infrastructure or third-party services
Support multiple authentication methods
Add network latency but enable centralized tool management
For detailed guidance on when to use local vs remote MCP toolkits, see Choosing a tool type.
​
Python toolkits
Use Python toolkits to bundle multiple related Python tools that run together in a single Python process. This approach eliminates process startup overhead and provides better performance for frequently called tools.
Key characteristics:
Tools share the same Python process and dependencies
No process overhead after initial startup (saves 100-300ms per call)
Requires all tools to be thread-safe and reentrant
In live premium environments, each toolkit gets dedicated resources (2 vCPUs, 2 GB memory)
Supports up to 10 concurrent requests per toolkit
When to use Python toolkits:
You have multiple related Python tools
Tools are called frequently (>10 times per minute)
All tools are thread-safe
You want to minimize execution overhead
When to use standalone Python tools instead:
Tools use non-thread-safe operations
Tools are called infrequently
You need process isolation between calls
For migration guidance from standalone tools to toolkits, see Migrating to Python toolkits.
​
Tool naming convention
When you import a toolkit, watsonx Orchestrate exposes each tool within it individually using the naming format:
toolkit_name:tool_name
Example:
# Toolkit name: customer_service
# Tools in toolkit: get_customer, update_customer, create_ticket

# Exposed tool names:
customer_service:get_customer
customer_service:update_customer
customer_service:create_ticket
This naming convention ensures tools from different toolkits don’t conflict, even if they have the same base name. When migrating from standalone tools to toolkits, you must update agent configurations to use the new toolkit_name:tool_name format.
​
Next steps
Choosing a tool type - Decision guide for selecting the right tool type
Importing Python toolkits - How to create and import Python toolkits
Importing local MCP toolkits - How to import local MCP servers
Importing remote MCP toolkits - How to connect to remote MCP servers
Migrating to Python toolkits - Step-by-step migration guide
Managing toolkits - How to update and remove toolkits

---

Toolkits
Choosing a tool type
When building tools for watsonx Orchestrate, you can choose from several deployment options. Each option offers different tradeoffs in performance, complexity, and operational characteristics. This guide helps you select the right tool type for your scenario.
​
Available tool types
watsonx Orchestrate supports the following tool types:
Standalone Python tools: Individual Python tools that run in isolated processes
Python toolkits: Groups of related Python tools that run together in a single Python process
Local MCP toolkits: MCP servers (Python or Node.js) that run inside the watsonx Orchestrate runtime
Remote MCP toolkits: MCP servers hosted externally that watsonx Orchestrate connects to via HTTP
OpenAPI tools: REST API endpoints defined by OpenAPI specifications
​
Decision framework
Use this decision tree to identify the best tool type for your needs:








Yes

No

External/Cloud

Inside Orchestrate

Python

Node.js

Yes

No

Yes

No

Unsure

Yes

No

Start: What are you building?

Existing REST API?

Use OpenAPI tools

Where will tools run?

Use Remote MCP toolkit

Language preference?

Multiple related tools?

Use Local MCP toolkit

Are tools thread-safe?

Use Standalone Python tool

Use Python toolkit

High concurrency expected?

Make thread-safe, use Python toolkit

​
Detailed comparison
​
Standalone Python tools
Use when:
You have a single, independent tool
The tool uses non-thread-safe operations (file I/O, global state, etc.)
You need process isolation between tool invocations
You’re prototyping or testing a new tool
Characteristics:
Each tool invocation starts a lightweight Python process
Full process isolation ensures no state leakage between calls
Supports non-thread-safe operations without modification
Higher execution overhead due to process startup
Simpler to develop and debug
Performance:
Draft environment: Runs in shared container per tenant (2 vCPUs, 2 GB memory, 5 workers)
Live environment: Same shared container model
Process overhead: ~100-300ms per invocation for process startup
Example use cases:
Tools that write to temporary files
Tools using libraries with global state
Infrequently called tools where startup overhead is acceptable
Prototype tools during development
​
Python toolkits
Use when:
You have multiple related Python tools
All tools are thread-safe and reentrant
You expect high concurrency or frequent tool calls
You want to minimize execution overhead
Characteristics:
Groups related tools in a single Python process
Tools share the same process and can share dependencies
Requires all tools to be thread-safe
Significantly faster execution (no process startup overhead)
Tools deploy and update together as a unit
Performance:
Draft environment: Runs in shared container per tenant (2 vCPUs, 2 GB memory, 5 workers)
Live premium environment: Each toolkit gets dedicated container (2 vCPUs, 2 GB memory, 5 workers, 2 replicas)
Process overhead: None after initial startup
Concurrency: Up to 5 concurrent requests per toolkit
Example use cases:
Suite of data transformation tools
Multiple tools accessing the same API or service
High-frequency tools called repeatedly by agents
Tools sharing common utility functions or dependencies
Requirements:
All tools must be thread-safe
No global mutable state
No file system writes (read-only filesystem)
​
Local MCP toolkits
Use when:
You have existing MCP servers (Python or Node.js)
You want to use Node.js for tool development
You need the MCP protocol’s features (resources, prompts, etc.)
You want to share tools across multiple AI platforms
Characteristics:
Runs MCP servers inside watsonx Orchestrate runtime
Supports both Python and Node.js implementations
Can import from npm, PyPI, or local filesystem
Behaves like standalone Python tools (process per invocation)
Full MCP protocol support
Performance:
Similar to standalone Python tools
Process startup overhead per invocation
Supports stdio transport only (local execution)
Example use cases:
Existing MCP servers you want to reuse
Node.js-based tools
Tools that need MCP resources or prompts
Cross-platform tool sharing
​
Remote MCP toolkits
Use when:
Tools must run in external infrastructure
You need to integrate cloud services or third-party APIs
You want centralized tool management across multiple Orchestrate instances
You have existing remote MCP servers
Characteristics:
MCP server runs externally (your infrastructure or third-party)
watsonx Orchestrate connects via HTTP (SSE or streamable HTTP)
Supports multiple authentication methods
Network latency added to each tool call
Centralized updates without redeploying to Orchestrate
Performance:
Network latency: typically 50-200ms per call
Depends on remote server’s performance
No local resource consumption
Example use cases:
Integration with cloud services (AWS, Azure, GCP)
Third-party MCP servers (GitHub Copilot, CoinGecko, etc.)
Tools requiring specialized infrastructure
Centrally managed tools used by multiple tenants
​
OpenAPI tools
Use when:
You have existing REST APIs
You want to expose HTTP endpoints as tools
You don’t need custom Python logic
You want declarative tool definitions
Characteristics:
Defined by OpenAPI specifications
No custom code required
Automatic schema validation
Supports various authentication methods
Direct HTTP calls to your APIs
Performance:
Network latency depends on API location
No local processing overhead
Scales with your API infrastructure
Example use cases:
Existing microservices or REST APIs
Third-party API integrations
CRUD operations on databases
Webhook-based integrations
​
Performance considerations
​
Execution overhead comparison
Tool Type	Process Startup	Network Latency	Best For
Standalone Python tool	~100-300ms	None	Low-frequency calls
Python toolkit	None (after init)	None	High-frequency calls
Local MCP toolkit	~100-300ms	None	Node.js or MCP features
Remote MCP toolkit	Minimal	50-200ms	External services
OpenAPI tool	None	50-200ms	REST APIs
​
Concurrency and scaling
Python toolkits (live premium):
5 workers per toolkit
2 replicas per toolkit
Up to 10 concurrent requests per toolkit
Dedicated resources (2 vCPUs, 2 GB per toolkit)
Standalone Python tools and Local MCP toolkits:
Share tenant-wide container
5 workers total across all tools
2 replicas
Suitable for moderate concurrency
Remote MCP toolkits:
Scaling depends on remote server
No local resource limits
Network becomes the bottleneck
​
Thread safety requirements
​
What makes a tool thread-safe?
A tool is thread-safe when multiple threads can call it concurrently without causing race conditions or data corruption.
Thread-safe patterns:
# ✅ Good: No shared state
@tool()
def calculate_sum(numbers: list[int]) -> int:
    return sum(numbers)

# ✅ Good: Immutable shared data
CONSTANTS = {"pi": 3.14159, "e": 2.71828}

@tool()
def get_constant(name: str) -> float:
    return CONSTANTS.get(name)

# ✅ Good: Thread-local storage
import threading
thread_local = threading.local()

@tool()
def process_data(data: str) -> str:
    thread_local.temp = data.upper()
    return thread_local.temp
Non-thread-safe patterns:
# ❌ Bad: Global mutable state
counter = 0

@tool()
def increment_counter() -> int:
    global counter
    counter += 1  # Race condition!
    return counter

# ❌ Bad: File system writes
@tool()
def save_to_file(data: str) -> str:
    with open("/tmp/data.txt", "w") as f:  # Multiple threads conflict
        f.write(data)
    return "saved"

# ❌ Bad: Non-thread-safe library
import some_library  # Assume this has global state

@tool()
def use_library(input: str) -> str:
    some_library.set_config(input)  # Affects all threads
    return some_library.process()
​
Making tools thread-safe
If your tool has non-thread-safe operations:
Remove global mutable state: Use function parameters instead
Use thread-safe libraries: Check library documentation
Add synchronization: Use threading.Lock() for critical sections
Keep as standalone tool: If thread-safety is too complex
​
Migration scenarios
​
From standalone Python tool to Python toolkit
When to migrate:
Tool is called frequently (>10 times per minute)
You have multiple related tools
You’ve verified thread-safety
You want better performance in live environment
Migration steps:
Verify all tools are thread-safe
Create toolkit folder structure
Move tool files into toolkit
Update imports if needed
Import as toolkit
Test in draft environment
Update agents to use toolkit_name:tool_name format
Deploy to live environment
For detailed migration instructions, see Migrating to Python toolkits.
​
From Python toolkit to standalone tools
When to migrate:
Discovering thread-safety issues in production
Tools are called infrequently
Tools have conflicting dependencies
Need independent tool updates
Migration steps:
Export each tool from toolkit
Import each as standalone tool
Update agent configurations
Test thoroughly
Remove old toolkit
​
From local MCP to Python toolkit
When to migrate:
Want better performance (eliminate process overhead)
Don’t need MCP-specific features
Tools are Python-based and thread-safe
Want dedicated resources in live environment
Migration steps:
Extract Python code from MCP server
Convert to @tool decorated functions
Ensure thread-safety
Import as Python toolkit
Update agent configurations
Test and validate
​
Choosing based on ownership and dependencies
​
Shared dependencies
Use Python toolkit when:
Multiple tools use the same libraries
Dependencies are large (reduces memory usage)
Tools need to share utility functions
Use standalone tools when:
Tools have conflicting dependency versions
Each tool has unique dependencies
You want independent dependency updates
​
Ownership boundaries
Use separate toolkits when:
Different teams own different tools
Tools have different update schedules
You want independent deployment
Use single toolkit when:
One team owns all tools
Tools are tightly coupled
You want atomic updates
​
Environment-specific considerations
​
Draft environment
All Python toolkits and tools share one container per tenant
Process overhead exists for all tool types
Good for testing and development
Resource limits: 2 vCPUs, 2 GB memory, 5 workers
Recommendation: Use standalone tools in draft for easier debugging, then migrate to toolkits for live deployment.
​
Live environment (premium)
Each Python toolkit gets dedicated container
No process overhead for toolkit tools
Better isolation and performance
Up to 5 toolkits per tenant
Recommendation: Use Python toolkits for production workloads to maximize performance.
​
Live environment (non-premium)
Similar to draft environment
Shared container model
Contact support for toolkit access
Recommendation: Use standalone tools or request premium access for toolkits.
​
Best practices summary
Start simple: Begin with standalone Python tools during development
Measure performance: Profile your tools to identify bottlenecks
Group related tools: Bundle tools that share dependencies or are called together
Ensure thread-safety: Test thoroughly before using Python toolkits
Monitor concurrency: Track concurrent requests to avoid worker exhaustion
Plan for scaling: Consider expected load when choosing tool type
Document dependencies: Clearly specify shared dependencies in toolkits
​
Next steps
Authoring Python tools
Importing Python toolkits
Importing local MCP toolkits
Importing remote MCP toolkits
Migrating to Python toolkits
Managing toolkits


---

Toolkits
Importing local MCP toolkits
The 2.0 release introduces a breaking change: the former orchestrate toolkits import command has been renamed to orchestrate toolkits add. Additionally, a new orchestrate toolkits import command has been added, which works on files in a way that is the inverse of the orchestrate toolkits export command.
Local MCP toolkits run MCP servers inside the watsonx Orchestrate runtime using the stdio transport. They support both Python and Node.js implementations and can be imported from npm, PyPI, or your local filesystem.
When to use local MCP toolkits:
You have existing MCP servers you want to reuse
You need Node.js for tool development
You want MCP protocol features (resources, prompts, etc.)
You want to share tools across multiple AI platforms
Performance characteristics:
Similar to standalone Python tools with process-per-invocation model
Process startup overhead of approximately 100-300ms per call
Suitable for moderate-frequency tool calls
For help choosing between local MCP toolkits, remote MCP toolkits, Python toolkits, and standalone Python tools, see Choosing a tool type.
​
Adding directly from the CLI
Use the orchestrate toolkits add command to add a local MCP toolkit into your environment.
BASH
orchestrate toolkits add
Show command flags

Examples:
Adding from pypi
Importing from npm
Local Python
Local Nodejs
BASH
# Setup connection if not already set
orchestrate connections add -a tavily
for env in draft live; do
    orchestrate connections configure -a tavily --env $env --type team --kind key_value
    orchestrate connections set-credentials -a tavily --env $env -e "TAVILY_API_KEY=$TAVILY_API_KEY"
done

# Import the toolkit
# Note this is a third party mcp server for illustrative purposes only, use the npm variant for production use
orchestrate toolkits add --kind mcp \
  --name tavily \
  --description "Search the internet" \
  --command "pipx  -y mcp-tavily@0.1.10" \
  --tools "*"  \
  --app-id tavily
​
Importing from a file
It is also possible to import an MCP server configuration from a file. The file contains the same configuration options used by the add command, within a yaml file, but is easier to integrate with import scripts and CI/CD pipelines.
BASH
orchestrate connections add -a my_connection
for env in draft live; do
    orchestrate connections configure -a my_connection --env $env --type team --kind key_value
    orchestrate connections set-credentials -a my_connection --env $env -e "SECURE_ENVIRONMENT_VARIABLE=value"
done

orchestrate toolkits import -f toolkit_name.yaml -a my_connection
toolkit_name.yaml
spec_version: v1
kind: mcp
name: toolkit_name
command: uvx ibm-watsonx-orchestrate-mcp-server
env: []
tools:
  - *
connections:
  - my_connection
package_root: ./my_toolkit_folder # <-- This is the folder containing your mcp server. The path is relative to this file.
​
Supported connection types for local MCP servers
Local MCP servers can use multiple connection types, and each connection type exposes a specific set of environment variables to the server. These variables allow MCP tools to read the required credentials directly at runtime. The following environment variables are provided for each connection type:
Basic Connections

Bearer Connections

API Key Connections

OAuth (Client Credentials)

OAuth (Auth Code)

🚧 OAuth (Implicit)

OAuth (Password)

🌐 OAuth (SSO/IDP Flow)

Key Value Connections

​
Comparing local MCP toolkits with other options
Local MCP vs Python toolkits:
Use local MCP when you need Node.js or MCP-specific features
Use Python toolkits for better performance with frequently called Python tools (no process overhead)
Local MCP vs Remote MCP:
Use local MCP when tools run inside Orchestrate infrastructure
Use remote MCP when tools must run on external infrastructure or cloud services
Local MCP vs Standalone Python tools:
Use local MCP when you need Node.js or want to reuse existing MCP servers
Use standalone Python tools for simpler Python-only tools without MCP protocol needs
For detailed comparison and decision guidance, see Choosing a tool type.
​
Next steps
Choosing a tool type - Decision guide for selecting the right tool type
Importing remote MCP toolkits - Connect to external MCP servers
Importing Python toolkits - Bundle Python tools for better performance
Managing toolkits - Update and remove toolkits


---

Toolkits
Importing remote MCP toolkits
The 2.0 release contains a breaking change renaming what was previously the orchestrate toolkits import command as the orchestrate toolkits add command. A new orchestrate toolkits import command was introduced which operates on files in manner inverse from the orchestrate toolkits export command.
Remote MCP integration lets you connect watsonx Orchestrate to external toolkits hosted on remote servers. Use this setup when your tools live outside your local environment, such as in cloud services or third-party APIs. You can import and manage them using the ADK CLI.
When to use remote MCP toolkits:
Tools must run on external infrastructure (cloud services, third-party APIs)
You need centralized tool management across multiple Orchestrate instances
You have existing remote MCP servers to integrate
Tools require specialized infrastructure not available in Orchestrate
Performance characteristics:
Network latency added to each tool call (typically 50-200ms)
No local resource consumption in Orchestrate
Scaling depends on your remote server infrastructure
Tradeoffs:
Pros: Centralized updates, external infrastructure, no local resource limits
Cons: Network latency, requires external hosting, more complex deployment
For help choosing between remote MCP toolkits, local MCP toolkits, Python toolkits, and standalone Python tools, see Choosing a tool type.
​
Adding remote MCP toolkits using ADK CLI
To import a remote MCP, run the orchestrate toolkits add command with the URL and transport protocol for the MCP server.
BASH
orchestrate toolkits add --kind mcp --name <toolkit-name> --description <toolkit-description>  --url <toolkit-url>  --transport <protocol-for-remote-mcp> --tools <tools>  --app-id <connection>
Show command flags

Examples:
Using SSE
Using streamable HTTP
This example connects watsonx Orchestrate to CoinGecko remote MCP server using SSE. For more information, see CoinGecko MCP Server
BASH
orchestrate toolkits add --kind mcp --name coingecko --description "coingecko toolkit"  --url "https://mcp.api.coingecko.com/sse"  --transport "sse" --tools "get_range_coins_market_chart"
​
Importing from a file
You can also import an MCP server configuration from a file. The file contains the same configuration options used by the add command, within a yaml file, but is easier to integrate with import scripts and CI/CD pipelines.
BASH
orchestrate connections add -a my_connection
for env in draft live; do
    orchestrate connections configure -a my_connection --env $env --type team --kind key_value
    orchestrate connections set-credentials -a my_connection --env $env -e "SECURE_ENVIRONMENT_VARIABLE=value"
done

orchestrate toolkits import -f toolkit_name.yaml -a my_connection
toolkit_name.yaml
spec_version: v1
kind: mcp
name: toolkit_name
transport: streamable_http # streamable_http|sse
server_url: http://my-mcp-server/mcp
tools:
  - *
connections:
  - my_connection
​
Understanding the import process
During import, ADK connects to the remote MCP server to retrieve and validate available tools.
ADK checks only the tool schemas for structural correctness and compatibility with watsonx Orchestrate. It doesn’t test tool execution at this stage.
watsonx Orchestrate waits up to 30 seconds for the server to respond with the tool list. If the server responds in time, the import continues. If not, the process fails or times out.
ADK doesn’t test individual tools during import, so no execution timeouts apply at this stage.
​
Importing toolkits with SSO/OBO connections
When a toolkit is associated with an SSO/OBO (On-Behalf-Of) connection, watsonx Orchestrate attempts to obtain a valid access token from the identity provider during import. This fails at import time because there is no authenticated end user available — SSO/OBO tokens require a real user session to perform the token exchange.
As a result, toolkit import fails when the associated connection uses the oauth_auth_on_behalf_of_flow authentication kind.
Recommended workaround
Use different connection configurations for the draft and live environments:
Environment	Connection kind	Purpose
draft	key_value (with placeholder credentials)	Allows toolkit import to succeed. Most MCP servers do not require authentication for tool discovery (tools/list).
live	oauth_auth_on_behalf_of_flow (SSO/OBO)	Ensures that tool execution uses the authenticated end user’s identity at runtime.
Setting up environment-specific connections:
BASH
# Step 1: Create a key_value connection for draft (used for import only)
orchestrate connections add -a my_sso_obo_connection

# Configure draft with key_value (placeholder credentials are sufficient)
orchestrate connections configure -a my_sso_obo_connection \
    --env draft --type team --kind key_value
orchestrate connections set-credentials -a my_sso_obo_connection \
    --env draft -e "PLACEHOLDER=value"

# Configure live with SSO/OBO for tool execution
orchestrate connections configure -a my_sso_obo_connection \
    --env live --type member --kind oauth_auth_on_behalf_of_flow

# Step 2: Import the toolkit (uses draft key_value connection — succeeds)
orchestrate toolkits import -f my_toolkit.yaml -a my_sso_obo_connection
After this setup, toolkit import runs against the draft environment using the key_value connection and succeeds. When the agent runs in the live environment, the SSO/OBO connection provides a user-scoped access token for each tool execution.
This behavior applies specifically to remote MCP toolkits where the import process calls the MCP server’s tools/list endpoint. If your MCP server requires authentication even for tool discovery, configure the draft connection with credentials that satisfy the server’s listing endpoint requirements instead of using a placeholder key_value connection.
​
Choosing an MCP protocol
ADK supports two transport protocols for MCP:
Server-Sent Events (SSE)
Streamable HTTP
You must choose the transport protocol explicitly. ADK doesn’t support fallback or automatic switching between protocols.
Any MCP server that follows the standard protocol and supports SSE or streamable HTTP works without extra configuration.
When you use the ADK CLI, Remote MCP supports multiple authentication methods:
OAuth2 (without Dynamic Client Registration)
API Key
Bearer Token
Basic Auth
Key-value
Note:
When connecting to a remote MCP server that uses an API key with a custom name, use the key–value pair method.
For OAuth authentication, import the toolkit using Team credentials. To use the tool, you can either switch to Member credentials or continue using Team credentials.
For more information about connections, see Connections.
​
Tracing, tenant and agent context
When Orchestrate calls a remote MCP server through the MCP Gateway, it automatically includes standard tracing information so downstream services can participate in the same request trace for observability and debugging. The tracing context (traceparent and tracestate) is always included and passed in the request metadata. This behavior is built in and requires no configuration.
You can also attach correlation identifiers that help with governance, audit logging, and usage attribution. These values are passed as request headers:
tenant_id: identifies the customer or tenant
agent_id: identifies the calling agent
The following example shows an MCP server definition that includes contextual metadata:
YAML
spec_version: v1
kind: mcp
name: doc-mcp
description: helps you talk to the manager
url: https://developer.watson-orchestrate.ibm.com/mcp
transport: streamable_http
metadata:
    allowed_context:
        - my_context_1
        - my_context_2To
tenant_id and agent_id are not sent by default. You must configure them when you import the remote MCP server or toolkit in the ADK. The tracing context (traceparent, tracestate) is always included and is not configurable.
​
Using SSE protocol
When you use SSE, ADK starts the handshake with a 30-second timeout. This timeout applies during the callback phase of the import.
ADK expects only standard SSE headers. The connection setup stays minimal and depends on the server for protocol compliance.
ADK doesn’t enforce connection pooling or keep-alive settings. If your server supports them, ADK works with those features.
​
Comparing remote MCP toolkits with other options
Remote MCP vs Local MCP:
Use remote MCP when tools must run on external infrastructure or cloud services
Use local MCP when tools can run inside Orchestrate and you want to avoid network latency
Remote MCP vs Python toolkits:
Use remote MCP when you need external infrastructure or want centralized tool management
Use Python toolkits for better performance with Python tools running inside Orchestrate (no network latency)
Remote MCP vs OpenAPI tools:
Use remote MCP when you need MCP protocol features (resources, prompts, streaming)
Use OpenAPI tools for simple REST API integrations without MCP protocol overhead
For detailed comparison and decision guidance, see Choosing a tool type.
​
Next steps
Choosing a tool type - Decision guide for selecting the right tool type
Importing local MCP toolkits - Run MCP servers inside Orchestrate
Importing Python toolkits - Bundle Python tools for better performance
Managing toolkits - Update and remove toolkits
During tool execution testing, you might see End of File (EOF) errors. These usually happen when the server times out or doesn’t respond in time.
​
Using streamable HTTP protocol
When you use streamable HTTP, ADK also starts the handshake with a 30-second timeout.
ADK doesn’t expect SSE headers in this case. The setup remains minimal and relies on the server to follow the protocol.
​
Handling import errors
If the server returns an HTTP status code in the 4xx range, the import fails. These errors usually point to invalid requests, authentication issues, or missing resources.
Other status codes may trigger warnings, depending on the server’s response.
ADK doesn’t distinguish between import-time and runtime execution from the server’s perspective. All responses during import return in JSON format.

---

Toolkits
Importing Python toolkits
After you create your Python tools, import them as a Python toolkit. A Python toolkit groups related tools so you can deploy and run them together in a single Python process. To meet this goal, design every tool in the toolkit to be thread-safe and reentrant. This approach gives you faster execution because the tools share the same process.
When you run Python tools outside a toolkit (as standalone Python tools), the system starts a lightweight process each time the tool runs. This design supports tools that use non-thread-safe operations, but it increases execution time by approximately 100-300ms per invocation compared to a toolkit.
When to use Python toolkits vs standalone Python tools:
Use Python toolkits when you have multiple related tools that are thread-safe, called frequently, or share dependencies
Use standalone Python tools when tools use non-thread-safe operations, are called infrequently, or need process isolation
For detailed guidance, see Choosing a tool type.
To create a Python toolkit, place all required Python tools in one folder. Each tool can include one or more Python files. In those files, define your functions and apply the @tool decorator so watsonx Orchestrate exposes each function as a usable tool.
You can place tools that multiple agents use into a single toolkit. When you update tools inside a toolkit, redeploy all related agents to the live environment so you use the updated versions. Choose the number of tools in each toolkit based on the level of concurrent requests you expect. For more information, see CPU and memory allocation for Python toolkits.
​
CPU and memory allocation for Python toolkits
Draft environment:
All imported Python toolkits and Python tools run in a single Kubernetes deployment container per tenant
Process overheads per tool call exist in draft (approximately 100-300ms per invocation)
Container resources: 2 vCPUs, 2 GB of memory, and 5 workers
Deployment supports two replicas
Live environment (Premium plan):
You can import up to five Python toolkits per tenant
Each toolkit runs in its own dedicated Kubernetes deployment container
No process overheads per tool call — tools run in a persistent process
Container resources per toolkit: 2 vCPUs, 2 GB of memory, and 5 workers
Each deployment supports two replicas
Supports up to 10 concurrent requests per toolkit (5 workers × 2 replicas)
Live environment (Non-Premium plan):
--tier is not enabled by default — contact support to request access.
Performance optimization: In live premium environments, Python toolkits eliminate process startup overhead, reducing tool execution time by 100-300ms per call compared to standalone Python tools. For frequently called tools (>10 calls/minute), this can significantly improve agent response times.
​
Add Python toolkits using the ADK CLI
Use the orchestrate toolkits add command to add a Python toolkit.
BASH
orchestrate toolkits add \
  --kind python \
  --name <toolkit-name> \
  --description <toolkit-description> \
  --tier <deployment-tier> \
  --package_root <toolkit-path>
Note:
--tier is required when importing a Python toolkit. Premium plan customers only — contact support to request access.
Show command flags

​
Import Python toolkits from a file
You can also import a Python toolkit from a YAML file. This file defines the same configuration options as the add command and fits well into import scripts and CI/CD pipelines.
Use the orchestrate toolkits import command to import a toolkit from a file.
BASH
orchestrate toolkits import -f <path to spec> --app-id <connection>
Show command flags

For the YAML file, configure the following:
​
spec_version
stringrequired
The version of the YAML specification.
​
kind
stringrequired
The type of toolkit. For Python toolkits, use python.
​
name
stringrequired
The name of the toolkit.
​
description
string
The description of the toolkit.
​
environment
object
Key-value pairs for the toolkit.
Example:
toolkit_name.yaml
spec_version: v1
kind: python
name: toolkit_name
description: A toolkit sample
environment:
    key1: value1
​
Thread-safety requirements
All tools in a Python toolkit must be thread-safe because they run in a shared process with concurrent requests. A tool is thread-safe when multiple threads can call it simultaneously without causing race conditions or data corruption.
Thread-safe patterns:
No global mutable state
Use immutable data structures
Use thread-safe libraries
Non-thread-safe patterns to avoid:
Global variables that change
File system writes
Non-thread-safe libraries
Shared database connections without pooling
For detailed guidance on thread-safety and migration from standalone tools, see Migrating to Python toolkits.


---

Toolkits
Migrating to Python toolkits
This guide helps you migrate existing standalone Python tools into Python toolkits for improved performance and resource efficiency in production environments.
​
Why migrate to Python toolkits?
Python toolkits offer significant advantages over standalone Python tools in production:
Performance benefits:
No process overhead: Tools run in a persistent process, eliminating 100-300ms startup time per call
Shared resources: Tools share dependencies and memory, reducing overall resource usage
Dedicated containers: In live premium environments, each toolkit gets its own container with 2 vCPUs and 2 GB memory
Operational benefits:
Atomic updates: All tools in a toolkit update together, ensuring consistency
Simplified management: Deploy and manage related tools as a single unit
Better scaling: Dedicated resources in live environments support higher concurrency
When to migrate:
Tools are called frequently (>10 times per minute)
You have multiple related tools that share dependencies
You need better performance in production
You’ve verified all tools are thread-safe
When NOT to migrate:
Tools use non-thread-safe operations
Tools are called infrequently
Tools have conflicting dependencies
You need independent tool updates
For help deciding, see Choosing a tool type.
​
Prerequisites
Before migrating, ensure your tools meet these requirements:
​
1. Thread-safety verification
All tools in a Python toolkit must be thread-safe. Review each tool for:
Common thread-safety issues:
Global mutable state
File system writes
Non-thread-safe libraries
Shared database connections without pooling
Race conditions in shared resources
Testing for thread-safety:
import concurrent.futures
from your_tool import my_tool

def test_concurrent_calls():
    """Test tool with concurrent requests"""
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(my_tool, f"input_{i}") for i in range(10)]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]
    
    # Verify all results are correct and independent
    assert len(results) == 10
    assert len(set(results)) == 10  # All unique if expected

test_concurrent_calls()
​
2. Dependency compatibility
Verify that all tools can use the same dependency versions:
# Check for conflicting dependencies
cat tool1/requirements.txt tool2/requirements.txt | sort | uniq -d
If tools require different versions of the same package, they cannot be in the same toolkit.
​
3. Shared utility functions
Identify common code that can be shared:
Authentication helpers
Data transformation utilities
API client wrappers
Validation functions
​
Migration process
​
Step 1: Identify candidate tools
List all standalone Python tools and group them by:
Functional relationship:
Tools that work with the same API or service
Tools that perform related operations
Tools that share business logic
Usage patterns:
Frequently called tools (>10 calls/minute)
Tools called together by the same agents
Tools with similar performance requirements
Example grouping:
Customer Service Toolkit:
  - get_customer_info
  - update_customer_address
  - create_support_ticket

Data Processing Toolkit:
  - validate_csv
  - transform_data
  - export_results
​
Step 2: Create toolkit folder structure
Organize your tools into a toolkit folder:
my_toolkit/
├── requirements.txt          # Shared dependencies
├── __init__.py              # Optional: shared utilities
├── tool1.py                 # First tool
├── tool2.py                 # Second tool
├── tool3.py                 # Third tool
└── utils/                   # Optional: shared modules
    ├── __init__.py
    ├── auth.py
    └── helpers.py
Best practices:
Use descriptive folder names (e.g., customer_service_toolkit)
Keep one tool per file for clarity
Place shared code in utils/ or __init__.py
Include comprehensive requirements.txt
​
Step 3: Consolidate dependencies
Merge requirements.txt files from all tools:
# Combine all requirements
cat tool1/requirements.txt tool2/requirements.txt tool3/requirements.txt | sort | uniq > my_toolkit/requirements.txt
Resolve version conflicts:
# Before (conflicting versions)
# tool1/requirements.txt
requests==2.28.0

# tool2/requirements.txt
requests==2.31.0

# After (choose compatible version)
# my_toolkit/requirements.txt
requests==2.31.0  # Use latest compatible version
Pin all dependencies:
# ✅ Good: Exact versions
requests==2.31.0
pydantic==2.5.0
httpx==0.25.0

# ❌ Bad: Unpinned versions
requests
pydantic>=2.0
httpx~=0.25
​
Step 4: Refactor tool code
Update each tool file to work in a toolkit context:
Before (standalone tool):
# customer_tool.py
from ibm_watsonx_orchestrate.agent_builder.tools import tool
import requests

@tool(name="get_customer")
def get_customer(customer_id: str) -> dict:
    """Get customer information"""
    response = requests.get(f"https://api.example.com/customers/{customer_id}")
    return response.json()
After (toolkit tool):
# customer_toolkit/get_customer.py
from ibm_watsonx_orchestrate.agent_builder.tools import tool
import requests

@tool(name="get_customer")
def get_customer(customer_id: str) -> dict:
    """Get customer information"""
    response = requests.get(f"https://api.example.com/customers/{customer_id}")
    return response.json()
Key changes:
Remove global mutable state
Ensure all functions are thread-safe and reentrant
Use thread-safe libraries
​
Step 5: Extract shared utilities
Move common code to shared modules:
Before (duplicated code):
# tool1.py
def authenticate():
    return {"Authorization": "Bearer token"}

@tool()
def tool1():
    headers = authenticate()
    # ...

# tool2.py
def authenticate():
    return {"Authorization": "Bearer token"}

@tool()
def tool2():
    headers = authenticate()
    # ...
After (shared utilities):
# my_toolkit/utils/auth.py
def get_auth_headers() -> dict:
    """Get authentication headers"""
    return {"Authorization": "Bearer token"}

# my_toolkit/tool1.py
from .utils.auth import get_auth_headers

@tool()
def tool1():
    headers = get_auth_headers()
    # ...

# my_toolkit/tool2.py
from .utils.auth import get_auth_headers

@tool()
def tool2():
    headers = get_auth_headers()
    # ...
​
Step 6: Update tool names
When you import a toolkit, tool names change to include the toolkit prefix:
Naming convention:
toolkit_name:tool_name
Example:
# Before (standalone)
Tool name: get_customer

# After (in toolkit named "customer_service")
Tool name: customer_service:get_customer
Document the name changes:
# Tool Name Mapping

| Old Name | New Name |
|----------|----------|
| get_customer | customer_service:get_customer |
| update_customer | customer_service:update_customer |
| create_ticket | customer_service:create_ticket |
​
Step 7: Import the toolkit
Import your toolkit using the ADK CLI:
# Import toolkit
orchestrate toolkits add \
  --kind python \
  --name customer_service \
  --description "Customer service tools for support agents" \
  --package_root ./customer_service_toolkit \
  --tier small
Verify import:
# List all tools in the toolkit
orchestrate tools list | grep "customer_service:"
Expected output:
customer_service:get_customer
customer_service:update_customer
customer_service:create_ticket
​
Step 8: Update agent configurations
Update all agents that use the migrated tools:
Before (standalone tools):
# agent.yaml
spec_version: v1
kind: native
name: support_agent
tools:
  - get_customer
  - update_customer
  - create_ticket
After (toolkit tools):
# agent.yaml
spec_version: v1
kind: native
name: support_agent
tools:
  - customer_service:get_customer
  - customer_service:update_customer
  - customer_service:create_ticket
Update and redeploy agents:
# Update agent configuration
orchestrate agents import -f agent.yaml

# Deploy to live environment
orchestrate agents publish -n support_agent
​
Step 9: Test in draft environment
Thoroughly test the toolkit before deploying to live:
Functional testing:
# Test each tool individually
orchestrate agents chat -n support_agent -m "Get customer info for ID 12345"
orchestrate agents chat -n support_agent -m "Update customer address"
orchestrate agents chat -n support_agent -m "Create a support ticket"
Concurrency testing:
# test_concurrency.py
import concurrent.futures
from ibm_watsonx_orchestrate import OrchestrateChatClient

def test_concurrent_requests():
    client = OrchestrateChatClient()
    
    # Send 10 concurrent requests
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [
            executor.submit(client.chat, agent="support_agent", message=f"Get customer {i}")
            for i in range(10)
        ]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]
    
    # Verify all succeeded
    assert all(r.status == "success" for r in results)
    print("✅ Concurrency test passed")

test_concurrent_requests()
Performance testing:
# Measure response times
time orchestrate agents chat -n support_agent -m "Get customer 12345"
Compare with standalone tool performance to verify improvement.
​
Step 10: Deploy to live environment
After successful testing in draft:
# Publish agent to live
orchestrate agents publish -n support_agent

# Verify in live environment
orchestrate env switch live
orchestrate tools list | grep "customer_service:"
Monitor performance:
Check response times
Monitor error rates
Verify concurrent request handling
Review resource usage
​
Step 11: Remove old standalone tools
After confirming the toolkit works correctly:
# Remove old standalone tools
orchestrate tools remove -n get_customer
orchestrate tools remove -n update_customer
orchestrate tools remove -n create_ticket
Important: Only remove standalone tools after:
All agents are updated and tested
Toolkit is deployed to live
No agents reference the old tool names
​
Common migration patterns
​
Pattern 1: Simple consolidation
Scenario: Multiple independent tools with no shared code
Before:
tools/
├── tool1.py
├── tool2.py
└── tool3.py
After:
my_toolkit/
├── requirements.txt
├── tool1.py
├── tool2.py
└── tool3.py
Steps:
Create toolkit folder
Move tool files
Consolidate requirements.txt
Import as toolkit
​
Pattern 2: Shared utilities extraction
Scenario: Tools with duplicated helper functions
Before:
tools/
├── tool1.py  # Contains auth_helper()
├── tool2.py  # Contains auth_helper() (duplicate)
└── tool3.py  # Contains auth_helper() (duplicate)
After:
my_toolkit/
├── requirements.txt
├── __init__.py
├── utils/
│   ├── __init__.py
│   └── auth.py  # Shared auth_helper()
├── tool1.py     # Imports from utils.auth
├── tool2.py     # Imports from utils.auth
└── tool3.py     # Imports from utils.auth
Steps:
Identify duplicated code
Extract to shared module
Update imports in all tools
Test thoroughly
​
Pattern 3: Multi-file tool consolidation
Scenario: Standalone tools with package roots
Before:
tool1/
├── requirements.txt
├── main.py
└── helpers/
    └── utils.py

tool2/
├── requirements.txt
├── main.py
└── helpers/
    └── utils.py
After:
my_toolkit/
├── requirements.txt
├── tool1/
│   ├── main.py
│   └── helpers/
│       └── utils.py
└── tool2/
    ├── main.py
    └── helpers/
        └── utils.py
Steps:
Create toolkit folder
Move each tool into subfolder
Consolidate requirements.txt
Update relative imports if needed
​
Handling special cases
​
Non-thread-safe tools
If a tool cannot be made thread-safe:
Option 1: Keep as standalone tool
# Keep problematic tool separate
orchestrate tools import -k python -f non_threadsafe_tool.py

# Import other tools as toolkit
orchestrate toolkits add --kind python --name my_toolkit --package_root ./toolkit
Option 2: Add synchronization
import threading

# Add lock for non-thread-safe operations
_lock = threading.Lock()

@tool()
def non_threadsafe_tool(input: str) -> str:
    with _lock:
        # Critical section - only one thread at a time
        result = perform_non_threadsafe_operation(input)
    return result
​
Conflicting dependencies
If tools require different versions:
Option 1: Separate toolkits
# Create separate toolkits
orchestrate toolkits add --kind python --name toolkit_a --package_root ./toolkit_a
orchestrate toolkits add --kind python --name toolkit_b --package_root ./toolkit_b
Option 2: Update to compatible versions
# Test with newer version
pip install package==2.0.0
# Run tests
pytest tests/

# If successful, update requirements.txt
echo "package==2.0.0" >> requirements.txt
​
Connection remapping
If tools use different connection names:
# Before (tool1 uses "api_connection")
@tool(expected_credentials=[{"app_id": "api_connection", "type": ConnectionType.API_KEY}])
def tool1():
    conn = connections.api_key("api_connection")

# Before (tool2 uses "service_connection")
@tool(expected_credentials=[{"app_id": "service_connection", "type": ConnectionType.API_KEY}])
def tool2():
    conn = connections.api_key("service_connection")

# After (standardize on one connection)
@tool(expected_credentials=[{"app_id": "shared_connection", "type": ConnectionType.API_KEY}])
def tool1():
    conn = connections.api_key("shared_connection")

@tool(expected_credentials=[{"app_id": "shared_connection", "type": ConnectionType.API_KEY}])
def tool2():
    conn = connections.api_key("shared_connection")
​
Validation checklist
Before deploying to production, verify:
All tools are thread-safe
Dependencies are consolidated and pinned
Shared utilities are extracted
Tool names are documented
Agent configurations are updated
Tests pass in draft environment
Concurrency tests pass
Performance meets expectations
Error handling is robust
Logging is adequate
Documentation is updated
Rollback plan is ready
​
Rollback procedure
If issues occur after migration:
​
Immediate rollback
# Switch back to draft
orchestrate env switch draft

# Reimport standalone tools
orchestrate tools import -k python -f tool1.py
orchestrate tools import -k python -f tool2.py
orchestrate tools import -k python -f tool3.py

# Revert agent configurations
orchestrate agents import -f agent_backup.yaml

# Publish to live
orchestrate agents publish -n support_agent
​
Gradual rollback
# Keep toolkit but add standalone versions
orchestrate tools import -k python -f tool1.py -n tool1_standalone

# Update agent to use standalone version
# Edit agent.yaml to use tool1_standalone instead of toolkit:tool1

# Test and verify
orchestrate agents chat -n support_agent -m "test message"

# If successful, remove toolkit
orchestrate toolkits remove -n my_toolkit
​
Performance optimization
After migration, optimize toolkit performance:
​
1. Connection pooling
# Use connection pooling for HTTP clients
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import threading

# Create a thread-local session for connection reuse
_thread_local = threading.local()

def get_session() -> requests.Session:
    if not hasattr(_thread_local, "session"):
        session = requests.Session()
        adapter = HTTPAdapter(
            pool_connections=10,
            pool_maxsize=20,
            max_retries=Retry(total=3, backoff_factor=0.5)
        )
        session.mount("https://", adapter)
        _thread_local.session = session
    return _thread_local.session

@tool()
def my_tool() -> dict:
    session = get_session()
    response = session.get("https://api.example.com/data", timeout=30)
    return response.json()
​
2. Caching
from functools import lru_cache

# Cache expensive computations
@lru_cache(maxsize=128)
def expensive_computation(input: str) -> str:
    # Expensive operation
    return result

@tool()
def my_tool(input: str) -> str:
    result = expensive_computation(input)
    return result
​
3. Efficient request batching
import requests

# ✅ Good: Batch requests where the API supports it
@tool()
def fetch_multiple(ids: list[str]) -> list[dict]:
    response = requests.get(
        "https://api.example.com/items/batch",
        params={"ids": ",".join(ids)},
        timeout=30
    )
    return response.json()

# ✅ Also acceptable: Sequential requests (simple and predictable)
@tool()
def fetch_multiple_sequential(ids: list[str]) -> list[dict]:
    results = []
    session = requests.Session()
    for id in ids:
        response = session.get(f"https://api.example.com/api/{id}", timeout=30)
        results.append(response.json())
    return results
​
Monitoring and troubleshooting
​
Monitor toolkit health
# Check toolkit status
orchestrate toolkits list -v

# View tool execution logs
orchestrate logs --agent support_agent --filter "customer_service:"

# Monitor resource usage
orchestrate toolkits stats -n customer_service
​
Common issues
Issue: Tools timing out
Solution: Increase timeout or optimize tool code
- Check for blocking operations
- Add connection pooling
Issue: Memory errors
Solution: Reduce memory usage
- Limit concurrent requests
- Clear caches periodically
- Process data in chunks
Issue: Race conditions
Solution: Add synchronization
- Use threading.Lock for critical sections
- Avoid global mutable state
- Test with high concurrency
​
Next steps
Choosing a tool type
Managing toolkits
Python toolkit documentation
Authoring Python tools
Performance guide

---

Toolkits
Managing toolkits
Manage the toolkits in your active environment.
​
Listing toolkits
Use the orchestrate tools list command to list all tools in your environment. You can also use the --verbose (-v) flag to get detailed information about each tool in JSON format.
BASH
orchestrate toolkits list -v
Exporting remote MCP toolkits with the ADK CLI enables you to package and distribute custom tool integrations for watsonx Orchestrate. This process ensures consistent agent workflows across environments and simplifies deployment for development, testing, or production. Use this capability when you need to share toolkits with other teams, migrate configurations, or maintain version control for your MCP integrations.
​
Exporting remote MCP toolkits using ADK CLI
Use the ADK CLI to export a remote MCP toolkit configuration for deployment or integration.
BASH
orchestrate toolkits export -n my-toolkit -o my-toolkit.zip
​
Updating toolkits
You can update Python toolkits and MCP toolkits in watsonx Orchestrate, but each type follows a different process.
Important: When you update a toolkit, all agents using tools from that toolkit must be redeployed to use the updated versions. Plan toolkit updates carefully to minimize disruption to production agents.
​
Updating Python toolkits
You can update a Python toolkit by importing it again with your updated specifications. When you import the toolkit, watsonx Orchestrate replaces the existing version so you can continue working with the latest changes.
Update process:
Make changes to your toolkit code
Test changes locally
Import the updated toolkit (replaces existing version)
Test in draft environment
Redeploy all agents that use the toolkit
Publish agents to live environment
BASH
orchestrate toolkits add \
  --kind python \
  --name my-toolkit-name \
  --description "helps you talk to the manager" \
  --language python \
  --package <python-package-name> \
  --package_root <path-to-package-root> \
  --tier small
​
Updating local and remote MCP toolkits
Unlike Python toolkits, you cannot update an MCP toolkit in place. Instead, you must remove the existing toolkit and reimport it with the new specifications.
Update process:
1
Delete the existing toolkit

BASH
orchestrate toolkits remove -n my-toolkit-name
2
Import the toolkit with the new specs

BASH
  orchestrate toolkits add \
      --kind mcp \
      --name my-toolkit-name \
      --description "helps you talk to the manager" \
      --package_root /path/to/folder \
      --command '["node", "dist/index.js", "--transport", "stdio"]' \
      --tools "*" \
      --app-id "my_app_id" 
3
Redeploy all agents that use the toolkit

After reimporting the toolkit, you must redeploy all agents that use tools from this toolkit to ensure they use the updated version.
BASH
# Update agent configuration if needed
orchestrate agents import -f agent.yaml

# Publish to live environment
orchestrate agents publish -n my-agent
For more information, see Importing agents.
Migration consideration: If you’re frequently updating MCP toolkits and the remove/reimport process is disruptive, consider migrating to Python toolkits which support in-place updates. For guidance, see Migrating to Python toolkits.
​
Removing toolkits
Removing a toolkit will remove all tools provided by that toolkit. Before removing a toolkit, ensure no agents are using tools from it.
Removal process:
Identify all agents using the toolkit
Update agents to remove toolkit tool references
Redeploy updated agents
Remove the toolkit
BASH
# Check which agents use the toolkit
orchestrate tools list | grep "my-toolkit-name:"

# After updating agents, remove the toolkit
orchestrate toolkits remove -n my-toolkit-name
Important: Removing a toolkit while agents still reference its tools will cause those agents to fail when they try to use the removed tools. Always update and redeploy agents before removing a toolkit.
​
Agent redeployment considerations
When you update or remove toolkits, you must redeploy affected agents:
Why redeployment is required:
Agents cache tool definitions at deployment time
Updated toolkit tools won’t be available until agents are redeployed
Removed toolkit tools will cause errors if agents aren’t updated first
Best practices:
Test in draft first: Update toolkits and test with agents in draft environment
Update agents atomically: Update all related agents together to maintain consistency
Use version control: Track toolkit and agent configurations in version control
Plan maintenance windows: Schedule toolkit updates during low-traffic periods
Monitor after deployment: Watch for errors after redeploying agents with updated toolkits
Redeployment workflow:
BASH
# 1. Update toolkit in draft
orchestrate env switch draft
orchestrate toolkits add --kind python --name my-toolkit --package_root ./my-toolkit

# 2. Test with agents in draft
orchestrate agents chat -n my-agent -m "test message"

# 3. Deploy to live
orchestrate env switch live
orchestrate toolkits add --kind python --name my-toolkit --package_root ./my-toolkit

# 4. Redeploy all affected agents
orchestrate agents publish -n agent1
orchestrate agents publish -n agent2
orchestrate agents publish -n agent3

# 5. Verify in live
orchestrate agents chat -n my-agent -m "test message"
​
Next steps
Choosing a tool type - Decision guide for selecting the right tool type
Migrating to Python toolkits - Migrate standalone tools to toolkits
Importing Python toolkits - Create and import Python toolkits
Importing local MCP toolkits - Import local MCP servers
Importing remote MCP toolkits - Connect to remote MCP servers


----

Connections
Why use connections
A connection represents a dependency on an external application or service. It contains all the necessary information for agents, tools, knowledge bases, or virtual models to securely authenticate and interact with that external system.
​
Types of connections
watsonx Orchestrate supports several types of authentication methods:
Basic, Bearer, and API Key: These methods pass the configured credentials directly to the consuming tool or service.
OAuth: Orchestrate supports multiple OAuth flows, as defined in the OpenAPI specification. When using OAuth:
Orchestrate authenticates the user interactively.
It generates an access_token on behalf of the user.
This token is securely passed to the downstream tool during execution.
OAuth-based connections currently only work when the user interacts with the agent through the watsonx Orchestrate UI (not embedded web chat).
When you embed web chat in an external website, Orchestrate supports integration with upstream SSO/IDP providers such as Azure AD, Workday CCX, and others.
Orchestrate also supports Key-Value connections, which allow builders to provide a secure dictionary of keys and values to downstream tools. You can use these connections to:
Pass arbitrary authentication configurations to Python tools.
Securely provide environment variables to MCP toolkits.
Configure connections to LLM providers through the AI Gateway.
Legend
✅ Supported ❌ Not supported 🚧 Partially supported (native agents only)
​
Support by tool type
Authentication Kind	Python	OpenAPI	Agentic workflows [1]	Local MCP Toolkits	Remote MCP Toolkits	Langflow
Basic Auth	✅	✅	✅	❌	✅	❌
Bearer Token	✅	✅	✅	❌	✅	❌
API Key	✅	✅	✅	❌	✅	❌
OAuth (Client Credentials) [2]	✅	✅	✅	❌	✅	❌
OAuth (Auth Code) [2]	✅	✅	✅	❌	✅	❌
OAuth (Implicit) [2]	🚧	🚧	✅	❌	❌	❌
OAuth (Password) [2]	✅	✅	✅	❌	✅	❌
OAuth (SSO/IDP Flow) [3] [4]	✅	✅	✅	❌	❌	❌
Key-Value	✅	❌	✅	✅	❌	✅
[1] Tools built using Agentic workflows do not require connection support as connections within Agentic workflows are configured via their downstream component tools.
[2] OAuth connections are currently only supported by agents in the watsonx Orchestrate integrated web chat ui.
[3] SSO/IDP connections are only supported by agents in web chat embedded into a customer’s website.
[4] SSO/OBO (oauth_auth_on_behalf_of_flow) connections cannot be used to import remote MCP toolkits because no authenticated user session is available at import time. Use a key_value connection for the draft environment import and reserve SSO/OBO for the live environment where tool execution occurs with a real user session. See Importing toolkits with SSO/OBO connections.
​
Support for knowledge
Authentication Kind	Milvus	Elastic Search	Custom Search
Basic Auth	✅	✅	✅
Bearer Token	❌	❌	❌
API Key	❌	✅	✅
OAuth (Client Credentials) [2]	❌	❌	❌
OAuth (Auth Code) [2]	❌	❌	❌
OAuth (Implicit) [2]	❌	❌	❌
OAuth (Password) [2]	❌	❌	❌
OAuth (SSO/IDP Flow) [3]	❌	❌	❌
Key-Value	❌	❌	❌
​
Support for member vs team
Authentication Kind	member (per user)	team (shared)
Basic Auth	✅	✅
Bearer Token	✅	✅
API Key	✅	✅
OAuth (Client Credentials)	✅	✅
OAuth (Auth Code)	✅	✅
OAuth (Implicit)	🚧	🚧
OAuth (Password)	✅	✅
OAuth (SSO/IDP Flow)	✅	✅
Key-Value	❌	✅
​
Support for AI Gateway
The AI Gateway supports only key-value connections.


---

Connections
Creating connections
Connections are composed of three parts:
Application ID (app_id): A unique identifier that distinguishes the connection within your environment.
Environment-specific configuration: Define separate configurations for the draft and live states of an agent. Each configuration specifies:
The type of credentials used (for example, Basic Auth, Bearer Token, API Key)
Whether the credentials are scoped to individual users (member) or shared across the organization (team)
Credentials:
For team connections, builders set the credentials, and all users share them across the instance.
For member connections, users are prompted in the chat to enter their credentials if they haven’t already provided them.
​
Adding and configuring connections
You can add and configure connections in two ways:
Use a combination of the connections add and connections configure commands to define and set up connections manually.
Import connections from a YAML file, just like other watsonx Orchestrate resources.
Importing from a file
Using the CLI only
You can create and import connection configurations using YAML files, which makes it easier to share setup details across users. However, you must set credentials separately using the CLI. This requirement helps prevent storing sensitive information like passwords in unsecured files.
In your YAML specification file, define the connection’s structure, including:
Application ID (app_id)
Authentication type
Environment-specific settings (e.g., draft vs. live)
Credential scope (member or team)
YAML
spec_version: v1
kind: connection
app_id: my_app
resource:
    component: knowledge
    category: milvus
environments:
    draft:  # in draft each person needs to provide their own basic credentials
        kind: basic
        type: team
        server_url: https://example.com/
        custom_config_entries: # Optional
            key1: value1
            key2: value2
    live:
        kind: api_key # note it's possible to auth different in the deployed live agent vs the draft agent
        type: member
        server_url: https://example.com/
Show detailed flag descriptions

To import this connection, run:
BASH
orchestrate connections import -f my_app.yaml
​
Example connection configuration files per type
Basic Connections

A Basic connection contains two secure fields (username and password), and one insecure field (server_url).
my_app.yaml
spec_version: v1
kind: connection
app_id: my_app
environments:
    draft:  # in draft each person needs to provide their own basic credentials
        kind: basic
        type: team
        server_url: https://example.com/
    live:
        kind: basic
        type: team
        server_url: https://example.com/
Bearer Connections

An Bearer connection contains one secure field called a token, and one insecure field for the server_url.
my_app.yaml
spec_version: v1
kind: connection
app_id: my_app
environments:
    draft:  # in draft each person needs to provide their own basic credentials
        kind: bearer
        type: team
        server_url: https://example.com/
    live:
        kind: bearer
        type: team
        server_url: https://example.com/
API Key Connections

An API key connection contains one secure field called an api_key, and one insecure field for the server_url.
my_app.yaml
spec_version: v1
kind: connection
app_id: my_app
environments:
    draft:  # in draft each person needs to provide their own basic credentials
        kind: api_key
        type: team
        server_url: https://example.com/
    live:
        kind: api_key
        type: team
        server_url: https://example.com/
Key Value Connections

Key-value connections allow you to pass an arbitrary set of keys and values to upstream providers. These connections are especially useful in Python tools when you need secure configuration options that don’t fit into standard authentication categories.
You can also use key-value connections to securely inject environment variables into MCP servers, enabling flexible and secure runtime configuration.
my_app.yaml
spec_version: v1
kind: connection
app_id: my_app
environments:
    draft:
        kind: key_value
        type: team
    live:
        kind: key_value
        type: team
OAuth auth code flow

OAuth Auth Code Flows provide a downstream service a field called an access_token which can be used used as an Bearer token by your tool.
**my_app.yaml**
spec_version
kind: connection
app_id: my_app
environments:
    draft:
        kind: oauth_auth_code_flow
        type: team
        server_url: https://example.com/
    live:
        kind: oauth_auth_code_flow
        type: team
        server_url: https://example.com/
🚧 OAuth auth implicit flow

OAuth Implicit Flows provide a downstream service a field called an access_token which can be used used as an Bearer token by your tool.
**my_app.yaml**
spec_version
kind: connection
app_id: my_app
environments:
    draft:
        kind: oauth_auth_implicit_flow
        type: team
        server_url: https://example.com/
    live:
        kind: oauth_auth_implicit_flow
        type: team
        server_url: https://example.com/
OAuth auth password flow

OAuth Auth Password Flows provide a downstream service a field called an access_token which can be used used as an Bearer token by your tool.
**my_app.yaml**
spec_version
kind: connection
app_id: my_app
environments:
    draft:
        kind: oauth_auth_password_flow
        type: team
        server_url: https://example.com/
    live:
        kind: oauth_auth_password_flow
        type: team
        server_url: https://example.com/
OAuth auth client credentials flow

OAuth Auth Client Flows provide a downstream service a field called an access_token which can be used used as an Bearer token by your tool.
my_app.yaml
spec_version
kind: connection
app_id: my_app
environments:
    draft:
        kind: oauth_auth_client_credentials_flow
        type: team
        server_url: https://example.com/
    live:
        kind: oauth_auth_client_credentials_flow
        type: team
        server_url: https://example.com/
Oauth auth direct access flow

Use an Oauth auth direct access flow connection to configure direct access for a team member in the draft environment.
Configure the connection with:
orchestrate connections configure --app-id direct --environment draft --type-member --kind oauth_auth_direct_access_flow --sso --server-url=url.
SSO / IDP auth (on behalf of single exchange)

OAuth Token Exchange enables a one-time token exchange between an identity provider (IDP) and a downstream service on behalf of a user. Unlike the full on-behalf-of flow, this approach is optimized for scenarios where only a single delegated request is needed, reducing overhead while maintaining secure access.
This feature is ideal for lightweight integrations or actions that require temporary, delegated authentication without establishing a persistent session.
my_app.yaml
spec_version: "v1"
kind: "connection"
app_id: my_app
environments:
draft:
    kind: oauth_auth_token_exchange
    type: member
    sso: true
    server_url: www.example.com
    app_config:
    header:
        content-type: application/x-www-form-urlencode
🌐 SSO / IDP auth (on behalf of flow)

OAuth on-behalf-of flows authenticate against an identity provider that can issue tokens to downstream services on behalf of a user. This enables secure, delegated access to external systems.
Currently, watsonx Orchestrate supports these flows only for agents accessed through embedded web chat.
YAML
spec_version: v1
kind: connection
app_id: workdaysso
environments:
  draft:
    kind: oauth_auth_on_behalf_of_flow
    type: member
    sso: true
    server_url: https://TBD.workday.com/ccx
    idp_config:
      header:
        content-type: application/x-www-form-urlencoded
      body:
        requested_token_use: on_behalf_of
        requested_token_type: urn:ietf:params:oauth:token-type:saml2
    app_config:
      header:
        content-type: application/x-www-form-urlencode
  live:
    kind: oauth_auth_on_behalf_of_flow
    type: member
    sso: true
    server_url: https://TBD.workday.com/ccx
    idp_config:
      header:
        content-type: application/x-www-form-urlencoded
      body:
        requested_token_use: on_behalf_of
        requested_token_type: urn:ietf:params:oauth:token-type:saml2
    app_config:
      header:
        content-type: application/x-www-form-urlencoded
​
Setting Credentials
Once a connection has been configured, you can set its credentials using either the CLI or the UI.
​
Setting credentials via the UI
Once you’ve added a connection, you can manage its credentials through the Connections Management UI, located under Manage → Connections.
For member connections, each end user sets their own credentials through this interface.
Connections UI
Connections UI

Note: In the watsonx Orchestrate Developer Edition, you can only set credentials using the CLI. The UI does not support credential management in this edition. As a result, you can only fully configure OAuth connections in the SaaS or on-premises offerings, where both CLI and UI credential setup are supported.
​
Setting credentials via the CLI
Alternatively, you can set connection credentials via the CLI to more easily script agent setup.
​
Basic Connections
BASH
orchestrate connections set-credentials -a application_id \
  --env draft \
  -u username \
  -p password
Show command flags

​
Bearer Connections
BASH
orchestrate connections set-credentials -a application_id \
  --env draft \
  --token thebearertoken
Hide command flags

​
--env
enumvalues: draft, live
You can choose to set credentials for either the draft environment (used in the Manage Agents preview) or the live environment, depending on where the agent will operate.
​
--token
string
The Bearer token to send.
​
API Key Connections
BASH
orchestrate connections set-credentials -a application_id \
  --env draft \
  --api-key theapikey
Hide command flags

​
--env
enumvalues: draft, live
You can choose to set credentials for either the draft environment (used in the Manage Agents preview) or the live environment, depending on where the agent will operate.
​
--api-key / -k
string
The API key to send.
​
Key Value Connections
BASH
orchestrate connections set-credentials -a application_id \
  --env draft \
  -e 'key1=value1' \
  -e 'key2=value2'
Hide command flags

​
--env
enumvalues: draft, live
You can choose to set credentials for either the draft environment (used in the Manage Agents preview) or the live environment, depending on where the agent will operate.
​
--entries / -e
string
A key-value pair can be used to securely pass configuration data to downstream tools or AI gateway providers. Entries are provided in the form key=value.
​
OAuth
OAuth supports multiple authentication flows, as outlined in the OpenAPI specification. watsonx Orchestrate can use these flows to generate authentication tokens for compatible downstream consumers.
Unlike other authentication methods, such as Basic Auth or API Key, where tools receive the same credentials that were configured, OAuth connections dynamically resolve an access_token within Orchestrate. The platform generates this token on behalf of the tool and securely provides it during execution.
Auth Code Flow
BASH
orchestrate connections set-credentials -a application_id \
  --env draft \
  --client-id 'clientid' \
  --client-secret 'clientsecret' \
  --authorization-url 'https://api.example.com/oauth2/authorize' \
  --token-url 'https://api.example.com/oauth2/token' \
  --scope admin
Hide command flags

​
--env / --environment
string
You can choose to set credentials for either the draft environment (used in the Manage Agents preview) or the live environment, depending on where the agent will operate
​
--client-id
string
The OAuth connection’s client ID. This value uniquely identifies the application (watsonx Orchestrate) to the OAuth provider.
​
--client-secret
string
The OAuth connection’s client secret. This value authenticates the application (watsonx Orchestrate) with the OAuth provider.
​
--send-via
string
Specifies how to send the OAuth credentials. Supported values: header, body.
​
--token-url
string
The URL where watsonx Orchestrate exchanges the user authorization, client ID, and client secret to obtain an access token.
​
--scope
string
A comma-separated list of OAuth scopes to request. These scopes define the permissions granted to the generated token for accessing the upstream service provider.
​
--token-entries / -t
string
Define custom field options for an OAuth request.
Use key-value pairs in the format location:<key>=<value> or <key>=<value>.
You can pass multiple values like this: -t key1=value1 -t location:key2=value2.
Valid locations are: header, body, and query. If you omit the location, it defaults to header.
​
--auth-entries
string
Define custom field options for an oauth_auth_code_flow auth server request.
Use key-value pairs in the format location:<key>=<value> or <key>=<value>.
You can pass multiple values like this: —auth-entries key1=value1 —auth-entries location:key2=value2.
The only valid location is query, which also serves as the default if you omit it.
🚧 Implicit flow
Currently, watsonx Orchestrate does not support OAuth implicit flows.  Support for this feature is coming soon.
Password flow
BASH
orchestrate connections set-credentials -a application_id \
  --env draft \
  --client-id 'clientid' \
  --client-secret 'clientsecret' \
  --username 'username' \
  --password 'password' \
  --token-url 'https://api.example.com/oauth2/token' \
  --scope admin
Hide command flags

​
--env
string
You can choose to set credentials for either the draft environment (used in the Manage Agents preview) or the live environment, depending on where the agent will operate
​
--client-id
string
The clientId of the OAuth connection. This is used to uniquely identify the application (watsonx Orchestrate) to the oauth provider.
​
--client-secret
string
The clientSecret of the Oauth connection. This is used to authentication the application (watsonx Orchestate) to the oauth provider.
​
--token-url
string
This is the url watsonx Orchestrate will exchange the user authorization, client id and secret to to fetch an access token.
​
--scope
string
A comma separated list of oauth scopes to request for the user to grant the generated token certain privileged accesses to the upstream service provider.
Client Credentials flow
BASH
orchestrate connections set-credentials -a application_id \
  --env draft \
  --client-id 'clientid' \
  --client-secret 'clientsecret' \
  --token-url 'https://api.example.com/oauth2/token' \
  --scope admin
Hide command flags

​
--env
string
You can choose to set credentials for either the draft environment (used in the Manage Agents preview) or the live environment, depending on where the agent will operate
​
--client-id
string
The clientId of the OAuth connection. This is used to uniquely identify the application (watsonx Orchestrate) to the oauth provider.
​
--client-secret
string
The clientSecret of the Oauth connection. This is used to authentication the application (watsonx Orchestate) to the oauth provider.
​
--send-via
string
A comma separated list of oauth scopes to request for the user to grant the generated token certain privileged accesses to the upstream service provider.
​
--token-url
string
This is the url watsonx Orchestrate will exchange the user authorization, client id and secret to to fetch an access token.
​
--scope
string
A comma separated list of oauth scopes to request for the user to grant the generated token certain privileged accesses to the upstream service provider.
​
🌐 SSO / IDP auth (on behalf of single exchange)
Single exchange uses the OAuth Token Exchange grant to perform a one-time delegated exchange on behalf of the user. It’s ideal for lightweight actions that need temporary, delegated access without establishing a persistent session.
BASH
orchestrate connections set-credentials \
  -a my_app \
  --env draft \
  --grant-type "urn:ietf:params:oauth:grant-type:token-exchange" \
  --client-id "<client_id>" \
  --token-url "<token_url>"
Hide command flags

​
--env
string
Choose the environment where the agent operates: draft (Manage Agents preview) or live.
​
--client-id
string
The OAuth connection’s client ID. Uniquely identifies watsonx Orchestrate to the OAuth provider.
​
--token-url
string
The OAuth token endpoint where watsonx Orchestrate performs the token exchange.
​
--grant-type
string
For single exchange, use urn:ietf:params:oauth:grant-type:token-exchange.
​
--token-entries / -t
string
Define custom field options for an OAuth request.

Use key-value pairs in the format location:&lt;key&gt;=&lt;value&gt; or &lt;key&gt;=&lt;value&gt;.

You can pass multiple values like this: -t key1=value1 -t location:key2=value2.

Valid locations are: header, body, and query. If you omit the location, it defaults to header.
​
🌐 SSO / IDP auth (on behalf of flow)
BASH
orchestrate connections set-identity-provider --app-id workday \
  --env draft \
  --url https://idp-server/oauth2/v2.0/token \
  --client-id clientid \
  --client-secret clientsecret \
  --scope scope \
  --grant-type urn:ietf:params:oauth:grant-type:jwt-bearer
Hide command flags

​
--env
string
You can choose to set credentials for either the draft environment (used in the Manage Agents preview) or the live environment, depending on where the agent will operate
​
--url
string
You can choose to set credentials for either the draft environment (used in the Manage Agents preview) or the live environment, depending on where the agent will operate
​
--client-id
string
The OAuth connection’s client ID. This value uniquely identifies the application (watsonx Orchestrate) to the OAuth provider.
​
--client-secret
string
The clientSecret of the Oauth connection. This is used to authentication the application (watsonx Orchestate) to the oauth provider.
​
--token-url
string
The URL where watsonx Orchestrate exchanges the user authorization, client ID, and client secret to obtain an access token.
​
--scope
string
A comma separated list of oauth scopes to request for the user to grant the generated token certain privileged accesses to the upstream service provider.
​
--token-entries / -t
string
Define custom field options for an OAuth request.
Use key-value pairs in the format location:&lt;key&gt;=&lt;value&gt; or &lt;key&gt;=&lt;value&gt;.
You can pass multiple values like this: -t key1=value1 -t location:key2=value2.
Valid locations are: header, body, and query. If you omit the location, it defaults to header.
BASH
orchestrate connections set-credentials --app-id workday \
  --env draft \
  --client-id clientid \
  --token-url https://token-server/ccx/oauth2/ibmsrv_dpt1/token \
  --grant-type urn:ietf:params:oauth:grant-type:saml2-bearer
Hide command flags

​
--env
string
You can choose to set credentials for either the draft environment (used in the Manage Agents preview) or the live environment, depending on where the agent will operate
​
--client-id
string
The OAuth connection’s client ID. This value uniquely identifies the application (watsonx Orchestrate) to the OAuth provider.
​
--token-url
string
The URL where watsonx Orchestrate exchanges the user authorization, client ID, and client secret to obtain an access token.
​
--grant-type
string
The grant type of the identity provider’s auth service.
​
--token-entries / -t
string
Define custom field options for an OAuth request.
Use key-value pairs in the format location:&lt;key&gt;=&lt;value&gt; or &lt;key&gt;=&lt;value&gt;.
You can pass multiple values like this: -t key1=value1 -t location:key2=value2.
Valid locations are: header, body, and query. If you omit the location, it defaults to header.

---
associating connections
