"""WSGI Messages."""

from his import Message


class _CleaningLogMessage(Message):
    """Abstract base message."""

    DOMAIN = 'damage_report'


class NoSuchReport(_CleaningLogMessage):
    """Indicates that the respective terminal does not exist."""

    STATUS = 404


class ReportToggled(_CleaningLogMessage):
    """Indicates that the respective user does not exist."""

    STATUS = 200


class ReportDeleted(_CleaningLogMessage):
    """Indicates that the respective terminal has no location assigned."""

    STATUS = 200
