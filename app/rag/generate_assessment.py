import json
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from app.rag.validate_assessment import parse_and_validate


# =========================================================
# Environment
# =========================================================

load_dotenv()


# =========================================================
# Project Paths
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

FAISS_INDEX_PATH = (
    PROJECT_ROOT
    / "knowledge"
    / "faiss_index"
)


# =========================================================
# Models
# =========================================================

EMBEDDING_MODEL = "text-embedding-3-small"

CHAT_MODEL = "gpt-4.1"


# =========================================================
# Load FAISS Vector Store
# =========================================================

def load_vector_store() -> FAISS:
    """
    Load the previously created FAISS vector store.
    """

    embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL
    )

    vector_store = FAISS.load_local(
        str(FAISS_INDEX_PATH),
        embeddings,
        allow_dangerous_deserialization=True,
    )

    return vector_store


# =========================================================
# Retrieve Relevant Context
# =========================================================

def retrieve_context(
    vector_store: FAISS,
    query: str,
    k: int = 4,
) -> tuple[str, list[str]]:
    """
    Retrieve the most relevant Microsoft migration
    guidance from FAISS.
    """

    documents = vector_store.similarity_search(
        query,
        k=k,
    )

    context_parts = []
    sources = []

    for index, document in enumerate(
        documents,
        start=1,
    ):

        metadata = document.metadata or {}

        title = (
            metadata.get("TITLE")
            or metadata.get("title")
            or "Microsoft migration guidance"
        )

        source_url = (
            metadata.get("SOURCE_URL")
            or metadata.get("source_url")
            or metadata.get("source")
            or ""
        )

        source_type = (
            metadata.get("SOURCE_TYPE")
            or metadata.get("source_type")
            or "Microsoft Learn"
        )

        context_parts.append(
            f"""
DOCUMENT {index}
Title: {title}
Source Type: {source_type}
Source URL: {source_url}

Content:
{document.page_content}
""".strip()
        )

        if (
            source_url
            and source_url not in sources
        ):
            sources.append(
                source_url
            )

    context_text = "\n\n---\n\n".join(
        context_parts
    )

    return (
        context_text,
        sources,
    )


# =========================================================
# Fabric Area Reliability Fallback
# =========================================================

def infer_fabric_area(
    migration_scenario: dict[str, Any],
) -> str:
    """
    Conservative fallback used only when GPT does not
    return a usable recommended_fabric_area.
    """

    source_platform = str(
        migration_scenario.get(
            "source_platform",
            "",
        )
    ).strip().lower()

    workload_type = str(
        migration_scenario.get(
            "workload_type",
            "",
        )
    ).strip().lower()

    dependencies = migration_scenario.get(
        "dependencies",
        [],
    )

    if isinstance(
        dependencies,
        list,
    ):
        dependency_text = " ".join(
            str(item)
            for item in dependencies
        ).lower()

    else:

        dependency_text = str(
            dependencies
        ).lower()

    combined_text = " ".join(
        [
            source_platform,
            workload_type,
            dependency_text,
        ]
    )

    # -----------------------------------------------------
    # Reporting / Power BI
    # -----------------------------------------------------

    if (
        "power bi" in combined_text
        or "report" in workload_type
        or "dashboard" in workload_type
        or "semantic" in workload_type
    ):

        return (
            "Power BI "
            "(Semantic Models, Reports, Dashboards)"
        )

    # -----------------------------------------------------
    # Data Warehouse
    # -----------------------------------------------------

    if (
        "data warehouse" in workload_type
        or (
            "synapse" in source_platform
            and "spark" not in workload_type
        )
        or "warehouse" in workload_type
    ):

        return (
            "Data Warehouse "
            "(Fabric Warehouse, SQL Analytics)"
        )

    # -----------------------------------------------------
    # Spark / Data Engineering
    # -----------------------------------------------------

    if (
        "spark" in combined_text
        or "databricks" in source_platform
        or "hd insight" in source_platform
        or "hdinsight" in source_platform
    ):

        return (
            "Data Engineering "
            "(Lakehouse, Notebooks, "
            "Spark Job Definitions, Pipelines)"
        )

    # -----------------------------------------------------
    # Data Factory / Pipelines
    # -----------------------------------------------------

    if (
        "azure data factory" in combined_text
        or "adf" in combined_text
        or "pipeline" in workload_type
        or "etl" in workload_type
        or "orchestration" in workload_type
    ):

        return (
            "Data Factory "
            "(Pipelines, Dataflows Gen2)"
        )

    return (
        "Microsoft Fabric "
        "(Fabric area requires architecture review)"
    )


def ensure_recommended_fabric_area(
    assessment: dict[str, Any],
    migration_scenario: dict[str, Any],
) -> dict[str, Any]:
    """
    Ensure recommended_fabric_area is never empty.
    """

    recommended_area = assessment.get(
        "recommended_fabric_area"
    )

    if (
        recommended_area is None
        or not str(
            recommended_area
        ).strip()
    ):

        assessment[
            "recommended_fabric_area"
        ] = infer_fabric_area(
            migration_scenario
        )

    return assessment


# =========================================================
# Risk Guardrail Helpers
# =========================================================

def normalize_criticality(
    value: Any,
) -> str:
    """
    Normalize business criticality.
    """

    return str(
        value or ""
    ).strip().lower()


def normalize_dependency_count(
    dependencies: Any,
) -> int:
    """
    Determine the number of workload dependencies.
    """

    if dependencies is None:
        return 0

    if isinstance(
        dependencies,
        list,
    ):
        return len(
            [
                item
                for item in dependencies
                if str(item).strip()
            ]
        )

    text = str(
        dependencies
    ).strip()

    if not text:
        return 0

    if ";" in text:

        return len(
            [
                item
                for item in text.split(";")
                if item.strip()
            ]
        )

    if "," in text:

        return len(
            [
                item
                for item in text.split(",")
                if item.strip()
            ]
        )

    return 1


def safe_float(
    value: Any,
    default: float = 0.0,
) -> float:
    """
    Safely convert numeric input.
    """

    try:
        return float(
            value
        )

    except (
        TypeError,
        ValueError,
    ):
        return default


def safe_int(
    value: Any,
    default: int = 0,
) -> int:
    """
    Safely convert integer input.
    """

    try:
        return int(
            float(value)
        )

    except (
        TypeError,
        ValueError,
    ):
        return default


# =========================================================
# Deterministic Enterprise Risk Guardrail
# =========================================================

def apply_risk_guardrail(
    assessment: dict[str, Any],
    migration_scenario: dict[str, Any],
) -> dict[str, Any]:
    """
    Apply deterministic enterprise risk rules after
    the AI assessment.

    GPT remains responsible for the initial assessment.

    The guardrail prevents highly business-critical,
    complex workloads from being reduced to Medium/Low
    because of normal LLM variability.

    Current rule:

    HIGH business criticality
    AND at least one of:

        - data size >= 1000 GB
        - daily jobs >= 40
        - dependency count >= 3

    => final risk must be High.
    """

    business_criticality = (
        normalize_criticality(
            migration_scenario.get(
                "business_criticality"
            )
        )
    )

    data_size_gb = safe_float(
        migration_scenario.get(
            "data_size_gb"
        )
    )

    daily_jobs = safe_int(
        migration_scenario.get(
            "daily_jobs"
        )
    )

    dependency_count = (
        normalize_dependency_count(
            migration_scenario.get(
                "dependencies"
            )
        )
    )

    current_risk = str(
        assessment.get(
            "risk_level",
            "",
        )
    ).strip().lower()

    high_business_criticality = (
        business_criticality == "high"
    )

    large_data_volume = (
        data_size_gb >= 1000
    )

    high_job_frequency = (
        daily_jobs >= 40
    )

    complex_dependencies = (
        dependency_count >= 3
    )

    complexity_triggered = any(
        [
            large_data_volume,
            high_job_frequency,
            complex_dependencies,
        ]
    )

    guardrail_triggered = (
        high_business_criticality
        and complexity_triggered
        and current_risk != "high"
    )

    if guardrail_triggered:

        assessment[
            "risk_level"
        ] = "High"

        assessment[
            "human_review_required"
        ] = True

        triggered_factors = []

        if large_data_volume:

            triggered_factors.append(
                f"large data volume "
                f"({data_size_gb:g} GB)"
            )

        if high_job_frequency:

            triggered_factors.append(
                f"high daily job volume "
                f"({daily_jobs} jobs)"
            )

        if complex_dependencies:

            triggered_factors.append(
                f"multiple dependencies "
                f"({dependency_count})"
            )

        factor_text = ", ".join(
            triggered_factors
        )

        existing_reason = str(
            assessment.get(
                "reason",
                "",
            )
        ).strip()

        guardrail_reason = (
            "Enterprise risk guardrail applied because "
            "the workload has High business criticality "
            f"combined with {factor_text}."
        )

        if existing_reason:

            assessment[
                "reason"
            ] = (
                f"{existing_reason} "
                f"{guardrail_reason}"
            )

        else:

            assessment[
                "reason"
            ] = guardrail_reason

    return assessment


# =========================================================
# Generate Migration Assessment
# =========================================================

def generate_assessment(
    migration_scenario: dict[str, Any],
    context: str,
    sources: list[str],
) -> str:
    """
    Generate a structured RAG-grounded Microsoft
    Fabric migration assessment.
    """

    llm = ChatOpenAI(
        model=CHAT_MODEL,
        temperature=0,
    )

    scenario_json = json.dumps(
        migration_scenario,
        indent=2,
        ensure_ascii=False,
    )

    sources_text = (
        "\n".join(
            f"- {source}"
            for source in sources
        )
        if sources
        else "No explicit source URLs were retrieved."
    )

    prompt = f"""
You are an enterprise Microsoft Fabric migration assessment assistant.

Your task is to assess the supplied migration workload using ONLY:

1. The migration scenario provided below.
2. The retrieved Microsoft migration guidance provided below.

Do not invent Microsoft features, migration utilities, timelines,
performance guarantees, compatibility guarantees or unsupported facts.

If the retrieved guidance does not directly cover the exact source
technology, clearly state that limitation in the assessment.

The assessment is advisory and must support human architectural review.


============================================================
MIGRATION SCENARIO
============================================================

{scenario_json}


============================================================
RETRIEVED MICROSOFT GUIDANCE
============================================================

{context}


============================================================
RETRIEVED SOURCE URLS
============================================================

{sources_text}


============================================================
OUTPUT REQUIREMENTS
============================================================

Return ONLY one valid JSON object.

Do not include Markdown.

Do not include JSON fences.

Do not include explanatory text outside the JSON object.

Use exactly these fields:

{{
  "project_id": "string",
  "recommended_fabric_area": "string",
  "risk_level": "Low|Medium|High",
  "confidence": 0.0,
  "key_risks": [
    "string"
  ],
  "migration_considerations": [
    "string"
  ],
  "human_review_required": true,
  "reason": "string",
  "sources_used": [
    "string"
  ]
}}


============================================================
FIELD RULES
============================================================

project_id:
- Must exactly match the supplied project_id.

recommended_fabric_area:
- MUST NEVER be null.
- MUST NEVER be blank.
- MUST NEVER be an empty string.
- MUST NEVER be omitted.
- Recommend the most appropriate Fabric area supported by the scenario
  and retrieved guidance.
- Useful examples include:

  "Data Engineering (Lakehouse, Notebooks, Spark Job Definitions, Pipelines)"

  "Data Factory (Pipelines, Dataflows Gen2)"

  "Data Warehouse (Fabric Warehouse, SQL Analytics)"

  "Power BI (Semantic Models, Reports, Dashboards)"

- If there is not enough information to confidently identify a specific
  Fabric area, use:

  "Microsoft Fabric (Fabric area requires architecture review)"

risk_level:
- Must be exactly Low, Medium or High.
- Base the rating on migration complexity, dependencies, workload scale,
  business criticality, current issues and limitations in the retrieved
  guidance.

confidence:
- Must be a number between 0.0 and 1.0.
- Reduce confidence when the retrieved guidance does not directly cover
  the exact source technology.

key_risks:
- Return practical migration risks supported by the scenario or retrieved
  guidance.
- Do not invent unsupported technical limitations.

migration_considerations:
- Provide practical considerations that should be reviewed during planning.

human_review_required:
- Must be a JSON boolean: true or false.
- Use true when architectural judgement or additional validation is needed.

reason:
- Explain the recommendation and risk rating concisely.
- Clearly mention evidence limitations where relevant.

sources_used:
- Include only URLs from the retrieved source list above.
- Do not invent URLs.
- If none of the retrieved sources were materially used, return an empty list.


Return ONLY the JSON object.
"""

    response = llm.invoke(
        prompt
    )

    response_text = str(
        response.content
    ).strip()

    # -----------------------------------------------------
    # 1. Validate AI response
    # -----------------------------------------------------

    assessment = parse_and_validate(
        response_text
    )

    # -----------------------------------------------------
    # 2. Ensure Fabric area is populated
    # -----------------------------------------------------

    assessment = (
        ensure_recommended_fabric_area(
            assessment=assessment,
            migration_scenario=migration_scenario,
        )
    )

    # -----------------------------------------------------
    # 3. Apply deterministic enterprise risk guardrail
    # -----------------------------------------------------

    assessment = (
        apply_risk_guardrail(
            assessment=assessment,
            migration_scenario=migration_scenario,
        )
    )

    return json.dumps(
        assessment,
        ensure_ascii=False,
    )


# =========================================================
# Optional Direct Test
# =========================================================

if __name__ == "__main__":

    vector_store = (
        load_vector_store()
    )

    test_scenario = {
        "project_id": "MIG005",
        "application_name": "IoT Processing",
        "source_platform": "Azure Databricks",
        "workload_type": "Spark",
        "data_size_gb": 2100,
        "daily_jobs": 48,
        "dependencies": [
            "Event Hubs",
            "ADLS Gen2",
            "ADF",
        ],
        "business_criticality": "High",
        "current_issues": (
            "Increasing compute cost and "
            "complex orchestration"
        ),
        "target_platform": (
            "Microsoft Fabric"
        ),
    }

    query = f"""
Assess migration of this workload to Microsoft Fabric:

Source platform: {test_scenario["source_platform"]}
Workload type: {test_scenario["workload_type"]}
Dependencies: {test_scenario["dependencies"]}
Current issues: {test_scenario["current_issues"]}
Target platform: {test_scenario["target_platform"]}
"""

    retrieved_context, retrieved_sources = (
        retrieve_context(
            vector_store=vector_store,
            query=query,
            k=4,
        )
    )

    result = generate_assessment(
        migration_scenario=test_scenario,
        context=retrieved_context,
        sources=retrieved_sources,
    )

    print(
        json.dumps(
            json.loads(result),
            indent=2,
            ensure_ascii=False,
        )
    )