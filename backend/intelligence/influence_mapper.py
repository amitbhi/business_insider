from typing import Dict, Any, List
import networkx as nx

class InfluenceNetworkMapper:
    """Maps the soft-power networks using formal graph centrality metrics."""
    
    def compute_influence_score(self, entity: str, graph: nx.DiGraph) -> float:
        """
        Calculates I(v) = lambda1*BC(v) + lambda2*EC_centrality(v) + lambda3*PR(v) + lambda4*Degree(v)/|V|
        Weights: lambda1=0.30, lambda2=0.25, lambda3=0.25, lambda4=0.20
        """
        if not graph.has_node(entity):
            return 0.0
            
        # lambda weights
        l1, l2, l3, l4 = 0.30, 0.25, 0.25, 0.20
        
        # Centrality metrics
        bc = nx.betweenness_centrality(graph).get(entity, 0.0)
        
        try:
            # Eigenvector centrality can fail if graph doesn't converge or is disconnected
            ec = nx.eigenvector_centrality_numpy(graph).get(entity, 0.0)
        except:
            ec = 0.0
            
        pr = nx.pagerank(graph).get(entity, 0.0)
        deg = graph.degree(entity) / max(1, len(graph.nodes()))
        
        score = (l1 * bc + l2 * ec + l3 * pr + l4 * deg) * 100
        return round(float(score), 4)

    def detect_director_interlocks(self, graph: nx.DiGraph) -> List[Dict[str, Any]]:
        """Identifies nodes acting as bridges between different clusters (Board Interlocks)."""
        interlocks = []
        for node, data in graph.nodes(data=True):
            if data.get('type') == 'Director':
                # Check if director is connected to multiple company nodes
                companies = [v for u, v, d in graph.out_edges(node, data=True) if d.get('type') == 'DIRECTS']
                if len(companies) > 1:
                    interlocks.append({"director": node, "connected_entities": companies})
        return interlocks

    def identify_influence_clusters(self, graph: nx.DiGraph) -> List[List[str]]:
        """Detects broader coalitions using Louvain-like community detection (greedy modularity in NX)."""
        undirected_graph = graph.to_undirected()
        communities = nx.community.greedy_modularity_communities(undirected_graph)
        return [list(c) for c in communities]
