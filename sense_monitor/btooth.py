import datetime
import struct
import array
import fcntl
import time

import bluetooth
import bluetooth._bluetooth as bt
from bluepy.btle import Scanner, BTLEManagementError


class BluetoothMonitor:
    def __init__(self, addr, debug=False):
        self.addr = addr
        self.debug = debug

    def print(self, *args):
        if self.debug:
            print(*args)

    def old_methodology(self):
        # Original methodoly.  Does not seem to work well on Pi Zero.
        scanner = Scanner()
        devices = scanner.scan(5.0)

        for d in devices:
            self.print(d.addr, d.rssi)
            if d.addr.lower() == self.addr.lower():
                return d.rssi
        return None

    def covid_methodology(self):
        # Scans BLE devices for those emmiting the covid tracking service
        # See btooth4 in scratchpad

        scanner = Scanner()
        scan_successful = False
        for n in range(3):
            try:
                devices = scanner.scan(2.0)
                scan_successful = True
            except BTLEManagementError:
                # May fail to acquire scan if someone else is trying to use the BT scanner at the same time
                # Wait a moment and try again
                time.sleep(2)
        if not scan_successful:
            raise Exception(f"Unable to scan after 3 attempts")

        for dev in devices:
            found_covid = False
            dev_desc = "Device %s (%s), RSSI=%d dB\n" % (dev.addr, dev.addrType, dev.rssi)
            for (adtype, desc, value) in dev.getScanData():
                dev_desc += "  %s = %s [%s]\n" % (desc, value, adtype)
                if value == '0000fd6f-0000-1000-8000-00805f9b34fb': # COVID service ID
                    self.print("found")
                    found_covid = True
            if found_covid:
                self.print(dev_desc)
                return dev.rssi

        return None

    def standard_methodology(self):
        # Tries to connect to the device using normal bluetooth (not low energy)
        # rssi is very unstable, so pull it 10 times and take the average of the non-zero ones
        btrssi = BluetoothRSSI(self.addr.upper())
        rssis = []
        for i in range(10):
            rssis.append(btrssi.get_rssi())
            time.sleep(0.5)

        self.print(rssis)
        rssis_less_nones = list(filter(lambda x: x is not None, rssis))
        if len(rssis_less_nones) == 0:
            return None # device was out of range for all measurements

        rssis_filtered = list(filter(lambda x: x != 0, rssis_less_nones))
        if len(rssis_filtered) == 0:
            return 0 # Device is close, but can't find an exact rssi

        return round(sum(rssis_filtered) / len(rssis_filtered), 1)


class BluetoothRSSI(object):
    """Object class for getting the RSSI value of a Bluetooth address.
    Reference: https://github.com/dagar/bluetooth-proximity
    Also: https://www.cwnp.com/rssi-changing-definition/
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
        handle = struct.unpack("8xH14x", request.tobytes())[0]
        self.cmd_pkt = struct.pack('H', handle)

    def connect(self):
        """Connects to the Bluetooth address"""
        self.bt_sock.connect_ex((self.addr, 1))  # PSM 1 - Service Discovery
        self.connected = True

    def get_rssi(self):
        """Gets the current RSSI value.
        @return: The RSSI value (float) or None if the device connection fails
                 (i.e. the device is nowhere nearby).

        A positive number is "better than ideal range"
        0 is "in the ideal range"
        A negative number is "worse than ideal range"
        https://www.cwnp.com/rssi-changing-definition/
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


if __name__ == '__main__':
    a = BluetoothMonitor("18:4E:16:94:38:AF", debug=True)
    print(f"old = {a.old_methodology()}")
    print(f"COVID = {a.covid_methodology()}")
    print(f"standard = {a.standard_methodology()}")
