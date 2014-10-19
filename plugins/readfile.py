#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2014 Thomas Elfström
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

import configparser
import codecs
import os.path

def main():

	# Initialize config parser for the readfiles settings file
    confreadfile = configparser.ConfigParser()
    confreadfile.readfp(codecs.open("/etc/switchhub/plugins/readfile", "r", "utf8"))

    for fil in confreadfile['files']:
        if os.path.isfile(confreadfile['files'][fil]):
            with open(confreadfile['files'][fil], "r") as f:
                print("readfile.py;" + fil + ";" + f.readline())
        else:                
            print("readfile.py;" + fil + ";" + confreadfile['default'][fil])

if __name__ == "__main__":
    main()
