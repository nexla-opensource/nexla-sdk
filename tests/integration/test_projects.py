"""Integration tests for projects resource."""

import pytest

from nexla_sdk.exceptions import NotFoundError, ValidationError
from nexla_sdk.models.flows.responses import FlowResponse
from nexla_sdk.models.projects.requests import ProjectCreate, ProjectUpdate
from nexla_sdk.models.projects.responses import Project


@pytest.mark.integration
class TestProjectsIntegration:
    """Integration tests for ProjectsResource."""

    def test_project_crud_operations(self, integration_client):
        """Test complete CRUD lifecycle for projects."""
        created_project = None

        try:
            # Test create
            project_data = ProjectCreate(
                name=f"Integration Test Project {pytest.current_timestamp}",
                description="Test project for integration testing",
            )

            created_project = integration_client.projects.create(project_data)
            assert isinstance(created_project, Project)
            assert created_project.name == project_data.name
            assert created_project.description == project_data.description
            assert created_project.id is not None

            project_id = created_project.id

            # Test get
            retrieved_project = integration_client.projects.get(project_id)
            assert isinstance(retrieved_project, Project)
            assert retrieved_project.id == project_id
            assert retrieved_project.name == project_data.name

            # Test update
            update_data = ProjectUpdate(
                name=f"Updated Test Project {pytest.current_timestamp}",
                description="Updated description",
            )

            updated_project = integration_client.projects.update(
                project_id, update_data
            )
            assert isinstance(updated_project, Project)
            assert updated_project.id == project_id
            assert updated_project.name == update_data.name
            assert updated_project.description == update_data.description

            # Test list (verify project appears in list)
            projects = integration_client.projects.list()
            assert isinstance(projects, list)
            project_ids = [p.id for p in projects]
            assert project_id in project_ids

        finally:
            # Cleanup: delete project if it was created
            if created_project:
                try:
                    integration_client.projects.delete(created_project.id)
                except Exception as e:
                    pytest.fail(
                        f"Cleanup failed for project {created_project.id}: {e}",
                        pytrace=False,
                    )

    def test_list_projects_with_expand(self, integration_client):
        """Test listing projects with expand parameter."""
        # Test without expand
        projects = integration_client.projects.list()
        assert isinstance(projects, list)

        # Test with expand
        expanded_projects = integration_client.projects.list(expand=True)
        assert isinstance(expanded_projects, list)

        # If projects exist, verify expanded structure
        if expanded_projects:
            project = expanded_projects[0]
            assert hasattr(project, "data_flows")
            assert hasattr(project, "flows")
            assert isinstance(project.data_flows, list)
            assert isinstance(project.flows, list)

    def test_project_with_pagination(self, integration_client):
        """Test project listing with pagination."""
        # Test first page
        page1_projects = integration_client.projects.list(page=1, per_page=5)
        assert isinstance(page1_projects, list)

        # Test access role filter
        owner_projects = integration_client.projects.list(access_role="owner")
        assert isinstance(owner_projects, list)

    def test_get_project_flows(self, integration_client):
        """Test getting flows for a project."""
        # First get a project
        projects = integration_client.projects.list()

        if not projects:
            pytest.skip("No projects available for testing flows")

        if projects:
            project_id = projects[0].id

            # Test get flows
            flows = integration_client.projects.get_flows(project_id)
            assert isinstance(flows, FlowResponse)
            assert hasattr(flows, "flows")
            # Test search flows (if project has flows)
            if hasattr(flows, "flows") and flows.flows:
                search_filters = [
                    {"field": "name", "operator": "contains", "value": "test"}
                ]
                search_result = integration_client.projects.search_flows(
                    project_id, search_filters
                )
                assert isinstance(search_result, FlowResponse)

    def test_project_not_found_error(self, integration_client):
        """Test error handling for non-existent project."""
        non_existent_id = 999999

        with pytest.raises(NotFoundError):
            integration_client.projects.get(non_existent_id)

        # Test creating project with invalid data (empty name)
        with pytest.raises((ValidationError, ValueError, TypeError)):
            invalid_data = ProjectCreate(name="", description="Test")
            integration_client.projects.create(invalid_data)
            invalid_data = ProjectCreate(name="", description="Test")

    @pytest.fixture(scope="class")
    def timestamp(self):
        """Provide timestamp for unique naming."""
        import time

        return int(time.time())
        import time

        pytest.current_timestamp = int(time.time())
