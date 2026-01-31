from typing import Any, Dict, Generic, Iterator, List, Optional, TypeVar

from nexla_sdk.models.base import BaseModel

T = TypeVar("T")


class PageInfo(BaseModel):
    """Information about the current page of results."""

    current_page: int
    total_pages: Optional[int] = None
    total_count: Optional[int] = None
    page_size: int = 20

    @property
    def has_next(self) -> bool:
        """Check if there's a next page."""
        if self.total_pages is not None:
            return self.current_page < self.total_pages
        return True  # Assume there might be more if we don't know total

    @property
    def has_previous(self) -> bool:
        """Check if there's a previous page."""
        return self.current_page > 1


class Page(Generic[T]):
    """A single page of results."""

    def __init__(
        self,
        items: List[T],
        page_info: PageInfo,
        raw_response: Optional[Dict[str, Any]] = None,
    ):
        self.items = items
        self.page_info = page_info
        self.raw_response = raw_response

    def __iter__(self) -> Iterator[T]:
        return iter(self.items)

    def __len__(self) -> int:
        return len(self.items)

    def __getitem__(self, index: int) -> T:
        return self.items[index]


class Paginator(Generic[T]):
    """Paginator for iterating through pages of results."""

    def __init__(self, fetch_func, page_size: int = 20, **kwargs):
        """
        Initialize paginator.

        Args:
            fetch_func: Function to fetch a page of results
            page_size: Number of items per page
            **kwargs: Additional arguments to pass to fetch function
        """
        self.fetch_func = fetch_func
        self.page_size = page_size
        self.kwargs = kwargs
        self.current_page = 1

    def get_page(self, page_number: int) -> Page[T]:
        """Get a specific page of results."""
        response = self.fetch_func(
            page=page_number, per_page=self.page_size, **self.kwargs
        )

        # Extract page info from response if available
        page_info = PageInfo(current_page=page_number, page_size=self.page_size)

        # Try to extract total pages/count from response metadata
        items: List[T]
        if isinstance(response, dict):
            if "meta" in response:
                meta = response["meta"] or {}
                # Support both snake_case and camelCase keys
                page_info.total_pages = meta.get("pageCount") or meta.get("total_pages")
                page_info.total_count = meta.get("totalCount") or meta.get(
                    "total_count"
                )
                current = meta.get("currentPage") or meta.get("current_page")
                if isinstance(current, int):
                    page_info.current_page = current
                items = response.get("data", [])
            else:
                # Response is not paginated; assume it's a list-like payload
                items = response  # type: ignore[assignment]
        else:
            items = response  # type: ignore[assignment]

        return Page(items=items, page_info=page_info, raw_response=response)

    def __iter__(self) -> Iterator[T]:
        """Iterate through all items across all pages."""
        self.current_page = 1
        while True:
            page = self.get_page(self.current_page)
            yield from page.items

            # If total pages known, use flag
            if not page.page_info.has_next:
                break
            # If total pages unknown, stop when we received fewer items than page size
            if len(page.items) < self.page_size:
                break

            self.current_page += 1

    def iter_pages(self) -> Iterator[Page[T]]:
        """Iterate through pages instead of individual items."""
        page_num = 1
        while True:
            page = self.get_page(page_num)
            yield page

            if not page.page_info.has_next:
                break
            if len(page.items) < self.page_size:
                break

            page_num += 1
