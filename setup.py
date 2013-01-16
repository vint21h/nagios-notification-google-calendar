#!/usr/bin/env python
# -*- coding: utf-8 -*-

# nagios-notification-google-calendar
# setup.py

from setuptools import setup, find_packages

from notification_jabber import (
    __author__,
    __email__,
    __version__,
    __licence__,
    __description__,
    __url__,
)

SHARED_FILES = ['README.rst', 'COPYING', 'CHANGELOG', 'INSTALL', 'TODO', ]

setup(
    name = "nagios_notification_google_calendar",
    version = __version__,
    packages = find_packages(),
    scripts = ['notification_google_calendar.py', ],
    install_requires = ['docutils', ],
    package_data = {
        '': (SHARED_FILES, ),
    },
    data_files = [
            ('/usr/share/doc/nagios-notification-google-calendar/', SHARED_FILES),
    ],
    author = __author__,
    author_email = __email__,
    description = __description__,
    long_description = open('README.rst').read(),
    license = __licence__,
    url = __url__,
    zip_safe = False,
    include_package_data = True,
)
