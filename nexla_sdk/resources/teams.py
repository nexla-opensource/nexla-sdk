from typing import List, Optional, Dict, Any
from nexla_sdk.resources.base_resource import BaseResource
from nexla_sdk.models.teams.responses import Team, TeamMember
from nexla_sdk.models.teams.requests import TeamMemberList


class TeamsResource(BaseResource):
    """Resource for managing teams."""
    
    def __init__(self, client):
        super().__init__(client)
        self._path = "/teams"
        self._model_class = Team
    
    def get_members(self, team_id: int) -> List[TeamMember]:
        """
        Get team members.
        
        Args:
            team_id: Team ID
        
        Returns:
            List of team members
        """
        path = f"{self._path}/{team_id}/members"
        response = self._make_request('GET', path)
        return [TeamMember(**member) for member in response]
    
    def add_members(self, team_id: int, members: TeamMemberList) -> List[TeamMember]:
        """
        Add members to team.
        
        Args:
            team_id: Team ID
            members: Members to add
        
        Returns:
            Updated member list
        """
        path = f"{self._path}/{team_id}/members"
        response = self._make_request('PUT', path, json=members.to_dict())
        return [TeamMember(**member) for member in response]
    
    def replace_members(self, team_id: int, members: TeamMemberList) -> List[TeamMember]:
        """
        Replace all team members.
        
        Args:
            team_id: Team ID
            members: New member list
        
        Returns:
            New member list
        """
        path = f"{self._path}/{team_id}/members"
        response = self._make_request('POST', path, json=members.to_dict())
        return [TeamMember(**member) for member in response]
    
    def remove_members(self,
                       team_id: int,
                       members: Optional[TeamMemberList] = None) -> List[TeamMember]:
        """
        Remove members from team.
        
        Args:
            team_id: Team ID
            members: Members to remove (None = remove all)
        
        Returns:
            Remaining members
        """
        path = f"{self._path}/{team_id}/members"
        data = members.to_dict() if members else None
        response = self._make_request('DELETE', path, json=data)
        return [TeamMember(**member) for member in response]
