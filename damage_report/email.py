"""Emailing of new damage reports."""

from typing import Iterator, Union

from emaillib import EMail
from notificationlib import get_email_func

from damage_report.config import CONFIG
from damage_report.orm import DamageReport, NotificationEmail


__all__ = ['email']


def get_emails(damage_report: Union[DamageReport, int]) -> Iterator[EMail]:
    """Yields notification emails."""

    damage_report = DamageReport.select(cascade=True).where(
        DamageReport.id == damage_report).get()

    for notification_email in NotificationEmail.select().where(
            NotificationEmail.customer == damage_report.customer):
        recipient = notification_email.email
        subject = notification_email.subject or CONFIG['email']['subject']
        subject = subject.format(
            damage_type=damage_report.damage_type,
            address=damage_report.address)
        sender = CONFIG['email']['from']
        message = 'Schadensmeldung "{}" von {} ({}):'.format(
            damage_report.damage_type, damage_report.name,
            damage_report.contact)

        if notification_email.html:
            html = message + '<br/><br/>' + damage_report.message
            plain = None
        else:
            plain = message + '\n\n' + damage_report.message
            html = None

        yield EMail(subject, sender, recipient, plain=plain, html=html)


email = get_email_func(get_emails)  # pylint: disable=C0103
