from .. import RefView
from ..internal import BaseAPI
from .enums import ObservationTypes
from .generic import GenericObservationsAPI


class ObservationsAPI(BaseAPI):
    """Observations API."""

    @property
    def generics(self) -> "GenericObservationsAPI":
        """Get generic observation route."""
        return GenericObservationsAPI(self._connector)


class ObservationCommonView(RefView):
    """Observation short view."""

    @property
    def type(self) -> "ObservationTypes":
        """Observation type."""
        return ObservationTypes(self._get("type"))
