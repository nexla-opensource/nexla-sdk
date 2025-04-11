"""
Audit Logs API endpoints
"""
from typing import List

from .base import BaseAPI
from ..models.audit_logs import AuditLogEntry


class AuditLogsAPI(BaseAPI):
    """API client for audit log endpoints"""

    def get_data_source_audit_log(self, source_id: int) -> List[AuditLogEntry]:
        """
        Get Audit Log for a Data Source
        
        Retrieves the history of changes made to the properties of a data source.
        
        Args:
            source_id: The unique ID of the data source
            
        Returns:
            List of audit log entries
        """
        return self._get(
            f"/data_sources/{source_id}/audit_log",
            headers={"Accept": "application/vnd.nexla.api.v1+json"},
            model_class=List[AuditLogEntry]
        )
        
    def get_data_sink_audit_log(self, sink_id: int) -> List[AuditLogEntry]:
        """
        Get Audit Log for a Data Sink
        
        Retrieves the history of changes made to the properties of a data sink.
        
        Args:
            sink_id: The unique ID of the data sink
            
        Returns:
            List of audit log entries
        """
        return self._get(
            f"/data_sinks/{sink_id}/audit_log",
            headers={"Accept": "application/vnd.nexla.api.v1+json"},
            model_class=List[AuditLogEntry]
        )
        
    def get_nexset_audit_log(self, set_id: int) -> List[AuditLogEntry]:
        """
        Get Audit Log for a Nexset
        
        Retrieves the history of changes made to the properties of a Nexset.
        
        Args:
            set_id: The unique ID of the Nexset (data set)
            
        Returns:
            List of audit log entries
        """
        return self._get(
            f"/data_sets/{set_id}/audit_log",
            headers={"Accept": "application/vnd.nexla.api.v1+json"},
            model_class=List[AuditLogEntry]
        )
        
    def get_data_credential_audit_log(self, credential_id: int) -> List[AuditLogEntry]:
        """
        Get Audit Log for a Data Credential
        
        Retrieves the history of changes made to the properties of a data credential.
        
        Args:
            credential_id: The unique ID of the data credential
            
        Returns:
            List of audit log entries
        """
        return self._get(
            f"/data_credentials/{credential_id}/audit_log",
            headers={"Accept": "application/vnd.nexla.api.v1+json"},
            model_class=List[AuditLogEntry]
        )
        
    def get_data_map_audit_log(self, data_map_id: int) -> List[AuditLogEntry]:
        """
        Get Audit Log for a Data Map
        
        Retrieves the history of changes made to the properties of a data map.
        
        Args:
            data_map_id: The unique ID of the data map
            
        Returns:
            List of audit log entries
        """
        return self._get(
            f"/data_maps/{data_map_id}/audit_log",
            headers={"Accept": "application/vnd.nexla.api.v1+json"},
            model_class=List[AuditLogEntry]
        )
        
    def get_data_schema_audit_log(self, schema_id: int) -> List[AuditLogEntry]:
        """
        Get Audit Log for a Data Schema
        
        Retrieves the history of changes made to the properties of a data schema.
        
        Args:
            schema_id: The unique ID of the data schema
            
        Returns:
            List of audit log entries
        """
        return self._get(
            f"/data_schemas/{schema_id}/audit_log",
            headers={"Accept": "application/vnd.nexla.api.v1+json"},
            model_class=List[AuditLogEntry]
        )
        
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
        return self._get(
            f"/code_containers/{code_container_id}/audit_log",
            headers={"Accept": "application/vnd.nexla.api.v1+json"},
            model_class=List[AuditLogEntry]
        )
        
    def get_project_audit_log(self, project_id: int) -> List[AuditLogEntry]:
        """
        Get Audit Log for a Project
        
        Retrieves the history of changes made to the properties of a project.
        
        Args:
            project_id: The unique ID of the project
            
        Returns:
            List of audit log entries
        """
        return self._get(
            f"/projects/{project_id}/audit_log",
            headers={"Accept": "application/vnd.nexla.api.v1+json"},
            model_class=List[AuditLogEntry]
        )
        
    def get_doc_container_audit_log(self, doc_container_id: int) -> List[AuditLogEntry]:
        """
        Get Audit Log for a Document
        
        Retrieves the history of changes made to the properties of a document.
        
        Args:
            doc_container_id: The unique ID of the document
            
        Returns:
            List of audit log entries
        """
        return self._get(
            f"/doc_containers/{doc_container_id}/audit_log",
            headers={"Accept": "application/vnd.nexla.api.v1+json"},
            model_class=List[AuditLogEntry]
        )
        
    def get_user_audit_log(self, user_id: int) -> List[AuditLogEntry]:
        """
        Get Audit Log for a User
        
        Retrieves the history of changes made to the properties of a user.
        
        Args:
            user_id: The unique ID of the user
            
        Returns:
            List of audit log entries
        """
        return self._get(
            f"/users/{user_id}/audit_log",
            headers={"Accept": "application/vnd.nexla.api.v1+json"},
            model_class=List[AuditLogEntry]
        )
        
    def get_org_audit_log(self, org_id: int) -> List[AuditLogEntry]:
        """
        Get Audit Log for an Organization
        
        Retrieves the history of changes made to the properties of an organization.
        
        Args:
            org_id: The unique ID of the organization
            
        Returns:
            List of audit log entries
        """
        return self._get(
            f"/orgs/{org_id}/audit_log",
            headers={"Accept": "application/vnd.nexla.api.v1+json"},
            model_class=List[AuditLogEntry]
        )
        
    def get_team_audit_log(self, team_id: int) -> List[AuditLogEntry]:
        """
        Get Audit Log for a Team
        
        Retrieves the history of changes made to the properties of a team.
        
        Args:
            team_id: The unique ID of the team
            
        Returns:
            List of audit log entries
        """
        return self._get(
            f"/teams/{team_id}/audit_log",
            headers={"Accept": "application/vnd.nexla.api.v1+json"},
            model_class=List[AuditLogEntry]
        ) 