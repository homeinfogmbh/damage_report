"""Authenticated and authorized HIS services."""

from flask import request

from his import CUSTOMER, authenticated, authorized, Application
from notificationlib import get_wsgi_funcs
from wsgilib import Binary, JSON

from damage_report.messages import NO_SUCH_ATTACHMENT
from damage_report.messages import NO_SUCH_REPORT
from damage_report.messages import REPORT_DELETED
from damage_report.messages import REPORT_PATCHED
from damage_report.orm import Attachment, DamageReport, NotificationEmail


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

    condition = DamageReport.id == ident
    condition &= DamageReport.customer == CUSTOMER.id

    try:
        return DamageReport.get(condition)
    except DamageReport.DoesNotExist:
        raise NO_SUCH_REPORT from None


def _get_attachment(ident):
    """Returns the respective attachment."""

    condition = Attachment.id == ident
    condition &= DamageReport.customer == CUSTOMER.id

    try:
        return Attachment.select().join(DamageReport).where(condition).get()
    except Attachment.DoesNotExist:
        raise NO_SUCH_ATTACHMENT from None


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
def patch_report(ident):
    """patches the respective damage report."""

    damage_report = _get_damage_report(ident)
    damage_report.patch_json(request.json)
    damage_report.save()
    return REPORT_PATCHED


@authenticated
@authorized('damage_report')
def delete_report(ident):
    """Deletes the respective damage report."""

    damage_report = _get_damage_report(ident)
    damage_report.delete_instance()
    return REPORT_DELETED


@authenticated
@authorized('damage_report')
def get_attachment(ident):
    """Returns the respective attachment."""

    attachment = get_attachment(ident)
    return Binary(attachment.file.bytes)


GET_EMAILS, SET_EMAILS = get_wsgi_funcs('damage_report', NotificationEmail)


ROUTES = (
    ('GET', '/report', list_reports),
    ('GET', '/report/<int:ident>', get_report),
    ('PATCH', '/report/<int:ident>', patch_report),
    ('DELETE', '/report/<int:ident>', delete_report),
    ('GET', '/attachment/<int:ident>', get_attachment),
    ('GET', '/email', GET_EMAILS),
    ('POST', '/email', SET_EMAILS)
)
APPLICATION.add_routes(ROUTES)
