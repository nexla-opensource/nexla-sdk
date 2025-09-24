from enum import Enum


class DestinationStatus(str, Enum):
    """Destination status values."""
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    DRAFT = "DRAFT"
    DELETED = "DELETED"
    ERROR = "ERROR"


class DestinationType(str, Enum):
    """Supported sink types."""
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
    
    # Special
    EMAIL = "email"
    DATA_MAP = "data_map"
    
    # Vector Databases
    PINECONE = "pinecone"
    
    # Add all other types from the spec...


class DestinationFormat(str, Enum):
    """Output format for destinations."""
    JSON = "json"
    CSV = "csv"
    PARQUET = "parquet"
    AVRO = "avro"
    XML = "xml"
    DELIMITED = "delimited"
    FIXED_WIDTH = "fixed_width"