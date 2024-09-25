import uuid
from typing import Dict, Any

from cybsi.api import RefView, Tag
from cybsi.api.custom_lists import CustomListView, CustomListCommonView
from cybsi.api.internal import BaseAPI, JsonObjectForm
from cybsi.api.pagination import Cursor, Page
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
            cursor: Cursor = None,
            limit: int = None,
    ) -> Page["ThreatLandscapeCommonView"]:
        """
        Get a list of all threat landscapes.

        .. versionadded:: 2.14.0
        Note:
            Calls `GET /threat-landscapes`
        Args:
            cursor: Page cursor
            limit: Page limit
        """
        params: Dict[str, Any] = {}
        if cursor:
            params["cursor"] = cursor
        if limit:
            params["limit"] = limit
        resp = self._connector.do_get(path=_PATH, params=params)
        page = Page(self._connector.do_get, resp, ThreatLandscapeCommonView)
        return page

    def register(self, threat_landscape: "ThreatLanscapeForm") -> RefView:
        """
        Register a new threat landscape.

        .. versionadded:: 2.14.0
        Note:
            Calls `POST /threat-landscapes`
        Args:
            threat_landscape: Threat landscape form
        """
        resp = self._connector.do_post(path=_PATH, json=threat_landscape.json())
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
            :class:`~cybsi.api.error.NotFoundError`: Threat Landscape not found.
        """

        path = f"/threat-landscapes/{landscape_uuid}"
        resp = self._connector.do_get(path=path)
        return ThreatLandscapeView(resp.json())

    def edit(
            self,
            landscape_uuid: uuid.UUID,
            tag: Tag,
            name: str
    ) -> None:
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
            :class:`~cybsi.api.error.NotFoundError`: Threat landscape not found.
        """
        path = f"{_PATH}/{landscape_uuid}"
        self._connector.do_delete(path=path)

    def filter_custom_lists(self, landscape_uuid: uuid.UUID) -> Page[CustomListCommonView]:

class ThreatLanscapeForm(JsonObjectForm):
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