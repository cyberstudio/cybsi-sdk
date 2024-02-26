from enum_tools import document_enum

from cybsi.api.enum import CybsiAPIEnum


@document_enum
class RoleName(CybsiAPIEnum):
    """Role name.

    Role means a list of permissions.
    Each permission is Resource:Action pair.
    See :class:`ResourceName`.
    """

    Administrator = "Administrator"
    """
        Administrator's role permissions:
        [DataSources:rw,EnrichmentConfig:r,Users:r]
    """
    ConfigReader = "ConfigReader"
    """
        ConfigReader's role permissions:
        [DataSources:r, EnrichmentConfig:r]
    """
    FeedAdministrator = "FeedAdministrator"
    """
        FeedAdministrator's role permissions:
        [DataSources:r, Observable:r, ReputationLists:rw,
        ReputationListsContent:r, Search:r, StoredQuery:rw,
        Users:r]
    """
    FeedDataReader = "FeedDataReader"
    """
        FeedDataReader's role permissions:
        [DataSources:r, ReputationLists:r, ReputationListsContent:r,
        StoredQuery:r, Users:r]
    """
    EnrichmentRunner = "EnrichmentRunner"
    """
        EnrichmentRunner's role permissions:
        [DataSources:r, EnrichmentTasks:rw]
    """
    EnrichmentTaskReader = "EnrichmentTaskReader"
    """
        EnrichmentTaskReader's role permissions:
        [DataSources:r, EnrichmentTasks:r]
    """
    ReportRegistrant = "ReportRegistrant"
    """
        ReportRegistrant's role permissions:
        [Observations:w, Reports:w]
    """
    ReportReader = "ReportReader"
    """
        ReportReader's role permissions:
        [DataSources:r, Observations:r, RawReports:r, Reports:r]
    """
    EntityRegistrant = "EntityRegistrant"
    """
        EntityRegistrant's role permissions:
        [Observable:w]
    """
    EntityReader = "EntityReader"
    """
        EntityReader's role permissions:
        [DataSources:r, Observable:r]
    """
    ArtifactReader = "ArtifactReader"
    """
        ArtifactReader's role permissions:
        [Artifacts:r, DataSources:r]
    """
    ArtifactRegistrant = "ArtifactRegistrant"
    """
        ArtifactRegistrant's role permissions:
        [Artifacts:w]
    """
    ArtifactContentReader = "ArtifactContentReader"
    """
        ArtifactContentReader's role permissions:
        [Artifacts:r, ArtifactsContent:r]
    """
    Searcher = "Searcher"
    """
        Searcher's role permissions:
        [DataSources:r, Observable:r, Search:r]
    """
    UserAdministrator = "UserAdministrator"
    """
        UserAdministrator's role permissions:
        [APIKeys:rw, Users:rw]
    """
    DictionaryReader = "DictionaryReader"
    """
        .. versionadded:: 2.11.2

        DictionaryReader's role permissions:
        [Dictionaries:r]
    """
    DictionaryRegistrant = "DictionaryRegistrant"
    """
        .. versionadded:: 2.11.2

        DictionaryRegistrant's role permissions:
        [Dictionaries:w]
    """


@document_enum
class ResourceName(CybsiAPIEnum):
    """Resource name.

    Permission can be with read/write action for almost all resources.
    Exclusion resources:
    ArtifactsContent, RawReports, Search, ReputationListsContent.
    """

    Artifacts = "Artifacts"
    """Samples."""
    ArtifactsContent = "ArtifactsContent"
    """Sample contents. Permission can be only with reading action."""
    DataSources = "DataSources"
    """Data sources."""
    Dictionaries = "Dictionaries"
    """
        .. versionadded:: 2.11.2

        Dictionaries
    """
    EnrichmentConfig = "EnrichmentConfig"
    """Enrichment configs."""
    EnrichmentTasks = "EnrichmentTasks"
    """Enrichment tasks."""
    Feeds = "Feeds"
    """Feeds."""
    FeedsData = "FeedsData"
    """Feed contents. Permission can be only with reading action."""
    Observable = "Observable"
    """Observable entities."""
    Observations = "Observations"
    """Observations."""
    RawReports = "RawReports"
    """
    Initial data of reports and observations.
    Permission can be only with reading action.
    """
    Reports = "Reports"
    """Reports."""
    Search = "Search"
    """Search. Permission can be only with reading action."""
    SearchFilters = "SearchFilters"
    """Search filters."""
    Users = "Users"
    """Users."""
    APIKeys = "APIKeys"
    """Access keys."""
    ReputationLists = "ReputationLists"
    """Reputation lists."""
    ReputationListsContent = "ReputationListsContent"
    """Reputation list contents. Permission can be only with reading action."""
    StoredQuery = "StoredQuery"
    """Stored queries."""
