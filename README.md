# SwitchHub
## Introduction
SwitchHub is a command line application for Linux that allows flexible control of the [Telldus Tellstick](http://www.telldus.se/products/tellstick). The Telldus Tellstick is a device that can be controlled from a computer to control power switches (i.e. remote socket receivers) remotely.

The scheduling of events (i.e. scheduling switches to turn on or off or dim) is made by creating Boolean expressions, one per switch. An event definition can look like this:

*on = 06:00 <= t < 07:15 and sundown*

Here are some of the important characteristics of SwitchHub:
- The scheduling of events is very flexible. This is because:
	- The amount of meaningful variables.
	- You have a high degree of freedom when you write the Boolean expressions.
- You can easily add your own plugins to let SwitchHub use variables of your liking.
- SwitchHub will run unattended. Once configured, SwitchHub will be out of your way.
- SwitchHub does not have a GUI. You will edit text files to configure SwitchHub and the events.
- SwitchHub is written in Python 3. This is only of interest if you want to read the code or make changes to it.

For more information, refer to [SwitchHub.pdf](https://github.com/thoelf/switchhub/blob/master/SwitchHub.pdf) and to the list of [issues](https://github.com/thoelf/switchhub/issues).

### Status
The application works very well. The installation script is not guaranteed to work, but it's a good start.

## Updates
### SwitchHub 0.5
- A class for switches was created. Every switch is now its own object.
- Added the plug-in *sensor_receiver.py* that handles "on/off-sensors" such as motion sensors, light sensors and buttons.
- Plug-ins now communicate via TCP socket and can deliver data at any time (before only in predefined intervals via stdout).
- Configuration files for plug-ins has been removed. Any setting is now made in the applicable program file.
- The start/stop/status-script *switchhub.sh* has turned into a "control console" with more functions than before.
- The manual was updated.

### SwitchHub 0.42
- Configurable turnaround time to handle sensors or events that requires a fast response.
- A new plugin directory that is run at every turnaround.

### SwitchHub 0.41
- Replaced the gcalendar plugin with two other plugins (suntime.py and cal.py). These plugins provides the variables for sunrise/sunset and holidays. Refer to issue 20.

### SwitchHub 0.4
- Dimmer support.
- Better logging of errors when evaluating the event expressions.
- New plugin readfile, lets SwitchHub read variable values from any file.
- Do not crash when there is no internet connection (plugin gcalendar).
- Simplified syntax for event expressions.

### SwitchHub 0.3
It is now possible to use plug-ins. A plug-in is a program/script that provides variables that can be used in the event definitions. The module for communication with Google Calendar has been transformed to a plug-in.

### SwitchHub 0.2
Added:
- Logging functionality using the logging Python library.
- Scripts for starting, stopping and checking the status.
- An installation script to simplify the installation.

Fixed:
- Program will crash if no connection to Google.
