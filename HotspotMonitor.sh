#!/bin/sh

# * HotspotMonitor.sh - turn the wifi into monitor mode       */
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

#  This script should be run from Cron, we are using 5 min intervals
#  Note the optional argument - to send a message or not.  We send
#  messages every 30 mins, again set up in Cron.

#  Set up the parameters for the wifi monitoring
monFile="/home/pi/Hotspot/monFile"
hashfile="/home/pi/Hotspot/hashFile"
macFile="/home/pi/Hotspot/macFile"
duration=100
meanOut=""

cd /home/pi/Hotspot

#  Tshark listens for wifi probe requests and captures MAC addresses
tshark -a duration:$duration -f wlan[0]=0x40 -i mon0 -T fields -E separator=,  -e wlan.sa  1> $monFile
   
#  Now filter out the unique MACs
sort -d -u $monFile > $macFile
wificount=`cat $macFile | wc -l`

#  Hash them like good citizens (we don't want to keep MAC addresses)
python /home/pi/Hotspot/hashing.py

#  Update the mean duration
meanOut=$(python /home/pi/Hotspot/meantime.py run)
timenow=`date`

#  Decide whether to send a message or not
case "$1" in
  "")
	# Nothing to do
	echo "Did not send at $timenow\n" >>/home/pi/Hotspot/logfile
	exit
	;;
  send)
	# Collect sensor stats and send message
	echo "Launched hotspotmq at $timenow\n" >>/home/pi/Hotspot/logfile
	/home/pi/Hotspot/hotspotmq $wificount $meanOut
	;;
  *)
	# Usage error
	echo "USAGE: HotspotMonitor.sh [start]"
	exit 3
	;;
esac

