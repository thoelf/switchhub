#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2016 Thomas Elfström
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

import codecs
import configparser
import logging
import os
import queue
import random
import re
import select
import socket
import subprocess
import sys
import time
from datetime import datetime
from threading import Thread


class switch:
    def __init__(self, events):
        self.events = events
        self.name = events['name']
        self.events.pop('name')
        self.idno = events['id']
        self.events.pop('id')
        self.state = 0
        self.old_state = None
        self.eventsd = {}
#		for key in self.events.keys():
#			self.eventsd.update({key: events[key]})  # eventsd är dict med t ex 'on' och 'dim_50' som keys. data är eventuttryck
#		key_temp = {}
#		for key in self.eventsd.keys():  # byt namn på keys
#			if key == "only_on":
#				key_temp.update({key: "1001"})
#			elif key == "on":
#				key_temp.update({key: "1000"})
#			elif key == "only_off":
#				key_temp.update({key: "0"})
#			else:
#				key_temp.update({key: re.sub(r'dim_', "", key)})
#		for key in key_temp.keys():
#			self.eventsd[key_temp[key]] = self.eventsd.pop(key)

    def update(self, timestamp, t, plugin_data):
        for key in self.events.keys():
            self.eventsd.update({key: self.events[key]})  # eventsd är dict med t ex 'on' och 'dim_50' som keys. data är eventuttryck
        key_temp = {}
        for key in self.eventsd.keys():  # Change key names
            if key == "only_on":
                key_temp.update({key: "1001"})
            elif key == "on":
                key_temp.update({key: "1000"})
            elif key == "only_off":
                key_temp.update({key: "0"})
            else:
                key_temp.update({key: re.sub(r'dim_', "", key)})
        for key in key_temp.keys():
            self.eventsd[key_temp[key]] = self.eventsd.pop(key)

        for key in self.eventsd:
            for pkey in plugin_data:
                if pkey in self.eventsd[key]:
                    self.eventsd[key] = re.sub("\\b" + pkey + "\\b", plugin_data[pkey], self.eventsd[key])
            self.eventsd[key] = re.sub(r'([0-2][0-9]:[0-5][0-9])', r"'\1'", self.eventsd[key])
            self.eventsd[key] = re.sub(r"'+", r"'", self.eventsd[key])
            self.eventsd[key] = re.sub(r'(\\+\n)', "", self.eventsd[key])

        only_on = False
        on = False
        dim_old = 0
        dim = 0
        only_off = False
#		for key in sorted(self.eventsd):
        for key in self.eventsd:
            if key == "1001" and eval(self.eventsd[key]):
                only_on = True
            elif key == "1000" and eval(self.eventsd[key]):
#				print(key, eval(self.eventsd[key]), self.eventsd[key])
                on = True
            elif (1 <= int(key) <= 999) and eval(self.eventsd[key]) and int(key) > int(dim_old):
                dim = key
                dim_old = dim
            elif key == "0" and eval(self.eventsd[key]):
                only_off = True

        if self.state == 0:
            if on:
                self.state = 2
            elif only_on and not on and not only_off and not dim:
                self.state = 3
            elif dim and not on:
                self.state = 4
            elif only_off and not on and not only_on and not dim:
                self.state = 5
        elif self.state == 1:
            if on:
                self.state = 2
            elif only_on and not on and not only_off and not bool(dim):
                self.state = 3
            elif bool(dim) and not on:
                self.state = 4
            elif only_off and not on and not only_on and not bool(dim):
                self.state = 5
        elif self.state == 2:
            if not on and not bool(dim):
                self.state = 1
            elif bool(dim) and not on:
                self.state = 4
            elif only_off and not on and not only_on and not bool(dim):
                self.state = 5
        elif self.state == 3:
            if on:
                self.state == 2
            elif bool(dim) and not on:
                self.state = 4
            elif only_off and not bool(dim) and not only_on and not on:
                self.state = 5
            else:
                self.state = 0
        elif self.state == 4:
            if not bool(dim) and not on:
                self.state = 1
            elif on:
                self.state = 2
            elif only_off and not on and not only_on and not bool(dim):
                self.state = 5
        else:  #elif self.state == 5:
            if on:
                self.state = 2
            elif only_on and not bool(dim) and not only_off and not on:
                self.state = 3
            elif bool(dim) and not on:
                self.state = 4
            else:
                self.state = 0

        cmd = ""
        if self.state != self.old_state:
            if self.state == 0:
                print(timestamp + "  " + self.name + " " * (20 - len(self.name)) + " waiting")
            elif self.state == 2 or self.state == 3:
                cmd = "tdtool --on " + self.idno + " > /dev/null"
                print(timestamp + "  " + self.name + " " * (20 - len(self.name)) + " on")
            elif self.state == 4:
                cmd = "tdtool --dimlevel " + str(dim) + " --dim " + self.idno + " > /dev/null"
                print(timestamp + "  " + self.name + " " * (20 - len(self.name)) + " dim " + str(dim))
            else:  # elif self.state == 1 or self.state == 5:
                cmd = "tdtool --off " + self.idno + " > /dev/null"
                print(timestamp + "  " + self.name + " " * (20 - len(self.name)) + " off")
        self.old_state = self.state
        return(cmd)

# varför två on states och två off states... för att inte gå till off efter att only_on gått från True till False och vice versa för only_off


def main():

    print("\n********************** \033[92mSWITCHHUB\033[0m **********************\n")
    print("If you started SwitchHub with 'switchhub.sh start',\npress 'Ctrl+A D' to detach SwitchHub from the terminal.\n")

    # Initialize config parser for program.cfg
    confprg = configparser.ConfigParser(allow_no_value = True)
    confprg.readfp(codecs.open("/etc/switchhub/switchhub", "r", "utf8"))

    # Read the switchhub configuration file
    log_level = confprg['settings']['log_level']
    transmits = int(confprg['settings']['transmits'])
    events_dir = confprg['settings']['event_config']
    receive_buf = int(confprg['settings']['receive_buf'])
    port = int(confprg['settings']['port'])
    plugin_wait = int(confprg['settings']['wait for plugins'])
    plugins = []
    for plugin in list(confprg['plugins'].items()):
        plugins.append(plugin[1])
    plugins.sort()

    # Initialize config parser for events.cfg
    confev = configparser.ConfigParser(allow_no_value = True)
    confev.readfp(codecs.open(events_dir + "events", "r", "utf8"))

    # Initialize logging
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filename="/var/log/switchhub.log")
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)
    logger.info('SwitchHub started')

    global data
    data = 0
    global first_run
    first_run = True
    nu = datetime.now()
    que = {}
    que_only_on = {}
    que_only_off = {}
    que_dim = {}
    old_state = {}
    global plugin_data
    plugin_data = {}
    plugin_data_old = {"just":"anything"}
    sim = False
    thread = {}
    dimmer = {}
    dimmer_old = {}


    def operate_switch(cmd, transmits, sim):
        for i in range(transmits):
            if not sim:
                subprocess.call([cmd], shell=True)
                time.sleep(random.uniform(0.5, 5))

    def socket_server():
        global data
        global first_run
        global plugin_data
        while inputs:
            # Wait for at least one of the sockets to be ready for processing
            readable, writable, exceptional = select.select(inputs, outputs, inputs)
            time.sleep(0.1)  # If no delay, CPU runs at nearly 100 %
            # Handle inputs
            for s in readable:
                if s is server:
            # A "readable" server socket is ready to accept a connection
                    connection, client_address = s.accept()
                    connection.setblocking(0)
                    inputs.append(connection)
                # Give the connection a queue for data we want to send
                    message_queues[connection] = queue.Queue()
                else:
                    data = s.recv(receive_buf)
                    if data:
                # A readable client socket has data
                        message_queues[s].put(data)
                        #for line in lines.splitlines():
                        for line in ((data).decode('UTF-8')).splitlines():
                            if line.strip():
                                if (len(line.split(";")) == 3):  # and (f == line.split(";")[0]):
                                    plugin = line.split(";")[0]
                                    var_name = line.split(";")[1]
                                    if first_run:
                                        first_char = var_name[0]
                                        if first_char.isdigit():
                                            logger.critical("The variable {0} from the plugin {1} starts with a digit! Alphanumeric character was expected.".format(var_name, plugin))
                                            print("CRITICAL: The variable {0} from the plugin {1}\nstarts with a digit! Alphanumeric character was expected.".format(var_name, plugin))
                                            sys.exit()
                                    var_value = line.split(";")[2]
                                    if first_run and (var_name in locals() or var_name in globals()):
                                        logger.critical("The variable {0} from the plugin {1} is already in use!".format(var_name, plugin))
                                        print("CRITICAL: The variable {0} from the plugin {1} is already in use!".format(var_name, plugin))
                                        sys.exit()
                                    plugin_data[var_name] = var_value
#									logger.debug("From plugin {0}, plugin_data['{1}'] = {2}.".format(plugin, var_name, var_value))
                                else:
                                    logger.info("Bogous data was read and discarded from plugin {0}.".format(plugin))

                # Add output channel for response
                        if s not in outputs:
                            outputs.append(s)

    # Create a TCP/IP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(0)

    # Bind the socket to the port
    server_address = ('localhost', port)
    print(("Starting plugin server on {0} port {1}.\n".format(server_address[0], server_address[1])))
    server.bind(server_address)
    server.listen(5)  # Listen for incoming connections
    inputs = [server]  # Sockets from which we expect to read
    outputs = []  # Sockets to which we expect to write
    message_queues = {}  # Outgoing message queues (socket:Queue)

    Thread(target = socket_server).start()

    #start any plugins
    if plugins:
        print("Starting plugins:")
        for plugin in plugins:
            subprocess.Popen([plugin], stdout=subprocess.DEVNULL)
            print((" * " + os.path.basename(plugin)))
        print("\n")
        time.sleep(plugin_wait)
    else:
        print("No plugins to start. Using time (t) as the only variable.\n")

    # Create switch objects with their own event list
    # Create dict with events idno:expr
    eventdict = {}
    for section in confev.sections():
        sectiondict = {}
        sectiondict.update({"name": section})
        sectiondict.update({'id': confev[section]['id']})
        if confev[section]['id']:
            for (key, val) in confev.items(section):
                if key != "id":
                    sectiondict.update({key: val})
            eventdict.update({confev[section]['id']: sectiondict})

    # Remove switches without events
    dicttemp = {}
    dicttemp.update(eventdict)
    for key in dicttemp.keys():
        if not dicttemp[key]:
            eventdict.pop(key)

    # Create a list of switch objects
    objectlist = []
    for key in eventdict.keys():
        x_obj = switch(eventdict[key])  # Crete an object per idno with an eventdict including events for the idno
        objectlist.append(x_obj)        # eventdict = dict with all events for the idno, and the idno and the name of the section, e.g. lamp bedroom


    while True:
        minutetimer = time.monotonic()
        while (plugin_data == plugin_data_old) and (time.monotonic() - minutetimer < 59.95):
            time.sleep(0.1)

        time_now = datetime.now()
        t = time_now.strftime("%H:%M")	# t is used as a variable in events.cfg
        timestamp = time_now.strftime("%Y-%m-%d") + "  " + time_now.strftime("%H:%M")

        # Re-build the event expressions each time there is new plug-in data or at first run.
        if (plugin_data_old != plugin_data):
            plugin_data_old.clear()
            plugin_data_old.update(plugin_data)
        # Update the objects with new data. The objects decides if their states are to be changed
        for count in range(len(objectlist)):
            cmd = objectlist[count].update(timestamp, t, plugin_data)
            if cmd:
                Thread(target = operate_switch, args = (cmd, transmits, sim)).start()

if __name__ == "__main__":
    main()
