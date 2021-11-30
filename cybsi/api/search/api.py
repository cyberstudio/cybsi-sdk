from ..internal import BaseAPI
from .stored_queries import StoredQueriesAPI


class SearchAPI(BaseAPI):
    """Search API."""

    @property
    def stored_queries(self) -> StoredQueriesAPI:
        """Get stored queries route."""
        return StoredQueriesAPI(self._connector)
