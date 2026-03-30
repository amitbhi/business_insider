"""social Agent Controller"""
from ..base.base_agent import BaseAgent
from .collector import SocialCollector
from .analyzer import SocialAnalyzer
from .inference import SocialInference
from .report import SocialReport

class SocialAgent(BaseAgent):
    def __init__(self):
        self.collector = SocialCollector()
        self.analyzer = SocialAnalyzer()
        self.inference = SocialInference()
        self.reporter = SocialReport()

