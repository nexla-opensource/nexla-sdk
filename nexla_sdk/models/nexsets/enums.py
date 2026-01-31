from enum import Enum


class NexsetStatus(str, Enum):
    """Nexset status values."""

    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    DRAFT = "DRAFT"
    DELETED = "DELETED"
    ERROR = "ERROR"
    PROCESSING = "PROCESSING"


class TransformType(str, Enum):
    """Transform types."""

    JOLT_STANDARD = "jolt_standard"
    JOLT_CUSTOM = "jolt_custom"
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    SQL = "sql"


class OutputType(str, Enum):
    """Transform output types."""

    RECORD = "record"
    ATTRIBUTE = "attribute"
    CUSTOM = "custom"
