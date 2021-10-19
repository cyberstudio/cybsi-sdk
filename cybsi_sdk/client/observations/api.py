from cybsi_sdk.client import base
from cybsi_sdk.client.observations import generic


class GenericObservationAPI(base.API):
    _path = "/enrichment/observations/generics"

    def register(self, model: generic.GenericObservationForm) -> base.RefView:
        """Register generic observations
        """
        r = self._connector.do_post(path=self._path, json=model.json())
        return base.RefView(r.json())

    def view(self, observation_uuid) -> generic.GenericObservationView:
        """Get generic observations view
        """
        path = f'{self._path}/{observation_uuid}'
        r = self._connector.do_get(path)
        return generic.GenericObservationView(r.json())


class ObservationsAPI(base.API):

    @property
    def generics(self) -> GenericObservationAPI:
        """Generic observations route
        """
        return GenericObservationAPI(self._connector)
