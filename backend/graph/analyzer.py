from typing import Dict, Any, List
import networkx as nx
from intelligence.ownership_inference import OwnershipInferenceEngine

class GraphAnalyzer:
    """Responsible for detecting power structures using the Business Insider graph core."""
    
    def __init__(self, graph: nx.DiGraph):
        self.graph = graph
        self.ownership_engine = OwnershipInferenceEngine()
        
    def infer_control_structure(self) -> Dict[str, Any]:
        """Runs the semantic ownership engine logic upon the configured graph."""
        direct = self.ownership_engine.compute_direct_control(self.graph)
        indirect = self.ownership_engine.compute_indirect_control(self.graph)
        ubo = self.ownership_engine.identify_ultimate_controllers(self.graph)
        
        return {
            "ultimate_controllers": ubo,
            "control_percentages": {"direct": direct, "indirect": indirect}
        }
        
    def detect_strategic_vulnerabilities(self, control_structure: Dict[str, Any]) -> Any:
        """Helper to invoke weak founder detection rules natively against the graph struct."""
        from intelligence.weak_founder_detector import WeakFounderDetector
        detector = WeakFounderDetector()
        return detector.detect_weak_founders(control_structure, self.graph)
        
    def analyze_influence_network(self) -> Dict[str, Any]:
        """Maps broad soft-power structures using the InfluenceNetworkMapper."""
        from intelligence.influence_mapper import InfluenceNetworkMapper
        mapper = InfluenceNetworkMapper()
        
        influence_scores = {}
        for node in self.graph.nodes():
            influence_scores[node] = mapper.compute_influence_score(node, self.graph)
            
        return {
            "influence_scores": influence_scores,
            "interlocks": mapper.detect_director_interlocks(self.graph),
            "clusters": mapper.identify_influence_clusters(self.graph)
        }

    def detect_acquisition_targets(self, vulnerabilities: List[Dict[str, Any]], influence_data: Dict[str, Any]) -> Dict[str, Any]:
        """Runs multi-dimensional checks linking graph intelligence to acquisition viability."""
        from intelligence.acquisition_target_engine import AcquisitionTargetEngine
        engine = AcquisitionTargetEngine()
        return engine.identify_acquisition_targets(vulnerabilities, influence_data)
