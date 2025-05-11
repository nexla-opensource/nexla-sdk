"""
Example usage of the Audit Logs API
"""
from client import nexla_client

def run_audit_logs_examples():
    """Run through examples of using the Audit Logs API"""
    client = nexla_client
    
    # First, get a resource ID to use for audit logs
    print("\n=== Getting a source to check audit logs ===")
    sources = client.sources.list(limit=1)
    if not sources.items:
        print("No sources found to check audit logs")
        return
    
    source_id = sources.items[0].id
    print(f"Using source ID: {source_id}")
    
    # Get audit logs for a source
    print(f"\n=== Getting audit logs for source {source_id} ===")
    source_audit_logs = client.audit_logs.get_data_source_audit_log(source_id)
    print(f"Found {len(source_audit_logs)} audit log entries for source {source_id}")
    
    # If there are audit logs, print details of the first one
    if source_audit_logs:
        log_entry = source_audit_logs[0]
        print("\n=== Sample audit log entry ===")
        print(f"ID: {log_entry.id}")
        print(f"Event: {log_entry.event}")
        print(f"Item type: {log_entry.item_type}")
        print(f"Created at: {log_entry.created_at}")
        
        if log_entry.object_changes:
            print("\nChanges:")
            for key, values in log_entry.object_changes.items():
                if isinstance(values, list) and len(values) == 2:
                    print(f"  {key}: {values[0]} -> {values[1]}")
    
    # Get audit logs for a Nexset
    print("\n=== Getting Nexsets to check audit logs ===")
    nexsets = client.nexsets.list(limit=1)
    if nexsets.items:
        nexset_id = nexsets.items[0].id
        print(f"Using Nexset ID: {nexset_id}")
        
        print(f"\n=== Getting audit logs for Nexset {nexset_id} ===")
        nexset_audit_logs = client.audit_logs.get_nexset_audit_log(nexset_id)
        print(f"Found {len(nexset_audit_logs)} audit log entries for Nexset {nexset_id}")
    
    # Get audit logs for a destination
    print("\n=== Getting destinations to check audit logs ===")
    destinations = client.destinations.list(limit=1)
    if destinations.items:
        destination_id = destinations.items[0].id
        print(f"Using destination ID: {destination_id}")
        
        print(f"\n=== Getting audit logs for destination {destination_id} ===")
        destination_audit_logs = client.audit_logs.get_data_sink_audit_log(destination_id)
        print(f"Found {len(destination_audit_logs)} audit log entries for destination {destination_id}")
    
    # Get audit logs for an organization
    print("\n=== Getting organizations to check audit logs ===")
    orgs = client.organizations.list()
    if orgs:
        org_id = orgs[0].id
        print(f"Using organization ID: {org_id}")
        
        print(f"\n=== Getting audit logs for organization {org_id} ===")
        org_audit_logs = client.audit_logs.get_org_audit_log(org_id)
        print(f"Found {len(org_audit_logs)} audit log entries for organization {org_id}")
    
    # Get audit logs for a credential
    print("\n=== Getting credentials to check audit logs ===")
    credentials = client.credentials.list()
    if credentials.items:
        credential_id = credentials.items[0].id
        print(f"Using credential ID: {credential_id}")
        
        print(f"\n=== Getting audit logs for credential {credential_id} ===")
        credential_audit_logs = client.audit_logs.get_data_credential_audit_log(credential_id)
        print(f"Found {len(credential_audit_logs)} audit log entries for credential {credential_id}")
    
    # Get audit logs for a project
    print("\n=== Getting projects to check audit logs ===")
    projects = client.projects.list()
    if projects.items:
        project_id = projects.items[0].id
        print(f"Using project ID: {project_id}")
        
        print(f"\n=== Getting audit logs for project {project_id} ===")
        project_audit_logs = client.audit_logs.get_project_audit_log(project_id)
        print(f"Found {len(project_audit_logs)} audit log entries for project {project_id}")

if __name__ == "__main__":
    run_audit_logs_examples() 