import uuid

from .internal import JsonObjectView

Tag = str

E_TAG = "ETag"
IF_MATCH = "If-Match"


class RefView(JsonObjectView):
    """Reference to an object.

    Many API methods operate such references.
    Most commonly, methods return a reference on object registration.
    """

    @property
    def uuid(self) -> uuid.UUID:
        """Object UUID."""
        return uuid.UUID(self._get("uuid"))

    @property
    def url(self) -> str:
        """URL of the object in API.
        Can be used to retrieve complete view of the object.
        """
        return self._get("url")


class TaggedRefView(RefView):
    """Reference to an object with internal tag.
    Tag is extracted from response header E_TAG
    and used to protect against concurrent object changes."""

    def __init__(self, resp):
        super().__init__(resp.json())
        self._tag = resp.headers.get(E_TAG, "")

    @property
    def tag(self) -> Tag:
        """Object tag."""
        return self._tag
