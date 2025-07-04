"""Enums for sources."""
from enum import Enum


class SourceStatus(str, Enum):
    """Source status values."""
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    DRAFT = "DRAFT"
    DELETED = "DELETED"
    ERROR = "ERROR"


class SourceType(str, Enum):
    """Supported source types."""
    # File Systems
    S3 = "s3"
    GCS = "gcs"
    AZURE_BLB = "azure_blb"
    FTP = "ftp"
    DROPBOX = "dropbox"
    BOX = "box"
    GDRIVE = "gdrive"
    SHAREPOINT = "sharepoint"
    
    # Databases
    MYSQL = "mysql"
    POSTGRES = "postgres"
    SQLSERVER = "sqlserver"
    ORACLE = "oracle"
    REDSHIFT = "redshift"
    SNOWFLAKE = "snowflake"
    BIGQUERY = "bigquery"
    DATABRICKS = "databricks"
    
    # NoSQL
    MONGO = "mongo"
    DYNAMODB = "dynamodb"
    FIREBASE = "firebase"
    
    # Streaming
    KAFKA = "kafka"
    CONFLUENT_KAFKA = "confluent_kafka"
    GOOGLE_PUBSUB = "google_pubsub"
    
    # APIs
    REST = "rest"
    SOAP = "soap"
    NEXLA_REST = "nexla_rest"
    
    # Special
    FILE_UPLOAD = "file_upload"
    EMAIL = "email"
    NEXLA_MONITOR = "nexla_monitor"
    
    # Add all other types from the spec...


class IngestMethod(str, Enum):
    """Data ingestion methods."""
    BATCH = "BATCH"
    STREAMING = "STREAMING"
    REAL_TIME = "REAL_TIME"
    SCHEDULED = "SCHEDULED"


class FlowType(str, Enum):
    """Flow processing types."""
    BATCH = "batch"
    STREAMING = "streaming"
    REAL_TIME = "real_time"