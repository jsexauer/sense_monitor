import bluetooth
import datetime
import time

addr = "18:4E:16:94:38:AF"

while True:
  if len(bluetooth.find_service(address=addr)) > 0:
    print(f"{datetime.datetime.now()} - device exists!")
  else:
    print(f"{datetime.datetime.now()} - device out of range!")
    time.sleep(30)


