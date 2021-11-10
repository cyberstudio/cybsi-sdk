"""
Pagination API.

See Also:
    See :ref:`pagination-example`
    for complete examples of pagination usage.
"""
import requests

from typing import TypeVar, Callable, Iterator, List, Generic, Optional


DEFAULT_PAGE_LIMIT = 30
X_CURSOR_HEADER = "X-Cursor"

T = TypeVar("T")


class Page(Generic[T]):
    """Page returned by Cybsi API.

    Args:
        api_call: Callable object for getting next page
        resp: Response which represents a start page
        view: View class for page elements
    """

    def __init__(
        self,
        api_call: Callable[..., requests.Response],
        resp: requests.Response,
        view: Callable[..., T],
    ):
        self._api_call = api_call
        self._resp = resp
        self._view = view

    @property
    def next_link(self) -> str:
        """Next page link"""
        return self._resp.links.get("next", {}).get("url")

    @property
    def cursor(self) -> str:
        """Page cursor"""
        return self._resp.headers.get(X_CURSOR_HEADER, "")

    def data(self) -> List[T]:
        """Get page data as a list of items."""
        return list(iter(self))

    def next_page(self) -> "Optional[Page[T]]":
        """Get next page.
        If there is no link to the next page it return None.
        """
        if self.next_link is None:
            return None

        return Page(self._api_call, self._api_call(self.next_link), self._view)

    def __iter__(self) -> Iterator[T]:
        yield from (self._view(x) for x in self._resp.json())


def chain_pages(start_page: Page[T]) -> Iterator[T]:
    """Get chain of collection objects"""

    page: Optional[Page[T]] = start_page
    while page:
        yield from page
        page = page.next_page()
