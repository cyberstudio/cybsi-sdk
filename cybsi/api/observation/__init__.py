"""Use this section of API to register/retrieve
observation of types known to Cybsi.

Each type of observation is handled by their own subsection of API.
"""
from .api import ObservationsAPI
from .enums import ObservationTypes
from .generic import (
    GenericObservationsAPI,
    GenericObservationForm,
    GenericObservationView,
    GenericObservationContentView,
    RelationshipView,
    AttributeValueView,
)
from .view import ObservationHeaderView, ObservationCommonView
from .archive import (
    ArchiveObservationsAPI,
    ArchiveObservationView,
    ArchiveObservationContentView,
)
from .dns_lookup import (
    DNSLookupObservationsAPI,
    DNSLookupObservationView,
    DNSLookupObservationContentView,
)
from .network_session import (
    NetworkSessionObservationsAPI,
    NetworkSessionObservationView,
    NetworkSessionObservationContentView,
)
from .scan_session import (
    ScanSessionObservationsAPI,
    ScanSessionObservationView,
    ScanSessionObservationContentView,
    ScanSessionFiltrationMode,
)
from .threat import (
    ThreatObservationsAPI,
    ThreatObservationView,
    ThreatObservationContentView,
)
from .whois_lookup import (
    WhoisLookupObservationsAPI,
    WhoisLookupObservationView,
    WhoisLookupObservationContentView,
)

ObservationHeaderView.__module__ = "cybsi.api.observation"
ObservationCommonView.__module__ = "cybsi.api.observation"
