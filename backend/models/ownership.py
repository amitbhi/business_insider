"""
Relational Association Model - Ownership / Relationship Edge.

Represents an edge linking nodes (Company -> Company, Person -> Company).
Stores structural connection data (Directorship, Parent/Subsidiary, Family).
"""

from typing import Optional
from pydantic import BaseModel

class RelationshipModel(BaseModel):
    """Data model representing an edge in the intelligence network."""
    id: str # UUID
    source_entity_id: str # FK -> Company or Person
    target_entity_id: str # FK -> Company or Person
    type: str # DIRECTOR_OF, SHAREHOLDER_OF, SUBSIDIARY_OF, FAMILY_MEMBER
    percentage_ownership: Optional[float] = None
    weight: float = 1.0 # Computed edge weight based on influence
