"""
Users API endpoints
"""
from typing import Dict, Any, List, Optional, Union
from datetime import datetime

from .base import BaseAPI
from ..models.users import (
    User, UserList, UserDetail, UserDetailExpanded, 
    CreateUserRequest, UpdateUserRequest, UserPreferences
)
from ..models.common import ResourceType
from ..models.metrics import (
    AccessRole, AccountMetricsResponse, DashboardResponse, DailyMetricsResponse
)


class UsersAPI(BaseAPI):
    """API client for users endpoints"""
    
    def list(self, page: int = 1, per_page: int = 100, expand: bool = False, access_role: Optional[str] = None) -> List[Union[User, UserDetailExpanded]]:
        """
        List users
        
        Args:
            page: Page number for pagination
            per_page: Number of items per page
            expand: Whether to expand user details
            access_role: Optional access role filter (e.g., "all" for admins to see all users)
            
        Returns:
            List of User objects or expanded user details
        """
        params = {"page": page, "per_page": per_page}
        if expand:
            params["expand"] = 1
        if access_role:
            params["access_role"] = access_role
            
        response = self._get("/users", params=params)
        
        # Handle response as a raw list and convert each item individually
        if isinstance(response, list):
            model_class = UserDetailExpanded if expand else User
            return [model_class.model_validate(item) for item in response]
        
        return []
        
    def get(self, user_id: Union[str, int], expand: bool = False) -> Union[User, UserDetailExpanded]:
        """
        Get a user by ID
        
        Args:
            user_id: User ID
            expand: Whether to expand user references
            
        Returns:
            User object (expanded if expand=True)
        """
        params = {}
        if expand:
            params["expand"] = 1
            
        return self._get(f"/users/{user_id}", params=params, model_class=UserDetailExpanded if expand else User)
        
    def get_current(self) -> User:
        """
        Get the current user
        
        Returns:
            Current User object
        """
        return self._get("/users/current", model_class=User)
        
    def create(self, user_data: Union[Dict[str, Any], CreateUserRequest]) -> User:
        """
        Create a new user
        
        This requires admin access to the provided organization.
        
        Args:
            user_data: User information as dict or CreateUserRequest
            
        Returns:
            Created User object
        """
        if isinstance(user_data, CreateUserRequest):
            user_data = user_data.model_dump(exclude_none=True)
            
        return self._post("/users", json=user_data, model_class=User)
        
    def update(self, user_id: Union[str, int], user_data: Union[Dict[str, Any], UpdateUserRequest]) -> User:
        """
        Update a user
        
        Args:
            user_id: User ID
            user_data: User information to update as dict or UpdateUserRequest
            
        Returns:
            Updated User object
        """
        if isinstance(user_data, UpdateUserRequest):
            user_data = user_data.model_dump(exclude_none=True)
            
        return self._put(f"/users/{user_id}", json=user_data, model_class=User)
        
    def delete(self, user_id: Union[str, int]) -> Dict[str, Any]:
        """
        Delete a user
        
        Args:
            user_id: User ID
            
        Returns:
            Empty dictionary on success
        """
        return self._delete(f"/users/{user_id}")
        
    def get_preferences(self) -> UserPreferences:
        """
        Get user preferences
        
        Returns:
            User preferences
        """
        return self._get("/users/preferences", model_class=UserPreferences)
        
    def update_preferences(self, preferences_data: Dict[str, Any]) -> UserPreferences:
        """
        Update user preferences
        
        Args:
            preferences_data: Preferences data to update
            
        Returns:
            Updated user preferences
        """
        return self._put("/users/preferences", json=preferences_data, model_class=UserPreferences)
        
    def get_account_metrics(
        self, 
        user_id: Union[str, int], 
        from_date: Union[str, datetime], 
        to_date: Optional[Union[str, datetime]] = None,
        org_id: Optional[int] = None
    ) -> AccountMetricsResponse:
        """
        Get total account metrics for a user
        
        Retrieves total account utilization metrics for a user in an organization. 
        The result consists of aggregated information about records processed within 
        the specified date range by all resources owned by the user.
        
        Args:
            user_id: User ID
            from_date: Start date for metrics aggregation
            to_date: End date for metrics aggregation (defaults to current date)
            org_id: Organization ID (defaults to user's default organization)
            
        Returns:
            Account metrics response
        """
        params = {"from": from_date}
        if to_date:
            params["to"] = to_date
        if org_id:
            params["org_id"] = org_id
            
        return self._get(
            f"/users/{user_id}/flows/account_metrics", 
            params=params, 
            model_class=AccountMetricsResponse
        )
        
    def get_flow_stats(
        self, 
        user_id: Union[str, int], 
        access_role: Optional[AccessRole] = None
    ) -> DashboardResponse:
        """
        Get 24-hour flow stats for a user
        
        Retrieves the metrics and processing status of each flow that processed data
        in the last 24 hours.
        
        Args:
            user_id: User ID
            access_role: Access role filter (defaults to owner)
            
        Returns:
            Dashboard response with flow stats
        """
        params = {}
        if access_role:
            params["access_role"] = access_role.value
            
        return self._get(
            f"/users/{user_id}/flows/dashboard", 
            params=params, 
            model_class=DashboardResponse
        )
        
    def get_daily_metrics(
        self, 
        user_id: Union[str, int], 
        resource_type: ResourceType,
        from_date: Union[str, datetime], 
        to_date: Optional[Union[str, datetime]] = None,
        org_id: Optional[int] = None
    ) -> DailyMetricsResponse:
        """
        Get daily data processing metrics for a user
        
        Retrieves daily data processing metrics of all sources or all destinations 
        owned by a user.
        
        Args:
            user_id: User ID
            resource_type: Type of resource (SOURCE or SINK)
            from_date: Start date for metrics reporting
            to_date: End date for metrics reporting (defaults to current date)
            org_id: Organization ID (defaults to user's default organization)
            
        Returns:
            Daily metrics response
        """
        params = {
            "resource_type": resource_type.value,
            "from": from_date,
            "aggregate": 1
        }
        
        if to_date:
            params["to"] = to_date
        if org_id:
            params["org_id"] = org_id
            
        return self._get(
            f"/users/{user_id}/metrics", 
            params=params, 
            model_class=DailyMetricsResponse
        ) 