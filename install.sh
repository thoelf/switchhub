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


resize -s 24 86 &> /dev/null

echo -ne "\033]0;SwitchHub installation\007"
clear

INSTALL_DIR=/opt/switchhub
LOG_FILE=/var/log/switchhub
USERNAME=$(whoami)

printf "This is required during the installation:\n    * Internet connection (to download SwitchHub)."
if [ "$USERNAME" != "root" ]; then
    printf "\n    * The root password (to make changes that require root permissions).\n\n"
fi

if [ "$USERNAME" == "root" ]; then
    printf "\n\nFor which user are you installing SwitchHub? "
    read USERNAME
    UEXIST="false"
    while [ "$UEXIST" == "false" ]; do
        getent passwd $USERNAME >/dev/null 2>&1 && UEXIST="true"
        if [ "$UEXIST" == "false" ]; then
            printf "Error: The user does not exist!"
            printf "\n\nFor which user are you installing SwitchHub? "
            read USERNAME
        fi
    done
    printf "\n"
fi

printf "You are about to install SwitchHub for user $USERNAME.\n"
printf "Press any key to continue the installation or Ctrl+C to quit."
read

sudo groupadd switchhub
sudo usermod -a -G switchhub $USERNAME

cd
mv -v switchhub-master switchhub

sudo mkdir /etc/switchhub
sudo mv -v ./switchhub/{events.cfg, free_days.cfg, holidays.cfg, program.cfg} /etc/switchhub
sudo chgrp switchhub /etc/switchhub/*
sudo chmod g+w /etc/switchhub/*

mv -v ./switchhub/{switchhub_start, switchhub_stop} .
sudo chown $USERNAME:$USERNAME /home/$USERNAME/{switchhub_start, switchhub_stop}
chmod u+x switchhub_start switchhub_stop

sudo mv -v switchhub /opt
cd $INSTALL_DIR
sudo chgrp -R switchhub *
sudo chmod -R g+w *
sudo chmod g+x switchhub.py

sudo cp -v switchhub_logrotate /etc/logrotate.d/switchhub
echo "Refer to /etc/logrotate.d/switchhub for the configuration of log rotation." > switchhub_logrotate

sudo touch $LOG_FILE
sudo chgrp switchhub $LOG_FILE
sudo chmod g+w $LOG_FILE

printf "\nThe installation was succesful!\n"
printf "The installation directory is: $INSTALL_DIR\n"
printf "The configuration files are in the directory /etc/switchhub.\n"
printf "The log file is: $LOG_FILE\n"
printf "The configuration file for log rotation was copied to /etc/logrotate.d/switchhub\n"
printf "The group switchhub was created and $USERNAME is now a member of that group.\n"
printf "A start script named switchhub_start was created in $USERNAME's home directory.\n"
printf "To start SwitchHub, go to /home/$USERNAME and enter \"./switchhub_start\" or \"sh switchhub_start\"\n\n"
printf "A stop script named switchhub_stop was created in $USERNAME's home directory.\n"
printf "To stop SwitchHub, go to /home/$USERNAME and enter \"./switchhub_stop\" or \"sh switchhub_stop\"\n\n"

printf "Press any key to quit."
read
