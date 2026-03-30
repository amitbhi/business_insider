"""legal Agent Controller"""
from ..base.base_agent import BaseAgent
from .collector import LegalCollector
from .analyzer import LegalAnalyzer
from .inference import LegalInference
from .report import LegalReport

class LegalAgent(BaseAgent):
    def __init__(self):
        self.collector = LegalCollector()
        self.analyzer = LegalAnalyzer()
        self.inference = LegalInference()
        self.reporter = LegalReport()

