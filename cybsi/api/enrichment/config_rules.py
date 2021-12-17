"""Use this section of API to operate config rules.
"""
from typing import List, Optional
import uuid

from ..common import RefView
from ..internal import BaseAPI, JsonObjectForm
from ..artifact import ArtifactTypes
from ..observable import EntityTypes
from .enums import EnrichmentTypes, EnrichmentTriggerTypes


class ConfigRulesAPI(BaseAPI):
    """Config rules API."""

    _path = "/enrichment/config/rules"

    def view(self, rule_uuid: uuid.UUID) -> "ConfigRuleView":
        """Get the config rule view.

        Note:
            Calls `GET /enrichment/config/rules/{rule_uuid}`.
        Args:
            rule_uuid: config rule uuid.
        Returns:
            View of the config rule.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: Config rule not found.
        """
        path = f"{self._path}/{rule_uuid}"
        r = self._connector.do_get(path=path)
        return ConfigRuleView(r.json())

    def register(self, rule: "ConfigRuleForm") -> RefView:
        """Register config rule.

        Note:
            Calls `POST /enrichment/config/rules`.
        Args:
            rule: Filled config rule form.
        Returns:
            Reference to config rule in API.
        Raises:
            :class:`~cybsi.api.error.SemanticError`: Form contains logic errors.
        Note:
            Semantic error codes specific for this method:
              * :attr:`~cybsi.api.error.SemanticErrorCodes.InvalidRule`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.DataSourceNotFound`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.MisconfiguredDataSource`
        """
        r = self._connector.do_post(path=self._path, json=rule.json())
        return RefView(r.json())


class ConfigRuleView(RefView):
    """Config rule view."""

    @property
    def name(self) -> str:
        """Config rule name."""
        return self._get("name")

    @property
    def is_disabled(self) -> bool:
        """Disabled config rule flag."""
        return self._get("isDisabled")

    @property
    def is_builtin(self) -> bool:
        """Builtin config rule flag.

        Builtin rules can be set to disabled state, other attributes are immutable.
        """
        return self._get("isBuiltin")

    @property
    def triggers(self) -> List[EnrichmentTriggerTypes]:
        """List of enrichment trigger types."""
        return [EnrichmentTriggerTypes(t) for t in self._get("triggers")]

    @property
    def enrichment(self) -> EnrichmentTypes:
        """Enrichment type."""
        return EnrichmentTypes(self._get("enrichment"))

    @property
    def artifact_types(self) -> Optional[List[ArtifactTypes]]:
        """List of artifact types.

        Not empty for `ArtifactAnalysis` and `ArchiveUnpack` enrichment types.
        """
        return self._map_list_optional("artifactTypes", ArtifactTypes)

    @property
    def entity_types(self) -> Optional[List[EntityTypes]]:
        """List of entity types.

        Not empty for `DNSLookup`, `WhoisLookup`, `ExternalDBLookup` enrichment types.
        """
        return self._map_list_optional("entityTypes", EntityTypes)

    @property
    def data_sources(self) -> Optional[List[RefView]]:
        """Data sources associated with enrichers.

        The rule creates enrichment tasks for enrichers listed here.
        """
        return self._map_list_optional("dataSources", RefView)

    @property
    def trigger_data_sources(self) -> Optional[List[RefView]]:
        """Entity/Artifact registrar associated datasource list.

        The rule is applied only if entity was mentioned or artifact was registered
        by one of data sources from the list.
        """
        return self._map_list_optional("triggerDataSources", RefView)

    @property
    def throttling_interval(self) -> Optional[int]:
        """Throttling interval in seconds."""
        return self._get_optional("throttlingInterval")


class ConfigRuleForm(JsonObjectForm):
    """Config rule form.

    This is the form you need to fill to register config rule.

    Args:
        name: Config rule name.
        triggers: Non-empty list of enrichment trigger types.
        data_source_uuids: Non-empty data source uuid list associated with enrichers.
        enrichment: Enrichment type.
            Must be `ArtifactAnalysis` or `ExternalDBLookup` type for rule registration.
        is_disabled: Disabled config rule flag.
        trigger_data_source_uuids: Entity/Artifact registrar associated datasource list
        artifact_types: List of artifact types.
            Not-empty for `ArtifactAnalysis` enrichment type.
        entity_types: List of entity types.
            Not-empty for `ExternalDBLookup` enrichment type.
        throttling_interval: Throttling interval in seconds.
            Required for `OnRegistration` trigger type and
            must be minimum 3600 sec.

    Usage:
        >>> import uuid
        >>> from cybsi.api.enrichment import (
        >>>     EnrichmentTypes,
        >>>     EnrichmentTriggerTypes,
        >>>     ConfigRuleForm,
        >>> )
        >>> from cybsi.api.artifact import ArtifactTypes
        >>> rule = ConfigRuleForm(
        >>>     name="test artifact analysis rule",
        >>>     data_source_uuids=[uuid.UUID("3ab411dc-17ab-4169-8ea6-c08271fca49e")],
        >>>     triggers=[EnrichmentTriggerTypes.OnRegistration],
        >>>     enrichment=EnrichmentTypes.ArtifactAnalysis,
        >>>     artifact_types=[ArtifactTypes.FileSample, ArtifactTypes.Archive],
        >>>     is_disabled=True,
        >>> )
    """

    def __init__(
        self,
        name: str,
        triggers: List[EnrichmentTriggerTypes],
        data_source_uuids: List[uuid.UUID],
        enrichment: EnrichmentTypes,
        is_disabled: Optional[bool] = False,
        trigger_data_source_uuids: Optional[List[uuid.UUID]] = None,
        artifact_types: Optional[List[ArtifactTypes]] = None,
        entity_types: Optional[List[ArtifactTypes]] = None,
        throttling_interval: Optional[int] = None,
    ):
        super().__init__()
        self._data["name"] = name
        self._data["isDisabled"] = is_disabled
        self._data["triggers"] = [typ.value for typ in triggers]
        self._data["dataSourceUUIDs"] = [str(u) for u in data_source_uuids]
        if trigger_data_source_uuids is not None:
            self._data["triggerDataSourceUUIDs"] = [
                str(u) for u in trigger_data_source_uuids
            ]
        if artifact_types is not None:
            self._data["artifactTypes"] = [typ.value for typ in artifact_types]
        if entity_types is not None:
            self._data["entityTypes"] = [typ.value for typ in entity_types]
        self._data["enrichment"] = enrichment.value
        if throttling_interval is not None:
            self._data["throttlingInterval"] = throttling_interval
