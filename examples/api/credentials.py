#!/usr/bin/env python
"""
Example usage of the Nexla SDK Credentials API
"""
import os
import json
from typing import Dict, Any
from pprint import pprint

from nexla_sdk import NexlaClient
from nexla_sdk.models.credentials import CredentialCreate, CredentialUpdate
from nexla_sdk.exceptions import NexlaNotFoundError, NexlaAPIError
from client import nexla_client


def list_credentials():
    """List all credentials"""
    print("\n=== Listing credentials ===")
    credentials = nexla_client.credentials.list()
    print(f"Found {len(credentials)} credentials:")
    for cred in credentials:
        print(f"- {cred.id}: {cred.name} ({cred.credentials_type})")
    return credentials

def get_credential(credential_id):
    """Get a credential by ID"""
    print(f"\n=== Getting credential {credential_id} ===")
    try:
        credential = nexla_client.credentials.get(credential_id, expand=True)
        print(f"Found credential: {credential.name}")
        print(f"Description: {credential.description}")
        print(f"Type: {credential.credentials_type}")
        print(f"Non-secure data: {json.dumps(credential.credentials_non_secure_data, indent=2)}")
        return credential
    except NexlaNotFoundError:
        print(f"Credential with ID {credential_id} not found")
        return None

def create_s3_credential():
    """Create a new S3 credential"""
    print("\n=== Creating new S3 credential ===")
    
    credential_data = CredentialCreate(
        name="Test S3 Credential",
        description="Example S3 credential created with SDK",
        credentials_type="s3",
        credentials={
            "credentials_type": "s3", 
            "access_key_id": "YOUR_AWS_ACCESS_KEY",
            "secret_key": "YOUR_AWS_SECRET_KEY"
        }
    )
    
    try:
        credential = nexla_client.credentials.create(credential_data)
        print(f"Created credential with ID: {credential.id}")
        return credential
    except NexlaAPIError as e:
        print(f"Failed to create credential: {e}")
        return None

def update_credential(credential_id):
    """Update an existing credential"""
    print(f"\n=== Updating credential {credential_id} ===")
    
    update_data = CredentialUpdate(
        name="Updated Credential Name",
        description="Updated description via SDK example"
    )
    
    try:
        updated = nexla_client.credentials.update(credential_id, update_data)
        print(f"Updated credential: {updated.name}")
        return updated
    except NexlaNotFoundError:
        print(f"Credential with ID {credential_id} not found")
        return None

def probe_credential(credential_id):
    """Test a credential by probing"""
    print(f"\n=== Testing credential {credential_id} ===")
    
    try:
        result = nexla_client.credentials.probe(credential_id)
        print(f"Probe result: {result.get('status', 'Unknown')}")
        return result
    except (NexlaNotFoundError, NexlaAPIError) as e:
        print(f"Failed to probe credential: {e}")
        return None

def probe_tree(credential_id, path=None):
    """Get directory tree for a credential"""
    print(f"\n=== Getting directory tree for credential {credential_id} ===")
    
    try:
        tree = nexla_client.credentials.probe_tree(
            credential_id, 
            depth=2,
            path=path
        )
        print(f"Found {len(tree.items)} items at path {tree.path}")
        for item in tree.items[:5]:  # Show just the first 5 items
            print(f"- {item.name} ({item.type})")
        return tree
    except NexlaAPIError as e:
        print(f"Failed to get directory tree: {e}")
        return None

def probe_files(credential_id, path, file):
    """Inspect file content for a credential"""
    print(f"\n=== Inspecting file content for credential {credential_id} ===")
    
    try:
        content = nexla_client.credentials.probe_files(credential_id, path, file)
        print(f"File format: {content.output.get('format', 'Unknown')}")
        print("Sample data:")
        messages = content.output.get("messages", [])
        for idx, msg in enumerate(messages[:3]):  # Show just the first 3 records
            print(f"Record {idx+1}: {json.dumps(msg, indent=2)}")
        return content
    except NexlaAPIError as e:
        print(f"Failed to inspect file content: {e}")
        return None

def get_data_sample(credential_id, path=None):
    """Get a sample of data for a credential"""
    print(f"\n=== Getting data sample for credential {credential_id} ===")
    
    try:
        sample = nexla_client.credentials.probe_sample(credential_id, path=path)
        print(f"Retrieved {len(sample.records)} sample records")
        for idx, record in enumerate(sample.records[:3]):  # Show just the first 3 records
            print(f"Record {idx+1}: {json.dumps(record, indent=2)}")
        return sample
    except NexlaAPIError as e:
        print(f"Failed to get data sample: {e}")
        return None

def delete_credential(credential_id):
    """Delete a credential"""
    print(f"\n=== Deleting credential {credential_id} ===")
    
    try:
        result = nexla_client.credentials.delete(credential_id)
        print(f"Deleted credential: {result.code} - {result.message}")
        return True
    except NexlaNotFoundError:
        print(f"Credential with ID {credential_id} not found")
        return False

def main():
    """Run the example"""
    # List all credentials
    credentials = list_credentials()
    
    if not credentials:
        print("No credentials found, creating a new one...")
        # Note: Replace with your own values before running
        # credential = create_s3_credential()
        # credential_id = credential.id if credential else None
        credential_id = None
    else:
        # Use the first credential for examples
        credential_id = credentials[0].id
    
    if credential_id:
        # Get detailed credential info
        credential = get_credential(credential_id)
        
        # Test the credential
        probe_credential(credential_id)
        
        # Examples of additional probe functions
        # Note: These require appropriate permissions and paths
        # probe_tree(credential_id, path="your-bucket-name")
        # probe_files(credential_id, path="your-bucket-name", file="path/to/file.json")
        # get_data_sample(credential_id, path="your-bucket-name/path/to/file.json")
        
        # Update the credential
        # update_credential(credential_id)
        
        # Delete a credential (commented out to prevent accidental deletion)
        # delete_credential(credential_id)

if __name__ == "__main__":
    main() 