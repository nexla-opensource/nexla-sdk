#!/usr/bin/env python
"""
Basic usage example for the Nexla SDK
"""
import os
import sys
import json
from pprint import pprint

# Add the parent directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from nexla_sdk import NexlaClient
from nexla_sdk.exceptions import NexlaAPIError, NexlaAuthError, NexlaValidationError
from nexla_sdk.models.flows import Flow
from nexla_sdk.models.sources import Source
from nexla_sdk.models.destinations import Destination


def main():
    # Replace with your actual token or set as environment variable
    token = os.environ.get("NEXLA_TOKEN")
    
    if not token:
        print("Please set the NEXLA_TOKEN environment variable.")
        sys.exit(1)
    
    # Initialize the client
    client = NexlaClient(token=token)
    
    try:
        # Get current user info
        print("Getting current user...")
        user = client.users.get_current()
        print(f"Logged in as: {user.get('email', 'Unknown')}")
        print("")
        
        # List flows
        print("Listing flows...")
        flows = client.flows.list(limit=5)
        print(f"Found {flows.total} flows.")
        
        if flows.items:
            print("First 5 flows:")
            for flow in flows.items:
                print(f"  - {flow.name} (ID: {flow.id})")
                # Access other Flow model properties
                if flow.config.is_active:
                    print(f"    Status: Active")
                else:
                    print(f"    Status: Inactive")
        print("")
        
        # List data sources
        print("Listing data sources...")
        sources = client.sources.list(limit=5)
        print(f"Found {sources.total} data sources.")
        
        if sources.items:
            print("First 5 data sources:")
            for source in sources.items:
                print(f"  - {source.name} (ID: {source.id})")
                # Access Source model properties
                print(f"    Connector type: {source.config.connector_type}")
        print("")
        
        # List data sinks (destinations)
        print("Listing data sinks (destinations)...")
        sinks = client.destinations.list(limit=5)
        print(f"Found {sinks.total} data sinks.")
        
        if sinks.items:
            print("First 5 data sinks:")
            for sink in sinks.items:
                print(f"  - {sink.name} (ID: {sink.id})")
                # Access Destination model properties
                print(f"    Connector type: {sink.config.connector_type}")
        print("")
        
        # Example of creating a source
        if False:  # Set to True to run this example
            new_source_data = {
                "name": "Example S3 Source",
                "description": "Created via SDK",
                "config": {
                    "connector_type": "s3",
                    "credential_id": "your_credential_id",
                    "options": {
                        "bucket": "example-bucket",
                        "path": "path/to/data",
                        "file_pattern": "*.csv"
                    },
                    "format_options": {
                        "format": "csv",
                        "delimiter": ","
                    }
                }
            }
            
            new_source = client.sources.create(new_source_data)
            print("Created new source:")
            print(f"ID: {new_source.id}")
            print(f"Name: {new_source.name}")
        
    except NexlaAuthError:
        print("Authentication failed. Please check your token.")
        sys.exit(1)
    except NexlaAPIError as e:
        print(f"API error: {str(e)}")
        if hasattr(e, "status_code"):
            print(f"Status code: {e.status_code}")
        sys.exit(1)
    except NexlaValidationError as e:
        print(f"Validation error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main() 