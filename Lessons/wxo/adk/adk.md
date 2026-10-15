Get Started
Welcome to IBM watsonx Orchestrate Agent Development Kit
The IBM watsonx Orchestrate Agent Development Kit (ADK) is a set of tools designed to make it easy to build and deploy agents using IBM watsonx Orchestrate. It is packaged as a Python library and command line tool that allows builders to configure agents that run on the IBM watsonx Orchestrate platform. The ADK also supports integrating agents and tools built on other frameworks.
Installing the ADK
Install the ADK with pip and then install watsonx Orchestrate Developer Edition with the ADK.
Environments
Activate and manage the environment to import your agents and tools.
Agents
Build and manage agents in your active environment.
Tools and Connections
Build and manage tools for your agents and manage connections for your tools.
Knowledge Bases
Build and manage knowledge bases in your active environment.
Managing
Monitor your LLM and manage the channels for your environment.


----

Get Started
What is watsonx Orchestrate ADK
The Agent Development Kit (ADK) is a comprehensive set of CLI utilities and Python modules that enables you to create, test, and deploy agents and tools for watsonx Orchestrate. You can use these agents and tools across all watsonx Orchestrate offerings, including:
watsonx Orchestrate AWS
watsonx Orchestrate AWS Gov
watsonx Orchestrate IBM Cloud
watsonx Orchestrate on-premises
watsonx Orchestrate Developer Edition
​
ADK components
The ADK includes a powerful CLI that streamlines the process of building, testing, and importing agents and tools into watsonx Orchestrate.
​
Core building blocks
Component	Description	Key Features
Agent	An AI agent that uses tools and other agents to plan and execute tasks, reflecting on results and refining outputs to align with defined objectives.	- Collaborates with other agents to solve complex tasks
- Handles task decomposition and synthesis
- Uses tools autonomously on behalf of users
Tool	A function that can be invoked to perform specific actions or retrieve information.	- Well-defined inputs and outputs
- Permission-based access control
- Support for multiple binding types (Python, OpenAPI, MCP, Skill, etc.)
- Schema validation
- Reusable across agents
The ADK provides a comprehensive framework that enables developers to define new tools and agents programmatically with ease.
​
How it all works together
Define Tools: Create tools using one of the available binding types (Python, OpenAPI, MCP, Skill, etc.) and import them into watsonx Orchestrate using the ADK CLI.
Build Agents: Define agents using the ADK framework and import them into watsonx Orchestrate using the ADK CLI. Agents leverage the tools created in step 1.
Deploy and Use: Once imported, agents can interact with users through the watsonx Orchestrate Agent Chat UI or via the Orchestrate API.

---

Get Started
Getting started with the ADK
The Agent Development Kit (ADK) gives you a set of developer-focused tools to build, test, and manage agents in watsonx Orchestrate. With the ADK, you take full control of agent design using a lightweight framework and a simple CLI.
Define agents in clear YAML or JSON files, create custom Python tools, and manage the entire agent lifecycle with just a few commands.
This guide walks you through installing the ADK, setting up your local development environment, and deploying your first agent to a watsonx Orchestrate SaaS instance. Start building flexible, reusable AI agents right away.
​
Before you begin
​
Required software
Make sure you have Python 3.11 or later installed on your system. To check your current Python version, open a terminal and run:
python --version
If you have an older version of Python, you have a few options to install a newer Python version:
Windows

To install a newer version of Python on Windows, download the installer from the official Python website and run the setup. During installation, enable the option to Add PYTHONPATH to the environment variables. This step ensures you can use the latest Python version directly from your terminal.
The installer also includes the pip package manager, so you don’t need to install it separately.
As an alternative, use a Python version manager like uv or pyenv to install and manage multiple Python versions on your system.
Linux

Most Linux distributions include Python by default. If your version is older than 3.11, check your distribution’s package repositories for newer versions:

Ubuntu

Fedora

Arch Linux
sudo apt-get update -y
sudo apt-get install -y python3 python3-pip
If your distribution does not include newer packages, you can use pyenv or uv to install a newer version of Python:
uv

pyenv

macOS

Python usually comes pre-installed on macOS. If your version is older than 3.11, install a newer version using Homebrew.
To install Homebrew, run the following command:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
And then install Python by running:
brew install python@3.11
This installation also comes with the pip package manager, so you don’t have to install it yourself.
Alternatively, you can use a Python version manager such as uv or pyenv to install different Python versions in your system.
​
watsonx Orchestrate account
To use the ADK, you must connect it to an existing watsonx Orchestrate environment. If you don’t have a watsonx Orchestrate account, you can sign up for a free 30-day trial.
If you already have a watsonx Orchestrate account, you can use your existing account to provide an environment to use with the ADK.
​
Setting up and installing the ADK
1
Installing the ADK

Use the following command to install the ADK with pip:
BASH
pip install --upgrade ibm-watsonx-orchestrate
You can optionally use a virtual environment (venv) or a version manager like uv to control the packages you install. This setup makes it easier to share and distribute your agents and tools with others.
To learn how to install the ADK in these situations, see the following steps:
System installation
Virtual environments
uv
Install the ADK on your system with the following command:
pip install  --upgrade ibm-watsonx-orchestrate
2
Configure your environment in the ADK

Configure your watsonx Orchestrate environment in the ADK. Use this environment to create your agents.
In this step, you need access to specific credentials for your environment. If you don’t know the type of environment you have, see Logging in to IBM watsonx Orchestrate.
IBM Cloud

To connect to IBM Cloud, you need both the service instance URL and an API key of your watsonx Orchestrate instance.
Don’t use the credentials that you get from the IBM Cloud resources page. Use the following procedure to get the appropriate API key and service instance URL.
1
Log in to your watsonx Orchestrate instance.
2
Click your user icon on the top right and click Settings.

3
Go to the API details tab.
4
Copy the service instance URL.
5
Click the Generate API key button.

6
Generate an API Key

The page redirects you to the IBM Cloud Identity Access Management center. Click Create to create a new API Key.

7
Enter a name and a description for your API Key.

8
Copy the API key and store it in a safe vault.

9
Add and activate your environment with the ADK CLI:
BASH
orchestrate env add -n <environment-name> -u <service-instance-url> --type ibm_iam --activate
Note:
You can set any name you prefer for the environment.
For more information, see Configuring your environments.
AWS

To connect to an instance hosted on AWS, follow these steps:
1
Log in to your watsonx Orchestrate instance.
2
Click your user icon on the top right and click Settings.

3
Go to the API details tab.
4
Copy the service instance URL.
5
Click the Generate API key button and copy the key.

API keys are not retrievable and can’t be edited or deleted. Make sure to store your API keys in a safe location after you generate a new API key.
You are limited to 10 API keys in this environment. If you have no more available keys, contact IBM Support for further assistance.
6
Add and activate your environment with the ADK CLI:
BASH
orchestrate env add -n <environment-name> -u <service-instance-url> --type mcsp --activate
Note:
You can set any name you prefer for the environment.
For more information, see Configuring your environments.
On-premises

For on-premises environments, you can authenticate using one of two methods:
API Key
Use the API key that authenticates your user in the on-premises watsonx Orchestrate environment.
Username and Password
Use your username and password credentials to authenticate in the on-premises watsonx Orchestrate environment.
Note: You can only use one authentication method at a time. If you try to authenticate using both methods simultaneously, an authentication error occurs.
To add your environment, run the following.
BASH
    orchestrate env add -n <environment-name> -u <service-instance-url>
Note:
You can set any name you prefer for the environment.
In the rare case when the watsonx Orchestrate ADK does not automatically infer the correct authentication type for your url please add the following to the orchestrate env add command:
IBM Cloud: --type ibm_iam
AWS: --type mcsp
On-premises: --type cpd
3
Activate your environment

Run the following command to activate the environment you created:
orchestrate env activate <environment-name>
Environments on AWS GovCloud

For FedRAMP-compliant environments on AWS GovCloud, use the following script to activate your environment:
fedramp_activate
#!/usr/bin/env python3
from typing import Annotated
import typer
import requests

from ibm_watsonx_orchestrate.cli.commands.tools.types import RegistryType
from ibm_watsonx_orchestrate.cli.config import Config, AUTH_CONFIG_FILE_FOLDER, AUTH_CONFIG_FILE, \
    AUTH_CONFIG_FILE_CONTENT, ENV_WXO_URL_OPT, AUTH_SECTION_HEADER, AUTH_MCSP_TOKEN_OPT, PYTHON_REGISTRY_HEADER, \
    PYTHON_REGISTRY_TYPE_OPT, PYTHON_REGISTRY_TEST_PACKAGE_VERSION_OVERRIDE_OPT, PYTHON_REGISTRY_SKIP_VERSION_CHECK_OPT, \
    CONTEXT_SECTION_HEADER, CONTEXT_ACTIVE_ENV_OPT, ENVIRONMENTS_SECTION_HEADER, DEFAULT_CONFIG_FILE_CONTENT
from ibm_watsonx_orchestrate.client.utils import check_token_validity, is_local_dev

app = typer.Typer(
    no_args_is_help=True,
    pretty_exceptions_enable=False
)

@app.command(name='activate', no_args_is_help=True)
def activate(
        name: Annotated[
            str,
            typer.Argument(),
        ],
        apikey: Annotated[
            str,
            typer.Option(
                "--api-key", "-a", help="WXO API Key."
            ),
        ],
        iam_url: Annotated[
            str,
            typer.Option(
                "--iam-url", help="IAM API URL for token generation. Defaults to dai.ibmforusgov.com"
            ),
        ] = "dai.ibmforusgov.com",
        registry: Annotated[
            RegistryType,
            typer.Option("--registry", help="Which registry to use when importing python tools", hidden=True),
        ] = None,
        test_package_version_override: Annotated[
            str,
            typer.Option("--test-package-version-override", help="Which prereleased package version to reference when using --registry testpypi", hidden=True),
        ] = None,
        skip_version_check: Annotated[
            bool,
            typer.Option('--skip-version-check/--enable-version-check', help='Use this flag to skip validating that adk version in use exists in pypi (for clients who mirror the ADK to a local registry and do not have local access to pypi).')
        ] = None
):
    cfg = Config()
    auth_cfg = Config(AUTH_CONFIG_FILE_FOLDER, AUTH_CONFIG_FILE)
    env_cfg = cfg.read(ENVIRONMENTS_SECTION_HEADER, name)
    url = cfg.get(ENVIRONMENTS_SECTION_HEADER, name, ENV_WXO_URL_OPT)
    is_local = is_local_dev(url)

    if not env_cfg:
        print(f"Environment '{name}' does not exist. Please create it with `orchestrate env add`")
        return
    elif not env_cfg.get(ENV_WXO_URL_OPT):
        print(f"Environment '{name}' is misconfigured. Please re-create it with `orchestrate env add`")
        return

    existing_auth_config = auth_cfg.get(AUTH_SECTION_HEADER).get(name, {})
    existing_token = existing_auth_config.get(AUTH_MCSP_TOKEN_OPT) if existing_auth_config else None

    if not check_token_validity(existing_token) or is_local:
        try:
            resp = requests.post(
                f"https://{iam_url}/api/rest/mcsp/apikeys/token",
                json={'apikey': apikey}
            )
            resp.raise_for_status()
            resp = resp.json()
            auth_cfg.save(
                {
                    AUTH_SECTION_HEADER: {
                        name: {
                            'wxo_mcsp_token': resp['token'],
                            'wxo_mcsp_token_expiry': resp['expiration']
                        }
                    },
                }
            )
        except requests.exceptions.HTTPError as e:
            print(e.response)
            exit(1)


    cfg.write(CONTEXT_SECTION_HEADER, CONTEXT_ACTIVE_ENV_OPT, name)
    if registry is not None:
        cfg.write(PYTHON_REGISTRY_HEADER, PYTHON_REGISTRY_TYPE_OPT, str(registry))
        cfg.write(PYTHON_REGISTRY_HEADER, PYTHON_REGISTRY_TEST_PACKAGE_VERSION_OVERRIDE_OPT, test_package_version_override)
    elif cfg.read(PYTHON_REGISTRY_HEADER, PYTHON_REGISTRY_TYPE_OPT) is None:
        cfg.write(PYTHON_REGISTRY_HEADER, PYTHON_REGISTRY_TYPE_OPT, DEFAULT_CONFIG_FILE_CONTENT[PYTHON_REGISTRY_HEADER][PYTHON_REGISTRY_TYPE_OPT])
        cfg.write(PYTHON_REGISTRY_HEADER, PYTHON_REGISTRY_TEST_PACKAGE_VERSION_OVERRIDE_OPT, test_package_version_override)
    if skip_version_check is not None:
        cfg.write(PYTHON_REGISTRY_HEADER, PYTHON_REGISTRY_SKIP_VERSION_CHECK_OPT, skip_version_check)

    print(f"Environment '{name}' is now active")

if __name__ == "__main__":
    app()
See all 101 lines
And run it as follows:
BASH
./fedramp_activate fedramp --api-key <your_api_key>
If you need to change your environment, see Configuring your environments.
Note: You can also activate a local development environment. This environment is provided by the watsonx Orchestrate Developer Edition, a stripped-down version of watsonx Orchestrate that runs under a Docker container to be used as a development server. To learn more about it, see watsonx Orchestrate Developer Edition.
​
Creating your first agent
With your ADK connected to your watsonx Orchestrate instance, you’re ready to test your setup by publishing a simple agent.
In watsonx Orchestrate, you define agents using YAML or JSON files. The agent specification file includes key details like the agent’s name, kind, instructions for the LLM, and the tools it can use.
When you build agents with the ADK, you write this specification yourself. This approach gives you full control over your agent’s behavior and capabilities. You can create advanced agents with custom tools, collaborators, or integrations. For now, start with a minimal Hello World agent to verify your setup.
For internal GovCloud environments (staging, pre-prod), specify the IAM URL: ./fedramp_activate fedramp --api-key <your_api_key> --iam-url dai.prep.ibmforusgov.com
1
Starting your ADK project

As a Python project, it’s a good practice to create a folder that stores your agents, tools, and other resources.
Example of folder structure:
.
└── adk-project/
    ├── agents/
    ├── tools/
    ├── knowledge/
    ├── flows/
    └── ...

macOS & Linux

Windows
mkdir -p adk-project/{agents,tools,knowledge,flows}
2
Creating the agent specification

Start by creating the YAML file for the agent and name the file as hello-world-agent.yaml. Open the created file with the text editor of your choice, then copy and paste the following code.
hello-world-agent.yaml
spec_version: v1 
kind: native 
name: Hello_World_Agent 
description: A simple Hello World agent 
instructions: "You are a test agent created for a tutorial on how to get started with watsonx Orchestrate ADK. When the user asks 'who are you', respond with: I'm the Hello World Agent. Congratulations on completing the Getting Started with watsonx Orchestrate ADK tutorial!"
llm: groq/openai/gpt-oss-120b
style: react_core 
collaborators: [] 
tools: [] 
See all 9 lines
And save the file in the agents folder.
3
Import the agent

Open your terminal and navigate to the folder where you created the YAML file. Then run the following command to publish your agent:
orchestrate agents import -f hello-world-agent.yaml 
If the import is successful, you get the following confirmation message:
[INFO] - Agent 'Hello World Agent' imported successfully
4
Open the Agent Builder

Log in to your watsonx Orchestrate instance and open the Agent Builder:
Open the Agent Builder
5
Select the Hello World agent

In the Build agents and tools page, select the Hello_World_Agent.
Select the agent
6
Test your agent

In this page, you can customize your agent’s behavior. Use the test chat to test your agent.
Test your chat
​
What’s next?
You have now created your first agent with the ADK and successfully imported it into your watsonx Orchestrate instance.
To extend your agent’s behavior, you can use tools, knowledge bases and agentic workflows. To connect to services, you must create Connections to safely store credentials and sensitive data. You can also change the agent’s large language model and style by changing the agent specification, and you can test and evaluate the agent with the Evaluation Framework.
See the following cards to learn more about what you can do with the ADK:
Agents
Learn more about what you can do with agents, how you can change your agent style and how to customize your agent’s large language model.
Environments
Learn how to change your watsonx Orchestrate environments to import your agents developed with the ADK.
Tools
Learn more about how to use tools to extend your agent’s capabilities and how to integrate with external services.
Connections
Learn more about how to safely store credentials and connect to external services.
Knowledge Base
Learn how to use knowledge bases to provide more accurate responses and improve your agent’s knowledge in specific situations.
Evaluation Framework
Assess your agent’s behavior by comparing simulated agent interactions with a predefined set of reference data.
