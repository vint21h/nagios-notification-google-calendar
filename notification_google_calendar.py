#!/usr/bin/env python

# -*- coding: utf-8 -*-

# nagios-notification-google-calendar
# notification_google_calendar.py

# Copyright (c) 2011-2012 Alexei Andrushievich <vint21h@vint21h.pp.ua>
# Notifications via Google Calendar Nagios plugin [https://github.com/vint21h/nagios-notification-google-calendar]
#
# This file is part of nagios-notification-google-calendar.
#
# nagios-notification-google-calendar is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


import sys

try:
    import os
    from optparse import OptionParser
except ImportError, err:
    sys.stderr.write("ERROR: Couldn't load module. %s\n" % err)
    sys.exit(-1)

# metadata
__author__ = "Alexei Andrushievich"
__email__ = "vint21h@vint21h.pp.ua"
__licence__ = "GPLv3 or later"
__description__ = "Notifications via Google Calendar Nagios plugin"
__url__ = "https://github.com/vint21h/nagios-notification-google-calendar"
VERSION = (0, 0, 0)
__version__ = '.'.join(map(str, VERSION))


def parse_cmd_line():
    """
    Commandline options arguments parsing.
    """

    # build options and help
    version = "%%prog %s" % (__version__)
    parser = OptionParser(version=version)
    parser.add_option("-r", "--recipient", action="store", dest="recipient",
                                        type="string", default="",
                                        metavar="RECIPIENT",
                                        help="message recipient")
    parser.add_option("-m", "--message", metavar="MESSAGE", action="store",
                                        type="string", dest="message",
                                        default="", help="message text")
    parser.add_option("-q", "--quiet", metavar="QUIET", action="store_false",
                                        default=False, dest="quiet",
                                        help="be quiet")

    options = parser.parse_args(sys.argv)[0]

    # check mandatory command line options supplied
    mandatories = ["recipient", "message", ]
    if not all(options.__dict__[mandatory] for mandatory in mandatories):
        sys.stdout.write("Mandatory command line option missing\n")
        sys.exit(0)

    return options


if __name__ == "__main__":
    # get options, check and parse config file and send message
    options = parse_cmd_line()
    send_message(parse_config(check_config_file(options.config)), options.recipient, options.message)
