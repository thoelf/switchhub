#!/usr/bin/env bash
#Copyright 2016 Thomas Elfström
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

prg_str="python3 /opt/switchhub/switchhub.py"
screen_str="SCREEN /opt/switchhub/switchhub"
logfile="/var/log/switchhub.log"
settings="/etc/switchhub/switchhub"
events="/etc/switchhub/events"
plugin_settings="/etc/switchhub/plugins"
port="8001"
editor="vim"

printf "\n"


start () {
	if [[ ! $(pgrep -f "$prg_str") && ! $(netstat -l | grep $port) ]]; then
    	screen /opt/switchhub/switchhub.py
	elif [[ $(pgrep -f "$prg_str") ]]; then
    	printf "\nSwitchHub is already running.\n"
    	read -p "Enter to continue."
    elif [[ $(netstat -l | grep $port) ]]; then
    	printf "Port is busy. Waiting...\n"
    	while [[ $(netstat -l | grep $port) ]]; do
			sleep 1
		done
		screen /opt/switchhub/switchhub.py
	fi
}


restart () {
	stop
	start
}


reattach () {
	if [[ $(pgrep -f "$screen_str") ]]; then
		screen -r $(pgrep -f "$screen_str")
	else
		printf "\nThere is no screen session to attach to.\n"
	fi
}


stop () {
	if [[ $(pgrep -f "$prg_str") ]]; then
    	printf "\nKilling switchhub.\n"
		kill $(ps aux|grep switchhub|grep -v switchhub.sh|grep -v grep|grep -v "vim switchhub"|tr -s " "|cut -d" " -f 2)
	else
    	printf "\nSwitchHub is not running. Doing nothing.\n"
	fi
}


show_log () {
	clear
	if [[ -a "$logfile" ]]; then
		tail "$logfile"
	else
		printf "\nThe log file does not exist.\n"
	fi
	read -p "Enter to continue."
	clear
}


clear_log () {
	if [[ -a "$logfile" ]]; then
		read -p "\nAre you sure [y/n]? " -n 1 -r
		if [[ $REPLY =~ ^[Yy]$ ]]; then
			> "$logfile"
		fi
		printf "\n"
	else
		printf "\nThe logfile does not exist.\n"
	fi
}


edit_events () {
	"$editor" "$events"
}


edit_program_settings () {
	"$editor" "$settings"
}


edit_plugin_settings () {
	"$editor" "$plugin_settings"
}


while :; do
	clear
#	cpu=0
#	mem=0
	if [[ $(pgrep -f "$prg_str") ]]; then
#		if [[ ! -p mypipe ]]; then
#			mkfifo mypipe
#		fi
#		ps aux|grep switchhub|grep -v switchhub.sh|grep -v grep|grep -v "vim switchhub"|grep -v "SCREEN /opt/switchhub/switchhub.py"|tr -s " "|cut -d" " -f 3 > mypipe &
#		while IFS= read -r line; do
#			cpu=$(echo $cpu + $line | bc)
#		done < mypipe
#		ps aux|grep switchhub|grep -v switchhub.sh|grep -v grep|grep -v "vim switchhub"|grep -v "SCREEN /opt/switchhub/switchhub.py"|tr -s " "|cut -d" " -f 4 > mypipe &
#		while IFS= read -r line; do
#			mem=$(echo $mem + $line | bc)
#		done < mypipe
		
		printf "SwitchHub is running since $(ps aux|grep switchhub.py|grep -v switchhub.sh|grep -v grep|grep -v "vim switchhub"|grep -v "SCREEN /opt/switchhub/switchhub.py"|tr -s " "|cut -d" " -f 9)\n"
#		printf "CPU: %1.1f%%, Mem: %1.1f%%\n" $cpu $mem

		printf "\nRunning programs:\n"
		for p in $(ps aux|grep switchhub|grep -v switchhub.sh|grep -v grep|grep -v "vim switchhub"|grep -v "SCREEN /opt/switchhub/switchhub.py"|tr -s " "|cut -d" " -f 12); do
			echo "  -" ${p##*/}
		done
	echo
	else
	   	printf "Switchhub is not running.\n"
	fi
	
	printf " %3s  %-16s\n" "1:" "Start" \
			"2:" "Restart" \
			"3:" "Stop" \
			"4:" "Reattach screen session (Deattach with 'Ctrl+A D')" \
			"5:" "Show latest log messages" \
			"6:" "Clear log" \
			"7:" "Edit events" \
			"8:" "Edit program settings" \
			"9:" "Edit plugin settings" \
			"Q:" "Quit" \
			""
	read -p " > " -n 1 ans
	
	case $ans in
		1)	start ;;
   		2)	restart ;;
   		3)	stop ;;
   		4)  reattach ;;
   		5)	show_log ;;
   		6)  clear_log ;;
   		7)	edit_events ;;
   		8)	edit_program_settings ;;
   		9)	edit_plugin_settings ;;
   		[qQ])	echo
   				exit 1 ;;
	esac
done

