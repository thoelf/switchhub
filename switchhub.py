#!/usr/bin/python3
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
import subprocess
from subprocess import Popen
import sys
from threading import Thread
import time
import logging
import re

import operate_switch
import get_plugin_data


def main():

	# Initialize config parser for program.cfg
	confprg = configparser.ConfigParser()
#	confprg.read("program.cfg")
	confprg.readfp(codecs.open("/etc/switchhub/switchhub", "r", "utf8"))

	# Initialize config parser for events.cfg
	confev = configparser.ConfigParser(allow_no_value = True)
#	confev.read("events.cfg")
	confev.readfp(codecs.open(confprg['misc']['event_config'] + "events", "r", "utf8"))

	# Initialize logging
	logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
		datefmt='%Y-%m-%d %H:%M:%S',
		filename="/var/log/switchhub.log")
	logger = logging.getLogger(__name__)
	logger.setLevel(confprg['logging']['log_level'])

	logger.info('SwitchHub started')
	first_run = True
	que = {}
	que_only_on = {}
	que_only_off = {}
	que_dim = {}
	old_state = {}
	pping = {}
	ping = {}
	ping_timer = {}
	plugin_data = {}
	plugin_data_old = {}
#	random = {}
	sim = False
	thread = {}
	dimmer = {}
	dimmer_old = {}
	diff_dim = {}
	for host in confprg['ping_ip']:
		ping_timer[host] = 0
	plugin_dirs = ["/opt/switchhub/plugins/1_minute/",
					"/opt/switchhub/plugins/15_minutes/",
					"/opt/switchhub/plugins/hour/",
					"/opt/switchhub/plugins/day/"]

	# Initialize old_state for on that is used to see if the state for on has been changed
	for key in confev.sections():
		old_state[key] = confev[key]['id'] + ";Old on state"

	# Read the random settings for the devices from the events definitions file
#	for key in confev.sections():
#		try:
#			random[key] = int(confev[key]["random"])
#		except KeyError:
#			random[key] = 0

	print("SwitchHub started.\n")
	print("If you started SwitchHub with switchhub.sh start,\npress Ctrl+A D to detach SwitchHub from the terminal.\n")

	while True:
		now = datetime.now()

		###Get data from the plugins. First, determine depending on the time, which directories to look for plugins in.
		# Each day at 00:00 or at first run, look in all directories
		if (now.strftime("%H:%M") == "00:00") or first_run: 
			x = 4
		# Each full hour, look in the directories hour, 15_minutes and 1_minute.
		elif (now.strftime("%M") == "00"):
			x = 3
		# Each full quarter, look in the directories 15_minutes and 1_minute.
		elif (now.strftime("%M") == "15") or (now.strftime("%M") == "30") or (now.strftime("%M") == "45"):
			x = 2
		# Each full minute, look in the directory 1_minute
		else:
			x = 1
		plugin_data = get_plugin_data.data(plugin_dirs, first_run, logger, plugin_data, x)
		logger.debug("Plugin data: {0}".format(plugin_data))

		if (now.strftime("%H:%M") == "00:00") or first_run: # or not data_read:
			# Update variables
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

		# Re-build the event expressions each time there is new plug-in data or at first run.
		if (plugin_data_old != plugin_data) or first_run:
			plugin_data_old = {}
			for key in plugin_data:
				plugin_data_old[key] = plugin_data[key]
			# Read the expressions for on
			for key in confev.sections():
				try:
					que[key] = confev[key]["id"] + ";" + confev[key]["on"]
					# Replace e.g. 22:30 with '22:30'
					que[key] = re.sub(r'([0-2][0-9]:[0-5][0-9])', r"'\1'", que[key])
					# Replace e.g. ping:sven with ping['sven']
					que[key] = re.sub(r'(ping:)([A-Za-z0-9\-\_]+)', r"ping['\2']", que[key])
					# In event definition, replace variable name from plugins with "plugin_data['variable name']"
					for pkey in plugin_data.keys():
						if pkey in que[key]:
							que[key] = re.sub("\\b" + pkey + "\\b", plugin_data[pkey], que[key])
							que[key] = re.sub(r'([0-2][0-9]:[0-5][0-9])', r"'\1'", que[key])
							que[key] = re.sub(r"'+", r"'", que[key])
				except KeyError:
					pass

			# Read the expressions for only_on
			for key in confev.sections():
				try:
					que_only_on[key] = confev[key]["id"] + ";" + confev[key]["only_on"]
					que_only_on[key] = re.sub(r'([0-2][0-9]:[0-5][0-9])', r"'\1'", que_only_on[key])
					que_only_on[key] = re.sub(r'(ping:)([A-Za-z0-9\-\_]+)', r"ping['\2']", que_only_on[key])
					# In event definition, replace variable name from plugins with "plugin_data['variable name']"
					for pkey in plugin_data.keys():
						if pkey in que_only_on[key]:
							que_only_on[key] = re.sub("\\b" + pkey + "\\b", plugin_data[pkey], que_only_on[key])
							que_only_on[key] = re.sub(r'([0-2][0-9]:[0-5][0-9])', r"'\1'", que_only_on[key])
							que_only_on[key] = re.sub(r"'+", r"'", que_only_on[key])
				except KeyError:
					pass

			# Read the expressions for only_off
			for key in confev.sections():
				try:
#					que_only_off[key] = confev[key]["id"] + ";" + rand_offset.calc(confev[key]["only_off"], random[key], sunrise, sunset)
					que_only_off[key] = confev[key]["id"] + ";" + confev[key]["only_off"]
					que_only_off[key] = re.sub(r'([0-2][0-9]:[0-5][0-9])', r"'\1'", que_only_off[key])
					que_only_off[key] = re.sub(r'(ping:)([A-Za-z0-9\-\_]+)', r"ping['\2']", que_only_off[key])
					# In event definition, replace variable name from plugins with "plugin_data['variable name']"
					for pkey in plugin_data.keys():
						if pkey in que_only_off[key]:
							que_only_off[key] = re.sub("\\b" + pkey + "\\b", plugin_data[pkey], que_only_off[key])
							que_only_off[key] = re.sub(r'([0-2][0-9]:[0-5][0-9])', r"'\1'", que_only_off[key])
							que_only_off[key] = re.sub(r"'+", r"'", que_only_off[key])
				except KeyError:
					pass

			# Read the expressions for dim_<0-100>
			for key in confev.sections():	#key = aquarium etc
				try:
					for value in confev.options(key):	#för varje option (t ex dim_25, only_on etc)
						match = re.match(r'(dim_)(\d{1,3})', value)
						if match:
#							print(confev[key]["id"] + ";" + confev[key][value] + ";" + match.group(2) + ";" + key)
							que_dim[key + value] = confev[key]["id"] + ";" + confev[key][value] + ";" + match.group(2) + ";" + key
							que_dim[key + value] = re.sub(r'([0-2][0-9]:[0-5][0-9])', r"'\1'", que_dim[key + value])
							que_dim[key + value] = re.sub(r'(ping:)([A-Za-z0-9\-\_]+)', r"ping['\2']", que_dim[key + value])
							# In event definition, replace variable name from plugins with "plugin_data['variable name']"
							for pkey in plugin_data.keys():
								if pkey in que_dim[key + value]:
									que_dim[key + value] = re.sub("\\b" + pkey + "\\b", plugin_data[pkey], que_dim[key + value])
									que_dim[key + value] = re.sub(r'([0-2][0-9]:[0-5][0-9])', r"'\1'", que_dim[key + value])
									que_dim[key + value] = re.sub(r"'+", r"'", que_dim[key + value])
				except KeyError:
					pass


		t = now.strftime("%H:%M")	# t is used as a variable in events.cfg

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

		# Operate switches, if there's time for a change
		# On
		for item in que:
			state = eval(que[item].split(';')[1])
			logger.debug("{0}, {1}, {2}".format(item, str(state), que[item].split(';')[1]))
			if str(state) != old_state[item].split(';')[1]:
				sstate = "--on" if state else "--off"
				cmd = "tdtool " + sstate + " " + que[item].split(';')[0] + " > /dev/null"
				logger.info("State change in que {0} {1}".format(item, sstate.replace('-', '')))
				print(now.strftime("%Y-%m-%d %H:%M") + "\t" + item + " " * (24 - len(item)) + sstate.replace('-', ''))

				with open("/run/shm/data/" + "switch_" + item, "w") as f:
					f.write(sstate.replace('-', ''))

				thread[item] = Thread(target=operate_switch.switch, args=(confprg,cmd,sim,))
				thread[item].start()
			old_state[item] = que[item].split(';')[0] + ";" + str(state)

		# Only on
		for item in que_only_on:
			state = eval(que_only_on[item].split(';')[1])
			logger.debug("{0}, {1}, {2}".format(item, str(state), que_only_on[item].split(';')[1]))
			if state:
				logger.info("State change in que_only_on {0} on", item)
				print(now.strftime("%Y-%m-%d %H:%M") + "\t" + item + " " * (24 - len(item)) + "on")

				with open("/run/shm/data/" + "switch_" + item, "w") as f:
					f.write(sstate.replace('-', ''))

				cmd = "tdtool --on " + que_only_on[item].split(';')[0] + " > /dev/null"
				thread[item] = Thread(target=operate_switch.switch, args=(confprg,cmd,sim,))
				thread[item].start()
	
        # Only off
		for item in que_only_off:
			state = eval(que_only_off[item].split(';')[1])
			logger.debug("{0}, {1}, {2}".format(item, str(state), que_only_off[item].split(';')[1]))
			if state:
				logger.info("State change in que_only_off {0} off".format(item))
				print(now.strftime("%Y-%m-%d %H:%M") + "\t" + item + " " * (24 - len(item)) + "off")

				with open("/run/shm/data/" + "switch_" + item, "w") as f:
					f.write(sstate.replace('-', ''))

				cmd = "tdtool --off " + que_only_off[item].split(';')[0] + " > /dev/null"
				thread[item] = Thread(target=operate_switch.switch, args=(confprg,cmd,sim,))
				thread[item].start()


		# Dim
		for item in que_dim:
			dimmer[que_dim[item].split(';')[0]] = 0  # All dim values for all id's are set to zero
		for item in que_dim:
			#For each item (e.g. lampdim_10), dimmer[id] = the value, if the expression if true, otherwise unchanged
			if eval(que_dim[item].split(';')[1]):
				if int(dimmer[que_dim[item].split(';')[0]]) < int(que_dim[item].split(';')[2]):
					dimmer[que_dim[item].split(';')[0]] = que_dim[item].split(';')[2] 

		if first_run:
			dimmer_old = dimmer.copy()
		
		for idno in dimmer:
			if (dimmer[idno] != dimmer_old[idno]) or first_run:
				if (dimmer[idno] != 0):
					logger.info("State change in dimmer id {0} set to {1}".format(idno, dimmer[idno]))
					cmd = "tdtool --dimlevel " + str(dimmer[idno]) + " --dim " + idno + " > /dev/null"
					print(now.strftime("%Y-%m-%d %H:%M") + "\t" + idno + " " * (24 - len(item)) + "dim " + str(dimmer[idno]))
				else:
					logger.info("State change in dimmer id {0} set to {1}".format(idno, dimmer[idno]))
					cmd = "tdtool --off " + idno + " > /dev/null"
					print(now.strftime("%Y-%m-%d %H:%M") + "\t" + idno + " " * (24 - len(item)) + "off")

				thread[item] = Thread(target=operate_switch.switch, args=(confprg,cmd,sim,))
				thread[item].start()

		dimmer_old = dimmer.copy()

		first_run = False
		
		while now.strftime("%M") == datetime.now().strftime("%M"):
			time.sleep(1)

if __name__ == "__main__":
    main()
