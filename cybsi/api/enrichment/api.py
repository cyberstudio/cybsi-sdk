from ..internal import BaseAPI

from .task_queue import TaskQueueAPI
from .config_rules import ConfigRulesAPI


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
