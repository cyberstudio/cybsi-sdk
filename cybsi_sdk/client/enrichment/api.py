from ..internal import BaseAPI

from .task_queue import TaskQueueAPI


class EnrichmentAPI(BaseAPI):
    """Enrichment API."""
    @property
    def task_queue(self) -> 'TaskQueueAPI':
        """Get task queue route."""
        return TaskQueueAPI(self._connector)
