"""
Quarantine Settings API client for the Nexla SDK

Nexla detects errors during different stages of data flow such as ingestion, 
transformation, and output. Error records are quarantined and accessible to the user 
via APIs as well as files.
"""
from typing import Optional, List, Dict, Any
from enum import Enum

from .base import BaseAPI
from ..models.quarantine_settings import (
    QuarantineSettings, 
    CreateQuarantineSettingsRequest, 
    UpdateQuarantineSettingsRequest,
    QuarantineResourceType
)


class ResourceTypeEnum(str, Enum):
    """Resource types for quarantine settings endpoints"""
    USERS = "users"
    ORGS = "orgs"
    DATA_SOURCES = "data_sources"
    DATA_SETS = "data_sets"
    DATA_SINKS = "data_sinks"


class QuarantineSettingsAPI(BaseAPI):
    """API client for quarantine settings"""

    def get_user_quarantine_settings(self, user_id: int) -> QuarantineSettings:
        """
        Get Quarantine Data Export Settings for a User

        Retrieve Quarantine Data Export Settings for all resources owned by a user.
        Nexla detects errors during different stages of data flow such as ingestion, 
        transformation, and output. Error records are quarantined and accessible to the user 
        via APIs as well as files. With Quarantine Data Export Settings, you can configure 
        Nexla to write files containing information about erroneous records across all 
        resources owned by a user.

        Args:
            user_id: The unique ID of the user whose quarantine settings you wish to retrieve

        Returns:
            QuarantineSettings: The user's quarantine settings

        Raises:
            NexlaAPIError: If the request fails
            NexlaNotFoundError: If no Quarantine Data Export Settings have been configured for the user
        """
        return self.get_quarantine_settings(ResourceTypeEnum.USERS, user_id)

    def create_quarantine_settings(
        self, 
        user_id: int, 
        settings: CreateQuarantineSettingsRequest
    ) -> QuarantineSettings:
        """
        Set Quarantine Data Export Settings for A User

        Sets Quarantine Data Export Settings for all resources owned by a user
        so that all erroneous records can be automatically exported by the
        platform to a file system regularly.

        Args:
            user_id: The unique ID of the user
            settings: The quarantine settings to create

        Returns:
            QuarantineSettings: The created quarantine settings

        Raises:
            NexlaAPIError: If the request fails
        """
        return self.create_resource_quarantine_settings(ResourceTypeEnum.USERS, user_id, settings)

    def update_quarantine_settings(
        self, 
        user_id: int, 
        settings: UpdateQuarantineSettingsRequest
    ) -> QuarantineSettings:
        """
        Update Quarantine Data Export Settings for A User

        Updates Quarantine Data Export Settings for all resources owned by a user
        so that all erroneous records can be automatically exported by the
        platform to a file system regularly.

        Args:
            user_id: The unique ID of the user
            settings: The updated quarantine settings

        Returns:
            QuarantineSettings: The updated quarantine settings

        Raises:
            NexlaAPIError: If the request fails
            NexlaNotFoundError: If no Quarantine Data Export Settings have been configured for the user
        """
        return self.update_resource_quarantine_settings(ResourceTypeEnum.USERS, user_id, settings)

    def delete_quarantine_settings(self, user_id: int) -> None:
        """
        Delete Quarantine Data Export Settings for A User

        Deletes Updates Quarantine Data Export Settings for all resources owned
        by a user. Deleting this setting will ensure the platform stops
        exporting all erroneous records for resources owned by the user to a
        file storage.

        Args:
            user_id: The unique ID of the user

        Raises:
            NexlaAPIError: If the request fails
            NexlaNotFoundError: If no Quarantine Data Export Settings have been configured for the user
        """
        self.delete_resource_quarantine_settings(ResourceTypeEnum.USERS, user_id)
    
    # Generic resource methods
    
    def get_quarantine_settings(
        self, 
        resource_type: ResourceTypeEnum, 
        resource_id: int
    ) -> QuarantineSettings:
        """
        Get Quarantine Data Export Settings for a specific resource

        Args:
            resource_type: The type of resource (users, orgs, data_sources, data_sets, data_sinks)
            resource_id: The unique ID of the resource

        Returns:
            QuarantineSettings: The resource's quarantine settings

        Raises:
            NexlaAPIError: If the request fails
            NexlaNotFoundError: If no Quarantine Data Export Settings have been configured for the resource
        """
        url = f"/{resource_type.value}/{resource_id}/quarantine_settings"
        return self._get(url, model_class=QuarantineSettings)

    def create_resource_quarantine_settings(
        self, 
        resource_type: ResourceTypeEnum, 
        resource_id: int, 
        settings: CreateQuarantineSettingsRequest
    ) -> QuarantineSettings:
        """
        Set Quarantine Data Export Settings for a specific resource

        Args:
            resource_type: The type of resource (users, orgs, data_sources, data_sets, data_sinks)
            resource_id: The unique ID of the resource
            settings: The quarantine settings to create

        Returns:
            QuarantineSettings: The created quarantine settings

        Raises:
            NexlaAPIError: If the request fails
        """
        url = f"/{resource_type.value}/{resource_id}/quarantine_settings"
        return self._post(url, json=settings.dict(exclude_none=True), model_class=QuarantineSettings)

    def update_resource_quarantine_settings(
        self, 
        resource_type: ResourceTypeEnum, 
        resource_id: int, 
        settings: UpdateQuarantineSettingsRequest
    ) -> QuarantineSettings:
        """
        Update Quarantine Data Export Settings for a specific resource

        Args:
            resource_type: The type of resource (users, orgs, data_sources, data_sets, data_sinks)
            resource_id: The unique ID of the resource
            settings: The updated quarantine settings

        Returns:
            QuarantineSettings: The updated quarantine settings

        Raises:
            NexlaAPIError: If the request fails
            NexlaNotFoundError: If no Quarantine Data Export Settings have been configured for the resource
        """
        url = f"/{resource_type.value}/{resource_id}/quarantine_settings"
        return self._put(url, json=settings.dict(exclude_none=True), model_class=QuarantineSettings)

    def delete_resource_quarantine_settings(
        self, 
        resource_type: ResourceTypeEnum, 
        resource_id: int
    ) -> None:
        """
        Delete Quarantine Data Export Settings for a specific resource

        Args:
            resource_type: The type of resource (users, orgs, data_sources, data_sets, data_sinks)
            resource_id: The unique ID of the resource

        Raises:
            NexlaAPIError: If the request fails
            NexlaNotFoundError: If no Quarantine Data Export Settings have been configured for the resource
        """
        url = f"/{resource_type.value}/{resource_id}/quarantine_settings"
        self._delete(url)
    
    def list_quarantine_settings(
        self,
        resource_type: Optional[QuarantineResourceType] = None,
        resource_id: Optional[int] = None
    ) -> List[QuarantineSettings]:
        """
        List all Quarantine Data Export Settings

        This is useful for reviewing all export locations of your account when 
        you have configured custom error data export locations for different resources.

        Args:
            resource_type: Optional filter by resource type (USER, ORG, SOURCE, DATASET, SINK)
            resource_id: Optional filter by resource ID

        Returns:
            List of QuarantineSettings objects

        Raises:
            NexlaAPIError: If the request fails
        """
        params = {}
        if resource_type:
            params["resource_type"] = resource_type.value.lower()
        if resource_id:
            params["resource_id"] = resource_id
            
        return self._get("/quarantine_settings", params=params, model_class=List[QuarantineSettings]) 