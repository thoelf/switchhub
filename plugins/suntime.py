#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2016 Thomas Elfström
# suntime.py

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
from datetime import datetime
from urllib.request import urlopen
import json
import os
import socket
import time


def main():
	# Local time - UTC (Local time is "normal" time, without daylight saving)
	utc_diff = 1

	# Change the lat och long if you don't live in Linköping. http://www.latlong.net/
	lat = 58.414054
	lng = 15.599525

	# Default data. Times from the middle of each month. Change if you don't live in Linköping.
	default_sunup = ("08:34", "07:32", "06:13", "05:45", "04:30", "03:50",
			"04:15", "05:19", "06:27", "07:34", "07:47", "08:41")
	default_sundown = ("15:39", "16:52", "18:01", "20:11", "21:19", "22:06",
			"21:50", "20:43", "19:16", "17:51", "15:37", "15:05")
	
	# Get today's times for sunset and sunrise from http://sunrise-sunset.org/
	sundata_url = "http://api.sunrise-sunset.org/json?lat=" + str(lat) + "&lng=" + str(lng) + "&date=today"
	server_address = ('localhost', 8001)
	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(server_address)

	ownfile = os.path.basename(__file__)


	while True:
		now = datetime.now()
		today = now.strftime("%d")
		day2 = today

		sun_data_avail = True  # Assume that sun data will be available

		try:
			data = urlopen(sundata_url, timeout = 10).read().decode('utf-8')  # Get the sun data
		except:
			sun_data_avail = False
		
		if sun_data_avail:
			theJSON = json.loads(data)
			if (theJSON['status']).lower() != "ok":  # Check if the data is OK
				sun_data_avail = False

		if sun_data_avail:
			t_sunup = theJSON['results']['sunrise']
			t_sundown = theJSON['results']['sunset']
		
			t_sunup = datetime.strptime(t_sunup.split(' ')[0], "%H:%M:%S")  # Convert from string to time object
			t_sunup = t_sunup + timedelta(hours = utc_diff + time.daylight)  # Convert to local time and compensate for daylight saving
		
			if (t_sundown.split(' ')[1]).lower() == "pm":
				t_sundown = datetime.strptime(t_sundown.split(' ')[0], "%H:%M:%S") + timedelta(hours=12)
			else:
				t_sundown = datetime.strptime(t_sundown.split(' ')[0], "%H:%M:%S")

			t_sundown = t_sundown + timedelta(hours = utc_diff + time.daylight)
		else:
			# Use default values
			t_sunup = datetime.strptime(default_sunup[now.month - 1], "%H:%M")
			t_sundown = datetime.strptime(default_sundown[now.month - 1], "%H:%M")


		sundata = {"sunup":'({0} <= t < {1})'.format((t_sunup - timedelta(minutes=0)).strftime('%H:%M'), (t_sundown - timedelta(minutes=0)).strftime('%H:%M')),
		"sunup_minus_10":'({0} <= t < {1})'.format((t_sunup - timedelta(minutes=10)).strftime('%H:%M'), (t_sundown - timedelta(minutes=10)).strftime('%H:%M')),
		"sunup_minus_20":'({0} <= t < {1})'.format((t_sunup - timedelta(minutes=20)).strftime('%H:%M'), (t_sundown - timedelta(minutes=20)).strftime('%H:%M')),
		"sunup_minus_30":'({0} <= t < {1})'.format((t_sunup - timedelta(minutes=30)).strftime('%H:%M'), (t_sundown - timedelta(minutes=30)).strftime('%H:%M')),
		"sunup_minus_40":'({0} <= t < {1})'.format((t_sunup - timedelta(minutes=40)).strftime('%H:%M'), (t_sundown - timedelta(minutes=40)).strftime('%H:%M')),
		"sunup_minus_50":'({0} <= t < {1})'.format((t_sunup - timedelta(minutes=50)).strftime('%H:%M'), (t_sundown - timedelta(minutes=50)).strftime('%H:%M')),
		"sunup_minus_60":'({0} <= t < {1})'.format((t_sunup - timedelta(minutes=60)).strftime('%H:%M'), (t_sundown - timedelta(minutes=60)).strftime('%H:%M')),
		"sunup_plus_10":'({0} <= t < {1})'.format((t_sunup + timedelta(minutes=10)).strftime('%H:%M'), (t_sundown + timedelta(minutes=10)).strftime('%H:%M')),
		"sunup_plus_20":'({0} <= t < {1})'.format((t_sunup + timedelta(minutes=20)).strftime('%H:%M'), (t_sundown + timedelta(minutes=20)).strftime('%H:%M')),
		"sunup_plus_30":'({0} <= t < {1})'.format((t_sunup + timedelta(minutes=30)).strftime('%H:%M'), (t_sundown + timedelta(minutes=30)).strftime('%H:%M')),
		"sunup_plus_40":'({0} <= t < {1})'.format((t_sunup + timedelta(minutes=40)).strftime('%H:%M'), (t_sundown + timedelta(minutes=40)).strftime('%H:%M')),
		"sunup_plus_50":'({0} <= t < {1})'.format((t_sunup + timedelta(minutes=50)).strftime('%H:%M'), (t_sundown + timedelta(minutes=50)).strftime('%H:%M')),
		"sunup_plus_60":'({0} <= t < {1})'.format((t_sunup + timedelta(minutes=60)).strftime('%H:%M'), (t_sundown + timedelta(minutes=60)).strftime('%H:%M')),
		"sundown":'(00:00 <= t < {0} or {1} <= t <= 23:59)'.format((t_sunup-timedelta(minutes=0)).strftime('%H:%M'), (t_sundown-timedelta(minutes=0)).strftime('%H:%M')),
		"sundown_minus_10":'(00:00 <= t < {0} or {1} <= t <= 23:59)'.format((t_sunup-timedelta(minutes=10)).strftime('%H:%M'), (t_sundown-timedelta(minutes=10)).strftime('%H:%M')),
		"sundown_minus_20":'(00:00 <= t < {0} or {1} <= t <= 23:59)'.format((t_sunup-timedelta(minutes=20)).strftime('%H:%M'), (t_sundown-timedelta(minutes=20)).strftime('%H:%M')),
		"sundown_minus_30":'(00:00 <= t < {0} or {1} <= t <= 23:59)'.format((t_sunup-timedelta(minutes=30)).strftime('%H:%M'), (t_sundown-timedelta(minutes=30)).strftime('%H:%M')),
		"sundown_minus_40":'(00:00 <= t < {0} or {1} <= t <= 23:59)'.format((t_sunup-timedelta(minutes=40)).strftime('%H:%M'), (t_sundown-timedelta(minutes=40)).strftime('%H:%M')),
		"sundown_minus_50":'(00:00 <= t < {0} or {1} <= t <= 23:59)'.format((t_sunup-timedelta(minutes=50)).strftime('%H:%M'), (t_sundown-timedelta(minutes=50)).strftime('%H:%M')),
		"sundown_minus_60":'(00:00 <= t < {0} or {1} <= t <= 23:59)'.format((t_sunup-timedelta(minutes=60)).strftime('%H:%M'), (t_sundown-timedelta(minutes=60)).strftime('%H:%M')),
		"sundown_plus_10":'(00:00 <= t < {0} or {1} <= t <= 23:59)'.format((t_sunup+timedelta(minutes=10)).strftime('%H:%M'), (t_sundown+timedelta(minutes=10)).strftime('%H:%M')),
		"sundown_plus_20":'(00:00 <= t < {0} or {1} <= t <= 23:59)'.format((t_sunup+timedelta(minutes=20)).strftime('%H:%M'), (t_sundown+timedelta(minutes=20)).strftime('%H:%M')),
		"sundown_plus_30":'(00:00 <= t < {0} or {1} <= t <= 23:59)'.format((t_sunup+timedelta(minutes=30)).strftime('%H:%M'), (t_sundown+timedelta(minutes=30)).strftime('%H:%M')),
		"sundown_plus_40":'(00:00 <= t < {0} or {1} <= t <= 23:59)'.format((t_sunup+timedelta(minutes=40)).strftime('%H:%M'), (t_sundown+timedelta(minutes=40)).strftime('%H:%M')),
		"sundown_plus_50":'(00:00 <= t < {0} or {1} <= t <= 23:59)'.format((t_sunup+timedelta(minutes=50)).strftime('%H:%M'), (t_sundown+timedelta(minutes=50)).strftime('%H:%M')),
		"sundown_plus_60":'(00:00 <= t < {0} or {1} <= t <= 23:59)'.format((t_sunup+timedelta(minutes=60)).strftime('%H:%M'), (t_sundown+timedelta(minutes=60)).strftime('%H:%M'))}

		for key in sundata:
			s.send(bytes(ownfile + ";" + key + ";" + sundata[key] + "\n", 'UTF-8'))

		while today == day2:
			now = datetime.now()
			day2 = now.strftime("%d")
			time.sleep(59.95)

if __name__ == "__main__":
	main()
