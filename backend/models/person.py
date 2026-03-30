"""
Relational Entity Model - Person.

Represents an individual node (Director, Shareholder, UBO, Politician)
in the intelligence graph.
"""

from typing import Optional, Dict, Any
from pydantic import BaseModel

class PersonModel(BaseModel):
    """Data model representing a human actor."""
    id: str # UUID
    din: Optional[str] = None # Director Identification Number
    pan: Optional[str] = None # Tax ID (Permanent Account Number)
    name: str # Full legal name
    address: Optional[str] = None # Used by SocialAgent for probabilistic family matching
    metadata: Dict[str, Any] = {} # e.g., {'political_affiliation': 'XYZ'}
