from enum_tools import document_enum

from cybsi.api.enum import CybsiAPIEnum


@document_enum
class EnrichmentTypes(CybsiAPIEnum):
    """Enrichment type."""

    ArchiveUnpack = "ArchiveUnpack"  # doc: Archive unpack.
    ArtifactAnalysis = "ArtifactAnalysis"  # doc: Artifact analysis.
    ArtifactDownload = "ArtifactDownload"  # doc: Artifact download.
    DNSLookup = "DNSLookup"  # doc: DNS lookup.
    ExternalDBLookup = "ExternalDBLookup"  # doc: External database lookup.
    WhoisLookup = "WhoisLookup"  # doc: Whois lookup.


@document_enum
class EnrichmentTriggerTypes(CybsiAPIEnum):
    """Enrichment trigger type."""

    OnDemand = "OnDemand"
    """Enrichment starts on manual task creation through API."""
    OnRegistration = "OnRegistration"
    """Enrichment starts automatically on artifact registration or entity mention."""


@document_enum
class EnrichmentErrorCodes(CybsiAPIEnum):
    """Enrichment task error code."""

    FatalError = "FatalError"
    """Enricher internal error."""
    TemporaryError = "TemporaryError"
    """Task timed out, network connectivity issues and so on."""
    NotFound = "NotFound"
    """Requested entity wasn't found in external database."""
    UnsupportedArtifact = "UnsupportedArtifact"
    """
        :attr:`EnrichmentTypes.ArtifactAnalysis` only.
        Enricher doesn't support such artifacts
        (invalid archive format, artifact size is too big).
    """
    Unavailable = "Unavailable"
    """
        :attr:`EnrichmentTypes.ArtifactDownload`,
        :attr:`EnrichmentTypes.WhoisLookup` only.
        Resource under provided URL is not available.
    """
    CorruptedArchive = "CorruptedArchive"
    """Only in task API. Archive is corrupted."""
    InvalidPassword = "InvalidPassword"
    """
        :attr:`EnrichmentTypes.ArchiveUnpack` only in task API.
        An incorrect archive password is specified or a password
        is required to unpack (not specified).
    """


@document_enum
class EnrichmentTaskPriorities(CybsiAPIEnum):
    """Enrichment task priority."""

    High = "High"  # doc: High.
    Normal = "Normal"  # doc: Normal.


@document_enum
class EnrichmentTaskStatuses(CybsiAPIEnum):
    """Enrichment task status."""

    Pending = "Pending"
    """Task in the queue, awaiting execution (new or has been restarted)."""
    Executing = "Executing"
    """The task is in progress."""
    Failed = "Failed"
    """An error has occurred, after a while another attempt will be made."""
    Completed = "Completed"
    """Final state. Task completed successfully."""
    Aborted = "Aborted"
    """Final state. The task could not be completed due to an error."""
