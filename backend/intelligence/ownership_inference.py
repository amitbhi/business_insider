from typing import Dict, Any, List
import networkx as nx

class OwnershipInferenceEngine:
    """Core module for tracing entity relationships to find true control flow using recursive graph-theoretic models."""
    
    def compute_direct_control(self, graph: nx.DiGraph) -> Dict[str, float]:
        """
        Calculates direct percentage ownership from edges.
        """
        direct_control = {}
        for u, v, data in graph.edges(data=True):
            if data.get('type') == 'OWNS':
                direct_control[f"{u}->{v}"] = data.get('weight', 0.0)
        return direct_control

    def compute_indirect_control(self, graph: nx.DiGraph, max_depth: int = 4) -> Dict[str, float]:
        """
        Calculates cascading control chains using a recursive propagation model.
        Formula: C = O + O^2 + O^3 ...
        Ensures cycle detection using depth-limited DFS.
        """
        indirect_control = {}
        
        def trace_ownership(start_node: str, current_node: str, multiplier: float, depth: int, visited: set):
            if depth > max_depth or current_node in visited:
                return
            
            visited.add(current_node)
            
            for _, neighbor, data in graph.out_edges(current_node, data=True):
                if data.get('type') == 'OWNS':
                    weight = data.get('weight', 0.0)
                    effective_weight = multiplier * weight
                    
                    target_pair = f"{start_node}->{neighbor}"
                    indirect_control[target_pair] = indirect_control.get(target_pair, 0.0) + effective_weight
                    
                    trace_ownership(start_node, neighbor, effective_weight, depth + 1, visited.copy())

        for node in graph.nodes():
            trace_ownership(node, node, 1.0, 1, set())
            
        return indirect_control

    def identify_ultimate_controllers(self, graph: nx.DiGraph) -> List[Dict[str, Any]]:
        """
        Identifies Ultimate Beneficial Owners (UBO) by resolving long-run control chains.
        """
        control_matrix = self.compute_indirect_control(graph)
        ubo_candidates = {}
        
        for pair, weight in control_matrix.items():
            investor, company = pair.split('->')
            # If the investor is a person or an entity with no incoming OWNS edges, they are a candidate UBO
            if graph.in_degree(investor) == 0:
                ubo_candidates[investor] = ubo_candidates.get(investor, 0.0) + weight
                
        return [
            {"entity": entity, "effective_control": round(weight, 4), "type": "UBO"}
            for entity, weight in ubo_candidates.items() if weight > 0.10 # 10% threshold as per SEC/MCA
        ]
