# Solution Architecture

## 1. Purpose

This document describes the final architecture of the **AI-Powered Fabric Migration Assessment Platform**.

The platform combines:

```text
Streamlit
+
n8n
+
FastAPI
+
RAG
+
FAISS
+
OpenAI Embeddings
+
GPT-4.1
+
Deterministic Guardrails
+
Slack
```

The main architectural principle is **separation of responsibilities**.

Each component performs a specific role rather than making one technology responsible for the complete application.

The final solution is best described as:

> A human-triggered, end-to-end automated AI migration assessment platform combining deterministic ETL, API-based orchestration, RAG-grounded AI reasoning, enterprise risk guardrails, operational Slack escalation, and interactive Streamlit reporting.

---

## 2. Final Solution Architecture

![AI-Powered Fabric Migration Assessment Platform - Solution Architecture](../assets/architecture/fabric-migration-architecture.png)

*Figure: End-to-end architecture showing Streamlit, n8n ETL and orchestration, FastAPI, RAG with OpenAI Embeddings and FAISS, GPT-4.1 assessment, deterministic safeguards, Slack escalation, and consolidated reporting.*

The complete application flow is:

```text
User
  ↓
Streamlit UI
  ↓
Upload One or More CSV Files
  ↓
Schema Validation
  ↓
Multi-File Consolidation
  ↓
n8n Webhook
  ↓
Extract from File
  ↓
ETL Cleaning & Standardization
  ↓
Structured Migration Workloads
  ↓
HTTP Request
  ↓
FastAPI /assess
  ↓
Create Retrieval Query
  ↓
OpenAI Embeddings
  ↓
FAISS Vector Search
  ↓
Relevant Microsoft Learn Context
  ↓
GPT-4.1 Initial Assessment
  ↓
Structured Output Validation
  ↓
Fabric Area Reliability Safeguard
  ↓
Enterprise Risk Guardrail
  ↓
Final Assessment
  ↓
n8n Risk Routing
  ↓
risk_level == High?
  ├── Yes → Slack Alert
  └── No  → Continue
  ↓
Convert Assessments to CSV
  ↓
Respond to Webhook
  ↓
Streamlit
  ↓
Risk Dashboard + Detailed Results + Download
```

---

## 3. Architecture Layers

The solution is organized into six logical layers:

```text
1. Presentation Layer
2. Automation & ETL Layer
3. API Layer
4. AI / RAG Layer
5. Reliability & Policy Layer
6. Notification & Reporting Layer
```

This separation makes it easier to understand where data preparation, AI reasoning, deterministic control, automation, and user interaction occur.

---

## 4. Presentation Layer

### Technology

```text
Streamlit
```

### Responsibilities

Streamlit provides the user-facing application.

It handles:

```text
Upload one or more migration inventory CSV files
Validate required columns
Consolidate valid CSV files
Preview input data
Display workload metrics
Trigger the assessment workflow
Display final assessment results
Highlight risk classifications
Show detailed workload assessments
Allow consolidated CSV download
```

Streamlit is intentionally **not responsible for migration reasoning or enterprise workflow orchestration**.

Its primary responsibilities are:

```text
User Interaction
+
Input Validation
+
Presentation
+
Reporting
```

---

## 5. Automation & ETL Layer

### Technology

```text
n8n
```

n8n acts as the central workflow orchestration layer.

### Responsibilities

```text
Receive the CSV through a webhook
Extract CSV records
Parse incoming data
Clean and normalize values
Convert data types
Prepare FastAPI payloads
Call FastAPI for each workload
Evaluate final risk
Send High-risk Slack alerts
Generate consolidated output CSV
Return the completed assessment to Streamlit
```

The workflow therefore connects:

```text
Streamlit
    ↓
n8n
    ↓
FastAPI
    ↓
AI Assessment
    ↓
n8n
   ↙   ↘
Slack  Report
```

---

## 6. Why ETL Happens Before AI

The migration inventory deliberately contains inconsistent values to simulate real enterprise data.

Examples include:

```text
HD insight
azure data factory
power bi

HIGH
MEDIUM
low

ADF; adls
```

The n8n ETL layer standardizes these values before they reach the AI system.

Examples:

```text
HD insight
→ HDInsight

azure data factory
→ Azure Data Factory

power bi
→ Power BI

HIGH
→ High

low
→ Low
```

Dependencies are converted from:

```text
ADF; adls
```

into structured data:

```json
[
  "ADF",
  "ADLS"
]
```

The architecture therefore follows:

```text
Raw Enterprise Data
        ↓
Deterministic ETL
        ↓
Clean Structured Data
        ↓
AI Assessment
```

This avoids using an LLM for transformations that deterministic ETL can perform more reliably.

---

## 7. Multi-File Architecture

The Streamlit application supports one or more migration inventory CSV files.

```text
CSV File 1
CSV File 2
CSV File 3
     ↓
Streamlit
     ↓
Schema Validation
     ↓
Consolidation
     ↓
Single Assessment Batch
     ↓
n8n
```

This keeps file-selection and user-interface concerns within Streamlit.

n8n receives a single consolidated batch and focuses on:

```text
ETL
Orchestration
API calls
Routing
Notifications
Report generation
```

---

## 8. Batch Processing Architecture

After the consolidated CSV reaches n8n:

```text
Consolidated CSV
       ↓
Extract from File
       ↓
ETL / Standardization
       ↓
Workload 1
Workload 2
Workload 3
...
Workload N
```

Each workload is independently submitted to:

```text
POST /assess
```

Conceptually:

```text
Workload 1 → FastAPI → Assessment 1
Workload 2 → FastAPI → Assessment 2
Workload 3 → FastAPI → Assessment 3
...
Workload N → FastAPI → Assessment N
```

The individual assessments are later consolidated into one final report.

---

## 9. API Layer

### Technology

```text
FastAPI
```

### Endpoint

```text
POST /assess
```

FastAPI exposes the Python migration intelligence as an HTTP service.

### Responsibilities

```text
Receive one structured migration workload
Build the retrieval query
Invoke the RAG pipeline
Generate the AI assessment
Validate structured output
Apply reliability safeguards
Apply enterprise risk guardrails
Return structured JSON
```

The API boundary separates the AI implementation from the workflow platform.

n8n does not need to understand how FAISS, embeddings, retrieval, or GPT are implemented.

It only needs the API contract:

```text
Migration Workload
       ↓
POST /assess
       ↓
Structured Assessment
```

---

## 10. AI / RAG Layer

The AI layer consists of:

```text
Microsoft Learn Knowledge
OpenAI Embeddings
FAISS
GPT-4.1
```

The runtime RAG flow is:

```text
Migration Scenario
       ↓
Retrieval Query
       ↓
OpenAI Embedding
       ↓
Query Vector
       ↓
FAISS Similarity Search
       ↓
Relevant Microsoft Learn Chunks
       ↓
Context + Migration Scenario
       ↓
GPT-4.1
       ↓
Initial Migration Assessment
```

---

## 11. Knowledge Base

The current knowledge base uses selected official Microsoft Learn documentation.

The sources cover guidance related to:

```text
Azure Data Factory migration planning
Azure Data Factory migration assessment
Synapse Spark migration
Fabric Data Factory migration best practices
```

Processed documents are stored under:

```text
knowledge/processed/
```

The FAISS index is stored under:

```text
knowledge/faiss_index/
```

Using authoritative Microsoft documentation provides stronger grounding than relying only on the model's general knowledge.

---

## 12. Knowledge Ingestion Architecture

Knowledge ingestion happens before runtime assessment.

```text
Microsoft Learn Web Pages
        ↓
requests + BeautifulSoup
        ↓
Clean Text
        ↓
Processed Text Files
        ↓
Chunking
        ↓
OpenAI Embeddings
        ↓
FAISS Index
```

Current chunk configuration:

```text
Chunk Size:     1000
Chunk Overlap:   150
```

The four processed documents produced:

```text
41 chunks
```

These chunks are embedded and stored in FAISS for semantic retrieval.

---

## 13. Embeddings and FAISS

The embedding model is:

```text
text-embedding-3-small
```

Its role is not to generate an assessment.

Its role is to convert text into vector representations.

At ingestion time:

```text
Document Chunk
      ↓
Embedding Model
      ↓
Vector
      ↓
FAISS
```

At runtime:

```text
Retrieval Query
      ↓
Embedding Model
      ↓
Query Vector
      ↓
FAISS Similarity Search
```

FAISS then returns the chunks most semantically relevant to the migration workload.

---

## 14. Retrieval Architecture

FastAPI constructs a retrieval query using fields such as:

```text
Source platform
Workload type
Dependencies
Current issues
Target platform
```

The runtime retrieval path is:

```text
Migration Workload
      ↓
Retrieval Query
      ↓
text-embedding-3-small
      ↓
Query Vector
      ↓
FAISS
      ↓
Top Relevant Chunks
      ↓
Retrieved Context
```

The API currently retrieves:

```text
k = 4
```

relevant chunks for each assessment.

---

## 15. How GPT Receives the Retrieved Knowledge

FAISS does not directly communicate with GPT.

The Python application performs the connection.

```text
FAISS
 ↓
Relevant Chunks
 ↓
Python Application
 ↓
Build Prompt
```

The prompt contains:

```text
Migration Scenario
        +
Retrieved Microsoft Learn Context
        +
Source Metadata
        +
Assessment Instructions
```

That complete prompt is then sent to GPT-4.1.

Therefore:

```text
Embeddings
→ Represent meaning

FAISS
→ Find relevant knowledge

GPT-4.1
→ Reason over the retrieved knowledge
```

---

## 16. GPT-4.1 Assessment

Configuration:

```text
Model: GPT-4.1
Temperature: 0
```

GPT-4.1 produces the initial migration assessment.

Expected fields:

```text
project_id
recommended_fabric_area
risk_level
confidence
key_risks
migration_considerations
human_review_required
reason
sources_used
```

Temperature 0 is used to improve consistency.

However, the architecture does not assume that the model becomes completely deterministic.

---

## 17. Reliability & Policy Layer

The AI output does not immediately become the final operational result.

The architecture adds a separate reliability and policy layer:

```text
GPT-4.1
   ↓
Initial Assessment
   ↓
Structured Output Validation
   ↓
Fabric Area Safeguard
   ↓
Enterprise Risk Guardrail
   ↓
Final Assessment
```

This is one of the most important architectural characteristics of the project.

---

## 18. Structured Output Validation

The GPT response is validated before downstream automation uses it.

Validation checks include:

```text
Required fields are present
JSON is parseable
Risk level is allowed
Confidence is within range
Human review is Boolean
```

For example:

```text
risk_level
```

must be one of:

```text
Low
Medium
High
```

The architecture therefore follows:

```text
GPT Response
     ↓
Validation
     ↓
Valid Structured Assessment
```

This prevents malformed AI output from directly controlling automation.

---

## 19. Fabric Area Reliability Safeguard

During testing, GPT occasionally returned a blank:

```text
recommended_fabric_area
```

A deterministic fallback was therefore added.

The fallback is used **only when the GPT recommendation is blank or missing**.

Examples:

```text
Reporting / Power BI
→ Power BI
  (Semantic Models, Reports, Dashboards)

Data Warehouse
→ Data Warehouse
  (Fabric Warehouse, SQL Analytics)

Spark / Databricks / HDInsight
→ Data Engineering
  (Lakehouse, Notebooks, Spark Job Definitions, Pipelines)

ADF / Pipeline / ETL
→ Data Factory
  (Pipelines, Dataflows Gen2)
```

If no specific Fabric area can safely be inferred:

```text
Microsoft Fabric
(Fabric area requires architecture review)
```

is used.

Conceptually:

```text
GPT Fabric Recommendation
          ↓
      Is Present?
      ↙       ↘
    Yes        No
     ↓          ↓
Use GPT      Fallback
     ↘          ↙
      Final Fabric Area
```

---

## 20. Enterprise Risk Guardrail

Repeated testing demonstrated that LLM risk classifications can vary between executions even with:

```text
temperature = 0
```

Since the final risk classification controls operational Slack escalation, the architecture includes a deterministic enterprise risk guardrail.

Current rule:

```text
Business Criticality = High

AND at least one:

Data Size >= 1000 GB
OR
Daily Jobs >= 40
OR
Dependencies >= 3

        ↓

Final Risk = High
```

If GPT already classifies the workload as High, the High classification remains.

If GPT returns a lower risk but the enterprise rule is triggered, the final risk is raised to High.

---

## 21. AI Assessment and Deterministic Control Flow

The final decision architecture is:

```text
Migration Workload
       ↓
RAG Retrieval
       ↓
GPT-4.1
       ↓
Initial AI Assessment
       ↓
Structured Output Validation
       ↓
Fabric Area Safeguard
       ↓
Enterprise Risk Guardrail
       ↓
Final Assessment
       ↓
n8n
```

The correct interpretation is:

> GPT-4.1 generates the initial migration assessment. Structured validation and deterministic enterprise safeguards are then applied before the assessment is used for operational automation.

The final High-risk classifications should therefore **not be described as coming solely from GPT-4.1**.

---

## 22. AI vs Deterministic Responsibilities

The architecture deliberately separates probabilistic reasoning from deterministic processing.

### AI Reasoning

GPT-4.1 handles:

```text
Interpreting migration complexity
Reasoning over retrieved guidance
Identifying migration risks
Generating migration considerations
Explaining recommendations
Generating the initial risk assessment
```

### Deterministic Processing

The application and n8n handle:

```text
CSV validation
ETL normalization
Data-type conversion
Output validation
Fabric-area fallback
Enterprise risk policy
High-risk routing
Slack notification
Report generation
```

This improves:

```text
Reliability
Explainability
Maintainability
Governance
```

---

## 23. Risk Routing Architecture

After FastAPI returns the final assessment, n8n evaluates:

```text
risk_level == High
```

Routing:

```text
Final Assessment
       ↓
Risk == High?
   ┌──────┴──────┐
  Yes           No
   ↓             ↓
Slack         Continue
Alert
```

This decision is deterministic.

n8n does not perform migration reasoning itself.

It acts on the final structured assessment.

---

## 24. Slack Notification Layer

### Technology

```text
Slack
```

### Purpose

Slack provides:

```text
Operational escalation for High-risk workloads
```

The High-risk notification includes:

```text
Project ID
Risk Level
Confidence
Recommended Fabric Area
Reason
Human Review Required
```

The demonstration channel is:

```text
#fabric-migration-alerts
```

Slack serves as the **operational notification channel**, not the primary reporting interface.

---

## 25. Reporting Layer

After all workloads are assessed, n8n consolidates the results.

```text
Assessment 1
Assessment 2
Assessment 3
...
Assessment N
       ↓
Convert to File
       ↓
Consolidated CSV
       ↓
Respond to Webhook
       ↓
Streamlit
```

Streamlit then displays:

```text
Total workloads
High-risk count
Medium-risk count
Low-risk count
Human-review count
High-risk warning banner
Color-coded assessment register
Detailed workload assessments
Recommended Fabric areas
Key risks
Migration considerations
Grounding sources
Downloadable CSV
```

Therefore:

```text
Slack
→ Operational Escalation

Streamlit
→ Assessment Reporting
```

---

## 26. End-to-End Automated Flow

The user performs only the initial trigger:

```text
Upload CSV Files
       +
Run Fabric Migration Assessment
```

After submission, the following stages execute automatically:

```text
File consolidation
       ↓
n8n webhook
       ↓
CSV extraction
       ↓
ETL cleaning
       ↓
Data standardization
       ↓
FastAPI calls
       ↓
Embedding generation
       ↓
FAISS retrieval
       ↓
GPT assessment
       ↓
Validation
       ↓
Reliability safeguard
       ↓
Risk guardrail
       ↓
Risk routing
       ↓
Slack notification
       ↓
CSV generation
       ↓
Webhook response
       ↓
Streamlit reporting
```

The system is therefore accurately described as:

> A human-triggered, end-to-end automated AI assessment workflow.

---

## 27. Current Development Deployment

The current development environment is:

```text
Local Windows Development Machine
├── Streamlit
├── FastAPI
├── Python RAG Pipeline
├── FAISS
└── Project Files

Hostinger VPS
└── n8n

External Services
├── OpenAI API
├── Microsoft Learn
├── Slack
└── Cloudflare Tunnel
```

---

## 28. Development Connectivity

FastAPI currently runs locally:

```text
http://127.0.0.1:8000
```

n8n runs remotely on a Hostinger VPS.

The VPS cannot directly access the development computer's localhost.

A temporary Cloudflare tunnel therefore provides connectivity:

```text
n8n on Hostinger VPS
        ↓
Temporary HTTPS Endpoint
        ↓
Cloudflare Tunnel
        ↓
Local FastAPI
```

The tunnel is started using:

```text
cloudflared tunnel --url http://127.0.0.1:8000
```

The generated URL is temporary.

If the tunnel restarts, the n8n HTTP Request endpoint must be updated.

This behavior was observed during testing and is documented as a development limitation.

---

## 29. Production Architecture Direction

The temporary Cloudflare tunnel is appropriate for the learning environment but should not be used as the final production architecture.

A future production architecture could use:

```text
User
 ↓
Web Application
 ↓
Authenticated n8n Webhook
 ↓
n8n
 ↓
Secure FastAPI Service
 ↓
RAG Assessment Service
 ↓
Vector Store
 ↓
OpenAI
```

Production improvements would include:

```text
Persistent FastAPI hosting
API authentication
Webhook authentication
HTTPS
Reverse proxy
Secrets management
Central logging
Monitoring
Retries
Failure handling
Service health checks
Database persistence
Assessment history
Audit logging
Role-based access
Duplicate alert suppression
```

---

## 30. Architecture Responsibility Matrix

| Component | Primary Responsibility |
|---|---|
| Streamlit | User interface, validation, consolidation and reporting |
| n8n | ETL, workflow orchestration, routing and notification |
| FastAPI | Migration assessment API |
| OpenAI Embeddings | Retrieval-query vectorization |
| FAISS | Semantic knowledge retrieval |
| Microsoft Learn | Authoritative migration knowledge |
| GPT-4.1 | Grounded migration reasoning |
| Validation | Structured output contract enforcement |
| Fabric Area Safeguard | Recommendation completeness |
| Enterprise Risk Guardrail | Deterministic risk policy |
| Slack | High-risk operational escalation |

---

## 31. Technology Stack

### User Interface

```text
Streamlit
Pandas
```

### Workflow Automation

```text
n8n
```

### API

```text
FastAPI
Uvicorn
Pydantic
```

### RAG

```text
LangChain
LangChain OpenAI
FAISS
OpenAI Embeddings
```

### AI Models

```text
GPT-4.1
text-embedding-3-small
```

### Knowledge Ingestion

```text
requests
BeautifulSoup
Microsoft Learn
```

### Notification

```text
Slack
```

### Development Connectivity

```text
Cloudflare Tunnel
```

---

## 32. Why Neo4j Was Not Used

Neo4j was intentionally not included in this project.

A previous learning project used a knowledge graph where explicit entity relationships added value.

The current migration-assessment problem primarily requires:

```text
Semantic Knowledge Retrieval
        +
Workload Reasoning
```

FAISS-based retrieval is sufficient for the current scope.

Adding Neo4j simply to increase the number of technologies would unnecessarily complicate the architecture.

### Design Principle

> Use a technology because it solves a genuine problem, not simply because it is available.

---

## 33. Why Browser Automation Was Not Used

Playwright or other UI automation was also not required.

The required integrations already expose:

```text
APIs
Webhooks
Structured Files
```

API-based integration is more appropriate than automating a browser for this use case.

### Design Principle

> Prefer stable APIs and structured integration points over UI automation when they are available.

---

## 34. Current Scope

The current platform is designed for:

```text
Migration assessment toward Microsoft Fabric
```

The current RAG knowledge base should not automatically be used for unrelated migration scenarios such as:

```text
Spotfire → Power BI
Tableau → Power BI
```

Those migration types would require appropriate:

```text
Knowledge sources
RAG indexes
Prompt logic
Assessment rules
Validation
```

---

## 35. Future Multi-Engine Architecture

A future version could introduce an assessment router.

```text
Migration Request
       ↓
Assessment Type Router
       ↓
 ┌──────────────┬──────────────┬──────────────┐
 ↓              ↓              ↓
Fabric       Spotfire       Tableau
Migration    → Power BI     → Power BI
 ↓              ↓              ↓
Fabric RAG   BI RAG         BI RAG
```

n8n could remain the common orchestration layer while specialized RAG engines handle different migration domains.

---

## 36. Architecture Design Principles

The final architecture follows these principles:

1. **Separate responsibilities** between UI, orchestration, API and AI.
2. **Perform deterministic work deterministically** whenever possible.
3. **Use AI where reasoning and interpretation add value.**
4. **Ground AI using authoritative knowledge.**
5. **Validate AI output before downstream automation consumes it.**
6. **Keep deterministic business policy separate from AI reasoning.**
7. **Keep human review for important enterprise decisions.**
8. **Prefer APIs over tight application coupling.**
9. **Keep user-interface concerns separate from workflow logic.**
10. **Make limitations and safeguards transparent.**

---

## 37. Complete Data Flow

The final end-to-end data flow is:

```text
1. User uploads one or more migration inventory CSV files

2. Streamlit validates the required schema

3. Streamlit consolidates valid files

4. Streamlit sends the consolidated CSV to the n8n webhook

5. n8n extracts the CSV records

6. n8n cleans and standardizes each workload

7. n8n sends each structured workload to FastAPI

8. FastAPI creates a retrieval query

9. OpenAI Embeddings converts the query into a vector

10. FAISS retrieves relevant Microsoft Learn chunks

11. Python combines:
       Migration Scenario
       +
       Retrieved Context
       +
       Source Metadata

12. GPT-4.1 generates the initial assessment

13. Structured output validation checks the response

14. Fabric-area safeguard fills a missing recommendation if required

15. Enterprise risk guardrail applies deterministic business policy

16. FastAPI returns the final structured assessment

17. n8n evaluates the final risk level

18. High-risk workloads are automatically routed to Slack

19. All workload assessments are consolidated into CSV

20. n8n returns the completed report through the webhook

21. Streamlit displays the assessment dashboard

22. User can review details and download the final CSV
```

---

## 38. Final Architecture Summary

The final architecture can be summarized as:

```text
Streamlit
    ↓
Multi-File Intake
    ↓
n8n
    ↓
ETL & Standardization
    ↓
FastAPI
    ↓
OpenAI Embeddings
    ↓
FAISS
    ↓
Microsoft Learn Context
    ↓
GPT-4.1
    ↓
Structured Validation
    ↓
Fabric Area Safeguard
    ↓
Enterprise Risk Guardrail
    ↓
Final Assessment
    ↓
n8n
   ↙   ↘
Slack  Consolidated Report
          ↓
       Streamlit
```

The architecture demonstrates that a practical enterprise GenAI solution is not simply:

```text
Prompt → LLM → Answer
```

Instead, it combines:

```text
Enterprise Data
      +
ETL
      +
Workflow Automation
      +
API
      +
RAG
      +
AI Reasoning
      +
Validation
      +
Deterministic Business Rules
      +
Operational Escalation
      +
Human Review
```

This provides a practical enterprise-style foundation for AI-assisted Microsoft Fabric migration assessment.