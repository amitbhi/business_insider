import os
import httpx
from typing import Dict, Any, List
from .base import RegistryAdapter

class EUAdapter(RegistryAdapter):
    """
    Adapter for the EU (BRIS / Companies House UK).
    """
    
    def __init__(self):
        self.api_key = os.getenv("COMPANIES_HOUSE_API_KEY")
        self.base_url = "https://api.company-information.service.gov.uk"

    async def fetch_company_master(self, company_id: str) -> Dict[str, Any]:
        """Fetch high-level company data."""
        if self.api_key:
            auth = httpx.BasicAuth(user=self.api_key, password="")
            async with httpx.AsyncClient(auth=auth) as client:
                url = f"{self.base_url}/company/{company_id}"
                response = await client.get(url)
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "registration_number": company_id,
                        "company_info": {
                            "name": data.get("company_name"),
                            "status": data.get("company_status"),
                            "registered_address": data.get("registered_office_address", {}).get("address_line_1")
                        },
                        "directors": [] # Requires /company/{id}/officers call
                    }

        # Mock fallback
        return {
            "registration_number": company_id,
            "company_info": {
                "name": f"EU Entity {company_id}",
                "authorized_capital": "N/A",
                "paid_up_capital": "N/A",
                "registered_address": "Amsterdam, Netherlands"
            },
            "directors": [
                {"din": "EU-789", "name": "JEAN-CLAUDE VAN", "designation": "Director", "date_of_appointment": "2020-06-15"},
            ]
        }
        
    async def fetch_ownership_data(self, company_id: str) -> List[Dict[str, Any]]:
        """Fetch Companies House PSC (Persons with Significant Control) data."""
        return [
            {"investor": "MAJOR HOLDINGS B.V.", "percentage": 85.0, "type": "Parent"},
            {"investor": "FOUNDER X", "percentage": 15.0, "type": "Individual"}
        ]
        
    async def fetch_directors(self, company_id: str) -> List[Dict[str, Any]]:
        data = await self.fetch_company_master(company_id)
        return data["directors"]
        
    async def fetch_filings(self, company_id: str) -> List[Dict[str, Any]]:
        return [
            {"filing_date": "2024-01-05", "form_type": "AA01", "status": "APPROVED"}
        ]
