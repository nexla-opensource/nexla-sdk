from typing import List, Optional, Dict, Any
from nexla_sdk.resources.base_resource import BaseResource
from nexla_sdk.models.organizations.responses import Organization, OrgMember
from nexla_sdk.models.organizations.requests import OrgMemberList, OrgMemberDelete


class OrganizationsResource(BaseResource):
    """Resource for managing organizations."""
    
    def __init__(self, client):
        super().__init__(client)
        self._path = "/orgs"
        self._model_class = Organization
    
    def get_members(self, org_id: int) -> List[OrgMember]:
        """
        Get all members in organization.
        
        Args:
            org_id: Organization ID
        
        Returns:
            List of organization members
        """
        path = f"{self._path}/{org_id}/members"
        response = self._make_request('GET', path)
        return [OrgMember(**member) for member in response]
    
    def update_members(self, org_id: int, members: OrgMemberList) -> List[OrgMember]:
        """
        Add or update members in organization.
        
        Args:
            org_id: Organization ID
            members: Members to add/update
        
        Returns:
            Updated member list
        """
        path = f"{self._path}/{org_id}/members"
        response = self._make_request('PUT', path, json=members.to_dict())
        return [OrgMember(**member) for member in response]
    
    def replace_members(self, org_id: int, members: OrgMemberList) -> List[OrgMember]:
        """
        Replace all members in organization.
        
        Args:
            org_id: Organization ID
            members: New member list
        
        Returns:
            New member list
        """
        path = f"{self._path}/{org_id}/members"
        response = self._make_request('POST', path, json=members.to_dict())
        return [OrgMember(**member) for member in response]
    
    def delete_members(self, org_id: int, members: OrgMemberDelete) -> Dict[str, Any]:
        """
        Remove members from organization.
        
        Args:
            org_id: Organization ID
            members: Members to remove
        
        Returns:
            Response status
        """
        path = f"{self._path}/{org_id}/members"
        return self._make_request('DELETE', path, json=members.to_dict())
    
    def get_account_metrics(self,
                            org_id: int,
                            from_date: str,
                            to_date: Optional[str] = None) -> Dict[str, Any]:
        """
        Get total account metrics for organization.
        
        Args:
            org_id: Organization ID
            from_date: Start date (YYYY-MM-DD)
            to_date: End date (optional)
        
        Returns:
            Account metrics
        """
        path = f"{self._path}/{org_id}/flows/account_metrics"
        params = {'from': from_date}
        if to_date:
            params['to'] = to_date
        
        return self._make_request('GET', path, params=params)
    
    def get_auth_settings(self, org_id: int) -> List[Dict[str, Any]]:
        """
        Get authentication settings for organization.
        
        Args:
            org_id: Organization ID
        
        Returns:
            List of auth settings
        """
        path = f"{self._path}/{org_id}/auth_settings"
        return self._make_request('GET', path)
    
    def update_auth_setting(self,
                            org_id: int,
                            auth_setting_id: int,
                            enabled: bool) -> Dict[str, Any]:
        """
        Enable/disable authentication configuration.
        
        Args:
            org_id: Organization ID
            auth_setting_id: Auth setting ID
            enabled: Whether to enable
        
        Returns:
            Updated auth setting
        """
        path = f"{self._path}/{org_id}/auth_settings/{auth_setting_id}"
        data = {'enabled': enabled}
        return self._make_request('PUT', path, json=data)
