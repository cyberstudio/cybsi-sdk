from enum_tools import document_enum

from cybsi.api.enum import CybsiAPIEnum


@document_enum
class EnrichmentTypes(CybsiAPIEnum):
    """Enrichment type."""

    ArchiveUnpack = "ArchiveUnpack"  #: doc: Archive unpack.
    ArtifactAnalysis = "ArtifactAnalysis"  #: doc: Artifact analysis.
    ArtifactDownload = "ArtifactDownload"  #: doc: Artifact download.
    DNSLookup = "DNSLookup"  #: doc: DNS lookup.
    ExternalDBLookup = "ExternalDBLookup"  #: doc: External database lookup.
    WhoisLookup = "WhoisLookup"  #: doc: Whois lookup.


@document_enum
class EnrichmentTriggerTypes(CybsiAPIEnum):
    """Enrichment trigger type."""

    OnDemand = "OnDemand"  # noqa: E501 doc: Enrichment starts on manual task creation through API.
    OnRegistration = "OnRegistration"  # noqa: E501 doc: Enrichment starts automatically on artifact registration or entity mention.


@document_enum
class EnrichmentErrorCodes(CybsiAPIEnum):
    """Enrichment task error code."""

    # fmt: off
    FatalError = "FatalError"  #: doc: Enricher internal error.
    TemporaryError = "TemporaryError"  # noqa: E501 #doc: Task timed out, network connectivity issues and so on.
    NotFound = "NotFound"  # noqa: E501 #doc: Requested entity wasn't found in external database.
    UnsupportedArtifact = "UnsupportedArtifact"  # noqa: E501 #doc: :attr:`EnrichmentTypes.ArtifactAnalysis` only. Enricher doesn't support such artifacts (invalid archive format, artifact size is too big).
    Unavailable = "Unavailable"  # noqa: E501 #doc: :attr:`EnrichmentTypes.ArtifactDownload`, :attr:`EnrichmentTypes.WhoisLookup` only. Resource under provided URL is not available.
    CorruptedArchive = "CorruptedArchive"   # noqa: E501 #doc: Only in task API. Archive is corrupted.
    InvalidPassword = "InvalidPassword"  # noqa: E501 #doc: :attr:`EnrichmentTypes.ArchiveUnpack` only in task API. An incorrect archive password is specified or a password is required to unpack (not specified).
    # fmt: on


@document_enum
class EnrichmentTaskPriorities(CybsiAPIEnum):
    """Enrichment task priority."""

    High = "High"  #: doc: High.
    Normal = "Normal"  #: doc: Normal.


@document_enum
class EnrichmentTaskStatuses(CybsiAPIEnum):
    """Enrichment task status."""

    Pending = "Pending"  # noqa: E501 doc: Task in the queue, awaiting execution (new or has been restarted).
    Executing = "Executing"  # noqa: E501 doc: The task is in progress.
    Failed = "Failed"  # noqa: E501 doc: An error has occurred, after a while another attempt will be made.
    Completed = "Completed"  # noqa: E501 doc: Final state. Task completed successfully.
    Aborted = "Aborted"  # noqa: E501 doc: Final state. The task could not be completed due to an error.
