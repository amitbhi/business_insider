"""finance Collector Module"""
from ..base.base_agent import BaseCollector
from typing import Dict, Any

class FinanceCollector(BaseCollector):
    def __init__(self, data_source: str = "mock"):
        self.data_source = data_source

    async def collect(self, target: str) -> Dict[str, Any]:
        if self.data_source == "mca":
            return {"module": "finance", "status": "collected_from_mca", "source": "mca"}
        return {"module": "finance", "status": "collected"}

