import datetime
import time
from traceback import format_exc

import pytz


from bluepy.btle import Scanner
from sense_monitor.sense_api import SenseApi
from sense_monitor.shared_data import PolledData, SHARED_DATA

EPT = pytz.timezone('US/Eastern')



def poll_sense_data():

    # Pull sense data
    sense = SenseApi()
    sense.authenticate()
    heater = sense.get_device_info('08a647f2')
    heater_ts = datetime.datetime.strptime(heater['device']['last_state_time'], '%Y-%m-%dT%H:%M:%S.000Z')

    # Pull bluetooth data
    scanner = Scanner()
    devices = scanner.scan(3)

    phone_present = False
    for d in devices:
        print(d.addr, d.rssi)
        if d.addr == '73:4a:76:d9:5f:7f':
            phone_present = True
    print('*'*20)

    ppt = SHARED_DATA.history[-1].phone_present_time
    if phone_present != SHARED_DATA.history[-1].phone_present:
        ppt = datetime.datetime.now()



    data = PolledData(
        timestamp=datetime.datetime.now(),
        heater_state=heater['device']['last_state'],
        heater_state_time=pytz.utc.localize(heater_ts).astimezone(EPT),
        phone_present=phone_present,
        phone_present_time=ppt
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
        time.sleep(60)