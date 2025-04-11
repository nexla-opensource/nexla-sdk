"""
Access Control API client for the Nexla SDK

APIs for managing access permissions on various resources like data sources, data sets, 
data sinks, data maps, credentials, projects, flows, etc.
"""
from typing import List, Optional, Union

from .base import BaseAPI
from ..models.access import Accessor, AccessorsRequest


class AccessControlAPI(BaseAPI):
    """API client for access control operations"""

    def get_data_source_accessors(self, data_source_id: int) -> List[Accessor]:
        """
        Get Access Rules on Data Source

        Returns a list of the access-control rules set for this data source.

        Args:
            data_source_id: The unique ID of the data source

        Returns:
            List[Accessor]: The list of accessors for the data source

        Raises:
            NexlaAPIError: If the request fails
            NexlaNotFoundError: If the data source is not found
        """
        url = f"/data_sources/{data_source_id}/accessors"
        return self._get(url, response_model=List[Accessor])

    def replace_data_source_accessors(
        self, data_source_id: int, accessors: AccessorsRequest
    ) -> List[Accessor]:
        """
        Replace Access Rules on Data Source

        Replaces the list of accessors belonging to a data source. 
        Existing accessors will be removed from the data source.

        Args:
            data_source_id: The unique ID of the data source
            accessors: The new accessors to set for the data source

        Returns:
            List[Accessor]: The updated list of accessors for the data source

        Raises:
            NexlaAPIError: If the request fails
            NexlaNotFoundError: If the data source is not found
        """
        url = f"/data_sources/{data_source_id}/accessors"
        return self._post(url, json=accessors.dict(exclude_none=True), response_model=List[Accessor])

    def add_data_source_accessors(
        self, data_source_id: int, accessors: AccessorsRequest
    ) -> List[Accessor]:
        """
        Add Access Rules on Data Source

        Adds a list of accessors to a data source. The existing accessors list 
        is retained and merged with the new accessors list.

        Args:
            data_source_id: The unique ID of the data source
            accessors: The accessors to add to the data source

        Returns:
            List[Accessor]: The updated list of accessors for the data source

        Raises:
            NexlaAPIError: If the request fails
            NexlaNotFoundError: If the data source is not found
        """
        url = f"/data_sources/{data_source_id}/accessors"
        return self._put(url, json=accessors.dict(exclude_none=True), response_model=List[Accessor])

    def delete_data_source_accessors(
        self, data_source_id: int, accessors: Optional[AccessorsRequest] = None
    ) -> List[Accessor]:
        """
        Delete Access Rules on Data Source

        Removes access-control rules from a data source. If no accessors are provided, 
        all rules associated with the data source will be removed.

        Args:
            data_source_id: The unique ID of the data source
            accessors: Optional list of accessors to remove

        Returns:
            List[Accessor]: The remaining list of accessors for the data source

        Raises:
            NexlaAPIError: If the request fails
            NexlaNotFoundError: If the data source is not found
        """
        url = f"/data_sources/{data_source_id}/accessors"
        if accessors:
            return self._delete(url, json=accessors.dict(exclude_none=True), response_model=List[Accessor])
        return self._delete(url, response_model=List[Accessor])

    # Nexset (Data Set) access control methods

    def get_nexset_accessors(self, data_set_id: int) -> List[Accessor]:
        """
        Get Access Rules on Nexset

        Returns a list of the access-control rules set for this Nexset.

        Args:
            data_set_id: The unique ID of the Nexset

        Returns:
            List[Accessor]: The list of accessors for the Nexset

        Raises:
            NexlaAPIError: If the request fails
            NexlaNotFoundError: If the Nexset is not found
        """
        url = f"/data_sets/{data_set_id}/accessors"
        return self._get(url, response_model=List[Accessor])

    def replace_nexset_accessors(
        self, data_set_id: int, accessors: AccessorsRequest
    ) -> List[Accessor]:
        """
        Replace Access Rules on Nexset

        Replaces the list of access-control rules set for this Nexset. 
        Existing rules will be removed from the Nexset, and only these 
        new rules will be applied.

        Args:
            data_set_id: The unique ID of the Nexset
            accessors: The new accessors to set for the Nexset

        Returns:
            List[Accessor]: The updated list of accessors for the Nexset

        Raises:
            NexlaAPIError: If the request fails
            NexlaNotFoundError: If the Nexset is not found
        """
        url = f"/data_sets/{data_set_id}/accessors"
        return self._post(url, json=accessors.dict(exclude_none=True), response_model=List[Accessor])

    def add_nexset_accessors(
        self, data_set_id: int, accessors: AccessorsRequest
    ) -> List[Accessor]:
        """
        Add Access Rules on Nexset

        Adds new access-control rules to this Nexset.

        Args:
            data_set_id: The unique ID of the Nexset
            accessors: The accessors to add to the Nexset

        Returns:
            List[Accessor]: The updated list of accessors for the Nexset

        Raises:
            NexlaAPIError: If the request fails
            NexlaNotFoundError: If the Nexset is not found
        """
        url = f"/data_sets/{data_set_id}/accessors"
        return self._put(url, json=accessors.dict(exclude_none=True), response_model=List[Accessor])

    def delete_nexset_accessors(
        self, data_set_id: int, accessors: Optional[AccessorsRequest] = None
    ) -> List[Accessor]:
        """
        Delete Access Rules on Nexset

        Removes access-control rules from a Nexset. If no accessors are provided, 
        all rules associated with the Nexset will be removed.

        Args:
            data_set_id: The unique ID of the Nexset
            accessors: Optional list of accessors to remove

        Returns:
            List[Accessor]: The remaining list of accessors for the Nexset

        Raises:
            NexlaAPIError: If the request fails
            NexlaNotFoundError: If the Nexset is not found
        """
        url = f"/data_sets/{data_set_id}/accessors"
        if accessors:
            return self._delete(url, json=accessors.dict(exclude_none=True), response_model=List[Accessor])
        return self._delete(url, response_model=List[Accessor])

    # Data Sink access control methods

    def get_data_sink_accessors(self, data_sink_id: int) -> List[Accessor]:
        """
        Get Access Rules on Data Sink

        Returns a list of the access-control rules set for this data sink.

        Args:
            data_sink_id: The unique ID of the data sink

        Returns:
            List[Accessor]: The list of accessors for the data sink

        Raises:
            NexlaAPIError: If the request fails
            NexlaNotFoundError: If the data sink is not found
        """
        url = f"/data_sinks/{data_sink_id}/accessors"
        return self._get(url, response_model=List[Accessor])

    def replace_data_sink_accessors(
        self, data_sink_id: int, accessors: AccessorsRequest
    ) -> List[Accessor]:
        """
        Replace Access Rules on Data Sink

        Replaces the list of access-control rules set for this data sink. 
        Existing rules will be removed from the data sink, and only these 
        new rules will be applied.

        Args:
            data_sink_id: The unique ID of the data sink
            accessors: The new accessors to set for the data sink

        Returns:
            List[Accessor]: The updated list of accessors for the data sink

        Raises:
            NexlaAPIError: If the request fails
            NexlaNotFoundError: If the data sink is not found
        """
        url = f"/data_sinks/{data_sink_id}/accessors"
        return self._post(url, json=accessors.dict(exclude_none=True), response_model=List[Accessor])

    def add_data_sink_accessors(
        self, data_sink_id: int, accessors: AccessorsRequest
    ) -> List[Accessor]:
        """
        Add Access Rules on Data Sink

        Adds new access-control rules to this data sink.

        Args:
            data_sink_id: The unique ID of the data sink
            accessors: The accessors to add to the data sink

        Returns:
            List[Accessor]: The updated list of accessors for the data sink

        Raises:
            NexlaAPIError: If the request fails
            NexlaNotFoundError: If the data sink is not found
        """
        url = f"/data_sinks/{data_sink_id}/accessors"
        return self._put(url, json=accessors.dict(exclude_none=True), response_model=List[Accessor])

    def delete_data_sink_accessors(
        self, data_sink_id: int, accessors: Optional[AccessorsRequest] = None
    ) -> List[Accessor]:
        """
        Delete Access Rules on Data Sink

        Removes access-control rules from a data sink. If no accessors are provided, 
        all rules associated with the data sink will be removed.

        Args:
            data_sink_id: The unique ID of the data sink
            accessors: Optional list of accessors to remove

        Returns:
            List[Accessor]: The remaining list of accessors for the data sink

        Raises:
            NexlaAPIError: If the request fails
            NexlaNotFoundError: If the data sink is not found
        """
        url = f"/data_sinks/{data_sink_id}/accessors"
        if accessors:
            return self._delete(url, json=accessors.dict(exclude_none=True), response_model=List[Accessor])
        return self._delete(url, response_model=List[Accessor])

    # Data Map access control methods

    def get_data_map_accessors(self, data_map_id: int) -> List[Accessor]:
        """
        Get Access Rules on Data Map

        Returns a list of the access-control rules set for this data map.

        Args:
            data_map_id: The unique ID of the data map

        Returns:
            List[Accessor]: The list of accessors for the data map

        Raises:
            NexlaAPIError: If the request fails
            NexlaNotFoundError: If the data map is not found
        """
        url = f"/data_maps/{data_map_id}/accessors"
        return self._get(url, response_model=List[Accessor])

    def replace_data_map_accessors(
        self, data_map_id: int, accessors: AccessorsRequest
    ) -> List[Accessor]:
        """
        Replace Access Rules on Data Map

        Replaces the list of access-control rules set for this data map. 
        Existing rules will be removed from the data map, and only these 
        new rules will be applied.

        Args:
            data_map_id: The unique ID of the data map
            accessors: The new accessors to set for the data map

        Returns:
            List[Accessor]: The updated list of accessors for the data map

        Raises:
            NexlaAPIError: If the request fails
            NexlaNotFoundError: If the data map is not found
        """
        url = f"/data_maps/{data_map_id}/accessors"
        return self._post(url, json=accessors.dict(exclude_none=True), response_model=List[Accessor])

    def add_data_map_accessors(
        self, data_map_id: int, accessors: AccessorsRequest
    ) -> List[Accessor]:
        """
        Add Access Rules on Data Map

        Adds new access-control rules to this data map.

        Args:
            data_map_id: The unique ID of the data map
            accessors: The accessors to add to the data map

        Returns:
            List[Accessor]: The updated list of accessors for the data map

        Raises:
            NexlaAPIError: If the request fails
            NexlaNotFoundError: If the data map is not found
        """
        url = f"/data_maps/{data_map_id}/accessors"
        return self._put(url, json=accessors.dict(exclude_none=True), response_model=List[Accessor])

    def delete_data_map_accessors(
        self, data_map_id: int, accessors: Optional[AccessorsRequest] = None
    ) -> List[Accessor]:
        """
        Delete Access Rules on Data Map

        Removes access-control rules from a data map. If no accessors are provided, 
        all rules associated with the data map will be removed.

        Args:
            data_map_id: The unique ID of the data map
            accessors: Optional list of accessors to remove

        Returns:
            List[Accessor]: The remaining list of accessors for the data map

        Raises:
            NexlaAPIError: If the request fails
            NexlaNotFoundError: If the data map is not found
        """
        url = f"/data_maps/{data_map_id}/accessors"
        if accessors:
            return self._delete(url, json=accessors.dict(exclude_none=True), response_model=List[Accessor])
        return self._delete(url, response_model=List[Accessor])

    # Credential access control methods

    def get_credential_accessors(self, credential_id: int) -> List[Accessor]:
        """
        Get Access Rules on Credential

        Returns a list of the access-control rules set for this credential.

        Args:
            credential_id: The unique ID of the credential

        Returns:
            List[Accessor]: The list of accessors for the credential

        Raises:
            NexlaAPIError: If the request fails
            NexlaNotFoundError: If the credential is not found
        """
        url = f"/data_credentials/{credential_id}/accessors"
        return self._get(url, response_model=List[Accessor])

    def replace_credential_accessors(
        self, credential_id: int, accessors: AccessorsRequest
    ) -> List[Accessor]:
        """
        Replace Access Rules on Credential

        Replaces the list of access-control rules set for this credential. 
        Existing rules will be removed from the credential, and only these 
        new rules will be applied.

        Args:
            credential_id: The unique ID of the credential
            accessors: The new accessors to set for the credential

        Returns:
            List[Accessor]: The updated list of accessors for the credential

        Raises:
            NexlaAPIError: If the request fails
            NexlaNotFoundError: If the credential is not found
        """
        url = f"/data_credentials/{credential_id}/accessors"
        return self._post(url, json=accessors.dict(exclude_none=True), response_model=List[Accessor])

    def add_credential_accessors(
        self, credential_id: int, accessors: AccessorsRequest
    ) -> List[Accessor]:
        """
        Add Access Rules on Credential

        Adds new access-control rules to this credential.

        Args:
            credential_id: The unique ID of the credential
            accessors: The accessors to add to the credential

        Returns:
            List[Accessor]: The updated list of accessors for the credential

        Raises:
            NexlaAPIError: If the request fails
            NexlaNotFoundError: If the credential is not found
        """
        url = f"/data_credentials/{credential_id}/accessors"
        return self._put(url, json=accessors.dict(exclude_none=True), response_model=List[Accessor])

    def delete_credential_accessors(
        self, credential_id: int, accessors: Optional[AccessorsRequest] = None
    ) -> List[Accessor]:
        """
        Delete Access Rules on Credential

        Removes access-control rules from a credential. If no accessors are provided, 
        all rules associated with the credential will be removed.

        Args:
            credential_id: The unique ID of the credential
            accessors: Optional list of accessors to remove

        Returns:
            List[Accessor]: The remaining list of accessors for the credential

        Raises:
            NexlaAPIError: If the request fails
            NexlaNotFoundError: If the credential is not found
        """
        url = f"/data_credentials/{credential_id}/accessors"
        if accessors:
            return self._delete(url, json=accessors.dict(exclude_none=True), response_model=List[Accessor])
        return self._delete(url, response_model=List[Accessor])

    # Project access control methods

    def get_project_accessors(self, project_id: int) -> List[Accessor]:
        """
        Get Project Accessors

        Returns a list of the access-control rules set for this project.

        Args:
            project_id: The unique ID of the project

        Returns:
            List[Accessor]: The list of accessors for the project

        Raises:
            NexlaAPIError: If the request fails
            NexlaNotFoundError: If the project is not found
        """
        url = f"/projects/{project_id}/accessors"
        return self._get(url, response_model=List[Accessor])

    def replace_project_accessors(
        self, project_id: int, accessors: AccessorsRequest
    ) -> List[Accessor]:
        """
        Replace Access Rules on Project

        Replaces the list of access-control rules set for this project. 
        Existing rules will be removed from the project, and only these 
        new rules will be applied.

        Args:
            project_id: The unique ID of the project
            accessors: The new accessors to set for the project

        Returns:
            List[Accessor]: The updated list of accessors for the project

        Raises:
            NexlaAPIError: If the request fails
            NexlaNotFoundError: If the project is not found
        """
        url = f"/projects/{project_id}/accessors"
        return self._post(url, json=accessors.dict(exclude_none=True), response_model=List[Accessor])

    def add_project_accessors(
        self, project_id: int, accessors: AccessorsRequest
    ) -> List[Accessor]:
        """
        Add Project Accessors

        Adds new access-control rules to this project.

        Args:
            project_id: The unique ID of the project
            accessors: The accessors to add to the project

        Returns:
            List[Accessor]: The updated list of accessors for the project

        Raises:
            NexlaAPIError: If the request fails
            NexlaNotFoundError: If the project is not found
        """
        url = f"/projects/{project_id}/accessors"
        return self._put(url, json=accessors.dict(exclude_none=True), response_model=List[Accessor])

    def delete_project_accessors(
        self, project_id: int, accessors: Optional[AccessorsRequest] = None
    ) -> List[Accessor]:
        """
        Delete Project Accessors

        Removes access-control rules from a project. If no accessors are provided, 
        all rules associated with the project will be removed.

        Args:
            project_id: The unique ID of the project
            accessors: Optional list of accessors to remove

        Returns:
            List[Accessor]: The remaining list of accessors for the project

        Raises:
            NexlaAPIError: If the request fails
            NexlaNotFoundError: If the project is not found
        """
        url = f"/projects/{project_id}/accessors"
        if accessors:
            return self._delete(url, json=accessors.dict(exclude_none=True), response_model=List[Accessor])
        return self._delete(url, response_model=List[Accessor])

    # Flow access control methods

    def get_flow_accessors(self, flow_id: str) -> List[Accessor]:
        """
        Get Access Rules on Flow

        Returns a list of the access-control rules set for this flow.

        Args:
            flow_id: The unique ID of the flow

        Returns:
            List[Accessor]: The list of accessors for the flow

        Raises:
            NexlaAPIError: If the request fails
            NexlaNotFoundError: If the flow is not found
        """
        url = f"/flows/{flow_id}/accessors"
        return self._get(url, response_model=List[Accessor])

    def replace_flow_accessors(
        self, flow_id: str, accessors: AccessorsRequest
    ) -> List[Accessor]:
        """
        Replace Access Rules on Flow

        Replaces the list of access-control rules set for this flow. 
        Existing rules will be removed from the flow, and only these 
        new rules will be applied.

        Args:
            flow_id: The unique ID of the flow
            accessors: The new accessors to set for the flow

        Returns:
            List[Accessor]: The updated list of accessors for the flow

        Raises:
            NexlaAPIError: If the request fails
            NexlaNotFoundError: If the flow is not found
        """
        url = f"/flows/{flow_id}/accessors"
        return self._post(url, json=accessors.dict(exclude_none=True), response_model=List[Accessor])

    def add_flow_accessors(
        self, flow_id: str, accessors: AccessorsRequest
    ) -> List[Accessor]:
        """
        Add Access Rules on Flow

        Adds new access-control rules to this flow.

        Args:
            flow_id: The unique ID of the flow
            accessors: The accessors to add to the flow

        Returns:
            List[Accessor]: The updated list of accessors for the flow

        Raises:
            NexlaAPIError: If the request fails
            NexlaNotFoundError: If the flow is not found
        """
        url = f"/flows/{flow_id}/accessors"
        return self._put(url, json=accessors.dict(exclude_none=True), response_model=List[Accessor])

    def delete_flow_accessors(
        self, flow_id: str, accessors: Optional[AccessorsRequest] = None
    ) -> List[Accessor]:
        """
        Delete Access Rules on Flow

        Removes access-control rules from a flow. If no accessors are provided, 
        all rules associated with the flow will be removed.

        Args:
            flow_id: The unique ID of the flow
            accessors: Optional list of accessors to remove

        Returns:
            List[Accessor]: The remaining list of accessors for the flow

        Raises:
            NexlaAPIError: If the request fails
            NexlaNotFoundError: If the flow is not found
        """
        url = f"/flows/{flow_id}/accessors"
        if accessors:
            return self._delete(url, json=accessors.dict(exclude_none=True), response_model=List[Accessor])
        return self._delete(url, response_model=List[Accessor])

    # Team access control methods

    def get_team_accessors(self, team_id: int) -> List[Accessor]:
        """
        Get Team Accessors

        Returns a list of the access-control rules set for this team.

        Args:
            team_id: The unique ID of the team

        Returns:
            List[Accessor]: The list of accessors for the team

        Raises:
            NexlaAPIError: If the request fails
            NexlaNotFoundError: If the team is not found
        """
        url = f"/teams/{team_id}/accessors"
        return self._get(url, response_model=List[Accessor])

    def replace_team_accessors(
        self, team_id: int, accessors: AccessorsRequest
    ) -> List[Accessor]:
        """
        Replace Team Accessors List

        Replaces the list of access-control rules set for this team. 
        Existing rules will be removed from the team, and only these 
        new rules will be applied.

        Args:
            team_id: The unique ID of the team
            accessors: The new accessors to set for the team

        Returns:
            List[Accessor]: The updated list of accessors for the team

        Raises:
            NexlaAPIError: If the request fails
            NexlaNotFoundError: If the team is not found
        """
        url = f"/teams/{team_id}/accessors"
        return self._post(url, json=accessors.dict(exclude_none=True), response_model=List[Accessor])

    def add_team_accessors(
        self, team_id: int, accessors: AccessorsRequest
    ) -> List[Accessor]:
        """
        Add Team Accessors

        Adds new access-control rules to this team.

        Args:
            team_id: The unique ID of the team
            accessors: The accessors to add to the team

        Returns:
            List[Accessor]: The updated list of accessors for the team

        Raises:
            NexlaAPIError: If the request fails
            NexlaNotFoundError: If the team is not found
        """
        url = f"/teams/{team_id}/accessors"
        return self._put(url, json=accessors.dict(exclude_none=True), response_model=List[Accessor])

    def delete_team_accessors(
        self, team_id: int, accessors: Optional[AccessorsRequest] = None
    ) -> List[Accessor]:
        """
        Delete Team Accessors

        Removes access-control rules from a team. If no accessors are provided, 
        all rules associated with the team will be removed.

        Args:
            team_id: The unique ID of the team
            accessors: Optional list of accessors to remove

        Returns:
            List[Accessor]: The remaining list of accessors for the team

        Raises:
            NexlaAPIError: If the request fails
            NexlaNotFoundError: If the team is not found
        """
        url = f"/teams/{team_id}/accessors"
        if accessors:
            return self._delete(url, json=accessors.dict(exclude_none=True), response_model=List[Accessor])
        return self._delete(url, response_model=List[Accessor]) 