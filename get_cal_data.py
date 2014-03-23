#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2014 Thomas Elfström
# get_cal_data

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

import subprocess
from datetime import datetime
from datetime import timedelta
import datetime
import logging


def events(confprg, now):

	logger = logging.getLogger("get_cal_data")
	data_read = True

	# Get sun data from Google
	command = "google calendar list --fields name --cal " + confprg['calendars']['sun']  + " --date today"
	try:
		stdoutdata = subprocess.check_output([command], shell=True)
	except subprocess.CalledProcessError:
		logger.warning('No connection to Google Calendar %s', confprg['calendars']['sun'])
		data_read = False
	else:
		nlines = stdoutdata.decode("utf-8")
		for line in nlines.splitlines():
			if line.strip():                        # If line not empty
				if line[0][0] != '[':               # If line does not start with '['
					sunrise = line.split(' ')[1]
					sunset = line.split(' ')[4]

	cmd = {}
	holi = {}
	stdoutdata = {}
	nlines = {}
	no_connection = False
	command = "google calendar list --fields name --cal " + confprg['calendars']['holidays'] + " --date "
	cmd['yesterday'] = command + (now - timedelta(days=1)).strftime("%Y-%m-%d")
	cmd['today'] = command + "today"
	cmd['tomorrow'] = command + (now + timedelta(days=1)).strftime("%Y-%m-%d")
	for day in cmd:
		try:
			stdoutdata[day] = subprocess.check_output([cmd[day]], shell=True)
		except subprocess.CalledProcessError:
			no_connection = True
		else:
			nlines[day] = stdoutdata[day].decode("utf-8")
			for line in nlines[day].splitlines():
				if line.strip():
					if line[0][0] != '[':
						holi[day] = line.split('\n')[0]
					else:
						holi[day] = ""
		
		if no_connection:
			logger.warning('No connection to Google Calendar %s', confprg['calendars']['holidays'])
			data_read = False
		
	return sunrise, sunset, holi, data_read

##	[Soluppgång och solnedgång för Linköping]
##	Soluppgång: 07:31  Solnedgång: 16:54

