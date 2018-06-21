"""WSGI Messages."""

from his import Message


class _DamageReportMessage(Message):
    """Abstract base message."""

    DOMAIN = 'damage_report'


class NoSuchReport(_DamageReportMessage):
    """Indicates that the respective damage report does not exist."""

    STATUS = 404


class ReportToggled(_DamageReportMessage):
    """Indicates that the respective damage report was toggled."""

    STATUS = 200


class ReportDeleted(_DamageReportMessage):
    """Indicates that the respective damage report was deleted."""

    STATUS = 200
