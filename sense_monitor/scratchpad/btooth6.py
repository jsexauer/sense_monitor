import bluetooth
import bluetooth._bluetooth as bt
import struct
import array
import fcntl
import math
from time import sleep

class BluetoothRSSI(object):
    """Object class for getting the RSSI value of a Bluetooth address.
    Reference: https://github.com/dagar/bluetooth-proximity
    """
    def __init__(self, addr):
        self.addr = addr
        self.hci_sock = bt.hci_open_dev()
        self.hci_fd = self.hci_sock.fileno()
        self.bt_sock = bluetooth.BluetoothSocket(bluetooth.L2CAP)
        self.bt_sock.settimeout(10)
        self.connected = False
        self.cmd_pkt = None

    def prep_cmd_pkt(self):
        """Prepares the command packet for requesting RSSI"""
        reqstr = struct.pack(
            "6sB17s", bt.str2ba(self.addr), bt.ACL_LINK, b"\0" * 17)
        request = array.array("H", reqstr)
        handle = fcntl.ioctl(self.hci_fd, bt.HCIGETCONNINFO, request, 1)
        handle = struct.unpack("8xH14x", request.tostring())[0]
        self.cmd_pkt = struct.pack('H', handle)

    def connect(self):
        """Connects to the Bluetooth address"""
        self.bt_sock.connect_ex((self.addr, 1))  # PSM 1 - Service Discovery
        self.connected = True

    def get_rssi(self):
        """Gets the current RSSI value.
        @return: The RSSI value (float) or None if the device connection fails
                 (i.e. the device is nowhere nearby).
        """
        try:
            # Only do connection if not already connected
            if not self.connected:
                self.connect()
            if self.cmd_pkt is None:
                self.prep_cmd_pkt()
            # Send command to request RSSI
            rssi = bt.hci_send_req(
                self.hci_sock, bt.OGF_STATUS_PARAM,
                bt.OCF_READ_RSSI, bt.EVT_CMD_COMPLETE, 4, self.cmd_pkt)
            rssi = struct.unpack('b', rssi[3].to_bytes(1, 'big'))[0]
            return rssi
        except IOError:
            # Happens if connection fails (e.g. device is not in range)
            self.connected = False
            return None

def distance_to_device(addr, num=30):
    """Approximate distance based off of Log Normal Shadowing Model
    https://github.com/laksh225/bluetooth-proximity/tree/patch-1/examples/lnsm
    https://ewenchou.github.io/blog/2016/09/21/bluetooth-proximity-detection/
    """
    btrssi = BluetoothRSSI(addr=addr)

    n = 1.5  # Path loss exponent(n) = 1.5
    c = 10  # Environment constant(C) = 10
    A0 = 6  # Average RSSI value at 1 meter
    actual_dist = 37  # Static distance between transmitter and Receiver in cm
    sum_error = 0
    count = 0

    for i in range(1, num):
        rssi_bt = float(btrssi.get_rssi())
        if (rssi_bt != 0 and i > 10):  # reduces initial false values of RSSI using initial delay of 10sec
            count = count + 1
            x = float((rssi_bt - A0) / (-10 * n))  # Log Normal Shadowing Model considering d0 =1m where
            distance = (math.pow(10, x) * 100) + c
            error = abs(actual_dist - distance)
            sum_error = sum_error + error
            avg_error = sum_error / count
            print("Average Error=  " + str(avg_error))
            print("Error=  " + str(error))
            print("Approximate Distance:" + str(distance))
            print("RSSI: " + str(rssi_bt))
            print("Count: " + str(count))
            print(" ")
        sleep(1)

while True:
    addr = "18:4E:16:94:38:AF"

    print(bluetooth.lookup_name(addr))
    rssi = BluetoothRSSI(addr).get_rssi()
    print(f"RSSI = {rssi}")

    distance_to_device(addr)

    sleep(5)