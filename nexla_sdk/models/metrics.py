"""
Metrics models for the Nexla SDK
"""
from typing import Dict, List, Optional, Union, Any
from datetime import datetime, date
from enum import Enum
from pydantic import BaseModel, Field, model_validator


class AccessRole(str, Enum):
    """Access role types for metrics queries"""
    COLLABORATOR = "collaborator"
    OPERATOR = "operator"
    ADMIN = "admin"
    OWNER = "owner"


class MetricsStatus(str, Enum):
    """Metrics status types"""
    OK = "OK"
    WARNING = "WARNING"
    ERROR = "ERROR"


class AccountMetricData(BaseModel):
    """Data for account metrics"""
    records: int = Field(..., description="Total number of records processed")
    size: int = Field(..., description="Total volume of records processed in bytes")
    pipeline_count: Optional[int] = Field(None, description="Count of pipelines")


class AccountMetric(BaseModel):
    """Account metric for a time period"""
    data: AccountMetricData = Field(..., description="Metric data")
    start_time: datetime = Field(..., description="Start time of metrics period")
    end_time: datetime = Field(..., description="End time of metrics period")


class AccountMetricsResponse(BaseModel):
    """Response for account metrics"""
    status: int = Field(..., description="Status of the report request")
    metrics: Union[List[AccountMetric], AccountMetric] = Field(..., description="Account metrics")
    
    @model_validator(mode='before')
    @classmethod
    def handle_single_metric(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle both list and single metric responses"""
        if isinstance(data, dict) and "metrics" in data:
            metrics = data["metrics"]
            # If metrics is a dict with start_time/end_time, wrap it in a list
            if isinstance(metrics, dict) and "start_time" in metrics and "end_time" in metrics:
                # It's a direct metric object, not a list
                return data
            elif isinstance(metrics, dict) and "data" in metrics:
                # New format where metrics has data inside it
                return data
                
        return data


class ResourceMetric(BaseModel):
    """Metrics for a resource (source, sink, or dataset)"""
    records: int = Field(..., description="Total number of records processed")
    size: int = Field(..., description="Total volume in bytes of records processed")
    errors: int = Field(..., description="Total number of data processing errors")
    status: MetricsStatus = Field(..., description="Status of the resource")


class DashboardMetrics(BaseModel):
    """Dashboard metrics for all resources"""
    sources: Optional[Dict[str, ResourceMetric]] = Field(default_factory=dict, description="Source metrics by ID")
    sinks: Optional[Dict[str, ResourceMetric]] = Field(default_factory=dict, description="Sink metrics by ID")
    datasets: Optional[Dict[str, ResourceMetric]] = Field(default_factory=dict, description="Dataset metrics by ID")
    start_time: datetime = Field(..., description="Start time of metrics period")
    end_time: datetime = Field(..., description="End time of metrics period")


class DashboardResponse(BaseModel):
    """Response for dashboard metrics"""
    status: int = Field(..., description="Status of the report request")
    metrics: DashboardMetrics = Field(..., description="Dashboard metrics")


class DailyMetric(BaseModel):
    """Daily metric for a date"""
    time: date = Field(..., description="Date of the metrics")
    records: int = Field(..., description="Total number of records processed")
    size: int = Field(..., description="Total volume in bytes of records processed")
    errors: int = Field(..., description="Total number of data processing errors")


class DailyMetricsResponse(BaseModel):
    """Response for daily metrics"""
    status: int = Field(..., description="Status of the report request")
    metrics: List[DailyMetric] = Field(..., description="Daily metrics")


class ResourceType(str, Enum):
    """Resource types for metrics queries"""
    DATA_SOURCES = "data_sources"
    DATA_SINKS = "data_sinks"
    DATA_SETS = "data_sets"


class MetaPagination(BaseModel):
    """Pagination metadata for metrics responses"""
    currentPage: int = Field(..., description="Current page that this response corresponds to")
    pageCount: int = Field(..., description="Total number of valid pages of metrics data given the current page size")
    totalCount: int = Field(..., description="Total number of metrics entries that are available for this resource")


class RunMetric(BaseModel):
    """Metrics for a specific run"""
    runId: Optional[int] = Field(None, description="The run ID / ingestion cycle the metrics are applicable for")
    lastWritten: Optional[int] = Field(None, description="The destination write batch id the metrics are applicable for")
    dataSetId: Optional[int] = Field(None, description="The Nexset ID these records were applicable for")
    records: int = Field(..., description="Total number of records processed")
    size: int = Field(..., description="Total volume in bytes of records processed")
    errors: int = Field(..., description="Total number of data processing errors")


class RunMetricsData(BaseModel):
    """Run metrics data with pagination"""
    data: List[RunMetric] = Field(..., description="Metrics data for each run")
    meta: MetaPagination = Field(..., description="Pagination metadata")


class RunMetricsResponse(BaseModel):
    """Response for run metrics"""
    status: int = Field(..., description="Status of the report request")
    metrics: RunMetricsData = Field(..., description="Run metrics with pagination")


class ResourceMetricData(BaseModel):
    """Metric data for a specific resource"""
    id: int = Field(..., description="Resource ID")
    metric: dict = Field(..., description="Metric data including records, size, and errors")


class FlowMetricsData(BaseModel):
    """Flow metrics data structure"""
    data_sources: Optional[List[ResourceMetricData]] = Field(None, description="Metrics for data sources in the flow")
    data_sets: Optional[List[ResourceMetricData]] = Field(None, description="Metrics for data sets in the flow")
    data_sinks: Optional[List[ResourceMetricData]] = Field(None, description="Metrics for data sinks in the flow")


class FlowRunMetricsData(BaseModel):
    """Flow metrics data grouped by run ID"""
    data: Union[Dict[str, FlowMetricsData], FlowMetricsData] = Field(..., description="Flow metrics data, possibly grouped by run ID")
    meta: Optional[MetaPagination] = Field(None, description="Pagination metadata")


class FlowMetricsResponse(BaseModel):
    """Response for flow metrics"""
    status: int = Field(..., description="Status of the report request")
    message: Optional[str] = Field(None, description="Status message")
    metrics: FlowRunMetricsData = Field(..., description="Flow metrics data")


class LogType(str, Enum):
    """Log entry types for flow logs"""
    LOG = "LOG"
    SUMMARY = "SUMMARY"


class LogSeverity(str, Enum):
    """Severity levels for flow logs"""
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


class FlowLogEntry(BaseModel):
    """A log entry from flow execution"""
    timestamp: int = Field(..., description="Timestamp at which this log entry was generated")
    resource_id: int = Field(..., description="The ID of the resource that generated this log entry")
    resource_type: str = Field(..., description="The type of flow resource that generated this log entry")
    log: str = Field(..., description="Detailed information about the data processing events on the flow resource")
    log_type: LogType = Field(..., description="Indicates the type of event reflected by log entry")
    severity: LogSeverity = Field(..., description="Indicates the severity of the event reflected by this log entry")


class FlowLogMetadata(BaseModel):
    """Metadata for flow logs"""
    current_page: int = Field(..., description="Current page that this response corresponds to")
    pages_count: int = Field(..., description="Total number of valid pages of logs data given the current page size")
    total_count: int = Field(..., description="Total number of log entries that are available for this resource")
    org_id: int = Field(..., description="The id of the organization this flow belongs to")
    run_id: int = Field(..., description="The run id (denoting ingestion cycle) that these log were generated as part of")


class FlowLogsData(BaseModel):
    """Flow logs data with pagination"""
    data: List[FlowLogEntry] = Field(..., description="Flow log entries")
    meta: FlowLogMetadata = Field(..., description="Log pagination metadata")


class FlowLogsResponse(BaseModel):
    """Response for flow logs"""
    status: int = Field(..., description="Status of the report request")
    message: str = Field(..., description="Message signifying status of the report request")
    logs: FlowLogsData = Field(..., description="Flow logs data with pagination") 