#! /usr/bin/env python3

from setuptools import setup


setup(
    name="damage_report",
    use_scm_version={"local_scheme": "node-and-timestamp"},
    setup_requires=["setuptools_scm"],
    author="HOMEINFO - Digitale Informationssysteme GmbH",
    author_email="<info at homeinfo dot de>",
    maintainer="Richard Neumann",
    maintainer_email="<r dot neumann at homeinfo period de>",
    install_requires=[
        "configlib",
        "emaillib",
        "filedb",
        "flask",
        "his",
        "mdb",
        "notificationlib",
        "peewee",
        "peeweeplus",
    ],
    packages=["damage_report"],
    description="HIS microservice to handle damage reports.",
)
