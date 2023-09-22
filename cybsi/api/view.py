import uuid
from typing import Optional, cast

import httpx

from .api import Tag
from .internal import JsonObjectView


class RefView(JsonObjectView):
    """Reference to a resource.

    Many API methods operate such references.
    Most commonly, methods return a reference on a resource registration.
    """

    @property
    def uuid(self) -> uuid.UUID:
        """Resource UUID."""
        return uuid.UUID(self._get("uuid"))

    @property
    def url(self) -> Optional[str]:
        """URL of the resource in API.
        Can be used to retrieve complete view of the resource.
        Property is presented if :class:`~cybsi.api.client.Config`
        embed_object_url is True.
        """
        return self._get_optional("url")


class _TaggedRefView(RefView):
    _etag_header = "ETag"

    def __init__(self, resp: httpx.Response):
        super().__init__(resp.json())
        self._tag = cast(Tag, resp.headers.get(self._etag_header, ""))

    @property
    def tag(self) -> Tag:
        """Resource tag.

        Protects against concurrent object changes.
        Alternatively, can be used for caching.
        """
        return self._tag
