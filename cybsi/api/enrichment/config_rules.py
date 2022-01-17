"""Use this section of API to operate config rules.
"""
import uuid
from typing import Any, List, Optional

from .. import RefView, Tag
from ..api import Nullable, _unwrap_nullable
from ..artifact import ArtifactTypes
from ..internal import BaseAPI, JsonObject, JsonObjectForm
from ..observable import EntityTypes
from ..pagination import Cursor, Page
from ..view import _TaggedRefView
from .enums import EnrichmentTriggerTypes, EnrichmentTypes


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
        return ConfigRuleView(r)

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

    def filter(
        self,
        data_source_uuid: Optional[uuid.UUID] = None,
        trigger_data_source_uuid: Optional[uuid.UUID] = None,
        cursor: Optional[Cursor] = None,
        limit: Optional[int] = None,
    ) -> Page["ConfigRuleCommonView"]:
        """Filter config rules.

        Note:
            Calls `GET /enrichment/config/rules`.
        Args:
            data_source_uuid: Data source identifier.
                Filter config rules by the associated data source.
            trigger_data_source_uuid: Data source identifier.
                Filter config rules by the data source which is the trigger for rules.
            cursor: Page cursor.
            limit: Page limit.
        Returns:
            Page of config rules.
        Raises:
            :class:`~cybsi.api.error.SemanticError`: query arguments contain errors.
        Note:
            Semantic error codes specific for this method:
              * :attr:`~cybsi.api.error.SemanticErrorCodes.DataSourceNotFound`
        """

        params: JsonObject = {}
        if data_source_uuid is not None:
            params["dataSourceUUID"] = data_source_uuid
        if trigger_data_source_uuid is not None:
            params["triggerDataSourceUUID"] = trigger_data_source_uuid
        if limit is not None:
            params["limit"] = limit
        if cursor is not None:
            params["cursor"] = cursor

        resp = self._connector.do_get(self._path, params=params)
        page = Page(self._connector.do_get, resp, ConfigRuleCommonView)
        return page

    def edit(
        self,
        rule_uuid: uuid.UUID,
        tag: Tag,
        name: Optional[str] = None,
        is_disabled: Optional[bool] = None,
        triggers: Optional[List[EnrichmentTriggerTypes]] = None,
        trigger_data_source_uuids: Nullable[List[uuid.UUID]] = None,
        artifact_types: Nullable[List[ArtifactTypes]] = None,
        entity_types: Nullable[List[EntityTypes]] = None,
        data_source_uuids: Optional[List[uuid.UUID]] = None,
        throttling_interval: Nullable[int] = None,
        enrichment: Optional[EnrichmentTypes] = None,
    ) -> None:
        """Edit config rule.

        Note:
            Calls `PATCH /enrichment/config/rules/{rule_uuid}`.
        Args:
            rule_uuid: config rule identifier.
            tag: :attr:ConfigRuleView`.tag` value. Use :meth:`view` to retrieve it.
            name: Config rule name.
            triggers: Non-empty list of enrichment trigger types.
            data_source_uuids:
                Non-empty data source uuid list associated with enrichers.
            enrichment: Enrichment type.
                Must be `ArtifactAnalysis` or `ExternalDBLookup`
                type for rule registration.
            is_disabled: Disabled config rule flag.
            trigger_data_source_uuids:
                Entity/Artifact registrar associated datasource list
            artifact_types: List of artifact types.
                Not-empty for `ArtifactAnalysis` enrichment type.
            entity_types: List of entity types.
                Not-empty for `ExternalDBLookup` enrichment type.
            throttling_interval: Throttling interval in seconds.
                Required for `OnRegistration` trigger type and
                must be minimum 3600 sec.
        Raises:
            :class:`~cybsi.api.error.SemanticError`: Query arguments contain errors.
            :class:`~cybsi.api.error.InvalidRequestError`:
                Provided arguments have invalid values.
            :class:`~cybsi.api.error.NotFoundError`: Config rule not found.
            :class:`~cybsi.api.error.ResourceModifiedError`:
                Config rule changed since last request. Retry using updated tag.
        Note:
            Semantic error codes specific for this method:
              * :attr:`~cybsi.api.error.SemanticErrorCodes.DataSourceNotFound`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.MisconfiguredDataSource`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.InvalidRule`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.ImmutableValue`
        """
        data = _create_rule_form_data(
            name=name,
            is_disabled=is_disabled,
            triggers=triggers,
            trigger_data_source_uuids=trigger_data_source_uuids,
            data_source_uuids=data_source_uuids,
            artifact_types=artifact_types,
            entity_types=entity_types,
            throttling_interval=throttling_interval,
            enrichment=enrichment,
        )
        path = f"{self._path}/{rule_uuid}"
        self._connector.do_patch(path=path, tag=tag, json=data)


class ConfigRuleCommonView(RefView):
    """Config rule object view."""

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


class ConfigRuleView(_TaggedRefView, ConfigRuleCommonView):
    """Config rule response view."""

    pass


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
        entity_types: Optional[List[EntityTypes]] = None,
        throttling_interval: Optional[int] = None,
    ):
        data = _create_rule_form_data(
            name=name,
            triggers=triggers,
            data_source_uuids=data_source_uuids,
            enrichment=enrichment,
            is_disabled=is_disabled,
            trigger_data_source_uuids=trigger_data_source_uuids,
            artifact_types=artifact_types,
            entity_types=entity_types,
            throttling_interval=throttling_interval,
        )
        super().__init__(data)


def _create_rule_form_data(
    name: Optional[str],
    is_disabled: Optional[bool] = None,
    triggers: Optional[List[EnrichmentTriggerTypes]] = None,
    trigger_data_source_uuids: Nullable[List[uuid.UUID]] = None,
    artifact_types: Nullable[List[ArtifactTypes]] = None,
    entity_types: Nullable[List[EntityTypes]] = None,
    data_source_uuids: Optional[List[uuid.UUID]] = None,
    throttling_interval: Nullable[int] = None,
    enrichment: Optional[EnrichmentTypes] = None,
) -> JsonObject:
    """Create rule form data"""

    data: JsonObject = dict()

    if name is not None:
        data["name"] = name
    if is_disabled is not None:
        data["isDisabled"] = is_disabled
    if triggers is not None:
        data["triggers"] = [typ.value for typ in triggers]
    if data_source_uuids is not None:
        data["dataSourceUUIDs"] = [str(u) for u in data_source_uuids]
    if enrichment is not None:
        data["enrichment"] = enrichment.value
    if throttling_interval is not None:
        data["throttlingInterval"] = _unwrap_nullable(throttling_interval)

    if entity_types is not None:
        casted_ent_types: Any = _unwrap_nullable(entity_types)
        if casted_ent_types is not None:
            casted_ent_types = [typ.value for typ in casted_ent_types]
        data["entityTypes"] = casted_ent_types

    if trigger_data_source_uuids is None:
        casted_trigger_uuids = _unwrap_nullable(trigger_data_source_uuids)
        if casted_trigger_uuids is not None:
            casted_trigger_uuids = [str(u) for u in casted_trigger_uuids]
        data["triggerDataSourceUUIDs"] = casted_trigger_uuids

    if artifact_types is not None:
        casted_artifact_types: Any = _unwrap_nullable(artifact_types)
        if casted_artifact_types is not None:
            casted_artifact_types = [typ.value for typ in casted_artifact_types]
        data["artifactTypes"] = casted_artifact_types

    return data
