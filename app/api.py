from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.rag.generate_assessment import (
    generate_assessment,
    load_vector_store,
    retrieve_context,
)
from app.rag.validate_assessment import parse_and_validate


load_dotenv()


app = FastAPI(
    title="AI Fabric Migration Assessment API",
    version="1.0.0",
)


vector_store = load_vector_store()


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


@app.get("/")
def root():
    """
    Basic API health check.
    """
    return {
        "message": "AI Fabric Migration Assessment API is running"
    }


@app.post("/assess")
def assess_migration(
    scenario: MigrationScenario,
):
    """
    Generate a grounded migration assessment.
    """
    scenario_dict = scenario.model_dump()

    retrieval_query = f"""
Assess migration of this workload to Microsoft Fabric:

Source platform: {scenario.source_platform}
Workload type: {scenario.workload_type}
Dependencies: {scenario.dependencies}
Current issues: {scenario.current_issues}
Target platform: {scenario.target_platform}
"""

    try:
        context, sources = retrieve_context(
            vector_store=vector_store,
            query=retrieval_query,
            k=4,
        )

        response_text = generate_assessment(
            migration_scenario=scenario_dict,
            context=context,
            sources=sources,
        )

        assessment = parse_and_validate(
            response_text
        )

        return assessment

    except ValueError as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Assessment validation failed: {exc}",
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Assessment generation failed: {exc}",
        ) from exc