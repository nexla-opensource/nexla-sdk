import logging
import os

from dotenv import load_dotenv

from nexla_sdk import NexlaClient

load_dotenv(override=True)

logger = logging.getLogger(__name__)


service_key = os.environ.get("NEXLA_SERVICE_KEY")
api_url = os.environ.get("NEXLA_API_URL", "https://dataops.nexla.io/nexla-api")

logger.info(f"Using API URL: {api_url}")
logger.info(f"Using Service Key: {service_key}")
print(f"Using Service Key: {service_key}")
print(f"Using API URL: {api_url}")
nexla_client = NexlaClient(service_key=service_key, api_url=api_url)
