"""Authenticated and authorized HIS services."""

from contextlib import suppress
from datetime import datetime

from flask import request

from his import CUSTOMER, authenticated, authorized, Application
from his.messages import NotAnInteger
from terminallib import Terminal
from timelib import DATE_FORMAT, DATETIME_BASE, DATETIME_FORMAT
from wsgilib import JSON

from cleaninglog.messages import NoSuchUser, NoSuchTerminal, TerminalUnlocated
from digsigdb import CleaningUser, CleaningDate

__all__ = ['APPLICATION']


APPLICATION = Application('Damage Report', cors=True, debug=True)
SHORT_TIME_FORMAT = '%H:%M'
DATETIME_FORMATS = (
    DATE_FORMAT, DATETIME_FORMAT, SHORT_TIME_FORMAT,
    DATETIME_BASE.format(DATE_FORMAT, SHORT_TIME_FORMAT))


def _parse_datetime(string):
    """Parses a datetime from the given string."""

    if string is None:
        return None

    for date_format in DATETIME_FORMATS:
        with suppress(ValueError):
            return datetime.strptime(string, date_format)

    raise ValueError('Invalid datetime or time format: {}'.format(string))


def _cleaning_user_selects():
    """Returns a basic expression for cleaning users selection."""

    return (
        (CleaningUser.created < datetime.now())
        & (CleaningUser.enabled == 1))


def _users():
    """Yields the customer's users."""

    return CleaningUser.select().where(
        (CleaningUser.customer == CUSTOMER.id) & _cleaning_user_selects())


def _user(ident):
    """Returns the respective user."""

    try:
        return CleaningUser.select().where(
            (CleaningUser.id == ident)
            & (CleaningUser.customer == CUSTOMER.id)
            & _cleaning_user_selects()).get()
    except CleaningUser.DoesNotExist:
        raise NoSuchUser()


def _terminal(tid):
    """Returns the respective terminal."""

    try:
        return Terminal.select().where(
            (Terminal.tid == tid) & (Terminal.customer == CUSTOMER.id)).get()
    except Terminal.DoesNotExist:
        raise NoSuchTerminal()


def _address(terminal):
    """Returns the terminal's address."""

    try:
        return terminal.location.address
    except AttributeError:
        return TerminalUnlocated()


def _entries(start, end, user=None, address=None):
    """Yields the respective customer's entries."""

    if user is None:
        expression = CleaningDate.user << [user.id for user in _users()]
    else:
        expression = CleaningDate.user == user

    if address is not None:
        expression &= CleaningDate.address == address

    if start is not None:
        expression &= CleaningDate.timestamp >= start

    if end is not None:
        expression &= CleaningDate.timestamp <= end

    return CleaningDate.select().where(expression)


@authenticated
@authorized('cleaninglog')
def list_users():
    """Lists the cleaning log users of the respective customer."""

    return JSON([user.to_dict() for user in _users()])


@authenticated
@authorized('cleaninglog')
def list_entries():
    """Lists the cleaning log entries of the respective customer."""

    start = _parse_datetime(request.args.get('from'))
    end = _parse_datetime(request.args.get('until'))

    try:
        user = int(request.args['user'])
    except KeyError:
        user = None
    except (ValueError, TypeError):
        return NotAnInteger()
    else:
        user = _user(user)

    try:
        tid = int(request.args['terminal'])
    except KeyError:
        address = None
    except (ValueError, TypeError):
        return NotAnInteger()
    else:
        address = _address(_terminal(tid))

    entries = _entries(start, end, user=user, address=address)
    return JSON([entry.to_dict() for entry in entries])


ROUTES = (
    ('GET', '/', list_entries, 'list_entries'),
    ('GET', '/users', list_users, 'list_users'))
APPLICATION.add_routes(ROUTES)
