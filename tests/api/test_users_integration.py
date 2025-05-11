"""
Integration tests for the Users API

These tests validate read operations for users:
1. Get current user
2. Get user preferences 
3. List users (if allowed)
4. Get user details (if allowed)
5. Get user metrics (if available)
"""
import logging
import os
import uuid
import pytest
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

from nexla_sdk import NexlaClient
from nexla_sdk.exceptions import NexlaAPIError
from nexla_sdk.models.users import (
    User,
    UserList,
    UserDetail,
    UserDetailExpanded,
    UserPreferences
)
from nexla_sdk.models.common import ResourceType
from nexla_sdk.models.metrics import (
    AccessRole,
    AccountMetricsResponse,
    DashboardResponse,
    DailyMetricsResponse
)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Apply the skip_if_no_integration_creds marker to all tests in this module
pytestmark = [
    pytest.mark.integration,
    pytest.mark.usefixtures("nexla_client"),
]


@pytest.fixture(scope="module")
def unique_test_id():
    """Generate a unique ID for test resources"""
    return f"sdk_test_{uuid.uuid4().hex[:8]}"


class TestUsersIntegration:
    """Integration tests for the Users API"""
    
    def test_get_current_user(self, nexla_client: NexlaClient):
        """Test getting the current user"""
        try:
            logger.info("Getting current user")
            current_user = nexla_client.users.get_current()
            logger.debug(f"Current user details: {current_user}")
            
            assert isinstance(current_user, User)
            assert hasattr(current_user, "id")
            assert hasattr(current_user, "email")
            assert hasattr(current_user, "full_name")
            logger.info(f"Successfully retrieved current user: {current_user.email}")
            
        except Exception as e:
            logger.error(f"Test failed: {e}")
            raise Exception(f"Get current user test failed: {e}") from e
    
    def test_get_user_preferences(self, nexla_client: NexlaClient):
        """Test getting user preferences"""
        try:
            logger.info("Getting user preferences")
            try:
                preferences = nexla_client.users.get_preferences()
                logger.debug(f"User preferences: {preferences}")
                
                assert isinstance(preferences, (UserPreferences, Dict))
                logger.info("Successfully retrieved user preferences")
                
                # Try updating preferences with the same values (non-destructive)
                try:
                    logger.info("Updating user preferences (non-destructive)")
                    # Get the current preferences as a dict
                    pref_dict = preferences.model_dump() if hasattr(preferences, "model_dump") else dict(preferences)
                    
                    # Update with the same values
                    updated_preferences = nexla_client.users.update_preferences(pref_dict)
                    logger.debug(f"Updated user preferences: {updated_preferences}")
                    
                    assert isinstance(updated_preferences, (UserPreferences, Dict))
                    logger.info("Successfully updated user preferences")
                    
                except NexlaAPIError as e:
                    # Update might not be allowed for the current user
                    logger.warning(f"Update preferences not allowed: {e}")
            except NexlaAPIError as e:
                # The preferences endpoint might not be available
                if e.status_code == 404:
                    logger.warning("User preferences endpoint not available")
                    pytest.skip("User preferences endpoint not available")
                else:
                    raise e
                
        except Exception as e:
            logger.error(f"Test failed: {e}")
            raise Exception(f"Get user preferences test failed: {e}") from e
    
    def test_list_users(self, nexla_client: NexlaClient):
        """Test listing users (if allowed)"""
        try:
            logger.info("Listing users")
            users = nexla_client.users.list()
            
            # Note: This might fail if the current user doesn't have permissions
            logger.debug(f"Users list (first few): {users[:5] if len(users) >= 5 else users}")
            
            assert isinstance(users, List)
            # There should be at least one user (the current one)
            assert len(users) > 0
            assert isinstance(users[0], User)
            logger.info(f"Successfully listed {len(users)} users")
            
            # Try with expand=True
            try:
                logger.info("Listing users with expand=True")
                expanded_users = nexla_client.users.list(expand=True)
                logger.debug(f"Expanded users list (first few): {expanded_users[:5] if len(expanded_users) >= 5 else expanded_users}")
                
                assert isinstance(expanded_users, List)
                assert len(expanded_users) > 0
                logger.info(f"Successfully listed {len(expanded_users)} expanded users")
                
            except NexlaAPIError as e:
                # Expanded list might not be available
                logger.warning(f"Expanded users list not available: {e}")
            
        except NexlaAPIError as e:
            # List users might not be allowed for the current user
            logger.warning(f"List users operation not allowed: {e}")
            pytest.skip(f"List users operation not allowed: {e}")
            
        except Exception as e:
            logger.error(f"Test failed: {e}")
            raise Exception(f"List users test failed: {e}") from e
    
    def test_get_user(self, nexla_client: NexlaClient):
        """Test getting a user by ID (using current user)"""
        try:
            # First get the current user to have a valid ID
            logger.info("Getting current user ID")
            current_user = nexla_client.users.get_current()
            user_id = current_user.id
            logger.info(f"Current user ID: {user_id}")
            
            # Now get the same user by ID
            logger.info(f"Getting user with ID: {user_id}")
            user = nexla_client.users.get(user_id)
            logger.debug(f"User details: {user}")
            
            assert isinstance(user, User)
            assert user.id == current_user.id
            assert user.email == current_user.email
            logger.info(f"Successfully retrieved user: {user.email}")
            
            # Try with expand=True
            try:
                logger.info(f"Getting user with ID: {user_id} and expand=True")
                expanded_user = nexla_client.users.get(user_id, expand=True)
                logger.debug(f"Expanded user details: {expanded_user}")
                
                assert isinstance(expanded_user, (User, UserDetailExpanded))
                assert expanded_user.id == user_id
                logger.info(f"Successfully retrieved expanded user: {expanded_user.email}")
                
            except NexlaAPIError as e:
                # Expanded details might not be available
                logger.warning(f"Expanded user details not available: {e}")
            
        except Exception as e:
            logger.error(f"Test failed: {e}")
            raise Exception(f"Get user test failed: {e}") from e
    
    def test_user_metrics(self, nexla_client: NexlaClient):
        """Test getting user metrics (if available)"""
        try:
            # First get the current user to have a valid ID
            logger.info("Getting current user ID")
            current_user = nexla_client.users.get_current()
            user_id = current_user.id
            logger.info(f"Current user ID: {user_id}")
            
            # Get flow stats (dashboard)
            try:
                logger.info(f"Getting flow stats for user with ID: {user_id}")
                flow_stats = nexla_client.users.get_flow_stats(user_id)
                logger.debug(f"Flow stats: {flow_stats}")
                
                assert isinstance(flow_stats, DashboardResponse)
                logger.info(f"Successfully retrieved flow stats")
                
            except NexlaAPIError as e:
                # Flow stats might not be available
                logger.warning(f"Flow stats not available: {e}")
            
            # Get account metrics
            try:
                # Get metrics for the last 7 days
                from_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
                to_date = datetime.now().strftime("%Y-%m-%d")
                
                logger.info(f"Getting account metrics for user with ID: {user_id} from {from_date} to {to_date}")
                account_metrics = nexla_client.users.get_account_metrics(
                    user_id=user_id,
                    from_date=from_date,
                    to_date=to_date
                )
                logger.debug(f"Account metrics: {account_metrics}")
                
                assert isinstance(account_metrics, AccountMetricsResponse)
                logger.info(f"Successfully retrieved account metrics")
                
            except NexlaAPIError as e:
                # Account metrics might not be available
                logger.warning(f"Account metrics not available: {e}")
            
            # Get daily metrics for sources
            try:
                # Get metrics for the last 7 days
                from_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
                to_date = datetime.now().strftime("%Y-%m-%d")
                
                logger.info(f"Getting daily metrics for sources for user with ID: {user_id} from {from_date} to {to_date}")
                daily_source_metrics = nexla_client.users.get_daily_metrics(
                    user_id=user_id,
                    resource_type=ResourceType.DATA_SOURCE,
                    from_date=from_date,
                    to_date=to_date
                )
                logger.debug(f"Daily source metrics: {daily_source_metrics}")
                
                assert isinstance(daily_source_metrics, DailyMetricsResponse)
                logger.info(f"Successfully retrieved daily source metrics")
                
            except NexlaAPIError as e:
                # Daily metrics might not be available
                logger.warning(f"Daily source metrics not available: {e}")
            
            # Get daily metrics for sinks
            try:
                # Get metrics for the last 7 days
                from_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
                to_date = datetime.now().strftime("%Y-%m-%d")
                
                logger.info(f"Getting daily metrics for sinks for user with ID: {user_id} from {from_date} to {to_date}")
                daily_sink_metrics = nexla_client.users.get_daily_metrics(
                    user_id=user_id,
                    resource_type=ResourceType.DATA_SINK,
                    from_date=from_date,
                    to_date=to_date
                )
                logger.debug(f"Daily sink metrics: {daily_sink_metrics}")
                
                assert isinstance(daily_sink_metrics, DailyMetricsResponse)
                logger.info(f"Successfully retrieved daily sink metrics")
                
            except NexlaAPIError as e:
                # Daily metrics might not be available
                logger.warning(f"Daily sink metrics not available: {e}")
            
        except Exception as e:
            logger.error(f"Test failed: {e}")
            raise Exception(f"User metrics test failed: {e}") from e 