"""
Quarantine Settings API client for the Nexla SDK

Nexla detects errors during different stages of data flow such as ingestion, 
transformation, and output. Error records are quarantined and accessible to the user 
via APIs as well as files.
"""
from typing import Optional

from .base import BaseAPI
from ..models.quarantine_settings import (
    QuarantineSettings, 
    CreateQuarantineSettingsRequest, 
    UpdateQuarantineSettingsRequest
)


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
        url = f"/users/{user_id}/quarantine_settings"
        return self._get(url, response_model=QuarantineSettings)

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
        url = f"/users/{user_id}/quarantine_settings"
        return self._post(url, json=settings.dict(exclude_none=True), response_model=QuarantineSettings)

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
        url = f"/users/{user_id}/quarantine_settings"
        return self._put(url, json=settings.dict(exclude_none=True), response_model=QuarantineSettings)

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
        url = f"/users/{user_id}/quarantine_settings"
        self._delete(url) 