"""Miscellaneous functions."""

from typing import Union

from peewee import ModelSelect

from mdb import Customer
from wsgilib import JSONMessage

from damage_report.orm import Attachment, DamageReport


__all__ = ['get_damage_reports', 'get_damage_report', 'get_attachment']


def get_attachment(ident: int, customer: Union[Customer, int]) -> Attachment:
    """Returns the respective attachment."""

    condition = Attachment.id == ident
    condition &= DamageReport.customer == customer

    try:
        return Attachment.select(cascade=True).where(condition).get()
    except Attachment.DoesNotExist:
        raise JSONMessage('No such attachment.', status=404) from None


def get_damage_report(
        ident: int,
        customer: Union[Customer, int]
) -> DamageReport:
    """Returns the respective damage report."""

    condition = DamageReport.id == ident
    condition &= DamageReport.customer == customer

    try:
        return DamageReport.select(cascade=True).where(condition).get()
    except DamageReport.DoesNotExist:
        raise JSONMessage('No such report.', status=404) from None


def get_damage_reports(
        customer: Union[Customer, int],
        *,
        checked: bool = None
) -> ModelSelect:
    """Yields the customer's damage reports."""

    expression = DamageReport.customer == customer

    if checked is not None:
        expression &= DamageReport.checked == int(checked)

    return DamageReport.select(cascade=True).where(expression)
