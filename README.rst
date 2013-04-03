.. nagios-notification-google-calendar
.. README.rst

A nagios-notification-google-calendar documentation
===================================

    *nagios-notification-google-calendar is a Nagios-plugin that send Nagios notifications via google calendar SMS reminder*

.. contents::

Installation
------------
* Obtain your copy of source code from git repository: ``git clone https://github.com/vint21h/nagios-notification-google-calendar.git``. Or download latest release from https://github.com/vint21h/nagios-notification-google-calendar/tags.
* Run ``python ./setup.py install`` from repository source tree or unpacked archive under root user.

Configuration
-------------
* Read and understand Nagios documentation.
* Add Nagios variable ``$NG$=/usr/bin/notification_google_calendar.py``
* Create Nagios commands definitions like this:

::

# 'notify-host-by-sms' command
define command{
    command_name    notify-host-by-sms
    command_line    $NG$/notification_google_calendar.py -u $CONTACTNAME$ -m "Host '$HOSTALIAS$' is $HOSTSTATE$ - Info: $HOSTOUTPUT$" -C $CONTACTADDRESS1$
}

# 'notify-by-sms' command
define command{
    command_name    notify-by-sms
    command_line    $NG$/notification_google_calendar.py -u $CONTACTNAME$ -m "$NOTIFICATIONTYPE$ $HOSTNAME$ $SERVICEDESC$ $SERVICESTATE$ $SERVICEOUTPUT$ $LONGDATETIME$" -C $C
}

Licensing
---------
nagios-notification-google-calendar is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
For complete license text see COPYING file.


Contacts
--------
**Project Website**: https://github.com/vint21h/nagios-notification-google-calendar

**Author**: Alexei Andrushievich <vint21h@vint21h.pp.ua>
