"""WSGI Messages."""

from wsgilib import JSONMessage


__all__ = [
    'NO_SUCH_REPORT',
    'REPORT_TOGGLED',
    'REPORT_DELETED',
    'EMAILS_UPDATED']


NO_SUCH_REPORT = JSONMessage(
    'The requested report does not exist.', status=404)
REPORT_TOGGLED = JSONMessage('The report has been toggled.', status=200)
REPORT_DELETED = JSONMessage('The report has been deleted.', status=200)
EMAILS_UPDATED = JSONMessage('The emails list has benn updated.', status=200)
