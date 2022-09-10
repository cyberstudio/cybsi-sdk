import uuid
from typing import Any, Dict, Optional

from .. import RefView
from ..api import Tag
from ..internal import BaseAPI, JsonObjectForm
from ..pagination import Cursor, Page
from ..view import _TaggedRefView


class DictionariesAPI(BaseAPI):
    """API to operate dictionaries.

    .. versionadded:: 2.9
    """

    _path = "/dictionaries"
    _path_dictionary_items = "/dictionary-items"

    def view(self, dictionary_uuid: uuid.UUID) -> "DictionaryView":
        """Get the dictionary view.

        .. versionadded:: 2.9
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
    ) -> Page["DictionaryCommonView"]:
        """Get a filtered list of dictionaries.

        Results are sorted in alphabetical order by dictionary name.

        .. versionadded:: 2.9
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
        page = Page(self._connector.do_get, resp, DictionaryCommonView)
        return page

    def register_item(
        self, *, dictionary_uuid: uuid.UUID, item: "DictionaryItemForm"
    ) -> RefView:
        """Register item for the dictionary.

        .. versionadded:: 2.9
        Note:
            Calls `POST /dictionary-items`.
        Args:
            dictionary_uuid: Dictionary UUID.
            item: Filled dictionary item form.
        Returns:
            Reference to a newly added dictionary item.
        Raises:
            :class:`~cybsi.api.error.InvalidRequestError`:
                Provided values are invalid (see form value requirements).
            :class:`~cybsi.api.error.ConflictError`: Dictionary item already exists
                for the specified dictionary with the same key and
                a different non-empty description. An empty description in the form
                does not cause the conflict.
        """

        item._data["dictionaryUUID"] = dictionary_uuid
        r = self._connector.do_post(path=self._path_dictionary_items, json=item.json())
        return RefView(r.json())

    def view_item(self, item_uuid: uuid.UUID) -> "DictionaryItemView":
        """Get the dictionary item view.

        .. versionadded:: 2.9
        Note:
            Calls `GET /dictionary-items/{item_uuid}`.
        Args:
            item_uuid: Dictionary item UUID.
        Returns:
            View of the dictionary item with tag.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: Dictionary item not found.
        """
        path = f"{self._path_dictionary_items}/{item_uuid}"
        r = self._connector.do_get(path)
        return DictionaryItemView(r)

    def edit_item(
        self,
        item_uuid: uuid.UUID,
        tag: Tag,
        *,
        description: Optional[str] = None,
    ) -> None:
        """Edit the dictionary item.

        .. versionadded:: 2.9
        Note:
            Calls `PATCH /dictionary-items/{item_uuid}`.
        Args:
            item_uuid: Dictionary item UUID.
            tag: :attr:`DictionaryItemView.tag` value. Use :meth:`view_item`
                to retrieve it.
            description: Dictionary item description.
                Length must be in range [1;3000].
        Raises:
            :class:`~cybsi.api.error.InvalidRequestError`:
                Provided value are invalid (see args value requirements).
            :class:`~cybsi.api.error.NotFoundError`: Dictionary item not found.
            :class:`~cybsi.api.error.ResourceModifiedError`:
                Dictionary item changed since last request. Update tag and retry.
        """
        form = {}
        if description is not None:
            form["description"] = description

        path = f"{self._path_dictionary_items}/{item_uuid}"
        self._connector.do_patch(path=path, tag=tag, json=form)

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

        .. versionadded:: 2.9
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

    def add_item_synonym(
        self, *, item_uuid: uuid.UUID, synonym_uuid: uuid.UUID
    ) -> None:
        """Add dictionary item to synonym group.

        .. versionadded:: 2.9
        Note:
            Calls `PUT /dictionary-items/{item_uuid}/synonyms`.
        Args:
            item_uuid: Dictionary item UUID.
            synonym_uuid: Synonym item UUID.
        Raises:
            :class:`~cybsi.api.error.SemanticError`: Form contains logic errors.
            :class:`~cybsi.api.error.InvalidRequestError`:
                Provided values are invalid (see form value requirements).
            :class:`~cybsi.api.error.NotFoundError`: Dictionary item not found.
        Note:
            Semantic error codes specific for this method:
              * :attr:`~cybsi.api.error.SemanticErrorCodes.InvalidDictionary`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.SynonymGroupConflict`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.ItemAlreadyInSynonymGroup`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.InvalidSynonym`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.DictionaryItemNotFound`
        """

        form = {"synonymUUID": str(synonym_uuid)}
        path = f"{self._path_dictionary_items}/{item_uuid}/synonyms"
        self._connector.do_put(path=path, json=form)

    def remove_item_synonym(self, item_uuid: uuid.UUID) -> None:
        """Remove dictionary item from synonym group.

        .. versionadded:: 2.9
        Note:
            Calls `DELETE /dictionary-items/{item_uuid}/synonyms`.
        Args:
            item_uuid: Dictionary item UUID.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: Dictionary item not found.
        """

        path = f"{self._path_dictionary_items}/{item_uuid}/synonyms"
        self._connector.do_delete(path=path)


class DictionaryCommonView(RefView):
    """Dictionary common view."""

    @property
    def name(self) -> str:
        """Dictionary name."""
        return self._get("name")


class DictionaryView(DictionaryCommonView):
    """Dictionary detailed view."""

    @property
    def description(self) -> Optional[str]:
        """Dictionary description."""
        return self._get_optional("description")


class DictionaryCommonItemView(RefView):
    """Dictionary item common view."""

    @property
    def key(self) -> str:
        """Dictionary item key."""
        return self._get("key")


class DictionaryItemView(_TaggedRefView, DictionaryCommonItemView):
    """Dictionary item detailed view."""

    @property
    def dictionary(self) -> RefView:
        """Reference to dictionary."""
        return self._get("dictionary")

    @property
    def description(self) -> Optional[str]:
        """Dictionary item description."""
        return self._get_optional("description")

    @property
    def synonyms(self) -> Optional[RefView]:
        """List of refs to dictionary item that are synonyms."""
        return self._map_list_optional("synonyms", RefView)


class DictionaryItemForm(JsonObjectForm):
    """Dictionary item form. Use to add dictionary item.

    Args:
        key: Dictionary item key. The key should consist of characters
            according to the pattern `[a-zA-Z0-9_ -]` and
            have length in the range `[1;30]`.
            User-specified key case is preserved.
    """

    def __init__(self, *, key: str):
        super().__init__()
        self._data["key"] = key


class DictItemAttributeValue(JsonObjectForm):
    """Dictionary item. Used as attribute value to create a general observation.
    See :meth:`~cybsi.api.observation.generic.GenericObservationForm.add_attribute_fact`

    Args:
       key: Dictionary item key. The key should consist of characters
            according to the pattern `[a-zA-Z0-9_ -]` and
            have length in the range `[1;30]`.
            User-specified key case is preserved.
    """

    def __init__(self, *, key: str):
        super().__init__()
        self._data["key"] = key
