from ..internal import BaseAPI

from .task_queue import TaskQueueAPI
from .config_rules import ConfigRulesAPI
from .external_dbs import ExternalDBsAPI


class EnrichmentAPI(BaseAPI):
    """Enrichment API."""

    @property
    def config_rules(self) -> "ConfigRulesAPI":
        """Get config rules route."""
        return ConfigRulesAPI(self._connector)

    @property
    def task_queue(self) -> "TaskQueueAPI":
        """Get task queue route."""
        return TaskQueueAPI(self._connector)

    @property
    def external_dbs(self) -> "ExternalDBsAPI":
        """Get external databases route."""
        return ExternalDBsAPI(self._connector)
