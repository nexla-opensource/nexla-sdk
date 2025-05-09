"""
Source metrics models for the Nexla SDK
"""
from typing import List, Dict, Any, Optional, Union
from datetime import datetime, date
from enum import Enum
from pydantic import BaseModel, Field


class SourceMetricsResponse(BaseModel):
    """Response for source lifetime metrics"""
    status: int = Field(..., description="Status code")
    metrics: Dict[str, int] = Field(..., description="Metrics data")


class DailyMetric(BaseModel):
    """Daily metric for a source"""
    time: str = Field(..., description="Date of the metrics (YYYY-MM-DD)")
    record: int = Field(..., description="Total number of records processed")
    size: int = Field(..., description="Total volume in bytes of records processed")


class AggregatedMetricsResponse(BaseModel):
    """Response for aggregated metrics"""
    status: int = Field(..., description="Status code")
    metrics: List[DailyMetric] = Field(..., description="List of daily metrics")


class RunMetric(BaseModel):
    """Metrics for a specific ingestion run"""
    records: int = Field(..., description="Total number of records processed")
    size: int = Field(..., description="Total volume in bytes of records processed")
    errors: int = Field(..., description="Total number of errors during processing")


class RunMetricsData(BaseModel):
    """Paginated run metrics data"""
    data: Dict[str, RunMetric] = Field(default_factory=dict, description="Run metrics by run ID")
    meta: Dict[str, Any] = Field(..., description="Pagination metadata")


class RunMetricsResponse(BaseModel):
    """Response for run metrics"""
    status: int = Field(..., description="Status code")
    metrics: RunMetricsData = Field(..., description="Run metrics with pagination")


class FileStatus(str, Enum):
    """File ingestion status"""
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETE = "COMPLETE"
    ERROR = "ERROR"
    PARTIAL = "PARTIAL"


class FileStatsResponse(BaseModel):
    """Response for file status metrics"""
    status: int = Field(..., description="Status code")
    metrics: Dict[str, Dict[str, int]] = Field(..., description="Files stats by status")


class FileMeta(BaseModel):
    """Pagination metadata for file metrics"""
    currentPage: int = Field(..., description="Current page number")
    totalCount: int = Field(..., description="Total count of files")
    pageCount: int = Field(..., description="Total number of pages")


class FileMetric(BaseModel):
    """Metrics for a specific file"""
    dataSourceId: int = Field(..., description="Data source ID")
    dataSetId: Optional[int] = Field(None, description="Dataset ID")
    size: int = Field(..., description="File size in bytes")
    ingestionStatus: FileStatus = Field(..., description="Ingestion status")
    recordCount: int = Field(..., description="Number of records in file")
    name: Optional[str] = Field(None, description="File name/path")
    id: Optional[int] = Field(None, description="File ID")
    lastModified: Optional[datetime] = Field(None, description="Last modified timestamp")
    error: Optional[str] = Field(None, description="Error message if any")
    lastIngested: Optional[datetime] = Field(None, description="Last ingestion timestamp")
    errorCount: Optional[int] = Field(None, description="Number of errors")


class FileMetricsData(BaseModel):
    """File metrics data with pagination"""
    data: List[FileMetric] = Field(..., description="List of file metrics")
    meta: FileMeta = Field(..., description="Pagination metadata")


class FileMetricsResponse(BaseModel):
    """Response for file metrics"""
    status: int = Field(..., description="Status code")
    metrics: FileMetricsData = Field(..., description="File metrics with pagination")


class RawFileMetric(FileMetric):
    """Raw metrics for a specific file including all ingestion attempts"""
    pass


class RawFileMetricsResponse(BaseModel):
    """Response for raw file metrics"""
    status: int = Field(..., description="Status code")
    metrics: List[RawFileMetric] = Field(..., description="List of raw file metrics")


class CronFileMetric(FileMetric):
    """Metrics for a file in a specific cron/scheduled run"""
    runId: Optional[int] = Field(None, description="Run ID of the ingestion cycle")


class CronFileMetricsResponse(BaseModel):
    """Response for cron file metrics"""
    data: List[CronFileMetric] = Field(..., description="List of cron file metrics")
    meta: FileMeta = Field(..., description="Pagination metadata")


class ConfigValidationField(BaseModel):
    """Validation result for a config field"""
    name: str = Field(..., description="Field name")
    value: Optional[Any] = Field(None, description="Current value")
    errors: List[str] = Field(..., description="List of validation errors")
    visible: bool = Field(..., description="Whether the field is visible")
    recommendedValues: List[Any] = Field(..., description="Recommended values")


class ConfigValidationResponse(BaseModel):
    """Response for config validation"""
    status: str = Field(..., description="Status (ok/error)")
    output: List[ConfigValidationField] = Field(..., description="Validation output")


class ProbeTreeResponse(BaseModel):
    """Response for content hierarchy probe"""
    status: str = Field(..., description="Status (ok/error)")
    output: Dict[str, Any] = Field(..., description="Hierarchical output of directories and files")
    connection_type: str = Field(..., description="Connection type (s3, ftp, etc.)")


class FileSampleMessage(BaseModel):
    """Sample record from a file"""
    pass  # This is a dynamic model that will hold any key/value pairs


class FileSampleOutput(BaseModel):
    """Output from a file sample probe"""
    format: str = Field(..., description="File format (json, csv, etc.)")
    messages: List[FileSampleMessage] = Field(..., description="Sample records")


class FileSampleResponse(BaseModel):
    """Response for file sample probe"""
    status: int = Field(..., description="Status code")
    message: str = Field(..., description="Status message")
    output: FileSampleOutput = Field(..., description="Sample output")
    connection_type: str = Field(..., description="Connection type (s3, ftp, etc.)")


class ReingestionResponse(BaseModel):
    """Response for file reingestion"""
    status: str = Field(..., description="Status (ok/error)") 