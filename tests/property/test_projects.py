"""Property-based tests for projects resource."""

import os
from unittest.mock import MagicMock

import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from nexla_sdk.models.projects.requests import (
    ProjectCreate,
    ProjectFlowIdentifier,
    ProjectFlowList,
    ProjectUpdate,
)
from nexla_sdk.models.projects.responses import Project, ProjectDataFlow
from tests.utils.fixtures import create_test_client
from tests.utils.mock_builders import MockDataFactory

# Suppress function-scoped fixture warnings for CI
SETTINGS = settings(
    suppress_health_check=[HealthCheck.function_scoped_fixture],
    max_examples=3 if os.getenv("CI") else 10,
    deadline=None,
)


class TestProjectsProperties:
    """Property-based tests for ProjectsResource."""

    @pytest.fixture
    def mock_client(self):
        """Create a test client with mocked HTTP."""
        return create_test_client()

    @given(
        name=st.text(
            min_size=1,
            max_size=100,
            alphabet=st.characters(min_codepoint=33, max_codepoint=126),
        ),
        description=st.text(
            min_size=0,
            max_size=500,
            alphabet=st.characters(min_codepoint=33, max_codepoint=126),
        ),
        flows_count=st.integers(min_value=0, max_value=50),
    )
    @SETTINGS
    def test_create_project_serialization(
        self, mock_client, name, description, flows_count
    ):
        """Test project creation with various input combinations."""
        # Arrange
        factory = MockDataFactory()
        mock_project = factory.create_mock_project(
            name=name, description=description, flows_count=flows_count
        )
        mock_client.http_client.request = MagicMock(return_value=mock_project)

        project_data = ProjectCreate(
            name=name,
            description=description,
            data_flows=[
                ProjectFlowIdentifier(data_source_id=i)
                for i in range(min(flows_count, 5))  # Limit for test performance
            ],
        )

        # Act
        project = mock_client.projects.create(project_data)

        # Assert
        assert isinstance(project, Project)
        assert project.name == name
        assert project.description == description
        if flows_count is not None:
            assert project.flows_count == flows_count

    @given(
        project_data=st.fixed_dictionaries(
            {
                "id": st.integers(min_value=1, max_value=10000),
                "name": st.text(
                    min_size=1,
                    max_size=100,
                    alphabet=st.characters(min_codepoint=33, max_codepoint=126),
                ),
                "description": st.text(
                    min_size=0,
                    max_size=500,
                    alphabet=st.characters(min_codepoint=33, max_codepoint=126),
                ),
                "flows_count": st.integers(min_value=0, max_value=100),
                "client_identifier": st.one_of(
                    st.none(),
                    st.text(
                        min_size=0,
                        max_size=50,
                        alphabet=st.characters(min_codepoint=33, max_codepoint=126),
                    ),
                ),
                "client_url": st.one_of(
                    st.none(),
                    st.text(
                        min_size=0,
                        max_size=200,
                        alphabet=st.characters(min_codepoint=33, max_codepoint=126),
                    ),
                ),
            }
        )
    )
    @SETTINGS
    def test_project_response_parsing(self, mock_client, project_data):
        """Test project response parsing with various data combinations."""
        # Arrange
        factory = MockDataFactory()
        mock_project = factory.create_mock_project(**project_data)
        mock_client.http_client.request = MagicMock(return_value=mock_project)

        # Act
        project = mock_client.projects.get(project_data["id"])

        # Assert
        assert isinstance(project, Project)
        assert project.id == project_data["id"]
        assert project.name == project_data["name"]
        assert project.description == project_data["description"]
        if project_data["flows_count"] is not None:
            assert project.flows_count == project_data["flows_count"]
        if project_data["client_identifier"] is not None:
            assert project.client_identifier == project_data["client_identifier"]
        if project_data["client_url"] is not None:
            assert project.client_url == project_data["client_url"]

    @given(
        projects=st.lists(
            st.fixed_dictionaries(
                {
                    "id": st.integers(min_value=1, max_value=10000),
                    "name": st.text(
                        min_size=1,
                        max_size=100,
                        alphabet=st.characters(min_codepoint=33, max_codepoint=126),
                    ),
                    "description": st.text(
                        min_size=0,
                        max_size=500,
                        alphabet=st.characters(min_codepoint=33, max_codepoint=126),
                    ),
                    "flows_count": st.integers(min_value=0, max_value=50),
                }
            ),
            min_size=0,
            max_size=5,
        )
    )
    @SETTINGS
    def test_list_projects_response_parsing(self, mock_client, projects):
        """Test project list response parsing with various data combinations."""
        # Arrange
        factory = MockDataFactory()
        mock_projects = [factory.create_mock_project(**proj) for proj in projects]
        mock_client.http_client.request = MagicMock(return_value=mock_projects)

        # Act
        result = mock_client.projects.list()

        # Assert
        assert isinstance(result, list)
        assert len(result) == len(projects)

        for i, project in enumerate(result):
            assert isinstance(project, Project)
            assert project.id == mock_projects[i]["id"]
            assert project.name == mock_projects[i]["name"]
            assert project.description == mock_projects[i]["description"]

    @given(
        data_flows=st.lists(
            st.fixed_dictionaries(
                {
                    "data_source_id": st.one_of(
                        st.none(), st.integers(min_value=1, max_value=10000)
                    ),
                    "data_set_id": st.one_of(
                        st.none(), st.integers(min_value=1, max_value=10000)
                    ),
                    "data_sink_id": st.one_of(
                        st.none(), st.integers(min_value=1, max_value=10000)
                    ),
                }
            ),
            min_size=1,
            max_size=10,
        )
    )
    @SETTINGS
    def test_project_data_flows_with_various_configurations(
        self, mock_client, data_flows
    ):
        """Test project data flow operations with various configurations."""
        # Arrange
        project_id = 123
        factory = MockDataFactory()
        mock_flows = [
            factory.create_mock_project_data_flow(**flow) for flow in data_flows
        ]
        mock_client.http_client.request = MagicMock(return_value=mock_flows)

        # Create flow identifiers - ensure at least one ID is provided per flow
        flow_identifiers = []
        for flow in data_flows:
            if flow["data_source_id"]:
                flow_identifiers.append(
                    ProjectFlowIdentifier(data_source_id=flow["data_source_id"])
                )
            elif flow["data_set_id"]:
                flow_identifiers.append(
                    ProjectFlowIdentifier(data_set_id=flow["data_set_id"])
                )
            else:
                # Fallback to source if no valid ID
                flow_identifiers.append(ProjectFlowIdentifier(data_source_id=1))

        flows = ProjectFlowList(data_flows=flow_identifiers)

        # Act
        result = mock_client.projects.add_data_flows(project_id, flows)

        # Assert
        assert isinstance(result, list)
        assert len(result) == len(data_flows)
        for flow in result:
            assert isinstance(flow, ProjectDataFlow)

    @given(
        name=st.one_of(
            st.none(),
            st.text(
                min_size=1,
                max_size=100,
                alphabet=st.characters(min_codepoint=33, max_codepoint=126),
            ),
        ),
        description=st.one_of(
            st.none(),
            st.text(
                min_size=0,
                max_size=500,
                alphabet=st.characters(min_codepoint=33, max_codepoint=126),
            ),
        ),
    )
    @SETTINGS
    def test_project_update_serialization(self, mock_client, name, description):
        """Test project update with various field combinations."""
        # Arrange
        project_id = 123
        factory = MockDataFactory()

        # Create update data with only provided fields
        update_data = {}
        if name is not None:
            update_data["name"] = name
        if description is not None:
            update_data["description"] = description

        mock_project = factory.create_mock_project(**update_data)
        mock_client.http_client.request = MagicMock(return_value=mock_project)

        update_request = ProjectUpdate(**update_data)

        # Act
        project = mock_client.projects.update(project_id, update_request)

        # Assert
        assert isinstance(project, Project)
        if name is not None:
            assert project.name == name
        if description is not None:
            assert project.description == description

    @given(
        tags=st.lists(
            st.text(
                min_size=1,
                max_size=50,
                alphabet=st.characters(min_codepoint=33, max_codepoint=126),
            ),
            min_size=0,
            max_size=10,
        ),
        access_roles=st.lists(
            st.sampled_from(["owner", "admin", "collaborator", "operator"]),
            min_size=1,
            max_size=4,
            unique=True,
        ),
    )
    @SETTINGS
    def test_project_metadata_parsing(self, mock_client, tags, access_roles):
        """Test project metadata parsing with various tags and roles."""
        # Arrange
        factory = MockDataFactory()
        mock_project = factory.create_mock_project(tags=tags, access_roles=access_roles)
        mock_client.http_client.request = MagicMock(return_value=mock_project)

        # Act
        project = mock_client.projects.get(123)

        # Assert
        assert isinstance(project, Project)
        assert project.tags == mock_project["tags"]
        assert project.access_roles == mock_project["access_roles"]

    @given(
        search_filters=st.lists(
            st.fixed_dictionaries(
                {
                    "field": st.sampled_from(["name", "description", "status"]),
                    "operator": st.sampled_from(["contains", "equals", "starts_with"]),
                    "value": st.text(
                        min_size=1,
                        max_size=50,
                        alphabet=st.characters(min_codepoint=33, max_codepoint=126),
                    ),
                }
            ),
            min_size=1,
            max_size=5,
        )
    )
    @SETTINGS
    def test_flows_search_with_various_filters(self, mock_client, search_filters):
        """Test flows search with various filter combinations."""
        # Arrange
        project_id = 123
        mock_response = {
            "flows": [
                {
                    "id": 1,
                    "origin_node_id": 1,
                    "parent_node_id": None,
                    "data_source_id": None,
                    "data_set_id": None,
                    "data_sink_id": None,
                    "status": None,
                    "project_id": None,
                    "flow_type": None,
                    "ingestion_mode": None,
                    "name": "test flow",
                    "description": None,
                    "children": None,
                }
            ],
            "data_sources": [],
            "data_sets": [],
            "data_sinks": [],
        }
        mock_client.http_client.request = MagicMock(return_value=mock_response)

        # Act
        result = mock_client.projects.search_flows(project_id, search_filters)

        # Assert
        assert result is not None

        # Verify the call was made
        mock_client.http_client.request.assert_called_once()
        call_args = mock_client.http_client.request.call_args
        assert call_args[0][0] == "POST"
        assert f"/projects/{project_id}/flows/search" in call_args[0][1]

    @given(
        project_name=st.text(
            min_size=1,
            max_size=100,
            alphabet=st.characters(min_codepoint=33, max_codepoint=126),
        )
    )
    @SETTINGS
    def test_project_name_edge_cases(self, mock_client, project_name):
        """Test project creation with various name edge cases."""
        # Arrange
        factory = MockDataFactory()
        mock_project = factory.create_mock_project(name=project_name)
        mock_client.http_client.request = MagicMock(return_value=mock_project)

        project_data = ProjectCreate(name=project_name, description="Test description")

        # Act
        project = mock_client.projects.create(project_data)

        # Assert
        assert isinstance(project, Project)
        assert project.name == project_name
