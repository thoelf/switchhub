#!/usr/bin/env python3

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

def main():

    import codecs
    import configparser
    import datetime
    import time
    from datetime import datetime
    from datetime import timedelta
    import os
    import subprocess

	# Initialize config parser for the suntime settings file
    confsuntime = configparser.ConfigParser()
    confsuntime.readfp(codecs.open("/etc/switchhub/plugins/suntime", "r", "utf8"))

    location = confsuntime['settings']['location']

    # Wait until www.yahoo.com can be reached or wait 10 minutes.
    # The whole program will wait, so we don't want to wait too long.
    # If the connection cannot be established, switchhub will use the existing (old) values.
    # If there are no old values (first run), switchhub will crash if variables in the
    # events configuration file becomes undefined.
    minutes = 0
    while os.system("ping -c 1 www.yahoo.com > /dev/null") and minutes < 10:
        time.sleep(60)
        minutes += 1
    if minutes < 10:

        command = "curl -s http://weather.yahooapis.com/forecastrss?w=" + location + \
			"|grep astronomy| awk -F\\" + '"' + " '{print $2 " + '"' + "\\n" + '"' + " $4;}'"

        stdoutdata = subprocess.check_output([command], shell=True)
        nlines = stdoutdata.decode("utf-8")

        count = 0
        for line in nlines.splitlines():
            if line.strip():                        # If line not empty
                count += 1
                if count == 1:
                    t_sunup = datetime.strptime(line.split(' ')[0], "%H:%M")
                if count == 2:
                    if line.split(' ')[1] == "pm":
                        t_sundown = datetime.strptime(line.split(' ')[0], '%H:%M') + timedelta(hours=12)
                    else:
                        t_sundown = datetime.strptime(line.split(' ')[0], "%H:%M")

        sunup = '({0} <= t < {1})'.format((t_sunup - timedelta(minutes=0)).strftime('%H:%M'), (t_sundown - timedelta(minutes=0)).strftime('%H:%M'))
        sunup_minus_10 = '({0} <= t < {1})'.format((t_sunup - timedelta(minutes=10)).strftime('%H:%M'), (t_sundown - timedelta(minutes=10)).strftime('%H:%M'))
        sunup_minus_20 = '({0} <= t < {1})'.format((t_sunup - timedelta(minutes=20)).strftime('%H:%M'), (t_sundown - timedelta(minutes=20)).strftime('%H:%M'))
        sunup_minus_30 = '({0} <= t < {1})'.format((t_sunup - timedelta(minutes=30)).strftime('%H:%M'), (t_sundown - timedelta(minutes=30)).strftime('%H:%M'))
        sunup_minus_40 = '({0} <= t < {1})'.format((t_sunup - timedelta(minutes=40)).strftime('%H:%M'), (t_sundown - timedelta(minutes=40)).strftime('%H:%M'))
        sunup_minus_50 = '({0} <= t < {1})'.format((t_sunup - timedelta(minutes=50)).strftime('%H:%M'), (t_sundown - timedelta(minutes=50)).strftime('%H:%M'))
        sunup_minus_60 = '({0} <= t < {1})'.format((t_sunup - timedelta(minutes=60)).strftime('%H:%M'), (t_sundown - timedelta(minutes=60)).strftime('%H:%M'))
    
        sunup_plus_10 = '({0} <= t < {1})'.format((t_sunup + timedelta(minutes=10)).strftime('%H:%M'), (t_sundown + timedelta(minutes=10)).strftime('%H:%M'))
        sunup_plus_20 = '({0} <= t < {1})'.format((t_sunup + timedelta(minutes=20)).strftime('%H:%M'), (t_sundown + timedelta(minutes=20)).strftime('%H:%M'))
        sunup_plus_30 = '({0} <= t < {1})'.format((t_sunup + timedelta(minutes=30)).strftime('%H:%M'), (t_sundown + timedelta(minutes=30)).strftime('%H:%M'))
        sunup_plus_40 = '({0} <= t < {1})'.format((t_sunup + timedelta(minutes=40)).strftime('%H:%M'), (t_sundown + timedelta(minutes=40)).strftime('%H:%M'))
        sunup_plus_50 = '({0} <= t < {1})'.format((t_sunup + timedelta(minutes=50)).strftime('%H:%M'), (t_sundown + timedelta(minutes=50)).strftime('%H:%M'))
        sunup_plus_60 = '({0} <= t < {1})'.format((t_sunup + timedelta(minutes=60)).strftime('%H:%M'), (t_sundown + timedelta(minutes=60)).strftime('%H:%M'))

        sundown = '(00:00 <= t < {0} or {1} <= t < 23:59)'.format((t_sunup - timedelta(minutes=0)).strftime('%H:%M'), (t_sundown - timedelta(minutes=0)).strftime('%H:%M')) 
        sundown_minus_10 = '(00:00 <= t < {0} or {1} <= t < 23:59)'.format((t_sunup - timedelta(minutes=10)).strftime('%H:%M'), (t_sundown - timedelta(minutes=10)).strftime('%H:%M'))
        sundown_minus_20 = '(00:00 <= t < {0} or {1} <= t < 23:59)'.format((t_sunup - timedelta(minutes=20)).strftime('%H:%M'), (t_sundown - timedelta(minutes=20)).strftime('%H:%M'))
        sundown_minus_30 = '(00:00 <= t < {0} or {1} <= t < 23:59)'.format((t_sunup - timedelta(minutes=30)).strftime('%H:%M'), (t_sundown - timedelta(minutes=30)).strftime('%H:%M'))
        sundown_minus_40 = '(00:00 <= t < {0} or {1} <= t < 23:59)'.format((t_sunup - timedelta(minutes=40)).strftime('%H:%M'), (t_sundown - timedelta(minutes=40)).strftime('%H:%M'))
        sundown_minus_50 = '(00:00 <= t < {0} or {1} <= t < 23:59)'.format((t_sunup - timedelta(minutes=50)).strftime('%H:%M'), (t_sundown - timedelta(minutes=50)).strftime('%H:%M'))
        sundown_minus_60 = '(00:00 <= t < {0} or {1} <= t < 23:59)'.format((t_sunup - timedelta(minutes=60)).strftime('%H:%M'), (t_sundown - timedelta(minutes=60)).strftime('%H:%M'))

        sundown_plus_10 = '(00:00 <= t < {0} or {1} <= t < 23:59)'.format((t_sunup + timedelta(minutes=10)).strftime('%H:%M'), (t_sundown + timedelta(minutes=10)).strftime('%H:%M'))
        sundown_plus_20 = '(00:00 <= t < {0} or {1} <= t < 23:59)'.format((t_sunup + timedelta(minutes=20)).strftime('%H:%M'), (t_sundown + timedelta(minutes=20)).strftime('%H:%M'))
        sundown_plus_30 = '(00:00 <= t < {0} or {1} <= t < 23:59)'.format((t_sunup + timedelta(minutes=30)).strftime('%H:%M'), (t_sundown + timedelta(minutes=30)).strftime('%H:%M'))
        sundown_plus_40 = '(00:00 <= t < {0} or {1} <= t < 23:59)'.format((t_sunup + timedelta(minutes=40)).strftime('%H:%M'), (t_sundown + timedelta(minutes=40)).strftime('%H:%M'))
        sundown_plus_50 = '(00:00 <= t < {0} or {1} <= t < 23:59)'.format((t_sunup + timedelta(minutes=50)).strftime('%H:%M'), (t_sundown + timedelta(minutes=50)).strftime('%H:%M'))
        sundown_plus_60 = '(00:00 <= t < {0} or {1} <= t < 23:59)'.format((t_sunup + timedelta(minutes=60)).strftime('%H:%M'), (t_sundown + timedelta(minutes=60)).strftime('%H:%M'))

        print("suntime.py;sunup;{0}".format(sunup))
        print("suntime.py;sunup_minus_10;{0}".format(sunup_minus_10))
        print("suntime.py;sunup_minus_20;{0}".format(sunup_minus_20))
        print("suntime.py;sunup_minus_30;{0}".format(sunup_minus_30))
        print("suntime.py;sunup_minus_40;{0}".format(sunup_minus_40))
        print("suntime.py;sunup_minus_50;{0}".format(sunup_minus_50))
        print("suntime.py;sunup_minus_60;{0}".format(sunup_minus_60))
        print("suntime.py;sunup_plus_10;{0}".format(sunup_plus_10))
        print("suntime.py;sunup_plus_20;{0}".format(sunup_plus_20))
        print("suntime.py;sunup_plus_30;{0}".format(sunup_plus_30))
        print("suntime.py;sunup_plus_40;{0}".format(sunup_plus_40))
        print("suntime.py;sunup_plus_50;{0}".format(sunup_plus_50))
        print("suntime.py;sunup_plus_60;{0}".format(sunup_plus_60))
        print("suntime.py;sundown;{0}".format(sundown))      
        print("suntime.py;sundown_minus_10;{0}".format(sundown_minus_10))
        print("suntime.py;sundown_minus_20;{0}".format(sundown_minus_20))
        print("suntime.py;sundown_minus_30;{0}".format(sundown_minus_30))
        print("suntime.py;sundown_minus_40;{0}".format(sundown_minus_40))
        print("suntime.py;sundown_minus_50;{0}".format(sundown_minus_50))
        print("suntime.py;sundown_minus_60;{0}".format(sundown_minus_60))
        print("suntime.py;sundown_plus_10;{0}".format(sundown_plus_10))
        print("suntime.py;sundown_plus_20;{0}".format(sundown_plus_20))
        print("suntime.py;sundown_plus_30;{0}".format(sundown_plus_30))
        print("suntime.py;sundown_plus_40;{0}".format(sundown_plus_40))
        print("suntime.py;sundown_plus_50;{0}".format(sundown_plus_50))
        print("suntime.py;sundown_plus_60;{0}".format(sundown_plus_60))

if __name__ == "__main__":
    main()
