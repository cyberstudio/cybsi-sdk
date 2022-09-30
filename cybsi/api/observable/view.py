import abc
import uuid
from typing import Any, Dict, Optional, TypeVar

from ..internal import BaseAPI, JsonObjectView
from ..pagination import Cursor, Page


class EntityViewsAPI(BaseAPI):
    """Entity views API.

    Entity views allow to redefine API response format.
    In other words, some API methods returning basic entity view
    (:class:`~cybsi.api.observable.EntityView`) can return a completely
    different structure.

    The basic entity view contains entity keys and type,
    but custom views can contain much more information about entity.
    The example of a method utilizing custom views is
    :meth:`~cybsi.api.replist.ReplistsAPI.entities`.

    Extend :class:`AbstractEntityView` to implement a custom entity view.
    """

    _path = "/observable/entity-views"

    def filter(
        self,
        *,
        cursor: Optional[Cursor] = None,
        limit: Optional[int] = None,
    ) -> Page["EntityViewView"]:
        """Filter views of observable entities.

        Note:
            Calls `GET /observable/entity-views`.
        Args:
            cursor: Page cursor.
            limit: Page limit.
        Returns: List of views.
        """

        params: Dict[str, Any] = {}
        if cursor is not None:
            params["cursor"] = str(cursor)
        if limit is not None:
            params["limit"] = str(limit)

        resp = self._connector.do_get(path=self._path, params=params)
        page = Page(self._connector.do_get, resp, EntityViewView)
        return page


class EntityViewView(JsonObjectView):
    """
    View of the entity view.
    """

    @property
    def uuid(self) -> uuid.UUID:
        """Entity view UUID."""
        return uuid.UUID(self._get("uuid"))

    @property
    def name(self) -> str:
        """Entity view name."""
        return str(self._get("name"))


class AbstractEntityView(JsonObjectView, metaclass=abc.ABCMeta):
    """
    This is the class you need to extend to implement a custom entity view.

    .. automethod:: _view_uuid
    """

    @classmethod
    @abc.abstractmethod
    def _view_uuid(cls) -> uuid.UUID:
        """
        UUID of the view in API. Usually well-known.
        """
        pass


EntityViewT = TypeVar("EntityViewT", bound=AbstractEntityView)
"""
Any class implementing entity view.
"""
