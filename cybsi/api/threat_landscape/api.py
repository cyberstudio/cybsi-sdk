import uuid
from typing import Any, Dict, Optional, List

from cybsi.api import RefView, Tag
from cybsi.api.custom_list import CustomListCommonView
from cybsi.api.internal import BaseAPI, BaseAsyncAPI, JsonObjectForm
from cybsi.api.pagination import AsyncPage, Cursor, Page
from cybsi.api.view import _TaggedRefView

_PATH = "threat-landscapes"


class ThreatLandscapesAPI(BaseAPI):
    """
    API to operate Threat Landscapes.

    .. versionadded:: 2.14.0
    """

    def filter(
        self,
        *,
        cursor: Optional[Cursor] = None,
        limit: Optional[int] = None,
    ) -> Page["ThreatLandscapeCommonView"]:
        """
        Get a list of threat landscapes.

        .. versionadded:: 2.14.0
        Note:
            Calls `GET /threat-landscapes`
        Args:
            cursor: Page cursor
            limit: Page limit
        Raises:
            :class:`~cybsi.api.error.InvalidRequestError`:
                Provided value are invalid (see args value requirements).
        """
        params: Dict[str, Any] = {}
        if cursor:
            params["cursor"] = cursor
        if limit:
            params["limit"] = limit
        resp = self._connector.do_get(path=_PATH, params=params)
        page = Page(self._connector.do_get, resp, ThreatLandscapeCommonView)
        return page

    def register(self, landscape: "ThreatLandscapeForm") -> RefView:
        """
        Register a new threat landscape.

        .. versionadded:: 2.14.0
        Note:
            Calls `POST /threat-landscapes`
        Args:
            landscape: Threat landscape form
        Raises:
            :class:`~cybsi.api.error.InvalidRequestError`:
                Provided value are invalid (see args value requirements).
        """
        resp = self._connector.do_post(path=_PATH, json=landscape.json())
        return RefView(resp.json())

    def view(self, landscape_uuid: uuid.UUID) -> "ThreatLandscapeView":
        """
        Get a threat landscape.

        .. versionadded:: 2.14.0
        Note:
            Calls `GET /threat-landscapes/{landscape_uuid}`
        Args:
            landscape_uuid: Landscape UUID
        Returns:
            View of Threat landscape
        Raises:
            :class:`~cybsi.api.error.InvalidRequestError`:
                Provided value are invalid (see args value requirements).
            :class:`~cybsi.api.error.NotFoundError`: Threat Landscape not found.
        """

        path = f"/threat-landscapes/{landscape_uuid}"
        resp = self._connector.do_get(path=path)
        return ThreatLandscapeView(resp)

    def edit(self, landscape_uuid: uuid.UUID, tag: Tag, name: str) -> None:
        """
        Edit a Threat landscape.

        .. versionadded:: 2.14.0
        Note:
            Calls `PATCH /threat-landscapes/{landscape_uuid}`
        Args:
            landscape_uuid: Threat landscape UUID
            tag: :attr:`CustomListView.tag` value. Use :meth:`view` to retrieve it.
            name: new Threat landscape name
        Raises:
            :class:`~cybsi.api.error.InvalidRequestError`:
                Provided value are invalid (see args value requirements).
            :class:`~cybsi.api.error.NotFoundError`: Threat landscape not found.
            :class:`~cybsi.api.error.ResourceModifiedError`:
                Threat landscape changed since last request. Update tag and retry.
        """
        form = {"name": name}
        path = f"{_PATH}/{landscape_uuid}"
        self._connector.do_patch(path=path, json=form, tag=tag)

    def delete(self, landscape_uuid: uuid.UUID) -> None:
        """
        Delete a Threat landscape.

        .. versionadded:: 2.14.0
        Note:
            Calls `DELETE /threat-landscapes/{landscape_uuid}`
        Args:
            landscape_uuid: Threat landscape UUID
        Raises:
            :class:`~cybsi.api.error.InvalidRequestError`:
                Provided value are invalid (see args value requirements).
            :class:`~cybsi.api.error.NotFoundError`: Threat landscape not found.
        """
        path = f"{_PATH}/{landscape_uuid}"
        self._connector.do_delete(path=path)

    def filter_custom_lists(
        self,
        landscape_uuid: uuid.UUID,
        *,
        cursor: Optional[Cursor] = None,
        limit: Optional[int] = None,
    ) -> Page["ThreatLandscapesCustomListView"]:
        """
        Get a list of all custom lists related to a Threat landscape.

        .. versionadded:: 2.14.0
        Note:
            Calls `GET /threat-landscapes/{landscape_uuid}/custom-lists`
        Args:
            landscape_uuid: Landscape UUID
            cursor: Page cursor
            limit: Page limit
        Raises:
            :class:`~cybsi.api.error.InvalidRequestError`:
                Provided value are invalid (see args value requirements).
            :class:`~cybsi.api.error.NotFoundError`: Threat landscape not found.
        """
        params: Dict[str, Any] = {}
        if cursor:
            params["cursor"] = cursor
        if limit:
            params["limit"] = limit
        path = f"{_PATH}/{landscape_uuid}/custom-lists"
        resp = self._connector.do_get(path=path, params=params)
        page = Page(self._connector.do_get, resp, ThreatLandscapesCustomListView)
        return page

    def add_custom_list(
        self,
        landscape_uuid: uuid.UUID,
        custom_list_uuid: uuid.UUID,
    ) -> None:
        """
        Add custom list to a Threat landscape.

        .. versionadded:: 2.14.0
        Note:
            Calls `POST /threat-landscapes/{landscape_uuid}/custom-lists`
        Args:
            landscape_uuid: Landscape UUID
            custom_list_uuid: Custom list UUID
        Raises:
            :class:`~cybsi.api.error.InvalidRequestError`:
                Provided value are invalid (see args value requirements).
            :class:`~cybsi.api.error.NotFoundError`: Threat landscape not found.
            :class:`~cybsi.api.error.SemanticError`:
        Note:
            Semantic error codes specific for this method:
              * :attr:`~cybsi.api.error.SemanticErrorCodes.CustomListNotFound`
        """
        params: Dict[str, Any] = {"customListUUID": str(custom_list_uuid)}
        path = f"{_PATH}/{landscape_uuid}/custom-lists"
        self._connector.do_post(path=path, json=params)

    def delete_custom_list(
        self,
        landscape_uuid: uuid.UUID,
        custom_list_uuid: uuid.UUID,
    ) -> None:
        """
        Delete custom list to a Threat landscape.

        .. versionadded:: 2.14.0
        Note:
            Calls `DELETE /threat-landscapes/{landscape_uuid}/custom-lists`
        Args:
            landscape_uuid: Landscape UUID
            custom_list_uuid: Custom list UUID
        Raises:
            :class:`~cybsi.api.error.InvalidRequestError`:
                Provided value are invalid (see args value requirements).
            :class:`~cybsi.api.error.NotFoundError`: Threat landscape not found.
        """
        path = f"{_PATH}/{landscape_uuid}/custom-lists/{custom_list_uuid}"
        self._connector.do_delete(path=path)

    def add_related_dictionary(
        self,
        landscape_uuid: uuid.UUID,
        dictionary_uuid: uuid.UUID,
        custom_list_uuid: uuid.UUID,
    ) -> None:
        """
        Add related dictionary to custom list of Threat landscape.

        .. versionadded:: 2.14.0
        Note:
            Calls `POST /threat-landscapes/{landscapeUUID}/
                    custom-lists/{customListUUID}/related-dictionaries`
        Args:
            landscape_uuid: Landscape UUID
            dictionary_uuid: Dictionary UUID
            custom_list_uuid: Custom list UUID
        Raises:
            :class:`~cybsi.api.error.InvalidRequestError`:
                Provided value are invalid (see args value requirements).
            :class:`~cybsi.api.error.NotFoundError`:
                Threat landscape or custom list not found.
            :class:`~cybsi.api.error.SemanticError`:
        Note:
            Semantic error codes specific for this method:
              * :attr:`~cybsi.api.error.SemanticErrorCodes.DictionaryNotFound`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.DictionaryMismatch`

        """
        params: Dict[str, Any] = {"dictionaryUUID": str(dictionary_uuid)}
        path = (
            f"{_PATH}/{landscape_uuid}/custom-lists/"
            f"{custom_list_uuid}/related-dictionaries"
        )
        self._connector.do_post(path=path, json=params)

    def delete_related_dictionary(
        self,
        landscape_uuid: uuid.UUID,
        dictionary_uuid: uuid.UUID,
        custom_list_uuid: uuid.UUID,
    ) -> None:
        """
        Add related dictionary to custom list of Threat landscape.

        .. versionadded:: 2.14.0
        Note:
            Calls `DELETE /threat-landscapes/{landscapeUUID}/custom-lists/
                    {customListUUID}/related-dictionaries/{dictionary_uuid}/related-dictionaries/{dictionary_uuid}`
        Args:
            landscape_uuid: Landscape UUID
            dictionary_uuid: Dictionary UUID
            custom_list_uuid: Custom list UUID
        Raises:
            :class:`~cybsi.api.error.InvalidRequestError`:
                Provided value are invalid (see args value requirements).
            :class:`~cybsi.api.error.NotFoundError`:
                Threat landscape or custom list not found.

        """
        path = (
            f"{_PATH}/{landscape_uuid}/custom-lists/"
            f"{custom_list_uuid}/related-dictionaries/{dictionary_uuid}"
        )
        self._connector.do_delete(path=path)

    def build_query(
        self,
        landscape_uuid: uuid.UUID,
        *,
        data_source_uuid: Optional[uuid.UUID] = None,
    ) -> str:
        """
        Build a query for a Threat landscape.

        .. versionadded:: 2.14.0
        Note:
            Calls `GET /threat-landscapes/{landscapeUUID}/query`
        Args:
            landscape_uuid: Landscape UUID
            data_source_uuid: Data source UUID
        Raises:
            :class:`~cybsi.api.error.InvalidRequestError`:
                Provided value are invalid (see args value requirements).
            :class:`~cybsi.api.error.NotFoundError`: Threat landscape not found.
            :class:`~cybsi.api.error.SemanticError`:
        Note:
            Semantic error codes specific for this method:
            * :attr:`~cybsi.api.error.SemanticErrorCodes.DataSourceNotFound`
            * :attr:`~cybsi.api.error.SemanticErrorCodes.EmptyLandscapeQuery`
        """
        params: Dict[str, Any] = {}
        if data_source_uuid:
            params["dataSourceUUID"] = str(data_source_uuid)
        path = f"{_PATH}/{landscape_uuid}/query"
        resp = self._connector.do_post(path=path, json=params)
        return resp.json().get("query")


class ThreatLandscapesAsyncAPI(BaseAsyncAPI):
    """
    async API to operate Threat Landscapes.

    .. versionadded:: 2.14.0
    """

    async def filter(
        self,
        *,
        cursor: Optional[Cursor] = None,
        limit: Optional[int] = None,
    ) -> AsyncPage["ThreatLandscapeCommonView"]:
        """
        Get a list of all threat landscapes.

        .. versionadded:: 2.14.0
        Note:
            Calls `GET /threat-landscapes`
        Args:
            cursor: Page cursor
            limit: Page limit
        Raises:
            :class:`~cybsi.api.error.InvalidRequestError`:
                Provided value are invalid (see args value requirements).
        """
        params: Dict[str, Any] = {}
        if cursor:
            params["cursor"] = cursor
        if limit:
            params["limit"] = limit
        resp = await self._connector.do_get(path=_PATH, params=params)
        page = AsyncPage(self._connector.do_get, resp, ThreatLandscapeCommonView)
        return page

    async def register(self, landscape: "ThreatLandscapeForm") -> RefView:
        """
        Register a new threat landscape.

        .. versionadded:: 2.14.0
        Note:
            Calls `POST /threat-landscapes`
        Args:
            landscape: Threat landscape form
        Raises:
            :class:`~cybsi.api.error.InvalidRequestError`:
                Provided value are invalid (see args value requirements).
        """
        resp = await self._connector.do_post(path=_PATH, json=landscape.json())
        return RefView(resp.json())

    async def view(self, landscape_uuid: uuid.UUID) -> "ThreatLandscapeView":
        """
        Get a threat landscape.

        .. versionadded:: 2.14.0
        Note:
            Calls `GET /threat-landscapes/{landscape_uuid}`
        Args:
            landscape_uuid: Landscape UUID
        Returns:
            View of Threat landscape
        Raises:
            :class:`~cybsi.api.error.InvalidRequestError`:
                Provided value are invalid (see args value requirements).
            :class:`~cybsi.api.error.NotFoundError`: Threat Landscape not found.
        """

        path = f"/threat-landscapes/{landscape_uuid}"
        resp = await self._connector.do_get(path=path)
        return ThreatLandscapeView(resp)

    async def edit(self, landscape_uuid: uuid.UUID, tag: Tag, name: str) -> None:
        """
        Edit a Threat landscape.

        .. versionadded:: 2.14.0
        Note:
            Calls `PATCH /threat-landscapes/{landscape_uuid}`
        Args:
            landscape_uuid: Threat landscape UUID
            tag: :attr:`CustomListView.tag` value. Use :meth:`view` to retrieve it.
            name: new Threat landscape name
        Raises:
            :class:`~cybsi.api.error.InvalidRequestError`:
                Provided value are invalid (see args value requirements).
            :class:`~cybsi.api.error.NotFoundError`: Threat landscape not found.
            :class:`~cybsi.api.error.ResourceModifiedError`:
                Threat landscape changed since last request. Update tag and retry.
        """
        form = {"name": name}
        path = f"{_PATH}/{landscape_uuid}"
        await self._connector.do_patch(path=path, json=form, tag=tag)

    async def delete(self, landscape_uuid: uuid.UUID) -> None:
        """
        Delete a Threat landscape.

        .. versionadded:: 2.14.0
        Note:
            Calls `DELETE /threat-landscapes/{landscape_uuid}`
        Args:
            landscape_uuid: Threat landscape UUID
        Raises:
            :class:`~cybsi.api.error.InvalidRequestError`:
                Provided value are invalid (see args value requirements).
            :class:`~cybsi.api.error.NotFoundError`: Threat landscape not found.
        """
        path = f"{_PATH}/{landscape_uuid}"
        await self._connector.do_delete(path=path)

    async def filter_custom_lists(
        self,
        landscape_uuid: uuid.UUID,
        *,
        cursor: Optional[Cursor] = None,
        limit: Optional[int] = None,
    ) -> AsyncPage["ThreatLandscapesCustomListView"]:
        """
        Get a list of all custom lists related to a Threat landscape.

        .. versionadded:: 2.14.0
        Note:
            Calls `GET /threat-landscapes/{landscape_uuid}/custom-lists`
        Args:
            landscape_uuid: Landscape UUID
            cursor: Page cursor
            limit: Page limit
        Raises:
            :class:`~cybsi.api.error.InvalidRequestError`:
                Provided value are invalid (see args value requirements).
            :class:`~cybsi.api.error.NotFoundError`: Threat landscape not found.
        """
        params: Dict[str, Any] = {}
        if cursor:
            params["cursor"] = cursor
        if limit:
            params["limit"] = limit
        path = f"{_PATH}/{landscape_uuid}/custom-lists"
        resp = await self._connector.do_get(path=path, params=params)
        page = AsyncPage(self._connector.do_get, resp, ThreatLandscapesCustomListView)
        return page

    async def add_custom_list(
        self,
        landscape_uuid: uuid.UUID,
        custom_list_uuid: uuid.UUID,
    ) -> None:
        """
        Add custom list to a Threat landscape.

        .. versionadded:: 2.14.0
        Note:
            Calls `POST /threat-landscapes/{landscape_uuid}/custom-lists`
        Args:
            landscape_uuid: Landscape UUID
            custom_list_uuid: Custom list UUID
        Raises:
            :class:`~cybsi.api.error.InvalidRequestError`:
                Provided value are invalid (see args value requirements).
            :class:`~cybsi.api.error.NotFoundError`: Threat landscape not found.
            :class:`~cybsi.api.error.SemanticError`:
        Note:
            Semantic error codes specific for this method:
              * :attr:`~cybsi.api.error.SemanticErrorCodes.CustomListNotFound`
        """
        params: Dict[str, Any] = {"customListUUID": str(custom_list_uuid)}
        path = f"{_PATH}/{landscape_uuid}/custom-lists"
        await self._connector.do_post(path=path, json=params)

    async def delete_custom_list(
        self,
        landscape_uuid: uuid.UUID,
        custom_list_uuid: uuid.UUID,
    ) -> None:
        """
        Delete custom list to a Threat landscape.

        .. versionadded:: 2.14.0
        Note:
            Calls `DELETE /threat-landscapes/{landscape_uuid}/custom-lists`
        Args:
            landscape_uuid: Landscape UUID
            custom_list_uuid: Custom list UUID
        Raises:
            :class:`~cybsi.api.error.InvalidRequestError`:
                Provided value are invalid (see args value requirements).
            :class:`~cybsi.api.error.NotFoundError`: Threat landscape not found.
        """
        path = f"{_PATH}/{landscape_uuid}/custom-lists/{custom_list_uuid}"
        await self._connector.do_delete(path=path)

    async def add_related_dictionary(
        self,
        landscape_uuid: uuid.UUID,
        dictionary_uuid: uuid.UUID,
        custom_list_uuid: uuid.UUID,
    ) -> None:
        """
        Add related dictionary to custom list of Threat landscape.

        .. versionadded:: 2.14.0
        Note:
            Calls `POST /threat-landscapes/{landscapeUUID}/
                    custom-lists/{customListUUID}/related-dictionaries`
        Args:
            landscape_uuid: Landscape UUID
            dictionary_uuid: Dictionary UUID
            custom_list_uuid: Custom list UUID
        Raises:
            :class:`~cybsi.api.error.InvalidRequestError`:
                Provided value are invalid (see args value requirements).
            :class:`~cybsi.api.error.NotFoundError`:
                Threat landscape or custom list not found.
            :class:`~cybsi.api.error.SemanticError`:
        Note:
            Semantic error codes specific for this method:
              * :attr:`~cybsi.api.error.SemanticErrorCodes.DictionaryNotFound`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.DictionaryMismatch`

        """
        params: Dict[str, Any] = {"dictionaryUUID": str(dictionary_uuid)}
        path = (
            f"{_PATH}/{landscape_uuid}/custom-lists/"
            f"{custom_list_uuid}/related-dictionaries"
        )
        await self._connector.do_post(path=path, json=params)

    async def delete_related_dictionary(
        self,
        landscape_uuid: uuid.UUID,
        dictionary_uuid: uuid.UUID,
        custom_list_uuid: uuid.UUID,
    ) -> None:
        """
        Add related dictionary to custom list of Threat landscape.

        .. versionadded:: 2.14.0
        Note:
            Calls `DELETE /threat-landscapes/{landscapeUUID}/custom-lists/
                    {customListUUID}/related-dictionaries/{dictionary_uuid}/related-dictionaries/{dictionary_uuid}`
        Args:
            landscape_uuid: Landscape UUID
            dictionary_uuid: Dictionary UUID
            custom_list_uuid: Custom list UUID
        Raises:
            :class:`~cybsi.api.error.InvalidRequestError`:
                Provided value are invalid (see args value requirements).
            :class:`~cybsi.api.error.NotFoundError`:
                Threat landscape or custom list not found.

        """
        path = (
            f"{_PATH}/{landscape_uuid}/custom-lists/"
            f"{custom_list_uuid}/related-dictionaries/{dictionary_uuid}"
        )
        await self._connector.do_delete(path=path)

    async def build_query(
        self,
        landscape_uuid: uuid.UUID,
        *,
        data_source_uuid: Optional[uuid.UUID] = None,
    ) -> str:
        """
        Build a query for a Threat landscape.

        .. versionadded:: 2.14.0
        Note:
            Calls `GET /threat-landscapes/{landscapeUUID}/query`
        Args:
            landscape_uuid: Landscape UUID
            data_source_uuid: Data source UUID
        Raises:
            :class:`~cybsi.api.error.InvalidRequestError`:
                Provided value are invalid (see args value requirements).
            :class:`~cybsi.api.error.NotFoundError`: Threat landscape not found.
            :class:`~cybsi.api.error.SemanticError`:
        Note:
            Semantic error codes specific for this method:
            * :attr:`~cybsi.api.error.SemanticErrorCodes.DataSourceNotFound`
            * :attr:`~cybsi.api.error.SemanticErrorCodes.EmptyLandscape`
        """
        params: Dict[str, Any] = {}
        if data_source_uuid:
            params["dataSourceUUID"] = str(data_source_uuid)
        path = f"{_PATH}/{landscape_uuid}/query"
        resp = await self._connector.do_post(path=path, json=params)
        return resp.json().get("query")


class ThreatLandscapeForm(JsonObjectForm):
    """
    Threat Landscape Form. Use to add Threat Landscapes.

    Args:
        name: name of the Threat Landscape
    """

    def __init__(self, name: str):
        super().__init__()
        self._data["name"] = name


class ThreatLandscapeCommonView(RefView):
    """
    Threat Landscape short view
    """

    @property
    def name(self) -> str:
        """
        Threat Landscape name
        """
        return self._get("name")


class ThreatLandscapeView(_TaggedRefView, ThreatLandscapeCommonView):
    """
    Threat Landscape full view
    """


class ThreatLandscapesCustomListView(RefView):
    """
    Threat Landscape's custom list view
    """

    @property
    def custom_list(self) -> CustomListCommonView:
        return CustomListCommonView(self._get("customList"))

    @property
    def dictionaries(self) -> List[RefView]:
        return [RefView(dictionary) for dictionary in self._get("dictionaries")]
