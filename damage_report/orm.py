"""Damage report ORM models."""

from __future__ import annotations
from datetime import datetime

from peewee import BooleanField
from peewee import DateTimeField
from peewee import ForeignKeyField
from peewee import ModelSelect

from filedb import File
from mdb import Address, Company, Customer
from notificationlib import get_email_orm_model
from peeweeplus import HTMLCharField, HTMLTextField, MySQLDatabase, JSONModel

from damage_report.config import CONFIG


__all__ = ['DamageReport', 'Attachment', 'NotificationEmail']


DATABASE = MySQLDatabase.from_config(CONFIG['db'])


class _DamageReportModel(JSONModel):    # pylint: disable=R0903
    """Basic model for this database."""

    class Meta:     # pylint: disable=C0111,R0903
        database = DATABASE
        schema = database.database


class DamageReport(_DamageReportModel):
    """Damage reports."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'damage_report'

    customer = ForeignKeyField(
        Customer, column_name='customer', lazy_load=False)
    address = ForeignKeyField(Address, column_name='address', lazy_load=False)
    message = HTMLTextField()
    name = HTMLCharField(255)
    contact = HTMLCharField(255, null=True, default=None)
    damage_type = HTMLCharField(255)
    annotation = HTMLTextField(null=True)
    timestamp = DateTimeField(default=datetime.now)
    checked = BooleanField(default=False)

    @classmethod
    def from_json(cls, json: dict, customer: Customer, address: Address,
                  **kwargs) -> DamageReport:
        """Creates a new entry from the respective
        customer, address and dictionary.
        """
        record = super().from_json(json, **kwargs)
        record.customer = customer
        record.address = address
        return record

    @classmethod
    def select(cls, *args, cascade: bool = False, **kwargs) -> ModelSelect:
        """Selects damage reports."""
        if not cascade:
            return super().select(*args, **kwargs)

        args = {cls, Customer, Company, Address, *args}
        return super().select(*args).join(Customer).join(Company).join_from(
            cls, Address)

    def to_json(self, *, address: bool = True, attachments: bool = False,
                **kwargs) -> dict:
        """Returns a JSON-ish dictionary."""
        json = super().to_json(**kwargs)

        if address:
            json['address'] = self.address.to_json()

        if attachments:
            json['attachments'] = [
                attachment.to_json(skip={'damageReport'})
                for attachment in self.attachments
            ]

        return json


class Attachment(_DamageReportModel):   # pylint: disable=R0903
    """Attachment to a damage report."""

    damage_report = ForeignKeyField(
        DamageReport, column_name='damage_report', backref='attachments',
        on_delete='CASCADE', lazy_load=False)
    file = ForeignKeyField(File, column_name='file')


NotificationEmail = get_email_orm_model(_DamageReportModel)
