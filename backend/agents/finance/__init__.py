"""finance Agent Controller"""
from ..base.base_agent import BaseAgent
from .collector import FinanceCollector
from .analyzer import FinanceAnalyzer
from .inference import FinanceInference
from .report import FinanceReport

class FinanceAgent(BaseAgent):
    def __init__(self, data_source: str = "mock"):
        self.collector = FinanceCollector(data_source)
        self.analyzer = FinanceAnalyzer()
        self.inference = FinanceInference()
        self.reporter = FinanceReport()

