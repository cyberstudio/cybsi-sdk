"""Use this section of API to register/retrieve
observation of types known to Cybsi.

Each type of observation is handled by their own sub-section of API.
"""
from .api import ObservationsAPI
from .generic import (
    GenericObservationsAPI,
    GenericObservationForm,
    GenericObservationView,
    GenericObservationContentView,
    RelationshipView,
    AttributeValueView,
)
