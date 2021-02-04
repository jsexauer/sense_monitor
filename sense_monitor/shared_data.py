import datetime
import pytz
from typing import *
from collections import deque
from dataclasses import dataclass

EPT = pytz.timezone('US/Eastern')

@dataclass
class PolledData:
    timestamp: datetime.datetime
    heater_state: str
    heater_state_time: datetime.datetime
    phone_present: bool
    phone_present_time: datetime.datetime
    phone_rssi: float

    @property
    def html(self):
        x = self
        return f"""
            <p>Heater: {x.heater_state}</p>
            <p>Heater last state change: {EPT.localize(datetime.datetime.now()) - x.heater_state_time} at {x.heater_state_time}</p>
            <p>Phone present: {x.phone_present}</p>
            <p>Phone last state chagne: {datetime.datetime.now() - x.phone_present_time} at {x.phone_present_time}</p>
            <p>Updated: {x.timestamp}</p>
            """

class _SharedData:
    def __init__(self):
        self.history: Deque[PolledData] = deque(maxlen=5)
        self.last_error = ''

        self.history.append(PolledData(
            timestamp=datetime.datetime.now(),
            heater_state='???',
            heater_state_time=pytz.utc.localize(datetime.datetime(2000,1,1)),
            phone_present=False,
            phone_present_time=datetime.datetime(2000,1,1),
            phone_rssi=0,
        ))

SHARED_DATA = _SharedData()