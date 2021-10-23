"""Use this section of API to register and retrieve observations.

Use ObservationsAPI as entry point,
it allows to select observation type you want to work with.
"""
from .generic import GenericObservationForm, GenericObservationView
from .api import GenericObservationAPI, ObservationsAPI

__all__ = [
    'GenericObservationAPI',
    'GenericObservationForm',
    'GenericObservationView',
    'ObservationsAPI',
]
