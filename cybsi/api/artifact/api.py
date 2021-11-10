import io
import uuid
from typing import List, cast

from ..common import RefView
from ..internal import BaseAPI, JsonObjectView
from ..observable import ShareLevels

from .enums import ArtifactTypes


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
        """
        path = f"{self._path}/{artifact_uuid}"
        r = self._connector.do_get(path)
        return ArtifactView(r.json())

    def get_content(self, artifact_uuid: uuid.UUID) -> io.BytesIO:
        """Get artifact content as stream of bytes.

        Note:
            Calls `GET /enrichment/artifacts/{artifact_uuid}/content`.
        Args:
            artifact_uuid: Artifact uuid.
        Returns:
            Binary artifact content.
        Warning:
            Not implemented yet.
        """
        raise NotImplementedError()


class ArtifactView(RefView):
    """Artifact view.

    TODO:
        Implement other properties.
    """

    @property
    def types(self) -> List[ArtifactTypes]:
        """Artifact types."""
        return [ArtifactTypes(t) for t in self._get("types")]

    @property
    def share_levels(self) -> List[ShareLevels]:
        """Artifact share levels."""
        return [ShareLevels(s) for s in self._get("shareLevels")]

    @property
    def content(self) -> "ArtifactContentView":
        """Artifact content meta information."""
        return ArtifactContentView(self._get("content"))


class ArtifactContentView(JsonObjectView):
    """Artifact content meta information.

    TODO:
        Implement other properties.
    """

    @property
    def md5_hash(self) -> str:
        """MD5 hash of artifact content."""
        return cast(str, self._get("md5Hash"))
