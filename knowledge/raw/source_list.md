# RAG Knowledge Sources

The RAG knowledge base for this project uses official Microsoft Learn
documentation related to Azure-to-Microsoft Fabric migration.

## Initial Sources

### 1. Azure Data Factory to Fabric Data Factory - Migration Planning

Purpose:
Provides migration strategies, architecture differences, migration
paths, compatibility considerations, and planning guidance for moving
Azure Data Factory workloads to Fabric Data Factory.

Source:
Microsoft Learn - Migration planning for Azure Data Factory to Fabric Data Factory

---

### 2. Azure Data Factory / Synapse Pipeline Migration Assessment

Purpose:
Explains how migration readiness is assessed and introduces statuses
such as:

- Ready
- Needs review
- Coming soon
- Not compatible

This will help the GenAI application identify when workloads may
require additional validation or human review.

Source:
Microsoft Learn - Assess Azure Data Factory and Synapse pipelines for
upgrade to Fabric Data Factory

---

### 3. Azure Synapse Spark to Microsoft Fabric

Purpose:
Provides guidance for migrating Spark workloads from Azure Synapse
Analytics to Fabric Data Engineering.

Topics include:

- Migration preparation
- Spark workload compatibility
- Notebook migration
- Data access changes
- Code refactoring
- Post-migration validation

Source:
Microsoft Learn - Overview of migrating Azure Synapse Spark to Fabric

---

### 4. Azure Data Factory Migration Best Practices

Purpose:
Provides implementation-level migration considerations including:

- Connections
- Authentication
- Integration runtimes
- Network requirements
- Activities
- Scheduling
- Monitoring
- Global parameters

Source:
Microsoft Learn - Migration Best Practices for Azure Data Factory to
Fabric Data Factory

---

## Knowledge Base Principle

Only relevant sections from trusted Microsoft documentation will be
used.

The objective is not to copy the entire Microsoft Fabric documentation
library.

The curated knowledge base should contain enough information to support
the migration scenarios used in this Week 3 mini-capstone.

The expected flow is:

Official Microsoft Documentation
        ↓
Selected Relevant Content
        ↓
knowledge/raw
        ↓
Cleaned Content
        ↓
knowledge/processed
        ↓
Chunking
        ↓
Embeddings
        ↓
FAISS Vector Database
        ↓
RAG Retrieval