echo "Upgrading"
sudo apt-get update
sudo apt-get upgrade
echo "Upgrade Complete"
echo "Intalling libraries"
sudo apt-get install aircrack-ng i2c-tools mosquitto mosquitto-clients pciutils tshark wiringPi
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
if grep -q 'dtparam=i2c1=on' /boot/config.txt; then
  echo 'Seems i2c1 parameter already set, skip this step.'
else
  echo 'dtparam=i2c1=on' >> /boot/config.txt
fi
if grep -q 'dtparam=i2c_arm=on' /boot/config.txt; then
  echo 'Seems i2c_arm parameter already set, skip this step.'
else
  echo 'dtparam=i2c_arm=on' >> /boot/config.txt
fi
if [ -f /etc/modprobe.d/raspi-blacklist.conf ]; then
  sed -i 's/^blacklist spi-bcm2708/#blacklist spi-bcm2708/' /etc/modprobe.d/raspi-blacklist.conf
  sed -i 's/^blacklist i2c-bcm2708/#blacklist i2c-bcm2708/' /etc/modprobe.d/raspi-blacklist.conf
else
  echo 'File raspi-blacklist.conf does not exist, skip this step.'
fi

cd "~"
rm rf Hotspot
git clone https://github.com/SamKimbinyi/Hotspot.git

echo "Setting up Auto Run"

echo "Autorun the Reading Hotspot monitor script" >>  /etc/rc.local
echo "sudo /home/pi/Hotspot/HotspotMonitor.sh 2>/var/log/hotspot.log &" >> /etc/rc.local

echo "Setting up Cron Jobs"
#write out current crontab
#echo new cron into cron file
echo "05 00 * * * python /home/pi/Hotspot/meantime.py day" > mycron
echo "08 00 * * * python /home/pi/Hotspot/meantime.py refresh" >> mycron
echo "00,30 * * * * sudo /home/pi/Hotspot/HotspotMonitor.sh send" >>mycron
echo "10,20,40,50 * * * * sudo /home/pi/Hotspot/HotspotMonitor.sh">>mycron
#install new cron file
crontab mycron
rm mycron
