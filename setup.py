#!/usr/bin/env python
# -*- coding: utf-8 -*-

# nagios-notification-google-calendar
# setup.py

from setuptools import setup, find_packages

# metadata
VERSION = (0, 2, 1)
__version__ = '.'.join(map(str, VERSION))

DATA = ['README.rst', 'COPYING', 'notification_google_calendar.ini', ]

setup(
    name="nagios-notification-google-calendar",
    version=__version__,
    packages=find_packages(),
    scripts=['notification_google_calendar.py', ],
    install_requires=['httplib2 == 0.7.7', 'oauth2client == 1.0', 'google-api-python-client == 1.0', ],
    package_data={
        'nagios-notification-google-calendar': DATA,
    },
    data_files=[
        ('share/doc/nagios-notification-google-calendar/', DATA),
    ],
    author="Alexei Andrushievich",
    author_email="vint21h@vint21h.pp.ua",
    description="Notifications via Google Calendar Nagios plugin",
    long_description=open('README.rst').read(),
    license="GPLv3 or later",
    url="https://github.com/vint21h/nagios-notification-google-calendar",
    download_url="https://github.com/vint21h/nagios-notification-google-calendar/archive/%s.tar.gz" % __version__,
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        "Environment :: Console",
        "Environment :: Plugins",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: Unix",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: System :: Monitoring",
        "Topic :: Utilities",
    ]
)
