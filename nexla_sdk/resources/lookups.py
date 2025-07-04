"""Lookups resource implementation."""
from typing import List, Optional, Dict, Any, Union
from nexla_sdk.resources.base_resource import BaseResource
from nexla_sdk.models.lookups.responses import Lookup
from nexla_sdk.models.lookups.requests import LookupEntriesUpsert


class LookupsResource(BaseResource):
    """Resource for managing lookups (data maps)."""
    
    def __init__(self, client):
        super().__init__(client)
        self._path = "/data_maps"
        self._model_class = Lookup
    
    def upsert_entries(self,
                       data_map_id: int,
                       entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Upsert entries in a lookup.
        
        Args:
            data_map_id: Lookup ID
            entries: List of entries to upsert
        
        Returns:
            Updated entries
        """
        path = f"{self._path}/{data_map_id}/entries"
        request = LookupEntriesUpsert(entries=entries)
        return self._make_request('PUT', path, json=request.to_dict())
    
    def get_entries(self,
                    data_map_id: int,
                    entry_keys: Union[str, List[str]]) -> List[Dict[str, Any]]:
        """
        Get entries from lookup by keys.
        
        Args:
            data_map_id: Lookup ID
            entry_keys: Single key or list of keys (supports wildcards)
        
        Returns:
            Matching entries
        """
        if isinstance(entry_keys, list):
            keys_str = ','.join(str(k) for k in entry_keys)
        else:
            keys_str = str(entry_keys)
        
        path = f"{self._path}/{data_map_id}/entries/{keys_str}"
        return self._make_request('GET', path)
    
    def delete_entries(self,
                       data_map_id: int,
                       entry_keys: Union[str, List[str]]) -> Dict[str, Any]:
        """
        Delete entries from lookup by keys.
        
        Args:
            data_map_id: Lookup ID
            entry_keys: Single key or list of keys (supports wildcards)
        
        Returns:
            Response status
        """
        if isinstance(entry_keys, list):
            keys_str = ','.join(str(k) for k in entry_keys)
        else:
            keys_str = str(entry_keys)
        
        path = f"{self._path}/{data_map_id}/entries/{keys_str}"
        return self._make_request('DELETE', path)
