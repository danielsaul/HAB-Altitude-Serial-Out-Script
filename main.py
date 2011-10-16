#Daniel Saul

import json
import urllib2
import serial
import time

port = '\\\.\CNCA0'
baud = 19200
qualifier = "HELLO"
payload = "BUZZ"
prevAltitude = 0

serout = serial.Serial(port,baud,timeout=2,writeTimeout=2)


def getAltitude():
    #Get data from Habitat
    try:
        data = urllib2.urlopen('http://habitat.habhub.org/habitat/_design/habitat/_view/payload_telemetry?startkey=[%22{0}%22,%22latest%22]&descending=true&limit=1&include_docs=true'.format(payload))
    except: return prevAltitude
    habitatdata = json.load(data)
    data.close()

    try:
        altitude = habitatdata['rows'][0]['doc']['data']['altitude']
    except: return prevAltitude

    if isinstance(altitude, str) == True:
        return prevAltitude
    else:
        return altitude


while True:
    currentAltitude = getAltitude()
    currentAltitude = '%0*d' % (5, currentAltitude)
    if currentAltitude != prevAltitude:
        serout.write(bytes(qualifier))
        serout.write(bytes(currentAltitude))
        print currentAltitude
        prevAltitude = currentAltitude
raw_input("Press ENTER to exit")
