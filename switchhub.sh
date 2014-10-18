#!/usr/bin/env bash
#Copyright 2014 Thomas Elfström
#switchhub.sh

# This file is part of SwitchHub.

# SwitchHub is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# SwitchHub is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with SwitchHub. If not, see <http://www.gnu.org/licenses/>.

start () {
if [[ ! $(pgrep -f switchhub.py) ]]; then
    screen /opt/switchhub/switchhub.py
else
    printf "Switchhub is already running. Doing nothing.\n"
fi
}

stop () {
if [[ $(pgrep -f switchhub.py) ]]; then
    printf "Killing switchhub.\n"
    pkill -f switchhub
else
    printf "Switchhub is not running. Doing nothing.\n"
fi
}

status () {
if [[ $(pgrep -f switchhub.py) ]]; then
    printf "Switchhub is running with PID: %s\n" $(pgrep -f switchhub.py)
else
    printf "\nSwitchhub is not running.\n"
fi
}

case $1 in
    start)	start ;;
    stop)	stop ;;
    status)	status ;;
    *)      printf "Usage: switchhub.sh [start|stop|status]\n"
            exit 1 ;;
esac

#unset status
