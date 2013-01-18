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
    import ConfigParser
    import datetime
    import httplib2
    from oauth2client.client import flow_from_clientsecrets
    from oauth2client.file import Storage
    from apiclient.discovery import build
except ImportError, err:
    sys.stderr.write("ERROR: Couldn't load module. %s\n" % err)
    sys.exit(-1)


# metadata
__author__ = "Alexei Andrushievich"
__email__ = "vint21h@vint21h.pp.ua"
__licence__ = "GPLv3 or later"
__description__ = "Notifications via Google Calendar Nagios plugin"
__url__ = "https://github.com/vint21h/nagios-notification-google-calendar"
VERSION = (0, 0, 2)
__version__ = '.'.join(map(str, VERSION))


# global variables
SCOPE = 'https://www.googleapis.com/auth/calendar'


def parse_cmd_line():
    """
    Commandline options arguments parsing.
    """

    # build options and help
    version = "%%prog %s" % __version__
    parser = OptionParser(version=version)
    parser.add_option("-u", "--username", action="store", dest="username",
                                        type="string", default="",
                                        metavar="RECIPIENT",
                                        help="user")
    parser.add_option("-C", "--calendar", metavar="CALENDAR", action="store",
                                        type="string", dest="calendar",
                                        default="", help="google calendar id")
    parser.add_option("-m", "--message", metavar="MESSAGE", action="store",
                                        type="string", dest="message",
                                        default="", help="message text")
    parser.add_option("-c", "--config", metavar="CONFIG", action="store",
                                        type="string", dest="config",
                                        help="path to config file",
                                        default="notification_google_calendar.ini")
    parser.add_option("-q", "--quiet", metavar="QUIET", action="store_true",
                                        default=False, dest="quiet",
                                        help="be quiet")
    parser.add_option("-g", "--get-google-credentials", metavar="GET-GOOGLE-CREDENTIALS",
                                        action="store_true", default=False,
                                        dest="get_google_credentials",
                                        help="get google API credentials for user")

    options = parser.parse_args(sys.argv)[0]

    mandatories = ["username", ]
    # check mandatory command line options supplied
    if not options.get_google_credentials:
        mandatories.append("calendar")  # set calendar option required when sending message
        mandatories.append("message")  # set message option required when sending message
    if not all(options.__dict__[mandatory] for mandatory in mandatories):
        sys.stdout.write(u"Mandatory command line option missing\n")
        sys.exit(0)

    return options


def check_config_file(ini):
    """
    Check config exist.
    """

    default_ini = "notification_google_calendar.ini"
    if ini and os.path.exists(ini):  # user config file path
        return ini
    elif os.path.exists(os.path.join("/etc", default_ini)):  # default config file path in /etc
        return os.path.join("/etc", default_ini)
    else:
        sys.stderr.write(u"ERROR: Config file %s don't exist\n" % ini)
        sys.exit(0)


def parse_config(configini):
    """
    Get settings from config file.
    """

    config = ConfigParser.ConfigParser()
    try:
        config.read(configini)
    except Exception:
        sys.stderr.write(u"ERROR: Config file read %s error." % configini)
        sys.exit(-1)

    try:
        configdata = {
            'secrets': config.get('GOOGLE', 'secrets'),
            'credentials': config.get('nagios-notification-google-calendar', 'credentials'),
            'start': config.get('nagios-notification-google-calendar', 'start'),
            'end': config.get('nagios-notification-google-calendar', 'end'),
            'message': config.get('nagios-notification-google-calendar', 'message'),
        }
    except ConfigParser.NoOptionError, err:
        sys.stderr.write(u"ERROR: Config file missing option error. %s\n" % err)
        sys.exit(-1)

    # check mandatory config options supplied
    mandatories = ["secrets", "credentials", "start", "end", "message", ]
    if not all(configdata[mandatory] for mandatory in mandatories):
        sys.stdout.write(u"Mandatory config option missing\n")
        sys.exit(0)

    return configdata


def get_google_credentials(options, config):
    """
    Get google API credentials for user.
    """

    try:
        if options.get_google_credentials:

            flow = flow_from_clientsecrets(config['secrets'], scope=SCOPE, redirect_uri="oob")
            sys.stdout.write(u'Follow this URL: %s and grant plugin access to calendar.\n' % flow.step1_get_authorize_url())
            token = raw_input(u'Enter token:')
            credentials = flow.step2_exchange(token)
            storage = Storage(os.path.join(config['credentials'], '%s.json' % options.username))
            storage.put(credentials)
            credentials.set_store(storage)

        else:
            storage = Storage(os.path.join(config['credentials'], '%s.json' % options.username))
            credentials = storage.get()
    except Exception, err:
        sys.stderr.write(u"ERROR: Getting google API credentials error. %s\n" % err)
        sys.exit(-1)

    return credentials


def create_event_datetimes(config):
    """
    Create event start and end datetimes.
    """

    DT_FORMAT = '%Y-%m-%dT%H:%M:00.000+02:00'

    now = datetime.datetime.now()

    return {
        'start': {
            'dateTime': (now + datetime.timedelta(minutes=int(config['start']))).strftime(DT_FORMAT),
        },
        'end': {
            'dateTime': (now + datetime.timedelta(minutes=int(config['end']))).strftime(DT_FORMAT),
        },
    }


def create_event(options, config, credentials):
    """
    Create event in calendar with sms reminder.
    """

    try:
        http = credentials.authorize(httplib2.Http())
        service = build('calendar', 'v3', http=http)

        event = {
            'summary': options.message,
            'location': '',
            'reminders': {
                "useDefault": False,
                "overrides": [
                    {
                        "method": 'sms',
                        "minutes": config['message'],
                        },
                    ],
                }
        }
        event.update(create_event_datetimes(config))

        service.events().insert(calendarId=options.calendar, sendNotifications=True, body=event).execute()
    except Exception, err:
        sys.stderr.write(u"ERROR: Creating google calendar event error. %s\n" % err)
        sys.exit(-1)


def main():
    """
    Processing notification call main function.
    """

    # getting info for creating event
    options = parse_cmd_line()
    config = parse_config(check_config_file(options.config))
    credentials = get_google_credentials(options, config)

    if not options.get_google_credentials:
        create_event(options, config, credentials)


if __name__ == "__main__":
    main()
