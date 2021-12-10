from .entities_api import EntitiesAPI
from ..internal import BaseAPI


class ObservableAPI(BaseAPI):
    @property
    def entities(self) -> EntitiesAPI:
        """Entities API."""
        return EntitiesAPI(self._connector)
