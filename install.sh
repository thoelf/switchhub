#!/bin/bash
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


#resize -s 30 92 &> /dev/null

echo -ne "\033]0;SwitchHub installation\007"
clear

if [ $(id -u) -ne 0 ]; then
    printf "Run as root or with sudo.\n"
    exit 1
fi

INSTALL_DIR=/opt/switchhub/
LOG_FILE=/var/log/switchhub.log
SETTINGS_DIR=/etc/switchhub/

printf "You are about to install SwitchHub. "
printf "Press any key to continue the installation or Ctrl+C to quit."
read

GEXIST=false
getent group switchhub >/dev/null 2>&1 && GEXIST="true"
if [ "$GEXIST" == "false" ]; then
    groupadd switchhub
    printf "\nAdded the group switchhub.\n"
fi

cd ..
mv -v switchhub-master switchhub

if [ ! -d "/etc/switchhub" ]; then
    mkdir $SETTINGS_DIR
    printf "Created the directory $SETTINGS_DIR"
fi

mv -v ./switchhub/{events.cfg,free_days.cfg,holidays.cfg,program.cfg} $SETTINGS_DIR
chgrp switchhub $SETTINGS_DIR*
chmod g+w $SETTINGS_DIR*

mv -v ./switchhub/{switchhub_start,switchhub_status,switchhub_stop} .
chmod u+x switchhub_start switchhub_status switchhub_stop

if [ -d "$INSTALL_DIR" ]; then
    rm -rf $INSTALL_DIR
    printf "Removed old install directory $INSTALL_DIR\n"
fi

mv -v switchhub /opt
printf "Created new install directory $INSTALL_DIR\n"
chown root:root $INSTALL_DIR

cd $INSTALL_DIR
chgrp -R switchhub *
chmod -R g+w *
chmod g+x switchhub.py

mv -v switchhub_logrotate /etc/logrotate.d/switchhub

if [ ! -f "$LOG_FILE" ]; then
    touch $LOG_FILE
    printf "Created $LOG_FILE"
fi

chgrp switchhub $LOG_FILE
chmod g+w $LOG_FILE

cd

printf "\nThe installation was succesful! \n"
printf "The installation directory is: $INSTALL_DIR\n"
printf "The configuration files are in the directory /etc/switchhub.\n"
printf "The log file is: $LOG_FILE\n"
printf "The configuration file for log rotation was moved to /etc/logrotate.d/switchhub\n"
printf "The group switchhub was created.\n\n"
printf "Press any key to quit."
read
