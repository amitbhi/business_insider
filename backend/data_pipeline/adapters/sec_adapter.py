import os
import httpx
from typing import Dict, Any, List
from .base import RegistryAdapter

class SECAdapter(RegistryAdapter):
    """
    Adapter for the SEC (USA) - EDGAR data.
    """
    
    def __init__(self):
        # SEC requires a descriptive User-Agent header (Person/Email)
        self.user_agent = os.getenv("SEC_USER_AGENT", "BusinessInsider/1.0 (Research Project)")
        self.base_url = "https://data.sec.gov/submissions"

    async def fetch_company_master(self, company_id: str) -> Dict[str, Any]:
        """Fetch high-level company data via CIK."""
        # Normalize CIK to 10 digits
        cik = company_id.zfill(10)
        
        if os.getenv("USE_LIVE_SEC"):
            async with httpx.AsyncClient(headers={"User-Agent": self.user_agent}) as client:
                url = f"{self.base_url}/CIK{cik}.json"
                response = await client.get(url)
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "cik": cik,
                        "company_info": {
                            "name": data.get("name"),
                            "ticker": data.get("tickers", ["N/A"])[0],
                            "exchange": data.get("exchanges", ["N/A"])[0]
                        },
                        "directors": [] # SEC EDGAR submissions JSON doesn't list directors directly, needs parsing of 4/DEF14A
                    }

        # Mock fallback
        return {
            "cik": cik,
            "company_info": {
                "name": f"US Entity {cik}",
                "authorized_capital": "N/A",
                "paid_up_capital": "N/A",
                "registered_address": "Delaware, USA"
            },
            "directors": [
                {"din": "US-123", "name": "STEVE JOBS", "designation": "CEO", "date_of_appointment": "2010-01-01"},
            ]
        }
        
    async def fetch_ownership_data(self, company_id: str) -> List[Dict[Dict[str, Any]]]:
        """Fetch SEC 13D/G ownership data."""
        # Simulated logic: This would normally query the open SEC API or Edgar-Query
        return [
            {"investor": "VANGUARD GROUP", "percentage": 7.5, "type": "Institutional"},
            {"investor": "BLACKROCK", "percentage": 6.8, "type": "Institutional"}
        ]
        
    async def fetch_directors(self, company_id: str) -> List[Dict[str, Any]]:
        data = await self.fetch_company_master(company_id)
        return data["directors"]
        
    async def fetch_filings(self, company_id: str) -> List[Dict[str, Any]]:
        return [
            {"filing_date": "2024-02-10", "form_type": "10-K", "status": "ACCEPTED"},
            {"filing_date": "2023-11-05", "form_type": "8-K", "status": "ACCEPTED"}
        ]
