from typing import List, Optional, Dict, Any
from nexla_sdk.resources.base_resource import BaseResource
from nexla_sdk.models.sources.responses import Source
from nexla_sdk.models.sources.requests import SourceCreate, SourceUpdate, SourceCopyOptions


class SourcesResource(BaseResource):
    """Resource for managing data sources."""
    
    def __init__(self, client):
        super().__init__(client)
        self._path = "/data_sources"
        self._model_class = Source
    
    def list(self, **kwargs) -> List[Source]:
        """
        List all sources.
        
        Args:
            **kwargs: Additional parameters (page, per_page, access_role, etc.)
        
        Returns:
            List of sources
        """
        return super().list(**kwargs)
    
    def get(self, source_id: int, expand: bool = False) -> Source:
        """
        Get single source by ID.
        
        Args:
            source_id: Source ID
            expand: Include expanded references
        
        Returns:
            Source instance
        """
        return super().get(source_id, expand)
    
    def create(self, data: SourceCreate) -> Source:
        """
        Create new source.
        
        Args:
            data: Source creation data
        
        Returns:
            Created source
        """
        return super().create(data)
    
    def update(self, source_id: int, data: SourceUpdate) -> Source:
        """
        Update source.
        
        Args:
            source_id: Source ID
            data: Updated source data
        
        Returns:
            Updated source
        """
        return super().update(source_id, data)
    
    def delete(self, source_id: int) -> Dict[str, Any]:
        """
        Delete source.
        
        Args:
            source_id: Source ID
        
        Returns:
            Response with status
        """
        return super().delete(source_id)
    
    def activate(self, source_id: int) -> Source:
        """
        Activate source.
        
        Args:
            source_id: Source ID
        
        Returns:
            Activated source
        """
        return super().activate(source_id)
    
    def pause(self, source_id: int) -> Source:
        """
        Pause source.
        
        Args:
            source_id: Source ID
        
        Returns:
            Paused source
        """
        return super().pause(source_id)
    
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