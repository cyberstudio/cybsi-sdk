import uuid
from typing import Any, Dict, List, Optional

from .. import RefView
from ..api import Tag
from ..error import CybsiError, SemanticError, SemanticErrorCodes
from ..internal import BaseAPI, JsonObjectForm, JsonObjectView
from ..pagination import Cursor, Page
from ..view import _TaggedRefView
from .enums import QueryCompatibility
from .error import CybsiLangErrorCodes


class StoredQueriesAPI(BaseAPI):
    """Stored queries API."""

    _path = "/search/stored-queries"
    _validate_path = "/search/query"

    def register(self, stored_query: "StoredQueryForm") -> RefView:
        """Register a stored query.

        Note:
            Calls `POST /search/stored-queries`.
        Args:
            stored_query: Stored query registration form.
        Returns:
            Reference to a registered stored query.
        Raises:
            :class:`~cybsi.api.error.SemanticError`: Form contains logic errors.
        Note:
            Semantic error codes specific for this method:
              * :attr:`~cybsi.api.error.SemanticErrorCodes.InvalidQueryText`
        """
        r = self._connector.do_post(path=self._path, json=stored_query.json())
        return RefView(r.json())

    def view(self, query_uuid: uuid.UUID) -> "StoredQueryView":
        """Get a stored query view.

        Note:
            Calls `GET /search/stored-queries/{query_uuid}`.
        Args:
            query_uuid: Stored query uuid.
        Returns:
            View of the stored query.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: Stored query not found.
        """
        path = f"{self._path}/{query_uuid}"
        r = self._connector.do_get(path)
        return StoredQueryView(r)

    def validate(
        self, text: str, compatibility: QueryCompatibility
    ) -> "StoredQueryValidationView":
        """Validates search query.

        Note:
            Calls `PUT /search/query`.
        Args:
            text: Text of the query.
            compatibility: Compatibility scope for query text.
        Returns:
            View of the validation results.
        """
        data = {"text": text, "compatibility": compatibility.value}
        r = self._connector.do_put(self._validate_path, data)
        return StoredQueryValidationView(r.json())

    def edit(
        self,
        query_uuid: uuid.UUID,
        tag: Tag,
        *,
        name: Optional[str] = None,
        text: Optional[str] = None,
    ) -> None:
        """Edit the stored query.

        Note:
            Calls `PATCH /search/stored-queries/{query_uuid}`.
        Args:
            query_uuid: Stored query uuid.
            tag: :attr:`StoredQueryView.tag` value. Use :meth:`view` to retrieve it.
            name: New stored query name, non-empty if not :data:`None`.
            text: New stored query text, non-empty if not :data:`None`.
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
        form: Dict[str, Any] = {}
        if name is not None:
            form["name"] = name
        if text is not None:
            form["text"] = text
        path = f"{self._path}/{query_uuid}"
        self._connector.do_patch(path=path, tag=tag, json=form)

    def filter(
        self,
        *,
        user_uuid: Optional[uuid.UUID] = None,
        cursor: Optional[Cursor] = None,
        limit: Optional[int] = None,
    ) -> Page["StoredQueryView"]:
        """Get page of filtered stored queries list.

        Note:
            Calls `GET /search/stored-queries`
        Args:
            user_uuid: User's identifier.
                Filter stored queries by author's id.
            cursor: Page cursor.
            limit: Page limit.
        Returns:
            Page of filtered stored queries list and next page cursor.
        Raises:
            :class:`~cybsi.api.error.SemanticError`: query arguments contain errors.
        Note:
            Semantic error codes specific for this method:
              * :attr:`~cybsi.api.error.SemanticErrorCodes.UserNotFound`
        """
        params: Dict[str, Any] = {}

        if user_uuid is not None:
            params["userUUID"] = str(user_uuid)
        if cursor:
            params["cursor"] = str(cursor)
        if limit:
            params["limit"] = str(limit)

        resp = self._connector.do_get(self._path, params=params)
        page = Page(self._connector.do_get, resp, StoredQueryView)
        return page


class StoredQueryForm(JsonObjectForm):
    """Stored query form.

    This is the form you need to fill to register stored query.

    Args:
        name: Name of the stored query, non-empty.
        text: Text of the stored query, non-empty.
    """

    def __init__(self, name: str, text: str):
        super().__init__()
        self._data["name"] = name
        self._data["text"] = text


class StoredQueryValidationView(JsonObjectView):
    """View of a search query validation,
    as retrieved by :meth:`StoredQueriesAPI.validate`."""

    @property
    def errors(self) -> List["CybsiLangErrorView"]:
        """Errors."""

        return [CybsiLangErrorView(err) for err in self._get("errors")]

    @property
    def warnings(self) -> List["CybsiLangErrorView"]:
        """Warnings."""

        return [CybsiLangErrorView(warn) for warn in self._get("warnings")]


class CybsiLangErrorView(JsonObjectView):
    """View of a search query validation errors."""

    @classmethod
    def from_semantic_error(cls, exc: SemanticError) -> "CybsiLangErrorView":
        """Extract CybsiLang error from semantic error.

        Args:
            exc: SemanticError exception.

        Note:
            Only :attr:`~cybsi.api.error.SemanticErrorCodes.InvalidQueryText`
            can be unwrapped
        """
        if exc.code == SemanticErrorCodes.InvalidQueryText:
            return cls(exc.content["details"])
        raise CybsiError("unexpected error code")

    @property
    def code(self) -> CybsiLangErrorCodes:
        """Code.
        See :class:`~cybsi.api.search.error.CybsiLangErrorCodes`
        for all available error codes
        """

        return CybsiLangErrorCodes(self._get("code"))

    @property
    def message(self) -> str:
        """Message."""

        return self._get("message")

    @property
    def details_raw(self) -> Dict[str, Any]:
        """Details."""

        return self._get("details")

    @property
    def position(self) -> "ErrorPosition":
        """Position of the error start."""

        return ErrorPosition(self._get("position"))

    @property
    def until_position(self) -> "ErrorPosition":
        """Position of the error end.

        Points to a symbol next to the last symbol of the error.
        """

        return ErrorPosition(self._get("untilPosition"))


class ErrorPosition(JsonObjectView):
    """Error position."""

    @property
    def line(self) -> int:
        """Line. Starts from 1."""

        return self._get("line")

    @property
    def column(self) -> int:
        """Column. Relative position from start of line.
        Starts from 1."""

        return self._get("column")

    @property
    def offset(self) -> int:
        """Offset. Absolute position from start of query text.
        Starts from 0."""

        return self._get("offset")


class StoredQueryCommonView(RefView):
    """Stored query short view,
    as retrieved by :meth:`~cybsi.api.replist.ReplistsAPI.view`."""

    @property
    def name(self) -> str:
        """Query name."""
        return self._get("name")


class StoredQueryView(_TaggedRefView, StoredQueryCommonView):
    """View of a stored query,
    as retrieved by :meth:`StoredQueriesAPI.view`."""

    @property
    def text(self) -> str:
        """Query text."""

        return self._get("text")

    @property
    def author(self) -> RefView:
        """User, author of the query."""

        return RefView(self._get("author"))
