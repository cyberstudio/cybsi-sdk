from enum_tools import document_enum

from cybsi.api.enum import CybsiAPIEnum


@document_enum
class ObservationTypes(CybsiAPIEnum):
    """Observation types."""

    DNSLookup = "DNSLookup"  # doc: DNS lookup results.
    WhoisLookup = "WhoisLookup"  # doc: Whois lookup results.
    NetworkSession = "NetworkSession"  # doc: Network activity information.
    Threat = "Threat"  # doc: Threat information.
    Generic = "Generic"  # doc: Fact set of attributes and relationships.
