.. nagios-notification-google-calendar
.. README.rst

A nagios-notification-google-calendar documentation
===================================================

    *nagios-notification-google-calendar is a Nagios-plugin that send Nagios notifications via google calendar SMS reminder*

.. contents::

Installation
------------
* Obtain your copy of source code from git repository: ``git clone https://github.com/vint21h/nagios-notification-google-calendar.git``. Or download latest release from https://github.com/vint21h/nagios-notification-google-calendar/tags.
* Run ``python ./setup.py install`` from repository source tree or unpacked archive under root user. Or use pip: ``pip install nagios-notification-google-calendar``.

Configuration
-------------
* Read and understand Nagios documentation.
* Create Nagios commands definitions like this:

::

    # 'notify-host-by-sms' command
    define command{
        command_name    notify-host-by-sms
        command_line    /usr/bin/notification_google_calendar.py -u $CONTACTNAME$ -m "Host '$HOSTALIAS$' is $HOSTSTATE$ - Info: $HOSTOUTPUT$" -C $CONTACTADDRESS1$
    }

    # 'notify-by-sms' command
    define command{
        command_name    notify-by-sms
        command_line    /usr/bin/notification_google_calendar.py -u $CONTACTNAME$ -m "$NOTIFICATIONTYPE$ $HOSTNAME$ $SERVICEDESC$ $SERVICESTATE$ $SERVICEOUTPUT$ $LONGDATETIME$" -C $C
    }

* Go to https://code.google.com/apis/console/ and create new project.
* Enable calendar API for project.
* Create an OAuth 2.0 client ID for project with ``Installed application`` type and download JSON client secrets file.
* Copy ``/usr/share/doc/nagios-notification-google-calendar/notification_google_calendar.ini`` to ``/etc/nagios`` with your settings. Attention: nagios user must have ``notification_google_calendar.ini`` read permissions, and credentials directory read/write permissions.
* Modify contacts definitions:
    * Add ``addressX`` option to contact definition with contact google calendar ID.
    * Get and save credentials by run ``notification_google_calendar.py`` with ``-g`` option.
    * Add commands to the lists of service and host notifications commands for contact.
    * Configure google calendar for mobile devices.

Licensing
---------
nagios-notification-google-calendar is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
For complete license text see COPYING file.


Contacts
--------
**Project Website**: https://github.com/vint21h/nagios-notification-google-calendar

**Author**: Alexei Andrushievich <vint21h@vint21h.pp.ua>
