"""Credentials resource implementation."""
from typing import List, Optional, Dict, Any
from nexla_sdk.resources.base_resource import BaseResource
from nexla_sdk.models.credentials.responses import Credential, ProbeTreeResponse, ProbeSampleResponse
from nexla_sdk.models.credentials.requests import (
    CredentialCreate, CredentialUpdate, ProbeTreeRequest, ProbeSampleRequest
)


class CredentialsResource(BaseResource):
    """Resource for managing data credentials."""
    
    def __init__(self, client):
        super().__init__(client)
        self._path = "/data_credentials"
        self._model_class = Credential
    
    def list(self, 
             credentials_type: Optional[str] = None,
             **kwargs) -> List[Credential]:
        """
        List all credentials.
        
        Args:
            credentials_type: Filter by credential type
            **kwargs: Additional parameters
        
        Returns:
            List of credentials
        """
        params = kwargs.copy()
        if credentials_type:
            params['credentials_type'] = credentials_type
        
        return super().list(**params)
    
    def get(self, credential_id: int, expand: bool = False) -> Credential:
        """
        Get single credential by ID.
        
        Args:
            credential_id: Credential ID
            expand: Include expanded references
        
        Returns:
            Credential instance
        """
        return super().get(credential_id, expand)
    
    def create(self, data: CredentialCreate) -> Credential:
        """
        Create new credential.
        
        Args:
            data: Credential creation data
        
        Returns:
            Created credential
        """
        return super().create(data)
    
    def update(self, credential_id: int, data: CredentialUpdate) -> Credential:
        """
        Update credential.
        
        Args:
            credential_id: Credential ID
            data: Updated credential data
        
        Returns:
            Updated credential
        """
        return super().update(credential_id, data)
    
    def delete(self, credential_id: int) -> Dict[str, Any]:
        """
        Delete credential.
        
        Args:
            credential_id: Credential ID
        
        Returns:
            Response with status
        """
        return super().delete(credential_id)
    
    def probe(self, credential_id: int) -> Dict[str, Any]:
        """
        Test credential validity.
        
        Args:
            credential_id: Credential ID
        
        Returns:
            Probe response
        """
        path = f"{self._path}/{credential_id}/probe"
        response = self._make_request('GET', path)
        
        # Handle cases where the response might be None or contain raw text
        if response is None:
            return {"status": "success", "message": "Credential probe completed successfully"}
        elif isinstance(response, dict) and "raw_text" in response:
            return {"status": "success", "message": response["raw_text"], "status_code": response.get("status_code")}
        else:
            return response
    
    def probe_tree(self, 
                   credential_id: int, 
                   request: ProbeTreeRequest) -> ProbeTreeResponse:
        """
        Preview storage structure accessible by credential.
        
        Args:
            credential_id: Credential ID
            request: Probe tree request
        
        Returns:
            Storage structure response
        """
        path = f"{self._path}/{credential_id}/probe/tree"
        response = self._make_request('POST', path, json=request.to_dict())
        return ProbeTreeResponse(**response)
    
    def probe_sample(self, 
                     credential_id: int,
                     request: ProbeSampleRequest) -> ProbeSampleResponse:
        """
        Preview data content accessible by credential.
        
        Args:
            credential_id: Credential ID
            request: Probe sample request
        
        Returns:
            Sample data response
        """
        path = f"{self._path}/{credential_id}/probe/sample"
        response = self._make_request('POST', path, json=request.to_dict())
        return ProbeSampleResponse(**response)
