"""
Organizations API endpoints
"""
from typing import Dict, Any, List, Optional, Union
from datetime import datetime

from .base import BaseAPI
from ..models.organizations import (
    Organization, OrganizationList, OrganizationMember, OrganizationMemberList,
    UpdateOrganizationRequest, UpdateOrganizationMembersRequest, DeleteOrganizationMembersRequest,
    DeleteResponse
)
from ..models.metrics import AccountMetricsResponse


class OrganizationsAPI(BaseAPI):
    """API client for organizations endpoints"""
    
    def get_all(self) -> OrganizationList:
        """
        Get all organizations accessible to the authenticated user.
        
        Returns:
            List of Organization objects
        """
        response = self._get("/orgs")
        return OrganizationList([Organization.parse_obj(org) for org in response])
        
    def get(self, org_id: int) -> Organization:
        """
        Get an organization by ID
        
        Args:
            org_id: Organization ID
            
        Returns:
            Organization object
        """
        response = self._get(f"/orgs/{org_id}")
        return Organization.parse_obj(response)
        
    def update(self, org_id: int, update_data: UpdateOrganizationRequest) -> Organization:
        """
        Update an organization
        
        Args:
            org_id: Organization ID
            update_data: Organization data to update
            
        Returns:
            Updated Organization object
        """
        response = self._put(f"/orgs/{org_id}", json=update_data.dict(exclude_none=True))
        return Organization.parse_obj(response)
        
    def get_members(self, org_id: int) -> OrganizationMemberList:
        """
        Get all members in an organization
        
        Args:
            org_id: Organization ID
            
        Returns:
            List of organization members
        """
        response = self._get(f"/orgs/{org_id}/members")
        return OrganizationMemberList([OrganizationMember.parse_obj(member) for member in response])
        
    def update_members(self, org_id: int, update_data: UpdateOrganizationMembersRequest) -> OrganizationMemberList:
        """
        Update organization members
        
        Args:
            org_id: Organization ID
            update_data: Members data to update
            
        Returns:
            Updated list of organization members
        """
        response = self._put(f"/orgs/{org_id}/members", 
                           json=update_data.dict(exclude_none=True))
        return OrganizationMemberList([OrganizationMember.parse_obj(member) for member in response])
    
    def delete_members(self, org_id: int, delete_data: DeleteOrganizationMembersRequest) -> DeleteResponse:
        """
        Remove members from an organization
        
        Args:
            org_id: Organization ID
            delete_data: Members to remove
            
        Returns:
            Deletion response
        """
        response = self._delete(f"/orgs/{org_id}/members", 
                              json=delete_data.dict(exclude_none=True))
        return DeleteResponse.parse_obj(response)
    
    def get_account_metrics(
        self, 
        org_id: int, 
        from_date: Union[str, datetime], 
        to_date: Optional[Union[str, datetime]] = None
    ) -> AccountMetricsResponse:
        """
        Get Total Account Metrics for An Organization
        
        Retrieves total account utilization metrics for an organization. The result consists
        of aggregated information about records processed within the specified date range
        by all resources owned by users in the organization.
        
        Args:
            org_id: The unique ID of the organization
            from_date: Start date for metrics aggregation period
            to_date: End date for metrics aggregation period (defaults to current date)
            
        Returns:
            Account metrics response
        """
        params = {"from": from_date}
        if to_date:
            params["to"] = to_date
            
        response = self._get(
            f"/orgs/{org_id}/flows/account_metrics",
            params=params
        )
        return AccountMetricsResponse.parse_obj(response) 