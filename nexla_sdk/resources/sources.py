from typing import List, Optional, Dict, Any
from nexla_sdk.resources.base_resource import BaseResource
from nexla_sdk.models.sources.responses import Source
from nexla_sdk.models.sources.requests import SourceCopyOptions


class SourcesResource(BaseResource):
    """Resource for managing data sources."""
    
    def __init__(self, client):
        super().__init__(client)
        self._path = "/data_sources"
        self._model_class = Source
    
    def copy(self, source_id: int, options: Optional[SourceCopyOptions] = None) -> Source:
        """
        Copy a source.
        
        Args:
            source_id: Source ID
            options: Copy options
        
        Returns:
            Copied source
        """
        data = options.to_dict() if options else {}
        return super().copy(source_id, data)