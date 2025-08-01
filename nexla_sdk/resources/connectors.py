"""Connectors resource implementation."""
import os
import json
from typing import List, Optional, Dict, Any
from nexla_sdk.resources.base_resource import BaseResource


class ConnectorsResource(BaseResource):
    """Resource for managing connectors."""
    
    def __init__(self, client):
        super().__init__(client)
        self._cache = None
        # Use absolute path relative to this file
        self.connectors_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            'models', 'connectors'
        )
    
    def _load_connectors(self) -> List[Dict[str, Any]]:
        """Load all connectors from JSON files with caching."""
        if self._cache is not None:
            return self._cache
            
        connectors = []
        if not os.path.exists(self.connectors_path):
            return connectors
            
        for file in os.listdir(self.connectors_path):
            if file.endswith('.json'):
                try:
                    with open(os.path.join(self.connectors_path, file), 'r') as f:
                        connector = json.load(f)
                        connectors.append({
                            "name": connector['name'],
                            "display_name": connector['display_name'],
                            "config": connector['config'],
                            "small_logo": connector['small_logo'],
                            "logo": connector['logo'],
                            "connection_type": connector['connection_type'],
                        })
                except (json.JSONDecodeError, KeyError):
                    # Skip malformed files
                    continue
                    
        self._cache = connectors
        return connectors
    
    def list(self, type: str = None, **_kwargs) -> List[Dict[str, Any]]:
        """
        List all connectors.
        
        Args:
            type: Filter by connector type ('source' or 'destination')
            **kwargs: Additional parameters
        
        Returns:
            List of connectors
        """
        connectors = self._load_connectors()
        
        if type:
            if type == 'source':
                connectors = [c for c in connectors if c['config'].get('isSource', False)]
            elif type == 'destination':
                connectors = [c for c in connectors if c['config'].get('isSink', False)]
        
        return connectors


        
    def get(self, name: str, **_kwargs) -> Optional[Dict[str, Any]]:
        """
        Get single connector by name.
        
        Args:
            name: Connector name
            **kwargs: Additional parameters
        
        Returns:
            Connector info or None if not found
        """
        # First try exact match
        file_path = os.path.join(self.connectors_path, f"{name}.json")
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    connector = json.load(f)
                    return connector
            except (json.JSONDecodeError, KeyError):
                pass
        
        # If not found, search through all connectors
        connectors = self._load_connectors()
        for connector in connectors:
            if connector['name'] == name:
                return connector
        
        return None
    