# sense_monitor
Sense monitor on raspberry pi

# Install

Below only needed when playing with bluetooth low energy (BLE)
```
# From https://github.com/pybluez/pybluez/wiki/Installation-on-Raspberry-Pi-3
sudo apt-get install libbluetooth-dev python-dev libglib2.0-dev libboost-python-dev libboost-thread-dev
pip3 download gattlib
tar xvzf ./gattlib-0.20150805.tar.gz
cd gattlib-0.20150805/
sed -ie 's/boost_python-py34/boost_python-py37/' setup.py
pip3 install .

# Give Bluetooth access to pybleno --> Python3.7 
sudo setcap 'cap_net_raw,cap_net_admin+eip' /usr/bin/python3.7
# Give Bluetooth access to bluepy --> bluepy-helper 
sudo setcap 'cap_net_raw,cap_net_admin+eip' /home/pi/.local/lib/python3.7/site-packages/bluepy/bluepy-helper

```

# Bluetooth info
18:4E:16:94:38:AF = Samsung S20 FE

Pair using UI or
```
bluetoothctl
scan on
# Put phone into pariring mode
# Now you should see the id
info 18:4E:16:94:38:AF
pair 18:4E:16:94:38:AF
connect 18:4E:16:94:38:AF
```

