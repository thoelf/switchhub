#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2016 Thomas Elfström
# sensor_receiver.py

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
import subprocess
import time
from threading import Thread


class monostable_onoff_sensor:
    def __init__(self, sensor_data):
        self.sensor_data = sensor_data
        self.name = sensor_data['name']
        self.state = sensor_data['initial_state']
        self.bounce_filter_time = sensor_data['bounce_filter_time']
        self.time_to_rest = sensor_data['time_to_rest']
        self.extend_time_to_rest = sensor_data['extend_time_to_rest']
        self.rest_timer = time.monotonic()
        self.bounce_filter_timer = time.monotonic()

    def set(self):
        if time.monotonic() > self.bounce_filter_time + self.bounce_filter_timer:
            if not self.state or (self.state and self.extend_time_to_rest):
                self.rest_timer = time.monotonic()
            self.state = True
            self.bounce_filter_timer = time.monotonic()

    def reset(self):
        if time.monotonic() > self.bounce_filter_time + self.bounce_filter_timer:
            self.state = False
            self.rest_timer = time.monotonic()
            self.bounce_filter_timer = time.monotonic()

    def check_if_str_set(self, strline):
        if self.sensor_data['str_set'] != None:
            return(strline in self.sensor_data['str_set'])
        else:
            return(False)

    def check_if_str_reset(self, strline):
        if self.sensor_data['str_reset'] != None:
            return(strline in self.sensor_data['str_reset'])
        else:
            return(False)

    def check_state(self):
        if self.state and time.monotonic() > self.rest_timer + self.time_to_rest:
            self.state = False
        return(self.state)


class bistable_onoff_sensor:
    def __init__(self, sensor_data):
        self.sensor_data = sensor_data
        self.name = sensor_data['name']
        self.state = sensor_data['initial_state']
        self.bounce_filter_time = sensor_data['bounce_filter_time']
        self.toggle_on_input = sensor_data['toggle_on_input']
        self.bounce_filter_timer = time.monotonic()

    def set(self):
        if time.monotonic() > self.bounce_filter_time + self.bounce_filter_timer:
            if self.toggle_on_input and self.state:
                self.state = False
            else:
                self.state = True
            self.bounce_filter_timer = time.monotonic()

    def reset(self):
        if time.monotonic() > self.bounce_filter_time + self.bounce_filter_timer:
            if self.toggle_on_input and not self.state:
                self.state = True
            else:
                self.state = False
            self.bounce_filter_timer = time.monotonic()

    def check_if_str_set(self, strline):
        if self.sensor_data['str_set'] != None:
            return(strline in self.sensor_data['str_set'])
        else:
            return(False)

    def check_if_str_reset(self, strline):
        if self.sensor_data['str_reset'] != None:
            return(strline in self.sensor_data['str_reset'])
        else:
            return(False)

    def check_state(self):
        return(self.state)


def send_data(sensor_obj):
    ownfile = os.path.basename(__file__)
    # Connect to server
    server_address = ('localhost', 8001)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(server_address)
    old_states = {}
    for sensor in sensor_obj:  # Send fast once
        old_states.update({sensor.name: sensor.check_state()})
        s.send(bytes(ownfile + ";" + sensor.name + ";" + str(sensor.check_state()) + "\n", 'UTF-8'))
#S		print(ownfile + ";" + sensor.name + ";" + str(sensor.check_state())
    while True:
        for sensor in sensor_obj:
            state = sensor.check_state()
            if state != old_states[sensor.name]:
                if state:
#					print(ownfile + ";" + sensor.name + ";True\n")
                    s.send(bytes(ownfile + ";" + sensor.name + ";True\n", 'UTF-8'))
                else:
#					print(ownfile + ";" + sensor.name + ";False\n")
                    s.send(bytes(ownfile + ";" + sensor.name + ";False\n", 'UTF-8'))
                old_states[sensor.name] = state
        time.sleep(0.25)


def main():
    button = {"name": "button",
                    "type": "bistable",
                    "initial_state": False,
                    "bounce_filter_time": 5,
                    "toggle_on_input": True,  # Toggle on any valid input
                    "str_set": (
                    "16:TDRawDeviceEvent94:class:command;protocol:arctech;model:selflearning;house:19706470;unit:1;group:1;method:turnon;i2s",
                    "16:TDRawDeviceEvent78:class:command;protocol:sartano;model:codeswitch;code:1111001001;method:turnon;i2s",
                    "16:TDRawDeviceEvent88:class:command;protocol:everflourish;model:selflearning;house:2854;unit:2;method:turnoff;i2s",
                    "16:TDRawDeviceEvent94:class:command;protocol:arctech;model:selflearning;house:20765430;unit:1;group:1;method:turnon;i2s",
                    "16:TDRawDeviceEvent88:class:command;protocol:everflourish;model:selflearning;house:3503;unit:2;method:turnoff;i2s",
                    "16:TDRawDeviceEvent88:class:command;protocol:everflourish;model:selflearning;house:3503;unit:2;method:turnoff;i2s"),
                    "str_reset": None}

    light_outdoors = {"name": "light_outdoors",
                    "type": "bistable",
                    "initial_state": False,
                    "bounce_filter_time": 5,
                    "toggle_on_input": False,
                    "str_set": ("16:TDRawDeviceEvent95:class:command;protocol:arctech;model:selflearning;house:18248602;unit:10;group:0;method:turnon;i2s",
                    "16:TDRawDeviceEvent79:class:command;protocol:sartano;model:codeswitch;code:0110011010;method:turnoff;i2s"),
                    "str_reset": ("16:TDRawDeviceEvent96:class:command;protocol:arctech;model:selflearning;house:23491482;unit:10;group:0;method:turnoff;i2s",
                    "16:TDRawDeviceEvent79:class:command;protocol:sartano;model:codeswitch;code:0110111010;method:turnoff;i2s")}

    motion_sovrum = {"name": "motion_sovrum",
                    "type": "monostable",
                    "initial_state": False,
                    "bounce_filter_time": 5,
                    "time_to_rest": 300,
                    "extend_time_to_rest": True,
                    "str_set": ("16:TDRawDeviceEvent94:class:command;protocol:arctech;model:selflearning;house:7839730;unit:16;group:0;method:turnon;i2s",
                    "16:TDRawDeviceEvent88:class:command;protocol:everflourish;model:selflearning;house:14847;unit:1;method:turnon;i2s"),
                    "str_reset": None}

    # List of on/off-sensors
    onoff_sensors = (button, light_outdoors, motion_sovrum)

    # Create sensor objects
    sensor_obj = []
    for sensor in onoff_sensors:
        if sensor['type'] == "monostable":
            s_obj = monostable_onoff_sensor(sensor)
        else:  # bistable
            s_obj = bistable_onoff_sensor(sensor)
        sensor_obj.append(s_obj)

    Thread(target = send_data, args = (sensor_obj,)).start()

#	cmd = "stdbuf -i0 -o0 -e0 python2 callbacks.py"
#	proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)
    cmd = "/opt/switchhub/plugins/signal_receiver.php"
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    stdout = []

    while True:
        line = proc.stdout.readline()
        stdout.append(line)
        strline = line.decode('UTF-8').rstrip()

        for sensor in sensor_obj:
            if sensor.check_if_str_set(strline):
                sensor.set()
                break  # Stop after match
            elif sensor.check_if_str_reset(strline):
                sensor.reset()
                break  # Stop after match

        if line == '' and proc.poll() is not None:
            break
    return ''.join(stdout)

if __name__ == "__main__":
    main()
