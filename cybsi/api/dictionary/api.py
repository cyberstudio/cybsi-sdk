import uuid
from typing import Any, Dict, Optional

from .. import RefView
from ..internal import BaseAPI, JsonObjectForm
from ..pagination import Cursor, Page


class DictionariesAPI(BaseAPI):
    """API to operate dictionaries.

    .. versionadded:: 2.9
    """

    _path = "/dictionaries"
    _path_dictionary_items = "/dictionary-items"

    def view(self, dictionary_uuid: uuid.UUID) -> "DictionaryView":
        """Get the dictionary view.

        Note:
            Calls `GET /dictionaries/{dictionary_uuid}`.
        Args:
            dictionary_uuid: Dictionary UUID.
        Returns:
            View of the dictionary.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: Dictionary not found.
        """
        path = f"{self._path}/{dictionary_uuid}"
        r = self._connector.do_get(path)
        return DictionaryView(r.json())

    def filter(
        self,
        *,
        cursor: Optional[Cursor] = None,
        limit: Optional[int] = None,
    ) -> Page["DictionaryView"]:
        """Get a filtered list of dictionaries.

        Results are sorted in alphabetical order by dictionary name.

        Note:
            Calls `GET /dictionaries`.
        Args:
            cursor: Page cursor.
            limit: Page limit.
        Returns:
            Page with dictionary views and next page cursor.
        Usage:
            >>> import uuid
            >>> from cybsi.api import CybsiClient
            >>> from cybsi.api.pagination import chain_pages
            >>>
            >>> client: CybsiClient
            >>>
            >>> started_page = client.dictionaries.filter()
            >>> for item in chain_pages(started_page):
            >>>     # do something with dictionaries
            >>>     print(item)
            >>> pass
        """

        params: Dict[str, Any] = {}
        if cursor:
            params["cursor"] = str(cursor)
        if limit:
            params["limit"] = str(limit)

        resp = self._connector.do_get(path=self._path, params=params)
        page = Page(self._connector.do_get, resp, DictionaryView)
        return page

    def view_item(self, item_uuid: uuid.UUID) -> "DictionaryItemView":
        """Get the dictionary item view.

        Note:
            Calls `GET /dictionary-items/{item_uuid}`.
        Args:
            item_uuid: Dictionary item UUID.
        Returns:
            View of the dictionary item.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: Dictionary item not found.
        """
        path = f"{self._path_dictionary_items}/{item_uuid}"
        r = self._connector.do_get(path)
        return DictionaryItemView(r.json())

    def filter_items(
        self,
        dictionary_uuid: uuid.UUID,
        *,
        prefix: Optional[str] = None,
        cursor: Optional[Cursor] = None,
        limit: Optional[int] = None,
    ) -> Page["DictionaryCommonItemView"]:
        """Get a filtered list of dictionary items.

        Results are sorted in alphabetical order by dictionary item name.

        Note:
            Calls `GET /dictionaries/{dictionaryUUID}/items`.
        Args:
            dictionary_uuid: Open dictionary UUID.
            prefix: Dictionary item name prefix (case-insensitive).
                Prefix length must be in range [1;30].
            cursor: Page cursor.
            limit: Page limit.
        Returns:
            Page with dictionary items common views and next page cursor.
        Usage:
            >>> import uuid
            >>> from cybsi.api import CybsiClient
            >>> from cybsi.api.pagination import chain_pages
            >>>
            >>> client: CybsiClient
            >>>
            >>> started_page = client.dictionaries.filter_items(
            >>>     dictionary_uuid=uuid.UUID("89200bef-2f50-4d4f-8b38-843d5ab9dfa9"),
            >>> )
            >>> for item in chain_pages(started_page):
            >>>     # do something with dictionary items
            >>>     print(item)
            >>> pass
        """

        params: Dict[str, Any] = {}
        if prefix is not None:
            params["prefix"] = prefix
        if cursor:
            params["cursor"] = str(cursor)
        if limit:
            params["limit"] = str(limit)

        path = f"{self._path}/{dictionary_uuid}/items"
        resp = self._connector.do_get(path=path, params=params)
        page = Page(self._connector.do_get, resp, DictionaryCommonItemView)
        return page


class DictionaryView(RefView):
    """Dictionary view."""

    @property
    def name(self) -> str:
        """Dictionary name."""
        return self._get("name")


class DictionaryCommonItemView(RefView):
    """Dictionary item common view."""

    @property
    def key(self) -> str:
        """Dictionary item key."""
        return self._get("key")


class DictionaryItemView(DictionaryCommonItemView):
    """Dictionary item view."""

    @property
    def dictionary(self) -> RefView:
        """Reference to dictionary."""
        return self._get("dictionary")


class DictItemAttributeValue(JsonObjectForm):
    """Dictionary item. Used as attribute value to create a general observation.
    See :meth:`~cybsi.api.observation.generic.GenericObservationForm.add_attribute_fact`

    Args:
       key: Dictionary item key.
    """

    def __init__(self, *, key: str):
        super().__init__()
        self._data["key"] = key
