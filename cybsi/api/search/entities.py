from typing import Optional, Type, cast

from ..internal import BaseAPI, BaseAsyncAPI, JsonObject
from ..observable import EntityView, EntityViewT, ShareLevels
from ..pagination import X_CURSOR_HEADER, AsyncPage, Cursor, Page


class SearchEntitiesAPI(BaseAPI):
    """Search entities API."""

    _path = "/search/entities"

    def start_search(
        self,
        query_text: str,
        *,
        share_level: Optional[ShareLevels] = None,
    ) -> Cursor:
        """Starts entities search.

        Note:
            Calls `POST /search/entities`.
        Args:
            query_text: CybsiLang query text.
                Query must not be empty.
            share_level: Facts share level.
                Use facts appropriate to share_level.
                None means current user access level.
        Returns:
            Cursor of the first page of the search.
            The cursor can be used to call :meth:`next_search_page`.
        Raises:
            :class:`~cybsi.api.error.SemanticError`: Form contains logic errors.
        Note:
            Semantic error codes specific for this method:
              * :attr:`~cybsi.api.error.SemanticErrorCodes.InvalidQueryText`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.InvalidShareLevel`
        """
        form: JsonObject = {"queryText": query_text}
        if share_level is not None:
            form["shareLevel"] = share_level.value
        resp = self._connector.do_post(self._path, json=form)
        return cast(Cursor, resp.headers[X_CURSOR_HEADER])

    def next_search_page(
        self,
        cursor: Cursor,
        *,
        limit: Optional[int] = None,
        entity_view: Type[EntityViewT] = EntityView,  # type: ignore
    ) -> Page[EntityViewT]:
        """Get next search page result.

        Note:
            Calls `GET /search/entities`.
        Args:
            cursor: Page cursor.
            limit: Page limit.
            entity_view: Entity view to use.
                Default is :class:`~cybsi.api.observable.EntityView` -
                - only natural keys.
                You can specify one of builtin views in :mod:`~cybsi.utils.views`.
        Raises:
            :class:`~cybsi.api.error.SemanticError`: Request contains logic errors.
        Note:
            Semantic error codes specific for this method:
              * :attr:`~cybsi.api.error.SemanticErrorCodes.EntityViewNotFound`
        """
        params = {"cursor": str(cursor)}
        if limit is not None:
            params["limit"] = str(limit)
        if entity_view is not EntityView:
            params["viewUUID"] = str(entity_view._view_uuid())
        resp = self._connector.do_get(path=self._path, params=params)
        return Page(self._connector.do_get, resp, entity_view)


class SearchEntitiesAsyncAPI(BaseAsyncAPI):
    """Search entities API."""

    _path = "/search/entities"

    async def start_search(
        self,
        query_text: str,
        *,
        share_level: Optional[ShareLevels] = None,
    ) -> Cursor:
        """Starts entities search.

        Note:
            Calls `POST /search/entities`.
        Args:
            query_text: CybsiLang query text.
                Query must not be empty.
            share_level: Facts share level.
                Use facts appropriate to share_level.
                None means current user access level.
        Returns:
            Cursor of the first page of the search.
            The cursor can be used to call :meth:`next_search_page`.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: Stored query not found.
        """
        form: JsonObject = {"queryText": query_text}
        if share_level is not None:
            form["shareLevel"] = share_level.value
        resp = await self._connector.do_post(self._path, json=form)
        return cast(Cursor, resp.headers[X_CURSOR_HEADER])

    async def next_search_page(
        self,
        cursor: Cursor,
        *,
        limit: Optional[int] = None,
        entity_view: Type[EntityViewT] = EntityView,  # type: ignore
    ) -> AsyncPage[EntityViewT]:
        """Get next search page result.

        Note:
            Calls `GET /search/entities`.
        Args:
            cursor: Page cursor.
            limit: Page limit.
            entity_view: Entity view to use.
                Default is :class:`~cybsi.api.observable.EntityView` -
                - only natural keys.
                You can specify one of builtin views in :mod:`~cybsi.utils.views`.
        Raises:
            :class:`~cybsi.api.error.InvalidRequestError`:
                Provided arguments have invalid values.
            :class:`~cybsi.api.error.NotFoundError`: Stored query not found.
            :class:`~cybsi.api.error.ResourceModifiedError`:
                Stored query changed since last request. Update tag and retry.
            :class:`~cybsi.api.error.SemanticError`: Form contains logic errors.
        Note:
            Semantic error codes specific for this method:
              * :attr:`~cybsi.api.error.SemanticErrorCodes.InvalidQueryText`
        """
        params = {"cursor": str(cursor)}
        if limit is not None:
            params["limit"] = str(limit)
        if entity_view is not EntityView:
            params["viewUUID"] = str(entity_view._view_uuid())
        resp = await self._connector.do_get(path=self._path, params=params)
        return AsyncPage(self._connector.do_get, resp, entity_view)
