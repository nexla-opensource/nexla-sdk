import os
from nexla_sdk import NexlaClient
from nexla_sdk.models.credentials.requests import CredentialCreate
from nexla_sdk.models.sources.requests import SourceCreate
from nexla_sdk.models.nexsets.requests import NexsetCreate
from nexla_sdk.models.destinations.requests import DestinationCreate


def main():
    # Initialize client
    client = NexlaClient(
        api_key=os.getenv("NEXLA_API_KEY"),
        base_url="https://dataops.nexla.com/nexla-api"
    )
    
    # Example 1: List all sources
    print("=== Listing Sources ===")
    sources = client.sources.list()
    for source in sources:
        print(f"Source: {source.name} ({source.id}) - Status: {source.status}")
    
    # Example 2: Create a credential
    print("\n=== Creating Credential ===")
    credential = client.credentials.create(CredentialCreate(
        name="My S3 Bucket",
        credentials_type="s3",
        credentials={
            "access_key_id": "your_access_key",
            "secret_access_key": "your_secret_key",
            "region": "us-east-1"
        }
    ))
    print(f"Created credential: {credential.name} ({credential.id})")
    
    # Example 3: Create a source
    print("\n=== Creating Source ===")
    source = client.sources.create(SourceCreate(
        name="My S3 Source",
        source_type="s3",
        data_credentials_id=credential.id,
        source_config={
            "path": "my-bucket/data/",
            "file_format": "json",
            "start.cron": "0 0 * * * ?"  # Daily at midnight
        }
    ))
    print(f"Created source: {source.name} ({source.id})")
    
    # Example 4: Get detected nexsets
    print("\n=== Detected Nexsets ===")
    nexsets = client.nexsets.list()
    source_nexsets = [n for n in nexsets if n.data_source_id == source.id]
    for nexset in source_nexsets:
        print(f"Nexset: {nexset.name} ({nexset.id})")
    
    # Example 5: Create a transformed nexset
    if source_nexsets:
        parent_nexset = source_nexsets[0]
        print(f"\n=== Creating Transformed Nexset from {parent_nexset.name} ===")
        
        transformed = client.nexsets.create(NexsetCreate(
            name="Transformed Data",
            parent_data_set_id=parent_nexset.id,
            has_custom_transform=True,
            transform={
                "version": 1,
                "operations": [{
                    "operation": "shift",
                    "spec": {
                        "*": "&"  # Pass through all fields
                    }
                }]
            }
        ))
        print(f"Created nexset: {transformed.name} ({transformed.id})")
        
        # Example 6: Create a destination
        print("\n=== Creating Destination ===")
        destination = client.destinations.create(DestinationCreate(
            name="My S3 Output",
            sink_type="s3",
            data_credentials_id=credential.id,
            data_set_id=transformed.id,
            sink_config={
                "path": "my-bucket/output/",
                "file_format": "parquet",
                "file_compression": "snappy"
            }
        ))
        print(f"Created destination: {destination.name} ({destination.id})")
    
    # Example 7: View flow
    print("\n=== Flow Structure ===")
    flows = client.flows.list(flows_only=True)
    if flows:
        flow = flows[0]
        print(f"Flow has {len(flow.flows)} nodes")
    
    # Example 8: Pagination example
    print("\n=== Pagination Example ===")
    paginator = client.sources.paginate(per_page=10)
    
    # Iterate through all items
    for source in paginator:
        print(f"Source: {source.name}")
    
    # Or iterate by pages
    for page in paginator.iter_pages():
        print(f"Page {page.page_info.current_page}: {len(page.items)} items")
    
    # Example 9: Error handling
    print("\n=== Error Handling Example ===")
    try:
        client.sources.get(999999)  # Non-existent ID
    except Exception as e:
        print(f"Expected error: {type(e).__name__}: {e}")
    
    # Example 10: Access control
    print("\n=== Access Control Example ===")
    if source_nexsets:
        nexset = source_nexsets[0]
        
        # Get current accessors
        accessors = client.nexsets.get_accessors(nexset.id)
        print(f"Current accessors: {len(accessors)}")
        
        # Add a user accessor
        new_accessors = [{
            "type": "USER",
            "email": "colleague@example.com",
            "access_roles": ["collaborator"]
        }]
        
        updated = client.nexsets.add_accessors(nexset.id, new_accessors)
        print(f"Updated accessors: {len(updated)}")
    
    # Example 11: Metrics
    print("\n=== Metrics Example ===")
    from datetime import datetime, timedelta
    
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    today = datetime.now().strftime("%Y-%m-%d")
    
    if sources:
        source = sources[0]
        metrics = client.metrics.get_resource_daily_metrics(
            resource_type="data_sources",
            resource_id=source.id,
            from_date=yesterday,
            to_date=today
        )
        print(f"Metrics status: {metrics.status}")
        if metrics.metrics:
            for metric in metrics.metrics:
                print(f"  {metric}")


if __name__ == "__main__":
    main()
