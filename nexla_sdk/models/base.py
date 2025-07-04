from typing import TypeVar, Any, Dict
import json
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
    - Easy logging and printing support
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
    
    def to_dict(self, exclude_none: bool = True) -> Dict[str, Any]:
        """
        Convert model to dictionary.
        
        Args:
            exclude_none: Whether to exclude None values
        
        Returns:
            Dictionary representation
        """
        return self.model_dump(exclude_none=exclude_none)
    
    def to_json(self, exclude_none: bool = True, indent: int = 2) -> str:
        """
        Convert model to JSON string.
        
        Args:
            exclude_none: Whether to exclude None values
            indent: JSON indentation level
        
        Returns:
            JSON string representation
        """
        return json.dumps(self.to_dict(exclude_none=exclude_none), indent=indent, default=str)
    
    def __str__(self) -> str:
        """
        String representation of the model.
        
        Returns:
            Formatted string showing model name and key fields
        """
        # Get model name
        model_name = self.__class__.__name__
        
        # Get key fields for display (limit to avoid too much output)
        data = self.to_dict(exclude_none=True)
        
        # Show first few key fields
        key_fields = []
        for key, value in list(data.items())[:5]:  # Show first 5 fields
            if isinstance(value, str):
                key_fields.append(f"{key}='{value}'")
            else:
                key_fields.append(f"{key}={value}")
        
        field_str = ", ".join(key_fields)
        
        # Add "..." if there are more fields
        if len(data) > 5:
            field_str += ", ..."
        
        return f"{model_name}({field_str})"
    
    def __repr__(self) -> str:
        """
        Detailed string representation of the model.
        
        Returns:
            Detailed string representation
        """
        return f"{self.__class__.__name__}({self.to_dict(exclude_none=True)})"
