#!/bin/bash
# This script is run once by the HotspotUpdates/checkforUpdates.sh
# after a successful update to the Hotspot code
#
# You should add any setup changes required by the Hotspot update
# such as cron jobs, package installations etc., to this script.

echo "** `date` ** Running update script" >>/home/pi/HotspotUpdates/log 
cd /home/pi/Hotspot

# Insert changes for this update here...

# MS 5 Nov 2016 - update for Hotspot v1.1
# Purpose of this is to get the Hotspot to update the checkForUpdates.sh
# so that in future it runs this script!  Sorry it's a bit recursive ;-)
# Also the new checkForUpdates.sh fixes a bug whereby the Hotspot folder
# got deleted if the git clone failed, for example if the network is down.
# So the fix is quite important...

mv /home/pi/Hotspot/checkForUpdate.sh /home/pi/HotspotUpdates
chown pi:pi /home/pi/HotspotUpdates/checkForUpdate.sh

# Setting up Cron Jobs - there aren't any changes this time but I thought 
# I would leave it in as example code.

echo "@reboot sudo /home/pi/Hotspot/WifiMon.sh on" > mycron
echo "@reboot sudo hwclock -s" >> mycron
echo "00 03 * * * sudo /home/pi/HotspotUpdates/checkForUpdate.sh" >> mycron
echo "05 00 * * * python /home/pi/Hotspot/meantime.py day" >> mycron
echo "08 00 * * * python /home/pi/Hotspot/meantime.py refresh" >> mycron
echo "00,30 * * * * sudo /home/pi/Hotspot/HotspotMonitor.sh send" >>mycron
echo "10,20,40,50 * * * * sudo /home/pi/Hotspot/HotspotMonitor.sh">>mycron

# install new cron file
crontab -u pi mycron
rm mycron

# End of changes for v1.1

echo "Update.sh completed successfully." >>/home/pi/HotspotUpdates/log
echo "Done - `date`" >/home/pi/Hotspot/up_to_date

# Note that when this script exits, checkForUpdates.sh will reboot 
# the Hotspot and your new update should be live!  Congratulations :-)

exit
