"""power Agent Controller"""
from ..base.base_agent import BaseAgent
from .collector import PowerCollector
from .analyzer import PowerAnalyzer
from .inference import PowerInference
from .report import PowerReport

class PowerAgent(BaseAgent):
    def __init__(self, data_source: str = "mock"):
        self.collector = PowerCollector(data_source)
        self.analyzer = PowerAnalyzer()
        self.inference = PowerInference()
        self.reporter = PowerReport()

