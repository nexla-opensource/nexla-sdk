from typing import TypeVar
from pydantic import BaseModel as PydanticBaseModel, ConfigDict

T = TypeVar('T', bound='BaseModel')


class BaseModel(PydanticBaseModel):
    """
    Base model class with Pydantic functionality and Nexla API compatibility.
    
    Features:
    - Automatically ignores unknown fields from API responses
    - Supports both camelCase and snake_case field names
    - Handles datetime parsing automatically
    - Provides JSON serialization methods
    - Validates data types automatically
    """
    
    model_config = ConfigDict(
        # Ignore unknown fields from API responses
        extra="allow",
        # Allow population by field name and alias
        populate_by_name=True,
        # Validate assignment when setting attributes
        validate_assignment=True,
        # Use enum values instead of enum objects in serialization
        use_enum_values=True,
        # Allow arbitrary types (for complex nested objects)
        arbitrary_types_allowed=True,
        # Handle datetime strings automatically
        str_strip_whitespace=True,
        # Validate default values
        validate_default=True,
        # Allow both snake_case and camelCase field names
        from_attributes=True
    )
