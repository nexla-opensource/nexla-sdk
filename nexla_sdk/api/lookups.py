"""
Lookups API endpoints
"""
from typing import Dict, Any, List, Optional

from .base import BaseAPI
from ..models.lookups import Lookup, LookupList, LookupExpanded


class LookupsAPI(BaseAPI):
    """API client for lookups endpoints"""
    
    def list(self, limit: int = 100, offset: int = 0) -> LookupList:
        """
        List lookups
        
        Args:
            limit: Number of items to return
            offset: Pagination offset
            
        Returns:
            LookupList containing lookups
        """
        return self._get("/lookups", params={"limit": limit, "offset": offset}, model_class=LookupList)
        
    def get(self, lookup_id: str, expand: bool = False) -> Lookup:
        """
        Get a lookup by ID
        
        Args:
            lookup_id: Lookup ID
            expand: Whether to expand the resource details
            
        Returns:
            Lookup object
        """
        path = f"/lookups/{lookup_id}"
        if expand:
            path += "?expand=1"
            
        return self._get(path, model_class=Lookup if not expand else LookupExpanded)
        
    def create(self, lookup_data: Dict[str, Any]) -> Lookup:
        """
        Create a new lookup
        
        Args:
            lookup_data: Lookup configuration
            
        Returns:
            Created Lookup object
        """
        return self._post("/lookups", json=lookup_data, model_class=Lookup)
        
    def update(self, lookup_id: str, lookup_data: Dict[str, Any]) -> Lookup:
        """
        Update a lookup
        
        Args:
            lookup_id: Lookup ID
            lookup_data: Lookup configuration to update
            
        Returns:
            Updated Lookup object
        """
        return self._put(f"/lookups/{lookup_id}", json=lookup_data, model_class=Lookup)
        
    def delete(self, lookup_id: str) -> Dict[str, Any]:
        """
        Delete a lookup
        
        Args:
            lookup_id: Lookup ID
            
        Returns:
            Empty dictionary on success
        """
        return self._delete(f"/lookups/{lookup_id}")
        
    def copy(self, lookup_id: str, new_name: Optional[str] = None) -> Lookup:
        """
        Create a copy of a lookup
        
        Args:
            lookup_id: Lookup ID
            new_name: Optional new name for the copied lookup
            
        Returns:
            New Lookup object
        """
        params = {}
        if new_name:
            params["name"] = new_name
            
        return self._post(f"/lookups/{lookup_id}/copy", params=params, model_class=Lookup) 