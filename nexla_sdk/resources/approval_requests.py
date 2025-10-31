from typing import List, Dict, Any
from nexla_sdk.resources.base_resource import BaseResource
from nexla_sdk.models.approval_requests.responses import ApprovalRequest


class ApprovalRequestsResource(BaseResource):
    """Resource for managing approval requests."""

    def __init__(self, client):
        super().__init__(client)
        self._path = "/approval_requests"
        self._model_class = ApprovalRequest

    def list_pending(self) -> List[ApprovalRequest]:
        path = f"{self._path}/pending"
        response = self._make_request('GET', path)
        return self._parse_response(response)

    def list_requested(self) -> List[ApprovalRequest]:
        path = f"{self._path}/requested"
        response = self._make_request('GET', path)
        return self._parse_response(response)

    def approve(self, request_id: int) -> ApprovalRequest:
        path = f"{self._path}/{request_id}/approve"
        response = self._make_request('PUT', path)
        return self._parse_response(response)

    def reject(self, request_id: int, reason: str = "") -> ApprovalRequest:
        path = f"{self._path}/{request_id}/reject"
        body = {"reason": reason} if reason else {}
        response = self._make_request('DELETE', path, json=body)
        return self._parse_response(response)
