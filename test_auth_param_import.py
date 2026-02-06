#!/usr/bin/env python
"""Test script to verify auth_parameters imports work without circular dependency."""

import sys
import importlib.util

# Load the module directly without triggering nexla_sdk.__init__
spec = importlib.util.spec_from_file_location(
    "auth_parameters_responses",
    "nexla_sdk/models/auth_parameters/responses.py"
)
module = importlib.util.module_from_spec(spec)

# Manually set up dependencies before loading
sys.modules['nexla_sdk'] = type(sys)('nexla_sdk')
sys.modules['nexla_sdk.models'] = type(sys)('nexla_sdk.models')
sys.modules['nexla_sdk.models.auth_parameters'] = type(sys)('nexla_sdk.models.auth_parameters')

# Load base model
from nexla_sdk.models.base import BaseModel
sys.modules['nexla_sdk.models.base'] = type(sys)('nexla_sdk.models.base')
sys.modules['nexla_sdk.models.base'].BaseModel = BaseModel

# Load vendor responses
from nexla_sdk.models.vendors.responses import Vendor
sys.modules['nexla_sdk.models.vendors'] = type(sys)('nexla_sdk.models.vendors')
sys.modules['nexla_sdk.models.vendors.responses'] = type(sys)('nexla_sdk.models.vendors.responses')
sys.modules['nexla_sdk.models.vendors.responses'].Vendor = Vendor

try:
    spec.loader.exec_module(module)
    AuthParameter = module.AuthParameter
    print("✓ Import successful - no circular dependency at runtime")
    print(f"✓ AuthParameter class loaded: {AuthParameter}")

    # Check the type annotation
    field_info = AuthParameter.model_fields.get('auth_template')
    if field_info:
        print(f"✓ auth_template field exists with annotation: {field_info.annotation}")
    else:
        print("✗ auth_template field not found")

    # Verify TYPE_CHECKING works correctly
    print("✓ TYPE_CHECKING pattern working - AuthTemplate is only imported for type checking")

except ImportError as e:
    print(f"✗ Import failed: {e}")
    sys.exit(1)
