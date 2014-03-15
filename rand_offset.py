#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2014 Thomas Elfström
# rand_offset.py

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

import re
from random import randint
from datetime import datetime
from datetime import timedelta


def replace_words(text, word_dic):
	rc = re.compile('|'.join(map(re.escape, word_dic)))
	def translate(match):
		return word_dic[match.group(0)]
	return rc.sub(translate, text)


def calc_times(updown_times, s, upordown):
	suntime_dict = {}
	re_compiled = re.compile(r"(" + re.escape(upordown) + "([+-]\d{1,2})?)")
	suntime = re.findall(re_compiled, s)
	try:
		upordown in suntime[0]
	except:
		pass
	else:
		i = 0
		while i < len(suntime):
			try:
				offset = int(suntime[i][0].split(upordown)[1])
			except:
				offset = 0

			if upordown == "sunup":
				sunup_offset = "\"" + datetime.strftime(datetime.strptime(updown_times[0],'%H:%M') + \
					timedelta(minutes=offset), '%H:%M') + "\""
				suntime_dict[suntime[i][0]] = sunup_offset + " <= t < " + "\"" + updown_times[1] + "\""
			else:
				sundown_offset =  "\"" + datetime.strftime(datetime.strptime(updown_times[1],'%H:%M') + \
					timedelta(minutes=offset), '%H:%M') + "\""
				suntime_dict[suntime[i][0]] = "((" + "\"first_min\" <= t < " + "\"" + updown_times[0] + \
					"\") or (" +  sundown_offset + " <= t <= \"last_min\"))"

			i += 1
		s = replace_words(s, suntime_dict)
	return s


def calc(s, randtime, sunuptime, sundowntime):
	r_time = {}
	sud = [sunuptime, sundowntime]
	s = re.sub(r"(\d{3,})", "99", s)

	suntype = "sunup"
	s = calc_times(sud, s, suntype)
	suntype = "sundown"
	s = calc_times(sud, s, suntype)

	s = re.sub(r"(([+-]\d{1,2})?)", "", s)

	re_time = re.compile(r"\d{2}:\d{2}")
	times = re.findall(re_time, s)
	if times:
		for time in times:
			r_time[time] = datetime.strftime(datetime.strptime(time, "%H:%M") + \
				timedelta(minutes=randint(-randtime, randtime)), "%H:%M")
		s = replace_words(s, r_time)
		s = s.replace("first_min", "00:00")
		s = s.replace("last_min", "23:59")
	return s

