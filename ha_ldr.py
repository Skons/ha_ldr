"""
@ Authors     : Kevin Temming
@ Date        : 05-05-2019
@ Description : HA LDR - Get the LDR value into Home Assistant.

05-05-2019 - First version
"""

import RPi.GPIO as GPIO
import time
import sys
import logging
import requests
import argparse

#parse the arguments
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--pin', action='store', dest='pin', type=int, help="LDR GPIO data pin", default=11)
parser.add_argument('-m', '--max-value', action='store', dest='max', type=int, help="Max brightness value reported", default=2500)
parser.add_argument('-l', '--max-loop', action='store', dest='loop', type=int, help="Max number of loops, 0 for indefinate", default=1)
parser.add_argument('-u', '--url', action='store', dest='url', help="Url to post the value to, if not provided the output is console")
parser.add_argument('-s', '--sleep', action='store', dest='sleep', help="Number of seconds to wait for next brightness retreival", default=10)
parser.add_argument('-f', '--log-file', action='store', dest='logfile', help="Log file location")
parser.add_argument('-v', '--verbose', action='store_true', dest='verbose', help="Show verbose logging")
args = parser.parse_args()

#prepare logging stuff
if args.verbose:
    loglevel = logging.INFO
else: 
    loglevel = logging.ERROR

if args.logfile is not None:
    logging.basicConfig(filename=args.logfile,filemode='w',format='%(asctime)s %(name)s %(levelname)s %(message)s',datefmt='%H:%M:%S',level=loglevel)
else:
    logging.basicConfig(level=loglevel)

#show the provided parameters
logging.info('Pin          = %s',args.pin)
logging.info('Max          = %s',args.max)
logging.info('Max loop     = %s',args.loop)
logging.info('URL          = %s',args.url)
logging.info('Sleep        = %s',args.sleep)
logging.info('Logfile      = %s',args.logfile)

GPIO.setmode(GPIO.BOARD)

#https://pimylifeup.com/raspberry-pi-light-sensor/
def rc_time (pin_to_circuit,max_value):
    count = 0
  
    #Output on the pin for 
    GPIO.setup(pin_to_circuit, GPIO.OUT)
    GPIO.output(pin_to_circuit, GPIO.LOW)
    time.sleep(0.1)

    #Change the pin back to input
    GPIO.setup(pin_to_circuit, GPIO.IN)
  
    #Count until the pin goes high
    while (GPIO.input(pin_to_circuit) == GPIO.LOW):
        count += 1

    if max_value == 0:
        count = count
    elif max_value < count:
        count = max_value

    return count

def post_rc_time (url, value):
    headers = {'content-type': 'application/json'}
    payload = {"state":value}
    logging.info('JSON         = %s',payload)
    try:
        r = requests.post(url, json=payload)
        logging.info('Status Code  = %s',r.status_code)
        return r.status_code
    except requests.exceptions.RequestException as e:
        logging.error('%s', e)
        return ""

counter = 0 #counter for the while loop
logging.info('--- initialization done ---')
#Catch when script is interupted, cleanup correctly
try:
    # Main loop
    while (counter < args.loop or args.loop == 0):
        value = rc_time(args.pin,args.max)
        if args.url is not None: #if url is provided, post the data to HA
            response = post_rc_time(args.url,value)
            print(response)
        else: #print the response to the console
            print(value)
        counter += 1
        if args.loop is not counter: #sleep when the loop is not at the end
            time.sleep(args.sleep)
finally:
    GPIO.cleanup()
