import uuid
from typing import Any, Dict, Optional

from .. import RefView
from ..api import Nullable, Tag, _unwrap_nullable
from ..internal import BaseAPI, BaseAsyncAPI, JsonObjectForm
from ..pagination import AsyncPage, Cursor, Page
from ..view import _TaggedRefView
from .enums import DataSourceTypeListOrder

_PATH = "/data-source-types"


class DataSourceTypesAPI(BaseAPI):
    """API to operate data source types."""

    def register(self, form: "DataSourceTypeForm") -> RefView:
        """Register a data source type.

        Note:
            Calls `POST /data-source-types`.
        Args:
            form: Filled data source type form.
        Raises:
            :class:`~cybsi.api.error.ConflictError`: DataSourceType
                already exist.
        """
        r = self._connector.do_post(path=_PATH, json=form.json())
        return RefView(r.json())

    def view(self, type_uuid: uuid.UUID) -> "DataSourceTypeView":
        """Get the data source type view.

        Note:
            Calls `GET /data-source-types/{type_uuid}`.
        Args:
            type_uuid: Data source UUID.
        Returns:
            View of the data source type.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: Data source type not found.
        """
        path = f"{_PATH}/{type_uuid}"
        r = self._connector.do_get(path)
        return DataSourceTypeView(r)

    def edit(
        self,
        type_uuid: uuid.UUID,
        tag: Tag,
        long_name: Optional[str] = None,
        manual_confidence: Nullable[float] = None,
    ) -> None:
        """Edit the data source type.

        Note:
            Calls `PATCH /data-source-types/{type_uuid}`.
        Args:
            type_uuid: Data source type UUID.
            tag: :attr:`DataSourceTypeView.tag` value. Use :meth:`view` to retrieve it.
            long_name:  Human-readable data source type name.
                Non-empty if not :data:`None`.
            manual_confidence:
                Confidence for datasource type.
                Overrides default confidence of the data source type.
                Valid values are in [0, 1].
                :data:`~cybsi.api.Null` means
                that Cybsi can use default confidence.
                :data:`None` means that confidence is left unchanged.
        Raises:
            :class:`~cybsi.api.error.InvalidRequestError`:
                Provided arguments have invalid values.
            :class:`~cybsi.api.error.NotFoundError`: Data source type not found.
            :class:`~cybsi.api.error.ResourceModifiedError`:
                Data source type changed since last request. Update tag and retry.
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
        order_by: Optional[DataSourceTypeListOrder] = None,
        cursor: Optional[Cursor] = None,
        limit: Optional[int] = None,
    ) -> Page["DataSourceTypeCommonView"]:
        """Get a filtered list of data source type.

        Note:
            Calls `GET /data-source-types`.
        Args:
            order_by: The field to sort the list. Default value is "ShortName".
                The sort is performed in case-insensitive manner in lexicographic order.

                If ``order_by`` is not :data:`None` then it is necessary to pass
                the parameter to each next request along with a non-empty cursor.
                Otherwise, the sort will be reset to the "default" sort
                which may lead to inconsistency in the data selection.
            cursor: Page cursor.
            limit: Page limit.
        Returns:
            Page with data source type common views and next page cursor.
        Usage:
            >>> import uuid
            >>> from cybsi.api import CybsiClient
            >>> from cybsi.api.pagination import chain_pages
            >>> from cybsi.api.data_source import DataSourceTypeListOrder
            >>>
            >>> client: CybsiClient
            >>> # filter data sources by specified sort
            >>> started_page = client.data_source_types.filter(
            >>>     order_by=DataSourceTypeListOrder.LongName,
            >>> )
            >>> for item in chain_pages(started_page):
            >>>     # do something with data source type
            >>>     print(item)
            >>> pass
        """

        params: Dict[str, Any] = {}
        if order_by is not None:
            params["orderBy"] = order_by.value
        if cursor:
            params["cursor"] = str(cursor)
        if limit:
            params["limit"] = str(limit)

        resp = self._connector.do_get(path=_PATH, params=params)
        page = Page(self._connector.do_get, resp, DataSourceTypeCommonView)
        return page


class DataSourceTypesAsyncAPI(BaseAsyncAPI):
    """API to operate data source types."""

    async def register(self, form: "DataSourceTypeForm") -> RefView:
        """Register a data source type.

        Note:
            Calls `POST /data-source-types`.
        Args:
            form: Filled data source type form.
        Raises:
            :class:`~cybsi.api.error.ConflictError`: DataSourceType
                already exist.
        """
        r = await self._connector.do_post(path=_PATH, json=form.json())
        return RefView(r.json())

    async def view(self, type_uuid: uuid.UUID) -> "DataSourceTypeView":
        """Get the data source type view.

        Note:
            Calls `GET /data-source-types/{type_uuid}`.
        Args:
            type_uuid: Data source UUID.
        Returns:
            View of the data source type.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: Data source type not found.
        """
        path = f"{_PATH}/{type_uuid}"
        r = await self._connector.do_get(path)
        return DataSourceTypeView(r)

    async def edit(
        self,
        type_uuid: uuid.UUID,
        tag: Tag,
        long_name: Optional[str] = None,
        manual_confidence: Nullable[float] = None,
    ) -> None:
        """Edit the data source type.

        Note:
            Calls `PATCH /data-source-types/{type_uuid}`.
        Args:
            type_uuid: Data source type UUID.
            tag: :attr:`DataSourceTypeView.tag` value. Use :meth:`view` to retrieve it.
            long_name:  Human-readable data source type name.
                Non-empty if not :data:`None`.
            manual_confidence:
                Confidence for datasource type.
                Overrides default confidence of the data source type.
                Valid values are in [0, 1].
                :data:`~cybsi.api.Null` means
                that Cybsi can use default confidence.
                :data:`None` means that confidence is left unchanged.
        Raises:
            :class:`~cybsi.api.error.InvalidRequestError`:
                Provided arguments have invalid values.
            :class:`~cybsi.api.error.NotFoundError`: Data source type not found.
            :class:`~cybsi.api.error.ResourceModifiedError`:
                Data source type changed since last request. Update tag and retry.
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
        order_by: Optional[DataSourceTypeListOrder] = None,
        cursor: Optional[Cursor] = None,
        limit: Optional[int] = None,
    ) -> AsyncPage["DataSourceTypeCommonView"]:
        """Get a filtered list of data source type.

        Note:
            Calls `GET /data-source-types`.
        Args:
            order_by: The field to sort the list. Default value is "ShortName".
                The sort is performed in case-insensitive manner in lexicographic order.

                If ``order_by`` is not :data:`None` then it is necessary to pass
                the parameter to each next request along with a non-empty cursor.
                Otherwise, the sort will be reset to the "default" sort
                which may lead to inconsistency in the data selection.
            cursor: Page cursor.
            limit: Page limit.
        Returns:
            Page with data source type common views and next page cursor.
        """

        params: Dict[str, Any] = {}
        if order_by is not None:
            params["orderBy"] = order_by.value
        if cursor:
            params["cursor"] = str(cursor)
        if limit:
            params["limit"] = str(limit)

        resp = await self._connector.do_get(path=_PATH, params=params)
        page = AsyncPage(self._connector.do_get, resp, DataSourceTypeCommonView)
        return page


class DataSourceTypeForm(JsonObjectForm):
    """Data source type form.

    This is the form you need to fill to register data source type.

    Args:
        short_name: Data source type identifier. Must be unique across all data
            source types. Non-empty.
            Short name should consist of characters without spaces (`[a-zA-Z0-9_-]`) and
            have length in the range [1, 250].
        long_name: Human-readable data source type name. Non-empty.
            Long name length must be in the range [1, 250].
        manual_confidence: Confidence for datasource type.
            Overrides default confidence of the data source type.
            Valid values are in [0, 1].
    Return:
        Datasource Type register form.
    """

    def __init__(
        self,
        short_name: str,
        long_name: str,
        manual_confidence: Optional[float] = None,
    ):
        super().__init__()
        self._data["shortName"] = short_name
        self._data["longName"] = long_name
        if manual_confidence is not None:
            self._data["manualConfidence"] = manual_confidence


class DataSourceTypeView(_TaggedRefView):
    """View of data source type."""

    @property
    def short_name(self) -> str:
        """Data source type identifier. Unique across all data source types."""
        return self._get("shortName")

    @property
    def long_name(self) -> str:
        """Human-readable data source type name."""
        return self._get("longName")

    @property
    def confidence(self) -> float:
        """Confidence."""
        return self._get("confidence")

    @property
    def manual_confidence(self) -> Optional[float]:
        """Manually set confidence for datasource type.
        Overrides confidence of the data source type.
        """
        return self._get_optional("manualConfidence")


class DataSourceTypeCommonView(RefView):
    """Data source type short view"""

    @property
    def long_name(self) -> str:
        """Human-readable data source type name."""
        return self._get("longName")

    @property
    def confidence(self) -> float:
        """Confidence of data source type."""
        return self._get("confidence")
