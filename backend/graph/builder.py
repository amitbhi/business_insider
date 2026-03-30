from typing import Any, Dict
import networkx as nx

class GraphBuilder:
    """Transforms jurisdictional registry data into a NetworkX directed graph."""
    
    def __init__(self, postgres_manager):
        self.db = postgres_manager
        self.graph = nx.DiGraph()
        
    def add_node(self, node_id: str, attributes: dict):
        """Append node safely to the network structure."""
        self.graph.add_node(node_id, **attributes)

    def add_edge(self, source_id: str, target_id: str, relationship: str, weight: float = 1.0):
        """Build relational link representing control/ownership/law."""
        self.graph.add_edge(source_id, target_id, type=relationship, weight=weight)

    def build_ownership_graph(self, root_entity_id: str) -> nx.DiGraph:
        """Constructs a graph centered around an entity."""
        if not self.graph.has_node(root_entity_id):
            self.add_node(root_entity_id, {"type": "Company", "name": root_entity_id})
        self.graph.graph["root_entity"] = root_entity_id
        return self.graph

    def build_from_registry_data(self, master_data: Dict[str, Any], ownership_data: list):
        """Populates the graph from the Intelligence Context Object (ICO)."""
        root_name = master_data.get("company_info", {}).get("name", "Unknown")
        root_id = master_data.get("cin") or master_data.get("cik") or master_data.get("registration_number") or root_name
        self.add_node(root_id, {"type": "Company", "name": root_name})
        self.graph.graph["root_entity"] = root_id
        
        for director in master_data.get("directors", []):
            d_id = director.get("din") or director.get("name")
            self.add_node(d_id, {"type": "Director", "name": director.get("name")})
            self.add_edge(d_id, root_id, "DIRECTS")
            
        for owner in ownership_data:
            o_name = owner.get("investor")
            weight = owner.get("percentage", 0.0) / 100.0
            self.add_node(o_name, {"type": "Investor", "name": o_name})
            self.add_edge(o_name, root_id, "OWNS", weight=weight)
            
        return self.graph
