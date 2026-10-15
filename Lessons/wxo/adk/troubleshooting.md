Release Notes
Troubleshooting
​
Installing the watsonx Orchestrate Developer Edition
You might encounter errors when installing the watsonx Orchestrate Developer Edition. To address the most common errors, see the following topics for solutions:
server start command fails with pull access denied

Try to log in manually with the following command:
docker login -u cp -p APIKEY cp.icr.io
If you manage to log in and the server still fails to start, locate the Docker config file. Usually, you find this file in ~/.docker/config.json. If it doesn’t exist, you can create it.
Add the following content to the file:
{
  "auths": {
    "us.icr.io": {
      "auth": "BASE64_ENCODED_APIKEY"
    }
  }
}
Where BASE64_ENCODED_APIKEY is the base64 encoded string of iamapikey:DOCKER_IAM_KEY.
Permission denied when trying to download Docker images

You get an error message such as the following one:
dial unix /var/run/docker.sock: connect: permission denied
This issue happens because the Docker daemon runs as a root-owned process that communicates through a Unix socket. You must have the necessary permissions to access this socket.
To solve this problem, follow these steps:
Add Docker to the group of users that can use sudo.
sudo usermod -aG docker $USER
Run the following command to log in to a new group:
newgrp docker
Check if your user belongs to the docker group:
groups
Try running Docker’s hello-world to check if you’re able to run Docker:
docker run hello-world
Document processing image not found during server startup

If you encounter an error when starting the server with document processing enabled (--with-doc-processing or -d), such as:
Error response from daemon: failed to resolve reference "registry.dl.watson-orchestrate.ibm.com/cp/wxo-lite/document-processing/wo_doc_processing_evaluation_pg_init:20260629-main-67-230c0a9":
registry.dl.watson-orchestrate.ibm.com/cp/wxo-lite/document-processing/wo_doc_processing_evaluation_pg_init:20260629-main-67-230c0a9: not found
This issue occurs when required document processing Docker images are not available in the registry. This can happen with certain versions or registry configurations.
To resolve this issue:
Verify your ADK version: Ensure you’re using the latest version of the ADK CLI:
orchestrate --version
Update to the latest version if needed:
pip install --upgrade ibm-watsonx-orchestrate
Reset and restart the server:
orchestrate server reset
orchestrate server start -e <path-.env-file> --with-doc-processing
Check your registry configuration: If you’re using a custom registry or on-premises setup, verify that all required images are available in your registry. Contact your administrator if images are missing.
Alternative workaround: If document processing is not critical for your current work, start the server without the -d or --with-doc-processing flag:
orchestrate server start -e <path-.env-file>
Note: Document processing requires additional system resources. Ensure your system meets the minimum requirements of 24 GB RAM when using this feature.
For Windows users, you might also encounter containerization issues as Windows systems do not support Docker natively.
No environment file

If you’re using Windows, you may have created your .env file on your local machine. To make it accessible within your Ubuntu environment in WSL, follow these steps:
Open File Explorer and enter the following path in the address bar, replacing yourUsername with your actual Linux username:
PATH
\\wsl.localhost\Ubuntu\home\yourUsername
Open another File Explorer window and navigate to the location where your .env file is saved.
Copy the .env file into your Linux home directory shown in the first window.
The Compose file is invalid because of unsupported variable types

If you get an error similar to this:
ERROR: The Compose file '/home/user/adktest/.venv/lib/python3.12/site-packages/ibm_watsonx_orchestrate/docker/compose-lite.yml' is invalid because:
services.wxo-server-worker.environment.DO_NOT_TRACK contains true, which is an invalid type, it should be a string, number, or a null
services.wxo-tempus-runtime.environment.REDIS_TLS contains false, which is an invalid type, it should be a string, number, or a null
services.wxo-server.environment.DO_NOT_TRACK contains true, which is an invalid type, it should be a string, number, or a null
services.socket-handler.build contains unsupported option: 'ssh'
services.wxo-server-worker.depends_on contains unsupported option: 'required'
services.wxo-server.depends_on contains unsupported option: 'required'
That’s because you’re using an older version of Docker Compose (v1 instead of v2) that does not support some variable types.
To solve this issue, you must install Docker Compose v2.
On Ubuntu 24.04, for example, you can simply run the following commands:
sudo apt-get remove docker-compose
sudo apt-get install docker-compose-v2
Check your distribution repositories for the appropriate packages of Docker Compose v2.
Homebrew not installed in Ubuntu

If Homebrew is not installed in your Ubuntu distribution on WSL, you’ll need to install it manually:
Open Ubuntu via the Start Menu
Check if Homebrew is already installed:
BASH
brew --version
If you get a “command not found” error, proceed to the next step.
Install Homebrew:
BASH
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
Verify the installation path:
BASH
whereis brew
Note: The default location is usually /home/linuxbrew/.linuxbrew/bin/brew
Python not installed or incorrect version

The ADK supports Python 3.11 to Python 3.14. Follow these steps to configure Python 3.12:
Open Ubuntu via the Start Menu.
Check if Python 3.12 is installed:
BASH
python3.12 --version
If not installed, continue with the steps below.
Install Python 3.12 using Homebrew:
BASH
brew install python@3.12
Set Python 3.12 as the default:
BASH
ln -s /home/linuxbrew/.linuxbrew/opt/python@3.12/bin/python3.12 /home/linuxbrew/.linuxbrew/opt/python@3.12/bin/python
ln -s /home/linuxbrew/.linuxbrew/opt/python@3.12/bin/pip3.12  /home/linuxbrew/.linuxbrew/opt/python@3.12/bin/pip
echo 'export PATH="/home/linuxbrew/.linuxbrew/opt/python@3.12/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
Confirm the installation path:
BASH
whereis python3.12
Verify that Python 3.12 is now the default:
BASH
python --version
This should return the installed version of Python 3.12.
​
Managing connections for Python tools
There are many error messages that may occur when importing a Python tool with credentials (especially one with expected_credentials). Most serve to help guide the user in how to properly define their connections to work with their Python tool.
No app-id given

If no app-id is passed into a tool that has expected_credentials you see the following error:
BASH
[ERROR] - The tool 'my_sample_tool' requires an app-id 'my_app_id'. Please use the `--app-id` flag to provide the required app-id
To fix this, be sure to pass in the —app-id flag when importing the tool and make sure that the name is correct:
BASH
orchestrate tools import -k python -f <path to file> --app-id my_app_id
No connection exists

If you try to pass in a connection that doesn’t exist you see the following:
BASH
[ERROR] - No connection exists with the app-id 'my_app_id'
To fix this be sure that you create the connection before importing the tool:
BASH
orchestrate connections add --app-id my_sample_tool
Type Mismatch

If you specify an app id on a connection that is of a different type than what the tool specifies in expected_credentials you see the following:
BASH
[ERROR] - The app-id 'my_app_id' is of type 'basic_auth'. The tool 'my_sample_tool' expects this connection to be of type 'api_key_auth'. Use `orchestrate connections list` to view current connections and use `orchestrate connections add ` to create the relevant connection
To fix this remove the existing connection with that name and re-create it with the correct type. Or if that connection is used by a different tool that requires that type, create a new connection with a different name (my_app_id_2) and the correct type. Then import using an alias:
BASH
orchestrate tools import -k python -f <path to file> --app-id my_app_id=my_app_id_2
​
Remote MCP toolkits
The following sections describe errors that can occur when importing or executing remote MCP toolkits.
Toolkit import fails with CM-REFRESH-TOKEN-FAILED-001 (SSO/OBO connection)

When you import a remote MCP toolkit that is associated with an SSO/OBO (oauth_auth_on_behalf_of_flow) connection, the import fails with an error similar to the following:
ClientAPIException(status_code=500, message={"detail":"Failed to import tools from MCP server:
CM-REFRESH-TOKEN-FAILED-001: Unable to authenticate with the application.
Please try again. If this continues, ask your administrator to reauthorize the application connection."})
Cause
During toolkit import, watsonx Orchestrate calls the MCP server’s tools/list endpoint to discover available tools. If the toolkit is bound to an SSO/OBO connection, the platform attempts to obtain an access token from the identity provider. This token exchange requires an authenticated end-user session, which does not exist at import time. The identity provider therefore rejects the request and the import fails.
Resolution
Configure the draft and live environments with different connection kinds. Use key_value for draft (where the import happens) and keep SSO/OBO for live (where tool execution happens with a real user session):
BASH
# Create the connection
orchestrate connections add -a my_sso_obo_connection

# Configure draft with key_value (placeholder credentials are sufficient for tool discovery)
orchestrate connections configure -a my_sso_obo_connection \
    --env draft --type team --kind key_value
orchestrate connections set-credentials -a my_sso_obo_connection \
    --env draft -e "PLACEHOLDER=value"

# Configure live with SSO/OBO for authenticated tool execution
orchestrate connections configure -a my_sso_obo_connection \
    --env live --type member --kind oauth_auth_on_behalf_of_flow

# Import the toolkit — uses draft key_value connection and succeeds
orchestrate toolkits import -f my_toolkit.yaml -a my_sso_obo_connection
For more information, see Importing toolkits with SSO/OBO connections.
MCP tool execution fails with HTTP 431 (Request Header Fields Too Large)

When a user executes a remote MCP tool through the embedded chat or a Microsoft Teams channel, the call fails. The surface-level error shown to the user is:
500: Failed to execute MCP tool. Please check server availability.
The underlying error in platform logs is:
HTTP 431 - Request Header Fields Too Large
Cause
watsonx Orchestrate enforces an 8 KB per-header size limit as part of RFC 6585-compliant header size validation. During remote MCP tool execution with an SSO/OBO connection, the platform propagates the user’s access token in the x-wxo-access-token header. If your application injects many context variables into the JWT, the resulting access token can exceed this limit.
Resolution
Reduce the size of the JWT payload by removing context variables that are not needed by the agent or MCP tool. Common candidates for removal include internal system values, verbose metadata, or redundant fields added by the identity provider.
After pruning, verify that the x-wxo-access-token header stays below 8 KB. You can measure the JWT size by base64-decoding it and checking the payload byte length.
The 8 KB per-header limit applies to each individual header. If your use case requires a larger header, contact IBM support to evaluate configuration options.