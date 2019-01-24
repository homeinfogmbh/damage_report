"""WSGI Messages."""

from his import HIS_MESSAGE_FACILITY


__all__ = [
    'NO_SUCH_REPORT',
    'REPORT_TOGGLED',
    'REPORT_DELETED',
    'EMAILS_UPDATED']


DR_MESSAGE_DOMAIN = HIS_MESSAGE_FACILITY.domain('damage_report')
DR_MESSAGE = DR_MESSAGE_DOMAIN.message
NO_SUCH_REPORT = DR_MESSAGE('The requested report does not exist.', status=404)
REPORT_TOGGLED = DR_MESSAGE('The report has been toggled.', status=200)
REPORT_DELETED = DR_MESSAGE('The report has been deleted.', status=200)
EMAILS_UPDATED = DR_MESSAGE('The emails list has benn updated.', status=200)
