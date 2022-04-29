import cgi
import uuid
from contextlib import asynccontextmanager, contextmanager
from datetime import datetime
from io import BytesIO
from typing import (
    Any,
    AsyncContextManager,
    AsyncIterator,
    ContextManager,
    Dict,
    Iterable,
    Iterator,
    List,
    Optional,
    cast,
)

from .. import RefView
from ..error import CybsiError
from ..internal import BaseAPI, BaseAsyncAPI, JsonObjectView, parse_rfc3339_timestamp
from ..observable import EntityView, ShareLevels
from ..pagination import AsyncPage, Cursor, Page
from ..view import _TaggedRefView
from .enums import ArtifactContentDownloadCompressionTypes, ArtifactTypes

_ARTIFACTS_PATH = "/enrichment/artifacts"
_ARTIFACTS_TYPE_PATH = "/enrichment/artifact-type"


class ArtifactsAPI(BaseAPI):
    """Artifact API."""

    def view(self, artifact_uuid: uuid.UUID) -> "ArtifactView":
        """Get an artifact view.

        Note:
            Calls `GET /enrichment/artifacts/{artifact_uuid}`.
        Args:
            artifact_uuid: Artifact uuid.
        Returns:
            View of the artifact.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: Artifact not found.
        """
        path = f"{_ARTIFACTS_PATH}/{artifact_uuid}"
        r = self._connector.do_get(path)
        return ArtifactView(r)

    def view_registrations(
        self, artifact_uuid: uuid.UUID
    ) -> List["ArtifactRegistrationView"]:
        """Get artifact registrations.

        Note:
            Calls `GET /enrichment/artifacts/{artifact_uuid}/registrations`.
        Args:
            artifact_uuid: Artifact uuid.
        Returns:
            List of artifact registrations.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: Artifact not found.
        """
        path = f"{_ARTIFACTS_PATH}/{artifact_uuid}/registrations"
        r = self._connector.do_get(path)
        return [ArtifactRegistrationView(v) for v in r.json()]

    def recognize_type(self, data: Any) -> "ArtifactTypeRecognizedView":
        """Recognize artifact type by its first bytes.

        The function allows to send the entire artifact, but it's recommended
        to send 10KB or less to save time and bandwidth.

        Note:
            Calls `PUT /enrichment/artifact-type`.
        Args:
            data: File-like object. If you have bytes, wrap them in BytesIO.
        Returns:
            Recognized artifact type.
        See Also:
            The function is similar to :meth:`upload`.
            The example for :meth:`upload` is applicable here too.
        """

        form = {"file": ("filename", data)}

        r = self._connector.do_put(path=_ARTIFACTS_TYPE_PATH, files=form)
        return ArtifactTypeRecognizedView(r.json())

    def upload(
        self,
        filename: str,
        data: Any,
        artifact_type: ArtifactTypes = None,
        share_level: ShareLevels = ShareLevels.White,
    ) -> RefView:
        """Upload an artifact.

        Note:
            Calls `POST /enrichment/artifacts`.
        Args:
            filename: Name of the artifact.
            data: File-like object. If you have bytes, wrap them in BytesIO.
            artifact_type: Artifact type.
            share_level: Artifact share level.
        Returns:
            Reference to artifact in API.
        Raises:
            :class:`~cybsi.api.error.SemanticError`: Semantic error. Possible code is
             :attr:`~cybsi.api.error.SemanticErrorCodes.InvalidShareLevel`.
        See Also:
            See :ref:`upload-download-artifact-example`
            for a complete example of this function usage.

        """

        form: Dict[str, Any] = {}

        if artifact_type is not None:
            form["type"] = artifact_type.value.encode()

        form["shareLevel"] = share_level.value.encode()
        form["file"] = (filename, data)

        r = self._connector.do_post(path=_ARTIFACTS_PATH, files=form)
        return RefView(r.json())

    def get_content(
        self,
        artifact_uuid: uuid.UUID,
        archive: ArtifactContentDownloadCompressionTypes = None,
        archive_password: str = None,
    ) -> ContextManager["ArtifactContent"]:
        """Get artifact content.

        Note:
            Calls `GET /enrichment/artifacts/{artifact_uuid}/content`.
        Args:
            artifact_uuid: Artifact uuid.
            archive: Compress artifact content to archive of chosen type before sending.
            archive_password: Set archive password,
             if compression was chosen using ``archive`` argument.
        Returns:
            Contextmanager of binary file content.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: Artifact not found.
        Examples:
            >>> with client.artifacts.get_content(artifact_uuid) as content:
            >>>     with open("/tmp/artifact", "wb") as f:
            >>>         shutil.copyfileobj(content.stream, f, length=1024 * 1024)
        See Also:
            See :ref:`upload-download-artifact-example`
            for a complete example of this function usage.
        """
        path = f"{_ARTIFACTS_PATH}/{artifact_uuid}/content"

        params = {}
        if archive:
            params["archive"] = archive.value
        if archive_password:
            params["password"] = archive_password

        @contextmanager
        def load_content():
            r = self._connector.do_get(path=path, params=params, stream=True)
            try:
                filename = _parse_content_filename(r)
                yield ArtifactContent(filename, r)
            finally:
                r.close()

        return load_content()

    def filter(
        self,
        artifact_type: Optional[ArtifactTypes] = None,
        data_source_uuids: Optional[Iterable[uuid.UUID]] = None,
        file_uuid: Optional[uuid.UUID] = None,
        artifact_hash: Optional[str] = None,
        cursor: Optional[Cursor] = None,
        limit: Optional[int] = None,
    ) -> Page["ArtifactCommonView"]:
        """Filter artifacts using provided parameters.

        Note:
            Calls `GET /enrichment/artifacts`
        Args:
            artifact_type: Artifact type.
            data_source_uuids: Data sources of the artifact.
            file_uuid: Artifact hash must be the same
                as one of the hashes of provided File entity.
            artifact_hash: Artifact hash.
                Hash type (md5, sha1, sha256) is determined using its length.
            cursor: Page cursor.
            limit: Page limit.
        Raises:
            :class:`~cybsi.api.error.SemanticError`: Query contains logic errors.
        Note:
            Semantic error codes specific for this method:
                * :attr:`~cybsi.api.error.SemanticErrorCodes.DataSourceNotFound`
                * :attr:`~cybsi.api.error.SemanticErrorCodes.FileNotFound`
        Return:
            Page containing artifact descriptions.
        """
        params: Dict[str, Any] = {}
        if artifact_type:
            params["type"] = artifact_type.value
        if data_source_uuids:
            params["dataSourceUUID"] = [str(u) for u in data_source_uuids]
        if file_uuid:
            params["fileUUID"] = str(file_uuid)
        if artifact_hash:
            params["hash"] = artifact_hash
        if cursor:
            params["cursor"] = str(cursor)
        if limit:
            params["limit"] = str(limit)

        resp = self._connector.do_get(_ARTIFACTS_PATH, params=params)
        page = Page(self._connector.do_get, resp, ArtifactCommonView)
        return page


class ArtifactsAsyncAPI(BaseAsyncAPI):
    """Asynchronous artifact API."""

    async def view(self, artifact_uuid: uuid.UUID) -> "ArtifactView":
        """Get an artifact view.

        Note:
            Calls `GET /enrichment/artifacts/{artifact_uuid}`.
        Args:
            artifact_uuid: Artifact uuid.
        Returns:
            View of the artifact.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: Artifact not found.
        """
        path = f"{_ARTIFACTS_PATH}/{artifact_uuid}"
        r = await self._connector.do_get(path)
        return ArtifactView(r)

    async def view_registrations(
        self, artifact_uuid: uuid.UUID
    ) -> List["ArtifactRegistrationView"]:
        """Get artifact registrations.

        Note:
            Calls `GET /enrichment/artifacts/{artifact_uuid}/registrations`.
        Args:
            artifact_uuid: Artifact uuid.
        Returns:
            List of artifact registrations.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: Artifact not found.
        """
        path = f"{_ARTIFACTS_PATH}/{artifact_uuid}/registrations"
        r = await self._connector.do_get(path)
        return [ArtifactRegistrationView(v) for v in r.json()]

    async def recognize_type(self, data: Any) -> "ArtifactTypeRecognizedView":
        """Recognize artifact type by its first bytes.

        The function allows to send the entire artifact, but it's recommended
        to send 10KB or less to save time and bandwidth.

        Note:
            Calls `PUT /enrichment/artifact-type`.
        Args:
            data: File-like object. If you have bytes, wrap them in BytesIO.
        Returns:
            Recognized artifact type.
        See Also:
            The function is similar to :meth:`upload`.
            The example for :meth:`upload` is applicable here too.
        """

        form = {"file": ("filename", data)}

        r = await self._connector.do_put(path=_ARTIFACTS_TYPE_PATH, files=form)
        return ArtifactTypeRecognizedView(r.json())

    async def upload(
        self,
        filename: str,
        data: Any,
        artifact_type: ArtifactTypes = None,
        share_level: ShareLevels = ShareLevels.White,
    ) -> RefView:
        """Upload an artifact.

        Note:
            Calls `POST /enrichment/artifacts`.
        Args:
            filename: Name of the artifact.
            data: File-like object. If you have bytes, wrap them in BytesIO.
            artifact_type: Artifact type.
            share_level: Artifact share level.
        Returns:
            Reference to artifact in API.
        Raises:
            :class:`~cybsi.api.error.SemanticError`: Semantic error. Possible code is
             :attr:`~cybsi.api.error.SemanticErrorCodes.InvalidShareLevel`.
        See Also:
            See :ref:`upload-download-artifact-example`
            for a complete example of this function usage.

        """

        form: Dict[str, Any] = {}

        if artifact_type is not None:
            form["type"] = artifact_type.value.encode()

        form["shareLevel"] = share_level.value.encode()
        form["file"] = (filename, data)

        r = await self._connector.do_post(path=_ARTIFACTS_PATH, files=form, timeout=300)
        return RefView(r.json())

    def get_content(
        self,
        artifact_uuid: uuid.UUID,
        archive: ArtifactContentDownloadCompressionTypes = None,
        archive_password: str = None,
    ) -> AsyncContextManager["ArtifactAsyncContent"]:
        """Get artifact content

        Note:
            Calls `GET /enrichment/artifacts/{artifact_uuid}/content`.
        Args:
            artifact_uuid: Artifact uuid.
            archive: Compress artifact content to archive of chosen type before sending.
            archive_password: Set archive password,
             if compression was chosen using ``archive`` argument.
        Returns:
            Contextmanager of binary file content.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: Artifact not found.
        Examples:
            >>>    async with aiofiles.open("/tmp/artifact", "wb") as f, client.artifacts.get_content(
            >>>        artifact_uuid
            >>>    ) as content:
            >>>        async for chunk in content.iter_chunks(size=8192):
            >>>            await f.write(chunk)
        See Also:
            See :ref:`upload-download-artifact-example`
            for a complete example of this function usage.
        """  # noqa: E501
        path = f"{_ARTIFACTS_PATH}/{artifact_uuid}/content"

        params = {}
        if archive:
            params["archive"] = archive.value
        if archive_password:
            params["password"] = archive_password

        @asynccontextmanager
        async def load_content():
            r = await self._connector.do_get(path=path, params=params, stream=True)
            try:
                filename = _parse_content_filename(r)
                yield ArtifactAsyncContent(filename, r)
            finally:
                await r.aclose()

        return load_content()

    async def filter(
        self,
        artifact_type: Optional[ArtifactTypes] = None,
        data_source_uuids: Optional[Iterable[uuid.UUID]] = None,
        file_uuid: Optional[uuid.UUID] = None,
        artifact_hash: Optional[str] = None,
        cursor: Optional[Cursor] = None,
        limit: Optional[int] = None,
    ) -> AsyncPage["ArtifactCommonView"]:
        """Filter artifacts using provided parameters.

        Note:
            Calls `GET /enrichment/artifacts`
        Args:
            artifact_type: Artifact type.
            data_source_uuids: Data sources of the artifact.
            file_uuid: Artifact hash must be the same
                as one of the hashes of provided File entity.
            artifact_hash: Artifact hash.
                Hash type (md5, sha1, sha256) is determined using its length.
            cursor: Page cursor.
            limit: Page limit.
        Raises:
            :class:`~cybsi.api.error.SemanticError`: Query contains logic errors.
        Note:
            Semantic error codes specific for this method:
                * :attr:`~cybsi.api.error.SemanticErrorCodes.DataSourceNotFound`
                * :attr:`~cybsi.api.error.SemanticErrorCodes.FileNotFound`
        Return:
            Page containing artifact descriptions.
        """
        params: Dict[str, Any] = {}
        if artifact_type:
            params["type"] = artifact_type.value
        if data_source_uuids:
            params["dataSourceUUID"] = [str(u) for u in data_source_uuids]
        if file_uuid:
            params["fileUUID"] = str(file_uuid)
        if artifact_hash:
            params["hash"] = artifact_hash
        if cursor:
            params["cursor"] = str(cursor)
        if limit:
            params["limit"] = str(limit)

        resp = await self._connector.do_get(_ARTIFACTS_PATH, params=params)
        page = AsyncPage(self._connector.do_get, resp, ArtifactCommonView)
        return page


class ArtifactTypeRecognizedView(JsonObjectView):
    """Artifact type view, as recognized by Cybsi."""

    @property
    def type(self) -> ArtifactTypes:
        """Artifact type."""
        return ArtifactTypes(self._get("type"))

    @property
    def format_description(self) -> str:
        """Format description (magic).

        Example:
         ``PE32 executable (GUI) Intel 80386, for MS Windows, Nullsoft Installer self-extracting archive``
        """  # noqa: E501
        return self._get("formatDescription")


class ArtifactContent:
    """Binary artifact content.

    May be packed in archive, if it is requested in :meth:`ArtifactsAPI.get_content`.
    """

    def __init__(self, filename: str, raw: Any):
        self._filename = filename
        self._raw = raw

    @property
    def filename(self) -> str:
        """Artifact file name."""
        return self._filename

    @property
    def stream(self) -> Any:
        """Stream with binary artifact content.

        File-like object, supports read() but does not support seek().
        """
        # TODO: Implement actual streaming using iter_bytes()
        # https://www.python-httpx.org/compatibility/#streaming-responses
        return BytesIO(self._raw.read())

    def iter_chunks(self, size=4096) -> Iterator[bytes]:
        """Iterates over data chunks with maximum size limit.

        Args:
            size: chunk size.
        Return:
            Iterator over data chunks.
        """
        return self._raw.iter_bytes(size)

    def readall(self) -> bytes:
        """Read all content data."""
        return self._raw.read()


class ArtifactAsyncContent:
    """Binary artifact content with asynchronous API.

    May be packed in archive,
     if it is requested in :meth:`ArtifactsAsyncAPI.get_content`.
    """

    def __init__(self, filename: str, raw: Any):
        self._filename = filename
        self._raw = raw

    @property
    def filename(self) -> str:
        """Artifact file name."""
        return self._filename

    def iter_chunks(self, size=4096) -> AsyncIterator[bytes]:
        """Iterates over data chunks with maximum size limit.

        Args:
            size: chunk size.
        Return:
            Asynchronous iterator over data chunks.
        """
        return self._raw.aiter_bytes(size)

    async def readall(self) -> bytes:
        """Read all content data."""
        chunks = []
        async for chunk in self.iter_chunks():
            chunks.append(chunk)
        return b"".join(chunks)


def _parse_content_filename(response) -> str:
    """Parse filename parameter from content-disposition header."""
    try:
        value, params = cgi.parse_header(response.headers["content-disposition"])
    except KeyError:
        raise CybsiError("Content-disposition header not found") from None

    try:
        return params["filename"]
    except KeyError:
        raise CybsiError("filename not found in Content-disposition header") from None


class ArtifactCommonView(RefView):
    """Common artifact view."""

    @property
    def types(self) -> List[ArtifactTypes]:
        """Artifact types."""
        return [ArtifactTypes(t) for t in self._get("types")]

    @property
    def data_sources(self) -> List[RefView]:
        """Data sources which registered the artifact."""
        return [RefView(t) for t in self._get("dataSources")]

    @property
    def share_levels(self) -> Optional[List[ShareLevels]]:
        """Artifact share levels, ordered from lowest to highest."""
        return self._map_list_optional("shareLevels", ShareLevels)

    @property
    def content(self) -> "ArtifactContentView":
        """Artifact content meta information."""
        return ArtifactContentView(self._get("content"))


class ArtifactView(_TaggedRefView):
    """Artifact view."""

    @property
    def types(self) -> List[ArtifactTypes]:
        """Artifact types."""
        return [ArtifactTypes(t) for t in self._get("types")]

    @property
    def data_sources(self) -> List[RefView]:
        """Data sources which registered the artifact."""
        return [RefView(t) for t in self._get("dataSources")]

    @property
    def share_levels(self) -> Optional[List[ShareLevels]]:
        """Artifact share levels, ordered from lowest to highest."""
        return self._map_list_optional("shareLevels", ShareLevels)

    @property
    def content(self) -> "ArtifactContentView":
        """Artifact content meta information."""
        return ArtifactContentView(self._get("content"))

    @property
    def file_names(self) -> List[str]:
        """Artifact file names. Ordered by time of registration."""
        return cast(List[str], self._get("fileNames"))

    @property
    def entities(self) -> List[EntityView]:
        """List of file entities associated with this artifact."""
        return [EntityView(e) for e in self._get("entities")]


class ArtifactContentView(JsonObjectView):
    """Artifact content meta information."""

    @property
    def url(self) -> str:
        """Absolute URL of artifact content."""
        return cast(str, self._get("url"))

    @property
    def size(self) -> int:
        """File size."""
        return int(self._get("size"))

    @property
    def md5_hash(self) -> str:
        """MD5 hash of file content."""
        return cast(str, self._get("md5Hash"))

    @property
    def sha1_hash(self) -> str:
        """SHA1 hash of file content."""
        return cast(str, self._get("sha1Hash"))

    @property
    def sha256_hash(self) -> str:
        """SHA256 hash of file content."""
        return cast(str, self._get("sha256Hash"))

    @property
    def format_description(self) -> Optional[str]:
        """File format description magically extracted from signature."""
        return self._get_optional("formatDescription")


class ArtifactRegistrationView(JsonObjectView):
    """Artifact registration view."""

    @property
    def data_source(self) -> RefView:
        """Data source which registered the artifact."""
        return RefView(self._get("dataSource"))

    @property
    def type(self) -> ArtifactTypes:
        """Artifact type."""
        return ArtifactTypes(self._get("type"))

    @property
    def file_name(self) -> str:
        """Artifact file name"""
        return self._get("fileName")

    @property
    def share_level(self) -> ShareLevels:
        """Artifact share level"""
        return ShareLevels(self._get("shareLevel"))

    @property
    def registered_at(self) -> datetime:
        return parse_rfc3339_timestamp(self._get("registeredAt"))
