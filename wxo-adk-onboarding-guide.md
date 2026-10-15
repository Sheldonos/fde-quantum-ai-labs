# watsonx Orchestrate ADK — New Teammate Onboarding Guide

> **Time to complete:** approximately 30 minutes (active setup time; provisioning may add 5–10 minutes)

---

## Table of Contents

1. [Phase 1 — IBMid Account](#phase-1--ibmid-account)
2. [Phase 2 — IBM Cloud Setup](#phase-2--ibm-cloud-setup)
3. [Phase 3 — watsonx Orchestrate Setup](#phase-3--watsonx-orchestrate-setup)
4. [Phase 4 — ADK Installation](#phase-4--adk-installation)
5. [Phase 5 — Connect to IBM Bob](#phase-5--connect-to-ibm-bob)
6. [Phase 6 — First Agent (Hello World)](#phase-6--first-agent-hello-world)
7. [Troubleshooting](#troubleshooting)

---

## Phase 1 — IBMid Account

### What is an IBMid?

An **IBMid** is IBM's Single Sign-On (SSO) identity for all IBM SaaS products. One IBMid credential grants you access to IBM Cloud, watsonx, IBM Bob, and every other IBM-managed platform without creating separate accounts per service.

### Steps

1. Open a browser and navigate to **https://ibm.com/account**.

2. Click **Create an IBMid** if you are new, or **Log in** if you already have one.
   - *Screenshot description:* The IBM account page shows a centered card with "IBMid" in the header, an email input field, and two buttons: "Create an IBMid" (blue, primary) and "Log in" (white, secondary).

3. Fill in the registration form:
   - **First name**, **Last name**
   - **Email address** — use your `@ibm.com` address for internal access
   - **Password** — must meet IBM's 12-character complexity policy

4. Click **Create account**. IBM will send a **verification email** to the address you provided.

5. Open the verification email and click the **Verify email** link.
   - *Screenshot description:* Email from `no-reply@ibm.com` with subject "Verify your IBMid email address" showing a blue "Verify" button.

6. If prompted, set up **Multi-Factor Authentication (MFA)**:
   - IBM recommends the **IBM Verify** app (iOS / Android) or **TOTP** via Google Authenticator.
   - Scan the QR code displayed on screen and enter the 6-digit code to confirm.

> ✅ **Confirmation:** After verifying your email and completing MFA setup, you will be redirected to the IBM account dashboard at `https://myibm.ibm.com`. Your IBMid is now active.

---

## Phase 2 — IBM Cloud Setup

### Steps

1. Navigate to **https://cloud.ibm.com** and sign in with your IBMid.

2. **Select or create an account type:**
   - If you are joining an existing IBM team account, ask your account administrator to invite your IBMid. You will receive an invitation email.
   - If you are setting up independently, click **Create a free account** on the Cloud dashboard.
   - For production workloads, upgrade to a **Pay-As-You-Go** account via **Manage → Account → Account type**.

   > ⚠️ **Warning:** The **Lite** (free) tier of watsonx Orchestrate is restricted to the **Dallas (us-south)** region. If you need Frankfurt, London, or Tokyo, you must upgrade to a paid tier.

3. From the IBM Cloud top navigation, click **Catalog** (or use the search bar at the top of the page).

4. In the catalog search box, type **`watsonx Orchestrate`** and press Enter.
   - *Screenshot description:* The catalog page shows a grid of IBM service tiles. After searching, a single tile labeled "watsonx Orchestrate" with the IBM watsonx logo appears in the results.

5. Click the **watsonx Orchestrate** tile to open the provisioning page.

6. **Configure your instance:**
   - **Region:** Select `Dallas (us-south)` for Lite, or your preferred region for paid tiers.
   - **Plan:** Select `Lite` (free, Dallas only) or `Plus` (paid).
   - **Service name:** Accept the auto-generated name or type a descriptive one (e.g., `wxo-prod-us-south`).
   - **Resource group:** Select `Default` or your team's resource group.

7. Click **Create**. Provisioning typically takes 1–3 minutes.

8. After provisioning, you will be redirected to the **Resource details** page. Locate the **Manage** tab:
   - **CRN (Cloud Resource Name):** A long string starting with `crn:v1:bluemix:public:ai-assistant:...` — copy and save this.
   - **Service URL:** Shown as `https://api.<region>.watsonx-orchestrate.cloud.ibm.com` — copy and save this.

   > ✅ **Confirmation:** Both the CRN and Service URL are visible under **Manage → Overview**. You will need these in Phase 4.

---

## Phase 3 — watsonx Orchestrate Setup

### Steps

1. Navigate to **https://cloud.ibm.com/resources** (IBM Cloud Resource List).

2. Expand the **AI / Machine Learning** section. Locate your watsonx Orchestrate instance and click its name.

3. On the instance page, click **Launch watsonx Orchestrate**. The Orchestrate UI will open in a new tab at a URL such as:
   ```
   https://<region>.watsonx-orchestrate.cloud.ibm.com
   ```

4. Complete the **onboarding wizard** on first launch:
   - **Display name:** Enter your name or your team's bot name.
   - **Timezone:** Select your local timezone from the dropdown.
   - Click **Get started**.

5. **Generate a Service API Key:**
   - In the Orchestrate UI left sidebar, navigate to **Settings** (gear icon) → **API Keys**.
   - Click **Generate API key**.
   - Give it a name (e.g., `adk-local-dev`).
   - **Copy the API key immediately** — it will not be shown again.
   - Save it securely (e.g., in a password manager or `.env` file that is `.gitignore`d).

   > ⚠️ **Warning:** This must be a **Service credential** API key generated inside the Orchestrate Settings UI. Do **not** use your personal IBMid API key from IBM Cloud IAM — the ADK requires service-scoped credentials.

6. **Confirm model access:**
   - In the Orchestrate UI, navigate to **Settings → Connections**.
   - Verify that at least one LLM is listed as available.
   - For **Lite tier**, confirm **`granite-3-3-8b-instruct`** is visible and shows a green "Connected" status.

   > ✅ **Confirmation:** You should see `granite-3-3-8b-instruct` (or a similar Granite model) listed as available under Connections. This is the default reasoning model for Lite instances.

---

## Phase 4 — ADK Installation

### Prerequisites

Before running any install commands, confirm the following are installed and running on your machine:

| Requirement | Minimum Version | Check Command |
|---|---|---|
| Python | 3.11+ | `python3 --version` |
| pip | 23+ | `pip --version` |
| Docker Desktop | Latest stable | `docker info` |

> ⚠️ **Warning:** Docker Desktop **must be running** before you use `orchestrate app run`. If Docker is not running, the ADK will fail with a connection error. Start Docker Desktop from your Applications menu and wait for the whale icon to appear in the system tray.

### Steps

1. **Install the ADK package:**

   ```bash
   pip install ibm-watsonx-orchestrate==2.14.0
   ```

   > ✅ **Recommended:** Pin to `==2.14.0` to ensure reproducibility. Check [PyPI](https://pypi.org/project/ibm-watsonx-orchestrate/) for the latest stable release.

2. **Verify the installation:**

   ```bash
   orchestrate --version
   ```

   Expected output:
   ```
   ibm-watsonx-orchestrate, version 2.14.0
   ```

3. **Confirm the developer edition tooling is available:**

   ```bash
   orchestrate app status
   ```

   Expected output (Docker must be running):
   ```
   Developer Edition services: stopped
   Use 'orchestrate app run' to start them.
   ```

   > ✅ If you see `Developer Edition services: stopped` or `running`, the tooling is installed correctly. If you see `command not found`, re-run the pip install and ensure your Python `bin` directory is on your `$PATH`.

4. **Configure your environment:**

   Replace `<region>` with your instance region (e.g., `us-south`, `eu-de`, `eu-gb`, `jp-tok`) and `<YOUR_API_KEY>` with the Service API key you generated in Phase 3.

   ```bash
   orchestrate env add --name prod \
     --url https://api.<region>.watsonx-orchestrate.cloud.ibm.com \
     --api-key <YOUR_API_KEY>
   ```

   **Activate the environment:**

   ```bash
   orchestrate env activate prod
   ```

   **Verify the active environment:**

   ```bash
   orchestrate env list
   ```

   Expected output:
   ```
   NAME    URL                                                          ACTIVE
   prod    https://api.us-south.watsonx-orchestrate.cloud.ibm.com     *
   ```

   > ✅ **Confirmation:** The `*` next to `prod` confirms it is the active environment. All subsequent `orchestrate` CLI commands will target this instance.

---

## Phase 5 — Connect to IBM Bob

### What is IBM Bob?

IBM Bob is IBM's AI-powered coding partner. The `wxo-adk-mentor` mode turns Bob into a specialized watsonx Orchestrate ADK expert — capable of teaching concepts, generating agents, reviewing YAML, and running publish sequences.

### Steps

1. Open **IBM Bob** in your browser:
   - **Internal IBM link:** https://ibmbob.ibm.com
   - Sign in with your **IBMid** (the same credential from Phase 1).

2. After signing in, you will land on the Bob workspace. In the **mode selector** (bottom-left or top of the chat panel), click the current mode name to open the mode switcher.

3. Search for or scroll to **`wxo-adk-mentor`** and click to activate it.

   > ⚠️ **Warning:** If `wxo-adk-mentor` is not visible in the mode list, the custom mode file may not have been loaded. See the [Troubleshooting](#troubleshooting) section — "Bob mode not visible".

4. **Confirm the three WxO ADK modes are visible** in the mode selector:
   - `wxo-adk-mentor` — orchestration and guidance mode
   - `wxo-adk-learn` — step-by-step learning mode (concepts and walkthroughs)
   - `wxo-adk-vibe` — vibe coding mode (generate agents from plain English)

5. **Run your first smoke test.** With `wxo-adk-mentor` active, type the following in the Bob chat:

   ```
   I want to learn watsonx Orchestrate ADK
   ```

   > ✅ **Confirmation:** Bob should respond with a structured learning roadmap covering ADK concepts, tool registration, agent YAML, and deployment workflows. If Bob responds generically without ADK-specific guidance, the mode did not activate correctly — switch modes again using the mode selector.

---

## Phase 6 — First Agent (Hello World)

### Steps

1. In Bob's mode selector, switch from `wxo-adk-mentor` to **`wxo-adk-vibe`** (vibe coding mode).

2. Type the following prompt:

   ```
   Build me a Hello World agent
   ```

3. Bob will generate a complete Hello World agent scaffold. Expect output containing at minimum:

   **`agent.yaml`**
   ```yaml
   spec_version: v1
   style: default
   name: hello-world-agent
   description: A simple Hello World agent for watsonx Orchestrate ADK.
   instructions: |
     You are a friendly assistant. When the user greets you,
     respond with a warm Hello World message and ask how you can help.
   tools:
     - hello_world_tool
   ```

   **`tools.py`**
   ```python
   from ibm_watsonx_orchestrate.agent_builder.tools import tool

   @tool
   def hello_world_tool() -> str:
       """Returns a Hello World greeting."""
       return "Hello, World! Welcome to watsonx Orchestrate ADK."
   ```

4. Save both files to a local project directory, for example `~/wxo-hello-world/`.

5. **Publish the agent** using the ADK CLI sequence Bob provides. The standard publish sequence is:

   ```bash
   # Start the Developer Edition locally (requires Docker Desktop running)
   orchestrate app run

   # In a new terminal, import and publish the agent
   orchestrate agents import -f agent.yaml
   orchestrate tools import -f tools.py
   ```

6. **Open Studio to test:**
   - In the Orchestrate UI, navigate to **Studio** (left sidebar).
   - Find `hello-world-agent` in the agent list.
   - Click **Test** and type: `Hello`
   - The agent should respond: `Hello, World! Welcome to watsonx Orchestrate ADK.`

   > ✅ **Confirmation:** A successful response in the Studio test panel confirms your first agent is fully deployed and functional.

---

## Troubleshooting

### IBMid Login Loop (browser keeps redirecting back to login)

**Symptoms:** After entering correct credentials, the page refreshes and asks you to log in again.

**Fix:**
1. Clear all browser cookies and site data for `ibm.com` and `cloud.ibm.com`.
2. Open a new **incognito / private browsing** window.
3. Navigate directly to https://cloud.ibm.com and sign in.
4. If the issue persists, try a different browser (Chrome vs. Firefox vs. Edge).
5. If using a corporate proxy or VPN, try disabling it temporarily — some proxies strip session cookies.

---

### Orchestrate Lite Region Restriction (provisioning fails outside Dallas)

**Symptoms:** When creating a watsonx Orchestrate instance, the Lite plan is greyed out for all regions except Dallas.

**Fix:**
- The Lite (free) plan is **only available in `us-south` (Dallas)**. This is a platform-level restriction.
- If you need another region (Frankfurt `eu-de`, London `eu-gb`, Tokyo `jp-tok`), you must upgrade your IBM Cloud account to **Pay-As-You-Go** and select the **Plus** plan.
- Contact your IBM account team or manager for access to a funded team account if you cannot upgrade independently.

---

### `orchestrate app run` Docker Errors

**Symptoms:**
```
Error response from daemon: Cannot connect to the Docker daemon at unix:///var/run/docker.sock
```
or
```
docker: command not found
```

**Fix:**
1. Confirm Docker Desktop is **installed** — download from https://www.docker.com/products/docker-desktop/
2. **Start Docker Desktop** from your Applications / Start menu. Wait until the Docker whale icon in the system tray shows "Docker Desktop is running".
3. Run `docker info` in your terminal. You should see engine details without errors.
4. Re-run `orchestrate app run`.

> ⚠️ On macOS, Docker Desktop requires **at least 8 GB RAM** allocated in Docker Desktop → Settings → Resources. If the ADK containers crash silently, increase the memory limit.

---

### API Key Scope Errors

**Symptoms:**
```
Error: 403 Forbidden — insufficient scope
```
or
```
AuthorizationError: The API key provided does not have access to this resource.
```

**Fix:**
- The ADK requires a **Service API key** generated from inside the **watsonx Orchestrate UI** (Settings → API Keys), **not** a personal IBM Cloud IAM API key.
- IBM Cloud IAM API keys (generated at `cloud.ibm.com/iam/apikeys`) have different scopes and will fail with 403 errors on Orchestrate APIs.
- Go back to [Phase 3, Step 5](#steps-2) and regenerate a Service API key from the Orchestrate Settings panel.
- Re-run:
  ```bash
  orchestrate env add --name prod \
    --url https://api.<region>.watsonx-orchestrate.cloud.ibm.com \
    --api-key <NEW_SERVICE_API_KEY>
  orchestrate env activate prod
  ```

---

### Bob Mode Not Visible (`wxo-adk-mentor` missing from mode selector)

**Symptoms:** After opening IBM Bob, the modes `wxo-adk-mentor`, `wxo-adk-learn`, and `wxo-adk-vibe` do not appear in the mode switcher.

**Fix:**
1. **Restart Bob:** Close the Bob browser tab, wait 5 seconds, and reopen https://ibmbob.ibm.com.
2. **Check `custom_modes.yaml`:** The WxO ADK modes are defined in Bob's custom modes configuration file. Confirm the file exists and was saved correctly:
   ```bash
   cat ~/.bob/custom_modes.yaml | grep -A 2 "wxo-adk"
   ```
   You should see entries for `wxo-adk-mentor`, `wxo-adk-learn`, and `wxo-adk-vibe`.
3. **Re-save the file:** If the file is missing or malformed, re-apply the custom modes configuration. Contact your Bob workspace administrator or refer to the Bob custom modes documentation.
4. **Hard refresh:** In the Bob browser tab, press `Cmd+Shift+R` (macOS) or `Ctrl+Shift+R` (Windows/Linux) to force a full reload.

---

*Made with IBM Bob*
