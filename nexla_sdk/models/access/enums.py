from enum import Enum


class AccessorType(str, Enum):
    """Types of accessors."""
    USER = "USER"
    TEAM = "TEAM"
    ORG = "ORG" 
