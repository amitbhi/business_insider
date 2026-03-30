from typing import Dict, Any, List
from .vulnerability_scoring import VulnerabilityScoring
import networkx as nx

class WeakFounderDetector:
    """Core logic to deduce vulnerable founders using the formal V(F,j) scoring function."""
    
    def __init__(self):
        self.scorer = VulnerabilityScoring()
        
    def detect_weak_founders(self, control_structure: Dict[str, Any], graph: nx.DiGraph) -> List[Dict[str, Any]]:
        """
        Identifies "Weak Founders" using the pre-filter: control_pct > 0.30 AND ownership_pct < 0.10.
        Calculates the finalized Vulnerability Score V(F,j).
        """
        results = []
        control_percentages = control_structure.get("control_percentages", {}).get("indirect", {})
        
        # Ownership data extraction from graph
        for entity in graph.nodes():
            if graph.nodes[entity].get('type') == 'Investor':
                # Recursive Control pct (calculated by GOIE)
                control_pct = control_percentages.get(f"{entity}->{graph.graph.get('root_entity')}", 0.0)
                
                # Immediate direct ownership pct
                direct_edge = graph.get_edge_data(entity, graph.graph.get('root_entity'))
                ownership_pct = direct_edge.get('weight', 0.0) if direct_edge else 0.0
                
                # Pre-filter from Paper (Section IV.B)
                if control_pct > 0.30 and ownership_pct < 0.10:
                    # Calculate sub-scores (Mocks for board/tenure in V1)
                    board_score = 0.50 # Simulated board presence
                    tenure_score = 0.80 # Simulated tenure
                    
                    score = self.scorer.compute_vulnerability_score(
                        ownership_pct=ownership_pct,
                        control_pct=control_pct,
                        board_score=board_score,
                        tenure_score=tenure_score
                    )
                    
                    results.append({
                        "founder_name": entity,
                        "vulnerability_score": score,
                        "metrics": {
                            "ownership": ownership_pct,
                            "control": control_pct,
                            "disparity": abs(control_pct - ownership_pct)
                        },
                        "risk_classification": "HIGH" if score > 0.65 else ("MODERATE" if score > 0.40 else "SECURE")
                    })
                    
        return results
