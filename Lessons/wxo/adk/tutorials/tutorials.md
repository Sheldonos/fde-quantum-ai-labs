Tutorials
Tutorial: Creating your first agent with the Agent builder
In this tutorial, you’ll follow a step-by-step guide to create your first agent with the Agent builder.
​
Before you begin
Before you start to follow this tutorial, you must set up your IBM watsonx Orchestrate ADK environment, where you build agents and tools. It also provides a convenient interface for managing credentials, sending requests, and handling responses from the service’s APIs. See the Installing the watsonx Orchestrate ADK and Installing the watsonx Orchestrate Developer Edition.
​
Developing the ‘Hello world’ agent
The following steps guide you to make you agent available on Agent builder.
In your directory, create a folder with the name hello-world.
Open a text editor, such as Visual Studio Code.
To create the agent, copy the following code:
YAML
spec_version: v1
kind: native
name: greeter
description: An agent that greets you using the output from its tool
instructions: Always run the tool "Greeting" when the user types Greeting in the chat. 
llm: groq/openai/gpt-oss-120b
style: react_core
collaborators: []
tools: 
- greeting
See all 10 lines
Paste the code in the text editor and save the file as greeter.yaml in the *hello-world folder.
To create the tool, copy the following code:
Python
#greetings.py
from ibm_watsonx_orchestrate.agent_builder.tools import tool


@tool
def greeting() -> str:
    """
    Greeting for everyone   
    """

    greeting = "Hello World"
    return greeting
See all 12 lines
Paste the code in the text editor and save the file as greetings.py in the *hello-world folder.
Open the terminal that you commonly use.
Navigate to the folder. For instance, cd ~/Desktop/hello-world.
Run the command orchestrate tools import -k python -f tools/greetings.py.
Run the command orchestrate agents import -f greeter.yaml.
Run the command orchestrate chat start.
​
Testing your agent
After the configuration, you can enter “Greeting” into the chat window and continue interacting with your agent.

---


Tutorials
Tutorial: Creating the Empower agent on Agent builder
The following step-by-step guides you through setting the IBM watsonx Orchestrate Agent builder, creating an agent, adding tools, and other agent to collaborate with your agent on accomplishing tasks.
​
Before your begin
Before you start to follow this tutorial, you must set up your IBM watsonx Orchestrate ADK environment, where you build agents and tools. It also provides a convenient interface for managing credentials, sending requests, and handling responses from the service’s APIs. See the Installing the watsonx Orchestrate ADK and Installing the watsonx Orchestrate Developer Edition.
​
Empower: An agent for employee success
This tutorial is based on a scenario called Empower: An agent for employee success. The goal is to create an agent with a key role in assisting employees by answering their questions, providing guidance on supporting tickets, service issues, and referencing FAQs stored in Sharepoint. The following sections walk you through the complete agent building process, from defining the name and description until the deployment process and the agent’s usage on watsonx Orchestrate chat.
​
ServiceNow and Customer care examples
After setting up the ADK and starting your local orchestrate server, you need to import the ServiceNow and Customer care examples, both agent and tools, once they are used to create the Empower agent. The following sections make available the files that are needed to build the ServiceNow and Customer care examples, and how to install them.
​
Customer care and ServiceNow agents
The following section guides you to create the Customer care and ServiceNow agents.
Create a folder to structure your agents and tools. For instance, name this folder as agents.
In the new folder, create a YAML file with a text editor of your preference. Name the file as customer_care_agent.
Insert the following code into the customer_care_agent.yaml file.
YAML
spec_version: v1
style: react_core
name: customer_care_agent
llm: groq/openai/gpt-oss-120b
description: |
    You are an agent who specializes in customer care for a large healthcare institution. You should be compassionate
    to the user.
    
    You are able to answer questions around benefits provided by different plans, the status of a claim,
    and are able to help direct people to the nearest provider for a particular ailment.
instructions: |
    Use the search_healthcare_providers tool to search for providers. If more than 1 is returned format as a github
    formatted markdown table. Otherwise simply return the output in a kind conversational tone. Do not expand speciality acronyms.
    
    Use the get_healthcare_benefits tool to fetch the benefits coverage for a particular ailment, or for generic plan 
    comparisons. Respond to get_healthcare_benefits requests in a github style formatted markdown table. Be specific about
    the expected coverage type if a particular condition is mentioned.
    
    Use the get_my_claims tool to fetch your open medical claims. Make sure to respond in a direct tone and 
    do not negotiate prices. Format the output of get_my_claims as a github style markdown table.
collaborators:
    - service_now_agent
tools:
    - search_healthcare_providers
    - get_healthcare_benefits
    - get_my_claims
See all 26 lines
Save your file.
Create another YAML file, but name it as service_now_agent.
Insert the following code into the service_now_agent.yaml file.
YAML
spec_version: v1
style: react_core
name: service_now_agent
llm: groq/openai/gpt-oss-120b
description: |
    You are an agent who specializes in customer care for a large healthcare institution. You should be compassionate
    to the user.
    
    You are able to help help a user create tickets in service now for processing by a human later. Examples of when to do
    do this include for adding members to plans or helping users with documentation.
instructions: |
    If a user is having difficulty either generating benefits documents or adding additional members to their plan,
    create a new incident for our support team using service_now_create_incident tool. Be compassionate about the user
    facing difficulty.
    
    The output of get_service_now_incidents should be formatted as a github style formatted markdown table.
collaborators: []
tools:
    - create_service_now_incident
    - get_my_service_now_incidents
    - get_service_now_incident_by_number
See all 21 lines
Save your file.
Up until here, you created the agents that are needed for Customer care and ServiceNow examples.
​
Creating the Customer care tools
The following section guides you to create the tools for Customer care example.
Create a new folder to insert the tools of your examples. For instance, name this folder as tools.
In the new folder, create another one to insert the customer care tools. Name this folder as customer_care.
In the customer_care folder, create a Python file with a text editor of your preference. Name the file as get_healthcare_benefits.
Insert the following code into the get_healthcare_benefits.py file.
Python
from enum import Enum

from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
import requests

class Plan(str, Enum):
    HDHP = 'HDHP'
    HDHP_Plus = 'HDHP Plus'
    PPO = 'PPO'


@tool
def get_healthcare_benefits(plan: Plan, in_network: bool = None):
    """Retrieves a comprehensive list of health benefits data, organized by coverage type and plan variant.

    This data includes details such as annual deductibles, out-of-pocket maximums, and various co-pays or
    percentages for medical services under different network plans (HDHP, HDHP Plus, and PPO).

    Args:
        plan (str, optional): The plan the user is currently on. Can be one of "HDHP", "HDHP Plus", or "PPO".
            If not provided, all plans will be returned.
        in_network (bool, optional): Whether the user wants coverage for in-network or out-of-network.
            If not provided, both will be returned.

    Returns:
        list[dict]: A list of dictionaries, where each dictionary contains:
            - 'Coverage': A description of the coverage type (e.g., 'Preventive Services').
            - 'HDHP (In-Network)': The cost/percentage coverage for an in-network HDHP plan.
            - 'HDHP (Out-of-Network)': The cost/percentage coverage for an out-of-network HDHP plan.
            - 'HDHP Plus (In-Network)': The cost/percentage coverage for an in-network HDHP Plus plan.
            - 'HDHP Plus (Out-of-Network)': The cost/percentage coverage for an out-of-network HDHP Plus plan.
            - 'PPO (In-Network)': The cost/percentage coverage for an in-network PPO plan.
            - 'PPO (Out-of-Network)': The cost/percentage coverage for an out-of-network PPO plan.
    """
    resp = requests.get(
        'https://get-benefits-data.1sqnxi8zv3dh.us-east.codeengine.appdomain.cloud/',
        params={
            'plan': plan,
            'in_network': in_network
        }
    )
    resp.raise_for_status()
    return resp.json()['benefits']
See all 43 lines
Save your file.
In the same folder, create another Python file and name it as get_my_claims.
Insert the following code into the get_my_claims.py file.
Python
from ibm_watsonx_orchestrate.agent_builder.tools import tool


@tool
def get_my_claims() -> list[dict]:
    """Retrieves detailed information about submitted claims.

    The details include claim status, submission and processing dates, amounts claimed and approved,
    provider information, and services included in the claims.

    Returns:
        list[dict]: A list of dictionaries, each containing details about a specific claim:
            - claimId (str): Unique identifier for the claim.
            - submittedDate (str): Date when the claim was submitted.
            - claimStatus (str): Current status of the claim (e.g., 'Processed', 'Pending', 'Rejected').
            - processedDate (str or None): Date when the claim was processed (None if not processed yet).
            - amountClaimed (float): Total amount claimed.
            - amountApproved (float or None): Amount approved for reimbursement (None if pending, 0 if rejected).
            - rejectionReason (str, optional): Reason for rejection if applicable (only present if claimStatus is 'Rejected').
            - provider (str or dict): Provider details, either as a simple string or a dictionary with detailed provider information.
            - services (list[dict]): List of services included in the claim, each with:
                - serviceId (str): Identifier for the service.
                - description (str): Description of the service provided.
                - dateOfService (str): Date the service was provided.
                - amount (float): Amount charged for the service.
    """

    claims_data = [
        {
            "claimId": "CLM1234567",
            "claimStatus": "Processed",
            "amountClaimed": 150.00,
            "amountApproved": 120.00,
            "provider": {
                "name": "Healthcare Clinic ABC",
                "providerId": "PRV001234",
                "providerType": "Clinic"
            },
            "services": [
                {"serviceId": "SVC001", "description": "General Consultation", "dateOfService": "2025-02-28", "amount": 100.00},
                {"serviceId": "SVC002", "description": "Blood Test", "dateOfService": "2025-02-28", "amount": 50.00}
            ]
        },
        {
            "claimId": "CLM7654321",
            "claimStatus": "Pending",
            "amountClaimed": 300.00,
            "amountApproved": None,
            "provider": "City Health Hospital",
            "services": [
                {"serviceId": "SVC003", "description": "X-ray Imaging", "dateOfService": "2025-02-14", "amount": 300.00}
            ]
        },
        {
            "claimId": "CLM9876543",
            "claimStatus": "Rejected",
            "amountClaimed": 200.00,
            "amountApproved": 0.00,
            "rejectionReason": "Service not covered by policy",
            "provider": "Downtown Diagnostics",
            "services": [
                {"serviceId": "SVC003", "description": "MRI Scan", "dateOfService": "2025-02-05", "amount": 200.00}
            ]
        }
    ]

    return claims_data
See all 67 lines
Save your file.
In the same folder, create another Python file and name it as search_healthcare_providers.
Insert the following code into the search_healthcare_providers.py file.
Python
from typing import List

import requests
from pydantic import BaseModel, Field
from enum import Enum

from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission


class ContactInformation(BaseModel):
    phone: str
    email: str


class HealthcareSpeciality(str, Enum):
    GENERAL_MEDICINE = 'General Medicine'
    CARDIOLOGY = 'Cardiology'
    PEDIATRICS = 'Pediatrics'
    ORTHOPEDICS = 'Orthopedics'
    ENT = 'Ear, Nose and Throat'
    MULTI_SPECIALTY = 'Multi-specialty'


class HealthcareProvider(BaseModel):
    provider_id: str = Field(None, description="The unique identifier of the provider")
    name: str = Field(None, description="The providers name")
    provider_type: str = Field(None, description="Type of provider, (e.g. Hospital, Clinic, Individual Practitioner)")
    specialty: HealthcareSpeciality = Field(None, description="Medical speciality, if applicable")
    address: str = Field(None, description="The address of the provider")
    contact: ContactInformation = Field(None, description="The contact information of the provider")


@tool
def search_healthcare_providers(
        location: str,
        specialty: HealthcareSpeciality = HealthcareSpeciality.GENERAL_MEDICINE
) -> List[HealthcareProvider]:
    """Retrieves a list of the nearest healthcare providers based on location and optional specialty.

    The function can infer the specialty of the location from the request.

    Args:
        location (str): Geographic location to search providers in (city, state, zip code, etc.).
        specialty (str, optional): Medical specialty to filter providers by. Must be one of:
            "ENT", "General Medicine", "Cardiology", "Pediatrics", "Orthopedics", "Multi-specialty".

    Returns:
        list: A list of healthcare providers near the specified location for the given specialty.
    """
    resp = requests.get(
        'https://find-provider.1sqnxi8zv3dh.us-east.codeengine.appdomain.cloud',
        params={
            'location': location,
            'speciality': specialty
        }
    )
    resp.raise_for_status()
    return resp.json()['providers']
See all 58 lines
Up until here, you created the tools for the customer care example.
​
Creating the ServiceNow tools
The following section guides you to create the tools for ServiceNow example.
In the tools folder, create a new folder named as servicenow.
In the servicenow folder, create a Python file and name it as create_service_now_incident.
Insert the following code into the create_service_now_incident.py file.
Python
import base64
import json
from typing import Optional

import requests
from requests.auth import HTTPBasicAuth

from pydantic import Field, BaseModel

from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from ibm_watsonx_orchestrate.run import connections

from ibm_watsonx_orchestrate.agent_builder.connections import ConnectionType

CONNECTION_SNOW = 'service-now'

class ServiceNowIncidentResponse(BaseModel):
    """
    Represents the response received after creating a ServiceNow incident.
    """
    incident_number: str = Field(..., description='The incident number assigned by ServiceNow')
    sys_id: str = Field(..., description='The system ID of the created incident')


class ServiceNowIncident(BaseModel):
    """
    Represents the details of a ServiceNow incident.
    """
    incident_number: str = Field(..., description='The incident number assigned by ServiceNow')
    short_description: str = Field(..., description='A brief summary of the incident')
    description: Optional[str] = Field(None, description='Detailed information about the incident')
    state: str = Field(..., description='Current state of the incident')
    urgency: str = Field(..., description='Urgency level of the incident')
    created_on: str = Field(..., description='The date and time the incident was created')


@tool(
    permission=ToolPermission.READ_WRITE,
    expected_credentials=[
        {"app_id": CONNECTION_SNOW, "type": ConnectionType.BASIC_AUTH}
    ]
)
def create_service_now_incident(
        short_description: str,
        description: str = None,
        urgency: int = 3
):
    """Creates a new ServiceNow incident.

    Args:
        short_description (str): A brief summary of the incident.
        description (str, optional): Detailed information about the incident.
        urgency (int, optional): Urgency level. Must be 1 (High), 2 (Medium), or 3 (Low). Defaults to 3.

    Returns:
        dict: The created incident details, including the incident number and system ID.
    """

    creds = connections.basic_auth(CONNECTION_SNOW)
    base_url = creds.url
    url = f"{base_url}/api/now/table/incident"

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    payload = {
        'short_description': short_description,
        'description': description,
        'urgency': urgency
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        auth=HTTPBasicAuth(creds.username, creds.password)
    )
    response.raise_for_status()
    data = response.json()['result']

    number, sys_id = data['number'], data['sys_id']

    url = f"{base_url}/api/now/table/incident/{sys_id}"
    response = requests.get(
        url,
        headers=headers,
        json=payload,
        auth=HTTPBasicAuth(creds.username, creds.password)
    )
    response.raise_for_status()
    data = response.json()['result']

    return ServiceNowIncident(
        incident_number=data['number'],
        sys_id=data['sys_id'],
        short_description=data['short_description'],
        description=data.get('description', ''),
        state=data['state'],
        urgency=data['urgency'],
        created_on=data['opened_at']
    ).model_dump_json()

# if __name__ == '__main__':
#     incident = create_service_now_incident(short_description='Test Incident', description='This is a test incident')
#     print(json.dumps(incident.dict(), indent=2))

See all 107 lines
Save your file.
In the same folder, create another Python file and name it as get_my_service_now_incidents.
Insert the following code into the get_my_service_now_incidents.py file.
get_my_service_now_incidents.py
import json
from typing import Optional, List

import requests
from pydantic import Field, BaseModel
import base64

from requests.auth import HTTPBasicAuth

from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from ibm_watsonx_orchestrate.run import connections

from ibm_watsonx_orchestrate.agent_builder.connections import ConnectionType


CONNECTION_SNOW = 'service-now'

class ServiceNowIncident(BaseModel):
    """
    Represents the details of a ServiceNow incident.
    """
    incident_number: str = Field(..., description='The incident number assigned by ServiceNow')
    short_description: str = Field(..., description='A brief summary of the incident')
    description: Optional[str] = Field(None, description='Detailed information about the incident')
    state: str = Field(..., description='Current state of the incident')
    urgency: str = Field(..., description='Urgency level of the incident')
    created_on: str = Field(..., description='The date and time the incident was created')

@tool(
    expected_credentials=[
        {"app_id": CONNECTION_SNOW, "type": ConnectionType.BASIC_AUTH}
    ]
)
def get_my_service_now_incidents() -> List[ServiceNowIncident]:
    """
    Fetch all ServiceNow that the user was the author of.

    Returns:
        The incident details including number, system ID, description, state, and urgency.
    """
    creds = connections.basic_auth(CONNECTION_SNOW)
    base_url = creds.url
    url = f"{base_url}/api/now/table/incident"

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    query_params = {}
    query_params['sys_created_by'] = 'admin'
    
    response = requests.get(
        url,
        headers=headers,
        params=query_params,
        auth=HTTPBasicAuth(creds.username, creds.password)
    )
    response.raise_for_status()
    data = response.json()['result']
    
    lst =  [ServiceNowIncident(
        incident_number=d['number'],
        short_description=d['short_description'],
        description=d.get('description', ''),
        state=d['state'],
        urgency=d['urgency'],
        created_on=d['opened_at']
    ) for d in data]
    lst.sort(key=lambda o: o.created_on, reverse=True)
    lst = lst[:min(len(lst), 10)]
    return lst

# if __name__ == '__main__':
#     incidents = get_my_service_now_incidents()
#     print(incidents)
See all 76 lines
Save your file.
In the same folder, create another Python file and name as get_service_now_incident_by_number.
Insert the following code into the get_service_now_incident_by_number.py file.
Python
import json
from typing import Optional

import requests
from pydantic import Field, BaseModel
import base64

from requests.auth import HTTPBasicAuth

from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from ibm_watsonx_orchestrate.run import connections

from ibm_watsonx_orchestrate.agent_builder.connections import ConnectionType

CONNECTION_SNOW = 'service-now'

class ServiceNowIncident(BaseModel):
    """
    Represents the details of a ServiceNow incident.
    """
    incident_number: str = Field(..., description='The incident number assigned by ServiceNow')
    short_description: str = Field(..., description='A brief summary of the incident')
    description: Optional[str] = Field(None, description='Detailed information about the incident')
    state: str = Field(..., description='Current state of the incident')
    urgency: str = Field(..., description='Urgency level of the incident')
    created_on: str = Field(..., description='The date and time the incident was created')

@tool(
    expected_credentials=[
        {"app_id": CONNECTION_SNOW, "type": ConnectionType.BASIC_AUTH}
    ]
)
def get_service_now_incident_by_number(incident_number: str):
    """Fetches a ServiceNow incident based on incident ID, creation date, or other filters.

    Args:
        incident_number (str): The uniquely identifying incident number of the ticket.

    Returns:
        dict: The incident details, including number, system ID, description, state, and urgency.
    """
    creds = connections.basic_auth(CONNECTION_SNOW)
    base_url = creds.url
    url = f"{base_url}/api/now/table/incident"

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    query_params = {}
    if incident_number:
        query_params['number'] = incident_number
    
    response = requests.get(
        url,
        headers=headers,
        params=query_params,
        auth=HTTPBasicAuth(creds.username, creds.password)
    )
    response.raise_for_status()
    data = response.json()['result']
    data = data[0]  # Assuming only one incident is returned
    
    return ServiceNowIncident(
        incident_number=data['number'],
        short_description=data['short_description'],
        description=data.get('description', ''),
        state=data['state'],
        urgency=data['urgency'],
        created_on=data['opened_at']
    ).model_dump_json()

# if __name__ == '__main__':
#     incident = fetch_service_now_incident(incident_number='INC0010311')
#     print(json.dumps(incident.dict(), indent=2))
See all 76 lines
Up until here, you created the tools for the service now example. Before finishing, you must create the requirements file.
Into the servicenow folder, create a TXT file named as requirements.
Insert the following code into the requirements.txt file.
TEXT
requests==2.32.3
You finished to create the files that are needed to install the Customer care and ServiceNow examples.
​
Installing ServiceNow and Customer care
The following section guides you to install the ServiceNow and Customer care examples.
Start the watsonx Orchestrate Developer Edition local server orchestrate server start --env-file={{The path of your .env file}}.
Signup for a Sevice Now account at https://developer.servicenow.com/dev.do.
Validate your email address (check email).
On the landing page, click start building. This allocates a new instance of ServiceNow for you.
Back on the landing page, click your profile icon on the upper right. Under “My instance”, click manage instance password.
In the terminal, create an application connection by using these credentials:
BASH
orchestrate connections add -a service-now
BASH
orchestrate connections configure -a service-now --env draft --type team --kind basic --url <the instance url>
BASH
orchestrate connections set-credentials -a service-now --env draft -u admin -p '<password from modal>'
In the terminal, navigate to the customer_care folder and run the following commands to import the customer care tools:
BASH
orchestrate tools import -k python -f ./get_my_claims.py
BASH
orchestrate tools import -k python -f ./get_healthcare_benefits.py
BASH
orchestrate tools import -k python -f ./search_healthcare_providers.py
Go to the servicenow folder and install the tools by running the following commands:
BASH
orchestrate tools import -k python -f ./create_service_now_incident.py -r ./requirements.txt -a service-now
BASH
orchestrate tools import -k python -f ./get_my_service_now_incidents.py -r ./requirements.txt -a service-now
BASH
orchestrate tools import -k python -f ./get_service_now_incident_by_number.py -r ./requirements.txt -a service-now
Go to your agents folder and import the agents created previously:
BASH
orchestrate agents import -f service_now_agent.yaml
BASH
orchestrate agents import -f customer_care_agent.yaml
Run orchestrate chat start.
When you run the chat, you must be able to see a list of agents in your local chat interface.
​
Agent’s profile
This section shows how to define the name and description of your agent. This step gives your agent a clear purpose and helps guide how it interacts with users.
From the IBM watsonx Orchestrate chat page, click Manage agents.
Click Create agent.
Choose Create from Scratch.
In the Name field, insert Empower and in the Description, insert a text as you prefer to describe the agent. Suggestion: “This agent’s role is to assist employees by answering their questions, providing guidance on supporting tickets, service issues, and referencing FAQs stored in Sharepoint”.
Click Create to complete.
You finished working on the profile.
​
Agent’s toolset
This section guides you through how to equip your agent with tools, and how to add other agents to collaborate in accomplishing tasks.
From the Empower agent management screen, click Toolset.
In Tools, click Add tool, and select Add from local instance.
Select the get_healthcare_benefits tool, and click Add to agent.
In Agents, add the agent that collaborates with your agent on running tasks. Click Add agent.
Click Add from local instance, select service_now_agent, and click Add to agent.
You finished working on the toolset.
​
Chat preview
This section shows how you can see your agent in action before deploying, allowing you to quickly validate that everything works as expected.
From the Empower agent management screen, type in the chat bar “Show my benefits related to mental health”, and press Enter.
Wait for the chat response. You can check how your response was generated by clicking How did I get this response.
You finished previewing your chat.
​
Deploying Empower agent
This final section guides you to deploy your agent and make it available in the IBM watsonx Orchestrate chat.
Click Deploy.
Click IBM watsonx Orchestrate to return for the chat page.
In the Agents list, select the Empower agent, and start by using it directly from the watsonx Orchestrate chat page.
You can ask about service now issues, as your agent has the Service now agent collaborating on running tasks.
You completed the process of creating and deploying your Empower agent.


---

Tutorials
Tutorial: Multi-language support
AI Agents can already support multi-language communication with users, as they are based on large language models (LLMs), and these models are usually trained in multiple languages. However, depending on the task you want to run with your agent, you might need to add further instructions to the agent so that it can better support multi-language communication.
​
Before your begin
Before you start, you must comply with some requirements:
Follow the steps in the Empower agent tutorial to configure your agents.
Set up your IBM watsonx Orchestrate ADK environment, where you build agents and tools. It also provides a convenient interface for managing credentials, sending requests, and handling responses from the service’s APIs. See the Installing the watsonx Orchestrate ADK and Installing the watsonx Orchestrate Developer Edition.
​
Configuring multi-language support
Follow the steps to configure the multi-language support in your agent.
Open the service_now_agent.yaml file with a text editor, such as Visual Studio Code.
In the instructions section, add the two following lines:
YAML
Make sure to communicate with the user by matching the language it uses to communicate with you and adapting names and terms as appropriate, and also translate column names and anything else when returning the information to the user.

Pay attention to the correct language adaptation of inputs and outputs, always returning the information to the user in the same language they are using to communicate with you.
Save the YAML file.
Open the customer_care_agent.yaml file and apply the previous steps. It is necessary as the Customer Care agent is the supervisor of the ServiceNow agent.
By adding these two lines of instructions to your agents, you can ensure that the agent expects to be engaged in multiple languages and can adapt more accurately. You can even use these same instructions, or something similar to them, with any agent you build to help ensure that your agent can adapt to being engaged in multiple languages.
​
Importing your agents
Now that you finished editing instructions of the two agents, you must reimport them to update these agents in the IBM watsonx Orchestrate ADK. You can follow the steps that are described in the Empower agent tutorial, but that procedure also reimports the tools, which can take a long time. To import only the agents directly, you can follow the steps:
Open the terminal that you commonly use.
Navigate to the folder where your agents are saved.
Write the command orchestrate agents import -f agent_file_name.yaml.
Replace agent_file_name expression with your agent file name. For this tutorial, you can run the following commands:
BASH
orchestrate agents import -f customer_care_agent.yaml
BASH
orchestrate agents import -f service_now_agent.yaml
You can see in the terminal a message that confirms the agents were successfully imported.
Note: If you do not navigate to the agent files folder, you must run the command with the folder path, for example:
BASH
orchestrate agents import -f home/documents/agents/agentFile.yaml
​
Testing your agent
Now, you can test your multilanguage agents in the chat by using other languages.
​
Troubleshooting
If you have problems with the agent’s response, you can try changing the LLM that the agent uses.
To do that, you must first check which models are available in your current environment:
BASH
orchestrate models list
And then you can edit the customer_care_agent.yaml and service_now_agent.yaml files to use the model you chose. For example:
model: groq/openai/gpt-oss-120b
If you want to add a custom model, see Adding a custom LLM.



---


Tutorials
Tutorial: Creating the Healthcare provider agent on Agent builder
The following step-by-step guides you to create Healthcare provider agent on IBM watsonx Orchestrate Agent builder.
​
Before you begin
Before you start following this tutorial, you must set up your IBM watsonx Orchestrate ADK environment, where you build agents and tools. It also provides a convenient interface for managing credentials, sending requests, and handling responses from the service’s APIs. See the Installing the watsonx Orchestrate ADK and Installing the watsonx Orchestrate Developer Edition.
​
Creating the agent and tool files
The following steps guide you to create the agent and tool files in YAML.
In your directory, create a folder with the name healthcare_provider.
Open a text editor, such as Visual Studio Code.
To create the agent, copy the following code:
YAML
spec_version: v1
kind: native
name: healthcare_agent
description: |
    You are a specialist in healthcare providers. When prompted use the getHealthCareProviders tool to get a list of all healthcare providers matching the users qquery. Display the results are a table

llm: groq/openai/gpt-oss-120b
style: react_core
tools:
- getHealthCareProviders
See all 10 lines
Paste the code in the text editor and save the file as healthcare_agent.yaml in the healthcare_provider folder.
To create the tool, copy the following code:
YAML
servers:
- url: https://find-provider.1sqnxi8zv3dh.us-east.codeengine.appdomain.cloud
paths:
  /:
    get:
      operationId: getHealthCareProviders
      summary: Gets a list of healthcare providers
      description: Gets a list of healthcare providers
      parameters:
        - in: path
          name: location
          schema:
            type: string
          required: false
          description: The city, state or zipcode you want to get healthcare providers
        - in: path
          name: speciality
          schema:
            type: string
            enum: ["General Medicine", "Cardiology", "Pediatrics", "Orthopedics", "ENT", "Multi-specialty"]
          required: false
          description: The speciality of the healthcare provider
      responses:
        '200':
          description: Successfully retrieved list of healthcare providers
          content:
            application/json:
              schema:
                type: object
                properties:
                  providers:
                    type: array
                    items:
                      type: object
                      properties:
                        address:
                            type: string
                        contact:
                            type: object
                            properties:
                                email:
                                    type: string
                                phone:
                                    type: string
                        name:
                            type: string
                        provider_id:
                            type: string
                        provider_type:
                            type: string
                        specialty:
                            type: string
                required:
                  - data
See all 54 lines
Paste the code in the text editor and save the file as get_healthcare_providers.yaml in the healthcare_provider folder.
​
Importing the agent and tool files
The following steps guide you to import the agent and tool files to IBM watsonx Orchestrate Agent builder.
Open the terminal that you commonly use.
Navigate to the folder. For instance, cd ~/Desktop/healthcare_provider.
Run the following commands:
BASH
orchestrate tools import -k openapi -f ./get_healthcare_providers.yaml
BASH
orchestrate agents import -f healthcare_agent.yaml
​
Testing the agent
Test the agent in the IBM watsonx Orchestrate chat by following the steps:
Run the command orchestrate chat start.
In the chat, enter the question “What are my healthcare providers?”.
You can continue interacting with your agent.


---

Configuring SSO for Workday
Configuring SSO for Workday by using OAuth On-Behalf-Of flow
You can integrate watsonx Orchestrate with any enterprise application that supports token exchange and Single Sign-On (SSO). This configuration enables users to access third-party applications through watsonx Orchestrate embedded chat by using their own credentials.
Architecture overview
The diagram explains how watsonx Orchestrate connects with the following components:
An identity provider (IdP), such as Microsoft Entra ID (Entra ID). The same approach applies to other identity providers that support token exchange and Single Sign-On (SSO).
A third-party enterprise application, like Workday.
An application that hosts the embedded chat
This flow uses OAuth 2.0 On-Behalf-Of (OBO) to exchange tokens and enable secure access to data.
​
Flow summary
User authentication: The user logs in to the application that hosts the embedded chat by using their own credentials. The IdP authenticates the user and returns an access token.
Token propagation through embedded chat: The application that embeds watsonx Orchestrate web chat and receives the access token from IdP and passes it to watsonx Orchestrate.
Exchange tokens:
IBM watsonx Orchestrate:
Requests a SAML assertion from the IdP by using the access token.
Exchanges the SAML assertion for an access token from the enterprise application’s OAuth server.
API access: IBM watsonx Orchestrate uses the enterprise app’s access token to call its API, for example, Workday API, and retrieves data.
Response: The API response is returned to the user through the embedded chat in the application.
​
Tutorial: Connecting watsonx Orchestrate to Workday using Entra ID
The tutorial guides you to configure Single Sign-On (SSO) for Workday using Entra ID and the OAuth 2.0 On-Behalf-Of (OBO) flow with watsonx Orchestrate. This integration allows you to manage authentication centrally while giving users direct, secure access to Workday without separate logins.
​
Before you begin
Make sure that you have:
The application or web page where the embedded chat is hosted and registered with Entra ID and configured with the appropriate API permissions.
Client credentials for Workday API, such as client ID and secret.
Admin or Builder access to your watsonx Orchestrate instance.
The watsonx Orchestrate Agent Development Kit (ADK) installed and authenticated.
To install ADK, see Installing the watsonx Orchestrate ADK and Installing the watsonx Orchestrate Developer Edition.
​
Steps for configuring SSO authentication between watsonx Orchestrate and Workday
Verify SSO authentication between Entra ID and Workday (Optional)
Make sure that the SSO authentication is configured between Entra ID and Workday.
Configuring Workday connection on watsonx Orchestrate
Use the watsonx Orchestrate ADK (Agent Development Kit) to set up the OAuth 2.0 OBO flow. This configuration allows token exchange between Entra ID and Workday.
a. Set up the connection between Workday and watsonx Orchestrate.
You can either use a configuration file or CLI commands to set up the connection.
b. Configure the connection to the identity provider
c. Set the Workday OAuth server credentials
d. Embed watsonx Orchestrate web chat to your application
e. Test the integration


---

Configuring SSO for Workday
Verify SSO authentication between Entra ID and Workday
This part is optional, but very recommended before you start the configuration to make sure that the SSO authentication is configured between Entra ID and Workday.
​
Verify SSO authentication between Entra ID and Workday
Before configuring watsonx Orchestrate, verify the SSO authentication between Entra ID and Workday. Use CURL or Postman to run the commands.
1
Set your environment variables

Run the following commands in the terminal.
BASH
export CLIENTID=<entra_app_client_id>
export CLIENTSEC=<entra_app_client_secret>
export WD_TENANT=<entra_directory_tenant_id>
export SCOPE=http://www.workday.com/user_impersonation
export WD_CLIENTID=<workday_api_client_id>
export UNAME=<username_of_user>
export PWD=<password_of_user>
Replace <entra_app_client_id>, <entra_app_client_secret>, <entra_directory_tenant_id>, <workday_api_client_id>, <username_of_user> and <password_of_user> with the appropriate information.
2
Add permissions to access the Workday API

Before you can exchange tokens and access Workday APIs by using Entra ID, you need to configure the permissions for your app in Microsoft Entra.
a. Open Microsoft Entra admin center and navigate to App registrations.
b. Select your application used for token exchange.
c. Go to API permissions and select Add a permission.
d. Choose the Workday API.
e. Select Delegated permissions and add the required scopes.
For detailed steps, see Configure an application to access a web API in the Microsoft documentation.
3
Get a login token from Entra ID

Use the following command to get a login token. The password grant type is used to simulate user logging in to Entra ID.
BASH
curl -H 'Content-Type: application/x-www-form-urlencoded' \
  https://login.microsoftonline.com/$WD_TENANT/oauth2/v2.0/token \
  -d "grant_type=password&client_id=$CLIENTID&client_secret=$CLIENTSEC&scope=api://$CLIENTID/default&username=$UNAME&password=$PWD"
4
Exchange the login token for a SAML assertion

Use the following command to get SAML assertion from Entra ID. The JWT bearer grant type is used to exchange the access token for a SAML assertion.
Replace the $TOKEN with the token you received in the Step 3.
BASH
curl -H 'Content-Type: application/x-www-form-urlencoded' \
  https://login.microsoftonline.com/$WD_TENANT/oauth2/v2.0/token \
  -d "grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer&client_id=$CLIENTID&client_secret=$CLIENTSEC&assertion=$TOKEN&scope=$SCOPE&requested_token_use=on_behalf_of&requested_token_type=urn:ietf:params:oauth:token-type:saml2"
5
Exchange the SAML assertion for Workday access token

Run the following command to get SAML assertion. Replace the $SAML_ASSERT with the SAML assertion that you received in the Step 4.
BASH
curl -X POST https://<workday_domain>/ccx/oauth2/<workday_tenant>/token \
  -H 'content-type: application/x-www-form-urlencoded' \
  -d 'grant_type=urn:ietf:params:oauth:grant-type:saml2-bearer&client_id=$WD_CLIENTID&assertion=$SAML_ASSERT'
Replace the placeholders with your app’s details.
Parameter	Description
<workday_domain>	The domain of your Workday instance. This is where API requests are sent.
<workday_tenant>	Your Workday tenant identifier.
$SAML_ASSERT	The SAML assertion token received from Entra ID. Used to request a Workday access token.
6
Trigger the Workday API

Use your access token received from Step 5 to call Workday API.
BASH
curl --location 'https://<workday_domain>/ccx/api/common/v1/<workday_tenant>/workers' \
  --header 'Authorization: Bearer <workday_access_token>'
7
Result

If the token is valid and the API is correctly configured:
Workday returns a JSON response containing a list of workers for the specified tenant.


---


Configuring SSO for Workday
Configuring Workday connection on watsonx Orchestrate
In this part, you learn to configure the Workday connection on watsonx Orchestrate by setting the identity provider as Entra ID.
​
Before you begin
Start the Orchestrate ADK
Install the watsonx Orchestrate Developer Edition with the ADK and activate your watsonx Orchestrate instance. For detailed instructions, see Using your watsonx Orchestrate account and Activating an environment.
​
Setting the connection between Workday and watsonx Orchestrate
You can configure Workday connection in two ways:
Configuring the Workday connection with file
Configuring the Workday connection with CLI commands
The configuration with file is the recommended approach.
​
Configuring the Workday connection with file
Follow the steps to create and import the file:
Create a configuration file and name it as connections.yaml.
Insert the following code into the connections.yaml file.
YAML
spec_version: v1
kind: connections
app_id: <workday-app-id>
environments:
    draft:
    kind: oauth_auth_on_behalf_of_flow
    type: member
    sso: true
    server_url: https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token
    idp_config:
        header:
        content-type: application/x-www-form-urlencoded
        body:
        requested_token_use: on_behalf_of
        requested_token_type: urn:ietf:params:oauth:token-type:saml2
    app_config:
        header:
        content-type: application/x-www-form-urlencoded

    live:
    kind: oauth_auth_on_behalf_of_flow
    type: member
    sso: true
    server_url: https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token
    idp_config:
        header:
        content-type: application/x-www-form-urlencoded
        body:
        requested_token_use: on_behalf_of
        requested_token_type: urn:ietf:params:oauth:token-type:saml2
    app_config:
        header:
        content-type: application/x-www-form-urlencoded
See all 33 lines
Replace the following values:
<workday-app-id> - The ID of the Workday web page that hosts the embedded chat.
{tenant-id} - The tenant ID of the Microsoft Entra.
Run the commands to import the connections.yaml file. For more information, see Creating connections.
​
Configuring the Workday connection with CLI commands
Follow the steps to set the connection:
Enter the following code in the terminal:
BASH
orchestrate connections configure \
 --app-id <workday-app-id> \
 --env <env> \
 --type team \
 --kind oauth_auth_on_behalf_of_flow \
 --server-url https://example.workday.com/ccx/api/v1/tenant1
Replace the following values:
<workday-app-id> - The ID of the Workday web page that hosts the embedded chat.
<env> - The environment type, draft or live.
<token-url> - Token URL provided in your Workday API registration.
​
Configuring the identity provider as Entra ID
Enter the following code in the terminal:
BASH
orchestrate connections set-identity-provider \
 --app-id <workday-app-id> \
 --env <env> \
 --url https://login.microsoftonline.com/{tenant-id}/token \ 
 --client-id <entra-client-id> \ 
 --client-secret <entra-client-secret> \ 
 --scope http://www.workday.com/user_impersonation \ 
 --grant-type urn:ietf:params:oauth:grant-type:jwt-bearer \ 
 --requested_token_use=on_behalf_of \ --requested_token_type=urn:ietf:params:oauth:token-type:saml2
Note: If you are using IBM Security Verify as your identity provider, you need to specify only the grant_type. You can remove the requested_token_use and requested_token_type from the code.
Replace the following values:
<workday-app-id> - The ID of the Workday web page that hosts the embedded chat.
<env> - The environment type, draft or live.
{tenant-id} - The tenant ID of the Microsoft Entra.
<entra-client-id> - The Client ID of the Microsoft Entra.
<entra-client-secret> - The Client Secret of the Microsoft Entra.
​
Importing tool
You need to import your tool with the Workday application to watsonx Orchestrate. You can use the orchestrate tools import command with the --app-id flag to associate the Workday connection with the tool. See the steps:
Run the command according to the tool file type:
Python
BASH
orchestrate tools import -k python -f <path-to-file> --app-id <workday-app-id>
YAML (OpenAPI tools)
BASH
orchestrate tools import -k openapi -f <path-to-file> --app-id <workday-app-id>
Replace the following values:
<workday-app-id> - The ID of the Workday web page that hosts the embedded chat.
<path-to-file> - The path, name, and extension of the file
For more information, see [Associating a connection to a tool].
​
Configuring the Workday OAuth credentials
Enter the following code in the terminal:
BASH
orchestrate connections set-credentials \ 
--app-id <workday-app-id> \ 
--env <env> \ 
--client-id <client-id-workday> \ 
--token-url <token-url>  \
--grant-type authorization_code
Replace the following values:
<workday-app-id> - The ID of the Workday web page that hosts the embedded chat.
<env> - The environment type, draft or live.
<client-id-workday> - Client ID provided in your Workday API registration.
<token-url> - Token URL provided in your Workday API registration.
​
Adding watsonx Orchestrate web chat to your application
After the configuration is complete, embed the watsonx Orchestrate web chat to your web page or application. For detailed instructions on embedding the web chat, see Enabling Secure Embed Flow.
To enable SSO, in addition to the embed instructions, complete the following steps:
Create the createJWT.js and embed.html files. You can use the examples that are provided in the following tabs as templates for each file.
Save these files in your watsonx Orchestrate repository.
createJWT.js
embed.html
JAVASCRIPT
    /**
   * JWT Creation Service for watsonx Orchestrate Secure Embed Chat
   *
   * This module handles the server-side creation of JSON Web Tokens (JWTs) for secure
   * authentication with IBM watsonx Orchestrate embed chat. It demonstrates:
   *
   * 1. RS256 JWT signing using your private key
   * 2. Optional user payload encryption using IBM's public key
   * 3. Cookie-based anonymous user tracking
   * 4. Session-based user information enrichment
   *
   * Security Notes:
   * - Never expose your private key to the client side
   * - Always generate JWTs server-side only
   * - Use HTTPS in production environments
   * - Adjust token expiration times based on your security requirements
   */

  const fs = require("fs");
  const path = require("path");
  const express = require("express");
  const { v4: uuid } = require("uuid");
  const jwtLib = require("jsonwebtoken");
  const NodeRSA = require("node-rsa");

  const router = express.Router();

  /**
   * Load your server-side RSA private key (PEM format)
   *
   * This key is used to sign JWTs with the RS256 algorithm. The corresponding public key
   * must be uploaded to your watsonx Orchestrate instance security settings.
   *
   * IMPORTANT: Keep this file secure and never expose it to clients!
   *
   * Generate a new key pair using either method:
   *
   * Method 1 - Using ssh-keygen:
   *   ssh-keygen -t rsa -b 4096 -m PEM -f example-jwtRS256.key
   *   openssl rsa -in example-jwtRS256.key -pubout -outform PEM -out example-jwtRS256.key.pub
   *
   * Method 2 - Using openssl directly:
   *   openssl genrsa -out example-jwtRS256.key 4096
   *   openssl rsa -in example-jwtRS256.key -pubout -out example-jwtRS256.key.pub
   */
  const PRIVATE_KEY_PATH = path.join(__dirname, "../keys/example-jwtRS256.key");
  if (!fs.existsSync(PRIVATE_KEY_PATH)) {
    throw new Error(`Private key not found at ${PRIVATE_KEY_PATH}`);
  }
  const PRIVATE_KEY = fs.readFileSync(PRIVATE_KEY_PATH);

  /**
   * Load IBM's RSA public key (PEM format)
   *
   * This key is provided by IBM watsonx Orchestrate and is used to encrypt the user_payload
   * field in the JWT. This ensures that sensitive user information cannot be read by clients,
   * as only IBM's servers can decrypt it.
   *
   * You can obtain this key by:
   * 1. Running the wxo-embed-security-v4.sh script (recommended)
   * 2. Calling the generate-key-pair API endpoint manually
   *
   * The encrypted payload will be decrypted server-side by watsonx Orchestrate.
   */

  const IBM_PUBLIC_KEY_PATH = path.join(__dirname, "../keys/ibmPublic.key.pub");
  if (!fs.existsSync(IBM_PUBLIC_KEY_PATH)) {
    throw new Error(`IBM public key not found at ${IBM_PUBLIC_KEY_PATH}`);
  }
  const IBM_PUBLIC_KEY = fs.readFileSync(IBM_PUBLIC_KEY_PATH);

  /**
   * Cookie lifetime configuration
   *
   * This defines how long the anonymous user ID cookie will persist.
   * Currently set to 60ms for demonstration purposes. For production, use a longer duration
   * such as 45 days (45 * 24 * 60 * 60 * 1000 milliseconds).
   */

  const TIME_45_DAYS = 60; // Value for demonstration. Replace with: 45 * 24 * 60 * 60 * 1000 for production.

  /**
   * Create a signed JWT string for the Orchestrate embedded chat client.
   *
   * This function constructs a JWT with the following structure:
   *
   * @param {string} anonymousUserID - A stable identifier for anonymous users (from cookie)
   * @param {object|null} sessionInfo - Optional authenticated user session data
   *
   * JWT Claims:
   * - sub: Subject (user identifier) - should be a stable, unique ID for the user
   * - user_payload: Encrypted user data that will be decrypted by watsonx Orchestrate
   *   - name: User's display name
   *   - custom_message: Any custom message or metadata
   *   - custom_user_id: Your application's internal user ID
   *   - sso_token: Single sign-on token if applicable
   * - context: Additional context data accessible by the agent
   *   - clientID: Your client/organization identifier
   *   - name: User's name for display in chat
   *   - role: User's role (e.g., Admin, User, Guest)
   *
   * @returns {string} A signed JWT token string
   */
  function createJWTString(anonymousUserID, sessionInfo) {
    // Base JWT claims structure
    // Customize these fields based on your application's requirements
    const jwtContent = {
      // Subject: Unique identifier for the user
      // In production, use a real user ID from your authentication system
      sub: "FHY1234DD5", // Example value. Replace with actual user ID.

      // User payload: It will be encrypted with IBM's public key
      // This data is sensitive and will only be readable by watsonx Orchestrate servers
      // Optional
      user_payload: {
        sso_token: "sso_token",
      },

      // Context: Additional metadata accessible by the agent
      // This data is NOT encrypted and can be read by the client
      context: {
        clientID: "865511",      // Your client/organization ID
        name: "Ava",             // Display name in chat
        role: "Admin",           // User role
      },
    };

    // Enrich the JWT with authenticated session data if available
    // In production, this would come from your authentication system
    if (sessionInfo) {
      jwtContent.user_payload.name = sessionInfo.userName;
      jwtContent.user_payload.custom_user_id = sessionInfo.customUserID;
    }

    // Encrypt the user_payload using IBM's RSA public key
    // This ensures sensitive user data cannot be read by clients
    // Only watsonx Orchestrate servers can decrypt this data
    if (jwtContent.user_payload) {
      const rsaKey = new NodeRSA(IBM_PUBLIC_KEY);
      const dataString = JSON.stringify(jwtContent.user_payload);
      const utf8Data = Buffer.from(dataString, "utf-8");
      // Encrypt and encode as base64 string
      jwtContent.user_payload = rsaKey.encrypt(utf8Data, "base64");
    }

    // Sign the JWT using RS256 algorithm with your private key
    // The token expiration should be set based on your security requirements
    // Common values: "1h" (1 hour), "6h" (6 hours), "1d" (1 day)
    const jwtString = jwtLib.sign(jwtContent, PRIVATE_KEY, {
      algorithm: "RS256",
      expiresIn: "7100s", // Value for demonstration. The maximum expiry time is 7100 seconds.
    });

    return jwtString;
  }

  /**
   * Retrieve or create a stable anonymous user ID stored in a cookie
   *
   * This function ensures that anonymous users maintain a consistent identity across
   * page refreshes and sessions. The ID is stored in a secure HTTP-only cookie.
   *
   * Benefits:
   * - Prevents user identity from changing mid-session
   * - Enables conversation continuity for anonymous users
   * - Provides basic user tracking without requiring authentication
   *
   * @param {object} request - Express request object
   * @param {object} response - Express response object
   * @returns {string} The anonymous user ID
   */
  function getOrSetAnonymousID(request, response) {
    // Check if an anonymous ID already exists in cookies
    let anonymousID = request.cookies["ANONYMOUS-USER-ID"];

    // Generate a new ID if none exists
    if (!anonymousID) {
      // Create a short, readable ID using UUID (first 5 characters for demonstration)
      // In production, you might want to use the full UUID for better uniqueness
      anonymousID = `anon-${uuid().slice(0, 5)}`;
    }

    // Set or refresh the cookie with each request to maintain the session
    response.cookie("ANONYMOUS-USER-ID", anonymousID, {
      expires: new Date(Date.now() + TIME_45_DAYS),
      httpOnly: true,  // Prevents client-side JavaScript from accessing the cookie (security)
      sameSite: "Lax", // Provides CSRF protection while allowing normal navigation
      secure: false,   // Set to true in production when using HTTPS
    });

    return anonymousID;
  }

  /**
   * Parse authenticated session information from cookies
   *
   * This function retrieves user session data if the user is authenticated.
   * In a production application, you would:
   * 1. Verify the session token/cookie
   * 2. Fetch user information from your database or identity provider
   * 3. Validate user permissions
   *
   * For this demonstration, we simply parse a JSON string from a cookie.
   *
   * @param {object} request - Express request object
   * @returns {object|null} Session info object or null if not authenticated
   */
  function getSessionInfo(request) {
    const sessionInfo = request.cookies?.SESSION_INFO;
    if (!sessionInfo) return null;

    try {
      // Parse the JSON session data
      return JSON.parse(sessionInfo);
    } catch {
      // Return null if parsing fails (invalid JSON)
      return null;
    }
  }

  /**
   * Express route handler for JWT creation
   *
   * This endpoint is called by the client to obtain a fresh JWT token.
   * The token is required for secure authentication with watsonx Orchestrate embedded chat.
   *
   * Flow:
   * 1. Retrieve or create an anonymous user ID (stored in cookie)
   * 2. Check for authenticated session information
   * 3. Generate a signed JWT with user data
   * 4. Return the JWT as plain text response
   *
   * The client will include this JWT in the wxOConfiguration.token field
   * when initializing the embedded chat.
   *
   * @param {object} request - Express request object
   * @param {object} response - Express response object
   */
  function createJWT(request, response) {
    // Ensure we have a stable user ID (anonymous or authenticated)
    const anonymousUserID = getOrSetAnonymousID(request, response);

    // Get authenticated session data if available
    const sessionInfo = getSessionInfo(request);

    // Create and sign the JWT
    const token = createJWTString(anonymousUserID, sessionInfo);

    // Return the JWT as plain text
    response.send(token);
  }

  // Define the GET endpoint that returns a signed JWT string
  // This endpoint is called by the client before initializing the chat
  router.get("/", createJWT);

  module.exports = router;
See all 257 lines
Replace the <wo_tenant_id> and <sso_token> with appropriate information.
Parameter	Description
<wo_tenant_id>	Your watsonx Orchestrate tenant ID.
<sso_token>	The SSO token obtained from the Entra ID.
Run the following commands to retrieve the SSO token
BASH
curl --location 'https://login.microsoftonline.com/0195ea87-1839-4df0-9739-bf7eec6de925/oauth2/v2.0/token' \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --header 'Cookie: fpc=ArnSgeQ8FmNJkcInGVBWnw94mWYSAQAAAG0uod8OAAAA; stsservicecookie=estsfd; x-ms-gateway-slice=estsfd' \
  --data-urlencode 'grant_type=password' \
  --data-urlencode 'client_id=<client_id>' \
  --data-urlencode 'client_secret=<client_secret>' \
  --data-urlencode 'scope=api://<client_id>/default' \
  --data-urlencode '<username>' \
  --data-urlencode '<password>'
​
Testing the integration
To test the integration, sign in and interact with Workday through embedded chat.
Log in to the web page or application that hosts the embedded chat using your own credentials.
Start the watsonx Orchestrate chat widget.
Ask a Workday related query in the embedded chat.
​
Result
If the SSO authentication is correctly configured, the Workday returns a JSON response with the requested data.
​
Troubleshooting
Issue	Possible cause	Resolution
401 Unauthorized	Invalid SAML assertion or client credentials	Check your app’s API client credentials
invalid_grant	Redirect URI mismatch	Verify your IDP app settings
No response in embedded chat	Chat not embedded correctly	Verify the script and app ID


---

Configuring SSO for Workday
Configuring Workday connection on watsonx Orchestrate
In this part, you learn to configure the Workday connection on watsonx Orchestrate by setting the identity provider as Entra ID.
​
Before you begin
Start the Orchestrate ADK
Install the watsonx Orchestrate Developer Edition with the ADK and activate your watsonx Orchestrate instance. For detailed instructions, see Using your watsonx Orchestrate account and Activating an environment.
​
Setting the connection between Workday and watsonx Orchestrate
You can configure Workday connection in two ways:
Configuring the Workday connection with file
Configuring the Workday connection with CLI commands
The configuration with file is the recommended approach.
​
Configuring the Workday connection with file
Follow the steps to create and import the file:
Create a configuration file and name it as connections.yaml.
Insert the following code into the connections.yaml file.
YAML
spec_version: v1
kind: connections
app_id: <workday-app-id>
environments:
    draft:
    kind: oauth_auth_on_behalf_of_flow
    type: member
    sso: true
    server_url: https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token
    idp_config:
        header:
        content-type: application/x-www-form-urlencoded
        body:
        requested_token_use: on_behalf_of
        requested_token_type: urn:ietf:params:oauth:token-type:saml2
    app_config:
        header:
        content-type: application/x-www-form-urlencoded

    live:
    kind: oauth_auth_on_behalf_of_flow
    type: member
    sso: true
    server_url: https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token
    idp_config:
        header:
        content-type: application/x-www-form-urlencoded
        body:
        requested_token_use: on_behalf_of
        requested_token_type: urn:ietf:params:oauth:token-type:saml2
    app_config:
        header:
        content-type: application/x-www-form-urlencoded
See all 33 lines
Replace the following values:
<workday-app-id> - The ID of the Workday web page that hosts the embedded chat.
{tenant-id} - The tenant ID of the Microsoft Entra.
Run the commands to import the connections.yaml file. For more information, see Creating connections.
​
Configuring the Workday connection with CLI commands
Follow the steps to set the connection:
Enter the following code in the terminal:
BASH
orchestrate connections configure \
 --app-id <workday-app-id> \
 --env <env> \
 --type team \
 --kind oauth_auth_on_behalf_of_flow \
 --server-url https://example.workday.com/ccx/api/v1/tenant1
Replace the following values:
<workday-app-id> - The ID of the Workday web page that hosts the embedded chat.
<env> - The environment type, draft or live.
<token-url> - Token URL provided in your Workday API registration.
​
Configuring the identity provider as Entra ID
Enter the following code in the terminal:
BASH
orchestrate connections set-identity-provider \
 --app-id <workday-app-id> \
 --env <env> \
 --url https://login.microsoftonline.com/{tenant-id}/token \ 
 --client-id <entra-client-id> \ 
 --client-secret <entra-client-secret> \ 
 --scope http://www.workday.com/user_impersonation \ 
 --grant-type urn:ietf:params:oauth:grant-type:jwt-bearer \ 
 --requested_token_use=on_behalf_of \ --requested_token_type=urn:ietf:params:oauth:token-type:saml2
Note: If you are using IBM Security Verify as your identity provider, you need to specify only the grant_type. You can remove the requested_token_use and requested_token_type from the code.
Replace the following values:
<workday-app-id> - The ID of the Workday web page that hosts the embedded chat.
<env> - The environment type, draft or live.
{tenant-id} - The tenant ID of the Microsoft Entra.
<entra-client-id> - The Client ID of the Microsoft Entra.
<entra-client-secret> - The Client Secret of the Microsoft Entra.
​
Importing tool
You need to import your tool with the Workday application to watsonx Orchestrate. You can use the orchestrate tools import command with the --app-id flag to associate the Workday connection with the tool. See the steps:
Run the command according to the tool file type:
Python
BASH
orchestrate tools import -k python -f <path-to-file> --app-id <workday-app-id>
YAML (OpenAPI tools)
BASH
orchestrate tools import -k openapi -f <path-to-file> --app-id <workday-app-id>
Replace the following values:
<workday-app-id> - The ID of the Workday web page that hosts the embedded chat.
<path-to-file> - The path, name, and extension of the file
For more information, see [Associating a connection to a tool].
​
Configuring the Workday OAuth credentials
Enter the following code in the terminal:
BASH
orchestrate connections set-credentials \ 
--app-id <workday-app-id> \ 
--env <env> \ 
--client-id <client-id-workday> \ 
--token-url <token-url>  \
--grant-type authorization_code
Replace the following values:
<workday-app-id> - The ID of the Workday web page that hosts the embedded chat.
<env> - The environment type, draft or live.
<client-id-workday> - Client ID provided in your Workday API registration.
<token-url> - Token URL provided in your Workday API registration.
​
Adding watsonx Orchestrate web chat to your application
After the configuration is complete, embed the watsonx Orchestrate web chat to your web page or application. For detailed instructions on embedding the web chat, see Enabling Secure Embed Flow.
To enable SSO, in addition to the embed instructions, complete the following steps:
Create the createJWT.js and embed.html files. You can use the examples that are provided in the following tabs as templates for each file.
Save these files in your watsonx Orchestrate repository.
createJWT.js
embed.html
JAVASCRIPT
    /**
   * JWT Creation Service for watsonx Orchestrate Secure Embed Chat
   *
   * This module handles the server-side creation of JSON Web Tokens (JWTs) for secure
   * authentication with IBM watsonx Orchestrate embed chat. It demonstrates:
   *
   * 1. RS256 JWT signing using your private key
   * 2. Optional user payload encryption using IBM's public key
   * 3. Cookie-based anonymous user tracking
   * 4. Session-based user information enrichment
   *
   * Security Notes:
   * - Never expose your private key to the client side
   * - Always generate JWTs server-side only
   * - Use HTTPS in production environments
   * - Adjust token expiration times based on your security requirements
   */

  const fs = require("fs");
  const path = require("path");
  const express = require("express");
  const { v4: uuid } = require("uuid");
  const jwtLib = require("jsonwebtoken");
  const NodeRSA = require("node-rsa");

  const router = express.Router();

  /**
   * Load your server-side RSA private key (PEM format)
   *
   * This key is used to sign JWTs with the RS256 algorithm. The corresponding public key
   * must be uploaded to your watsonx Orchestrate instance security settings.
   *
   * IMPORTANT: Keep this file secure and never expose it to clients!
   *
   * Generate a new key pair using either method:
   *
   * Method 1 - Using ssh-keygen:
   *   ssh-keygen -t rsa -b 4096 -m PEM -f example-jwtRS256.key
   *   openssl rsa -in example-jwtRS256.key -pubout -outform PEM -out example-jwtRS256.key.pub
   *
   * Method 2 - Using openssl directly:
   *   openssl genrsa -out example-jwtRS256.key 4096
   *   openssl rsa -in example-jwtRS256.key -pubout -out example-jwtRS256.key.pub
   */
  const PRIVATE_KEY_PATH = path.join(__dirname, "../keys/example-jwtRS256.key");
  if (!fs.existsSync(PRIVATE_KEY_PATH)) {
    throw new Error(`Private key not found at ${PRIVATE_KEY_PATH}`);
  }
  const PRIVATE_KEY = fs.readFileSync(PRIVATE_KEY_PATH);

  /**
   * Load IBM's RSA public key (PEM format)
   *
   * This key is provided by IBM watsonx Orchestrate and is used to encrypt the user_payload
   * field in the JWT. This ensures that sensitive user information cannot be read by clients,
   * as only IBM's servers can decrypt it.
   *
   * You can obtain this key by:
   * 1. Running the wxo-embed-security-v4.sh script (recommended)
   * 2. Calling the generate-key-pair API endpoint manually
   *
   * The encrypted payload will be decrypted server-side by watsonx Orchestrate.
   */

  const IBM_PUBLIC_KEY_PATH = path.join(__dirname, "../keys/ibmPublic.key.pub");
  if (!fs.existsSync(IBM_PUBLIC_KEY_PATH)) {
    throw new Error(`IBM public key not found at ${IBM_PUBLIC_KEY_PATH}`);
  }
  const IBM_PUBLIC_KEY = fs.readFileSync(IBM_PUBLIC_KEY_PATH);

  /**
   * Cookie lifetime configuration
   *
   * This defines how long the anonymous user ID cookie will persist.
   * Currently set to 60ms for demonstration purposes. For production, use a longer duration
   * such as 45 days (45 * 24 * 60 * 60 * 1000 milliseconds).
   */

  const TIME_45_DAYS = 60; // Value for demonstration. Replace with: 45 * 24 * 60 * 60 * 1000 for production.

  /**
   * Create a signed JWT string for the Orchestrate embedded chat client.
   *
   * This function constructs a JWT with the following structure:
   *
   * @param {string} anonymousUserID - A stable identifier for anonymous users (from cookie)
   * @param {object|null} sessionInfo - Optional authenticated user session data
   *
   * JWT Claims:
   * - sub: Subject (user identifier) - should be a stable, unique ID for the user
   * - user_payload: Encrypted user data that will be decrypted by watsonx Orchestrate
   *   - name: User's display name
   *   - custom_message: Any custom message or metadata
   *   - custom_user_id: Your application's internal user ID
   *   - sso_token: Single sign-on token if applicable
   * - context: Additional context data accessible by the agent
   *   - clientID: Your client/organization identifier
   *   - name: User's name for display in chat
   *   - role: User's role (e.g., Admin, User, Guest)
   *
   * @returns {string} A signed JWT token string
   */
  function createJWTString(anonymousUserID, sessionInfo) {
    // Base JWT claims structure
    // Customize these fields based on your application's requirements
    const jwtContent = {
      // Subject: Unique identifier for the user
      // In production, use a real user ID from your authentication system
      sub: "FHY1234DD5", // Example value. Replace with actual user ID.

      // User payload: It will be encrypted with IBM's public key
      // This data is sensitive and will only be readable by watsonx Orchestrate servers
      // Optional
      user_payload: {
        sso_token: "sso_token",
      },

      // Context: Additional metadata accessible by the agent
      // This data is NOT encrypted and can be read by the client
      context: {
        clientID: "865511",      // Your client/organization ID
        name: "Ava",             // Display name in chat
        role: "Admin",           // User role
      },
    };

    // Enrich the JWT with authenticated session data if available
    // In production, this would come from your authentication system
    if (sessionInfo) {
      jwtContent.user_payload.name = sessionInfo.userName;
      jwtContent.user_payload.custom_user_id = sessionInfo.customUserID;
    }

    // Encrypt the user_payload using IBM's RSA public key
    // This ensures sensitive user data cannot be read by clients
    // Only watsonx Orchestrate servers can decrypt this data
    if (jwtContent.user_payload) {
      const rsaKey = new NodeRSA(IBM_PUBLIC_KEY);
      const dataString = JSON.stringify(jwtContent.user_payload);
      const utf8Data = Buffer.from(dataString, "utf-8");
      // Encrypt and encode as base64 string
      jwtContent.user_payload = rsaKey.encrypt(utf8Data, "base64");
    }

    // Sign the JWT using RS256 algorithm with your private key
    // The token expiration should be set based on your security requirements
    // Common values: "1h" (1 hour), "6h" (6 hours), "1d" (1 day)
    const jwtString = jwtLib.sign(jwtContent, PRIVATE_KEY, {
      algorithm: "RS256",
      expiresIn: "7100s", // Value for demonstration. The maximum expiry time is 7100 seconds.
    });

    return jwtString;
  }

  /**
   * Retrieve or create a stable anonymous user ID stored in a cookie
   *
   * This function ensures that anonymous users maintain a consistent identity across
   * page refreshes and sessions. The ID is stored in a secure HTTP-only cookie.
   *
   * Benefits:
   * - Prevents user identity from changing mid-session
   * - Enables conversation continuity for anonymous users
   * - Provides basic user tracking without requiring authentication
   *
   * @param {object} request - Express request object
   * @param {object} response - Express response object
   * @returns {string} The anonymous user ID
   */
  function getOrSetAnonymousID(request, response) {
    // Check if an anonymous ID already exists in cookies
    let anonymousID = request.cookies["ANONYMOUS-USER-ID"];

    // Generate a new ID if none exists
    if (!anonymousID) {
      // Create a short, readable ID using UUID (first 5 characters for demonstration)
      // In production, you might want to use the full UUID for better uniqueness
      anonymousID = `anon-${uuid().slice(0, 5)}`;
    }

    // Set or refresh the cookie with each request to maintain the session
    response.cookie("ANONYMOUS-USER-ID", anonymousID, {
      expires: new Date(Date.now() + TIME_45_DAYS),
      httpOnly: true,  // Prevents client-side JavaScript from accessing the cookie (security)
      sameSite: "Lax", // Provides CSRF protection while allowing normal navigation
      secure: false,   // Set to true in production when using HTTPS
    });

    return anonymousID;
  }

  /**
   * Parse authenticated session information from cookies
   *
   * This function retrieves user session data if the user is authenticated.
   * In a production application, you would:
   * 1. Verify the session token/cookie
   * 2. Fetch user information from your database or identity provider
   * 3. Validate user permissions
   *
   * For this demonstration, we simply parse a JSON string from a cookie.
   *
   * @param {object} request - Express request object
   * @returns {object|null} Session info object or null if not authenticated
   */
  function getSessionInfo(request) {
    const sessionInfo = request.cookies?.SESSION_INFO;
    if (!sessionInfo) return null;

    try {
      // Parse the JSON session data
      return JSON.parse(sessionInfo);
    } catch {
      // Return null if parsing fails (invalid JSON)
      return null;
    }
  }

  /**
   * Express route handler for JWT creation
   *
   * This endpoint is called by the client to obtain a fresh JWT token.
   * The token is required for secure authentication with watsonx Orchestrate embedded chat.
   *
   * Flow:
   * 1. Retrieve or create an anonymous user ID (stored in cookie)
   * 2. Check for authenticated session information
   * 3. Generate a signed JWT with user data
   * 4. Return the JWT as plain text response
   *
   * The client will include this JWT in the wxOConfiguration.token field
   * when initializing the embedded chat.
   *
   * @param {object} request - Express request object
   * @param {object} response - Express response object
   */
  function createJWT(request, response) {
    // Ensure we have a stable user ID (anonymous or authenticated)
    const anonymousUserID = getOrSetAnonymousID(request, response);

    // Get authenticated session data if available
    const sessionInfo = getSessionInfo(request);

    // Create and sign the JWT
    const token = createJWTString(anonymousUserID, sessionInfo);

    // Return the JWT as plain text
    response.send(token);
  }

  // Define the GET endpoint that returns a signed JWT string
  // This endpoint is called by the client before initializing the chat
  router.get("/", createJWT);

  module.exports = router;
See all 257 lines
Replace the <wo_tenant_id> and <sso_token> with appropriate information.
Parameter	Description
<wo_tenant_id>	Your watsonx Orchestrate tenant ID.
<sso_token>	The SSO token obtained from the Entra ID.
Run the following commands to retrieve the SSO token
BASH
curl --location 'https://login.microsoftonline.com/0195ea87-1839-4df0-9739-bf7eec6de925/oauth2/v2.0/token' \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --header 'Cookie: fpc=ArnSgeQ8FmNJkcInGVBWnw94mWYSAQAAAG0uod8OAAAA; stsservicecookie=estsfd; x-ms-gateway-slice=estsfd' \
  --data-urlencode 'grant_type=password' \
  --data-urlencode 'client_id=<client_id>' \
  --data-urlencode 'client_secret=<client_secret>' \
  --data-urlencode 'scope=api://<client_id>/default' \
  --data-urlencode '<username>' \
  --data-urlencode '<password>'
​
Testing the integration
To test the integration, sign in and interact with Workday through embedded chat.
Log in to the web page or application that hosts the embedded chat using your own credentials.
Start the watsonx Orchestrate chat widget.
Ask a Workday related query in the embedded chat.
​
Result
If the SSO authentication is correctly configured, the Workday returns a JSON response with the requested data.
​
Troubleshooting
Issue	Possible cause	Resolution
401 Unauthorized	Invalid SAML assertion or client credentials	Check your app’s API client credentials
invalid_grant	Redirect URI mismatch	Verify your IDP app settings
No response in embedded chat	Chat not embedded correctly	Verify the script and app ID


---

Tutorials
Tutorial: Using watsonx Orchestrate and Langflow
In this tutorial, you learn how to use Langflow flows in your watsonx Orchestrate agents.
To follow this tutorial, make sure you have access to a watsonx Orchestrate environment that supports Langflow integration.
Follow these steps to use watsonx Orchestrate with Langflow:
1
Set up your environment

Create a folder named watsonx_orchestrate_and_langflow to store all agents and tools.
Folder structure
watsonx_orchestrate_and_langflow
  |- .env
  |- .venv
  |- tools
  |- agents
Show folder structure details

2
Install watsonx Orchestrate ADK and activate your environment

To install watsonx Orchestrate ADK, run:

macOS & Linux

Windows
python -m venv .venv
source ./.venv/bin/activate
pip install ibm-watsonx-orchestrate
For more information about installing watsonx Orchestrate ADK, see Setting up and installing the ADK.
To add and activate your environment, run:
IBM Cloud
orchestrate env add -n <environment-name> -u <service-instance-url> --type <environment-type> --activate
The environment name is flexible—you can choose whatever you prefer. The service instance URL and environment type, however, must match your specific setup. For more information, see Getting credentials for your environments.
Note: To use watsonx Orchestrate Developer Edition as your environment, install it first. Then, start it using the --with-langflow flag to enable Langflow integration. For more information, see Installing watsonx Orchestrate Developer Edition.
3
Create a Langflow flow

Langflow flows convert into tools for watsonx Orchestrate. You create a flow in the Langflow visual editor and export it as JSON to import as a tool. You can access the Langflow visual editor as a standalone tool or through watsonx Orchestrate Developer Edition, which runs on port 7861.
For this tutorial, use the following prebuilt Langflow flow. It extracts actionable tasks from unstructured text such as meeting notes, transcripts, or chat logs. It identifies who needs to do what and by when, using pattern-based heuristics.
Copy the following JSON code block and save it as transcripts_action_item_extractor.json in your tools folder.
transcripts_action_item_extractor.json
{
  "data": {
    "edges": [
      {
        "animated": false,
        "className": "",
        "data": {
          "sourceHandle": {
            "dataType": "ChatInput",
            "id": "ChatInput-0jIqY",
            "name": "message",
            "output_types": [
              "Message"
            ]
          },
          "targetHandle": {
            "fieldName": "input_text",
            "id": "ActionItemExtractor-wFCst",
            "inputTypes": [
              "Message",
              "Data",
              "Text"
            ],
            "type": "other"
          }
        },
        "id": "xy-edge__ChatInput-0jIqY{œdataTypeœ:œChatInputœ,œidœ:œChatInput-0jIqYœ,œnameœ:œmessageœ,œoutput_typesœ:[œMessageœ]}-ActionItemExtractor-wFCst{œfieldNameœ:œinput_textœ,œidœ:œActionItemExtractor-wFCstœ,œinputTypesœ:[œMessageœ,œDataœ,œTextœ],œtypeœ:œotherœ}",
        "selected": false,
        "source": "ChatInput-0jIqY",
        "sourceHandle": "{œdataTypeœ:œChatInputœ,œidœ:œChatInput-0jIqYœ,œnameœ:œmessageœ,œoutput_typesœ:[œMessageœ]}",
        "target": "ActionItemExtractor-wFCst",
        "targetHandle": "{œfieldNameœ:œinput_textœ,œidœ:œActionItemExtractor-wFCstœ,œinputTypesœ:[œMessageœ,œDataœ,œTextœ],œtypeœ:œotherœ}"
      },
      {
        "animated": false,
        "className": "",
        "data": {
          "sourceHandle": {
            "dataType": "ActionItemExtractor",
            "id": "ActionItemExtractor-wFCst",
            "name": "message",
            "output_types": [
              "Message"
            ]
          },
          "targetHandle": {
            "fieldName": "input_value",
            "id": "ChatOutput-foQFW",
            "inputTypes": [
              "Data",
              "DataFrame",
              "Message"
            ],
            "type": "other"
          }
        },
        "id": "xy-edge__ActionItemExtractor-wFCst{œdataTypeœ:œActionItemExtractorœ,œidœ:œActionItemExtractor-wFCstœ,œnameœ:œmessageœ,œoutput_typesœ:[œMessageœ]}-ChatOutput-foQFW{œfieldNameœ:œinput_valueœ,œidœ:œChatOutput-foQFWœ,œinputTypesœ:[œDataœ,œDataFrameœ,œMessageœ],œtypeœ:œotherœ}",
        "selected": false,
        "source": "ActionItemExtractor-wFCst",
        "sourceHandle": "{œdataTypeœ:œActionItemExtractorœ,œidœ:œActionItemExtractor-wFCstœ,œnameœ:œmessageœ,œoutput_typesœ:[œMessageœ]}",
        "target": "ChatOutput-foQFW",
        "targetHandle": "{œfieldNameœ:œinput_valueœ,œidœ:œChatOutput-foQFWœ,œinputTypesœ:[œDataœ,œDataFrameœ,œMessageœ],œtypeœ:œotherœ}"
      }
    ],
    "nodes": [
      {
        "data": {
          "id": "ChatOutput-foQFW",
          "node": {
            "base_classes": [
              "Message"
            ],
            "beta": false,
            "conditional_paths": [],
            "custom_fields": {},
            "description": "Display a chat message in the Playground.",
            "display_name": "Chat Output",
            "documentation": "https://docs.langflow.org/components-io#chat-output",
            "edited": false,
            "field_order": [
              "input_value",
              "should_store_message",
              "sender",
              "sender_name",
              "session_id",
              "data_template",
              "background_color",
              "chat_icon",
              "text_color",
              "clean_data"
            ],
            "frozen": false,
            "icon": "MessagesSquare",
            "legacy": false,
            "lf_version": "1.5.0.post2",
            "metadata": {},
            "minimized": true,
            "output_types": [],
            "outputs": [
              {
                "allows_loop": false,
                "cache": true,
                "display_name": "Output Message",
                "group_outputs": false,
                "method": "message_response",
                "name": "message",
                "selected": "Message",
                "tool_mode": true,
                "types": [
                  "Message"
                ],
                "value": "__UNDEFINED__"
              }
            ],
            "pinned": false,
            "template": {
              "_type": "Component",
              "background_color": {
                "_input_type": "MessageTextInput",
                "advanced": true,
                "display_name": "Background Color",
                "dynamic": false,
                "info": "The background color of the icon.",
                "input_types": [
                  "Message"
                ],
                "list": false,
                "list_add_label": "Add More",
                "load_from_db": false,
                "name": "background_color",
                "placeholder": "",
                "required": false,
                "show": true,
                "title_case": false,
                "tool_mode": false,
                "trace_as_input": true,
                "trace_as_metadata": true,
                "type": "str",
                "value": ""
              },
              "chat_icon": {
                "_input_type": "MessageTextInput",
                "advanced": true,
                "display_name": "Icon",
                "dynamic": false,
                "info": "The icon of the message.",
                "input_types": [
                  "Message"
                ],
                "list": false,
                "list_add_label": "Add More",
                "load_from_db": false,
                "name": "chat_icon",
                "placeholder": "",
                "required": false,
                "show": true,
                "title_case": false,
                "tool_mode": false,
                "trace_as_input": true,
                "trace_as_metadata": true,
                "type": "str",
                "value": ""
              },
              "clean_data": {
                "_input_type": "BoolInput",
                "advanced": true,
                "display_name": "Basic Clean Data",
                "dynamic": false,
                "info": "Whether to clean the data",
                "list": false,
                "list_add_label": "Add More",
                "name": "clean_data",
                "placeholder": "",
                "required": false,
                "show": true,
                "title_case": false,
                "tool_mode": false,
                "trace_as_metadata": true,
                "type": "bool",
                "value": true
              },
              "code": {
                "advanced": true,
                "dynamic": true,
                "fileTypes": [],
                "file_path": "",
                "info": "",
                "list": false,
                "load_from_db": false,
                "multiline": true,
                "name": "code",
                "password": false,
                "placeholder": "",
                "required": true,
                "show": true,
                "title_case": false,
                "type": "code",
                "value": "from collections.abc import Generator\nfrom typing import Any\n\nimport orjson\nfrom fastapi.encoders import jsonable_encoder\n\nfrom langflow.base.io.chat import ChatComponent\nfrom langflow.helpers.data import safe_convert\nfrom langflow.inputs.inputs import BoolInput, DropdownInput, HandleInput, MessageTextInput\nfrom langflow.schema.data import Data\nfrom langflow.schema.dataframe import DataFrame\nfrom langflow.schema.message import Message\nfrom langflow.schema.properties import Source\nfrom langflow.template.field.base import Output\nfrom langflow.utils.constants import (\n    MESSAGE_SENDER_AI,\n    MESSAGE_SENDER_NAME_AI,\n    MESSAGE_SENDER_USER,\n)\n\n\nclass ChatOutput(ChatComponent):\n    display_name = \"Chat Output\"\n    description = \"Display a chat message in the Playground.\"\n    documentation: str = \"https://docs.langflow.org/components-io#chat-output\"\n    icon = \"MessagesSquare\"\n    name = \"ChatOutput\"\n    minimized = True\n\n    inputs = [\n        HandleInput(\n            name=\"input_value\",\n            display_name=\"Inputs\",\n            info=\"Message to be passed as output.\",\n            input_types=[\"Data\", \"DataFrame\", \"Message\"],\n            required=True,\n        ),\n        BoolInput(\n            name=\"should_store_message\",\n            display_name=\"Store Messages\",\n            info=\"Store the message in the history.\",\n            value=True,\n            advanced=True,\n        ),\n        DropdownInput(\n            name=\"sender\",\n            display_name=\"Sender Type\",\n            options=[MESSAGE_SENDER_AI, MESSAGE_SENDER_USER],\n            value=MESSAGE_SENDER_AI,\n            advanced=True,\n            info=\"Type of sender.\",\n        ),\n        MessageTextInput(\n            name=\"sender_name\",\n            display_name=\"Sender Name\",\n            info=\"Name of the sender.\",\n            value=MESSAGE_SENDER_NAME_AI,\n            advanced=True,\n        ),\n        MessageTextInput(\n            name=\"session_id\",\n            display_name=\"Session ID\",\n            info=\"The session ID of the chat. If empty, the current session ID parameter will be used.\",\n            advanced=True,\n        ),\n        MessageTextInput(\n            name=\"data_template\",\n            display_name=\"Data Template\",\n            value=\"{text}\",\n            advanced=True,\n            info=\"Template to convert Data to Text. If left empty, it will be dynamically set to the Data's text key.\",\n        ),\n        MessageTextInput(\n            name=\"background_color\",\n            display_name=\"Background Color\",\n            info=\"The background color of the icon.\",\n            advanced=True,\n        ),\n        MessageTextInput(\n            name=\"chat_icon\",\n            display_name=\"Icon\",\n            info=\"The icon of the message.\",\n            advanced=True,\n        ),\n        MessageTextInput(\n            name=\"text_color\",\n            display_name=\"Text Color\",\n            info=\"The text color of the name\",\n            advanced=True,\n        ),\n        BoolInput(\n            name=\"clean_data\",\n            display_name=\"Basic Clean Data\",\n            value=True,\n            info=\"Whether to clean the data\",\n            advanced=True,\n        ),\n    ]\n    outputs = [\n        Output(\n            display_name=\"Output Message\",\n            name=\"message\",\n            method=\"message_response\",\n        ),\n    ]\n\n    def _build_source(self, id_: str | None, display_name: str | None, source: str | None) -> Source:\n        source_dict = {}\n        if id_:\n            source_dict[\"id\"] = id_\n        if display_name:\n            source_dict[\"display_name\"] = display_name\n        if source:\n            # Handle case where source is a ChatOpenAI object\n            if hasattr(source, \"model_name\"):\n                source_dict[\"source\"] = source.model_name\n            elif hasattr(source, \"model\"):\n                source_dict[\"source\"] = str(source.model)\n            else:\n                source_dict[\"source\"] = str(source)\n        return Source(**source_dict)\n\n    async def message_response(self) -> Message:\n        # First convert the input to string if needed\n        text = self.convert_to_string()\n\n        # Get source properties\n        source, icon, display_name, source_id = self.get_properties_from_source_component()\n        background_color = self.background_color\n        text_color = self.text_color\n        if self.chat_icon:\n            icon = self.chat_icon\n\n        # Create or use existing Message object\n        if isinstance(self.input_value, Message):\n            message = self.input_value\n            # Update message properties\n            message.text = text\n        else:\n            message = Message(text=text)\n\n        # Set message properties\n        message.sender = self.sender\n        message.sender_name = self.sender_name\n        message.session_id = self.session_id\n        message.flow_id = self.graph.flow_id if hasattr(self, \"graph\") else None\n        message.properties.source = self._build_source(source_id, display_name, source)\n        message.properties.icon = icon\n        message.properties.background_color = background_color\n        message.properties.text_color = text_color\n\n        # Store message if needed\n        if self.session_id and self.should_store_message:\n            stored_message = await self.send_message(message)\n            self.message.value = stored_message\n            message = stored_message\n\n        self.status = message\n        return message\n\n    def _serialize_data(self, data: Data) -> str:\n        \"\"\"Serialize Data object to JSON string.\"\"\"\n        # Convert data.data to JSON-serializable format\n        serializable_data = jsonable_encoder(data.data)\n        # Serialize with orjson, enabling pretty printing with indentation\n        json_bytes = orjson.dumps(serializable_data, option=orjson.OPT_INDENT_2)\n        # Convert bytes to string and wrap in Markdown code blocks\n        return \"```json\\n\" + json_bytes.decode(\"utf-8\") + \"\\n```\"\n\n    def _validate_input(self) -> None:\n        \"\"\"Validate the input data and raise ValueError if invalid.\"\"\"\n        if self.input_value is None:\n            msg = \"Input data cannot be None\"\n            raise ValueError(msg)\n        if isinstance(self.input_value, list) and not all(\n            isinstance(item, Message | Data | DataFrame | str) for item in self.input_value\n        ):\n            invalid_types = [\n                type(item).__name__\n                for item in self.input_value\n                if not isinstance(item, Message | Data | DataFrame | str)\n            ]\n            msg = f\"Expected Data or DataFrame or Message or str, got {invalid_types}\"\n            raise TypeError(msg)\n        if not isinstance(\n            self.input_value,\n            Message | Data | DataFrame | str | list | Generator | type(None),\n        ):\n            type_name = type(self.input_value).__name__\n            msg = f\"Expected Data or DataFrame or Message or str, Generator or None, got {type_name}\"\n            raise TypeError(msg)\n\n    def convert_to_string(self) -> str | Generator[Any, None, None]:\n        \"\"\"Convert input data to string with proper error handling.\"\"\"\n        self._validate_input()\n        if isinstance(self.input_value, list):\n            return \"\\n\".join([safe_convert(item, clean_data=self.clean_data) for item in self.input_value])\n        if isinstance(self.input_value, Generator):\n            return self.input_value\n        return safe_convert(self.input_value)\n"
              },
              "data_template": {
                "_input_type": "MessageTextInput",
                "advanced": true,
                "display_name": "Data Template",
                "dynamic": false,
                "info": "Template to convert Data to Text. If left empty, it will be dynamically set to the Data's text key.",
                "input_types": [
                  "Message"
                ],
                "list": false,
                "list_add_label": "Add More",
                "load_from_db": false,
                "name": "data_template",
                "placeholder": "",
                "required": false,
                "show": true,
                "title_case": false,
                "tool_mode": false,
                "trace_as_input": true,
                "trace_as_metadata": true,
                "type": "str",
                "value": "{text}"
              },
              "input_value": {
                "_input_type": "HandleInput",
                "advanced": false,
                "display_name": "Inputs",
                "dynamic": false,
                "info": "Message to be passed as output.",
                "input_types": [
                  "Data",
                  "DataFrame",
                  "Message"
                ],
                "list": false,
                "list_add_label": "Add More",
                "name": "input_value",
                "placeholder": "",
                "required": true,
                "show": true,
                "title_case": false,
                "trace_as_metadata": true,
                "type": "other",
                "value": ""
              },
              "sender": {
                "_input_type": "DropdownInput",
                "advanced": true,
                "combobox": false,
                "dialog_inputs": {},
                "display_name": "Sender Type",
                "dynamic": false,
                "info": "Type of sender.",
                "name": "sender",
                "options": [
                  "Machine",
                  "User"
                ],
                "options_metadata": [],
                "placeholder": "",
                "required": false,
                "show": true,
                "title_case": false,
                "toggle": false,
                "tool_mode": false,
                "trace_as_metadata": true,
                "type": "str",
                "value": "Machine"
              },
              "sender_name": {
                "_input_type": "MessageTextInput",
                "advanced": true,
                "display_name": "Sender Name",
                "dynamic": false,
                "info": "Name of the sender.",
                "input_types": [
                  "Message"
                ],
                "list": false,
                "list_add_label": "Add More",
                "load_from_db": false,
                "name": "sender_name",
                "placeholder": "",
                "required": false,
                "show": true,
                "title_case": false,
                "tool_mode": false,
                "trace_as_input": true,
                "trace_as_metadata": true,
                "type": "str",
                "value": "AI"
              },
              "session_id": {
                "_input_type": "MessageTextInput",
                "advanced": true,
                "display_name": "Session ID",
                "dynamic": false,
                "info": "The session ID of the chat. If empty, the current session ID parameter will be used.",
                "input_types": [
                  "Message"
                ],
                "list": false,
                "list_add_label": "Add More",
                "load_from_db": false,
                "name": "session_id",
                "placeholder": "",
                "required": false,
                "show": true,
                "title_case": false,
                "tool_mode": false,
                "trace_as_input": true,
                "trace_as_metadata": true,
                "type": "str",
                "value": ""
              },
              "should_store_message": {
                "_input_type": "BoolInput",
                "advanced": true,
                "display_name": "Store Messages",
                "dynamic": false,
                "info": "Store the message in the history.",
                "list": false,
                "list_add_label": "Add More",
                "name": "should_store_message",
                "placeholder": "",
                "required": false,
                "show": true,
                "title_case": false,
                "tool_mode": false,
                "trace_as_metadata": true,
                "type": "bool",
                "value": true
              },
              "text_color": {
                "_input_type": "MessageTextInput",
                "advanced": true,
                "display_name": "Text Color",
                "dynamic": false,
                "info": "The text color of the name",
                "input_types": [
                  "Message"
                ],
                "list": false,
                "list_add_label": "Add More",
                "load_from_db": false,
                "name": "text_color",
                "placeholder": "",
                "required": false,
                "show": true,
                "title_case": false,
                "tool_mode": false,
                "trace_as_input": true,
                "trace_as_metadata": true,
                "type": "str",
                "value": ""
              }
            },
            "tool_mode": false
          },
          "showNode": false,
          "type": "ChatOutput"
        },
        "dragging": false,
        "id": "ChatOutput-foQFW",
        "measured": {
          "height": 48,
          "width": 192
        },
        "position": {
          "x": 1305.2380909179308,
          "y": 1447.3493269157782
        },
        "selected": false,
        "type": "genericNode"
      },
      {
        "data": {
          "id": "ChatInput-0jIqY",
          "node": {
            "base_classes": [
              "Message"
            ],
            "beta": false,
            "conditional_paths": [],
            "custom_fields": {},
            "description": "Get chat inputs from the Playground.",
            "display_name": "Chat Input",
            "documentation": "https://docs.langflow.org/components-io#chat-input",
            "edited": false,
            "field_order": [
              "input_value",
              "should_store_message",
              "sender",
              "sender_name",
              "session_id",
              "files",
              "background_color",
              "chat_icon",
              "text_color"
            ],
            "frozen": false,
            "icon": "MessagesSquare",
            "legacy": false,
            "lf_version": "1.5.0.post2",
            "metadata": {},
            "minimized": true,
            "output_types": [],
            "outputs": [
              {
                "allows_loop": false,
                "cache": true,
                "display_name": "Chat Message",
                "group_outputs": false,
                "method": "message_response",
                "name": "message",
                "selected": "Message",
                "tool_mode": true,
                "types": [
                  "Message"
                ],
                "value": "__UNDEFINED__"
              }
            ],
            "pinned": false,
            "template": {
              "_type": "Component",
              "background_color": {
                "_input_type": "MessageTextInput",
                "advanced": true,
                "display_name": "Background Color",
                "dynamic": false,
                "info": "The background color of the icon.",
                "input_types": [
                  "Message"
                ],
                "list": false,
                "list_add_label": "Add More",
                "load_from_db": false,
                "name": "background_color",
                "placeholder": "",
                "required": false,
                "show": true,
                "title_case": false,
                "tool_mode": false,
                "trace_as_input": true,
                "trace_as_metadata": true,
                "type": "str",
                "value": ""
              },
              "chat_icon": {
                "_input_type": "MessageTextInput",
                "advanced": true,
                "display_name": "Icon",
                "dynamic": false,
                "info": "The icon of the message.",
                "input_types": [
                  "Message"
                ],
                "list": false,
                "list_add_label": "Add More",
                "load_from_db": false,
                "name": "chat_icon",
                "placeholder": "",
                "required": false,
                "show": true,
                "title_case": false,
                "tool_mode": false,
                "trace_as_input": true,
                "trace_as_metadata": true,
                "type": "str",
                "value": ""
              },
              "code": {
                "advanced": true,
                "dynamic": true,
                "fileTypes": [],
                "file_path": "",
                "info": "",
                "list": false,
                "load_from_db": false,
                "multiline": true,
                "name": "code",
                "password": false,
                "placeholder": "",
                "required": true,
                "show": true,
                "title_case": false,
                "type": "code",
                "value": "from langflow.base.data.utils import IMG_FILE_TYPES, TEXT_FILE_TYPES\nfrom langflow.base.io.chat import ChatComponent\nfrom langflow.inputs.inputs import BoolInput\nfrom langflow.io import (\n    DropdownInput,\n    FileInput,\n    MessageTextInput,\n    MultilineInput,\n    Output,\n)\nfrom langflow.schema.message import Message\nfrom langflow.utils.constants import (\n    MESSAGE_SENDER_AI,\n    MESSAGE_SENDER_NAME_USER,\n    MESSAGE_SENDER_USER,\n)\n\n\nclass ChatInput(ChatComponent):\n    display_name = \"Chat Input\"\n    description = \"Get chat inputs from the Playground.\"\n    documentation: str = \"https://docs.langflow.org/components-io#chat-input\"\n    icon = \"MessagesSquare\"\n    name = \"ChatInput\"\n    minimized = True\n\n    inputs = [\n        MultilineInput(\n            name=\"input_value\",\n            display_name=\"Input Text\",\n            value=\"\",\n            info=\"Message to be passed as input.\",\n            input_types=[],\n        ),\n        BoolInput(\n            name=\"should_store_message\",\n            display_name=\"Store Messages\",\n            info=\"Store the message in the history.\",\n            value=True,\n            advanced=True,\n        ),\n        DropdownInput(\n            name=\"sender\",\n            display_name=\"Sender Type\",\n            options=[MESSAGE_SENDER_AI, MESSAGE_SENDER_USER],\n            value=MESSAGE_SENDER_USER,\n            info=\"Type of sender.\",\n            advanced=True,\n        ),\n        MessageTextInput(\n            name=\"sender_name\",\n            display_name=\"Sender Name\",\n            info=\"Name of the sender.\",\n            value=MESSAGE_SENDER_NAME_USER,\n            advanced=True,\n        ),\n        MessageTextInput(\n            name=\"session_id\",\n            display_name=\"Session ID\",\n            info=\"The session ID of the chat. If empty, the current session ID parameter will be used.\",\n            advanced=True,\n        ),\n        FileInput(\n            name=\"files\",\n            display_name=\"Files\",\n            file_types=TEXT_FILE_TYPES + IMG_FILE_TYPES,\n            info=\"Files to be sent with the message.\",\n            advanced=True,\n            is_list=True,\n            temp_file=True,\n        ),\n        MessageTextInput(\n            name=\"background_color\",\n            display_name=\"Background Color\",\n            info=\"The background color of the icon.\",\n            advanced=True,\n        ),\n        MessageTextInput(\n            name=\"chat_icon\",\n            display_name=\"Icon\",\n            info=\"The icon of the message.\",\n            advanced=True,\n        ),\n        MessageTextInput(\n            name=\"text_color\",\n            display_name=\"Text Color\",\n            info=\"The text color of the name\",\n            advanced=True,\n        ),\n    ]\n    outputs = [\n        Output(display_name=\"Chat Message\", name=\"message\", method=\"message_response\"),\n    ]\n\n    async def message_response(self) -> Message:\n        background_color = self.background_color\n        text_color = self.text_color\n        icon = self.chat_icon\n\n        message = await Message.create(\n            text=self.input_value,\n            sender=self.sender,\n            sender_name=self.sender_name,\n            session_id=self.session_id,\n            files=self.files,\n            properties={\n                \"background_color\": background_color,\n                \"text_color\": text_color,\n                \"icon\": icon,\n            },\n        )\n        if self.session_id and isinstance(message, Message) and self.should_store_message:\n            stored_message = await self.send_message(\n                message,\n            )\n            self.message.value = stored_message\n            message = stored_message\n\n        self.status = message\n        return message\n"
              },
              "files": {
                "_input_type": "FileInput",
                "advanced": true,
                "display_name": "Files",
                "dynamic": false,
                "fileTypes": [
                  "txt",
                  "md",
                  "mdx",
                  "csv",
                  "json",
                  "yaml",
                  "yml",
                  "xml",
                  "html",
                  "htm",
                  "pdf",
                  "docx",
                  "py",
                  "sh",
                  "sql",
                  "js",
                  "ts",
                  "tsx",
                  "jpg",
                  "jpeg",
                  "png",
                  "bmp",
                  "image"
                ],
                "file_path": "",
                "info": "Files to be sent with the message.",
                "list": true,
                "list_add_label": "Add More",
                "name": "files",
                "placeholder": "",
                "required": false,
                "show": true,
                "temp_file": true,
                "title_case": false,
                "trace_as_metadata": true,
                "type": "file",
                "value": ""
              },
              "input_value": {
                "_input_type": "MultilineInput",
                "advanced": false,
                "copy_field": false,
                "display_name": "Input Text",
                "dynamic": false,
                "info": "Message to be passed as input.",
                "input_types": [],
                "list": false,
                "list_add_label": "Add More",
                "load_from_db": false,
                "multiline": true,
                "name": "input_value",
                "placeholder": "",
                "required": false,
                "show": true,
                "title_case": false,
                "tool_mode": false,
                "trace_as_input": true,
                "trace_as_metadata": true,
                "type": "str",
                "value": ""
              },
              "sender": {
                "_input_type": "DropdownInput",
                "advanced": true,
                "combobox": false,
                "dialog_inputs": {},
                "display_name": "Sender Type",
                "dynamic": false,
                "info": "Type of sender.",
                "name": "sender",
                "options": [
                  "Machine",
                  "User"
                ],
                "options_metadata": [],
                "placeholder": "",
                "required": false,
                "show": true,
                "title_case": false,
                "toggle": false,
                "tool_mode": false,
                "trace_as_metadata": true,
                "type": "str",
                "value": "User"
              },
              "sender_name": {
                "_input_type": "MessageTextInput",
                "advanced": true,
                "display_name": "Sender Name",
                "dynamic": false,
                "info": "Name of the sender.",
                "input_types": [
                  "Message"
                ],
                "list": false,
                "list_add_label": "Add More",
                "load_from_db": false,
                "name": "sender_name",
                "placeholder": "",
                "required": false,
                "show": true,
                "title_case": false,
                "tool_mode": false,
                "trace_as_input": true,
                "trace_as_metadata": true,
                "type": "str",
                "value": "User"
              },
              "session_id": {
                "_input_type": "MessageTextInput",
                "advanced": true,
                "display_name": "Session ID",
                "dynamic": false,
                "info": "The session ID of the chat. If empty, the current session ID parameter will be used.",
                "input_types": [
                  "Message"
                ],
                "list": false,
                "list_add_label": "Add More",
                "load_from_db": false,
                "name": "session_id",
                "placeholder": "",
                "required": false,
                "show": true,
                "title_case": false,
                "tool_mode": false,
                "trace_as_input": true,
                "trace_as_metadata": true,
                "type": "str",
                "value": ""
              },
              "should_store_message": {
                "_input_type": "BoolInput",
                "advanced": true,
                "display_name": "Store Messages",
                "dynamic": false,
                "info": "Store the message in the history.",
                "list": false,
                "list_add_label": "Add More",
                "name": "should_store_message",
                "placeholder": "",
                "required": false,
                "show": true,
                "title_case": false,
                "tool_mode": false,
                "trace_as_metadata": true,
                "type": "bool",
                "value": true
              },
              "text_color": {
                "_input_type": "MessageTextInput",
                "advanced": true,
                "display_name": "Text Color",
                "dynamic": false,
                "info": "The text color of the name",
                "input_types": [
                  "Message"
                ],
                "list": false,
                "list_add_label": "Add More",
                "load_from_db": false,
                "name": "text_color",
                "placeholder": "",
                "required": false,
                "show": true,
                "title_case": false,
                "tool_mode": false,
                "trace_as_input": true,
                "trace_as_metadata": true,
                "type": "str",
                "value": ""
              }
            },
            "tool_mode": false
          },
          "showNode": false,
          "type": "ChatInput"
        },
        "dragging": false,
        "id": "ChatInput-0jIqY",
        "measured": {
          "height": 48,
          "width": 192
        },
        "position": {
          "x": 483.27198739198275,
          "y": 1403.115073503278
        },
        "selected": false,
        "type": "genericNode"
      },
      {
        "data": {
          "id": "ActionItemExtractor-wFCst",
          "node": {
            "base_classes": [
              "Message"
            ],
            "beta": false,
            "conditional_paths": [],
            "custom_fields": {},
            "description": "Extracts actionable tasks, assignees, and due dates from text using pattern matching.",
            "display_name": "Action Item Extractor",
            "documentation": "https://github.com/logspace-ai/langflow/wiki/Custom-Components",
            "edited": true,
            "field_order": [
              "input_text"
            ],
            "frozen": false,
            "icon": "check-square",
            "legacy": false,
            "metadata": {},
            "minimized": false,
            "output_types": [],
            "outputs": [
              {
                "allows_loop": false,
                "cache": true,
                "display_name": "Action Items (Formatted)",
                "group_outputs": false,
                "hidden": null,
                "method": "extract_action_items",
                "name": "message",
                "options": null,
                "required_inputs": null,
                "selected": "Message",
                "tool_mode": true,
                "types": [
                  "Message"
                ],
                "value": "__UNDEFINED__"
              }
            ],
            "pinned": false,
            "template": {
              "_type": "Component",
              "code": {
                "advanced": true,
                "dynamic": true,
                "fileTypes": [],
                "file_path": "",
                "info": "",
                "list": false,
                "load_from_db": false,
                "multiline": true,
                "name": "code",
                "password": false,
                "placeholder": "",
                "required": true,
                "show": true,
                "title_case": false,
                "type": "code",
                "value": "from langflow.custom import Component\nfrom langflow.inputs import HandleInput\nfrom langflow.io import Output\nfrom langflow.schema.message import Message\nimport re\nfrom datetime import datetime, timedelta\n\n# ---------- helpers (Action Item Logic) ----------\n# (All helpers remain the same as they handle the core logic correctly)\n\nVERB_TRIGGERS = [\n    \"send\",\"email\",\"review\",\"approve\",\"draft\",\"write\",\"update\",\"fix\",\"create\",\n    \"schedule\",\"set up\",\"setup\",\"follow up\",\"follow-up\",\"ping\",\"share\",\n    \"prepare\",\"organize\",\"book\",\"call\",\"document\",\"summarize\",\"deploy\",\n    \"ship\",\"merge\",\"assign\",\"clean up\",\"cleanup\"\n]\nVERB_RX = r\"(?:{})(?:\\b|$)\".format(\"|\".join(sorted(set(map(re.escape, VERB_TRIGGERS)), key=len, reverse=True)))\n\nWEEKDAY_MAP = {\n    \"monday\":0,\"mon\":0,\"tuesday\":1,\"tue\":1,\"tues\":1,\"wednesday\":2,\"wed\":2,\n    \"thursday\":3,\"thu\":3,\"thur\":3,\"thurs\":3,\"friday\":4,\"fri\":4,\"saturday\":5,\n    \"sat\":5,\"sun\":6\n}\n\n# Regex Patterns for Assignments\nASSIGNMENT_PATTERNS = [\n    rf\"\"\"\n    (?P<full_match>^.*?)\n    (?P<assignee>(?:@?\\b[A-Z][a-z]+(?:\\s[A-Z][a-z]+)?\\b|@[\\w\\.-]+))\n    \\s*(?:to|will|should|must|needs\\s+to)\\s+\n    (?P<task>.*?)\n    (?:\\s+(?:by|before|due|deadline)\\s+(?P<due>[^.;,\\n]+))?\n    (?=[.;\\n]|$|\\n)\n    \"\"\",\n    rf\"\"\"\n    (?P<full_match>^.*?)\n    (?P<assignee>(?:@?\\b[A-Z][a-z]+(?:\\s[A-Z][a-z]+)?\\b|@[\\w\\.-]+))\n    \\s*:\\s*\n    (?P<task>.*?)\n    (?:\\s+(?:by|before|due|deadline)\\s+(?P<due>[^.;,\\n]+))?\n    (?=[.;\\n]|$|\\n)\n    \"\"\",\n    rf\"\"\"\n    (?:^|\\n)(?:[-*]\\s+|\\d+\\.\\s+)?(?P<task>(?:(?!- \\[).)*?\\b{VERB_RX}.*?)\n    (?:\\s+(?:by|before|due|deadline)\\s+(?P<due>[^.;,\\n]+))?\n    (?=[.;\\n]|$)\n    \"\"\"\n]\nASSIGNMENT_RES_SPECIFIC = [re.compile(p, re.IGNORECASE | re.VERBOSE | re.MULTILINE | re.DOTALL) for p in ASSIGNMENT_PATTERNS[:2]]\nASSIGNMENT_RES_GENERAL = re.compile(ASSIGNMENT_PATTERNS[2], re.IGNORECASE | re.MULTILINE)\n\nCHECKBOX_RE = re.compile(\n    rf\"(?:^|\\n)-\\s*\\[\\s*\\]\\s*(?P<task>.*?)(?:\\s+(?:by|before|due|deadline)\\s+(?P<due>[^.;,\\n]+))?(?=[.;\\n]|$)\",\n    re.IGNORECASE | re.MULTILINE\n)\n\nDUE_TOKEN_RE = re.compile(r\"(?:^|\\s)(?:by|before|due|deadline)\\s+\", re.IGNORECASE)\n\nDATE_FORM_RXES = [\n    re.compile(r\"\\b(\\d{4})-(\\d{1,2})-(\\d{1,2})\\b\"),\n    re.compile(r\"\\b(\\d{1,2})/(\\d{1,2})(?:/(\\d{2,4}))?\\b\"),\n    re.compile(r\"\\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec|January|February|March|April|June|July|August|September|October|November|December)\\.?\\s+(\\d{1,2})(?:,\\s*(\\d{4}))?\\b\", re.IGNORECASE),\n]\n\ndef _today():\n    return datetime(2025, 10, 7).date()\n\ndef parse_relative_due(text: str):\n    if not text: return None\n    t = text.strip().lower()\n    if t in (\"eod\",\"by eod\",\"before eod\",\"today\"): return _today()\n    if t in (\"tomorrow\",): return _today() + timedelta(days=1)\n    if t in (\"eow\",\"end of week\"):\n        today = _today(); dow = today.isoweekday(); return today + timedelta(days=(7 - dow))\n    if t == \"next week\":\n        today=_today(); dow=today.weekday(); d=(7-dow)%7; d=7 if d==0 else d; return today+timedelta(days=d)\n    if t.startswith(\"next \"):\n        wd = t.replace(\"next \",\"\").strip().lower()\n        if wd in WEEKDAY_MAP:\n            today=_today(); target=WEEKDAY_MAP[wd]; cur=today.weekday()\n            d=(target-cur)%7; d=7 if d==0 else d; return today+timedelta(days=d)\n    if t in WEEKDAY_MAP:\n        today=_today(); target=WEEKDAY_MAP[t]; cur=today.weekday()\n        d=(target-cur)\n        if d < 0:\n            d += 7\n        return today+timedelta(days=d)\n    return None\n\ndef parse_any_date(text: str):\n    rel = parse_relative_due(text)\n    if rel: return rel.isoformat()\n    for rx in DATE_FORM_RXES:\n        m = rx.search(text)\n        if not m: continue\n        if rx is DATE_FORM_RXES[0]:\n            try: y,mo,d = map(int,m.groups()); return datetime(y,mo,d).date().isoformat()\n            except ValueError: continue\n        elif rx is DATE_FORM_RXES[1]:\n            mo,d,y = m.groups(); mo,d = int(mo),int(d)\n            if y:\n                y = int(y); y = y+2000 if y<70 else (y+1900 if y<100 else y)\n            else:\n                y = _today().year\n            try: return datetime(y,mo,d).date().isoformat()\n            except ValueError: continue\n        else:\n            mon_str,d,y = m.groups(); d=int(d)\n            mon_map={\"jan\":1,\"feb\":2,\"mar\":3,\"apr\":4,\"may\":5,\"jun\":6,\"jul\":7,\"aug\":8,\"sep\":9,\"sept\":9,\n                     \"oct\":10,\"nov\":11,\"dec\":12,\"january\":1,\"february\":2,\"march\":3,\"april\":4,\"june\":6,\n                     \"july\":7,\"august\":8,\"september\":9,\"october\":10,\"november\":11,\"december\":12}\n            mon_key = mon_str.lower()\n            if mon_key not in mon_map: continue\n            mo = mon_map[mon_key]\n            y = int(y) if y else _today().year\n            try: return datetime(y,mo,d).date().isoformat()\n            except ValueError: continue\n    return None\n\ndef clean_due_phrase(due: str) -> str:\n    return DUE_TOKEN_RE.sub(\"\", (due or \"\")).strip(\" .,:;\")\n\ndef extract_candidates(text: str):\n    items = []\n    text = re.sub(r\"[•·►]+\", \"-\", text).replace(\"\\r\", \"\")\n    \n    for m in CHECKBOX_RE.finditer(text):\n        task = (m.group(\"task\") or \"\").strip()\n        due_raw = clean_due_phrase(m.group(\"due\") or \"\")\n        due_iso = parse_any_date(due_raw) if due_raw else None\n        items.append({\"assignee\": None, \"task\": task, \"due_raw\": due_raw or None, \"due\": due_iso})\n\n    for rx in ASSIGNMENT_RES_SPECIFIC:\n        for m in rx.finditer(text):\n            task = (m.group(\"task\") or \"\").strip()\n            if not re.search(VERB_RX, task, flags=re.IGNORECASE): continue\n            assignee = m.groupdict().get(\"assignee\")\n            if assignee: assignee = assignee.strip()\n            due_raw = clean_due_phrase(m.groupdict().get(\"due\") or \"\")\n            task = re.sub(r\"\\s+(?:by|before|due|deadline)\\s+[^.;,\\n]+$\", \"\", task, flags=re.IGNORECASE).strip()\n            due_iso = parse_any_date(due_raw) if due_raw else None\n            items.append({\"assignee\": assignee, \"task\": task, \"due_raw\": due_raw or None, \"due\": due_iso})\n            \n    for m in ASSIGNMENT_RES_GENERAL.finditer(text):\n        task = (m.group(\"task\") or \"\").strip()\n        if re.match(VERB_RX, task, flags=re.IGNORECASE):\n            due_raw = clean_due_phrase(m.groupdict().get(\"due\") or \"\")\n            task = re.sub(r\"\\s+(?:by|before|due|deadline)\\s+[^.;,\\n]+$\", \"\", task, flags=re.IGNORECASE).strip()\n            due_iso = parse_any_date(due_raw) if due_raw else None\n            items.append({\"assignee\": None, \"task\": task, \"due_raw\": due_raw or None, \"due\": due_iso})\n\n    seen, out = set(), []\n    for it in items:\n        if not it[\"assignee\"] and re.search(r'(\\b[A-Z][a-z]+\\b|\\@[\\w\\.-]+).*(to|will|should|must|needs\\s+to).*\\b{}'.format(VERB_RX), it[\"task\"], flags=re.IGNORECASE):\n            continue\n        key = ((it[\"assignee\"] or \"\").lower(), it[\"task\"].lower(), it[\"due\"] or it[\"due_raw\"] or \"\")\n        if key in seen: continue\n        seen.add(key); out.append(it)\n        \n    return out\n\n# --- FINAL REVISED FORMATTING FUNCTION ---\ndef format_output_message(items):\n    current_date_str = datetime.now().strftime(\"%Y-%m-%d\")\n    \n    # Check for no items found\n    if not items:\n        # Move the emoji immediately after the header text and use a single newline\n        # to see if it helps with visibility and line breaks in the UI.\n        return f\"🚨 Action Items ({current_date_str}) \\n\\n_No clear action items found._\"\n    \n    lines = [f\"🚨 Action Items ({current_date_str})\\n\"]\n    \n    for it in items:\n        who = it[\"assignee\"] or \"*Unassigned*\"\n        task = it[\"task\"]\n        due = it[\"due\"] or it[\"due_raw\"]\n        \n        # Format: • *Assignee* — Task Description — (*Due/by: Date*)\n        line = f\"• *{who}* — {task}\"\n        if due:\n            due_prefix = \"Due\" if it[\"due\"] else \"by\"\n            line += f\" — (*{due_prefix}: {due}*)\"\n        \n        # Use a single newline for clean separation within the final output string\n        lines.append(line + \"\\n\") \n    \n    # Join with no separator between items, relying on the single newline added inside the loop\n    return \"\\n\".join(lines).strip()\n# ----------------------------------------\n\n# --------------------------------------------------------------------------\n\nclass ActionItemExtractorComponent(Component):\n    display_name = \"Action Item Extractor\"\n    description = \"Extracts actionable tasks, assignees, and due dates from text using pattern matching.\"\n    documentation: str = \"https://github.com/logspace-ai/langflow/wiki/Custom-Components\"\n    icon = \"check-square\"\n    name = \"ActionItemExtractor\"\n    \n    inputs = [\n        HandleInput(\n            name=\"input_text\",\n            display_name=\"Text Input (Notes/Transcript)\",\n            info=\"The unstructured text to analyze for action items.\",\n            input_types=[\"Message\", \"Data\", \"Text\"],\n            required=True,\n        ),\n    ]\n    \n    outputs = [\n        Output(display_name=\"Action Items (Formatted)\", name=\"message\", method=\"extract_action_items\"),\n    ]\n\n    async def extract_action_items(self) -> Message:\n        input_data = self.input_text\n        if hasattr(input_data, 'text'):\n            text = input_data.text\n        elif isinstance(input_data, str):\n            text = input_data\n        else:\n            text = str(input_data)\n        \n        if not text:\n            output_str = format_output_message([])\n            items = []\n        else:\n            items = extract_candidates(text)\n            output_str = format_output_message(items)\n\n        message = await Message.create(\n            text=output_str,\n            data={\"action_items\": items}\n        )\n        self.status = message\n        return message"
              },
              "input_text": {
                "_input_type": "HandleInput",
                "advanced": false,
                "display_name": "Text Input (Notes/Transcript)",
                "dynamic": false,
                "info": "The unstructured text to analyze for action items.",
                "input_types": [
                  "Message",
                  "Data",
                  "Text"
                ],
                "list": false,
                "list_add_label": "Add More",
                "name": "input_text",
                "placeholder": "",
                "required": true,
                "show": true,
                "title_case": false,
                "trace_as_metadata": true,
                "type": "other",
                "value": ""
              }
            },
            "tool_mode": false
          },
          "showNode": true,
          "type": "ActionItemExtractor"
        },
        "dragging": false,
        "id": "ActionItemExtractor-wFCst",
        "measured": {
          "height": 182,
          "width": 320
        },
        "position": {
          "x": 854.216673639581,
          "y": 1312.4409402877736
        },
        "selected": false,
        "type": "genericNode"
      }
    ],
    "viewport": {
      "x": -513.2138469095416,
      "y": -1407.4845991779855,
      "zoom": 1.403054578646979
    }
  },
  "description": "Extracts actionable tasks from unstructured text such as meeting notes, transcripts, or chat logs. It identifies who needs to do what and by when, using pattern-based heuristics.",
  "endpoint_name": null,
  "id": "72f8a871-0697-43d1-b460-f77cb845dbc1",
  "is_component": false,
  "last_tested_version": "1.5.0.post2",
  "name": "transcripts_action_item_extractor",
  "tags": []
}
See all 805 lines
4
(Optional) Test Langflow flow in the visual editor

You can test the Langflow flow in the Playground of the Langflow visual editor. To do this:
Open the Langflow visual editor.
Click Upload a flow.
Import the transcripts_action_item_extractor.json file.
Click Playground.
Test the Langflow flow.
Input
Output
Example
**[09:00:15] Sarah:** Okay everyone, let's officially kick off. The core Q3 review is actually solid. . Honestly, very good. We just have these, like, these weird loose ends.
**[09:01:22] Alice:** Uh, yeah. On the comms part, I was just thinking about that Q3 deck. So, uh, I'm taking the lead on the client update. We're good there. Alice to send the Q3 deck by Friday. I mean, that's what I said before, but yeah, it's firm.
**[09:02:40] Mark:** Yeah, and I know Bob, you're slammed, but what's the ETA on the new API documentation? That's kinda our bottleneck now.
**[09:03:01] Bob:** Uh-huh. Bob will review the API docs tomorrow. Yeah, that's completely locked in. I just need a clean four hours for the final check. Oh, and John, are you on the call?
**[09:03:55] John:** (unintelligible) Yeah, I'm here. Customer call. Yes. John: I'm speaking with the customer by 10/12. We can move that out of the blocker list.
**[09:04:30] Sarah:** Fantastic, okay. So John's clear. Now, the public announcement, let's not let that slip. We need to get the statement ready. Draft the announcement before Oct 15 so Legal has, like, you know, a full week.
**[09:05:15] Mark:** And one other thing, admin stuff, but critical. Site visits are coming up fast. We should also book rooms next week for the new candidates. I'll flag that in a separate chat right after this.
**[09:06:05] Sarah:** Sounds like a plan. Thanks for the clarity on those dates. Let's sync up again. Bye.
See all 9 lines

Langflow chat example

5
Import your Langflow flow into watsonx Orchestrate

To import your Langflow flow as a tool into watsonx Orchestrate, run:
BASH
orchestrate tools import -k langflow -f tools/transcripts_action_item_extractor.json
6
Add a tool to an agent

After importing your Langflow flow as a tool, add it to an agent. Copy the following agent definition to create a new agent that uses the Langflow flow tool. Save it as langflow_agent.yml in your agents folder.
langflow_agent.yml
kind: native
name: langflow_agent
display_name: Tutorial Langflow Agent
description: Tutorial Langflow Agent
context_access_enabled: true
context_variables: []
llm: watsonx/ibm/granite-4-h-small 
style: react_core
instructions: ''
guidelines: []
collaborators: []
tools:
- transcripts_action_item_extractor
knowledge_base: []
spec_version: v1
See all 15 lines
Then import the agent using:
ADK CLI command
orchestrate agents import -f  agents/langflow_agent.yml
7
Use your Langflow tool

To use your Langflow tool in the chat UI, go to the langflow_agent.
Input
Output
Example
**[09:00:15] Sarah:** Okay everyone, let's officially kick off. The core Q3 review is actually solid. . Honestly, very good. We just have these, like, these weird loose ends.
**[09:01:22] Alice:** Uh, yeah. On the comms part, I was just thinking about that Q3 deck. So, uh, I'm taking the lead on the client update. We're good there. Alice to send the Q3 deck by Friday. I mean, that's what I said before, but yeah, it's firm.
**[09:02:40] Mark:** Yeah, and I know Bob, you're slammed, but what's the ETA on the new API documentation? That's kinda our bottleneck now.
**[09:03:01] Bob:** Uh-huh. Bob will review the API docs tomorrow. Yeah, that's completely locked in. I just need a clean four hours for the final check. Oh, and John, are you on the call?
**[09:03:55] John:** (unintelligible) Yeah, I'm here. Customer call. Yes. John: I'm speaking with the customer by 10/12. We can move that out of the blocker list.
**[09:04:30] Sarah:** Fantastic, okay. So John's clear. Now, the public announcement, let's not let that slip. We need to get the statement ready. Draft the announcement before Oct 15 so Legal has, like, you know, a full week.
**[09:05:15] Mark:** And one other thing, admin stuff, but critical. Site visits are coming up fast. We should also book rooms next week for the new candidates. I'll flag that in a separate chat right after this.
**[09:06:05] Sarah:** Sounds like a plan. Thanks for the clarity on those dates. Let's sync up again. Bye.
See all 9 lines

Langflow and watsonx Orchestrate chat example

---

Tutorials
Tutorial: Using watsonx Orchestrate and BeeAI Framework
​
Overview
BeeAI Framework is an open-source, Linux Foundation-hosted framework for building production-grade AI agents with built-in constraint enforcement and rule-based governance. It supports both Python and TypeScript with native watsonx Orchestrate integration.
This tutorial shows you how to create and deploy a BeeAI external agent in Python that integrates with watsonx Orchestrate.
​
Prerequisites
Before starting, ensure you have:
Python 3.11 or higher
Poetry (Python package manager)
BeeAI Framework along with the watsonx Orchestrate extension installed (pip install 'beeai-framework[watsonx-orchestrate]')
Docker
An active watsonx Orchestrate account
Tavily API key (optional, for web search) - Get a free API key at tavily.com
​
Development & Testing
1
Project setup

Create a project directory and initialize Poetry:
mkdir watsonx_orchestrate_and_beeai_framework
cd watsonx_orchestrate_and_beeai_framework
poetry init --no-interaction
2
Configure dependencies

Show project files

Install dependencies and update the lock file:
poetry install --no-root
poetry lock
3
Configure your environment variables

Create a .env file in your project root and add your credentials:
touch .env
.env
# watsonx Configuration
WATSONX_URL=https://us-south.ml.cloud.ibm.com
WATSONX_REGION=us-south
WATSONX_PROJECT_ID=your-project-id-here
WATSONX_API_KEY=your-watsonx-api-key-here

# External Agent Security
API_KEY=your-secure-random-key

# Optional: Web Search
TAVILY_API_KEY=your-tavily-api-key-here
Where to find these values:
WATSONX_URL: Usually https://us-south.ml.cloud.ibm.com or your region’s URL
WATSONX_REGION: Your IBM Cloud region (e.g., us-south, eu-gb, jp-tok)
WATSONX_PROJECT_ID: Found in your watsonx.ai project settings
WATSONX_API_KEY: Create in IBM Cloud → Manage → Access (IAM) → API keys
API_KEY: Generate with openssl rand -base64 32 or use https://randomkeygen.com
TAVILY_API_KEY: Get free at https://tavily.com (optional)
4
Create project structure

Create the following directory structure:
mkdir wxo_beeai
touch wxo_beeai/__init__.py wxo_beeai/settings.py wxo_beeai/tools.py wxo_beeai/app.py Dockerfile docker-compose.yml
watsonx_orchestrate_and_beeai_framework/
├── wxo_beeai/
│   ├── __init__.py
│   ├── settings.py
│   ├── tools.py
│   └── app.py
├── .env
├── pyproject.toml
├── Dockerfile
└── docker-compose.yml
5
Create settings module

Create wxo_beeai/settings.py:
This file loads environment variables from the .env file, validates required configurations with Pydantic, and provides type-safe access to settings across the app.
wxo_beeai/settings.py
from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

__all__ = ["AppSettings"]

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="", str_to_upper=False)
    api_key: str = Field(..., description="Project API Key")
    watsonx_url: str
    watsonx_project_id: str
    watsonx_api_key: str
    tavily_api_key: str
    log_intermediate_steps: bool = Field(default=False)
    watsonx_default_model: str = "ibm/granite-3-3-8b-instruct"

AppSettings = Settings()
See all 19 lines
6
Create custom tools

Create wxo_beeai/tools.py:
This code defines a web search tool powered by the Tavily API. The @tool decorator registers it with the BeeAI Framework, and it’s configured to perform advanced searches returning up to 10 results.
wxo_beeai/tools.py
from beeai_framework.tools import tool
from tavily import TavilyClient
from wxo_beeai.settings import AppSettings

@tool
def search_web_tool(query: str) -> dict[str, str] | None:
    """
    Searches the web for the given query and returns the most relevant results.
    """
    client = TavilyClient(api_key=AppSettings.tavily_api_key)

    results = client.search(
        query,
        search_depth="advanced",
        max_results=10,
        include_images=False,
        include_answer=False,
    )

    return results

See all 21 lines
7
Create main application

Create wxo_beeai/app.py:
The following code launches an HTTP server that exposes a RequirementAgent built for deep research.
It connects key components — an unconstrained memory, a Watsonx chat model, reasoning tools (Think + Web Search), and runtime rules that guide the agent’s thinking process.
wxo_beeai/app.py
import logging
import sys
import traceback
import warnings

from beeai_framework.agents.requirement import RequirementAgent
from beeai_framework.agents.requirement.requirements.conditional import (
    ConditionalRequirement,
)
from beeai_framework.errors import FrameworkError
from beeai_framework.middleware.trajectory import GlobalTrajectoryMiddleware
from beeai_framework.tools import Tool
from beeai_framework.tools.think import ThinkTool
from beeai_framework.adapters.watsonx_orchestrate import (
    WatsonxOrchestrateServer,
    WatsonxOrchestrateServerConfig,
)
from beeai_framework.memory import UnconstrainedMemory
from beeai_framework.adapters.watsonx import WatsonxChatModel
from wxo_beeai.settings import AppSettings
from wxo_beeai.tools import search_web_tool

warnings.filterwarnings("ignore")

logger = logging.getLogger()
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

def main() -> None:

    memory = UnconstrainedMemory()

    llm = WatsonxChatModel(
        model_id=AppSettings.watsonx_default_model.removeprefix("watsonx/").lower(),
        api_key=AppSettings.watsonx_api_key,
        project_id=AppSettings.watsonx_project_id,
        base_url=AppSettings.watsonx_url,
        middlewares=[
            GlobalTrajectoryMiddleware(enabled=AppSettings.log_intermediate_steps)
        ],
    )

    agent = RequirementAgent(
        llm=llm,
        memory=memory,
        tools=[ThinkTool(), search_web_tool],
        role="a deep researcher",
        instructions=[
            "Your task is to conduct in-depth research on the given topic.",
            "Before you start, thoroughly prepare a step-by-step plan for how you will solve the task.",
            "After each action, reflect on what you have obtained and what you need to do to gather evidence for the final answer.",
        ],
        middlewares=[
            GlobalTrajectoryMiddleware(
                included=[Tool], enabled=AppSettings.log_intermediate_steps
            )
        ],
        requirements=[
            ConditionalRequirement(ThinkTool, consecutive_allowed=False),
            ConditionalRequirement(
                ThinkTool, force_at_step=1, force_after=[search_web_tool]
            ),
        ],
    )

    config = WatsonxOrchestrateServerConfig(
        port=8080, host="0.0.0.0", api_key=AppSettings.api_key
    )

    server = WatsonxOrchestrateServer(config=config)
    server.register(agent)
    server.serve()

if __name__ == "__main__":
    try:
        main()
    except FrameworkError as e:
        traceback.print_exc()
        sys.exit(e.explain())
See all 83 lines
Key components:
Memory — UnconstrainedMemory: Stores the full conversation history
LLM — WatsonxChatModel: The Watsonx chat model, configured from AppSettings, with middleware for logging intermediate steps
Agent — RequirementAgent: The main reasoning agent with planning capabilities, research-oriented instructions, and tool access
Tools — ThinkTool() and search_web_tool: Enable structured reasoning and online information retrieval
Requirements — ConditionalRequirement rules:
Enforces “thinking” at step 1
Prevents consecutive Think tool calls
Requires reflection after searches
Middleware — GlobalTrajectoryMiddleware: Logs intermediate reasoning and tool usage when enabled in settings
Server — WatsonxOrchestrateServer: Registers the agent and serves it via HTTP (0.0.0.0:8080) using the configured API key
Error handling — Catches FrameworkError, prints a traceback, and exits cleanly with a clear message
8
Docker configuration

Create Dockerfile:
Dockerfile
FROM python:3.11-slim AS python-base

# https://python-poetry.org/docs#ci-recommendations
ENV POETRY_VERSION=2.1.1
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv

# Tell Poetry where to place its cache and virtual environment
ENV POETRY_CACHE_DIR=/opt/.cache

# Create stage for Poetry installation
FROM python-base AS poetry-base

# Creating a virtual environment just for poetry and install it with pip
RUN python3 -m venv $POETRY_VENV \
	&& $POETRY_VENV/bin/pip install -U pip setuptools \
	&& $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Create a new stage from the base python image
FROM python-base AS example-app

# Copy Poetry to app image
COPY --from=poetry-base ${POETRY_VENV} ${POETRY_VENV}

# Add Poetry to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /app

# Copy Dependencies
COPY poetry.lock pyproject.toml ./

# Tell Poetry to not use its own venv
RUN poetry config virtualenvs.create false

# [OPTIONAL] Validate the project is properly configured
RUN poetry check

# Copy Application
COPY . /app

# Install Dependencies
RUN poetry install --no-interaction --no-cache

# Run Application
EXPOSE 8080

ENTRYPOINT ["poetry", "run", "python", "wxo_beeai/app.py"]
See all 48 lines
Create docker-compose.yml:
docker-compose.yml
services:
  app:
    container_name: wxo_beeai_test
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8080:8080"
    env_file:
      - .env
    environment:
      - PYTHONUNBUFFERED=1
    restart: no
9
Test locally

Run your agent locally with Docker Compose:
docker-compose up --build
Or run directly with Poetry:
poetry run python wxo_beeai/app.py
Tip: Visit http://localhost:8080/docs to see the FastAPI documentation and test the /chat/completions endpoint.
Test with curl:
curl -X POST "http://localhost:8080/chat/completions" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "messages": [
      {"role": "user", "content": "What are the latest developments in quantum computing?"}
    ]
  }'
​
Production Deployment
1
Deploy to IBM Code Engine

​
Create a Code Engine project
Navigate to IBM Cloud Code Engine Projects
Click Create and name your project (e.g., wxo-beeai)
​
Create registry secret
Go to Manage → Access (IAM) → API keys
Click Create and save the API key
​
Create the application
In your Code Engine project, select Applications → Create
Under Code, select Build container image from source code
Configure build details:
SSH secret: None
Context directory: Your GitHub repository URL
Branch: main
Dockerfile: Dockerfile
Registry secret: Create using your API key
Configure application:
Name: beeai-agent
Domain mappings: Public
Add environment variables:
WATSONX_URL
WATSONX_REGION
WATSONX_PROJECT_ID
WATSONX_API_KEY
API_KEY
TAVILY_API_KEY (optional)
Click Create
Visit your application URL with /docs appended, e.g. https://beeai-agent.xxxxx.codeengine.appdomain.cloud/docs
2
Register external agent in watsonx Orchestrate

In watsonx Orchestrate, click the hamburger menu → Agent Configuration
Select Assistants → Add assistant → External Assistant
Check External-agent Assistant
Configure:
Display Name: Research Agent
Description: Agent to conduct deep research using web search
API Key: Your API_KEY from .env
Service Instance URL: https://your-app-url/chat/completions
Click Save
3
Use your agent

Use from the GUI, or API
Navigate to Chat in watsonx Orchestrate
Ask research questions that route to your agent:
What are the latest developments in quantum computing?
Research the current state of renewable energy adoption.
What are the recent breakthroughs in AI?
The BeeAI agent will:
Create a research plan
Search the web for relevant information
Reflect on findings after each search
Provide a research-based answer
​
Next Steps
Explore BeeAI Framework documentation
Learn about RequirementAgent capabilities
Add custom tools for your specific use case
Experiment with different agent requirements and constraints

---

Customizing Embedded Chat
Customizing embedded chat to match your brand
By default, the watsonx Orchestrate embedded chat widget renders with IBM Blue styling. For customer-facing applications where visual consistency matters, this default appearance often conflicts with your brand identity.
watsonx Orchestrate supports full customization of the embedded chat, including colors, typography, layout, header controls, icons, and welcome messaging. You apply all customization options through documented, supported configuration properties — no internal CSS overrides or DOM manipulation needed.
​
Use cases
Brand customization is particularly relevant for:
Customer-facing portals such as banking, insurance, healthcare, and retail, where the chat must feel native to the site.
White-label products, where the application requires its own brand identity in place of vendor branding.
Design system compliance, where your organization enforces strict front-end standards that govern fonts, colors, and layout across all components.
​
Expected outcome
After you apply customization, the embedded chat widget uses your site’s brand colors for the header and message bubbles, displays your custom icon, and presents starter prompts aligned with your users’ most common tasks. The visual transition between the page and the chat stays consistent, and the widget feels like a native part of the application rather than a third-party component.
​
Next steps
Follow the step-by-step tutorial to apply these customizations to your own agent:
Customizing embedded chat to match your brand
watsonx Orchestrate continuously adds new customization options. Always refer to the UI configuration reference for the most up-to-date list of supported properties.

---

Customizing Embedded Chat
Tutorial: Customizing embedded chat to match your brand
In this tutorial, you learn how to customize the appearance and behavior of the watsonx Orchestrate embedded chat widget so that it matches your website’s brand. By default, the widget ships with IBM Blue styling. This tutorial covers three levels of customization, from point-and-click UI settings to full embed script control.
Customization is organized into three levels, each building on the previous one:
Level	Approach	Time estimate	What you control
1	Builder UI	~10 minutes	Agent name, starter prompts, voice mode, document upload
2	ADK YAML edits	~15 minutes	Custom icon, welcome message, hide reasoning trace
3	Embed script	~20 minutes	Colors, typography, layout, header controls
​
Before you begin
This tutorial uses a fictional banking assistant called Lendyr to exemplify branding customizations you can apply to any embedded chat deployment.
Before you start this tutorial, ensure you have the following:
An active watsonx Orchestrate account with an agent created and published.
The Agent Development Kit (ADK) installed for YAML-based edits.
Security configured for the embedded chat. For more information, see Configuring security for embedded chat.
Your orchestrationID and agentId values from the Channels tab in the Builder UI.
​
Level 1: Builder UI settings
The Builder UI provides point-and-click controls for the most common settings. No code is required.
Log in to the watsonx Orchestrate Builder UI.
Open your agent.
Configure the following settings:
Agent name, such as Lendyr Banking Assistant.
Starter prompts, such as Apply for a loan and Find nearest branch.
Chat with docs toggle: enable to allow document uploads.
Voice mode toggle: enable to allow speech input.
​
Level 2: ADK YAML edits
Three settings are not available in the Builder UI and require direct edits to the agent YAML file: hiding the reasoning trace, adding a custom icon, and writing a branded welcome message.
Open your agent YAML file in the ADK.
Add the following fields:
YAML
hide_reasoning: true

icon: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect width="100" height="100" fill="#2d5016"/>
  <text x="50" y="70" font-family="Arial" font-size="60"
        font-weight="bold" fill="#81c784" text-anchor="middle">D</text>
</svg>'

welcome_content:
  welcome_message: "Hi, I'm the Lendyr assistant!"
  description: "How can I help you today?"
  is_default_message: false
See all 12 lines
Deploy the updated agent:
BASH
orchestrate agents import -f your_agent.yaml
The custom icon SVG is the first visual element users see and carries the greatest branding impact. Set hide_reasoning: true in production deployments to prevent the agent’s internal thinking trace from reaching end users.
​
Level 3: Embed script configuration
The embed script gives you full control over colors, typography, layout, and header behavior.
Get the embed script from the Channels tab. You can also generate it from the CLI:
BASH
orchestrate channels webchat embed --agent-name=your_agent_name
Before the closing </body> tag of your page, add the window.wxOConfiguration object with your customizations:
JavaScript
window.wxOConfiguration = {
    orchestrationID: "your-orchestration-id",
    hostURL: "https://dl.watson-orchestrate.ibm.com",
    rootElementID: "root",
    showLauncher: true,

    chatOptions: {
        agentId: "your-agent-id",
        agentEnvironmentId: "your-env-id"
    },

    layout: {
        form: 'float',
        width: '800px',
        height: '600px',
        showMaxWidth: true
    },

    style: {
        headerColor: '#2d5016',
        userMessageBackgroundColor: '#2d5016',
        primaryColor: '#2d5016',
        showBackgroundGradient: true,
        fontFamily: 'Inter, system-ui, sans-serif'
    },

    header: {
        showResetButton: true,
        showAiDisclaimer: false,
        showMaximize: true,
        showAgentName: false,
        showAgentAvatar: false
    },

    features: {
        showThreadList: true
    },

    language: 'en'
};
See all 40 lines
Test on your staging site and adjust the colors and layout as needed.
Deploy to production.
​
Key configuration reference
Category	Property	Description
style	headerColor	Brand color for the chat header background
style	primaryColor	Color for interactive accents and highlights
style	userMessageBackgroundColor	Color for user message bubbles
style	fontFamily	Font stack to match your brand typography
header	showResetButton	Show or hide the conversation reset button
header	showMaximize	Show or hide the maximize button
header	showAgentName	Show or hide the agent name in the header
header	showAgentAvatar	Show or hide the agent avatar in the header
layout	form	'float' for a chat bubble, 'fullscreen-overlay' for full-page
layout	width / height	Override the default chat dimensions
features	showThreadList	Show or hide the conversation history panel
For a full list of supported options, see the UI configuration.
​
Testing your customization
After you deploy the embed script, verify the following:
The chat header uses your brand color.
User message bubbles use your brand color.
Your custom icon appears when the chat bubble is closed.
The welcome message matches your configured welcome_content.
Users do not see the reasoning trace or internal thinking.
Starter prompts appear on the chat landing screen.
​
Common issues
Issue	Solution
Colors appear different on your site	Test on a staging environment against your actual page background
Custom icon does not display	Check that the SVG syntax is valid and correctly inlined in YAML
Changes do not appear after deployment	Clear the browser cache and confirm you are targeting the correct environment, either Live or Draft


---

Tutorials
Advanced tutorials
​
Overview
This page provides advanced, pro-code tutorials for developing, extending, and operating agents by using the watsonx Orchestrate Agent Development Kit (ADK). The content focuses on programmatic patterns such as agent orchestration, MCP integration, security, event-driven architectures, and custom AI pipelines. Use these tutorials to build scalable, production-ready agent solutions with full control over behavior, integrations, and deployment workflows.
This content is authored by community contributors. Some information might not reflect the latest product behavior or updates. Validate the guidance before you use it in production environments.
​
Agent architecture and patterns
Building an Agent Swarm Pattern with watsonx Orchestrate https://achan2013.medium.com/building-agent-swarm-c412b0668f7b
Building an event-driven agentic AI system with Apache Kafka on Confluent Cloud and watsonx Orchestrate https://developer.ibm.com/tutorials/event-driven-agentic-ai-system-confluent-watsonx-orchestrate/
​
Programmatic agent development (ADK + Bob)
Build agentic workflows programmatically on watsonx Orchestrate using IBM Bob https://developer.ibm.com/tutorials/build-programmatic-agentic-workflows-watsonx-orchestrate-bob/
Using IBM Bob to build watsonx Orchestrate agents and MCP tools https://developer.ibm.com/tutorials/build-agents-mcp-tools-watsonx-orchestrate-using-bob/
Turn BPMN diagrams into production‑ready agents with Bob skills and watsonx Orchestrate https://developer.ibm.com/tutorials/bpmn-to-agents-bob-skills-watsonx-orchestrate/
​
Security, access control, and governance
Implement secure RBAC for MCP server access using context variables and On-Behalf-Of (OBO) flow in watsonx Orchestrate https://developer.ibm.com/tutorials/secure-rbac-mcp-context-variables-obo-watsonx-orchestrate/
Implement agent guardrails with watsonx Orchestrate plug-ins https://developer.ibm.com/tutorials/ai-agents-guardrails-watsonx-orchestrate-plugins/
​
Retrieval-augmented generation (RAG) and data integration
Build a custom RAG pipeline with Langflow and watsonx Orchestrate https://developer.ibm.com/tutorials/build-custom-rag-pipeline-langflow-watsonx-orchestrate/
Build a GraphRAG agent using watsonx Orchestrate and DataStax Astra DB https://developer.ibm.com/tutorials/graphrag-agent-watsonx-orchestrate-astradb/
​
Enterprise and industry use cases
Build an AI-driven supply chain workflow using IBM Sterling OMS and watsonx Orchestrate https://developer.ibm.com/tutorials/suppy-chain-agentic-ai-oms-watsonx-orchestrate/


---

Voice Runtime Browser Test Application
Overview
Build a comprehensive web-based testing tool for voice agents that provides real-time conversation testing, call recording, and CDR (Call Detail Record) monitoring capabilities.
This FastAPI application serves a browser-based interface for testing voice agents with three main features:
Talk to Your Agent - Interactive voice conversation testing with DTMF support
Call Recording Server - Record and playback voice conversations
CDR Logs - Monitor Call Detail Records and conversation analytics
​
Features
Talk to Your Agent

Test your voice agent in real-time through the browser interface.
Key Capabilities:
Real-time Voice Conversation: Connect to your voice agent via WebSocket
DTMF Support: Test touch-tone input using on-screen keypad or keyboard (0-9, *, #)
Audio Streaming: Bidirectional audio streaming at 16kHz PCM
Connection Management: Start/stop conversations with visual status indicators
Configuration Settings:
Agent ID
Environment ID
Access Token
Thread ID (optional)
WebSocket URL (defaults to current host)
Call Recording Server

Record, store, and playback voice conversations for analysis and debugging.
Recording Features:
Automatic Recording: Captures both user and agent audio streams
Multiple Audio Formats:
user.raw - User audio (mono, 16kHz, 16-bit PCM)
agent.raw - Agent audio (mono, 16kHz, 16-bit PCM)
interleave.raw - Combined stereo audio (both channels mixed)
Metadata Tracking: Duration, frame counts, timestamps
Browser Playback: Built-in audio player with automatic PCM-to-WAV conversion
Recording Management: View, browse, and delete recordings
Recording Server URL:
ws(s)://<host>/record
Configure your voice runtime to send recordings to this endpoint.
CDR Logs

Monitor and analyze Call Detail Records from your voice runtime.
CDR Monitoring Features:
Real-time Updates: Auto-refresh every 5 seconds when viewing
Statistics Dashboard:
Total reports count
Successful calls
Failed calls
Last received timestamp
Detailed Reports: View complete CDR payloads including:
Transaction ID
Agent ID
Environment ID
Call duration
Turn count
End reason
Failure indicators
Search Capabilities: Find reports by transaction ID or thread ID
Report Management: Clear all reports or view individual details
CDR Webhook URL:
http(s)://<host>/cdr-webhook
Configure your voice runtime to send CDR webhooks to this endpoint.

---

Voice Runtime Browser Test Application
Getting Started
You use this web-based tool to run real-time conversation tests for voice agents. You access the source code in the watsonx Orchestrate ADK repository.
​
Prerequisites
Install the following tools on your computer before you begin:
Git
Docker Engine
Python
pip
​
Quick start
Follow these steps to set up and run the tool.
1
Clone the watsonx Orchestrate ADK repository


HTTPS

SSH

GitHub CLI
git clone https://github.com/IBM/ibm-watsonx-orchestrate-adk.git
cd ibm-watsonx-orchestrate-adk
2
(Optional) Create a virtual environment


macOS & Linux

Windows
python -m venv .venv
source ./.venv/bin/activate
3
Install watsonx Orchestrate ADK

BASH
pip install ibm-watsonx-orchestrate
4
Navigate to the tool directory


macOS & Linux

Windows
cd /examples/voice
5
Start the tool

Run the following command to start the application:
BASH
uvicorn app:app --host 0.0.0.0 --port 9511
Open your browser and go to:
Browser UI: http://localhost:9511/
​
Environment Variables
PORT: Defines the port where the application runs. The default value is 9511.


--

Voice Runtime Browser Test Application
Deploying Browser Changes to IBM Code Engine
Package the voice testing harness as a Docker image and run it on IBM Code Engine to make your browser changes available remotely.
​
Build and Verify the Image Locally:
From the project root directory, build the Docker image:
BASH
docker buildx build \
  --platform linux/amd64 \
  -t agentic-webhooks \
  --load . 
After the build completes, run the image locally to confirm that the application starts and responds as expected:
BASH
# Run the local image
docker run -p 9511:9511 <your-image-name>

# Run interactively with shell access:
docker run -it -p 9511:9511 <your-image-name> /bin/bash

# Stop running container
docker stop <container-id-or-name>

# Tidy
docker rm <container-id-or-name>
Then, tag the image for IBM Cloud Container Registry:
BASH
# Use a date structure instead of latest for clarity
docker tag agentic-webhooks {{REGISTRY_URL}}/agentic-webhooks:20260421

$ docker image ls
agentic-webhooks:latest                         d350a69a97bf        163MB             0B
{{REGISTRY_URL}}/agentic-webhooks:20260421      d350a69a97bf        163MB             0B

--


Voice Runtime
Voice Runtime WebSocket Proxy
WebSocket proxy endpoint for browser ↔ voice runtime audio and control messages.

Voice Runtime WebSocket Proxy

curl --request GET \
  --url http://localhost:9511/v1/conversation


Query Parameters
​
agent_id
stringrequired
​
environment_id
stringrequired
​
access_token
stringrequired
​
thread_id
string
​
target_url
string<uri>required
  ---

Recordings
Call Recording WebSocket
WebSocket endpoint used by the voice runtime to stream call recordings.

Call Recording WebSocket

curl --request GET \
  --url http://localhost:9511/record

  ---

  Recordings
List all recordings
List all recordings

curl --request GET \
  --url http://localhost:9511/api/recordings

200
{
  "recordings": [
    {
      "id": "<string>",
      "name": "<string>",
      "metadata": {
        "transaction_id": "3c90c3cc-0d44-4b50-8888-8dd25736052a",
        "duration_ms": 123,
        "start_time": "2023-11-07T05:31:56Z",
        "user_frames": 123,
        "agent_frames": 123
      }
    }
  ],
  "count": 123
}
Response
200 - application/json
List of available recordings

​
recordings
object[]
Hide child attributes

​
recordings.id
string
​
recordings.name
string
​
recordings.metadata
object
Hide child attributes

​
recordings.metadata.transaction_id
string<uuid>
​
recordings.metadata.duration_ms
integer
​
recordings.metadata.start_time
string<date-time>
​
recordings.metadata.user_frames
integer
​
recordings.metadata.agent_frames
integer
​
count
integer

---

Recordings
Get files in a recording
Get files in a recording

curl --request GET \
  --url http://localhost:9511/api/recordings/{recording_id}

200
{
  "recording_id": "<string>",
  "files": [
    {
      "name": "<string>",
      "size": 123,
      "type": "<string>"
    }
  ]
}
Path Parameters
​
recording_id
stringrequired
Response
200 - application/json
Recording file list

​
recording_id
string
​
files
object[]
Hide child attributes

​
files.name
string
​
files.size
integer
​
files.type
string

---

Recordings
Delete a recording
Delete a recording

curl --request DELETE \
  --url http://localhost:9511/api/recordings/{recording_id}

200
{
  "message": "<string>",
  "recording_id": "<string>"
}
Path Parameters
​
recording_id
stringrequired
Response
200 - application/json
Recording deleted

​
message
string
​
recording_id
string

---

Recordings
Get recording metadata
Get recording metadata

curl --request GET \
  --url http://localhost:9511/api/recordings/{recording_id}/metadata

200
{
  "transaction_id": "3c90c3cc-0d44-4b50-8888-8dd25736052a",
  "duration_ms": 123,
  "start_time": "2023-11-07T05:31:56Z",
  "user_frames": 123,
  "agent_frames": 123
}
Path Parameters
​
recording_id
stringrequired
Response
200 - application/json
Recording metadata

​
transaction_id
string<uuid>
​
duration_ms
integer
​
start_time
string<date-time>
​
user_frames
integer
​
agent_frames
integer


---

Recordings
Download role audio
Download role audio

curl --request GET \
  --url http://localhost:9511/api/recordings/{recording_id}/audio/{role}

200
"<string>"
Path Parameters
​
recording_id
stringrequired
​
role
enum<string>required
Available options: user, agent 
Response
200 - application/octet-stream
Raw mono PCM audio

The response is of type file.

---

Recordings
Download interleaved stereo audio
Download interleaved stereo audio

curl --request GET \
  --url http://localhost:9511/api/recordings/{recording_id}/audio/interleaved

200
"<string>"
Path Parameters
​
recording_id
stringrequired
Response
200 - application/octet-stream
Raw interleaved stereo PCM audio (16kHz, 16-bit)

The response is of type file.

---

CDR
Receive CDR webhook
Receive CDR webhook

curl --request POST \
  --url http://localhost:9511/cdr-webhook \
  --header 'Content-Type: application/json' \
  --data '
{
  "cdr": {
    "transaction_id": "<string>",
    "thread_id": "<string>",
    "agent_id": "<string>",
    "environment_id": "<string>",
    "call": {
      "start_timestamp": "2023-11-07T05:31:56Z",
      "end_reason": "<string>",
      "milliseconds_elapsed": 123
    },
    "turns": [
      {}
    ],
    "failure_occurred": true,
    "system_error": true
  },
  "message": "<string>"
}
'

200
{
  "status": "<string>",
  "id": "<string>"
}
Body
application/json
​
cdr
object
Show child attributes

​
message
string
Response
200 - application/json
Webhook processed

​
status
string
​
id
string

---

CDR
Receive CDR webhook
Receive CDR webhook

curl --request POST \
  --url http://localhost:9511/cdr-webhook \
  --header 'Content-Type: application/json' \
  --data '
{
  "cdr": {
    "transaction_id": "<string>",
    "thread_id": "<string>",
    "agent_id": "<string>",
    "environment_id": "<string>",
    "call": {
      "start_timestamp": "2023-11-07T05:31:56Z",
      "end_reason": "<string>",
      "milliseconds_elapsed": 123
    },
    "turns": [
      {}
    ],
    "failure_occurred": true,
    "system_error": true
  },
  "message": "<string>"
}
'

200
{
  "status": "<string>",
  "id": "<string>"
}
Body
application/json
​
cdr
object
Hide child attributes

​
cdr.transaction_id
string
​
cdr.thread_id
string
​
cdr.agent_id
string
​
cdr.environment_id
string
​
cdr.call
object
Show child attributes

​
cdr.turns
object[]
​
cdr.failure_occurred
boolean
​
cdr.system_error
boolean
​
message
string
Response
200 - application/json
Webhook processed

​
status
string
​
id
string
--

CDR
List CDR reports
List CDR reports

curl --request GET \
  --url http://localhost:9511/api/cdr/reports

200
[
  {
    "id": "<string>",
    "received_at": "2023-11-07T05:31:56Z",
    "transaction_id": "<string>",
    "agent_id": "<string>",
    "environment_id": "<string>",
    "end_reason": "<string>",
    "milliseconds_elapsed": 123,
    "turn_count": 123,
    "failure_occurred": true,
    "system_error": true,
    "message": "<string>"
  }
]
Response
200 - application/json
CDR report summaries

​
id
string
​
received_at
string<date-time>
​
transaction_id
string
​
agent_id
string
​
environment_id
string
​
end_reason
string
​
milliseconds_elapsed
integer
​
turn_count
integer
​
failure_occurred
boolean
​
system_error
boolean
​
message
string

---

CDR
Clear CDR reports
Clear CDR reports

curl --request DELETE \
  --url http://localhost:9511/api/cdr/reports

200
{
  "status": "<string>"
}
Response
200 - application/json
Reports cleared

​
status
string

---

Reference
Browser UI Tabs
​
1. Talk to your Agent
Configure connection settings (Agent ID, Environment ID, Access Token)
Start/stop voice conversations
Use DTMF keypad for touch-tone input
View connection status in real-time
​
2. Connection Settings
Agent ID configuration
Environment ID configuration
Access Token authentication
Thread ID (optional for conversation continuity)
WebSocket URL (defaults to current host)
​
3. Call Recordings
Browse all available recordings
View recording metadata (duration, timestamps, frame counts)
Play back user audio, agent audio, or combined audio
Delete recordings
Recording server URL display for configuration
​
4. CDR Logs
Real-time CDR report monitoring
Statistics dashboard (total, successful, failed, last received)
Detailed report viewer with full JSON payload
Search by transaction ID or thread ID
Clear all reports
CDR webhook URL display for configuration

---

Reference
Storage
​
Recordings
Recordings are stored in the ./tmp/ directory (relative to the application directory). Each recording creates a subdirectory containing:
user.raw - User audio stream
agent.raw - Agent audio stream
interleave.raw - Combined stereo audio
metadata.json - Recording metadata
Note:
In IBM Code Engine, the filesystem is ephemeral. For persistent storage, integrate with IBM Cloud Object Storage or another durable storage solution.
​
CDR Reports
CDR reports are stored in-memory and will be lost when the application restarts. For persistent CDR storage, integrate with a database or external logging service.


---

Reference
Audio Format Specifications
​
Individual Streams (user.raw, agent.raw)
Encoding: PCM signed 16-bit little-endian (pcm_s16le)
Sample Rate: 16000 Hz (16 kHz)
Channels: Mono (1 channel)
Bit Depth: 16-bit
​
Interleaved Stream (interleave.raw)
Encoding: PCM signed 16-bit little-endian (pcm_s16le)
Sample Rate: 16000 Hz (16 kHz)
Channels: Stereo (2 channels)
Channel Layout: Both channels contain the same mixed audio (user + agent)
Bit Depth: 16-bit
​
Converting Recordings to WAV
Use FFmpeg to convert raw PCM files to WAV format:
BASH
# Convert user audio
ffmpeg -f s16le -ar 16000 -ac 1 -i user.raw user.wav

# Convert agent audio
ffmpeg -f s16le -ar 16000 -ac 1 -i agent.raw agent.wav

# Convert interleaved audio
ffmpeg -f s16le -ar 16000 -ac 2 -i interleave.raw interleave.wav


---

Voice Runtime Browser Test Application
Troubleshooting
​
Cannot Connect to Voice Runtime
Verify the WebSocket URL is correct
Check that the voice runtime is running and accessible
Ensure the access token is valid
Check browser console for connection errors
Verify network connectivity and firewall rules
​
Recording Not Working
Confirm the agent has voice webhooks configured
Confirm that the CONNECTION_MANAGER_URL is configured
Check that the /record WebSocket endpoint is accessible
Review application logs for recording errors
​
CDR Reports Not Appearing
Verify the CDR webhook URL is configured in voice runtime
Check that the /cdr-webhook endpoint is accessible
Ensure the voice runtime is sending CDR webhooks
Review application logs for webhook errors
Try the refresh button to manually reload reports
​
Audio Playback Issues
Ensure your browser supports the Web Audio API
Check that the recording files exist in the ./tmp/ directory
Verify the audio format is correct (16kHz, 16-bit PCM)
Try converting to WAV format using FFmpeg
​
DTMF Not Working
Verify the voice runtime supports DTMF messages
Check that the WebSocket connection is active
Ensure the voice agent is configured to handle DTMF input
Review browser console for DTMF send errors


---

Performance Guide
watsonx Orchestrate Performance Guide
Comprehensive guide to understanding, measuring, and optimizing performance in watsonx Orchestrate agents, flows, and tools

Version 2.0
Last Updated: 2026-04-10
IMPORTANT NOTICE ABOUT PERFORMANCE NUMBERS
This guide focuses on helping you understand how to measure and optimize performance in your wxO solutions. Performance will vary significantly based on your specific workload, configuration, system load, and other factors. Always measure performance in your own environment. The guidance provided helps you understand relative differences between approaches and identify optimization opportunities.
IMPORTANT: Large-Scale Performance Load Testing & Deployment Planning
While wxO is designed to scale elastically, we maintain optimal utilization ratios to operate the system effectively. If you plan to conduct large-scale performance load testing, please notify wxO support at least one week in advance. This allows us to:
Ensure the system is properly prepared for your test
Monitor system behavior together with you during the test
Provide guidance and support throughout the testing process
For successful large-scale deployments, please share with IBM your:
Intended rollout schedule
Expected user growth projections
Anticipated usage patterns
This enables us to proactively monitor the system and ensure optimal performance as your deployment scales.
Contact IBM Support to coordinate your performance testing activities and deployment planning.
​
About This Guide
This is the restructured version of the wxO Performance Guide, organized by the correct architecture hierarchy:
Agents (highest level) - Orchestrate and reason
Flow (wxO Agentic Workflow) - Sequences Agents, Tools, and People
Tools (execution level) - Flow, Python, Langflow, API, MCP, and Knowledge Tools.
​
Document Structure
This guide is organized into modular sections for easier maintenance and updates:
Introduction and Overview (this document)
Understanding Performance Testing (this document)
Agent Performance - Dedicated document
Flow Performance - Dedicated document
Tool Performance - Dedicated document
Knowledge Performance - Dedicated document
Accessing Performance Data (this document)
Quick Reference (this document)
​
Introduction and Overview
​
Purpose of This Guide
This guide helps you understand, measure, and optimize the performance of your agents, flows, and tools in watsonx Orchestrate (wxO). Whether you’re building approval workflows, data processing pipelines, or interactive agents, understanding performance characteristics at each level is essential for delivering excellent user experiences.
​
Balancing Performance with Quality
⚖️ Speed is Not Everything
In agentic solutions, optimal performance is about finding the right balance between:
Response Time: How quickly the system responds
Information Relevancy: How well the response addresses the user’s needs
Accuracy: How correct and reliable the information is
Engagement Experience: How natural and helpful the interaction feels
A faster response that provides irrelevant or inaccurate information creates a poor user experience. Similarly, a highly accurate response that takes too long may frustrate users. This guide helps you optimize response time while maintaining the quality and accuracy that users expect from agentic solutions.
​
Who Should Use This Guide
This guide is designed for:
Developers building agents, flows, and tools
Architects designing wxO solutions
Technical leads responsible for performance and SLAs
DevOps engineers monitoring production systems
​
Understanding the wxO Architecture
wxO follows a hierarchical architecture where each level has distinct performance characteristics:
wxO Architecture
Key Concepts:
Agents are the highest level - they orchestrate workflows and make decisions by using tools
Agents can call other Agents: An agent can use another agent as a tool, which in turn can call other agents and tools, creating nested agent hierarchies
Tools are the execution layer that agents can use:
Flow (wxO Agentic Workflow): A stateful workflow tool that support long running tasks and can deterministically sequence Agents, Tools, and People
Python Tools: Custom Python functions
Langflow Tools: Langflow-based flows
API Tools: External service integrations
MCP Tools: Model Context Protocol tools
Knowledge Tools: Knowledge base and retrieval tools
Flow is a Tool: Flow is a special type of tool that provides orchestration capabilities
Performance at each level affects the others - e.g., slow tools make flows slow, slow flows make agents slow, and nested agent calls compound performance impacts
​
What You Can Control and Measure
As a wxO SaaS customer, you have control over application-level performance:
✅ What You Control:
Agent configuration and prompts
Flow design and structure
Tool implementation and efficiency
Data mapping strategies
User interaction design
External API integrations
✅ What You Can Measure:
Agent response time and quality
Flow execution time and breakdown
Tool execution times
Task-level performance
LLM interaction duration
Error rates and success metrics
User response times
🔒 What IBM Manages:
Infrastructure scaling and availability
Platform-level performance
Orchestration engine optimization
Database performance
Network infrastructure
​
Shared Responsibility Model
In wxO SaaS, performance optimization is a shared responsibility:
Responsibility	You (Customer)	IBM (Platform)
Agent prompt engineering	✅	
Flow design efficiency	✅	
Tool code optimization	✅	
Data mapping strategy	✅	
External API performance	✅	
Orchestration engine		✅
Infrastructure scaling		✅
Platform availability		✅
Database optimization		✅
​
When to Conduct Performance Testing
Consider performance testing when:
Before deployment: Establish baselines and validate SLAs
After major changes: Verify performance impact of new features
During optimization: Measure improvement from changes
Investigating issues: Diagnose slow or failing agents/flows/tools
Capacity planning: Understand limits and scaling needs
Significant time has elapsed since last baseline: Re-establish an accurate baseline for comparisons
​
How to Use This Guide
For Understanding Performance:
Start with the architecture overview (above)
Read the relevant section for what you’re optimizing:
Agent Performance - If agents are slow or inaccurate
Flow Performance - If flows are slow or inefficient
Tool Performance - If tools are slow or timing out
Knowledge Performance - If knowledge retrieval is slow or returning poor results
For Optimization:
Identify the bottleneck level (agent, flow, or tool)
Read the relevant performance guide (agent, flow, or tool)
Apply level-specific optimizations from that guide
Measure improvement
For Troubleshooting:
Review the relevant performance guide (agent, flow, or tool)
Check the performance testing methodology
Follow the diagnosis and optimization steps
For Quick Reference:
Use the Quick Reference section below
Check performance baselines
Review optimization checklists
This guide focuses on SaaS deployments. Infrastructure is managed by IBM, so we emphasize application-level optimization that you control.
​
Understanding Performance Testing
​
Overview
Not all performance testing is the same. Choosing the right type of test helps you answer specific questions about your agents, flows, and tools. This section helps you identify which tests are most relevant for your needs.
CRITICAL: Simulating Realistic User Interactions
Understanding the Stateless Nature of LLM Inference
LLM inference is stateless - each request is independent. When testing agents, it’s crucial to understand how conversation history affects performance:
How Conversation History Works:
When a user asks an agent multiple questions in a session, each new question includes the entire conversation history
The LLM processes the full context (all previous Q&A pairs + the new question) for every interaction
As the conversation grows, both response time and token consumption increase cumulatively
Why This Matters for Performance Testing:
Artificially driving high load with unrealistic interaction patterns will produce misleading results
Testing with excessive interactions per session creates artificially large contexts that don’t reflect real usage
This leads to inflated response times and token consumption that won’t occur in production
Realistic Testing Parameters:
Interactions per Agent Session:
Recommended: 3-5 interactions per agent session
Why: Real users typically ask a few related questions before starting a new conversation
Adjust based on your use case: Analyze your actual user behavior patterns
Avoid: Long conversation chains (10+ interactions) unless your use case specifically requires them
Realistic Think Time:
Recommended: 10-30 seconds between interactions (depending on complexity)
Why: Real users need time to read, understand, and formulate follow-up questions
Example: If a user asks an agent for a list of doctors, they will take time to review the results before asking the next question
Avoid: Rapid-fire questions every 5 seconds - this doesn’t reflect real user behavior
Impact of Unrealistic Testing:
❌ Unrealistic: 20 interactions per session, 5s think time
   - Creates 20x context accumulation
   - Artificially slow response times
   - Inflated token costs
   - Does not represent production behavior

✅ Realistic: 3-5 interactions per session, 15-20s think time
   - Matches actual user behavior
   - Accurate performance metrics
   - Realistic token consumption
   - Valid basis for capacity planning
Best Practice: Before conducting performance tests, analyze your actual user interaction patterns (if available) or use industry-standard assumptions for your use case type. This ensures your test results are meaningful and actionable.
​
Tests Relevant for SaaS Customers
​
1. Baseline Testing
Purpose: Establish inherent performance characteristics under minimal load
When to Use:
Initial development and deployment
After significant code changes
Creating performance benchmarks
Comparing different implementation approaches
Configuration:
Users: 1-10 concurrent users
Duration: 15-30 minutes
Ramp-up: Immediate
Think Time: 10-30 seconds (realistic user behavior)
Interactions per Session: 3-5 interactions per agent session
What You’ll Learn:
Minimum execution time for your agent/flow/tool
Individual component performance
Baseline for comparison
Success Criteria:
- Components complete successfully
- Response times are consistent
- No errors or timeouts
- Metrics match expectations
Example Scenarios:
“I’ve built an agent with 3 tools. I want to know how fast it runs with a single user.”
“I’ve created a new Python tool. I want to measure its baseline execution time.”
“I’ve designed a flow with 5 tasks. I want to establish performance benchmarks.”
​
2. Load Testing
Purpose: Validate system behavior under expected production load
When to Use:
Before production deployment
Validating SLA compliance
Testing with realistic user volumes
Verifying concurrent execution handling
Configuration:
Users: Expected peak concurrent users
Duration: 30-60 minutes
Ramp-up: 10-15 minutes
Think Time: 10-30 seconds (realistic user behavior - adjust based on use case complexity)
Interactions per Session: 3-5 interactions per agent session
What You’ll Learn:
Performance under realistic load
Concurrent execution behavior
Error rates at scale
Whether you meet SLA requirements
Success Criteria:
- Meets SLA requirements (e.g., 95th percentile < target)
- Error rate < 1%
- No timeout failures
- Consistent performance across duration
Example Scenario:
“I expect 50 concurrent users during peak hours. I want to verify my agent can handle this load while maintaining acceptable response times.”
Important Considerations for SaaS:
IBM manages infrastructure scaling automatically
Focus on application-level performance
Contact IBM support if hitting platform limits
​
Test Case Selection Criteria
Choose test cases based on these criteria:
​
Transaction-Based Selection
Focus on high-frequency operations:
Search and query operations
Status checks and monitoring
Real-time data retrieval
Frequently accessed workflows
Example Test Cases:
✓ Document search flow
✓ Status query tools
✓ Notification processing
✓ Data synchronization flows
​
Business-Critical Operations
Focus on operations with business impact:
Revenue-generating workflows (payments, orders)
Customer-facing operations (support, onboarding)
SLA-bound processes (response time commitments)
Compliance-required operations (audit, security)
Example Test Cases:
✓ Purchase approval agents
✓ Customer onboarding flows
✓ Support ticket routing
✓ Contract generation
✓ Compliance reporting
​
Resource-Intensive Operations
Focus on operations that consume significant resources:
Complex agent interactions with multiple reasoning steps
Document processing and extraction
Large data transformations
Multiple external API calls
Long-running workflows
Example Test Cases:
✓ Document analysis agents
✓ Multi-step reasoning agents
✓ Batch data processing flows
✓ Complex approval chains
✓ Integration-heavy workflows
​
What About Stress and Endurance Testing?
Stress Testing (finding breaking points) and Endurance Testing (long-running stability) are not the responsibility of customers in wxO SaaS:
IBM conducts these tests as part of ongoing performance validation of the wxO platform
IBM manages infrastructure capacity and scaling
Platform automatically handles load distribution
Customer Focus:
Focus your efforts on application-level optimization (baseline and load testing)
If you suspect platform-level issues, contact IBM support to investigate infrastructure performance
​
Triggering Agents for Performance Testing
​
Overview
Before you can access performance data, you need to trigger your agents to generate test data. wxO provides two primary methods for executing agents:
​
Method 1: Chat UI
Best for: Interactive testing and manual validation
The wxO Chat UI provides a user-friendly interface for:
Testing agent responses interactively
Validating agent behavior with real conversations
Exploring different user inputs and scenarios
Access: Available through the wxO web interface
​
Method 2: Orchestrate Runs API
Best for: Baseline testing and load testing
The Orchestrate Runs API allows you to:
Execute agents programmatically
Automate performance testing
Run baseline tests (1-10 concurrent users)
Run load tests with multiple concurrent requests
Integrate agent testing into CI/CD pipelines
API Documentation: Orchestrate Runs API
​
Detailed Testing Guidance
For comprehensive information on agent testing methodology, test scenarios, and best practices, see:
Agent Performance Guide - Section: “How to Test Agent Performance”
​
Accessing Performance Data
​
Overview
wxO provides multiple methods for accessing performance data:
Built-in Monitoring UI - Visual interface for exploring traces
Programmatic API Access - Retrieve traces via REST API for automation
Trace CLI - Command-line interface for trace analysis (wxO ADK v2.4.0+)
All methods provide access to agent, flow, and tool performance data.
​
Method 1: Built-in Monitoring UI
Documentation: IBM watsonx Orchestrate - Monitoring Agents
​
Method 2: Programmatic API Access
There is no direct correlation between agent runs and trace IDs. To retrieve traces:
Execute your agent using the orchestrate runs API or other method
Search for traces using the searchTraces API by time range and agent ID to find the trace_id
Retrieve trace spans using the Get Spans for Trace API
​
Method 3: Trace CLI
Documentation: Traces with CLI
Available in: wxO ADK v2.4.0 and later
For detailed usage and examples, see the Trace CLI documentation.
​
Quick Reference
​
Performance Characteristics by Level
​
Agent Performance
What to Measure:
Total response time
Number of reasoning loops
Tool calls made
Success rate and accuracy
Optimization Focus:
Prompt engineering
Tool selection strategy
Context management
Model selection
​
Flow Performance
What to Measure:
Total execution time
Per-task execution time
Orchestration overhead
User interaction time
Optimization Focus:
Task count reduction
Data mapping strategy
Parallel execution
User interaction design
​
Tool Performance
Characteristics:
Python tools: Typically sub-second for simple operations
Langflow tools: Minimum 2+ seconds due to Langflow initialization
API tools: Varies based on external service
Knowledge tools: Varies based on repository type and search strategy
Timeout limit: 2 minutes maximum
What to Measure:
Individual tool execution time
External API latency
Knowledge retrieval time
Optimization Focus:
Algorithm efficiency
API call batching
Tool type selection
Knowledge search strategy
​
Common Pitfalls
Agent Level:
❌ Using Agents for simple text generation → ✅ Use Generative Prompts in Flow
❌ Too many tools available → ✅ Limit to relevant tools only
❌ Vague prompts → ✅ Use specific, clear prompts
❌ Ignoring accuracy metrics → ✅ Balance speed and quality
❌ Extensive guidelines → ✅ Keep guidelines concise and focused
❌ Inefficient pre/post plugins → ✅ Optimize plugin code for performance
Flow Level:
❌ Using auto-mapping for well-defined schemas → ✅ Use explicit data mapping for known, stable schemas (auto-mapping provides robust tool/agent response handling but adds latency)
❌ Too many small tasks → ✅ Combine related operations
❌ Not pre-filling forms → ✅ Use context to populate fields
❌ Sequential when parallel possible → ✅ Run independent tasks concurrently
Tool Level:
❌ Using Langflow for simple deterministic logic → ✅ Use Python tools or just code block in Flows
❌ Multiple sequential API calls → ✅ Batch into single call
❌ Trying to persist state → ✅ Use external state management
❌ Ignoring 2-minute timeout → ✅ Design for timeout constraints
​
Key Performance Factors
Agent Performance Factors:
Prompt complexity and clarity
Number of available tools
Reasoning loop iterations
LLM model selection
Context size
Guidelines (extensive guidelines can result in latency)
Flow Performance Factors:
Number of tasks
Data mapping strategy
Task dependencies
User interaction design
Agent context retrieval
Tool Performance Factors:
Tool type
Algorithm efficiency
External API latency
Data volume
Custom caching strategy (tool developers can implement caching in external services)
​
Resources and Links
Agent Performance: performance-guide-v2-agent
Flow Performance: performance-guide-v2-flow
Tool Performance: performance-guide-v2-tools
Knowledge Performance: performance-guide-v2-knowledge
Monitoring Documentation: https://www.ibm.com/docs/en/watsonx/watson-orchestrate/base?topic=agents-monitoring
Trace API Documentation: https://developer.ibm.com/apis/catalog/watsonorchestrate—custom-assistants/api/API—watsonorchestrate—observability-and-tracing#searchTraces
Evaluation Framework: https://developer.watson-orchestrate.ibm.com/evaluate/overview
IBM Support: Contact for platform-level issues
​
Next Steps
Understand your architecture: Review the hierarchy above
Identify your bottleneck: Agent, Flow, Tool, or Knowledge level?
Read the relevant guide:
Agent Performance
Flow Performance
Tool Performance
Knowledge Performance
Apply optimizations: Use strategies from the relevant performance guide
Monitor and iterate: Continuous improvement

---

Performance Guide
Agent Performance Guide
Understanding, measuring, and optimizing Agent performance in watsonx Orchestrate

Part of: watsonx Orchestrate Performance Guide
IMPORTANT NOTICE
This guide focuses on helping you understand how to measure and optimize agent performance in your wxO solutions. Performance will vary significantly based on your specific workload, configuration, and system load. Always measure performance in your own environment.
Note: “Flow” in this document refers to wxO Agentic Workflow
​
Agent Performance Overview
​
What is an Agent in wxO?
An agent in watsonx Orchestrate is an intelligent component that:
Reasons about problems and makes decisions
Orchestrates tools and flows to accomplish tasks
Interacts with users through natural language
Adapts its approach based on context and results
​
Agent Execution Model (ReAct Loop)
Agents use a ReAct (Reasoning and Acting) loop to solve problems:
ReAct Loop Steps:
Thought: Analyze the situation (LLM call)
Action: Select tool or provide answer (LLM call)
Observation: Execute tool and observe result
Repeat or Finish: Continue loop or provide answer
Key Characteristics:
Each loop iteration involves multiple LLM calls
Agents can call tools (Python, Langflow, APIs, Flows)
Agents can invoke other agents
Loop continues until agent determines task is complete
Performance Impact of Nested Agents
When an agent calls another agent, the nested agent also runs its own ReAct loop
Each nested agent adds its own reasoning overhead (LLM calls for thinking and action selection)
Deep agent hierarchies multiply LLM inference time exponentially
Example: Agent A → Agent B → Agent C means 3x the reasoning overhead
Recommendation: Limit agent nesting depth to 2-3 levels maximum for optimal performance
​
Agent Performance Components
Total agent response time consists of:
Total Agent Response Time =
  Guidelines Processing Time (if applicable) +
  Reasoning Loop Time +
  Tool Selection Time +
  Tool Execution Time +
  LLM Inference Time +
  Context Processing Time +
  Plugin Logic Time (if applicable)
What Affects Performance:
Guidelines processing: LLM call before agent loop to process guidelines (if configured)
Number of reasoning loops: More loops = longer response time
Tool selection complexity: More available tools = longer selection time
Tool execution time: Slow tools slow down the entire agent
LLM model size: Larger models are slower but more capable
Context size: Larger context = longer processing time
Prompt complexity: Complex prompts require more reasoning
Plugin logic: Custom plugin code execution (if using plugins)
​
How to Test Agent Performance
​
Testing Methodology
For comprehensive testing methodology, see the main Performance Guide which covers:
Baseline Testing: Establish performance benchmarks under minimal load
Load Testing: Validate behavior under expected production load
Stress Testing: Determine system breaking points (less relevant for SaaS)
​
Testing Agents via API
API Documentation: Orchestrate Runs API
How to Test:
Execute agent runs and retrieve run information using the Orchestrate Assistant Runs API
Get detailed traces using the searchTraces API and Get Spans for Trace API
For Agents that Use Flows:
User requests (human-in-the-loop interactions) must be obtained through the Messages API
This API retrieves messages from a thread, including user responses to flow requests
For Automated Testing:
Use the APIs programmatically to run multiple test queries
Collect performance metrics across runs
Calculate statistics (average, median, percentiles)
Compare performance across different agent configurations
​
Testing Agents via Channel-Specific Interfaces
Available Testing Channels:
Web chat UI
Voice interfaces
Slack
Other integrated channels
Recommended Testing Approach:
Test via API first - Ensure the agent works correctly through the API before running UI automation tests
Then test via channels - Once API testing is successful, validate the agent through channel-specific interfaces
Use appropriate tools - wxO has no specific tool recommendations; choose tools that fit your testing needs
Why Test API First
Isolates agent logic from channel-specific issues
Easier to debug and identify root causes
Faster test execution and iteration
Provides baseline performance metrics
Channel tests can then focus on UI/UX-specific concerns
​
Key Metrics to Track
​
Speed Metrics
Response Time

Reasoning Loops

Tool Calls

LLM Calls

​
Quality Metrics
Accuracy

Relevance

Completeness

Consistency

​
Cost Metrics
Token Usage:
Total tokens consumed per run
Directly impacts LLM costs
Track: Average tokens per query type
Tool Execution Costs:
External API calls and their costs
Track: API call count and associated costs
​
Agent Optimization Strategies
​
1. Choose the Right Approach
Different Agent Styles:
Use Case	Recommended Approach	Why
Simple text generation	Default Agent	Faster, simplier call
Straightforward Q&A	Default Agent	No reasoning loop needed
Complex reasoning	ReAct Agent	Needs multi-step thinking
Tool orchestration	ReAct Agent	Requires tool selection
Multi-step workflows	ReAct Agent	Benefits from reasoning loop
​
2. Optimize Prompts
Make Prompts Clear and Specific
❌ Vague: “Help the user”
✅ Clear: “Answer customer questions about order status using the order_lookup tool”
Provide Examples
Include few-shot examples in the prompt
Shows the agent the expected behavior
Reduces reasoning loops
Structure Output
Request structured responses (JSON, specific format)
Reduces generation time
Easier to parse
​
3. Optimize Guidelines
What are Guidelines: Agent Guidelines are instructions that help shape agent behavior.
Performance Impact
Guidelines trigger an LLM call before the agent loop starts
This adds latency to every agent invocation
The LLM processes guidelines to understand behavioral constraints
Optimization Strategies:
Keep guidelines concise: Shorter guidelines = faster processing
Use guidelines only when needed: Remove if not providing value
Test with and without: Measure impact on response time
Balance guidance vs speed: Guidelines improve quality but add latency
​
4. Limit Available Tools
Problem: Too many tools slow down tool selection
Solution:
Provide only relevant tools for the agent’s purpose
Group related tools
Use clear, descriptive tool names
Example:
❌ Agent with 25 generic tools
✅ Agent with 5-10 focused, relevant tools
​
4a. Avoid Deep Agent Hierarchies
Problem: Nested agents multiply LLM inference overhead
Why It Matters:
Each nested agent runs its own ReAct loop with multiple LLM calls
Deep hierarchies spend more time on reasoning than actual work
Agent A → Agent B → Agent C means 3x the reasoning overhead
LLM inference time compounds at each level
Solution:
Limit nesting depth to 2-3 levels maximum
Consider using Flows instead of nested agents for deterministic orchestration
Use tools (Python, API) for simple operations instead of wrapping them in agents
Flatten agent hierarchies where possible
Example:
❌ Agent → Agent → Agent → Agent (4 levels of reasoning overhead)
✅ Agent → Flow → Tools (reasoning only at top level, deterministic execution below)
✅ Agent → Agent → Tools (2 levels, acceptable for complex scenarios)
​
5. Choose Appropriate Model
Model Selection Trade-offs:
Model Size	Speed	Capability	Use Case
Small	Fastest	Basic	Simple queries, high volume
Medium	Moderate	Good	General purpose
Large	Slower	Best	Complex reasoning, high accuracy needs
Recommendation: Start with medium models, adjust based on accuracy requirements.
Note on Caching: Caching agent responses can be implemented through pre-agent plugins if needed for your use case.
​
Agent Quality and Evaluation
​
Why Quality Matters
Speed vs Quality Trade-off
Fast but inaccurate agents provide poor user experience
Slow but accurate agents frustrate users
Goal: Optimize for both speed AND quality
​
Agent Evaluation
Evaluation Framework: Quick Evaluation of Agents and Tools
What You Can Evaluate:
Agent accuracy on test queries
Response quality and relevance
Consistency across similar queries
Comparison between different agent configurations
Key Point: Always validate agent quality after making performance optimizations to ensure accuracy hasn’t degraded.
​
Best Practices Summary
​
Do’s
Measure before optimizing
Establish baseline performance
Identify actual bottlenecks
Track both speed and quality metrics
Use the right approach
Generative Prompts for simple tasks
Agents for complex reasoning
Don’t over-engineer
Optimize prompts
Clear, specific instructions
Include examples
Request structured output
Optimize guidelines
Keep guidelines concise
Use only when needed
Test impact on performance
Limit tool count
Provide only relevant tools
Use descriptive names
Group related functionality
Avoid deep agent hierarchies
Limit agent nesting to 2-3 levels maximum
Use Flows for deterministic orchestration
Use tools instead of agents for simple operations
Flatten hierarchies to reduce reasoning overhead
Optimize plugin logic
Write efficient plugin code
Cache plugin results when appropriate
Profile plugin performance
Validate quality
Use evaluation framework to validate accuracy
Ensure optimizations don’t degrade quality
Iterate based on real metrics
​
Don’ts
Common Pitfalls to Avoid
❌ Don’t provide too many tools
Slows down tool selection
Increases reasoning complexity
❌ Don’t use verbose guidelines
Adds unnecessary LLM processing time
Keep guidelines concise and focused
❌ Don’t create deep agent hierarchies
Each nested agent adds reasoning overhead
Multiplies LLM inference time exponentially
Limit nesting to 2-3 levels maximum
❌ Don’t ignore quality metrics
Speed without accuracy is useless
Always validate accuracy after optimization
❌ Don’t optimize without measuring
Measure first, optimize second
Track impact of each change
❌ Don’t write inefficient plugin logic
Plugins run in agent execution path
Optimize plugin code for performance
​
Resources and Links
Main Performance Guide
Comprehensive performance guide overview
Flow Performance
Flow-specific performance optimization
Tool Performance
Tool execution performance guide
​
API References
Evaluation Framework
Monitoring Documentation

---

Performance Guide
Flow Performance Guide
Understanding, measuring, and optimizing Flow (wxO Agentic Workflow) performance in watsonx Orchestrate

Part of: watsonx Orchestrate Performance Guide
Performance Testing Approach
This guide focuses on how to measure and optimize Flow (wxO Agentic Workflow) performance. Performance varies significantly based on workload, configuration, system load, and network conditions. Always measure in your own environment.
Note: “Flow” refers to wxO Agentic Workflow
​
Overview
Flow (wxO Agentic Workflow) is a specialized orchestration tool in watsonx Orchestrate that sequences the execution of Agents, Tools, and People interactions. Understanding Flow’s performance characteristics helps you design efficient workflows and set appropriate expectations.
​
What is Flow?
Flow (wxO Agentic Workflow) orchestrates:
Agents: For reasoning and complex decision-making
Tools: Python tools, Langflow tools, and other execution units
People: User interactions, approvals, and forms
Data: Mapping and transformation between tasks
​
Key Characteristics
Stateful: Maintains context across tasks
Resumable: Can pause and resume execution
Auditable: Complete execution traces
Scalable: Auto-scales for concurrent executions
Observable: Rich monitoring and tracing
​
Flow as an Orchestration Tool
​
When to Use Flow
Use Flow When:
Orchestrating multiple tools in sequence or in parallel
Coordinating agents with tools and people
Managing complex, multi-step workflows
Requiring state persistence and resumability
Handling user interactions and approvals
Consider Alternatives When:
Single tool execution is sufficient
Agent can handle the task independently
​
Flow Performance Characteristics
​
Key Performance Insights
Flow performance consists of several components:
Orchestration Overhead: Minimal and predictable (< 100ms)
Initialization time is very fast
Per-task transition overhead is consistent
Scales linearly with task count
Represents a small fraction of total execution time
Task Execution Time: Dominates total duration
Simple operations: Very fast
Complex computations: Moderate to slow
External API calls: Variable based on network and service
LLM interactions: Moderate to slow depending on complexity
Data Mapping: Negligible with explicit mapping
Explicit mapping (default): Extremely fast
Auto-mapping with LLM: Slower but flexible
Context compression: Automatic when needed, adds latency, applicable for flows with large context
User Interactions: Highly variable
Can range from seconds to hours
Often dominates total flow duration
Optimization focuses on user experience
​
Flow Execution Time Components
Total flow execution time consists of multiple independent components:
Total Flow Duration =
  Flow Orchestration Overhead +
  Tool & Agent Execution Time +
  User Activity Wait Time +
  Data Mapping Time +
  Agent Context Retrieval Time
​
1. Flow Orchestration Overhead
This is the fixed cost of flow execution, independent of task complexity.
Components:
Initialization: Flow context setup, variable initialization, first task preparation
Inter-task Coordination: Result processing, context updates, next task preparation
Completion: Result aggregation, cleanup, response formatting
Characteristics:
Minimal and predictable
Scales linearly with task count
Represents small fraction of total time for most flows
Negligible compared to actual work time
​
2. Tool & Agent Execution Time
This is the actual work time and varies significantly based on:
Tool Complexity:
Simple string operations: Very fast
Complex computations: Moderate to slow
External API calls: Variable (network and service dependent)
Agent Interactions:
Simple agent tasks: Moderate (includes LLM overhead)
Complex reasoning: Slower (multiple LLM calls)
Multiple tool uses: Slowest (iterative problem-solving)
​
Performance Considerations for Large Data
Document Handling:
Binary documents via API: When sending large documents as binary-encoded data, Flow stores them in S3 first, adding storage overhead
Document references: Flow optimizes by passing document references rather than full content
Recommendation: For large documents, use document references or pre-upload to storage when possible
Large Content from Tools/Agents:
Large responses: Tools/agents returning large content can impact performance
Processing overhead: Flow must process, store, and potentially pass large data between tasks
Context compression: May trigger automatic context compression
Recommendation: Design tools to return summaries or references rather than full content
​
LLM-Based Features in Flows
Flows can leverage LLMs through multiple features:
A. Generative Prompt (Direct LLM Call)
Performance: Faster than agent interactions
Use case: Direct text generation, transformation, or analysis
Characteristics: Single LLM inference call, no agent loop overhead
B. Document Processing Features (LLM-based)
Performance: Moderate to slow (depends on document complexity)
Use case: Document extraction, text extraction, document classification
Characteristics: LLM-based analysis, duration varies with document complexity
C. Agent Interactions (with ReAct Loop)
Performance: Slower due to reasoning loop
Use case: Complex reasoning, tool use, multi-step problem solving
Characteristics: Multiple LLM calls, iterative problem-solving, higher latency but more capable
Recommendation: Use Generative Prompts for straightforward LLM tasks to minimize latency; use document processing features when analyzing documents; use Agents when reasoning and tool orchestration are needed.
​
3. User Activity Wait Time
When flows include user interactions (forms, approvals, confirmations):
Immediate response: Very fast (user reading and clicking)
Typical response: Moderate (user reviewing and deciding)
Delayed response: Slow (user away from keyboard)
Impact: Can dominate total flow duration, making orchestration overhead negligible.
Key Insight: Flow’s minimal initialization overhead means user-facing interactions can be surfaced almost immediately after flow start, providing excellent responsiveness for interactive workflows.
​
4. Data Mapping Time
Data mapping between task outputs and inputs:
Explicit mapping: Extremely fast (direct field assignments, recommended when latency is a concern)
Auto-mapping with LLM: Slower but make programming Flow very simple (requires LLM inference for schema transformation)
Context compression: Slower (automatic LLM-based summarization when needed)
When it occurs:
Every task transition (explicit mapping is default and fast)
Auto-mapping only when explicitly configured for complex transformations
Context compression automatically triggered when flow context exceeds token threshold
​
5. Agent Context Retrieval Time
Agent conversation history retrieval at flow start:
Default retrieval: Moderate (fetches last N conversation turns)
Bypassed: No overhead (when conditions below are met)
When it’s bypassed (no overhead):
Flow invoked via API endpoint
Flow invoked via MCP (Model Context Protocol)
Configuration set to 0 turns
Flow not associated with an agent conversation
Optimization Strategies:
Minimize Task Count: Combine related operations, batch processing, use parallel execution when possible
Optimize Tool Logic: Efficient algorithms, minimize I/O, cache results, batch operations
Choose Data Mapping Strategy:
Explicit mapping (fast): For production and time-sensitive flows
Auto-mapping (slower): For development and dynamic schemas
Migrate from auto-mapping to explicit mapping as flows mature
Optimize Agent Context: Set appropriate turn limits, use 0 for stateless flows, invoke via API/MCP to bypass retrieval
Optimize LLM Interactions: Use Generative Prompts for simple tasks, Agents only when reasoning needed
Optimize User Interactions: Pre-fill forms, provide defaults, clear instructions
​
Flow Optimization Strategies
Minimize Task Count
Combine related operations, batch processing, use parallel execution when possible
Optimize Tool Logic
Efficient algorithms, minimize I/O, cache results, batch operations
Choose Data Mapping Strategy
Use explicit mapping for production, auto-mapping for development
Optimize Agent Context
Set appropriate turn limits, use 0 for stateless flows
​
Measuring Flow Performance
​
How to Measure Flow Performance
Flow Inspector (Visual)
APIs (Programmatic)
Use the Flow Inspector to visually inspect flow execution and timing data:
View execution history and traces
See timing data for each task
Analyze flow performance visually
Identify bottlenecks in the workflowFlow Inspector
​
Performance Analysis Tips
1
Run multiple iterations

At least 3-5 runs for consistency
2
Consider cold vs warm starts

First run may include initialization
3
Monitor system resources

CPU, memory, network can affect results
4
Test under load

Performance may degrade with concurrent flows
5
Isolate components

Compare task durations to identify bottlenecks
​
Summary
Key Points

Optimization Priority

​
Related Guides
Main Performance Guide
Comprehensive performance guide overview
Agent Performance Guide
Agent-specific performance optimization
Tool Performance Guide
Tool execution performance guide
​
API References
Flow API

---

Performance Guide
Tool Performance Guide
Understanding, measuring, and optimizing Tool performance in watsonx Orchestrate

Part of: watsonx Orchestrate Performance Guide
Performance Testing Approach
This guide focuses on how to measure and optimize Tool performance. Performance varies significantly based on workload, configuration, system load, and network conditions. Always measure in your own environment.
Note: “Flow” in this document refers to wxO Agentic Workflow
​
Overview
Tools are executable units in watsonx Orchestrate that perform specific tasks (API calls, data processing, calculations) within isolated, secure environments. They are invoked by Agents or orchestrated by Flows.
​
Tool Types in wxO
​
Choosing the Right Tool Type
wxO Flow (first choice): Native support for connections/security, Python code snippets, orchestration of wxO agents, tools and people (e.g. confirmation before transaction, custom forms), built-in document extraction and processing, LLM support.
Python Tools: For custom libraries not in wxO Flow code blocks
Langflow Tools: For Langflow-specific AI components or existing langflow flows
​
Tool Type Comparison
Tool Type	Runtime/Base	Timeout	Key Features	Best For
wxO Flow	Visual workflow	None	Stateful, resumable, orchestrates Agents/Tools/People, LLM support	Multi-step workflows, API integrations, human-in-loop, simple document processing
Python	Python 3.12	2 min	Stateless, read-only FS, outbound network only	Data processing, business logic, calculations
Langflow	Langflow 1.10.0	2 min	Stateless, read-only FS, outbound network only, 2+ sec initialization	LLM processing, RAG, complex document analysis
API	OpenAPI spec	2 min (sync) / None (async)	External REST APIs, network-dependent	Third-party integrations, external services
MCP	MCP protocol	2 min	Extended capabilities, varies by implementation	Custom integrations, protocol-based interactions
​
Understanding Tool Performance
​
The Granularity Principle
Key Insight: Tool performance has two distinct components:
Tool Call Overhead: The cost of invoking a tool
Includes initialization, context setup, and result handling
Exists for every tool invocation
Relatively consistent per tool type
Execution Inside the Tool: The actual work being done
Runs fast once inside the tool
Varies based on the logic and operations
Where optimization efforts should focus
Implication:
Multiple small tool calls = Multiple overhead costs
Single larger tool call = One overhead cost, fast internal execution
Recommendation: Combine related operations into single tools when possible
​
Performance Characteristics by Tool Type
Python Tools:
Call overhead: Present but minimal
Internal execution: Very fast for most operations
Overall: Fast to very fast
Best for: Deterministic logic, data processing, API calls
Langflow Tools:
Call overhead: Includes Langflow initialization (2+ seconds due to initialization)
Internal execution: Depends on LLM operations
Overall: Slower due to LLM inference (if using LLM)
Best for: LLM reasoning, NLP tasks, document analysis
​
Python & Langflow Tool Performance
​
Shared Technical Constraints
Both Python and Langflow tools operate in secure sandboxes with identical constraints:
Constraint	Impact	Best Practice
Isolated pod execution	Each tool instance runs in a separate pod for tenant isolation and security	Design for stateless, independent execution
2 CPU cores maximum	Limited computational resources per tool instance	Optimize algorithms and avoid CPU-intensive operations
2GB memory maximum	Limited memory per tool instance	Manage memory efficiently, avoid large data structures
2-minute timeout	Maximum execution time per call	Design for timeout awareness, break long operations into chunks
No GPU access	GPU operations will fail	Use CPU-optimized algorithms and libraries only
Cold start penalty	First run takes longer; subsequent runs within 72 hours are faster	Expect initial latency; warm pods improve performance
Stateless execution	No state persists between calls	Use external storage (Redis, S3, database)
Read-only filesystem	Cannot write files locally	Use in-memory buffers or external storage
Network isolation	Outbound requests only	Design for outbound-only patterns
Security Note: Due to tenant isolation requirements and the potentially unsecured nature of user-authored code, wxO runs each Python and Langflow tool instance as a separate pod with strict resource limits. This ensures security and prevents resource contention between tenants.
Performance Note: Tool pods experience cold start latency on first invocation. Once warmed up, the pod remains available for approximately 6 hours, with the time extended upon continuous use of the tool. This provides faster execution for subsequent calls. Plan for initial latency in performance testing and user experience design.
​
Python Tools
Execution Speed: Very fast (simple operations), fast (data processing), variable (external API calls)
Optimization Strategies:
Minimize and batch external API calls
Use efficient algorithms (O(n) vs O(n²))
Choose performant libraries
Implement external caching (Redis) for expensive operations
​
Overview
Tool builders in IBM watsonx Orchestrate can build their tools by using Python and deploy them as toolkits on the platform. The platform now provides a toolkit runtime architecture that offers significant improvements over the individual tool import architecture. This document provides guidelines for designing, developing, and deploying Python tools for watsonx Orchestrate.
Key changes in Python toolkits
New toolkit runtime: Overcomes individual tool processing overheads.
Improved performance: Improves resource utilization and reduces cold start latency.
​
New toolkit runtime architecture
Architecture overview
Both individual Python tools and Python toolkits run in isolated containers, but with fundamentally different execution models:
Individual Python tool approach:
Each tool has its own requirements.txt with specific dependencies
Process-level isolation: Each tool invocation creates a new process, albeit a lightweight one.
Thread-safety: Tools need not be thread-safe.
Performance overhead: Creates a lightweight process for each execution and a virtual environment for tools that are not yet loaded in the worker.
Resource allocation: 2 vCPU and 2 GB RAM per replica (2 replicas provided)
Cold-start delays: Significant latency from process creation and dependency loading.
Python toolkit runtime approach:
Multiple related tools packaged together in a single toolkit.
Single shared requirements.txt for all tools in the toolkit.
Thread-level isolation: Tools run in persistent worker threads.
Preinstalled dependencies: All dependencies are loaded once at container startup.
Thread-safety required: All tools must be thread-safe and reentrant.
High performance: No process creation or dependency loading overhead.
Resource allocation: 2 vCPU and 2 GiB RAM per replica (2 replicas provided).
FastAPI/Gunicorn workers: 5 persistent workers per replica handle concurrent requests.
Deployment architecture
Each toolkit deployment consists of:
Kubernetes deployment: 2 replicas
Per-Replica resources:
2 vCPU cores
2 GiB memory
5 FastAPI/Gunicorn workers per replica
Load balancing: Automatic distribution across replicas and workers
Health monitoring: Built-in health checks and automatic recovery
Benefits of toolkit approach
Higher performance:
No process creation overhead per execution.
No dynamic dependency loading.
Persistent workers eliminate cold start delays.
Thread-based execution is orders of magnitude faster than process-based.
Shared dependencies:
Single requirements.txt for all tools in the toolkit
Dependencies loaded once at container startup
Reduced memory footprint through shared libraries
Better resource utilization:
Multiple tools share container resources
Efficient thread-based concurrency
Lower per-request overhead
Improved scalability:
Each replica handles multiple concurrent requests through workers
Better throughput per unit of compute
Enhanced reliability:
Built-in health checks and automatic failover
Persistent workers reduce failure points
No dependency loading failures during execution
Cost efficiency:
More tools per unit of compute resource
Reduced infrastructure overhead
Better resource density
Thread safety requirements
Critical: All tools in a toolkit must be thread-safe because:
Multiple worker threads run tools concurrently
No process-level isolation between tool invocations
Shared memory space within the container
Thread-safe practices:
PYTHON
# ✅ CORRECT: Thread-safe tool (no shared mutable state)
@tool
def thread_safe_tool(user_id: str) -> Dict:
    """Each invocation uses local variables only"""
    response = requests.get(f"https://api.example.com/users/{user_id}")
    return response.json()

# ❌ INCORRECT: Not thread-safe (shared mutable state)
_cache = {}  # Shared across all threads!

@tool
def not_thread_safe(key: str) -> str:
    """Dangerous: modifying shared state without locks"""
    if key not in _cache:
        _cache[key] = fetch_data(key)  # Race condition!
    return _cache[key]

See all 17 lines
A toolkit in draft is run by using the Python tool approach to cover a large number of tools and toolkits that might be present in a tenant in the draft environment.
Toolkits in live run with thread safety and a separate deployment per toolkit.
​
Resource allocation and performance requirements
CPU computation limits
Critical requirement: Python tools must limit CPU-bound computation to approximately 50 milliseconds to ensure performance scaling.
This constraint helps ensure:
Fair resource sharing across concurrent requests
Predictable response times
Prevention of worker starvation
What counts as CPU time
CPU time includes:
Data parsing and transformation logic
JSON serialization/deserialization
String manipulation and formatting
Mathematical computations
In-memory data filtering and sorting
Object instantiation and manipulation
CPU time does not include:
Network I/O wait time (HTTP requests, database queries)
File I/O wait time
Sleep/delay operations
External API call latency
Memory constraints
Each replica has 2 GiB of memory that is shared across 5 workers:
Per-worker budget: ~400 MB (accounting for overhead).
Tool memory usage: Cannot not exceed 100-200 MB per concurrent request.
Memory leaks: Avoid memory leaks to prevent pod crashes.
Throttling: Implement request throttling if memory usage approaches limits.
​
Python tool design principles
1. Tools as API wrappers
Python tools must be lightweight wrappers around existing API implementations:
PYTHON
from ibm_watsonx_orchestrate.agent_builder.tools import tool
import requests
from typing import Dict, List

@tool
def get_customer_orders(customer_id: str) -> Dict:
    """
    Fetch customer orders from multiple services and format the response.
    
    This tool demonstrates the correct pattern:
    - Heavy lifting done by external APIs
    - Minimal CPU time for response formatting
    """
    session = requests.Session()

    # API call 1: Get customer profile
    profile = session.get(
        f"https://api.example.com/customers/{customer_id}"
    ).json()
    
    # API call 2: Get order history
    orders = session.get(
        f"https://api.example.com/orders?customer_id={customer_id}"
    ).json()
    
    # API call 3: Get loyalty points
    loyalty = session.get(
        f"https://api.example.com/loyalty/{customer_id}"
    ).json()
    
    # API call 4: Get recommendations
    recommendations = session.get(
        f"https://api.example.com/recommendations/{customer_id}"
    ).json()
    
    # CPU work: Format and combine responses (~10-20ms)
    return {
        "customer_name": profile.get("name"),
        "email": profile.get("email"),
        "total_orders": len(orders.get("items", [])),
        "recent_orders": orders.get("items", [])[:5],
        "loyalty_points": loyalty.get("points", 0),
        "tier": loyalty.get("tier", "standard"),
        "recommended_products": [
            {
                "id": rec["product_id"],
                "name": rec["product_name"],
                "score": rec["relevance_score"]
            }
            for rec in recommendations.get("items", [])[:3]
        ]
    }
See all 52 lines
2. Response formatting guidelines
Keep CPU-intensive formatting minimal (target: 10-50ms):
PYTHON
# ✅ CORRECT: Minimal formatting
@tool
def process_api_response(data: dict) -> dict:
    """Simple field extraction and renaming"""
    return {
        "id": data.get("customer_id"),
        "name": data.get("full_name"),
        "status": data.get("account_status", "active")
    }

# ⚠️ CAUTION: More complex but still acceptable
@tool
def aggregate_metrics(data: List[dict]) -> dict:
    """Light aggregation - keep under 50ms"""
    total = sum(item.get("value", 0) for item in data)
    avg = total / len(data) if data else 0
    return {
        "total": total,
        "average": avg,
        "count": len(data)
    }

# ❌ INCORRECT: Heavy computation
@tool
def complex_analysis(data: List[dict]) -> dict:
    """This will exceed 50ms CPU time"""
    # Heavy statistical analysis
    # Machine learning inference
    # Complex data transformations
    # These should be done by external APIs!
    pass
See all 31 lines
​
Performance analysis and capacity planning
Example scenario: high-throughput tool
The following example shows a tool that makes 4 sequential API calls:
Tool characteristics:
CPU time per request: 50 ms (formatting/parsing)
API call latency: 15 seconds each (4 sequential calls)
Total wall-clock time: ~60 seconds (sequential execution)
Deployment configuration:
2 Kubernetes replicas
2 vCPU per replica
5 workers per replica
Total workers: 10 (2 replicas × 5 workers)
Throughput calculation
CPU capacity & practical throughput:
Total vCPUs: 4 (2 replicas × 2 vCPU)
CPU time per request: 50 ms = 0.05 seconds
Typical CPU-based throughput: 50 requests/second
​
When to use platform-hosted Python toolkits
Platform-hosted Python toolkits are good for:
✅ Suitable use cases
API orchestration tools
Calling 2-5 external APIs and combining results
Response formatting and field mapping
Simple data aggregation from multiple sources
Data transformation tools
JSON/XML format conversions
Field extraction and renaming
Simple filtering and sorting
Data validation and sanitization
Integration wrappers
Wrapping REST APIs with simplified interfaces
Authentication token management
Request/response normalization
Lightweight processing
Text formatting and templating
Date/time conversions
Unit conversions
Simple calculations (< 50 ms CPU)
Requirements checklist
Use platform-hosted toolkits when ALL of the following are true:
CPU computation ≤ 50 ms per request
Memory usage is less than 200 MB per request
Heavy processing is delegated to external APIs
Response time is acceptable at 5-30 seconds
The tool is stateless or uses platform context management
No special runtime dependencies (such as custom C libraries)
​
When to use self-hosted solutions
Consider self-hosting tools through Remote MCP Servers or OpenAPI Tools when:
❌ Not suitable for platform toolkits
CPU-intensive operations
Complex statistical analysis
Cryptographic operations
Large-scale data transformations
High memory requirements
Loading large models (> 500 MB)
Processing large datasets in memory
Caching extensive reference data
In-memory databases
Special runtime requirements
Custom system libraries
Specific Python versions
Native code dependencies
Long-running operations
Batch processing jobs
Report generation (> 60 seconds)
Data migration tasks
Background processing
Stateful operations
Maintaining persistent connections
Session management
Transaction coordination
Workflow orchestration
Self-hosting options
Option 1: Remote MCP server
Best for: Custom tool collections with complex logic
Deployment: Your infrastructure
Protocol: Model Context Protocol over HTTP/SSE
Benefits: Full control, custom resources, flexible scaling
Option 2: OpenAPI tools
Best for: Existing REST APIs
Deployment: Your infrastructure or third-party services
Protocol: Standard HTTP/REST
Benefits: Use existing APIs, no code changes needed
Option 3: Hybrid approach
Platform toolkits for orchestration and formatting
Self-hosted services for heavy computation
Example: Platform tool calls your ML inference API
​
Best practices
1. Request batching and reuse
PYTHON
import requests
from typing import List, Dict

@tool
def batch_api_calls(ids: List[str]) -> List[Dict]:
    """Efficiently fetch data for multiple IDs using a shared session"""
    session = requests.Session()
    results = []
    for id in ids:
        response = session.get(f"https://api.example.com/items/{id}", timeout=30)
        results.append(response.json())
    return results
See all 12 lines
2. Error handling
PYTHON
import requests

@tool
def robust_api_call(endpoint: str) -> Dict:
    """Proper error handling for external API calls"""
    try:
        response = requests.get(endpoint, timeout=30.0)
        response.raise_for_status()
        return response.json()
    except requests.Timeout:
        return {"error": "API timeout", "status": "timeout"}
    except requests.HTTPError as e:
        return {"error": f"API error: {e.response.status_code}", "status": "error"}
    except Exception as e:
        return {"error": str(e), "status": "error"}
See all 15 lines
3. Connection pooling
PYTHON
import requests
from requests.adapters import HTTPAdapter
import threading

# Thread-local session for safe connection reuse per thread
_thread_local = threading.local()

def get_session() -> requests.Session:
    """Reuse HTTP session per thread"""
    if not hasattr(_thread_local, "session"):
        session = requests.Session()
        adapter = HTTPAdapter(pool_connections=10, pool_maxsize=20)
        session.mount("https://", adapter)
        _thread_local.session = session
    return _thread_local.session

@tool
def efficient_api_call(url: str) -> Dict:
    """Use connection pooling for better performance"""
    session = get_session()
    response = session.get(url, timeout=30)
    return response.json()
See all 22 lines
4. Memory management
PYTHON
import requests

@tool
def memory_efficient_processing(data_url: str) -> Dict:
    """Stream large responses instead of loading into memory"""
    total_size = 0
    with requests.get(data_url, stream=True, timeout=30) as response:
        for chunk in response.iter_content(chunk_size=8192):
            total_size += len(chunk)
            # Process chunk without loading entire response
    return {"processed_bytes": total_size}
See all 11 lines
5. Context management
PYTHON
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from ibm_watsonx_orchestrate.utils import update_context
from ibm_watsonx_orchestrate.run.context import AgentRun

@tool
def stateful_tool(user_input: str, context: AgentRun) -> str:
    """Use platform context for state management"""
    # Read previous state
    previous_step = context.request_context.get('workflow_step', 'start')
    
    # Perform operation
    result = process_step(user_input, previous_step)
    
    # Update context for next tool
    update_context('workflow_step', result['next_step'])
    update_context('last_result', result['data'])
    
    return result['message']
See all 18 lines
​
Migration from individual tools to toolkits
If you have existing individual tools, consider migrating to the toolkit approach:
Migration checklist
Group-related tools:
Identify tools that share similar dependencies
Group tools by functional domain or use case
Aim for 10-15 tools per toolkit for optimal resource utilization
Consolidate dependencies:
Merge all requirements.txt files into a single file
Resolve version conflicts between tools
Remove duplicate dependencies
Test compatibility of consolidated dependencies
Ensure thread safety:
Critical: Review all tools for thread-safety issues
Remove or protect shared mutable state
Use thread-safe data structures (queue.Queue, threading.Lock)
Avoid global variables that are modified during execution
Test tools under concurrent load
Review CPU usage:
Profile each tool to help ensure CPU time < 50 ms
Identify and optimize CPU-intensive operations
Consider moving heavy computation to external APIs
Test concurrency:
Load test with multiple concurrent requests
Verify no race conditions or deadlocks
Monitor memory usage under load
Validate thread-safety under stress
Package as toolkit:
Follow toolkit packaging format
Create single requirements.txt
Document thread-safety guarantees
Include toolkit metadata
​
Summary
The new toolkit runtime architecture provides a high-performance, scalable platform for Python tools that:
Eliminates cold start delays through persistent workers
Maximizes throughput through efficient resource sharing
Ensures predictability through strict CPU time limits
Key takeaway: Design tools as lightweight wrappers around external APIs. Keep CPU computation under 50 ms and let external services handle heavy processing. This approach enables high concurrency, predictable performance, and efficient resource utilization.
For tools that don’t fit these constraints, use self-hosted solutions through Remote MCP Servers or OpenAPI Tools to maintain full control over resources and runtime environment.
​
Langflow Tools
Execution Speed: Minimum 2+ seconds (initialization overhead per run), then variable depending on workflow complexity
Key Consideration: Due to the initialization overhead on every run, Langflow tools are most effective for operations that take longer to execute (but remain under the 2-minute timeout). The initialization penalty becomes less significant when the actual workflow processing time is substantial.
Note: LLM operations in Langflow are optional. Use Langflow when you need its specific AI components or have existing Langflow workflows, not solely for LLM capabilities.
Optimization Strategies:
Use for longer-running operations where initialization overhead is proportionally smaller
Minimize and combine LLM calls into single prompts (when using LLMs)
Use concise, focused prompts with minimal context (when using LLMs)
Choose smaller models for simple tasks, larger for complex reasoning (when using LLMs)
Cache expensive operation results externally (Redis) for repeated queries
​
API & MCP Tool Performance
​
API Tools (OpenAPI-based)
Performance: Depends entirely on external service (network latency, service speed, payload size, rate limiting, authentication)
Timeout:
Synchronous calls: 2 minutes (same as Python/Langflow/MCP)
Asynchronous calls: None (via OpenAPI callback syntax)
​
MCP Tools (Model Context Protocol)
Performance: Varies by implementation (tool design, external dependencies, protocol overhead, resource requirements)
Timeout: 2 minutes (same as Python/Langflow/synchronous API tools; MCP protocol does not support async)
​
Summary
Key Points:
wxO Flow: First choice for most scenarios - supports connections, security, custom code, no timeout limit
Python Tools: For custom libraries not supported in wxO Flow code blocks
Langflow Tools: For Langflow-specific AI components
API Tools: For OpenAPI-based external service integrations - performance depends on external service
MCP Tools: For Model Context Protocol capabilities - performance varies by implementation
Tool call overhead exists: Combine operations when possible
2-minute timeout: Applies to synchrous tools such as Python, Langflow, OpenAPI sync and MCP tools
Related Guides:
Main Performance Guide
Agent Performance Guide
Flow Performance Guide



---


Performance Guide
Knowledge Performance Guide
Understanding, measuring, and optimizing Knowledge runtime performance in watsonx Orchestrate

Part of: watsonx Orchestrate Performance Guide
Performance Testing Approach
This guide focuses on how to measure and optimize Knowledge runtime performance. Performance varies significantly based on workload, configuration, system load, and network conditions. Always measure in your own environment.
Note: “Flow” in this document refers to wxO Agentic Workflow
​
Overview
Knowledge in watsonx Orchestrate enables agents to return accurate, relevant answers based on trusted information. Knowledge sources provide factual and contextual data that help interpret user questions and generate meaningful responses.
Knowledge Source Types:
File Uploads: Static content stored in internal knowledge base
External Repositories: Milvus, Elasticsearch, Astra DB, or custom services
​
Understanding Knowledge Performance
​
Knowledge as a Built-in Tool
Key Insight: Knowledge is internally implemented as a built-in tool, which means:
It shares the same performance characteristics as other tools in wxO
Each knowledge retrieval incurs tool invocation overhead
Performance depends on both the tool call overhead and the actual search execution
Understanding this helps you optimize knowledge usage patterns
Performance Components:
Tool Invocation: Time to initialize and prepare the knowledge request
Search Execution: Time to perform the actual search (varies by repository type)
Result Processing: Time to format and return results to the agent
This is important because:
Multiple knowledge calls = Multiple tool invocation costs
The actual search time is often fast, but tool overhead exists for each call
​
Knowledge Modes: Classic vs Dynamic
Knowledge can operate in two modes, each with different performance characteristics:
Classic Mode:
Knowledge performs query rewrite, search, and answer generation
Returns a complete answer to the agent
Latency: Higher (includes query rewrite + search + answer generation)
Use case: When you want consistent, pre-formatted answers
Dynamic Mode (Recommended):
Knowledge returns raw search results to the agent
Agent processes the results and formulates its own response
Latency: Lower for knowledge retrieval
Use case: When agent needs flexibility to interpret and combine results
Performance Comparison:
Aspect	Classic Mode	Dynamic Mode
Knowledge execution	Slower (query rewrite + search + answer generation)	Faster (search only)
Agent processing	Minimal (receives answer)	More (interprets results)
Total latency	Higher	Variable (depends on agent processing)
Flexibility	Lower (fixed answer format)	Higher (agent can combine/interpret)
Best for	Simple Q&A, consistent answers	Complex reasoning, multi-source synthesis
Recommendation: Use Dynamic mode for better performance and flexibility unless you specifically need pre-formatted answers.
​
Performance by Knowledge Sources
You can use the built-in file uploads or connect to external knowledge sources like Milvus, Elasticsearch, Astra DB, or a custom service as your knowledge source.
Note: Using external knowledge sources require creating your own vector index and ingesting your data into it.
​
Performance Characteristics by Type
Repository Type	Performance	Network Dependency	Best For
File Uploads	Very fast	Managed by wxO	Static content, quick setup, small to medium datasets
Milvus	Fast	Yes	Large-scale vector search, high-volume queries
Elasticsearch	Fast	Yes	Full-text/hybrid search, structured data, complex filtering
Astra DB	Fast	Yes	Cloud-native deployments, managed service
Custom Service	Varies	Yes	Specialized integrations, custom search logic
​
Repository Selection Guide
File Uploads:
Best for: Static content, documentation, policies, FAQs
Limits: 20 files per batch, 30MB total, 600 pages per file
Formats: .docx, .pdf, .pptx, .xlsx (25MB max), .csv, .html, .txt (5MB max)
Performance: Fastest option for small to medium datasets
Milvus:
Best for: Large-scale semantic search, high query volumes
Strengths: Optimized for vector similarity search, scales well
Consideration: Requires setup and maintenance
Elasticsearch:
Best for: Full-text search, hybrid search, structured content
Strengths: Flexible query capabilities, good for keyword and semantic search
Consideration: Supports custom query bodies for advanced filtering
Astra DB:
Best for: Cloud deployments, managed service preference
Strengths: Consistent performance, reduced operational overhead
Consideration: Cloud-native architecture
Custom Service:
Best for: Specialized integrations, custom search logic, unique requirements
Strengths: Full control over search implementation, can integrate proprietary systems
Consideration: Performance varies by implementation, requires custom development and maintenance
​
Retrieval Speed vs Quality Trade-offs
Understanding the trade-offs between speed and quality is crucial for optimizing knowledge performance. Different configurations impact both retrieval speed and answer accuracy.
​
Search Strategy Trade-offs
For Elasticsearch & Astra DB:
Search Type	Speed	Quality	Best For
Keyword Search	Fastest	Good for exact matches	Known terminology, product codes, exact phrases
Vector Search	Moderate	Best for semantic understanding	Natural language queries, conceptual similarity
Hybrid Search	Slowest	Best overall accuracy	Complex queries requiring both precision and recall
Keyword Search:
Speed: Fastest - no embedding generation required
Quality: Excellent for exact matches, limited for semantic similarity
Use when: Users search with specific terms, product codes, or exact phrases
Example: “Order #12345”, “Return policy”, “Product SKU-789”
Vector Search:
Speed: Moderate - requires embedding generation for query
Quality: Excellent for semantic understanding, handles synonyms and paraphrasing
Use when: Natural language queries, conceptual searches, multilingual content
Example: “How do I get my money back?” (matches “refund policy”)
Hybrid Search:
Speed: Slightly slower - combines both keyword and vector search
Quality: Best overall - combines precision of keywords with semantic understanding
Use when: Accuracy is critical, queries are complex, or you need both exact and semantic matches
Example: “iPhone 15 battery life issues” (exact product + semantic problem)
Recommendation: Use hybrid search for best quality, and only optimize to keyword or vector search based on your specific use case and performance requirements.
​
Result Count Trade-offs (Default is 5)
Result Count	Speed	Quality	Best For
Low (1-3)	Fastest	Risk of missing relevant info	Simple queries, single-fact retrieval
Medium (5-10)	Moderate	Balanced coverage	General purpose, most use cases
High (15+)	Slowest	Comprehensive but may include noise	Complex queries, research tasks
Performance Impact:
More results = Longer retrieval time
More results = Larger context for agent processing
More results = Higher token usage
Quality Impact:
Too few results = May miss relevant information
Too many results = Noise and irrelevant content dilute quality
Optimal count depends on content granularity and query complexity
Recommendation: Start with 5-10 results for most use cases. Increase for complex queries requiring comprehensive coverage; decrease for simple fact retrieval.
​
Index Configuration Trade-offs
For External Repositories (Milvus, Elasticsearch, Astra DB):
Proper indexing significantly impacts both speed and quality:
Vector Index Types:
HNSW (Hierarchical Navigable Small World): Fast search, high accuracy, more memory usage
IVF (Inverted File): Balanced speed/memory, good for large datasets
Flat: Most accurate but slowest, only suitable for small datasets
Embedding Dimensions:
Lower dimensions (384): Faster, less storage, slightly lower quality
Higher dimensions (768, 1536): Slower, more storage, better semantic understanding
Recommendation:
Use HNSW indexing for vector search in production
Choose embeddings models with 768 dimensions for balanced performance and quality
Test with your specific data to find optimal configuration
​
Optimization Strategies
​
1. Choose the Right Mode
Use Dynamic Mode (Recommended):
Faster knowledge retrieval
More flexible agent processing
Better for complex reasoning tasks
Use Classic Mode:
When you need consistent, pre-formatted answers
For simple Q&A scenarios
When agent flexibility is not required
​
2. Select Appropriate Repository
File Uploads:
✅ Static content (policies, documentation, FAQs)
✅ Quick setup and testing
✅ Small to medium datasets
External Repositories:
✅ Large-scale content (100K+ documents)
✅ Frequently updated information
✅ High query volumes
✅ Advanced search capabilities needed
​
3. Optimize Search Strategy
Choose Based on Your Use Case:
Keyword search: For exact term matching, fastest performance
Vector search: For natural language queries, semantic understanding
Hybrid search: For best accuracy with slightly slower performance
Adjust Result Counts:
Start with 5-10 results
Reduce to 1-3 for simple fact retrieval
Increase to 15+ only for complex research queries
​
4. Optimize Repository Configuration
For External Repositories:
Ensure proper indexing (HNSW for vector search)
Minotor index size and performance
Use metadata filtering to narrow search scope
Monitor and optimize network connectivity
​
5. Provide Clear Knowledge Source Descriptions
Why It Matters:
Helps agents select the right knowledge source
Improves query formulation
Enhances overall agent performance
Best Practices:
Describe what content the source contains
Specify the types of questions it can answer
Include relevant keywords and topics
Keep descriptions clear and concise
Example:
❌ Poor: “Company documents”
✅ Good: “Employee handbook containing HR policies, benefits information, and workplace guidelines. Use for questions about PTO, health insurance, and company policies.”
​
Measuring Knowledge Performance
​
How to Measure
Using Agent Traces:
Execute agent runs that use knowledge
Retrieve detailed traces using the searchTraces API
Analyze knowledge tool execution time in traces Knowledge tool response has a debug object with detailed information about processing time and other metrics, including the following:
total_time_ms: Total time spent in the knowledge tool
search_time_ms: Time spent calling search excluding embeeding generation
answer_generation_time_ms: Time spent calling LLM to generate answer
Identify bottlenecks in the knowledge pipeline
Testing External Repositories Independently:
Test repository performance directly (outside of wxO)
Measure search latency at the repository level
Compare with end-to-end knowledge tool performance
Isolate network vs processing time
​
Key Metrics to Track
Speed Metrics:
Total knowledge execution time: End-to-end retrieval time
Embedding generation time: Time to create vector embeddings
Search latency: Time spent in actual search operation
Answer generation time: Time to create final response
Network latency: Time for external repository communication (if applicable)
​
Performance Analysis Tips
Establish baselines: Measure performance with different configurations
Test with representative queries: Use real-world query patterns
Monitor over time: Track performance trends as data grows
Compare modes: Test Classic vs Dynamic mode for your use case
Test different search strategies: Compare keyword, vector, and hybrid search
Vary result counts: Find optimal balance for your use case
​
Summary
Key Points:
Dynamic mode (recommended): Faster knowledge retrieval, more flexible agent processing
Repository selection matters: File uploads for static content, external repositories for scale
Search strategy impacts performance: Keyword (fastest) → Vector (moderate) → Hybrid (slowest, most accurate)
Result count affects speed and quality: 5-10 results optimal for most use cases
Proper indexing is critical: Use HNSW for vector search
Speed vs Quality Trade-offs:
Search strategy: Balance between speed (keyword) and semantic understanding (vector/hybrid)
Result count: More results = better coverage but slower and potentially noisier
Index configuration: Better indexing = faster search but requires more resources
Performance Best Practices:
Use Dynamic mode for better performance and flexibility
Choose appropriate repository based on content size and update frequency
Select search strategy based on query types (keyword/vector/hybrid)
Optimize result counts (start with 5-10)
Ensure proper indexing for external repositories
Provide clear, detailed knowledge source descriptions
Monitor performance metrics and adjust based on real usage patterns
Test with representative queries before production deployment
Related Guides:
Main Performance Guide
Agent Performance Guide
Flow Performance Guide
Tool Performance Guide


---

CI/CD Deployment
wxO CI/CD Deployment Approach
A GitOps-inspired deployment strategy for watsonx Orchestrate agents, flows, tools, and knowledge bases using standard CI/CD pipelines

Use case: This guide provides one approach for customers on watsonx Orchestrate SaaS to leverage Git-based deployment and CI/CD practices that follow GitOps principles to control the lifecycle of agents and associated tools, flows, and other wxO assets.
Note on CI/CD Neutrality: There are many valid CI/CD approaches for managing wxO assets. This document presents one specific implementation using Git-based workflows. watsonx Orchestrate maintains a CI/CD-neutral stance, providing CLI tools and APIs that enable customers to adopt agent lifecycle management into their own existing CI/CD pipelines, regardless of the specific tools or practices they use (Jenkins, GitLab CI, GitHub Actions, Azure DevOps, and others).
Scope: While this guide focuses on agents, flows, knowledge, and tools, the same approach can be applied to other wxO features that have file-based assets, including but not limited to:
Voice (voice configurations)
Custom Models (custom LLM model configurations)
Plugins (plugin definitions and configurations)
Each of these features has corresponding CLI commands and file-based representations that can follow the same GitOps workflow outlined in this document.
​
Executive Summary
This document proposes a GitOps-inspired deployment strategy for watsonx Orchestrate (wxO) agents, flows, and tools that works without Kubernetes or Argo CD access. The approach uses standard CI/CD tools such as Jenkins, GitLab CI, or GitHub Actions together with the wxO CLI.
​
Key Components
1. Two-Tenant Architecture

2. Git-Based Versioning

3. Deployment Approach

4. Multi-Repository Support

​
Deployment Flow
Code Change → Git Branch → CI/CD Pipeline → wxO Deployment

develop → dev-qa-tenant Draft → Auto-deploy
  ↓ (PR: develop → qa-<version>)
qa-<version> → dev-qa-tenant Live → Auto-deploy + approval
  ↓ (PR: qa-<version> → staging-<version>) ← CROSS-TENANT BOUNDARY
staging-<version> → prod-tenant Draft → Auto-deploy + approval
  ↓ (PR: staging-<version> → main)
main → prod-tenant Live → Auto-deploy + CAB approval
​
Key Benefits
GitOps Principles
Works without requiring Kubernetes access
Complete Isolation
Separates production from non-production environments
Automatic Versioning
Uses Git tags for release tracking
Safe Promotions
Uses Git merges with approval gates
Easy Rollbacks
Supports rollback through git revert
Multi-Repository Support
Coordinates deployments across repositories
Secret-Free Git
Resolves secrets at runtime
Audit Trail
Preserves deployment history in Git
​
Document Structure
This guide is organized into four parts:
Part 1: Foundation
Goals, two-tenant architecture, repository layout, and Git-based versioning
Part 2: Configuration
Configuration specifications, knowledge-base deployment, and secret handling
Part 3: Operations
Inter-agent dependencies, testing gates, promotion workflows, and CLI deployment
Part 4: Summary
Core principles summary and implementation checklist
​
Important Disclaimer
All code examples, configurations, and scripts in this document are provided for reference purposes only.
These examples are intended to illustrate concepts and approaches. They must be customized and adapted to match your organization’s specific:
Deployment practices and standards
Security requirements and policies
CI/CD tooling and infrastructure
Network architecture and access controls
Compliance and governance requirements
Organizational workflows and approval processes
Before implementing:
Review all examples with your security, DevOps, and compliance teams
Adapt code to your organization’s coding standards and best practices
Test thoroughly in non-production environments
Validate against your organization’s security policies
Ensure compliance with relevant regulations and standards
This document does not constitute:
Production-ready code or configurations
Security-hardened implementations
Officially supported IBM solutions or recommendations
A substitute for proper security review and testing
​
1) Goals and Non-Goals
​
Goals
Deterministic, auditable promotion of agents (YAML), flows (Python or JSON), and tools (Python) across Dev → QA → PreProd → Prod
Support multiple versions of the same agent; flows and tools are shared rather than tied one-to-one to agents
No credentials in Git; secrets are resolved at deploy time from a secret manager
Safe rollbacks, easy diffs, and clear separation of concerns
​
Non-Goals
Does not require Kubernetes or Argo CD access for customers
Does not mandate a single secrets backend; compatible with Vault, AWS, Azure, IBM, and similar secret managers
​
2) Two-Tenant Architecture
​
Current wxO environments per tenant
wxO currently provides only two environments per tenant:
Draft for development and testing
Live for production use
​
Proposed Solution: Two Tenants
To support a full Dev → QA → PreProd → Prod promotion pipeline, use two separate wxO tenants or accounts.
Tenant 1: Non-Production
Tenant 2: Production
Non-Production Account (dev-qa-tenant)
This single tenant or account contains both Dev and QA environments:
Draft environment → Dev (develop branch)
Live environment → QA (qa-<version> branches)
Dev and QA are in the same tenant or account. Dev uses the Draft environment, and QA uses the Live environment.
A knowledge base created in a tenant is used for both Draft and Live environments.
​
Key Architecture Points
Environment Mapping:
dev-qa-tenant (Account 1)
  ├─ Draft  = Dev
  └─ Live   = QA

prod-tenant (Account 2)
  ├─ Draft  = PreProd/Staging
  └─ Live   = Production
Rationale:
Isolation: Production is completely isolated from development and testing activities
Security: Different RBAC, credentials, and network policies per account
Compliance: Audit trails and change controls are separated by account
Risk mitigation: Issues in Dev or QA cannot affect PreProd or Prod infrastructure
Same-account promotion: Dev → QA and PreProd → Prod use wxO’s native Draft → Live promotion
​
Tenant Configuration
Each tenant requires:
Separate API endpoints and authentication tokens
Separate secrets in the secret manager, scoped by tenant
Separate connection configurations
Tenant-specific feature flags and resource quotas
​
Cross-Tenant Promotion
Promoting from QA → PreProd involves:
Updating version pins in envs/preprod/*-releases.yaml
The pipeline authenticates to prod-tenant instead of dev-qa-tenant
The deployment targets the Draft environment in prod-tenant for PreProd
After validation, the deployment is promoted to the Live environment in prod-tenant for Prod
​
3) Repository Layout and Branching Strategy
​
Git Branch Structure
develop (dev-qa-tenant Draft)
  ↓
qa-<version> (dev-qa-tenant Live)
  ↓
staging-<version> (prod-tenant Draft)
  ↓
main (prod-tenant Live) ← PRODUCTION
​
Branch Convention
develop: current development branch, auto-deploys to dev-qa-tenant Draft
qa-<version>: QA release branch, auto-deploys to dev-qa-tenant Live
staging-<version>: pre-production branch, auto-deploys to prod-tenant Draft
main: production branch, auto-deploys to prod-tenant Live
​
Branch Protection Rules
develop: requires pull request reviews for feature merges
qa-<version>: created from develop, requires approval to promote
staging-<version>: created from the QA branch, requires approval and cross-tenant validation
main: requires CAB approval, change ticket, and final sign-off
​
Repository Structure Per Branch
repo/
  agents/
    employee_onboarding/
      agent.yaml
    document_processing_agent/
      agent.yaml

  tools/
    hr_api/
      tool.py
    db_query/
      tool.py
    document_processing/
      workflow.py
    hr_workflow/
      workflow.py

  knowledge-bases/
    hr_policy_docs.yaml
    product_catalog.yaml

  connections/
    dev-qa-tenant/
      connections.template.yaml
    prod-tenant/
      connections.template.yaml

  config/
    tenant.yaml
    values.yaml

  ci/
    pipelines/
      jenkins/
        Jenkinsfile
    policies/
      opa/rego/...

  docs/
    adr/
    runbooks/
​
Rationale
Git branches provide versioning, and each branch represents the state of a specific environment
No version directories are needed because agent, tool, and flow files sit at the root of their folders
Git tags mark releases, for example v1.2.0 or release-2024-01-15
Branch merging promotes code from one environment to the next
Tenant separation is defined by the branch-specific config/tenant.yaml
Secrets are never stored in Git; only templates and secret references are committed
Structural changes can evolve naturally through branches
The tools/ directory can contain both Python or OpenAPI tools and agentic workflows
​
4) Git-Based Versioning Strategy
​
Branch-Based Versioning
Git branches represent environment state; each branch contains the current version for that environment
Git tags mark releases using semantic versioning (MAJOR.MINOR.PATCH)
MAJOR: breaking changes in I/O or behavior
MINOR: backward-compatible features
PATCH: bug fixes
Git commits provide a full audit trail of all changes
Branch merging promotes code from one environment to the next
​
Backward Compatibility Principle
Critical design principle: Agents and tools should be designed to maintain backward compatibility. Upgrading an agent or tool should not break existing functionality that other agents or systems depend on.
​
Why backward compatibility matters
Single active version: Because only one version of an agent or tool is active in each environment, breaking changes can immediately affect all dependent agents
Deployment safety: Backward-compatible changes allow safe, incremental deployments without extra coordination overhead
Reduced risk: They reduce the chance of cascading failures across dependent agents
Simplified rollback: Rollback is easier when changes are additive instead of breaking
​
Best practices for backward compatibility
Additive changes: Add new parameters or features without removing or changing existing ones
Optional parameters: New parameters should have sensible defaults
Deprecation path: If breaking changes are unavoidable:
Add new functionality alongside the old implementation
Mark the old functionality as deprecated with warnings
Remove the old functionality only in the next major version
Tool I/O contracts: Maintain consistent input and output schemas; extend rather than modify
Agent instructions: Update prompts to support new features while preserving existing behavior
Version communication: Clearly document breaking changes in release notes and Git tags
​
When breaking changes are necessary
Because wxO supports only one agent version per environment, it is better to create a new agent with a different name rather than upgrade an existing agent in a breaking way.
​
Recommended approach for breaking changes
Create a new agent such as employee_onboarding_v2 or employee_onboarding_enhanced
Give the new agent a distinct name
Allow both old and new agents to coexist in the same environment
Let dependent systems migrate at their own pace
Maintain the old agent
Keep the original agent available for existing consumers
Mark it as deprecated in documentation
Decommission it after all consumers migrate
Coordinate migration
Update dependent agents or systems to use the new agent name
Test thoroughly in lower environments
Migrate production consumers in a controlled way
Monitor both agents during the transition
Decommission the old agent
Remove it after all consumers have migrated
Document the migration in release notes
​
Why this approach works better
No Downtime
Both agents can run during migration
Gradual Migration
Consumers can move at their own pace
Easy Rollback
Consumers can switch back if needed
Clear Separation
Distinct names make versions obvious
​
Example: Tool Evolution (Backward Compatible)
# v1.0.0 - Original tool
def process_document(document_path):
    return {"status": "processed", "path": document_path}

# v1.1.0 - Backward compatible (adds optional parameter)
def process_document(document_path, format="pdf"):
    # format defaults to "pdf" - existing callers unaffected
    return {"status": "processed", "path": document_path, "format": format}

# v1.2.0 - Backward compatible (adds new output field)
def process_document(document_path, format="pdf"):
    return {
        "status": "processed",
        "path": document_path,
        "format": format,
        "page_count": 10  # New field - existing consumers can ignore
    }
​
Example: Agent Evolution (Breaking Change → New Agent)
# Original agent: employee_onboarding
# agents/employee_onboarding/agent.yaml
spec_version: v1
kind: native
name: employee_onboarding
llm: groq/openai/gpt-oss-120b
tools:
  - hr_api
  - document_processor

# New agent with breaking changes: employee_onboarding_v2
# agents/employee_onboarding_v2/agent.yaml
spec_version: v1
kind: native
name: employee_onboarding_v2
llm: groq/openai/gpt-oss-120b
tools:
  - hr_api_v2
  - document_processor_enhanced
  - compliance_checker
​
Migration Path
Deploy employee_onboarding_v2 alongside employee_onboarding
Update consuming systems to call employee_onboarding_v2
Monitor both agents during transition
Once all consumers have migrated, decommission employee_onboarding
​
Tagging Strategy
Release tags on each branch:
# Tag format: v{MAJOR}.{MINOR}.{PATCH}-{environment}
v1.2.0-dev
v1.2.0-qa
v1.2.0-preprod
v1.2.0-prod
Annotated tags for traceability:
git tag -a v1.2.0-prod -m "Release 1.2.0 to production
- Added new HR onboarding workflow
- Fixed document processing bug
- Updated connection timeout settings
Approved by: CAB-2024-001
Deployed: 2024-01-15T10:00:00Z"
​
Version Evolution Example
develop branch:
  └─ v1.2.0-dev (deployed to dev-qa-tenant Draft)

qa-1.1.0 branch:
  └─ v1.1.0-qa (deployed to dev-qa-tenant Live)

staging-1.0.0 branch:
  └─ v1.0.0-staging (deployed to prod-tenant Draft)

main branch:
  └─ v1.0.0-prod (deployed to prod-tenant Live)
​
Benefits of Git-Based Versioning
Natural evolution: agent structures can change significantly between environments
No manual version management: Git handles versioning automatically
Full history: every change is tracked with commit messages
Easy comparison: git diff qa..preprod shows exactly what will be promoted
Simplified structure: no need for multiple version directories
Branch protection: helps prevent accidental changes to stable environments


---

CI/CD Deployment
wxO CI/CD Deployment Approach (Part 2)
Configuration specifications, knowledge-base deployment considerations, and secret handling patterns for wxO CI/CD workflows

​
5) Configuration Specifications (Per Branch)
​
5.1 Tenant Configuration
Each branch contains config/tenant.yaml, which specifies which wxO tenant and environment to target.
Dev
QA
PreProd
Prod
dev branch — config/tenant.yaml (dev-qa-tenant, Draft)
tenant:
  name: dev-qa-tenant
  id: "tenant-12345-dev-qa"
  wxo_environment: draft        # wxO's Draft environment
  api_endpoint: "https://dev-qa.wxo.example.com/api"
  auth:
    type: api_key
    secret_ref: "wxo/dev-qa-tenant/api-key"  # reference to secrets manager
branch: dev
logical_environment: dev
​
5.2 Environment Values
Each branch contains environment-specific configuration in config/values.yaml.
Dev values
Prod values
dev branch — config/values.yaml
environment: dev
tenant: dev-qa-tenant
featureFlags:
  enableHrToolV2: true
  enableBetaFeatures: true
endpoints:
  hr_api_base: "https://api.dev.company.com"
  db_host: "db.dev.company.com"
timeouts:
  api_timeout: 30
  db_timeout: 10
​
5.3 Agent Structure (Example)
agents/employee_onboarding/agent.yaml (evolves per branch)
spec_version: v1
kind: native
name: employee_onboarding
description: "Automates employee onboarding process"
instructions: |
  You are an HR onboarding assistant that helps automate the employee onboarding process.
  
  Your responsibilities:
  - Create employee records in the HR system
  - Set up accounts and access permissions
  - Schedule onboarding meetings
  - Track onboarding progress
  
  Tool Usage Guidelines:
  1. Before calling a tool, ensure you have all required parameters
  2. Do NOT assume any tool parameters
  3. Do NOT pass parameters that are not explicitly defined
  4. Do NOT call the same tool multiple times with the same parameters
  
  How to Use Tools:
  - Use hr_api to create and update employee records
  - Use db_query to retrieve employee information
  - Use document_processing workflow for document handling

llm: groq/openai/gpt-oss-120b
style: react_core
tools:
  - hr_api
  - db_query
  - document_processing
knowledge_base:
  - hr_policy_docs
collaborators: []
​
Alternative: Minimal Agent Structure
spec_version: v1
kind: native
name: employee_onboarding
description: "Automates employee onboarding process"
instructions: "You are an HR onboarding assistant."
llm: groq/openai/gpt-oss-120b
style: react_core
tools:
  - hr_api
  - db_query
collaborators: []
Agents can be created through the UI or YAML
If agents are built through the UI, they should be exported as YAML and versioned in Git
If flows are built through the UI, they should be exported as JSON and versioned in Git
The YAML or JSON files in Git are the source of truth for version control
The agent structure can differ significantly between branches, for example when dev includes experimental tools
​
Key Agent Fields
spec_version: always v1
kind: native for wxO native agents, external for external agents
name: unique identifier for the agent
description: brief description of the agent’s purpose
instructions: natural-language guidance for the LLM
llm: model in the format provider/developer/model_id, for example groq/openai/gpt-oss-120b
style: agent style such as default or react
tools: list of tool names the agent can use
knowledge_base: list of knowledge bases. Currently, only one knowledge base is supported.
collaborators: list of other agents this agent can call
Note on credentials: Agents do not have credentials. Credentials such as connection IDs or app_id values are associated with tools only. When a tool is imported through the CLI, it specifies its required connection ID. Agents use tools, and the tools handle their own authentication.
​
Agent Deployment Workflow
Create the agent YAML file manually
List required tools in the agent’s tools: section
Store the agent YAML in Git for version control
Deploy flows separately if needed through orchestrate tools import -k flow
Deploy the agent through orchestrate agents import -f agent.yaml
Tools listed in tools: are automatically deployed
Each tool specifies its own connection ID or app_id during import
Test the agent in the Draft environment
Promote to the Live environment when ready through orchestrate agents deploy
​
5.4 Knowledge-Base Deployment Considerations
Knowledge bases in wxO have unique deployment characteristics that differ from agents and tools.
​
Tenant-Scoped, Not Environment-Scoped
Unlike agents, which have separate Draft and Live states, knowledge bases are tenant-scoped:
A knowledge-base update applies to both Draft and Live environments simultaneously
There is no concept of promoting a knowledge base from Draft to Live within a tenant
Testing must occur in dev-qa-tenant before deployment to prod-tenant
​
Deployment Order
Knowledge bases must be deployed before agents that reference them:
# 1. Deploy knowledge-base first
orchestrate knowledge-bases import -f knowledge-bases/hr_policy_docs.yaml

# 2. Then deploy agent that uses it
orchestrate agents import -f agents/employee_onboarding/agent.yaml
​
Cross-Tenant Promotion
Knowledge bases must be explicitly deployed to each tenant:
Merging code from qa-branch to staging-branch does not automatically deploy the knowledge base to prod-tenant
The CI/CD pipeline must deploy knowledge bases to prod-tenant separately
Each tenant maintains its own knowledge-base instance
​
Testing Strategy
Because knowledge-base updates affect both Draft and Live:
Test in dev-qa-tenant first by deploying and validating there before prod-tenant
Validate queries in the Draft environment before promoting the agent
Monitor impact because knowledge-base changes immediately affect Live agents in the same tenant
​
Rollback Implications
Rolling back a knowledge base requires redeploying the previous version:
# Checkout previous version
git checkout v1.2.0 -- knowledge-bases/hr_policy_docs.yaml

# Redeploy to tenant
orchestrate knowledge-bases import -f knowledge-bases/hr_policy_docs.yaml
Rolling back an agent does not automatically roll back its knowledge base.
​
Tool Access
Credentials are associated with tools, not agents
Each tool specifies its connection ID or app_id when imported
Tools handle their own authentication by using the specified connection
Agents reference tools by name in the tools: section
​
6) Secrets Handling (No Secrets in Git)
Use the customer’s secrets manager, such as Vault, AWS Secrets Manager, Azure Key Vault, or IBM Secrets Manager / Key Protect
Jenkins fetches secrets at deploy time, exports them as environment variables, and performs substitution
Tenant-scoped secrets ensure complete isolation because each tenant has its own set of secrets
​
Secret Organization by Tenant
Secrets manager structure:
wxo/
  dev-qa-tenant/
    api-key                    # wxO API authentication for dev-qa tenant
    connections/
      hr/username
      hr/password
      hr/client_id
      db/user
      db/pass
      db/host
  prod-tenant/
    api-key                    # wxO API authentication for prod tenant
    connections/
      hr/username
      hr/password
      hr/client_id
      db/user
      db/pass
      db/host
​
Example Substitution (Bash)
Dev environment
Prod environment
For Dev (dev-qa-tenant):
# Fetch tenant-specific wxO API credentials
export WXO_API_KEY=$(vault kv get -field=api_key secret/wxo/dev-qa-tenant/api-key)
export WXO_API_ENDPOINT="https://dev-qa.wxo.example.com/api"

# Fetch connection secrets for dev-qa tenant
export HR_USERNAME=$(vault kv get -field=username secret/wxo/dev-qa-tenant/connections/hr)
export HR_PASSWORD=$(vault kv get -field=password secret/wxo/dev-qa-tenant/connections/hr)
export HR_CLIENT_ID=$(vault kv get -field=client_id secret/wxo/dev-qa-tenant/connections/hr)
export DB_USER=$(vault kv get -field=user secret/wxo/dev-qa-tenant/connections/db)
export DB_PASS=$(vault kv get -field=pass secret/wxo/dev-qa-tenant/connections/db)
export DB_HOST=$(vault kv get -field=host secret/wxo/dev-qa-tenant/connections/db)
export ENV=dev
export TENANT=dev-qa-tenant

# Resolve connections template for dev-qa tenant
envsubst < connections/dev-qa-tenant/connections.template.yaml > connections/connections-resolved.yaml
Principles:
Secrets are materialized only inside the pipeline execution context and are never committed back to Git
Each tenant has completely isolated secrets to prevent cross-tenant credential leakage
Production secrets are never accessible from non-production pipelines

---

CI/CD Deployment
wxO CI/CD Deployment Approach (Part 3)
Inter-agent dependency patterns, testing gates, promotion and rollback workflows, security controls, and CLI deployment examples for wxO CI/CD

​
7) Inter-Agent Dependencies (Multi-Repository)
​
Overview
When agents are managed in separate Git repositories and have dependencies on each other, such as AgentA depending on AgentB, you need a strategy to coordinate deployments across repositories.
​
Core Principle: CI/CD Pipeline as the Only Authorized Deployment Path
The general approach is to use the CI/CD pipeline as the only authorized path to deploy agents to production environments. Customers should not deploy agents manually by hand or with ad hoc scripts. This ensures:
Consistency: all deployments follow the same process
Auditability: every deployment is tracked in CI/CD logs
Governance: approval gates and quality checks are enforced
Traceability: deployments are linked to Git commits and pull requests
​
Key Challenges
Version synchronization: dependent agents must reference compatible versions
Deployment order: dependencies must be deployed before dependents
Cross-tenant coordination: agents must exist in the same tenant and environment
Testing: integration tests require all dependent agents to be available
Single active version: only one version of an agent or tool is active in a given environment
​
Illustrative Solution: File-Based Agent Registry
The file-based registry approach described below is one possible solution for illustration purposes only. It is not a recommendation or best practice. The final solution might be more sophisticated or simpler depending on the level of lifecycle governance required by your organization.
Given that only one version of an agent or tool is active in a given environment, a simple file-based agent registry can be used to maintain dependencies and validate deployments.
​
Example Registry Structure
# agent-registry.yaml - File-based catalog for multi-repo dependencies
# This is an ILLUSTRATIVE example, not a prescriptive solution
agents:
  document_processor:
    repository: git@github.com:company/repo-b.git
    dependencies: []  # No dependencies - deploys first
    environments:
      dev: { branch: dev, version: v1.2.3, status: configured }
  
  employee_onboarding:
    repository: git@github.com:company/repo-a.git
    dependencies:
      - agent: document_processor
        version: ">=1.2.0"
    environments:
      dev: { branch: dev, version: v2.1.0, status: configured }
​
How This Illustrative Approach Works
The pipeline reads agent-registry.yaml
It builds a dependency graph such as document_processor → employee_onboarding
It deploys in order: first document_processor, then employee_onboarding
It validates version requirements before each deployment
It updates the registry with new versions and timestamps
​
Why This Simple Approach Can Work
Single Active Version
One active version per environment simplifies tracking
No Extra Infrastructure
No server infrastructure is required beyond a YAML file in Git
Version Controlled
Git tracks every registry change
Dependency Validation
Helps prevent incompatible deployments
​
Alternative Approaches
Option 1: More Sophisticated Solutions

Option 2: Simpler Solutions

Option 3: No Explicit Dependency Management

​
8) Testing and Quality Gates
Unit tests: knowledge bases, tools, and flows
Static validation: JSON Schema for agent.yaml and *-releases.yaml
Contract tests: tool I/O and validation that agents reference valid tool versions
Prompt regression: low-temperature runs to validate tool selection and output format
Security: SAST and dependency scans
Policy: OPA or Conftest rules, for example forbidding latest, enforcing approved model IDs, and applying temperature caps in production
​
8) Git-Based Promotion and Rollback
​
Promotion Workflow via Branch Merging
Promotions follow a strict path: dev → qa → preprod → prod
All promotions are performed through Git branch merges by using pull requests.
​
Within-Tenant Promotions
Dev to QA
PreProd to Prod
Dev → QA within dev-qa-tenant
# 1. Develop and test in dev branch (dev-qa-tenant Draft)
# 2. Create PR: dev → qa
# 3. PR review + approval
# 4. Merge triggers Jenkins pipeline
# 5. Auto-deploys to dev-qa-tenant Live (QA)
# 6. Git tag created: v1.2.3-qa

# Example PR
git checkout qa
git pull origin qa
git merge --no-ff dev
git push origin qa
​
Cross-Tenant Promotion
QA → PreProd crosses the tenant boundary from dev-qa-tenant to prod-tenant.
# This is the critical cross-tenant boundary
# 1. Validate in qa branch (dev-qa-tenant Live)
# 2. Create PR: qa → preprod
# 3. Requires team lead approval
# 4. Merge triggers Jenkins pipeline
# 5. Pipeline switches authentication from dev-qa-tenant to prod-tenant
# 6. Deploys to prod-tenant Draft (PreProd)
# 7. Git tag created: v1.2.3-preprod

# Example cross-tenant PR
git checkout preprod
git pull origin preprod
git merge --no-ff qa
# Resolve any conflicts (e.g., config/tenant.yaml, config/values.yaml)
git push origin preprod
​
Handling Merge Conflicts
# Common conflicts during cross-tenant merge (qa → preprod):
# - config/tenant.yaml (keep preprod's tenant config)
# - config/values.yaml (keep preprod's environment values)
# - connections/ (may differ between tenants)

# Resolution strategy:
git checkout preprod
git merge qa
# CONFLICT in config/tenant.yaml
git checkout --theirs config/tenant.yaml  # Keep preprod's tenant config
git checkout --theirs config/values.yaml  # Keep preprod's values
git add config/
git commit -m "Merge qa → preprod: Promote v1.2.3"
​
Promotion Best Practices
Always use pull requests: never push directly to environment branches
Use merge commits: use --no-ff to preserve promotion history
Enforce approval gates
dev → qa: automated after CI checks pass
qa → preprod: team lead approval for the cross-tenant boundary
preprod → prod: CAB approval and a change ticket
Run smoke tests after each deployment before marking success
Tag only after success: Git tags are created automatically by Jenkins after successful deployment
Review diffs: use git diff qa..preprod to inspect what will be promoted
​
Comparing Branches Before Promotion
# See what changes will be promoted from qa to preprod
git diff qa..preprod

# See commit history
git log preprod..qa --oneline

# See file-level changes
git diff qa..preprod --stat

# See specific file changes
git diff qa..preprod -- agents/employee_onboarding/agent.yaml
​
Rollback Strategies
​
Knowledge-Base Promotion and Rollback
Knowledge bases require special handling during promotion and rollback.
Promotion workflow:
Knowledge bases are not promoted from Draft to Live because that concept does not exist
During cross-tenant promotion (qa → staging), knowledge bases must be redeployed to prod-tenant
Git merges bring the knowledge-base YAML files forward, but CI/CD must still execute deployment
Rollback considerations:
Rolling back an agent does not automatically roll back its knowledge base
Rolling back a knowledge base requires explicit redeployment of the previous version
# Checkout previous knowledge-base version
git checkout v1.2.0 -- knowledge-bases/hr_policy_docs.yaml

# Redeploy to tenant
orchestrate knowledge-bases import -f knowledge-bases/hr_policy_docs.yaml
A knowledge-base rollback affects both Draft and Live agents in the same tenant immediately.
​
Simple Rollback (Revert Merge)
# Rollback prod to previous state
git checkout prod
git revert -m 1 <merge-commit-sha>  # Revert the merge commit
git push origin prod
# Triggers pipeline to redeploy previous version
Example:
# Find the merge commit to revert
git log prod --oneline --merges
# Output: abc1234 Merge preprod → prod: v1.2.3

# Revert the merge
git revert -m 1 abc1234
git push origin prod
# Jenkins redeploys the previous version (v1.2.2-prod)
​
Rollback to Specific Tag
# Rollback prod to a specific known-good version
git checkout prod
git reset --hard v1.2.0-prod  # Reset to specific tag
git push --force origin prod  # Force push (requires special permissions)
# Triggers pipeline to redeploy v1.2.0
Force-pushing requires special permissions and should be used only in emergency situations.
​
Emergency Rollback (Cross-Tenant)
If Production (prod-tenant Live) has critical issues:
# 1. Identify last known good tag
git tag -l "v*-prod" --sort=-version:refname | head -5

# 2. Create emergency rollback branch
git checkout -b emergency-rollback-prod v1.2.0-prod

# 3. Force restore to prod (with approvals)
git checkout prod
git reset --hard emergency-rollback-prod
git push --force origin prod

# 4. Pipeline redeploys v1.2.0 to prod-tenant Live
# 5. Post-mortem to understand root cause
​
Rollback Considerations
Git history: all rollbacks remain visible in Git history
Backward compatibility: verify that old versions still work with current infrastructure
Database migrations: might require manual intervention when schema changes exist
Connection changes: verify that old versions still work with current connection settings
Tenant isolation: a rollback in prod-tenant does not affect dev-qa-tenant
Tag references: use tags to identify exact versions for rollback
​
Promotion Checklist
​
Before promoting qa → preprod
All QA tests passed
Security scan completed
Performance benchmarks met
git diff qa..preprod reviewed
Merge conflicts resolved, especially configuration files
Documentation updated
Runbooks reviewed
Rollback plan documented
Change ticket approved
Stakeholders notified
​
Before promoting preprod → prod
PreProd validation completed
No critical issues in PreProd
Load testing completed
git diff preprod..prod reviewed
Disaster recovery tested
On-call team briefed
Maintenance window scheduled if needed
CAB approval obtained
Emergency rollback plan ready
​
Git Workflow Diagram
main (development)
  ↓ (feature branches merge here)
dev branch
  ↓ (PR: dev → qa)
qa branch
  ↓ (PR: qa → preprod) ← CROSS-TENANT BOUNDARY
preprod branch
  ↓ (PR: preprod → prod)
prod branch

Tags:
v1.2.3-dev → v1.2.3-qa → v1.2.3-preprod → v1.2.3-prod
​
9) Security and Governance
Secrets: use secret managers only; never commit secrets; rotate regularly
RBAC: restrict Jenkins credentials and use scoped tokens for the wxO API
Network: use allowlists for API endpoints
Images: if using image mode, sign images and avoid :latest
Reviews: use code owners for agents/ and envs/prod/
​
11) wxO ADK CLI Deployment Commands
This section provides examples of using the watsonx Orchestrate ADK CLI to deploy agents, flows, and tools to different environments and tenants.
​
Prerequisites
Install wxO ADK: pip install ibm-watsonx-orchestrate
Activate environment: point the CLI to the correct tenant
Authenticate: ensure the proper credentials are configured
​
Environment Activation
Before deploying, activate the correct tenant environment:
# Activate dev-qa-tenant for Dev/QA deployments
orchestrate env activate dev-qa-tenant

# Activate prod-tenant for PreProd/Prod deployments
orchestrate env activate prod-tenant
​
Deploying Tools
Tools must be deployed before agents that use them.
Python tool
Flow
OpenAPI tool
# Deploy a Python tool
orchestrate tools import \
  -k python \
  -f tools/hr_api/tool.py
​
Deploying Knowledge Bases
Knowledge bases must be deployed before an agent can use them.
Built-in knowledge base
External knowledge base
orchestrate knowledge-bases import -f knowledge-bases/hr_policy_docs.yaml
​
Agent Deployment Commands
Agents use two different commands depending on the target environment.
​
1. orchestrate agents import
Used for Dev and PreProd Draft environments
Imports the hand-written agent YAML into Draft
orchestrate agents import -f agents/employee_onboarding/agent.yaml
​
2. orchestrate agents deploy
Used for QA and Prod Live environments
Promotes an existing agent from Draft to Live within the same tenant
See Deploying an agent
orchestrate agents deploy \
  --name employee_onboarding
​
Deployment Flow
Deploy flows first if the agent uses them
For Dev and PreProd, use import to deploy the agent to Draft
Tools are automatically deployed based on the agent’s tools: section
Test the agent in Draft
For QA and Prod, use deploy to promote from Draft to Live
​
Agent YAML Creation
Agent YAML files are hand-written and stored in Git
Do not use orchestrate agents create to generate YAML
YAML files serve as the source of truth for agent configuration
This supports version control and code review for agent definitions
​
Deployment Examples by Environment
Dev
QA
PreProd
Prod
Dev Deployment (dev-qa-tenant, Draft)
# 1. Activate dev-qa-tenant
orchestrate env activate dev-qa-tenant

# 2. Deploy flows (if any)
orchestrate tools import -k flow -f tools/document_processing/workflow.py

# 3. Deploy knowledge-bases (if any)
orchestrate knowledge-bases import -f knowledge-bases/hr_policy_docs.yaml

# 4. Deploy agent (tools auto-deploy via agent's tools: section)
orchestrate agents import -f agents/employee_onboarding/agent.yaml
# - Agent will be in Draft state in dev-qa-tenant
​
Complete Deployment Script Example
#!/bin/bash
set -e

# Deployment script for a specific environment
ENVIRONMENT=$1  # dev, qa, preprod, or prod
BRANCH=$(git branch --show-current)

echo "Deploying branch: $BRANCH to environment: $ENVIRONMENT"

# Determine tenant based on environment
if [ "$ENVIRONMENT" = "dev" ] || [ "$ENVIRONMENT" = "qa" ]; then
  TENANT="dev-qa-tenant"
elif [ "$ENVIRONMENT" = "preprod" ] || [ "$ENVIRONMENT" = "prod" ]; then
  TENANT="prod-tenant"
else
  echo "Invalid environment: $ENVIRONMENT"
  exit 1
fi

echo "Activating tenant: $TENANT"
orchestrate env activate $TENANT

# Deploy all knowledge-bases (affects both Draft and Live)
echo "Deploying knowledge-bases (affects both Draft and Live)..."
for kb_file in knowledge-bases/*.yaml; do
  if [ -f "$kb_file" ]; then
    kb_name=$(basename "$kb_file")
    echo "Deploying knowledge-base: $kb_name"
    orchestrate knowledge-bases import -f "$kb_file"
  fi
done

# Deploy all flows from tools/ directory (other tools auto-deploy via agents)
echo "Deploying flows..."
for tool_dir in tools/*/; do
  tool_name=$(basename "$tool_dir")
  if [ -f "$tool_dir/workflow.py" ]; then
    echo "Deploying flow: $tool_name"
    orchestrate tools import -k flow -f "$tool_dir/workflow.py"
  fi
done

# Deploy all agents (tools auto-deploy based on agent's tools: section)
echo "Deploying agents..."
for agent_dir in agents/*/; do
  agent_name=$(basename "$agent_dir")
  if [ -f "$agent_dir/agent.yaml" ]; then
    echo "Deploying agent: $agent_name"
    if [ "$ENVIRONMENT" = "dev" ] || [ "$ENVIRONMENT" = "preprod" ]; then
      # Deploy to Draft environment
      orchestrate agents import -f "$agent_dir/agent.yaml"
    elif [ "$ENVIRONMENT" = "qa" ] || [ "$ENVIRONMENT" = "prod" ]; then
      # Promote from Draft to Live
      orchestrate agents deploy --name "$agent_name"
    fi
  fi
done

echo "Note: Tools are automatically deployed when agents reference them in tools: section"

echo "Deployment to $ENVIRONMENT ($TENANT) completed successfully!"
​
Usage
# Deploy develop branch to dev environment
./deploy.sh dev

# Deploy qa-1.2.0 branch to qa environment
./deploy.sh qa

# Deploy staging-1.2.0 branch to staging environment
./deploy.sh staging

# Deploy main branch to prod environment
./deploy.sh prod
​
Key Differences by Tenant
Aspect	dev-qa-tenant	prod-tenant
Activation	orchestrate env activate dev-qa-tenant	orchestrate env activate prod-tenant
Environments	Draft (Dev), Live (QA)	Draft (PreProd), Live (Prod)
Credentials	Dev/QA API keys	Prod API keys
Connections	connections/dev-qa-tenant/	connections/prod-tenant/
Approval	Automated	Requires CAB approval
​
Additional CLI Commands
List agents
Export agent
Delete agent
List tools
Export tool
orchestrate agents list
For complete CLI documentation, see the watsonx Orchestrate developer documentation.
​
11) Summary
​
Core Principles
Apply GitOps principles by using Git branches for versioning instead of manual version directories
Replace Argo CD with a Jenkins multi-branch pipeline as the orchestrator
Use the wxO CLI to deploy agents, flows, tools, and knowledge bases through orchestrate commands
Keep agent YAML files hand-written and stored in Git
Treat knowledge bases as tenant-scoped and not environment-scoped
Maintain secret-free Git through connections.template.yaml plus secret substitution at deploy time
Achieve traceable promotions through Git merges, safe rollbacks through Git reverts, and consistent deployments across environments without direct cluster access
​
Git-Based Versioning
Git branches represent environment state such as dev, qa, preprod, and prod
Git tags mark deployments such as v1.2.3-dev and v1.2.3-qa
Git merges promote code between environments
No manual version management is required because Git handles versioning
Natural evolution is possible because agent structures can change between environments
​
Two-Tenant Architecture
Tenant 1
Tenant 2
dev-qa-tenant for non-production workloads
Draft → Dev (develop)
Live → QA (qa-<version>)
​
Key Benefits
Complete Isolation
Production infrastructure remains separated from development and testing
Security
Different credentials, RBAC, and network policies per tenant
Compliance
Separate audit trails for production and non-production
Risk Mitigation
Issues in Dev or QA cannot impact PreProd or Prod
Flexibility
Each tenant can have different configurations, quotas, and policies
Simplified Versioning
Git branches and tags replace manual version directories
Natural Evolution
Code structure can evolve through branches
Easy Comparison
git diff shows exactly what will be promoted
​
Promotion Path
develop → dev-qa-tenant Draft
  ↓ (PR: develop → qa-<version>)
qa-<version> → dev-qa-tenant Live
  ↓ (PR: qa-<version> → staging-<version>) ← CROSS-TENANT BOUNDARY
staging-<version> → prod-tenant Draft
  ↓ (PR: staging-<version> → main)
main → prod-tenant Live (PRODUCTION)

Git Tags:
v1.2.3-dev → v1.2.3-qa → v1.2.3-staging → v1.2.3-prod
​
Critical Cross-Tenant Transition
The qa-<version> → staging-<version> merge is the critical boundary where:
The pipeline switches from dev-qa-tenant authentication to prod-tenant
API endpoints and credentials change
Configuration files such as tenant.yaml and values.yaml may require conflict resolution
Additional approval gates apply
Production-grade validation begins
​
Implementation Checklist
Provision two wxO tenants: dev-qa-tenant and prod-tenant
Set up Git repository with protected branches: develop, qa-*, staging-*, and main
Configure branch protection rules and approval requirements
Set up tenant-specific secrets in the secret manager
Configure Jenkins multi-branch pipeline
Configure Jenkins with tenant-aware credentials
Create tenant-specific connection templates
Implement approval gates for cross-tenant promotions
Set up Git tagging automation in Jenkins
Set up monitoring and alerting per tenant
Document merge conflict resolution strategy
Document runbooks for each tenant
Train the team on the versioned branch workflow
Train the team on rollback procedures

---

CI/CD Deployment
wxO CI/CD Deployment Approach (Part 4)
Summary of core principles, Git-based versioning, two-tenant architecture, and implementation checklist for wxO CI/CD

​
Summary
​
Core Principles
Apply GitOps principles using Git branches for versioning instead of manual version directories.
Replace Argo CD with Jenkins multi-branch pipeline as the orchestrator.
Use wxO CLI to deploy agents, flows, tools, and knowledge-bases via orchestrate commands.
Agent YAML files are hand-written (not CLI-generated) and stored in Git.
Knowledge-bases are tenant-scoped (not environment-scoped) and affect both Draft and Live environments simultaneously.
Maintain secret-free Git via connections.template.yaml + secrets manager substitution at deploy time.
Achieve traceable promotions via Git merges, safe rollbacks via Git reverts, and consistent deployments across environments without direct cluster access.
​
Git-Based Versioning
Git branches represent environment state (dev, qa, preprod, prod)
Git tags mark deployments (v1.2.3-dev, v1.2.3-qa, etc.)
Git merges promote code between environments
No manual version management: Git handles all versioning automatically
Natural evolution: Agent structures can change significantly between environments
​
Two-Tenant Architecture
Tenant 1
Tenant 2
dev-qa-tenant for non-production workloads
Draft environment → Dev (develop branch)
Live environment → QA (qa-<version> branches)
​
Key Benefits
Complete Isolation
Production infrastructure is completely separated from development/testing
Security
Different credentials, RBAC, and network policies per tenant
Compliance
Separate audit trails for production vs non-production
Risk Mitigation
Issues in Dev/QA cannot impact PreProd/Prod
Flexibility
Each tenant can have different configurations, quotas, and policies
Simplified Versioning
Git branches and tags replace manual version directories
Natural Evolution
Code structure can evolve naturally through branches
Easy Comparison
git diff shows exactly what will be promoted
​
Promotion Path (Git Branch Merging)
develop → dev-qa-tenant Draft
  ↓ (PR: develop → qa-<version>)
qa-<version> → dev-qa-tenant Live
  ↓ (PR: qa-<version> → staging-<version>) ← CROSS-TENANT BOUNDARY
staging-<version> → prod-tenant Draft
  ↓ (PR: staging-<version> → main)
main → prod-tenant Live (PRODUCTION)

Git Tags:
v1.2.3-dev → v1.2.3-qa → v1.2.3-staging → v1.2.3
​
Critical Cross-Tenant Transition
The qa-<version> → staging-<version> merge is the critical boundary where:
Git merge switches from dev-qa-tenant to prod-tenant
Pipeline switches authentication and API endpoints
Config files (tenant.yaml, values.yaml) may have merge conflicts (keep staging’s config)
Additional approval gates are enforced
Production-grade validation begins
​
Implementation Checklist
Provision two wxO tenants (dev-qa-tenant, prod-tenant)
Set up Git repository with protected branches (develop, qa-, staging-, main)
Configure branch protection rules and approval requirements
Set up tenant-specific secrets in secrets manager
Configure Jenkins multi-branch pipeline
Configure Jenkins with tenant-aware credentials
Create tenant-specific connection templates
Implement approval gates for cross-tenant promotions (qa-* → staging-*)
Set up Git tagging automation in Jenkins
Set up monitoring and alerting per tenant
Document merge conflict resolution strategy
Document runbooks for each tenant
Train team on versioned branch workflow (qa-<version>, staging-<version>)
Train team on rollback procedures (git revert, git reset)

---

Get Started
Examples
In the IBM watsonx Orchestrate ADK official repository, you can find pre-built examples of agents and tools located in the examples folder.
To import the examples of this folder on your local environment:
1
Download the examples

Download the example files to your local computer. You can do this by downloading the entire repository or by copying and creating each file individually.
2
Activate your environment

Activate your local environment to import the agent and tool examples.
BASH
orchestrate env activate local
3
Deploy the examples

Deploy the pre-built examples of agents and tools by running the import-all.sh script.
4
Use the agent and tool examples

Start the watsonx Orchestrate Developer Edition chat and use your imported agents and tools.
BASH
orchestrate chat start

---

Configuring environments
Configure access to remote environments
The watsonx Orchestrate ADK introduces environments (env), which represent instances of watsonx Orchestrate you can access.
Environments can be:
Local: Running on your laptop using the Developer Edition of watsonx Orchestrate.
Remote: Hosted on IBM Cloud, AWS, or on-premises using Cloud Pak for Data.
When you activate an environment, all commands, except orchestrate server and orchestrate chat, target that environment. This includes importing, listing, and removing agents, tools, and connections.
​
Environment commands
​
Adding an environment
Use the orchestrate env add command to add a remote environment to your local CLI. To learn where to find your service instance url and api key see Getting credentials for your environments.
BASH
orchestrate env add -n <environment-name> -u <your-instance-url>  
Note:
You can set any name you prefer for the environment.
When you use a HIPAA‑regulated cluster, you must include the --iam-url parameter.
Example:
BASH
orchestrate env add -n <onprem-environment-name> --iam-url https://api.us-east-1-reg.watson-orchestrate.ibm.com -u <watsonxorchestrateinstance>
For on-premises environments, you can ignore invalid SSL certificates, if your environment uses a self-signed certificate:
BASH
orchestrate env add -n <onprem-environment-name> -u <your-instance-url> --insecure
Show command flags

​
Activating an environment
Use the orchestrate env activate command to authenticate against a given environment and target all commands other than orchestrate server and orchestrate chat to that environment.
Note: Authentication against a remote environment expires every two hours. After expiration, you need to run orchestrate env activate again. This behavior does not exist in the local environment.
To interactively activate an environment:
BASH
orchestrate env activate <environment-name>
Please enter WXO API key: 
To non-interactively log in for scripting, use the following:
BASH
orchestrate env activate <environment-name> --api-key <your-api-key>
For on-premises environments:
BASH
orchestrate env activate <onprem-environment-name> --username=<username> --password=<password>
You can also use an api-key in the on-premises environment:
BASH
orchestrate env activate <onprem-environment-name> --username=<username> --api-key=<api-key>
Show command flags

​
Listing all environments
Use the orchestrate env list command to list all environments currently available to your CLI.
By default, you have one known as local. Your local environment refers to the watsonx Orchestrate Development Edition server. Others can be added by using the orchestrate env add command. The currently active environment will be indicated by an indicator saying (active) at the end of the line.
BASH
orchestrate env list
​
Removing an environment
Use the orchestrate env remove command to remove an environment from your environment list.
BASH
orchestrate env remove -n <environment-name>
​
Important configuration files
The watsonx Orchestrate CLI maintains two configuration files which are manipulated by the above env commands.
The first is ~/.config/orchestrate/config.yaml. This configuration file records each of your environments as well as which environment is currently active.
The second is ~/.cache/orchestrate/credentials.yaml. This file contains the JWT token from your last env activation used to authenticate with your environment.


---

Configuring environments
Getting credentials for your environments
To change your environments in the ADK, you must provide the ADK with your service instance URL and your watsonx Orchestrate API key. Currently, watsonx Orchestrate as a service (SaaS) is deployed in both IBM Cloud and AWS. Depending on which environment you have a valid account, the process to retrieve this information can vary.
​
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
​
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
​
On-premises
For on-premises environments, you can authenticate using one of two methods:
API Key
Use the API key that authenticates your user in the on-premises watsonx Orchestrate environment.
Username and Password
Use your username and password credentials to authenticate in the on-premises watsonx Orchestrate environment.
Note: You can only use one authentication method at a time. If you try to authenticate using both methods simultaneously, an authentication error occurs.


---

Configuring environments
Operating in an air-gapped environment
Using the ADK in an air-gapped environment introduces additional challenges that you need to address:
The ADK Python package is hosted on PyPI, which is inaccessible in an air-gapped environment.
By default, watsonx Orchestrate pulls packages from PyPI when installing Python tools.
Python tool dependencies are installed server-side at deployment time, not during tool import. This means your internal registry must be accessible from watsonx Orchestrate when tools are deployed. For comprehensive information on dependency management, see Python dependency management.
​
Prerequisites
As a site administrator, you need:
Access to a jumpbox that connects to both the internet and your Cloud Pak for Data cluster
A locally hosted Python package registry accessible from your internal network (common PyPI registry providers include Artifactory and Sonatype Nexus)
​
Uploading the ADK to your local PyPI registry
1
Get the dependencies list

On your jumpbox, run the following commands to get the full list of dependencies and generate wheel files for each ADK dependency:
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create a UV Virtual environment
uv venv adk --seed --python=3.12
source adk/bin/activate

pip install ibm-watsonx-orchestrate==<supported_version>
pip freeze > requirements.txt
mkdir dependencies
cd dependencies
pip wheel -r ../requirements.txt
2
Upload wheel files

Upload all generated wheel files from the dependencies directory to your local PyPI registry provider.
​
Configuring Python tool imports
To import Python tools successfully, configure watsonx Orchestrate to pull the ADK from your local registry.
All Python tools must be imported with a requirements.txt file that contains at least the following:
--extra-index-url https://my-pypi-registry
ibm-watsonx-orchestrate==<supported_version>
# Optional: Add other dependencies
my-dependency==dependency-version
Important: Use --extra-index-url, --index-url, or -i to configure your internal registry. When watsonx Orchestrate detects any of these flags, it automatically removes public PyPI access and pulls packages only from your internal registry. This ensures security compliance in air-gapped environments.
Any dependencies other than the ADK that you want to use in your tools must also be uploaded to your PyPI registry by the site administrator. Remember that dependencies are installed server-side when tools are deployed, so your registry must remain accessible from watsonx Orchestrate.
​
Best practices for air-gapped deployments
Pin all dependency versions to ensure reproducible builds:
ibm-watsonx-orchestrate==2.4.0
requests==2.32.3
pydantic==2.8.2
Use hash verification for maximum security:
pip-compile --generate-hashes requirements.in -o requirements.txt
Lock your internal registry to prevent package changes between environments
For detailed guidance on enterprise dependency patterns, see Python dependency management.
​
Related resources
For version compatibility information, see the On-premises compatibility
For general environment setup, see Initiate environment

---

Configuring environments
IBM Software Hub compatibility
This page provides version compatibility information for the watsonx Orchestrate ADK when deployed on IBM Software Hub (on-premises).
​
Overview
When deploying watsonx Orchestrate on IBM Software Hub, it’s essential to use the correct ADK version that corresponds to your IBM Software Hub version. This ensures optimal performance and compatibility.
For air-gapped environment setup instructions, see Operating in an air-gapped environment.
​
Compatibility matrix
The following table shows the supported ADK versions for each IBM Software Hub release:
Release Date	IBM Software Hub Version	ADK Version	Standard Environment	Air-Gapped Environment
30 June, 2025	5.2.0	1.6.2	Supported	Not supported
30 July, 2025	5.2.0.1	1.6.x	Supported	Not supported
27 August, 2025	5.2.1	1.8.x	Supported	Contact IBM support
30 October, 2025	5.2.2	1.12.x	Supported	Supported
15 December, 2025	5.3.0	1.14.x	Supported	Supported
26 February, 2026	5.3.1	2.3.x	Supported	Supported
13 April, 2026	5.3.1 Patch 2	2.7.x	Supported	Supported
21 May, 2026	5.3.1 Patch 5	2.10.x	Supported	Supported
17 June, 2026	5.4.0	2.11.x	Supported	Supported
​
Version selection guidelines
When selecting an ADK version:
Match your IBM Software Hub version: Always use the ADK version that corresponds to your IBM Software Hub deployment
Check air-gapped support: If operating in an air-gapped environment, verify that your IBM Software Hub version supports it
Apply patches: For patch releases, use the specified ADK version to ensure compatibility with bug fixes and improvements
Using an incompatible ADK version may result in unexpected behavior or functionality issues. Always verify version compatibility before deployment.
​
Installing the ADK
To install a specific ADK version:
pip install ibm-watsonx-orchestrate==<version>
Replace <version> with the appropriate version from the compatibility matrix (e.g., 2.13.0).
​
Related resources
Operating in an air-gapped environment
Initiate environment
Installing the ADK

---

Get Started
Useful CLI commands
​
Checking the ADK version
To check the currently installed version of the ADK, use the --version flag.
Example
BASH
orchestrate --version
​
Getting help with commands
Use the --help flag to get more information about a command and its available flags.
To use it, simply add —help after the command you want to learn more about.
Example
Example 1
Example 2
Example 3
Example 4
BASH
orchestrate --help
​
Running commands in debug mode
If you want more detailed output when running a command, use the --debug flag. This runs the command in debug mode and provides additional diagnostic information.
Add —debug before the command you want to run.
Example
Example 1
Example 2
Example 3
BASH
orchestrate --debug env activate local
​
Settings
ADK opens many files—such as Python, JSON, and YAML—to build agents, tools, knowledge bases, and more. You can override the encoding method ADK uses to decode files when automatic detection fails.
Note:
You don’t need to configure the encoding type to use ADK. The following commands are optional and help handle specific edge cases.
​
Setting an encoding Type
Set the encoding type ADK uses for file access. If unset, ADK tries to detect the encoding of each file.
To set the encoding type, use the command:
BASH
orchestrate settings set-encoding <encoding-type>
​
Setting encoding to default
Unset the encoding override and return to the default behavior, where ADK tries to detect the encoding of each file.
To set the encoding type to default, use the command:
BASH
orchestrate settings unset-encoding

---

