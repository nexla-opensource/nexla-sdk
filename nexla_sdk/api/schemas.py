"""
Schemas API client
"""
import logging
from typing import Dict, Any, List, Optional, Union, cast

from .base import BaseAPI
from ..models.schemas import DataSchema, SchemaList

logger = logging.getLogger(__name__)


class SchemasAPI(BaseAPI):
    """Client for the Nexla Schemas API"""
    
    def list(self, template: Optional[bool] = None, page: int = 1, per_page: int = 100) -> SchemaList:
        """
        List all schemas owned by the authenticated user
        
        Args:
            template: Optional filter for template status
                If True, return only templates, if False, return only non-templates
            page: Page number for pagination
            per_page: Number of items per page
                
        Returns:
            SchemaList object containing DataSchema items
        """
        path = "/data_schemas"
        
        # Add query parameters if specified
        params = {"page": page, "per_page": per_page}
        if template is not None:
            params["template"] = 1 if template else 0
            
        # Get raw response as a list of schemas
        response = self._get(path, params=params)
        
        # If response is empty, return an empty SchemaList
        if not response:
            return SchemaList(items=[], total=0, page=page, page_size=per_page)
            
        # Convert the list of schemas to DataSchema objects
        schemas = []
        for schema_data in response:
            try:
                schema = DataSchema.model_validate(schema_data)
                schemas.append(schema)
            except Exception as e:
                # Log the error and continue
                logger.warning(f"Failed to validate schema: {e}")
                continue
                
        return SchemaList(
            items=schemas,
            total=len(schemas),  # Use actual count as total
            page=page,
            page_size=per_page
        )
    
    def get(self, schema_id: Union[str, int], expand: bool = False) -> DataSchema:
        """
        Get a schema by ID
        
        Args:
            schema_id: Schema ID
            expand: Whether to expand the resource details (include data sets)
            
        Returns:
            DataSchema object
        """
        path = f"/data_schemas/{schema_id}"
        
        # Add query parameters if specified
        params = {}
        if expand:
            params["expand"] = 1
            
        return self._get(path, params=params, model_class=DataSchema)
    
    def create(self, schema_data: Dict[str, Any]) -> DataSchema:
        """
        Create a new schema
        
        Args:
            schema_data: Schema configuration with any of the following:
                - Schema specification (name, schema, annotations, etc.)
                - data_set_id: ID of a dataset whose schema to copy
                - template: Whether to create as a template (default: false)
                
        Returns:
            Created DataSchema
        """
        return self._post("/data_schemas", json=schema_data, model_class=DataSchema)
    
    def create_from_dataset(self, dataset_id: Union[str, int], template: bool = False) -> DataSchema:
        """
        Create a new schema using the output schema of an existing dataset
        
        Args:
            dataset_id: ID of the dataset whose schema to copy
            template: Whether to create as a template
            
        Returns:
            Created DataSchema
        """
        schema_data = {
            "data_set_id": dataset_id,
            "template": template
        }
        return self.create(schema_data)
    
    def update(self, schema_id: Union[str, int], schema_data: Dict[str, Any]) -> DataSchema:
        """
        Update a schema
        
        Args:
            schema_id: Schema ID
            schema_data: Schema configuration to update
            
        Returns:
            Updated DataSchema
        """
        return self._put(f"/data_schemas/{schema_id}", json=schema_data, model_class=DataSchema)
    
    def delete(self, schema_id: Union[str, int]) -> Dict[str, Any]:
        """
        Delete a schema
        
        Args:
            schema_id: Schema ID
            
        Returns:
            Empty dictionary on success
        """
        return self._delete(f"/data_schemas/{schema_id}") 