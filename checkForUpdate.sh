#!/bin/bash
# Script to check for updates
echo "Checking for updates"
sudo rm -r /home/pi/HotspotUpdates/new

sudo chmod -r 777 /home/pi/HotspotUpdates/new

#turn the wifi back on
sudo airmon-ng stop mon0
sudo ifconfig wlan0 down
sudo iwconfig wlan0 mode managed 
sudo ifconfig wlan0 up

sleep 60

#download reprositry from github

git clone https://github.com/Thingitude/Hotspot /home/pi/HotspotUpdates/new

version=`sudo python /home/pi/HotspotUpdates/checkForUpdate.py`
echo "And the answer is $version"

if [ $version -eq 1 ]; then
  echo script ends here
else
  sudo rm -r /home/pi/HotspotUpdates/old
  sudo cp -r /home/pi/HotspotUpdates/current /home/pi/HotspotUpdates/old
  sudo rm -r /home/pi/HotspotUpdates/current
  sudo cp -r /home/pi/HotspotUpdates/new /home/pi/HotspotUpdates/current
  sudo reboot
fi
