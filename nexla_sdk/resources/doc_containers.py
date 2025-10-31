from typing import List, Dict, Any
from nexla_sdk.resources.base_resource import BaseResource
from nexla_sdk.models.common import LogEntry


class DocContainersResource(BaseResource):
    """Resource for document containers accessors and audit logs."""

    def __init__(self, client):
        super().__init__(client)
        self._path = "/doc_containers"
        self._model_class = None

    def get_audit_log(self, doc_container_id: int, **params) -> List[LogEntry]:
        path = f"{self._path}/{doc_container_id}/audit_log"
        response = self._make_request('GET', path, params=params)
        return [LogEntry.model_validate(item) for item in (response or [])]

    # Accessors via BaseResource methods are compatible
    # get_accessors, add_accessors, replace_accessors, delete_accessors
