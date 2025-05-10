"""
Credentials API endpoints
"""
from typing import Dict, Any, List, Optional, Union

from .base import BaseAPI
from ..models.access import AccessRole
from ..models.credentials import (
    Credential, 
    CredentialList, 
    CredentialExpanded, 
    CredentialCreate,
    CredentialUpdate,
    ProbeResult,
    DirectoryTree,
    DataSample,
    DeleteDataCredentialResponse,
    FileProbeContent
)


class CredentialsAPI(BaseAPI):
    """API client for data credentials endpoints"""
    
    def list(self, access_role: Optional[AccessRole] = None, credentials_type: Optional[str] = None) -> List[Credential]:
        """
        List data credentials
        
        Args:
            access_role: Filter by access role
            credentials_type: Filter by credentials type
            
        Returns:
            List of Credential objects
        """
        params = {}
        if access_role:
            params["access_role"] = access_role.value
        if credentials_type:
            params["credentials_type"] = credentials_type
            
        return self._get("/data_credentials", params=params)
        
    def get(self, credential_id: Union[str, int], expand: bool = False) -> Union[Credential, CredentialExpanded]:
        """
        Get a data credential by ID
        
        Args:
            credential_id: Credential ID
            expand: Whether to expand the resource details
            
        Returns:
            Credential object
        """
        path = f"/data_credentials/{credential_id}"
        if expand:
            path += "?expand=1"
            
        return self._get(path, model_class=CredentialExpanded if expand else Credential)
        
    def create(self, credential_data: CredentialCreate) -> Credential:
        """
        Create a new data credential
        
        Args:
            credential_data: Credential configuration
            
        Returns:
            Created Credential object
        """
        return self._post(
            "/data_credentials", 
            json=credential_data.dict(), 
            model_class=CredentialExpanded
        )
        
    def update(self, credential_id: Union[str, int], credential_data: CredentialUpdate) -> CredentialExpanded:
        """
        Update a data credential
        
        Args:
            credential_id: Credential ID
            credential_data: Credential configuration to update
            
        Returns:
            Updated Credential object
        """
        return self._put(
            f"/data_credentials/{credential_id}", 
            json=credential_data.dict(), 
            model_class=CredentialExpanded
        )
        
    def delete(self, credential_id: Union[str, int]) -> DeleteDataCredentialResponse:
        """
        Delete a data credential
        
        Args:
            credential_id: Credential ID
            
        Returns:
            Response model with status code and message
        """
        return self._delete(
            f"/data_credentials/{credential_id}",
            model_class=DeleteDataCredentialResponse
        )
        
    def probe(self, credential_id: Union[str, int]) -> Dict[str, Any]:
        """
        Test a data credential
        
        Args:
            credential_id: Data credential ID
            
        Returns:
            Probe results
        """
        return self._get(f"/data_credentials/{credential_id}/probe")
        
    def probe_files(self, credential_id: Union[str, int], path: str, file: str) -> FileProbeContent:
        """
        Inspect file type credential content
        
        Args:
            credential_id: Data credential ID
            path: Path to the base directory
            file: Path to the file relative to base path
            
        Returns:
            File probe results with content details
        """
        payload = {
            "path": path,
            "file": file
        }
        
        return self._post(
            f"/data_credentials/{credential_id}/probe/files",
            json=payload,
            model_class=FileProbeContent
        )
        
    def probe_tree(
        self, 
        credential_id: Union[str, int], 
        depth: int = 1,
        path: Optional[str] = None, 
        database: Optional[str] = None,
        table: Optional[str] = None
    ) -> DirectoryTree:
        """
        Get a directory/file tree for a data credential
        
        Args:
            credential_id: Data credential ID
            depth: Hierarchy depth to scan
            path: Optional path to get the tree for (file-type connectors)
            database: Optional database name (database connectors)
            table: Optional table name (database connectors)
            
        Returns:
            Directory tree or database schema
        """
        payload = {"depth": depth}
        if path:
            payload["path"] = path
        if database:
            payload["database"] = database
        if table:
            payload["table"] = table
            
        return self._post(
            f"/data_credentials/{credential_id}/probe/tree", 
            json=payload,
            model_class=DirectoryTree
        )
        
    def probe_sample(
        self, 
        credential_id: Union[str, int], 
        path: Optional[str] = None,
        **connector_config
    ) -> DataSample:
        """
        Get a sample of data for a data credential
        
        Args:
            credential_id: Data credential ID
            path: Path to the file to sample (for file-type connectors)
            **connector_config: Additional connector-specific configuration
            
        Returns:
            Data sample
        """
        payload = {}
        if path:
            payload["path"] = path
        # Add any additional connector-specific config
        payload.update(connector_config)
            
        return self._post(
            f"/data_credentials/{credential_id}/probe/sample",
            json=payload,
            model_class=DataSample
        ) 