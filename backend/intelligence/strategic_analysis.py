"""
Strategic Analysis Engine Module.

Acts as the core intelligence synthesizer. Combines data from various
intelligence sub-modules (weakness detection, control mapping).
"""
from typing import Dict, Any
from .weakness_detector import WeaknessDetector
from .control_analysis import ControlAnalyzer
from .influence_mapper import InfluenceNetworkMapper

class StrategicEngine:
    """Consolidates findings from all engines into a holistic strategic profile."""
    
    def generate_strategic_profile(self, ico: Dict[str, Any]) -> Dict[str, Any]:
        """
        Synthesizes the ICO (Intelligence Context Object) into strategic flags.
        """
        vulnerabilities = ico.get("vulnerabilities", [])
        influence = ico.get("influence_network", {})
        ubos = ico.get("control_structure", {}).get("ultimate_controllers", [])
        
        flags = []
        if any(v.get("vulnerability_score", 0) > 0.65 for v in vulnerabilities):
            flags.append("CRITICAL_FOUNDER_INSTABILITY")
            
        if len(ubos) > 3:
            flags.append("FRAGMENTED_UBO_BASE")
        elif len(ubos) == 1:
            flags.append("MONOLITHIC_CONTROL")
            
        # Interlock check
        if influence.get("interlocks"):
            flags.append("BOARD_INTERLOCK_RISK")
            
        return {
            "strategic_flags": flags,
            "risk_summary": f"Identified {len(flags)} strategic risk vectors.",
            "target_status": ico.get("acquisition_targets", {}).get("strategic_priority", "MONITOR")
        }
