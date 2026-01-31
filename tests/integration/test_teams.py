"""Integration tests for TeamsResource."""

import os

import pytest

from nexla_sdk import NexlaClient
from nexla_sdk.exceptions import NotFoundError, ServerError
from nexla_sdk.models.teams.requests import TeamCreate, TeamUpdate


@pytest.mark.integration
class TestTeamsIntegration:
    """Integration tests for TeamsResource."""

    @pytest.fixture
    def client(self):
        """Create a test client with real credentials."""
        service_key = os.getenv("NEXLA_SERVICE_KEY")
        if not service_key:
            pytest.skip("NEXLA_SERVICE_KEY not set")
        return NexlaClient(service_key=service_key)

    def test_list_teams_integration(self, client):
        """Test listing teams against real API."""
        teams = client.teams.list()

        # Should return a list (may be empty for new accounts)
        assert isinstance(teams, list)

        # If there are teams, verify structure
        for team in teams:
            assert hasattr(team, "id")
            assert hasattr(team, "name")
            assert hasattr(team, "description")
            assert hasattr(team, "owner")
            assert hasattr(team, "org")
            assert hasattr(team, "members")
            assert hasattr(team, "access_roles")

    def test_list_teams_with_access_role_member(self, client):
        """Test listing teams with access_role=member parameter."""
        member_teams = client.teams.list(access_role="member")

        assert isinstance(member_teams, list)

        # All returned teams should have member=True
        for team in member_teams:
            assert hasattr(team, "member")
            assert team.member

    def test_get_nonexistent_team(self, client):
        """Test getting a team that doesn't exist."""
        with pytest.raises(NotFoundError):
            client.teams.get(999999)

    def test_pagination_functionality(self, client):
        """Test pagination with real API."""
        # Test first page
        page1 = client.teams.list(page=1, per_page=10)
        assert isinstance(page1, list)

        # Test second page (might be empty)
        page2 = client.teams.list(page=2, per_page=10)
        assert isinstance(page2, list)

    @pytest.mark.create_team
    def test_team_lifecycle_integration(self, client):
        """Test complete team lifecycle: create, update, manage members, delete."""
        # Note: This test requires the ability to create/delete teams
        # Use @pytest.mark.create_team to run only when explicitly requested

        try:
            # Create a test team
            create_request = TeamCreate(
                name="Test Integration Team",
                description="A team created by integration tests",
            )

            created_team = client.teams.create(create_request)
            team_id = created_team.id

            assert created_team.name == "Test Integration Team"
            assert created_team.description == "A team created by integration tests"

            # Get the created team
            retrieved_team = client.teams.get(team_id)
            assert retrieved_team.id == team_id
            assert retrieved_team.name == "Test Integration Team"

            # Update the team
            update_request = TeamUpdate(
                name="Updated Integration Team", description="Updated description"
            )

            updated_team = client.teams.update(team_id, update_request)
            assert updated_team.name == "Updated Integration Team"
            assert updated_team.description == "Updated description"

            # Get team members (should be empty initially)
            members = client.teams.get_members(team_id)
            assert isinstance(members, list)

            # Clean up - delete the team
            client.teams.delete(team_id)

            # Verify deletion
            with pytest.raises(NotFoundError):
                client.teams.get(team_id)

        except ServerError as e:
            if e.status_code == 403:
                pytest.skip("User does not have permission to create teams")
            else:
                raise

    def test_get_team_members_real_team(self, client):
        """Test getting members of a real team if any exist."""
        teams = client.teams.list()

        if teams:
            # Test getting members of the first team
            team_id = teams[0].id
            members = client.teams.get_members(team_id)

            assert isinstance(members, list)

            # If there are members, verify their structure
            for member in members:
                assert hasattr(member, "id")
                assert hasattr(member, "email")
                assert hasattr(member, "admin")
                assert isinstance(member.admin, bool)

    def test_error_handling_real_api(self, client):
        """Test error handling with real API responses."""
        # Test various error scenarios

        # Invalid team ID format (if the API validates this)
        try:
            client.teams.get(-1)
        except (NotFoundError, ServerError):
            # Expected - either not found or validation error
            pass

    def test_team_validation_with_real_api(self, client):
        """Test that team responses match expected model structure."""
        teams = client.teams.list()

        for team in teams:
            # Verify all required fields are present
            assert team.id is not None
            assert team.name is not None
            assert hasattr(team, "description")
            assert team.owner is not None
            assert team.org is not None
            assert hasattr(team, "member")
            assert hasattr(team, "access_roles")
            assert isinstance(team.access_roles, list)

            # Verify owner structure
            assert hasattr(team.owner, "id")
            assert hasattr(team.owner, "full_name")
            assert hasattr(team.owner, "email")

            # Verify org structure
            assert hasattr(team.org, "id")
            assert hasattr(team.org, "name")

            # Verify members structure
            assert hasattr(team, "members")
            assert isinstance(team.members, list)

            # Verify each member structure
            for member in team.members:
                assert hasattr(member, "id")
                assert hasattr(member, "email")
                assert hasattr(member, "admin")
                assert isinstance(member.admin, bool)

    def test_team_access_roles_validation(self, client):
        """Test that team access roles are properly validated."""
        teams = client.teams.list()

        for team in teams:
            # Access roles should be a list of strings
            assert isinstance(team.access_roles, list)

            # Common access roles from the API docs
            # valid_roles = ["owner", "admin", "collaborator", "operator", "member"]  # Not used

            for role in team.access_roles:
                assert isinstance(role, str)
                # Note: Not all roles may be in our predefined list
                # as the API might support additional roles

    def test_expand_parameter_functionality(self, client):
        """Test expand parameter functionality."""
        teams = client.teams.list()

        if teams:
            team_id = teams[0].id

            # Get team without expand
            team_normal = client.teams.get(team_id)

            # Get team with expand
            team_expanded = client.teams.get(team_id, expand=True)

            # Both should have the same basic structure
            assert team_normal.id == team_expanded.id
            assert team_normal.name == team_expanded.name

    def test_list_vs_get_consistency(self, client):
        """Test that list and get operations return consistent data."""
        teams = client.teams.list()

        if teams:
            # Get the first team from the list
            list_team = teams[0]
            team_id = list_team.id

            # Get the same team individually
            get_team = client.teams.get(team_id)

            # Verify key fields match
            assert list_team.id == get_team.id
            assert list_team.name == get_team.name
            assert list_team.owner.id == get_team.owner.id
            assert list_team.org.id == get_team.org.id
