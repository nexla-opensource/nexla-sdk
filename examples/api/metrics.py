"""
Example usage of the Metrics API
"""
from datetime import datetime, timedelta
from pprint import pprint

from nexla_sdk.models import ResourceType

from client import nexla_client

def run_metrics_examples():
    """Run through examples of using the Metrics API"""
    client = nexla_client
    
    # Get organization for metrics
    print("\n=== Getting organization for metrics ===")
    orgs = client.organizations.list()
    if not orgs:
        print("No organizations found for metrics")
        return
    
    org_id = orgs[0].id
    print(f"Using organization ID: {org_id}")
    
    # Get account metrics for the organization
    print(f"\n=== Getting account metrics for organization {org_id} ===")
    # Calculate date range for the past 7 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    
    try:
        account_metrics = client.metrics.get_organization_account_metrics(
            org_id=org_id,
            from_date=start_date.isoformat(),
            to_date=end_date.isoformat()
        )
        
        print(f"Status: {account_metrics.status}")
        print(f"Found {len(account_metrics.metrics)} metrics periods")
        
        if account_metrics.metrics:
            metric = account_metrics.metrics[0]
            print("\n=== Sample Account Metric ===")
            print(f"Start time: {metric.start_time}")
            print(f"End time: {metric.end_time}")
            print(f"Records processed: {metric.data.records}")
            print(f"Data size processed: {metric.data.size} bytes")
    except Exception as e:
        print(f"Failed to get account metrics: {e}")
    
    # Get a source for resource metrics
    print("\n=== Getting a source for resource metrics ===")
    sources = client.sources.list(limit=1)
    if not sources.items:
        print("No sources found for resource metrics")
        return
    
    source_id = sources.items[0].id
    print(f"Using source ID: {source_id}")
    
    # Get daily metrics for the source
    print(f"\n=== Getting daily metrics for source {source_id} ===")
    try:
        daily_metrics = client.metrics.get_resource_metrics_daily(
            resource_type=ResourceType.DATA_SOURCES,
            resource_id=source_id,
            from_date=start_date.isoformat(),
            to_date=end_date.isoformat()
        )
        
        print(f"Status: {daily_metrics.status}")
        print(f"Found {len(daily_metrics.metrics)} daily metrics")
        
        if daily_metrics.metrics:
            metric = daily_metrics.metrics[0]
            print("\n=== Sample Daily Metric ===")
            print(f"Date: {metric.time}")
            print(f"Records processed: {metric.records}")
            print(f"Data size processed: {metric.size} bytes")
            print(f"Errors: {metric.errors}")
    except Exception as e:
        print(f"Failed to get daily metrics: {e}")
    
    # Get run metrics for the source
    print(f"\n=== Getting run metrics for source {source_id} ===")
    try:
        run_metrics = client.metrics.get_resource_metrics_by_run(
            resource_type=ResourceType.DATA_SOURCES,
            resource_id=source_id,
            groupby="runId",
            orderby="runId",
            page=1,
            size=5
        )
        
        print(f"Status: {run_metrics.status}")
        print(f"Total runs: {run_metrics.metrics.meta.totalCount}")
        print(f"Current page: {run_metrics.metrics.meta.currentPage}")
        print(f"Found {len(run_metrics.metrics.data)} run metrics on this page")
        
        if run_metrics.metrics.data:
            metric = run_metrics.metrics.data[0]
            print("\n=== Sample Run Metric ===")
            print(f"Run ID: {metric.runId}")
            print(f"Records processed: {metric.records}")
            print(f"Data size processed: {metric.size} bytes")
            print(f"Errors: {metric.errors}")
            
            # If there's a valid run ID, get flow logs for it
            if metric.runId:
                run_id = metric.runId
                print(f"\n=== Getting flow logs for run ID {run_id} ===")
                try:
                    # Calculate timestamp range for logs
                    now_timestamp = int(datetime.now().timestamp() * 1000)
                    past_timestamp = int((datetime.now() - timedelta(days=30)).timestamp() * 1000)
                    
                    flow_logs = client.metrics.get_flow_logs(
                        resource_type=ResourceType.DATA_SOURCES,
                        resource_id=source_id,
                        run_id=run_id,
                        from_timestamp=past_timestamp,
                        to_timestamp=now_timestamp,
                        page=1,
                        per_page=5
                    )
                    
                    print(f"Status: {flow_logs.status}")
                    print(f"Message: {flow_logs.message}")
                    print(f"Total logs: {flow_logs.logs.meta.total_count}")
                    print(f"Current page: {flow_logs.logs.meta.current_page}")
                    print(f"Found {len(flow_logs.logs.data)} log entries on this page")
                    
                    if flow_logs.logs.data:
                        log = flow_logs.logs.data[0]
                        print("\n=== Sample Flow Log ===")
                        print(f"Timestamp: {datetime.fromtimestamp(log.timestamp/1000)}")
                        print(f"Resource ID: {log.resource_id}")
                        print(f"Resource Type: {log.resource_type}")
                        print(f"Severity: {log.severity}")
                        print(f"Log Type: {log.log_type}")
                        print(f"Log: {log.log[:100]}...")  # Truncate long log messages
                except Exception as e:
                    print(f"Failed to get flow logs: {e}")
    except Exception as e:
        print(f"Failed to get run metrics: {e}")
    
    # Get flow metrics for the source
    print(f"\n=== Getting flow metrics for source {source_id} ===")
    try:
        flow_metrics = client.metrics.get_flow_metrics(
            resource_type=ResourceType.DATA_SOURCES,
            resource_id=source_id,
            from_date=start_date.isoformat(),
            to_date=end_date.isoformat(),
            groupby="runId",
            orderby="created_at",
            page=1,
            per_page=5
        )
        
        print(f"Status: {flow_metrics.status}")
        if hasattr(flow_metrics.metrics, 'meta') and flow_metrics.metrics.meta:
            print(f"Total flows: {flow_metrics.metrics.meta.totalCount}")
            print(f"Current page: {flow_metrics.metrics.meta.currentPage}")
        
        print("\n=== Flow Metrics Structure ===")
        if hasattr(flow_metrics.metrics, 'data'):
            if isinstance(flow_metrics.metrics.data, dict):
                print(f"Flow metrics grouped by run IDs: {list(flow_metrics.metrics.data.keys())}")
            else:
                print("Flow metrics not grouped by run IDs")
                
                # Check sources in flow
                if hasattr(flow_metrics.metrics.data, 'data_sources') and flow_metrics.metrics.data.data_sources:
                    print(f"Data sources in flow: {len(flow_metrics.metrics.data.data_sources)}")
                    
                # Check datasets in flow
                if hasattr(flow_metrics.metrics.data, 'data_sets') and flow_metrics.metrics.data.data_sets:
                    print(f"Data sets in flow: {len(flow_metrics.metrics.data.data_sets)}")
                    
                # Check destinations in flow
                if hasattr(flow_metrics.metrics.data, 'data_sinks') and flow_metrics.metrics.data.data_sinks:
                    print(f"Data sinks in flow: {len(flow_metrics.metrics.data.data_sinks)}")
    except Exception as e:
        print(f"Failed to get flow metrics: {e}")

if __name__ == "__main__":
    run_metrics_examples() 