from datetime import datetime
from typing import Optional, Tuple

import uuid

from .enums import EntitySetOperations, ReplistStatus
from ..common import RefView, TaggedRefView, IF_MATCH, Tag
from ..internal import (
    BaseAPI,
    JsonObjectForm,
    JsonObjectView,
    parse_rfc3339_timestamp,
)
from ..observable import EntityView, ShareLevels
from ..pagination import Page
from ..search import StoredQueryCommonView

X_CHANGE_CURSOR = "X-Change-Cursor"


class ReplistsAPI(BaseAPI):
    """Reputation list API."""

    _replist_base_url = "/replists"
    _replist_entities_tpl = _replist_base_url + "/{}/entities"
    _replist_changes_tpl = _replist_base_url + "/{}/changes"

    def register(self, replist: "ReplistForm") -> RefView:
        """Register reputation list.

        Note:
            Calls `POST /replists`.
        Args:
            replist: Filled replist form.
        Returns:
            Reference to the registered replist.
        Raises:
            :class:`~cybsi.api.error.SemanticError`: Form contains logic errors.
        Note:
            Semantic error codes specific for this method:
              * :attr:`~cybsi.api.error.SemanticErrorCodes.StoredQueryNotFound`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.InvalidShareLevel`
        """
        resp = self._connector.do_post(path=self._replist_base_url, json=replist.json())
        return RefView(resp.json())

    def view(self, replist_uuid: uuid.UUID) -> "ReplistView":
        """Get reputation list full view.

        Note:
            Calls `GET /replists/{replist_uuid}`.
        Args:
            replist_uuid: Replist uuid.
        Returns:
            Full view of the replist with ETag string value.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: Replist not found.
        """
        path = f"{self._replist_base_url}/{replist_uuid}"
        resp = self._connector.do_get(path)
        return ReplistView(resp)

    def edit(
        self,
        replist_uuid: uuid.UUID,
        tag: Tag,
        is_enabled: Optional[bool] = None,
        query_uuid: Optional[uuid.UUID] = None,
        share_level: Optional[ShareLevels] = None,
    ) -> None:
        """Edit current reputation list.

        Note:
            Calls `PATCH /replists/{replist_uuid}`.
        Args:
            replist_uuid: Replist uuid.
            etag: ETag header value obataned from replist view method.
            query_uuid: Search query UUID attached to replist.
            share_level: Replist share level.
            is_enabled: Replist initial status.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: Replist not found.
            :class:`~cybsi.api.error.ResourceModifiedError`:
                Replist changed since last request. Update ETag and retry.
            :class:`~cybsi.api.error.SemanticError`: Form contains logic errors.
        Note:
            Semantic error codes specific for this method:
              * :attr:`~cybsi.api.error.SemanticErrorCodes.StoredQueryNotFound`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.InvalidShareLevel`
        """
        form = {}
        if query_uuid is not None:
            form["queryUUID"] = str(query_uuid)
        if share_level is not None:
            form["shareLevel"] = share_level.value
        if is_enabled is not None:
            form["isEnabled"] = is_enabled  # type: ignore
        path = f"{self._replist_base_url}/{replist_uuid}"
        self._connector.do_patch(
            path=path,
            json=form,
            headers={IF_MATCH: tag},
        )

    def filter(
        self,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> Page["ReplistCommonView"]:
        """Get replist filtration list.

        Note:
            Calls `GET /replists`
        Args:
            cursor: Page cursor.
            limit: Page limit.
        Return:
            Page with entities and cursor allowing to get next batch of changes.
        """
        params = {}
        if cursor:
            params["cursor"] = cursor
        if limit:
            params["limit"] = str(limit)

        resp = self._connector.do_get(self._replist_base_url, params=params)
        page = Page(self._connector.do_get, resp, ReplistCommonView)
        return page

    def entities(
        self,
        replist_uuid: str,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> Tuple[Page[EntityView], str]:
        """Get replist entities.

        Note:
            Calls `GET /replist/{replist_uuid}/entities`
        Args:
            replist_uuid: Replist uuid.
            cursor: Page cursor.
            limit: Page limit.
        Return:
            Page with entities and cursor allowing to get next batch of changes.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: Replist not found.
        """

        params = {}
        if cursor:
            params["cursor"] = cursor
        if limit:
            params["limit"] = str(limit)

        path = self._replist_entities_tpl.format(replist_uuid)
        resp = self._connector.do_get(path, params=params)
        page = Page(self._connector.do_get, resp, EntityView)
        return page, resp.headers.get(X_CHANGE_CURSOR, "")

    def changes(
        self,
        replist_uuid: str,
        cursor: str,
        limit: Optional[int] = None,
    ) -> Page["EntitySetChangeView"]:
        """Get replist changes

        Note:
            Calls `GET /replist/{replist_uuid}/changes`
        Args:
            replist_uuid: Replist uuid.
            cursor: Page cursor.
            limit: Page limit.
        Return:
            Page with changes.
        Warning:
            Cursor behaviour differs from other API methods.

            Do not save returned cursor if it's empty.
            Empty cursor value means that all changes **for this moment** are received.
            But more changes can arrive later. Pass your previous non-empty ``cursor``
            value in loop, until non-empty cursor is returned.

            Please wait some time if method returns an empty cursor.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: Replist not found.
            :class:`~cybsi.api.error.SemanticError`: Semantic request error.
        Note:
            Semantic error codes specific for this method:
              * :attr:`~cybsi.api.error.SemanticErrorCodes.CursorOutOfRange`
        """

        params = {"cursor": cursor}
        if limit:
            params["limit"] = str(limit)

        path = self._replist_entities_tpl.format(replist_uuid)
        resp = self._connector.do_get(path, params=params)
        page = Page(self._connector.do_get, resp, EntitySetChangeView)
        return page


class ReplistForm(JsonObjectForm):
    """Reputation list form.

    Args:
        query_uuid: Search query UUID attached to replist.
        share_level: Replist share level.
        is_enabled: Replist initial status.
    """

    def __init__(
        self,
        query_uuid: uuid.UUID,
        share_level: ShareLevels,
        is_enabled: Optional[bool] = None,
    ):
        super().__init__()
        self._data["queryUUID"] = str(query_uuid)
        self._data["shareLevel"] = share_level.value
        if is_enabled is not None:
            self._data["isEnabled"] = is_enabled


class ReplistCommonView(RefView):
    """Reputation list short view."""

    @property
    def query(self) -> "StoredQueryCommonView":
        """Search query attached to replist (without raw query text)."""
        return StoredQueryCommonView(self._get("query"))

    @property
    def author(self) -> "RefView":
        """Replist author."""
        return RefView(self._get("author"))

    @property
    def share_level(self) -> ShareLevels:
        """Replist share level."""
        return ShareLevels(self._get("shareLevel"))

    @property
    def is_enabled(self) -> bool:
        """Replist enabled status."""
        return self._get("isEnabled")


class ReplistView(TaggedRefView, ReplistCommonView):
    """Reputation list full view."""

    @property
    def updated_at(self) -> datetime:
        """Replist last updated time."""
        return parse_rfc3339_timestamp(self._get("createdAt"))

    @property
    def status(self) -> ReplistStatus:
        """Replist current status."""
        return ReplistStatus(self._get("status"))


class EntitySetChangeView(JsonObjectView):
    """Replist change."""

    @property
    def operation(self) -> EntitySetOperations:
        """Get change operation."""
        return EntitySetOperations(self._get("operation"))

    @property
    def entity(self) -> EntityView:
        """Get entity."""
        return self._get("entity")
