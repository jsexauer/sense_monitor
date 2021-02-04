import datetime
import pytz
from typing import *
from collections import deque
from dataclasses import dataclass

@dataclass
class PolledData:
    timestamp: datetime.datetime
    heater_state: str
    heater_state_time: datetime.datetime
    phone_present: bool
    phone_present_time: datetime.datetime

class _SharedData:
    def __init__(self):
        self.history: Deque[PolledData] = deque(maxlen=10)
        self.last_error = ''

        self.history.append(PolledData(
            timestamp=datetime.datetime.now(),
            heater_state='???',
            heater_state_time=pytz.utc.localize(datetime.datetime(2000,1,1)),
            phone_present=False,
            phone_present_time=datetime.datetime(2000,1,1)
        ))

SHARED_DATA = _SharedData()