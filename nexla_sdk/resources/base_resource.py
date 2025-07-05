from typing import Dict, Any, Optional, List, TypeVar, Type, Union
from nexla_sdk.utils.pagination import Paginator, Page
from nexla_sdk.models.access import (
    AccessorResponse,
    AccessorRequestList, AccessorResponseList
)

T = TypeVar('T')


class BaseResource:
    """Base class for all Nexla resources."""
    
    def __init__(self, client):
        """
        Initialize resource.
        
        Args:
            client: Nexla client instance
        """
        self.client = client
        self._path = ""  # Override in subclasses
        self._model_class = None  # Override in subclasses
    
    def _make_request(self, 
                      method: str, 
                      path: str, 
                      **kwargs) -> Any:
        """Make HTTP request using client."""
        return self.client.request(method, path, **kwargs)
    
    def _serialize_data(self, data: Union[Dict[str, Any], Any]) -> Dict[str, Any]:
        """
        Convert data to dictionary for JSON serialization.
        
        Args:
            data: Data to serialize (dict or Pydantic model)
        
        Returns:
            Dictionary representation
        """
        if data is None:
            return {}
        
        # Check if it's a Pydantic model (has model_dump method)
        if hasattr(data, 'model_dump'):
            return data.model_dump(exclude_none=True)
        
        # If it's already a dict, return as-is
        if isinstance(data, dict):
            return data
        
        # For other types, try to convert to dict
        if hasattr(data, '__dict__'):
            return data.__dict__
        
        return data
    
    def _parse_response(self, response: Any, model_class: Optional[Type[T]] = None) -> Any:
        """Parse response into model objects."""
        model_class = model_class or self._model_class
        
        if not model_class:
            return response
        
        if isinstance(response, list):
            return [model_class.model_validate(item) if isinstance(item, dict) else item 
                    for item in response]
        elif isinstance(response, dict):
            return model_class.model_validate(response)
        return response
    
    def list(self, 
             page: Optional[int] = None,
             per_page: Optional[int] = None,
             access_role: Optional[str] = None,
             **params) -> List[T]:
        """
        List resources.
        
        Args:
            page: Page number
            per_page: Items per page
            access_role: Filter by access role (owner, collaborator, operator, admin)
            **params: Additional query parameters
        
        Returns:
            List of resources
        """
        query_params = {}
        if page is not None:
            query_params['page'] = page
        if per_page is not None:
            query_params['per_page'] = per_page
        if access_role is not None:
            query_params['access_role'] = access_role
        query_params.update(params)
        
        response = self._make_request('GET', self._path, params=query_params)
        return self._parse_response(response)
    
    def paginate(self,
                 per_page: int = 20,
                 access_role: Optional[str] = None,
                 **params) -> Paginator[T]:
        """
        Get paginator for iterating through resources.
        
        Args:
            per_page: Items per page
            access_role: Filter by access role
            **params: Additional query parameters
        
        Returns:
            Paginator instance
        """
        return Paginator(
            fetch_func=self.list,
            page_size=per_page,
            access_role=access_role,
            **params
        )
    
    def get(self, resource_id: int, expand: bool = False) -> T:
        """
        Get single resource by ID.
        
        Args:
            resource_id: Resource ID
            expand: Include expanded references
        
        Returns:
            Resource instance
        """
        path = f"{self._path}/{resource_id}"
        params = {'expand': 1} if expand else {}
        
        response = self._make_request('GET', path, params=params)
        return self._parse_response(response)
    
    def create(self, data: Union[Dict[str, Any], Any]) -> T:
        """
        Create new resource.
        
        Args:
            data: Resource data (dict or Pydantic model)
        
        Returns:
            Created resource
        """
        serialized_data = self._serialize_data(data)
        response = self._make_request('POST', self._path, json=serialized_data)
        return self._parse_response(response)
    
    def update(self, resource_id: int, data: Union[Dict[str, Any], Any]) -> T:
        """
        Update resource.
        
        Args:
            resource_id: Resource ID
            data: Updated data (dict or Pydantic model)
        
        Returns:
            Updated resource
        """
        path = f"{self._path}/{resource_id}"
        serialized_data = self._serialize_data(data)
        response = self._make_request('PUT', path, json=serialized_data)
        return self._parse_response(response)
    
    def delete(self, resource_id: int) -> Dict[str, Any]:
        """
        Delete resource.
        
        Args:
            resource_id: Resource ID
        
        Returns:
            Response with status
        """
        path = f"{self._path}/{resource_id}"
        return self._make_request('DELETE', path)
    
    def activate(self, resource_id: int) -> T:
        """
        Activate resource.
        
        Args:
            resource_id: Resource ID
        
        Returns:
            Activated resource
        """
        path = f"{self._path}/{resource_id}/activate"
        response = self._make_request('PUT', path)
        return self._parse_response(response)
    
    def pause(self, resource_id: int) -> T:
        """
        Pause resource.
        
        Args:
            resource_id: Resource ID
        
        Returns:
            Paused resource
        """
        path = f"{self._path}/{resource_id}/pause"
        response = self._make_request('PUT', path)
        return self._parse_response(response)
    
    def copy(self, resource_id: int, options: Optional[Union[Dict[str, Any], Any]] = None) -> T:
        """
        Copy resource.
        
        Args:
            resource_id: Resource ID
            options: Copy options (dict or Pydantic model)
        
        Returns:
            Copied resource
        """
        path = f"{self._path}/{resource_id}/copy"
        serialized_options = self._serialize_data(options) if options else {}
        response = self._make_request('POST', path, json=serialized_options)
        return self._parse_response(response)
    
    def get_audit_log(self, resource_id: int) -> List[Dict[str, Any]]:
        """
        Get audit log for resource.
        
        Args:
            resource_id: Resource ID
        
        Returns:
            List of audit log entries
        """
        path = f"{self._path}/{resource_id}/audit_log"
        return self._make_request('GET', path)
    
    def get_accessors(self, resource_id: int) -> AccessorResponseList:
        """
        Get access control rules for resource.
        
        Args:
            resource_id: Resource ID
        
        Returns:
            List of access control rules
        """
        path = f"{self._path}/{resource_id}/accessors"
        response = self._make_request('GET', path)
        
        # Parse response into AccessorResponse objects
        if isinstance(response, list):
            return [AccessorResponse.model_validate(item) for item in response]
        return []
    
    def add_accessors(self, resource_id: int, accessors: AccessorRequestList) -> AccessorResponseList:
        """
        Add access control rules.
        
        Args:
            resource_id: Resource ID
            accessors: List of accessor rules
        
        Returns:
            Updated accessor list
        """
        path = f"{self._path}/{resource_id}/accessors"
        serialized_accessors = [self._serialize_data(accessor) for accessor in accessors]
        response = self._make_request('PUT', path, json={'accessors': serialized_accessors})
        
        # Parse response into AccessorResponse objects
        if isinstance(response, list):
            return [AccessorResponse.model_validate(item) for item in response]
        return []
    
    def replace_accessors(self, resource_id: int, accessors: AccessorRequestList) -> AccessorResponseList:
        """
        Replace all access control rules.
        
        Args:
            resource_id: Resource ID
            accessors: List of accessor rules
        
        Returns:
            New accessor list
        """
        path = f"{self._path}/{resource_id}/accessors"
        serialized_accessors = [self._serialize_data(accessor) for accessor in accessors]
        response = self._make_request('POST', path, json={'accessors': serialized_accessors})
        
        # Parse response into AccessorResponse objects
        if isinstance(response, list):
            return [AccessorResponse.model_validate(item) for item in response]
        return []
    
    def delete_accessors(self, resource_id: int, accessors: Optional[AccessorRequestList] = None) -> AccessorResponseList:
        """
        Delete access control rules.
        
        Args:
            resource_id: Resource ID
            accessors: Specific accessors to delete (None = delete all)
        
        Returns:
            Remaining accessor list
        """
        path = f"{self._path}/{resource_id}/accessors"
        data = None
        if accessors:
            serialized_accessors = [self._serialize_data(accessor) for accessor in accessors]
            data = {'accessors': serialized_accessors}
        response = self._make_request('DELETE', path, json=data)
        
        # Parse response into AccessorResponse objects
        if isinstance(response, list):
            return [AccessorResponse.model_validate(item) for item in response]
        return []