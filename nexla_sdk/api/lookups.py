"""
Lookups API endpoints
"""
from typing import Dict, Any, List, Optional, Union, BinaryIO
from io import StringIO
import requests

from .base import BaseAPI
from ..models.access import AccessRole
from ..models.lookups import (
    Lookup, LookupList, LookupExpanded, DataMapEntryBatch, 
    CreateDataMapRequest, UpdateDataMapRequest, DeleteDataMapResponse,
    SampleEntriesRequest, SampleEntriesResponse
)


class LookupsAPI(BaseAPI):
    """API client for lookups endpoints"""
    
    def list(self, page: int = 1, per_page: int = 100, access_role: Optional[AccessRole] = None, 
             validate: bool = False) -> LookupList:
        """
        List lookups (data maps)
        
        Args:
            page: Page number for pagination
            per_page: Number of items per page
            access_role: Filter by access role
            validate: Include entry counts and caching information
            
        Returns:
            LookupList containing lookups
        """
        params = {"page": page, "per_page": per_page}
        if access_role:
            params["access_role"] = access_role.value
        if validate:
            params["validate"] = 1
            
        response = self.client.request("GET", "/data_maps", params=params)
        
        # Handle both array responses and structured paginated responses
        if isinstance(response, list):
            # Direct array of items
            items = [self.client._convert_to_model(item, Lookup) for item in response]
            return LookupList(items=items, total=len(items), page=page, per_page=per_page)
        elif isinstance(response, dict) and "items" in response:
            # Structured paginated response
            items = [self.client._convert_to_model(item, Lookup) for item in response.get("items", [])]
            return LookupList(
                items=items,
                total=response.get("total", len(items)),
                page=response.get("page", page),
                per_page=response.get("per_page", per_page)
            )
        else:
            # Fallback for other response formats
            items = [self.client._convert_to_model(item, Lookup) for item in (response or [])]
            return LookupList(items=items, total=len(items), page=page, per_page=per_page)
        
    def get(self, lookup_id: str, expand: bool = False, validate: bool = False) -> Lookup:
        """
        Get a lookup (data map) by ID
        
        Args:
            lookup_id: Lookup ID
            expand: Whether to expand the resource details
            validate: Include entry counts and caching information
            
        Returns:
            Lookup object
        """
        params = {}
        if expand:
            params["expand"] = 1
        if validate:
            params["validate"] = 1
            
        return self._get(f"/data_maps/{lookup_id}", params=params, model_class=Lookup if not expand else LookupExpanded)
        
    def create(self, lookup_data: Union[Dict[str, Any], CreateDataMapRequest]) -> Lookup:
        """
        Create a new lookup (data map)
        
        For static lookups, provide:
        - name
        - data_type
        - map_primary_key (field to use for matching)
        - data_defaults (optional, default values for keys)
        - data_map (optional, array of objects for initial mapping)
        
        For dynamic lookups, also provide:
        - data_sink_id (ID of the data destination)
        
        Args:
            lookup_data: Lookup configuration or CreateDataMapRequest instance
            
        Returns:
            Created Lookup object
        """
        return self._post("/data_maps", json=lookup_data, model_class=Lookup)
        
    def update(self, lookup_id: str, lookup_data: Union[Dict[str, Any], UpdateDataMapRequest]) -> Lookup:
        """
        Update a lookup (data map)
        
        For static maps, you can update metadata and/or the entire mapping at once.
        Note: To update specific entries, use upsert_entries() instead.
        
        Args:
            lookup_id: Lookup ID
            lookup_data: Lookup configuration to update or UpdateDataMapRequest instance
            
        Returns:
            Updated Lookup object
        """
        return self._put(f"/data_maps/{lookup_id}", json=lookup_data, model_class=Lookup)
        
    def delete(self, lookup_id: str) -> DeleteDataMapResponse:
        """
        Delete a lookup (data map)
        
        Args:
            lookup_id: Lookup ID
            
        Returns:
            DeleteDataMapResponse with status message
        """
        return self._delete(f"/data_maps/{lookup_id}", model_class=DeleteDataMapResponse)
        
    def copy(self, lookup_id: str, new_name: Optional[str] = None) -> Lookup:
        """
        Create a copy of a lookup (data map)
        
        Args:
            lookup_id: Lookup ID
            new_name: Optional new name for the copied lookup
            
        Returns:
            New Lookup object
        """
        params = {}
        if new_name:
            params["name"] = new_name
            
        return self._post(f"/data_maps/{lookup_id}/copy", params=params, model_class=Lookup)
        
    def upsert_entries(self, lookup_id: str, entries: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Upsert (add or update) entries to a data map
        
        Use this to update specific entries without replacing the entire mapping.
        
        Args:
            lookup_id: Lookup (data map) ID
            entries: List of entries to upsert, each being a dictionary of key-value pairs
            
        Returns:
            Dictionary with success message
        """
        data = {"entries": entries}
        return self._put(f"/data_maps/{lookup_id}/entries", json=data)
        
    def check_entries(self, lookup_id: str, entry_keys: Union[str, List[str]]) -> List[Dict[str, Any]]:
        """
        Check data map entries that match the specified keys
        
        Args:
            lookup_id: Lookup (data map) ID
            entry_keys: Single key or list of keys (can include wildcards)
            
        Returns:
            List of matching entries
        """
        if isinstance(entry_keys, list):
            entry_keys = ",".join([str(key) for key in entry_keys])
            
        return self._get(f"/data_maps/{lookup_id}/entries/{entry_keys}")
        
    def delete_entries(self, lookup_id: str, entry_keys: Union[str, List[str]]) -> Dict[str, Any]:
        """
        Delete specific entries from a data map
        
        Args:
            lookup_id: Lookup (data map) ID
            entry_keys: Single key or list of keys to delete (wildcards NOT supported)
            
        Returns:
            Success response
        """
        if isinstance(entry_keys, list):
            entry_keys = ",".join([str(key) for key in entry_keys])
            
        return self._delete(f"/data_maps/{lookup_id}/entries/{entry_keys}")
        
    def download_entries(self, lookup_id: str) -> str:
        """
        Download all entries from a data map in CSV format
        
        Args:
            lookup_id: Lookup (data map) ID
            
        Returns:
            CSV string containing all entries
        """
        # The download endpoint returns raw CSV data, not JSON
        # Use the client's request method with raw_response=True to get the text content
        url = f"{self.client.api_url}/data_maps/{lookup_id}/download_map"
        
        # Get access token from auth handler and ensure it's valid
        access_token = self.client.auth_handler.ensure_valid_token()
        
        headers = {
            "Accept": f"application/vnd.nexla.api.{self.client.api_version}+json",
            "Authorization": f"Bearer {access_token}"
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        return response.text
        
    def get_sample_entries(self, lookup_id: str, field_name: str = "*", page: int = 1, 
                           per_page: int = 10) -> SampleEntriesResponse:
        """
        Get sample entries from a data map
        
        Args:
            lookup_id: Lookup (data map) ID
            field_name: Field name to filter on, or "*" for all fields
            page: Page number for pagination
            per_page: Number of items per page
            
        Returns:
            SampleEntriesResponse containing sample entries
        """
        params = {"page": page, "per_page": per_page}
        data = {"field.name": field_name} if field_name != "*" else {"id.field.name": field_name}
        
        # Make the request and handle various response formats
        response = self.client.request("POST", f"/data_maps/{lookup_id}/probe/sample", params=params, json=data)
        
        # Let the model validator handle all different response formats
        return self.client._convert_to_model(response, SampleEntriesResponse) 