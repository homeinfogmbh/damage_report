"""Damage report ORM models."""

from datetime import datetime

from peewee import BooleanField
from peewee import CharField
from peewee import DateTimeField
from peewee import ForeignKeyField
from peewee import TextField

from mdb import Address, Customer
from peeweeplus import MySQLDatabase, JSONModel

from damage_report.config import CONFIG


__all__ = ['DamageReport', 'NotificationEmail']


DATABASE = MySQLDatabase.from_config(CONFIG['db'])


class _DamageReportModel(JSONModel):
    """Basic model for this database."""

    class Meta:     # pylint: disable=C0111
        database = DATABASE
        schema = database.database


class DamageReport(_DamageReportModel):
    """Damage reports."""

    class Meta:     # pylint: disable=C0111
        table_name = 'damage_report'

    customer = ForeignKeyField(Customer, column_name='customer')
    address = ForeignKeyField(Address, column_name='address')
    message = TextField()
    name = CharField(255)
    contact = CharField(255, null=True, default=None)
    damage_type = CharField(255)
    timestamp = DateTimeField(default=datetime.now)
    checked = BooleanField(default=False)

    @classmethod
    def from_json(cls, json, customer, address):
        """Creates a new entry from the respective
        customer, address and dictionary.
        """
        record = super().from_json(json)
        record.customer = customer
        record.address = address
        return record

    def to_json(self, address=True, **kwargs):
        """Returns a JSON-ish dictionary."""
        json = super().to_json(**kwargs)

        if address:
            json['address'] = self.address.to_json()

        return json


class NotificationEmail(_DamageReportModel):
    """Stores emails for notifications about new messages."""

    class Meta:     # pylint: disable=C0111
        table_name = 'notification_emails'

    customer = ForeignKeyField(Customer, column_name='customer')
    email = CharField(255)
    subject = CharField(255, null=True)
    html = BooleanField(default=False)

    @classmethod
    def from_json(cls, json, customer, **kwargs):
        """Creates a notification email for the respective customer."""
        record = super().from_json(json, **kwargs)
        record.customer = customer
        return record
