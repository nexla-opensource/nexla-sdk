"""Unit tests for TeamsResource."""

import pytest
from nexla_sdk.exceptions import ServerError, NotFoundError, ValidationError
from nexla_sdk.models.teams.responses import Team, TeamMember
from nexla_sdk.models.teams.requests import TeamCreate, TeamUpdate, TeamMemberRequest, TeamMemberList
from nexla_sdk.http_client import HttpClientError
from tests.utils.mock_builders import MockResponseBuilder
from tests.utils.assertions import NexlaAssertions


class TestTeamsUnitTests:
    """Unit tests for TeamsResource."""

    def test_list_teams_success(self, mock_client):
        """Test successful listing of teams."""
        client = mock_client
        team_data = MockResponseBuilder.team()
        team_data["id"] = 123
        client.http_client.add_response("/teams", [team_data])
        
        teams = client.teams.list()
        
        assert len(teams) == 1
        assert isinstance(teams[0], Team)
        NexlaAssertions.assert_team_response(teams[0], team_data)
        client.http_client.assert_request_made("GET", "/teams")

    def test_list_teams_with_access_role_member(self, mock_client):
        """Test listing teams with access_role=member parameter."""
        client = mock_client
        team_data1 = MockResponseBuilder.team()
        team_data1.update({"id": 123, "member": True})
        team_data2 = MockResponseBuilder.team()
        team_data2.update({"id": 124, "member": True})
        team_data = [team_data1, team_data2]
        client.http_client.add_response("/teams", team_data)
        
        teams = client.teams.list(access_role="member")
        
        assert len(teams) == 2
        client.http_client.assert_request_made("GET", "/teams", params={"access_role": "member"})

    def test_list_teams_with_pagination(self, mock_client):
        """Test listing teams with pagination parameters."""
        client = mock_client
        team_data = MockResponseBuilder.team()
        team_data["id"] = 123
        client.http_client.add_response("/teams", [team_data])
        
        client.teams.list(page=2, per_page=50)
        
        client.http_client.assert_request_made("GET", "/teams", params={"page": 2, "per_page": 50})

    def test_get_team_success(self, mock_client):
        """Test successful getting of a team."""
        client = mock_client
        team_data = MockResponseBuilder.team()
        team_data["id"] = 123
        client.http_client.add_response("/teams/123", team_data)
        
        team = client.teams.get(123)
        
        assert isinstance(team, Team)
        NexlaAssertions.assert_team_response(team, team_data)
        client.http_client.assert_request_made("GET", "/teams/123")

    def test_get_team_with_expand(self, mock_client):
        """Test getting a team with expand parameter."""
        client = mock_client
        team_data = MockResponseBuilder.team()
        team_data["id"] = 123
        client.http_client.add_response("/teams/123", team_data)
        
        team = client.teams.get(123, expand=True)
        
        assert isinstance(team, Team)
        client.http_client.assert_request_made("GET", "/teams/123", params={"expand": 1})

    def test_get_team_not_found(self, mock_client):
        """Test getting a non-existent team."""
        client = mock_client
        client.http_client.add_error("/teams/999", 
            HttpClientError("Not found", status_code=404, response={"message": "Team not found"}))
        
        with pytest.raises(NotFoundError):
            client.teams.get(999)

    def test_create_team_success(self, mock_client):
        """Test successful creation of a team."""
        client = mock_client
        request_data = TeamCreate(
            name="Test Team",
            description="A test team",
            members=[
                TeamMemberRequest(email="test@example.com", admin=True)
            ]
        )
        response_data = MockResponseBuilder.team()
        response_data.update({
            "id": 123,
            "name": "Test Team",
            "description": "A test team",
            "members": [
                {
                    "id": 456,
                    "email": "test@example.com",
                    "admin": True
                }
            ]
        })
        client.http_client.add_response("/teams", response_data)
        
        team = client.teams.create(request_data)
        
        assert isinstance(team, Team)
        assert team.name == "Test Team"
        assert team.description == "A test team"
        assert len(team.members) == 1
        client.http_client.assert_request_made("POST", "/teams")

    def test_create_team_validation_error(self, mock_client):
        """Test team creation with validation error."""
        client = mock_client
        request_data = TeamCreate(
            name="",  # Invalid empty name
            description="A test team"
        )
        client.http_client.add_error("/teams",
            HttpClientError("Validation failed", status_code=400,
                          response={"message": "Team name cannot be empty"}))

        with pytest.raises(ValidationError):
            client.teams.create(request_data)

    def test_update_team_success(self, mock_client):
        """Test successful updating of a team."""
        client = mock_client
        request_data = TeamUpdate(
            name="Updated Team",
            members=[TeamMemberRequest(email="new@example.com", admin=False)]
        )
        response_data = MockResponseBuilder.team()
        response_data.update({"id": 123, "name": "Updated Team"})
        client.http_client.add_response("/teams/123", response_data)
        
        team = client.teams.update(123, request_data)
        
        assert isinstance(team, Team)
        assert team.name == "Updated Team"
        client.http_client.assert_request_made("PUT", "/teams/123")

    def test_delete_team_success(self, mock_client):
        """Test successful deletion of a team."""
        client = mock_client
        client.http_client.add_response("/teams/123", {"status": "deleted"})
        
        result = client.teams.delete(123)
        
        assert result["status"] == "deleted"
        client.http_client.assert_request_made("DELETE", "/teams/123")

    def test_get_members_success(self, mock_client):
        """Test successful getting of team members."""
        client = mock_client
        member1 = MockResponseBuilder.team_member()
        member1.update({"id": 456, "email": "user1@example.com", "admin": True})
        member2 = MockResponseBuilder.team_member()
        member2.update({"id": 457, "email": "user2@example.com", "admin": False})
        members_data = [member1, member2]
        client.http_client.add_response("/teams/123/members", members_data)
        
        members = client.teams.get_members(123)
        
        assert len(members) == 2
        assert all(isinstance(member, TeamMember) for member in members)
        assert members[0].email == "user1@example.com"
        assert members[0].admin
        assert members[1].email == "user2@example.com"
        assert not members[1].admin
        client.http_client.assert_request_made("GET", "/teams/123/members")

    def test_add_members_success(self, mock_client):
        """Test successful adding of team members."""
        client = mock_client
        request_data = TeamMemberList(
            members=[
                TeamMemberRequest(email="new1@example.com", admin=True),
                TeamMemberRequest(id=789, admin=False)
            ]
        )
        response_data = [
            MockResponseBuilder.team_member(user_id=456, email="existing@example.com", admin=True),
            MockResponseBuilder.team_member(user_id=789, email="new1@example.com", admin=True),
            MockResponseBuilder.team_member(user_id=790, email="new2@example.com", admin=False)
        ]
        client.http_client.add_response("/teams/123/members", response_data)
        
        members = client.teams.add_members(123, request_data)
        
        assert len(members) == 3
        assert all(isinstance(member, TeamMember) for member in members)
        client.http_client.assert_request_made("PUT", "/teams/123/members")

    def test_replace_members_success(self, mock_client):
        """Test successful replacing of team members."""
        client = mock_client
        request_data = TeamMemberList(
            members=[TeamMemberRequest(email="only@example.com", admin=True)]
        )
        response_data = [
            MockResponseBuilder.team_member(user_id=999, email="only@example.com", admin=True)
        ]
        client.http_client.add_response("/teams/123/members", response_data)
        
        members = client.teams.replace_members(123, request_data)
        
        assert len(members) == 1
        assert members[0].email == "only@example.com"
        client.http_client.assert_request_made("POST", "/teams/123/members")

    def test_remove_members_success(self, mock_client):
        """Test successful removal of team members."""
        client = mock_client
        request_data = TeamMemberList(
            members=[TeamMemberRequest(email="remove@example.com")]
        )
        response_data = [
            MockResponseBuilder.team_member(user_id=456, email="remaining@example.com", admin=False)
        ]
        client.http_client.add_response("/teams/123/members", response_data)
        
        members = client.teams.remove_members(123, request_data)
        
        assert len(members) == 1
        assert members[0].email == "remaining@example.com"
        client.http_client.assert_request_made("DELETE", "/teams/123/members")

    def test_remove_all_members_success(self, mock_client):
        """Test successful removal of all team members."""
        client = mock_client
        client.http_client.add_response("/teams/123/members", [])
        
        members = client.teams.remove_members(123)  # No members specified = remove all
        
        assert len(members) == 0
        client.http_client.assert_request_made("DELETE", "/teams/123/members")

    def test_team_with_complex_members(self, mock_client):
        """Test team response with complex member structure."""
        client = mock_client
        team_data = MockResponseBuilder.team(
            team_id=123,
            members=[
                MockResponseBuilder.team_member(user_id=1, email="admin@example.com", admin=True),
                MockResponseBuilder.team_member(user_id=2, email="user@example.com", admin=False),
                MockResponseBuilder.team_member(user_id=3, email="another@example.com", admin=True)
            ]
        )
        client.http_client.add_response("/teams/123", team_data)
        
        team = client.teams.get(123)
        
        assert len(team.members) == 3
        admin_members = [m for m in team.members if m.admin]
        regular_members = [m for m in team.members if not m.admin]
        assert len(admin_members) == 2
        assert len(regular_members) == 1

    def test_http_error_handling(self, mock_client):
        """Test proper HTTP error handling."""
        client = mock_client
        client.http_client.add_error("/teams", 
            HttpClientError("Server Error", status_code=500, response={"message": "Internal error"}))
        
        with pytest.raises(ServerError) as exc_info:
            client.teams.list()
        
        assert exc_info.value.status_code == 500

    def test_empty_list_response(self, mock_client):
        """Test handling of empty list response."""
        client = mock_client
        client.http_client.add_response("/teams", [])
        
        teams = client.teams.list()
        
        assert teams == []

    def test_empty_members_list(self, mock_client):
        """Test handling of empty members list."""
        client = mock_client
        client.http_client.add_response("/teams/123/members", [])
        
        members = client.teams.get_members(123)
        
        assert members == []

    def test_team_member_request_validation(self, mock_client):
        """Test TeamMemberRequest validation."""
        # Valid with email
        request1 = TeamMemberRequest(email="test@example.com", admin=True)
        assert request1.email == "test@example.com"
        assert request1.admin
        assert request1.id is None
        
        # Valid with ID
        request2 = TeamMemberRequest(id=123, admin=False)
        assert request2.id == 123
        assert not request2.admin
        assert request2.email is None
        
        # Valid with both (API allows this)
        request3 = TeamMemberRequest(id=123, email="test@example.com", admin=True)
        assert request3.id == 123
        assert request3.email == "test@example.com"
        assert request3.admin

    def test_create_team_minimal_data(self, mock_client):
        """Test creating team with minimal required data."""
        client = mock_client
        request_data = TeamCreate(name="Minimal Team")  # Only name required
        response_data = MockResponseBuilder.team()
        response_data.update({"id": 123, "name": "Minimal Team"})
        client.http_client.add_response("/teams", response_data)
        
        team = client.teams.create(request_data)
        
        assert isinstance(team, Team)
        assert team.name == "Minimal Team"

    def test_update_team_partial_data(self, mock_client):
        """Test updating team with partial data."""
        client = mock_client
        request_data = TeamUpdate(description="New description only")
        response_data = MockResponseBuilder.team(team_id=123, description="New description only")
        client.http_client.add_response("/teams/123", response_data)
        
        team = client.teams.update(123, request_data)
        
        assert isinstance(team, Team)
        assert team.description == "New description only"

    def test_member_management_error_handling(self, mock_client):
        """Test error handling in member management operations."""
        client = mock_client
        client.http_client.add_error("/teams/123/members",
            HttpClientError("Member not found", status_code=404, 
                          response={"message": "User not found"}))
        
        request_data = TeamMemberList(
            members=[TeamMemberRequest(email="nonexistent@example.com")]
        )
        
        with pytest.raises(NotFoundError):
            client.teams.add_members(123, request_data) 