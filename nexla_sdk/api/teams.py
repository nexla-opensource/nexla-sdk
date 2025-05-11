"""
Teams API endpoints
"""
from typing import Dict, Any, List, Optional, Union

from .base import BaseAPI
from ..models.access import AccessRole
from ..models.teams import Team, TeamList, TeamMember, TeamMemberList


class TeamsAPI(BaseAPI):
    """API client for teams endpoints"""
    
    def list(self, page: int = 1, per_page: int = 100, access_role: Optional[Union[AccessRole, str]] = None) -> TeamList:
        """
        List teams
        
        Args:
            page: Page number for pagination
            per_page: Number of items per page
            access_role: Filter by access role (can be an AccessRole enum or string like "member")
            
        Returns:
            TeamList containing teams
        """
        params = {"page": page, "per_page": per_page}
        if access_role:
            # Handle both enum and string values
            if isinstance(access_role, AccessRole):
                params["access_role"] = access_role.value
            else:
                params["access_role"] = access_role
            
        response = self._get("/teams", params=params)
        
        # Create and populate a TeamList object
        team_list = TeamList(items=[], total=0, page=page, per_page=per_page)
        
        if isinstance(response, list):
            # Convert each team item
            team_list.items = [Team.model_validate(item) for item in response]
            team_list.total = len(team_list.items)
            
        return team_list
        
    def get(self, team_id: int) -> Team:
        """
        Get a team by ID
        
        Args:
            team_id: Team ID
            
        Returns:
            Team object
        """
        return self._get(f"/teams/{team_id}", model_class=Team)
        
    def create(self, name: str, description: Optional[str] = None, 
               members: Optional[List[Dict[str, Any]]] = None) -> Team:
        """
        Create a new team
        
        Args:
            name: Team name
            description: Optional team description
            members: Optional list of team members, where each member is a dict with
                     either 'id' (user ID) or 'email' keys, and an optional 'admin' boolean
            
        Returns:
            Created Team object
        """
        team_data = {"name": name}
        if description:
            team_data["description"] = description
        if members:
            team_data["members"] = members
            
        return self._post("/teams", json=team_data, model_class=Team)
        
    def update(self, team_id: int, name: Optional[str] = None, 
               description: Optional[str] = None, 
               members: Optional[List[Dict[str, Any]]] = None) -> Team:
        """
        Update a team
        
        Args:
            team_id: Team ID
            name: Optional new team name
            description: Optional new team description
            members: Optional new list of team members, where each member is a dict with
                    either 'id' (user ID) or 'email' keys, and an optional 'admin' boolean
            
        Returns:
            Updated Team object
        """
        team_data = {}
        if name:
            team_data["name"] = name
        if description:
            team_data["description"] = description
        if members:
            team_data["members"] = members
            
        return self._put(f"/teams/{team_id}", json=team_data, model_class=Team)
        
    def delete(self, team_id: int) -> Dict[str, Any]:
        """
        Delete a team
        
        Args:
            team_id: Team ID
            
        Returns:
            Empty dictionary on success
        """
        return self._delete(f"/teams/{team_id}")
        
    def get_members(self, team_id: int) -> TeamMemberList:
        """
        Get members of a team
        
        Args:
            team_id: Team ID
            
        Returns:
            TeamMemberList containing team members
        """
        response = self._get(f"/teams/{team_id}/members")
        
        # API returns a list of members, but our model expects an object with members property
        if isinstance(response, list):
            return TeamMemberList(members=[TeamMember.model_validate(member) for member in response])
        
        return self._get(f"/teams/{team_id}/members", model_class=TeamMemberList)
    
    def replace_members(self, team_id: int, members: List[Dict[str, Any]]) -> TeamMemberList:
        """
        Replace all members of a team
        
        Args:
            team_id: Team ID
            members: List of team members, where each member is a dict with
                    either 'id' (user ID) or 'email' keys, and an optional 'admin' boolean
            
        Returns:
            TeamMemberList containing updated team members
        """
        response = self._post(f"/teams/{team_id}/members", json={"members": members})
        
        # API returns a list of members, but our model expects an object with members property
        if isinstance(response, list):
            return TeamMemberList(members=[TeamMember.model_validate(member) for member in response])
            
        return self._post(f"/teams/{team_id}/members", json={"members": members}, model_class=TeamMemberList)
    
    def add_members(self, team_id: int, members: List[Dict[str, Any]]) -> TeamMemberList:
        """
        Add members to a team
        
        Args:
            team_id: Team ID
            members: List of team members to add, where each member is a dict with
                    either 'id' (user ID) or 'email' keys, and an optional 'admin' boolean
            
        Returns:
            TeamMemberList containing updated team members
        """
        response = self._put(f"/teams/{team_id}/members", json={"members": members})
        
        # API returns a list of members, but our model expects an object with members property
        if isinstance(response, list):
            return TeamMemberList(members=[TeamMember.model_validate(member) for member in response])
            
        return self._put(f"/teams/{team_id}/members", json={"members": members}, model_class=TeamMemberList)
    
    def remove_members(self, team_id: int, members: Optional[List[Dict[str, Any]]] = None) -> TeamMemberList:
        """
        Remove members from a team
        
        Args:
            team_id: Team ID
            members: Optional list of team members to remove. If not provided, all members will be removed.
                    Each member is a dict with either 'id' (user ID) or 'email' keys
            
        Returns:
            TeamMemberList containing remaining team members
        """
        data = {}
        if members:
            data["members"] = members
            
        response = self._delete(f"/teams/{team_id}/members", json=data if data else None)
        
        # API returns a list of members, but our model expects an object with members property
        if isinstance(response, list):
            return TeamMemberList(members=[TeamMember.model_validate(member) for member in response])
            
        return self._delete(f"/teams/{team_id}/members", json=data if data else None, model_class=TeamMemberList) 