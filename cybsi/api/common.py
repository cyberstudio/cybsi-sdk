import uuid

from .internal import JsonObjectView


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
