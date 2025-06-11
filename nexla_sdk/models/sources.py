"""
Source models for the Nexla SDK (Data Sources)
"""
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, EmailStr

from .common import Resource, PaginatedList, ConnectorType
from .access import AccessRole, Owner, Organization
from .credentials import Credential


class SourceType(str, Enum):
    """Source type enumeration"""
    AS400 = "as400"
    AWS_ATHENA = "aws_athena"
    AZURE_BLB = "azure_blb"
    AZURE_DATA_LAKE = "azure_data_lake"
    AZURE_SYNAPSE = "azure_synapse"
    BIGQUERY = "bigquery"
    BOX = "box"
    CLOUDSQL_MYSQL = "cloudsql_mysql"
    CLOUDSQL_POSTGRES = "cloudsql_postgres"
    CLOUDSQL_SQLSERVER = "cloudsql_sqlserver"
    CONFLUENT_KAFKA = "confluent_kafka"
    DATABRICKS = "databricks"
    DB2 = "db2"
    DROPBOX = "dropbox"
    DYNAMODB = "dynamodb"
    FILE_UPLOAD = "file_upload"
    FIREBASE = "firebase"
    FIREBOLT = "firebolt"
    FTP = "ftp"
    GCP_ALLOYDB = "gcp_alloydb"
    GCP_SPANNER = "gcp_spanner"
    GCS = "gcs"
    GDRIVE = "gdrive"
    GOOGLE_PUBSUB = "google_pubsub"
    HANA_JDBC = "hana_jdbc"
    HIVE = "hive"
    JMS = "jms"
    KAFKA = "kafka"
    MIN_IO_S3 = "min_io_s3"
    MONGO = "mongo"
    MYSQL = "mysql"
    NETSUITE_JDBC = "netsuite_jdbc"
    NEXLA_MONITOR = "nexla_monitor"
    NEXLA_REST = "nexla_rest"
    ORACLE = "oracle"
    ORACLE_AUTONOMOUS = "oracle_autonomous"
    PINECONE = "pinecone"
    POSTGRES = "postgres"
    REDSHIFT = "redshift"
    REST = "rest"
    S3 = "s3"
    S3_ICEBERG = "s3_iceberg"
    SHAREPOINT = "sharepoint"
    SNOWFLAKE = "snowflake"
    SOAP = "soap"
    SQLSERVER = "sqlserver"
    SYBASE = "sybase"
    TERADATA = "teradata"
    TIBCO = "tibco"
    WEBDAV = "webdav"


class ConnectionType(str, Enum):
    """Connection type enumeration"""
    PUSH = "push"
    PULL = "pull"
    WEBHOOK = "webhook"


class FlowType(str, Enum):
    """Flow type enumeration"""
    INPUT = "input"
    OUTPUT = "output"


class VerifiedStatus(str, Enum):
    """Verified status enumeration"""
    VERIFIED = "verified"
    UNVERIFIED = "unverified"
    FAILED = "failed"


class SourceStatus(str, Enum):
    """Source status enumeration"""
    ACTIVE = "active"
    PAUSED = "paused"
    ERROR = "error"


class IngestMethod(str, Enum):
    """Ingest method enumeration"""
    PUSH = "push"
    PULL = "pull"
    WEBHOOK = "webhook"


class FileStatus(str, Enum):
    """File ingestion status"""
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETE = "COMPLETE"
    ERROR = "ERROR"
    PARTIAL = "PARTIAL"


class Connector(BaseModel):
    """Connector information"""
    id: int = Field(..., description="Connector ID")
    type: str = Field(..., description="Connector type")
    connection_type: str = Field(..., description="Connection type")
    name: str = Field(..., description="Connector name")
    description: str = Field(..., description="Connector description")
    nexset_api_compatible: bool = Field(..., description="Whether compatible with Nexset API")


class RunInfo(BaseModel):
    """Run information"""
    id: int = Field(..., description="Run ID")
    created_at: datetime = Field(..., description="Run creation timestamp")


class DataSetBasic(BaseModel):
    """Basic DataSet information"""
    version: Optional[int] = Field(None, description="DataSet version")
    id: int = Field(..., description="DataSet ID")
    owner_id: int = Field(..., description="Owner ID")
    org_id: int = Field(..., description="Organization ID")
    name: str = Field(..., description="DataSet name")
    description: Optional[str] = Field(None, description="DataSet description")
    updated_at: datetime = Field(..., description="Last update timestamp")
    created_at: datetime = Field(..., description="Creation timestamp")


class SourceConfig(BaseModel):
    """Data source configuration"""
    source_config_property: Dict[str, Any] = Field(
        default_factory=dict,
        description="Source configuration properties"
    )


class VendorEndpoint(BaseModel):
    """Vendor endpoint information"""
    id: int = Field(..., description="Vendor endpoint ID")
    name: str = Field(..., description="Vendor endpoint name")
    display_name: str = Field(..., description="Vendor endpoint display name")


class Vendor(BaseModel):
    """Vendor information"""
    id: int = Field(..., description="Vendor ID")
    name: str = Field(..., description="Vendor name")
    display_name: str = Field(..., description="Vendor display name")
    connection_type: str = Field(..., description="Vendor connection type")


class Source(BaseModel):
    """Base Source model"""
    id: int = Field(..., description="Source ID")
    name: str = Field(..., description="Source name")
    description: Optional[str] = Field(None, description="Source description")
    status: str = Field(..., description="Source status")
    ingest_method: str = Field(..., description="Ingest method")
    source_format: str = Field(..., description="Source format")
    managed: bool = Field(..., description="Whether the source is managed")
    code_container_id: Optional[int] = Field(None, description="Code container ID")
    copied_from_id: Optional[int] = Field(None, description="ID of the source this was copied from")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    source_type: str = Field(..., description="Source type")
    connector_type: str = Field(..., description="Connector type")
    auto_generated: bool = Field(..., description="Whether the source was auto-generated")
    flow_type: str = Field(..., description="Flow type")
    
    # Relationships
    owner: Owner = Field(..., description="Source owner information")
    org: Organization = Field(..., description="Organization information")
    access_roles: List[AccessRole] = Field(..., description="Access roles for this source")
    data_sets: List[DataSetBasic] = Field(default_factory=list, description="DataSets associated with the source")
    connector: Connector = Field(..., description="Connector information")
    run_ids: List[RunInfo] = Field(default_factory=list, description="Run IDs associated with the source")
    tags: List[str] = Field(default_factory=list, description="Tags associated with the source")
    
    # Optional relationships
    has_template: Optional[bool] = Field(None, description="Whether the source has a template")
    vendor_endpoint: Optional[VendorEndpoint] = Field(None, description="Vendor endpoint information")
    vendor: Optional[Vendor] = Field(None, description="Vendor information")


class SourceList(BaseModel):
    """List of sources response"""
    items: List[Source] = Field(..., description="List of sources")


class SourceExpanded(Source):
    """Expanded source with additional details"""
    source_config: Dict[str, Any] = Field(
        default_factory=dict,
        description="Source configuration properties"
    )
    poll_schedule: Optional[Any] = Field(None, description="Poll schedule for the source")
    api_keys: List[Any] = Field(default_factory=list, description="API keys")
    data_credentials: Optional[Credential] = Field(None, description="Data credentials")

    class Config:
        """Configuration for the SourceExpanded model"""
        json_schema_extra = {
            "description": "Expanded source details including credentials and configuration"
        }
        populate_by_field_name = True


class ExpandedDataSet(DataSetBasic):
    """Expanded DataSet information with schema and transform details"""
    sample_service_id: Optional[Any] = Field(None, description="Sample service ID")
    source_schema: Optional[Dict[str, Any]] = Field(None, description="Source schema")
    transform: Optional[Dict[str, Any]] = Field(None, description="Transform configuration")
    output_schema: Optional[Dict[str, Any]] = Field(None, description="Output schema")


class SourceWithExpandedDataSets(SourceExpanded):
    """Source with expanded datasets information"""
    data_sets: List[ExpandedDataSet] = Field(default_factory=list, description="Expanded DataSets")

    class Config:
        """Configuration for the SourceWithExpandedDataSets model"""
        json_schema_extra = {
            "description": "Source with expanded datasets including schema and transform information"
        }


class CreateSourceRequest(BaseModel):
    """Request body for creating a source"""
    name: str = Field(..., description="Name of the source")
    description: Optional[str] = Field(None, description="Description of the source")
    data_credentials_id: Optional[int] = Field(
        None, 
        description="Nexla data credential ID containing authentication information"
    )
    source_type: SourceType = Field(
        ..., 
        description="Connector type codename"
    )
    source_config: Dict[str, Any] = Field(
        ..., 
        description="Source configuration properties"
    )


class CopySourceRequest(BaseModel):
    """Request body for copying a source"""
    reuse_data_credentials: Optional[bool] = Field(
        None, 
        description="Whether to reuse the credentials of the source"
    )
    copy_access_controls: Optional[bool] = Field(
        None, 
        description="Whether to copy access controls to the new source"
    )
    owner_id: Optional[int] = Field(
        None, 
        description="Owner ID for the new source"
    )
    org_id: Optional[int] = Field(
        None, 
        description="Organization ID for the new source"
    )


class DeleteSourceResponse(BaseModel):
    """Response for deleting a source"""
    code: str = Field(..., description="Response status code")
    message: str = Field(..., description="Response status text") 