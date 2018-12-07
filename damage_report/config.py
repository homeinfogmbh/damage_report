"""Configuration file parser."""

from configlib import INIParser


__all__ = ['CONFIG']


CONFIG = INIParser('/usr/local/etc/damage_report.conf')
