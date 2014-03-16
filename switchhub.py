#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2014 Thomas Elfström
# switchhub.py

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

import configparser
import codecs
from datetime import datetime
import os
from os import path
from subprocess import Popen
import sys
from threading import Thread
import time

import get_cal_data
import get_holiday
import operate_switch
import rand_offset


def main():
	# Check the command line  arguments
	if len(sys.argv) == 1:
		sim = False
	elif len(sys.argv) == 2:
		if sys.argv[1] == "-s":
			sim = True
			print("Simulation mode activated")
		else:
			print ('Usage: switchhub [-s]')
			sys.exit()
	else:
		print ('Usage: switchhub [-s]')
		sys.exit()

	now = datetime.now()
	print(now.strftime("%Y-%m-%d %H:%M") + "\tSwitchHub started")

	confprg = configparser.ConfigParser()
#	confprg.read("program.cfg")
	confprg.readfp(codecs.open("program.cfg", "r", "utf8"))

	confev = configparser.ConfigParser(allow_no_value = True)
#	confev.read("events.cfg")
	confev.readfp(codecs.open("events.cfg", "r", "utf8"))

	with open("free_days.cfg", "r") as f:
		free_days = f.read()

#	with open("holidays.cfg", "r") as f:
#		holidays = f.read()
	with codecs.open("holidays.cfg", "r", "utf8") as f:
		holidays = f.read()

	if not path.isdir(confprg['paths']['workdir']):
		os.mkdir(confprg['paths']['workdir'])

	first_run = True
	verbose = True if (confprg['misc']['verbose'].lower() == "yes" or sim == True) else False
	que = {}
	que_only_on = {}
	que_only_off = {}
	old_state = {}
	pping = {}
	ping = {}
	ping_timer = {}
	random = {}
	thread = {}
	for host in confprg['ping_ip']:
		ping_timer[host] = 0

	# Initialize old_state
	for key in confev.sections():
		old_state[key] = confev[key]['id'] + ";" + "Any string for now. Hi mom!"

	# Read the random settings for the devices
	for key in confev.sections():
		try:
			random[key] = int(confev[key]["random"])
		except KeyError:
			random[key] = 0


	while True:
		now = datetime.now()

		if (now.strftime("%H:%M") == confprg['misc']['party_ends'] and party) or first_run:
			with open (confprg['paths']['workdir'] + "party", "w") as f:
				f.write("No party")

		if (now.strftime("%H:%M") == "00:00") or first_run:

			# Update the variables
			sunrise, sunset, holid = get_cal_data.events(confprg, now)
			holiday_yesterday, holiday, holiday_tomorrow = get_holiday.free(confprg, holid, now, free_days, holidays)
			workday = not holiday
			weekday = True if 0 <= now.weekday() < 5 else False
			monday = True if now.weekday() == 0 else False
			tuesday = True if now.weekday() == 1 else False
			wednesday = True if now.weekday() == 2 else False
			thursday = True if now.weekday() == 3 else False
			friday = True if now.weekday() == 4 else False
			saturday = True if now.weekday() == 5 else False
			sunday = True if now.weekday() == 6 else False
			january = True if now.month == 1 else False
			february = True if now.month == 2 else False
			march = True if now.month == 3 else False
			april = True if now.month == 4 else False
			may = True if now.month == 5 else False
			june = True if now.month == 6 else False
			july = True if now.month == 7 else False
			august = True if now.month == 8 else False
			september = True if now.month == 9 else False
			october = True if now.month == 10 else False
			november = True if now.month == 11 else False
			december = True if now.month == 12 else False
			dst = True if time.localtime()[8] == 1 else False

			# Read the expressions for on
			for key in confev.sections():
				try:
					que[key] = confev[key]["id"] + ";" + rand_offset.calc(confev[key]["on"], random[key], sunrise, sunset)
				except KeyError:
					pass

			# Read the expressions for only_on
			for key in confev.sections():
				try:
					que_only_on[key] = confev[key]["id"] + ";" + rand_offset.calc(confev[key]["only_on"], random[key], sunrise, sunset)
				except KeyError:
					pass

			# Read the expressions for only_off
			for key in confev.sections():
				try:
					que_only_off[key] = confev[key]["id"] + ";" + rand_offset.calc(confev[key]["only_off"], random[key], sunrise, sunset)
				except KeyError:
					pass

		t = now.strftime("%H:%M")	# t is used as a variable in events.cfg
		sunup = True if sunrise <= t < sunset else False
		sundown = not sunup

		for host in confprg['ping_ip']:
			if host[0] != '#':
				pping[host] = True if os.system("ping -c 1 " + confprg['ping_ip'][host] + " > /dev/null") == 0 else False

		# Delay the state of ping to go from True to False
		for host in pping:
			if pping[host]:
				ping[host] = True
				ping_timer[host] = int(confprg['timer']['ping_off_delay'])
			elif (not pping[host]) and (ping_timer[host] > 0):
				ping_timer[host] -= 1
				ping[host] = True
			else:
				ping[host] = False

		# Party time?
#		with open (confprg['paths']['workdir'] + "party", "r") as f:
#			party = f.read()
#		f.close()
#		party = True if party == "party" else False
		party = False

		# Operate switches, if there's time for a change
		# On
		for item in que:
			state = eval(que[item].split(';')[1])
			if str(state) != old_state[item].split(';')[1]:
				sstate = "--on" if state else "--off"
				cmd = "tdtool " + sstate + " " + que[item].split(';')[0] + " > /dev/null"
				if verbose:
					print(now.strftime("%Y-%m-%d %H:%M") + "\t" + item + " " * (24 - len(item)) + sstate.replace('-', ''))
				thread[item] = Thread(target=operate_switch.switch, args=(confprg,cmd,sim,))
				thread[item].start()
			old_state[item] = que[item].split(';')[0] + ";" + str(state)

		# Only on
		for item in que_only_on:
			state = eval(que_only_on[item].split(';')[1])
			if state:
				if verbose:
					print(now.strftime("%Y-%m-%d %H:%M") + "\t" + item + " " * (24 - len(item)) + "on")
				cmd = "tdtool --on " + que_only_on[item].split(';')[0] + " > /dev/null"
				thread[item] = Thread(target=operate_switch.switch, args=(confprg,cmd,sim,))
				thread[item].start()
	
        # Only off
		for item in que_only_off:
			state = eval(que_only_off[item].split(';')[1])
			if state:
				if verbose:
					print(now.strftime("%Y-%m-%d %H:%M") + "\t" + item + " " * (24 - len(item)) + "off")
				cmd = "tdtool --off " + que_only_off[item].split(';')[0] + " > /dev/null"
				thread[item] = Thread(target=operate_switch.switch, args=(confprg,cmd,sim,))
				thread[item].start()

		first_run = False
		
		while now.strftime("%M") == datetime.now().strftime("%M"):
			time.sleep(1)

if __name__ == "__main__":
    main()
