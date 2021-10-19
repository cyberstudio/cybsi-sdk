from typing import Optional, Tuple

from cybsi_sdk import enums

from .. import base
from .. import pagination
from .. import observable

X_CHANGE_CURSOR = 'X-Change-Cursor'


class ChangeView(base.JsonObjectView):

    @property
    def operation(self) -> enums.ReplistOperations:
        """Get change operation
        """
        return enums.ReplistOperations(self._get('operation'))

    @property
    def entity(self) -> observable.EntityView:
        """Get entity
        """
        return self._get('entity')


class ReplistsAPI(base.API):
    _replist_base_url = '/replists'
    _replist_entities_tpl = _replist_base_url + '/{}/entities'
    _replist_changes_tpl = _replist_base_url + '/{}/changes'

    def entities(
            self,
            replist_uuid: str,
            cursor: Optional[str] = None,
            limit: Optional[int] = None,
    ) -> Tuple[pagination.Page[observable.EntityView], str]:
        """Get replists entities

        :param replist_uuid: replist uuid
        :param cursor: page cursor
        :param limit: page limit
        :return: page and replist's event cursor
            for getting replist's changes.
        """

        params = {}
        if cursor:
            params['cursor'] = cursor
        if limit:
            params['limit'] = str(limit)

        path = self._replist_entities_tpl.format(replist_uuid)
        resp = self._connector.do_get(path, params=params)
        page = pagination.Page(
            self._connector.do_get,
            resp,
            observable.EntityView
        )
        return page, resp.headers.get(X_CHANGE_CURSOR, '')

    def changes(
            self,
            replist_uuid: str,
            cursor: str,
            limit: Optional[int] = None,
    ) -> pagination.Page[ChangeView]:
        """Get replist changes

        :param replist_uuid: replist uuid
        :param cursor: page cursor
        :param limit: page limit
        """

        params = {'cursor': cursor}
        if limit:
            params['limit'] = str(limit)

        path = self._replist_entities_tpl.format(replist_uuid)
        resp = self._connector.do_get(path, params=params)
        page = pagination.Page(self._connector.do_get, resp, ChangeView)
        return page
