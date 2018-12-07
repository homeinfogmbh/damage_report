"""Configuration file parser."""

from configlib import loadcfg


__all__ = ['CONFIG']


CONFIG = loadcfg('damage_report.conf')
