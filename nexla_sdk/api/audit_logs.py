"""
Audit Logs API endpoints
"""
from typing import List

from .base import BaseAPI
from ..models.audit_logs import AuditLogEntry


class AuditLogsAPI(BaseAPI):
    """API client for audit log endpoints"""

    def _get_resource_audit_log(self, resource_path_segment: str, resource_id: int) -> List[AuditLogEntry]:
        """
        Private helper method to get audit logs for any resource type
        
        Args:
            resource_path_segment: The API path segment for the resource type
            resource_id: The unique ID of the resource
            
        Returns:
            List of audit log entries
        """
        return self._get(
            f"/{resource_path_segment}/{resource_id}/audit_log",
            model_class=List[AuditLogEntry]
        )

    def get_data_source_audit_log(self, source_id: int) -> List[AuditLogEntry]:
        """
        Get Audit Log for a Data Source
        
        Retrieves the history of changes made to the properties of a data source.
        
        Args:
            source_id: The unique ID of the data source
            
        Returns:
            List of audit log entries
        """
        return self._get_resource_audit_log("data_sources", source_id)
        
    def get_data_sink_audit_log(self, sink_id: int) -> List[AuditLogEntry]:
        """
        Get Audit Log for a Data Sink
        
        Retrieves the history of changes made to the properties of a data sink.
        
        Args:
            sink_id: The unique ID of the data sink
            
        Returns:
            List of audit log entries
        """
        return self._get_resource_audit_log("data_sinks", sink_id)
        
    def get_nexset_audit_log(self, set_id: int) -> List[AuditLogEntry]:
        """
        Get Audit Log for a Nexset
        
        Retrieves the history of changes made to the properties of a Nexset.
        
        Args:
            set_id: The unique ID of the Nexset (data set)
            
        Returns:
            List of audit log entries
        """
        return self._get_resource_audit_log("data_sets", set_id)
        
    def get_data_credential_audit_log(self, credential_id: int) -> List[AuditLogEntry]:
        """
        Get Audit Log for a Data Credential
        
        Retrieves the history of changes made to the properties of a data credential.
        
        Args:
            credential_id: The unique ID of the data credential
            
        Returns:
            List of audit log entries
        """
        return self._get_resource_audit_log("data_credentials", credential_id)
        
    def get_data_map_audit_log(self, data_map_id: int) -> List[AuditLogEntry]:
        """
        Get Audit Log for a Data Map
        
        Retrieves the history of changes made to the properties of a data map.
        
        Args:
            data_map_id: The unique ID of the data map
            
        Returns:
            List of audit log entries
        """
        return self._get_resource_audit_log("data_maps", data_map_id)
        
    def get_data_schema_audit_log(self, schema_id: int) -> List[AuditLogEntry]:
        """
        Get Audit Log for a Data Schema
        
        Retrieves the history of changes made to the properties of a data schema.
        
        Args:
            schema_id: The unique ID of the data schema
            
        Returns:
            List of audit log entries
        """
        return self._get_resource_audit_log("data_schemas", schema_id)
        
    def get_code_container_audit_log(self, code_container_id: int) -> List[AuditLogEntry]:
        """
        Get Audit Log for a Code Container
        
        Retrieves the history of changes made to the properties of a code container.
        This endpoint can also be used to fetch the history of changes made to any transform object.
        
        Args:
            code_container_id: The unique ID of the code container
            
        Returns:
            List of audit log entries
        """
        return self._get_resource_audit_log("code_containers", code_container_id)
        
    def get_project_audit_log(self, project_id: int) -> List[AuditLogEntry]:
        """
        Get Audit Log for a Project
        
        Retrieves the history of changes made to the properties of a project.
        
        Args:
            project_id: The unique ID of the project
            
        Returns:
            List of audit log entries
        """
        return self._get_resource_audit_log("projects", project_id)
        
    def get_doc_container_audit_log(self, doc_container_id: int) -> List[AuditLogEntry]:
        """
        Get Audit Log for a Document
        
        Retrieves the history of changes made to the properties of a document.
        
        Args:
            doc_container_id: The unique ID of the document
            
        Returns:
            List of audit log entries
        """
        return self._get_resource_audit_log("doc_containers", doc_container_id)
        
    def get_user_audit_log(self, user_id: int) -> List[AuditLogEntry]:
        """
        Get Audit Log for a User
        
        Retrieves the history of changes made to the properties of a user.
        
        Args:
            user_id: The unique ID of the user
            
        Returns:
            List of audit log entries
        """
        return self._get_resource_audit_log("users", user_id)
        
    def get_org_audit_log(self, org_id: int) -> List[AuditLogEntry]:
        """
        Get Audit Log for an Organization
        
        Retrieves the history of changes made to the properties of an organization.
        
        Args:
            org_id: The unique ID of the organization
            
        Returns:
            List of audit log entries
        """
        return self._get_resource_audit_log("orgs", org_id)
        
    def get_team_audit_log(self, team_id: int) -> List[AuditLogEntry]:
        """
        Get Audit Log for a Team
        
        Retrieves the history of changes made to the properties of a team.
        
        Args:
            team_id: The unique ID of the team
            
        Returns:
            List of audit log entries
        """
        return self._get_resource_audit_log("teams", team_id) 