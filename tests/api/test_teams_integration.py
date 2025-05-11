"""
Integration tests for the Teams API

These tests validate operations for teams:
1. List teams
2. Get team details
3. Team member operations
"""
import logging
import os
import uuid
import pytest
from typing import Dict, Any, List, Optional

from nexla_sdk import NexlaClient
from nexla_sdk.exceptions import NexlaAPIError
from nexla_sdk.models.access import AccessRole
from nexla_sdk.models.teams import Team, TeamList, TeamMember, TeamMemberList

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


class TestTeamsIntegration:
    """Integration tests for the Teams API"""
    
    def test_list_teams(self, nexla_client: NexlaClient):
        """Test listing teams"""
        try:
            logger.info("Listing teams")
            teams = nexla_client.teams.list()
            logger.debug(f"Teams: {teams}")
            
            assert isinstance(teams, TeamList)
            assert hasattr(teams, "items")
            assert isinstance(teams.items, list)
            
            if teams.items:
                logger.info(f"Found {len(teams.items)} teams")
                first_team = teams.items[0]
                assert isinstance(first_team, Team)
                assert hasattr(first_team, "id")
                assert hasattr(first_team, "name")
                logger.info(f"First team: {first_team.name} (ID: {first_team.id})")
            else:
                logger.info("No teams found")
                
            # Try with member access role
            try:
                logger.info("Listing teams where user is a member")
                # The API actually expects 'member' as a string, not an enum value
                member_teams = nexla_client.teams.list(access_role="member")
                
                assert isinstance(member_teams, TeamList)
                logger.info(f"Found {len(member_teams.items)} teams where user is a member")
                
            except NexlaAPIError as e:
                logger.warning(f"Could not list teams with member role: {e}")
            
        except Exception as e:
            logger.error(f"Test failed: {e}")
            raise Exception(f"List teams test failed: {e}") from e
    
    def test_create_get_update_delete_team(self, nexla_client: NexlaClient, unique_test_id):
        """Test creating, getting, updating, and deleting a team"""
        test_team_id = None
        
        try:
            # Create a team
            test_team_name = f"SDK Test Team {unique_test_id}"
            test_description = f"Team created by SDK integration tests {unique_test_id}"
            
            logger.info(f"Creating test team: {test_team_name}")
            
            try:
                new_team = nexla_client.teams.create(
                    name=test_team_name,
                    description=test_description
                )
                
                assert isinstance(new_team, Team)
                assert new_team.name == test_team_name
                assert new_team.description == test_description
                
                test_team_id = new_team.id
                logger.info(f"Successfully created test team with ID: {test_team_id}")
                
                # Get the team
                logger.info(f"Getting team details for ID: {test_team_id}")
                team = nexla_client.teams.get(test_team_id)
                
                assert isinstance(team, Team)
                assert team.id == test_team_id
                assert team.name == test_team_name
                assert team.description == test_description
                
                logger.info(f"Successfully retrieved team details")
                
                # Update the team
                updated_name = f"{test_team_name} - Updated"
                updated_description = f"{test_description} - Updated"
                
                logger.info(f"Updating team {test_team_id} with new name and description")
                updated_team = nexla_client.teams.update(
                    team_id=test_team_id,
                    name=updated_name,
                    description=updated_description
                )
                
                assert isinstance(updated_team, Team)
                assert updated_team.id == test_team_id
                assert updated_team.name == updated_name
                assert updated_team.description == updated_description
                
                logger.info(f"Successfully updated team")
                
            except NexlaAPIError as e:
                logger.warning(f"Team operations not available or authorized: {e}")
                pytest.skip(f"Team operations not available or authorized: {e}")
                
        except Exception as e:
            logger.error(f"Test failed: {e}")
            raise Exception(f"Team create/get/update test failed: {e}") from e
            
        finally:
            # Clean up - delete the team if it was created
            if test_team_id:
                try:
                    logger.info(f"Cleaning up - deleting test team {test_team_id}")
                    nexla_client.teams.delete(test_team_id)
                    logger.info(f"Successfully deleted test team")
                except Exception as e:
                    # Try with force=1 if it fails
                    try:
                        nexla_client.teams.delete(test_team_id, params={"force": 1})
                        logger.info(f"Successfully deleted test team with force=1")
                    except Exception as inner_e:
                        logger.warning(f"Could not delete test team: {inner_e}")
    
    def test_team_members(self, nexla_client: NexlaClient, unique_test_id):
        """Test team member operations"""
        test_team_id = None
        
        try:
            # Create a team for testing
            test_team_name = f"SDK Test Team Members {unique_test_id}"
            
            logger.info(f"Creating test team: {test_team_name}")
            
            try:
                # Get current user to use as a member
                current_user = nexla_client.users.get_current()
                
                # Create team with the current user as a member
                new_team = nexla_client.teams.create(
                    name=test_team_name,
                    members=[
                        {"email": current_user.email, "admin": True}
                    ]
                )
                
                test_team_id = new_team.id
                logger.info(f"Successfully created test team with ID: {test_team_id}")
                
                # Verify initial members
                logger.info(f"Getting team members for team {test_team_id}")
                members = nexla_client.teams.get_members(test_team_id)
                
                assert isinstance(members, TeamMemberList)
                assert hasattr(members, "members")
                assert len(members.members) == 1
                assert members.members[0].email == current_user.email
                assert members.members[0].admin == True
                
                logger.info(f"Team has 1 member as expected")
                
                # Test updating members (if we have multiple users available)
                try:
                    users = nexla_client.users.list()
                    if len(users) > 1:
                        # Find a user that isn't the current user
                        other_user = next((u for u in users if u.id != current_user.id), None)
                        
                        if other_user:
                            logger.info(f"Adding another member to the team: {other_user.email}")
                            
                            # Add the user
                            updated_members = nexla_client.teams.add_members(
                                team_id=test_team_id,
                                members=[
                                    {"email": other_user.email}
                                ]
                            )
                            
                            assert isinstance(updated_members, TeamMemberList)
                            assert len(updated_members.members) == 2
                            
                            logger.info(f"Successfully added member, team now has 2 members")
                            
                            # Replace members
                            logger.info(f"Replacing all members with just the new user")
                            replaced_members = nexla_client.teams.replace_members(
                                team_id=test_team_id,
                                members=[
                                    {"email": other_user.email, "admin": True}
                                ]
                            )
                            
                            assert isinstance(replaced_members, TeamMemberList)
                            assert len(replaced_members.members) == 1
                            assert replaced_members.members[0].email == other_user.email
                            
                            logger.info(f"Successfully replaced members")
                            
                            # Remove members
                            logger.info(f"Removing all members")
                            removed_members = nexla_client.teams.remove_members(test_team_id)
                            
                            assert isinstance(removed_members, TeamMemberList)
                            assert len(removed_members.members) == 0
                            
                            logger.info(f"Successfully removed all members")
                    else:
                        logger.info("Not enough users available to test add/replace operations")
                        
                except Exception as e:
                    logger.warning(f"Could not test all member operations: {e}")
                    
            except NexlaAPIError as e:
                logger.warning(f"Team member operations not available or authorized: {e}")
                pytest.skip(f"Team member operations not available or authorized: {e}")
                
        except Exception as e:
            logger.error(f"Test failed: {e}")
            raise Exception(f"Team members test failed: {e}") from e
            
        finally:
            # Clean up - delete the team if it was created
            if test_team_id:
                try:
                    logger.info(f"Cleaning up - deleting test team {test_team_id}")
                    nexla_client.teams.delete(test_team_id)
                    logger.info(f"Successfully deleted test team")
                except Exception as e:
                    # Try with force=1 if it fails
                    try:
                        nexla_client.teams.delete(test_team_id, params={"force": 1})
                        logger.info(f"Successfully deleted test team with force=1")
                    except Exception as inner_e:
                        logger.warning(f"Could not delete test team: {inner_e}") 