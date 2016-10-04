echo "Upgrading"
#sudo apt-get update
#sudo apt-get upgrade
echo "Upgrade Complete"
echo "Intalling libraries"
sudo apt-get install aircrack-ng i2c-tools mosquitto mosquitto-clients pciutils tshark wiringPi python-smbus
echo "Enabling I2C"
echo '>>> Enable I2C'
if grep -q 'i2c-bcm2708' /etc/modules; then
  echo 'Seems i2c-bcm2708 module already exists, skip this step.'
else
  echo 'i2c-bcm2708' >> /etc/modules
fi
if grep -q 'i2c-dev' /etc/modules; then
  echo 'Seems i2c-dev module already exists, skip this step.'
else
  echo 'i2c-dev' >> /etc/modules
fi
if grep -q 'rtc-ds1307' /etc/modules; then
  echo 'Seems rtc-ds1307 module already exists, skip this step.'
else
  echo 'rtc-ds1307' >> /etc/modules
fi


#replace config.txt in /boot
sudo cp /boot/config.txt /boot/config.old
sudo cp /home/pi/Hotspot/config.txt /boot/config.txt

sudo cp /boot/cmdline.txt /boot/cmdline.old
sudo cp /home/pi/Hotspot/cmdline.txt /boot/cmdline.txt

if [ -f /etc/modprobe.d/raspi-blacklist.conf ]; then
  sed -i 's/^blacklist spi-bcm2708/#blacklist spi-bcm2708/' /etc/modprobe.d/raspi-blacklist.conf
  sed -i 's/^blacklist i2c-bcm2708/#blacklist i2c-bcm2708/' /etc/modprobe.d/raspi-blacklist.conf
else
  echo 'File raspi-blacklist.conf does not exist, skip this step.'
fi

cd /home/pi

sudo hwclock -w

echo "Setting up Cron Jobs"
#write out current crontab
#echo new cron into cron file
echo "@reboot sudo /home/pi/Hotspot/WifiMon.sh on" > mycron
echo "@reboot sudo hwclock -s" >> mycron
echo "00 03 * * * sudo /home/pi/HotspotUpdates/checkForUpdate.sh" >> mycron
echo "05 00 * * * python /home/pi/Hotspot/meantime.py day" >> mycron
echo "08 00 * * * python /home/pi/Hotspot/meantime.py refresh" >> mycron
echo "00,30 * * * * sudo /home/pi/Hotspot/HotspotMonitor.sh send" >>mycron
echo "10,20,40,50 * * * * sudo /home/pi/Hotspot/HotspotMonitor.sh">>mycron
#install new cron file
crontab mycron
rm mycron
