#SwitchHub
##Introduction
SwitchHub is a command line application for Linux (exclusively for the time being) that allows flexible control of the [Telldus Tellstick](http://www.telldus.se/products/tellstick). The Telldus Tellstick is a device that can be controlled from a computer to control power switches (i.e. remote socket receivers) remotely. SwitchHub can be easily adopted to control other similar devices.

The scheduling of events (i.e. scheduling switches to turn on or off or dim) is made by creating Boolean
expressions, one per switch. An event definition can look like this:

*on = 06:00 <= t < 07:15 and sundown*

Here are some of the important characteristics of SwitchHub:
- SwitchHub is lightweight and will not use much of your system's resources.
- The scheduling of events is very flexible. This is because:
	- The amount of meaningful variables.
	- You have a high degree of freedom when you write the Boolean expressions.
- You can easily add your own plugins to let SwitchHub use variables of your liking.
- SwitchHub will run unattended. Once configured, SwitchHub will be out of your way.
- SwitchHub does not have a GUI. You will edit text files to configure SwitchHub and the events.
- SwitchHub is written in Python 3. This is only of interest if you want to read the code or make changes to it.

For more information, refer to [SwitchHub.pdf](https://github.com/thoelf/switchhub/blob/master/SwitchHub.pdf) and to the list of [issues](https://github.com/thoelf/switchhub/issues).

##Status
The program works very well, and have done so for several months. Most major functions are implemented. Cleaning up and making the code pretty still remains. I'm not sure that the installation script works perfectly. Should use a deb package instead... The manual updates are lagging a bit, but the code should be self-explaining. ;-)

##Updates
###SwitchHub 0.4
- Dimmer support.
- Better logging of errors when evaluating the event expressions.
- New plugin readfile, lets SwitchHub read variable values from any file.
- Do not crach when there is no internet connection (plugin gcalendar).
- Simplified syntax for event expressions.

###SwitchHub 0.3
It is now possible to use plug-ins. A plug-in is a program/script that provides variables that can be used in the event definitions. The module for communication with Google Calendar has been transformed to a plug-in.

###SwitchHub 0.2
Added:
- Logging functionality using the logging Python library.
- Scripts for starting, stopping and checking the status.
- An installation script to simplify the installation.

Fixed:
- Program will crash if no connection to Google.
