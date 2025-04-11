"""
Basic usage example for the Nexla SDK.

This example demonstrates how to:
1. Initialize the client
2. List available flows
3. Work with sources and destinations
4. Manage credentials
5. Work with transforms and nexsets
6. Explore metrics and notifications
7. Work with audit logs and access controls
"""

import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

from nexla_sdk import NexlaClient
from pprint import pprint

load_dotenv()

def main():
    # Initialize the client with your API key
    # You can specify a custom API endpoint if needed
    api_url = os.getenv("NEXLA_API_URL", "https://dataops.nexla.io/nexla-api")
    client = NexlaClient(
        api_key=os.getenv("NEXLA_TOKEN"), 
        api_url=api_url,
        api_version="v1"  # Specify API version
    )

    # List Flows
    print("\n=== Listing Flows ===")
    flows = client.flows.list(limit=5)
    pprint(flows)

    # List Sources
    print("\n=== Listing Sources ===")
    sources = client.sources.list(limit=5)
    pprint(sources)

    # List Destinations
    print("\n=== Listing Destinations ===")
    destinations = client.destinations.list(limit=5)
    pprint(destinations)

    # List Transforms
    print("\n=== Listing Transforms ===")
    transforms = client.transforms.list(limit=5)
    pprint(transforms)

    # List Nexsets
    print("\n=== Listing Nexsets ===")
    nexsets = client.nexsets.list(limit=5)
    pprint(nexsets)

    # Example: Creating a new flow
    flow_data = {
        "name": "Example Flow",
        "description": "A simple example flow",
        # Add other required flow configuration here
    }
    
    try:
        new_flow = client.flows.create(flow_data)
        print("\n=== Created New Flow ===")
        pprint(new_flow)
        
        # Get metrics for the new flow
        end_time = datetime.now()
        start_time = end_time - timedelta(days=7)
        
        print("\n=== Flow Metrics ===")
        metrics = client.metrics.get_flow_metrics(
            flow_id=new_flow.id,
            start_time=start_time,
            end_time=end_time
        )
        pprint(metrics)
        
        # Get audit logs for the flow
        print("\n=== Flow Audit Logs ===")
        audit_logs = client.audit_logs.get_resource_history(
            resource_type="flows",
            resource_id=new_flow.id,
            start_time=start_time,
            end_time=end_time
        )
        pprint(audit_logs)
        
    except Exception as e:
        print(f"Error creating flow: {e}")

    # Example: Working with credentials
    print("\n=== Listing Credentials ===")
    credentials = client.credentials.list()
    pprint(credentials)
    
    # Example: Working with notifications
    print("\n=== Listing Notifications ===")
    try:
        notifications = client.notifications.list(limit=5)
        pprint(notifications)
        
        # Get unread count
        unread_count = client.notifications.get_unread_count()
        print(f"Unread notifications: {unread_count}")
        
        # Get notification settings
        settings = client.notifications.get_settings()
        pprint(settings)
    except Exception as e:
        print(f"Error accessing notifications: {e}")
    
    # Example: Working with metrics
    print("\n=== Listing Metrics ===")
    try:
        end_time = datetime.now()
        start_time = end_time - timedelta(days=7)
        
        metrics = client.metrics.list(
            start_time=start_time,
            end_time=end_time,
            limit=5
        )
        pprint(metrics)
    except Exception as e:
        print(f"Error accessing metrics: {e}")
    
    # Example: Access controls
    if len(flows.flows) > 0:
        flow_id = flows.flows[0].id
        print(f"\n=== Listing Access Controls for Flow {flow_id} ===")
        try:
            access_controls = client.access_control.list("flows", flow_id)
            pprint(access_controls)
            
            # List available permissions
            permissions = client.access_control.list_available_permissions("flows")
            print("\n=== Available Flow Permissions ===")
            pprint(permissions)
        except Exception as e:
            print(f"Error accessing access controls: {e}")

if __name__ == "__main__":
    main()
