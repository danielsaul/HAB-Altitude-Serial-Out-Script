# Altitude Counter
# Count-up to next altitude
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
currentAltitude = 0

# Setup serial output
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

    #Get the altitude from Habitat
    currentAltitude = getAltitude()
    
    # Make the altitude always be 5 digits for outputting to serial
    # e.g. 60m -> 00060m    1340m -> 01340m
    try:
        extAltitude = '%0*d' % (5, currentAltitude)
    except:
        extAltitude = currentAltitude

    # If this is first iteration of loop, previous altitude will be 0, so set to currentAltitude
    # (We don't want to count up from 0 to an insanely high altitude if we start the program halfway through flight!)
    if prevAltitude == 0:
        prevAltitude = currentAltitude
        serout.write(bytes(qualifier))
        serout.write(bytes(extAltitude))

   
    if currentAltitude != prevAltitude:

        # Balloon is ascending: Countup from prevAltitude to currentAltitude
        while currentAltitude > prevAltitude:
            prevAltitude = prevAltitude + 1

            # Make the Altitude always be 5 digits
            try:
                printAlt = '%0*d' % (5, prevAltitude)
            except:
                printAlt = prevAltitude

            serout.write(bytes(qualifier))  # Output Qualifier
            serout.write(bytes(printAlt))   # Output 5 digit number
            print prevAltitude              # Print it to the screen too

            # Sleep a little before looping so the countup isn't instant
            time.sleep(0.05)

        # Balloon is descending: Count down from prevAltitude to currentAltitude
        while currentAltitude < prevAltitude:
            prevAltitude = prevAltitude - 1

            # Make the Altitude always be 5 digits
            try:
                printAlt = '%0*d' % (5, prevAltitude)
            except:
                printAlt = prevAltitude

            serout.write(bytes(qualifier))  # Output qualifier
            serout.write(bytes(printAlt))   # Output 5 digit number
            print prevAltitude              # Print it to the screen too

            # Sleep a little before looping so the count down isn't instant
            time.sleep(0.05)

        
        prevAltitude = currentAltitude

# End of Program Loop
