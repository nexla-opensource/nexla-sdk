"""
Users API endpoints
"""
from typing import Dict, Any, List, Optional

from .base import BaseAPI
from ..models.users import User, UserList


class UsersAPI(BaseAPI):
    """API client for users endpoints"""
    
    def list(self, limit: int = 100, offset: int = 0) -> UserList:
        """
        List users
        
        Args:
            limit: Number of items to return
            offset: Pagination offset
            
        Returns:
            UserList containing users
        """
        return self._get("/users", params={"limit": limit, "offset": offset}, model_class=UserList)
        
    def get(self, user_id: str) -> User:
        """
        Get a user by ID
        
        Args:
            user_id: User ID
            
        Returns:
            User object
        """
        return self._get(f"/users/{user_id}", model_class=User)
        
    def get_current(self) -> User:
        """
        Get the current user
        
        Returns:
            Current User object
        """
        return self._get("/users/current", model_class=User)
        
    def create(self, user_data: Dict[str, Any]) -> User:
        """
        Create a new user
        
        Args:
            user_data: User information
            
        Returns:
            Created User object
        """
        return self._post("/users", json=user_data, model_class=User)
        
    def update(self, user_id: str, user_data: Dict[str, Any]) -> User:
        """
        Update a user
        
        Args:
            user_id: User ID
            user_data: User information to update
            
        Returns:
            Updated User object
        """
        return self._put(f"/users/{user_id}", json=user_data, model_class=User)
        
    def delete(self, user_id: str) -> Dict[str, Any]:
        """
        Delete a user
        
        Args:
            user_id: User ID
            
        Returns:
            Empty dictionary on success
        """
        return self._delete(f"/users/{user_id}")
        
    def get_preferences(self) -> Dict[str, Any]:
        """
        Get user preferences
        
        Returns:
            User preferences
        """
        return self._get("/users/preferences")
        
    def update_preferences(self, preferences_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update user preferences
        
        Args:
            preferences_data: Preferences data to update
            
        Returns:
            Updated user preferences
        """
        return self._put("/users/preferences", json=preferences_data) 