#!/usr/bin/env python

# -*- coding: utf-8 -*-

# nagios-notification-google-calendar
# notification_google_calendar.py

# Copyright (c) 2013-2015 Alexei Andrushievich <vint21h@vint21h.pp.ua>
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


from __future__ import unicode_literals
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
except (ImportError, ), err:
    sys.stderr.write("ERROR: Couldn't load module. {err}\n".format(err=err))
    sys.exit(-1)

__all__ = ["main", ]

# metadata
VERSION = (0, 3, 0)
__version__ = ".".join(map(str, VERSION))


# global variables
SCOPE = "https://www.googleapis.com/auth/calendar"
DT_FORMAT = "%Y-%m-%dT%H:%M:00.000"


def parse_options():
    """
    Commandline options arguments parsing.
    """

    # build options and help
    version = "%%prog {version}".format(version=__version__)
    parser = OptionParser(version=version)
    parser.add_option(
        "-u", "--username", action="store", dest="username",
        type="string", default="", metavar="RECIPIENT", help="user"
    )
    parser.add_option(
        "-C", "--calendar", metavar="CALENDAR", action="store",
        type="string", dest="calendar", default="", help="google calendar ID"
    )
    parser.add_option(
        "-t", "--timezone", metavar="TIMEZONE", action="store",
        type="string", dest="timezone", default="", help="user timezone"
    )
    parser.add_option(
        "-m", "--message", metavar="MESSAGE", action="store",
        type="string", dest="message", default="", help="message text"
    )
    parser.add_option(
        "-c", "--config", metavar="CONFIG", action="store",
        type="string", dest="config", help="path to config file",
        default="/etc/nagios/notification_google_calendar.ini")
    parser.add_option(
        "-q", "--quiet", metavar="QUIET", action="store_true",
        default=False, dest="quiet", help="be quiet"
    )
    parser.add_option(
        "-g", "--get-google-credentials", metavar="GET-GOOGLE-CREDENTIALS",
        action="store_true", default=False, dest="get_google_credentials",
        help="get google API credentials for user"
    )

    options = parser.parse_args(sys.argv)[0]

    mandatories = ["username", ]
    # check mandatory command line options supplied
    if not options.get_google_credentials:
        mandatories.append("calendar")  # set calendar option required when sending message
        mandatories.append("message")  # set message option required when sending message
        mandatories.append("timezone")  # set timezone option required when sending message
    if not all(options.__dict__[mandatory] for mandatory in mandatories):
        parser.error("Required command line option missing\n")

    return options


def parse_config(options):
    """
    Get settings from config file.
    """

    if os.path.exists(options.config):
        config = ConfigParser.ConfigParser()
        try:
            config.read(options.config)
        except Exception, err:
            if not options.quiet:
                sys.stderr.write("ERROR: Config file read {config} error. {err}".format(config=options.config, err=err))
            sys.exit(-1)

        try:
            configdata = {
                "secrets": config.get("GOOGLE", "secrets"),
                "credentials": config.get("nagios-notification-google-calendar", "credentials"),
                "start": config.get("nagios-notification-google-calendar", "start"),
                "end": config.get("nagios-notification-google-calendar", "end"),
                "message": config.get("nagios-notification-google-calendar", "message"),
            }
        except ConfigParser.NoOptionError, err:
            if not options.quiet:
                sys.stderr.write("ERROR: Config file missing option error. {err}\n".format(err=err))
            sys.exit(-1)

        # check mandatory config options supplied
        mandatories = ["secrets", "credentials", "start", "end", "message", ]
        if not all(configdata[mandatory] for mandatory in mandatories):
            if not options.quiet:
                sys.stdout.write("Mandatory config option missing\n")
            sys.exit(0)

        return configdata
    else:
        if not options.quiet:
            sys.stderr.write("ERROR: Config file {config} does not exist\n".format(config=options.config))
        sys.exit(0)


def get_google_credentials(options, config):
    """
    Get google API credentials for user.
    """

    try:
        if options.get_google_credentials:
            flow = flow_from_clientsecrets(config["secrets"], scope=SCOPE, redirect_uri="oob")
            sys.stdout.write("Follow this URL: {url} and grant access to calendar.\n".format(url=flow.step1_get_authorize_url()))
            token = raw_input("Enter token:")
            credentials = flow.step2_exchange(token)
            storage = Storage(os.path.join(config["credentials"], "{username}.json".format(username=options.username)))
            storage.put(credentials)
            credentials.set_store(storage)
        else:
            storage = Storage(os.path.join(config["credentials"], "{username}.json".format(username=options.username)))
            credentials = storage.get()
    except Exception, err:
        if not options.quiet:
            sys.stderr.write("ERROR: Getting google API credentials error. {err}\n".format(err=err))
        sys.exit(-1)

    return credentials


def create_event_datetimes(options, config):
    """
    Create event start and end datetimes.
    """

    now = datetime.datetime.now()

    return {
        "start": {
            "dateTime": (now + datetime.timedelta(minutes=int(config["start"]))).strftime(DT_FORMAT),
            "timeZone": options.timezone,
        },
        "end": {
            "dateTime": (now + datetime.timedelta(minutes=int(config["end"]))).strftime(DT_FORMAT),
            "timeZone": options.timezone,
        },
    }


def create_event(options, config, credentials):
    """
    Create event in calendar with sms reminder.
    """

    try:
        http = credentials.authorize(httplib2.Http())
        service = build("calendar", "v3", http=http)

        event = {
            "summary": options.message,
            "location": "",
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {
                        "method": "sms",
                        "minutes": config["message"],
                    },
                ],
            }
        }
        event.update(create_event_datetimes(options, config))

        service.events().insert(calendarId=options.calendar, sendNotifications=True, body=event).execute()
    except Exception, err:
        if not options.quiet:
            sys.stderr.write("ERROR: Creating google calendar event error. {err}\n".format(err=err))
        sys.exit(-1)


def main():
    """
    Processing notification call main function.
    """

    # getting info for creating event
    options = parse_options()
    config = parse_config(options)
    credentials = get_google_credentials(options, config)

    if not options.get_google_credentials:
        create_event(options, config, credentials)


if __name__ == "__main__":

    main()
