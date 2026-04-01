from typing import Dict, Any, List
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.finance import FinanceAgent
from agents.power import PowerAgent
from agents.legal import LegalAgent
from agents.social import SocialAgent
from agents.market import MarketAgent
from graph.builder import GraphBuilder
from graph.analyzer import GraphAnalyzer
from intelligence.strategic_analysis import StrategicEngine
from llm.local_llm import LocalLLM
from data_pipeline.adapters.factory import RegistryFactory

class AgentManager:
    """
    Orchestrates the specialized agents to compile comprehensive corporate intelligence
    following a formal 8-stage lifecycle.
    """

    def __init__(self):
        self.agents = {
            "finance": FinanceAgent(),
            "power": PowerAgent(),
            "legal": LegalAgent(),
            "social": SocialAgent(),
            "market": MarketAgent()
        }
        
        # Registry Factory for Jurisdictional Adapters
        self.registry_factory = RegistryFactory()
        
        self.graph_builder = GraphBuilder(None)
        self.strategic_engine = StrategicEngine()
        self.llm = LocalLLM()

    async def run_full_analysis(self, query: str, country: str, job_id: str = "JOB-001", data_source: str = "mock") -> Dict[str, Any]:
        """
        Executes the formally defined 8-stage Intelligence Lifecycle.
        """
        print(f"[{job_id}] Stage 1: Query Reception - Analyzing {query} in {country}")
        
        # Stage 2: Registry Ingestion
        adapter = self.registry_factory.get_adapter(country)
        master_data = await adapter.fetch_company_master(query)
        ownership_data = await adapter.fetch_ownership_data(query)
        director_data = await adapter.fetch_directors(query)
        
        print(f"[{job_id}] Stage 2: Registry Ingestion Complete for {master_data.get('company_info', {}).get('name')}")

        # Stage 3: Graph Construction
        # Initialize graph builder (db manager optional for V1)
        builder = GraphBuilder(None)
        graph_data = builder.build_from_registry_data(master_data, ownership_data)
        
        # Stage 4: Recursive Expansion (GOIE)
        graph_analyzer = GraphAnalyzer(graph_data)
        control_structure = graph_analyzer.infer_control_structure()
        
        # Stage 5: Vulnerability Assessment (WFD)
        strategic_vulnerabilities = graph_analyzer.detect_strategic_vulnerabilities(control_structure)
        
        # Stage 6: Social Intelligence Augmentation
        # Resolved director profiles and SPI computation
        social_data = await self.agents["social"].execute(query) # Mock for now
        
        # Stage 7: Strategic Scoring
        influence_network = graph_analyzer.analyze_influence_network()
        acquisition_targets = graph_analyzer.detect_acquisition_targets(strategic_vulnerabilities, influence_network)
        
        ico = {
            "master_data": master_data,
            "control_structure": control_structure,
            "vulnerabilities": strategic_vulnerabilities,
            "influence_network": influence_network,
            "acquisition_targets": acquisition_targets,
            "social_intelligence": social_data
        }
        
        strategic_flags = self.strategic_engine.generate_strategic_profile(ico)
        
        llm_report = await self.llm.invoke_reasoning(
            prompt=f"Synthesize this Intelligence Context Object (ICO) into a strategic report: {ico}",
            system_prompt="You are the Strategic Synthesis Agent for Business Insider."
        )

        return {
            "job_id": job_id,
            "jurisdiction": country,
            "company_name": master_data.get('company_info', {}).get('name'),
            "control_structure": control_structure,
            "influence_network": influence_network,
            "strategic_vulnerabilities": strategic_vulnerabilities,
            "strategic_flags": strategic_flags,
            "acquisition_targets": acquisition_targets,
            "intelligence_report": llm_report.get("reasoning", "Analysis Complete"),
            "ico": ico # Return full context for transparency
        }
