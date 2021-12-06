import uuid

from typing import List, Dict, Any

from .enums import QueryCompatibility
from .error import CybsiLangErrorCodes
from ..common import RefView
from ..error import SemanticError, SemanticErrorCodes, CybsiError
from ..internal import (
    BaseAPI,
    JsonObjectForm,
    JsonObjectView,
)


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
        return StoredQueryView(r.json())

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


class StoredQueryForm(JsonObjectForm):
    """Stored query form.

    This is the form you need to fill to register stored query.

    Args:
        name: Name of the stored query.
        text: Text of the stored query.
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
        """Position."""

        return ErrorPosition(self._get("position"))


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
    as retrieved by :meth:`ReplistsAPI.view`."""

    @property
    def name(self) -> str:
        """Query name."""
        return self._get("name")


class StoredQueryView(StoredQueryCommonView):
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
