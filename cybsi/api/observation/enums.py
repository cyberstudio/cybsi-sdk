from enum_tools import document_enum

from cybsi.api.enum import CybsiAPIEnum


@document_enum
class ObservationTypes(CybsiAPIEnum):
    """Observation types."""

    DNSLookup = "DNSLookup"  # doc: DNS lookup results.
    WhoisLookup = "WhoisLookup"  # doc: Whois lookup results.
    NetworkSession = "NetworkSession"  # doc: Network activity information.
    ScanSession = "ScanSession"  # doc: File sample scan information.
    Threat = "Threat"  # doc: Threat information.
    Generic = "Generic"  # doc: Fact set of attributes and relationships.


@document_enum
class ScanSessionFiltrationMode(CybsiAPIEnum):
    """Filter mode."""

    Actual = "Actual"  # doc: Last (actual) session for each of analysis engine
