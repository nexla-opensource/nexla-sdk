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

    def _manage_accessors(
        self,
        resource_name_plural: str,  # e.g., "data_sources", "data_sets"
        resource_id: Union[int, str],
        http_method: str,  # "GET", "POST", "PUT", "DELETE"
        accessors_payload: Optional[AccessorsRequest] = None
    ) -> List[Accessor]:
        """
        Helper method to manage accessors for any resource type.
        
        Args:
            resource_name_plural: Plural name of the resource type (e.g., "data_sources")
            resource_id: The ID of the resource
            http_method: HTTP method to use ("GET", "POST", "PUT", "DELETE")
            accessors_payload: Optional payload for accessors

        Returns:
            List[Accessor]: The list of accessors for the resource

        Raises:
            NexlaAPIError: If the request fails
            NexlaNotFoundError: If the resource is not found
            ValueError: If an unsupported HTTP method is provided
        """
        url = f"/{resource_name_plural}/{resource_id}/accessors"
        kwargs = {}
        if accessors_payload and http_method in ["POST", "PUT", "DELETE"]:
            kwargs['json'] = accessors_payload.dict(exclude_none=True)

        if http_method == "GET":
            return self._get(url, response_model=List[Accessor], **kwargs)
        elif http_method == "POST":
            return self._post(url, response_model=List[Accessor], **kwargs)
        elif http_method == "PUT":
            return self._put(url, response_model=List[Accessor], **kwargs)
        elif http_method == "DELETE":
            return self._delete(url, response_model=List[Accessor], **kwargs)
        else:
            raise ValueError(f"Unsupported HTTP method: {http_method}")

    # Data Source access control methods

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
        return self._manage_accessors("data_sources", data_source_id, "GET")

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
        return self._manage_accessors("data_sources", data_source_id, "POST", accessors_payload=accessors)

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
        return self._manage_accessors("data_sources", data_source_id, "PUT", accessors_payload=accessors)

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
        return self._manage_accessors("data_sources", data_source_id, "DELETE", accessors_payload=accessors)

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
        return self._manage_accessors("data_sets", data_set_id, "GET")

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
        return self._manage_accessors("data_sets", data_set_id, "POST", accessors_payload=accessors)

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
        return self._manage_accessors("data_sets", data_set_id, "PUT", accessors_payload=accessors)

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
        return self._manage_accessors("data_sets", data_set_id, "DELETE", accessors_payload=accessors)

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
        return self._manage_accessors("data_sinks", data_sink_id, "GET")

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
        return self._manage_accessors("data_sinks", data_sink_id, "POST", accessors_payload=accessors)

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
        return self._manage_accessors("data_sinks", data_sink_id, "PUT", accessors_payload=accessors)

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
        return self._manage_accessors("data_sinks", data_sink_id, "DELETE", accessors_payload=accessors)

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
        return self._manage_accessors("data_maps", data_map_id, "GET")

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
        return self._manage_accessors("data_maps", data_map_id, "POST", accessors_payload=accessors)

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
        return self._manage_accessors("data_maps", data_map_id, "PUT", accessors_payload=accessors)

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
        return self._manage_accessors("data_maps", data_map_id, "DELETE", accessors_payload=accessors)

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
        return self._manage_accessors("data_credentials", credential_id, "GET")

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
        return self._manage_accessors("data_credentials", credential_id, "POST", accessors_payload=accessors)

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
        return self._manage_accessors("data_credentials", credential_id, "PUT", accessors_payload=accessors)

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
        return self._manage_accessors("data_credentials", credential_id, "DELETE", accessors_payload=accessors)

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
        return self._manage_accessors("projects", project_id, "GET")

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
        return self._manage_accessors("projects", project_id, "POST", accessors_payload=accessors)

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
        return self._manage_accessors("projects", project_id, "PUT", accessors_payload=accessors)

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
        return self._manage_accessors("projects", project_id, "DELETE", accessors_payload=accessors)

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
        return self._manage_accessors("flows", flow_id, "GET")

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
        return self._manage_accessors("flows", flow_id, "POST", accessors_payload=accessors)

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
        return self._manage_accessors("flows", flow_id, "PUT", accessors_payload=accessors)

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
        return self._manage_accessors("flows", flow_id, "DELETE", accessors_payload=accessors)

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
        return self._manage_accessors("teams", team_id, "GET")

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
        return self._manage_accessors("teams", team_id, "POST", accessors_payload=accessors)

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
        return self._manage_accessors("teams", team_id, "PUT", accessors_payload=accessors)

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
        return self._manage_accessors("teams", team_id, "DELETE", accessors_payload=accessors) 