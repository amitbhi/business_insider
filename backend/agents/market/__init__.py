"""market Agent Controller"""
from ..base.base_agent import BaseAgent
from .collector import MarketCollector
from .analyzer import MarketAnalyzer
from .inference import MarketInference
from .report import MarketReport

class MarketAgent(BaseAgent):
    def __init__(self):
        self.collector = MarketCollector()
        self.analyzer = MarketAnalyzer()
        self.inference = MarketInference()
        self.reporter = MarketReport()

