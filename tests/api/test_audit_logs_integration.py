"""
Integration tests for the Audit Logs API
"""
import os
import pytest

from nexla_sdk import NexlaClient

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
    """Get resource IDs for testing audit logs"""
    # Get a source ID
    sources = client.sources.list(limit=1)
    source_id = sources.items[0].id if sources.items else None
    
    # Get a nexset ID
    nexsets = client.nexsets.list(limit=1)
    nexset_id = nexsets.items[0].id if nexsets.items else None
    
    # Get a destination ID
    destinations = client.destinations.list(limit=1)
    destination_id = destinations.items[0].id if destinations.items else None
    
    # Get a credential ID
    credentials = client.credentials.list(limit=1)
    credential_id = credentials.items[0].id if credentials.items else None
    
    # Get an organization ID
    orgs = client.organizations.list()
    org_id = orgs[0].id if orgs else None
    
    # Get a user ID
    user = client.users.get_current_user()
    user_id = user.id if user else None
    
    # Get a project ID
    projects = client.projects.list()
    project_id = projects.items[0].id if projects.items else None
    
    return {
        "source_id": source_id,
        "nexset_id": nexset_id,
        "destination_id": destination_id,
        "credential_id": credential_id,
        "org_id": org_id,
        "user_id": user_id,
        "project_id": project_id
    }

@pytest.mark.skipif(SKIP_TESTS, reason=SKIP_REASON)
class TestAuditLogs:
    """Tests for the Audit Logs API"""
    
    def test_get_source_audit_logs(self, client, resource_ids):
        """Test getting audit logs for a source"""
        if not resource_ids["source_id"]:
            pytest.skip("No source available for testing")
        
        source_id = resource_ids["source_id"]
        audit_logs = client.audit_logs.get_data_source_audit_log(source_id)
        
        assert isinstance(audit_logs, list)
        # If there are audit logs, check their structure
        if audit_logs:
            log = audit_logs[0]
            assert hasattr(log, "id")
            assert hasattr(log, "item_type")
            assert hasattr(log, "item_id")
            assert hasattr(log, "event")
            assert hasattr(log, "created_at")
    
    def test_get_nexset_audit_logs(self, client, resource_ids):
        """Test getting audit logs for a nexset"""
        if not resource_ids["nexset_id"]:
            pytest.skip("No nexset available for testing")
        
        nexset_id = resource_ids["nexset_id"]
        audit_logs = client.audit_logs.get_nexset_audit_log(nexset_id)
        
        assert isinstance(audit_logs, list)
        # If there are audit logs, check their structure
        if audit_logs:
            log = audit_logs[0]
            assert hasattr(log, "id")
            assert hasattr(log, "item_type")
            assert hasattr(log, "item_id")
            assert hasattr(log, "event")
            assert hasattr(log, "created_at")
    
    def test_get_destination_audit_logs(self, client, resource_ids):
        """Test getting audit logs for a destination"""
        if not resource_ids["destination_id"]:
            pytest.skip("No destination available for testing")
        
        destination_id = resource_ids["destination_id"]
        audit_logs = client.audit_logs.get_data_sink_audit_log(destination_id)
        
        assert isinstance(audit_logs, list)
        # If there are audit logs, check their structure
        if audit_logs:
            log = audit_logs[0]
            assert hasattr(log, "id")
            assert hasattr(log, "item_type")
            assert hasattr(log, "item_id")
            assert hasattr(log, "event")
            assert hasattr(log, "created_at")
    
    def test_get_credential_audit_logs(self, client, resource_ids):
        """Test getting audit logs for a credential"""
        if not resource_ids["credential_id"]:
            pytest.skip("No credential available for testing")
        
        credential_id = resource_ids["credential_id"]
        audit_logs = client.audit_logs.get_data_credential_audit_log(credential_id)
        
        assert isinstance(audit_logs, list)
        # If there are audit logs, check their structure
        if audit_logs:
            log = audit_logs[0]
            assert hasattr(log, "id")
            assert hasattr(log, "item_type")
            assert hasattr(log, "item_id")
            assert hasattr(log, "event")
            assert hasattr(log, "created_at")
    
    def test_get_org_audit_logs(self, client, resource_ids):
        """Test getting audit logs for an organization"""
        if not resource_ids["org_id"]:
            pytest.skip("No organization available for testing")
        
        org_id = resource_ids["org_id"]
        audit_logs = client.audit_logs.get_org_audit_log(org_id)
        
        assert isinstance(audit_logs, list)
        # If there are audit logs, check their structure
        if audit_logs:
            log = audit_logs[0]
            assert hasattr(log, "id")
            assert hasattr(log, "item_type")
            assert hasattr(log, "item_id")
            assert hasattr(log, "event")
            assert hasattr(log, "created_at")
    
    def test_get_user_audit_logs(self, client, resource_ids):
        """Test getting audit logs for a user"""
        if not resource_ids["user_id"]:
            pytest.skip("No user available for testing")
        
        user_id = resource_ids["user_id"]
        audit_logs = client.audit_logs.get_user_audit_log(user_id)
        
        assert isinstance(audit_logs, list)
        # If there are audit logs, check their structure
        if audit_logs:
            log = audit_logs[0]
            assert hasattr(log, "id")
            assert hasattr(log, "item_type")
            assert hasattr(log, "item_id")
            assert hasattr(log, "event")
            assert hasattr(log, "created_at")
    
    def test_get_project_audit_logs(self, client, resource_ids):
        """Test getting audit logs for a project"""
        if not resource_ids["project_id"]:
            pytest.skip("No project available for testing")
        
        project_id = resource_ids["project_id"]
        audit_logs = client.audit_logs.get_project_audit_log(project_id)
        
        assert isinstance(audit_logs, list)
        # If there are audit logs, check their structure
        if audit_logs:
            log = audit_logs[0]
            assert hasattr(log, "id")
            assert hasattr(log, "item_type")
            assert hasattr(log, "item_id")
            assert hasattr(log, "event")
            assert hasattr(log, "created_at") 