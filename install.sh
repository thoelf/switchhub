#!/usr/bin/env bash
#Copyright 2014 Thomas Elfström
#install.sh

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


resize -s 42 92 &> /dev/null

echo -ne "\033]0;SwitchHub installation\007"
clear

if [[ $(id -u) -ne 0 ]]; then
    printf "Error: Run as root or with sudo.\n"
    exit 1
fi

INSTALL_DIR=/opt/switchhub
PLUGINS_DIR=/opt/switchhub/plugins
LOG_FILE=/var/log/switchhub.log
SETTINGS_DIR=/etc/switchhub
SETTINGS_DIR_PLUGINS=/etc/switchhub/plugins
STARTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
USER=$(logname)

printf "You are about to install SwitchHub for user $USER.\nEnter 'C' to change user or any other key to continue. "
read ANSWER
if [[ "$ANSWER" = [cC] ]]; then
    printf "\nFor which user do you want to install SwitchHub? "
    read USER
    UEXIST="false"
    while [[ "$UEXIST" = "false" ]] || [[ "$USER" = "" ]]; do
        getent passwd "$USER" >/dev/null 2>&1 && UEXIST="true"
        if [ "$UEXIST" = "false" ] || [[ "$USER" = "" ]]; then
            printf "Error: User $USER does not exist!"
            printf "\n\nFor which user are you installing SwitchHub? "
            read USER
        fi
    done
fi

GEXIST=false
getent group switchhub >/dev/null 2>&1 && GEXIST="true"
if [[ "$GEXIST" = "false" ]]; then
    groupadd switchhub
fi

chgrp -R switchhub *

if [[ -d "/etc/logrotate.d" ]]; then
    mv -v switchhub /etc/logrotate.d/switchhub
else
    printf "Warning: The directory /etc/logrotate.d/ does not exist. Could not copy the log rotate configuration file."
fi

mkdir -p "$SETTINGS_DIR"
cp ./configuration/events ./configuration/switchhub "$SETTINGS_DIR"
chgrp -R switchhub "$SETTINGS_DIR"
chmod -R g+w "$SETTINGS_DIR"

mkdir -p "$SETTINGS_DIR_PLUGINS"/gcalendar
cp ./configuration/gcalendar ./configuration/gcalendar_free_days ./configuration/gcalendar_holidays "$SETTINGS_DIR_PLUGINS"
chgrp -R switchhub "$SETTINGS_DIR_PLUGINS"
chmod -R g+w "$SETTINGS_DIR_PLUGINS"

mkdir -p "$INSTALL_DIR"
chgrp switchhub "$INSTALL_DIR"
chmod g+w "$INSTALL_DIR"

mkdir -p "$PLUGINS_DIR"
cp ./plugins/gcalendar.py "$PLUGINS_DIR"
chgrp -R switchhub "$PLUGINS_DIR"
chmod -R g+w "$PLUGINS_DIR"

mkdir -p "$PLUGINS_DIR"/1minute
chgrp switchhub "$PLUGINS_DIR"/1_minute
chmod g+w "$PLUGINS_DIR"/1minute

mkdir -p "$PLUGINS_DIR"/15minutes
chgrp switchhub "$PLUGINS_DIR"/15_minutes
chmod g+w "$PLUGINS_DIR"/15minutes

mkdir -p "$PLUGINS_DIR"/hour
chgrp switchhub "$PLUGINS_DIR"/hour
chmod g+w "$PLUGINS_DIR"/1hour

mkdir -p "$PLUGINS_DIR"/1day
chgrp switchhub "$PLUGINS_DIR"/day
chmod g+w "$PLUGINS_DIR"/1day

cp switchhub.py get_plugin_data.py operate_switch.py SwitchHub.pdf switchhub.sh LICENSE $INSTALL_DIR

chgrp -R switchhub "$INSTALL_DIR"/*
chmod -R g+w "$INSTALL_DIR"/*
chmod g+x "$INSTALL_DIR"/{switchhub.py,switchhub.sh}

if [[ ! -f "$LOG_FILE" ]]; then
    touch "$LOG_FILE"
fi

chgrp switchhub "$LOG_FILE"
chmod g+w "$LOG_FILE"

sudo usermod -a -G switchhub "$USER"

printf "\nThe installation directory is $INSTALL_DIR.\n"
printf "The configuration files are in the directory /etc/switchhub.\n"
printf "The log file is $LOG_FILE.\n"
printf "The configuration file for log rotation is /etc/logrotate.d/switchhub.\n"
printf "The group switchhub was created and $USER is now a member of that group.\n\n"
printf "Press any key to quit. "
read
