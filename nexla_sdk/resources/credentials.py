"""Credentials resource implementation."""
from typing import List, Optional, Dict, Any
from nexla_sdk.resources.base_resource import BaseResource
from nexla_sdk.models.credentials.responses import Credential, ProbeTreeResponse, ProbeSampleResponse
from nexla_sdk.models.credentials.requests import ProbeTreeRequest, ProbeSampleRequest


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
    
    def probe(self, credential_id: int) -> Dict[str, Any]:
        """
        Test credential validity.
        
        Args:
            credential_id: Credential ID
        
        Returns:
            Probe response
        """
        path = f"{self._path}/{credential_id}/probe"
        return self._make_request('GET', path)
    
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
