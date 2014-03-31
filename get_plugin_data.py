#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2014 Thomas Elfström
# get_plugin_data.py
#
# Reads a string on stdout in the format <plugin file name>;<variable name>;<variable value>
# from a plugin in /opt/switchhub/plugin/* and stores the variable name and the variable
# value in the dictionary plugin_data. '''

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

#def read_plugin_data

def data(plugin_dirs, first_run, logger, plugin_data, x):
#Gör trådade anrop
#	from threading import Thread
#	thread = {}
#	thread[item] = Thread(target=get_plugin_data.read_plugin_data, args=(plugin_dirs, first_run, logger, plugin_data, x,))
#	thread[item].start()

	import os
	import sys
	import subprocess
	import logging

	for directory in plugin_dirs[0:x]:
		for f in os.listdir(directory):
			stdoutdata = subprocess.check_output([directory + f], shell=True)
			lines = stdoutdata.decode("utf-8")
			for line in lines.splitlines():
				if line.strip():
					if (len(line.split(";")) == 3) and (f == line.split(";")[0]):
						plugin = line.split(";")[0]				
						var_name = line.split(";")[1]
						if first_run:
							first_char = var_name[0]
							if first_char.isdigit():
								logger.critical("The variable {0} from the plugin {1}{2} starts with a digit! Alphanumeric character was expected.".format(var_name, directory, f))
								print("CRITICAL: The variable {0} from the plugin {1}{2}\nstarts with a digit! Alphanumeric character was expected.".format(var_name, directory, f))
								sys.exit()			
						var_value = line.split(";")[2]
						if first_run and (var_name in locals() or var_name in globals()):
							logger.critical("The variable {0} from the plugin {1}{2} is already in use!".format(var_name, directory, f))
							print("CRITICAL: The variable {0} from the plugin {1}{2} is already in use!".format(var_name, directory, f))
							sys.exit()
						plugin_data[var_name] = var_value
						logger.debug("From plugin {0}{1}, plugin_data['{2}'] = {3}.".format(directory, f, var_name, var_value))
					else:
						logger.info("Bogous data was read and discarded from plugin {0}.".format(f))

	return plugin_data


## Kolla att variabeln uppfyller övriga krav, t ex ej börja med siffra
