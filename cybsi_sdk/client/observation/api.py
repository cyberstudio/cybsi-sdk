from ..internal import BaseAPI
from .generic import GenericObservationsAPI


class ObservationsAPI(BaseAPI):
    """Observations API."""
    @property
    def generics(self) -> 'GenericObservationsAPI':
        """Get generic observation route."""
        return GenericObservationsAPI(self._connector)
