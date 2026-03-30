from typing import Dict, Any, List
from .base import RegistryAdapter
from ..scrapers.mca_master_data import MCAMasterDataClient
from ..scrapers.mca_company_search import MCACompanySearchClient

class MCAAdapter(RegistryAdapter):
    """
    Adapter for the Ministry of Corporate Affairs (India).
    """
    
    def __init__(self):
        self.master_client = MCAMasterDataClient()
        self.search_client = MCACompanySearchClient()
        
    async def fetch_company_master(self, company_id: str) -> Dict[str, Any]:
        """Fetch high-level company data via CIN."""
        return await self.master_client.get_master_data(company_id)
        
    async def fetch_ownership_data(self, company_id: str) -> List[Dict[str, Any]]:
        """
        Fetch shareholding/ownership relationships.
        Note: Nominee shareholding is often undisclosed in MCA primary records.
        """
        # For Phase 4/8, we simulate the recursion based on promoter declarations
        return [
            {"investor": "PROMOTER GROUP A", "percentage": 45.0, "type": "Promoter"},
            {"investor": "INSTITUTIONAL INVESTOR X", "percentage": 15.0, "type": "Institutional"},
            {"investor": "PUBLIC", "percentage": 40.0, "type": "Public"}
        ]
        
    async def fetch_directors(self, company_id: str) -> List[Dict[str, Any]]:
        """Fetch list of directors."""
        data = await self.master_client.get_master_data(company_id)
        return data.get("directors", [])
        
    async def fetch_filings(self, company_id: str) -> List[Dict[str, Any]]:
        """Fetch filing history."""
        # Simulated filing history
        return [
            {"filing_date": "2024-03-20", "form_type": "AOC-4", "status": "APPROVED"},
            {"filing_date": "2023-11-15", "form_type": "MGT-7", "status": "APPROVED"}
        ]
