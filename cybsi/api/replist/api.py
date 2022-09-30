import uuid
from datetime import datetime
from typing import Generic, List, Optional, Tuple, Type, cast

from .. import RefView
from ..api import Tag
from ..internal import (
    BaseAPI,
    JsonObject,
    JsonObjectForm,
    JsonObjectView,
    parse_rfc3339_timestamp,
)
from ..observable import EntityTypes, EntityView, EntityViewT, ShareLevels
from ..pagination import Cursor, Page
from ..search import StoredQueryCommonView
from ..view import _TaggedRefView
from .enums import EntitySetOperations, ReplistStatus

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
        *,
        is_enabled: Optional[bool] = None,
        query_uuid: Optional[uuid.UUID] = None,
        share_level: Optional[ShareLevels] = None,
    ) -> None:
        """Edit the reputation list.

        Note:
            Calls `PATCH /replists/{replist_uuid}`.
        Args:
            replist_uuid: Replist uuid.
            tag: :attr:`ReplistView.tag` value. Use :meth:`view` to retrieve it.
            query_uuid: Search query UUID attached to replist.
            share_level: Replist share level.
            is_enabled: Replist status toggle.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: Replist not found.
            :class:`~cybsi.api.error.ResourceModifiedError`:
                Replist changed since last request. Update tag and retry.
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
        self._connector.do_patch(path=path, tag=tag, json=form)

    def filter(
        self,
        *,
        cursor: Optional[Cursor] = None,
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
            params["cursor"] = str(cursor)
        if limit:
            params["limit"] = str(limit)

        resp = self._connector.do_get(self._replist_base_url, params=params)
        page = Page(self._connector.do_get, resp, ReplistCommonView)
        return page

    def entities(
        self,
        replist_uuid: uuid.UUID,
        *,
        # see https://github.com/python/mypy/issues/3737
        entity_view: Type[EntityViewT] = EntityView,  # type: ignore
        cursor: Optional[Cursor] = None,
        limit: Optional[int] = None,
    ) -> Tuple[Page[EntityViewT], Cursor]:
        """Get replist entities.

        Note:
            Calls `GET /replist/{replist_uuid}/entities`
        Args:
            replist_uuid: Replist uuid.
            entity_view: Entity view to use.
                See :class:`~cybsi.api.observable.EntityViewsAPI` for details.
            cursor: Page cursor.
            limit: Page limit.
        Return:
            Page with entity views and cursor.
            The cursor can be used to call :meth:`changes`.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: Replist not found.
        """

        params = {}
        if entity_view is not EntityView:
            params["viewUUID"] = str(entity_view._view_uuid())
        if cursor:
            params["cursor"] = str(cursor)
        if limit:
            params["limit"] = str(limit)

        path = self._replist_entities_tpl.format(replist_uuid)
        resp = self._connector.do_get(path, params=params)

        page = Page(self._connector.do_get, resp, entity_view)
        return page, cast(Cursor, resp.headers.get(X_CHANGE_CURSOR, ""))

    def changes(
        self,
        replist_uuid: uuid.UUID,
        *,
        cursor: Cursor,
        # see https://github.com/python/mypy/issues/3737
        entity_view: Type[EntityViewT] = EntityView,  # type: ignore
        limit: Optional[int] = None,
    ) -> Page["EntitySetChangeView[EntityViewT]"]:
        """Get replist changes

        Note:
            Calls `GET /replist/{replist_uuid}/changes`
        Args:
            replist_uuid: Replist uuid.
            entity_view: Entity view to use.
                See :class:`~cybsi.api.observable.EntityViewsAPI` for details.
            cursor: Page cursor.
                On the first request you should pass the cursor value
                obtained when requesting replist entities :meth:`entities`.
                Subsequent calls should use cursor property of the page
                returned by :meth:`changes`.
            limit: Page limit.
        Return:
            Page with changes.
        Warning:
            Cursor behaviour differs from other API methods.

            Do not save returned page cursor if it is :data:`None`.
            :data:`None` means that all changes **for this moment** are received.
            More changes can arrive later. Pass your previous non-none ``cursor``
            value in loop, until non-none cursor is returned.

            Please wait some time if method returns a page with :data:`None` cursor.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: Replist not found.
            :class:`~cybsi.api.error.SemanticError`: Semantic request error.
        Note:
            Semantic error codes specific for this method:
              * :attr:`~cybsi.api.error.SemanticErrorCodes.CursorOutOfRange`
        """

        params = {"cursor": str(cursor)}
        if entity_view is not EntityView:
            params["viewUUID"] = str(entity_view._view_uuid())
        if limit:
            params["limit"] = str(limit)

        path = self._replist_changes_tpl.format(replist_uuid)
        resp = self._connector.do_get(path, params=params)

        def entity_view_converter(entity_data):
            return EntitySetChangeView(entity_view, entity_data)

        page = Page(self._connector.do_get, resp, entity_view_converter)
        return page

    def statistic(self, replist_uuid: uuid.UUID) -> "ReplistStatisticView":
        """Get replist statistic.

        Note:
            Calls `GET /replists/{replist_uuid}/statistic`.
        Args:
            replist_uuid: Replist uuid.
        Returns:
            Replist statistic view.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: Replist not found.
        """

        path = f"{self._replist_base_url}/{replist_uuid}/statistic"
        resp = self._connector.do_get(path)
        return ReplistStatisticView(resp.json())


class ReplistForm(JsonObjectForm):
    """Reputation list form.

    Args:
        query_uuid: Search query UUID attached to replist.
        share_level: Replist share level.
        is_enabled: Replist status toggle.
    """

    def __init__(
        self,
        query_uuid: uuid.UUID,
        share_level: ShareLevels,
        *,
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


class ReplistView(_TaggedRefView, ReplistCommonView):
    """Reputation list full view."""

    @property
    def updated_at(self) -> datetime:
        """Replist last updated time."""
        return parse_rfc3339_timestamp(self._get("createdAt"))

    @property
    def status(self) -> ReplistStatus:
        """Replist current status."""
        return ReplistStatus(self._get("status"))


class EntitySetChangeView(JsonObjectView, Generic[EntityViewT]):
    """Replist change."""

    def __init__(
        self, entity_view: Type[EntityViewT], data: Optional[JsonObject] = None
    ):
        super(EntitySetChangeView, self).__init__(data)
        self._entity_view = entity_view

    @property
    def operation(self) -> EntitySetOperations:
        """Get change operation."""
        return EntitySetOperations(self._get("operation"))

    @property
    def entity(self) -> EntityViewT:
        """Get entity view."""
        en = self._get("entity")
        return self._entity_view(en)


class ReplistStatisticView(JsonObjectView):
    """Replist statistic view."""

    @property
    def entity_count(self) -> int:
        """Total number of entities in the replist."""
        return self._get("entityCount")

    @property
    def entity_type_distribution(self) -> List["EntityTypeDistributionView"]:
        """Distribution of entities number by their types."""
        return [
            EntityTypeDistributionView(x) for x in self._get("entityTypeDistribution")
        ]


class EntityTypeDistributionView(JsonObjectView):
    """Entity type distribution."""

    @property
    def entity_type(self) -> EntityTypes:
        """Entity type."""
        return EntityTypes(self._get("entityType"))

    @property
    def count(self) -> int:
        """Number of entities."""
        return self._get("count")
