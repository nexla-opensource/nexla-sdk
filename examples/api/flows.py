"""
Example usage of the Nexla Flows API

This example demonstrates various operations on flows using the Nexla SDK:
1. List flows
2. Get a specific flow
3. Create a new flow
4. Update a flow
5. Add/remove tags
6. Activate/pause flows
7. Copy a flow
8. Delete a flow
9. Working with flows by resource IDs
"""
import logging
from typing import Dict, Any

from nexla_sdk.models.access import AccessRole
from nexla_client import nexla_client

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def list_flows():
    """List all flows with pagination"""
    logger.info("Listing flows...")
    
    # Basic listing
    flows = nexla_client.flows.list()
    logger.info(f"Found {len(flows.flows)} flows")
    
    # With pagination
    flows_page_1 = nexla_client.flows.list(page=1, per_page=10)
    logger.info(f"Page 1: Found {len(flows_page_1.flows)} flows")
    
    # Filter by access role
    admin_flows = nexla_client.flows.list(access_role=AccessRole.ADMIN)
    logger.info(f"Admin flows: Found {len(admin_flows.flows)} flows")
    
    # Get just flow chains without resource details
    flows_only = nexla_client.flows.list(flows_only=1)
    logger.info(f"Flows only: Found {len(flows_only.flows)} flows")
    
    return flows


def get_flow(flow_id: str):
    """Get a specific flow by ID"""
    logger.info(f"Getting flow with ID: {flow_id}")
    flow = nexla_client.flows.get(flow_id)
    
    # Print flow details
    if hasattr(flow, "flows") and len(flow.flows) > 0:
        # This is a FlowResponse
        logger.info(f"Flow name: {flow.flows[0].name}")
    elif hasattr(flow, "name"):
        # This is a Flow
        logger.info(f"Flow name: {flow.name}")
    
    return flow


def create_flow():
    """Create a new flow"""
    logger.info("Creating a new flow...")
    
    # Define flow data
    flow_data = {
        "name": "Example Flow",
        "description": "Created by the Nexla SDK example",
        "flow_type": "auto"
    }
    
    # Create the flow
    new_flow = nexla_client.flows.create(flow_data)
    logger.info(f"Created flow with ID: {new_flow.id}")
    
    return new_flow


def update_flow(flow_id: str):
    """Update an existing flow"""
    logger.info(f"Updating flow with ID: {flow_id}")
    
    # Update with dictionary
    flow_data = {
        "name": "Updated Flow Name",
        "description": "Updated by the Nexla SDK example"
    }
    updated_flow = nexla_client.flows.update(flow_id, flow_data)
    logger.info(f"Updated flow with dictionary: {updated_flow.name}")
    
    # Update with keyword arguments
    updated_flow = nexla_client.flows.update(
        flow_id,
        name="Flow with Keyword Args",
        description="Updated using keyword arguments"
    )
    logger.info(f"Updated flow with kwargs: {updated_flow.name}")
    
    return updated_flow


def work_with_tags(flow_id: str):
    """Add and remove tags from a flow"""
    logger.info(f"Working with tags for flow with ID: {flow_id}")
    
    # Add tags
    tags = ["example", "sdk", "test"]
    tagged_flow = nexla_client.flows.add_tags(flow_id, tags)
    logger.info(f"Added tags: {tags}")
    
    # Get flow to verify tags were added
    flow = nexla_client.flows.get(flow_id)
    if hasattr(flow, "tags"):
        logger.info(f"Flow tags after adding: {flow.tags}")
    
    # Remove some tags
    tags_to_remove = ["example"]
    untagged_flow = nexla_client.flows.remove_tags(flow_id, tags_to_remove)
    logger.info(f"Removed tags: {tags_to_remove}")
    
    # Get flow to verify tags were removed
    flow = nexla_client.flows.get(flow_id)
    if hasattr(flow, "tags"):
        logger.info(f"Flow tags after removing: {flow.tags}")
    
    return flow


def activate_and_pause_flow(flow_id: str):
    """Activate and pause a flow"""
    logger.info(f"Activating flow with ID: {flow_id}")
    activated_flow = nexla_client.flows.activate(flow_id)
    
    # Check status
    if hasattr(activated_flow, "flows") and len(activated_flow.flows) > 0:
        logger.info(f"Flow status after activation: {activated_flow.flows[0].runtime_status}")
    elif hasattr(activated_flow, "status"):
        logger.info(f"Flow status after activation: {activated_flow.status}")
    
    # Pause the flow
    logger.info(f"Pausing flow with ID: {flow_id}")
    paused_flow = nexla_client.flows.pause(flow_id)
    
    # Check status
    if hasattr(paused_flow, "flows") and len(paused_flow.flows) > 0:
        logger.info(f"Flow status after pausing: {paused_flow.flows[0].runtime_status}")
    elif hasattr(paused_flow, "status"):
        logger.info(f"Flow status after pausing: {paused_flow.status}")
    
    return paused_flow


def copy_flow(flow_id: str):
    """Create a copy of a flow"""
    logger.info(f"Copying flow with ID: {flow_id}")
    
    # Copy with basic options
    copied_flow = nexla_client.flows.copy(
        flow_id,
        new_name="Copy of Example Flow",
        reuse_data_credentials=True
    )
    
    if hasattr(copied_flow, "flows") and len(copied_flow.flows) > 0:
        logger.info(f"Copied flow ID: {copied_flow.flows[0].id}")
    elif hasattr(copied_flow, "id"):
        logger.info(f"Copied flow ID: {copied_flow.id}")
    
    return copied_flow


def run_flow(flow_id: str):
    """Run a flow and check its status"""
    logger.info(f"Running flow with ID: {flow_id}")
    
    try:
        # Run the flow
        run_response = nexla_client.flows.run(flow_id)
        logger.info(f"Flow run initiated: {run_response}")
        
        # If run_id is available, check status
        if "run_id" in run_response:
            run_id = run_response["run_id"]
            status = nexla_client.flows.get_run_status(flow_id, run_id)
            logger.info(f"Flow run status: {status}")
        
        return run_response
    except Exception as e:
        logger.warning(f"Flow run not supported or failed: {e}")
        return None


def get_flow_by_resource(resource_type: str, resource_id: str):
    """Get a flow by resource ID"""
    logger.info(f"Getting flow for {resource_type} with ID: {resource_id}")
    
    flow = nexla_client.flows.get_by_resource(resource_type, resource_id)
    
    if hasattr(flow, "flows") and len(flow.flows) > 0:
        logger.info(f"Flow ID: {flow.flows[0].id}")
    elif hasattr(flow, "id"):
        logger.info(f"Flow ID: {flow.id}")
    
    return flow


def activate_flow_by_resource(resource_type: str, resource_id: str):
    """Activate a flow by resource ID"""
    logger.info(f"Activating flow for {resource_type} with ID: {resource_id}")
    
    activated_flow = nexla_client.flows.activate_by_resource(resource_type, resource_id)
    
    if hasattr(activated_flow, "flows") and len(activated_flow.flows) > 0:
        logger.info(f"Flow status after activation: {activated_flow.flows[0].runtime_status}")
    elif hasattr(activated_flow, "status"):
        logger.info(f"Flow status after activation: {activated_flow.status}")
    
    return activated_flow


def pause_flow_by_resource(resource_type: str, resource_id: str):
    """Pause a flow by resource ID"""
    logger.info(f"Pausing flow for {resource_type} with ID: {resource_id}")
    
    paused_flow = nexla_client.flows.pause_by_resource(resource_type, resource_id)
    
    if hasattr(paused_flow, "flows") and len(paused_flow.flows) > 0:
        logger.info(f"Flow status after pausing: {paused_flow.flows[0].runtime_status}")
    elif hasattr(paused_flow, "status"):
        logger.info(f"Flow status after pausing: {paused_flow.status}")
    
    return paused_flow


def list_condensed_flows():
    """List flows in condensed format"""
    logger.info("Listing flows in condensed format...")
    
    condensed_flows = nexla_client.flows.list_condensed()
    
    if "items" in condensed_flows:
        logger.info(f"Found {len(condensed_flows['items'])} condensed flows")
    
    return condensed_flows


def delete_flow(flow_id: str):
    """Delete a flow"""
    logger.info(f"Deleting flow with ID: {flow_id}")
    
    # Make sure the flow is paused first
    nexla_client.flows.pause(flow_id)
    
    # Delete the flow
    delete_response = nexla_client.flows.delete(flow_id)
    logger.info(f"Flow deletion response: {delete_response}")
    
    return delete_response


if __name__ == "__main__":
    # Run a complete flow lifecycle example
    try:
         # List flows
        list_flows()
        
        # Create a flow
        new_flow = create_flow()
        flow_id = new_flow.id
        
        # Get the flow
        get_flow(flow_id)
        
        # Update the flow
        update_flow(flow_id)
        
        # Work with tags
        work_with_tags(flow_id)
        
        # Activate and pause
        activate_and_pause_flow(flow_id)
        
        # Run the flow
        run_flow(flow_id)
        
        # Copy the flow
        copied_flow = copy_flow(flow_id)
        copied_flow_id = copied_flow.id if hasattr(copied_flow, "id") else None
        
        # List flows
        list_flows()
        
        # List condensed flows
        list_condensed_flows()
        
        # Clean up
        if copied_flow_id:
            delete_flow(copied_flow_id)
        delete_flow(flow_id)
        
        logger.info("Flow lifecycle example completed successfully!")
    except Exception as e:
        logger.error(f"Error in flow lifecycle example: {e}") 