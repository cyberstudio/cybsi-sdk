from cybsi.api.observable.relationships import RelationshipsAPI
from .entities_api import EntitiesAPI
from ..internal import BaseAPI


class ObservableAPI(BaseAPI):
    """Observable API."""

    @property
    def entities(self) -> EntitiesAPI:
        """Entities API."""
        return EntitiesAPI(self._connector)

    @property
    def relationships(self) -> RelationshipsAPI:
        """Relationships API."""
        return RelationshipsAPI(self._connector)
