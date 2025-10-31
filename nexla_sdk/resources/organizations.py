from typing import List, Dict, Any
from nexla_sdk.resources.base_resource import BaseResource
from nexla_sdk.models.common import LogEntry
from nexla_sdk.models.organizations.responses import Organization, OrgMember, AccountSummary, CustodianUser
from nexla_sdk.models.organizations.requests import (
    OrganizationCreate,
    OrganizationUpdate,
    OrgMemberList,
    OrgMemberDelete,
    OrgMemberActivateDeactivateRequest
)
from nexla_sdk.models.organizations.custodians import OrgCustodiansPayload


class OrganizationsResource(BaseResource):
    """Resource for managing organizations."""

    def __init__(self, client):
        super().__init__(client)
        self._path = "/orgs"
        self._model_class = Organization

    def list(self, **kwargs) -> List[Organization]:
        """
        List organizations with optional filters.
        
        Args:
            page: Page number (via kwargs)
            per_page: Items per page (via kwargs)
            access_role: Filter by access role (via kwargs)
            **kwargs: Additional query parameters
        
        Returns:
            List of organizations
        
        Examples:
            client.organizations.list(page=1, per_page=25)
        """
        return super().list(**kwargs)

    def get(self, org_id: int, expand: bool = False) -> Organization:
        """
        Get single organization by ID.
        
        Args:
            org_id: Organization ID
            expand: Include expanded references
        
        Returns:
            Organization instance
        """
        return super().get(org_id, expand)

    def create(self, data: OrganizationCreate) -> Organization:
        """
        Create a new organization. Note: This is an admin-only operation.
        
        Args:
            data: Organization creation data
            
        Returns:
            Created organization
        """
        return super().create(data)

    def update(self, org_id: int, data: OrganizationUpdate) -> Organization:
        """
        Update organization.
        
        Args:
            org_id: Organization ID
            data: Updated organization data
        
        Returns:
            Updated organization
        """
        return super().update(org_id, data)

    def delete(self, org_id: int) -> Dict[str, Any]:
        """
        Delete organization.
        
        Args:
            org_id: Organization ID
        
        Returns:
            Response with status
        """
        return super().delete(org_id)

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

    def deactivate_members(self, org_id: int, members: OrgMemberActivateDeactivateRequest) -> List[OrgMember]:
        """
        Deactivate members in an organization.
        
        Args:
            org_id: Organization ID
            members: Members to deactivate
            
        Returns:
            Updated list of members
        """
        path = f"{self._path}/{org_id}/members/deactivate"
        response = self._make_request('PUT', path, json=members.to_dict())
        return [OrgMember(**member) for member in response]

    def activate_members(self, org_id: int, members: OrgMemberActivateDeactivateRequest) -> List[OrgMember]:
        """
        Activate members in an organization.
        
        Args:
            org_id: Organization ID
            members: Members to activate
            
        Returns:
            Updated list of members
        """
        path = f"{self._path}/{org_id}/members/activate"
        response = self._make_request('PUT', path, json=members.to_dict())
        return [OrgMember(**member) for member in response]

    def get_account_summary(self, org_id: int) -> AccountSummary:
        """
        Get account summary statistics for an organization.
        
        Args:
            org_id: Organization ID
        
        Returns:
            Account summary
        """
        path = f"{self._path}/{org_id}/account_summary"
        response = self._make_request('GET', path)
        return AccountSummary.model_validate(response)

    def get_current_account_summary(self) -> AccountSummary:
        """
        Get account summary for the current organization based on auth token.
        
        Returns:
            Account summary
        """
        path = f"{self._path}/account_summary"
        response = self._make_request('GET', path)
        return AccountSummary.model_validate(response)

    def get_org_flow_account_metrics(self, org_id: int, from_date: str, to_date: str = None) -> Dict[str, Any]:
        """Get total account metrics for an organization (flows)."""
        path = f"{self._path}/{org_id}/flows/account_metrics"
        params = {'from': from_date}
        if to_date:
            params['to'] = to_date
        return self._make_request('GET', path, params=params)

    def get_audit_log(self, org_id: int, **params) -> List[LogEntry]:
        """
        Get audit log for an organization.
        
        Args:
            org_id: Organization ID
            **params: Additional query parameters (e.g., page, per_page)
            
        Returns:
            List of audit log entries
        """
        path = f"{self._path}/{org_id}/audit_log"
        response = self._make_request('GET', path, params=params)
        return [LogEntry.model_validate(item) for item in response]

    def get_resource_audit_log(self, org_id: int, resource_type: str, **params) -> List[LogEntry]:
        """
        Get audit log for a specific resource type within an organization.
        
        Args:
            org_id: Organization ID
            resource_type: The type of resource (e.g., 'data_source', 'data_sink')
            **params: Additional query parameters
        
        Returns:
            List of audit log entries
        """
        path = f"{self._path}/{org_id}/{resource_type}/audit_log"
        response = self._make_request('GET', path, params=params)
        return [LogEntry.model_validate(item) for item in response]
        
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

    # Org custodians
    def get_custodians(self, org_id: int) -> List[CustodianUser]:
        path = f"{self._path}/{org_id}/custodians"
        response = self._make_request('GET', path)
        if isinstance(response, list):
            return [CustodianUser.model_validate(item) for item in response]
        return []

    def update_custodians(self, org_id: int, payload: OrgCustodiansPayload) -> List[CustodianUser]:
        path = f"{self._path}/{org_id}/custodians"
        data = self._serialize_data(payload)
        response = self._make_request('PUT', path, json=data)
        if isinstance(response, list):
            return [CustodianUser.model_validate(item) for item in response]
        return []

    def add_custodians(self, org_id: int, payload: OrgCustodiansPayload) -> List[CustodianUser]:
        path = f"{self._path}/{org_id}/custodians"
        data = self._serialize_data(payload)
        response = self._make_request('POST', path, json=data)
        if isinstance(response, list):
            return [CustodianUser.model_validate(item) for item in response]
        return []

    def remove_custodians(self, org_id: int, payload: OrgCustodiansPayload) -> Dict[str, Any]:
        path = f"{self._path}/{org_id}/custodians"
        data = self._serialize_data(payload)
        return self._make_request('DELETE', path, json=data)
