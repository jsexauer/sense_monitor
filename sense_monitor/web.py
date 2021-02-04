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
    html = f"""
    <h3>Current Status</h3>
    {x.html}

    <h3>Errors:</h3>
    <pre>{SHARED_DATA.last_error}</pre>

    <h3>Last 5 minutes:</h3>
    <table border=0 >
    <tr>
    """

    for x in reversed(SHARED_DATA):
        html += f"<td>{x.html}</td>"

    html += "</tr></table>"

    return html


def run_webserver():
    from sense_monitor.poll_worker import thread_worker
    t = Thread(target=thread_worker)
    t.start()
    server.run(host='0.0.0.0', port=5005)    


if __name__ == "__main__":
    run_webserver()