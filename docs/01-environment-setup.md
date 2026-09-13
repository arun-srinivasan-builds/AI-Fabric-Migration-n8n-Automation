# Environment Setup

## 1. Development Environment

This project is being developed on a Windows laptop using a project-specific Python virtual environment.

### Project Location

```text
D:\Week3-Capstone-AI-Fabric-Migration
```

### Core Tools Verified

| Tool | Version / Status |
|---|---|
| Python | 3.11.9 |
| pip | 24.0 |
| Git | 2.55.0 |
| Visual Studio Code | 1.137.0 |
| Docker | 29.7.2 - Installed |
| WSL | Version 2 |
| Ubuntu | Default WSL Distribution |
| n8n | Self-hosted instance accessible |

---

## 2. Python Environment

A dedicated Python virtual environment was created inside the project directory.

Command:

```bash
python -m venv .venv
```

### Why Use a Virtual Environment?

A virtual environment isolates the Python packages required by this application from the system-wide Python installation.

This helps:

- Prevent dependency conflicts between projects
- Maintain project-specific package versions
- Improve reproducibility
- Keep the development environment clean

---

## 3. Virtual Environment Activation

Initial activation was attempted from the VS Code PowerShell terminal:

```powershell
.venv\Scripts\activate
```

PowerShell returned:

```text
Activate.ps1 cannot be loaded because running scripts is disabled
on this system.
```

This occurred because the Windows PowerShell execution policy prevented the activation script from running.

Rather than modifying the system execution policy, the VS Code terminal was switched to **Command Prompt**.

The environment was then activated using:

```cmd
.venv\Scripts\activate.bat
```

Successful prompt:

```text
(.venv) D:\Week3-Capstone-AI-Fabric-Migration>
```

Validation:

```cmd
python --version
pip --version
```

Result:

```text
Python 3.11.9
pip 24.0
```

pip was confirmed to be running from:

```text
D:\Week3-Capstone-AI-Fabric-Migration\.venv\Lib\site-packages
```

This confirms that the project-specific Python environment is active.

---

## 4. Git Configuration

Git was verified using:

```cmd
git --version
```

Result:

```text
git version 2.55.0.windows.3
```

Git identity was also verified using:

```cmd
git config --global user.name
git config --global user.email
```

The laptop is therefore ready for local version control and future GitHub publishing.

> The actual email address is intentionally not included in this documentation.

---

## 5. n8n Verification

The existing self-hosted n8n instance was successfully accessed from the laptop browser.

n8n will later be used in this project for:

- ETL automation
- Calling the Migration Assessment API
- Conditional routing
- High-risk assessment escalation
- Workflow orchestration

### Role of n8n in This Project

n8n will act as the **workflow orchestrator**.

It will not perform the core RAG-based migration analysis itself.

The overall responsibility will be separated as:

```text
n8n
  ↓
Workflow / ETL / Routing
  ↓
Python API
  ↓
RAG + LLM
  ↓
Migration Assessment
  ↓
n8n
  ↓
Business Action
```

---

## 6. Docker Status

Docker Desktop and Docker CLI are installed.

Docker version:

```text
Docker version 29.7.2
```

The following command was tested:

```cmd
docker info
```

The Docker client was available, but the Docker Desktop Linux engine was not running at the time of validation.

The error indicated that the Docker client could not connect to the Docker Desktop Linux engine.

Docker is **not required for the initial version of this Week 3 mini-capstone**, so no additional troubleshooting was performed.

This decision keeps the project focused on the main learning objectives:

- GenAI
- RAG
- FAISS
- API automation
- n8n ETL
- Workflow orchestration
- Slack integration

Docker can be introduced later if containerized deployment becomes useful.

---

## 7. Environment Readiness Result

The essential development environment required to begin the project is ready.

| Component | Status |
|---|---|
| Python | Ready |
| pip | Ready |
| VS Code | Ready |
| Python virtual environment | Ready |
| Git | Ready |
| WSL2 / Ubuntu | Ready |
| n8n | Ready |
| Docker | Installed - Optional |

### Final Environment Status

```text
Python Development Environment    READY
Git / Version Control             READY
VS Code Development               READY
Virtual Environment               READY
n8n Automation Platform           READY
Docker                            OPTIONAL
```

The laptop is ready to proceed with the **AI-Powered Fabric Migration Assessment** mini-capstone.

---

## 8. Key Learning

Environment preparation is an important part of application development.

Before building the GenAI application, we verified that the required development tools were available and that the Python application could run inside an isolated virtual environment.

We also encountered a PowerShell execution-policy restriction while activating the virtual environment.

Instead of changing the operating-system security configuration unnecessarily, we used the Command Prompt activation script.

This reinforced an important development principle:

> Fix only what is required for the application and avoid introducing unnecessary system-level changes.

The environment is now ready for application design and implementation.