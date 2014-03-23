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
LOG_FILE=/var/log/switchhub.log
SETTINGS_DIR=/etc/switchhub
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
    printf "\nAdded the group switchhub.\n"
fi

if [[ -d "/etc/logrotate.d" ]]; then
    mv -v switchhub_logrotate /etc/logrotate.d/switchhub
else
    printf "Warning: The directory /etc/logrotate.d/ does not exist. Could not copy the log rotate configuration file."
fi

mv -v events.cfg free_days.cfg holidays.cfg program.cfg "$SETTINGS_DIR"
chgrp switchhub "$SETTINGS_DIR"/*
chmod g+w "$SETTINGS_DIR"/*

chmod u+x switchhub_start switchhub_status switchhub_stop
cp -v switchhub_start switchhub_status switchhub_stop /home/$USER

if [[ ! -d "$SETTINGS_DIR" ]]; then
    mkdir -p "$SETTINGS_DIR"
    printf "Created the directory $SETTINGS_DIR."
fi

if [[ -d "$INSTALL_DIR" ]]; then
    rm -rf "$INSTALL_DIR"
    printf "Removed old install directory $INSTALL_DIR.\n"
fi

mkdir -p $INSTALL_DIR
printf "Created new program directory $INSTALL_DIR.\n"
cp -vr $STARTDIR/* $INSTALL_DIR
chown root:root "$INSTALL_DIR"

chgrp -R switchhub "$INSTALL_DIR"/*
chmod -R g+w "$INSTALL_DIR"/*
chmod g+x "$INSTALL_DIR"/switchhub.py

if [[ ! -f "$LOG_FILE" ]]; then
    touch "$LOG_FILE"
    printf "Created $LOG_FILE."
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
