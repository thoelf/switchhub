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
	import datetime
	from datetime import datetime
	from datetime import timedelta
	import subprocess

	# Edit these settings for your location
	holidays_calendar = "Helgdagar i Sverige"
	sun_calendar = "Soluppgång och solnedgång för Linköping"

	with open("/etc/switchhub/plugins/gcalendar_holidays", "r") as f:
		holidays = f.read()

	with open("/etc/switchhub/plugins/gcalendar_free_days", "r") as f:
		free_days = f.read()

	now = datetime.now()


	# Get sun data from Google
	command = "google calendar list --fields name --cal " + "\"" + sun_calendar + "\"" + " --date today"
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
					sunup = '(\'{0}\' <= t < \'{1}\')'.format(_sunup, _sundown)
					sundown = '(\'00:00\' <= t < \'{0}\' or \'{1}\' <= t < \'23:59\')'.format(_sunup, _sundown)

	cmd = {}
	holi = {}
	stdoutdata = {}
	nlines = {}
	command = "google calendar list --fields name --cal " + "\"" + holidays_calendar + "\"" + " --date "
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
					if line.lower == holi[day].lower():
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

if __name__ == "__main__":
    main()
