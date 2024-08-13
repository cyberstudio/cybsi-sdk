from enum_tools import document_enum

from cybsi.api.enum import CybsiAPIEnum


@document_enum
class ObjectDomain(CybsiAPIEnum):
    """Object domain."""

    Auth = "Auth"  # doc: Auth
    Users = "Users"  # doc: Users
    ApiKeys = "ApiKeys"  # doc: ApiKeys
    Entities = "Entities"  # doc: Entities
    Artifacts = "Artifacts"  # doc: Artifacts
    Enrichment = "Enrichment"  # doc: Enrichment
    Tasks = "Tasks"  # doc: Tasks
    StoredQueries = "StoredQueries"  # doc: StoredQueries
    Reports = "Reports"  # doc: Reports
    Observations = "Observations"  # doc: Observations
    DataSources = "DataSources"  # doc: DataSources
    Replists = "Replists"  # doc: Replists
    Dictionaries = "Dictionaries"  # doc: Dictionaries
    EntityViews = "EntityViews"  # doc: EntityViews
    License = "License"  # doc: License


@document_enum
class ObjectType(CybsiAPIEnum):
    """Object type."""

    User = "User"  # doc: User
    ApiKey = "ApiKey"  # doc: ApiKey
    Entity = "Entity"  # doc: Entity
    Artifact = "Artifact"  # doc: Artifact
    EnrichmentRule = "EnrichmentRule"  # doc: EnrichmentRule
    Analyzer = "Analyzer"  # doc: Analyzer
    ExternalDB = "ExternalDB"  # doc: ExternalDB
    Task = "Task"  # doc: Task
    StoredQuery = "StoredQuery"  # doc: StoredQuery
    Report = "Report"  # doc: Report
    Observation = "Observation"  # doc: Observation
    DataSourceType = "DataSourceType"  # doc: DataSourceType
    DataSource = "DataSource"  # doc: DataSource
    Replist = "Replist"  # doc: Replist
    Dictionary = "Dictionary"  # doc: Dictionary
    DictionaryItem = "DictionaryItem"  # doc: DictionaryItem
    DictionaryRelatedItems = "DictionaryRelatedItems"  # doc: DictionaryRelatedItems
    EntityView = "EntityView"  # doc: EntityView
    License = "License"  # doc: License


@document_enum
class Operation(CybsiAPIEnum):
    """Operation."""

    Create = "Create"  # doc: Create
    Register = "Register"  # doc: Register
    Run = "Run"  # doc: Run
    Read = "Read"  # doc: Read
    Modify = "Modify"  # doc: Modify
    Delete = "Delete"  # doc: Delete
    Login = "Login"  # doc: Login
    Logout = "Logout"  # doc: Logout
    Import = "Import"  # doc: Import
    UpdatePasswd = "UpdatePasswd"  # doc: UpdatePasswd


@document_enum
class Result(CybsiAPIEnum):
    """Action result."""

    Unknown = "Unknown"  # doc: Unknown.
    Success = "Success"  # doc: Success.
    Failure = "Failure"  # doc: Failure.
