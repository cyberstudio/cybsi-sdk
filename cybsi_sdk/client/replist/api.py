from typing import Optional, Tuple

from cybsi_sdk.model.replist import EntitySetOperations

from ..internal import BaseAPI, JsonObjectView
from ..pagination import Page
from ..observable.entity import EntityView

X_CHANGE_CURSOR = 'X-Change-Cursor'


class ReplistsAPI(BaseAPI):
    """Reputation list API."""
    _replist_base_url = '/replist'
    _replist_entities_tpl = _replist_base_url + '/{}/entities'
    _replist_changes_tpl = _replist_base_url + '/{}/changes'

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
            Page with entities and cursor
            allowing to get next batch of changes.
        """

        params = {}
        if cursor:
            params['cursor'] = cursor
        if limit:
            params['limit'] = str(limit)

        path = self._replist_entities_tpl.format(replist_uuid)
        resp = self._connector.do_get(path, params=params)
        page = Page(
            self._connector.do_get,
            resp,
            EntityView
        )
        return page, resp.headers.get(X_CHANGE_CURSOR, '')

    def changes(
            self,
            replist_uuid: str,
            cursor: str,
            limit: Optional[int] = None,
    ) -> Page['EntitySetChangeView']:
        """Get replist changes

        Note:
            Calls `GET /replist/{replist_uuid}/changes`
        Args:
            replist_uuid: Replist uuid.
            cursor: Page cursor.
            limit: Page limit.
        Return:
            Page with changes.
        """

        params = {'cursor': cursor}
        if limit:
            params['limit'] = str(limit)

        path = self._replist_entities_tpl.format(replist_uuid)
        resp = self._connector.do_get(path, params=params)
        page = Page(self._connector.do_get, resp, EntitySetChangeView)
        return page


class EntitySetChangeView(JsonObjectView):
    """Replist change."""
    @property
    def operation(self) -> EntitySetOperations:
        """Get change operation.
        """
        return EntitySetOperations(self._get('operation'))

    @property
    def entity(self) -> EntityView:
        """Get entity.
        """
        return self._get('entity')
