"""
Organizations API endpoints
"""
from typing import Dict, Any, List, Optional

from .base import BaseAPI
from ..models.organizations import Organization, OrganizationList


class OrganizationsAPI(BaseAPI):
    """API client for organizations endpoints"""
    
    def list(self, limit: int = 100, offset: int = 0) -> OrganizationList:
        """
        List organizations
        
        Args:
            limit: Number of items to return
            offset: Pagination offset
            
        Returns:
            OrganizationList containing organizations
        """
        return self._get("/organizations", params={"limit": limit, "offset": offset}, model_class=OrganizationList)
        
    def get(self, organization_id: str) -> Organization:
        """
        Get an organization by ID
        
        Args:
            organization_id: Organization ID
            
        Returns:
            Organization object
        """
        return self._get(f"/organizations/{organization_id}", model_class=Organization)
        
    def get_current(self) -> Organization:
        """
        Get the current organization
        
        Returns:
            Current Organization object
        """
        return self._get("/organizations/current", model_class=Organization)
        
    def create(self, organization_data: Dict[str, Any]) -> Organization:
        """
        Create a new organization
        
        Args:
            organization_data: Organization configuration
            
        Returns:
            Created Organization object
        """
        return self._post("/organizations", json=organization_data, model_class=Organization)
        
    def update(self, organization_id: str, organization_data: Dict[str, Any]) -> Organization:
        """
        Update an organization
        
        Args:
            organization_id: Organization ID
            organization_data: Organization configuration to update
            
        Returns:
            Updated Organization object
        """
        return self._put(f"/organizations/{organization_id}", json=organization_data, model_class=Organization)
        
    def delete(self, organization_id: str) -> Dict[str, Any]:
        """
        Delete an organization
        
        Args:
            organization_id: Organization ID
            
        Returns:
            Empty dictionary on success
        """
        return self._delete(f"/organizations/{organization_id}")
        
    def get_settings(self) -> Dict[str, Any]:
        """
        Get organization settings
        
        Returns:
            Organization settings
        """
        return self._get("/organizations/settings")
        
    def update_settings(self, settings_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update organization settings
        
        Args:
            settings_data: Settings data to update
            
        Returns:
            Updated organization settings
        """
        return self._put("/organizations/settings", json=settings_data) 