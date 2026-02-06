from typing import Any, Dict, List, Optional, Union

from nexla_sdk.models.flows.requests import FlowCopyOptions
from nexla_sdk.models.flows.responses import (
    DocsRecommendation,
    FlowLogsResponse,
    FlowMetricsApiResponse,
    FlowResponse,
)
from nexla_sdk.resources.base_resource import BaseResource


class FlowsResource(BaseResource):
    """Resource for managing data flows."""

    def __init__(self, client):
        super().__init__(client)
        self._path = "/flows"
        self._model_class = FlowResponse

    def list(
        self,
        flows_only: bool = False,
        include_run_metrics: bool = False,
        access_role: Optional[str] = None,
        **kwargs,
    ) -> List[FlowResponse]:
        """
        List flows with optional filters.

        Args:
            flows_only: Only return flow structure without resource details
            include_run_metrics: Include run metrics in response
            access_role: Filter by access role (owner, collaborator, operator, admin)
            page: Page number (via kwargs)
            per_page: Items per page (via kwargs)
            **kwargs: Additional query parameters

        Returns:
            List of flows

        Examples:
            client.flows.list(flows_only=True)
            client.flows.list(include_run_metrics=True, page=1, per_page=50)
            client.flows.list(access_role="owner")
        """
        params = kwargs.copy()
        if flows_only:
            params["flows_only"] = 1
        if include_run_metrics:
            params["include_run_metrics"] = 1
        if access_role:
            params["access_role"] = access_role

        response = self._make_request("GET", self._path, params=params)
        # API returns a single FlowResponse object for list
        return [self._parse_response(response)]

    def get(
        self, flow_id: int, flows_only: bool = False, include_run_metrics: bool = False
    ) -> FlowResponse:
        """
        Get flow by ID.

        Args:
            flow_id: Flow ID
            flows_only: Only return flow structure without resource details
            include_run_metrics: Include run metrics in response

        Returns:
            Flow response
        """
        path = f"{self._path}/{flow_id}"
        params = {}
        if flows_only:
            params["flows_only"] = 1
        if include_run_metrics:
            params["include_run_metrics"] = 1
        response = self._make_request("GET", path, params=params)
        return self._parse_response(response)

    def get_by_resource(
        self, resource_type: str, resource_id: int, flows_only: bool = False
    ) -> FlowResponse:
        """
        Get flow by resource ID.

        Args:
            resource_type: Type of resource (data_sources, data_sets, data_sinks)
            resource_id: Resource ID
            flows_only: Only return flow structure

        Returns:
            Flow response
        """
        path = f"/{resource_type}/{resource_id}/flow"
        params = {"flows_only": 1} if flows_only else {}

        response = self._make_request("GET", path, params=params)
        return self._parse_response(response)

    def activate(
        self, flow_id: int, all: bool = False, full_tree: bool = False
    ) -> FlowResponse:
        """
        Activate a flow.

        Args:
            flow_id: Flow ID
            all: Activate entire flow tree

        Returns:
            Activated flow
        """
        path = f"{self._path}/{flow_id}/activate"
        params = {}
        if all:
            params["all"] = 1
        if full_tree:
            params["full_tree"] = 1

        response = self._make_request("PUT", path, params=params)
        return self._parse_response(response)

    def pause(
        self,
        flow_id: int,
        all: bool = False,
        full_tree: bool = False,
        async_mode: bool = False,
    ) -> FlowResponse:
        """
        Pause a flow.

        Args:
            flow_id: Flow ID
            all: Pause entire flow tree
            full_tree: Alias for 'all' parameter
            async_mode: Execute pause asynchronously

        Returns:
            Paused flow
        """
        path = f"{self._path}/{flow_id}/pause"
        params = {}
        if all:
            params["all"] = 1
        if full_tree:
            params["full_tree"] = 1
        if async_mode:
            params["async"] = 1

        response = self._make_request("PUT", path, params=params)
        return self._parse_response(response)

    def copy(
        self, flow_id: int, options: Optional[FlowCopyOptions] = None
    ) -> FlowResponse:
        """
        Copy a flow.

        Args:
            flow_id: Flow ID
            options: Copy options

        Returns:
            Copied flow
        """
        return super().copy(flow_id, options)

    def delete(self, flow_id: int) -> Dict[str, Any]:
        """
        Delete flow.

        Args:
            flow_id: Flow ID

        Returns:
            Response with status
        """
        return super().delete(flow_id)

    def delete_by_resource(
        self, resource_type: str, resource_id: int
    ) -> Dict[str, Any]:
        """
        Delete flow by resource ID.

        Args:
            resource_type: Type of resource
            resource_id: Resource ID

        Returns:
            Response status
        """
        path = f"/{resource_type}/{resource_id}/flow"
        return self._make_request("DELETE", path)

    def activate_by_resource(
        self,
        resource_type: str,
        resource_id: int,
        all: bool = False,
        full_tree: bool = False,
    ) -> FlowResponse:
        """
        Activate flow by resource ID.

        Args:
            resource_type: Type of resource
            resource_id: Resource ID
            all: Activate entire flow tree

        Returns:
            Activated flow
        """
        path = f"/{resource_type}/{resource_id}/activate"
        params = {}
        if all:
            params["all"] = 1
        if full_tree:
            params["full_tree"] = 1

        response = self._make_request("PUT", path, params=params)
        return self._parse_response(response)

    def pause_by_resource(
        self,
        resource_type: str,
        resource_id: int,
        all: bool = False,
        full_tree: bool = False,
    ) -> FlowResponse:
        """
        Pause flow by resource ID.

        Args:
            resource_type: Type of resource
            resource_id: Resource ID
            all: Pause entire flow tree

        Returns:
            Paused flow
        """
        path = f"/{resource_type}/{resource_id}/pause"
        params = {}
        if all:
            params["all"] = 1
        if full_tree:
            params["full_tree"] = 1

        response = self._make_request("PUT", path, params=params)
        return self._parse_response(response)

    def update_by_resource(self, resource_type: str, resource_id: int, payload: Dict[str, Any]) -> FlowResponse:
        path = f"/{resource_type}/{resource_id}/flow"
        response = self._make_request("PUT", path, json=payload)
        return self._parse_response(response)

    def copy_by_resource(self, resource_type: str, resource_id: int, payload: Optional[Dict[str, Any]] = None) -> FlowResponse:
        path = f"/{resource_type}/{resource_id}/flow/copy"
        response = self._make_request("POST", path, json=payload or {})
        return self._parse_response(response)

    def accessors_by_resource(
        self, resource_type: str, resource_id: int, mode: str = "list", payload: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        path = f"/{resource_type}/{resource_id}/flow/accessors"
        method_map = {"list": "GET", "reset": "POST", "add": "PUT", "remove": "DELETE"}
        method = method_map.get(mode, "GET")
        return self._make_request(method, path, json=payload or {})

    def docs_by_resource(
        self, resource_type: str, resource_id: int, mode: str = "list", payload: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        path = f"/{resource_type}/{resource_id}/flow/docs"
        method_map = {"list": "GET", "reset": "POST", "add": "PUT", "remove": "DELETE"}
        method = method_map.get(mode, "GET")
        return self._make_request(method, path, json=payload or [])

    def run_status_by_resource(self, resource_type: str, resource_id: int) -> Dict[str, Any]:
        path = f"/{resource_type}/{resource_id}/flow/run_status"
        return self._make_request("GET", path)

    def run_profiles_activate(self, flow_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
        path = f"{self._path}/{flow_id}/run_profiles/activate"
        return self._make_request("POST", path, json=payload)

    def run_now(self, flow_id: int, method: str = "POST") -> Dict[str, Any]:
        path = f"{self._path}/{flow_id}/run_now"
        return self._make_request(method.upper(), path)

    def flow_logs(self, flow_id: int, **params) -> Dict[str, Any]:
        path = f"{self._path}/{flow_id}/logs"
        return self._make_request("GET", path, params=params)

    def flow_logs_v2(self, flow_id: int, payload: Dict[str, Any], **params) -> Dict[str, Any]:
        path = f"{self._path}/{flow_id}/logs_v2"
        return self._make_request("POST", path, json=payload, params=params)

    def flow_metrics(self, flow_id: int, **params) -> Dict[str, Any]:
        path = f"{self._path}/{flow_id}/metrics"
        return self._make_request("GET", path, params=params)

    def list_linked_flows(self, flow_id: int) -> Dict[str, Any]:
        path = f"{self._path}/{flow_id}/links"
        return self._make_request("GET", path)

    def create_linked_flows(self, flow_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
        path = f"{self._path}/{flow_id}/links"
        return self._make_request("POST", path, json=payload)

    def update_linked_flows(self, flow_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
        path = f"{self._path}/{flow_id}/links"
        return self._make_request("PUT", path, json=payload)

    def delete_linked_flows(self, flow_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
        path = f"{self._path}/{flow_id}/links"
        return self._make_request("DELETE", path, json=payload)

    def delete_all_linked_flows(self, flow_id: int) -> Dict[str, Any]:
        path = f"{self._path}/{flow_id}/links/all"
        return self._make_request("DELETE", path)

    def insert_flow_node(self, flow_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
        path = f"{self._path}/{flow_id}/insert_flow_node"
        return self._make_request("POST", path, json=payload)

    def remove_flow_node(self, flow_id: int, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        path = f"{self._path}/{flow_id}/remove_flow_node"
        return self._make_request("POST", path, json=payload or {})

    def update_samples(self, flow_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
        path = f"{self._path}/{flow_id}/samples"
        return self._make_request("PUT", path, json=payload)

    def publish_rag(self, flow_id: int) -> Dict[str, Any]:
        path = f"{self._path}/{flow_id}/rag/publish"
        return self._make_request("PUT", path)

    def update_archival_status(self, flow_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
        path = f"{self._path}/{flow_id}/archival/status"
        return self._make_request("POST", path, json=payload)

    def restore_archival(self, flow_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
        path = f"{self._path}/{flow_id}/archival/restore"
        return self._make_request("POST", path, json=payload)

    def run_status(self, flow_id: int, run_id: Optional[int] = None) -> Dict[str, Any]:
        path = f"{self._path}/{flow_id}/run_status"
        if run_id is not None:
            path = f"{path}/{run_id}"
        return self._make_request("GET", path)

    def search(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request("POST", f"{self._path}/search", json=payload)

    def bulk_assign_project(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request("PUT", f"{self._path}/project", json=payload)

    def import_flow(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request("POST", f"{self._path}/import", json=payload)

    def publish_raw(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request("POST", f"{self._path}/raw", json=payload)

    def daily_metrics(self, **params) -> Dict[str, Any]:
        return self._make_request("GET", "/data_flows/metrics/daily", params=params)

    def total_metrics(self, **params) -> Dict[str, Any]:
        return self._make_request("GET", "/data_flows/metrics/total", params=params)

    def active_flows_metrics(self, **params) -> Dict[str, Any]:
        return self._make_request(
            "GET", "/data_flows/metrics/active_flows_metrics", params=params
        )

    def get_resources_access(self, flow_id: int) -> Dict[str, Any]:
        return self._make_request("GET", f"{self._path}/{flow_id}/resources_access")

    def docs_recommendation(
        self, flow_id: int
    ) -> Union[DocsRecommendation, Dict[str, Any]]:
        """Generate AI suggestion for flow documentation.

        Args:
            flow_id: Flow ID

        Returns:
            DocsRecommendation with AI-generated documentation suggestion,
            or raw dict if response doesn't match expected schema.
        """
        path = f"{self._path}/{flow_id}/docs/recommendation"
        response = self._make_request("POST", path)
        try:
            return DocsRecommendation.model_validate(response)
        except Exception:
            return response

    def get_logs(
        self,
        resource_type: str,
        resource_id: int,
        run_id: int,
        from_ts: int,
        to_ts: Optional[int] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> Union[FlowLogsResponse, Dict[str, Any]]:
        """Get flow execution logs for a specific run id of a flow.

        Args:
            resource_type: Type of resource (data_sources, data_sets, data_sinks)
            resource_id: Resource ID
            run_id: Run ID to get logs for
            from_ts: Start timestamp (Unix timestamp)
            to_ts: End timestamp (Unix timestamp)
            page: Page number for pagination
            per_page: Items per page

        Returns:
            FlowLogsResponse with log entries and pagination metadata,
            or raw dict if response doesn't match expected schema.
        """
        path = f"/data_flows/{resource_type}/{resource_id}/logs"
        params = {
            "run_id": run_id,
            "from": from_ts,
        }
        if to_ts is not None:
            params["to"] = to_ts
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page
        response = self._make_request("GET", path, params=params)
        try:
            return FlowLogsResponse.model_validate(response)
        except Exception:
            return response

    def get_metrics(
        self,
        resource_type: str,
        resource_id: int,
        from_date: str,
        to_date: Optional[str] = None,
        groupby: Optional[str] = None,
        orderby: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> Union[FlowMetricsApiResponse, Dict[str, Any]]:
        """Get flow metrics for a flow node keyed by resource id.

        Args:
            resource_type: Type of resource (data_sources, data_sets, data_sinks)
            resource_id: Resource ID
            from_date: Start date (ISO format, e.g., '2023-01-17')
            to_date: End date (ISO format)
            groupby: Group metrics by field (e.g., 'runId')
            orderby: Order results by field ('runId' or 'created_at')
            page: Page number for pagination
            per_page: Items per page

        Returns:
            FlowMetricsApiResponse with metrics data and pagination,
            or raw dict if response doesn't match expected schema.
        """
        path = f"/data_flows/{resource_type}/{resource_id}/metrics"
        params = {"from": from_date}
        if to_date:
            params["to"] = to_date
        if groupby:
            params["groupby"] = groupby
        if orderby:
            params["orderby"] = orderby
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page

        response = self._make_request("GET", path, params=params)
        try:
            return FlowMetricsApiResponse.model_validate(response)
        except Exception:
            return response
