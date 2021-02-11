import datetime
import pytz
from typing import *
from collections import deque
from dataclasses import dataclass

EPT = pytz.timezone('US/Eastern')


def td_format(td_object):
    seconds = int(td_object.total_seconds())
    periods = [
        ('year',        60*60*24*365),
        ('month',       60*60*24*30),
        ('day',         60*60*24),
        ('hr',        60*60),
        ('min',      60),
        ('sec',      1)
    ]

    strings=[]
    for period_name, period_seconds in periods:
        if seconds > period_seconds:
            period_value , seconds = divmod(seconds, period_seconds)
            has_s = 's' if period_value > 1 else ''
            strings.append("%s %s%s" % (period_value, period_name, has_s))

    return ", ".join(strings)


@dataclass
class PolledData:
    timestamp: datetime.datetime
    heater_state: str
    heater_state_time: datetime.datetime
    phone_present_time: datetime.datetime
    phone_rssi_covid: Optional[float]
    phone_rssi_std: Optional[float]

    @property
    def html(self):
        x = self
        return f"""
            <p>Heater: {x.heater_state}</p>
            <p>Heater changed: {td_format(EPT.localize(datetime.datetime.now()) - x.heater_state_time)} ago at {x.heater_state_time: %H:%M}</p>
            <p>Phone present: {x.phone_present} at {x.phone_rssi_covid} dB BLE and {x.phone_rssi_std} dB BL</p>
            <p>Phone changed: {td_format(datetime.datetime.now() - x.phone_present_time)} ago at {x.phone_present_time: %H:%M}</p>
            <p>Recorded at: {td_format(datetime.datetime.now() - x.timestamp)} ago at {x.timestamp:: %H:%M}</p>
            """

    @property
    def phone_present(self):
        if self.phone_rssi_std is None and self.phone_rssi_covid is None:
            # Found on neither BT scan
            return False
        if self.phone_rssi_covid is None and self.phone_rssi_std < 0:
            # Out of BLE range and outside the "golden range" for BT
            return False
        return True


class _SharedData:
    def __init__(self):
        self.history: Deque[PolledData] = deque(maxlen=5)
        self.last_error = ''
        self.last_notify = datetime.datetime(2000, 1, 1)

        self.history.append(PolledData(
            timestamp=datetime.datetime.now(),
            heater_state='???',
            heater_state_time=pytz.utc.localize(datetime.datetime(2000,1,1)),
            phone_present_time=datetime.datetime(2000,1,1),
            phone_rssi_covid=None,
            phone_rssi_std=None
        ))

SHARED_DATA = _SharedData()