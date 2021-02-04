import datetime
import time
from traceback import format_exc

import pytz


from bluepy.btle import Scanner, DefaultDelegate
from sense_monitor.sense_api import SenseApi
from sense_monitor.shared_data import PolledData, SHARED_DATA
from sense_monitor.emaillib import send_email

EPT = pytz.timezone('US/Eastern')

def poll_sense_data():

    # Pull sense data
    sense = SenseApi()
    sense.authenticate()
    heater = sense.get_device_info('08a647f2')
    heater_ts = datetime.datetime.strptime(heater['device']['last_state_time'], '%Y-%m-%dT%H:%M:%S.000Z')

    # Pull bluetooth data
    scanner = Scanner()
    devices = scanner.scan(5.0)

    phone_present = False
    phone_rssi = 0
    for d in devices:
        print(d.addr, d.rssi)
        if d.addr == '18:4e:16:94:38:af':
            phone_present = True
            phone_rssi = d.rssi
    print('*'*20)

    ppt = SHARED_DATA.history[-1].phone_present_time
    if phone_present != SHARED_DATA.history[-1].phone_present:
        ppt = datetime.datetime.now()


    # Update shared data
    data = PolledData(
        timestamp=datetime.datetime.now(),
        heater_state=heater['device']['last_state'],
        heater_state_time=pytz.utc.localize(heater_ts).astimezone(EPT),
        phone_present=phone_present,
        phone_present_time=ppt,
        phone_rssi=phone_rssi
    )

    SHARED_DATA.history.append(data)



def thread_worker():
    while True:
        try:
            poll_sense_data()
        except Exception as ex:
            SHARED_DATA.last_error = f"At datetime.datetime.now():\n" + format_exc()
        else:
            SHARED_DATA.last_error = ''
        time.sleep(6)