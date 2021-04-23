"""Authenticated and authorized HIS services."""

from flask import request

from his import CUSTOMER, authenticated, authorized, Application
from notificationlib import get_wsgi_funcs
from wsgilib import Binary, JSON, JSONMessage, get_bool

from damage_report.functions import get_attachment
from damage_report.functions import get_damage_report
from damage_report.functions import get_damage_reports
from damage_report.orm import NotificationEmail


__all__ = ['APPLICATION']


APPLICATION = Application('Damage Report', debug=True)


@authenticated
@authorized('damage_report')
def list_reports() -> JSON:
    """Lists the damage reports."""

    address = get_bool('address', True)
    attachments = get_bool('attachments')
    checked = get_bool('checked')
    return JSON([
        damage_report.to_json(address=address, attachments=attachments)
        for damage_report in get_damage_reports(CUSTOMER.id, checked=checked)])


@authenticated
@authorized('damage_report')
def get_report(ident: int) -> JSON:
    """Returns the respective damage report."""

    address = get_bool('address', True)
    attachments = get_bool('attachments')
    return JSON(get_damage_report(ident, CUSTOMER.id).to_json(
        address=address, attachments=attachments))


@authenticated
@authorized('damage_report')
def patch_report(ident: int) -> JSONMessage:
    """patches the respective damage report."""

    damage_report = get_damage_report(ident, CUSTOMER.id)
    damage_report.patch_json(request.json)
    damage_report.save()
    return JSONMessage('The report has been patched.', status=200)


@authenticated
@authorized('damage_report')
def delete_report(ident: int) -> JSONMessage:
    """Deletes the respective damage report."""

    damage_report = get_damage_report(ident, CUSTOMER.id)
    damage_report.delete_instance()
    return JSONMessage('The report has been deleted.', status=200)


@authenticated
@authorized('damage_report')
def get_attachment_(ident: int) -> JSONMessage:
    """Returns the respective attachment."""

    return Binary(get_attachment(ident, CUSTOMER.id).file.bytes)


GET_EMAILS, SET_EMAILS = get_wsgi_funcs('damage_report', NotificationEmail)


ROUTES = (
    ('GET', '/report', list_reports),
    ('GET', '/report/<int:ident>', get_report),
    ('PATCH', '/report/<int:ident>', patch_report),
    ('DELETE', '/report/<int:ident>', delete_report),
    ('GET', '/attachment/<int:ident>', get_attachment_),
    ('GET', '/email', GET_EMAILS),
    ('POST', '/email', SET_EMAILS)
)
APPLICATION.add_routes(ROUTES)
