# Nexla Python SDK

A Python SDK for interacting with the Nexla API.

## Installation

```bash
pip install nexla-sdk
```

## Authentication

The Nexla SDK requires a Service Key for authentication. You can create a service key from the Nexla UI:

1. Go to your Nexla UI instance (e.g., `https://dataops.nexla.io`)
2. Navigate to the **Authentication** screen in the **Settings** section
3. Click the **Create Service Key** button
4. Store the service key securely - it should be treated as highly sensitive since it is equivalent to your account password

## Quick Start

```python
from nexla_sdk import NexlaClient

# Initialize the client with your service key
client = NexlaClient(service_key="your_nexla_service_key")

# List flows - returns a FlowResponse object with flows
flows = client.flows.list()
for flow_response in flows:
    for flow in flow_response.flows:
        print(f"Flow name: {flow.name}, ID: {flow.id}")

# List sources - returns a list of Source objects
sources = client.sources.list()
for source in sources:
    print(f"Source name: {source.name}, ID: {source.id}")

# Get a specific source - returns a Source object
source = client.sources.get(source_id)
print(f"Source details: {source.name}, type: {source.source_type}")

# Create a credential
credential_data = {
    "name": "My S3 Credential",
    "credentials_type": "s3",
    "credentials": {
        "access_key_id": "your_access_key",
        "secret_access_key": "your_secret_key", 
        "region": "us-east-1"
    }
}
credential = client.credentials.create(credential_data)
print(f"Created credential: {credential.id}")

# Create a data source
source_data = {
    "name": "My New Source",
    "description": "Created via SDK",
    "source_type": "s3",
    "data_credentials_id": credential.id,
    "source_config": {
        "path": "bucket/path/",
        "file_format": "json"
    }
}
new_source = client.sources.create(source_data)
print(f"Created source: {new_source.id}, name: {new_source.name}")
```

## Authentication Methods

The SDK supports two authentication methods:

### 1. Service Key Authentication (Recommended)

Service keys are long-lived credentials that automatically obtain and refresh session tokens:

```python
client = NexlaClient(service_key="your_service_key")

# Or use environment variable
# export NEXLA_SERVICE_KEY="your_service_key"
client = NexlaClient()
```

### 2. Direct Access Token Authentication

For temporary access using pre-obtained tokens:

```python
client = NexlaClient(access_token="your_access_token")

# Or use environment variable
# export NEXLA_ACCESS_TOKEN="your_access_token"
client = NexlaClient()
```

## Core Resources

### Credentials

```python
# Create a credential
credential_data = {
    "name": "My S3 Credential",
    "credentials_type": "s3",
    "credentials": {
        "access_key_id": "xxx",
        "secret_access_key": "xxx",
        "region": "us-east-1"
    }
}
credential = client.credentials.create(credential_data)

# Test credential
probe_result = client.credentials.probe(credential.id)
print(f"Credential valid: {probe_result.get('success', False)}")

# Get credential tree structure
from nexla_sdk.models.credentials.requests import ProbeTreeRequest
tree_request = ProbeTreeRequest(path="/")
tree = client.credentials.probe_tree(credential.id, tree_request)

# Get sample data
from nexla_sdk.models.credentials.requests import ProbeSampleRequest
sample_request = ProbeSampleRequest(path="/data/file.json")
sample = client.credentials.probe_sample(credential.id, sample_request)
```

### Sources

```python
# Create a source
source_data = {
    "name": "My Data Source",
    "source_type": "s3",
    "data_credentials_id": credential.id,
    "source_config": {
        "path": "bucket/path/",
        "file_format": "json"
    }
}
source = client.sources.create(source_data)

# Activate source
activated_source = client.sources.activate(source.id)

# Copy source
from nexla_sdk.models.sources.requests import SourceCopyOptions
copy_options = SourceCopyOptions(new_name="Copied Source")
copied_source = client.sources.copy(source.id, copy_options)
```

### Nexsets (Data Sets)

```python
# List nexsets
nexsets = client.nexsets.list()

# Get samples from a nexset
samples = client.nexsets.get_samples(
    set_id=nexset.id,
    count=10,
    include_metadata=True
)

# Create a transformed nexset
nexset_data = {
    "name": "Transformed Data",
    "parent_data_set_id": parent_nexset.id,
    "has_custom_transform": True,
    "transform": {
        "version": 1,
        "operations": [...]
    }
}
transformed = client.nexsets.create(nexset_data)
```

### Destinations

```python
# Create a destination
destination_data = {
    "name": "My Output",
    "sink_type": "s3",
    "data_credentials_id": credential.id,
    "data_set_id": nexset.id,
    "sink_config": {
        "path": "output/path/",
        "file_format": "parquet"
    }
}
destination = client.destinations.create(destination_data)

# Activate destination
activated_destination = client.destinations.activate(destination.id)
```

### Flows

```python
# Get flow by resource
flow = client.flows.get_by_resource(
    resource_type="data_sources",
    resource_id=source.id
)

# Activate entire flow
client.flows.activate(flow.flows[0].id, all=True)

# Pause flow
client.flows.pause(flow.flows[0].id, all=True)

# Copy flow
from nexla_sdk.models.flows.requests import FlowCopyOptions
copy_options = FlowCopyOptions(new_name="Copied Flow")
copied_flow = client.flows.copy(flow.flows[0].id, copy_options)
```

## Pagination

The SDK provides built-in pagination support:

```python
# Get a paginator
paginator = client.sources.paginate(per_page=20)

# Iterate through all items
for source in paginator:
    print(source.name)

# Or iterate by pages
for page in paginator.iter_pages():
    print(f"Page {page.page_info.current_page}")
    for source in page:
        print(f"  - {source.name}")
```

## Access Control

Manage access to resources:

```python
# Get current access rules
accessors = client.sources.get_accessors(source.id)

# Add user access
new_accessors = [{
    "type": "USER",
    "email": "user@example.com", 
    "access_roles": ["collaborator"]
}]
client.sources.add_accessors(source.id, new_accessors)

# Add team access
team_accessor = [{
    "type": "TEAM",
    "id": team_id,
    "access_roles": ["operator"]
}]
client.sources.add_accessors(source.id, team_accessor)

# Replace all accessors
client.sources.replace_accessors(source.id, new_accessors)
```

## Organizations and Teams

```python
# List organizations
orgs = client.organizations.list()

# Get organization members
members = client.organizations.get_members(org.id)

# Update organization members
from nexla_sdk.models.organizations.requests import OrgMemberList
member_list = OrgMemberList(members=[
    {"email": "new@example.com", "access_role": ["admin"]}
])
client.organizations.update_members(org.id, member_list)

# Create a team
team_data = {
    "name": "Data Team",
    "description": "Team for data operations"
}
team = client.teams.create(team_data)

# Add team members
from nexla_sdk.models.teams.requests import TeamMemberList
team_members = TeamMemberList(members=[
    {"email": "lead@example.com", "admin": True},
    {"email": "member@example.com", "admin": False}
])
client.teams.add_members(team.id, team_members)
```

## Projects

```python
# Create a project
project_data = {
    "name": "My Project",
    "description": "Data integration project"
}
project = client.projects.create(project_data)

# Add flows to project
from nexla_sdk.models.projects.requests import ProjectFlowList
flow_list = ProjectFlowList(flows=[{"id": flow.id}])
client.projects.add_flows(project.id, flow_list)

# Get project flows
project_flows = client.projects.get_flows(project.id)
```

## Notifications

```python
# List unread notifications
notifications = client.notifications.list(read=0)

# Mark notification as read
client.notifications.mark_read(notification.id)

# Mark all notifications as read
client.notifications.mark_read("all")

# Get notification types
notification_types = client.notifications.get_types()

# Create notification setting
setting_data = {
    "notification_type_id": notification_type.id,
    "notification_channel_setting_id": channel_setting.id,
    "status": "ACTIVE"
}
setting = client.notifications.create_setting(setting_data)
```

## Metrics and Monitoring

```python
# Get daily metrics for a resource
metrics = client.metrics.get_resource_daily_metrics(
    resource_type="data_sources",
    resource_id=source.id,
    from_date="2024-01-01",
    to_date="2024-01-31"
)

# Get metrics by run
run_metrics = client.metrics.get_resource_metrics_by_run(
    resource_type="data_sources",
    resource_id=source.id,
    groupby="runId"
)

# Get rate limits
limits = client.metrics.get_rate_limits()
print(f"Rate limit: {limits}")
```

## Advanced Features

### Lookups (Data Maps)

```python
# Create a lookup table
lookup_data = {
    "name": "Product Mapping",
    "data_type": "string",
    "map_primary_key": "sku",
    "data_map": [
        {"sku": "ABC123", "name": "Product A", "price": 99.99},
        {"sku": "XYZ789", "name": "Product B", "price": 149.99}
    ]
}
lookup = client.lookups.create(lookup_data)

# Get lookup entries
entries = client.lookups.get_entries(lookup.id, "ABC*")

# Upsert lookup entries
new_entries = [
    {"sku": "DEF456", "name": "Product C", "price": 199.99}
]
client.lookups.upsert_entries(lookup.id, new_entries)
```

### User Management

```python
# Get current user
current_user = client.users.get_current()

# Get user settings
settings = client.users.get_settings()

# Get user dashboard metrics
dashboard_metrics = client.users.get_dashboard_metrics(user_id)

# Update quarantine settings
quarantine_config = {
    "cron_schedule": "0 0 * * *",
    "path": "/quarantine/exports/"
}
client.users.create_quarantine_settings(
    user_id=user.id,
    data_credentials_id=credential.id,
    config=quarantine_config
)
```

## Error Handling

The SDK provides specific exception types:

```python
from nexla_sdk.utils.exceptions import (
    NexlaError,
    AuthenticationError,
    NotFoundError,
    ValidationError,
    RateLimitError
)

try:
    source = client.sources.get(999999)
except NotFoundError as e:
    print(f"Source not found: {e}")
except AuthenticationError as e:
    print(f"Auth failed: {e}")
except RateLimitError as e:
    print(f"Rate limited: {e}")
```

## Resource Path Mappings

The SDK uses the following API path mappings:
- **Credentials** → `/data_credentials`
- **Sources** → `/data_sources`
- **Destinations** → `/data_sinks`
- **Nexsets** → `/data_sets`
- **Lookups** → `/data_maps`
- **Flows** → `/flows`
- **Users** → `/users`
- **Organizations** → `/orgs`
- **Teams** → `/teams`
- **Projects** → `/projects`
- **Notifications** → `/notifications`
- **Metrics** → Various endpoints

## Common Resource Methods

All resources support these base methods:

- `list()` - List all resources
- `get(id)` - Get specific resource by ID
- `create(data)` - Create new resource
- `update(id, data)` - Update existing resource
- `delete(id)` - Delete resource
- `activate(id)` - Activate resource
- `pause(id)` - Pause resource
- `copy(id, options)` - Copy resource
- `paginate()` - Get paginated results
- `get_accessors(id)` - Get access control rules
- `add_accessors(id, accessors)` - Add access control rules
- `get_audit_log(id)` - Get audit log entries

## Development

### Running Tests

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run unit tests
pytest tests/

# Run integration tests (requires API credentials)
export NEXLA_SERVICE_KEY="your_service_key"
export NEXLA_API_URL="https://your-nexla-instance.com/nexla-api"
pytest tests/integration/
```

### Setting Up Environment

```bash
# Create .env file
cat > .env << EOF
NEXLA_SERVICE_KEY=your_service_key
NEXLA_API_URL=https://dataops.nexla.io/nexla-api
EOF
```

## License

This project is licensed under the terms of the MIT license.

## Support

For API documentation and support:
- Visit: https://docs.nexla.com
- Email: support@nexla.com 