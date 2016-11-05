#!/bin/bash
# /home/pi/HotspotUpdates/checkForUpdates.sh
# 5 Nov 2016 version 1.1
# Script to check for updates

echo "** `date` ** Checking for updates" >>/home/pi/HotspotUpdates/log 
sudo rm -r /home/pi/HotspotUpdates/new

#turn the wifi back on
sudo airmon-ng stop mon0
sudo ifconfig wlan0 down
sudo iwconfig wlan0 mode managed 
sudo ifconfig wlan0 up

sleep 60

# Attempt to download Hotspot repository from github

git clone https://github.com/Thingitude/Hotspot /home/pi/HotspotUpdates/new

if [ -f /home/pi/HotspotUpdates/new/Version ]; then

  version=`sudo python /home/pi/HotspotUpdates/checkForUpdate.py`

  if [ $version -eq 1 ]; then
    echo "No update received. Rebooting..." >>/home/pi/HotspotUpdates/log 
  else
    echo "Updating..." >>/home/pi/HotspotUpdates/log 
    sudo rm -r /home/pi/HotspotUpdates/old
    sudo mv /home/pi/Hotspot /home/pi/HotspotUpdates/old
    sudo cp -r /home/pi/HotspotUpdates/new /home/pi/Hotspot
    sudo chown -R pi:pi /home/pi/Hotspot
    newver=`cat /home/pi/Hotspot/Version`
    echo "Success! Updated to version $newver." >>/home/pi/HotspotUpdates/log 
  fi
else
  echo "Failed. Could not clone repository." >>/home/pi/HotspotUpdates/log
fi

sudo reboot
