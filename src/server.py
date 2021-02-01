from flask import Flask
from sense_energy import Senseable
server = Flask(__name__)

@server.route("/")
 def hello():
    return "Hello World!"
	
@server.route("/sense")
def sense():
	pw = open('pw.txt').read().strip()
	assert pw != 'todo', "Set the password"
	
    sense.authenticate("GenericCarbonLifeform@gmail.com", pw)
	sense.update_realtime()
	sense.update_trend_data()
	return "Active Devices: " + ", ".join(sense.active_devices)

if __name__ == "__main__":
   print(" *!*!*!* About to start server!!!")
   server.run(host='0.0.0.0')