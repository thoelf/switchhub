#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2016 Thomas Elfström
# ping.py

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


import os
import socket
import time


def main():
	hosts = {'t': '192.168.1.100',
			't_lap': '192.168.1.101',
			't_n5': '192.168.1.155',
			'm_lap': '192.168.1.180',
			'm_n5x': '192.168.1.181'}

	server_address = ('localhost', 8001)
	ping_interval = 60

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(server_address)

	ownfile = os.path.basename(__file__)

	# Send fast once
	for host in hosts:
		message = ownfile + ";ping_" + host + ";False"
		s.send(bytes(message + "\n", 'UTF-8'))

	while True:
		t_end = time.monotonic() + ping_interval
		for host in hosts:
			ping = True if os.system("ping -c 1 " + hosts[host] + " > /dev/null") == 0 else False
			message = ownfile + ";ping_" + host + ";" + str(ping)
			s.send(bytes(message + "\n", 'UTF-8'))
		while time.monotonic() < t_end:
			time.sleep(1)

if __name__ == "__main__":
	main()
