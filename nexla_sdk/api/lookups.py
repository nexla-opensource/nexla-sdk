"""
Lookups API endpoints
"""
from typing import Dict, Any, List, Optional, Union

from .base import BaseAPI
from ..models.access import AccessRole
from ..models.lookups import (
    Lookup, LookupList, LookupExpanded, DataMapEntryBatch, 
    CreateDataMapRequest, UpdateDataMapRequest, DeleteDataMapResponse
)


class LookupsAPI(BaseAPI):
    """API client for lookups endpoints"""
    
    def list(self, page: int = 1, per_page: int = 100, access_role: Optional[AccessRole] = None) -> LookupList:
        """
        List lookups
        
        Args:
            page: Page number for pagination
            per_page: Number of items per page
            access_role: Filter by access role
            
        Returns:
            LookupList containing lookups
        """
        params = {"page": page, "per_page": per_page}
        if access_role:
            params["access_role"] = access_role.value
            
        return self._get("/lookups", params=params, model_class=LookupList)
        
    def get(self, lookup_id: str, expand: bool = False) -> Lookup:
        """
        Get a lookup (data map) by ID
        
        Args:
            lookup_id: Lookup ID
            expand: Whether to expand the resource details
            
        Returns:
            Lookup object
        """
        params = {}
        if expand:
            params["expand"] = 1
            
        return self._get(f"/data_maps/{lookup_id}", params=params, model_class=Lookup if not expand else LookupExpanded)
        
    def create(self, lookup_data: Union[Dict[str, Any], CreateDataMapRequest]) -> Lookup:
        """
        Create a new lookup (data map)
        
        Args:
            lookup_data: Lookup configuration or CreateDataMapRequest instance
            
        Returns:
            Created Lookup object
        """
        return self._post("/data_maps", json=lookup_data, model_class=Lookup)
        
    def update(self, lookup_id: str, lookup_data: Union[Dict[str, Any], UpdateDataMapRequest]) -> Lookup:
        """
        Update a lookup (data map)
        
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
        
    def upsert_entries(self, lookup_id: str, entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Upsert (add or update) entries to a static data map
        
        Args:
            lookup_id: Lookup (data map) ID
            entries: List of entries to upsert, each being a dictionary of key-value pairs
            
        Returns:
            List of updated/added entries
        """
        data = {"entries": entries}
        return self._put(f"/data_maps/{lookup_id}/entries", json=data)
        
    def check_entries(self, lookup_id: str, entry_keys: Union[str, List[str]]) -> List[Dict[str, Any]]:
        """
        Check data map entries that match the specified keys
        
        Args:
            lookup_id: Lookup (data map) ID
            entry_keys: Single key or comma-separated keys (can include wildcards)
            
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
            entry_keys: Single key or comma-separated keys (can include wildcards) to delete
            
        Returns:
            Success response
        """
        if isinstance(entry_keys, list):
            entry_keys = ",".join([str(key) for key in entry_keys])
            
        return self._delete(f"/data_maps/{lookup_id}/entries/{entry_keys}") 