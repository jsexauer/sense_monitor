import datetime
import pytz
import time
from flask import Flask
from threading import Thread
from sense_api import SenseApi
server = Flask(__name__)

EPT = pytz.timezone('US/Eastern')

class SenseData:
    def __init__(self):
        self.updated = datetime.datetime.now()
        self.heater_state = False
        self.heater_state_time = datetime.datetime(2000, 1, 1)
SENSE_DATA = SenseData()

def poll_sense_data():
    while True:
        sense = SenseApi()
        sense.authenticate()

        heater = sense.get_device_info('08a647f2')
        ts = datetime.datetime.strptime(heater['device']['last_state_time'], '%Y-%m-%dT%H:%M:%S.000Z')
        SENSE_DATA.updated = datetime.datetime.now()
        SENSE_DATA.heater_state_time = pytz.utc.localize(ts).astimezone(EPT)
        SENSE_DATA.heater_state = heater['device']['last_state']

        time.sleep(60)

@server.route("/")
def hello():
    return f"""
    <p>Heater: {SENSE_DATA.heater_state}</p>
    <p>Heater last on: {SENSE_DATA.heater_state_time}</p>
    <p>Updated: {SENSE_DATA.updated}</p>
    """


if __name__ == "__main__":
    t = Thread(target=poll_sense_data)
    t.start()
    server.run(host='0.0.0.0', port=5005)
