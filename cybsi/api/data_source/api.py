import uuid
from typing import Any, Dict, Iterable, Optional

from .. import RefView
from ..api import Nullable, Tag, _unwrap_nullable
from ..internal import BaseAPI, BaseAsyncAPI, JsonObjectForm, JsonObjectView
from ..pagination import AsyncPage, Cursor, Page
from ..view import _TaggedRefView
from .api_types import DataSourceTypeCommonView
from .enums import DataSourceListOrder

_PATH = "/data-sources"


class DataSourcesAPI(BaseAPI):
    """API to operate data source."""

    def view(self, datasource_uuid: uuid.UUID) -> "DataSourceView":
        """Get the data source view.

        Note:
            Calls `GET /data-sources/{datasource_uuid}`.
        Args:
            datasource_uuid: Data source UUID.
        Returns:
            View of the data source.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: Data source not found.
        """
        path = f"{_PATH}/{datasource_uuid}"
        r = self._connector.do_get(path)
        return DataSourceView(r)

    def view_links(self, datasource_uuid: uuid.UUID) -> "DataSourceLinksView":
        """Get links view of the data source.

        .. versionadded:: 2.7

        Note:
            Calls `GET /data-sources/{datasource_uuid}/links`.
        Args:
            datasource_uuid: Data source UUID.
        Returns:
            Links view of the data source.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: Data source not found.
        """

        path = f"{_PATH}/{datasource_uuid}/links"
        r = self._connector.do_get(path)
        return DataSourceLinksView(r.json())

    def me(self) -> "DataSourceView":
        """Get data source associated with current client.

        Note:
            Calls `GET /data-sources/me`.
        """
        path = f"{_PATH}/me"
        r = self._connector.do_get(path)
        return DataSourceView(r)

    def register(self, form: "DataSourceForm") -> RefView:
        """Register a data source.

        Note:
            Calls `POST /data-sources`.
        Args:
            form: Filled data source form.
        Raises:
            :class:`~cybsi.api.error.ConflictError`: Data source already exist.
            :class:`~cybsi.api.error.SemanticError`
        Note:
            Semantic error codes:
              * :attr:`~cybsi.api.error.SemanticErrorCodes.DataSourceTypeNotFound`
        """
        r = self._connector.do_post(path=_PATH, json=form.json())
        return RefView(r.json())

    def edit(
        self,
        type_uuid: uuid.UUID,
        tag: Tag,
        long_name: Optional[str] = None,
        manual_confidence: Nullable[float] = None,
    ) -> None:
        """Edit the data source.

        Note:
            Calls `PATCH /data-sources/{source_uuid}`.
        Args:
            type_uuid: Data source type uuid.
            tag: :attr:`DataSourceView.tag` value. Use :meth:`view` to retrieve it.
            long_name:  Human-readable data source name. Non-empty if not :data:`None`.
            manual_confidence:
                Confidence for data source.
                Overrides confidence of the data source inherited from data source type.
                Valid values are in [0, 1].
                :data:`~cybsi.api.Null` means
                that Cybsi can use confidence provided by data source type.
                :data:`None` means that confidence is left unchanged.
        Raises:
            :class:`~cybsi.api.error.InvalidRequestError`:
                Provided arguments have invalid values.
            :class:`~cybsi.api.error.NotFoundError`: Data source not found.
            :class:`~cybsi.api.error.ResourceModifiedError`:
                Data source changed since last request. Update tag and retry.
        """
        form: Dict[str, Any] = {}
        if long_name is not None:
            form["longName"] = long_name
        if manual_confidence is not None:
            form["manualConfidence"] = _unwrap_nullable(manual_confidence)
        path = f"{_PATH}/{type_uuid}"
        self._connector.do_patch(path=path, tag=tag, json=form)

    def filter(
        self,
        query: Optional[str] = None,
        type_uuids: Optional[Iterable[uuid.UUID]] = None,
        order_by: Optional[DataSourceListOrder] = None,
        cursor: Optional[Cursor] = None,
        limit: Optional[int] = None,
    ) -> Page["DataSourceCommonView"]:
        """Get a filtered list of data sources.

        .. versionchanged:: 2.8
            Added new parameters: `query`, `type_uuids`, `order_by`.
            Added semantic error `DataSourceNotFound`

        Note:
            Calls `GET /data-sources`.
        Args:
            query: Filter of data sources by specified substring (case-insensitive).
                Substring length must be in range [1, 50].
                Filtering is performed by specified substring in data source names or
                its type names.
            type_uuids: List of data source type UUIDs.
            order_by: The field to sort the list. Default value is "UUID".
                The sort is performed in case-insensitive manner in lexicographic order.

                If ``order_by`` is not :data:`None` then it is necessary to pass
                the parameter to each next request along with a non-empty cursor.
                Otherwise, the sort will be reset to the "default" sort,
                which may lead to inconsistency in the data selection.
            cursor: Page cursor.
            limit: Page limit.
        Returns:
            Page with data source common views and next page cursor.
        Raises:
            :class:`~cybsi.api.error.SemanticError`
        Note:
            Semantic error codes:
              * :attr:`~cybsi.api.error.SemanticErrorCodes.DataSourceTypeNotFound`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.DataSourceNotFound`
        Usage:
            >>> import uuid
            >>> from cybsi.api import CybsiClient
            >>> from cybsi.api.pagination import chain_pages
            >>> from cybsi.api.data_source import DataSourceListOrder
            >>>
            >>> client: CybsiClient
            >>> # filter data sources by specified type uuid and sort
            >>> started_page = client.data_sources.filter(
            >>>     type_uuids=[uuid.UUID("89200bef-2f50-4d4f-8b38-843d5ab9dfa9")],
            >>>     order_by=DataSourceListOrder.FullName,
            >>> )
            >>> for item in chain_pages(started_page):
            >>>     # do something with data source
            >>>     print(item)
            >>> pass
        """

        params: Dict[str, Any] = {}
        if query is not None:
            params["query"] = query
        if type_uuids is not None:
            params["typeUUID"] = [str(u) for u in type_uuids]
        if order_by is not None:
            params["orderBy"] = order_by.value
        if cursor:
            params["cursor"] = str(cursor)
        if limit:
            params["limit"] = str(limit)

        resp = self._connector.do_get(path=_PATH, params=params)
        page = Page(self._connector.do_get, resp, DataSourceCommonView)
        return page


class DataSourcesAsyncAPI(BaseAsyncAPI):
    """Asynchronous API to operate data source."""

    async def view(self, datasource_uuid: uuid.UUID) -> "DataSourceView":
        """Get the data source view.

        Note:
            Calls `GET /data-sources/{datasource_uuid}`.
        Args:
            datasource_uuid: Data source UUID.
        Returns:
            View of the data source.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: Data source not found.
        """
        path = f"{_PATH}/{datasource_uuid}"
        r = await self._connector.do_get(path)
        return DataSourceView(r)

    async def view_links(self, datasource_uuid: uuid.UUID) -> "DataSourceLinksView":
        """Get links view of the data source.

        .. versionadded:: 2.7

        Note:
            Calls `GET /data-sources/{datasource_uuid}/links`.
        Args:
            datasource_uuid: Data source UUID.
        Returns:
            Links view of the data source.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: Data source not found.
        """

        path = f"{_PATH}/{datasource_uuid}/links"
        r = await self._connector.do_get(path)
        return DataSourceLinksView(r.json())

    async def me(self) -> "DataSourceView":
        """Get data source associated with current client.

        Note:
            Calls `GET /data-sources/me`.
        """
        path = f"{_PATH}/me"
        r = await self._connector.do_get(path)
        return DataSourceView(r)

    async def register(self, form: "DataSourceForm") -> RefView:
        """Register a data source.

        Note:
            Calls `POST /data-sources`.
        Args:
            form: Filled data source form.
        Raises:
            :class:`~cybsi.api.error.ConflictError`: Data source already exist.
            :class:`~cybsi.api.error.SemanticError`
        Note:
            Semantic error codes:
              * :attr:`~cybsi.api.error.SemanticErrorCodes.DataSourceTypeNotFound`
        """
        r = await self._connector.do_post(path=_PATH, json=form.json())
        return RefView(r.json())

    async def edit(
        self,
        type_uuid: uuid.UUID,
        tag: Tag,
        long_name: Optional[str] = None,
        manual_confidence: Nullable[float] = None,
    ) -> None:
        """Edit the data source.

        Note:
            Calls `PATCH /data-sources/{source_uuid}`.
        Args:
            type_uuid: Data source type uuid.
            tag: :attr:`DataSourceView.tag` value. Use :meth:`view` to retrieve it.
            long_name:  Human-readable data source name. Non-empty if not :data:`None`.
            manual_confidence:
                Confidence for data source.
                Overrides confidence of the data source inherited from data source type.
                Valid values are in [0, 1].
                :data:`~cybsi.api.Null` means
                that Cybsi can use confidence provided by data source type.
                :data:`None` means that confidence is left unchanged.
        Raises:
            :class:`~cybsi.api.error.InvalidRequestError`:
                Provided arguments have invalid values.
            :class:`~cybsi.api.error.NotFoundError`: Data source not found.
            :class:`~cybsi.api.error.ResourceModifiedError`:
                Data source changed since last request. Update tag and retry.
        """
        form: Dict[str, Any] = {}
        if long_name is not None:
            form["longName"] = long_name
        if manual_confidence is not None:
            form["manualConfidence"] = _unwrap_nullable(manual_confidence)
        path = f"{_PATH}/{type_uuid}"
        await self._connector.do_patch(path=path, tag=tag, json=form)

    async def filter(
        self,
        query: Optional[str] = None,
        type_uuids: Optional[Iterable[uuid.UUID]] = None,
        order_by: Optional[DataSourceListOrder] = None,
        cursor: Optional[Cursor] = None,
        limit: Optional[int] = None,
    ) -> AsyncPage["DataSourceCommonView"]:
        """Get a filtered list of data sources.

        Note:
            Calls `GET /data-sources`.
        Args:
            query: Filter of data sources by specified substring (case-insensitive).
                Substring length must be in range [1, 50].
                Filtering is performed by specified substring in data source names or
                its type names.
            type_uuids: List of data source type UUIDs.
            order_by: The field to sort the list. Default value is "UUID".
                The sort is performed in case-insensitive manner in lexicographic order.

                If ``order_by`` is not :data:`None` then it is necessary to pass
                the parameter to each next request along with a non-empty cursor.
                Otherwise, the sort will be reset to the "default" sort,
                which may lead to inconsistency in the data selection.
            cursor: Page cursor.
            limit: Page limit.
        Returns:
            Page with data source common views and next page cursor.
        Raises:
            :class:`~cybsi.api.error.SemanticError`
        Note:
            Semantic error codes:
              * :attr:`~cybsi.api.error.SemanticErrorCodes.DataSourceTypeNotFound`
        """

        params: Dict[str, Any] = {}
        if query is not None:
            params["query"] = query
        if type_uuids is not None:
            params["typeUUID"] = [str(u) for u in type_uuids]
        if order_by is not None:
            params["orderBy"] = order_by.value
        if cursor:
            params["cursor"] = str(cursor)
        if limit:
            params["limit"] = str(limit)

        resp = await self._connector.do_get(path=_PATH, params=params)
        page = AsyncPage(self._connector.do_get, resp, DataSourceCommonView)
        return page


class DataSourceForm(JsonObjectForm):
    """Data source form.

    This is the form you need to fill to register data source.

    Args:
        type_uuid: Data source type UUID.
        name: Data source identifier. Must be unique name for data source type.
            Name should consist of characters without spaces (`[a-zA-Z0-9_-]`) and
            have length in the range [1, 250].
        long_name: Human-readable data source name.
            Long name length must be in the range [1, 250].
        manual_confidence:
            Confidence of the data source.
            Overrides confidence of the data source inherited from data source type.
            Valid values are in [0, 1].
    Return:
        Data source register form.
    """

    def __init__(
        self,
        type_uuid: uuid.UUID,
        name: str,
        long_name: str,
        manual_confidence: Optional[float] = None,
    ):
        super().__init__()
        self._data["typeUUID"] = str(type_uuid)
        self._data["name"] = name
        self._data["longName"] = long_name
        if manual_confidence is not None:
            self._data["manualConfidence"] = manual_confidence


class DataSourceView(_TaggedRefView):
    """View of data source."""

    @property
    def type(self) -> DataSourceTypeCommonView:
        """Data source type."""
        return DataSourceTypeCommonView(self._get("type"))

    @property
    def name(self) -> str:
        """Data source identifier. Must be unique name for data source type."""
        return self._get("name")

    @property
    def long_name(self) -> str:
        """Human-readable data source name."""
        return self._get("longName")

    @property
    def confidence(self) -> float:
        """Confidence of data source."""
        return self._get("confidence")

    @property
    def manual_confidence(self) -> Optional[float]:
        """Manually set confidence of the data source. Overrides
        confidence of the data source type."""
        return self._get_optional("manualConfidence")


class DataSourceCommonView(RefView):
    """Data source short view."""

    @property
    def long_name(self) -> str:
        """Human-readable data source name."""
        return self._get("longName")

    @property
    def unique_name(self) -> str:
        """The unique identifier contains of the type `ShortName` and
        the source `Name` (ShortName/Name)."""
        return self._get("uniqueName")

    @property
    def confidence(self) -> float:
        """Confidence of data source."""
        return self._get("confidence")

    @property
    def type(self) -> "DataSourceTypeCommonView":
        """Data source type short view."""
        return DataSourceTypeCommonView(self._get("type"))


class DataSourceLinksView(JsonObjectView):
    """Data source links view"""

    @property
    def analyzer(self) -> Optional[RefView]:
        """Reference to analyzer.

        Use :meth:`~cybsi.api.enrichment.analyzers.AnalyzersAPI.view` to retrieve analyzer view.
        """  # noqa: E501
        return self._map_optional("analyzer", RefView)

    @property
    def external_db(self) -> Optional[RefView]:
        """Reference to external database.

        Use :meth:`~cybsi.api.enrichment.external_dbs.ExternalDBsAPI.view` to retrieve external db view.
        """  # noqa: E501
        return self._map_optional("externalDB", RefView)

    @property
    def user(self) -> Optional[RefView]:
        """Reference to user.

        Use :meth:`~cybsi.api.user.UsersAPI.view` to retrieve user view.
        """
        return self._map_optional("user", RefView)
