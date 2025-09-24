---
id: quickstart
title: Quickstart
description: Ready-to-run examples for common Nexla Python SDK tasks.
slug: /quickstart
keywords: [quickstart, examples, code samples, tutorials]
---

# Quickstart Examples

Ready to jump in? Here are copy-paste examples for the most common Nexla SDK tasks. Each example is self-contained and ready to run.

## 🚀 Setup

```python
import os
from nexla_sdk import NexlaClient

# Set your credentials (replace with your actual key)
os.environ['NEXLA_SERVICE_KEY'] = 'REPLACE_WITH_YOUR_SERVICE_KEY'

# Initialize client
client = NexlaClient()
```

## 📋 List and Explore Resources

### List All Flows

```python
# Get all flows with basic info
flows = client.flows.list(flows_only=True)
print(f"📊 Found {len(flows)} flows")

for flow in flows[:5]:  # Show first 5
    print(f"  🔄 {flow.name} (ID: {flow.id})")
    print(f"     Status: {flow.status}")
    print(f"     Updated: {flow.updated_time}")
    print()
```

### Explore Flow Details

```python
# Get detailed information about a specific flow
if flows:
    flow_id = flows[0].id
    detailed_flow = client.flows.get(flow_id)
    
    print(f"🔍 Flow Details: {detailed_flow.name}")
    print(f"   Description: {detailed_flow.description or 'No description'}")
    print(f"   Created: {detailed_flow.created_time}")
    print(f"   Project: {detailed_flow.project_id}")
    print(f"   Sources: {len(detailed_flow.sources) if detailed_flow.sources else 0}")
    print(f"   Destinations: {len(detailed_flow.destinations) if detailed_flow.destinations else 0}")
```

## 🔌 Working with Data Sources

### List Data Sources

```python
# Get all data sources
sources = client.sources.list()
print(f"📥 Found {len(sources)} data sources")

# Group by type
source_types = {}
for source in sources:
    source_type = source.type
    source_types[source_type] = source_types.get(source_type, 0) + 1

print("\n📊 Sources by type:")
for source_type, count in source_types.items():
    print(f"   {source_type}: {count}")
```

### Get Source Details

```python
# Examine a specific source
if sources:
    source = client.sources.get(sources[0].id)
    print(f"\n🔍 Source: {source.name}")
    print(f"   Type: {source.type}")
    print(f"   Status: {source.status}")
    print(f"   Created: {source.created_time}")
    
    # Show connection info (if available)
    if hasattr(source, 'connection_info'):
        print(f"   Connection: {source.connection_info}")
```

## 🎯 Working with Destinations

### List and Analyze Destinations

```python
# Get all destinations
destinations = client.destinations.list()
print(f"📤 Found {len(destinations)} destinations")

# Show destinations with their types
for dest in destinations[:3]:  # Show first 3
    print(f"  🎯 {dest.name}")
    print(f"     Type: {dest.type}")
    print(f"     Status: {dest.status}")
    print(f"     Project: {dest.project_id}")
    print()
```

## 📊 Projects and Organization

### List Projects

```python
# Get all projects
projects = client.projects.list()
print(f"📁 Found {len(projects)} projects")

for project in projects:
    print(f"  📁 {project.name}")
    print(f"     ID: {project.id}")
    print(f"     Description: {project.description or 'No description'}")
    print(f"     Created: {project.created_time}")
    print()
```

### Get Current User Info

```python
# Get current user information
try:
    users = client.users.list()
    if users:
        current_user = users[0]  # Usually the authenticated user
        print(f"👤 Current User: {current_user.email}")
        print(f"   Name: {current_user.first_name} {current_user.last_name}")
        print(f"   Role: {current_user.role}")
        print(f"   Organization: {current_user.organization_id}")
except Exception as e:
    print(f"ℹ️  User info not available: {e}")
```

## 📈 Monitoring and Metrics

### Check Flow Status

```python
# Monitor flow status
def check_flow_health():
    flows = client.flows.list(flows_only=True)
    
    status_count = {}
    for flow in flows:
        status = flow.status
        status_count[status] = status_count.get(status, 0) + 1
    
    print("🏥 Flow Health Summary:")
    for status, count in status_count.items():
        emoji = "✅" if status == "running" else "⚠️" if status == "paused" else "❌"
        print(f"   {emoji} {status.title()}: {count} flows")

check_flow_health()
```

### Get Recent Notifications

```python
# Check recent notifications
try:
    notifications = client.notifications.list()
    print(f"\n🔔 Recent Notifications ({len(notifications[:5])} shown):")
    
    for notif in notifications[:5]:
        print(f"  📝 {notif.type}: {notif.message}")
        print(f"     Time: {notif.created_time}")
        print(f"     Severity: {notif.severity}")
        print()
except Exception as e:
    print(f"ℹ️  Notifications not available: {e}")
```

## 🔍 Advanced Queries

### Search Flows by Name

```python
def find_flows_by_name(search_term):
    """Find flows containing a specific term in their name"""
    flows = client.flows.list()
    matching_flows = [
        flow for flow in flows 
        if search_term.lower() in flow.name.lower()
    ]
    
    print(f"🔍 Found {len(matching_flows)} flows matching '{search_term}':")
    for flow in matching_flows:
        print(f"  🔄 {flow.name} (ID: {flow.id})")
    
    return matching_flows

# Example usage
# matching_flows = find_flows_by_name("test")
```

### Resource Summary Dashboard

```python
def show_dashboard():
    """Display a summary dashboard of all resources"""
    print("🏢 NEXLA DASHBOARD")
    print("=" * 50)
    
    try:
        # Get counts for each resource type
        flows = client.flows.list(flows_only=True)
        sources = client.sources.list()
        destinations = client.destinations.list()
        projects = client.projects.list()
        
        print(f"📊 Flows: {len(flows)}")
        print(f"📥 Sources: {len(sources)}")
        print(f"📤 Destinations: {len(destinations)}")
        print(f"📁 Projects: {len(projects)}")
        
        # Show flow status breakdown
        status_count = {}
        for flow in flows:
            status = flow.status
            status_count[status] = status_count.get(status, 0) + 1
        
        print(f"\n🏥 Flow Status:")
        for status, count in status_count.items():
            print(f"   {status.title()}: {count}")
            
    except Exception as e:
        print(f"❌ Error loading dashboard: {e}")

# Run the dashboard
show_dashboard()
```

## 🛠️ Error Handling Example

```python
from nexla_sdk.exceptions import NexlaAPIError, AuthenticationError

def safe_api_call():
    """Example of proper error handling"""
    try:
        # This might fail
        flows = client.flows.list()
        print(f"✅ Successfully retrieved {len(flows)} flows")
        
    except AuthenticationError:
        print("❌ Authentication failed:")
        print("   • Check your NEXLA_SERVICE_KEY")
        print("   • Verify the key is active")
        print("   • Ensure you have proper permissions")
        
    except NexlaAPIError as e:
        print(f"❌ API Error (Status {e.status_code}): {e.message}")
        print("   • Check your network connection")
        print("   • Verify the API endpoint")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("   • Check the documentation")
        print("   • Contact support if the issue persists")

safe_api_call()
```

## 🚀 Next Steps

Ready for more? Here's where to go next:

- **[Getting Started](getting-started)** - Detailed setup and configuration
- **[Core Concepts](core-concepts)** - Understanding Nexla's data model  
- **[API Reference](api/python/overview)** - Complete method documentation
- **[Examples](examples)** - More complex real-world scenarios

## 📝 Configuration Notes

- **API Endpoint**: Set `NEXLA_API_URL` if using a custom Nexla instance
- **Observability**: Set OpenTelemetry environment variables for tracing
- **Rate Limits**: The SDK handles rate limiting automatically
- **Retries**: Built-in retry logic for transient failures

:::tip Pro Tip
Start with the dashboard example above to get an overview of your Nexla environment, then dive into specific resource management based on your needs!
:::

