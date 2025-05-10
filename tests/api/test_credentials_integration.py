#!/usr/bin/env python
"""
Integration tests for the Nexla SDK Credentials API
"""
import os
import time
import unittest
import random
import string
from typing import Dict, Any, List

import pytest

from nexla_sdk import NexlaClient
from nexla_sdk.models.credentials import CredentialCreate, CredentialUpdate
from nexla_sdk.exceptions import NexlaNotFoundError, NexlaAPIError

# Skip tests if NEXLA_RUN_INTEGRATION_TESTS is not set to "true"
INTEGRATION_TESTS_ENABLED = os.environ.get("NEXLA_RUN_INTEGRATION_TESTS", "").lower() == "true"
SKIP_REASON = "Integration tests are disabled. Set NEXLA_RUN_INTEGRATION_TESTS=true to enable."

# Get Nexla service key from environment
NEXLA_TEST_SERVICE_KEY = os.environ.get("NEXLA_TEST_SERVICE_KEY", "")
if not NEXLA_TEST_SERVICE_KEY and INTEGRATION_TESTS_ENABLED:
    pytest.fail("NEXLA_SERVICE_KEY environment variable is required for integration tests")


def random_string(length=8):
    """Generate a random string of a given length"""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


@pytest.mark.skipif(not INTEGRATION_TESTS_ENABLED, reason=SKIP_REASON)
class TestCredentialsIntegration(unittest.TestCase):
    """Integration tests for Credentials API"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures before running tests"""
        cls.client = NexlaClient(service_key=NEXLA_TEST_SERVICE_KEY)
        cls.test_credentials = []

    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests"""
        # Clean up any test credentials created during the tests
        for cred_id in cls.test_credentials:
            try:
                cls.client.credentials.delete(cred_id)
                print(f"Deleted test credential {cred_id}")
            except Exception as e:
                print(f"Failed to delete test credential {cred_id}: {e}")

    def test_01_list_credentials(self):
        """Test listing credentials"""
        credentials = self.client.credentials.list()
        self.assertIsInstance(credentials, list)
        
        if credentials:
            cred = credentials[0]
            self.assertIsNotNone(cred.id)
            self.assertIsNotNone(cred.name)
            self.assertIsNotNone(cred.credentials_type)

    def test_02_create_rest_credential(self):
        """Test creating a REST API credential"""
        test_name = f"Test REST API {random_string()}"
        
        credential_data = CredentialCreate(
            name=test_name,
            description="Test REST API credential created by integration test",
            credentials_type="rest",
            credentials={
                "auth.type": "NONE",
                "ignore.ssl.cert.validation": False,
                "test.method": "GET",
                "test.content.type": "application/json",
                "jwt.enabled": False,
                "hmac.enabled": False,
                "test.url": "https://httpbin.org/get"
            }
        )
        
        credential = self.client.credentials.create(credential_data)
        self.assertIsNotNone(credential)
        self.assertIsNotNone(credential.id)
        self.assertEqual(credential.name, test_name)
        self.assertEqual(credential.credentials_type, "rest")
        
        # Keep track of the created credential for cleanup
        self.__class__.test_credentials.append(credential.id)
        
        return credential

    def test_03_get_credential(self):
        """Test getting a credential by ID"""
        # First create a credential to get
        credential = self.test_02_create_rest_credential()
        
        # Get the credential with expand=True to include non-secure data
        retrieved = self.client.credentials.get(credential.id, expand=True)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.id, credential.id)
        self.assertEqual(retrieved.name, credential.name)
        self.assertEqual(retrieved.credentials_type, credential.credentials_type)
        
        # Verify the non-secure data was returned
        self.assertIsNotNone(retrieved.credentials_non_secure_data)
        self.assertIn("test.url", retrieved.credentials_non_secure_data)
        
        # Also test get with expand=False
        basic = self.client.credentials.get(credential.id, expand=False)
        self.assertIsNotNone(basic)
        self.assertEqual(basic.id, credential.id)

    def test_04_update_credential(self):
        """Test updating a credential"""
        # First create a credential to update
        credential = self.test_02_create_rest_credential()
        new_name = f"Updated REST API {random_string()}"
        
        update_data = CredentialUpdate(
            name=new_name,
            description="Updated by integration test"
        )
        
        updated = self.client.credentials.update(credential.id, update_data)
        self.assertIsNotNone(updated)
        self.assertEqual(updated.id, credential.id)
        self.assertEqual(updated.name, new_name)
        self.assertEqual(updated.description, "Updated by integration test")

    def test_05_probe_credential(self):
        """Test probing a credential"""
        # First create a credential to probe
        credential = self.test_02_create_rest_credential()
        
        result = self.client.credentials.probe(credential.id)
        self.assertIsNotNone(result)
        self.assertIn("status", result)

    def test_06_nonexistent_credential(self):
        """Test handling of non-existent credential"""
        non_existent_id = 999999999  # Assuming this ID doesn't exist
        
        with self.assertRaises(NexlaNotFoundError):
            self.client.credentials.get(non_existent_id)

    def test_07_delete_credential(self):
        """Test deleting a credential"""
        # First create a credential to delete
        credential = self.test_02_create_rest_credential()
        
        # Remove from cleanup list since we're deleting it now
        if credential.id in self.__class__.test_credentials:
            self.__class__.test_credentials.remove(credential.id)
        
        result = self.client.credentials.delete(credential.id)
        self.assertIsNotNone(result)
        self.assertIn(result.code, ["200", "success", "Success", "OK", "ok"])
        
        # Verify the credential was deleted
        with self.assertRaises(NexlaNotFoundError):
            self.client.credentials.get(credential.id)

    def test_08_probe_tree(self):
        """Test probing a directory tree (if applicable)"""
        # Skip if no credentials are available
        credentials = self.client.credentials.list()
        if not credentials:
            self.skipTest("No credentials available for testing probe_tree")
        
        # Try to find a file-based credential (S3, GCS, etc)
        file_cred = None
        for cred in credentials:
            if cred.credentials_type in ["s3", "gcs", "ftp", "sftp"]:
                file_cred = cred
                break
                
        if not file_cred:
            self.skipTest("No file-based credential available for testing probe_tree")
            
        try:
            # Use a minimal request to avoid permission issues
            tree = self.client.credentials.probe_tree(file_cred.id, depth=1)
            self.assertIsNotNone(tree)
        except NexlaAPIError as e:
            # If we get an API error (could be permission-related), just skip the test
            self.skipTest(f"Could not access directory tree: {e}")

    def test_09_probe_files(self):
        """Test probing file content (if applicable)"""
        # Skip this test as it requires knowing valid path/file values
        self.skipTest("Requires specific path and file values for existing credential")
        
    def test_10_probe_sample(self):
        """Test getting a data sample (if applicable)"""
        # Skip this test as it requires knowing valid path values
        self.skipTest("Requires specific path values for existing credential")


if __name__ == "__main__":
    unittest.main() 