"""
Credentials API endpoints
"""
from typing import Dict, Any, List, Optional

from .base import BaseAPI
from ..models.credentials import Credential, CredentialList, CredentialExpanded


class CredentialsAPI(BaseAPI):
    """API client for credentials endpoints"""
    
    def list(self, limit: int = 100, offset: int = 0) -> CredentialList:
        """
        List credentials
        
        Args:
            limit: Number of items to return
            offset: Pagination offset
            
        Returns:
            CredentialList containing credentials
        """
        return self._get("/credentials", params={"limit": limit, "offset": offset}, model_class=CredentialList)
        
    def get(self, credential_id: str, expand: bool = False) -> Credential:
        """
        Get a credential by ID
        
        Args:
            credential_id: Credential ID
            expand: Whether to expand the resource details
            
        Returns:
            Credential object
        """
        path = f"/credentials/{credential_id}"
        if expand:
            path += "?expand=1"
            
        return self._get(path, model_class=Credential if not expand else CredentialExpanded)
        
    def create(self, credential_data: Dict[str, Any]) -> Credential:
        """
        Create a new credential
        
        Args:
            credential_data: Credential configuration
            
        Returns:
            Created Credential object
        """
        return self._post("/credentials", json=credential_data, model_class=Credential)
        
    def update(self, credential_id: str, credential_data: Dict[str, Any]) -> Credential:
        """
        Update a credential
        
        Args:
            credential_id: Credential ID
            credential_data: Credential configuration to update
            
        Returns:
            Updated Credential object
        """
        return self._put(f"/credentials/{credential_id}", json=credential_data, model_class=Credential)
        
    def delete(self, credential_id: str) -> Dict[str, Any]:
        """
        Delete a credential
        
        Args:
            credential_id: Credential ID
            
        Returns:
            Empty dictionary on success
        """
        return self._delete(f"/credentials/{credential_id}")
        
    def copy(self, credential_id: str, new_name: Optional[str] = None) -> Credential:
        """
        Create a copy of a credential
        
        Args:
            credential_id: Credential ID
            new_name: Optional new name for the copied credential
            
        Returns:
            New Credential object
        """
        params = {}
        if new_name:
            params["name"] = new_name
            
        return self._post(f"/credentials/{credential_id}/copy", params=params, model_class=Credential)
        
    def probe(self, credential_id: str) -> Dict[str, Any]:
        """
        Test a data credential
        
        Args:
            credential_id: Data credential ID
            
        Returns:
            Probe results
        """
        return self._post(f"/data_credentials/{credential_id}/probe")
        
    def probe_tree(self, credential_id: str, path: Optional[str] = None) -> Dict[str, Any]:
        """
        Get a directory/file tree for a data credential
        
        Args:
            credential_id: Data credential ID
            path: Optional path to get the tree for
            
        Returns:
            Directory tree
        """
        params = {}
        if path:
            params["path"] = path
            
        return self._post(f"/data_credentials/{credential_id}/probe/tree", params=params)
        
    def probe_sample(self, credential_id: str, path: str) -> Dict[str, Any]:
        """
        Get a sample of data for a data credential
        
        Args:
            credential_id: Data credential ID
            path: Path to the file to sample
            
        Returns:
            Data sample
        """
        return self._post(
            f"/data_credentials/{credential_id}/probe/sample",
            params={"path": path}
        ) 