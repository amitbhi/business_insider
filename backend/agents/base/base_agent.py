"""
Base Agent components to define the standard interface for all specialized intelligence agents.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseCollector(ABC):
    """Responsible for gathering raw data from external sources."""
    @abstractmethod
    async def collect(self, target: str) -> Dict[str, Any]:
        """Fetch raw data for the target entity."""
        raise NotImplementedError

class BaseAnalyzer(ABC):
    """Responsible for structuring and extracting facts from raw data."""
    @abstractmethod
    async def analyze(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process raw data into structured facts."""
        raise NotImplementedError

class BaseInference(ABC):
    """Responsible for strategic reasoning on structured facts."""
    @abstractmethod
    async def infer(self, structured_data: Dict[str, Any]) -> Dict[str, Any]:
        """Draw conclusions and identify patterns."""
        raise NotImplementedError

class BaseReport(ABC):
    """Responsible for formatting intelligence into standardized outputs."""
    @abstractmethod
    async def generate(self, inference_data: Dict[str, Any]) -> Dict[str, Any]:
        """Compile the final intelligence report for this domain."""
        raise NotImplementedError

class BaseAgent(ABC):
    """The orchestration wrapper for a specific intelligence domain."""
    
    def __init__(self):
        self.collector: BaseCollector | None = None
        self.analyzer: BaseAnalyzer | None = None
        self.inference: BaseInference | None = None
        self.reporter: BaseReport | None = None

    async def execute(self, target: str) -> Dict[str, Any]:
        """Run the complete agent lifecycle."""
        collector = self.collector
        analyzer = self.analyzer
        inference = self.inference
        reporter = self.reporter
        
        if not collector or not analyzer or not inference or not reporter:
            raise ValueError("Agent components are uninitialized.")
            
        raw_data = await collector.collect(target)
        structured_data = await analyzer.analyze(raw_data)
        inference_data = await inference.infer(structured_data)
        return await reporter.generate(inference_data)
