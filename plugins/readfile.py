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

#import configparser
#import codecs
import os.path

def main():
    #variable names and paths to the files with the data
    files = {"party": "/run/shm/data/party", \
    "weather_type": "/run/shm/data/weather_type"}

    #Default values, just in case there's no data in the files, or no files
    values = {"party": "False", "weather_type": "Clear"}

    for var, fil in files.items():
        if os.path.isfile(fil):
            with open(fil, "r") as f:
                print("readfile.py;" + var + ";" + f.readline())
        else:
            print("readfile.py;" + var + ";" + values[var])



#    files = {}

#    confreadfiles = configparser.ConfigParser()
#    confreadfiles.readfp(codecs.open("/etc/switchhub/plugins/readfile", "r", "utf8"))

#    with open("/etc/switchhub/plugins/readfile", "r") as f:
#        for item in confreadfiles['files']:
#            try:
#                with open(confreadfiles['files'][item], "r") as varf:
#                    print("readfile.py;" + item + ";" + varf.readline())
#            except:
#                pass

if __name__ == "__main__":
    main()
