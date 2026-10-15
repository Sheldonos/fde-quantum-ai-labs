Workspaces
Overview
Workspaces provide a structured way to organize and manage resources within an IBM Cloud environment. A workspace defines an isolated context where resources such as agents, tools, and toolkits are created and managed. It enables clear separation of resources while it maintains consistent workflows across environments. Each environment includes a global workspace by default. More workspaces can be created to support independent resource management. When you work within a workspace, all operations are scoped to that workspace context. Workspace functions are available through the orchestrate workspaces command group in the CLI. This command group provides capabilities to create, list, remove, activate, deactivate, and export workspaces, and manage workspace membership.
Workspaces are supported only for IBM Cloud environments.
​
Workspace context
A workspace must be activated to be used as the current working context. When activated, all subsequent CLI operations are run within that workspace. It includes creating, importing, updating, and listing resources. If no workspace is explicitly specified in a command, the active workspace is used by default.
​
Workspace management
Workspaces can be created or updated by using a single command. Listing workspaces returns all available workspaces within the tenant and indicates the currently active workspace. Workspaces can also be removed, with options to control how associated resources are handled. Workspaces can be exported into a ZIP file, which includes all resources within the workspace. It allows workspace resources to be packaged and reused.
​
Workspace membership
Workspaces support membership management to control access. Users can be added to a workspace with assigned roles. Supported roles include:
Owner – Full management access to the workspace, including managing members and workspace configuration
Editor – Access to use and interact with workspace resources Membership operations include adding or updating users, listing current members, and removing users from a workspace. When a workspace is active, membership commands operate on that workspace unless another workspace is specified.
​
Command structure
Workspace functions are organized under the following CLI structure:
orchestrate workspaces – Workspace lifecycle management
orchestrate workspaces members – Workspace membership management These commands provide a consistent interface for managing workspace configuration and access.

---

Workspaces
Workspace operations
Workspaces provide a way to organize and manage resources within an IBM Cloud environment. A workspace represents an isolated context where resources such as agents, tools, and toolkits can be created, managed, and accessed. Each environment includes a global workspace by default, and more workspaces can be created to segment resources and control access. All workspace operations are available through the orchestrate workspaces command group.
Workspaces are supported only for IBM Cloud environments.
​
Creating or updating a workspace
The orchestrate workspaces create command creates a new workspace or updates an existing one. If a workspace with the specified name exists, the command updates its description.
BASH
orchestrate workspaces create \
--name workspace_name \
--description "Workspace description"
Show command flags

​
Listing workspaces
The orchestrate workspaces list command lists all available workspaces and indicates which workspace is active.
BASH
orchestrate workspaces list
Show command flags

​
Removing a workspace
The orchestrate workspaces remove command deletes a workspace. Artifact handling behavior is controlled through command flags.
BASH
orchestrate workspaces remove \
--name workspace_name \
--delete-artifacts
Show command flags

​
Activating a workspace
The orchestrate workspaces activate command sets a workspace as the active context. All subsequent operations are run within this workspace.
BASH
orchestrate workspaces activate workspace_name
Show command flags

​
Deactivating a workspace
The orchestrate workspaces deactivate command resets the active context to the global workspace.
BASH
orchestrate workspaces deactivate
​
Exporting a workspace
The orchestrate workspaces export command exports all resources from a workspace into a ZIP file.
BASH
orchestrate workspaces export \
--name workspace_name \
--output workspace_export.zip
Show command flags

​
Managing workspace members
Workspace membership is managed by using the orchestrate workspaces members command group. These commands allow adding, listing, and removing users within a workspace. If no workspace name is provided, the active workspace is used.
​
Adding or updating a member
The orchestrate workspaces members add command adds a user to a workspace or updates their role.
BASH
orchestrate workspaces members add \
--user user@example.com \
--role owner \
--name workspace_name
Show command flags

​
Listing workspace members
The orchestrate workspaces members list command lists all members in a workspace.
BASH
orchestrate workspaces members list \
--name workspace_name
Show command flags

​
Removing a member
The orchestrate workspaces members remove command removes a user from a workspace.
BASH
orchestrate workspaces members remove \
--user user@example.com \
--name workspace_name
Show command flags

​
Workspace context
When a workspace is active, all resource operations are scoped to that workspace. Commands such as create, list, update, and delete operate within the active workspace context. If no workspace is explicitly specified in a command, the active workspace is used automatically.
To copy agents from another workspace, see Copy agents between workspaces.

---

