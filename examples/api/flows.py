"""
Example usage of the Nexla Flows API

This example demonstrates various operations on flows using the Nexla SDK:
1. List flows
2. Get a specific flow
3. Get flows for a data source
4. Get flows for a data sink
5. Activate/pause flows
6. Delete flows
"""
import logging
from typing import Dict, Any

from nexla_sdk.models.access import AccessRole
from client import nexla_client

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
        logger.info(f"Flow ID: {flow.flows[0].id}")
        if hasattr(flow.flows[0], "name") and flow.flows[0].name:
            logger.info(f"Flow name: {flow.flows[0].name}")
    elif hasattr(flow, "name"):
        # This is a Flow
        logger.info(f"Flow name: {flow.name}")
    
    return flow


def get_flow_by_source(source_id: str):
    """Get flows for a specific data source"""
    logger.info(f"Getting flows for source with ID: {source_id}")
    
    flows = nexla_client.flows.get_by_resource("data_sources", source_id)
    
    # Print flow details
    if hasattr(flows, "flows") and len(flows.flows) > 0:
        logger.info(f"Found {len(flows.flows)} flows for source {source_id}")
        for flow in flows.flows:
            logger.info(f"Flow ID: {flow.id}")
    else:
        logger.info(f"No flows found for source {source_id}")
    
    return flows


def get_flow_by_sink(sink_id: str):
    """Get flows for a specific data sink"""
    logger.info(f"Getting flows for sink with ID: {sink_id}")
    
    flows = nexla_client.flows.get_by_resource("data_sinks", sink_id)
    
    # Print flow details
    if hasattr(flows, "flows") and len(flows.flows) > 0:
        logger.info(f"Found {len(flows.flows)} flows for sink {sink_id}")
        for flow in flows.flows:
            logger.info(f"Flow ID: {flow.id}")
    else:
        logger.info(f"No flows found for sink {sink_id}")
    
    return flows


def get_flow_by_dataset(dataset_id: str):
    """Get flows for a specific dataset"""
    logger.info(f"Getting flows for dataset with ID: {dataset_id}")
    
    flows = nexla_client.flows.get_by_resource("data_sets", dataset_id)
    
    # Print flow details
    if hasattr(flows, "flows") and len(flows.flows) > 0:
        logger.info(f"Found {len(flows.flows)} flows for dataset {dataset_id}")
        for flow in flows.flows:
            logger.info(f"Flow ID: {flow.id}")
    else:
        logger.info(f"No flows found for dataset {dataset_id}")
    
    return flows


def activate_flow_by_source(source_id: str):
    """Activate a flow by source ID"""
    logger.info(f"Activating flow for source with ID: {source_id}")
    
    activated_flow = nexla_client.flows.activate_by_resource("data_sources", source_id)
    
    # Check status
    if hasattr(activated_flow, "flows") and len(activated_flow.flows) > 0:
        logger.info(f"Flow status after activation: {activated_flow.flows[0].status}")
        
        # Check if data_sources were included in the response
        if hasattr(activated_flow, "data_sources") and activated_flow.data_sources:
            logger.info(f"Data source status: {activated_flow.data_sources[0].status}")
    
    return activated_flow


def pause_flow_by_source(source_id: str):
    """Pause a flow by source ID"""
    logger.info(f"Pausing flow for source with ID: {source_id}")
    
    paused_flow = nexla_client.flows.pause_by_resource("data_sources", source_id)
    
    # Check status
    if hasattr(paused_flow, "flows") and len(paused_flow.flows) > 0:
        logger.info(f"Flow status after pausing: {paused_flow.flows[0].status}")
        
        # Check if data_sources were included in the response
        if hasattr(paused_flow, "data_sources") and paused_flow.data_sources:
            logger.info(f"Data source status: {paused_flow.data_sources[0].status}")
    
    return paused_flow


def delete_flow_by_source(source_id: str):
    """Delete a flow by source ID"""
    logger.info(f"Deleting flow by source with ID: {source_id}")
    
    # First check if the flow exists
    flow = nexla_client.flows.get_by_resource("data_sources", source_id)
    
    # Make sure the flow is paused first
    paused_flow = nexla_client.flows.pause_by_resource("data_sources", source_id)
    
    # Delete the flow
    delete_response = nexla_client.flows.delete_by_resource("data_sources", source_id)
    logger.info(f"Flow deletion response: {delete_response}")
    
    return delete_response


if __name__ == "__main__":
    # Run a complete flow lifecycle example
    try:
        # List flows
        flows = list_flows()
        
        if len(flows.flows) > 0:
            # Take the first flow as an example
            example_flow = flows.flows[0]
            
            # Get the flow by ID
            flow_id = example_flow.id
            get_flow(flow_id)
            
            # If the flow has a source, get flows by source
            if hasattr(example_flow, "data_source") and example_flow.data_source:
                source_id = example_flow.data_source.get("id")
                if source_id:
                    get_flow_by_source(source_id)
            
            # If the flow has sinks, get flows by sink
            if hasattr(example_flow, "data_sinks") and example_flow.data_sinks:
                sink_id = example_flow.data_sinks[0]
                get_flow_by_sink(sink_id)
        
        # For demonstration purposes, you might need actual IDs:
        # Note: Replace these IDs with actual IDs from your Nexla account
        # source_id = "your_source_id"
        # sink_id = "your_sink_id"
        # dataset_id = "your_dataset_id"
        
        # Activate, pause, and delete operations require actual IDs and should be used carefully
        # activate_flow_by_source(source_id)
        # pause_flow_by_source(source_id)
        # delete_flow_by_source(source_id)
        
        logger.info("Flow example completed successfully!")
    except Exception as e:
        logger.error(f"Error in flow example: {e}") 