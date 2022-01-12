"""
Pagination API.

See Also:
    See :ref:`pagination-example`
    for complete examples of pagination usage.
"""
from typing import Callable, Generic, Iterator, List, Optional, TypeVar, cast

import requests


class Cursor:

    """:attr:`Page.cursor` value.
    Use :meth:`Page` to retrieve it."""

    pass


# This is a hack to prevent Sphinx autodoc-typehint type inlining.
# If we simply alias Cursor = str, it inlines str everywhere,
# and functions lose descriptive parameter and return value types.
# Additionally, this hack prevents SDK users from creating Cursor instances.
# Users have to call view()-like methods.
Cursor.__supertype__ = str  # type: ignore

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
        """Next page link."""
        return self._resp.links.get("next", {}).get("url")

    @property
    def cursor(self) -> Cursor:
        """Page cursor. The current position in the collection.

        The value should be taken from the X-Cursor response header
        of the previous request. If you pass an empty value,
        the first page will be returned.
        """

        return cast(Cursor, self._resp.headers.get(X_CURSOR_HEADER, ""))

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
    """Get chain of collection objects."""

    page: Optional[Page[T]] = start_page
    while page:
        yield from page
        page = page.next_page()
