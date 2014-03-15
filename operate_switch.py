#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2014 Thomas Elfström
# operate_switch.py

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

import random
import time
import subprocess


def switch(confprg,cmd,sim):
	# Repeat calls. Paus between calls, but not after the last one
	for i in range(0, int(confprg['misc']['repeats']) + 1):
		if not sim:
			subprocess.call([cmd], shell=True)
		if int(confprg['misc']['repeats']) + 1 > 1 and i < int(confprg['misc']['repeats']):
			time.sleep(random.uniform(0.5, 5))

