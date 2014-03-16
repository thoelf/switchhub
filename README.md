#What is SwitchHub?
SwitchHub is a command line application for Linux (exclusively for the time being) that allows flexible control of the Telldus Tellstick. The Telldus Tellstick is a device that can be controlled from a computer to control power switches remotely. SwitchHub can be easily adopted to control other similar devices.

The scheduling of events (i.e. scheduling switches to turn on or off) is made by creating Boolean
expressions, one per switch.

Here are some of the important characteristics of SwitchHub:
- SwitchHub is lightweight and will not use much of your system's resources.
- The scheduling of events is very flexible. This is because:
	- The amount of meaningful variables.
	- You have a high degree of freedom when you write the Boolean expressions.
- SwitchHub is intended to run unattended as a server daemon. Once configured, SwitchHub will be out of your way.
- SwitchHub does not have a GUI. You will edit text files (there is four of them) to configure SwitchHub and the events.
- SwitchHub is written in Python 3. This is only of interest if you want to read the code or make changes to it.

For more information, refer to SwitchHub.pdf and to the list of [issues](https://github.com/thoelf/switchhub/issues).
