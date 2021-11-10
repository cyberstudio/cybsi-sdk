"""Use this section of API operate tasks.
"""
from typing import Optional, Union

from ..artifact import ArtifactTypes
from ..common import RefView
from ..internal import JsonObjectView
from ..observable import EntityView, ShareLevels


class ArtifactAnalysisParamsView(JsonObjectView):
    """Parameters of :attr:`~cybsi.api.enrichment.EnrichmentTypes.ArtifactAnalysis` tasks."""  # noqa: E501

    @property
    def artifact(self) -> "ArtifactParamView":
        """Artifact, enrichment target.

        Note:
            Use :class:`~cybsi.api.artifact.api.ArtifactsAPI`
            to retrieve complete artifact information and
            its binary content.
        """
        return ArtifactParamView(self._get("artifact"))

    @property
    def image_id(self) -> Optional[str]:
        """Analyzer-specific image id."""
        return self._get_optional("imageID")


class ArtifactParamView(RefView):
    """Artifact view."""

    @property
    def type(self) -> ArtifactTypes:
        """Artifact type."""
        return ArtifactTypes(self._get("type"))

    @property
    def share_level(self) -> ShareLevels:
        """Artifact share level."""
        return ShareLevels(self._get("shareLevel"))


class ExternalDBLookupParamsView(JsonObjectView):
    """Parameters of :attr:`~cybsi.api.enrichment.EnrichmentTypes.ExternalDBLookup` tasks."""  # noqa: E501

    @property
    def entity(self) -> EntityView:
        """Entity, enrichment target."""
        return EntityView(self._get("entity"))


EnrichmentTaskParamsView = Union[ArtifactAnalysisParamsView, ExternalDBLookupParamsView]
