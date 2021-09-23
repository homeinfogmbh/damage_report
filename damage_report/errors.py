"""Common errors."""

from wsgilib import JSONMessage

from damage_report.orm import Attachment, DamageReport


__all__ = ['ERRORS']


ERRORS = {
    Attachment.DoesNotExist: lambda _: JSONMessage(
        'No such attachment.', status=404),
    DamageReport.DoesNotExist: lambda _: JSONMessage(
        'No such damage report.', status=404)
}
