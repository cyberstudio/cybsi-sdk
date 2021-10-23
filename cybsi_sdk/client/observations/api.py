from cybsi_sdk.client import base
from cybsi_sdk.client.observations import generic


class GenericObservationAPI(base.API):
    """Generic observations API"""
    _path = "/enrichment/observations/generics"

    def register(self, model: generic.GenericObservationForm) -> base.RefView:
        """Register a generic observation
        """
        r = self._connector.do_post(path=self._path, json=model.json())
        return base.RefView(r.json())

    def view(self, observation_uuid) -> generic.GenericObservationView:
        """Get a generic observation view
        """
        path = f'{self._path}/{observation_uuid}'
        r = self._connector.do_get(path)
        return generic.GenericObservationView(r.json())


class ObservationsAPI(base.API):
    """Observations API.
    Allows to register/retrieve observations of different types.

    Each type of observations is handled by their own sub-section of API.
    """
    @property
    def generics(self) -> GenericObservationAPI:
        """Generic observations route
        """
        return GenericObservationAPI(self._connector)
