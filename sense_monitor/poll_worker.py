import datetime
import time
from traceback import format_exc

import pytz


from bluepy.btle import Scanner, DefaultDelegate
from sense_monitor.sense_api import SenseApi
from sense_monitor.shared_data import PolledData, SHARED_DATA
from sense_monitor.emaillib import send_email
from sense_monitor.secret import PHONE_EMAIL_ADDR

EPT = pytz.timezone('US/Eastern')

def poll_sense_data():
    print('*'*40)
    print(datetime.datetime.now())

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

    # See if we should send a warning email.  Heater has been on, but phone has not been present.  Only notify
    #  once an hour
    print(datetime.datetime.now() - SHARED_DATA.last_notify > datetime.timedelta(hours=1),
          all([d.heater_state == 'On' for d in SHARED_DATA.history]),
          all([d.phone_present == False for d in SHARED_DATA.history]))
    if (datetime.datetime.now() - SHARED_DATA.last_notify > datetime.timedelta(hours=1) and
              all([d.heater_state == 'On' for d in SHARED_DATA.history]) and
              all([d.phone_present == False for d in SHARED_DATA.history])):
        print(f"*** SENDING NOTICE TEXT at {datetime.datetime.now()} ***")
        send_email(
            send_to=PHONE_EMAIL_ADDR,
            subject="Heater left on",
            body="http://rpi:5005"
        )
        SHARED_DATA.last_notify = datetime.datetime.now()



def thread_worker():
    while True:
        try:
            poll_sense_data()
        except Exception as ex:
            SHARED_DATA.last_error = f"At {datetime.datetime.now()}:\n" + format_exc()
        time.sleep(60)