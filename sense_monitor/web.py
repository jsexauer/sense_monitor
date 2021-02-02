import datetime
from flask import Flask
from threading import Thread
from sense_monitor.shared_data import SHARED_DATA

server = Flask(__name__)
@server.route("/")
def hello():
    x = SHARED_DATA.history[-1]
    return f"""
    <h3>Current Status</h3>
    <p>Heater: {x.heater_state}</p>
    <p>Heater last state change: {datetime.datetime.now() - x.heater_state_time} at {x.heater_state_time}</p>
    <p>Phone present: {x.phone_present}</p>
    <p>Phone last state chagne: {datetime.datetime.now() - x.phone_present_time} at {x.phone_present_time}</p>
    <p>Updated: {x.timestamp}</p>

    <h3>Errors:</h3>
    <pre>{SHARED_DATA.last_error}</pre>
    """


if __name__ == "__main__":
    from sense_monitor.poll_worker import thread_worker
    t = Thread(target=thread_worker)
    t.start()
    server.run(host='0.0.0.0', port=5005)
