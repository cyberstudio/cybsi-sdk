import cgi
import uuid
from typing import List, cast, Any, Dict, Optional

from ..common import RefView
from ..error import CybsiError
from ..internal import BaseAPI, JsonObjectView
from ..observable import ShareLevels, EntityView

from .enums import ArtifactTypes, ArtifactContentDownloadCompressionTypes


class ArtifactsAPI(BaseAPI):
    """Artifact API."""

    _path = "/enrichment/artifacts"

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
        path = f"{self._path}/{artifact_uuid}"
        r = self._connector.do_get(path)
        return ArtifactView(r.json())

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
            form["type"] = artifact_type.value

        form["shareLevel"] = share_level.value
        form["file"] = (filename, data)

        r = self._connector.do_post(path=self._path, files=form)
        return RefView(r.json())

    def get_content(
        self,
        artifact_uuid: uuid.UUID,
        archive: ArtifactContentDownloadCompressionTypes = None,
        archive_password: str = None,
    ) -> "ArtifactContent":
        """Get artifact content as stream of bytes.

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
        Warning:
            Use ``with`` expression or :meth:`ArtifactContent.close()` to close content
            when it's no longer needed.
        Examples:
            >>> with client.artifacts.get_content(artifact_uuid) as content:
            >>>     with open("/tmp/artifact", "wb") as f:
            >>>         shutil.copyfileobj(content.stream, f, length=1024 * 1024)
        See Also:
            See :ref:`upload-download-artifact-example`
            for a complete example of this function usage.
        """
        path = f"{self._path}/{artifact_uuid}/content"

        params = {}
        if archive:
            params["archive"] = archive.value
        if archive_password:
            params["password"] = archive_password

        r = self._connector.do_get(path=path, params=params, stream=True)

        filename = _parse_content_filename(r)
        return ArtifactContent(filename, r.raw)


class ArtifactContent:
    """Binary artifact content.

    May be packed in archive, if it was requested in :meth:`ArtifactsAPI.get_content`.
    """

    def __init__(self, filename: str, raw: Any):
        self._filename = filename
        self._raw = raw
        self._raw.decode_content = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._raw.close()

    @property
    def filename(self) -> str:
        """Artifact file name."""
        return self._filename

    @property
    def stream(self) -> Any:
        """Stream with binary artifact content.

        File-like object, supports read() but does not support seek().
        """
        return self._raw

    def close(self):
        """Close content, releasing connection."""
        self._raw.close()


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


class ArtifactView(RefView):
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
        sl = self._get_optional("shareLevels")
        return None if sl is None else [ShareLevels(s) for s in sl]

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
