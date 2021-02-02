# sense_monitor
Sense monitor on raspberry pi

# Install
```
sudo apt-get install libglib2.0-dev

# Give Bluetooth access to pybleno --> Python3.7 
sudo setcap 'cap_net_raw,cap_net_admin+eip' /usr/bin/python3.7
# Give Bluetooth access to bluepy --> bluepy-helper 
sudo setcap 'cap_net_raw,cap_net_admin+eip' /home/pi/.local/lib/python3.7/site-packages/bluepy/bluepy-helper

```

# Bluetooth info
Turns out these change frequently, so this is worhtless...
73:4a:76:d9:5f:7f = Personal cell phone
55:1c:01:b9:f8:9a = ???
47:27:d4:12:9a:76 = Swidget Power insert
4a:9a:1c:85:63:00 = Work iPhone
