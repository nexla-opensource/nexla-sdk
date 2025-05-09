import os

import pytest
from dotenv import load_dotenv

from nexla_sdk import NexlaClient
from nexla_sdk.exceptions import NexlaAuthError

# Load environment variables from .env file in the tests directory
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path, override=True)

NEXLA_TEST_API_URL = os.getenv("NEXLA_TEST_API_URL")
NEXLA_TEST_SERVICE_KEY = os.getenv("NEXLA_TEST_SERVICE_KEY")
NEXLA_TEST_API_VERSION = os.getenv("NEXLA_TEST_API_VERSION", "v1")
NEXLA_TEST_LOG_LEVEL = os.getenv("NEXLA_TEST_LOG_LEVEL", "INFO")

# Configure logging level based on environment variable
import logging
log_level = getattr(logging, NEXLA_TEST_LOG_LEVEL.upper(), logging.INFO)
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)

# Pytest marker to skip tests if integration credentials are not set
skip_if_no_integration_creds = pytest.mark.skipif(
    not (NEXLA_TEST_API_URL and NEXLA_TEST_SERVICE_KEY),
    reason="Nexla integration test credentials not set (NEXLA_TEST_API_URL, NEXLA_TEST_SERVICE_KEY)",
)


@pytest.fixture(scope="session")
def api_url() -> str:
    if not NEXLA_TEST_API_URL:
        pytest.skip("NEXLA_TEST_API_URL not set for integration tests")
    return NEXLA_TEST_API_URL


@pytest.fixture(scope="session")
def service_key() -> str:
    if not NEXLA_TEST_SERVICE_KEY:
        pytest.skip("NEXLA_TEST_SERVICE_KEY not set for integration tests")
    return NEXLA_TEST_SERVICE_KEY


@pytest.fixture(scope="session")
def api_version() -> str:
    return NEXLA_TEST_API_VERSION


@pytest.fixture(scope="session")
def nexla_client(api_url: str, service_key: str, api_version: str) -> NexlaClient:
    """
    Provides a NexlaClient instance configured for integration tests.
    Tries to make a simple call to verify authentication.
    """
    logger.info(f"Initializing Nexla client with URL: {api_url}, API version: {api_version}")
    
    client = NexlaClient(service_key=service_key, api_url=api_url, api_version=api_version)
    
    # Perform a lightweight check to ensure the client is somewhat functional with the creds
    try:
        # A lightweight call to check connectivity and auth, e.g., get current user
        logger.info("Testing client authentication with get_current user call")
        user = client.users.get_current()
        logger.info(f"Authentication successful, current user: {user.email if hasattr(user, 'email') else 'Unknown'}")
    
    except NexlaAuthError as e:
        logger.error(f"Authentication failed for integration tests: {e}")
        pytest.skip(f"Authentication failed for integration tests: {e}")
    
    except Exception as e:
        # Catch other potential issues like network errors during setup
        logger.error(f"Could not connect to Nexla API or other setup error: {e}")
        pytest.skip(f"Could not connect to Nexla API or other setup error: {e}")
    
    return client
