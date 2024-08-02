from ..internal import BaseAPI, BaseAsyncAPI
from .entities import SearchEntitiesAPI, SearchEntitiesAsyncAPI
from .stored_queries import StoredQueriesAPI


class SearchAPI(BaseAPI):
    """Search API."""

    @property
    def stored_queries(self) -> StoredQueriesAPI:
        """Get stored queries route."""
        return StoredQueriesAPI(self._connector)

    @property
    def entities(self) -> SearchEntitiesAPI:
        """Get search entities route."""
        return SearchEntitiesAPI(self._connector)


class SearchAsyncAPI(BaseAsyncAPI):
    """Search API."""

    @property
    def entities(self) -> SearchEntitiesAsyncAPI:
        """Get search entities route."""
        return SearchEntitiesAsyncAPI(self._connector)
