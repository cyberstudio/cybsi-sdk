"""This section documents exceptions SDK can raise.

Those are exceptions SDK client can expect if SDK is used in correct way.
If your Python code didn't respect the expected model, there's no guarantees.
For example, if function argument types are ignored,
SDK can raise exceptions not listed here.

Each exception type is annotated if it makes sense to retry.

Some exceptions have ``code`` property. It allows to determine the concrete error.
"""
from typing import Any, Dict, Optional, cast

import httpx
from enum_tools import document_enum

from .enum import CybsiAPIEnum


class CybsiError(Exception):
    """Base exception used by SDK. Sometimes can be retried.

    If it's not of one of subclasses (see below), means unexpected error.

    :class:`CybsiError` covers those cases:

    * Unexpected API response status code. See :class:`APIError` for specific errors.
    * Unexpected API response content.
    * Connection error.

    """

    def __init__(self, message: str, ex: Optional[Exception] = None):
        if ex and str(ex) != "":
            message = f"{message}: {ex}"
        super().__init__(message)
        self._ex = ex


JsonObject = Dict[str, Any]


class APIError(CybsiError):
    """Base exception for HTTP 4xx API responses."""

    def __init__(
        self,
        status: int,
        content: JsonObject,
        header: Optional[str] = None,
        suffix: Optional[str] = None,
    ) -> None:
        self._status = status
        self._view = _ErrorView(content)
        self._header = (
            header
            if header is not None
            else f"API response error. HTTP status: {self._status}"
        )
        self._suffix = (
            suffix
            if suffix is not None
            else f"code: {self._view.code}, message: {self._view.message}"
        )

        msg = self._header
        if self._suffix:
            msg += f", {self._suffix}"
        super().__init__(msg)

    @property
    def content(self) -> JsonObject:
        return self._view


class InvalidRequestError(APIError):
    """Invalid request error. Retry will never work.

    Ideally, should not be raised by SDK. If it's raised, it means one of two things:

    * SDK was used incorrectly. For example, values of invalid type
      were passed to SDK functions.
    * There's a bug in request serialization in SDK. Please report the bug.

    """

    BadRequest = "BadRequest"
    InvalidData = "InvalidData"
    InvalidPathArgument = "InvalidPathArgument"
    InvalidQueryArgument = "InvalidQueryArgument"
    NoSuchAttribute = "NoSuchAttribute"

    def __init__(self, content: JsonObject) -> None:
        super().__init__(400, content, header="invalid request")


class UnauthorizedError(APIError):
    """Client lacks valid authentication credentials. Retry will never work."""

    Unauthorized = "Unauthorized"

    def __init__(self, content: JsonObject) -> None:
        super().__init__(401, content, header="operation not authorized")


class ForbiddenError(APIError):
    """Operation was forbidden. Retry will not work unless system is reconfigured."""

    def __init__(self, content: JsonObject) -> None:
        super().__init__(403, content, header="operation forbidden")

    @property
    def code(self) -> "ForbiddenErrorCodes":
        """Error code."""
        return ForbiddenErrorCodes(self._view.code)


class NotFoundError(APIError):
    """Requested resource not found. Retry will never work."""

    def __init__(self, content: JsonObject) -> None:
        super().__init__(404, {}, header="resource not found", suffix="")


class ConflictError(APIError):
    """Resource already exists. Retry will never work."""

    DuplicateDataSource = "DuplicateDataSource"
    DuplicateDataSourceType = "DuplicateDataSourceType"
    DuplicateKey = "DuplicateKey"
    DuplicateLogin = "DuplicateLogin"
    StoredQueryConflict = "StoredQueryConflict"
    DuplicateCustomList = "DuplicateCustomList"

    def __init__(self, content: JsonObject) -> None:
        super().__init__(409, content, header="resource already exists")


class ResourceModifiedError(APIError):
    """Resource was modified since last read. **Retry is a must**.

    Read the updated resource from API, and apply your modifications again.
    """

    ErrResourceModified = "ResourceModified"

    def __init__(self, content: JsonObject) -> None:
        super().__init__(
            412, content, header="resource was modified since last read", suffix=""
        )


class SemanticError(APIError):
    """Semantic error. Retry will not work (almost always).

    Request syntax was valid, but system business rules forbid the request.

    For example, we're trying to unpack an artifact, but the artifact is not an archive.
    """

    def __init__(self, content: JsonObject) -> None:
        super().__init__(422, content, header="semantic error")

    @property
    def code(self) -> "SemanticErrorCodes":
        """Error code."""
        return SemanticErrorCodes(self._view.code)


@document_enum
class ForbiddenErrorCodes(CybsiAPIEnum):
    """Possible error codes of :class:`ForbiddenError`."""

    InvalidCredentials = "InvalidCredentials"
    """User provided invalid credentials."""
    InsufficientAccessLevel = "InsufficientAccessLevel"
    """User authenticated but has insufficient access level to access the resource."""
    MissingPermissions = "MissingPermissions"
    """User authenticated but not authorized to perform operation."""
    NotOwner = "NotOwner"
    """Only owner can edit the resource."""
    Forbidden = "Forbidden"
    """Other cases."""


@document_enum
class SemanticErrorCodes(CybsiAPIEnum):
    """Common semantic error codes."""

    ArtifactNotFound = "ArtifactNotFound"
    """Artifact not found."""
    BrokenKeySet = "BrokenKeySet"
    """Key set identifies multiple entities."""
    CorruptedLicense = "CorruptedLicense"
    """Invalid signature or license data corrupted"""
    CursorOutOfRange = "CursorOutOfRange"
    """Cursor points outside of event list."""
    DataSourceNotFound = "DataSourceNotFound"
    """Data source not found."""
    DataSourceTypeNotFound = "DataSourceTypeNotFound"
    """Data source type not found."""
    DictionaryClosed = "DictionaryClosed"
    """Dictionary is closed for modification."""
    DictionaryNotFound = "DictionaryNotFound"
    """Dictionary not found."""
    DictionaryItemNotFound = "DictionaryItemNotFound"
    """Dictionary item not found."""
    DuplicatedEntityAttribute = "DuplicatedEntityAttribute"
    """
        Entity attribute was specified several times
        and attribute is not an array.
    """
    EnrichmentNotAllowed = "EnrichmentNotAllowed"
    """Enrichment using provided parameters is not possible."""
    EntityNotFound = "EntityNotFound"
    """Entity not found."""
    EntityViewNotFound = "EntityViewNotFound"
    """Entity view not found."""
    ExpiredLicense = "ExpiredLicense"
    """Expired license"""
    FileNotFound = "FileNotFound"
    """File entity not found."""
    LicenseFileMissing = "LicenseFileMissing"
    """License file is missing or corrupted"""
    ImmutableValue = "ImmutableValue"
    """Resource attribute edits are blocked."""
    InvalidAttribute = "InvalidAttribute"
    """Invalid attribute for such entity."""
    InvalidAttributeValue = "InvalidAttributeValue"
    """Invalid attribute value."""
    InvalidDictionary = "InvalidDictionary"
    """
        The specified dictionary item and the synonym
        refer to different directories.
    """
    InvalidErrorCode = "InvalidErrorCode"
    """Invalid task error code reported by enricher."""
    InvalidKey = "InvalidKey"
    """Invalid key value for such entity or entity key type."""
    InvalidKeySet = "InvalidKeySet"
    """
        Entity has invalid set of keys
        (invalid key type for such entity,
        invalid number of keys, and so on).
    """
    InvalidQueryText = "InvalidQueryText"
    """Query text is invalid CybsiLang expression."""
    InvalidRelationship = "InvalidRelationship"
    """Relationship is invalid."""
    InvalidRule = "InvalidRule"
    """Enrichment configuration rule is invalid."""
    InvalidShareLevel = "InvalidShareLevel"
    """Specified share level is above API client share level."""
    InvalidTaskResult = "InvalidTaskResult"
    """Invalid task result was reported by enricher."""
    InvalidTaskStatus = "InvalidTaskStatus"
    """
        Could not accept enrichment result,
        task status is not ``Executing``.
    """
    InvalidSynonym = "InvalidSynonym"
    """
        The specified element is an invalid synonym (for example,
        the element and the synonym have the same key).
    """
    InvalidTime = "InvalidTime"
    """Timestamp is invalid (for example, it's in the future)"""
    KeyConflict = "KeyConflict"
    """
        Provided entity key conflicts with key
        already registered in the system."""
    MisconfiguredDataSource = "MisconfiguredDataSource"
    """Enrichment rule is invalid for such data source."""
    NonLocalUser = "NonLocalUser"
    """
        Impossible to change user attribute because
        this attribute is managed by external provider.
    """
    NotOwner = "NotOwner"
    """Only owner can edit the resource."""
    ObservationNotFound = "ObservationNotFound"
    """Observation not found."""
    PasswordAuthDisabled = "PasswordAuthDisabled"
    """
        Impossible to change the password because
        password auth for such user is disabled.
    """
    PermissionsExceeded = "PermissionsExceeded"
    """Provided set of permissions exceeds user permissions."""
    ReportNotFound = "ReportNotFound"
    """Report not found."""
    StoredQueryNotFound = "StoredQueryNotFound"
    """Stored query not found."""
    SynonymGroupConflict = "SynonymGroupConflict"
    """The specified item and synonym belong to different synonym groups."""
    ItemAlreadyInSynonymGroup = "ItemAlreadyInSynonymGroup"
    """The specified synonym is already in a synonym group."""
    TaskNotFound = "TaskNotFound"
    """Enrichment task not found."""
    UnallowedObservationType = "UnallowedObservationType"
    """Observation of such type cannot be attached to report."""
    UnsupportedProduct = "UnsupportedProduct"
    """Unsupported product"""
    UserDisabled = "UserDisabled"
    """User disabled."""
    UserNotFound = "UserNotFound"
    """User not found."""
    WrongEntityAttribute = "WrongEntityAttribute"
    """The attribute is not registered for provided entity."""
    InvalidStoredQuery = "InvalidStoredQuery"
    """Query is not compatible with replist."""
    StoredQueryIsLocked = "StoredQueryIsLocked"
    """Stored query is in use. Probably used in replist."""
    CustomListNotFound = "CustomListNotFound"
    """Custom List Not Found"""
    DictionaryMismatch = "DictionaryMismatch"
    """Item related to dictionary that not related to custom list"""
    EmptyLandscapeQuery = "EmptyLandscapeQuery"
    """Landscape does not contain any custom list"""


class _ErrorView(dict):
    """Error returned by Cybsi API."""

    @property
    def code(self) -> str:
        """Error code."""

        return cast(str, self.get("code"))

    @property
    def message(self) -> str:
        """Error message."""

        return cast(str, self.get("message"))


_error_mapping = {
    400: InvalidRequestError,
    401: UnauthorizedError,
    403: ForbiddenError,
    404: NotFoundError,
    409: ConflictError,
    412: ResourceModifiedError,
    422: SemanticError,
}


def _raise_cybsi_error(resp: httpx.Response) -> None:
    err_cls = _error_mapping.get(resp.status_code, None)
    if err_cls is not None:
        raise err_cls(resp.json())

    raise CybsiError(
        f"unexpected response status code: {resp.status_code}. "
        f"Request body: {resp.text}"
    )
