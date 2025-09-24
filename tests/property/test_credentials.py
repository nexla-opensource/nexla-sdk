"""Property-based tests for credentials using hypothesis."""

import pytest
from hypothesis import given, strategies as st, settings, assume
from hypothesis.strategies import composite
from pydantic import ValidationError

from nexla_sdk.models.credentials.responses import Credential
from nexla_sdk.models.credentials.requests import CredentialCreate, ProbeTreeRequest


# Custom strategies for generating test data
@composite
def credential_dict(draw):
    """Generate random credential data for property testing."""
    return {
        "id": draw(st.integers(min_value=1, max_value=999999)),
        "name": draw(st.text(min_size=1, max_size=200)),
        "credentials_type": draw(st.sampled_from([
            "s3", "postgres", "mysql", "bigquery", "snowflake", "azure_blb", 
            "gcs", "ftp", "dropbox", "rest", "kafka"
        ])),
        "description": draw(st.one_of(st.none(), st.text(max_size=500))),
        "verified_status": draw(st.one_of(st.none(), st.sampled_from(["VERIFIED", "UNVERIFIED", "FAILED"]))),
        "credentials_version": draw(st.one_of(st.none(), st.text(min_size=1, max_size=10))),
        "managed": draw(st.booleans()),
        "tags": draw(st.lists(st.text(min_size=1, max_size=50), max_size=10)),
        "created_at": draw(st.one_of(st.none(), st.datetimes().map(lambda dt: dt.isoformat() + "Z"))),
        "updated_at": draw(st.one_of(st.none(), st.datetimes().map(lambda dt: dt.isoformat() + "Z"))),
    }


@composite
def credential_create_dict(draw):
    """Generate random credential creation data."""
    credentials_type = draw(st.sampled_from(["s3", "postgres", "mysql", "rest", "bigquery"]))
    
    base_data = {
        "name": draw(st.text(min_size=1, max_size=200)),
        "credentials_type": credentials_type,
        "description": draw(st.one_of(st.none(), st.text(max_size=500))),
    }
    
    # Add type-specific credentials
    if credentials_type == "s3":
        base_data["credentials"] = {
            "access_key_id": draw(st.text(min_size=10, max_size=50)),
            "secret_key": draw(st.text(min_size=20, max_size=100)),
            "region": draw(st.sampled_from(["us-east-1", "us-west-2", "eu-west-1", "ap-southeast-1"])),
        }
    elif credentials_type in ["postgres", "mysql"]:
        base_data["credentials"] = {
            "host": draw(st.text(min_size=5, max_size=100)),
            "port": draw(st.integers(min_value=1000, max_value=65535)),
            "database": draw(st.text(min_size=1, max_size=50)),
            "username": draw(st.text(min_size=1, max_size=50)),
            "password": draw(st.text(min_size=1, max_size=100)),
        }
    elif credentials_type == "rest":
        base_data["credentials"] = {
            "api_key": draw(st.text(min_size=10, max_size=100)),
            "endpoint": draw(st.text(min_size=10, max_size=200)),
        }
    
    return base_data


@composite
def probe_tree_request_dict(draw):
    """Generate random probe tree request data."""
    depth = draw(st.integers(min_value=1, max_value=10))
    
    # Choose between file system or database probing
    probe_type = draw(st.sampled_from(["filesystem", "database"]))
    
    if probe_type == "filesystem":
        return {
            "depth": depth,
            "path": draw(st.one_of(st.none(), st.text(min_size=1, max_size=200))),
        }
    else:
        return {
            "depth": depth,
            "database": draw(st.one_of(st.none(), st.text(min_size=1, max_size=100))),
            "table": draw(st.one_of(st.none(), st.text(min_size=1, max_size=100))),
        }


@pytest.mark.unit
class TestCredentialModelProperties:
    """Property-based tests for credential models."""
    
    @given(credential_dict())
    @settings(max_examples=100, deadline=1000)
    def test_credential_model_handles_various_inputs(self, credential_data):
        """Test that Credential model handles various valid inputs correctly."""
        # Act & Assert - should either validate successfully or raise ValidationError
        try:
            credential = Credential(**credential_data)
            
            # If validation succeeds, verify basic properties
            assert credential.id == credential_data["id"]
            assert credential.name == credential_data["name"]
            assert credential.credentials_type == credential_data["credentials_type"]
            
            # Verify serialization works
            credential_dict = credential.to_dict()
            assert isinstance(credential_dict, dict)
            assert credential_dict["id"] == credential_data["id"]
            
            # Verify JSON serialization works
            credential_json = credential.to_json()
            assert isinstance(credential_json, str)
            assert str(credential_data["id"]) in credential_json
            
        except ValidationError:
            # Validation errors are expected for some random inputs
            pass
    
    @given(credential_create_dict())
    @settings(max_examples=50, deadline=1000)
    def test_credential_create_model_validation(self, create_data):
        """Test CredentialCreate model with various inputs."""
        try:
            credential_create = CredentialCreate(**create_data)
            
            # If validation succeeds, verify required fields
            assert credential_create.name == create_data["name"]
            assert credential_create.credentials_type == create_data["credentials_type"]
            
            # Verify serialization
            create_dict = credential_create.to_dict()
            assert isinstance(create_dict, dict)
            assert create_dict["name"] == create_data["name"]
            
        except ValidationError:
            # Some random inputs may not be valid
            pass
    
    @given(probe_tree_request_dict())
    @settings(max_examples=50, deadline=1000)
    def test_probe_tree_request_validation(self, request_data):
        """Test ProbeTreeRequest with various inputs."""
        try:
            probe_request = ProbeTreeRequest(**request_data)
            
            # If validation succeeds, verify depth is preserved
            assert probe_request.depth == request_data["depth"]
            assert probe_request.depth > 0
            
        except ValidationError:
            # Some combinations may not be valid
            pass
    
    @given(st.text(min_size=1, max_size=500))
    def test_credential_name_property(self, name):
        """Test that credential names are handled correctly."""
        minimal_data = {
            "id": 1,
            "name": name,
            "credentials_type": "s3"
        }
        
        try:
            credential = Credential(**minimal_data)
            assert credential.name == name
            
            # Test string representation includes name
            str_repr = str(credential)
            assert name in str_repr
            
        except ValidationError:
            # Some names might be invalid (e.g., very long strings)
            pass
    
    @given(st.lists(st.text(min_size=1, max_size=50), min_size=0, max_size=20))
    def test_credential_tags_property(self, tags):
        """Test that credential tags are handled correctly."""
        credential_data = {
            "id": 1,
            "name": "Test Credential",
            "credentials_type": "s3",
            "tags": tags
        }
        
        credential = Credential(**credential_data)
        assert credential.tags == tags
        
        # Test serialization includes tags
        credential_dict = credential.to_dict()
        assert credential_dict["tags"] == tags


@pytest.mark.unit
class TestCredentialInvariants:
    """Test invariants that should hold for all credential operations."""
    
    @given(credential_dict())
    @settings(max_examples=50)
    def test_serialization_round_trip(self, credential_data):
        """Test that serialization and deserialization preserve data."""
        assume(credential_data.get("name"))  # Assume name is not empty
        
        try:
            # Create credential from dict
            credential = Credential(**credential_data)
            
            # Serialize to dict
            serialized = credential.to_dict()
            
            # Create new credential from serialized data
            credential2 = Credential(**serialized)
            
            # Verify key fields are preserved
            assert credential2.id == credential.id
            assert credential2.name == credential.name
            assert credential2.credentials_type == credential.credentials_type
            
        except ValidationError:
            # Skip invalid inputs
            pass
    
    @given(credential_create_dict())
    @settings(max_examples=30)
    def test_create_request_always_has_required_fields(self, create_data):
        """Test that valid create requests always have required fields."""
        try:
            credential_create = CredentialCreate(**create_data)
            
            # Required fields should always be present
            assert credential_create.name is not None
            assert credential_create.name != ""
            assert credential_create.credentials_type is not None
            assert credential_create.credentials_type != ""
            
        except ValidationError:
            # Invalid inputs are acceptable
            pass
    
    @given(st.integers(min_value=1, max_value=10))
    def test_probe_tree_depth_bounds(self, depth):
        """Test that probe tree requests handle depth correctly."""
        probe_request = ProbeTreeRequest(depth=depth)
        
        # Depth should be preserved and positive
        assert probe_request.depth == depth
        assert probe_request.depth > 0
        
        # Serialization should preserve depth
        serialized = probe_request.to_dict()
        assert serialized["depth"] == depth


@pytest.mark.unit
class TestCredentialEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_credential_with_empty_optional_fields(self):
        """Test credential with all optional fields empty."""
        minimal_data = {
            "id": 1,
            "name": "Minimal Credential",
            "credentials_type": "s3"
        }
        
        credential = Credential(**minimal_data)
        
        # Optional fields should have sensible defaults
        assert credential.description is None
        assert credential.tags == []
        assert credential.managed is False
        assert credential.access_roles is None
    
    @given(st.text(min_size=1000, max_size=5000))  # Very long strings
    def test_credential_with_long_strings(self, long_text):
        """Test credential handling of long strings."""
        credential_data = {
            "id": 1,
            "name": long_text[:200],  # Limit name to reasonable size
            "credentials_type": "s3",
            "description": long_text
        }
        
        try:
            credential = Credential(**credential_data)
            assert len(credential.name) <= 200
            assert credential.description == long_text
            
        except ValidationError:
            # Very long strings might be rejected
            pass
    
    @given(st.lists(st.integers(), min_size=0, max_size=100))
    def test_credential_with_various_list_sizes(self, int_list):
        """Test credential with various list sizes for access_roles."""
        # Convert integers to valid role strings
        valid_roles = ["owner", "admin", "collaborator", "operator"]
        access_roles = [valid_roles[i % len(valid_roles)] for i in int_list[:10]]  # Limit size
        
        credential_data = {
            "id": 1,
            "name": "Test Credential",
            "credentials_type": "s3",
            "access_roles": access_roles
        }
        
        credential = Credential(**credential_data)
        assert credential.access_roles == access_roles
    
    def test_credential_with_null_values(self):
        """Test credential handling of explicit None values."""
        credential_data = {
            "id": 1,
            "name": "Test Credential",
            "credentials_type": "s3",
            "description": None,
            "verified_status": None,
            "verified_at": None,
            "tags": None,  # Should be converted to empty list
        }
        
        credential = Credential(**credential_data)
        
        # None values should be handled gracefully
        assert credential.description is None
        assert credential.verified_status is None
        assert credential.verified_at is None
        assert credential.tags == []  # Should be converted to empty list 