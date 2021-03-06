#!/bin/bash

# * WifiMon.sh - turn the wifi monitor mode on or off         */
# * (c) Mark Stanley 2016                                     */
# *                                                           */
# * Created for the Reading Hotspot project, 2016             */
# *                                                           */
# * Funded through Thingitude.com by Reading Council and      */
# * Coraledge Ltd, for The Things Network Reading.            */
# *                                                           */
# * You are welcome to use or modify as you like, but please  */
# * keep these comments at the top of the code so credit and  */
# * copyright are preserved.                                  */

# * MS - 5 Nov 2016 - version 1.1
# * Added a test to make sure update.sh has been run, and if
# * it hasn't then we'll run it for the first time.  Bit of
# * belt and braces for the HotspotUpdates routines

if [ ! -f /home/pi/Hotspot/up_to_date ]; then
  /home/pi/Hotspot/update.sh
fi

echo "WifiMon running in 1 mins"
echo `date`

sleep 60

#  Reset the wifi to a known state
airmon-ng stop mon0 
ifconfig wlan0 down
iwconfig wlan0 mode managed
ifconfig wlan0 up

case "$1" in
  on)
	#  Switch the wifi to monitor mode
	ifconfig wlan0 down
	iwconfig wlan0 mode Monitor
	ifconfig wlan0 up
	
	#  Get mon0 up and running
	airmon-ng start wlan0 6
        ;;
  off)
        # Nothing to do
        ;;
  *)
        # Usage error
        echo "USAGE: WifiMon.sh on|off"
        exit 3
        ;;
esac
