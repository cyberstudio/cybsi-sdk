import uuid
from typing import Any, Dict, Optional

from cybsi.api import RefView, Tag
from cybsi.api.internal import BaseAPI, BaseAsyncAPI, JsonObjectForm
from cybsi.api.pagination import AsyncPage, Cursor, Page
from cybsi.api.view import _TaggedRefView

_PATH = "/custom-lists"


class CustomListsAPI(BaseAPI):
    """API to operate custom lists.

    .. versionadded:: 2.14.0"""

    def filter(
        self,
        *,
        prefix: Optional[str] = None,
        cursor: Optional[Cursor] = None,
        limit: Optional[int] = None,
    ) -> Page["CustomListCommonView"]:
        """Get custom lists.

        .. versionadded:: 2.14.0
        Note:
            Calls `GET /custom-lists`.
        Args:
            prefix: Custom list's name prefix.
            cursor: Page cursor.
            limit: Page limit.
        Return:
            Page with custom lists and next page cursor.
        Raises:
            :class:`~cybsi.api.error.InvalidRequestError`:
                Provided arguments have invalid values.
        """
        params: Dict[str, Any] = {}
        if prefix is not None:
            params["prefix"] = prefix
        if cursor is not None:
            params["cursor"] = cursor
        if limit is not None:
            params["limit"] = limit
        resp = self._connector.do_get(path=_PATH, params=params)
        page = Page(self._connector.do_get, resp, CustomListCommonView)
        return page

    def register(self, custom_list: "CustomListForm") -> RefView:
        """Register a custom list.

        .. versionadded:: 2.14.0
        Note:
            Calls `POST /custom-lists`.
        Args:
            custom_list: Filled custom list form.
        Returns:
            Reference to the registered custom list.
        Raises:
            :class:`~cybsi.api.error.ConflictError`:
                Custom list with the same string ID already exists.
            :class:`~cybsi.api.error.InvalidRequestError`:
                Provided arguments have invalid values.
            :class:`~cybsi.api.error.SemanticError`: Form contains logic errors.
        Note:
            Semantic error codes specific for this method:
            * :attr:`cybsi.api.error.SemanticErrorCodes.DictionaryNotFound`
        """
        resp = self._connector.do_post(path=_PATH, json=custom_list.json())
        return RefView(resp.json())

    def view(self, custom_list_uuid: uuid.UUID) -> "CustomListView":
        """Get view of a custom list.

        .. versionadded:: 2.14.0
        Note:
            Calls `GET /custom-lists/{custom_list_uuid}`.
        Args:
            custom_list_uuid: Custom list UUID.
        Returns:
            Custom list view.
        Raises:
            :class:`~cybsi.api.error.InvalidRequestError`:
                Provided arguments have invalid values.
            :class:`~cybsi.api.error.NotFoundError`:
                Custom list does not exist.
        """
        path = f"{_PATH}/{custom_list_uuid}"
        resp = self._connector.do_get(path=path)
        return CustomListView(resp)

    def edit(
        self,
        custom_list_uuid: uuid.UUID,
        tag: Tag,
        name: str,
    ) -> None:
        """Edit the custom list.

        .. versionadded:: 2.14.0
        Note:
            Calls `PATCH /custom-lists/{list_uuid}`.
        Args:
            custom_list_uuid: UUID of custom list.
            tag: :attr:`CustomListView.tag` value. Use :meth:`view` to retrieve it.
            name: Custom list name.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: Custom list not found.
            :class:`~cybsi.api.error.ResourceModifiedError`:
                Custom list changed since last request. Update tag and retry.
            :class:`~cybsi.api.error.InvalidRequestError`:
                Provided arguments have invalid values.
        """
        form = {"name": name}
        path = f"{_PATH}/{custom_list_uuid}"
        self._connector.do_patch(path=path, json=form, tag=tag)

    def filter_items(
        self,
        custom_list_uuid: uuid.UUID,
        *,
        cursor: Optional[Cursor] = None,
        limit: Optional[int] = None,
    ) -> Page[RefView]:
        """Get custom list items.

        .. versionadded:: 2.14.0
        Note:
            Calls `GET /custom-lists/{custom_list_uuid}/items`.
        Args:
            custom_list_uuid: Custom list UUID.
            cursor: Page cursor.
            limit: Page limit.
        Returns:
            Page with custom list items and next page cursor.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: Custom list not found.
            :class:`~cybsi.api.error.InvalidRequestError`:
                Provided arguments have invalid values.
        """
        params: Dict[str, Any] = {}
        if cursor:
            params["cursor"] = cursor
        if limit:
            params["limit"] = limit
        path = f"{_PATH}/{custom_list_uuid}/items"
        resp = self._connector.do_get(path=path, params=params)
        page = Page(self._connector.do_get, resp, RefView)
        return page

    def add_item(
        self, custom_list_uuid: uuid.UUID, dictionary_item_uuid: uuid.UUID
    ) -> None:
        """Add item to custom list.

        .. versionadded:: 2.14.0
        Note:
            Calls `POST /custom-lists/{custom_list_uuid}/items`.
        Args:
            custom_list_uuid: Custom list UUID.
            dictionary_item_uuid: Dictionary item UUID.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: Custom list not found.
            :class:`~cybsi.api.error.SemanticError`: Form contains logic errors.
            :class:`~cybsi.api.error.InvalidRequestError`:
                Provided arguments have invalid values.
        Note:
            Semantic error codes specific for this method:
            * :attr:`cybsi.api.error.SemanticErrorCodes.DictionaryItemNotFound`
            * :attr:`cybsi.api.error.SemanticErrorCodes.DictionaryMismatch`
        """
        params = {"dictionaryItemUUID": str(dictionary_item_uuid)}
        path = f"{_PATH}/{custom_list_uuid}/items"
        self._connector.do_post(path=path, json=params)

    def delete_item(
        self, custom_list_uuid: uuid.UUID, dictionary_item_uuid: uuid.UUID
    ) -> None:
        """Delete item from custom list.

        .. versionadded:: 2.14.0
        Note:
            Calls `DELETE /custom-lists/{custom_list_uuid}/items/{item_uuid}`.
        Args:
            custom_list_uuid: Custom list UUID
            dictionary_item_uuid: Dictionary item UUID.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: Custom list not found.
            :class:`~cybsi.api.error.InvalidRequestError`:
                Provided arguments have invalid values.
        """
        path = f"{_PATH}/{custom_list_uuid}/items/{dictionary_item_uuid}"
        self._connector.do_delete(path=path)

    def get_related_items(
        self,
        custom_list_uuid: uuid.UUID,
        dictionary_uuid: uuid.UUID,
        *,
        cursor: Optional[Cursor] = None,
        limit: Optional[int] = None,
    ) -> Page[RefView]:
        """Get dictionary items that are related to custom list.

        .. versionadded:: 2.14.0
        Note:
            Calls `GET /custom-lists/{custom_list_uuid}/related-items`.
        Args:
            custom_list_uuid: Custom list UUID
            dictionary_uuid: Dictionary UUID.
            cursor: Page cursor.
            limit: Page limit.
        Returns:
            Page with related items and next page cursor.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: Custom list not found.
            :class:`~cybsi.api.error.SemanticError`: Form contains logic errors.
            :class:`~cybsi.api.error.InvalidRequestError`:
                Provided arguments have invalid values.
        Note:
            Semantic error codes specific for this method:
            * :attr:`cybsi.api.error.SemanticErrorCodes.DictionaryNotFound`
        """
        params: Dict[str, Any] = {"dictionaryUUID": str(dictionary_uuid)}
        if cursor:
            params["cursor"] = cursor
        if limit:
            params["limit"] = limit

        path = f"{_PATH}/{custom_list_uuid}/related-items"
        resp = self._connector.do_get(path=path, params=params)
        page = Page(self._connector.do_get, resp, RefView)
        return page


class CustomListsAsyncAPI(BaseAsyncAPI):
    """Async API to operate custom lists.

    .. versionadded:: 2.14.0
    """

    async def filter(
        self,
        *,
        prefix: Optional[str] = None,
        cursor: Optional[Cursor] = None,
        limit: Optional[int] = None,
    ) -> AsyncPage["CustomListCommonView"]:
        """Get custom lists.

        .. versionadded:: 2.14.0
        Note:
            Calls `GET /custom-lists`.
        Args:
            prefix: Custom list's name prefix.
            cursor: Page cursor.
            limit: Page limit.
        Return:
            Page with custom lists and next page cursor.
        Raises:
            :class:`~cybsi.api.error.SemanticError`: Request contains logic errors.
            :class:`~cybsi.api.error.InvalidRequestError`:
                Provided arguments have invalid values.
        """
        params: Dict[str, Any] = {}
        if prefix is not None:
            params["prefix"] = prefix
        if cursor is not None:
            params["cursor"] = cursor
        if limit is not None:
            params["limit"] = limit
        resp = await self._connector.do_get(path=_PATH, params=params)
        page = AsyncPage(self._connector.do_get, resp, CustomListCommonView)
        return page

    async def register(self, custom_list: "CustomListForm") -> RefView:
        """Register a custom list.

        .. versionadded:: 2.14.0
        Note:
            Calls `POST /custom-lists`.
        Args:
            custom_list: Filled custom list form.
        Returns:
            Reference to the registered custom list.
        Raises:
            :class:`~cybsi.api.error.ConflictError`:
                Replist with same identifying data already exists.
            :class:`~cybsi.api.error.SemanticError`: Form contains logic errors.
            :class:`~cybsi.api.error.InvalidRequestError`:
                Provided arguments have invalid values.
        Note:
            Semantic error codes specific for this method:
            * :attr:`cybsi.api.error.SemanticErrorCodes.DictionaryNotFound`
        """
        resp = await self._connector.do_post(path=_PATH, json=custom_list.json())
        return RefView(resp.json())

    async def view(self, custom_list_uuid: uuid.UUID) -> "CustomListView":
        """Get view of the custom list.

        .. versionadded:: 2.14.0
        Note:
            Calls `GET /custom-lists/{custom_list_uuid}`.
        Args:
            custom_list_uuid: Custom list UUID.
        Returns:
            View of the custom list.
        Raises:
            :class:`~cybsi.api.error.InvalidRequestError`:
                Provided arguments have invalid values.
            :class:`~cybsi.api.error.NotFoundError`:
             Custom list not found.`
        """
        path = f"{_PATH}/{custom_list_uuid}"
        resp = await self._connector.do_get(path=path)
        return CustomListView(resp)

    async def edit(
        self,
        custom_list_uuid: uuid.UUID,
        tag: Tag,
        name: str,
    ) -> None:
        """Edit the custom list.

        .. versionadded:: 2.14.0
        Note:
            Calls `PATCH /custom-lists/{custom_list_uuid}`.
        Args:
            custom_list_uuid: Custom list UUID.
            tag: :attr:`CustomListView.tag` value. Use :meth:`view` to retrieve it.
            name: Custom list name.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: Custom list not found.
            :class:`~cybsi.api.error.ResourceModifiedError`:
                Custom list changed since last request. Update tag and retry.
            :class:`~cybsi.api.error.InvalidRequestError`:
                Provided arguments have invalid values.
        """
        form = {"name": name}
        path = f"{_PATH}/{custom_list_uuid}"
        await self._connector.do_patch(path=path, json=form, tag=tag)

    async def filter_items(
        self,
        custom_list_uuid: uuid.UUID,
        *,
        cursor: Optional[Cursor] = None,
        limit: Optional[int] = None,
    ) -> AsyncPage[RefView]:
        """Get custom list items.

        .. versionadded:: 2.14.0
        Note:
            Calls `GET /custom-lists/{custom_list_uuid}/items`.
        Args:
            custom_list_uuid: Custom list UUID.
            cursor: Page cursor.
            limit: Page limit.
        Returns:
            Page with custom list items and next page cursor.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: Custom list not found.
            :class:`~cybsi.api.error.InvalidRequestError`:
                Provided arguments have invalid values.
        """
        params: Dict[str, Any] = {}
        if cursor:
            params["cursor"] = cursor
        if limit:
            params["limit"] = limit
        path = f"{_PATH}/{custom_list_uuid}/items"
        resp = await self._connector.do_get(path=path, params=params)
        page = AsyncPage(self._connector.do_get, resp, RefView)
        return page

    async def add_item(
        self, custom_list_uuid: uuid.UUID, dictionary_item_uuid: uuid.UUID
    ) -> None:
        """Add item to custom list.

        .. versionadded:: 2.14.0
        Note:
            Calls `POST /custom-lists/{custom_list_uuid}/items`.
        Args:
            custom_list_uuid: Custom list UUID.
            dictionary_item_uuid: Dictionary item UUID.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: Custom list not found.
            :class:`~cybsi.api.error.SemanticError`: Form contains logic errors.
            :class:`~cybsi.api.error.InvalidRequestError`:
                Provided arguments have invalid values.
        Note:
            Semantic error codes specific for this method:
            * :attr:`cybsi.api.error.SemanticErrorCodes.DictionaryItemNotFound`
            * :attr:`cybsi.api.error.SemanticErrorCodes.DictionaryMismatch`
        """
        params = {"dictionaryItemUUID": str(dictionary_item_uuid)}
        path = f"{_PATH}/{custom_list_uuid}/items"
        await self._connector.do_post(path=path, json=params)

    async def delete_item(
        self, custom_list_uuid: uuid.UUID, dictionary_item_uuid: uuid.UUID
    ) -> None:
        """Delete item from custom list.

        .. versionadded:: 2.14.0
        Note:
            Calls `DELETE /custom-lists/{custom_list_uuid}/items/{item_uuid}`.
        Args:
            custom_list_uuid: Custom list UUID.
            dictionary_item_uuid: Dictionary item UUID.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: Custom list not found.
            :class:`~cybsi.api.error.InvalidRequestError`:
                Provided arguments have invalid values.
        """
        path = f"{_PATH}/{custom_list_uuid}/items/{dictionary_item_uuid}"
        await self._connector.do_delete(path=path)

    async def get_related_items(
        self,
        custom_list_uuid: uuid.UUID,
        dictionary_uuid: uuid.UUID,
        *,
        cursor: Optional[Cursor] = None,
        limit: Optional[int] = None,
    ) -> AsyncPage[RefView]:
        """Get dictionary items that are related to custom list.

        .. versionadded:: 2.14.0
        Note:
            Calls `GET /custom-lists/{custom_list_uuid}/related-items`.
        Args:
            custom_list_uuid: Custom list UUID.
            dictionary_uuid: Dictionary UUID.
            cursor: Page cursor.
            limit: Page limit.
        Returns:
            Page with related items and next page cursor.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: Custom list not found.
            :class:`~cybsi.api.error.SemanticError`: Form contains logic errors.
            :class:`~cybsi.api.error.InvalidRequestError`:
                Provided arguments have invalid values.
        Note:
            Semantic error codes specific for this method:
            * :attr:`cybsi.api.error.SemanticErrorCodes.DictionaryNotFound`
        """
        params: Dict[str, Any] = {"dictionaryUUID": str(dictionary_uuid)}
        if cursor:
            params["cursor"] = cursor
        if limit:
            params["limit"] = limit

        path = f"{_PATH}/{custom_list_uuid}/related-items"
        resp = await self._connector.do_get(path=path, params=params)
        page = AsyncPage(self._connector.do_get, resp, RefView)
        return page


class CustomListForm(JsonObjectForm):
    """Custom list form.

    Args:
        custom_list_id: String id of custom list.
        name: String name of custom list.
        dictionary_uuid: UUID of dictionary attached to custom list.
    """

    def __init__(
        self,
        custom_list_id: str,
        name: str,
        dictionary_uuid: uuid.UUID,
    ):
        super().__init__()
        self._data["id"] = custom_list_id
        self._data["name"] = name
        self._data["dictionaryUuid"] = str(dictionary_uuid)


class CustomListCommonView(RefView):
    """Custom list short view."""

    @property
    def id(self) -> str:
        """String id of custom list."""
        return self._get("id")

    @property
    def name(self) -> str:
        """String name of custom list."""
        return self._get("name")

    @property
    def dictionary(self) -> RefView:
        """Dictionary ref for custom list."""
        return self._get("dictionary")


class CustomListView(_TaggedRefView, CustomListCommonView):
    """Custom list full view."""
