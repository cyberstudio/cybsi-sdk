from ..internal import BaseAPI
from .annotations import AnnotationsAPI
from .entities_api import EntitiesAPI
from .relationships import RelationshipsAPI


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

    @property
    def annotations(self) -> AnnotationsAPI:
        """Annotations API."""
        return AnnotationsAPI(self._connector)
