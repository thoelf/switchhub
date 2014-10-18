#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2014 Thomas Elfström
# google_calendar.py

''' This file is part of SwitchHub.

SwitchHub is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

SwitchHub is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with SwitchHub. If not, see <http://www.gnu.org/licenses/>. '''


def main():
    import configparser
    import codecs
    import datetime
    from datetime import datetime
    from datetime import timedelta
    import os
    import subprocess
    import time

	# Initialize config parser for the gcalendar settings file
    confgcal = configparser.ConfigParser()
    confgcal.readfp(codecs.open("/etc/switchhub/plugins/gcalendar", "r", "utf8"))

    # Wait until www.google.com can be reached or wait 10 minutes.
    # The whole program will wait, so we don't want to wait too long.
    # If the connection cannot be established, switchhub will use the existing (old) values.
    # If there are no old values (first run), switchhub will crash if variables in the
    # events configuration file becomes undefined.
    minutes = 0
    while os.system("ping -c 1 www.google.com") and minutes < 10:
        time.sleep(60)
        minutes += 1

    if minutes < 10:

        # Edit these settings for your location - move to config file
#        holidays_calendar = "Helgdagar i Sverige"
        holidays_calendar = confgcal['calendars']['holidays_calendar']
 #       sun_calendar = "Soluppgång och solnedgång för Linköping"
        sun_calendar = confgcal['calendars']['sun_calendar']

#        print(holidays_calendar, sun_calendar)

        with open("/etc/switchhub/plugins/gcalendar_holidays", "r") as f:
            holidays = f.read()

        with open("/etc/switchhub/plugins/gcalendar_free_days", "r") as f:
            free_days = f.read()

        now = datetime.now()

        command = "google calendar list --fields name --cal " + sun_calendar + " --date today"
        try:
            stdoutdata = subprocess.check_output([command], shell=True)
        except subprocess.CalledProcessError:
            pass
        else:
            nlines = stdoutdata.decode("utf-8")
            for line in nlines.splitlines():
                if line.strip():                        # If line not empty
                    if line[0][0] != '[':               # If line does not start with '['
                        _sunup = line.split(' ')[1]
                        _sundown = line.split(' ')[4]
                        sunup = '({0} <= t < {1})'.format(_sunup, _sundown)
                        sundown = '(00:00 <= t < {0} or {1} <= t < 23:59)'.format(_sunup, _sundown)


            t_sunup = datetime.strptime(_sunup, '%H:%M')
            t_sundown = datetime.strptime(_sundown, '%H:%M')

            sunup_minus_10 = '({0} <= t < {1})'.format((\
			t_sunup - timedelta(minutes=10)).strftime('%H:%M'), (t_sundown - timedelta(minutes=10)).strftime('%H:%M'))
            sunup_minus_20 = '({0} <= t < {1})'.format((\
			t_sunup - timedelta(minutes=20)).strftime('%H:%M'), (t_sundown - timedelta(minutes=20)).strftime('%H:%M'))
            sunup_minus_30 = '({0} <= t < {1})'.format((\
			t_sunup - timedelta(minutes=30)).strftime('%H:%M'), (t_sundown - timedelta(minutes=30)).strftime('%H:%M'))
            sunup_minus_40 = '({0} <= t < {1})'.format((\
			t_sunup - timedelta(minutes=40)).strftime('%H:%M'), (t_sundown - timedelta(minutes=40)).strftime('%H:%M'))
            sunup_minus_50 = '({0} <= t < {1})'.format((\
			t_sunup - timedelta(minutes=50)).strftime('%H:%M'), (t_sundown - timedelta(minutes=50)).strftime('%H:%M'))
            sunup_minus_60 = '({0} <= t < {1})'.format((\
			t_sunup - timedelta(minutes=60)).strftime('%H:%M'), (t_sundown - timedelta(minutes=60)).strftime('%H:%M'))

            sunup_plus_10 = '({0} <= t < {1})'.format((\
			t_sunup + timedelta(minutes=10)).strftime('%H:%M'), (t_sundown + timedelta(minutes=10)).strftime('%H:%M'))
            sunup_plus_20 = '({0} <= t < {1})'.format((\
			t_sunup + timedelta(minutes=20)).strftime('%H:%M'), (t_sundown + timedelta(minutes=20)).strftime('%H:%M'))
            sunup_plus_30 = '({0} <= t < {1})'.format((\
			t_sunup + timedelta(minutes=30)).strftime('%H:%M'), (t_sundown + timedelta(minutes=30)).strftime('%H:%M'))
            sunup_plus_40 = '({0} <= t < {1})'.format((\
			t_sunup + timedelta(minutes=40)).strftime('%H:%M'), (t_sundown + timedelta(minutes=40)).strftime('%H:%M'))
            sunup_plus_50 = '({0} <= t < {1})'.format((\
			t_sunup + timedelta(minutes=50)).strftime('%H:%M'), (t_sundown + timedelta(minutes=50)).strftime('%H:%M'))
            sunup_plus_60 = '({0} <= t < {1})'.format((\
			t_sunup + timedelta(minutes=60)).strftime('%H:%M'), (t_sundown + timedelta(minutes=60)).strftime('%H:%M'))

            sundown_minus_10 = '(00:00 <= t < {0} or {1} <= t < 23:59)'.format((\
			t_sunup - timedelta(minutes=10)).strftime('%H:%M'), (t_sundown - timedelta(minutes=10)).strftime('%H:%M'))
            sundown_minus_20 = '(00:00 <= t < {0} or {1} <= t < 23:59)'.format((\
			t_sunup - timedelta(minutes=20)).strftime('%H:%M'), (t_sundown - timedelta(minutes=20)).strftime('%H:%M'))
            sundown_minus_30 = '(00:00 <= t < {0} or {1} <= t < 23:59)'.format((\
			t_sunup - timedelta(minutes=30)).strftime('%H:%M'), (t_sundown - timedelta(minutes=30)).strftime('%H:%M'))
            sundown_minus_40 = '(00:00 <= t < {0} or {1} <= t < 23:59)'.format((\
			t_sunup - timedelta(minutes=40)).strftime('%H:%M'), (t_sundown - timedelta(minutes=40)).strftime('%H:%M'))
            sundown_minus_50 = '(00:00 <= t < {0} or {1} <= t < 23:59)'.format((\
			t_sunup - timedelta(minutes=50)).strftime('%H:%M'), (t_sundown - timedelta(minutes=50)).strftime('%H:%M'))
            sundown_minus_60 = '(00:00 <= t < {0} or {1} <= t < 23:59)'.format((\
			t_sunup - timedelta(minutes=60)).strftime('%H:%M'), (t_sundown - timedelta(minutes=60)).strftime('%H:%M'))

            sundown_plus_10 = '(00:00 <= t < {0} or {1} <= t < 23:59)'.format((\
			t_sunup + timedelta(minutes=10)).strftime('%H:%M'), (t_sundown + timedelta(minutes=10)).strftime('%H:%M'))
            sundown_plus_20 = '(00:00 <= t < {0} or {1} <= t < 23:59)'.format((\
			t_sunup + timedelta(minutes=20)).strftime('%H:%M'), (t_sundown + timedelta(minutes=20)).strftime('%H:%M'))
            sundown_plus_30 = '(00:00 <= t < {0} or {1} <= t < 23:59)'.format((\
			t_sunup + timedelta(minutes=30)).strftime('%H:%M'), (t_sundown + timedelta(minutes=30)).strftime('%H:%M'))
            sundown_plus_40 = '(00:00 <= t < {0} or {1} <= t < 23:59)'.format((\
			t_sunup + timedelta(minutes=40)).strftime('%H:%M'), (t_sundown + timedelta(minutes=40)).strftime('%H:%M'))
            sundown_plus_50 = '(00:00 <= t < {0} or {1} <= t < 23:59)'.format((\
			t_sunup + timedelta(minutes=50)).strftime('%H:%M'), (t_sundown + timedelta(minutes=50)).strftime('%H:%M'))
            sundown_plus_60 = '(00:00 <= t < {0} or {1} <= t < 23:59)'.format((\
			t_sunup + timedelta(minutes=60)).strftime('%H:%M'), (t_sundown + timedelta(minutes=60)).strftime('%H:%M'))

        cmd = {}
        holi = {}
        stdoutdata = {}
        nlines = {}
        command = "google calendar list --fields name --cal " + holidays_calendar + " --date "
        cmd['yesterday'] = command + (now - timedelta(days=1)).strftime("%Y-%m-%d")
        cmd['today'] = command + "today"
        cmd['tomorrow'] = command + (now + timedelta(days=1)).strftime("%Y-%m-%d")
        for day in cmd:
            try:
                stdoutdata[day] = subprocess.check_output([cmd[day]], shell=True)
            except subprocess.CalledProcessError:
                pass
            else:
                nlines[day] = stdoutdata[day].decode("utf-8")
                for line in nlines[day].splitlines():
                    if line.strip():
                        if line[0][0] != '[':
                            holi[day] = line.split('\n')[0]
                        else:
                            holi[day] = ""

        days = {}
        days['yesterday'] = now - timedelta(days = 1)
        days['today'] = now
        days['tomorrow'] = now + timedelta(days = 1)

        holiday = {}
        holiday['yesterday'] = holiday['today'] = holiday['tomorrow'] = False

        # Check holiday depending on weekday
        for day in days:
            holiday[day] = True if 5 <= days[day].weekday() <= 6 else False
    
        # Check holiday from Google calendar that matches holidays.cfg
        for day in holiday:
            if not holiday[day]:
                for line in holidays.splitlines():
                    if line.strip():
                        if line.lower() == holi[day].lower():
                            holiday[day] = True
                            break

        # Check holiday with dates in free_days.cfg
        for day in holiday:
            if not holiday[day]:
                for line in free_days.splitlines():
                    line = line.split('\n')[0]
                    line = line.replace(' ', '')
                    if len(line.split(':')) == 1:
                        if days[day].strftime("%Y-%m-%d") == line:
                            holiday[day] = True
                            break
                    elif len(line.split(':')) == 2:
                        if line.split(':')[0] <= days[day].strftime("%Y-%m-%d") <= line.split(':')[1]:
                            holiday[day] = True
                            break


        print("gcalendar.py;sunup;{0}".format(sunup))
        print("gcalendar.py;sundown;{0}".format(sundown))
        print("gcalendar.py;holiday_yesterday;{0}".format(holiday['yesterday']))
        print("gcalendar.py;holiday_today;{0}".format(holiday['today']))
        print("gcalendar.py;holiday_tomorrow;{0}".format(holiday['tomorrow']))
        print("gcalendar.py;workday;{0}".format(not holiday['today']))
        print("gcalendar.py;sunup_minus_10;{0}".format(sunup_minus_10))
        print("gcalendar.py;sunup_minus_20;{0}".format(sunup_minus_20))
        print("gcalendar.py;sunup_minus_30;{0}".format(sunup_minus_30))
        print("gcalendar.py;sunup_minus_40;{0}".format(sunup_minus_40))
        print("gcalendar.py;sunup_minus_50;{0}".format(sunup_minus_50))
        print("gcalendar.py;sunup_minus_60;{0}".format(sunup_minus_60))
        print("gcalendar.py;sunup_plus_10;{0}".format(sunup_plus_10))
        print("gcalendar.py;sunup_plus_20;{0}".format(sunup_plus_20))
        print("gcalendar.py;sunup_plus_30;{0}".format(sunup_plus_30))
        print("gcalendar.py;sunup_plus_40;{0}".format(sunup_plus_40))
        print("gcalendar.py;sunup_plus_50;{0}".format(sunup_plus_50))
        print("gcalendar.py;sunup_plus_60;{0}".format(sunup_plus_60))
        print("gcalendar.py;sundown_minus_10;{0}".format(sundown_minus_10))
        print("gcalendar.py;sundown_minus_20;{0}".format(sundown_minus_20))
        print("gcalendar.py;sundown_minus_30;{0}".format(sundown_minus_30))
        print("gcalendar.py;sundown_minus_40;{0}".format(sundown_minus_40))
        print("gcalendar.py;sundown_minus_50;{0}".format(sundown_minus_50))
        print("gcalendar.py;sundown_minus_60;{0}".format(sundown_minus_60))
        print("gcalendar.py;sundown_plus_10;{0}".format(sundown_plus_10))
        print("gcalendar.py;sundown_plus_20;{0}".format(sundown_plus_20))
        print("gcalendar.py;sundown_plus_30;{0}".format(sundown_plus_30))
        print("gcalendar.py;sundown_plus_40;{0}".format(sundown_plus_40))
        print("gcalendar.py;sundown_plus_50;{0}".format(sundown_plus_50))
        print("gcalendar.py;sundown_plus_60;{0}".format(sundown_plus_60))

if __name__ == "__main__":
    main()
