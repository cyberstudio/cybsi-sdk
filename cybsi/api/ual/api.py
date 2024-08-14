import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from ..internal import (
    BaseAPI,
    JsonObject,
    JsonObjectView,
    parse_rfc3339_timestamp,
    rfc3339_timestamp,
)
from ..pagination import Cursor, Page
from .enums import ObjectDomain, ObjectType, Operation, Result


class AccessLogsAPI(BaseAPI):
    """User access logs API."""

    _path = "/access-log/entries"

    def filter_entries(
        self,
        *,
        user_uuid: Optional[uuid.UUID] = None,
        operation: Optional[Operation] = None,
        object_type: Optional[ObjectType] = None,
        object_domain: Optional[ObjectDomain] = None,
        since: Optional[datetime] = None,
        till: Optional[datetime] = None,
        cursor: Optional[Cursor] = None,
        limit: Optional[int] = None,
    ) -> Page["EntryView"]:
        """Get list of user access log entry.

        Note:
            Calls `GET /access-log/entries`.
        Args:
            user_uuid: User UUID.
            operation: Operation.
            object_type: Object type.
            object_domain: Object domain.
            since: Start of time range for date/time filtering.
            till: End of time range for date/time filtering.
            cursor: Page cursor.
            limit: Page limit.
        Returns:
            Page with entries and next page cursor.
        Raises:
            :class:`~cybsi.api.error.InvalidRequestError`:
                Provided arguments have invalid values.
        """

        params: Dict[str, Any] = {}
        if user_uuid is not None:
            params["userUUID"] = str(user_uuid)
        if operation is not None:
            params["operation"] = operation.value
        if object_type is not None:
            params["objectType"] = object_type.value
        if object_domain is not None:
            params["objectDomain"] = object_domain.value
        if since is not None:
            params["since"] = rfc3339_timestamp(since)
        if till is not None:
            params["till"] = rfc3339_timestamp(till)
        if cursor:
            params["cursor"] = str(cursor)
        if limit:
            params["limit"] = limit

        resp = self._connector.do_get(path=self._path, params=params)
        return Page(self._connector.do_get, resp, EntryView)


class EntryView(JsonObjectView):
    """Access user log entry view."""

    @property
    def remote_addr(self) -> str:
        """User ip-address. Format ipv4."""
        return self._get("remoteAddr")

    @property
    def begin_at(self) -> datetime:
        """Start time of action."""
        return parse_rfc3339_timestamp(self._get("beginAt"))

    @property
    def end_at(self) -> Optional[datetime]:
        """End time of action. :data:`None` if it wasn't end yet"""
        return self._map_optional("endAt", parse_rfc3339_timestamp)

    @property
    def user_uuid(self) -> uuid.UUID:
        """User UUID."""
        return uuid.UUID(self._get("userUUID"))

    @property
    def object_type(self) -> ObjectType:
        """Object domain."""
        return ObjectType(self._get("objectType"))

    @property
    def object_domain(self) -> ObjectDomain:
        """Object domain."""
        return ObjectDomain(self._get("objectDomain"))

    @property
    def operation(self) -> Operation:
        """Operation."""
        return Operation(self._get("operation"))

    @property
    def object_uuid(self) -> Optional[uuid.UUID]:
        """Object UUID."""
        return self._map_optional("objectUUID", uuid.UUID)

    @property
    def result(self) -> Result:
        """Action result."""
        return Result(self._get("result"))

    @property
    def details(self) -> Optional[JsonObject]:
        """Action details."""
        return self._get_optional("details")
