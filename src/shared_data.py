import datetime
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

SHARED_DATA = _SharedData()