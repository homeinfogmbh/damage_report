"""Damage report ORM models."""

from datetime import datetime

from peewee import BooleanField
from peewee import CharField
from peewee import DateTimeField
from peewee import ForeignKeyField
from peewee import TextField

from filedb import File
from hwdb import Deployment
from mdb import Address, Customer
from notificationlib import get_email_orm_model
from peeweeplus import MySQLDatabase, JSONModel

from damage_report.config import CONFIG


__all__ = ['DamageReport', 'Attachment', 'NotificationEmail']


DATABASE = MySQLDatabase.from_config(CONFIG['db'])


class _DamageReportModel(JSONModel):
    """Basic model for this database."""

    class Meta:     # pylint: disable=C0111,R0903
        database = DATABASE
        schema = database.database


class DamageReport(_DamageReportModel):
    """Damage reports."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'damage_report'

    customer = ForeignKeyField(Customer, column_name='customer')
    address = ForeignKeyField(Address, column_name='address')
    deployment = ForeignKeyField(
        Deployment, column_name='deployment', null=True, on_delete='SET NULL')
    message = TextField()
    name = CharField(255)
    contact = CharField(255, null=True, default=None)
    damage_type = CharField(255)
    timestamp = DateTimeField(default=datetime.now)
    checked = BooleanField(default=False)

    @classmethod
    def from_json(cls, json, customer, address, **kwargs):
        """Creates a new entry from the respective
        customer, address and dictionary.
        """
        record = super().from_json(json, **kwargs)
        record.customer = customer
        record.address = address
        return record

    def to_json(self, deployment=False, submitter=False, **kwargs):
        """Returns a JSON-ish dictionary."""
        json = super().to_json(**kwargs)

        if deployment and self.deployment:
            json['deployment'] = self.deployment.to_json()

        if submitter and self.submitter:
            json['submitter'] = self.submitter.to_json()

        return json


class Attachment(_DamageReportModel):
    """Attachment to a damage report."""

    damage_report = ForeignKeyField(
        DamageReport, column_name='damage_report', backref='attachments',
        on_delete='CASCADE')
    file = ForeignKeyField(File, column_name='file')


NotificationEmail = get_email_orm_model(_DamageReportModel)
