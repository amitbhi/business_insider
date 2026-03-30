"""
Base MCA Scraper Architecture.

Provides the interface for communicating with Ministry of Corporate Affairs (India)
or third-party proxy APIs. Built to swap out mock vs production ingesters.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List

class MCAScraperBase(ABC):
    """Abstract interface defining required scraping actions for Indian regulatory data."""
    
    @abstractmethod
    async def search_company(self, company_name: str) -> List[Dict[str, Any]]:
        """
        Query system to find exact entity match by fuzzy or exact string.
        Returns potential matches and their CINs.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_company_filings(self, company_id: str) -> Dict[str, Any]:
        """
        Retrieves raw structural, financial, and regulatory documents 
        (e.g., Annual Returns, MoA, AoA) associated with a CIN.
        """
        raise NotImplementedError
