import requests
from pprint import pprint
import pytz
import datetime

API_URL = 'https://api.sense.com/apiservice/api/v1/'


class SenseApi(object):
    def __init__(self):
        self.s = requests.Session()

        self.api_timeout = 5

        self.sense_access_token = ''
        self.sense_user_id = -1
        self.sense_monitor_id = -1
        self.headers = {}



    def authenticate(self):
        auth_data = {
            "email": "GenericCarbonLifeform@gmail.com",
            "password": open("pw.txt").read().strip()
        }

        # Create session
        self.s = requests.session()

        # Get auth token
        try:
            response = self.s.post(API_URL + 'authenticate',
                                   auth_data, timeout=self.api_timeout)
        except Exception as e:
            raise Exception('Connection failure: %s' % e)

        # check for 200 return
        if response.status_code != 200:
            raise Exception(
                "Please check username and password. API Return Code: %s" %
                response.status_code)

        data = response.json()

        self.sense_access_token = data['access_token']
        self.sense_user_id = data['user_id']
        self.sense_monitor_id = data['monitors'][0]['id']

        # create the auth header
        self.headers = {'Authorization': 'bearer {}'.format(
            self.sense_access_token)}

    def api_call(self, url, payload={}):
        return self.s.get(API_URL + url,
                          headers=self.headers,
                          timeout=self.api_timeout,
                          data=payload).json()


    def get_device_info(self, device_id):
        # Get specific informaton about a device
        return self.api_call('app/monitors/%s/devices/%s' %
                             (self.sense_monitor_id, device_id))

    def get_discovered_device_data(self):
        return self.api_call('monitors/%s/devices' %
                             self.sense_monitor_id)

if __name__ == '__main__':
    sense = SenseApi()
    sense.authenticate()
    pprint(sense.get_device_info('08a647f2')) # heater
    data = sense.get_device_info('f0f75587') # fridge
    ts = data['device']['last_state_time']
    ts = datetime.datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S.000Z')
    print(ts)
    eastern = pytz.timezone('US/Eastern')
    print(data['device']['name'])
    print(data['device']['last_state_time'])
    print(ts)
    print(pytz.utc.localize(ts).astimezone(eastern))


    #for d in sense.get_discovered_device_data():
    #    pprint((d['name'], d['id']))
    #    print('*'*30)