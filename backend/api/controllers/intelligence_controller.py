"""
Intelligence Controller Layer

Handles the business logic between the REST API and the Agent Orchestration Layer.
"""

from typing import Dict, Any
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from orchestration.agent_manager import AgentManager

class IntelligenceController:
    """Manages the lifecycle of an intelligence analysis request."""
    
    def __init__(self):
        self.agent_manager = AgentManager()
    
    async def run_analysis(self, company_name: str, country: str, data_source: str = "mock") -> Dict[str, Any]:
        """
        Executes the full intelligence gathering pipeline and returns the result.
        """
        job_id = f"job-{company_name[:4]}-123"
        result = await self.agent_manager.run_full_analysis(company_name, country, job_id, data_source)
        
        return {
            "company": company_name,
            "resolved_company_name": result.get("company_name", "N/A"),
            "country": country,
            "job_id": job_id,
            "intelligence_summary": result.get("intelligence_report", ""),
            "graph": result.get("graph", {}),
            "control_structure": result.get("control_structure", {}),
            "strategic_flags": result.get("strategic_flags", {}),
            "strategic_vulnerabilities": result.get("strategic_vulnerabilities", {}),
            "vulnerability_report": result.get("vulnerability_report", ""),
            "control_reasoning": result.get("control_reasoning", ""),
            "influence_network": result.get("influence_network", {}),
            "influence_report": result.get("influence_report", ""),
            "acquisition_targets": result.get("acquisition_targets", {}),
            "acquisition_report": result.get("acquisition_report", ""),
            "raw_agent_data": result.get("agent_outputs", {})
        }
