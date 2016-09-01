#!/bin/sh
cd /home/pi/Hotspot

macFile="/home/pi/Hotspot/macFile"
monFile="/home/pi/Hotspot/monFile"
meanOut=""

#  Now filter out the unique MACs
	sort -d -u $monFile > $macFile
	wificount=`cat $macFile | wc -l`
	timeNow=`date +%s`

	python /home/pi/Hotspot/hashing.py
	meanOut=$(python /home/pi/Hotspot/meantime.py run)


	#  Now display the number with the other data on the LCD display
	/home/pi/Hotspot/hotspotmq $wificount $meanOut
