"""
Data caching module to safely throttle and optimize MCA and similar external API ingestion limits.
Stores responses explicitly into `.cache` filesystem paths or JSON keys to optimize re-runs.
"""
from typing import Dict, Any, Optional
import os
import json

class CacheManager:
    """Safely intercepts requests to read local files before hitting MCA endpoints."""
    
    def __init__(self, cache_dir: str = ".cache"):
        self.cache_dir = cache_dir
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
            
    def get_company_data(self, key: str) -> Optional[Dict[str, Any]]:
        """Attempt to retrieve target payload from File cache."""
        path = os.path.join(self.cache_dir, f"{key}.json")
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                pass
        return None
        
    def save_company_data(self, key: str, payload: Dict[str, Any]) -> None:
        """Saves successful JSON structured responses specifically isolated from Relational logic."""
        path = os.path.join(self.cache_dir, f"{key}.json")
        with open(path, "w") as f:
            json.dump(payload, f, indent=4)
