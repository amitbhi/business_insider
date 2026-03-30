"""
Base parser interface for standardizing data ingestion.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseParser(ABC):
    @abstractmethod
    def parse(self, raw_document: Any) -> Dict[str, Any]:
        """Convert unstructured doc into dict representation."""
        raise NotImplementedError
