"""
Destination models for the Nexla SDK (Data Sinks)
"""
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field

from .common import Resource, PaginatedList, Status, ConnectorType, ResourceID
from .access import Owner, Organization, AccessRole
from .nexsets import Nexset, DataSet
from .credentials import Credential, CredentialExpanded, Connector, Vendor, VerifiedStatus


class SinkType(str, Enum):
    """Sink type enumeration"""
    AS400 = "as400"
    AZURE_BLB = "azure_blb"
    AZURE_DATA_LAKE = "azure_data_lake"
    AZURE_SYNAPSE = "azure_synapse"
    BIGQUERY = "bigquery"
    BOX = "box"
    CLOUDSQL_MYSQL = "cloudsql_mysql"
    CLOUDSQL_POSTGRES = "cloudsql_postgres"
    CLOUDSQL_SQLSERVER = "cloudsql_sqlserver"
    CONFLUENT_KAFKA = "confluent_kafka"
    DATA_MAP = "data_map"
    DATABRICKS = "databricks"
    DELTA_LAKE_AZURE_BLB = "delta_lake_azure_blb"
    DELTA_LAKE_AZURE_DATA_LAKE = "delta_lake_azure_data_lake"
    DELTA_LAKE_S3 = "delta_lake_s3"
    DROPBOX = "dropbox"
    DYNAMODB = "dynamodb"
    EMAIL = "email"
    FIREBASE = "firebase"
    FIREBOLT = "firebolt"
    FTP = "ftp"
    GCP_ALLOYDB = "gcp_alloydb"
    GCP_SPANNER = "gcp_spanner"
    GCS = "gcs"
    GDRIVE = "gdrive"
    GOOGLE_PUBSUB = "google_pubsub"
    JMS = "jms"
    KAFKA = "kafka"
    MIN_IO_S3 = "min_io_s3"
    MONGO = "mongo"
    MYSQL = "mysql"
    NETSUITE_JDBC = "netsuite_jdbc"
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
    SNOWFLAKE_DCR = "snowflake_dcr"
    SQLSERVER = "sqlserver"
    TERADATA = "teradata"
    TIBCO = "tibco"


class SinkStatus(str, Enum):
    """Data sink status enumeration"""
    ACTIVE = "active"
    PAUSED = "paused"
    ERROR = "error"
    PENDING = "pending"
    DELETED = "deleted"


class VendorEndpoint(BaseModel):
    """Vendor endpoint information"""
    id: int = Field(..., description="Endpoint ID")
    name: str = Field(..., description="Endpoint name")
    display_name: str = Field(..., description="Display name")


class DataSetSummary(BaseModel):
    """Basic data set information"""
    id: int = Field(..., description="Data set ID")
    name: str = Field(..., description="Data set name")


class DataMapSummary(BaseModel):
    """Basic data map information"""
    id: int = Field(..., description="Data map ID")
    owner_id: int = Field(..., description="Owner ID")
    org_id: int = Field(..., description="Organization ID")
    name: str = Field(..., description="Data map name")
    description: str = Field(..., description="Data map description")
    public: bool = Field(..., description="Whether the data map is public")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")


class DataSetExpanded(BaseModel):
    """Data set expanded information"""
    id: int = Field(..., description="Data set ID")
    name: str = Field(..., description="Data set name")
    description: str = Field(..., description="Data set description")
    output_schema: Optional[Dict[str, Any]] = Field(None, description="Output schema")
    status: str = Field(..., description="Status")
    updated_at: datetime = Field(..., description="Last update timestamp")
    created_at: datetime = Field(..., description="Creation timestamp")
    version: Optional[int] = Field(None, description="Version number")


class DestinationConfig(BaseModel):
    """Data destination configuration"""
    sink_config: Dict[str, Any] = Field(..., description="Sink configuration properties")
    sink_format: Optional[str] = Field(None, description="Sink format")
    sink_schedule: Optional[Dict[str, Any]] = Field(None, description="Sink schedule")


class CreateDataSinkRequest(BaseModel):
    """Request model for creating a data sink"""
    name: str = Field(..., description="Data sink name")
    description: Optional[str] = Field(None, description="Data sink description")
    data_credentials_id: int = Field(..., description="Data credential ID")
    data_set_id: int = Field(..., description="Data set ID")
    sink_type: str = Field(..., description="Sink type")
    sink_config: Dict[str, Any] = Field(..., description="Sink configuration")
    tags: Optional[List[str]] = Field(None, description="Tags")


class UpdateDataSinkRequest(BaseModel):
    """Request model for updating a data sink"""
    name: Optional[str] = Field(None, description="Data sink name")
    description: Optional[str] = Field(None, description="Data sink description")
    data_credentials_id: Optional[int] = Field(None, description="Data credential ID")
    data_set_id: Optional[int] = Field(None, description="Data set ID")
    sink_type: Optional[str] = Field(None, description="Sink type")
    sink_config: Optional[Dict[str, Any]] = Field(None, description="Sink configuration")
    tags: Optional[List[str]] = Field(None, description="Tags")


class CopyDataSinkRequest(BaseModel):
    """Request model for copying a data sink"""
    reuse_data_credentials: Optional[bool] = Field(None, description="Whether to reuse the credentials")
    copy_access_controls: Optional[bool] = Field(None, description="Whether to copy access controls")
    owner_id: Optional[int] = Field(None, description="Owner ID for the new sink")
    org_id: Optional[int] = Field(None, description="Organization ID for the new sink")


class DeleteDataSinkResponse(BaseModel):
    """Response model for deleting a data sink"""
    code: str = Field(..., description="Response status code")
    message: str = Field(..., description="Response status text")


class DataSink(Resource):
    """Data sink model"""
    id: int = Field(..., description="Data sink ID")
    owner: Optional[Owner] = Field(None, description="Owner information")
    org: Optional[Organization] = Field(None, description="Organization information")
    access_roles: Optional[List[AccessRole]] = Field(None, description="Access roles")
    name: str = Field(..., description="Data sink name")
    description: Optional[str] = Field(None, description="Data sink description")
    status: str = Field(..., description="Data sink status")
    data_set_id: Optional[int] = Field(None, description="Data set ID")
    data_map_id: Optional[int] = Field(None, description="Data map ID")
    data_source_id: Optional[int] = Field(None, description="Data source ID")
    sink_format: Optional[str] = Field(None, description="Sink format")
    sink_config: Optional[Dict[str, Any]] = Field(None, description="Sink configuration")
    sink_schedule: Optional[Dict[str, Any]] = Field(None, description="Sink schedule")
    in_memory: Optional[bool] = Field(None, description="Whether the sink is in-memory")
    managed: bool = Field(..., description="Whether the sink is managed")
    sink_type: str = Field(..., description="Sink type")
    connector_type: str = Field(..., description="Connector type")
    connector: Optional[Connector] = Field(None, description="Connector information")
    data_set: Optional[Union[DataSetSummary, DataSetExpanded]] = Field(None, description="Data set information")
    data_map: Optional[DataMapSummary] = Field(None, description="Data map information")
    data_credentials: Optional[Union[Credential, CredentialExpanded]] = Field(None, description="Data credential information")
    copied_from_id: Optional[int] = Field(None, description="ID of the sink this was copied from")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    tags: Optional[List[str]] = Field(None, description="Tags")
    flow_type: Optional[str] = Field(None, description="Flow type")
    has_template: Optional[bool] = Field(None, description="Whether the sink has a template")
    vendor_endpoint: Optional[VendorEndpoint] = Field(None, description="Vendor endpoint information")
    vendor: Optional[Vendor] = Field(None, description="Vendor information")


class DataSinkList(PaginatedList[DataSink]):
    """Paginated list of data sinks"""
    pass


class Destination(DataSink):
    """Legacy Destination model for backward compatibility"""
    pass


class DestinationList(PaginatedList[Destination]):
    """Paginated list of destinations (for backward compatibility)"""
    pass 