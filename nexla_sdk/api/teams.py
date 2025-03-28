"""
Teams API endpoints
"""
from typing import Dict, Any, List, Optional

from .base import BaseAPI
from ..models.teams import Team, TeamList


class TeamsAPI(BaseAPI):
    """API client for teams endpoints"""
    
    def list(self, limit: int = 100, offset: int = 0) -> TeamList:
        """
        List teams
        
        Args:
            limit: Number of items to return
            offset: Pagination offset
            
        Returns:
            TeamList containing teams
        """
        return self._get("/teams", params={"limit": limit, "offset": offset}, model_class=TeamList)
        
    def get(self, team_id: str) -> Team:
        """
        Get a team by ID
        
        Args:
            team_id: Team ID
            
        Returns:
            Team object
        """
        return self._get(f"/teams/{team_id}", model_class=Team)
        
    def create(self, team_data: Dict[str, Any]) -> Team:
        """
        Create a new team
        
        Args:
            team_data: Team configuration
            
        Returns:
            Created Team object
        """
        return self._post("/teams", json=team_data, model_class=Team)
        
    def update(self, team_id: str, team_data: Dict[str, Any]) -> Team:
        """
        Update a team
        
        Args:
            team_id: Team ID
            team_data: Team configuration to update
            
        Returns:
            Updated Team object
        """
        return self._put(f"/teams/{team_id}", json=team_data, model_class=Team)
        
    def delete(self, team_id: str) -> Dict[str, Any]:
        """
        Delete a team
        
        Args:
            team_id: Team ID
            
        Returns:
            Empty dictionary on success
        """
        return self._delete(f"/teams/{team_id}")
        
    def add_user(self, team_id: str, user_id: str) -> Team:
        """
        Add a user to a team
        
        Args:
            team_id: Team ID
            user_id: User ID to add
            
        Returns:
            Updated Team object
        """
        return self._post(f"/teams/{team_id}/users/{user_id}", model_class=Team)
        
    def remove_user(self, team_id: str, user_id: str) -> Team:
        """
        Remove a user from a team
        
        Args:
            team_id: Team ID
            user_id: User ID to remove
            
        Returns:
            Updated Team object
        """
        return self._delete(f"/teams/{team_id}/users/{user_id}", model_class=Team) 