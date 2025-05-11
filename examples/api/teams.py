"""
Examples of using the Nexla Teams API
"""
import os
import logging

from nexla_sdk.models.access import AccessRole

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from client import nexla_client


def list_owned_teams():
    """Example: List teams you own"""
    logger.info("Listing teams you own")
    
    try:
        teams = nexla_client.teams.list()
        logger.info(f"Found {len(teams.items)} teams")
        
        for i, team in enumerate(teams.items[:5], 1):  # Show first 5 teams
            logger.info(f"Team {i}: {team.name} (ID: {team.id})")
            if team.members:
                logger.info(f"  Members: {len(team.members)}")
            
        if len(teams.items) > 5:
            logger.info(f"...and {len(teams.items) - 5} more teams")
            
        return teams.items
    except Exception as e:
        logger.error(f"Failed to list teams: {e}")
        return []


def list_member_teams():
    """Example: List teams you're a member of"""
    logger.info("Listing teams you're a member of")
    
    try:
        # Use string value 'member' instead of enum
        member_teams = nexla_client.teams.list(access_role="member")
        logger.info(f"Found {len(member_teams.items)} teams where you're a member")
        
        for i, team in enumerate(member_teams.items, 1):
            logger.info(f"Team {i}: {team.name} (ID: {team.id})")
            if team.members:
                logger.info(f"  Members: {len(team.members)}")
            
        return member_teams.items
    except Exception as e:
        logger.error(f"Failed to list teams: {e}")
        return []


def get_team_details(team_id):
    """Example: Get details for a specific team
    
    Args:
        team_id: Team ID to retrieve
    """
    logger.info(f"Getting details for team ID {team_id}")
    
    try:
        team = nexla_client.teams.get(team_id)
        logger.info(f"Team: {team.name} (ID: {team.id})")
        
        if team.description:
            logger.info(f"Description: {team.description}")
            
        if team.owner:
            logger.info(f"Owner: {team.owner.full_name} ({team.owner.email})")
            
        if team.org:
            logger.info(f"Organization: {team.org.name} (ID: {team.org.id})")
            
        if team.members:
            logger.info(f"Members ({len(team.members)}):")
            for member in team.members:
                admin_status = " (admin)" if member.admin else ""
                logger.info(f"  - {member.email}{admin_status}")
                
        if team.access_roles:
            logger.info(f"Your roles: {', '.join([role.value for role in team.access_roles])}")
            
        return team
    except Exception as e:
        logger.error(f"Failed to get team details: {e}")
        return None


def create_team(name, description=None, members=None):
    """Example: Create a new team
    
    Args:
        name: Team name
        description: Optional team description
        members: Optional list of team members, where each member is a dict with
                 either 'id' (user ID) or 'email' keys, and an optional 'admin' boolean
    """
    logger.info(f"Creating new team: {name}")
    
    try:
        team = nexla_client.teams.create(
            name=name,
            description=description,
            members=members
        )
        
        logger.info(f"Successfully created team: {team.name} (ID: {team.id})")
        
        if team.members:
            logger.info(f"Added {len(team.members)} members:")
            for member in team.members:
                admin_status = " (admin)" if member.admin else ""
                logger.info(f"  - {member.email}{admin_status}")
                
        return team
    except Exception as e:
        logger.error(f"Failed to create team: {e}")
        return None


def update_team(team_id, name=None, description=None, members=None):
    """Example: Update an existing team
    
    Args:
        team_id: Team ID to update
        name: Optional new team name
        description: Optional new team description
        members: Optional list of new members to add (does not replace existing members)
    """
    logger.info(f"Updating team {team_id}")
    
    try:
        updated_team = nexla_client.teams.update(
            team_id=team_id,
            name=name,
            description=description,
            members=members
        )
        
        logger.info(f"Successfully updated team: {updated_team.name} (ID: {updated_team.id})")
        
        if updated_team.members:
            logger.info(f"Current members ({len(updated_team.members)}):")
            for member in updated_team.members:
                admin_status = " (admin)" if member.admin else ""
                logger.info(f"  - {member.email}{admin_status}")
                
        return updated_team
    except Exception as e:
        logger.error(f"Failed to update team: {e}")
        return None


def get_team_members(team_id):
    """Example: Get members of a team
    
    Args:
        team_id: Team ID
    """
    logger.info(f"Getting members for team {team_id}")
    
    try:
        members = nexla_client.teams.get_members(team_id)
        
        logger.info(f"Team has {len(members.members)} members:")
        for i, member in enumerate(members.members, 1):
            admin_status = " (admin)" if member.admin else ""
            logger.info(f"  {i}. {member.email}{admin_status}")
            
        return members.members
    except Exception as e:
        logger.error(f"Failed to get team members: {e}")
        return []


def add_team_members(team_id, new_members):
    """Example: Add members to a team
    
    Args:
        team_id: Team ID
        new_members: List of members to add, where each member is a dict with
                    either 'id' (user ID) or 'email' keys, and an optional 'admin' boolean
    """
    logger.info(f"Adding members to team {team_id}")
    
    try:
        updated_members = nexla_client.teams.add_members(team_id, new_members)
        
        logger.info(f"Successfully updated team members. Team now has {len(updated_members.members)} members:")
        for i, member in enumerate(updated_members.members, 1):
            admin_status = " (admin)" if member.admin else ""
            logger.info(f"  {i}. {member.email}{admin_status}")
            
        return updated_members.members
    except Exception as e:
        logger.error(f"Failed to add team members: {e}")
        return []


def replace_team_members(team_id, members):
    """Example: Replace all team members
    
    Args:
        team_id: Team ID
        members: New list of members, where each member is a dict with
                either 'id' (user ID) or 'email' keys, and an optional 'admin' boolean
    """
    logger.info(f"Replacing all members of team {team_id}")
    
    try:
        updated_members = nexla_client.teams.replace_members(team_id, members)
        
        logger.info(f"Successfully replaced team members. Team now has {len(updated_members.members)} members:")
        for i, member in enumerate(updated_members.members, 1):
            admin_status = " (admin)" if member.admin else ""
            logger.info(f"  {i}. {member.email}{admin_status}")
            
        return updated_members.members
    except Exception as e:
        logger.error(f"Failed to replace team members: {e}")
        return []


def remove_team_members(team_id, members_to_remove=None):
    """Example: Remove members from a team
    
    Args:
        team_id: Team ID
        members_to_remove: List of members to remove, where each member is a dict with
                          either 'id' (user ID) or 'email' keys. If None, all members will be removed.
    """
    action = "all members" if members_to_remove is None else f"{len(members_to_remove)} members"
    logger.info(f"Removing {action} from team {team_id}")
    
    try:
        remaining_members = nexla_client.teams.remove_members(team_id, members_to_remove)
        
        if len(remaining_members.members) == 0:
            logger.info("Successfully removed all members. Team now has no members.")
        else:
            logger.info(f"Successfully removed members. Team now has {len(remaining_members.members)} members:")
            for i, member in enumerate(remaining_members.members, 1):
                admin_status = " (admin)" if member.admin else ""
                logger.info(f"  {i}. {member.email}{admin_status}")
            
        return remaining_members.members
    except Exception as e:
        logger.error(f"Failed to remove team members: {e}")
        return []


def delete_team(team_id, force=False):
    """Example: Delete a team
    
    Args:
        team_id: Team ID to delete
        force: Whether to force deletion if the team has active permissions
    """
    logger.info(f"Deleting team {team_id}")
    
    try:
        params = {"force": 1} if force else {}
        result = nexla_client.teams.delete(team_id)
        logger.info(f"Successfully deleted team {team_id}")
        return True
    except Exception as e:
        if "force=1" in str(e):
            logger.warning(f"Team has active permissions. Set force=True to delete anyway.")
            return False
        logger.error(f"Failed to delete team: {e}")
        return False


if __name__ == "__main__":
    # Run the examples
    # Note: Some examples may fail if you don't have the necessary permissions
    
    # List teams
    owned_teams = list_owned_teams()
    member_teams = list_member_teams()
    
    # Example of creating a team (commented out to prevent accidental creation)
    # team = create_team(
    #     name="Example SDK Team",
    #     description="A team created using the Nexla SDK",
    #     members=[
    #         {"email": "user@example.com", "admin": True},
    #         {"email": "user2@example.com"}
    #     ]
    # )
    
    # If we have any teams, demonstrate other operations
    selected_team_id = None
    
    if owned_teams:
        selected_team_id = owned_teams[0].id
    elif member_teams:
        selected_team_id = member_teams[0].id
        
    if selected_team_id:
        # Get team details
        team_details = get_team_details(selected_team_id)
        
        # Get team members
        members = get_team_members(selected_team_id)
        
        # Example of updating a team (commented out to prevent accidental changes)
        # updated_team = update_team(
        #     team_id=selected_team_id,
        #     description="Updated description via SDK example"
        # )
        
        # Example of adding a member (commented out to prevent accidental changes)
        # new_members = add_team_members(
        #     team_id=selected_team_id,
        #     new_members=[{"email": "new.member@example.com"}]
        # )
        
        # Examples of additional operations (all commented out to prevent accidental changes)
        # replace_team_members(
        #     team_id=selected_team_id,
        #     members=[{"email": "replacement@example.com", "admin": True}]
        # )
        
        # remove_team_members(
        #     team_id=selected_team_id,
        #     members_to_remove=[{"email": "user@example.com"}]
        # )
        
        # delete_team(selected_team_id, force=True) 