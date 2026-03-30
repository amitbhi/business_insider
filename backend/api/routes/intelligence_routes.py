"""
API Routes for Triggering and Managing Intelligence Analysis.
"""

from fastapi import APIRouter
from typing import Dict, Any

from ..controllers.intelligence_controller import IntelligenceController

router = APIRouter(prefix="/analyze_company", tags=["Corporate Intelligence"])
controller = IntelligenceController()

@router.post("/")
async def start_analysis(payload: Dict[str, Any]):
    """
    Endpoint to trigger a full multi-agent corporate analysis.
    Takes company name and country.
    """
    company_name = payload.get("company_name", "Unknown Focus")
    country = payload.get("country", "India")
    data_source = payload.get("data_source", "mock")
    
    # Run full synchronous mock pipeline
    result = await controller.run_analysis(company_name, country, data_source)
    return result

@router.get("/{job_id}/status")
async def get_status(job_id: str):
    """Check the status of a running intelligence task."""
    return {"job_id": job_id, "status": "processing"}

@router.get("/{job_id}/report")
async def get_intelligence_report(job_id: str):
    """Retrieve the generated strategic report."""
    return {"job_id": job_id, "report_data": {}}
