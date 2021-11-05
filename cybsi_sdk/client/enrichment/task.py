"""Use this section of API operate tasks.
"""
from typing import Optional, Union

from cybsi_sdk.model.artifact import ArtifactTypes
from cybsi_sdk.model.observable import ShareLevels

from ..common import RefView
from ..internal import JsonObjectView
from ..observable.entity import EntityView


class ArtifactAnalysisParamsView(JsonObjectView):
    """Parameters of :attr:`~cybsi_sdk.model.enrichment.EnrichmentTypes.ArtifactAnalysis` tasks.
    """  # noqa: E501

    @property
    def artifact(self) -> 'ArtifactParamView':
        """Artifact, enrichment target.

        Note:
            Use :class:`~cybsi_sdk.client.artifact.api.ArtifactsAPI`
            to retrieve complete artifact information and
            its binary content.
        """
        return ArtifactParamView(self._get('artifact'))

    @property
    def image_id(self) -> Optional[str]:
        """Analyzer-specific image id."""
        return self._get_optional('imageID')


class ArtifactParamView(RefView):
    """Artifact view."""
    @property
    def type(self) -> ArtifactTypes:
        """Artifact type."""
        return ArtifactTypes(self._get('type'))

    @property
    def share_level(self) -> ShareLevels:
        """Artifact share level."""
        return ShareLevels(self._get('shareLevel'))


class ExternalDBLookupParamsView(JsonObjectView):
    """Parameters of :attr:`~cybsi_sdk.model.enrichment.EnrichmentTypes.ExternalDBLookup` tasks.
    """  # noqa: E501
    @property
    def entity(self) -> EntityView:
        """Entity, enrichment target."""
        return EntityView(self._get('entity'))


EnrichmentTaskParamsView = Union[
    ArtifactAnalysisParamsView,
    ExternalDBLookupParamsView
]
