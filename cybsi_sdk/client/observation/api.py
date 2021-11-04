from ..internal import BaseAPI
from .generic import GenericObservationsAPI


class ObservationsAPI(BaseAPI):
    """
    Hint:
        Use :attr:`cybsi_sdk.client.CybsiClient.observations`
        and properties of :class:`ObservationsAPI` to select
        observation type you want to work with.

        Don't construct sub-APIs manually.
    """
    @property
    def generics(self) -> 'GenericObservationsAPI':
        """Get generic observation route."""
        return GenericObservationsAPI(self._connector)
