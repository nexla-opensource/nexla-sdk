"""Integration tests for UsersResource."""

import os

import pytest

from nexla_sdk import NexlaClient
from nexla_sdk.exceptions import NotFoundError, ServerError


@pytest.mark.integration
class TestUsersIntegration:
    """Integration tests for UsersResource."""

    @pytest.fixture
    def client(self):
        """Create a test client with real credentials."""
        service_key = os.getenv("NEXLA_SERVICE_KEY")
        if not service_key:
            pytest.skip("NEXLA_SERVICE_KEY not set")
        return NexlaClient(service_key=service_key)

    def test_list_users_integration(self, client):
        """Test listing users against real API."""
        users = client.users.list()

        # Should return at least the current user
        assert len(users) >= 1

        # Verify structure
        user = users[0]
        assert hasattr(user, "id")
        assert hasattr(user, "email")
        assert hasattr(user, "full_name")
        assert hasattr(user, "default_org")

        # Verify API key is included
        assert hasattr(user, "api_key")

    def test_list_users_with_access_role_all(self, client):
        """Test listing all users with access_role=all parameter."""
        # This might require admin privileges
        try:
            users = client.users.list(access_role="all")
            assert isinstance(users, list)
        except ServerError as e:
            # If not authorized, expect 403
            if e.status_code == 403:
                pytest.skip("User does not have permission to list all users")
            else:
                raise

    def test_list_users_with_expand(self, client):
        """Test listing users with expand parameter."""
        users = client.users.list(expand=True)

        assert len(users) >= 1

        # When expanded, might include account summary
        user = users[0]
        assert hasattr(user, "id")
        assert hasattr(user, "email")

    def test_get_current_user(self, client):
        """Test getting current user details."""
        # Get the current user from list
        users = client.users.list()
        current_user_id = users[0].id

        # Get user details
        user = client.users.get(current_user_id)

        assert user.id == current_user_id
        assert user.email is not None
        assert user.full_name is not None
        assert user.default_org is not None

    def test_get_user_with_expand(self, client):
        """Test getting user with expand parameter."""
        users = client.users.list()
        user_id = users[0].id

        user = client.users.get(user_id, expand=True)

        assert user.id == user_id
        # Expanded user might have account summary
        assert hasattr(user, "account_summary")

    def test_get_nonexistent_user(self, client):
        """Test getting a user that doesn't exist."""
        with pytest.raises(NotFoundError):
            client.users.get(999999)

    def test_get_settings(self, client):
        """Test getting user settings."""
        settings = client.users.get_settings()

        # Settings might be empty, but should be a list
        assert isinstance(settings, list)

    def test_get_account_metrics(self, client):
        """Test getting account metrics."""
        users = client.users.list()
        user_id = users[0].id

        # Get metrics for the last 30 days
        metrics = client.users.get_account_metrics(user_id, from_date="2023-01-01")

        # Should return some metrics structure
        assert isinstance(metrics, dict)

    def test_get_dashboard_metrics(self, client):
        """Test getting dashboard metrics."""
        users = client.users.list()
        user_id = users[0].id

        metrics = client.users.get_dashboard_metrics(user_id)

        # Should return metrics structure
        assert isinstance(metrics, dict)

    def test_get_daily_metrics(self, client):
        """Test getting daily metrics."""
        users = client.users.list()
        user_id = users[0].id

        metrics = client.users.get_daily_metrics(
            user_id, resource_type="SOURCE", from_date="2023-01-01"
        )

        # Should return metrics data
        assert isinstance(metrics, dict)

    def test_pagination_functionality(self, client):
        """Test pagination with real API."""
        # Test first page
        page1 = client.users.list(page=1, per_page=1)
        assert len(page1) >= 0  # Might be 0 or 1 user

        # If there are users, verify pagination works
        if len(page1) > 0:
            # Try getting a second page (might be empty)
            page2 = client.users.list(page=2, per_page=1)
            assert isinstance(page2, list)

    def test_error_handling_real_api(self, client):
        """Test error handling with real API responses."""
        # Test various error scenarios that might occur

        # Invalid user ID format (if the API validates this)
        with pytest.raises((NotFoundError, ServerError)) as exc_info:
            client.users.get(-1)

        # Verify we got one of the expected exceptions
        assert isinstance(exc_info.value, (NotFoundError, ServerError))
        # Optionally verify the error message or status code
        if isinstance(exc_info.value, ServerError):
            assert exc_info.value.status_code in [400, 404]

    def test_user_validation_with_real_api(self, client):
        """Test that user responses match expected model structure."""
        users = client.users.list()

        if users:
            user = users[0]

            # Verify all required fields are present
            assert user.id is not None
            assert user.email is not None
            assert user.full_name is not None
            assert user.default_org is not None
            assert hasattr(user, "status")
            assert hasattr(user, "impersonated")

            # Verify org_memberships structure
            assert hasattr(user, "org_memberships")
            assert isinstance(user.org_memberships, list)

            # If there are org memberships, verify their structure
            for membership in user.org_memberships:
                assert hasattr(membership, "id")
                assert hasattr(membership, "name")
                assert hasattr(membership, "org_membership_status")
                # Should have API key after our model enhancement
                assert hasattr(membership, "api_key")
