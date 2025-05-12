"""
Example Nexla SDK client configuration

This file sets up the NexlaClient instance used in all the examples.
"""
import logging
import os

from dotenv import load_dotenv

from nexla_sdk import NexlaClient

load_dotenv(override=True)

logger = logging.getLogger(__name__)
service_key = os.environ.get("NEXLA_SERVICE_KEY")
api_url = os.environ.get("NEXLA_API_URL", "https://dataops.nexla.io/nexla-api")

logger.info(f"Using API URL: {api_url}")
if not service_key:
    raise ValueError("NEXLA_SERVICE_KEY is not set")

nexla_client = NexlaClient(service_key=service_key, api_url=api_url)
