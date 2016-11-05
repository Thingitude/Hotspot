#!/bin/bash
# This script is run once by the HotspotUpdates/checkforUpdates.sh
# after a successful update to the Hotspot code
#
# You should add any setup changes required by the Hotspot update
# such as cron jobs, package installations etc., to this script.

echo "** `date` ** Running update script" >>/home/pi/HotspotUpdates/log 
cd /home/pi/Hotspot

# Insert changes for this update here...

# Setting up Cron Jobs

echo "@reboot sudo /home/pi/Hotspot/WifiMon.sh on" > mycron
echo "@reboot sudo hwclock -s" >> mycron
echo "00 03 * * * sudo /home/pi/HotspotUpdates/checkForUpdate.sh" >> mycron
echo "05 00 * * * python /home/pi/Hotspot/meantime.py day" >> mycron
echo "08 00 * * * python /home/pi/Hotspot/meantime.py refresh" >> mycron
echo "00,30 * * * * sudo /home/pi/Hotspot/HotspotMonitor.sh send" >>mycron
echo "10,20,40,50 * * * * sudo /home/pi/Hotspot/HotspotMonitor.sh">>mycron

# install new cron file
crontab mycron
rm mycron

echo "Update.sh completed successfully." >>/home/pi/HotspotUpdates/log

# Note that when this script exits, checkForUpdates.sh will reboot 
# the Hotspot and your new update should be live!  Congratulations :-)

exit
