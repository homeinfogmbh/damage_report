"""Authenticated and authorized HIS services."""

from flask import request

from his import CUSTOMER, authenticated, authorized, admin, Application
from wsgilib import JSON


from damage_report.messages import EMAILS_UPDATED
from damage_report.messages import NO_SUCH_REPORT
from damage_report.messages import REPORT_DELETED
from damage_report.messages import REPORT_TOGGLED
from damage_report.orm import DamageReport, NotificationEmail

__all__ = ['APPLICATION']


APPLICATION = Application('Damage Report', debug=True)


def _get_damage_reports(checked=None):
    """Yields the customer's damage reports."""

    expression = DamageReport.customer == CUSTOMER.id

    if checked is not None:
        expression &= DamageReport.checked == int(checked)

    return DamageReport.select().where(expression)


def _get_checked():
    """Returns the checked flag."""

    checked = request.args.get('checked')

    if checked is None:
        return None

    try:
        checked = int(checked)
    except ValueError:
        return None

    return bool(checked)


def _get_damage_report(ident):
    """Returns the respective damage report."""

    try:
        return DamageReport.get(
            (DamageReport.id == ident)
            & (DamageReport.customer == CUSTOMER.id))
    except DamageReport.DoesNotExist:
        raise NO_SUCH_REPORT


@authenticated
@authorized('damage_report')
def list_reports():
    """Lists the damage reports."""

    return JSON([
        damage_report.to_json() for damage_report
        in _get_damage_reports(_get_checked())])


@authenticated
@authorized('damage_report')
def get_report(ident):
    """Returns the respective damage report."""

    return JSON(_get_damage_report(ident).to_json())


@authenticated
@authorized('damage_report')
def toggle_report(ident):
    """Toggles the respective damage report."""

    damage_report = _get_damage_report(ident)
    damage_report.checked = not damage_report.checked
    damage_report.save()
    return REPORT_TOGGLED.update(checked=damage_report.checked)


@authenticated
@authorized('damage_report')
def delete_report(ident):
    """Deletes the respective damage report."""

    damage_report = _get_damage_report(ident)
    damage_report.delete_instance()
    return REPORT_DELETED


@authenticated
@authorized('tenant2tenant')
def get_emails():
    """Deletes the respective message."""

    return JSON([email.to_json() for email in NotificationEmail.select().where(
        NotificationEmail.customer == CUSTOMER.id)])


@authenticated
@authorized('tenant2tenant')
@admin
def set_emails():
    """Replaces all email address of the respective customer."""

    emails = request.json
    ids = []

    for email in NotificationEmail.select().where(
            NotificationEmail.customer == CUSTOMER.id):
        email.delete_instance()

    for email in emails:
        email = NotificationEmail.from_json(email, CUSTOMER.id)
        email.save()
        ids.append(email.id)

    return EMAILS_UPDATED.update(ids=ids)


ROUTES = (
    ('GET', '/report', list_reports, 'list_reports'),
    ('GET', '/report/<int:ident>', get_report, 'get_report'),
    ('PATCH', '/report/<int:ident>', toggle_report, 'toggle_report'),
    ('DELETE', '/report/<int:ident>', delete_report, 'delete_report'),
    ('GET', '/email', get_emails, 'get_emails'),
    ('POST', '/email', set_emails, 'set_emails'))
APPLICATION.add_routes(ROUTES)
