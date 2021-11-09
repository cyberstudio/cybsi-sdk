import uuid

from ..common import RefView
from ..internal import BaseAPI, JsonObjectForm
from ..observable import ShareLevels


class ReportsAPI(BaseAPI):
    """Report API."""
    _path = '/enrichment/reports'

    def register(self, report: 'ReportForm') -> RefView:
        """Register report.

        Note:
            Calls `POST /enrichment/reports`.
        Args:
            report: Filled report form.
        Returns:
            Reference to the registered report.
        """
        raise NotImplementedError()

    def view(self, report_uuid: uuid.UUID) -> 'ReportView':
        """Get report view.

        Note:
            Calls `GET /enrichment/reports/{report_uuid}`.
        Args:
            report_uuid: Report uuid.
        Returns:
            View of the report.
        """
        path = f'{self._path}/{report_uuid}'
        r = self._connector.do_get(path)
        return ReportView(r.json())


class ReportForm(JsonObjectForm):
    """Report form.

    Args:
        share_level: Report share level.
    """
    def __init__(self, share_level: ShareLevels):
        super().__init__()
        self._data['shareLevel'] = str(share_level)

    def add_observation(self, observation_uuid: uuid.UUID) -> 'ReportForm':
        """Add observation to report."""
        observations = self._data.setdefault('observations', [])
        observations.append(str(observation_uuid))
        return self


class ReportView(RefView):
    """Report view.

    TODO:
        Implement.
    """
