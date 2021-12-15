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
    """Observation short view, used in ReportView"""

    @property
    def type(self) -> ObservationTypes:
        """Observation type."""
        return self._get("type")
