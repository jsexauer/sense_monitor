# This one works!
# Phone = 18:4e:16:94:38:af
import datetime
from bluepy.btle import Scanner, DefaultDelegate
from time import sleep

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:pass
            #print("Discovered device", dev.addr)
        elif isNewData:pass
            #print("Received new data from", dev.addr)



def print_devices():
    scanner = Scanner().withDelegate(ScanDelegate())
    devices = scanner.scan(2.0)

    for dev in devices:
        print("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
        for (adtype, desc, value) in dev.getScanData():
            print("  %s = %s" % (desc, value))
            
def scan_for_phone():
    while True:
        scanner = Scanner().withDelegate(ScanDelegate())
        devices = scanner.scan(2.0)
        
        print('*'*20)
        print(datetime.datetime.now())
        for dev in devices:
            found_services = 0
            for (adtype, desc, value) in dev.getScanData():
                if value in ('0000fd6f-0000-1000-8000-00805f9b34fb', '6ffd96b27d212f47562ffd7b037fb048baf1e57d27df'):
                    found_services += 1
            if found_services == 2:
                print(f"Found phone {dev.addr} at {dev.rssi}")
         sleep(15)
        
if __name__=='__main__':
    scan_for_phone()
