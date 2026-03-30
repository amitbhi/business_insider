"""
Relational Entity Model - Company.

Represents a corporate entity node in the intelligence graph.
Designed for SQLAlchemy + PostgreSQL.
"""

from typing import Optional, Dict, Any
from pydantic import BaseModel

class CompanyModel(BaseModel):
    """Data model representing a corporate entity."""
    id: str # UUID
    cin: str # Corporate Identity Number (India)
    name: str # Registered entity name
    status: str # Active, Strike off etc.
    incorporation_date: Optional[str] = None
    paid_up_capital: float = 0.0
    metadata: Dict[str, Any] = {} # For flexible agent-found data
