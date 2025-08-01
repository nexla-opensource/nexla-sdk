"""Property-based tests for TeamsResource."""

import pytest
from hypothesis import given, strategies as st, assume
from nexla_sdk.models.teams.responses import Team, TeamMember
from nexla_sdk.models.teams.requests import TeamCreate, TeamUpdate, TeamMemberRequest, TeamMemberList
from tests.utils.mock_builders import MockResponseBuilder
from tests.utils.assertions import NexlaAssertions


def generate_text_without_space():
    """Generate text without space characters to avoid Pydantic str_strip_whitespace issues."""
    return st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=100)


class TestTeamsPropertyTests:
    """Property-based tests for TeamsResource."""

    @given(
        team_id=st.integers(min_value=1, max_value=999999),
        name=generate_text_without_space(),
        description=st.one_of(st.none(), generate_text_without_space()),
        member=st.booleans(),
        access_roles=st.lists(
            st.sampled_from(["owner", "admin", "collaborator", "operator", "member"]),
            min_size=1,
            max_size=3,
            unique=True
        )
    )
    def test_team_creation_with_various_inputs(self, mock_client, team_id, name, 
                                              description, member, access_roles):
        """Test team creation with various input combinations."""
        client = mock_client
        
        # Create team data with generated values
        team_data = MockResponseBuilder.team(
            team_id=team_id,
            name=name,
            description=description,
            member=member,
            access_roles=access_roles
        )
        
        # Mock the API response
        client.http_client.add_response("GET", f"/teams/{team_id}", team_data)
        
        # Test the response
        team = client.teams.get(team_id)
        
        assert isinstance(team, Team)
        assert team.id == team_id
        assert team.name == name
        if description is not None:
            assert team.description == description
        assert team.member == member
        assert team.access_roles == access_roles

    @given(
        members=st.lists(
            st.fixed_dictionaries({
                'id': st.integers(min_value=1, max_value=10000),
                'email': st.emails(),
                'admin': st.booleans()
            }),
            min_size=0,
            max_size=10
        )
    )
    def test_team_response_parsing_with_members(self, mock_client, members):
        """Test team response parsing with various member configurations."""
        client = mock_client
        
        team_data = MockResponseBuilder.team(
            team_id=123,
            members=members
        )
        
        client.http_client.add_response("GET", "/teams/123", team_data)
        
        team = client.teams.get(123)
        
        assert isinstance(team, Team)
        assert len(team.members) == len(members)
        
        for i, member in enumerate(team.members):
            assert isinstance(member, TeamMember)
            assert member.id == members[i]['id']
            assert member.email == members[i]['email']
            assert member.admin == members[i]['admin']

    @given(
        teams_count=st.integers(min_value=0, max_value=10),
        page=st.integers(min_value=1, max_value=100),
        per_page=st.integers(min_value=1, max_value=100),
        access_role=st.one_of(st.none(), st.sampled_from(["owner", "member", "collaborator", "admin"]))
    )
    def test_list_teams_with_various_parameters(self, mock_client, teams_count, 
                                               page, per_page, access_role):
        """Test listing teams with various parameter combinations."""
        client = mock_client
        
        # Generate list of teams
        teams_data = [
            MockResponseBuilder.team(team_id=i+1) 
            for i in range(teams_count)
        ]
        
        client.http_client.add_response("GET", "/teams", teams_data)
        
        # Call with parameters
        kwargs = {"page": page, "per_page": per_page}
        if access_role:
            kwargs["access_role"] = access_role
        
        teams = client.teams.list(**kwargs)
        
        assert len(teams) == teams_count
        assert all(isinstance(team, Team) for team in teams)

    @given(
        name=st.one_of(st.none(), generate_text_without_space()),
        description=st.one_of(st.none(), generate_text_without_space()),
        members_count=st.integers(min_value=0, max_value=5)
    )
    def test_team_update_with_various_fields(self, mock_client, name, description, 
                                           members_count):
        """Test team update with various field combinations."""
        client = mock_client
        
        # Create update request with only non-None values
        update_data = {}
        if name is not None:
            update_data["name"] = name
        if description is not None:
            update_data["description"] = description
        
        # Add some members if count > 0
        if members_count > 0:
            update_data["members"] = [
                TeamMemberRequest(email=f"user{i}@example.com", admin=(i % 2 == 0))
                for i in range(members_count)
            ]
        
        request = TeamUpdate(**update_data)
        
        # Mock response
        response_data = MockResponseBuilder.team(team_id=123)
        if name is not None:
            response_data["name"] = name
        if description is not None:
            response_data["description"] = description
        
        client.http_client.add_response("PUT", "/teams/123", response_data)
        
        # Test the update
        team = client.teams.update(123, request)
        
        assert isinstance(team, Team)
        if name is not None:
            assert team.name == name
        if description is not None:
            assert team.description == description

    @given(
        team_id=st.integers(min_value=1, max_value=999999),
        members_count=st.integers(min_value=0, max_value=10)
    )
    def test_team_members_response_parsing(self, mock_client, team_id, members_count):
        """Test team members response parsing with various configurations."""
        client = mock_client
        
        # Generate members data
        members_data = []
        for i in range(members_count):
            members_data.append(MockResponseBuilder.team_member(
                user_id=i+1,
                email=f"user{i}@example.com",
                admin=(i % 2 == 0)
            ))
        
        client.http_client.add_response("GET", f"/teams/{team_id}/members", members_data)
        
        members = client.teams.get_members(team_id)
        
        assert len(members) == members_count
        assert all(isinstance(member, TeamMember) for member in members)
        
        for i, member in enumerate(members):
            assert member.id == i + 1
            assert member.email == f"user{i}@example.com"
            assert member.admin == (i % 2 == 0)

    @given(
        add_members=st.lists(
            st.fixed_dictionaries({
                'email': st.emails(),
                'admin': st.booleans()
            }),
            min_size=1,
            max_size=5
        )
    )
    def test_add_members_with_various_configurations(self, mock_client, add_members):
        """Test adding members with various configurations."""
        client = mock_client
        
        # Create member request list
        member_requests = [
            TeamMemberRequest(email=member['email'], admin=member['admin'])
            for member in add_members
        ]
        
        request_data = TeamMemberList(members=member_requests)
        
        # Mock response - existing members plus new ones
        response_data = [
            MockResponseBuilder.team_member(user_id=999, email="existing@example.com", admin=True)
        ]
        
        for i, member in enumerate(add_members):
            response_data.append(MockResponseBuilder.team_member(
                user_id=i+1000,
                email=member['email'],
                admin=member['admin']
            ))
        
        client.http_client.add_response("PUT", "/teams/123/members", response_data)
        
        members = client.teams.add_members(123, request_data)
        
        assert len(members) == len(add_members) + 1  # existing + new
        assert all(isinstance(member, TeamMember) for member in members)

    @given(
        replace_members=st.lists(
            st.fixed_dictionaries({
                'email': st.emails(),
                'admin': st.booleans()
            }),
            min_size=0,
            max_size=5
        )
    )
    def test_replace_members_with_various_configurations(self, mock_client, replace_members):
        """Test replacing members with various configurations."""
        client = mock_client
        
        # Create member request list
        member_requests = [
            TeamMemberRequest(email=member['email'], admin=member['admin'])
            for member in replace_members
        ]
        
        request_data = TeamMemberList(members=member_requests)
        
        # Mock response - only the new members
        response_data = []
        for i, member in enumerate(replace_members):
            response_data.append(MockResponseBuilder.team_member(
                user_id=i+1,
                email=member['email'],
                admin=member['admin']
            ))
        
        client.http_client.add_response("POST", "/teams/123/members", response_data)
        
        members = client.teams.replace_members(123, request_data)
        
        assert len(members) == len(replace_members)
        assert all(isinstance(member, TeamMember) for member in members)

    @given(
        member_specification=st.one_of(
            st.fixed_dictionaries({'email': st.emails()}),
            st.fixed_dictionaries({'id': st.integers(min_value=1, max_value=10000)}),
            st.fixed_dictionaries({
                'email': st.emails(),
                'id': st.integers(min_value=1, max_value=10000)
            })
        ),
        admin=st.booleans()
    )
    def test_team_member_request_variations(self, member_specification, admin):
        """Test TeamMemberRequest with various identification methods."""
        # Add admin to the specification
        member_data = {**member_specification, 'admin': admin}
        
        # Should not raise validation error
        request = TeamMemberRequest(**member_data)
        
        if 'email' in member_specification:
            assert request.email == member_specification['email']
        else:
            assert request.email is None
            
        if 'id' in member_specification:
            assert request.id == member_specification['id']
        else:
            assert request.id is None
            
        assert request.admin == admin

    @given(
        name=generate_text_without_space(),
        description=st.one_of(st.none(), generate_text_without_space()),
        initial_members=st.lists(
            st.fixed_dictionaries({
                'email': st.emails(),
                'admin': st.booleans()
            }),
            min_size=0,
            max_size=3
        )
    )
    def test_team_creation_request_validation(self, name, description, initial_members):
        """Test team creation request with various input combinations."""
        # Create request with generated values
        create_data = {"name": name}
        if description is not None:
            create_data["description"] = description
        
        if initial_members:
            create_data["members"] = [
                TeamMemberRequest(email=member['email'], admin=member['admin'])
                for member in initial_members
            ]
        
        # Should not raise validation error
        request = TeamCreate(**create_data)
        
        assert request.name == name
        if description is not None:
            assert request.description == description
        
        if initial_members:
            assert len(request.members) == len(initial_members)
            for i, member in enumerate(request.members):
                assert member.email == initial_members[i]['email']
                assert member.admin == initial_members[i]['admin']

    @given(
        expand=st.booleans(),
        page=st.one_of(st.none(), st.integers(min_value=1, max_value=100)),
        per_page=st.one_of(st.none(), st.integers(min_value=1, max_value=100))
    )
    def test_list_teams_parameter_combinations(self, mock_client, expand, page, per_page):
        """Test listing teams with various parameter combinations."""
        client = mock_client
        
        team_data = MockResponseBuilder.team(team_id=123)
        client.http_client.add_response("GET", "/teams", [team_data])
        
        kwargs = {}
        if page is not None:
            kwargs["page"] = page
        if per_page is not None:
            kwargs["per_page"] = per_page
        
        teams = client.teams.list(**kwargs)
        
        assert len(teams) == 1
        assert isinstance(teams[0], Team)

    @given(
        remove_by=st.sampled_from(['email', 'id', 'both']),
        members_to_remove=st.lists(
            st.fixed_dictionaries({
                'email': st.emails(),
                'id': st.integers(min_value=1, max_value=10000)
            }),
            min_size=1,
            max_size=3
        )
    )
    def test_remove_members_with_various_identifiers(self, mock_client, remove_by, 
                                                   members_to_remove):
        """Test removing members using various identification methods."""
        client = mock_client
        
        # Create removal request based on identification method
        member_requests = []
        for member in members_to_remove:
            if remove_by == 'email':
                member_requests.append(TeamMemberRequest(email=member['email']))
            elif remove_by == 'id':
                member_requests.append(TeamMemberRequest(id=member['id']))
            else:  # both
                member_requests.append(TeamMemberRequest(
                    email=member['email'], 
                    id=member['id']
                ))
        
        request_data = TeamMemberList(members=member_requests)
        
        # Mock response - remaining members (empty for simplicity)
        client.http_client.add_response("DELETE", "/teams/123/members", [])
        
        members = client.teams.remove_members(123, request_data)
        
        assert isinstance(members, list)
        # After removal, we expect the response (could be empty)

    @given(
        tags=st.lists(
            generate_text_without_space(),
            min_size=0,
            max_size=5,
            unique=True
        )
    )
    def test_team_with_tags(self, mock_client, tags):
        """Test team response with various tag configurations."""
        client = mock_client
        
        team_data = MockResponseBuilder.team(team_id=123, tags=tags)
        client.http_client.add_response("GET", "/teams/123", team_data)
        
        team = client.teams.get(123)
        
        assert isinstance(team, Team)
        assert team.tags == tags 