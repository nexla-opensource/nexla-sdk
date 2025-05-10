"""
Credential models for the Nexla SDK
"""
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field

from .common import Resource, PaginatedList
from .access import AccessRole

class CredentialType(str, Enum):
    """Credential type enumeration"""
    # File storage types
    S3 = "s3"
    GCS = "gcs"
    AZURE_BLB = "azure_blb"
    AZURE_DATA_LAKE = "azure_data_lake"
    DELTA_LAKE_S3 = "delta_lake_s3"
    DELTA_LAKE_AZURE_BLB = "delta_lake_azure_blb"
    DELTA_LAKE_AZURE_DATA_LAKE = "delta_lake_azure_data_lake"
    S3_ICEBERG = "s3_iceberg"
    MIN_IO_S3 = "min_io_s3"
    FTP = "ftp"
    BOX = "box"
    DROPBOX = "dropbox"
    GDRIVE = "gdrive"
    SHAREPOINT = "sharepoint"
    WEBDAV = "webdav"
    
    # Database types
    MYSQL = "mysql"
    POSTGRES = "postgres"
    SNOWFLAKE = "snowflake"
    SNOWFLAKE_DCR = "snowflake_dcr"
    REDSHIFT = "redshift"
    BIGQUERY = "bigquery"
    DATABRICKS = "databricks"
    SQLSERVER = "sqlserver"
    ORACLE = "oracle"
    ORACLE_AUTONOMOUS = "oracle_autonomous"
    DB2 = "db2"
    SYBASE = "sybase"
    TERADATA = "teradata"
    AWS_ATHENA = "aws_athena"
    AZURE_SYNAPSE = "azure_synapse"
    FIREBOLT = "firebolt"
    GCP_ALLOYDB = "gcp_alloydb"
    GCP_SPANNER = "gcp_spanner"
    AS400 = "as400"
    HANA_JDBC = "hana_jdbc"
    NETSUITE_JDBC = "netsuite_jdbc"
    HIVE = "hive"
    CLOUDSQL_MYSQL = "cloudsql_mysql"
    CLOUDSQL_POSTGRES = "cloudsql_postgres"
    CLOUDSQL_SQLSERVER = "cloudsql_sqlserver"
    
    # NoSQL types
    MONGO = "mongo"
    DYNAMODB = "dynamodb"
    FIREBASE = "firebase"
    PINECONE = "pinecone"
    
    # API types
    REST = "rest"
    SOAP = "soap"
    
    # Streaming types
    KAFKA = "kafka"
    CONFLUENT_KAFKA = "confluent_kafka"
    GOOGLE_PUBSUB = "google_pubsub"
    JMS = "jms"
    TIBCO = "tibco"
    
    # Other types
    NEXLA_MONITOR = "nexla_monitor"


class VerifiedStatus(str, Enum):
    """Verification status enumeration"""
    VERIFIED = "verified"
    UNVERIFIED = "unverified"
    FAILED = "failed"
    SUCCESS = "200 Ok"     # Additional status returned by API
    OK = "OK"
    ERROR = "ERROR"
    
    # For backward compatibility, allow any string
    def __new__(cls, *values):
        obj = str.__new__(cls, values[0])
        obj._value_ = values[0]
        return obj
    
    @classmethod
    def _missing_(cls, value):
        # Handle unexpected values gracefully, allowing any string
        return cls(value)


class Owner(BaseModel):
    """Owner information"""
    id: int = Field(..., description="Owner ID")
    full_name: str = Field(..., description="Owner's full name")
    email: str = Field(..., description="Owner's email address")


class Organization(BaseModel):
    """Organization information"""
    id: int = Field(..., description="Organization ID")
    name: str = Field(..., description="Organization name")
    email_domain: str = Field(..., description="Organization email domain")
    email: Optional[str] = Field(None, description="Organization email")
    client_identifier: Optional[str] = Field(None, description="Client identifier")


class Connector(BaseModel):
    """Connector information"""
    id: int = Field(..., description="Connector ID")
    type: str = Field(..., description="Connector type")
    connection_type: str = Field(..., description="Connection type")
    name: str = Field(..., description="Connector name")
    description: str = Field(..., description="Connector description")
    nexset_api_compatible: bool = Field(..., description="Whether compatible with Nexset API")


class Vendor(BaseModel):
    """Vendor information"""
    id: int = Field(..., description="Vendor ID")
    name: str = Field(..., description="Vendor name")
    display_name: str = Field(..., description="Vendor display name")
    connection_type: str = Field(..., description="Connection type")


class Credential(BaseModel):
    """Credential resource model"""
    id: int = Field(..., description="Unique identifier for the credential")
    name: str = Field(..., description="Name of the credential")
    description: Optional[str] = Field(None, description="Description of the credential")
    owner: Owner = Field(..., description="Owner information")
    org: Organization = Field(..., description="Organization information")
    access_roles: List[AccessRole] = Field(..., description="Access roles for this credential")
    credentials_version: str = Field(..., description="Credentials version")
    credentials_type: str = Field(..., description="Credentials type")
    connector: Connector = Field(..., description="Connector information")
    verified_status: VerifiedStatus = Field(..., description="Verification status")
    verified_at: Optional[datetime] = Field(None, description="Verification timestamp")
    copied_from_id: Optional[int] = Field(None, description="ID of the credential this was copied from")
    updated_at: datetime = Field(..., description="Last update timestamp")
    created_at: datetime = Field(..., description="Creation timestamp")
    vendor: Optional[Vendor] = Field(None, description="Vendor information")
    template_config: Optional[Dict[str, Any]] = Field(None, description="Template configuration")


class CredentialCreate(BaseModel):
    """Credential creation model"""
    name: str = Field(..., description="Name of the credential")
    description: Optional[str] = Field(None, description="Description of the credential")
    credentials_type: str = Field(..., description="Credentials type")
    credentials: Dict[str, Any] = Field(..., description="Credential configuration")


class CredentialUpdate(BaseModel):
    """Credential update model"""
    name: Optional[str] = Field(None, description="Name of the credential")
    description: Optional[str] = Field(None, description="Description of the credential")
    credentials_type: Optional[str] = Field(None, description="Credentials type")
    credentials: Optional[Dict[str, Any]] = Field(None, description="Credential configuration")


class CredentialExpanded(Credential):
    """Expanded credential model with additional details"""
    managed: bool = Field(..., description="Whether the credential is managed")
    api_keys: List[Any] = Field(..., description="API keys")
    credentials_non_secure_data: Dict[str, Union[str, int, Dict[str, Any]]] = Field(
        ..., description="Non-secure credential data"
    )
    tags: List[str] = Field(..., description="Tags associated with this credential")


class CredentialList(BaseModel):
    """List of credentials"""
    items: List[Credential] = Field(..., description="List of credentials")


class FileProbeTree(BaseModel):
    """File system probe tree result"""
    status: str = Field(..., description="Response status")
    message: str = Field(..., description="Message string")
    connection_type: str = Field(..., description="Connector type")
    # Additional file system specific fields


class DatabaseProbeTree(BaseModel):
    """Database probe tree result"""
    status: str = Field(..., description="Response status")
    message: str = Field(..., description="Message string")
    connection_type: str = Field(..., description="Connector type")
    # Additional database specific fields


class NoSqlProbeTree(BaseModel):
    """NoSQL probe tree result"""
    status: str = Field(..., description="Response status")
    message: str = Field(..., description="Message string")
    connection_type: str = Field(..., description="Connector type")
    # Additional NoSQL specific fields


class ProbeOutputFile(BaseModel):
    """Probe output for file content"""
    contentType: str = Field(..., description="File content type")
    statusCode: int = Field(..., description="Storage system status code")
    response: str = Field(..., description="Sample lines from the file")


class ProbeOutputDatabase(BaseModel):
    """Probe output for database content"""
    contentType: str = Field(..., description="Response content type")
    statusCode: int = Field(..., description="Storage system status code")
    response: Dict[str, Any] = Field(..., description="Database sample response")


class ProbeOutputNoSql(BaseModel):
    """Probe output for NoSQL content"""
    contentType: str = Field(..., description="Response content type")
    statusCode: int = Field(..., description="Storage system status code")
    response: str = Field(..., description="JSON string of document contents")


class ProbeOutputAPI(BaseModel):
    """Probe output for API response"""
    contentType: str = Field(..., description="Connector response content type")
    statusCode: int = Field(..., description="Storage system status code")
    response: str = Field(..., description="API response from the 3rd party API")


class ProbeResult(BaseModel):
    """Probe test result for a credential"""
    status: str = Field(..., description="Response status code")
    message: str = Field(..., description="Status message")
    connection_type: str = Field(..., description="Connection type")
    output: Union[ProbeOutputFile, ProbeOutputDatabase, ProbeOutputNoSql, ProbeOutputAPI] = Field(
        ..., description="Probe output"
    )


class FileProbeContent(BaseModel):
    """File probe content result from the probe/files endpoint"""
    status: int = Field(..., description="Response status code")
    message: str = Field(..., description="Status message")
    connection_type: str = Field(..., description="Connection type")
    output: Dict[str, Any] = Field(..., description="Output with file format and content sample")


class DirectoryItem(BaseModel):
    """Directory tree item"""
    name: str = Field(..., description="Item name")
    path: str = Field(..., description="Full path to the item")
    type: str = Field(..., description="Item type (e.g., 'file', 'directory')")
    size: Optional[int] = Field(None, description="Size in bytes (for files)")
    last_modified: Optional[datetime] = Field(None, description="Last modified timestamp")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class DirectoryTree(BaseModel):
    """Directory/file tree for a credential"""
    path: str = Field(..., description="Base path for the tree")
    items: List[DirectoryItem] = Field(..., description="Items in the tree")
    credential_id: str = Field(..., description="Credential ID")


class DataSample(BaseModel):
    """Sample data from a data source"""
    records: List[Dict[str, Any]] = Field(..., description="Sample data records")
    schema_: Optional[Dict[str, Any]] = Field(None, alias="schema", description="Schema information")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")

class DeleteDataCredentialResponse(BaseModel):
    """Response model for deleting a data credential"""
    code: str = Field(..., description="Response status code")
    message: str = Field(..., description="Response status text")