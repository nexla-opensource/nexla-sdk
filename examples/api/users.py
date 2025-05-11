"""
Examples of using the Nexla Users API
"""
import logging
from datetime import datetime, timedelta

from nexla_sdk.models.users import CreateUserRequest, UpdateUserRequest, UserStatus
from nexla_sdk.models.common import ResourceType

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from client import nexla_client


def get_current_user():
    """Example: Get current user information"""
    logger.info("Getting current user information")
    current_user = nexla_client.users.get_current()
    
    logger.info(f"Current user: {current_user.full_name} ({current_user.email})")
    logger.info(f"User ID: {current_user.id}")
    logger.info(f"Status: {current_user.status}")
    
    if current_user.default_org:
        logger.info(f"Default organization: {current_user.default_org.name} (ID: {current_user.default_org.id})")
    
    return current_user


def get_user_preferences():
    """Example: Get user preferences"""
    logger.info("Getting user preferences")
    try:
        preferences = nexla_client.users.get_preferences()
        logger.info(f"User preferences: {preferences.preferences}")
        return preferences
    except Exception as e:
        logger.warning(f"Could not retrieve preferences: {e}")
        return None


def list_users(access_role=None):
    """Example: List users in organization
    
    Args:
        access_role: Optional access role filter
    """
    logger.info("Listing users")
    
    # Note: This operation is only available for organization admins
    try:
        users = nexla_client.users.list()
        logger.info(f"Found {len(users)} users")
        
        for i, user in enumerate(users[:5], 1):  # Show first 5 users
            logger.info(f"User {i}: {user.full_name} ({user.email})")
        
        if len(users) > 5:
            logger.info(f"...and {len(users) - 5} more users")
            
        return users
    except Exception as e:
        logger.error(f"Failed to list users: {e}")
        return None


def get_user_details(user_id=None):
    """Example: Get details for a specific user
    
    Args:
        user_id: User ID to retrieve (defaults to current user's ID if None)
    """
    if user_id is None:
        current_user = get_current_user()
        user_id = current_user.id
    
    logger.info(f"Getting details for user ID {user_id}")
    
    try:
        # First try non-expanded mode
        user = nexla_client.users.get(user_id)
        logger.info(f"Found user: {user.full_name} ({user.email})")
        
        # Then try expanded mode if you need account summary
        try:
            expanded_user = nexla_client.users.get(user_id, expand=True)
            if hasattr(expanded_user, 'account_summary'):
                sources = expanded_user.account_summary.data_sources.counts
                sinks = expanded_user.account_summary.data_sinks.counts
                nexsets = expanded_user.account_summary.data_sets.counts
                
                logger.info(f"Resource counts:")
                logger.info(f"  Sources: {sources.total} total, {sources.active} active")
                logger.info(f"  Destinations: {sinks.total} total, {sinks.active} active")
                logger.info(f"  Data Sets: {nexsets.total} total")
        except Exception as e:
            logger.warning(f"Could not get expanded user details: {e}")
        
        return user
    except Exception as e:
        logger.error(f"Failed to get user details: {e}")
        return None


def create_user(org_id, email, full_name, is_admin=False):
    """Example: Create a new user in an organization
    
    Args:
        org_id: Organization ID to add user to
        email: User email
        full_name: User full name
        is_admin: Whether the user should be an org admin
    """
    logger.info(f"Creating new user {email} in organization {org_id}")
    
    # Note: This operation is only available for organization admins
    try:
        # Create a request object
        user_request = CreateUserRequest(
            full_name=full_name,
            email=email,
            default_org_id=org_id,
            status=UserStatus.ACTIVE
        )
        
        new_user = nexla_client.users.create(user_request)
        logger.info(f"Successfully created user: {new_user.full_name} (ID: {new_user.id})")
        return new_user
    except Exception as e:
        logger.error(f"Failed to create user: {e}")
        return None


def update_user(user_id, new_full_name=None, new_status=None):
    """Example: Update a user
    
    Args:
        user_id: User ID to update
        new_full_name: New name for the user (or None to keep current)
        new_status: New status for the user (or None to keep current)
    """
    logger.info(f"Updating user {user_id}")
    
    try:
        # Build update request with only fields to change
        update_data = {}
        if new_full_name:
            update_data['name'] = new_full_name
        if new_status:
            update_data['status'] = new_status
            
        if not update_data:
            logger.info("No changes requested")
            return get_user_details(user_id)
            
        # Create update request
        update_request = UpdateUserRequest(**update_data)
        
        # Update the user
        updated_user = nexla_client.users.update(user_id, update_request)
        logger.info(f"Successfully updated user {updated_user.id}: {updated_user.full_name}")
        return updated_user
    except Exception as e:
        logger.error(f"Failed to update user: {e}")
        return None


def get_user_metrics(user_id=None):
    """Example: Get metrics for a user
    
    Args:
        user_id: User ID to get metrics for (defaults to current user's ID if None)
    """
    if user_id is None:
        current_user = get_current_user()
        user_id = current_user.id
    
    logger.info(f"Getting metrics for user ID {user_id}")
    
    results = {}
    
    # Get metrics for the last 7 days
    from_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    to_date = datetime.now().strftime("%Y-%m-%d")
    
    # Get account metrics
    try:
        account_metrics = nexla_client.users.get_account_metrics(
            user_id=user_id,
            from_date=from_date,
            to_date=to_date
        )
        logger.info(f"Account metrics retrieved successfully")
        results["account_metrics"] = account_metrics
    except Exception as e:
        logger.warning(f"Failed to get account metrics: {e}")
    
    # Get source metrics
    try:
        source_metrics = nexla_client.users.get_daily_metrics(
            user_id=user_id,
            resource_type=ResourceType.DATA_SOURCE,
            from_date=from_date,
            to_date=to_date
        )
        logger.info(f"Source metrics retrieved successfully")
        results["source_metrics"] = source_metrics
    except Exception as e:
        logger.warning(f"Failed to get source metrics: {e}")
    
    # Get flow stats
    try:
        flow_stats = nexla_client.users.get_flow_stats(user_id=user_id)
        logger.info(f"Flow stats retrieved successfully")
        results["flow_stats"] = flow_stats
    except Exception as e:
        logger.warning(f"Failed to get flow stats: {e}")
    
    return results if results else None


if __name__ == "__main__":
    # Run the examples
    # Note: Some examples may fail if you don't have the necessary permissions
    
    # Basic information retrieval (works for all users)
    current_user = get_current_user()
    preferences = get_user_preferences()
    metrics = get_user_metrics()
    
    # Operations that may require admin privileges
    if current_user and hasattr(current_user, 'org_memberships'):
        for org in current_user.org_memberships:
            if org.is_admin:
                logger.info(f"You are an admin of organization: {org.name} (ID: {org.id})")
                
                # You can list users or create new ones
                users = list_users()
                
                # Example of creating a user (commented out to prevent accidental creation)
                # new_user = create_user(
                #     org_id=org.id,
                #     email="new.user@example.com",
                #     full_name="New Test User"
                # )
    
    # Get metrics for the current user
    metrics = get_user_metrics() 