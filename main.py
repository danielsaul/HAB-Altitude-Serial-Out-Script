import json
import urllib2

#Get data from Habitat
data = urllib2.urlopen('http://habitat.habhub.org/habitat/_design/habitat/_view/payload_telemetry?startkey=[%22ALPHA%22,%22latest%22]&descending=true&limit=1&include_docs=true')
data = json.load(data)

data.close()
