from typing import Optional
from .base import RegistryAdapter
from .mca_adapter import MCAAdapter
from .sec_adapter import SECAdapter
from .eu_adapter import EUAdapter

class RegistryFactory:
    """
    Factory to return the appropriate Registry Adapter based on jurisdiction.
    """
    
    @staticmethod
    def get_adapter(country: str) -> RegistryAdapter:
        country = country.upper()
        if country in ["INDIA", "IN"]:
            return MCAAdapter()
        elif country in ["USA", "US"]:
            return SECAdapter()
        elif country in ["EU", "UK", "GERMANY", "FRANCE", "NETHERLANDS"]:
            return EUAdapter()
        else:
            # Default to India if not specified, or raise error
            print(f"Jurisdiction {country} not fully implemented. Falling back to MCA Mock.")
            return MCAAdapter()
