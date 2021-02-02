import datetime
import pytz
from flask import Flask
from threading import Thread
from sense_monitor.shared_data import SHARED_DATA

EPT = pytz.timezone('US/Eastern')

server = Flask(__name__)


@server.route("/")
def hello():
    x = SHARED_DATA.history[-1]
    return f"""
    <h3>Current Status</h3>
    <p>Heater: {x.heater_state}</p>
    <p>Heater last state change: {EPT.localize(datetime.datetime.now()) - x.heater_state_time} at {x.heater_state_time}</p>
    <p>Phone present: {x.phone_present}</p>
    <p>Phone last state chagne: {datetime.datetime.now() - x.phone_present_time} at {x.phone_present_time}</p>
    <p>Updated: {x.timestamp}</p>

    <h3>Errors:</h3>
    <pre>{SHARED_DATA.last_error}</pre>
    """


def run_webserver():
    from sense_monitor.poll_worker import thread_worker
    t = Thread(target=thread_worker)
    t.start()
    server.run(host='0.0.0.0', port=5005)    


if __name__ == "__main__":
    run_webserver()