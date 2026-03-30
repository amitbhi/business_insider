"""
Base validator interface to secure data types before Database ingestion.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseValidator(ABC):
    @abstractmethod
    def validate(self, structured_data: Dict[str, Any]) -> bool:
        """Ensure entity payload meets rigorous database specifications."""
        raise NotImplementedError
