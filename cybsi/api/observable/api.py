from ..internal import BaseAPI, BaseAsyncAPI
from .annotations import AnnotationsAPI
from .entities_api import EntitiesAPI, EntitiesAsyncAPI
from .relationships import RelationshipsAPI
from .view import EntityViewsAPI


class ObservableAPI(BaseAPI):
    """Observable API."""

    @property
    def entities(self) -> EntitiesAPI:
        """Entities API."""
        return EntitiesAPI(self._connector)

    @property
    def entity_views(self) -> EntityViewsAPI:
        """Entity views API."""
        return EntityViewsAPI(self._connector)

    @property
    def relationships(self) -> RelationshipsAPI:
        """Relationships API."""
        return RelationshipsAPI(self._connector)

    @property
    def annotations(self) -> AnnotationsAPI:
        """Annotations API."""
        return AnnotationsAPI(self._connector)


class ObservableAsyncAPI(BaseAsyncAPI):
    """Observable async API."""

    @property
    def entities(self) -> EntitiesAsyncAPI:
        """Entities API handle."""
        return EntitiesAsyncAPI(self._connector)
