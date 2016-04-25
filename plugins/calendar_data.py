#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2016 Thomas Elfström
# calendar_data.py

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

import datetime
import json
import os
import socket
import time
import urllib.request
from datetime import datetime, timedelta


def get_cal(calurl):
    try:
        urllib.request.urlretrieve(calurl, '/var/tmp/calendar.json')
    except:
        pass


def main():
    ownfile = os.path.basename(__file__)

    holidays = ("nyårsdagen",
                "trettondedag jul",
                "långfredagen",
                "påskdagen",
                "annandag påsk",
                "första maj",
                "kristi himmelsfärds dag",
                "sveriges nationaldag",
                "midsommarafton",
                "midsommardagen",
                "alla helgons dag",
                "julafton",
                "juldagen",
                "annandag jul",
                "nyårsafton")

    free_days = ("2016-05-06",
                "2016-07-11:2016-08-12")


    calurl = "http://www.webcal.fi/cal.php?id=230&format=json&start_year=current_year&end_year=current_year&tz=Europe%%2FStockholm"

    server_address = ('localhost', 8001)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect(server_address)

    while True:
        now = datetime.now()
        today = now.strftime("%d")
        day2 = now.strftime("%d")

        cal_data = {"weekday": True if 0 <= now.weekday() < 5 else False,
                    "monday": True if now.weekday() == 0 else False,
                    "tuesday": True if now.weekday() == 1 else False,
                    "wednesday": True if now.weekday() == 2 else False,
                    "thursday": True if now.weekday() == 3 else False,
                    "friday": True if now.weekday() == 4 else False,
                    "saturday": True if now.weekday() == 5 else False,
                    "sunday": True if now.weekday() == 6 else False,
                    "january": True if now.month == 1 else False,
                    "february": True if now.month == 2 else False,
                    "march": True if now.month == 3 else False,
                    "april": True if now.month == 4 else False,
                    "may": True if now.month == 5 else False,
                    "june": True if now.month == 6 else False,
                    "july": True if now.month == 7 else False,
                    "august": True if now.month == 8 else False,
                    "september": True if now.month == 9 else False,
                    "october": True if now.month == 10 else False,
                    "november": True if now.month == 11 else False,
                    "december": True if now.month == 12 else False}

        if os.path.exists('/var/tmp/calendar.json') and os.stat("/var/tmp/calendar.json").st_size > 0:
            try:
                if str(now.year) != time.ctime(os.path.getctime('/var/tmp/calendar.json')).split()[4]:
                    get_cal(calurl)
            except:
                pass
        else:
            get_cal(calurl)

        with open('/var/tmp/calendar.json', 'r') as calfile:
            data = calfile.read()
        theJSON = json.loads(data)

        holiday_yesterday = False
        holiday = False
        holiday_tomorrow = False

        # Check for free days according to the calendar
        for day in range(len(theJSON)):
            if theJSON[day]['date'] == (now - timedelta(days=1)).strftime('%Y-%m-%d') and theJSON[day]['name'].lower() in holidays:
                holiday_yesterday = True
            if theJSON[day]['date'] == now.strftime('%Y-%m-%d') and theJSON[day]['name'].lower() in holidays:
                holiday = True
            if theJSON[day]['date'] == (now + timedelta(days=1)).strftime('%Y-%m-%d') and theJSON[day]['name'].lower() in holidays:
                holiday_tomorrow = True

        # Check for free days according to weekday (assume Saturday's and Sunday's are free)
        if cal_data['monday'] == True:
            holiday_yesterday = True
        elif cal_data['friday'] == True:
            holiday_tomorrow = True
        elif cal_data['saturday'] == True:
            holiday = True
            holiday_tomorrow = True
        elif cal_data['sunday'] == True:
            holiday_yesterday = True
            holiday = True

        # Check for free days in a date span in free_days
        for line in free_days:
            if len(line.split(':')) == 2:
                if line.split(':')[0] <= (now - timedelta(days=1)).strftime('%Y-%m-%d') <= line.split(':')[1]:
                    holiday_yesterday = True
                if line.split(':')[0] <= now.strftime("%Y-%m-%d") <= line.split(':')[1]:
                    holiday = True
                if line.split(':')[0] <= (now + timedelta(days=1)).strftime('%Y-%m-%d') <= line.split(':')[1]:
                    holiday_tomorrow = True

        # Check for free days in free_days
        if (now - timedelta(days=1)).strftime('%Y-%m-%d') in free_days:
            holiday_yesterday = True
        if now.strftime('%Y-%m-%d') in free_days:
            holiday = True
        if (now + timedelta(days=1)).strftime('%Y-%m-%d') in free_days:
            holiday_tomorrow = True

        workday_yesterday = True if holiday_yesterday == False else False
        workday = True if holiday == False else False
        workday_tomorrow = True if holiday_tomorrow == False else False

        s.send(bytes(ownfile + ";holiday_yesterday;{0}".format(holiday_yesterday) + "\n",'UTF-8'))
        s.send(bytes(ownfile + ";holiday;{0}".format(holiday) + "\n",'UTF-8'))
        s.send(bytes(ownfile + ";holiday_tomorrow;{0}".format(holiday_tomorrow) + "\n",'UTF-8'))
        s.send(bytes(ownfile + ";workday_yesterday;{0}".format(workday_yesterday) + "\n",'UTF-8'))
        s.send(bytes(ownfile + ";workday;{0}".format(workday) + "\n",'UTF-8'))
        s.send(bytes(ownfile + ";workday_tomorrow;{0}".format(workday_tomorrow) + "\n",'UTF-8'))

        for key in cal_data.keys():
            s.send(bytes(ownfile + ";" + key + ";" + str(cal_data[key]) + "\n", 'UTF-8'))

        while today == day2:
            now = datetime.now()
            day2 = now.strftime("%d")
            time.sleep(60)

if __name__ == "__main__":
    main()
