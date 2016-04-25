#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2016 Thomas Elfström
# weather.py

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

import json
import os
import socket
import time
from urllib.request import urlopen


def main():
    weather_data_url = "http://api.wunderground.com/api/<your api key>/conditions/q/Sweden/Linkoping.json"
    var_Weather = "Clear"  # Assume clear weather
    weather_interval = 900

    ownfile = os.path.basename(__file__)

    server_address = ('localhost', 8001)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(server_address)

    try:
        data = urlopen(weather_data_url, timeout = 10).read().decode('utf-8')
    except:
        pass

    try:
        theJSON = json.loads(data)
        var_Weather =  theJSON['current_observation']['weather']
    except:
        pass

    s.send(bytes(ownfile + ";weather;{0}".format(var_Weather) + "\n", 'UTF-8'))
    time.sleep(weather_interval)

if __name__ == "__main__":
    main()
