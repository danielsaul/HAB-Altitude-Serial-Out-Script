import json
import urllib2
import serial

def getAltitude():
    #Get data from Habitat
    data = urllib2.urlopen('http://habitat.habhub.org/habitat/_design/habitat/_view/payload_telemetry?startkey=[%22ALPHA%22,%22latest%22]&descending=true&limit=1&include_docs=true')
    habitatdata = json.load(data)
    data.close()

    altitude = habitatdata['rows'][0]['doc']['data']['altitude']
    return altitude

currentAltitude = getAltitude()



