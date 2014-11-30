#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2014 Thomas Elfström
# calendar.py

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
    import json
    import os
    import subprocess
    import time
    import urllib.request

    # Initialize config parser for the calendar settings file
    confcal = configparser.ConfigParser()
    confcal.readfp(codecs.open("/etc/switchhub/plugins/calendar", "r", "utf8"))
    calurl = confcal['settings']['url']

    # Wait until www.webcal.fi can be reached or wait 10 minutes.
    # The whole program will wait, so we don't want to wait too long.
    # If the connection cannot be established, switchhub will use the existing (old) values.
    # If there are no old values (first run), switchhub will crash if variables in the
    # events configuration file becomes undefined.

#    minutes = 0
#    while os.system("ping -c 1 www.webcal.fi >/dev/null") and minutes < 10:
#        time.sleep(60)
#        minutes += 1
#    if minutes < 10:

    now = datetime.now()

    if not os.path.exists('/run/shm/data'):
        os.mkdir('/run/shm/data')

    if os.path.exists('/run/shm/data/calendar.json'):
        if now.year != time.ctime(os.path.getctime('/run/shm/data/calendar.json')).split()[4]:
            try:
                urllib.request.urlretrieve(calurl, '/run/shm/data/calendar.json')
            except:
                pass
    else:
        open('/run/shm/data/calendar.json', 'a').close()
        try:
            urllib.request.urlretrieve(calurl, '/run/shm/data/calendar.json')
        except:
            pass

    try:
        with open ('/run/shm/data/calendar.json', 'r') as calfile:
            data = calfile.read()
            theJSON = json.loads(data)
    except:
        pass


    calholi = {}
    calholi['yesterday'] = calholi['today'] = calholi['tomorrow'] = "No holiday"
    for n in range (0, len(theJSON)):
        if theJSON[n]['date'] == (now - timedelta(days=1)).strftime('%Y-%m-%d'):
            calholi['yesterday'] = theJSON[n]['name']
        if theJSON[n]['date'] == now.strftime('%Y-%m-%d'):
            calholi['today'] = theJSON[n]['name']
        if theJSON[n]['date'] == (now + timedelta(days=1)).strftime('%Y-%m-%d'):
            calholi['tomorrow'] = theJSON[n]['name']

#        print(theJSON[n]['date'])
#        print(theJSON[n]['2014-12-25'])
#        print(theJSON[n]['name'])


    # Read the settings from the calendar settings file
    with open("/etc/switchhub/plugins/calendar_holidays", "r") as f:
        holidays = f.read()

    with open("/etc/switchhub/plugins/calendar_free_days", "r") as f:
        free_days = f.read()


    holiday = {}
    holiday['yesterday'] = holiday['today'] = holiday['tomorrow'] = False

    days = {}
    days['yesterday'] = now - timedelta(days = 1)
    days['today'] = now
    days['tomorrow'] = now + timedelta(days = 1)

    # Check holiday depending on weekday
    for day in days:
        holiday[day] = True if 5 <= days[day].weekday() <= 6 else False


    # Check holiday from calendar that matches holidays.cfg
    for day in holiday:
#        print(day) => yesterday, today, tomorrow
        if not holiday[day]:
            for line in holidays.splitlines():
                if line.strip():
                    if line.lower() == calholi[day].lower():
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


    print("calendar.py;holiday_yesterday;{0}".format(holiday['yesterday']))
    print("calendar.py;holiday_today;{0}".format(holiday['today']))
    print("calendar.py;holiday_tomorrow;{0}".format(holiday['tomorrow']))
    print("calendar.py;workday;{0}".format(not holiday['today']))

if __name__ == "__main__":
    main()
