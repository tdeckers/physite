from googleapiclient.errors import HttpError
from googleapiclient import sample_tools
from oauth2client.client import AccessTokenRefreshError
from neopixel import *

import sys
import argparse
import os
import json

# LED strip configuration:
LED_COUNT      = 60      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 40     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

SCALE = 4

def getAnalytics(argv):
	# Authenticate and construct service.
	service, flags = sample_tools.init(
		argv, 'analytics', 'v3', __doc__, __file__,
		scope='https://www.googleapis.com/auth/analytics.readonly')
#	accounts = service.management().accounts().list().execute()
#	print json.dumps(accounts, indent=4)
#	accountId = 58214767
#	webproperties = service.management().webproperties().list(
#			        accountId=accountId).execute()
#	print json.dumps(webproperties, indent=4)
#	webpropertyId = 'UA-58214767-1'
#	profiles = service.management().profiles().list(
#		accountId=accountId,
#		webPropertyId=webpropertyId).execute()
#	print json.dumps(profiles, indent=4)

        # Hardcode this for now.
	profileId = '95874974'
	data = service.data().ga().get(
		ids='ga:' + profileId,
#		start_date='2015-01-18',
                start_date='7daysAgo',
#		end_date='2015-01-25',
                end_date='today',
                metrics='ga:sessions, ga:percentNewSessions',
#		dimensions='ga:source,ga:keyword',
		sort='-ga:sessions',
#		filters='ga:medium==organic',
		start_index='1',
		max_results='25').execute()
        print json.dumps(data, indent=4)
        sessions = int(data['rows'][0][0])
        new_sessions = float(data['rows'][0][1])
        print sessions
        print new_sessions
        return (sessions, new_sessions)

def display(scale, sessions, newsessions):
        strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
        # Intialize the library (must be called once before other functions).
        strip.begin()

        s_sessions = int(sessions / scale)
        if (s_sessions > 60):
                s_sessions = 60
        s_newsessions = int(s_sessions * newsessions / 100)
        print "Sessions: %d, new: %d" % (s_sessions, s_newsessions)
        for i in range(strip.numPixels()):
                if (i <= s_newsessions):
                        color = Color(0,0,127)
                elif (i <= s_sessions):
                        color = Color(127,127,127)
                else:
                        color = Color(0,0,0)
                strip.setPixelColor(i, color)
        strip.show() 

def main(argv):
        sessions, new_sessions = getAnalytics(argv)
        display(SCALE, sessions, new_sessions)

if __name__ == "__main__":
	main(sys.argv)

