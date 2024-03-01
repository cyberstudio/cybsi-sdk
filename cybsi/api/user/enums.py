from enum_tools import document_enum

from cybsi.api.enum import CybsiAPIEnum


@document_enum
class RoleName(CybsiAPIEnum):
    """Role name.

    Role means a list of permissions.
    Each permission is Resource:Action pair.
    See :class:`ResourceName`.
    """

    SystemAdministrator = "SystemAdministrator"
    """
        .. versionadded:: 2.12

        System administrator's role permissions:
        [DataSources:r,Users:rw,APIKeys:rw,License:w]
    """
    DataEngineer = "DataEngineer"
    """
        .. versionadded:: 2.12

        Data engineer's role permissions:
        [StoredQuery:rw,Observable:r,EntityView:r,Artifacts:r,
        ArtifactsContent:r,ReputationLists:rw,ReputationListsContent:r,
        EnrichmentConfig:rw,DataSources:rw,Users:rw,APIKeys:rw,
        Dictionaries:rw]
    """
    SOCAnalyst = "SOCAnalyst"
    """
        .. versionadded:: 2.12

        SOC analyst's role permissions:
        [StoredQuery:rw,Observable:rw,EntityView:r,Artifacts:rw,
        ArtifactsContent:r,Reports:rw,Observations:rw,RawReports:r
        EnrichmentTasks:rw,ReputationLists:rw,ReputationListsContent:r,
        EnrichmentConfig:r,DataSources:r,Users:r,Dictionaries:rw]
    """
    CTIAnalyst = "CTIAnalyst"
    """
        .. versionadded:: 2.12

        CTI analyst's role permissions:
        [StoredQuery:r,Observable:rw,EntityView:r,Artifacts:rw,
        ArtifactsContent:r,Reports:rw,Observations:rw,RawReports:r
        EnrichmentTasks:rw,ReputationLists:r,ReputationListsContent:r,
        EnrichmentConfig:r,DataSources:r,Users:r,Dictionaries:rw]
    """
    CyberSecuritySpecialist = "CyberSecuritySpecialist"
    """
        .. versionadded:: 2.12

        Cyber security specialist's role permissions:
        [StoredQuery:r,Observable:r,EntityView:r,Artifacts:r,
        Reports:r,Observations:r,RawReports:r,EnrichmentTasks:rw,
        ReputationLists:r,ReputationListsContent:r,
        EnrichmentConfig:r,DataSources:r,Users:r,Dictionaries:rw]
    """
    Guest = "Guest"
    """
        .. versionadded:: 2.12

        Guest's role permissions:
        [Observable:r,Artifacts:r,Reports:r,Observations:r,
        RawReports:r,EnrichmentTasks:r,EnrichmentConfig:r,
        DataSources:r,Dictionaries:r]
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
    License = "License"
    """
        .. versionadded:: 2.12

        Licenses.
    """
