#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2016 Thomas Elfström
# readfile.py

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
import os.path
import socket
import time


def main():
    files = {'party': '/run/shm/data/party'}
    default = {'party': 'False'}
    server_address = ('localhost', 8001)
    read_interval = 60

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(server_address)

    ownfile = os.path.basename(__file__)

    while True:
        for key in files:
            if os.path.isfile(files[key]):
                with open(files[key], "r") as f:
                    message = ownfile + ";" + key + ";" + f.readline()
            else:
                message = ownfile + ";" + key + ";" + default[key]
            s.send(bytes(message + "\n", 'UTF-8'))
        time.sleep(read_interval)

if __name__ == "__main__":
    main()
