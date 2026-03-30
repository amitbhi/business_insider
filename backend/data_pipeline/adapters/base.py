from abc import ABC, abstractmethod
from typing import Dict, Any, List

class RegistryAdapter(ABC):
    """
    Abstract Base Class for Registry Adapters (India, US, EU, etc.)
    """
    
    @abstractmethod
    async def fetch_company_master(self, company_id: str) -> Dict[str, Any]:
        """Fetch high-level company data."""
        raise NotImplementedError
        
    @abstractmethod
    async def fetch_ownership_data(self, company_id: str) -> List[Dict[str, Any]]:
        """Fetch shareholding/ownership relationships."""
        raise NotImplementedError
        
    @abstractmethod
    async def fetch_directors(self, company_id: str) -> List[Dict[str, Any]]:
        """Fetch list of directors and their IDs."""
        raise NotImplementedError
        
    @abstractmethod
    async def fetch_filings(self, company_id: str) -> List[Dict[str, Any]]:
        """Fetch regulatory filing history."""
        raise NotImplementedError
