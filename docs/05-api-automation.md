# API Automation

## 1. Purpose

The FastAPI layer exposes the Python-based migration assessment engine as an HTTP service.

Without an API, the RAG application would have to be executed directly from Python.

With FastAPI, external systems such as n8n can submit a migration workload and receive a structured migration assessment.

The final communication flow is:

```text
n8n
 ↓
HTTP Request
 ↓
FastAPI
 ↓
RAG Retrieval
 ↓
FAISS + OpenAI Embeddings
 ↓
GPT-4.1
 ↓
Structured Validation
 ↓
Reliability Safeguards
 ↓
Enterprise Risk Guardrail
 ↓
Final Assessment
 ↓
FastAPI Response
 ↓
n8n
```

The API therefore acts as the bridge between:

```text
Workflow Automation
        and
Migration Intelligence
```

---

## 2. API Implementation

The API is implemented in:

```text
app/api.py
```

The main technologies are:

```text
FastAPI
Pydantic
Uvicorn
python-dotenv
```

### FastAPI

Provides the HTTP endpoints.

### Pydantic

Validates incoming request data.

### Uvicorn

Runs the FastAPI application as the local development server.

### python-dotenv

Loads environment variables such as the OpenAI API key.

---

## 3. API Startup

The API is started using:

```cmd
uvicorn app.api:app --reload
```

The local development endpoint is:

```text
http://127.0.0.1:8000
```

The `--reload` option automatically reloads the application when Python files change during development.

---

## 4. Health Endpoint

Endpoint:

```text
GET /
```

Purpose:

```text
Verify that the FastAPI service is running.
```

Expected response:

```json
{
  "message": "AI Fabric Migration Assessment API is running"
}
```

This endpoint was successfully tested using:

```cmd
curl http://127.0.0.1:8000/
```

and confirmed that the API service was healthy.

---

## 5. Migration Assessment Endpoint

Endpoint:

```text
POST /assess
```

Purpose:

```text
Receive one structured migration workload and return a grounded Microsoft Fabric migration assessment.
```

The endpoint expects:

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

---

## 6. Request Model

The request contract is defined using Pydantic.

Conceptually:

```python
class MigrationScenario(BaseModel):
    project_id: str
    application_name: str
    source_platform: str
    workload_type: str
    data_size_gb: float
    daily_jobs: int
    dependencies: list[str]
    business_criticality: str
    current_issues: str
    target_platform: str
```

This ensures that FastAPI receives a structured workload rather than an arbitrary JSON payload.

---

## 7. Example Request

```json
{
  "project_id": "MIG001",
  "application_name": "Sales Analytics",
  "source_platform": "HDInsight",
  "workload_type": "Spark",
  "data_size_gb": 850,
  "daily_jobs": 24,
  "dependencies": [
    "ADF",
    "ADLS"
  ],
  "business_criticality": "High",
  "current_issues": "Long Spark processing time",
  "target_platform": "Microsoft Fabric"
}
```

The request reaches FastAPI only after n8n has performed ETL and standardization.

---

## 8. Pydantic Input Validation

FastAPI automatically validates the incoming request against the `MigrationScenario` model.

Examples of enforced types:

```text
data_size_gb
→ float

daily_jobs
→ integer

dependencies
→ list of strings
```

This creates a validation boundary before the RAG pipeline runs.

Conceptually:

```text
Incoming JSON
    ↓
Pydantic Validation
    ↓
Valid Migration Scenario
```

If the payload does not match the contract, FastAPI can reject it before invoking the AI pipeline.

---

## 9. API Assessment Flow

The `/assess` endpoint performs the following sequence:

```text
Migration Scenario
        ↓
Pydantic Validation
        ↓
Convert to Python Dictionary
        ↓
Build Retrieval Query
        ↓
OpenAI Query Embedding
        ↓
FAISS Retrieval
        ↓
Relevant Microsoft Learn Context
        ↓
GPT-4.1 Assessment
        ↓
Structured JSON Validation
        ↓
Fabric Area Safeguard
        ↓
Enterprise Risk Guardrail
        ↓
Final Structured Assessment
        ↓
HTTP Response
```

---

## 10. Retrieval Query Construction

FastAPI builds a retrieval query from the workload.

The query includes fields such as:

```text
Source platform
Workload type
Dependencies
Current issues
Target platform
```

Conceptually:

```text
Assess migration of this workload to Microsoft Fabric:

Source platform: HDInsight
Workload type: Spark
Dependencies: ADF, ADLS
Current issues: Long Spark processing time
Target platform: Microsoft Fabric
```

This query is used only for semantic knowledge retrieval.

---

## 11. Query Embedding

The retrieval query is converted into a vector using:

```text
text-embedding-3-small
```

Flow:

```text
Retrieval Query
      ↓
OpenAI Embeddings
      ↓
Query Vector
```

The query vector is then compared with the document vectors stored in FAISS.

---

## 12. FAISS Retrieval

The final API implementation retrieves:

```text
k = 4
```

relevant chunks.

Flow:

```text
Query Vector
      ↓
FAISS
      ↓
Top 4 Relevant Chunks
      ↓
Retrieved Context
```

The retrieved chunks come from the curated Microsoft Learn knowledge base.

---

## 13. GPT-4.1 Assessment

FastAPI passes the following to GPT-4.1:

```text
Migration Scenario
+
Retrieved Microsoft Learn Context
+
Source Metadata
+
Assessment Instructions
```

The model configuration is:

```text
Model: GPT-4.1
Temperature: 0
```

GPT-4.1 generates the initial migration assessment.

---

## 14. Structured Assessment Contract

The model is instructed to return structured JSON containing:

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

Structured output is essential because n8n must later use individual fields.

For example:

```text
risk_level
```

is used for workflow routing.

---

## 15. Structured Output Validation

The GPT response is passed through:

```text
app/rag/validate_assessment.py
```

Validation checks include:

```text
Required fields exist
risk_level is Low / Medium / High
confidence is numeric
confidence is between 0 and 1
human_review_required is Boolean
```

Conceptually:

```text
GPT Response
    ↓
Parse JSON
    ↓
Validate Contract
    ↓
Structured Assessment
```

This reduces the risk of malformed AI output reaching n8n.

---

## 16. Fabric Area Safeguard

Repeated testing showed that GPT could occasionally return a blank:

```text
recommended_fabric_area
```

A deterministic fallback was added.

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

The fallback is used only when the AI-generated recommendation is missing or blank.

---

## 17. Enterprise Risk Guardrail

The final API applies deterministic enterprise risk policy after the AI assessment.

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

If GPT already returns:

```text
High
```

the result remains High.

If GPT returns a lower risk but the deterministic enterprise rule is triggered, the final result is raised to:

```text
High
```

---

## 18. Why the Risk Guardrail Belongs After the AI

The AI is useful for:

```text
Reasoning
Interpretation
Risk identification
Migration considerations
Recommendation explanation
```

The deterministic guardrail is useful for:

```text
Enterprise policy
Consistent escalation
Predictable workflow behavior
```

The combined flow is:

```text
GPT-4.1
    ↓
Initial Risk Assessment
    ↓
Enterprise Risk Policy
    ↓
Final Risk
```

This is more reliable than using the LLM as the sole policy engine.

---

## 19. Final Response Contract

The final API response contains:

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

Example:

```json
{
  "project_id": "MIG001",
  "recommended_fabric_area": "Data Engineering (Lakehouse, Notebooks, Spark Job Definitions, Pipelines)",
  "risk_level": "High",
  "confidence": 0.5,
  "key_risks": [
    "Spark workload migration requires architecture review"
  ],
  "migration_considerations": [
    "Review Spark dependencies and orchestration design"
  ],
  "human_review_required": true,
  "reason": "Assessment generated from retrieved Microsoft Learn guidance and enterprise risk policy.",
  "sources_used": [
    "Synapse Spark Migration"
  ]
}
```

Exact AI-generated text and confidence values may vary between executions.

---

## 20. API Error Handling

The endpoint includes separate handling for validation and runtime failures.

Conceptually:

```text
Assessment Validation Error
        ↓
HTTP 500
        ↓
Assessment validation failed
```

and:

```text
Unexpected Processing Error
        ↓
HTTP 500
        ↓
Assessment generation failed
```

This prevents raw internal Python exceptions from being returned directly as successful workflow results.

---

## 21. FastAPI Exception Flow

The endpoint uses FastAPI:

```text
HTTPException
```

to convert application failures into HTTP responses.

This allows n8n to detect:

```text
HTTP Success
or
HTTP Failure
```

rather than assuming every API call succeeded.

---

## 22. Swagger Documentation

FastAPI automatically exposes interactive API documentation at:

```text
http://127.0.0.1:8000/docs
```

Swagger was used during development to test:

```text
POST /assess
```

before connecting n8n.

This was useful because it allowed the API to be validated independently of the workflow platform.

---

## 23. Initial API Test

The first API test used:

```text
Project ID: MIG001
Application: Sales Analytics
Source Platform: HDInsight
Workload Type: Spark
Data Size: 850 GB
Daily Jobs: 24
Dependencies: ADF, ADLS
Business Criticality: High
Current Issue: Long Spark processing time
Target Platform: Microsoft Fabric
```

The API successfully returned a grounded structured assessment.

An early result included:

```text
Risk Level: Medium
Confidence: 0.7
Human Review Required: True
```

Later project improvements added:

```text
Fabric Area Safeguard
Enterprise Risk Guardrail
```

so the final result should be understood as the post-validation and post-policy assessment.

---

## 24. Why FastAPI Is Needed

The RAG implementation contains the migration intelligence.

n8n contains the workflow orchestration.

FastAPI provides the interface between them.

```text
Python / RAG
→ Migration Intelligence

FastAPI
→ HTTP Service Interface

n8n
→ Workflow Orchestration
```

Without FastAPI, n8n would need to directly run or tightly integrate with Python code.

The HTTP boundary makes the components more independent.

---

## 25. Loose Coupling

The API creates loose coupling.

n8n does not need to know:

```text
How embeddings are generated
How FAISS works
How prompts are created
How GPT is invoked
How validation is implemented
How safeguards are applied
```

n8n only needs to know:

```text
POST /assess
```

and the request and response contracts.

This makes the architecture easier to maintain and evolve.

---

## 26. Structured Output for Automation

The response can be directly consumed by workflow logic.

For example:

```text
FastAPI Response
        ↓
n8n IF Node
        ↓
risk_level == High?
   ┌─────────┴─────────┐
  Yes                  No
   ↓                    ↓
Slack Alert          Continue
```

This demonstrates how probabilistic AI reasoning can feed deterministic automation.

---

## 27. Batch Processing Through n8n

FastAPI assesses one workload per request.

n8n handles the batch.

Conceptually:

```text
10 Workloads
     ↓
n8n
     ↓
Request 1 → /assess
Request 2 → /assess
Request 3 → /assess
...
Request 10 → /assess
```

This keeps the API contract simple:

```text
One workload
→ One assessment
```

while allowing n8n to orchestrate any number of records.

---

## 28. Why Batch Logic Remains in n8n

The project could have created a FastAPI endpoint that accepts an entire CSV or list of workloads.

Instead, batch orchestration remains in n8n because this clearly demonstrates:

```text
Workflow Automation
ETL
Iteration
API Integration
Conditional Routing
Slack Notification
Output Aggregation
```

This separation also keeps FastAPI focused on migration intelligence.

---

## 29. Development Connectivity Challenge

The architecture contains an important networking difference:

```text
FastAPI
→ Local Windows Machine

n8n
→ Hostinger VPS
```

The remote n8n instance cannot directly call:

```text
http://127.0.0.1:8000
```

because that address refers to the VPS itself when called remotely.

A temporary tunnel was therefore required.

---

## 30. Cloudflare Tunnel

For development, Cloudflare Tunnel exposes the local FastAPI server through a temporary HTTPS endpoint.

Command:

```cmd
cloudflared tunnel --url http://127.0.0.1:8000
```

Conceptually:

```text
n8n VPS
    ↓
HTTPS
    ↓
Cloudflare Tunnel
    ↓
Local FastAPI
```

This allows the self-hosted n8n workflow to call the locally running API.

---

## 31. Temporary URL Limitation

The Cloudflare quick tunnel URL changes when the tunnel is restarted.

During testing, the n8n HTTP Request node still contained an expired tunnel URL.

This caused:

```text
HTTP 500 in Streamlit
```

and the n8n execution showed:

```text
The connection cannot be established
```

The issue was resolved by:

```text
Restart Cloudflare Tunnel
        ↓
Copy New HTTPS URL
        ↓
Update n8n HTTP Request Node
        ↓
Save / Publish Workflow
        ↓
Rerun Assessment
```

The workflow then worked again successfully.

---

## 32. Development Dependency

During the current local-development setup, both of these must remain running:

```text
FastAPI terminal

Cloudflare tunnel terminal
```

If either stops:

```text
n8n → FastAPI
```

connectivity will fail.

This is acceptable for the learning project but not appropriate for production.

---

## 33. Production API Direction

A production version should host FastAPI as a persistent service.

Possible architecture:

```text
n8n
 ↓
Authenticated HTTPS
 ↓
Hosted FastAPI
 ↓
RAG Service
```

This would remove the temporary tunnel dependency.

Production improvements could include:

```text
Persistent hosting
Authentication
API keys or OAuth
Reverse proxy
HTTPS
Secrets management
Rate limiting
Request logging
Central monitoring
Retries
Health monitoring
Timeout handling
Audit logging
```

---

## 34. API and Security

The current implementation is a learning and demonstration environment.

For production, the `/assess` endpoint should not be exposed as an unrestricted public service.

Security controls should include:

```text
Authentication
Authorization
HTTPS
Secrets management
Rate limiting
Input validation
Audit logging
Network restrictions
```

---

## 35. API Role in the Final Architecture

The API sits between orchestration and AI intelligence:

```text
Streamlit
    ↓
n8n
    ↓
FastAPI
    ↓
RAG + GPT
    ↓
Validation + Guardrails
    ↓
FastAPI
    ↓
n8n
   ↙   ↘
Slack  Report
```

This makes FastAPI the reusable migration-assessment service layer.

---

## 36. API Validation Results

The following components were successfully tested:

```text
FastAPI Startup                     COMPLETE
Health Endpoint                     COMPLETE
Swagger UI                          COMPLETE
Pydantic Request Validation         COMPLETE
Migration Assessment Endpoint       COMPLETE
Query Embedding                     COMPLETE
FAISS Retrieval Through API         COMPLETE
GPT-4.1 Assessment                  COMPLETE
JSON Parsing                        COMPLETE
Structured Output Validation        COMPLETE
Fabric Area Safeguard               COMPLETE
Enterprise Risk Guardrail           COMPLETE
Structured API Response             COMPLETE
n8n HTTP Integration                COMPLETE
Cloudflare Development Connectivity COMPLETE
10-Workload Batch Integration       COMPLETE
```

---

## 37. Final End-to-End API Test

The final application processed:

```text
2 input CSV files
10 workloads
```

n8n sent each workload to:

```text
POST /assess
```

FastAPI successfully processed all workloads through:

```text
RAG Retrieval
GPT-4.1
Validation
Safeguards
Enterprise Policy
```

The final batch produced:

```text
10 Assessments
6 High Risk
4 Medium Risk
0 Low Risk
10 Human Review Required
```

The six final High-risk assessments were then routed by n8n to Slack.

---

## 38. Key API Learnings

1. FastAPI can expose Python AI logic as a reusable service.
2. Pydantic provides a strong request-validation boundary.
3. API contracts help separate AI logic from workflow automation.
4. n8n does not need to understand the internal RAG implementation.
5. Structured AI output is essential for downstream automation.
6. AI responses should be validated before returning them to orchestration systems.
7. Deterministic safeguards can be applied inside the service after AI reasoning.
8. One-record API contracts can still support batch processing through orchestration.
9. Localhost is not reachable from a remote VPS without additional networking.
10. Temporary tunneling is useful for development but should not replace production deployment.
11. HTTP errors are an important part of automation design.
12. A clean API boundary makes the intelligence layer reusable by future applications.

---

## 39. Final API Summary

The FastAPI layer can be summarized as:

```text
Clean Migration Workload
        ↓
FastAPI /assess
        ↓
Pydantic Validation
        ↓
Retrieval Query
        ↓
OpenAI Embeddings
        ↓
FAISS
        ↓
Retrieved Microsoft Learn Context
        ↓
GPT-4.1
        ↓
Structured Validation
        ↓
Fabric Area Safeguard
        ↓
Enterprise Risk Guardrail
        ↓
Final JSON Assessment
        ↓
n8n
```

The main architectural role of FastAPI is:

> Convert the Python RAG migration intelligence into a reusable HTTP service that can be safely consumed by workflow automation.