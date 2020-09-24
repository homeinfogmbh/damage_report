"""WSGI Messages."""

from wsgilib import JSONMessage


__all__ = [
    'NO_SUCH_ATTACHMENT',
    'NO_SUCH_REPORT',
    'REPORT_PATCHED',
    'REPORT_DELETED'
]


NO_SUCH_ATTACHMENT = JSONMessage('No such attachment.', status=404)
NO_SUCH_REPORT = JSONMessage('No such report.', status=404)
REPORT_PATCHED = JSONMessage('The report has been patched.', status=200)
REPORT_DELETED = JSONMessage('The report has been deleted.', status=200)
