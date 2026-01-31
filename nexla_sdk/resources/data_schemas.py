from typing import List

from nexla_sdk.models.common import LogEntry
from nexla_sdk.resources.base_resource import BaseResource


class DataSchemasResource(BaseResource):
    """Resource for data schemas (accessors + audit log only)."""

    def __init__(self, client):
        super().__init__(client)
        self._path = "/data_schemas"
        self._model_class = None

    def get_audit_log(self, schema_id: int, **params) -> List[LogEntry]:
        path = f"{self._path}/{schema_id}/audit_log"
        response = self._make_request("GET", path, params=params)
        return [LogEntry.model_validate(item) for item in (response or [])]
