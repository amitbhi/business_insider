"""
Power Collector Module
"""
from typing import Dict, Any
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from agents.base.base_agent import BaseCollector

from data_pipeline.scrapers.mca_company_search import MCACompanySearchClient
from data_pipeline.scrapers.mca_master_data import MCAMasterDataClient
from data_pipeline.cache.cache_manager import CacheManager
from data_pipeline.parsers.mca_parser_base import MCADocumentParserBase
from database.postgres import PostgresManager

class PowerCollector(BaseCollector):
    def __init__(self, data_source: str = "mock"):
        self.data_source = data_source
        self.search_client = MCACompanySearchClient()
        self.master_client = MCAMasterDataClient()
        self.cache = CacheManager()
        self.parser = MCADocumentParserBase()
        self.db = PostgresManager("postgresql://mock")

    async def collect(self, target: str) -> Dict[str, Any]:
        if self.data_source == "mca":
            # 1. Cache Check
            cached = self.cache.get_company_data(target.replace(" ", "_"))
            if cached:
                return {"module": "power", "status": "cached_mca", "data": cached}
                
            # 2. Network Fetch sequence
            search_results = await self.search_client.search_company(target)
            cin = search_results[0].get("cin", "UNKNOWN")
            
            # 3. Explicit Filing structures
            raw_master_data = await self.master_client.get_master_data(cin)
            
            # 4. Pipeline normalization
            parsed_entities = self.parser.parse_company_master_data(raw_master_data)
            self.cache.save_company_data(target.replace(" ", "_"), parsed_entities)
            
            # 5. Database Push natively triggering
            await self.db.save_full_company_profile(parsed_entities)

            return {
                "module": "power", 
                "status": "collected_from_mca", 
                "source": "mca",
                "cin": cin,
                "data": parsed_entities
            }
        return {"module": "power", "status": "collected"}
