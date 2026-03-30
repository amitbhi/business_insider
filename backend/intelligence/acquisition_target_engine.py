from typing import Dict, Any, List
import numpy as np

class AcquisitionTargetEngine:
    """Evaluates targets using the formal Business Insider AA(j) acquisition attractiveness model."""
    
    def compute_acquisition_score(self, vulnerabilities: List[Dict[str, Any]], influence_data: Dict[str, Any]) -> float:
        """
        Calculates AA(j) = alpha1 * sum(V_Fj) + alpha2 * S_j + alpha3 * mean_influence(V_j)
        Weights: alpha1=0.45, alpha2=0.30, alpha3=0.25
        """
        a1, a2, a3 = 0.45, 0.30, 0.25
        
        # 1. Aggregate Founder Vulnerability
        v_scores = [v.get("vulnerability_score", 0.0) for v in vulnerabilities]
        sum_v = sum(v_scores) if v_scores else 0.0
        
        # 2. Systemic Importance Score S(j) (MOCKED for V1)
        s_j = 0.75 
        
        # 3. Mean Influence of Vulnerable Nodes
        influence_scores = influence_data.get("influence_scores", {})
        v_node_influences = [influence_scores.get(v.get("founder_name"), 0.0) for v in vulnerabilities]
        mean_i = np.mean(v_node_influences) / 100.0 if v_node_influences else 0.0
        
        # Final Score
        aa_score = (a1 * sum_v + a2 * s_j + a3 * mean_i)
        return round(float(aa_score), 4)
        
    def classify_target(self, score: float) -> str:
        """Categorizes targets by acquisition priority based on normalized AA(j)."""
        if score >= 0.70:
            return "HIGH_PRIORITY"
        elif score >= 0.40:
            return "MEDIUM_PRIORITY"
        return "MONITOR"

    def identify_acquisition_targets(self, vulnerabilities: List[Dict[str, Any]], influence_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Synthesizes all intelligence feeds to declare a target's strategic status.
        """
        aa_score = self.compute_acquisition_score(vulnerabilities, influence_data)
        priority = self.classify_target(aa_score)
        
        return {
            "acquisition_attractiveness_score": aa_score,
            "strategic_priority": priority,
            "justification": f"Target identified with aggregate founder vulnerability of {sum([v.get('vulnerability_score', 0) for v in vulnerabilities])}.",
            "recommended_action": "Proceed with due diligence" if priority == "HIGH_PRIORITY" else "Maintain surveillance"
        }
    
    def compute_strategic_fit(self, target_entity: str, acquirer_influence: Dict[str, Any]) -> float:
        """Future expansion: Calculates synergy between target and existing network."""
        return 0.50
