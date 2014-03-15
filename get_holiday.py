#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2014 Thomas Elfström
# get_holiday

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
from datetime import timedelta


def free(confprg, holid, now, free_days, holidays):
	
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
					if line.lower == holid[day].lower():
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

	return holiday['yesterday'], holiday['today'], holiday['tomorrow']
