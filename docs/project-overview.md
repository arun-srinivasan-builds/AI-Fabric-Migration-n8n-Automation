# AI-Powered Fabric Migration Assessment Platform

## Week 3 Mini-Capstone Project

## 1. Project Purpose

This project implements an end-to-end **AI-assisted Microsoft Fabric migration assessment platform**.

It combines concepts from the GenAI learning program into one integrated solution:

```text
Multi-File Input
+
ETL Automation
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
+
Streamlit
```

The objective is not to automatically make final migration decisions.

Instead, the platform performs an initial AI-assisted assessment to help identify:

- Recommended Microsoft Fabric areas
- Migration risks
- Migration considerations
- Evidence from relevant Microsoft Learn guidance
- Workloads requiring human review
- High-risk workloads requiring operational escalation

---

## 2. Business Problem

Enterprise migration assessments require engineers and architects to review information such as:

```text
Source technology
Workload type
Data volume
Job frequency
Dependencies
Business criticality
Current technical issues
Target platform
```

This information must then be compared with migration guidance before determining an appropriate migration approach.

When many workloads are involved, the initial assessment becomes repetitive and time-consuming.

This project demonstrates how **ETL, RAG, GenAI and workflow automation** can assist with that initial assessment while retaining human review for important migration decisions.

---

## 3. Final Solution

The completed platform follows this flow:

```text
User
 ↓
Streamlit
 ↓
Upload One or More Migration Inventory CSVs
 ↓
Validate & Consolidate
 ↓
n8n Webhook
 ↓
Extract CSV
 ↓
ETL Cleaning & Standardization
 ↓
FastAPI /assess
 ↓
RAG Knowledge Retrieval
 ↓
OpenAI Embeddings + FAISS
 ↓
Relevant Microsoft Learn Context
 ↓
GPT-4.1 Assessment
 ↓
Structured Output Validation
 ↓
Fabric Area Safeguard
 ↓
Enterprise Risk Guardrail
 ↓
Final Assessment
 ↓
n8n Risk Routing
   ↙            ↘
High Risk     All Results
   ↓              ↓
Slack          CSV Report
                  ↓
               Streamlit
```

The platform is best described as:

> **A human-triggered, end-to-end automated AI migration assessment workflow.**

---

## 4. Migration Inventory

Synthetic migration inventory data is used instead of confidential enterprise or customer information.

Each workload contains:

```text
project_id
application_name
source_platform
workload_type
data_size_gb
daily_jobs
dependencies
business_criticality
current_issues
target_platform
```

The sample data intentionally includes inconsistencies such as:

```text
HD insight
azure data factory
power bi
HIGH
low
ADF; adls
```

This allows the project to demonstrate realistic ETL cleaning before AI processing.

The final application supports **multiple CSV files** in a single assessment run.

---

## 5. Streamlit Application

Streamlit provides the user-facing interface.

It handles:

- Multi-file CSV upload
- Schema validation
- File consolidation
- Input preview
- Workload metrics
- Assessment execution
- Risk summary
- Color-coded assessment register
- Detailed workload results
- Final CSV download

Streamlit is the presentation and reporting layer rather than the migration intelligence layer.

---

## 6. n8n ETL and Automation

n8n provides workflow orchestration and ETL.

It performs:

```text
Webhook Intake
      ↓
CSV Extraction
      ↓
Parsing
      ↓
Source Platform Normalization
      ↓
Business Criticality Normalization
      ↓
Dependency Normalization
      ↓
Data-Type Conversion
      ↓
FastAPI Calls
      ↓
Risk Routing
      ↓
Slack Escalation
      ↓
CSV Report Generation
```

This ensures predictable data-cleaning operations are handled deterministically before the workload reaches the AI system.

---

## 7. FastAPI Assessment Service

FastAPI exposes the Python migration intelligence through:

```text
POST /assess
```

Each cleaned migration workload is submitted independently.

FastAPI coordinates:

```text
Request Validation
        ↓
RAG Retrieval
        ↓
GPT-4.1 Assessment
        ↓
Output Validation
        ↓
Reliability Safeguards
        ↓
Enterprise Risk Policy
        ↓
Structured Response
```

This creates a clean boundary between n8n orchestration and Python-based AI intelligence.

---

## 8. Retrieval-Augmented Generation

The platform uses RAG to ground assessments in selected official Microsoft Learn documentation.

The knowledge pipeline is:

```text
Microsoft Learn
      ↓
Web Ingestion
      ↓
Cleaning
      ↓
Chunking
      ↓
OpenAI Embeddings
      ↓
FAISS
```

At runtime:

```text
Migration Workload
      ↓
Retrieval Query
      ↓
Query Embedding
      ↓
FAISS Retrieval
      ↓
Relevant Microsoft Learn Context
      +
Original Workload
      ↓
GPT-4.1
```

This reduces reliance on the model's general knowledge alone.

---

## 9. Knowledge Base

The current knowledge base contains selected Microsoft Learn guidance covering:

- Azure Data Factory migration planning
- Azure Data Factory migration assessment
- Synapse Spark migration
- Fabric Data Factory migration best practices

The four processed documents produced:

```text
41 chunks
```

Configuration:

```text
Chunk Size:       1000
Chunk Overlap:     150
Embedding Model:  text-embedding-3-small
Vector Store:     FAISS
Runtime Retrieval: k = 4
```

---

## 10. AI Assessment

The assessment model is:

```text
GPT-4.1
Temperature: 0
```

The model receives:

```text
Structured Migration Workload
+
Retrieved Microsoft Learn Context
+
Source Metadata
+
Assessment Instructions
```

It generates:

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

The response is structured so that downstream automation can use individual fields safely.

---

## 11. Validation and Reliability Safeguards

AI output is validated before being returned to n8n.

Checks include:

```text
Required fields
Valid risk classification
Confidence range
Boolean human-review value
Valid JSON structure
```

A deterministic Fabric-area safeguard also fills `recommended_fabric_area` when the AI response leaves it blank.

This prevents a known LLM failure mode from producing incomplete downstream reports.

---

## 12. Enterprise Risk Guardrail

Testing demonstrated that LLM risk classifications can vary between executions even at temperature 0.

A deterministic enterprise risk rule was therefore added.

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

The final assessment therefore combines:

```text
AI Reasoning
+
Deterministic Enterprise Policy
```

rather than treating GPT as the sole policy engine.

---

## 13. Slack Escalation

n8n evaluates the final:

```text
risk_level
```

When:

```text
risk_level == High
```

the workload is automatically sent to:

```text
#fabric-migration-alerts
```

Slack is used for **operational escalation**, while Streamlit remains the primary assessment and reporting interface.

---

## 14. Technologies Used

| Area | Technology |
|---|---|
| User Interface | Streamlit |
| Data Processing | Pandas |
| Workflow & ETL | n8n |
| API | FastAPI, Pydantic, Uvicorn |
| RAG | LangChain |
| Vector Database | FAISS |
| Embeddings | OpenAI `text-embedding-3-small` |
| AI Model | GPT-4.1 |
| Knowledge Source | Microsoft Learn |
| Web Ingestion | requests, BeautifulSoup |
| Notifications | Slack |
| Development Connectivity | Cloudflare Tunnel |
| Development | Python 3.11, VS Code, Git/GitHub |

---

## 15. Final Test

The final end-to-end test used:

```text
2 CSV Files
10 Migration Workloads
```

The completed workflow produced:

```text
Total Workloads:          10
High Risk:                 6
Medium Risk:               4
Low Risk:                  0
Human Review Required:    10
Slack Escalations:         6
```

The test validated the complete flow:

```text
Multi-File Upload
      ↓
ETL
      ↓
FastAPI
      ↓
RAG
      ↓
GPT-4.1
      ↓
Validation
      ↓
Enterprise Guardrails
      ↓
Risk Routing
      ↓
Slack
      ↓
Reporting
```

---

## 16. Key Learning Objectives Achieved

The project reinforced practical understanding of:

- GenAI application architecture
- Retrieval-Augmented Generation
- Embeddings
- Vector databases
- Chunking and retrieval
- Prompt/context construction
- Grounded LLM reasoning
- Structured AI output
- FastAPI-based AI services
- ETL automation
- n8n workflow orchestration
- Conditional business routing
- Human-in-the-loop AI
- LLM variability
- Deterministic safeguards
- Enterprise AI integration
- Multi-component debugging

---

## 17. Scope

This is a **Week 3 mini-capstone**, not a production migration assessment product.

The current RAG knowledge base is intentionally limited to selected Microsoft Fabric migration guidance.

It should not be treated as comprehensive guidance for every:

```text
HDInsight
Databricks
Power BI
Azure
or third-party migration scenario
```

Human architecture review remains part of the design.

---

## 18. Intentional Technology Choices

Neo4j was not added because the current problem does not require explicit knowledge-graph relationships.

Playwright was not added because the required integrations are available through APIs and webhooks.

This reflects an important engineering principle:

> **Use technology when it solves a real problem, not simply to increase the number of technologies in the solution.**

---

## 19. Current Development Limitation

FastAPI currently runs on the local development machine while n8n runs on a Hostinger VPS.

A temporary Cloudflare tunnel connects them.

This is appropriate for development and demonstration, but a production version should use a persistent hosted API with:

```text
Authentication
HTTPS
Secrets Management
Monitoring
Logging
Retries
Auditability
```

Repeated submissions can also create duplicate Slack alerts. A production workflow should add idempotency or duplicate-alert suppression.

---

## 20. Future Enhancements

Possible future extensions include:

- Persistent FastAPI deployment
- Authentication and API security
- Expanded Microsoft Fabric knowledge base
- Dedicated HDInsight and Databricks migration guidance
- Assessment history and persistence
- Audit logging
- Configurable enterprise risk policies
- Duplicate Slack alert suppression
- Retrieval-quality scoring
- Improved confidence calculation
- Specialized migration assessment engines

A future routing architecture could support:

```text
Migration Request
       ↓
Assessment Router
       ↓
 ┌─────────────┬─────────────┐
 ↓             ↓             ↓
Fabric      Spotfire      Tableau
RAG         → Power BI    → Power BI
```

Each migration domain would use its own appropriate knowledge base and assessment logic.

---

## 21. Final Outcome

The project successfully demonstrates:

```text
Raw Enterprise-Style Data
          ↓
Deterministic ETL
          ↓
API-Based AI Service
          ↓
RAG-Grounded Reasoning
          ↓
Structured AI Assessment
          ↓
Validation & Guardrails
          ↓
Automated Business Action
          ↓
Human Review
```

The result is a working **AI-Powered Fabric Migration Assessment Platform** that demonstrates how GenAI can be integrated with enterprise data processing, APIs, workflow automation, deterministic controls, notifications, and reporting without treating the LLM as an autonomous decision-maker.

---

## 22. Detailed Documentation

Continue with:

- [01 – Environment Setup](01-environment-setup.md)
- [02 – Solution Architecture](02-architecture.md)
- [03 – Data and ETL Design](03-data-and-etl.md)
- [04 – RAG Pipeline](04-rag-pipeline.md)
- [05 – API Automation](05-api-automation.md)
- [06 – n8n Workflow](06-n8n-workflow.md)
- [07 – Testing and Results](07-testing-results.md)
- [08 – Key Learnings](08-key-learnings.md)