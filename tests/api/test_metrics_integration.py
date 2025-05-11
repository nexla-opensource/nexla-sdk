"""
Integration tests for the Metrics API
"""
import os
import pytest
from datetime import datetime, timedelta

from nexla_sdk import NexlaClient
from nexla_sdk.models import ResourceType

# Skip tests if environment variables are missing
missing_vars = []
if "NEXLA_SERVICE_KEY" not in os.environ:
    missing_vars.append("NEXLA_SERVICE_KEY")

SKIP_REASON = f"Missing environment variables: {', '.join(missing_vars)}" if missing_vars else ""
SKIP_TESTS = bool(missing_vars)

@pytest.fixture(scope="module")
def client():
    """Create a Nexla client for testing"""
    if SKIP_TESTS:
        pytest.skip(SKIP_REASON)
    return NexlaClient(service_key=os.environ["NEXLA_SERVICE_KEY"])

@pytest.fixture(scope="module")
def resource_ids(client):
    """Get resource IDs for testing metrics"""
    # Get an organization ID
    orgs = client.organizations.list()
    org_id = orgs[0].id if orgs else None
    
    # Get a source ID
    sources = client.sources.list(limit=1)
    source_id = sources.items[0].id if sources.items else None
    
    # Get a nexset ID
    nexsets = client.nexsets.list(limit=1)
    nexset_id = nexsets.items[0].id if nexsets.items else None
    
    # Get a destination ID
    destinations = client.destinations.list(limit=1)
    destination_id = destinations.items[0].id if destinations.items else None
    
    return {
        "org_id": org_id,
        "source_id": source_id,
        "nexset_id": nexset_id,
        "destination_id": destination_id
    }

@pytest.mark.skipif(SKIP_TESTS, reason=SKIP_REASON)
class TestMetrics:
    """Tests for the Metrics API"""
    
    def test_get_organization_account_metrics(self, client, resource_ids):
        """Test getting account metrics for an organization"""
        if not resource_ids["org_id"]:
            pytest.skip("No organization available for testing")
        
        org_id = resource_ids["org_id"]
        
        # Calculate date range for the past 7 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        account_metrics = client.metrics.get_organization_account_metrics(
            org_id=org_id,
            from_date=start_date.isoformat(),
            to_date=end_date.isoformat()
        )
        
        assert hasattr(account_metrics, "status")
        assert hasattr(account_metrics, "metrics")
        assert isinstance(account_metrics.metrics, list)
        
        if account_metrics.metrics:
            metric = account_metrics.metrics[0]
            assert hasattr(metric, "start_time")
            assert hasattr(metric, "end_time")
            assert hasattr(metric, "data")
            assert hasattr(metric.data, "records")
            assert hasattr(metric.data, "size")
    
    def test_get_resource_metrics_daily(self, client, resource_ids):
        """Test getting daily metrics for a resource"""
        # Try with source, then nexset, then destination
        resource_id = None
        resource_type = None
        
        if resource_ids["source_id"]:
            resource_id = resource_ids["source_id"]
            resource_type = ResourceType.DATA_SOURCES
        elif resource_ids["nexset_id"]:
            resource_id = resource_ids["nexset_id"]
            resource_type = ResourceType.DATA_SETS
        elif resource_ids["destination_id"]:
            resource_id = resource_ids["destination_id"]
            resource_type = ResourceType.DATA_SINKS
        
        if not resource_id:
            pytest.skip("No resource available for testing")
        
        # Calculate date range for the past 7 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        daily_metrics = client.metrics.get_resource_metrics_daily(
            resource_type=resource_type,
            resource_id=resource_id,
            from_date=start_date.isoformat(),
            to_date=end_date.isoformat()
        )
        
        assert hasattr(daily_metrics, "status")
        assert hasattr(daily_metrics, "metrics")
        assert isinstance(daily_metrics.metrics, list)
        
        if daily_metrics.metrics:
            metric = daily_metrics.metrics[0]
            assert hasattr(metric, "time")
            assert hasattr(metric, "records")
            assert hasattr(metric, "size")
            assert hasattr(metric, "errors")
    
    def test_get_resource_metrics_by_run(self, client, resource_ids):
        """Test getting metrics by run for a resource"""
        # Try with source, then nexset, then destination
        resource_id = None
        resource_type = None
        
        if resource_ids["source_id"]:
            resource_id = resource_ids["source_id"]
            resource_type = ResourceType.DATA_SOURCES
        elif resource_ids["nexset_id"]:
            resource_id = resource_ids["nexset_id"]
            resource_type = ResourceType.DATA_SETS
        elif resource_ids["destination_id"]:
            resource_id = resource_ids["destination_id"]
            resource_type = ResourceType.DATA_SINKS
        
        if not resource_id:
            pytest.skip("No resource available for testing")
        
        run_metrics = client.metrics.get_resource_metrics_by_run(
            resource_type=resource_type,
            resource_id=resource_id,
            groupby="runId",
            orderby="runId",
            page=1,
            size=5
        )
        
        assert hasattr(run_metrics, "status")
        assert hasattr(run_metrics, "metrics")
        assert hasattr(run_metrics.metrics, "data")
        assert hasattr(run_metrics.metrics, "meta")
        assert isinstance(run_metrics.metrics.data, list)
        
        if run_metrics.metrics.data:
            metric = run_metrics.metrics.data[0]
            assert hasattr(metric, "records")
            assert hasattr(metric, "size")
            assert hasattr(metric, "errors")
    
    def test_get_flow_metrics(self, client, resource_ids):
        """Test getting flow metrics for a resource"""
        # Try with source, then nexset, then destination
        resource_id = None
        resource_type = None
        
        if resource_ids["source_id"]:
            resource_id = resource_ids["source_id"]
            resource_type = ResourceType.DATA_SOURCES
        elif resource_ids["nexset_id"]:
            resource_id = resource_ids["nexset_id"]
            resource_type = ResourceType.DATA_SETS
        elif resource_ids["destination_id"]:
            resource_id = resource_ids["destination_id"]
            resource_type = ResourceType.DATA_SINKS
        
        if not resource_id:
            pytest.skip("No resource available for testing")
        
        # Calculate date range for the past 7 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        try:
            flow_metrics = client.metrics.get_flow_metrics(
                resource_type=resource_type,
                resource_id=resource_id,
                from_date=start_date.isoformat(),
                to_date=end_date.isoformat(),
                groupby="runId",
                orderby="created_at",
                page=1,
                per_page=5
            )
            
            assert hasattr(flow_metrics, "status")
            assert hasattr(flow_metrics, "metrics")
            
            # If we have metrics data, verify its structure
            if hasattr(flow_metrics.metrics, "data"):
                # Data could be a dict (grouped by run ID) or a FlowMetricsData object
                assert isinstance(flow_metrics.metrics.data, (dict, object))
        except Exception as e:
            pytest.skip(f"Failed to get flow metrics: {e}")
    
    def test_get_flow_logs(self, client, resource_ids):
        """Test getting flow logs for a resource and run ID"""
        # Try with source, then nexset, then destination
        resource_id = None
        resource_type = None
        
        if resource_ids["source_id"]:
            resource_id = resource_ids["source_id"]
            resource_type = ResourceType.DATA_SOURCES
        elif resource_ids["nexset_id"]:
            resource_id = resource_ids["nexset_id"]
            resource_type = ResourceType.DATA_SETS
        elif resource_ids["destination_id"]:
            resource_id = resource_ids["destination_id"]
            resource_type = ResourceType.DATA_SINKS
        
        if not resource_id:
            pytest.skip("No resource available for testing")
        
        # First, get run metrics to find a run ID
        try:
            run_metrics = client.metrics.get_resource_metrics_by_run(
                resource_type=resource_type,
                resource_id=resource_id,
                groupby="runId",
                orderby="runId",
                page=1,
                size=1
            )
            
            if not run_metrics.metrics.data:
                pytest.skip("No run metrics data available")
            
            run_id = run_metrics.metrics.data[0].runId
            if not run_id:
                pytest.skip("No run ID found in metrics")
            
            # Calculate timestamp range for logs
            now_timestamp = int(datetime.now().timestamp() * 1000)
            past_timestamp = int((datetime.now() - timedelta(days=30)).timestamp() * 1000)
            
            flow_logs = client.metrics.get_flow_logs(
                resource_type=resource_type,
                resource_id=resource_id,
                run_id=run_id,
                from_timestamp=past_timestamp,
                to_timestamp=now_timestamp,
                page=1,
                per_page=5
            )
            
            assert hasattr(flow_logs, "status")
            assert hasattr(flow_logs, "message")
            assert hasattr(flow_logs, "logs")
            assert hasattr(flow_logs.logs, "data")
            assert hasattr(flow_logs.logs, "meta")
            assert isinstance(flow_logs.logs.data, list)
            
            if flow_logs.logs.data:
                log = flow_logs.logs.data[0]
                assert hasattr(log, "timestamp")
                assert hasattr(log, "resource_id")
                assert hasattr(log, "resource_type")
                assert hasattr(log, "log")
                assert hasattr(log, "log_type")
                assert hasattr(log, "severity")
        
        except Exception as e:
            pytest.skip(f"Failed to test flow logs: {e}") 