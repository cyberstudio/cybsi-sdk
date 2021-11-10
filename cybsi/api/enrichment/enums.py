from enum import Enum

from enum_tools import document_enum


@document_enum
class EnrichmentTypes(Enum):
    """Enrichment type."""

    ArchiveUnpack = "ArchiveUnpack"  #: doc: Archive unpack.
    ArtifactAnalysis = "ArtifactAnalysis"  #: doc: Artifact analysis.
    ArtifactDownload = "ArtifactDownload"  #: doc: Artifact download.
    DNSLookup = "DNSLookup"  #: doc: DNS lookup.
    ExternalDBLookup = "ExternalDBLookup"  #: doc: External database lookup.
    WhoisLookup = "WhoisLookup"  #: doc: Whois lookup.


@document_enum
class EnrichmentErrorCodes(Enum):
    """Enrichment task error code."""

    FatalError = "FatalError"  #: doc: Enricher internal error.
    TemporaryError = "TemporaryError"  # noqa: E501 #doc: Task timed out, network connectivity issues and so on.
    NotFound = "NotFound"  # noqa: E501 #doc: Requested entity wasn't found in external database.
    UnsupportedArtifact = "UnsupportedArtifact"  # noqa: E501 #doc: :attr:`EnrichmentTypes.ArtifactAnalysis` only. Enricher doesn't support such artifacts (invalid archive format, artifact size is too big).
    Unavailable = "Unavailable"  # noqa: E501 #doc: :attr:`EnrichmentTypes.ArtifactDownload` only. Resource under provided URL is not available.


@document_enum
class EnrichmentTaskPriorities(Enum):
    """Enrichment task priority."""

    High = "High"  #: doc: High.
    Normal = "Normal"  #: doc: Normal.
