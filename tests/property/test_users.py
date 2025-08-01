"""Property-based tests for UsersResource."""

import pytest
from hypothesis import given, strategies as st, assume
from nexla_sdk.models.users.responses import User, UserExpanded, UserSettings, DefaultOrg, OrgMembership
from nexla_sdk.models.users.requests import UserCreate, UserUpdate
from tests.utils.mock_builders import MockResponseBuilder
from tests.utils.assertions import NexlaAssertions


def generate_text_without_space():
    """Generate text without space characters to avoid Pydantic str_strip_whitespace issues."""
    return st.text(alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=100)


class TestUsersPropertyTests:
    """Property-based tests for UsersResource."""

    @given(
        user_id=st.integers(min_value=1, max_value=999999),
        email=st.emails(),
        full_name=generate_text_without_space(),
        super_user=st.booleans(),
        impersonated=st.booleans(),
        user_tier=st.sampled_from(["FREE", "TRIAL", "PAID", "FREE_FOREVER"]),
        status=st.sampled_from(["ACTIVE", "DEACTIVATED", "SOURCE_COUNT_CAPPED"]),
        account_locked=st.booleans()
    )
    def test_user_creation_with_various_inputs(self, mock_client, user_id, email, 
                                               full_name, super_user, impersonated, 
                                               user_tier, status, account_locked):
        """Test user creation with various input combinations."""
        client = mock_client
        
        # Create user data with generated values
        user_data = MockResponseBuilder.user(
            user_id=user_id,
            email=email,
            full_name=full_name,
            super_user=super_user,
            impersonated=impersonated,
            user_tier=user_tier,
            status=status,
            account_locked=account_locked
        )
        
        # Mock the API response
        client.http_client.add_response("GET", f"/users/{user_id}", user_data)
        
        # Test the response
        user = client.users.get(user_id)
        
        assert isinstance(user, User)
        assert user.id == user_id
        assert user.email == email
        assert user.full_name == full_name
        assert user.super_user == super_user
        assert user.impersonated == impersonated
        assert user.user_tier == user_tier
        assert user.status == status
        assert user.account_locked == account_locked

    @given(
        org_memberships=st.lists(
            st.fixed_dictionaries({
                'id': st.integers(min_value=1, max_value=1000),
                'name': generate_text_without_space(),
                'is_admin': st.booleans(),
                'org_membership_status': st.sampled_from(["ACTIVE", "DEACTIVATED"]),
                'api_key': st.text(min_size=10, max_size=50)
            }),
            min_size=0,
            max_size=5
        )
    )
    def test_user_response_parsing_with_org_memberships(self, mock_client, org_memberships):
        """Test user response parsing with various org membership configurations."""
        client = mock_client
        
        user_data = MockResponseBuilder.user(
            user_id=123,
            org_memberships=org_memberships
        )
        
        client.http_client.add_response("GET", "/users/123", user_data)
        
        user = client.users.get(123)
        
        assert isinstance(user, User)
        assert len(user.org_memberships) == len(org_memberships)
        
        for i, membership in enumerate(user.org_memberships):
            assert isinstance(membership, OrgMembership)
            assert membership.id == org_memberships[i]['id']
            assert membership.name == org_memberships[i]['name']
            assert membership.is_admin == org_memberships[i]['is_admin']
            assert membership.org_membership_status == org_memberships[i]['org_membership_status']
            assert membership.api_key == org_memberships[i]['api_key']

    @given(
        users_count=st.integers(min_value=0, max_value=10),
        page=st.integers(min_value=1, max_value=100),
        per_page=st.integers(min_value=1, max_value=100),
        access_role=st.one_of(st.none(), st.sampled_from(["owner", "collaborator", "operator", "admin", "all"]))
    )
    def test_list_users_with_various_parameters(self, mock_client, users_count, 
                                                page, per_page, access_role):
        """Test listing users with various parameter combinations."""
        client = mock_client
        
        # Generate list of users
        users_data = [
            MockResponseBuilder.user(user_id=i+1) 
            for i in range(users_count)
        ]
        
        client.http_client.add_response("GET", "/users", users_data)
        
        # Call with parameters
        kwargs = {"page": page, "per_page": per_page}
        if access_role:
            kwargs["access_role"] = access_role
        
        users = client.users.list(**kwargs)
        
        assert len(users) == users_count
        assert all(isinstance(user, User) for user in users)

    @given(
        name=st.one_of(st.none(), generate_text_without_space()),
        email=st.one_of(st.none(), st.emails()),
        status=st.one_of(st.none(), st.sampled_from(["ACTIVE", "DEACTIVATED"])),
        user_tier=st.one_of(st.none(), st.sampled_from(["FREE", "TRIAL", "PAID"])),
        password=st.one_of(st.none(), st.text(min_size=8, max_size=50))
    )
    def test_user_update_with_various_fields(self, mock_client, name, email, 
                                            status, user_tier, password):
        """Test user update with various field combinations."""
        client = mock_client
        
        # Create update request with only non-None values
        update_data = {}
        if name is not None:
            update_data["name"] = name
        if email is not None:
            update_data["email"] = email
        if status is not None:
            update_data["status"] = status
        if user_tier is not None:
            update_data["user_tier"] = user_tier
        if password is not None:
            update_data["password"] = password
        
        request = UserUpdate(**update_data)
        
        # Mock response
        response_data = MockResponseBuilder.user(user_id=123)
        if name is not None:
            response_data["full_name"] = name
        if email is not None:
            response_data["email"] = email
        if status is not None:
            response_data["status"] = status
        if user_tier is not None:
            response_data["user_tier"] = user_tier
        
        client.http_client.add_response("PUT", "/users/123", response_data)
        
        # Test the update
        user = client.users.update(123, request)
        
        assert isinstance(user, User)
        if name is not None:
            assert user.full_name == name
        if email is not None:
            assert user.email == email
        if status is not None:
            assert user.status == status
        if user_tier is not None:
            assert user.user_tier == user_tier

    @given(
        user_id=st.integers(min_value=1, max_value=999999),
        settings_count=st.integers(min_value=0, max_value=5)
    )
    def test_user_settings_response_parsing(self, mock_client, user_id, settings_count):
        """Test user settings response parsing with various configurations."""
        client = mock_client
        
        # Generate settings data
        settings_data = []
        for i in range(settings_count):
            settings_data.append({
                "id": f"setting_{i}",
                "owner": {"id": user_id, "name": f"User {user_id}"},
                "org": {"id": 1, "name": "Test Org"},
                "user_settings_type": "general",
                "settings": {"key": f"value_{i}"}
            })
        
        client.http_client.add_response("GET", "/user_settings", settings_data)
        
        settings = client.users.get_settings()
        
        assert len(settings) == settings_count
        assert all(isinstance(setting, UserSettings) for setting in settings)

    @given(
        from_date=st.dates(min_value=st.datetime(2020, 1, 1).date(), 
                          max_value=st.datetime(2025, 12, 31).date()).map(str),
        to_date=st.one_of(st.none(), 
                         st.dates(min_value=st.datetime(2020, 1, 1).date(), 
                                 max_value=st.datetime(2025, 12, 31).date()).map(str)),
        org_id=st.one_of(st.none(), st.integers(min_value=1, max_value=1000))
    )
    def test_account_metrics_with_various_parameters(self, mock_client, from_date, 
                                                    to_date, org_id):
        """Test account metrics with various parameter combinations."""
        # Ensure to_date is after from_date if both are provided
        if to_date is not None:
            assume(to_date >= from_date)
        
        client = mock_client
        
        metrics_data = {
            "total_sources": 5,
            "total_sinks": 3,
            "total_records": 10000
        }
        
        client.http_client.add_response("GET", "/users/123/flows/account_metrics", metrics_data)
        
        kwargs = {"from_date": from_date}
        if to_date is not None:
            kwargs["to_date"] = to_date
        if org_id is not None:
            kwargs["org_id"] = org_id
        
        metrics = client.users.get_account_metrics(123, **kwargs)
        
        assert isinstance(metrics, dict)
        assert "total_sources" in metrics

    @given(
        resource_type=st.sampled_from(["SOURCE", "SINK"]),
        from_date=st.dates(min_value=st.datetime(2020, 1, 1).date(), 
                          max_value=st.datetime(2025, 12, 31).date()).map(str),
        to_date=st.one_of(st.none(), 
                         st.dates(min_value=st.datetime(2020, 1, 1).date(), 
                                 max_value=st.datetime(2025, 12, 31).date()).map(str)),
        org_id=st.one_of(st.none(), st.integers(min_value=1, max_value=1000))
    )
    def test_daily_metrics_with_various_parameters(self, mock_client, resource_type, 
                                                  from_date, to_date, org_id):
        """Test daily metrics with various parameter combinations."""
        # Ensure to_date is after from_date if both are provided
        if to_date is not None:
            assume(to_date >= from_date)
        
        client = mock_client
        
        metrics_data = {
            "daily_records": 1000,
            "resource_type": resource_type
        }
        
        client.http_client.add_response("GET", "/users/123/metrics", metrics_data)
        
        kwargs = {
            "resource_type": resource_type,
            "from_date": from_date
        }
        if to_date is not None:
            kwargs["to_date"] = to_date
        if org_id is not None:
            kwargs["org_id"] = org_id
        
        metrics = client.users.get_daily_metrics(123, **kwargs)
        
        assert isinstance(metrics, dict)

    @given(
        full_name=generate_text_without_space(),
        email=st.emails(),
        default_org_id=st.one_of(st.none(), st.integers(min_value=1, max_value=1000)),
        status=st.one_of(st.none(), st.sampled_from(["ACTIVE", "DEACTIVATED"])),
        user_tier=st.one_of(st.none(), st.sampled_from(["FREE", "TRIAL", "PAID"]))
    )
    def test_user_creation_request_validation(self, full_name, email, default_org_id, 
                                             status, user_tier):
        """Test user creation request with various input combinations."""
        # Create request with only non-None values
        create_data = {
            "full_name": full_name,
            "email": email
        }
        if default_org_id is not None:
            create_data["default_org_id"] = default_org_id
        if status is not None:
            create_data["status"] = status
        if user_tier is not None:
            create_data["user_tier"] = user_tier
        
        # Should not raise validation error
        request = UserCreate(**create_data)
        
        assert request.full_name == full_name
        assert request.email == email
        if default_org_id is not None:
            assert request.default_org_id == default_org_id
        if status is not None:
            assert request.status == status
        if user_tier is not None:
            assert request.user_tier == user_tier

    @given(
        expand=st.booleans(),
        page=st.one_of(st.none(), st.integers(min_value=1, max_value=100)),
        per_page=st.one_of(st.none(), st.integers(min_value=1, max_value=100))
    )
    def test_list_users_parameter_combinations(self, mock_client, expand, page, per_page):
        """Test listing users with various parameter combinations."""
        client = mock_client
        
        user_data = MockResponseBuilder.user(user_id=123)
        
        if expand:
            client.http_client.add_response("GET", "/users?expand=1", [user_data])
        else:
            client.http_client.add_response("GET", "/users", [user_data])
        
        kwargs = {"expand": expand}
        if page is not None:
            kwargs["page"] = page
        if per_page is not None:
            kwargs["per_page"] = per_page
        
        users = client.users.list(**kwargs)
        
        assert len(users) == 1
        if expand:
            assert isinstance(users[0], UserExpanded)
        else:
            assert isinstance(users[0], User) 