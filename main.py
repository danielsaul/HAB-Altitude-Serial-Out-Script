# Altitude Counter
# Just change to next altitude
# Daniel Saul

import json
import urllib2
import serial
import time

# Configuration #
port = 'COM6'           # Serial port to output data to
baud = 76800            # Baud rate to output data at
qualifier = "hello"     # Qualifier to output before data
payload = "ALPHA"       # Balloon callsign to get altitude for

prevAltitude = 0

#Setup serial output
serout = serial.Serial(port,baud,timeout=2,writeTimeout=2)

# Function: Get the altitude from Habitat
def getAltitude():

    #Get data from Habitat
    try:
        data = urllib2.urlopen('http://habitat.habhub.org/habitat/_design/habitat/_view/payload_telemetry?startkey=[%22{0}%22,%22latest%22]&descending=true&limit=1&include_docs=true'.format(payload))
    except: 
        return prevAltitude
    
    habitatdata = json.load(data)
    data.close()

    # Get altitude from the Habitat Data
    try:
        altitude = habitatdata['rows'][0]['doc']['data']['altitude']
    except:
        return prevAltitude

    return altitude

# Program loop
while True:

    # Get the altitude from Habitat
    currentAltitude = getAltitude()

    # Make the altitude always be 5 digits for outputting to serial
    # e.g. 60m -> 00060m    1340m -> 01340m
    try:
        currentAltitude = '%0*d' % (5, currentAltitude)
    except:
        currentAltitude = prevAltitude

    
    if currentAltitude != prevAltitude:
        serout.write(bytes(qualifier))          # Output the Qualifier
        serout.write(bytes(currentAltitude))    # Output 5digit Altitude
        print currentAltitude                   # Print Altitude to screen
        prevAltitude = currentAltitude  
# End of Program loop

