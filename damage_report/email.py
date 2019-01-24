"""Emailing of new damage reports."""

from emaillib import EMail, Mailer
from functoolsplus import coerce

from damage_report.config import CONFIG
from damage_report.orm import NotificationEmail


__all__ = ['email']


MAILER = Mailer.from_config(CONFIG['email'])


@coerce(frozenset)
def get_emails(damage_report):
    """Yields notification emails."""

    for notification_email in NotificationEmail.select().where(
            NotificationEmail.customer == damage_report.customer):
        recipient = notification_email.email
        subject = notification_email.subject or CONFIG['email']['subject']
        address = damage_report.address
        subject = subject.format(
            damage_report.damage_type, address.street, address.house_number)
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


def email(damage_report):
    """Sends notifications emails."""

    emails = get_emails(damage_report)

    if emails:  # pylint: disable=W0125
        return MAILER.send(emails)

    return None
